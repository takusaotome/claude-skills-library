#!/usr/bin/env python3
"""
Theme definitions and font discovery for Professional PDF generation.

Provides color themes (navy, gray) and cross-platform CJK font discovery
for use with fpdf2-based PDF rendering.
"""

import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


@dataclass
class Theme:
    """Color theme definition for professional PDF documents."""

    name: str

    # Primary colors
    primary: Tuple[int, int, int] = (0, 51, 102)
    primary_light: Tuple[int, int, int] = (230, 238, 247)

    # Text colors
    text_dark: Tuple[int, int, int] = (34, 34, 34)
    text_medium: Tuple[int, int, int] = (100, 100, 100)

    # Table colors
    table_header_bg: Tuple[int, int, int] = (0, 51, 102)
    table_header_fg: Tuple[int, int, int] = (255, 255, 255)
    table_row_alt: Tuple[int, int, int] = (230, 238, 247)

    # Accent colors
    accent_red: Tuple[int, int, int] = (180, 40, 40)
    accent_green: Tuple[int, int, int] = (0, 120, 60)

    # Utility colors
    white: Tuple[int, int, int] = (255, 255, 255)
    gray_light: Tuple[int, int, int] = (240, 240, 240)


# Built-in themes
NAVY_THEME = Theme(
    name="navy",
    primary=(0, 51, 102),
    primary_light=(230, 238, 247),
    text_dark=(34, 34, 34),
    text_medium=(100, 100, 100),
    table_header_bg=(0, 51, 102),
    table_header_fg=(255, 255, 255),
    table_row_alt=(230, 238, 247),
)

GRAY_THEME = Theme(
    name="gray",
    primary=(60, 60, 60),
    primary_light=(240, 240, 240),
    text_dark=(34, 34, 34),
    text_medium=(100, 100, 100),
    table_header_bg=(60, 60, 60),
    table_header_fg=(255, 255, 255),
    table_row_alt=(240, 240, 240),
)

_THEMES = {
    "navy": NAVY_THEME,
    "gray": GRAY_THEME,
}


def get_theme(name: str) -> Theme:
    """Get a theme by name. Raises ValueError for unknown themes."""
    if name not in _THEMES:
        available = ", ".join(_THEMES.keys())
        raise ValueError(f"Unknown theme '{name}'. Available: {available}")
    return _THEMES[name]


def _has_truetype_outlines(font_path: str) -> Optional[bool]:
    """Check if a font file uses TrueType outlines (glyf table).

    Returns:
        True  — glyf table found (TrueType outlines)
        False — CFF/CFF2 found, no glyf (CFF outlines)
        None  — could not determine (fontTools unavailable or parse error)

    Note: For TTC files, only fontNumber=0 is checked. This matches fpdf2's
    default collection_font_number. While it's theoretically possible for
    different faces in a TTC to have different outline formats, this is
    extremely rare in practice.
    """
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    try:
        font = TTFont(font_path, fontNumber=0)
        try:
            if "glyf" in font:
                return True
            if "CFF " in font or "CFF2" in font:
                return False
            return None
        finally:
            font.close()
    except Exception:
        return None


# Font discovery paths per platform
_eu = os.path.expanduser

_MACOS_FONTS = [
    # TrueType candidates (best fpdf2 compatibility)
    (_eu("~/Library/Fonts/UDEVGothic-Regular.ttf"), _eu("~/Library/Fonts/UDEVGothic-Bold.ttf")),
    (_eu("~/Library/Fonts/UDEVGothicJPDOC-Regular.ttf"), _eu("~/Library/Fonts/UDEVGothicJPDOC-Bold.ttf")),
    (_eu("~/Library/Fonts/NotoSansJP-Regular.ttf"), _eu("~/Library/Fonts/NotoSansJP-Bold.ttf")),
    ("/Library/Fonts/NotoSansJP-Regular.ttf", "/Library/Fonts/NotoSansJP-Bold.ttf"),
    (_eu("~/Library/Fonts/NotoSansCJK-Regular.ttc"), _eu("~/Library/Fonts/NotoSansCJK-Bold.ttc")),
    ("/Library/Fonts/NotoSansCJK-Regular.ttc", "/Library/Fonts/NotoSansCJK-Bold.ttc"),
    # CFF candidates (fallback — may cause garbled CJK text)
    ("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"),
]

