#!/usr/bin/env python3
"""
Professional PDF generation from Markdown using fpdf2.

Converts Markdown files with YAML frontmatter into professionally styled PDFs
with cover pages, themed headers/footers, styled tables, and CJK font support.

Dependencies:
    fpdf2, mistune (>=3.0), pyyaml

Usage:
    python markdown_to_fpdf.py input.md output.pdf
    python markdown_to_fpdf.py input.md output.pdf --theme navy
    python markdown_to_fpdf.py input.md output.pdf --theme gray --confidential
    python markdown_to_fpdf.py input.md output.pdf --no-cover
    python markdown_to_fpdf.py input.md output.pdf --font-regular /path/to/font.ttc --font-bold /path/to/bold.ttc
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import mistune
import yaml
from fpdf import FPDF
from fpdf.drawing import DeviceRGB
from fpdf.enums import TableBordersLayout, TableCellFillMode
from fpdf.fonts import FontFace

# Ensure sibling imports work
_SCRIPT_DIR = Path(__file__).parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from themes import Theme, discover_fonts, get_theme

# Constants
FONT_FAMILY = "DocFont"
PAGE_WIDTH_MM = 210
PAGE_MARGIN_MM = 10
CONTENT_WIDTH_MM = PAGE_WIDTH_MM - 2 * PAGE_MARGIN_MM  # 190mm


# ============================================================
# Frontmatter parsing
# ============================================================

def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter from Markdown text.

    Returns (frontmatter_dict, body_text). If no frontmatter, returns ({}, text).
    """
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, text, re.DOTALL)
    if not match:
        return {}, text
    fm_str = match.group(1)
    body = text[match.end():]
    try:
        fm = yaml.safe_load(fm_str) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, body


# ============================================================
# Markdown AST parsing via mistune 3.x
# ============================================================

def parse_markdown(text: str) -> List[Dict]:
    """Parse Markdown to AST tokens using mistune 3.x."""
    md = mistune.create_markdown(renderer=None, plugins=["table"])
    tokens = md(text)
    return tokens


def extract_text(children: List[Dict]) -> str:
    """Recursively extract plain text from AST children nodes."""
    parts = []
    for child in children:
        if child["type"] == "text":
            parts.append(child.get("raw", child.get("children", "")))
        elif child["type"] == "codespan":
            parts.append(child.get("raw", child.get("children", "")))
        elif "children" in child and isinstance(child["children"], list):
            parts.append(extract_text(child["children"]))
        elif "children" in child and isinstance(child["children"], str):
            parts.append(child["children"])
        elif "raw" in child:
            parts.append(child["raw"])
    return "".join(parts)


def children_to_markdown(children: List[Dict]) -> str:
    """Convert AST children back to a markdown-like string for multi_cell(markdown=True)."""
    parts = []
    for child in children:
        ctype = child["type"]
        if ctype == "text":
            parts.append(child.get("raw", child.get("children", "")))
        elif ctype == "strong":
            inner = children_to_markdown(child["children"]) if isinstance(child["children"], list) else child["children"]
            parts.append(f"**{inner}**")
        elif ctype == "emphasis":
            inner = children_to_markdown(child["children"]) if isinstance(child["children"], list) else child["children"]
            parts.append(f"__{inner}__")
        elif ctype == "codespan":
            raw = child.get("raw", child.get("children", ""))
            parts.append(raw)
        elif ctype == "link":
            text = children_to_markdown(child["children"]) if isinstance(child["children"], list) else child["children"]
            parts.append(text)
        elif ctype == "softbreak":
            parts.append(" ")
        elif ctype == "linebreak":
            parts.append("\n")
        elif "children" in child and isinstance(child["children"], list):
            parts.append(children_to_markdown(child["children"]))
        elif "raw" in child:
            parts.append(child["raw"])
    return "".join(parts)


# ============================================================
# ProfessionalPDF class
# ============================================================

