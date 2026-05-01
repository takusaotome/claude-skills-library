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
import sys
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

# Paper sizes (width, height in mm + fpdf2 format string).
# Default is US Letter (8.5" × 11"); A4 remains available via --paper-size.
PAPER_SIZES = {
    "letter": {"width": 215.9, "height": 279.4, "fpdf_format": "Letter"},
    "a4": {"width": 210.0, "height": 297.0, "fpdf_format": "A4"},
}
DEFAULT_PAPER_SIZE = "letter"

PAGE_MARGIN_MM = 10
PAGE_WIDTH_MM = PAPER_SIZES[DEFAULT_PAPER_SIZE]["width"]
PAGE_HEIGHT_MM = PAPER_SIZES[DEFAULT_PAPER_SIZE]["height"]
CONTENT_WIDTH_MM = PAGE_WIDTH_MM - 2 * PAGE_MARGIN_MM


def set_paper_size(size: str) -> None:
    """Update module-level page dimensions for the given paper size."""
    global PAGE_WIDTH_MM, PAGE_HEIGHT_MM, CONTENT_WIDTH_MM
    if size not in PAPER_SIZES:
        raise ValueError(f"Unknown paper size: {size}. Use one of {list(PAPER_SIZES.keys())}.")
    PAGE_WIDTH_MM = PAPER_SIZES[size]["width"]
    PAGE_HEIGHT_MM = PAPER_SIZES[size]["height"]
    CONTENT_WIDTH_MM = PAGE_WIDTH_MM - 2 * PAGE_MARGIN_MM


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
    body = text[match.end() :]
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
            inner = (
                children_to_markdown(child["children"]) if isinstance(child["children"], list) else child["children"]
            )
            parts.append(f"**{inner}**")
        elif ctype == "emphasis":
            inner = (
                children_to_markdown(child["children"]) if isinstance(child["children"], list) else child["children"]
            )
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

    def __init__(
        self,
        theme: Theme,
        frontmatter: Optional[Dict] = None,
        font_regular: str = "",
        font_bold: str = "",
        paper_size: str = DEFAULT_PAPER_SIZE,
    ):
        if paper_size not in PAPER_SIZES:
            raise ValueError(f"Unknown paper size: {paper_size}. Use one of {list(PAPER_SIZES.keys())}.")
        super().__init__(orientation="P", unit="mm", format=PAPER_SIZES[paper_size]["fpdf_format"])
        self.paper_size = paper_size
        self.theme = theme
        self.frontmatter = frontmatter or {}
        self._is_cover = False

        # Register fonts — all 4 styles to avoid 'Undefined font' on markdown=True
        self.add_font(FONT_FAMILY, "", font_regular)
        self.add_font(FONT_FAMILY, "B", font_bold)
        self.add_font(FONT_FAMILY, "I", font_regular)  # Map italic to regular
        self.add_font(FONT_FAMILY, "BI", font_bold)  # Map bold-italic to bold

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
        self.line(PAGE_MARGIN_MM, self.get_y(), PAGE_WIDTH_MM - PAGE_MARGIN_MM, self.get_y())
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
            self.cell(0, 8, "CONFIDENTIAL", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(3)

        # Title — auto-shrink font to fit page width, wrap if still too long
        title = fm.get("title", "")
        if title:
            self.set_text_color(*self.theme.primary)
            max_w = CONTENT_WIDTH_MM - 10  # 5mm padding each side
            font_size = 28
            min_font_size = 16
            self.set_font(FONT_FAMILY, "B", font_size)
            while self.get_string_width(title) > max_w and font_size > min_font_size:
                font_size -= 1
                self.set_font(FONT_FAMILY, "B", font_size)
            if self.get_string_width(title) > max_w:
                # Still too long after shrinking — use multi_cell to wrap
                line_h = font_size * 0.55
                self.multi_cell(0, line_h, title, align="C", new_x="LMARGIN", new_y="NEXT")
            else:
                line_h = max(15, font_size * 0.55)
                self.cell(0, line_h, title, align="C", new_x="LMARGIN", new_y="NEXT")
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

        # Metadata info — detect language from frontmatter
        _lang = fm.get("lang", "").lower()
        if not _lang:
            # Auto-detect: if title contains CJK characters, assume Japanese
            _title = fm.get("title", "")
            _lang = "ja" if any("\u3000" <= ch <= "\u9fff" for ch in _title) else "en"
        if _lang == "ja":
            info_fields = [
                ("document_number", "文書番号"),
                ("date", "発行日"),
                ("recipient", "宛先"),
                ("company", "発行元"),
                ("author", "担当"),
            ]
        else:
            info_fields = [
                ("document_number", "Document No."),
                ("date", "Date"),
                ("recipient", "To"),
                ("company", "Issued by"),
                ("author", "Prepared by"),
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
        self.rect(0, PAGE_HEIGHT_MM - 8, PAGE_WIDTH_MM, 8, "F")

        self._is_cover = False

    def _auto_fit_heading(self, text: str, max_size: int, min_size: int, line_h: float):
        """Render a heading, auto-shrinking font to fit in one line."""
        font_size = max_size
        self.set_font(FONT_FAMILY, "B", font_size)
        while self.get_string_width(text) > CONTENT_WIDTH_MM and font_size > min_size:
            font_size -= 0.5
            self.set_font(FONT_FAMILY, "B", font_size)
        actual_line_h = max(line_h, font_size * 0.5)
        self.cell(0, actual_line_h, text, new_x="LMARGIN", new_y="NEXT")

    def section_title(self, text: str):
        """Render H1 heading."""
        self.set_text_color(*self.theme.primary)
        self._auto_fit_heading(text, max_size=14, min_size=9, line_h=10)
        self.set_draw_color(*self.theme.primary)
        self.line(PAGE_MARGIN_MM, self.get_y(), PAGE_WIDTH_MM - PAGE_MARGIN_MM, self.get_y())
        self.ln(5)

    def sub_title(self, text: str):
        """Render H2 heading."""
        self.set_text_color(*self.theme.primary)
        self.ln(2)
        self._auto_fit_heading(text, max_size=11, min_size=8, line_h=8)
        self.ln(2)

    def sub_sub_title(self, text: str):
        """Render H3 heading."""
        self.set_text_color(*self.theme.primary)
        self.ln(1)
        self._auto_fit_heading(text, max_size=10, min_size=7, line_h=7)
        self.ln(1)

    def body_text(self, text: str):
        """Render body paragraph with inline markdown support."""
        self.set_font(FONT_FAMILY, "", 9.5)
        self.set_text_color(*self.theme.text_dark)
        self.multi_cell(0, 5.5, text, markdown=True, align="L", wrapmode="CHAR")
        self.ln(2)

    def bullet_list(self, items: List[str]):
        """Render bulleted list."""
        self.set_font(FONT_FAMILY, "", 9)
        self.set_text_color(*self.theme.text_dark)
        for item in items:
            x = self.get_x()
            self.cell(5, 5, "\u30fb", new_x="END")
            self.cell(2)
            self.multi_cell(0, 5, item, markdown=True, align="L", wrapmode="CHAR")
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

    def quote_block(self, paragraphs: List[str]):
        """Render a block quote with left accent bar, light fill, and indented italic-styled text.

        Args:
            paragraphs: List of paragraph strings (already markdown-formatted).
                        Each item becomes one paragraph inside the quote block.
        """
        if not paragraphs:
            return

        bar_w = 1.2  # accent bar width in mm
        pad_l = 4.0  # left padding inside block (after bar)
        pad_r = 3.0
        pad_v = 2.5  # vertical padding (top and bottom)
        line_h = 5.0
        font_size = 9.5

        # Calculate inner content width
        inner_w = CONTENT_WIDTH_MM - bar_w - pad_l - pad_r

        # Pre-measure: estimate total height by counting wrapped lines per paragraph
        self.set_font(FONT_FAMILY, "I", font_size)
        total_lines = 0
        for p in paragraphs:
            try:
                # fpdf2 ≥2.7.4: dry_run=True, output="LINES" returns wrapped lines
                wrapped = self.multi_cell(
                    inner_w, line_h, p, markdown=True, dry_run=True, output="LINES", wrapmode="CHAR"
                )
                total_lines += max(1, len(wrapped))
            except TypeError:
                # Fallback for older fpdf2 versions
                try:
                    wrapped = self.multi_cell(inner_w, line_h, p, markdown=True, split_only=True, wrapmode="CHAR")
                    total_lines += max(1, len(wrapped))
                except Exception:
                    total_lines += max(1, (len(p) // 60) + 1)
            except Exception:
                total_lines += max(1, (len(p) // 60) + 1)
        # Add inter-paragraph spacing (small gap between paragraphs)
        gap_lines = max(0, len(paragraphs) - 1) * 0.4
        block_h = pad_v * 2 + (total_lines + gap_lines) * line_h

        # Page break if not enough space
        if self.get_y() + block_h > self.h - 25:
            self.add_page()

        y_start = self.get_y()

        # Background fill (light gray)
        self.set_fill_color(*self.theme.gray_light)
        self.rect(PAGE_MARGIN_MM, y_start, CONTENT_WIDTH_MM, block_h, "F")

        # Left accent bar (theme primary color)
        self.set_fill_color(*self.theme.primary)
        self.rect(PAGE_MARGIN_MM, y_start, bar_w, block_h, "F")

        # Render text content
        self.set_xy(PAGE_MARGIN_MM + bar_w + pad_l, y_start + pad_v)
        self.set_font(FONT_FAMILY, "I", font_size)
        self.set_text_color(*self.theme.text_dark)
        for idx, p in enumerate(paragraphs):
            self.set_x(PAGE_MARGIN_MM + bar_w + pad_l)
            self.multi_cell(inner_w, line_h, p, markdown=True, align="L", wrapmode="CHAR")
            if idx < len(paragraphs) - 1:
                self.ln(line_h * 0.4)

        # Move below the block
        self.set_y(y_start + block_h)
        self.ln(2)

    def render_info_table(self, headers: List[str], rows: List[List[str]], col_widths_override=None):
        """Render a 2-column info table with alternating row colors."""
        if col_widths_override is not None:
            col_widths = _apply_col_widths_override(col_widths_override, len(headers))
        else:
            col_widths = _compute_col_widths(self, headers, rows)

        header_style = FontFace(
            color=DeviceRGB(*[c / 255 for c in self.theme.table_header_fg]),
            fill_color=DeviceRGB(*[c / 255 for c in self.theme.primary]),
            emphasis="BOLD",
            size_pt=9,
        )

        # Reset PDF state so _initial_style captures clean colors.
        # font_face() captures current fill_color as the base for non-filled rows.
        self.set_fill_color(*self.theme.white)
        self.set_text_color(*self.theme.text_dark)
        self.set_font(FONT_FAMILY, "", 9)

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

    def render_data_table(
        self, headers: List[str], rows: List[List[str]], col_aligns: List[str] = None, col_widths_override=None
    ):
        """Render a multi-column data table with header styling and column alignment."""
        if col_widths_override is not None:
            col_widths = _apply_col_widths_override(col_widths_override, len(headers))
        else:
            col_widths = _compute_col_widths(self, headers, rows)

        # Default alignment: all left
        if not col_aligns:
            col_aligns = ["L"] * len(headers)
        # Pad if shorter than headers
        while len(col_aligns) < len(headers):
            col_aligns.append("L")

        header_style = FontFace(
            color=DeviceRGB(*[c / 255 for c in self.theme.table_header_fg]),
            fill_color=DeviceRGB(*[c / 255 for c in self.theme.table_header_bg]),
            emphasis="BOLD",
            size_pt=8,
        )

        # Reset PDF state so _initial_style captures clean colors.
        # font_face() captures current fill_color as the base for non-filled rows.
        self.set_fill_color(*self.theme.white)
        self.set_text_color(*self.theme.text_dark)
        self.set_font(FONT_FAMILY, "", 8)

        with self.table(
            borders_layout=TableBordersLayout.NONE,
            cell_fill_color=DeviceRGB(*[c / 255 for c in self.theme.table_row_alt]),
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=col_widths,
            headings_style=header_style,
            line_height=self.font_size * 1.8,
            text_align="L",
        ) as table:
            # Header row
            row = table.row()
            for i, h in enumerate(headers):
                row.cell(h, align=col_aligns[i])
            # Data rows
            for data_row in rows:
                row = table.row()
                for i, cell_val in enumerate(data_row):
                    align = col_aligns[i] if i < len(col_aligns) else "L"
                    row.cell(cell_val, align=align)
        self.ln(3)

    def embed_image(self, image_path: str):
        """Embed an image, fitting within content width and page height."""
        if not Path(image_path).exists():
            self.body_text(f"[Image not found: {image_path}]")
            return
        # Calculate image dimensions to fit within page
        from PIL import Image as PILImage

        try:
            with PILImage.open(image_path) as img:
                img_w_px, img_h_px = img.size
        except Exception:
            self.image(image_path, x=PAGE_MARGIN_MM, w=CONTENT_WIDTH_MM)
            self.ln(5)
            return

        # Scale to content width first
        scale = CONTENT_WIDTH_MM / img_w_px
        render_w = CONTENT_WIDTH_MM
        render_h = img_h_px * scale

        # Max usable height on a page (Letter=279.4mm / A4=297mm, top/bottom margins ~20mm each)
        max_page_h = PAGE_HEIGHT_MM - 20 - 20
        if render_h > max_page_h:
            # Scale down to fit within max page height
            render_h = max_page_h
            render_w = img_w_px * (max_page_h / img_h_px)
            # Center horizontally if narrower than content width
            x = PAGE_MARGIN_MM + (CONTENT_WIDTH_MM - render_w) / 2
        else:
            x = PAGE_MARGIN_MM

        # Check if image fits on remaining space of current page
        available_h = PAGE_HEIGHT_MM - self.get_y() - 15  # 15mm bottom margin
        if render_h > available_h:
            self.add_page()

        self.image(image_path, x=x, w=render_w, h=render_h)
        self.ln(5)


# ============================================================
# Column width computation
# ============================================================


def _apply_col_widths_override(values: List[float], num_cols: int) -> List[float]:
    """Convert a list of relative width values (any unit) into mm widths summing to CONTENT_WIDTH_MM.

    If len(values) != num_cols, pad or truncate to match.
    """
    if not values:
        return [CONTENT_WIDTH_MM / num_cols] * num_cols
    if len(values) < num_cols:
        # pad with remaining share distributed equally
        deficit = num_cols - len(values)
        total_known = sum(values)
        avg = total_known / len(values) if values else 1.0
        values = values + [avg] * deficit
    elif len(values) > num_cols:
        values = values[:num_cols]
    total = sum(values)
    if total <= 0:
        return [CONTENT_WIDTH_MM / num_cols] * num_cols
    return [v / total * CONTENT_WIDTH_MM for v in values]


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

    def __init__(self, pdf: ProfessionalPDF, strict_mermaid: bool = True, debug_mermaid: bool = False):
        self.pdf = pdf
        self._next_table_style = "data"  # "data" or "info"
        self._next_col_widths = None  # Optional[List[float]] — ratios for next table
        self._strict_mermaid = strict_mermaid
        self._debug_mermaid = debug_mermaid
        self._mermaid_success = 0
        self._mermaid_failure = 0
        self._mermaid_renderer = None  # lazy init — shared across document

    @staticmethod
    def _parse_col_widths_directive(text: str):
        """Parse '<!-- col-widths: 10,45,45 -->' → [10.0, 45.0, 45.0].

        Accepts bare numbers, percentages (10%), or numbers followed by 'mm'.
        Returns None if parse fails.
        """
        import re as _re

        m = _re.search(r"col-widths\s*:\s*([0-9.,\s%mM]+)", text)
        if not m:
            return None
        raw = m.group(1)
        parts = [p.strip().rstrip("%mM").strip() for p in raw.split(",") if p.strip()]
        try:
            values = [float(p) for p in parts]
        except ValueError:
            return None
        if not values or any(v <= 0 for v in values):
            return None
        return values

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

                # Col-widths directive: <!-- col-widths: 10,45,45 -->
                if "col-widths" in stripped and "<!--" in stripped:
                    cw = self._parse_col_widths_directive(stripped)
                    if cw is not None:
                        self._next_col_widths = cw
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
                    if "col-widths" in raw:
                        cw = self._parse_col_widths_directive(raw)
                        if cw is not None:
                            self._next_col_widths = cw
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
            children = token.get("children", [])
            # Check if paragraph contains a single image token
            if len(children) == 1 and children[0].get("type") == "image":
                img_url = children[0].get("attrs", {}).get("url", "")
                if img_url:
                    self.pdf.embed_image(img_url)
            else:
                text = children_to_markdown(children)
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

        elif ttype == "block_quote":
            self._render_block_quote(token)

        elif ttype == "thematic_break":
            self.pdf.horizontal_rule()

        elif ttype == "block_html":
            # Already handled pagebreak/info-table in render() loop
            pass

        elif ttype == "blank_line":
            pass

    def _render_block_quote(self, quote_token: Dict):
        """Render a markdown block_quote (lines starting with `> `).

        Mistune produces a block_quote token whose children are typically
        paragraph tokens. Each paragraph becomes one entry in the
        quote_block paragraphs list. Non-paragraph children (e.g. nested
        lists) are flattened into markdown text as a best-effort fallback.
        """
        paragraphs: List[str] = []
        for child in quote_token.get("children", []):
            ctype = child.get("type")
            if ctype == "paragraph":
                paragraphs.append(children_to_markdown(child.get("children", [])))
            elif ctype == "blank_line":
                continue
            elif ctype == "block_quote":
                # Nested blockquote — render inline by recursion-like flattening
                self._render_block_quote(child)
            elif ctype == "list":
                # Flatten list items into bullet-prefixed lines
                items = self._extract_list_items(child)
                for it in items:
                    paragraphs.append(f"・ {it}")
            elif ctype == "block_code":
                raw = child.get("raw", child.get("children", ""))
                if isinstance(raw, list):
                    raw = extract_text(raw)
                paragraphs.append(str(raw))
            elif "children" in child and isinstance(child["children"], list):
                paragraphs.append(children_to_markdown(child["children"]))
        if paragraphs:
            self.pdf.quote_block(paragraphs)

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
        col_aligns = []

        for child in table_token.get("children", []):
            if child["type"] == "table_head":
                for cell_or_row in child.get("children", []):
                    if cell_or_row["type"] == "table_cell":
                        # mistune 3.x: table_cell directly under table_head
                        headers.append(extract_text(cell_or_row.get("children", [])))
                        attrs = cell_or_row.get("attrs", {}) or {}
                        col_aligns.append(attrs.get("align") or attrs.get("style", ""))
                    elif cell_or_row["type"] == "table_row":
                        # Compatibility: table_row wrapper around table_cells
                        for cell_token in cell_or_row.get("children", []):
                            if cell_token["type"] == "table_cell":
                                headers.append(extract_text(cell_token.get("children", [])))
                                attrs = cell_token.get("attrs", {}) or {}
                                col_aligns.append(attrs.get("align") or attrs.get("style", ""))
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

        # Normalize alignment strings to fpdf2 align values
        normalized_aligns = []
        for a in col_aligns:
            a_str = str(a).lower() if a else ""
            if "right" in a_str:
                normalized_aligns.append("R")
            elif "center" in a_str:
                normalized_aligns.append("C")
            else:
                normalized_aligns.append("L")

        # Determine style and reset
        style = self._next_table_style
        col_widths_override = self._next_col_widths
        self._next_table_style = "data"
        self._next_col_widths = None

        if style == "info":
            self.pdf.render_info_table(headers, rows, col_widths_override=col_widths_override)
        else:
            self.pdf.render_data_table(
                headers, rows, col_aligns=normalized_aligns, col_widths_override=col_widths_override
            )

    def _render_mermaid(self, code: str):
        """Render Mermaid diagram via MermaidRenderer (in-process).

        In strict mode (default), raises MermaidRenderError on failure.
        In permissive mode, falls back to rendering as a code block.
        """
        if self._mermaid_renderer is None:
            from mermaid_renderer import MermaidBackend, MermaidRenderer

            self._mermaid_renderer = MermaidRenderer(
                backend=MermaidBackend.AUTO,
                output_format="png",
                width=1200,
                debug=self._debug_mermaid,
            )

        result = self._mermaid_renderer.render(code)
        if result.success:
            self._mermaid_success += 1
            self.pdf.embed_image(result.image_path)
        else:
            self._mermaid_failure += 1
            print(
                f"  Mermaid failed: {result.error_category.value}: {result.error_message}",
                file=sys.stderr,
            )
            if result.fix_suggestion:
                print(f"  Fix: {result.fix_suggestion}", file=sys.stderr)
            if self._strict_mermaid:
                from mermaid_renderer import MermaidRenderError

                raise MermaidRenderError(result)
            else:
                self.pdf.code_block(code)

    def report_mermaid_stats(self):
        """Print Mermaid rendering statistics."""
        total = self._mermaid_success + self._mermaid_failure
        if total > 0:
            print(f"Mermaid: {self._mermaid_success}/{total} succeeded, {self._mermaid_failure}/{total} failed")


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
    strict_mermaid: bool = True,
    debug_mermaid: bool = False,
    paper_size: Optional[str] = None,
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
        strict_mermaid: If True (default), raise MermaidRenderError on failure.
        debug_mermaid: If True, print detailed Mermaid debug output.

    Returns:
        The output file path.
    """
    # Parse frontmatter from text if not provided
    if frontmatter is None:
        frontmatter, markdown_text = parse_frontmatter(markdown_text)

    # Resolve theme
    effective_theme = theme_name or frontmatter.get("theme", "navy")
    theme = get_theme(effective_theme)

    # Resolve paper size (CLI override > frontmatter > default)
    effective_paper_size = (paper_size or frontmatter.get("paper_size", DEFAULT_PAPER_SIZE)).lower()
    set_paper_size(effective_paper_size)

    # Apply overrides
    if confidential:
        frontmatter["confidential"] = True
    if no_cover:
        frontmatter["cover"] = False

    # Discover fonts
    fr, fb = discover_fonts(font_regular, font_bold)

    # Create PDF
    pdf = ProfessionalPDF(
        theme=theme, frontmatter=frontmatter, font_regular=fr, font_bold=fb, paper_size=effective_paper_size
    )
    pdf.alias_nb_pages()

    # Cover page
    pdf.cover_page()

    # Content pages
    pdf.add_page()

    # Parse and render
    tokens = parse_markdown(markdown_text)
    renderer = FPDFRenderer(pdf, strict_mermaid=strict_mermaid, debug_mermaid=debug_mermaid)
    renderer.render(tokens)

    # Report Mermaid stats and cleanup cache
    renderer.report_mermaid_stats()
    if renderer._mermaid_renderer is not None:
        renderer._mermaid_renderer.cleanup_cache()

    # Output
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pdf.output(output_path)
    return output_path


# ============================================================
# CLI
# ============================================================


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to Professional PDF (fpdf2)")
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("output", help="Output PDF file")
    parser.add_argument(
        "--theme", choices=["navy", "gray"], default=None, help="Color theme (default: from frontmatter or navy)"
    )
    parser.add_argument("--confidential", action="store_true", help="Mark document as confidential")
    parser.add_argument("--no-cover", action="store_true", help="Suppress cover page")
    parser.add_argument(
        "--paper-size",
        choices=list(PAPER_SIZES.keys()),
        default=None,
        help=f"Paper size (default: {DEFAULT_PAPER_SIZE}; also honors 'paper_size' in YAML frontmatter)",
    )
    parser.add_argument("--font-regular", default=None, help="Path to regular weight CJK font (.ttc/.ttf/.otf)")
    parser.add_argument("--font-bold", default=None, help="Path to bold weight CJK font (.ttc/.ttf/.otf)")
    parser.add_argument(
        "--no-strict-mermaid",
        action="store_true",
        help="Allow Mermaid fallback to code block on failure (default: strict)",
    )
    parser.add_argument("--debug-mermaid", action="store_true", help="Print detailed Mermaid conversion debug output")
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify PDF layout after generation (check for overflow/clipping)",
    )
    parser.add_argument(
        "--verify-save-images",
        action="store_true",
        help="Save page images to /tmp during verification (for debugging)",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)

    try:
        output = render_pdf(
            markdown_text=body,
            output_path=args.output,
            frontmatter=frontmatter,
            theme_name=args.theme,
            confidential=args.confidential,
            no_cover=args.no_cover,
            font_regular=args.font_regular,
            font_bold=args.font_bold,
            strict_mermaid=not args.no_strict_mermaid,
            debug_mermaid=args.debug_mermaid,
            paper_size=args.paper_size,
        )
        print(f"Generated: {output}")

        # Post-generation layout verification
        if args.verify or args.verify_save_images:
            try:
                from verify_pdf_layout import verify_pdf

                warnings = verify_pdf(
                    output,
                    save_images=args.verify_save_images,
                )
                if warnings:
                    print(f"\n⚠ Layout verification ({len(warnings)} issues):", file=sys.stderr)
                    for w in warnings:
                        print(f"  - {w}", file=sys.stderr)
                else:
                    print("✓ Layout verification passed — no overflow detected")
            except ImportError:
                print(
                    "Warning: PyMuPDF not installed, skipping layout verification. Run: pip install PyMuPDF",
                    file=sys.stderr,
                )
    except Exception as e:
        # Catch MermaidRenderError (and any other render errors) at CLI boundary
        err_name = type(e).__name__
        print(f"Error ({err_name}): {e}", file=sys.stderr)
        # Provide fix suggestion if available
        if hasattr(e, "result") and hasattr(e.result, "fix_suggestion") and e.result.fix_suggestion:
            print(f"Fix: {e.result.fix_suggestion}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
