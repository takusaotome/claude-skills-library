#!/usr/bin/env python3
"""
Mermaid to Image Converter — thin CLI wrapper around MermaidRenderer.

Converts Mermaid diagram code to high-quality images (PNG or SVG).

Dependencies:
    - Node.js and npm (for mermaid-cli)
    - mermaid-cli: npm install -g @mermaid-js/mermaid-cli
    - OR Playwright: pip install playwright && playwright install chromium

Usage:
    python mermaid_to_image.py input.mmd output.png --format png
    python mermaid_to_image.py input.mmd output.svg --format svg
    python mermaid_to_image.py --code "graph TD; A-->B" output.png
    python mermaid_to_image.py --code "graph TD; A-->B" output.png --debug
"""

import argparse
import os
import sys
from pathlib import Path

# Ensure sibling imports work
_SCRIPT_DIR = Path(__file__).parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from mermaid_renderer import MermaidBackend, MermaidRenderer


def main():
    parser = argparse.ArgumentParser(
        description="Convert Mermaid diagrams to high-quality images"
    )
    parser.add_argument("input", nargs="?", help="Input Mermaid file (.mmd)")
    parser.add_argument("output", help="Output image file")
    parser.add_argument(
        "--code", help="Mermaid code string (alternative to input file)"
    )
    parser.add_argument(
        "--format",
        choices=["png", "svg"],
        default="png",
        help="Output format (default: png)",
    )
    parser.add_argument(
        "--theme",
        choices=["default", "forest", "dark", "neutral"],
        default="default",
        help="Mermaid theme",
    )
    parser.add_argument(
        "--background", default="white", help="Background color (default: white)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=3200,
        help="Image width for PNG (default: 3200)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=2400,
        help="Image height for PNG (default: 2400)",
    )
    parser.add_argument(
        "--use-playwright",
        action="store_true",
        help="Force use of Playwright instead of mermaid-cli",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print detailed debug output for troubleshooting",
    )

    args = parser.parse_args()

    # Validate input
    if not args.input and not args.code:
        print("Error: Either input file or --code must be provided", file=sys.stderr)
        sys.exit(1)

    # Read Mermaid code
    if args.code:
        mermaid_code = args.code
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {input_path}", file=sys.stderr)
            sys.exit(1)
        mermaid_code = input_path.read_text(encoding="utf-8")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Map --use-playwright to backend
    if args.use_playwright:
        backend = MermaidBackend.PLAYWRIGHT
    else:
        backend = MermaidBackend.AUTO

    # Create renderer and render
    renderer = MermaidRenderer(
        backend=backend,
        output_format=args.format,
        theme=args.theme,
        background=args.background,
        width=args.width,
        height=args.height,
        debug=args.debug,
    )

    result = renderer.render(mermaid_code, output_path=str(output_path))

    # Cleanup cache
    renderer.cleanup_cache()

    # Report result
    if result.success:
        print(f"Successfully converted Mermaid diagram to {output_path}")
        print(f"  Backend: {result.backend_used}")
        sys.exit(0)
    else:
        print(f"Failed to convert Mermaid diagram", file=sys.stderr)
        if result.error_message:
            print(f"  Error: {result.error_message}", file=sys.stderr)
        if result.fix_suggestion:
            print(f"  Fix: {result.fix_suggestion}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
