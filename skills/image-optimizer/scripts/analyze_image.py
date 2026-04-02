#!/usr/bin/env python3
"""
Image analyzer for intelligent optimization recommendations.

Detects image type (photo, screenshot, diagram, illustration) and
recommends optimal compression settings based on image characteristics.
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class ImageInfo:
    """Basic image information from ImageMagick identify."""

    path: str
    filename: str
    width: int
    height: int
    format: str
    color_space: str
    depth: int
    size_bytes: int
    has_transparency: bool
    unique_colors: int


@dataclass
class ImageTypeDetection:
    """Result of image type detection."""

    detected_type: str  # photo, screenshot, diagram, illustration, mixed
    confidence: float
    edge_density: float
    color_variance: float
    solid_region_ratio: float


@dataclass
class OptimizationRecommendation:
    """Optimization recommendation for an image."""

    format: str
    quality: int
    max_dimension: Optional[int]
    estimated_size_bytes: int
    estimated_reduction_percent: float
    reasoning: str


@dataclass
class ImageAnalysis:
    """Complete analysis result for an image."""

    path: str
    filename: str
    current_size_bytes: int
    current_size_human: str
    dimensions: dict
    format: str
    color_space: str
    has_transparency: bool
    detected_type: str
    type_confidence: float
    recommendations: dict


def human_readable_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def parse_size_string(size_str: str) -> int:
    """Parse size string like '100KB' or '1MB' to bytes."""
    size_str = size_str.strip().upper()
    # Order by suffix length descending to match longer suffixes first
    multipliers = [
        ("GB", 1024 * 1024 * 1024),
        ("MB", 1024 * 1024),
        ("KB", 1024),
        ("B", 1),
    ]
    for suffix, multiplier in multipliers:
        if size_str.endswith(suffix):
            number = float(size_str[: -len(suffix)])
            return int(number * multiplier)
    return int(size_str)


def check_imagemagick() -> bool:
    """Check if ImageMagick is available."""
    try:
        result = subprocess.run(["magick", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_image_info(image_path: Path) -> Optional[ImageInfo]:
    """Get image information using ImageMagick identify."""
    try:
        # Get basic image properties
        result = subprocess.run(
            ["magick", "identify", "-format", "%w|%h|%m|%[colorspace]|%z|%B|%A|%k", str(image_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"Error identifying {image_path}: {result.stderr}", file=sys.stderr)
            return None

        # Parse output (may have multiple frames for GIF)
        lines = result.stdout.strip().split("\n")
        parts = lines[0].split("|")

        if len(parts) < 8:
            print(f"Unexpected identify output for {image_path}: {result.stdout}", file=sys.stderr)
            return None

        width = int(parts[0])
        height = int(parts[1])
        img_format = parts[2]
        color_space = parts[3]
        depth = int(parts[4])
        size_bytes = int(parts[5])
        has_alpha = parts[6].lower() in ("true", "blend", "yes")
        unique_colors = int(parts[7])

        return ImageInfo(
            path=str(image_path),
            filename=image_path.name,
            width=width,
            height=height,
            format=img_format,
            color_space=color_space,
            depth=depth,
            size_bytes=size_bytes,
            has_transparency=has_alpha,
            unique_colors=unique_colors,
        )

    except Exception as e:
        print(f"Error analyzing {image_path}: {e}", file=sys.stderr)
        return None


def calculate_edge_density(image_path: Path) -> float:
    """Calculate edge density using Sobel edge detection."""
    try:
        # Apply edge detection and calculate mean
        result = subprocess.run(
            ["magick", str(image_path), "-colorspace", "Gray", "-edge", "1", "-format", "%[mean]", "info:"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            # Normalize to 0-1 range (mean is typically 0-65535 for 16-bit)
            mean_value = float(result.stdout.strip())
            return min(mean_value / 65535, 1.0)
    except Exception:
        pass

    return 0.5  # Default if analysis fails


def calculate_color_variance(image_path: Path, unique_colors: int, width: int, height: int) -> float:
    """Calculate color variance as ratio of unique colors to total pixels."""
    total_pixels = width * height
    if total_pixels == 0:
        return 0.0

    # Normalize: photos typically have very high ratios
    ratio = unique_colors / total_pixels
    return min(ratio, 1.0)


def estimate_solid_region_ratio(image_path: Path) -> float:
    """Estimate the ratio of solid color regions."""
    try:
        # Posterize to detect solid regions
        result = subprocess.run(
            ["magick", str(image_path), "-colors", "16", "-format", "%k", "info:"], capture_output=True, text=True
        )

        if result.returncode == 0:
            posterized_colors = int(result.stdout.strip())
            # Fewer colors after posterization = more solid regions
            return 1.0 - (posterized_colors / 16)
    except Exception:
        pass

    return 0.3  # Default


def detect_image_type(info: ImageInfo, image_path: Path) -> ImageTypeDetection:
    """Detect image type based on characteristics."""
    edge_density = calculate_edge_density(image_path)
    color_variance = calculate_color_variance(image_path, info.unique_colors, info.width, info.height)
    solid_ratio = estimate_solid_region_ratio(image_path)

    total_pixels = info.width * info.height
    colors_per_million = (info.unique_colors / total_pixels) * 1_000_000 if total_pixels > 0 else 0

    # Classification logic
    scores = {
        "photo": 0.0,
        "screenshot": 0.0,
        "diagram": 0.0,
        "illustration": 0.0,
    }

    # Photo indicators
    if colors_per_million > 10000:
        scores["photo"] += 0.4
    if edge_density < 0.15:
        scores["photo"] += 0.3
    if solid_ratio < 0.3:
        scores["photo"] += 0.3

    # Screenshot indicators
    if 1000 < colors_per_million < 10000:
        scores["screenshot"] += 0.3
    if 0.15 <= edge_density <= 0.4:
        scores["screenshot"] += 0.3
    if solid_ratio > 0.3:
        scores["screenshot"] += 0.4

    # Diagram indicators
    if colors_per_million < 1000:
        scores["diagram"] += 0.5
    if edge_density > 0.2:
        scores["diagram"] += 0.25
    if info.unique_colors < 500:
        scores["diagram"] += 0.25

    # Illustration indicators
    if 500 <= info.unique_colors <= 5000:
        scores["illustration"] += 0.4
    if 0.1 <= edge_density <= 0.3:
        scores["illustration"] += 0.3
    if 0.4 <= solid_ratio <= 0.7:
        scores["illustration"] += 0.3

    # Determine best match
    best_type = max(scores, key=scores.get)
    confidence = scores[best_type]

    # If confidence is low, classify as mixed
    if confidence < 0.5:
        best_type = "mixed"
        confidence = 0.5

    return ImageTypeDetection(
        detected_type=best_type,
        confidence=min(confidence, 1.0),
        edge_density=edge_density,
        color_variance=color_variance,
        solid_region_ratio=solid_ratio,
    )


def get_optimization_recommendation(info: ImageInfo, detection: ImageTypeDetection) -> OptimizationRecommendation:
    """Generate optimization recommendations based on image analysis."""

    # Format recommendation based on type
    format_map = {
        "photo": ("webp", 82),
        "screenshot": ("webp", 95),  # Higher quality for text
        "diagram": ("png", 100),  # Lossless for sharp edges
        "illustration": ("webp", 90),
        "mixed": ("webp", 85),
    }

    recommended_format, base_quality = format_map.get(detection.detected_type, ("webp", 85))

    # Adjust for transparency
    if info.has_transparency and recommended_format == "jpeg":
        recommended_format = "png"

    # Determine max dimension
    max_dimension = None
    if info.width > 2560 or info.height > 2560:
        max_dimension = 2560  # Cap at 2560px for web

    # Estimate compressed size
    compression_ratios = {
        ("photo", "webp"): 0.15,
        ("photo", "jpeg"): 0.20,
        ("screenshot", "webp"): 0.10,
        ("screenshot", "png"): 0.60,
        ("diagram", "png"): 0.30,
        ("diagram", "webp"): 0.15,
        ("illustration", "webp"): 0.15,
        ("illustration", "png"): 0.50,
        ("mixed", "webp"): 0.18,
    }

    ratio = compression_ratios.get((detection.detected_type, recommended_format), 0.25)

    # Adjust for resolution reduction
    if max_dimension:
        current_max = max(info.width, info.height)
        if current_max > max_dimension:
            scale_factor = max_dimension / current_max
            ratio *= scale_factor**2  # Area reduction

    estimated_size = int(info.size_bytes * ratio)
    reduction_percent = (1 - ratio) * 100

    # Generate reasoning
    reasoning_parts = []
    reasoning_parts.append(f"Detected as {detection.detected_type} with {detection.confidence:.0%} confidence.")

    if detection.detected_type == "photo":
        reasoning_parts.append("WebP provides excellent compression for photographic content.")
    elif detection.detected_type == "screenshot":
        reasoning_parts.append("Higher quality preserves text readability.")
    elif detection.detected_type == "diagram":
        reasoning_parts.append("PNG lossless compression preserves sharp edges.")

    if max_dimension:
        reasoning_parts.append(f"Resolution capped at {max_dimension}px for web use.")

    return OptimizationRecommendation(
        format=recommended_format,
        quality=base_quality,
        max_dimension=max_dimension,
        estimated_size_bytes=estimated_size,
        estimated_reduction_percent=reduction_percent,
        reasoning=" ".join(reasoning_parts),
    )


def analyze_image(image_path: Path) -> Optional[ImageAnalysis]:
    """Perform complete analysis on a single image."""
    info = get_image_info(image_path)
    if not info:
        return None

    detection = detect_image_type(info, image_path)
    recommendation = get_optimization_recommendation(info, detection)

    return ImageAnalysis(
        path=str(image_path),
        filename=image_path.name,
        current_size_bytes=info.size_bytes,
        current_size_human=human_readable_size(info.size_bytes),
        dimensions={"width": info.width, "height": info.height},
        format=info.format,
        color_space=info.color_space,
        has_transparency=info.has_transparency,
        detected_type=detection.detected_type,
        type_confidence=detection.confidence,
        recommendations={
            "format": recommendation.format,
            "quality": recommendation.quality,
            "max_dimension": recommendation.max_dimension,
            "estimated_size_bytes": recommendation.estimated_size_bytes,
            "estimated_reduction_percent": round(recommendation.estimated_reduction_percent, 1),
            "reasoning": recommendation.reasoning,
        },
    )


def find_images(input_path: Path) -> list[Path]:
    """Find all supported image files in path."""
    supported_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"}

    if input_path.is_file():
        if input_path.suffix.lower() in supported_extensions:
            return [input_path]
        return []

    images = []
    for ext in supported_extensions:
        images.extend(input_path.glob(f"*{ext}"))
        images.extend(input_path.glob(f"*{ext.upper()}"))

    return sorted(images)


def main():
    parser = argparse.ArgumentParser(description="Analyze images and generate optimization recommendations")
    parser.add_argument("--input", "-i", required=True, help="Input image file or directory")
    parser.add_argument("--output", "-o", help="Output JSON file path (default: stdout)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")

    args = parser.parse_args()

    # Check ImageMagick availability
    if not check_imagemagick():
        print("Error: ImageMagick not found. Install with:", file=sys.stderr)
        print("  macOS: brew install imagemagick", file=sys.stderr)
        print("  Linux: sudo apt-get install imagemagick", file=sys.stderr)
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Find images
    images = find_images(input_path)
    if not images:
        print(f"Error: No supported images found in {input_path}", file=sys.stderr)
        sys.exit(1)

    # Analyze each image
    analyses = []
    total_current = 0
    total_estimated = 0

    for image_path in images:
        print(f"Analyzing: {image_path.name}", file=sys.stderr)
        analysis = analyze_image(image_path)
        if analysis:
            analyses.append(asdict(analysis))
            total_current += analysis.current_size_bytes
            total_estimated += analysis.recommendations["estimated_size_bytes"]

    # Build output
    output = {
        "schema_version": "1.0",
        "analyzed_at": datetime.now().isoformat(),
        "images": analyses,
        "summary": {
            "total_images": len(analyses),
            "total_current_size_bytes": total_current,
            "total_current_size_human": human_readable_size(total_current),
            "total_estimated_size_bytes": total_estimated,
            "total_estimated_size_human": human_readable_size(total_estimated),
            "estimated_reduction_percent": round(
                (1 - total_estimated / total_current) * 100 if total_current > 0 else 0, 1
            ),
        },
    }

    # Output results
    indent = 2 if args.pretty else None
    json_output = json.dumps(output, indent=indent, ensure_ascii=False)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_output)
        print(f"Analysis written to: {output_path}", file=sys.stderr)
    else:
        print(json_output)


if __name__ == "__main__":
    main()
