"""Tests for agent/tools.py."""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from agent.tools import (
    _load_checklist,
    list_skills,
    load_skill,
    render_mermaid,
    convert_to_pdf,
    convert_to_html,
    review_structure,
    review_design,
    create_presentation_tools_server,
)


class TestLoadChecklist:
    def test_reads_file_when_exists(self, tmp_path):
        refs = tmp_path / "fujisoft-presentation-creator" / "references"
        refs.mkdir(parents=True)
        (refs / "presentation_best_practices_checklist.md").write_text(
            "# Checklist\n- Item 1"
        )
        with patch("agent.tools.SKILLS_LIBRARY_PATH", tmp_path):
            result = _load_checklist()
        assert "Checklist" in result

    def test_returns_placeholder_when_missing(self, tmp_path):
        with patch("agent.tools.SKILLS_LIBRARY_PATH", tmp_path):
            result = _load_checklist()
        assert "not found" in result.lower()


class TestListSkills:
    @pytest.mark.asyncio
    @patch("agent.tools.get_all_skills")
    async def test_returns_content(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "skill-a", "description": "Desc A", "category": "Cat1"},
        ]
        result = await list_skills({})
        assert "content" in result
        assert any("skill-a" in c["text"] for c in result["content"])

    @pytest.mark.asyncio
    @patch("agent.tools.get_all_skills")
    async def test_groups_by_category(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "s1", "description": "D1", "category": "Alpha"},
            {"name": "s2", "description": "D2", "category": "Beta"},
        ]
        result = await list_skills({})
        text = result["content"][0]["text"]
        assert "## Alpha" in text
        assert "## Beta" in text


class TestLoadSkill:
    @pytest.mark.asyncio
    @patch("agent.tools.load_skill_content")
    async def test_loads_skill_content(self, mock_load):
        mock_load.return_value = "# Skill Content"
        result = await load_skill({"skill_name": "test-skill"})
        assert result["content"][0]["text"] == "# Skill Content"
        mock_load.assert_called_once_with("test-skill")

    @pytest.mark.asyncio
    @patch("agent.tools.load_skill_content")
    async def test_handles_empty_skill_name(self, mock_load):
        mock_load.return_value = "Error: Skill '' not found."
        result = await load_skill({})
        mock_load.assert_called_once_with("")


class TestConvertToPdf:
    @pytest.mark.asyncio
    @patch("agent.tools.convert_marp_to_pdf")
    async def test_success(self, mock_convert):
        mock_convert.return_value = Path("/tmp/test.pdf")
        result = await convert_to_pdf(
            {"markdown_content": "# Slide", "filename": "test"}
        )
        assert "content" in result
        assert "test.pdf" in result["content"][0]["text"]
        assert "is_error" not in result

    @pytest.mark.asyncio
    @patch("agent.tools.convert_marp_to_pdf")
    async def test_failure(self, mock_convert):
        mock_convert.side_effect = RuntimeError("marp not found")
        result = await convert_to_pdf(
            {"markdown_content": "# Slide", "filename": "test"}
        )
        assert result.get("is_error") is True
        assert "failed" in result["content"][0]["text"].lower()


class TestConvertToHtml:
    @pytest.mark.asyncio
    @patch("agent.tools.convert_marp_to_html")
    async def test_success(self, mock_convert):
        mock_convert.return_value = Path("/tmp/test.html")
        result = await convert_to_html(
            {"markdown_content": "# Slide", "filename": "test"}
        )
        assert "test.html" in result["content"][0]["text"]

    @pytest.mark.asyncio
    @patch("agent.tools.convert_marp_to_html")
    async def test_failure(self, mock_convert):
        mock_convert.side_effect = RuntimeError("marp not found")
        result = await convert_to_html(
            {"markdown_content": "# Slide", "filename": "test"}
        )
        assert result.get("is_error") is True


