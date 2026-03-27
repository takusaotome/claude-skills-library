# Image Optimization Guide

## Overview

This guide covers image optimization strategies for document processing. Understanding how to balance quality, file size, and compatibility is essential for producing optimal output.

## Image Format Comparison

### Format Characteristics

| Format | Compression | Transparency | Animation | Best For |
|--------|-------------|--------------|-----------|----------|
| JPEG | Lossy | No | No | Photographs |
| PNG | Lossless | Yes | No | Screenshots, diagrams |
| WebP | Both | Yes | Yes | Web delivery |
| GIF | Lossless (256 colors) | Yes | Yes | Simple graphics |
| TIFF | Both | Yes | No | Archival, print |

### Format Selection Decision Tree

```
Is the image a photograph?
├─ Yes → JPEG (or WebP for web)
└─ No → Does it need transparency?
         ├─ Yes → PNG (or WebP for web)
         └─ No → Is it for web delivery?
                  ├─ Yes → WebP
                  └─ No → PNG for diagrams, JPEG for mixed content
```

## Quality Settings

### JPEG Quality

JPEG quality is controlled by a 0-100 scale where higher values mean better quality but larger files.

| Quality | Description | Use Case |
|---------|-------------|----------|
| 95-100 | Maximum quality | Print production |
| 85-95 | High quality | Professional documents |
| 75-85 | Good quality | General purpose |
| 60-75 | Medium quality | Web thumbnails |
| <60 | Low quality | Extreme compression |

**ImageMagick command:**
```bash
magick input.png -quality 85 output.jpg
```

### WebP Quality

WebP supports both lossy and lossless compression.

**Lossy WebP:**
```bash
magick input.png -quality 80 output.webp
```

**Lossless WebP:**
```bash
magick input.png -define webp:lossless=true output.webp
```

### PNG Compression

PNG uses lossless compression. The compression level (0-9) affects file size and encoding time, not quality.

```bash
# Maximum compression (slowest encoding)
magick input.jpg -define png:compression-level=9 output.png

# Fast compression
magick input.jpg -define png:compression-level=1 output.png
```

## Resolution and DPI

### Understanding DPI

DPI (dots per inch) describes the relationship between pixel dimensions and physical print size.

```
Physical Size (inches) = Pixel Dimensions / DPI
```

**Example:** A 3000×2000 pixel image at 300 DPI prints as 10"×6.67"

### Recommended DPI by Use Case

| Use Case | DPI | Notes |
|----------|-----|-------|
| Screen display | 72-96 | Most monitors |
| Web images | 72-96 | Smaller file size |
| Office printing | 150 | Acceptable quality |
| Professional print | 300 | Standard for publications |
| High-quality print | 600 | Fine detail preservation |

### Setting DPI with ImageMagick

```bash
# Set DPI metadata (does not resample)
magick input.png -density 300 output.png

# Resample to target DPI and physical size
magick input.png -density 300 -units PixelsPerInch -resize 2400x output.png
```

## Resizing Strategies

### Resize Filters

Different filters produce different quality results when scaling images.

| Filter | Quality | Speed | Best For |
|--------|---------|-------|----------|
| Lanczos | Excellent | Slow | Downscaling photographs |
| Mitchell | Very Good | Medium | General purpose |
| Catrom | Very Good | Medium | Upscaling |
| Triangle | Fair | Fast | Quick previews |
| Point | Nearest neighbor | Fastest | Pixel art, no interpolation |

**ImageMagick command:**
```bash
magick input.png -filter Lanczos -resize 800x output.png
```

### Downscaling Guidelines

1. **Calculate target dimensions** based on display/print requirements
2. **Use high-quality filter** (Lanczos or Mitchell)
3. **Apply sharpening** after resize to restore edge definition

```bash
# High-quality downscale with sharpening
magick input.png \
    -filter Lanczos \
    -resize 800x600 \
    -unsharp 0x0.5+0.5+0 \
    output.png
```

### Upscaling Guidelines

Upscaling should generally be avoided as it cannot add detail. When necessary:

1. Use a smooth filter (Catrom, Mitchell)
2. Limit upscaling to 2x maximum
3. Consider using AI upscaling tools for better results

```bash
# Conservative upscale
magick input.png -filter Catrom -resize 200% output.png
```

## Color Space Management

### Color Spaces

| Color Space | Use Case |
|-------------|----------|
| sRGB | Web, screen display (standard) |
| Adobe RGB | Professional photography |
| CMYK | Print production |
| Grayscale | Black and white documents |

### Converting Color Spaces

```bash
# Convert to sRGB (web-safe)
magick input.png -colorspace sRGB output.png

# Convert to grayscale
magick input.png -colorspace Gray output.png

# Convert to CMYK for print
magick input.png -colorspace CMYK output.tiff
```

### Color Profile Handling

```bash
# Strip all color profiles (for web)
magick input.jpg -strip output.jpg

# Embed sRGB profile
magick input.png -profile sRGB.icc output.png
```

## Batch Optimization Patterns

