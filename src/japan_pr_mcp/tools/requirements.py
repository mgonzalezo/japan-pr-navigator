"""PR requirements search tool."""

from __future__ import annotations

from typing import Any

from japan_pr_mcp.knowledge_base import KnowledgeBase

RESIDENCE_REQUIREMENTS: dict[str, dict[str, str]] = {
    "hsp": {
        "standard": "1 year (80+ points) or 3 years (70+ points)",
        "description": "Highly Skilled Professional fast-track via point system",
    },
    "engineer": {
        "standard": "10 years of continuous residence",
        "description": "Engineer/Specialist in Humanities/International Services visa",
    },
    "specialist": {
        "standard": "10 years of continuous residence",
        "description": "Specialist in Humanities/International Services visa",
    },
}

DEFAULT_RESIDENCE = {
    "standard": "10 years of continuous residence (general requirement)",
    "description": "Standard PR requirement for most visa categories",
}


def search_pr_requirements(
    kb: KnowledgeBase,
    visa_type: str,
    marital_status: str,
) -> dict[str, Any]:
    visa_type = visa_type.lower()
    marital_status = marital_status.lower()

    residence_info = RESIDENCE_REQUIREMENTS.get(visa_type, DEFAULT_RESIDENCE)

    eligibility: list[str] = [
        "Must have been a good citizen (no criminal record in Japan)",
        "Must have sufficient assets or ability to make an independent living",
        "Must be in the interest of Japan for the applicant to reside permanently",
        f"Residence requirement: {residence_info['standard']}",
    ]

    if visa_type == "hsp":
        eligibility.append("Must score 70+ points on the HSP point calculation table")
        eligibility.append(
            "Points calculated at time of application AND at time of initial HSP visa grant"
        )

    result: dict[str, Any] = {
        "visa_type": visa_type,
        "marital_status": marital_status,
        "eligibility": eligibility,
        "residence_requirement": residence_info["standard"],
        "visa_description": residence_info["description"],
    }

    if marital_status in ("married", "with_children"):
        result["additional_requirements"] = [
            "Must provide spouse's tax certificates (even if finances are separate)",
            "Must provide spouse's pension records",
            "Must provide marriage certificate",
            "Must provide dependent insurance cards",
        ]
        if marital_status == "with_children":
            result["additional_requirements"].append(
                "Must provide children's health insurance eligibility certificates"
            )

    related_faq = kb.search_faq(visa_type)
    if not related_faq:
        related_faq = kb.search_faq("PR")
    result["related_faq"] = [
        {"question": f["question"], "id": f["id"]} for f in related_faq
    ]

    return result
