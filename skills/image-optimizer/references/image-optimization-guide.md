# Image Optimization Guide

## Format Comparison

### JPEG

**Best For**: Photographs, images with gradients
**Compression**: Lossy
**Transparency**: Not supported
**Animation**: Not supported

| Quality | Use Case | Typical Reduction |
|---------|----------|-------------------|
| 95-100 | Archival, print-ready | 20-30% |
| 85-94 | High-quality web | 50-70% |
| 75-84 | Standard web | 70-85% |
| 60-74 | Thumbnails, previews | 85-95% |

**Best Practices**:
- Use progressive encoding for web (`-interlace Plane`)
- Strip metadata for production (`-strip`)
- Use 4:2:0 chroma subsampling for smaller files
- Quality 80-85 is optimal for most web use cases

### PNG

**Best For**: Screenshots, diagrams, images with text, transparency
**Compression**: Lossless (or lossy with pngquant)
**Transparency**: Full alpha channel support
**Animation**: APNG supported

| Compression Level | Trade-off |
|-------------------|-----------|
| 0 | No compression, fastest |
| 1-3 | Fast compression |
| 4-6 | Balanced (default) |
| 7-9 | Maximum compression, slowest |

**Best Practices**:
- Use PNG-8 for images with <256 colors
- Use PNG-24/32 for photos or complex transparency
- Apply `pngquant` for lossy PNG compression (60-90% reduction)
- Use `optipng` or `pngcrush` for lossless optimization

### WebP

**Best For**: All web images (universal replacement for JPEG/PNG)
**Compression**: Lossy and lossless modes
**Transparency**: Full alpha channel support
**Animation**: Supported

| Mode | Quality | Use Case |
|------|---------|----------|
| Lossy | 75-85 | Photos, gradients |
| Lossy | 90-95 | Screenshots with some photo content |
| Lossless | N/A | Diagrams, pixel-perfect requirements |

**Typical Savings vs JPEG**: 25-35% smaller at equivalent quality
**Typical Savings vs PNG**: 26% smaller (lossless), 80%+ smaller (lossy)

**Best Practices**:
- Use lossy mode for photos (quality 75-85)
- Use lossless mode for diagrams and screenshots
- Provide JPEG/PNG fallback for older browsers
- Use `-define webp:method=6` for better compression (slower)

### AVIF

**Best For**: Maximum compression for modern browsers
**Compression**: Lossy and lossless
**Transparency**: Full alpha channel support
**Animation**: Supported

| Quality | Equivalent JPEG Quality |
|---------|-------------------------|
| 30-40 | JPEG 75-80 |
| 45-55 | JPEG 85-90 |
| 60-70 | JPEG 95+ |

**Typical Savings vs JPEG**: 50% smaller at equivalent quality
**Typical Savings vs WebP**: 20% smaller at equivalent quality

**Best Practices**:
- Use quality 30-50 for most web content
- Encoding is slower than WebP (consider build-time vs runtime)
- Not supported in older browsers (Safari < 16, Edge < 121)
- Use `speed` parameter to trade encoding time for compression

## Image Type Detection

### Photo Detection

Characteristics:
- High color variance (many unique colors)
- Smooth gradients between adjacent pixels
- Natural noise patterns
- High entropy in color distribution

Detection Metrics:
- Unique colors > 10,000 per 1M pixels
- Edge density < 15%
- Gradient smoothness > 0.7
- Color histogram entropy > 6.0 bits

### Screenshot Detection

Characteristics:
- Sharp edges (anti-aliased text and UI elements)
- Solid color regions
- Limited color palette
- Rectangular shapes

Detection Metrics:
- Unique colors < 5,000 per 1M pixels
- Edge density 15-40%
- Solid region coverage > 30%
- Horizontal/vertical edge dominance > 0.8

### Diagram Detection

Characteristics:
- Very limited color palette (<100 colors)
- Geometric shapes (circles, rectangles, lines)
- High contrast edges
- Minimal gradients

Detection Metrics:
- Unique colors < 500
- Edge density 20-50%
- Color count < 64 for most pixels
- Anti-aliasing present but limited

