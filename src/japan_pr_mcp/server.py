"""FastMCP server entry point for Japan PR Navigator."""

from __future__ import annotations

import json
from pathlib import Path

from fastmcp import FastMCP

from japan_pr_mcp.knowledge_base import KnowledgeBase
from japan_pr_mcp.resources.knowledge import (
    get_document_resource,
    get_hsp_points_table_resource,
    get_offices_resource,
    get_phase_resource,
)
from japan_pr_mcp.tools.documents import get_document_checklist
from japan_pr_mcp.tools.hsp_points import check_hsp_points
from japan_pr_mcp.tools.linkedin import search_linkedin_insights
from japan_pr_mcp.tools.offices import lookup_immigration_office
from japan_pr_mcp.tools.phases import get_phase_guidance
from japan_pr_mcp.tools.requirements import search_pr_requirements

KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "knowledge"

mcp = FastMCP(
    "japan-pr-navigator",
    instructions=(
        "You are a helpful assistant for foreigners in Japan navigating the "
        "Permanent Residence application process. Use the available tools to "
        "answer questions about PR requirements, documents, HSP points, "
        "immigration offices, and application phases."
    ),
)

_kb: KnowledgeBase | None = None


def _get_kb() -> KnowledgeBase:
    global _kb
    if _kb is None:
        _kb = KnowledgeBase.load(KNOWLEDGE_DIR)
    return _kb


@mcp.tool(name="search_pr_requirements")
def search_pr_requirements_tool(visa_type: str, marital_status: str) -> str:
    """Search PR eligibility requirements by visa type and marital status.

    Args:
        visa_type: Visa type (e.g., 'hsp', 'engineer', 'specialist')
        marital_status: Marital status ('single', 'married', 'with_children')
    """
    result = search_pr_requirements(_get_kb(), visa_type, marital_status)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name="check_hsp_points")
def check_hsp_points_tool(
    age: int,
    salary_jpy: int,
    education: str,
    experience_years: int,
    jlpt_level: str = "none",
    bonus: list[str] | None = None,
) -> str:
    """Calculate HSP points to check PR fast-track eligibility.

    Args:
        age: Applicant's age
        salary_jpy: Annual salary in JPY
        education: Education level ('doctorate', 'masters', 'bachelors', 'none')
        experience_years: Years of professional experience
        jlpt_level: JLPT level ('N1', 'N2', 'none')
        bonus: Optional bonus categories (e.g., ['japanese_university', 'patent'])
    """
    result = check_hsp_points(
        _get_kb(), age, salary_jpy, education, experience_years, jlpt_level, bonus
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name="get_document_checklist")
def get_document_checklist_tool(applicant_type: str) -> str:
    """Get a personalized document checklist for PR application.

    Args:
        applicant_type: Applicant type ('single', 'married', 'with_children')
    """
    result = get_document_checklist(_get_kb(), applicant_type)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name="lookup_immigration_office")
def lookup_immigration_office_tool(
    prefecture: str | None = None,
    city: str | None = None,
) -> str:
    """Find the nearest immigration office by prefecture or city.

    Args:
        prefecture: Prefecture name (e.g., 'Tokyo', 'Osaka')
        city: City name (e.g., 'Yokohama')
    """
    result = lookup_immigration_office(_get_kb(), prefecture, city)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name="search_linkedin_insights")
def search_linkedin_insights_tool(
    query: str,
    category: str | None = None,
) -> str:
    """Search community insights and tips about Japan PR applications.

    Args:
        query: Search query (e.g., 'salary certificate', 'guarantor')
        category: Optional category filter ('phase_1', 'phase_2', 'phase_3', 'phase_4', 'general')
    """
    result = search_linkedin_insights(_get_kb(), query, category)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name="get_phase_guidance")
def get_phase_guidance_tool(phase: int) -> str:
    """Get detailed guidance for a specific PR application phase.

    Args:
        phase: Phase number (1=Document Collection, 2=Immigration Application,
            3=Additional Docs, 4=Card Pickup)
    """
    result = get_phase_guidance(_get_kb(), phase)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.resource("knowledge://hsp/points-table")
def hsp_points_table() -> str:
    """Full HSP point calculation table with all categories and thresholds."""
    result = get_hsp_points_table_resource(KNOWLEDGE_DIR)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.resource("knowledge://documents/{doc_id}")
def document_by_id(doc_id: str) -> str:
    """Get details for a specific PR document by ID."""
    result = get_document_resource(KNOWLEDGE_DIR, doc_id)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.resource("knowledge://phases/{phase_number}")
def phase_by_number(phase_number: str) -> str:
    """Get details for a specific application phase."""
    result = get_phase_resource(KNOWLEDGE_DIR, phase_number)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.resource("knowledge://offices/{region}")
def offices_by_region(region: str) -> str:
    """Get immigration offices for a specific region/prefecture."""
    result = get_offices_resource(KNOWLEDGE_DIR, region)
    return json.dumps(result, ensure_ascii=False, indent=2)
