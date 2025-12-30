# Format Conversion Guide

## Supported Formats Overview

ImageMagick supports 200+ image formats. Most commonly used formats:

| Format | Extension | Features | Best For |
|--------|-----------|----------|----------|
| **JPEG** | .jpg, .jpeg | Lossy compression, small size | Photos, web images |
| **PNG** | .png | Lossless, transparency support | Graphics, screenshots |
| **WebP** | .webp | Modern, lossy/lossless, small size | Web optimization |
| **GIF** | .gif | Animation, 256 colors max | Simple animations, icons |
| **TIFF** | .tif, .tiff | Lossless, high quality | Print, archival |
| **BMP** | .bmp | Uncompressed, Windows native | Legacy compatibility |
| **HEIC** | .heic | Modern Apple format, efficient | iPhone photos |
| **AVIF** | .avif | Next-gen, excellent compression | Modern web |
| **SVG** | .svg | Vector graphics | Scalable graphics |
| **PDF** | .pdf | Document format | Multi-page documents |
| **EPS** | .eps | PostScript vector | Print graphics |
| **RAW** | Various | Camera raw data | Photography workflow |

## JPEG Conversion

### Quality Settings

Quality range: 1-100 (higher = better quality, larger file)

```bash
# Web standard (good balance)
magick input.png -quality 85 output.jpg

# High quality (minimal loss)
magick input.png -quality 95 output.jpg

# Small file (visible compression)
magick input.png -quality 60 output.jpg

# Maximum compression
magick input.png -quality 30 output.jpg
```

### Progressive JPEG

```bash
# Progressive (better web loading)
magick input.png -interlace Plane -quality 85 output.jpg

# Baseline (standard)
magick input.png -interlace None -quality 85 output.jpg
```

### Strip Metadata

```bash
# Remove EXIF, comments, profiles
magick input.png -strip output.jpg

# Keep color profile, remove other metadata
magick input.png -strip +profile "icc" output.jpg
```

### Subsampling

```bash
# 4:2:0 subsampling (default, smaller file)
magick input.png -sampling-factor 2x2 -quality 85 output.jpg

# 4:4:4 subsampling (no subsampling, sharper)
magick input.png -sampling-factor 1x1 -quality 85 output.jpg
```

## PNG Conversion

### Compression Level

Compression levels: 0-9 (higher = smaller file, slower)

```bash
# Maximum compression
magick input.jpg -define png:compression-level=9 output.png

# Fast compression
magick input.jpg -define png:compression-level=1 output.png

# Balanced
magick input.jpg -define png:compression-level=6 output.png
```

### Color Types

```bash
# True color (RGB)
magick input.jpg -type TrueColor output.png

# True color with alpha
magick input.jpg -type TrueColorAlpha output.png

# Grayscale
magick input.jpg -type Grayscale output.png

# Palette (indexed, 256 colors max)
magick input.jpg -type Palette output.png

# Reduce to specific number of colors
magick input.jpg -colors 16 output.png
```

### Bit Depth

```bash
# 8-bit per channel (standard)
magick input.tiff -depth 8 output.png

# 16-bit per channel (high precision)
magick input.tiff -depth 16 output.png
```

### Transparency

```bash
# Add transparency
magick input.jpg -alpha set output.png

# Remove transparency (flatten to white)
magick input.png -background white -alpha remove output.png

# Make white pixels transparent
magick input.png -transparent white output.png

# Make specific color transparent
magick input.png -fuzz 10% -transparent "#FFFFFF" output.png
```

## WebP Conversion

### Quality Settings

```bash
# Lossy compression
magick input.png -quality 80 output.webp

# Lossless
magick input.png -define webp:lossless=true output.webp

# Near-lossless
magick input.png -define webp:near-lossless=60 output.webp
```

### Advanced Options

```bash
# With alpha quality
magick input.png -quality 80 -define webp:alpha-quality=90 output.webp

# Target file size (approximate)
magick input.png -define webp:target-size=50000 output.webp

# Compression method (0-6, higher = slower/better)
magick input.png -define webp:method=6 output.webp
```

