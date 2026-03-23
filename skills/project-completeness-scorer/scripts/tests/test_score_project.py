"""Tests for the project completeness scorer."""

import json
from pathlib import Path

import pytest
from score_project import (
    EFFORT_MULTIPLIERS,
    SEVERITY_WEIGHTS,
    ProjectScorer,
    generate_markdown_report,
    get_document_template,
    get_library_template,
    get_skill_template,
    get_templates,
    get_webapp_template,
)


class TestGetTemplates:
    """Tests for template retrieval functions."""

    def test_get_templates_returns_all(self):
        """Test that get_templates returns all expected templates."""
        templates = get_templates()
        assert "skill" in templates
        assert "webapp" in templates
        assert "library" in templates
        assert "document" in templates

    def test_skill_template_has_required_fields(self):
        """Test that skill template has required structure."""
        template = get_skill_template()
        assert "template_id" in template
        assert "display_name" in template
        assert "description" in template
        assert "dimensions" in template
        assert len(template["dimensions"]) >= 4

    def test_template_weights_sum_to_one(self):
        """Test that dimension weights sum to 1.0 for all templates."""
        templates = get_templates()
        for name, template in templates.items():
            total_weight = sum(d["weight"] for d in template["dimensions"])
            assert abs(total_weight - 1.0) < 0.01, f"{name} weights sum to {total_weight}"