### Illustration Detection

Characteristics:
- Flat color regions with anti-aliased edges
- Moderate color count (100-5000)
- Artistic style (not photographic)
- May have transparency

Detection Metrics:
- Unique colors 500-5000
- Edge density 10-30%
- Large solid regions with smooth edges
- Possible alpha channel usage

## Quality Optimization Strategies

### Binary Search Quality

For target file size constraints, use binary search:

```
1. Start with estimated quality (based on image type)
2. Compress image, check file size
3. If too large: reduce quality by half the remaining range
4. If too small: increase quality by half the remaining range
5. Repeat until within 5% of target or quality delta < 1
```

### Resolution Scaling

For large images, consider resolution reduction:

| Target Use | Max Dimension | Typical Size |
|------------|---------------|--------------|
| Thumbnail | 150-200px | 5-20 KB |
| Preview | 400-600px | 30-80 KB |
| Mobile | 800-1200px | 50-150 KB |
| Desktop | 1920-2560px | 100-400 KB |
| Retina | 3840-5120px | 200-800 KB |

### Chroma Subsampling

JPEG chroma subsampling affects quality and size:

| Subsampling | Quality | Size |
|-------------|---------|------|
| 4:4:4 | Best color accuracy | Largest |
| 4:2:2 | Good for most photos | Medium |
| 4:2:0 | Acceptable for web | Smallest |

Use 4:4:4 for images with fine color detail or text.
Use 4:2:0 for typical photos and web content.

## Metadata Handling

### Metadata to Strip

- EXIF camera data (focal length, exposure, GPS)
- Thumbnail previews
- Software metadata
- Comments and annotations

### Metadata to Preserve (Optional)

- Color profile (sRGB conversion recommended)
- Copyright information
- Orientation (apply and strip)

### Command Examples

```bash
# Strip all metadata
magick input.jpg -strip output.jpg

# Preserve color profile only
magick input.jpg -strip +profile icc output.jpg

# Apply orientation and strip EXIF
magick input.jpg -auto-orient -strip output.jpg
```

## Batch Processing Best Practices

### Progress Tracking

- Show percentage complete
- Display estimated time remaining
- Report current file being processed
- Summarize results at completion

### Error Handling

- Skip corrupted files with warning
- Log failures to separate error report
- Continue processing remaining files
- Exit with non-zero code if any failures

### Resource Management

- Limit concurrent processes for memory-constrained systems
- Use temporary files for intermediate results
- Clean up temporary files on completion or failure

## Tool-Specific Settings

### ImageMagick (magick)

```bash
# High-quality JPEG
magick input.jpg -strip -interlace Plane -sampling-factor 4:2:0 \
  -quality 85 -define jpeg:dct-method=float output.jpg

# Optimized PNG
magick input.png -strip -define png:compression-level=9 \
  -define png:compression-filter=5 output.png

# WebP (lossy)
magick input.jpg -quality 82 -define webp:method=6 output.webp

# WebP (lossless)
magick input.png -define webp:lossless=true output.webp
```

### cwebp (WebP encoder)

```bash
# Lossy with quality
cwebp -q 82 -m 6 input.jpg -o output.webp

# Lossless
cwebp -lossless -z 9 input.png -o output.webp

# With target size (in bytes)
cwebp -size 100000 input.jpg -o output.webp

# With alpha (from PNG)
cwebp -q 82 -alpha_q 90 input.png -o output.webp
```

### avifenc (AVIF encoder)

```bash
# Standard quality
avifenc -s 6 -q 50 input.jpg output.avif

# High quality
avifenc -s 4 -q 60 input.jpg output.avif

# Lossless
avifenc -s 0 -l input.png output.avif
```

## Browser Support Matrix

| Format | Chrome | Firefox | Safari | Edge |
|--------|--------|---------|--------|------|
| JPEG | Yes | Yes | Yes | Yes |
| PNG | Yes | Yes | Yes | Yes |
| WebP | 32+ | 65+ | 14+ | 18+ |
| AVIF | 85+ | 93+ | 16+ | 121+ |

For maximum compatibility, provide fallbacks:
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description">
</picture>
```
