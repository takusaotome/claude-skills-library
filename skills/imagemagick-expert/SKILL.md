---
name: imagemagick-expert
description: ImageMagick CLIを使用した画像処理の専門家スキル。フォーマット変換、リサイズ、トリミング、回転、フィルタ適用、アニメーションGIF作成、PDF処理、バッチ処理を支援。Use when processing images via CLI, converting formats, resizing, cropping, applying filters, creating animations, or batch processing images.
---

# ImageMagick Expert Skill

## Overview

ImageMagickは画像の作成、編集、合成、変換を行うための強力なCLIツールセットです。200以上の画像フォーマットをサポートし、リサイズ、回転、トリミング、色調整、フィルタ適用、アニメーション作成など幅広い画像処理が可能です。

### Primary Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `magick` | メインコマンド（v7+）、画像変換・処理 | `magick input.png output.jpg` |
| `convert` | 画像変換・処理（レガシー、v6互換） | `convert input.png output.jpg` |
| `identify` | 画像情報の取得 | `identify -verbose image.png` |
| `mogrify` | 画像のインプレース変換 | `mogrify -resize 50% *.jpg` |
| `composite` | 画像の合成 | `composite overlay.png base.png result.png` |
| `montage` | 複数画像のモンタージュ作成 | `montage *.jpg -tile 3x3 montage.jpg` |

## When to Use This Skill

- 画像フォーマットの変換（PNG↔JPEG↔WebP↔GIF等）
- 画像のリサイズ、トリミング、回転
- バッチ処理で複数画像を一括変換
- 画像へのエフェクト・フィルタ適用
- アニメーションGIFの作成・編集
- PDF↔画像の相互変換
- 画像情報（サイズ、フォーマット、メタデータ）の取得
- 画像の結合・モンタージュ作成

## Prerequisites

```bash
# Check installation
magick --version

# macOS (Homebrew)
brew install imagemagick

# Linux (Ubuntu/Debian)
sudo apt-get install imagemagick

# Linux (CentOS/RHEL)
sudo yum install ImageMagick
```

## Core Operations

### Format Conversion

```bash
# Basic conversion
magick input.png output.jpg
magick input.jpg output.webp
magick input.gif output.png

# With quality setting (JPEG/WebP)
magick input.png -quality 85 output.jpg
magick input.png -quality 90 output.webp

# PNG compression level (0-9)
magick input.jpg -define png:compression-level=9 output.png

# Convert to grayscale
magick input.png -colorspace Gray output.png

# Convert to specific color depth
magick input.png -depth 8 output.png
```

### Image Information

```bash
# Basic info (format, dimensions, color depth)
magick identify image.png

# Verbose info (all metadata)
magick identify -verbose image.png

# Specific properties
magick identify -format "%w x %h\n" image.png
magick identify -format "Format: %m\nSize: %wx%h\nDepth: %z-bit\n" image.png

# JSON output
magick identify -format "%[json:*]" image.png

# Batch info
magick identify *.jpg
```

### Resize Operations

```bash
# Resize to width (maintain aspect ratio)
magick input.png -resize 800x output.png

# Resize to height (maintain aspect ratio)
magick input.png -resize x600 output.png

# Resize to fit within dimensions (maintain aspect ratio)
magick input.png -resize 800x600 output.png

# Resize to exact dimensions (ignore aspect ratio)
magick input.png -resize 800x600! output.png

# Resize by percentage
magick input.png -resize 50% output.png

# Resize only if larger (shrink only)
magick input.png -resize "800x600>" output.png

# Resize only if smaller (enlarge only)
magick input.png -resize "800x600<" output.png

# High-quality resize (Lanczos filter)
magick input.png -filter Lanczos -resize 800x output.png

# Thumbnail (faster, for previews)
magick input.png -thumbnail 200x200 output.png
```

### Crop and Trim

```bash
# Crop WxH+X+Y (width x height from position X,Y)
magick input.png -crop 400x300+100+50 output.png

# Center crop
magick input.png -gravity center -crop 400x300+0+0 output.png

# Trim whitespace/borders
magick input.png -trim output.png

# Trim with fuzz tolerance (for near-white)
magick input.png -fuzz 10% -trim output.png

# Add border after trim
magick input.png -trim -bordercolor white -border 10 output.png

# Crop to square (center)
magick input.png -gravity center -crop 1:1 output.png
```