class TestProjectScorer:
    """Tests for the ProjectScorer class."""

    def test_check_file_exists_positive(self, sample_skill_project):
        """Test file exists check returns True for existing file."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_file_exists("SKILL.md")
        assert met is True
        assert "exists" in details

    def test_check_file_exists_negative(self, sample_skill_project):
        """Test file exists check returns False for missing file."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_file_exists("nonexistent.md")
        assert met is False
        assert "missing" in details

    def test_check_dir_exists_positive(self, sample_skill_project):
        """Test directory exists check returns True for existing directory."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_dir_exists("scripts")
        assert met is True
        assert "exists" in details

    def test_check_dir_exists_negative(self, sample_skill_project):
        """Test directory exists check returns False for missing directory."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_dir_exists("nonexistent")
        assert met is False
        assert "missing" in details

    def test_check_yaml_frontmatter_valid(self, sample_skill_project):
        """Test YAML frontmatter check for valid frontmatter."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_yaml_frontmatter("SKILL.md")
        assert met is True
        assert "Valid" in details

    def test_check_yaml_frontmatter_invalid(self, incomplete_skill_project):
        """Test YAML frontmatter check for missing frontmatter."""
        scorer = ProjectScorer(incomplete_skill_project, get_skill_template())
        met, details = scorer.check_yaml_frontmatter("SKILL.md")
        assert met is False
        assert "No YAML frontmatter" in details

    def test_check_has_heading_positive(self, sample_skill_project):
        """Test heading check finds existing heading."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_has_heading("SKILL.md", "## Overview")
        assert met is True
        assert "Found" in details

    def test_check_has_heading_negative(self, sample_skill_project):
        """Test heading check returns False for missing heading."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_has_heading("SKILL.md", "## Nonexistent")
        assert met is False
        assert "Missing" in details

    def test_check_file_count(self, sample_skill_project):
        """Test file count check."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_file_count("scripts/*.py", 1)
        assert met is True
        assert "Found" in details

    def test_check_test_count(self, sample_skill_project):
        """Test test function count check."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_test_count("scripts/tests/test_*.py", 3)
        assert met is True
        assert "Found 3" in details

    def test_check_shebang_positive(self, sample_skill_project):
        """Test shebang check for files with shebang."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_shebang("scripts/*.py")
        assert met is True
        assert "have shebang" in details

    def test_check_shebang_negative(self, tmp_path):
        """Test shebang check for files without shebang."""
        # Create a project with Python file without shebang
        project = tmp_path / "no-shebang"
        project.mkdir()
        scripts = project / "scripts"
        scripts.mkdir()
        (scripts / "test.py").write_text("print('no shebang')")

        scorer = ProjectScorer(project, get_skill_template())
        met, details = scorer.check_shebang("scripts/*.py")
        assert met is False
        assert "Missing shebang" in details

    def test_check_contains_positive(self, sample_skill_project):
        """Test contains check finds search string."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_contains("scripts/*.py", "argparse")
        assert met is True
        assert "Found" in details

    def test_check_no_pattern_clean(self, sample_skill_project):
        """Test no_pattern check passes for clean files."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        met, details = scorer.check_no_pattern("scripts/*.py", ["/Users/", "/home/"])
        assert met is True
        assert "No forbidden" in details

    def test_check_no_pattern_violation(self, tmp_path):
        """Test no_pattern check fails when forbidden pattern found."""
        project = tmp_path / "has-hardcode"
        project.mkdir()
        scripts = project / "scripts"
        scripts.mkdir()
        (scripts / "bad.py").write_text("path = '/Users/someone/file.txt'")

        scorer = ProjectScorer(project, get_skill_template())
        met, details = scorer.check_no_pattern("scripts/*.py", ["/Users/", "/home/"])
        assert met is False
        assert "forbidden" in details


class TestScoring:
    """Tests for the overall scoring process."""

    def test_score_complete_skill_project(self, sample_skill_project):
        """Test scoring a complete skill project."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        result = scorer.score()

        assert result.overall_score >= 80
        assert result.project_type == "skill"
        assert len(result.dimensions) == 5
        assert result.summary["critical_gaps"] == 0

    def test_score_incomplete_skill_project(self, incomplete_skill_project):
        """Test scoring an incomplete skill project identifies gaps."""
        scorer = ProjectScorer(incomplete_skill_project, get_skill_template())
        result = scorer.score()

        assert result.overall_score < 50
        assert len(result.gaps) > 5
        assert result.summary["critical_gaps"] > 0
        assert result.summary["ready_for_release"] is False

    def test_score_webapp_project(self, webapp_project):
        """Test scoring a webapp project."""
        scorer = ProjectScorer(webapp_project, get_webapp_template())
        result = scorer.score()

        assert result.project_type == "webapp"
        assert result.overall_score > 60

    def test_gaps_sorted_by_priority(self, incomplete_skill_project):
        """Test that gaps are sorted by priority (descending)."""
        scorer = ProjectScorer(incomplete_skill_project, get_skill_template())
        result = scorer.score()

        priorities = [g["priority"] for g in result.gaps]
        assert priorities == sorted(priorities, reverse=True)

    def test_critical_missing_caps_dimension(self, incomplete_skill_project):
        """Test that critical missing criteria caps dimension score at 60%."""
        scorer = ProjectScorer(incomplete_skill_project, get_skill_template())
        result = scorer.score()

        # Find Functional Requirements dimension (has critical YAML frontmatter)
        func_dim = next(d for d in result.dimensions if d["name"] == "Functional Requirements")
        assert func_dim["raw_score"] <= 60


class TestMarkdownReport:
    """Tests for markdown report generation."""

    def test_generate_markdown_report_structure(self, sample_skill_project):
        """Test that markdown report has expected structure."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())
        result = scorer.score()
        report = generate_markdown_report(result)

        assert "# Project Completeness Report" in report
        assert "## Score Breakdown" in report
        assert "## Dimension Details" in report
        assert "## Readiness Assessment" in report
        assert f"**Overall Score**: {result.overall_score}/100" in report

    def test_generate_markdown_report_gaps_section(self, incomplete_skill_project):
        """Test that markdown report includes priority actions when gaps exist."""
        scorer = ProjectScorer(incomplete_skill_project, get_skill_template())
        result = scorer.score()
        report = generate_markdown_report(result)

        assert "## Priority Actions" in report
        assert "**[Critical]**" in report or "**[Major]**" in report


class TestPriorityCalculation:
    """Tests for gap priority calculation."""

    def test_priority_weights_defined(self):
        """Test that severity weights are defined."""
        assert SEVERITY_WEIGHTS["critical"] > SEVERITY_WEIGHTS["major"]
        assert SEVERITY_WEIGHTS["major"] > SEVERITY_WEIGHTS["minor"]

    def test_effort_multipliers_defined(self):
        """Test that effort multipliers are defined."""
        assert EFFORT_MULTIPLIERS["low"] < EFFORT_MULTIPLIERS["medium"]
        assert EFFORT_MULTIPLIERS["medium"] < EFFORT_MULTIPLIERS["high"]

    def test_calculate_priority(self, sample_skill_project):
        """Test priority calculation formula."""
        scorer = ProjectScorer(sample_skill_project, get_skill_template())

        # Critical severity, high weight, low effort = highest priority
        p1 = scorer.calculate_priority("critical", 0.30, "low")
        # Minor severity, low weight, high effort = lowest priority
        p2 = scorer.calculate_priority("minor", 0.10, "high")

        assert p1 > p2


class TestFileExistsAny:
    """Tests for file_exists_any check."""

    def test_file_exists_any_found(self, tmp_path):
        """Test file_exists_any when one file exists."""
        project = tmp_path / "project"
        project.mkdir()
        (project / "setup.py").write_text("")

        scorer = ProjectScorer(project, get_skill_template())
        met, details = scorer.check_file_exists_any(["pyproject.toml", "setup.py", "package.json"])
        assert met is True
        assert "Found: setup.py" in details

    def test_file_exists_any_none(self, tmp_path):
        """Test file_exists_any when no file exists."""
        project = tmp_path / "empty"
        project.mkdir()

        scorer = ProjectScorer(project, get_skill_template())
        met, details = scorer.check_file_exists_any(["pyproject.toml", "package.json"])
        assert met is False
        assert "None found" in details


class TestDirExistsAny:
    """Tests for dir_exists_any check."""

    def test_dir_exists_any_found(self, tmp_path):
        """Test dir_exists_any when one directory exists."""
        project = tmp_path / "project"
        project.mkdir()
        (project / "src").mkdir()

        scorer = ProjectScorer(project, get_skill_template())
        met, details = scorer.check_dir_exists_any(["src", "lib", "app"])
        assert met is True
        assert "Found: src" in details

    def test_dir_exists_any_none(self, tmp_path):
        """Test dir_exists_any when no directory exists."""
        project = tmp_path / "empty"
        project.mkdir()

        scorer = ProjectScorer(project, get_skill_template())
        met, details = scorer.check_dir_exists_any(["src", "lib"])
        assert met is False
        assert "None found" in details
