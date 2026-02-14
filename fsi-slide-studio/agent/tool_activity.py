"""Tool activity formatting for persistent display in chat history.

Pure Python module with no Streamlit dependency — easy to test.
"""

TOOL_DONE_LABELS = {
    "list_skills":      ("Listed skills",      "スキル一覧取得"),
    "load_skill":       ("Loaded skill",       "スキル読込"),
    "review_structure": ("Reviewed structure",  "構成レビュー"),
    "review_design":    ("Reviewed design",     "デザインレビュー"),
    "convert_to_pdf":   ("Generated PDF",       "PDF生成"),
    "convert_to_html":  ("Generated preview",   "プレビュー生成"),
    "render_mermaid":   ("Rendered diagram",    "図表レンダリング"),
}


def format_tool_activity(tool_name: str, tool_input: dict) -> dict | None:
    """Convert a tool_use_complete chunk into a display-ready dict.

    Returns None for tools not in TOOL_DONE_LABELS (e.g. built-in SDK tools
    like TodoWrite, Write, Read, Edit) so they are excluded from the display.
    """
    short = tool_name.split("__")[-1] if "__" in tool_name else tool_name
    if short not in TOOL_DONE_LABELS:
        return None
    label_en, label_jp = TOOL_DONE_LABELS[short]

    if short == "load_skill":
        skill = tool_input.get("skill_name", "")
        if skill:
            label_en = f"{label_en}: {skill}"
            label_jp = f"{label_jp}: {skill}"
    elif short in ("convert_to_pdf", "convert_to_html"):
        fname = tool_input.get("filename", "")
        if fname:
            label_en = f"{label_en} ({fname})"
            label_jp = f"{label_jp} ({fname})"

    return {"tool": short, "input": tool_input, "label_en": label_en, "label_jp": label_jp}


def build_activities_caption(activities: list, lang: str):
    """Format tool activities into a single caption string. Returns None if empty."""
    if not activities:
        return None
    header = "Tools used" if lang == "EN" else "使用ツール"
    items = " | ".join(a["label_en"] if lang == "EN" else a["label_jp"] for a in activities)
    return f"**{header}:** {items}"
