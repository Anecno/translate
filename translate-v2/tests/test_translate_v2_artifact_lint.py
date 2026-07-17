#!/usr/bin/env python3
"""Regression tests for the public artifact linter."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "translate_v2_artifact_lint.py"


def run_lint(artifact_type: str, text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "artifact.md"
        path.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--type", artifact_type, str(path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )


def test_prompt_package_blocks_missing_contract() -> None:
    result = run_lint("prompt-package", "# Prompt\nTranslate this.")
    assert result.returncode == 2
    assert "TRANSLATE_V2_ARTIFACT_LINT_STATUS=BLOCKED" in result.stdout
    assert "prompt:baton-context" in result.stdout


def test_prompt_package_ok() -> None:
    result = run_lint(
        "prompt-package",
        """
# Relay Package
principles first / translation principles.
source language: ja. target language: en.
N-1 and N-2 previous baton context must be included.
scores.language
scores.literary
scores.cultural
aggregate
raw capture requires full output.
round archive with round summary.
checkpoint: wait for user.
final output requires user confirmation.
""",
    )
    assert result.returncode == 0
    assert "TRANSLATE_V2_ARTIFACT_LINT_STATUS=OK" in result.stdout


def test_final_report_blocks_flat_scores() -> None:
    result = run_lint(
        "final-report",
        """
# Final
user confirmation and final output approved.
source text.
final translation.
relay trajectory baton.
artifact list.
compliance self-check.
scores_14d
""",
    )
    assert result.returncode == 2
    assert "flat-score-schema-forbidden" in result.stdout


def final_report_ok_text() -> str:
    return """
# Completed Relay Report
user confirmation and final output approved.
source text.
final translation.
relay trajectory baton.
artifact list.
compliance self-check.
sentence overview with source anchor.
phrase breakdown with literal meaning.
dependency root modifiers.
lemma and morphology.
translation strategy and strategy tag.
addition omission mistranslation hallucination redline audit.
scores.language
scores.literary
scores.cultural
aggregate quality_score penalty_per_1000
"""


def test_final_report_blocks_missing_core_element() -> None:
    result = run_lint(
        "final-report",
        final_report_ok_text().replace("final translation.", ""),
    )
    assert result.returncode == 2
    assert "final:final-translation" in result.stdout


def test_final_report_blocks_missing_syntax_element() -> None:
    result = run_lint(
        "final-report",
        final_report_ok_text().replace("lemma and morphology.", ""),
    )
    assert result.returncode == 2
    assert "final:syntax-lexical-morphology" in result.stdout


def test_final_report_ok() -> None:
    result = run_lint("final-report", final_report_ok_text())
    assert result.returncode == 0
    assert "TRANSLATE_V2_ARTIFACT_LINT_STATUS=OK" in result.stdout


def test_divergence_report_blocks_missing_report_element() -> None:
    result = run_lint(
        "divergence-report",
        """
# Divergence Report
dispute and recurring issue.
root cause.
sentence overview with source anchor.
phrase breakdown with literal meaning.
dependency root modifiers.
lemma and morphology.
translation strategy and strategy tag.
addition omission mistranslation hallucination redline audit.
""",
    )
    assert result.returncode == 2
    assert "divergence:candidate-comparison" in result.stdout


def first_baton_prompt_ok_text() -> str:
    return """
# Prompt — 哈士奇 R1B1
principles first / translation principles.
source language: ja. target language: en.
N-1 and N-2 previous baton context.
The target-language dictionary is priority and mandatory for every uncertainty; use the local dictionary library (and a NotebookLM notebook when available). Dictionary lookup is required.
If the target-language dictionary does not answer, fall back to ordinary web search.
Do not substitute the source-language dictionary for the target-language dictionary.
List all lookups in a complete lookup log (dictionary check record); mark misses as NOT_FOUND.
scores.language
scores.literary
scores.cultural
aggregate
raw capture requires full output.
round archive with round summary.
checkpoint: wait for user.
final output requires user confirmation.
"""


def fifth_baton_prompt_ok_text() -> str:
    return """