class ProfessionalPDF(FPDF):
    """FPDF subclass for professional document rendering with theme support."""

    def __init__(self, theme: Theme, frontmatter: Optional[Dict] = None,
                 font_regular: str = "", font_bold: str = ""):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.theme = theme
        self.frontmatter = frontmatter or {}
        self._is_cover = False

        # Register fonts — all 4 styles to avoid 'Undefined font' on markdown=True
        self.add_font(FONT_FAMILY, "", font_regular)
        self.add_font(FONT_FAMILY, "B", font_bold)
        self.add_font(FONT_FAMILY, "I", font_regular)   # Map italic to regular
        self.add_font(FONT_FAMILY, "BI", font_bold)      # Map bold-italic to bold

        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self._is_cover:
            return
        header_text = self.frontmatter.get("header_text", "")
        if not header_text:
            parts = []
            if self.frontmatter.get("document_number"):
                parts.append(self.frontmatter["document_number"])
            if self.frontmatter.get("company"):
                parts.append(self.frontmatter["company"])
            header_text = " | ".join(parts)

        if self.frontmatter.get("confidential"):
            header_text = f"CONFIDENTIAL | {header_text}" if header_text else "CONFIDENTIAL"

        self.set_font(FONT_FAMILY, "", 7)
        self.set_text_color(*self.theme.text_medium)
        self.cell(0, 5, header_text, align="C")
        self.ln(6)
        self.set_draw_color(*self.theme.primary)
        self.line(PAGE_MARGIN_MM, self.get_y(), PAGE_WIDTH_MM - PAGE_MARGIN_MM, self.get_y())
        self.ln(5)

    def footer(self):
        if self._is_cover:
            return
        self.set_y(-20)
        self.set_draw_color(*self.theme.primary)
        self.line(PAGE_MARGIN_MM, self.get_y(),
                  PAGE_WIDTH_MM - PAGE_MARGIN_MM, self.get_y())
        self.ln(2)
        self.set_font(FONT_FAMILY, "", 7)
        self.set_text_color(*self.theme.text_medium)

        if self.frontmatter.get("confidential"):
            self.cell(CONTENT_WIDTH_MM / 2, 5, "CONFIDENTIAL")
            self.cell(CONTENT_WIDTH_MM / 2, 5, f"{self.page_no()} / {{nb}}", align="R")
        else:
            self.cell(0, 5, f"{self.page_no()} / {{nb}}", align="R")

    def cover_page(self):
        """Generate a cover page from frontmatter metadata."""
        fm = self.frontmatter
        if not fm.get("cover", False):
            return

        self._is_cover = True
        self.add_page()
        self.ln(30)

        # Top bar
        self.set_fill_color(*self.theme.primary)
        self.rect(0, 0, PAGE_WIDTH_MM, 8, "F")

        # Confidential badge
        if fm.get("confidential"):
            self.set_font(FONT_FAMILY, "B", 11)
            self.set_text_color(*self.theme.accent_red)
            self.cell(0, 8, "CONFIDENTIAL", align="C",
                      new_x="LMARGIN", new_y="NEXT")
            self.ln(3)

        # Title
        title = fm.get("title", "")
        if title:
            self.set_font(FONT_FAMILY, "B", 28)
            self.set_text_color(*self.theme.primary)
            self.cell(0, 15, title, align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

        # Subtitle
        subtitle = fm.get("subtitle", "")
        if subtitle:
            self.set_font(FONT_FAMILY, "", 11)
            self.set_text_color(*self.theme.text_medium)
            self.cell(0, 8, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(12)

        # Separator line
        self.set_draw_color(*self.theme.primary)
        self.set_line_width(0.5)
        self.line(60, self.get_y(), 150, self.get_y())
        self.set_line_width(0.2)
        self.ln(15)

        # Metadata info
        info_fields = [
            ("document_number", "文書番号"),
            ("date", "発行日"),
            ("recipient", "宛先"),
            ("company", "発行元"),
            ("author", "担当"),
        ]
        for key, label in info_fields:
            val = fm.get(key, "")
            if not val:
                continue
            self.set_x(50)
            self.set_font(FONT_FAMILY, "B", 10)
            self.set_text_color(*self.theme.primary)
            self.cell(35, 7, label)
            self.set_font(FONT_FAMILY, "", 10)
            self.set_text_color(*self.theme.text_dark)
            self.cell(75, 7, str(val), new_x="LMARGIN", new_y="NEXT")

        # Bottom bar
        self.set_fill_color(*self.theme.primary)
        self.rect(0, 289, PAGE_WIDTH_MM, 8, "F")

        self._is_cover = False

    def section_title(self, text: str):
        """Render H1 heading."""
        self.set_font(FONT_FAMILY, "B", 14)
        self.set_text_color(*self.theme.primary)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.theme.primary)
        self.line(PAGE_MARGIN_MM, self.get_y(),
                  PAGE_WIDTH_MM - PAGE_MARGIN_MM, self.get_y())
        self.ln(5)

    def sub_title(self, text: str):
        """Render H2 heading."""
        self.set_font(FONT_FAMILY, "B", 11)
        self.set_text_color(*self.theme.primary)
        self.ln(2)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_sub_title(self, text: str):
        """Render H3 heading."""
        self.set_font(FONT_FAMILY, "B", 10)
        self.set_text_color(*self.theme.primary)
        self.ln(1)
        self.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text: str):
        """Render body paragraph with inline markdown support."""
        self.set_font(FONT_FAMILY, "", 9.5)
        self.set_text_color(*self.theme.text_dark)
        self.multi_cell(0, 5.5, text, markdown=True)
        self.ln(2)

    def bullet_list(self, items: List[str]):
        """Render bulleted list."""
        self.set_font(FONT_FAMILY, "", 9)
        self.set_text_color(*self.theme.text_dark)
        for item in items:
            x = self.get_x()
            self.cell(5, 5, "\u30fb", new_x="END")
            self.cell(2)
            self.multi_cell(0, 5, item, markdown=True)
            self.set_x(x)
        self.ln(2)

    def code_block(self, code: str):
        """Render a code block with monospace font and gray background."""
        self.set_font(FONT_FAMILY, "", 8)
        self.set_text_color(*self.theme.text_dark)
        self.set_fill_color(*self.theme.gray_light)

        # Calculate height
        lines = code.split("\n")
        block_height = len(lines) * 4.5 + 6

        # Background
        y_start = self.get_y()
        if y_start + block_height > self.h - 25:
            self.add_page()
            y_start = self.get_y()

        self.rect(PAGE_MARGIN_MM, y_start, CONTENT_WIDTH_MM, block_height, "F")
        self.set_xy(PAGE_MARGIN_MM + 3, y_start + 3)

        for line in lines:
            self.cell(0, 4.5, line, new_x="LMARGIN", new_y="NEXT")
            self.set_x(PAGE_MARGIN_MM + 3)

        self.set_y(y_start + block_height + 2)
        self.ln(2)

    def horizontal_rule(self):
        """Render a horizontal rule (thematic break)."""
        y = self.get_y()
        self.set_draw_color(*self.theme.text_medium)
        self.set_line_width(0.3)
        self.line(PAGE_MARGIN_MM, y, PAGE_WIDTH_MM - PAGE_MARGIN_MM, y)
        self.set_line_width(0.2)
        self.ln(5)

    def render_info_table(self, headers: List[str], rows: List[List[str]]):
        """Render a 2-column info table with alternating row colors."""
        col_widths = _compute_col_widths(self, headers, rows)

        header_style = FontFace(
            color=DeviceRGB(*[c / 255 for c in self.theme.table_header_fg]),
            fill_color=DeviceRGB(*[c / 255 for c in self.theme.primary]),
            emphasis="BOLD",
            size_pt=9,
        )

        with self.table(
            borders_layout=TableBordersLayout.NONE,
            cell_fill_color=DeviceRGB(*[c / 255 for c in self.theme.primary_light]),
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=header_style,
            line_height=self.font_size * 1.8,
        ) as table:
            # Header row
            row = table.row()
            for h in headers:
                row.cell(h)
            # Data rows
            for data_row in rows:
                row = table.row()
                for cell_val in data_row:
                    row.cell(cell_val)
        self.ln(3)

    def render_data_table(self, headers: List[str], rows: List[List[str]]):
        """Render a multi-column data table with header styling."""
        col_widths = _compute_col_widths(self, headers, rows)

        header_style = FontFace(
            color=DeviceRGB(*[c / 255 for c in self.theme.table_header_fg]),
            fill_color=DeviceRGB(*[c / 255 for c in self.theme.table_header_bg]),
            emphasis="BOLD",
            size_pt=8,
        )

        with self.table(
            borders_layout=TableBordersLayout.NONE,
            cell_fill_color=DeviceRGB(*[c / 255 for c in self.theme.table_row_alt]),
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=header_style,
            line_height=self.font_size * 1.8,
        ) as table:
            # Header row
            row = table.row()
            for h in headers:
                row.cell(h)
            # Data rows
            for data_row in rows:
                row = table.row()
                for cell_val in data_row:
                    row.cell(cell_val)
        self.ln(3)

    def embed_image(self, image_path: str):
        """Embed an image, fitting within content width."""
        if not Path(image_path).exists():
            self.body_text(f"[Image not found: {image_path}]")
            return
        self.image(image_path, x=PAGE_MARGIN_MM, w=CONTENT_WIDTH_MM)
        self.ln(5)


