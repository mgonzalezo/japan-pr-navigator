"""Tests for lookup_immigration_office tool. Written FIRST (RED phase)."""

from pathlib import Path


def test_search_by_prefecture(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.offices import lookup_immigration_office

    kb = KnowledgeBase.load(knowledge_dir)
    result = lookup_immigration_office(kb, prefecture="Tokyo")
    assert "offices" in result
    assert len(result["offices"]) >= 1
    assert result["offices"][0]["prefecture"] == "Tokyo"


def test_search_by_city(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.offices import lookup_immigration_office

    kb = KnowledgeBase.load(knowledge_dir)
    result = lookup_immigration_office(kb, city="Yokohama")
    assert len(result["offices"]) >= 1
    assert "Yokohama" in result["offices"][0]["city"]


def test_case_insensitive_prefecture(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.offices import lookup_immigration_office

    kb = KnowledgeBase.load(knowledge_dir)
    result = lookup_immigration_office(kb, prefecture="tokyo")
    assert len(result["offices"]) >= 1


def test_no_match_returns_all_prefectures(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.offices import lookup_immigration_office

    kb = KnowledgeBase.load(knowledge_dir)
    result = lookup_immigration_office(kb, prefecture="Okinawa")
    assert "message" in result
    assert "available_prefectures" in result
    assert isinstance(result["available_prefectures"], list)


def test_offices_have_required_fields(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.offices import lookup_immigration_office

    kb = KnowledgeBase.load(knowledge_dir)
    result = lookup_immigration_office(kb, prefecture="Tokyo")
    office = result["offices"][0]
    assert "name_en" in office
    assert "name_jp" in office
    assert "address" in office
    assert "estimated_pr_wait" in office


def test_no_params_returns_all(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.offices import lookup_immigration_office

    kb = KnowledgeBase.load(knowledge_dir)
    result = lookup_immigration_office(kb)
    assert len(result["offices"]) >= 5
