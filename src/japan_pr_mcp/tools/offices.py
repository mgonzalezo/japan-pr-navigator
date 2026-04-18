"""Immigration office lookup tool."""

from __future__ import annotations

from typing import Any

from japan_pr_mcp.knowledge_base import KnowledgeBase


def lookup_immigration_office(
    kb: KnowledgeBase,
    prefecture: str | None = None,
    city: str | None = None,
) -> dict[str, Any]:
    all_offices = kb.get_offices()

    if prefecture is None and city is None:
        return {"offices": all_offices}

    matches: list[dict[str, Any]] = []

    for office in all_offices:
        if (prefecture and office["prefecture"].lower() == prefecture.lower()) or (
            city and city.lower() in office.get("city", "").lower()
        ):
            matches.append(office)

    if not matches:
        available = sorted({o["prefecture"] for o in all_offices})
        message = (
            "No immigration offices found for the specified location. "
            "Try one of the available prefectures."
        )
        return {
            "offices": [],
            "message": message,
            "available_prefectures": available,
        }

    return {"offices": matches}