### Rotation and Flip

```bash
# Rotate clockwise
magick input.png -rotate 90 output.png
magick input.png -rotate 180 output.png
magick input.png -rotate 270 output.png

# Rotate counter-clockwise
magick input.png -rotate -90 output.png

# Rotate with background fill
magick input.png -background white -rotate 45 output.png

# Auto-rotate based on EXIF
magick input.jpg -auto-orient output.jpg

# Flip (vertical mirror)
magick input.png -flip output.png

# Flop (horizontal mirror)
magick input.png -flop output.png
```

## Effects and Filters

### Blur and Sharpen

```bash
# Gaussian blur (radius x sigma)
magick input.png -blur 0x8 output.png
magick input.png -gaussian-blur 0x3 output.png

# Motion blur (radius x sigma, angle)
magick input.png -motion-blur 0x12+45 output.png

# Sharpen
magick input.png -sharpen 0x1 output.png

# Unsharp mask (more control)
magick input.png -unsharp 0x1+1+0.05 output.png

# Noise reduction
magick input.png -despeckle output.png
magick input.png -noise 2 output.png
```

### Color Adjustments

```bash
# Brightness-Contrast (brightness x contrast)
magick input.png -brightness-contrast 10x5 output.png

# Modulate (brightness, saturation, hue) - percentages
magick input.png -modulate 110,120,100 output.png

# Level adjustment (black-point, gamma, white-point)
magick input.png -level 10%,1.2,90% output.png

# Auto-level (stretch contrast)
magick input.png -auto-level output.png

# Normalize (enhance contrast)
magick input.png -normalize output.png

# Enhance (simple improvement)
magick input.png -enhance output.png

# Negate (invert colors)
magick input.png -negate output.png

# Sepia tone
magick input.png -sepia-tone 80% output.png

# Colorize
magick input.png -colorize 30%,0%,0% output.png  # Add red tint
```

### Artistic Effects

```bash
# Charcoal sketch
magick input.png -charcoal 2 output.png

# Pencil sketch
magick input.png -sketch 0x10+120 output.png

# Oil painting
magick input.png -paint 4 output.png

# Emboss
magick input.png -emboss 0x1 output.png

# Edge detection
magick input.png -edge 1 output.png

# Posterize
magick input.png -posterize 4 output.png

# Solarize
magick input.png -solarize 50% output.png

# Vignette
magick input.png -vignette 0x50 output.png

# Polaroid effect
magick input.png -polaroid 0 output.png
```

## Animation and GIF

### Create Animation

```bash
# Create GIF from multiple images
magick -delay 100 frame_*.png animation.gif

# Delay in centiseconds (100 = 1 second)
magick -delay 50 *.png animation.gif  # 0.5 second per frame

# Set loop count (0 = infinite)
magick -delay 100 -loop 0 *.png animation.gif

# Different delays per frame
magick \( -delay 100 frame1.png \) \( -delay 200 frame2.png \) \( -delay 100 frame3.png \) animation.gif

# Resize during creation
magick -delay 100 *.png -resize 400x animation.gif
```

### Optimize GIF

```bash
# Optimize layers
magick animation.gif -layers Optimize optimized.gif

# Optimize colors (reduce palette)
magick animation.gif -colors 64 optimized.gif

# Optimize with coalesce first
magick animation.gif -coalesce -layers Optimize optimized.gif

# Reduce file size
magick animation.gif -fuzz 5% -layers Optimize optimized.gif
```

### Extract Frames

```bash
# Extract all frames
magick animation.gif frame_%03d.png

# Extract specific frame (0-indexed)
magick animation.gif[0] first_frame.png
magick animation.gif[5] sixth_frame.png

# Extract range
magick animation.gif[0-4] frame_%d.png
```

### Modify Animation

```bash
# Change speed (double speed)
magick animation.gif -delay 50 faster.gif

# Reverse animation
magick animation.gif -reverse reversed.gif

# Add frame to existing GIF
magick animation.gif new_frame.png -append updated.gif

# Coalesce (flatten for editing)
magick animation.gif -coalesce frames_%03d.png
```

## PDF Processing

### PDF to Images