# ============================================================
# Column width computation
# ============================================================

def _compute_col_widths(pdf: FPDF, headers: List[str], rows: List[List[str]]) -> List[float]:
    """Compute proportional column widths based on content."""
    num_cols = len(headers)
    if num_cols == 0:
        return []

    # Measure max string width per column
    pdf.set_font(FONT_FAMILY, "", 9)
    max_widths = []
    for i in range(num_cols):
        header_w = pdf.get_string_width(headers[i]) + 4
        col_max = header_w
        for row in rows:
            if i < len(row):
                cell_w = pdf.get_string_width(row[i]) + 4
                col_max = max(col_max, cell_w)
        max_widths.append(col_max)

    # Cap and proportionally distribute
    total = sum(max_widths)
    if total == 0:
        return [CONTENT_WIDTH_MM / num_cols] * num_cols

    return [w / total * CONTENT_WIDTH_MM for w in max_widths]


# ============================================================
# FPDFRenderer — walk mistune AST and call ProfessionalPDF methods
# ============================================================

class FPDFRenderer:
    """Renders mistune AST tokens to a ProfessionalPDF instance."""

    def __init__(self, pdf: ProfessionalPDF):
        self.pdf = pdf
        self._next_table_style = "data"  # "data" or "info"

    def render(self, tokens: List[Dict]):
        """Walk all top-level tokens."""
        i = 0
        while i < len(tokens):
            token = tokens[i]
            ttype = token["type"]

            # Check for HTML comment directives
            if ttype == "paragraph":
                text = extract_text(token.get("children", []))
                stripped = text.strip()

                # Pagebreak
                if "<!-- pagebreak -->" in stripped or "<!--pagebreak-->" in stripped:
                    self.pdf.add_page()
                    i += 1
                    continue

                # Info-table directive
                if "<!-- info-table -->" in stripped or "<!--info-table-->" in stripped:
                    self._next_table_style = "info"
                    i += 1
                    continue

            # Also check block_html for comments
            if ttype == "block_html":
                raw = token.get("raw", token.get("children", ""))
                if isinstance(raw, str):
                    if "<!-- pagebreak -->" in raw or "<!--pagebreak-->" in raw:
                        self.pdf.add_page()
                        i += 1
                        continue
                    if "<!-- info-table -->" in raw or "<!--info-table-->" in raw:
                        self._next_table_style = "info"
                        i += 1
                        continue

            self._render_token(token)
            i += 1

    def _render_token(self, token: Dict):
        ttype = token["type"]

        if ttype == "heading":
            level = token["attrs"]["level"]
            text = extract_text(token["children"])
            if level == 1:
                self.pdf.section_title(text)
            elif level == 2:
                self.pdf.sub_title(text)
            else:
                self.pdf.sub_sub_title(text)

        elif ttype == "paragraph":
            text = children_to_markdown(token.get("children", []))
            self.pdf.body_text(text)

        elif ttype == "list":
            items = self._extract_list_items(token)
            self.pdf.bullet_list(items)

        elif ttype == "block_code":
            info = token.get("attrs", {}).get("info", "")
            raw = token.get("raw", token.get("children", ""))
            if isinstance(raw, list):
                raw = extract_text(raw)

            if info == "mermaid":
                self._render_mermaid(raw)
            else:
                self.pdf.code_block(raw)

        elif ttype == "table":
            self._render_table(token)

        elif ttype == "thematic_break":
            self.pdf.horizontal_rule()

        elif ttype == "block_html":
            # Already handled pagebreak/info-table in render() loop
            pass

        elif ttype == "blank_line":
            pass

    def _extract_list_items(self, list_token: Dict) -> List[str]:
        items = []
        for child in list_token.get("children", []):
            if child["type"] == "list_item":
                item_children = child.get("children", [])
                parts = []
                for sub in item_children:
                    if sub["type"] == "paragraph":
                        parts.append(children_to_markdown(sub.get("children", [])))
                    elif sub["type"] == "block_text":
                        parts.append(children_to_markdown(sub.get("children", [])))
                    elif "children" in sub:
                        if isinstance(sub["children"], list):
                            parts.append(children_to_markdown(sub["children"]))
                        else:
                            parts.append(str(sub["children"]))
                items.append(" ".join(parts))
        return items

    def _render_table(self, table_token: Dict):
        """Parse table AST and render using appropriate table style."""
        headers = []
        rows = []

        for child in table_token.get("children", []):
            if child["type"] == "table_head":
                for cell_or_row in child.get("children", []):
                    if cell_or_row["type"] == "table_cell":
                        # mistune 3.x: table_cell directly under table_head
                        headers.append(extract_text(cell_or_row.get("children", [])))
                    elif cell_or_row["type"] == "table_row":
                        # Compatibility: table_row wrapper around table_cells
                        for cell_token in cell_or_row.get("children", []):
                            if cell_token["type"] == "table_cell":
                                headers.append(extract_text(cell_token.get("children", [])))
            elif child["type"] == "table_body":
                for row_token in child.get("children", []):
                    if row_token["type"] == "table_row":
                        row_cells = []
                        for cell_token in row_token.get("children", []):
                            if cell_token["type"] == "table_cell":
                                row_cells.append(extract_text(cell_token.get("children", [])))
                        rows.append(row_cells)

        if not headers:
            return

        # Determine style and reset
        style = self._next_table_style
        self._next_table_style = "data"

        if style == "info":
            self.pdf.render_info_table(headers, rows)
        else:
            self.pdf.render_data_table(headers, rows)

    def _render_mermaid(self, code: str):
        """Attempt to convert Mermaid to image; fall back to code block."""
        mermaid_script = _SCRIPT_DIR / "mermaid_to_image.py"
        if not mermaid_script.exists():
            self.pdf.code_block(code)
            return

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                [sys.executable, str(mermaid_script), "--code", code, tmp_path],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0 and Path(tmp_path).exists() and Path(tmp_path).stat().st_size > 0:
                self.pdf.embed_image(tmp_path)
            else:
                self.pdf.code_block(code)
        except (subprocess.TimeoutExpired, Exception):
            self.pdf.code_block(code)
        finally:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except Exception:
                pass


