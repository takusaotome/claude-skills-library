"""Tests for agent/tool_activity.py — format_tool_activity + build_activities_caption."""

from agent.tool_activity import format_tool_activity, build_activities_caption


class TestFormatToolActivity:
    def test_format_strips_mcp_prefix(self):
        result = format_tool_activity("mcp__ptools__load_skill", {})
        assert result["tool"] == "load_skill"

    def test_format_no_prefix_passthrough(self):
        result = format_tool_activity("load_skill", {})
        assert result["tool"] == "load_skill"

    def test_format_load_skill_includes_skill_name(self):
        result = format_tool_activity("load_skill", {"skill_name": "financial-analyst"})
        assert "financial-analyst" in result["label_en"]
        assert "financial-analyst" in result["label_jp"]

    def test_format_load_skill_empty_input(self):
        result = format_tool_activity("load_skill", {})
        assert result["tool"] == "load_skill"
        assert "label_en" in result
        assert "label_jp" in result

    def test_format_convert_to_pdf_includes_filename(self):
        result = format_tool_activity("convert_to_pdf", {"filename": "report"})
        assert "(report)" in result["label_en"]
        assert "(report)" in result["label_jp"]

    def test_format_unknown_tool_returns_none(self):
        result = format_tool_activity("unknown_tool", {})
        assert result is None

    def test_format_builtin_tools_return_none(self):
        for name in ("TodoWrite", "Write", "Read", "Edit", "Bash"):
            assert format_tool_activity(name, {}) is None

    def test_format_returns_required_keys(self):
        result = format_tool_activity("list_skills", {})
        assert set(result.keys()) >= {"tool", "input", "label_en", "label_jp"}


class TestBuildActivitiesCaption:
    def test_build_caption_en(self):
        activities = [format_tool_activity("list_skills", {})]
        caption = build_activities_caption(activities, "EN")
        assert caption is not None
        assert caption.startswith("**Tools used:**")

    def test_build_caption_jp(self):
        activities = [format_tool_activity("list_skills", {})]
        caption = build_activities_caption(activities, "JP")
        assert caption is not None
        assert caption.startswith("**使用ツール:**")

    def test_build_caption_multiple(self):
        activities = [
            format_tool_activity("list_skills", {}),
            format_tool_activity("load_skill", {"skill_name": "data-scientist"}),
        ]
        caption = build_activities_caption(activities, "EN")
        assert " | " in caption

    def test_build_caption_empty_returns_none(self):
        assert build_activities_caption([], "EN") is None
