#!/usr/bin/env python3
"""Shared helpers for public translate-v2 validators."""

from __future__ import annotations

import re


def has_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle.lower() in lowered for needle in needles)


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[\u3400-\u9fff]", text))


def non_code_lines(text: str):
    in_fence = False
    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield line_no, line


FLAT_SCORE_MARKERS = [
    "scores_14d",
    "flat 14",
    "flat-score",
    "flat score",
]


FLAT_SCORE_INVALIDATION_MARKERS = [
    "scores_14d is invalid",
    "do not use scores_14d",
    "quoted failure example",
]


def flat_scores_missing(text: str, prefix: str = "") -> list[str]:
    lowered = text.lower()
    if not has_any(lowered, FLAT_SCORE_MARKERS):
        return []
    if has_any(lowered, FLAT_SCORE_INVALIDATION_MARKERS):
        return []
    return [f"{prefix}flat-score-schema-forbidden"]


def has_layered_scores(text: str) -> bool:
    return all(
        has_any(text, needles)
        for needles in [
            ["scores.language", "layer a", "language layer"],
            ["scores.literary", "layer b", "literary layer"],
            ["scores.cultural", "layer c", "cultural layer"],
            ["aggregate", "quality_score", "penalty_per_1000"],
        ]
    )


# Standalone anchors for the three-layer (A/B/C) + aggregate scoring block.
# Any translate-v2 scored artifact must carry all three layers *and* the
# aggregate, and they must live together as one coherent block rather than
# being scattered across the whole document.
THREE_LAYER_SCORE_ANCHORS = [
    ("common:scores.language-layer", ["scores.language", "layer a", "language layer", "语言层", '"language"']),
    ("common:scores.literary-layer", ["scores.literary", "layer b", "literary layer", "文学层", '"literary"']),
    ("common:scores.cultural-layer", ["scores.cultural", "layer c", "cultural layer", "文化层", '"cultural"']),
    ("common:scores-aggregate", ["aggregate", "quality_score", "penalty_per_1000", "s_norm", "聚合"]),
]


def score_anchor_line_index(text: str, needles: list[str]) -> int | None:
    lowered_needles = [needle.lower() for needle in needles]
    for index, line in enumerate(text.splitlines()):
        lowered = line.lower()
        if any(needle in lowered for needle in lowered_needles):
            return index
    return None


def three_layer_score_block_missing(text: str, max_span: int = 120) -> list[str]:
    """Require a complete, co-located Layer A/B/C + aggregate scoring block."""

    missing: list[str] = []
    positions: list[int] = []
    for name, needles in THREE_LAYER_SCORE_ANCHORS:
        index = score_anchor_line_index(text, needles)
        if index is None:
            missing.append(name)
        else:
            positions.append(index)
    if not missing and positions and max(positions) - min(positions) > max_span:
        missing.append("common:three-layer-score-block-scattered")
    return missing


# "N/A" is only acceptable when it is justified with an explicit reason; a bare
# "N/A" is a common way to silently drop a required analysis dimension.
NA_REASON_MARKERS = [
    "n/a：",
    "n/a:",
    "n/a with reason",
    "n/a because",
    "n/a —",
    "n/a -",
    "reason_if_na",
    "reason if n/a",
    "not applicable because",
    "不适用，原因",
    "不适用：",
    "不适用:",
    "不适用（",
    "不适用(",
    "不适用，因",
    "不适用—",
]


def na_without_reason_missing(text: str, prefix: str = "") -> list[str]:
    lowered = text.lower()
    if not re.search(r"\bn/?a\b", lowered):
        return []
    if has_any(lowered, NA_REASON_MARKERS):
        return []
    return [f"{prefix}na-without-reason"]
