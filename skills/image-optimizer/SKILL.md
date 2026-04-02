---
name: image-optimizer
description: Intelligent image file size optimizer that analyzes images, detects image type (photo, screenshot, diagram), recommends optimal compression settings, and executes batch optimization with target file size constraints. Use when optimizing images for web, reducing file sizes, or batch-processing images with quality/size trade-offs.
---

# Image Optimizer Skill

## Overview

This skill provides intelligent image optimization by automatically detecting image characteristics (photo, screenshot, diagram, illustration) and selecting optimal compression parameters. It supports batch processing with target file size constraints, format conversion to modern formats (WebP, AVIF), and generates before/after comparison reports.

## When to Use

- Optimize images for web deployment with target file size limits
- Batch process a folder of images with intelligent quality settings
- Convert images to modern formats (WebP, AVIF) for better compression
- Reduce storage costs by compressing existing image libraries
- Analyze images to determine optimal format and compression settings
- Create optimized image variants (thumbnail, preview, full-size)

## Prerequisites

- Python 3.9+
- ImageMagick 7+ (`magick` command available)
- Optional: `cwebp`/`dwebp` for WebP conversion (better quality than ImageMagick)
- Optional: `avifenc` for AVIF conversion
- No API keys required

## Workflow

### Step 1: Analyze Images

Run the image analyzer to detect image types and get optimization recommendations.

```bash
python3 scripts/analyze_image.py \
  --input /path/to/image.jpg \
  --output /path/to/analysis.json
```

For batch analysis:

```bash
python3 scripts/analyze_image.py \
  --input /path/to/images/ \
  --output /path/to/analysis.json
```

### Step 2: Review Analysis Results

Examine the analysis output to understand:
- Detected image type (photo, screenshot, diagram, illustration)
- Current file size and dimensions
- Recommended format and quality settings
- Estimated size reduction

### Step 3: Optimize Images

Run the optimizer with target constraints:

```bash
python3 scripts/optimize_images.py \
  --input /path/to/images/ \
  --output /path/to/optimized/ \
  --target-size 200KB \
  --format webp
```

Available options:
- `--target-size`: Maximum file size (e.g., 100KB, 1MB)
- `--format`: Output format (jpeg, png, webp, avif, auto)
- `--quality`: Quality level 1-100 (default: auto-detected)
- `--max-width`: Maximum width in pixels (maintains aspect ratio)
- `--max-height`: Maximum height in pixels (maintains aspect ratio)
- `--preserve-metadata`: Keep EXIF data (default: strip)
- `--generate-report`: Create optimization report

### Step 4: Generate Comparison Report

Create a detailed report showing before/after metrics:

```bash
python3 scripts/optimize_images.py \
  --input /path/to/images/ \
  --output /path/to/optimized/ \
  --generate-report \
  --report-path /path/to/report.md
```

## Output Format

### Analysis JSON

```json
{
  "schema_version": "1.0",
  "analyzed_at": "2024-01-15T10:30:00Z",
  "images": [
    {
      "path": "/path/to/image.jpg",
      "filename": "image.jpg",
      "current_size_bytes": 2500000,
      "current_size_human": "2.4 MB",
      "dimensions": {"width": 3000, "height": 2000},
      "format": "JPEG",
      "color_space": "sRGB",
      "has_transparency": false,
      "detected_type": "photo",
      "type_confidence": 0.95,
      "recommendations": {
        "format": "webp",
        "quality": 82,
        "max_dimension": 2048,
        "estimated_size_bytes": 450000,
        "estimated_reduction_percent": 82
      }
    }
  ],
  "summary": {
    "total_images": 10,
    "total_current_size_bytes": 25000000,
    "total_estimated_size_bytes": 4500000,
    "estimated_reduction_percent": 82
  }
}
```

### Optimization Report (Markdown)

```markdown
# Image Optimization Report

Generated: 2024-01-15 10:35:00

## Summary

| Metric | Value |
|--------|-------|
| Images Processed | 10 |
| Original Total Size | 25.0 MB |
| Optimized Total Size | 4.5 MB |
| Size Reduction | 82% |
| Processing Time | 12.3s |

## Detailed Results

| File | Original | Optimized | Reduction | Format |
|------|----------|-----------|-----------|--------|
| image1.jpg | 2.4 MB | 450 KB | 82% | WebP |
| screenshot.png | 1.8 MB | 120 KB | 93% | WebP |
...
```

## Image Type Detection

The analyzer detects these image types with specialized optimization strategies:

| Type | Characteristics | Recommended Format | Quality Range |
|------|----------------|-------------------|---------------|
| Photo | High color variance, gradients, natural content | WebP/AVIF | 75-85 |
| Screenshot | Sharp edges, solid colors, text | PNG/WebP | 90-100 (lossless) |
| Diagram | Vector-like, limited colors, geometric shapes | PNG/SVG | 95-100 |
| Illustration | Flat colors, anti-aliased edges | PNG/WebP | 90-95 |
| Mixed | Combination of photo and graphics | WebP | 80-90 |

## Resources

- `scripts/analyze_image.py` -- Image type detection and recommendation engine
- `scripts/optimize_images.py` -- Batch optimization with target constraints
- `references/image-optimization-guide.md` -- Format comparison and best practices

## Key Principles

1. **Quality-First**: Never sacrifice visual quality below acceptable thresholds
2. **Format-Aware**: Select format based on image content, not just file extension
3. **Target-Driven**: Meet file size constraints through iterative quality adjustment
4. **Transparency-Safe**: Preserve alpha channels when present
5. **Batch-Efficient**: Process multiple images with progress tracking and reporting
