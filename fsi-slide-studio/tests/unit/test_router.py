"""Tests for skills/router.py."""

from pathlib import Path
from unittest.mock import patch

from skills.router import suggest_skills

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"
SAMPLE_YAML = FIXTURES_DIR / "sample_skill_categories.yaml"


@patch("skills.router.SKILL_CATEGORIES_PATH", SAMPLE_YAML)
class TestSuggestSkills:
    def test_matches_keyword(self):
        results = suggest_skills("I need help with testing")
        names = [s["name"] for s in results]
        assert "test-skill-1" in names

    def test_case_insensitive(self):
        results = suggest_skills("TESTING tools needed")
        names = [s["name"] for s in results]
        assert "test-skill-1" in names

    def test_no_match(self):
        results = suggest_skills("completely unrelated topic xyz")
        assert results == []

    def test_empty_message(self):
        results = suggest_skills("")
        assert results == []

    def test_deduplication(self):
        results = suggest_skills("test and testing")
        names = [s["name"] for s in results]
        assert len(names) == len(set(names))

    def test_multiple_categories(self):
        results = suggest_skills("test and demo")
        names = [s["name"] for s in results]
        assert "test-skill-1" in names
        assert "demo-skill" in names
