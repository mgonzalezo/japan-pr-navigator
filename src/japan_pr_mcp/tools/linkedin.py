"""LinkedIn insights search tool (local knowledge base search)."""

from __future__ import annotations

from typing import Any

from japan_pr_mcp.knowledge_base import KnowledgeBase


def search_linkedin_insights(
    kb: KnowledgeBase,
    query: str,
    category: str | None = None,
) -> dict[str, Any]:
    tips = kb.get_tips()
    needle = query.lower()

    matches: list[dict[str, Any]] = []
    for tip in tips:
        searchable = f"{tip['title']} {tip['content']}".lower()
        if needle in searchable and (category is None or tip["category"] == category):
            matches.append({
                "title": tip["title"],
                "content": tip["content"],
                "source": tip.get("source", "community"),
                "category": tip["category"],
            })

    result: dict[str, Any] = {"insights": matches, "query": query}

    if not matches:
        result["message"] = (
            f"No community insights found for '{query}'. "
            "Try broader terms or check the FAQ."
        )

    return result
