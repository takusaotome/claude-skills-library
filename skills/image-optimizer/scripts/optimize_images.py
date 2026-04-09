#!/usr/bin/env python3
"""
Image optimizer with target file size constraints.

Optimizes images using intelligent quality adjustment, format conversion,
and resolution scaling to meet target file size requirements.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import from analyze_image module
from analyze_image import (
    check_imagemagick,
    detect_image_type,
    find_images,
    get_image_info,
    human_readable_size,
    parse_size_string,
)


@dataclass
class OptimizationResult:
    """Result of optimizing a single image."""

    input_path: str
    output_path: str
    original_size_bytes: int
    optimized_size_bytes: int
    reduction_percent: float
    output_format: str
    quality_used: int
    dimensions: dict
    success: bool
    error_message: Optional[str] = None


def check_cwebp() -> bool:
    """Check if cwebp is available for better WebP encoding."""
    try:
        result = subprocess.run(["cwebp", "-version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_avifenc() -> bool:
    """Check if avifenc is available for AVIF encoding."""
    try:
        result = subprocess.run(["avifenc", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def compress_with_imagemagick(
    input_path: Path,
    output_path: Path,
    output_format: str,
    quality: int,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
    strip_metadata: bool = True,
) -> bool:
    """Compress image using ImageMagick."""
    cmd = ["magick", str(input_path)]

    # Resize if needed
    if max_width and max_height:
        cmd.extend(["-resize", f"{max_width}x{max_height}>"])
    elif max_width:
        cmd.extend(["-resize", f"{max_width}x>"])
    elif max_height:
        cmd.extend(["-resize", f"x{max_height}>"])

    # Strip metadata
    if strip_metadata:
        cmd.append("-strip")

    # Format-specific options
    if output_format.lower() in ("jpg", "jpeg"):
        cmd.extend(["-interlace", "Plane", "-sampling-factor", "4:2:0", "-quality", str(quality)])
    elif output_format.lower() == "png":
        cmd.extend(["-define", "png:compression-level=9", "-define", "png:compression-filter=5"])
        if quality < 100:
            # Use posterize for lossy PNG
            colors = max(16, int(256 * (quality / 100)))
            cmd.extend(["-colors", str(colors)])
    elif output_format.lower() == "webp":
        cmd.extend(["-quality", str(quality), "-define", "webp:method=6"])
    elif output_format.lower() == "avif":
        cmd.extend(["-quality", str(quality)])

    cmd.append(str(output_path))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def compress_with_cwebp(
    input_path: Path,
    output_path: Path,
    quality: int,
    max_dimension: Optional[int] = None,
    target_size: Optional[int] = None,
) -> bool:
    """Compress to WebP using cwebp for better quality."""
    cmd = ["cwebp"]

    if target_size:
        cmd.extend(["-size", str(target_size)])
    else:
        cmd.extend(["-q", str(quality)])

    cmd.extend(["-m", "6"])  # Best compression method

    if max_dimension:
        cmd.extend(["-resize", str(max_dimension), "0"])

    cmd.extend([str(input_path), "-o", str(output_path)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def compress_with_avifenc(input_path: Path, output_path: Path, quality: int) -> bool:
    """Compress to AVIF using avifenc."""
    # avifenc uses different quality scale (0-63, lower is better)
    avif_quality = int((100 - quality) * 63 / 100)

    cmd = [
        "avifenc",
        "-s",
        "6",  # Speed (0-10, 6 is balanced)
        "-q",
        str(avif_quality),
        str(input_path),
        str(output_path),
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def optimize_to_target_size(
    input_path: Path,
    output_path: Path,
    target_size_bytes: int,
    output_format: str,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
    strip_metadata: bool = True,
    min_quality: int = 30,
    max_quality: int = 95,
) -> tuple[bool, int]:
    """
    Optimize image to target file size using binary search on quality.

    Returns (success, quality_used)
    """
    # Create temporary directory for iterations
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_output = Path(tmpdir) / f"output.{output_format}"

        quality = (min_quality + max_quality) // 2
        best_quality = min_quality
        best_size = float("inf")

        # Binary search for optimal quality
        iterations = 0
        max_iterations = 8

        while iterations < max_iterations and (max_quality - min_quality) > 1:
            iterations += 1

            success = compress_with_imagemagick(
                input_path, tmp_output, output_format, quality, max_width, max_height, strip_metadata
            )

            if not success:
                return False, 0

            current_size = tmp_output.stat().st_size

            if current_size <= target_size_bytes:
                # Size is acceptable, try higher quality
                if current_size > best_size * 0.9:  # Within 10% of best
                    best_quality = quality
                    best_size = current_size
                min_quality = quality + 1
            else:
                # Size too large, reduce quality
                max_quality = quality - 1

            quality = (min_quality + max_quality) // 2

        # Final compression with best quality
        success = compress_with_imagemagick(
            input_path, output_path, output_format, best_quality, max_width, max_height, strip_metadata
        )

        return success, best_quality


def determine_output_format(info, detection, requested_format: str, has_cwebp: bool, has_avifenc: bool) -> str:
    """Determine the best output format."""
    if requested_format != "auto":
        return requested_format

    # Auto-select based on image type
    if detection.detected_type == "diagram":
        return "png"
    elif detection.detected_type == "screenshot":
        if info.has_transparency:
            return "png"
        return "webp" if has_cwebp else "png"
    else:
        # Photo, illustration, mixed
        if info.has_transparency:
            return "webp" if has_cwebp else "png"
        return "webp"


def optimize_image(
    input_path: Path,
    output_dir: Path,
    target_size_bytes: Optional[int] = None,
    output_format: str = "auto",
    quality: Optional[int] = None,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
    strip_metadata: bool = True,
    has_cwebp: bool = False,
    has_avifenc: bool = False,
) -> OptimizationResult:
    """Optimize a single image."""
    info = get_image_info(input_path)
    if not info:
        return OptimizationResult(
            input_path=str(input_path),
            output_path="",
            original_size_bytes=0,
            optimized_size_bytes=0,
            reduction_percent=0,
            output_format="",
            quality_used=0,
            dimensions={},
            success=False,
            error_message="Failed to read image information",
        )

    detection = detect_image_type(info, input_path)

    # Determine format
    final_format = determine_output_format(info, detection, output_format, has_cwebp, has_avifenc)

    # Determine quality if not specified
    if quality is None:
        quality_map = {
            "photo": 82,
            "screenshot": 95,
            "diagram": 100,
            "illustration": 90,
            "mixed": 85,
        }
        quality = quality_map.get(detection.detected_type, 85)

    # Build output path
    output_filename = input_path.stem + "." + final_format
    output_path = output_dir / output_filename

    # Optimize
    if target_size_bytes:
        success, quality_used = optimize_to_target_size(
            input_path, output_path, target_size_bytes, final_format, max_width, max_height, strip_metadata
        )
    else:
        # Use cwebp for WebP if available and no target size
        if final_format == "webp" and has_cwebp:
            success = compress_with_cwebp(input_path, output_path, quality, max_dimension=max_width or max_height)
        else:
            success = compress_with_imagemagick(
                input_path, output_path, final_format, quality, max_width, max_height, strip_metadata
            )
        quality_used = quality

    if not success or not output_path.exists():
        return OptimizationResult(
            input_path=str(input_path),
            output_path=str(output_path),
            original_size_bytes=info.size_bytes,
            optimized_size_bytes=0,
            reduction_percent=0,
            output_format=final_format,
            quality_used=quality_used,
            dimensions={"width": info.width, "height": info.height},
            success=False,
            error_message="Compression failed",
        )

    optimized_size = output_path.stat().st_size
    reduction = (1 - optimized_size / info.size_bytes) * 100 if info.size_bytes > 0 else 0

    # Get output dimensions
    output_info = get_image_info(output_path)
    output_dimensions = {
        "width": output_info.width if output_info else info.width,
        "height": output_info.height if output_info else info.height,
    }

    return OptimizationResult(
        input_path=str(input_path),
        output_path=str(output_path),
        original_size_bytes=info.size_bytes,
        optimized_size_bytes=optimized_size,
        reduction_percent=round(reduction, 1),
        output_format=final_format,
        quality_used=quality_used,
        dimensions=output_dimensions,
        success=True,
    )


def generate_markdown_report(results: list[OptimizationResult], processing_time: float, output_path: Path) -> None:
    """Generate a Markdown optimization report."""
    total_original = sum(r.original_size_bytes for r in results if r.success)
    total_optimized = sum(r.optimized_size_bytes for r in results if r.success)
    total_reduction = (1 - total_optimized / total_original) * 100 if total_original > 0 else 0

    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    lines = [
        "# Image Optimization Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Images Processed | {len(successful)} |",
        f"| Failed | {len(failed)} |",
        f"| Original Total Size | {human_readable_size(total_original)} |",
        f"| Optimized Total Size | {human_readable_size(total_optimized)} |",
        f"| Size Reduction | {total_reduction:.1f}% |",
        f"| Processing Time | {processing_time:.1f}s |",
        "",
    ]

    if successful:
        lines.extend(
            [
                "## Detailed Results",
                "",
                "| File | Original | Optimized | Reduction | Format | Quality |",
                "|------|----------|-----------|-----------|--------|---------|",
            ]
        )

        for r in successful:
            filename = Path(r.input_path).name
            lines.append(
                f"| {filename} | {human_readable_size(r.original_size_bytes)} | "
                f"{human_readable_size(r.optimized_size_bytes)} | "
                f"{r.reduction_percent:.1f}% | {r.output_format.upper()} | {r.quality_used} |"
            )

        lines.append("")

    if failed:
        lines.extend(
            [
                "## Failed Images",
                "",
            ]
        )
        for r in failed:
            filename = Path(r.input_path).name
            lines.append(f"- **{filename}**: {r.error_message}")
        lines.append("")

    output_path.write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Optimize images with intelligent compression")
    parser.add_argument("--input", "-i", required=True, help="Input image file or directory")
    parser.add_argument("--output", "-o", required=True, help="Output directory for optimized images")
    parser.add_argument("--target-size", "-s", help="Target maximum file size (e.g., 100KB, 1MB)")
    parser.add_argument(
        "--format",
        "-f",
        default="auto",
        choices=["auto", "jpeg", "jpg", "png", "webp", "avif"],
        help="Output format (default: auto)",
    )
    parser.add_argument("--quality", "-q", type=int, help="Quality level 1-100 (default: auto-detected)")
    parser.add_argument("--max-width", type=int, help="Maximum output width in pixels")
    parser.add_argument("--max-height", type=int, help="Maximum output height in pixels")
    parser.add_argument("--preserve-metadata", action="store_true", help="Keep EXIF and other metadata")
    parser.add_argument("--generate-report", action="store_true", help="Generate optimization report")
    parser.add_argument("--report-path", help="Path for the report file (default: output_dir/report.md)")
    parser.add_argument("--json-output", help="Write results to JSON file")

    args = parser.parse_args()

    # Check dependencies
    if not check_imagemagick():
        print("Error: ImageMagick not found. Install with:", file=sys.stderr)
        print("  macOS: brew install imagemagick", file=sys.stderr)
        print("  Linux: sudo apt-get install imagemagick", file=sys.stderr)
        sys.exit(1)

    has_cwebp = check_cwebp()
    has_avifenc = check_avifenc()

    if args.format == "avif" and not has_avifenc:
        print("Warning: avifenc not found, falling back to ImageMagick for AVIF", file=sys.stderr)

    # Parse target size
    target_size_bytes = None
    if args.target_size:
        target_size_bytes = parse_size_string(args.target_size)

    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find images
    images = find_images(input_path)
    if not images:
        print(f"Error: No supported images found in {input_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(images)} images to optimize", file=sys.stderr)

    # Process images
    results = []
    start_time = time.time()

    for i, image_path in enumerate(images, 1):
        print(f"[{i}/{len(images)}] Optimizing: {image_path.name}", file=sys.stderr)

        result = optimize_image(
            input_path=image_path,
            output_dir=output_dir,
            target_size_bytes=target_size_bytes,
            output_format=args.format,
            quality=args.quality,
            max_width=args.max_width,
            max_height=args.max_height,
            strip_metadata=not args.preserve_metadata,
            has_cwebp=has_cwebp,
            has_avifenc=has_avifenc,
        )

        results.append(result)

        if result.success:
            print(
                f"  → {human_readable_size(result.original_size_bytes)} → "
                f"{human_readable_size(result.optimized_size_bytes)} "
                f"({result.reduction_percent:.1f}% reduction)",
                file=sys.stderr,
            )
        else:
            print(f"  → Failed: {result.error_message}", file=sys.stderr)

    processing_time = time.time() - start_time

    # Generate report
    if args.generate_report:
        report_path = Path(args.report_path) if args.report_path else output_dir / "report.md"
        generate_markdown_report(results, processing_time, report_path)
        print(f"Report written to: {report_path}", file=sys.stderr)

    # Write JSON output
    if args.json_output:
        json_path = Path(args.json_output)
        json_data = {
            "schema_version": "1.0",
            "optimized_at": datetime.now().isoformat(),
            "processing_time_seconds": round(processing_time, 2),
            "results": [asdict(r) for r in results],
            "summary": {
                "total_images": len(results),
                "successful": len([r for r in results if r.success]),
                "failed": len([r for r in results if not r.success]),
                "total_original_bytes": sum(r.original_size_bytes for r in results if r.success),
                "total_optimized_bytes": sum(r.optimized_size_bytes for r in results if r.success),
            },
        }
        json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False))
        print(f"JSON results written to: {json_path}", file=sys.stderr)

    # Print summary
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    if successful:
        total_orig = sum(r.original_size_bytes for r in successful)
        total_opt = sum(r.optimized_size_bytes for r in successful)
        reduction = (1 - total_opt / total_orig) * 100 if total_orig > 0 else 0

        print("\nSummary:", file=sys.stderr)
        print(f"  Processed: {len(successful)} images", file=sys.stderr)
        print(f"  Original: {human_readable_size(total_orig)}", file=sys.stderr)
        print(f"  Optimized: {human_readable_size(total_opt)}", file=sys.stderr)
        print(f"  Reduction: {reduction:.1f}%", file=sys.stderr)

    if failed:
        print(f"  Failed: {len(failed)} images", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
