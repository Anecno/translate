#!/usr/bin/env python3
"""Preflight checks for public translate-v2 relay operations."""

from __future__ import annotations

import argparse

from translate_v2_common import has_any


# Wording that signals a capture is partial/truncated rather than the full text.
TRUNCATION_MARKERS = [
    "partial",
    "truncat",
    "excerpt",
    "snippet",
    "summary only",
    "not full",
    "incomplete",
    "省略",
    "截断",
    "部分",
    "节选",
    "片段",
    "摘要",
]


def raw_capture_plan_gaps(plan: str | None, prefix: str) -> list[str]:
    """A raw-capture plan must cover the full prompt *and* the full output."""

    if not plan:
        return []
    missing: list[str] = []
    if not has_any(plan, ["prompt", "input", "输入", "发送", "所发", "问题原文"]):
        missing.append(f"{prefix}raw-capture-plan-prompt-missing")
    if not has_any(plan, ["output", "result", "reply", "response", "输出", "结果", "回复", "回答", "产出", "译文"]):
        missing.append(f"{prefix}raw-capture-plan-output-missing")
    return missing


def capture_incomplete(value: str | None, name: str, prefix: str) -> list[str]:
    if not value:
        return []
    if has_any(value, TRUNCATION_MARKERS):
        return [f"{prefix}{name}-incomplete"]
    return []


def search_scope_gaps(state: str | None, is_web: bool, prefix: str) -> list[str]:
    """When a web relay declares ordinary search on, require a full scope contract.

    The public spec's first-baton search rule allows ordinary web search only for
    genuine target-language usage / source-ambiguity checks, and forbids any
    dictionary or search result from overriding the source text, user
    constraints, terminology, or context. If a web relay declares search on
    without stating that scope and override ban, the relay is under-specified.
    This check is optional in the public edition: it only fires when a search
    state is actually declared for a web relay.
    """

    if not state or not is_web:
        return []
    search_off = has_any(
        state,
        ["search off", "disabled", "offline", "unavailable", "关闭", "未开", "不开", "无搜索"],
    )
    search_on = has_any(
        state,
        ["search on", "enabled", "开启", "打开", "保持开", "联网搜索开", "普通搜索开", "ordinary search on"],
    )
    if not search_on or search_off:
        return []
    missing: list[str] = []
    scope_declared = has_any(
        state,
        [
            "scope",
            "范围",
            "only",
            "仅",
            "target language",
            "target-language",
            "grammar",
            "语法",
            "honorific",
            "敬语",
            "collocation",
            "搭配",
            "punctuation",
            "标点",
            "dictionary",
            "词典",
            "usage",
            "用法",
        ],
    )
    override_ban_declared = has_any(
        state,
        [
            "not override",
            "no override",
            "must not override",
            "不得覆盖",
            "不能覆盖",
            "不覆盖",
            "不得引入",
            "不引入外部",
            "外部事实",
            "source text",
            "源文",
            "user constraint",
            "用户约束",
            "terminology",
            "术语",
            "authoritative",
            "source of truth",
            "准据",
            "权威",
        ],
    )
    if not scope_declared:
        missing.append(f"{prefix}search-scope-undeclared")
    if not override_ban_declared:
        missing.append(f"{prefix}search-source-override-ban-missing")
    return missing


def before_send_missing(args: argparse.Namespace) -> list[str]:
    missing: list[str] = []
    required = {
        "operator": args.operator,
        "surface": args.surface,
        "prompt_file": args.prompt_file,
        "raw_capture_plan": args.raw_capture_plan,
        "contract_status": args.contract_status,
    }
    for name, value in required.items():
        if not value:
            missing.append(f"before-send:{name}-missing")
    if args.contract_status and "OK" not in args.contract_status:
        missing.append("before-send:contract-not-ok")
    if args.prompt_file and not args.prompt_file.endswith((".md", ".txt")):
        missing.append("before-send:prompt-file-extension")
    missing.extend(raw_capture_plan_gaps(args.raw_capture_plan, "before-send:"))
    is_web = "web" in (args.surface or "").lower()
    missing.extend(search_scope_gaps(args.network_search_state, is_web, "before-send:"))
    return missing


def after_result_missing(args: argparse.Namespace) -> list[str]:
    missing: list[str] = []
    required = {
        "surface": args.surface,
        "raw_capture_file": args.raw_capture_file,
        "artifact_lint_status": args.artifact_lint_status,
        "prompt_captured": args.prompt_captured,
        "output_captured": args.output_captured,
    }
    for name, value in required.items():
        if not value:
            missing.append(f"after-result:{name}-missing")
    if args.artifact_lint_status and "OK" not in args.artifact_lint_status:
        missing.append("after-result:artifact-lint-not-ok")
    if args.raw_capture_file and not args.raw_capture_file.endswith(".md"):
        missing.append("after-result:raw-capture-extension")
    # Both the exact prompt/input sent and the full output must be captured in
    # full; a partial/truncated capture cannot seed the next baton's N-1/N-2.
    missing.extend(capture_incomplete(args.prompt_captured, "prompt-capture", "after-result:"))
    missing.extend(capture_incomplete(args.output_captured, "output-capture", "after-result:"))
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Check translate-v2 relay preflight evidence.")
    sub = parser.add_subparsers(dest="command", required=True)

    before = sub.add_parser("before-send")
    before.add_argument("--operator")
    before.add_argument("--surface")
    before.add_argument("--prompt-file")
    before.add_argument("--raw-capture-plan")
    before.add_argument("--contract-status")
    before.add_argument(
        "--network-search-state",
        help="Optional. Declared search state for a web relay; when search is on, a scope + source-override-ban contract is required.",
    )

    after = sub.add_parser("after-result")
    after.add_argument("--surface")
    after.add_argument("--raw-capture-file")
    after.add_argument("--artifact-lint-status")
    after.add_argument("--prompt-captured")
    after.add_argument("--output-captured")

    args = parser.parse_args()
    missing = before_send_missing(args) if args.command == "before-send" else after_result_missing(args)
    if missing:
        print("TRANSLATE_V2_PREFLIGHT_STATUS=BLOCKED")
        print("MISSING_POLICY_ITEMS=" + ",".join(missing))
        return 2
    print("TRANSLATE_V2_PREFLIGHT_STATUS=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
