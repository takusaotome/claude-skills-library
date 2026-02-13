"""MARP CLI wrapper for Markdown to PDF/HTML conversion."""

import subprocess
import tempfile
from pathlib import Path

from config.settings import OUTPUT_DIR


def convert_marp_to_pdf(markdown: str, filename: str = "presentation") -> Path:
    """Convert MARP Markdown to PDF.

    Args:
        markdown: MARP-formatted Markdown content.
        filename: Output filename without extension.

    Returns:
        Path to the generated PDF file.
    """
    output_path = OUTPUT_DIR / f"{filename}.pdf"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, dir=OUTPUT_DIR
    ) as tmp:
        tmp.write(markdown)
        tmp_path = tmp.name

    try:
        subprocess.run(
            [
                "marp",
                "--pdf",
                "--allow-local-files",
                "--html",
                "-o",
                str(output_path),
                tmp_path,
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return output_path


def convert_marp_to_html(markdown: str, filename: str = "presentation") -> Path:
    """Convert MARP Markdown to HTML for preview.

    Args:
        markdown: MARP-formatted Markdown content.
        filename: Output filename without extension.

    Returns:
        Path to the generated HTML file.
    """
    output_path = OUTPUT_DIR / f"{filename}.html"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, dir=OUTPUT_DIR
    ) as tmp:
        tmp.write(markdown)
        tmp_path = tmp.name

    try:
        subprocess.run(
            [
                "marp",
                "--html",
                "--allow-local-files",
                "-o",
                str(output_path),
                tmp_path,
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return output_path
