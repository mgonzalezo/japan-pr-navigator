"""Tests for MCP resource handlers. Written FIRST (RED phase)."""

from pathlib import Path


def test_get_document_resource_returns_data(knowledge_dir: Path) -> None:
    from japan_pr_mcp.resources.knowledge import get_document_resource

    result = get_document_resource(knowledge_dir, doc_id="1")
    assert result["id"] == 1
    assert result["name_en"] == "Application Form"
    assert result["name_jp"] == "永住許可申請書"


def test_get_document_resource_missing_id(knowledge_dir: Path) -> None:
    from japan_pr_mcp.resources.knowledge import get_document_resource

    result = get_document_resource(knowledge_dir, doc_id="999")
    assert "error" in result


def test_get_phase_resource(knowledge_dir: Path) -> None:
    from japan_pr_mcp.resources.knowledge import get_phase_resource

    result = get_phase_resource(knowledge_dir, phase_number="2")
    assert result["phase"] == 2
    assert result["title"] == "Immigration Application"


def test_get_phase_resource_invalid(knowledge_dir: Path) -> None:
    from japan_pr_mcp.resources.knowledge import get_phase_resource

    result = get_phase_resource(knowledge_dir, phase_number="5")
    assert "error" in result


def test_get_hsp_points_table_resource(knowledge_dir: Path) -> None:
    from japan_pr_mcp.resources.knowledge import get_hsp_points_table_resource

    result = get_hsp_points_table_resource(knowledge_dir)
    assert "categories" in result
    assert "thresholds" in result


def test_get_offices_resource(knowledge_dir: Path) -> None:
    from japan_pr_mcp.resources.knowledge import get_offices_resource

    result = get_offices_resource(knowledge_dir, region="Tokyo")
    assert isinstance(result, list)
    assert len(result) >= 1
    assert result[0]["prefecture"] == "Tokyo"


def test_get_offices_resource_no_match(knowledge_dir: Path) -> None:
    from japan_pr_mcp.resources.knowledge import get_offices_resource

    result = get_offices_resource(knowledge_dir, region="Okinawa")
    assert isinstance(result, dict)
    assert "message" in result