_WINDOWS_FONTS = [
    ("C:/Windows/Fonts/YuGothR.ttc", "C:/Windows/Fonts/YuGothB.ttc"),
    ("C:/Windows/Fonts/yugothic.ttf", "C:/Windows/Fonts/yugothb.ttf"),
    ("C:/Windows/Fonts/msgothic.ttc", "C:/Windows/Fonts/msgothic.ttc"),
]

_LINUX_FONTS = [
    ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
    ("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc"),
    (
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc",
    ),
]


def discover_fonts(
    font_regular: Optional[str] = None,
    font_bold: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Discover CJK fonts for PDF generation.

    If font_regular/font_bold are provided, validates they exist and returns them.
    Otherwise, searches platform-specific paths.

    Args:
        font_regular: Explicit path to regular weight font.
        font_bold: Explicit path to bold weight font.

    Returns:
        Tuple of (regular_font_path, bold_font_path).

    Raises:
        SystemExit: If no suitable fonts are found.
    """
    # Explicit override
    if font_regular or font_bold:
        if not font_regular or not font_bold:
            print("Error: Both --font-regular and --font-bold must be specified together.", file=sys.stderr)
            sys.exit(1)
    if font_regular and font_bold:
        reg_path = Path(font_regular)
        bold_path = Path(font_bold)
        if not reg_path.exists():
            print(f"Error: Font file not found: {font_regular}", file=sys.stderr)
            sys.exit(1)
        if not bold_path.exists():
            print(f"Error: Font file not found: {font_bold}", file=sys.stderr)
            sys.exit(1)
        # Warn about CFF outlines but always accept CLI-specified fonts
        reg_tt = _has_truetype_outlines(font_regular)
        bold_tt = _has_truetype_outlines(font_bold)
        if reg_tt is False or bold_tt is False:
            print(
                "Warning: CFF outlines detected in specified font. "
                "CJK text may render incorrectly with fpdf2. "
                "Proceeding with specified font.",
                file=sys.stderr,
            )
        elif reg_tt is None or bold_tt is None:
            print(
                "Warning: Could not verify font outline type (fontTools not installed or parse error). Proceeding.",
                file=sys.stderr,
            )
        return str(reg_path), str(bold_path)

    # Platform-specific search with TrueType preference
    system = platform.system()
    if system == "Darwin":
        candidates = _MACOS_FONTS
    elif system == "Windows":
        candidates = _WINDOWS_FONTS
    else:
        candidates = _LINUX_FONTS

    cff_fallback = None
    unknown_fallback = None
    for reg, bold in candidates:
        if Path(reg).exists() and Path(bold).exists():
            reg_tt = _has_truetype_outlines(reg)
            bold_tt = _has_truetype_outlines(bold)
            if reg_tt is True and bold_tt is True:
                return reg, bold  # Both TrueType — use immediately
            elif reg_tt is False or bold_tt is False:
                if cff_fallback is None:
                    cff_fallback = (reg, bold)  # CFF found — record as fallback
            else:  # Either is None, neither is False
                if unknown_fallback is None:
                    unknown_fallback = (reg, bold)  # Unknown — record as fallback

    # Fallback priority: CFF > Unknown
    fallback = cff_fallback or unknown_fallback
    if fallback is not None:
        reg, bold = fallback
        if fallback is cff_fallback:
            print(
                "Warning: Using CFF-outline font for PDF generation. "
                "CJK text may render incorrectly with fpdf2.\n"
                "To fix, install a TrueType CJK font:\n"
                "  macOS:   Install UDEVGothic or Noto Sans JP (TTF) to ~/Library/Fonts/\n"
                "  Windows: Yu Gothic is usually TrueType (pre-installed)\n"
                "  Linux:   sudo apt install fonts-noto-cjk (if CFF, use Noto Sans JP TTF)",
                file=sys.stderr,
            )
        else:
            print(
                "Warning: Could not verify font outline type (fontTools not installed or parse error). Proceeding.",
                file=sys.stderr,
            )
        return reg, bold

    # Fail-fast with helpful message
    print(
        "Error: No CJK fonts found for PDF generation.\n"
        "\n"
        "Please specify font paths manually:\n"
        "  --font-regular /path/to/regular.ttc --font-bold /path/to/bold.ttc\n"
        "\n"
        "Recommended TrueType fonts by platform:\n"
        "  macOS:   UDEVGothic or Noto Sans JP (TTF) — install to ~/Library/Fonts/\n"
        "  Windows: Yu Gothic Regular/Bold (pre-installed)\n"
        "  Linux:   Noto Sans CJK Regular/Bold\n"
        "           Install: sudo apt install fonts-noto-cjk",
        file=sys.stderr,
    )
    sys.exit(1)
