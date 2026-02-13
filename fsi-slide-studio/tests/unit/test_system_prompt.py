"""Tests for agent/system_prompt.py."""

from pathlib import Path
from unittest.mock import patch

from agent.system_prompt import _load_template_css, build_system_prompt


class TestLoadTemplateCss:
    def test_extracts_frontmatter(self, tmp_path):
        template = tmp_path / "template.md"
        template.write_text("---\nmarp: true\ntheme: fujisoft\n---\n# Slide")
        with patch("agent.system_prompt.PRESENTATION_TEMPLATE_PATH", template):
            css = _load_template_css()
        assert "marp: true" in css
        assert "theme: fujisoft" in css

    def test_returns_placeholder_when_not_found(self):
        with patch(
            "agent.system_prompt.PRESENTATION_TEMPLATE_PATH",
            Path("/nonexistent/path.md"),
        ):
            css = _load_template_css()
        assert "not found" in css.lower()

    def test_returns_truncated_content_if_no_frontmatter(self, tmp_path):
        template = tmp_path / "template.md"
        template.write_text("No frontmatter here, just content.")
        with patch("agent.system_prompt.PRESENTATION_TEMPLATE_PATH", template):
            css = _load_template_css()
        assert "No frontmatter" in css


class TestBuildSystemPrompt:
    @patch("agent.system_prompt.get_skill_catalog_text", return_value="## Catalog")
    def test_contains_language_instruction_en(self, _mock_catalog, tmp_path):
        template = tmp_path / "t.md"
        template.write_text("---\ncss: here\n---\n# Slide")
        with patch("agent.system_prompt.PRESENTATION_TEMPLATE_PATH", template):
            prompt = build_system_prompt("EN")
        assert "Respond in English" in prompt

    @patch("agent.system_prompt.get_skill_catalog_text", return_value="## Catalog")
    def test_contains_language_instruction_jp(self, _mock_catalog, tmp_path):
        template = tmp_path / "t.md"
        template.write_text("---\ncss: here\n---\n# Slide")
        with patch("agent.system_prompt.PRESENTATION_TEMPLATE_PATH", template):
            prompt = build_system_prompt("JP")
        assert "日本語" in prompt

    @patch(
        "agent.system_prompt.get_skill_catalog_text",
        return_value="## Skill Catalog\n- skill-alpha",
    )
    def test_embeds_skill_catalog(self, _mock_catalog, tmp_path):
        template = tmp_path / "t.md"
        template.write_text("---\ntheme: x\n---\n")
        with patch("agent.system_prompt.PRESENTATION_TEMPLATE_PATH", template):
            prompt = build_system_prompt("EN")
        assert "Skill Catalog" in prompt
        assert "skill-alpha" in prompt

    @patch("agent.system_prompt.get_skill_catalog_text", return_value="")
    def test_contains_workflow_instructions(self, _mock_catalog, tmp_path):
        template = tmp_path / "t.md"
        template.write_text("---\ntheme: x\n---\n")
        with patch("agent.system_prompt.PRESENTATION_TEMPLATE_PATH", template):
            prompt = build_system_prompt("EN")
        assert "FSI Slide Studio" in prompt
        assert "review_structure" in prompt
