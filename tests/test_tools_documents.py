"""Tests for get_document_checklist tool. Written FIRST (RED phase)."""

from pathlib import Path


def test_checklist_single_excludes_family_docs(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.documents import get_document_checklist

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_document_checklist(kb, applicant_type="single")
    assert isinstance(result["documents"], list)
    names = [d["name_en"] for d in result["documents"]]
    assert "Application Form" in names
    assert "Marriage Certificate" not in names
    assert "Spouse's Tax Certificates" not in names


def test_checklist_married_includes_spouse_docs(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.documents import get_document_checklist

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_document_checklist(kb, applicant_type="married")
    names = [d["name_en"] for d in result["documents"]]
    assert "Marriage Certificate" in names
    assert "Spouse's Tax Certificates" in names
    assert "Spouse's Pension Record" in names


def test_checklist_with_children_includes_all(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.documents import get_document_checklist

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_document_checklist(kb, applicant_type="with_children")
    names = [d["name_en"] for d in result["documents"]]
    assert "Marriage Certificate" in names
    assert "Spouse & Child Insurance" in names
    assert "Application Form" in names


def test_checklist_includes_count(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.documents import get_document_checklist

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_document_checklist(kb, applicant_type="single")
    assert "total_documents" in result
    assert result["total_documents"] == len(result["documents"])


def test_checklist_documents_have_bilingual_names(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.documents import get_document_checklist

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_document_checklist(kb, applicant_type="single")
    for doc in result["documents"]:
        assert "name_en" in doc
        assert "name_jp" in doc
        assert "notes" in doc


def test_checklist_case_insensitive(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.documents import get_document_checklist

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_document_checklist(kb, applicant_type="SINGLE")
    assert result["applicant_type"] == "single"
    assert len(result["documents"]) > 0


def test_checklist_invalid_type_returns_error(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.documents import get_document_checklist

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_document_checklist(kb, applicant_type="invalid_type")
    assert "error" in result


def test_single_has_fewer_docs_than_married(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.documents import get_document_checklist

    kb = KnowledgeBase.load(knowledge_dir)
    single = get_document_checklist(kb, applicant_type="single")
    married = get_document_checklist(kb, applicant_type="married")
    assert single["total_documents"] < married["total_documents"]
