#!/usr/bin/env python3
"""
QR Code Generator

Generate QR code images from text, URLs, or contact information.
Supports single generation, batch processing, and vCard creation.
"""

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q
except ImportError:
    print("Error: qrcode library not installed. Run: pip install 'qrcode[pil]'", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow not installed. Run: pip install 'qrcode[pil]'", file=sys.stderr)
    sys.exit(1)


ERROR_CORRECTION_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


def parse_color(color_str: str) -> str:
    """Parse color string to a format accepted by PIL.

    Accepts:
    - Named colors: black, white, red, green, blue, etc.
    - Hex codes: #RRGGBB
    - RGB tuples: rgb(R,G,B)
    """
    if color_str.startswith("rgb(") and color_str.endswith(")"):
        # Parse rgb(R,G,B) format
        rgb_values = color_str[4:-1].split(",")
        if len(rgb_values) == 3:
            try:
                r, g, b = [int(v.strip()) for v in rgb_values]
                return f"#{r:02x}{g:02x}{b:02x}"
            except ValueError:
                pass
    # Return as-is for named colors and hex codes
    return color_str


def generate_vcard(
    name: str,
    phone: str | None = None,
    email: str | None = None,
    org: str | None = None,
    title: str | None = None,
    url: str | None = None,
    address: str | None = None,
) -> str:
    """Generate vCard 3.0 formatted string."""
    parts = name.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{last_name};{first_name}",
        f"FN:{name}",
    ]

    if phone:
        lines.append(f"TEL:{phone}")
    if email:
        lines.append(f"EMAIL:{email}")
    if org:
        lines.append(f"ORG:{org}")
    if title:
        lines.append(f"TITLE:{title}")
    if url:
        lines.append(f"URL:{url}")
    if address:
        lines.append(f"ADR:;;{address}")

    lines.append("END:VCARD")
    return "\n".join(lines)


def generate_qr_code(
    data: str,
    output_path: str | Path,
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
    error_correction: str = "M",
) -> dict[str, Any]:
    """Generate a single QR code image.

    Args:
        data: The string to encode in the QR code
        output_path: Path to save the PNG image
        box_size: Pixels per QR code module
        border: Quiet zone width in modules (minimum 4)
        fill_color: Foreground color
        back_color: Background color
        error_correction: Error correction level (L, M, Q, H)

    Returns:
        dict with generation metadata
    """
    output_path = Path(output_path)

    # Validate parameters
    if border < 4:
        print(f"Warning: border={border} is below minimum (4). Using 4.", file=sys.stderr)
        border = 4

    if box_size < 1:
        print(f"Warning: box_size={box_size} is invalid. Using 10.", file=sys.stderr)
        box_size = 10

    ec_level = ERROR_CORRECTION_MAP.get(error_correction.upper(), ERROR_CORRECT_M)

    # Parse colors
    fill = parse_color(fill_color)
    back = parse_color(back_color)

    # Create QR code
    qr = qrcode.QRCode(
        version=None,  # Auto-determine
        error_correction=ec_level,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill_color=fill, back_color=back)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save image
    img.save(str(output_path))

    return {
        "data": data[:100] + "..." if len(data) > 100 else data,
        "path": str(output_path),
        "version": qr.version,
        "box_size": box_size,
        "border": border,
        "error_correction": error_correction.upper(),
        "image_size": img.size,
        "status": "success",
    }