# ============================================================
# Public API
# ============================================================

def render_pdf(
    markdown_text: str,
    output_path: str,
    frontmatter: Optional[Dict] = None,
    theme_name: Optional[str] = None,
    confidential: bool = False,
    no_cover: bool = False,
    font_regular: Optional[str] = None,
    font_bold: Optional[str] = None,
) -> str:
    """Render Markdown text to a professional PDF.

    Args:
        markdown_text: Markdown body (frontmatter already stripped).
        output_path: Output PDF file path.
        frontmatter: Pre-parsed frontmatter dict (overrides in-text frontmatter).
        theme_name: Theme name override (overrides frontmatter theme).
        confidential: Force confidential mode.
        no_cover: Suppress cover page even if frontmatter says cover: true.
        font_regular: Explicit regular font path.
        font_bold: Explicit bold font path.

    Returns:
        The output file path.
    """
    # Parse frontmatter from text if not provided
    if frontmatter is None:
        frontmatter, markdown_text = parse_frontmatter(markdown_text)

    # Resolve theme
    effective_theme = theme_name or frontmatter.get("theme", "navy")
    theme = get_theme(effective_theme)

    # Apply overrides
    if confidential:
        frontmatter["confidential"] = True
    if no_cover:
        frontmatter["cover"] = False

    # Discover fonts
    fr, fb = discover_fonts(font_regular, font_bold)

    # Create PDF
    pdf = ProfessionalPDF(theme=theme, frontmatter=frontmatter,
                          font_regular=fr, font_bold=fb)
    pdf.alias_nb_pages()

    # Cover page
    pdf.cover_page()

    # Content pages
    pdf.add_page()

    # Parse and render
    tokens = parse_markdown(markdown_text)
    renderer = FPDFRenderer(pdf)
    renderer.render(tokens)

    # Output
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pdf.output(output_path)
    return output_path


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown to Professional PDF (fpdf2)"
    )
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("output", help="Output PDF file")
    parser.add_argument("--theme", choices=["navy", "gray"], default=None,
                        help="Color theme (default: from frontmatter or navy)")
    parser.add_argument("--confidential", action="store_true",
                        help="Mark document as confidential")
    parser.add_argument("--no-cover", action="store_true",
                        help="Suppress cover page")
    parser.add_argument("--font-regular", default=None,
                        help="Path to regular weight CJK font (.ttc/.ttf/.otf)")
    parser.add_argument("--font-bold", default=None,
                        help="Path to bold weight CJK font (.ttc/.ttf/.otf)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)

    output = render_pdf(
        markdown_text=body,
        output_path=args.output,
        frontmatter=frontmatter,
        theme_name=args.theme,
        confidential=args.confidential,
        no_cover=args.no_cover,
        font_regular=args.font_regular,
        font_bold=args.font_bold,
    )

    print(f"Generated: {output}")


if __name__ == "__main__":
    main()
