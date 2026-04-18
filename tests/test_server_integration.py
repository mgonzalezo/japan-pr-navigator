"""Integration tests for the FastMCP server."""

import json

import pytest
from fastmcp import Client


@pytest.fixture
async def client():
    from japan_pr_mcp.server import mcp

    async with Client(mcp) as c:
        yield c


async def test_server_lists_all_tools(client: Client) -> None:
    tools = await client.list_tools()
    tool_names = {t.name for t in tools}
    assert "search_pr_requirements" in tool_names
    assert "check_hsp_points" in tool_names
    assert "get_document_checklist" in tool_names
    assert "lookup_immigration_office" in tool_names
    assert "search_linkedin_insights" in tool_names
    assert "get_phase_guidance" in tool_names


async def test_call_search_pr_requirements(client: Client) -> None:
    result = await client.call_tool(
        "search_pr_requirements",
        {"visa_type": "hsp", "marital_status": "single"},
    )
    data = json.loads(result.content[0].text)
    assert data["visa_type"] == "hsp"
    assert "eligibility" in data


async def test_call_check_hsp_points(client: Client) -> None:
    result = await client.call_tool(
        "check_hsp_points",
        {
            "age": 35,
            "salary_jpy": 9000000,
            "education": "masters",
            "experience_years": 10,
            "jlpt_level": "N2",
        },
    )
    data = json.loads(result.content[0].text)
    assert "total_points" in data
    assert data["total_points"] >= 70


async def test_call_get_document_checklist(client: Client) -> None:
    result = await client.call_tool(
        "get_document_checklist",
        {"applicant_type": "married"},
    )
    data = json.loads(result.content[0].text)
    assert "documents" in data
    assert data["total_documents"] > 0
    names = [d["name_en"] for d in data["documents"]]
    assert "Marriage Certificate" in names


async def test_call_lookup_immigration_office(client: Client) -> None:
    result = await client.call_tool(
        "lookup_immigration_office",
        {"prefecture": "Tokyo"},
    )
    data = json.loads(result.content[0].text)
    assert len(data["offices"]) >= 1


async def test_call_search_linkedin_insights(client: Client) -> None:
    result = await client.call_tool(
        "search_linkedin_insights",
        {"query": "guarantor"},
    )
    data = json.loads(result.content[0].text)
    assert "insights" in data


async def test_call_get_phase_guidance(client: Client) -> None:
    result = await client.call_tool(
        "get_phase_guidance",
        {"phase": 1},
    )
    data = json.loads(result.content[0].text)
    assert data["phase"] == 1
    assert "title" in data
    assert "key_steps" in data


async def test_server_lists_resources(client: Client) -> None:
    resource_templates = await client.list_resource_templates()
    assert len(resource_templates) >= 1


async def test_read_hsp_points_table_resource(client: Client) -> None:
    result = await client.read_resource("knowledge://hsp/points-table")
    contents = result if isinstance(result, list) else result.contents
    data = json.loads(contents[0].text)
    assert "categories" in data
    assert "thresholds" in data
