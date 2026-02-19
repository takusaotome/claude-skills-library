#!/usr/bin/env python3
"""
Theme definitions and font discovery for Professional PDF generation.

Provides color themes (navy, gray) and cross-platform CJK font discovery
for use with fpdf2-based PDF rendering.
"""

import platform
import sys
from dataclasses import dataclass, field
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


# Font discovery paths per platform
_MACOS_FONTS = [
    ("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
     "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"),
    ("/System/Library/Fonts/Hiragino Sans GB W3.otf",
     "/System/Library/Fonts/Hiragino Sans GB W6.otf"),
]

_WINDOWS_FONTS = [
    ("C:/Windows/Fonts/YuGothR.ttc", "C:/Windows/Fonts/YuGothB.ttc"),
    ("C:/Windows/Fonts/yugothic.ttf", "C:/Windows/Fonts/yugothb.ttf"),
    ("C:/Windows/Fonts/msgothic.ttc", "C:/Windows/Fonts/msgothic.ttc"),
]

_LINUX_FONTS = [
    ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
     "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
    ("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
     "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc"),
    ("/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
     "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc"),
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
            print("Error: Both --font-regular and --font-bold must be specified together.",
                  file=sys.stderr)
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
        return str(reg_path), str(bold_path)

    # Platform-specific search
    system = platform.system()
    if system == "Darwin":
        candidates = _MACOS_FONTS
    elif system == "Windows":
        candidates = _WINDOWS_FONTS
    else:
        candidates = _LINUX_FONTS

    for reg, bold in candidates:
        if Path(reg).exists() and Path(bold).exists():
            return reg, bold

    # Fail-fast with helpful message
    print(
        "Error: No CJK fonts found for PDF generation.\n"
        "\n"
        "Please specify font paths manually:\n"
        "  --font-regular /path/to/regular.ttc --font-bold /path/to/bold.ttc\n"
        "\n"
        "Recommended fonts by platform:\n"
        "  macOS:   Hiragino Kaku Gothic W3/W6\n"
        "  Windows: Yu Gothic Regular/Bold\n"
        "  Linux:   Noto Sans CJK Regular/Bold\n"
        "           Install: sudo apt install fonts-noto-cjk",
        file=sys.stderr,
    )
    sys.exit(1)
