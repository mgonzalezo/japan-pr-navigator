"""Tests for check_hsp_points tool. Written FIRST (RED phase)."""

from pathlib import Path


def test_high_scoring_profile(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    result = check_hsp_points(
        kb,
        age=35,
        salary_jpy=9_000_000,
        education="masters",
        experience_years=10,
        jlpt_level="N2",
    )
    assert "total_points" in result
    assert "breakdown" in result
    assert result["total_points"] >= 70
    assert result["eligible_3_year_fast_track"] is True


def test_80_plus_gets_1_year_track(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    result = check_hsp_points(
        kb,
        age=28,
        salary_jpy=10_000_000,
        education="doctorate",
        experience_years=10,
        jlpt_level="N1",
    )
    assert result["total_points"] >= 80
    assert result["eligible_1_year_fast_track"] is True


def test_low_scoring_profile(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    result = check_hsp_points(
        kb,
        age=45,
        salary_jpy=3_000_000,
        education="none",
        experience_years=2,
        jlpt_level="none",
    )
    assert result["total_points"] < 70
    assert result["eligible_3_year_fast_track"] is False
    assert result["eligible_1_year_fast_track"] is False


def test_age_boundary_29_vs_30(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    result_29 = check_hsp_points(
        kb, age=29, salary_jpy=5_000_000, education="bachelors",
        experience_years=5, jlpt_level="none",
    )
    result_30 = check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="bachelors",
        experience_years=5, jlpt_level="none",
    )
    age_29_pts = result_29["breakdown"]["age"]
    age_30_pts = result_30["breakdown"]["age"]
    assert age_29_pts > age_30_pts


def test_salary_brackets(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    result_low = check_hsp_points(
        kb, age=30, salary_jpy=4_000_000, education="bachelors",
        experience_years=3, jlpt_level="none",
    )
    result_high = check_hsp_points(
        kb, age=30, salary_jpy=10_000_000, education="bachelors",
        experience_years=3, jlpt_level="none",
    )
    assert result_high["breakdown"]["salary"] > result_low["breakdown"]["salary"]


def test_education_levels(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    doctorate = check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="doctorate",
        experience_years=5, jlpt_level="none",
    )
    masters = check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="masters",
        experience_years=5, jlpt_level="none",
    )
    bachelors = check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="bachelors",
        experience_years=5, jlpt_level="none",
    )
    assert doctorate["breakdown"]["education"] > masters["breakdown"]["education"]
    assert masters["breakdown"]["education"] > bachelors["breakdown"]["education"]


def test_jlpt_n1_vs_n2(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    n1 = check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="bachelors",
        experience_years=5, jlpt_level="N1",
    )
    n2 = check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="bachelors",
        experience_years=5, jlpt_level="N2",
    )
    assert n1["breakdown"]["japanese_ability"] > n2["breakdown"]["japanese_ability"]


def test_missing_optional_fields_default_zero(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    result = check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="bachelors",
        experience_years=5,
    )
    assert result["breakdown"]["japanese_ability"] == 0
    assert "total_points" in result


def test_bonus_points(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    result = check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="bachelors",
        experience_years=5, bonus=["japanese_university", "patent"],
    )
    assert result["breakdown"]["bonus"] > 0
    assert result["total_points"] > check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="bachelors",
        experience_years=5,
    )["total_points"]


def test_case_insensitive_inputs(knowledge_dir: Path) -> None:
    from japan_pr_mcp.knowledge_base import KnowledgeBase
    from japan_pr_mcp.tools.hsp_points import check_hsp_points

    kb = KnowledgeBase.load(knowledge_dir)
    result = check_hsp_points(
        kb, age=30, salary_jpy=5_000_000, education="Masters",
        experience_years=5, jlpt_level="n2",
    )
    assert result["breakdown"]["education"] == 20
    assert result["breakdown"]["japanese_ability"] == 10
