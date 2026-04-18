"""Tests for get_phase_guidance tool. Written FIRST (RED phase)."""

from pathlib import Path


def test_phase_1_returns_guidance(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.phases import get_phase_guidance

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_phase_guidance(kb, phase=1)
    assert result["phase"] == 1
    assert "title" in result
    assert "description" in result
    assert "key_steps" in result
    assert isinstance(result["key_steps"], list)


def test_all_four_phases_valid(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.phases import get_phase_guidance

    kb = KnowledgeBase.load(knowledge_dir)
    for phase_num in [1, 2, 3, 4]:
        result = get_phase_guidance(kb, phase=phase_num)
        assert result["phase"] == phase_num
        assert "title" in result


def test_phase_includes_tips(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.phases import get_phase_guidance

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_phase_guidance(kb, phase=1)
    assert "tips" in result
    assert isinstance(result["tips"], list)
    assert len(result["tips"]) >= 1


def test_phase_includes_common_mistakes(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.phases import get_phase_guidance

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_phase_guidance(kb, phase=1)
    assert "common_mistakes" in result
    assert isinstance(result["common_mistakes"], list)


def test_phase_includes_community_tips(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.phases import get_phase_guidance

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_phase_guidance(kb, phase=1)
    assert "community_tips" in result
    assert isinstance(result["community_tips"], list)
    assert len(result["community_tips"]) >= 1


def test_invalid_phase_returns_error(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.phases import get_phase_guidance

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_phase_guidance(kb, phase=0)
    assert "error" in result

    result = get_phase_guidance(kb, phase=5)
    assert "error" in result


def test_phase_has_estimated_duration(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.phases import get_phase_guidance

    kb = KnowledgeBase.load(knowledge_dir)
    result = get_phase_guidance(kb, phase=1)
    assert "estimated_duration" in result