class TestRenderMermaid:
    @pytest.mark.asyncio
    @patch("agent.tools.render_mermaid_to_png")
    async def test_success_returns_filename_and_embed(self, mock_render):
        mock_render.return_value = Path("/tmp/output/gantt_chart.png")
        result = await render_mermaid(
            {"mermaid_code": "gantt\n  title Test", "filename": "gantt_chart"}
        )
        assert "content" in result
        assert "is_error" not in result
        text = result["content"][0]["text"]
        assert "gantt_chart.png" in text
        assert "![" in text  # embed instruction included

    @pytest.mark.asyncio
    @patch("agent.tools.render_mermaid_to_png")
    async def test_failure_returns_error(self, mock_render):
        mock_render.side_effect = RuntimeError("mmdc not found")
        result = await render_mermaid(
            {"mermaid_code": "gantt\n  title Test", "filename": "chart"}
        )
        assert result.get("is_error") is True
        assert "failed" in result["content"][0]["text"].lower()

    @pytest.mark.asyncio
    @patch("agent.tools.render_mermaid_to_png")
    async def test_default_filename(self, mock_render):
        mock_render.return_value = Path("/tmp/output/diagram.png")
        await render_mermaid({"mermaid_code": "flowchart TD\n  A-->B"})
        mock_render.assert_called_once_with("flowchart TD\n  A-->B", "diagram")

    @pytest.mark.asyncio
    @patch("agent.tools.render_mermaid_to_png")
    async def test_passes_args_to_converter(self, mock_render):
        mock_render.return_value = Path("/tmp/output/timeline.png")
        await render_mermaid(
            {"mermaid_code": "sequenceDiagram\n  A->>B: msg", "filename": "timeline"}
        )
        mock_render.assert_called_once_with(
            "sequenceDiagram\n  A->>B: msg", "timeline"
        )

    @pytest.mark.asyncio
    @patch("agent.tools.render_mermaid_to_png")
    async def test_subprocess_error_is_caught(self, mock_render):
        import subprocess
        mock_render.side_effect = subprocess.CalledProcessError(1, "mmdc")
        result = await render_mermaid(
            {"mermaid_code": "pie\n  title Budget", "filename": "budget"}
        )
        assert result.get("is_error") is True


class TestReviewStructure:
    @pytest.mark.asyncio
    async def test_returns_review_text(self):
        async def fake_query(**kwargs):
            msg = MagicMock()
            msg.content = [MagicMock(text="Good structure")]
            yield msg

        with patch("agent.tools.query", fake_query):
            result = await review_structure(
                {"structure": "outline", "context": "context"}
            )
        assert "Good structure" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_handles_query_error(self):
        async def failing_query(**kwargs):
            raise RuntimeError("API error")
            yield  # pragma: no cover

        with patch("agent.tools.query", failing_query):
            result = await review_structure(
                {"structure": "outline", "context": "context"}
            )
        assert result.get("is_error") is True


class TestReviewDesign:
    @pytest.mark.asyncio
    async def test_returns_review_text(self):
        async def fake_query(**kwargs):
            msg = MagicMock()
            msg.content = [MagicMock(text="Score: 85/100")]
            yield msg

        with patch("agent.tools.query", fake_query):
            with patch("agent.tools._load_checklist", return_value="# Checklist"):
                result = await review_design({"marp_markdown": "# Slide"})
        assert "85/100" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_handles_query_error(self):
        async def failing_query(**kwargs):
            raise RuntimeError("API error")
            yield  # pragma: no cover

        with patch("agent.tools.query", failing_query):
            with patch("agent.tools._load_checklist", return_value=""):
                result = await review_design({"marp_markdown": "# Slide"})
        assert result.get("is_error") is True


class TestCreatePresentationToolsServer:
    def test_creates_server_with_six_tools(self):
        import claude_agent_sdk

        claude_agent_sdk.create_sdk_mcp_server.reset_mock()
        create_presentation_tools_server()
        claude_agent_sdk.create_sdk_mcp_server.assert_called_once()
        kwargs = claude_agent_sdk.create_sdk_mcp_server.call_args[1]
        assert kwargs["name"] == "presentation-tools"
        assert kwargs["version"] == "2.0.0"
        assert len(kwargs["tools"]) == 7
