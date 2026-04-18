"""Tests for the KnowledgeBase loader. Written FIRST (RED phase)."""

from pathlib import Path

import pytest


def test_load_from_valid_directory(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    assert kb is not None


def test_load_raises_on_missing_directory(tmp_path: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    with pytest.raises(FileNotFoundError):
        KnowledgeBase.load(tmp_path / "nonexistent")


def test_load_handles_empty_directory(empty_knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(empty_knowledge_dir)
    assert kb.get_documents() == []
    assert kb.get_phases() == []
    assert kb.get_offices() == []
    assert kb.get_tips() == []
    assert kb.get_faq() == []
    assert kb.get_hsp_table() == {}


def test_get_documents_returns_list(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    docs = kb.get_documents()
    assert isinstance(docs, list)
    assert len(docs) == 28
    assert docs[0]["id"] == 1
    assert "name_en" in docs[0]
    assert "name_jp" in docs[0]


def test_get_documents_returns_copy(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    docs1 = kb.get_documents()
    docs2 = kb.get_documents()
    assert docs1 is not docs2


def test_get_phases_returns_all_four(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    phases = kb.get_phases()
    assert isinstance(phases, list)
    assert len(phases) == 4
    phase_numbers = [p["phase"] for p in phases]
    assert phase_numbers == [1, 2, 3, 4]


def test_get_hsp_table_has_categories(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    table = kb.get_hsp_table()
    assert isinstance(table, dict)
    assert "categories" in table
    assert "thresholds" in table
    category_names = [c["name"] for c in table["categories"]]
    assert "education" in category_names
    assert "salary" in category_names
    assert "age" in category_names
    assert "experience" in category_names
    assert "japanese_ability" in category_names


def test_get_offices_returns_list(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    offices = kb.get_offices()
    assert isinstance(offices, list)
    assert len(offices) >= 5
    assert all("prefecture" in o for o in offices)


def test_get_tips_returns_list(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    tips = kb.get_tips()
    assert isinstance(tips, list)
    assert len(tips) >= 3
    assert all("category" in t for t in tips)


def test_get_faq_returns_list(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    faq = kb.get_faq()
    assert isinstance(faq, list)
    assert len(faq) >= 3
    assert all("question" in f for f in faq)
    assert all("answer" in f for f in faq)


def test_get_document_by_id(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    doc = kb.get_document_by_id(1)
    assert doc is not None
    assert doc["name_en"] == "Application Form"
    assert doc["name_jp"] == "永住許可申請書"


def test_get_document_by_id_returns_none_for_missing(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    doc = kb.get_document_by_id(999)
    assert doc is None


def test_get_phase_by_number(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    phase = kb.get_phase_by_number(1)
    assert phase is not None
    assert phase["title"] == "Document Collection"


def test_get_phase_by_number_returns_none_for_invalid(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    assert kb.get_phase_by_number(0) is None
    assert kb.get_phase_by_number(5) is None


def test_get_offices_by_prefecture(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    offices = kb.get_offices_by_prefecture("Tokyo")
    assert len(offices) >= 1
    assert all(o["prefecture"] == "Tokyo" for o in offices)


def test_get_offices_by_prefecture_case_insensitive(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    offices = kb.get_offices_by_prefecture("tokyo")
    assert len(offices) >= 1


def test_get_tips_by_category(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    tips = kb.get_tips_by_category("phase_1")
    assert len(tips) >= 1
    assert all(t["category"] == "phase_1" for t in tips)


def test_search_faq(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    results = kb.search_faq("guarantor")
    assert len(results) >= 1
    assert any("guarantor" in r["question"].lower() for r in results)


def test_search_faq_no_results(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    kb = KnowledgeBase.load(knowledge_dir)
    results = kb.search_faq("xyznonexistent")
    assert results == []


def test_malformed_yaml_handled_gracefully(tmp_path: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase

    d = tmp_path / "bad_yaml"
    d.mkdir()
    (d / "documents.yaml").write_text("invalid: yaml: content: [")
    kb = KnowledgeBase.load(d)
    assert kb.get_documents() == []