def process_batch_csv(
    csv_path: str | Path,
    output_dir: str | Path,
    defaults: dict[str, Any],
) -> list[dict[str, Any]]:
    """Process batch QR code generation from CSV file."""
    csv_path = Path(csv_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = row.get("data", "")
            if not data:
                results.append({"data": "", "status": "failed", "error": "Empty data"})
                continue

            filename = row.get("filename", f"qr_{len(results)}.png")
            output_path = output_dir / filename

            try:
                result = generate_qr_code(
                    data=data,
                    output_path=output_path,
                    box_size=int(row.get("box_size", defaults["box_size"])),
                    border=int(row.get("border", defaults["border"])),
                    fill_color=row.get("fill_color", defaults["fill_color"]),
                    back_color=row.get("back_color", defaults["back_color"]),
                    error_correction=row.get("error_correction", defaults["error_correction"]),
                )
                results.append(result)
            except Exception as e:
                results.append(
                    {
                        "data": data[:50],
                        "filename": filename,
                        "status": "failed",
                        "error": str(e),
                    }
                )

    return results


def process_batch_json(
    json_path: str | Path,
    output_dir: str | Path,
    defaults: dict[str, Any],
) -> list[dict[str, Any]]:
    """Process batch QR code generation from JSON file."""
    json_path = Path(json_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []

    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for i, item in enumerate(items):
        data = item.get("data", "")
        if not data:
            results.append({"data": "", "status": "failed", "error": "Empty data"})
            continue

        filename = item.get("filename", f"qr_{i}.png")
        output_path = output_dir / filename

        try:
            result = generate_qr_code(
                data=data,
                output_path=output_path,
                box_size=item.get("box_size", defaults["box_size"]),
                border=item.get("border", defaults["border"]),
                fill_color=item.get("fill_color", defaults["fill_color"]),
                back_color=item.get("back_color", defaults["back_color"]),
                error_correction=item.get("error_correction", defaults["error_correction"]),
            )
            results.append(result)
        except Exception as e:
            results.append(
                {
                    "data": data[:50],
                    "filename": filename,
                    "status": "failed",
                    "error": str(e),
                }
            )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate QR code images from text, URLs, or contact information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a simple QR code
  python generate_qr.py --data "https://example.com" --output qr.png

  # Generate with custom settings
  python generate_qr.py --data "Hello World" --output hello.png \\
      --box-size 15 --fill-color "#003366" --error-correction H

  # Generate vCard QR code
  python generate_qr.py --vcard --name "John Doe" \\
      --phone "+1-555-1234" --email "john@example.com" --output contact.png

  # Batch generation from CSV
  python generate_qr.py --batch input.csv --output-dir ./qr_codes/
""",
    )

    # Single generation options
    parser.add_argument("--data", "-d", help="Data to encode in QR code")
    parser.add_argument("--output", "-o", default="./qr_output.png", help="Output PNG file path")

    # QR code parameters
    parser.add_argument("--box-size", type=int, default=10, help="Pixels per QR module (default: 10)")
    parser.add_argument("--border", type=int, default=4, help="Quiet zone width in modules (default: 4, minimum: 4)")
    parser.add_argument("--fill-color", default="black", help="Foreground color (default: black)")
    parser.add_argument("--back-color", default="white", help="Background color (default: white)")
    parser.add_argument(
        "--error-correction",
        "-e",
        default="M",
        choices=["L", "M", "Q", "H"],
        help="Error correction level (default: M)",
    )

    # vCard options
    parser.add_argument("--vcard", action="store_true", help="Generate vCard QR code")
    parser.add_argument("--name", help="Contact name for vCard")
    parser.add_argument("--phone", help="Phone number for vCard")
    parser.add_argument("--email", help="Email for vCard")
    parser.add_argument("--org", help="Organization for vCard")
    parser.add_argument("--title", help="Job title for vCard")
    parser.add_argument("--url", help="URL for vCard")
    parser.add_argument("--address", help="Address for vCard")

    # Batch options
    parser.add_argument("--batch", "-b", help="Batch input file (CSV or JSON)")
    parser.add_argument("--output-dir", default="./qr_batch_output", help="Output directory for batch generation")

    args = parser.parse_args()

    defaults = {
        "box_size": args.box_size,
        "border": args.border,
        "fill_color": args.fill_color,
        "back_color": args.back_color,
        "error_correction": args.error_correction,
    }

    # Handle batch processing
    if args.batch:
        batch_path = Path(args.batch)
        if not batch_path.exists():
            print(f"Error: Batch file not found: {args.batch}", file=sys.stderr)
            sys.exit(1)

        if batch_path.suffix.lower() == ".csv":
            results = process_batch_csv(batch_path, args.output_dir, defaults)
        elif batch_path.suffix.lower() == ".json":
            results = process_batch_json(batch_path, args.output_dir, defaults)
        else:
            print(f"Error: Unsupported batch file format: {batch_path.suffix}", file=sys.stderr)
            sys.exit(1)

        # Generate summary
        success_count = sum(1 for r in results if r.get("status") == "success")
        failed_count = len(results) - success_count

        summary = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_count": len(results),
            "success_count": success_count,
            "failed_count": failed_count,
            "files": results,
        }

        # Save summary
        summary_path = Path(args.output_dir) / "batch_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        print(f"Batch generation complete: {success_count}/{len(results)} successful")
        print(f"Summary saved to: {summary_path}")

        if failed_count > 0:
            print(f"Warning: {failed_count} QR codes failed to generate", file=sys.stderr)
            sys.exit(1)

        return

    # Handle vCard generation
    if args.vcard:
        if not args.name:
            print("Error: --name is required for vCard generation", file=sys.stderr)
            sys.exit(1)

        data = generate_vcard(
            name=args.name,
            phone=args.phone,
            email=args.email,
            org=args.org,
            title=args.title,
            url=args.url,
            address=args.address,
        )
    elif args.data:
        data = args.data
    else:
        print("Error: Either --data or --vcard with --name is required", file=sys.stderr)
        sys.exit(1)

    # Generate single QR code
    try:
        result = generate_qr_code(
            data=data,
            output_path=args.output,
            box_size=args.box_size,
            border=args.border,
            fill_color=args.fill_color,
            back_color=args.back_color,
            error_correction=args.error_correction,
        )

        print("QR code generated successfully:")
        print(f"  Path: {result['path']}")
        print(f"  Version: {result['version']}")
        print(f"  Size: {result['image_size'][0]}x{result['image_size'][1]} pixels")
        print(f"  Error correction: {result['error_correction']}")

    except Exception as e:
        print(f"Error generating QR code: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
