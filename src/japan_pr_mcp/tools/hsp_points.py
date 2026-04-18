"""HSP point calculator tool."""

from __future__ import annotations

from typing import Any

from japan_pr_mcp.knowledge_base import KnowledgeBase


def check_hsp_points(
    kb: KnowledgeBase,
    age: int,
    salary_jpy: int,
    education: str,
    experience_years: int,
    jlpt_level: str = "none",
    bonus: list[str] | None = None,
) -> dict[str, Any]:
    table = kb.get_hsp_table()
    categories = {c["name"]: c for c in table["categories"]}
    thresholds = table["thresholds"]

    education = education.lower()
    jlpt_level = jlpt_level.upper() if jlpt_level.lower() != "none" else "none"

    breakdown: dict[str, int] = {}

    breakdown["education"] = _score_options(categories["education"], education)
    breakdown["experience"] = _score_experience(categories["experience"], experience_years)
    breakdown["salary"] = _score_salary(categories["salary"], salary_jpy)
    breakdown["age"] = _score_age(categories["age"], age)
    breakdown["japanese_ability"] = _score_options(categories["japanese_ability"], jlpt_level)

    bonus_points = 0
    if bonus:
        bonus_map = {b["name"]: b["points"] for b in table.get("bonus_points", [])}
        for b in bonus:
            bonus_points += bonus_map.get(b, 0)
    breakdown["bonus"] = bonus_points

    total = sum(breakdown.values())

    return {
        "total_points": total,
        "breakdown": breakdown,
        "eligible_3_year_fast_track": total >= thresholds["fast_track_3_year"],
        "eligible_1_year_fast_track": total >= thresholds["fast_track_1_year"],
        "thresholds": thresholds,
    }


def _score_options(category: dict[str, Any], value: str) -> int:
    for opt in category.get("options", []):
        if opt["value"].lower() == value.lower():
            return opt["points"]
    return 0


def _score_experience(category: dict[str, Any], years: int) -> int:
    for bracket in category.get("brackets", []):
        min_y = bracket.get("min_years", 0)
        max_y = bracket.get("max_years", 999)
        if min_y <= years <= max_y:
            return bracket["points"]
    return 0


def _score_salary(category: dict[str, Any], jpy: int) -> int:
    for bracket in category.get("brackets", []):
        min_j = bracket.get("min_jpy", 0)
        max_j = bracket.get("max_jpy", float("inf"))
        if min_j <= jpy <= max_j:
            return bracket["points"]
    return 0


def _score_age(category: dict[str, Any], age: int) -> int:
    for bracket in category.get("brackets", []):
        min_a = bracket.get("min_age", 0)
        max_a = bracket.get("max_age", 999)
        if min_a <= age <= max_a:
            return bracket["points"]
    return 0