### Directory Processing

```bash
# Convert all PNG to WebP with quality 80
for f in *.png; do
    magick "$f" -quality 80 "${f%.png}.webp"
done

# Resize all JPEG to max 1920px width
for f in *.jpg; do
    magick "$f" -resize "1920x>" "$f"
done
```

### Parallel Processing

```bash
# Process in parallel (4 workers)
find . -name "*.png" | xargs -P 4 -I {} sh -c '
    magick "{}" -filter Lanczos -resize 800x -quality 85 "{}.optimized.jpg"
'
```

### Using mogrify for In-Place Editing

```bash
# Resize all images in place
mogrify -resize 1920x -quality 85 *.jpg

# Convert format and output to different directory
mogrify -path ./optimized -format webp -quality 80 *.png
```

## Document-Specific Optimization

### Screenshots and UI Images

- Use PNG or WebP (lossless if text-heavy)
- Avoid JPEG (creates artifacts around text)
- Crop unnecessary areas
- Consider reducing color depth for simple UIs

```bash
# Optimize screenshot
magick screenshot.png \
    -trim \
    -bordercolor white -border 10 \
    -define png:compression-level=9 \
    output.png
```

### Photographs in Documents

- Use JPEG or WebP lossy
- Resize to actual display dimensions
- Strip metadata for privacy and size
- Apply subtle sharpening after resize

```bash
# Optimize photograph for document
magick photo.jpg \
    -strip \
    -filter Lanczos \
    -resize 1200x \
    -unsharp 0x0.5+0.5+0 \
    -quality 85 \
    output.jpg
```

### Diagrams and Charts

- Use PNG for sharp lines and text
- Use WebP lossless for web delivery
- Avoid JPEG (text will be blurry)
- Maintain sufficient resolution for readability

```bash
# Optimize diagram
magick diagram.png \
    -define png:compression-level=9 \
    -strip \
    output.png
```

### Scanned Documents

- Binarize pure text pages (black and white)
- Use grayscale for text with images
- Apply deskew and despeckle
- Target 300 DPI for OCR

```bash
# Prepare scan for OCR
magick scan.png \
    -deskew 40% \
    -despeckle \
    -normalize \
    -density 300 \
    output.png
```

## Quality Assessment

### Visual Inspection Points

1. **Text clarity** — Edges should be sharp, no halos
2. **Gradient smoothness** — No banding in color transitions
3. **Detail preservation** — Fine textures maintained
4. **Artifact absence** — No blocking, ringing, or mosquito noise

### Automated Quality Metrics

**SSIM (Structural Similarity):**
```bash
magick compare -metric SSIM original.png optimized.jpg null:
# Returns value between 0 and 1 (1 = identical)
```

**PSNR (Peak Signal-to-Noise Ratio):**
```bash
magick compare -metric PSNR original.png optimized.jpg null:
# Higher is better, >40dB is excellent
```

### File Size Targets

| Document Type | Target Size per Page |
|---------------|---------------------|
| Text-only PDF | 50-100 KB |
| Mixed content | 100-300 KB |
| Image-heavy | 300-500 KB |
| Photo gallery | 500 KB-1 MB |

## Preset Implementations

### Web Preset Implementation

```bash
# Web optimization: WebP, 80%, max 1920px, strip metadata
magick input.png \
    -strip \
    -filter Lanczos \
    -resize "1920x1080>" \
    -quality 80 \
    output.webp
```

### Print Preset Implementation

```bash
# Print optimization: JPEG 95%, 300 DPI, preserve metadata
magick input.png \
    -filter Lanczos \
    -density 300 \
    -units PixelsPerInch \
    -quality 95 \
    output.jpg
```

### Archive Preset Implementation

```bash
# Archive optimization: JPEG 90%, max 2400px, minimal metadata
magick input.png \
    -strip \
    +profile "!icc" \
    -filter Lanczos \
    -resize "2400x2400>" \
    -quality 90 \
    output.jpg
```

### Minimal Preset Implementation

```bash
# Minimal optimization: WebP 70%, max 1280px, maximum compression
magick input.png \
    -strip \
    -filter Triangle \
    -resize "1280x720>" \
    -quality 70 \
    output.webp
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Blurry text | JPEG compression | Use PNG or higher quality |
| Color banding | Low bit depth | Use 24-bit color, higher quality |
| File too large | Inefficient format | Try WebP, reduce dimensions |
| Visible artifacts | Quality too low | Increase quality setting |
| Colors look wrong | Profile mismatch | Convert to sRGB, strip profiles |

### ImageMagick Policy Issues

If ImageMagick operations fail due to policy restrictions:

1. Check policy file: `/etc/ImageMagick-*/policy.xml`
2. Increase resource limits for large images
3. Enable PDF/PS codecs if needed

```xml
<!-- Example policy modifications -->
<policy domain="resource" name="memory" value="2GiB"/>
<policy domain="resource" name="disk" value="8GiB"/>
<policy domain="coder" rights="read|write" pattern="PDF"/>
```
