"""MARP CLI wrapper for Markdown to PDF/HTML conversion."""

import logging
import subprocess
import tempfile
import time
from pathlib import Path

from config.settings import OUTPUT_DIR

logger = logging.getLogger(__name__)


def convert_marp_to_pdf(markdown: str, filename: str = "presentation") -> Path:
    """Convert MARP Markdown to PDF.

    Args:
        markdown: MARP-formatted Markdown content.
        filename: Output filename without extension.

    Returns:
        Path to the generated PDF file.
    """
    stem = Path(filename).stem  # "proposal.pdf" → "proposal"
    output_path = OUTPUT_DIR / f"{stem}.pdf"
    logger.info("PDF conversion started: %s (%d bytes)", filename, len(markdown))
    t0 = time.monotonic()

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, dir=OUTPUT_DIR
    ) as tmp:
        tmp.write(markdown)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
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
        elapsed = time.monotonic() - t0
        logger.info("PDF conversion completed in %.2fs: %s", elapsed, output_path)
        if result.stderr:
            logger.debug("marp stderr: %s", result.stderr[:500])
        # Save Markdown source alongside the PDF
        md_output_path = OUTPUT_DIR / f"{stem}.md"
        Path(tmp_path).rename(md_output_path)
        logger.info("Markdown source saved: %s", md_output_path)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise

    return output_path


def convert_marp_to_html(markdown: str, filename: str = "presentation") -> Path:
    """Convert MARP Markdown to HTML for preview.

    Args:
        markdown: MARP-formatted Markdown content.
        filename: Output filename without extension.

    Returns:
        Path to the generated HTML file.
    """
    stem = Path(filename).stem  # "presentation.html" → "presentation"
    output_path = OUTPUT_DIR / f"{stem}.html"
    logger.info("HTML conversion started: %s (%d bytes)", filename, len(markdown))
    t0 = time.monotonic()

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, dir=OUTPUT_DIR
    ) as tmp:
        tmp.write(markdown)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
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
        elapsed = time.monotonic() - t0
        logger.info("HTML conversion completed in %.2fs: %s", elapsed, output_path)
        if result.stderr:
            logger.debug("marp stderr: %s", result.stderr[:500])
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return output_path
