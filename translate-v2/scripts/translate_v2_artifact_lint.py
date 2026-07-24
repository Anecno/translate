#!/usr/bin/env python3
"""Lint public translate-v2 Markdown artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from translate_v2_common import (
    flat_scores_missing,
    has_any,
    has_layered_scores,
    na_without_reason_missing,
    non_code_lines,
    three_layer_score_block_missing,
)


ARTIFACT_TYPES = {
    "prompt-package",
    "baton-raw",
    "round-archive",
    "checkpoint",
    "divergence-report",
    "final-report",
}


def missing_required(text: str, checks: list[tuple[str, list[str]]]) -> list[str]:
    return [name for name, needles in checks if not has_any(text, needles)]


# --- Member-aware relay safeguards: first-baton dictionary + fifth-baton web-access ---
# The reference relay chain hands a translation across five models in series. The
# first baton looks up the target-language dictionary before rendering; the fifth
# baton runs web-access research into the source- and target-language sites that
# other models cannot easily reach (README notes 2 and 4). These two safeguards
# keep the dictionary and web-access steps visible and enforceable. The member
# names below are this workflow's aliases — adapt them to your own lineup. Both
# checks fire only when an artifact actually targets the relevant baton, so a
# lineup that renames or drops these members simply stops triggering them.
RELAY_MEMBERS = ["哈基米", "哈士奇", "Qoder", "逗比", "小D", "小克", "小G", "Codex", "包子", "老D", "CC"]
FIRST_BATON_MEMBERS = ["哈士奇", "哈基米"]
FIFTH_BATON_MEMBERS = ["Qoder", "逗比"]
FIFTH_BATON_CHAINS = [
    "哈士奇 -> 小D -> 小克 -> Codex -> Qoder",
    "哈士奇→小D→小克→Codex→Qoder",
    "哈士奇 -> 小D -> 小克 -> Codex -> 逗比",
    "哈士奇→小D→小克→Codex→逗比",
    "哈基米 -> 小D -> 小克 -> 小G -> Qoder",
    "哈基米→小D→小克→小G→Qoder",
]


def detect_target_member(text: str) -> str | None:
    """Best-effort read of the artifact's target member from its title or header block.

    Raw-capture drops conventionally lead with a provenance line (such as
    ``captured_utc:``) and carry the identity line (``member:`` / a ``raw ...:`` label)
    a few lines below, so a first-line-only read would miss it and mis-fire the
    fifth-baton contract on a non-fifth self-filed drop. When the first line yields
    nothing, scan the header block — up to the first blank line, capped — for an
    explicit identity field. Only the metadata block is scanned, never the body, so an
    N-1/N-2 citation in prose is not mistaken for the target member.
    """
    stripped = text.strip()
    if not stripped:
        return None
    lines = stripped.splitlines()
    first = lines[0]
    match = re.search(r"(?:prompt|baton-raw|baton)\s*[—\-·:]\s*([^/·\n]{1,24})", first, re.IGNORECASE)
    segment = (match.group(1) if match else first[:64]).lower()
    for member in RELAY_MEMBERS:
        if member.lower() in segment:
            return member
    for line in lines[1:12]:
        if not line.strip():
            break
        field = re.match(r"\s*(?:member|成员|raw[\s\w]{0,8})\s*[:：]\s*([^/·\n]{1,24})", line, re.IGNORECASE)
        if field:
            segment = field.group(1).lower()
            for member in RELAY_MEMBERS:
                if member.lower() in segment:
                    return member
    return None


def first_baton_dictionary_missing(text: str) -> list[str]:
    """Require first-baton prompts to carry the target-language dictionary contract.

    The first baton specializes in target-language dictionary lookup — through a
    local dictionary library, or a target-language NotebookLM notebook when that
    is the first baton. Adapt the member names / dictionary route to your setup.
    """
    if detect_target_member(text) not in FIRST_BATON_MEMBERS:
        return []
    missing: list[str] = []
    if not has_any(
        text,
        ["target-language dictionary", "target language dictionary", "目标语词典", "目标语言词典", "目标语种词典"],
    ):
        missing.append("prompt:first-baton-target-language-dictionary-missing")
    if not has_any(text, ["local dictionary library", "本地词典库", "notebooklm", "dictionary", "词典"]):
        missing.append("prompt:first-baton-dictionary-route-missing")
    if not has_any(text, ["priority", "mandatory", "must", "优先", "必查", "每一处"]):
        missing.append("prompt:first-baton-dictionary-mandatory-missing")
    if not (
        has_any(text, ["does not answer", "cannot find", "not found", "查不到", "找不到"])
        and has_any(text, ["web search", "ordinary search", "联网搜索", "普通搜索"])
    ):
        missing.append("prompt:first-baton-web-search-fallback-missing")
    # The source-language dictionary is NOT restricted. The first baton may freely consult
    # source-language / bilingual dictionaries and the web; flag prompts that wrongly forbid
    # or "do not substitute" it. (An earlier revision required such an anti-rule to be present,
    # which was itself the misreading being corrected here.)
    if has_any(
        text,
        [
            "do not substitute the source-language dictionary",
            "do not use the source-language dictionary",
            "不得查源语词典",
            "不要查源语词典",
            "不许查源语词典",
            "禁止查源语词典",
            "不得用源语词典替代",
        ],
    ):
        missing.append("prompt:first-baton-source-language-dictionary-restriction-forbidden")
    if not (
        has_any(
            text,
            ["list all", "list every lookup", "complete lookup log", "dictionary check record",
             "逐项", "列全", "全量", "词典检查记录"],
        )
        and has_any(text, ["not_found", "not found", "cannot_verify", "查不到"])
    ):
        missing.append("prompt:first-baton-no-lazy-full-lookup-log-missing")
    return missing


def relay_n2_full_block_missing(text: str) -> list[str]:
    """Require a declared N-2 window to carry the full previous-baton translation.

    The N-1/N-2 label check only verifies that the labels appear. A prompt that assigns an
    N-2 baton (``N-2 = ...``) must also include that baton's full translation block, not a
    one-line "same as ..." reference, so the next baton can actually evaluate it.
    """
    if not re.search(r"n-?2\s*[＝=]", text, re.IGNORECASE):
        return []
    if not re.search(
        r"n-?2[^\n]{0,40}(full translation|complete translation|完整译文|完整候选)",
        text,
        re.IGNORECASE,
    ):
        return ["prompt:relay-n2-full-translation-block-missing"]
    return []


def fifth_baton_web_access_missing(text: str, prefix: str) -> list[str]:
    """Require the fifth baton (web-access baton) to run and fully report research.

    The fifth baton is equipped with web access and digs into source- and
    target-language sites, including hard-to-reach real-user/social platforms,
    that other models cannot easily reach. The fifth baton may be any of the
    FIFTH_BATON_MEMBERS; the contract is identical whichever one is dispatched.
    Adapt the member names to your setup.
    """
    member = detect_target_member(text)
    # A prompt/raw is one member's artifact; a non-fifth target only cites the
    # fifth baton as N-1/N-2 context and is not bound by this contract.
    if prefix in ("prompt", "baton-raw") and member is not None and member not in FIFTH_BATON_MEMBERS:
        return []
    member_is_fifth = member in FIFTH_BATON_MEMBERS
    fifth_context = has_any(text, ["Qoder", "逗比"]) and has_any(
        text, ["fifth baton", "5th baton", "第五棒", "final web-access baton", "R1B5", "R2B5"]
    )
    chain_context = has_any(text, FIFTH_BATON_CHAINS)
    if not (member_is_fifth or fifth_context or chain_context):
        return []

    missing: list[str] = []
    if prefix == "baton-raw":
        # The raw is the fifth baton's answer: judge whether research actually
        # happened, not whether it restated the instruction wording.
        url_count = len(re.findall(r"https?://", text))
        has_research_log = has_any(
            text, ["research log", "检索记录", "研究记录", "web-access", "web access", "web search"]
        )
        if url_count < 3 and not has_research_log:
            missing.append("baton-raw:fifth-baton-web-access-evidence-missing")
        if not has_any(
            text,
            ["小红书", "小紅書", "social platform", "real-user", "reddit", "twitter", "x.com",
             "weibo", "微博", "知乎", "pixiv", "note.com", "掲示板", "bbs", "quora"],
        ):
            missing.append("baton-raw:fifth-baton-hard-to-access-platforms-missing")
        if not has_any(text, ["not_found", "not found", "cannot_verify", "查不到", "无法核验"]):
            missing.append("baton-raw:fifth-baton-not-found-cannot-verify-marker-missing")
        if url_count < 3 and not has_any(
            text, ["url", "source note", "evidence", "来源", "证据", "检索记录", "research log"]
        ):
            missing.append("baton-raw:fifth-baton-source-evidence-log-missing")
        return missing

    if not has_any(text, ["web-access", "web access"]):
        missing.append(f"{prefix}:fifth-baton-web-access-required-missing")
    if not (
        has_any(text, ["source-language", "source language", "源文语种", "原文语种"])
        and has_any(text, ["target-language", "target language", "目标语种", "目标语"])
    ):
        missing.append(f"{prefix}:fifth-baton-source-and-target-language-search-missing")
    if not has_any(
        text, ["hard-to-reach", "hard to reach", "小红书", "social platform", "real-user", "不好上的网站"]
    ):
        missing.append(f"{prefix}:fifth-baton-hard-to-access-platforms-missing")
    if not (
        has_any(text, ["comprehensive", "every disputed", "all disputed", "逐项", "全量", "查全"])
        and has_any(text, ["list all", "full research log", "complete record", "列全", "写全", "完整记录"])
    ):
        missing.append(f"{prefix}:fifth-baton-no-lazy-full-search-and-report-missing")
    if not has_any(text, ["not_found", "not found", "cannot_verify", "查不到", "无法核验"]):
        missing.append(f"{prefix}:fifth-baton-not-found-cannot-verify-marker-missing")
    return missing


# The workflow can be linked to a companion fiction project (here: Antique Game
# Within Game / 《古董局中局》). This is the *general* linkage safeguard only — the
# project-boundary rule that any linked task must satisfy. Task-specific gates
# (a particular chapter, character, cover-title, or line-by-line pass) are NOT
# part of the public skill; keep those in your own private setup. Adapt the
# project name to your own linked project.
ANTIQUE_GAME_MARKERS = ["《古董局中局》", "Antique Game Within Game", "Antique Game"]


def antique_game_linkage_missing(text: str) -> list[str]:
    """When a prompt is for a linked companion-project (Antique Game Within Game)
    translation, require the general linkage safeguards: local-access members are
    given the manuscript and knowledge-base roots to read for story context, and
    a source-boundary rule keeps that project context out of the translation
    itself (background for understanding, never extra source text)."""
    if not has_any(text, ANTIQUE_GAME_MARKERS):
        return []
    missing: list[str] = []
    if not (
        has_any(text, ["manuscript", "chapter directory", "chapters", "稿件", "写作区", "手稿"])
        and has_any(text, ["knowledge base", "knowledge-base", "references", "知识库", "kb root"])
    ):
        missing.append("prompt:antique-linkage-project-roots-missing")
    if not has_any(
        text,
        ["source-boundary", "source boundary", "not source text", "not extra source",
         "background for understanding", "背景理解", "不得倒灌", "背景，不是"],
    ):
        missing.append("prompt:antique-linkage-source-boundary-missing")
    return missing


def english_only_surface_missing(text: str, prefix: str) -> list[str]:
    missing: list[str] = []
    for line_no, line in non_code_lines(text):
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if len(heading.split()) >= 2 and heading.isascii() and not any(ch.isdigit() for ch in heading):
                # Public artifacts may use English, but this catches placeholder-only
                # headings that usually indicate an unlocalized template leak.
                if heading.lower() in {"prompt package", "raw capture", "final report"}:
                    missing.append(f"{prefix}:placeholder-heading:L{line_no}")
    return missing


def syntax_morphology_missing(text: str, prefix: str) -> list[str]:
    # Full syntax/word-formation analysis for every source line: the rendered
    # sentence, an approximate literal gloss, the dependency/root structure, the
    # lexical morphology, the explicit source anchor, and a direct-vs-converted
    # audit. Needles carry both the English and Chinese-main phrasings so the
    # depth check works on real Chinese-main artifacts, not just English samples.
    checks = [
        (f"{prefix}:syntax-sentence-overview", ["sentence overview", "sentence rendering", "译句", "逐句"]),
        (f"{prefix}:syntax-approximate-literal", ["approximate literal", "literal meaning", "literal gloss", "近似直译"]),
        (f"{prefix}:syntax-phrase-breakdown", ["phrase breakdown", "逐短语", "particle", "honorific", "助词", "敬语"]),
        (f"{prefix}:syntax-dependency", ["dependency", "root", "modifiers", "依存", "source_alignment"]),
        (f"{prefix}:syntax-lexical-morphology", ["lemma", "morphology", "构词", "词形", "形态"]),
        (f"{prefix}:syntax-source-anchor", ["source anchor", "source alignment", "源文锚点", "锚点"]),
        (f"{prefix}:syntax-strategy-tags", ["translation strategy", "strategy tag", "翻译策略", "策略标记"]),
        (
            f"{prefix}:syntax-redline-audit",
            [
                "addition",
                "omission",
                "mistranslation",
                "hallucination",
                "free rewriting",
                "直译",
                "转换",
                "信息密度",
            ],
        ),
    ]
    return missing_required(text, checks)


def prompt_package_missing(text: str) -> list[str]:
    checks = [
        ("prompt:baton-context", ["n-1", "n-2", "previous baton", "上一棒", "上两棒"]),
        ("prompt:principles-first", ["translation principles", "principles first", "翻译原则", "原则前置"]),
        ("prompt:layered-scoring", ["scores.language", "scores.literary", "scores.cultural", "aggregate"]),
        ("prompt:raw-capture", ["raw capture", "full output", "raw 落档", "完整输出"]),
        ("prompt:round-archive", ["round archive", "round summary", "轮末合并", "合并落档"]),
        ("prompt:checkpoint", ["checkpoint", "wait for user", "等待用户", "停下来"]),
        ("prompt:final-output-confirmation", ["final output", "user confirmation", "最终产出", "用户确认"]),
    ]
    missing = missing_required(text, checks)
    missing.extend(three_layer_score_block_missing(text))
    missing.extend(flat_scores_missing(text, "prompt:"))
    missing.extend(na_without_reason_missing(text, "prompt:"))
    missing.extend(english_only_surface_missing(text, "prompt"))
    missing.extend(first_baton_dictionary_missing(text))
    missing.extend(relay_n2_full_block_missing(text))
    missing.extend(fifth_baton_web_access_missing(text, "prompt"))
    missing.extend(antique_game_linkage_missing(text))
    return missing


def baton_raw_missing(text: str) -> list[str]:
    checks = [
        ("baton:source-surface", ["source surface", "captured from", "源文表层", "捕获自"]),
        ("baton:relay-stage", ["relay stage", "baton", "棒次", "接力"]),
        ("baton:full-output", ["full output", "完整输出"]),
        ("baton:candidate", ["candidate translation", "candidate", "候选", "译文候选"]),
        ("baton:review", ["review", "reason", "审查", "修订理由"]),
        ("baton:convergence", ["convergence", "satisfaction", "收敛", "满意度"]),
    ]
    missing = missing_required(text, checks)
    missing.extend(flat_scores_missing(text, "baton:"))
    missing.extend(na_without_reason_missing(text, "baton:"))
    missing.extend(english_only_surface_missing(text, "baton"))
    missing.extend(fifth_baton_web_access_missing(text, "baton-raw"))
    return missing


def round_archive_missing(text: str) -> list[str]:
    checks = [
        ("round:metadata", ["round", "source language", "target language", "本轮", "源语", "目标语"]),
        ("round:baton-table", ["baton", "candidate", "review", "棒次", "候选", "审查"]),
        ("round:n-1-n-2", ["n-1", "n-2", "上一棒", "上两棒"]),
        ("round:checkpoint", ["checkpoint", "next step", "下一步", "用户 checkpoint"]),
        ("round:raw-links", ["raw capture", "raw 索引", "raw capture index", "raw 路径"]),
        (
            "round:convergence-index",
            ["convergence index", "strict_consecutive_identical_count", "收敛指数", "收敛计数"],
        ),
        ("round:resume-state", ["resume state", "current round/baton", "当前轮", "当前棒", "handover"]),
        ("round:next-step-inputs", ["next-baton", "下一棒", "继续", "修订", "深研"]),
        ("round:syntax-morphology", ["句法", "构词", "syntax", "morphology", "依存", "dependency"]),
    ]
    missing = missing_required(text, checks)
    missing.extend(flat_scores_missing(text, "round:"))
    missing.extend(na_without_reason_missing(text, "round:"))
    missing.extend(fifth_baton_web_access_missing(text, "round-archive"))
    return missing


def checkpoint_missing(text: str) -> list[str]:
    checks = [
        ("checkpoint:user-stop", ["wait for user", "user decision", "等待用户", "停下来"]),
        ("checkpoint:convergence-state", ["convergence", "remaining issue", "收敛", "未决问题"]),
        ("checkpoint:next-options", ["continue", "revise", "finalize", "继续", "修订", "收尾"]),
        (
            "checkpoint:strict-convergence",
            [
                "strict convergence",
                "exact text equality",
                "strict_consecutive_identical_count",
                "严格同文",
                "严格收敛",
                "逐字一致",
            ],
        ),
        ("checkpoint:latest-candidate", ["latest candidate", "最新候选", "当前候选", "最终候选"]),
        ("checkpoint:open-disputes", ["open disputes", "开放争议", "未决争议", "待决"]),
        ("checkpoint:locked-decisions", ["locked decisions", "已锁定", "用户锁定"]),
        ("checkpoint:next-baton-inputs", ["next-baton", "下一棒", "下一棒输入", "next baton prompt"]),
    ]
    missing = missing_required(text, checks)
    missing.extend(na_without_reason_missing(text, "checkpoint:"))
    return missing


def divergence_missing(text: str) -> list[str]:
    checks = [
        ("divergence:disputes", ["dispute", "recurring issue", "争议点", "反复出现"]),
        ("divergence:root-causes", ["root cause", "根因", "根本原因"]),
        ("divergence:candidate-comparison", ["candidate comparison", "候选比较", "候选对照"]),
        (
            "divergence:convergence-vs-divergence",
            ["convergence vs divergence", "收敛 vs 发散", "发散判定", "收敛判定"],
        ),
        (
            "divergence:non-divergence-case",
            ["non-divergence", "不发散", "早收敛", "early convergence", "若无发散"],
        ),
        ("divergence:n-1-n-2-drift", ["drift", "漂移", "风格回弹", "过度修正", "overcorrection", "回摆"]),
    ]
    missing = missing_required(text, checks)
    missing.extend(syntax_morphology_missing(text, "divergence"))
    missing.extend(flat_scores_missing(text, "divergence:"))
    missing.extend(na_without_reason_missing(text, "divergence:"))
    return missing


def final_report_missing(text: str) -> list[str]:
    checks = [
        ("final:user-confirmation", ["user confirmation", "final output approved", "用户确认", "用户接受"]),
        ("final:source-text", ["source text", "原文", "源文"]),
        ("final:final-translation", ["final translation", "最终译文", "定稿译文"]),
        ("final:relay-trajectory", ["relay trajectory", "baton", "接力轨迹", "棒次表"]),
        ("final:artifact-list", ["artifact list", "产物清单", "artifacts"]),
        ("final:compliance-check", ["compliance", "self-check", "合规自查", "红线"]),
    ]
    missing = missing_required(text, checks)
    missing.extend(syntax_morphology_missing(text, "final"))
    if not has_layered_scores(text):
        missing.append("final:layered-scoring")
    missing.extend(three_layer_score_block_missing(text))
    missing.extend(flat_scores_missing(text, "final:"))
    missing.extend(na_without_reason_missing(text, "final:"))
    return missing


def lint_text(artifact_type: str, text: str) -> list[str]:
    if artifact_type == "prompt-package":
        return prompt_package_missing(text)
    if artifact_type == "baton-raw":
        return baton_raw_missing(text)
    if artifact_type == "round-archive":
        return round_archive_missing(text)
    if artifact_type == "checkpoint":
        return checkpoint_missing(text)
    if artifact_type == "divergence-report":
        return divergence_missing(text)
    if artifact_type == "final-report":
        return final_report_missing(text)
    raise ValueError(f"unknown artifact type: {artifact_type}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a public translate-v2 Markdown artifact.")
    parser.add_argument("--type", required=True, choices=sorted(ARTIFACT_TYPES))
    parser.add_argument("path")
    args = parser.parse_args()

    path = Path(args.path)
    text = path.read_text(encoding="utf-8")
    missing = lint_text(args.type, text)
    if missing:
        print("TRANSLATE_V2_ARTIFACT_LINT_STATUS=BLOCKED")
        print("MISSING_POLICY_ITEMS=" + ",".join(missing))
        return 2
    print("TRANSLATE_V2_ARTIFACT_LINT_STATUS=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
