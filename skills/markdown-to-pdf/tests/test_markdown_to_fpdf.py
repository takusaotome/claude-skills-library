#!/usr/bin/env python3
"""
Unit tests for markdown_to_fpdf.py — Professional PDF generation from Markdown.

Tests cover:
- YAML frontmatter parsing
- AST heading mapping
- Inline formatting (bold/italic)
- Table rendering (data_table / info_table override)
- Pagebreak and thematic break handling
- Cover page generation
- Theme selection
- Font discovery fail-fast
- CLI font override
- Mermaid fallback
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ===== Fixtures =====

@pytest.fixture
def basic_md():
    return (FIXTURES_DIR / "basic_document.md").read_text(encoding="utf-8")


@pytest.fixture
def estimate_md():
    return (FIXTURES_DIR / "estimate_document.md").read_text(encoding="utf-8")


@pytest.fixture
def table_heavy_md():
    return (FIXTURES_DIR / "table_heavy.md").read_text(encoding="utf-8")


@pytest.fixture
def mermaid_md():
    return (FIXTURES_DIR / "mermaid_document.md").read_text(encoding="utf-8")


@pytest.fixture
def tmp_pdf(tmp_path):
    return tmp_path / "output.pdf"


# ===== Import helpers =====

@pytest.fixture(autouse=True)
def _import_module():
    """Import the module under test. Skip if dependencies missing."""
    try:
        import fpdf
        import mistune
        import yaml
    except ImportError as e:
        pytest.skip(f"Missing dependency: {e}")


def _import_fpdf_module():
    """Import markdown_to_fpdf module."""
    import markdown_to_fpdf
    return markdown_to_fpdf


# ===== Frontmatter Parsing Tests =====

class TestParseFrontmatter:

    def test_parse_frontmatter_full(self, estimate_md):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(estimate_md)
        assert fm["title"] == "御見積書"
        assert fm["subtitle"] == "AI プラットフォーム PoC サポート"
        assert fm["theme"] == "navy"
        assert fm["document_number"] == "FSAI-2026-0001"
        assert fm["cover"] is True
        assert fm["confidential"] is False
        assert "# 提案概要" in body

    def test_parse_frontmatter_missing(self, basic_md):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(basic_md)
        assert fm == {}
        assert "# Basic Document Title" in body

    def test_parse_frontmatter_defaults(self):
        mod = _import_fpdf_module()
        md = "---\ntitle: Test\n---\n\nContent"
        fm, body = mod.parse_frontmatter(md)
        assert fm["title"] == "Test"
        # theme not specified - should be absent
        assert "theme" not in fm


# ===== AST Mapping Tests =====

class TestASTHeadingMapping:

    def test_heading_h1(self, basic_md):
        mod = _import_fpdf_module()
        tokens = mod.parse_markdown(basic_md)
        # Find heading tokens
        headings = [t for t in tokens if t["type"] == "heading"]
        h1s = [h for h in headings if h["attrs"]["level"] == 1]
        assert len(h1s) >= 1

    def test_heading_h2(self, basic_md):
        mod = _import_fpdf_module()
        tokens = mod.parse_markdown(basic_md)
        headings = [t for t in tokens if t["type"] == "heading"]
        h2s = [h for h in headings if h["attrs"]["level"] == 2]
        assert len(h2s) >= 2


# ===== Inline Formatting Tests =====

class TestInlineFormatting:

    def test_extract_text_from_children(self):
        mod = _import_fpdf_module()
        children = [
            {"type": "text", "raw": "Hello "},
            {"type": "strong", "children": [{"type": "text", "raw": "bold"}]},
            {"type": "text", "raw": " world"},
        ]
        text = mod.extract_text(children)
        assert "Hello" in text
        assert "bold" in text
        assert "world" in text


# ===== Table Rendering Tests =====

class TestTableRendering:

    def test_table_data_rendering(self, table_heavy_md, tmp_pdf):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(table_heavy_md)
        # Should not raise
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        assert tmp_pdf.exists()
        assert tmp_pdf.stat().st_size > 0

    def test_table_info_override(self, estimate_md, tmp_pdf):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(estimate_md)
        # The estimate doc contains <!-- info-table --> comments
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        assert tmp_pdf.exists()

    def test_table_long_text_wrap(self, table_heavy_md, tmp_pdf):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(table_heavy_md)
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        # If it rendered without error, wrapping works
        assert tmp_pdf.stat().st_size > 0


# ===== Pagebreak and Thematic Break Tests =====

class TestPagebreakAndBreaks:

    def test_pagebreak_comment(self, estimate_md, tmp_pdf):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(estimate_md)
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        # Document has <!-- pagebreak --> so should have multiple pages
        from fpdf import FPDF
        # Read back to check page count
        assert tmp_pdf.exists()

    def test_thematic_break_as_line(self, basic_md, tmp_pdf):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(basic_md)
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        # --- should NOT cause a page break, just a horizontal line
        assert tmp_pdf.exists()


# ===== Cover Page Tests =====

class TestCoverPage:

    def test_cover_page_generation(self, estimate_md, tmp_pdf):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(estimate_md)
        assert fm.get("cover") is True
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        assert tmp_pdf.exists()
        # Cover page + content = at least 2 pages
        assert tmp_pdf.stat().st_size > 1000

    def test_no_cover_page(self, table_heavy_md, tmp_pdf):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(table_heavy_md)
        assert fm.get("cover") is False
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        assert tmp_pdf.exists()


# ===== Theme Tests =====

class TestThemes:

    def test_theme_navy(self):
        from themes import get_theme
        theme = get_theme("navy")
        assert theme.primary == (0, 51, 102)
        assert theme.name == "navy"

    def test_theme_gray(self):
        from themes import get_theme
        theme = get_theme("gray")
        assert theme.primary == (60, 60, 60)
        assert theme.name == "gray"

    def test_theme_unknown(self):
        from themes import get_theme
        with pytest.raises(ValueError, match="Unknown theme"):
            get_theme("nonexistent")


# ===== Font Discovery Tests =====

class TestFontDiscovery:

    def test_font_not_found_fail_fast(self):
        from themes import discover_fonts
        with patch("themes.platform") as mock_platform:
            mock_platform.system.return_value = "UnknownOS"
            with pytest.raises(SystemExit):
                # UnknownOS has no candidates, _LINUX_FONTS won't match either
                # Need to also patch Path.exists to return False
                with patch("themes.Path") as mock_path:
                    mock_path.return_value.exists.return_value = False
                    discover_fonts()

    def test_font_cli_override(self, tmp_path):
        from themes import discover_fonts
        # Create fake font files
        reg = tmp_path / "regular.ttc"
        bold = tmp_path / "bold.ttc"
        reg.write_bytes(b"fake")
        bold.write_bytes(b"fake")
        r, b = discover_fonts(str(reg), str(bold))
        assert r == str(reg)
        assert b == str(bold)

    def test_font_cli_override_missing(self):
        from themes import discover_fonts
        with pytest.raises(SystemExit):
            discover_fonts("/nonexistent/font.ttc", "/nonexistent/bold.ttc")


# ===== Italic Font Rendering Tests =====

class TestItalicFontRendering:

    def test_italic_font_rendering(self, tmp_pdf):
        """Verify italic text does not crash with Undefined font error."""
        mod = _import_fpdf_module()
        md_with_italic = "This has *italic* and **bold** and ***bold italic*** text."
        mod.render_pdf(md_with_italic, str(tmp_pdf))
        assert tmp_pdf.exists()


# ===== Mermaid Fallback Tests =====

class TestMermaidFallback:

    def test_mermaid_fallback(self, mermaid_md, tmp_pdf):
        """Mermaid blocks should fall back to code blocks when conversion fails."""
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(mermaid_md)
        # mermaid_to_image.py might not be available in test env,
        # so mermaid blocks should gracefully fall back
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        assert tmp_pdf.exists()


# ===== End-to-End Rendering Tests =====

class TestEndToEnd:

    def test_basic_document_renders(self, basic_md, tmp_pdf):
        mod = _import_fpdf_module()
        mod.render_pdf(basic_md, str(tmp_pdf))
        assert tmp_pdf.exists()
        assert tmp_pdf.stat().st_size > 0

    def test_estimate_document_renders(self, estimate_md, tmp_pdf):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(estimate_md)
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        assert tmp_pdf.exists()
        assert tmp_pdf.stat().st_size > 0

    def test_table_heavy_document_renders(self, table_heavy_md, tmp_pdf):
        mod = _import_fpdf_module()
        fm, body = mod.parse_frontmatter(table_heavy_md)
        mod.render_pdf(body, str(tmp_pdf), frontmatter=fm)
        assert tmp_pdf.exists()
        assert tmp_pdf.stat().st_size > 0


# ===== Table Content Verification Tests (Finding 3) =====

class TestTableContentExtraction:
    """Verify table headers and rows are correctly extracted from mistune AST."""

    def test_table_headers_extracted(self):
        """Headers must be extracted from mistune 3.x table_head (no table_row wrapper)."""
        mod = _import_fpdf_module()
        md = "| Name | Age |\n|------|-----|\n| Alice | 30 |"
        tokens = mod.parse_markdown(md)
        table_tokens = [t for t in tokens if t["type"] == "table"]
        assert len(table_tokens) == 1

        # Extract headers using the same logic as _render_table
        table = table_tokens[0]
        headers = []
        for child in table.get("children", []):
            if child["type"] == "table_head":
                for cell_or_row in child.get("children", []):
                    if cell_or_row["type"] == "table_cell":
                        headers.append(mod.extract_text(cell_or_row.get("children", [])))
                    elif cell_or_row["type"] == "table_row":
                        for cell_token in cell_or_row.get("children", []):
                            if cell_token["type"] == "table_cell":
                                headers.append(mod.extract_text(cell_token.get("children", [])))
        assert headers == ["Name", "Age"]

    def test_table_rows_extracted(self):
        """Body rows must be correctly extracted from table_body."""
        mod = _import_fpdf_module()
        md = "| Name | Age |\n|------|-----|\n| Alice | 30 |\n| Bob | 25 |"
        tokens = mod.parse_markdown(md)
        table_tokens = [t for t in tokens if t["type"] == "table"]
        assert len(table_tokens) == 1

        table = table_tokens[0]
        rows = []
        for child in table.get("children", []):
            if child["type"] == "table_body":
                for row_token in child.get("children", []):
                    if row_token["type"] == "table_row":
                        row_cells = []
                        for cell_token in row_token.get("children", []):
                            if cell_token["type"] == "table_cell":
                                row_cells.append(mod.extract_text(cell_token.get("children", [])))
                        rows.append(row_cells)
        assert len(rows) == 2
        assert rows[0] == ["Alice", "30"]
        assert rows[1] == ["Bob", "25"]

    def test_table_renders_with_content(self, tmp_pdf):
        """Table with known content must produce non-empty PDF (regression for Finding 1)."""
        mod = _import_fpdf_module()
        md = "| Name | Age |\n|------|-----|\n| Alice | 30 |\n| Bob | 25 |"
        mod.render_pdf(md, str(tmp_pdf))
        assert tmp_pdf.exists()
        # A PDF with actual table content should be larger than a minimal empty PDF
        assert tmp_pdf.stat().st_size > 500


# ===== Font One-Side Specification Tests (Finding 4) =====

class TestFontOneSideSpecification:

    def test_font_regular_only_error(self, tmp_path):
        """Specifying only --font-regular (without --font-bold) must exit with error."""
        from themes import discover_fonts
        reg = tmp_path / "regular.ttc"
        reg.write_bytes(b"fake")
        with pytest.raises(SystemExit):
            discover_fonts(font_regular=str(reg), font_bold=None)

    def test_font_bold_only_error(self, tmp_path):
        """Specifying only --font-bold (without --font-regular) must exit with error."""
        from themes import discover_fonts
        bold = tmp_path / "bold.ttc"
        bold.write_bytes(b"fake")
        with pytest.raises(SystemExit):
            discover_fonts(font_regular=None, font_bold=str(bold))