## GIF Conversion

### Color Reduction

GIF supports max 256 colors.

```bash
# Default conversion
magick input.png output.gif

# Specify colors
magick input.png -colors 64 output.gif
magick input.png -colors 128 output.gif

# Better color matching with dithering
magick input.png -dither FloydSteinberg -colors 256 output.gif

# No dithering (flat colors)
magick input.png +dither -colors 256 output.gif
```

### Transparency

```bash
# Preserve transparency
magick input.png -transparent-color white output.gif

# Single transparent color
magick input.png -transparent white output.gif
```

## TIFF Conversion

### Compression Options

```bash
# LZW compression (lossless)
magick input.jpg -compress LZW output.tiff

# ZIP compression (lossless)
magick input.jpg -compress Zip output.tiff

# JPEG compression (lossy, small file)
magick input.jpg -compress JPEG -quality 90 output.tiff

# No compression
magick input.jpg -compress None output.tiff
```

### Multi-page TIFF

```bash
# Combine multiple images
magick page1.png page2.png page3.png output.tiff

# Extract pages
magick input.tiff[0] page1.png
magick input.tiff page_%d.png
```

## HEIC/HEIF Conversion

```bash
# HEIC to JPEG
magick input.heic output.jpg

# JPEG to HEIC
magick input.jpg -quality 80 output.heic

# Batch conversion from iPhone photos
for f in *.HEIC; do
    magick "$f" "${f%.HEIC}.jpg"
done
```

## AVIF Conversion

```bash
# Convert to AVIF
magick input.png -quality 80 output.avif

# Lossless AVIF
magick input.png -define avif:lossless=true output.avif
```

## PDF Conversion

### PDF to Image

```bash
# High quality PNG (300 DPI)
magick -density 300 document.pdf pages_%03d.png

# JPEG with quality
magick -density 300 -quality 90 document.pdf pages_%03d.jpg

# Specific page
magick -density 300 document.pdf[0] first_page.png

# Handle transparency
magick -density 300 -background white -alpha remove document.pdf page.png
```

### Image to PDF

```bash
# Basic conversion
magick image.png output.pdf

# Multiple images
magick page1.png page2.png page3.png output.pdf

# With compression
magick *.jpg -compress jpeg -quality 85 output.pdf

# A4 page size
magick *.jpg -page A4 -gravity center output.pdf
```

## Color Space Conversion

### RGB to CMYK

```bash
# For print
magick input.jpg -colorspace CMYK output.tiff

# With specific profile
magick input.jpg -profile sRGB.icc -profile USWebCoatedSWOP.icc output.tiff
```

### Grayscale Conversion

```bash
# Standard grayscale
magick input.jpg -colorspace Gray output.jpg

# Preserve luminance
magick input.jpg -grayscale Rec709Luma output.jpg

# Alternative methods
magick input.jpg -grayscale Rec601Luma output.jpg
magick input.jpg -grayscale Average output.jpg
```

### sRGB Standardization

```bash
# Ensure sRGB color space
magick input.jpg -colorspace sRGB output.jpg

# Strip profile and convert to sRGB
magick input.jpg -strip -colorspace sRGB output.jpg
```

## Best Practices

### Web Images

```bash
# JPEG for photos
magick photo.png -strip -interlace Plane -quality 85 photo.jpg

# PNG for graphics with transparency
magick graphic.psd -strip -define png:compression-level=9 graphic.png

# WebP for modern browsers
magick image.png -quality 80 image.webp
```

### Print Images

```bash
# High-resolution TIFF
magick input.jpg -density 300 -colorspace CMYK -compress LZW output.tiff
```

### Archival

```bash
# Lossless PNG
magick input.jpg -depth 16 -define png:compression-level=9 archive.png

# Uncompressed TIFF
magick input.jpg -compress None archive.tiff
```

## Format Detection

```bash
# Identify format
magick identify image.unknown
magick identify -format "%m\n" image.unknown

# Check if animated
magick identify image.gif | wc -l  # >1 = animated

# Check color space
magick identify -format "%[colorspace]\n" image.jpg
```
