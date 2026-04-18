"""Tests for search_linkedin_insights tool. Written FIRST (RED phase)."""

from pathlib import Path


def test_search_by_query(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.linkedin import search_linkedin_insights

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_linkedin_insights(kb, query="salary")
    assert "insights" in result
    assert len(result["insights"]) >= 1


def test_search_returns_relevant_content(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.linkedin import search_linkedin_insights

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_linkedin_insights(kb, query="guarantor")
    assert any("guarantor" in i["content"].lower() for i in result["insights"])


def test_empty_results_returns_message(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.linkedin import search_linkedin_insights

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_linkedin_insights(kb, query="xyznonexistent12345")
    assert result["insights"] == []
    assert "message" in result


def test_search_by_category(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.linkedin import search_linkedin_insights

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_linkedin_insights(kb, query="phase 1", category="phase_1")
    assert all(i["category"] == "phase_1" for i in result["insights"])


def test_insights_have_required_fields(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.linkedin import search_linkedin_insights

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_linkedin_insights(kb, query="revenue stamp")
    if result["insights"]:
        insight = result["insights"][0]
        assert "title" in insight
        assert "content" in insight
        assert "source" in insight
