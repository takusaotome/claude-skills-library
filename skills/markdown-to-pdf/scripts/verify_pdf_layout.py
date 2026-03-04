#!/usr/bin/env python3
"""Verify PDF layout by converting each page to an image and checking for overflow.

Uses PyMuPDF (fitz) to render pages and PIL to analyze edge regions.
Content near page edges indicates potential overflow/clipping.

Usage:
    python verify_pdf_layout.py output.pdf [--margin 10] [--threshold 50] [--save-images]

Exit code:
    0 = all pages OK
    1 = overflow detected on one or more pages
"""

import argparse
import sys
import tempfile
from pathlib import Path

try:
    import pymupdf as fitz  # PyMuPDF >= 1.24
except ImportError:
    try:
        import fitz  # PyMuPDF < 1.24
    except ImportError:
        print("Error: PyMuPDF not installed. Run: pip install PyMuPDF", file=sys.stderr)
        sys.exit(2)

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(2)


def check_page_overflow(
    page_image: Image.Image,
    page_num: int,
    margin_px: int = 15,
    threshold: int = 50,
    bg_tolerance: int = 30,
) -> list[str]:
    """Check if content exists in the margin zones of a page image.

    Args:
        page_image: PIL Image of the rendered PDF page.
        page_num: 1-based page number (for error messages).
        margin_px: Pixel width of the edge zone to check.
        threshold: Minimum number of non-background pixels to flag as overflow.
        bg_tolerance: Max RGB deviation from white (255) to count as background.

    Returns:
        List of warning messages (empty if no overflow detected).
    """
    w, h = page_image.size
    warnings = []

    # Convert to RGB if needed
    if page_image.mode != "RGB":
        page_image = page_image.convert("RGB")

    def count_content_pixels(region: Image.Image) -> int:
        """Count pixels that are NOT near-white (background)."""
        pixels = list(region.getdata())
        count = 0
        for r, g, b in pixels:
            if (255 - r) > bg_tolerance or (255 - g) > bg_tolerance or (255 - b) > bg_tolerance:
                count += 1
        return count

    # Check right edge (most common overflow direction)
    right_strip = page_image.crop((w - margin_px, margin_px, w, h - margin_px))
    right_count = count_content_pixels(right_strip)
    if right_count > threshold:
        warnings.append(
            f"Page {page_num}: RIGHT edge overflow detected ({right_count} content pixels in right {margin_px}px margin)"
        )

    # Check bottom edge
    bottom_strip = page_image.crop((margin_px, h - margin_px, w - margin_px, h))
    bottom_count = count_content_pixels(bottom_strip)
    if bottom_count > threshold:
        warnings.append(
            f"Page {page_num}: BOTTOM edge overflow detected ({bottom_count} content pixels in bottom {margin_px}px margin)"
        )

    # Check left edge
    left_strip = page_image.crop((0, margin_px, margin_px, h - margin_px))
    left_count = count_content_pixels(left_strip)
    if left_count > threshold:
        warnings.append(
            f"Page {page_num}: LEFT edge overflow detected ({left_count} content pixels in left {margin_px}px margin)"
        )

    return warnings


def verify_pdf(
    pdf_path: str,
    margin_px: int = 15,
    threshold: int = 50,
    dpi: int = 150,
    save_images: bool = False,
    skip_first_page: bool = True,
) -> list[str]:
    """Verify all pages of a PDF for layout overflow.

    Args:
        pdf_path: Path to the PDF file.
        margin_px: Edge margin in pixels to check for content.
        threshold: Minimum content pixels to flag as overflow.
        dpi: Resolution for rendering pages.
        save_images: If True, save page images to /tmp for debugging.
        skip_first_page: Skip page 1 (cover pages have intentional edge-to-edge bars).

    Returns:
        List of warning messages (empty if all pages OK).
    """
    doc = fitz.open(pdf_path)
    all_warnings = []

    start_page = 1 if skip_first_page and len(doc) > 1 else 0
    for page_idx in range(start_page, len(doc)):
        page = doc[page_idx]
        # Render page to image
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)

        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        if save_images:
            img_path = f"/tmp/pdf_verify_page_{page_idx + 1}.png"
            img.save(img_path)
            print(f"  Saved: {img_path}", file=sys.stderr)

        warnings = check_page_overflow(
            img,
            page_num=page_idx + 1,
            margin_px=margin_px,
            threshold=threshold,
        )
        all_warnings.extend(warnings)

    doc.close()
    return all_warnings


def main():
    parser = argparse.ArgumentParser(description="Verify PDF layout for content overflow")
    parser.add_argument("pdf", help="PDF file to verify")
    parser.add_argument("--margin", type=int, default=15, help="Edge margin in pixels to check (default: 15)")
    parser.add_argument(
        "--threshold", type=int, default=50, help="Min content pixels to flag as overflow (default: 50)"
    )
    parser.add_argument("--dpi", type=int, default=150, help="Render DPI (default: 150)")
    parser.add_argument("--save-images", action="store_true", help="Save page images to /tmp for debugging")
    args = parser.parse_args()

    if not Path(args.pdf).exists():
        print(f"Error: File not found: {args.pdf}", file=sys.stderr)
        sys.exit(2)

    print(f"Verifying: {args.pdf} ({args.dpi} DPI, margin={args.margin}px, threshold={args.threshold})")
    warnings = verify_pdf(
        args.pdf,
        margin_px=args.margin,
        threshold=args.threshold,
        dpi=args.dpi,
        save_images=args.save_images,
    )

    if warnings:
        print(f"\n⚠ Layout issues found ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
        sys.exit(1)
    else:
        print("✓ All pages OK — no overflow detected")
        sys.exit(0)


if __name__ == "__main__":
    main()
