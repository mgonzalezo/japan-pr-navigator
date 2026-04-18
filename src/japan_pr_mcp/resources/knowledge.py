"""MCP resource handlers for the knowledge base."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from japan_pr_mcp.knowledge_base import KnowledgeBase


def get_document_resource(knowledge_dir: Path, doc_id: str) -> dict[str, Any]:
    kb = KnowledgeBase.load(knowledge_dir)
    doc = kb.get_document_by_id(int(doc_id))
    if doc is None:
        return {"error": f"Document with id {doc_id} not found"}
    return doc


def get_phase_resource(knowledge_dir: Path, phase_number: str) -> dict[str, Any]:
    kb = KnowledgeBase.load(knowledge_dir)
    phase = kb.get_phase_by_number(int(phase_number))
    if phase is None:
        return {"error": f"Phase {phase_number} not found. Valid phases: 1-4"}
    return phase


def get_hsp_points_table_resource(knowledge_dir: Path) -> dict[str, Any]:
    kb = KnowledgeBase.load(knowledge_dir)
    return kb.get_hsp_table()


def get_offices_resource(knowledge_dir: Path, region: str) -> list[dict[str, Any]] | dict[str, Any]:
    kb = KnowledgeBase.load(knowledge_dir)
    offices = kb.get_offices_by_prefecture(region)
    if not offices:
        available = sorted({o["prefecture"] for o in kb.get_offices()})
        return {"message": f"No offices found for '{region}'", "available_regions": available}
    return offices