```bash
# Convert all pages to PNG
magick -density 300 document.pdf page_%03d.png

# Specific page (0-indexed)
magick -density 300 document.pdf[0] first_page.png
magick -density 300 document.pdf[2] third_page.png

# Page range
magick -density 300 document.pdf[0-2] page_%d.png

# With quality settings
magick -density 300 -quality 90 document.pdf page_%03d.jpg

# Transparent background
magick -density 300 -background white -alpha remove document.pdf page_%03d.png
```

### Images to PDF

```bash
# Multiple images to PDF
magick *.jpg output.pdf

# With compression
magick *.jpg -compress jpeg -quality 85 output.pdf

# Specific page size
magick *.jpg -page A4 output.pdf

# Resize to fit
magick *.jpg -resize 595x842 output.pdf  # A4 at 72dpi
```

## Batch Processing

### Using mogrify (In-Place)

```bash
# Convert all PNG to JPEG
mogrify -format jpg *.png

# Resize all images
mogrify -resize 800x *.jpg

# Output to different directory
mogrify -path ./resized -resize 50% *.jpg

# Multiple operations
mogrify -resize 800x -quality 85 -format jpg *.png
```

### Using Shell Loop

```bash
# Process with custom naming
for f in *.png; do
    magick "$f" -resize 800x "${f%.png}_resized.png"
done

# Convert with counter
i=1; for f in *.jpg; do
    magick "$f" -resize 400x "thumb_$(printf "%03d" $i).jpg"
    ((i++))
done

# Parallel processing
find . -name "*.png" | xargs -P 4 -I {} magick {} -resize 50% {}.resized.png
```

### Using find

```bash
# Recursive processing
find . -name "*.jpg" -exec magick {} -resize 800x {} \;

# With output directory
find . -name "*.png" -exec sh -c 'magick "$1" -resize 50% "./output/$(basename "$1")"' _ {} \;
```

## Composite and Montage

### Image Composition

```bash
# Overlay image
magick base.png overlay.png -composite result.png

# With gravity
magick base.png overlay.png -gravity center -composite result.png

# With transparency
magick base.png \( overlay.png -alpha set -channel A -evaluate set 50% \) -composite result.png

# Watermark
magick photo.jpg -gravity southeast \( watermark.png -resize 200x \) -composite output.jpg
```

### Montage

```bash
# Basic grid
magick montage *.jpg -tile 3x3 -geometry +5+5 montage.jpg

# With labels
magick montage *.jpg -tile 3x3 -geometry +5+5 -label "%f" montage.jpg

# Custom size
magick montage *.jpg -tile 4x -geometry 200x200+10+10 montage.jpg

# With background
magick montage *.jpg -tile 3x3 -geometry +5+5 -background white montage.jpg
```

## Common Workflows

### Thumbnail Generation

```bash
# Square thumbnail with center crop
magick input.jpg -thumbnail 200x200^ -gravity center -extent 200x200 thumb.jpg

# Thumbnail with border
magick input.jpg -thumbnail 200x200 -bordercolor gray -border 2 thumb.jpg
```

### Web Optimization

```bash
# JPEG optimization
magick input.jpg -strip -interlace Plane -quality 85 output.jpg

# WebP conversion
magick input.jpg -quality 80 output.webp

# PNG optimization
magick input.png -strip -define png:compression-level=9 output.png
```

### Photo Enhancement

```bash
# Auto-enhance
magick input.jpg -auto-orient -auto-level -normalize output.jpg

# Subtle sharpening
magick input.jpg -unsharp 0x0.5+0.5+0 output.jpg
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `convert: not authorized` | Policy restriction | Edit `/etc/ImageMagick-*/policy.xml` |
| Memory error | Large image | Use `-limit memory 2GB` |
| Slow processing | High resolution | Use `-thumbnail` instead of `-resize` |
| Color shift (JPEG) | Color profile | Use `-strip` or `-colorspace sRGB` |

### Policy Configuration

For PDF processing issues, edit policy.xml:

```xml
<!-- Allow PDF read/write -->
<policy domain="coder" rights="read|write" pattern="PDF" />
```

### Memory Limits

```bash
# Set memory limits
magick -limit memory 2GB -limit map 4GB input.png output.png

# Check current limits
magick -list resource
```

## Reference Files

For detailed information, refer to:

- **references/format_conversion.md** - Format-specific options and best practices
- **references/image_manipulation.md** - Advanced manipulation techniques
- **references/batch_processing.md** - Batch processing patterns and scripts
