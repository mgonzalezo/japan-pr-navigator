"""Tests for search_pr_requirements tool. Written FIRST (RED phase)."""

from pathlib import Path


def test_search_hsp_single(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.requirements import search_pr_requirements

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_pr_requirements(kb, visa_type="hsp", marital_status="single")
    assert "eligibility" in result
    assert "residence_requirement" in result
    assert result["visa_type"] == "hsp"


def test_search_hsp_married(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.requirements import search_pr_requirements

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_pr_requirements(kb, visa_type="hsp", marital_status="married")
    assert result["marital_status"] == "married"
    assert "additional_requirements" in result


def test_search_general_visa(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.requirements import search_pr_requirements

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_pr_requirements(kb, visa_type="engineer", marital_status="single")
    assert result["visa_type"] == "engineer"
    assert "residence_requirement" in result


def test_search_case_insensitive(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.requirements import search_pr_requirements

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_pr_requirements(kb, visa_type="HSP", marital_status="Single")
    assert result["visa_type"] == "hsp"


def test_search_unknown_visa_returns_general_info(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.requirements import search_pr_requirements

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_pr_requirements(kb, visa_type="unknown_visa", marital_status="single")
    assert "eligibility" in result
    assert "residence_requirement" in result


def test_search_returns_relevant_faq(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.requirements import search_pr_requirements

    kb = KnowledgeBase.load(knowledge_dir)
    result = search_pr_requirements(kb, visa_type="hsp", marital_status="single")
    assert "related_faq" in result
    assert isinstance(result["related_faq"], list)