# Prompt — Qoder R1B5 fifth baton
principles first / translation principles.
source language: ja. target language: en.
N-1 and N-2 previous baton context.
Use the web-access route/skill for the fifth-baton research pass; cover source-language and target-language sites, including hard-to-reach real-user platforms such as 小红书.
Comprehensive: check every disputed segment and list all findings in a full research log (complete record).
Mark misses as NOT_FOUND / CANNOT_VERIFY.
scores.language
scores.literary
scores.cultural
aggregate
raw capture requires full output.
round archive with round summary.
checkpoint: wait for user.
final output requires user confirmation.
"""


def test_first_baton_prompt_ok() -> None:
    result = run_lint("prompt-package", first_baton_prompt_ok_text())
    assert result.returncode == 0, result.stdout
    assert "TRANSLATE_V2_ARTIFACT_LINT_STATUS=OK" in result.stdout


def test_first_baton_prompt_blocks_missing_dictionary() -> None:
    result = run_lint(
        "prompt-package",
        first_baton_prompt_ok_text()
        .replace(
            "The target-language dictionary is priority and mandatory for every uncertainty;"
            " use the local dictionary library (and a NotebookLM notebook when available)."
            " Dictionary lookup is required.",
            "",
        )
        .replace("If the target-language dictionary does not answer, fall back to ordinary web search.", "")
        .replace("Do not substitute the source-language dictionary for the target-language dictionary.", "")
        .replace(
            "List all lookups in a complete lookup log (dictionary check record); mark misses as NOT_FOUND.",
            "",
        ),
    )
    assert result.returncode == 2
    assert "prompt:first-baton-target-language-dictionary-missing" in result.stdout


def test_fifth_baton_prompt_ok() -> None:
    result = run_lint("prompt-package", fifth_baton_prompt_ok_text())
    assert result.returncode == 0, result.stdout
    assert "TRANSLATE_V2_ARTIFACT_LINT_STATUS=OK" in result.stdout


def test_fifth_baton_prompt_blocks_missing_web_access() -> None:
    # 逗比 as the fifth baton must be held to the same web-access contract as Qoder.
    result = run_lint(
        "prompt-package",
        fifth_baton_prompt_ok_text()
        .replace("Qoder R1B5", "逗比 R1B5")
        .replace(
            "Use the web-access route/skill for the fifth-baton research pass;"
            " cover source-language and target-language sites, including hard-to-reach"
            " real-user platforms such as 小红书.",
            "",
        )
        .replace(
            "Comprehensive: check every disputed segment and list all findings in a full research log (complete record).",
            "",
        )
        .replace("Mark misses as NOT_FOUND / CANNOT_VERIFY.", ""),
    )
    assert result.returncode == 2
    assert "prompt:fifth-baton-web-access-required-missing" in result.stdout


def test_baton_raw_blocks_fifth_baton_lazy() -> None:
    result = run_lint(
        "baton-raw",
        """
# baton-raw — Qoder R1B5
source surface captured from the tab.
relay stage baton.
full output.
candidate translation.
review and reason.
convergence and satisfaction.
""",
    )
    assert result.returncode == 2
    assert "baton-raw:fifth-baton-web-access-evidence-missing" in result.stdout


def test_non_target_prompt_not_bound_by_member_contracts() -> None:
    # A generic prompt that targets neither the first nor the fifth baton must not
    # trigger either member-specific safeguard (OK-baseline regression guard).
    result = run_lint(
        "prompt-package",
        """
# Relay Package
principles first / translation principles.
source language: ja. target language: en.
N-1 and N-2 previous baton context must be included.
scores.language
scores.literary
scores.cultural
aggregate
raw capture requires full output.
round archive with round summary.
checkpoint: wait for user.
final output requires user confirmation.
""",
    )
    assert result.returncode == 0, result.stdout
    assert "TRANSLATE_V2_ARTIFACT_LINT_STATUS=OK" in result.stdout


def antique_prompt_ok_text() -> str:
    return """
# Prompt — Antique relay
principles first / translation principles.
source language: zh. target language: ja.
N-1 and N-2 previous baton context.
This is an Antique Game Within Game / 《古董局中局》 task: give the local-access members the manuscript chapters directory and the knowledge-base (references) roots to read for story context.
Source-boundary: the manuscript and knowledge base are background for understanding only, not source text to translate; do not leak them into the translation.
scores.language
scores.literary
scores.cultural
aggregate
raw capture requires full output.
round archive with round summary.
checkpoint: wait for user.
final output requires user confirmation.
"""


def test_antique_linkage_ok() -> None:
    result = run_lint("prompt-package", antique_prompt_ok_text())
    assert result.returncode == 0, result.stdout
    assert "TRANSLATE_V2_ARTIFACT_LINT_STATUS=OK" in result.stdout


def test_antique_linkage_blocks_missing_project_roots() -> None:
    result = run_lint(
        "prompt-package",
        """
# Prompt — Antique relay
principles first / translation principles.
source language: zh. target language: ja.
N-1 and N-2 previous baton context.
This is a 《古董局中局》 task. Source-boundary: project context is background for understanding, not source text to translate.
scores.language
scores.literary
scores.cultural
aggregate
raw capture requires full output.
round archive with round summary.
checkpoint: wait for user.
final output requires user confirmation.
""",
    )
    assert result.returncode == 2
    assert "prompt:antique-linkage-project-roots-missing" in result.stdout


if __name__ == "__main__":
    test_prompt_package_blocks_missing_contract()
    test_prompt_package_ok()
    test_final_report_blocks_flat_scores()
    test_final_report_blocks_missing_core_element()
    test_final_report_blocks_missing_syntax_element()
    test_final_report_ok()
    test_divergence_report_blocks_missing_report_element()
    test_first_baton_prompt_ok()
    test_first_baton_prompt_blocks_missing_dictionary()
    test_fifth_baton_prompt_ok()
    test_fifth_baton_prompt_blocks_missing_web_access()
    test_baton_raw_blocks_fifth_baton_lazy()
    test_non_target_prompt_not_bound_by_member_contracts()
    test_antique_linkage_ok()
    test_antique_linkage_blocks_missing_project_roots()
    print("artifact lint tests passed")
