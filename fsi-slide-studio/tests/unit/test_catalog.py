"""Tests for skills/catalog.py."""

from pathlib import Path
from unittest.mock import patch

from skills.catalog import (
    load_skill_categories,
    get_all_skills,
    get_skill_catalog_text,
    load_skill_content,
    list_skill_names,
)

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"
SAMPLE_YAML = FIXTURES_DIR / "sample_skill_categories.yaml"


@patch("skills.catalog.SKILL_CATEGORIES_PATH", SAMPLE_YAML)
class TestLoadSkillCategories:
    def test_returns_dict(self):
        result = load_skill_categories()
        assert isinstance(result, dict)
        assert "categories" in result

    def test_has_expected_categories(self):
        result = load_skill_categories()
        cats = result["categories"]
        assert "TestCategory1" in cats
        assert "TestCategory2" in cats


@patch("skills.catalog.SKILL_CATEGORIES_PATH", SAMPLE_YAML)
class TestGetAllSkills:
    def test_returns_flat_list(self):
        skills = get_all_skills()
        assert isinstance(skills, list)
        assert len(skills) == 3

    def test_skill_has_required_keys(self):
        skills = get_all_skills()
        for skill in skills:
            assert "name" in skill
            assert "description" in skill
            assert "category" in skill

    def test_skill_category_is_correct(self):
        skills = get_all_skills()
        names_by_cat = {s["name"]: s["category"] for s in skills}
        assert names_by_cat["test-skill-1"] == "TestCategory1"
        assert names_by_cat["demo-skill"] == "TestCategory2"


@patch("skills.catalog.SKILL_CATEGORIES_PATH", SAMPLE_YAML)
class TestGetSkillCatalogText:
    def test_returns_string(self):
        text = get_skill_catalog_text()
        assert isinstance(text, str)

    def test_contains_category_headers(self):
        text = get_skill_catalog_text()
        assert "### TestCategory1" in text
        assert "### TestCategory2" in text

    def test_contains_skill_names(self):
        text = get_skill_catalog_text()
        assert "test-skill-1" in text
        assert "demo-skill" in text


class TestLoadSkillContent:
    def test_loads_skill_md(self, tmp_skill_dir):
        with patch("skills.catalog.SKILLS_LIBRARY_PATH", tmp_skill_dir.parent):
            content = load_skill_content("test-skill")
        assert "# Test Skill" in content

    def test_loads_reference_files(self, tmp_skill_dir):
        with patch("skills.catalog.SKILLS_LIBRARY_PATH", tmp_skill_dir.parent):
            content = load_skill_content("test-skill")
        assert "Reference: guide.md" in content

    def test_truncates_long_references(self, tmp_skill_dir_with_long_ref):
        with patch("skills.catalog.SKILLS_LIBRARY_PATH", tmp_skill_dir_with_long_ref.parent):
            content = load_skill_content("verbose-skill")
        assert "... (truncated)" in content

    def test_not_found_returns_error(self, tmp_path):
        with patch("skills.catalog.SKILLS_LIBRARY_PATH", tmp_path):
            content = load_skill_content("nonexistent-skill")
        assert "not found" in content.lower()

    def test_no_content_returns_message(self, tmp_path):
        empty_skill = tmp_path / "empty-skill"
        empty_skill.mkdir()
        with patch("skills.catalog.SKILLS_LIBRARY_PATH", tmp_path):
            content = load_skill_content("empty-skill")
        assert "no content" in content.lower()


class TestListSkillNames:
    def test_returns_sorted_list(self, tmp_skill_dir):
        with patch("skills.catalog.SKILLS_LIBRARY_PATH", tmp_skill_dir.parent):
            names = list_skill_names()
        assert isinstance(names, list)
        assert "test-skill" in names

    def test_excludes_dirs_without_skill_md(self, tmp_path):
        (tmp_path / "no-skill-md").mkdir()
        valid = tmp_path / "valid-skill"
        valid.mkdir()
        (valid / "SKILL.md").write_text("# Valid")
        with patch("skills.catalog.SKILLS_LIBRARY_PATH", tmp_path):
            names = list_skill_names()
        assert "valid-skill" in names
        assert "no-skill-md" not in names
