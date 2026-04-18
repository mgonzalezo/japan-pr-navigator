"""Document checklist tool."""

from __future__ import annotations

from typing import Any

from japan_pr_mcp.knowledge_base import KnowledgeBase

VALID_APPLICANT_TYPES = {"single", "married", "with_children"}


def get_document_checklist(
    kb: KnowledgeBase,
    applicant_type: str,
) -> dict[str, Any]:
    applicant_type = applicant_type.lower()

    if applicant_type not in VALID_APPLICANT_TYPES:
        valid_options = ', '.join(sorted(VALID_APPLICANT_TYPES))
        return {
            "error": f"Invalid applicant type: '{applicant_type}'. Must be one of: {valid_options}",
        }

    all_docs = kb.get_documents()
    filtered = [
        doc for doc in all_docs
        if applicant_type in doc.get("required_for", [])
    ]

    return {
        "applicant_type": applicant_type,
        "documents": filtered,
        "total_documents": len(filtered),
    }
