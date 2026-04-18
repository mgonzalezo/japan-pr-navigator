"""Phase guidance tool."""

from __future__ import annotations

from typing import Any

from japan_pr_mcp.knowledge_base import KnowledgeBase

PHASE_TO_TIP_CATEGORY = {
    1: "phase_1",
    2: "phase_2",
    3: "phase_3",
    4: "phase_4",
}


def get_phase_guidance(
    kb: KnowledgeBase,
    phase: int,
) -> dict[str, Any]:
    phase_data = kb.get_phase_by_number(phase)

    if phase_data is None:
        return {
            "error": f"Invalid phase: {phase}. Must be 1, 2, 3, or 4.",
        }

    tip_category = PHASE_TO_TIP_CATEGORY.get(phase, "")
    community_tips = kb.get_tips_by_category(tip_category)

    return {
        "phase": phase_data["phase"],
        "title": phase_data["title"],
        "title_jp": phase_data.get("title_jp", ""),
        "description": phase_data["description"],
        "estimated_duration": phase_data.get("estimated_duration", "Unknown"),
        "key_steps": phase_data.get("key_steps", []),
        "tips": phase_data.get("tips", []),
        "common_mistakes": phase_data.get("common_mistakes", []),
        "community_tips": [
            {"title": t["title"], "content": t["content"]}
            for t in community_tips
        ],
    }
