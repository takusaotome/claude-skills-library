# Image Manipulation Guide

## Geometry Syntax

ImageMagick uses a specific geometry syntax for resize, crop, and positioning.

### Basic Geometry Format

```
WxH+X+Y
```

| Component | Meaning | Example |
|-----------|---------|---------|
| `W` | Width | `800` |
| `H` | Height | `600` |
| `+X` | X offset (from left) | `+100` |
| `+Y` | Y offset (from top) | `+50` |
| `-X` | X offset (from right) | `-100` |
| `-Y` | Y offset (from bottom) | `-50` |

### Geometry Modifiers

| Modifier | Meaning | Example |
|----------|---------|---------|
| `!` | Ignore aspect ratio | `800x600!` |
| `>` | Only shrink if larger | `800x600>` |
| `<` | Only enlarge if smaller | `800x600<` |
| `^` | Fill area (may exceed) | `800x600^` |
| `%` | Percentage | `50%` |
| `@` | Maximum pixel count | `10000@` |

## Resize Operations

### Resize Algorithms

```bash
# Default (Mitchell for downscale, Lanczos for upscale)
magick input.png -resize 800x output.png

# Specific filters
magick input.png -filter Point -resize 200% output.png      # Nearest neighbor (pixelated)
magick input.png -filter Box -resize 50% output.png         # Box averaging
magick input.png -filter Triangle -resize 50% output.png    # Bilinear
magick input.png -filter Hermite -resize 50% output.png     # Smooth
magick input.png -filter Catrom -resize 50% output.png      # Catmull-Rom
magick input.png -filter Mitchell -resize 50% output.png    # Mitchell-Netravali
magick input.png -filter Lanczos -resize 200% output.png    # Lanczos (sharpest)
magick input.png -filter Sinc -resize 50% output.png        # Sinc
```

### Resize vs Scale vs Sample vs Thumbnail

```bash
# resize: Full quality, uses filter
magick input.png -resize 400x output.png

# scale: Fast, simple averaging
magick input.png -scale 400x output.png

# sample: Fastest, point sampling (no interpolation)
magick input.png -sample 400x output.png

# thumbnail: Optimized for thumbnails (strips profiles, faster)
magick input.png -thumbnail 200x200 output.png
```

### Aspect Ratio Handling

```bash
# Fit within box (default, maintains ratio)
magick input.png -resize 800x600 output.png

# Fill box, crop excess (for exact dimensions)
magick input.png -resize 800x600^ -gravity center -extent 800x600 output.png

# Stretch to exact size (distorts image)
magick input.png -resize 800x600! output.png

# Shrink only if larger
magick input.png -resize "800x600>" output.png

# Enlarge only if smaller
magick input.png -resize "800x600<" output.png
```

## Crop Operations

### Basic Cropping

```bash
# Crop to size from top-left
magick input.png -crop 400x300+0+0 output.png

# Crop from specific position
magick input.png -crop 400x300+100+50 output.png

# Crop from center
magick input.png -gravity center -crop 400x300+0+0 +repage output.png

# Crop percentage
magick input.png -crop 50%x50%+0+0 output.png
```

### Gravity-Based Cropping

Gravity determines the reference point for positioning:

```
NorthWest  North  NorthEast
West       Center       East
SouthWest  South  SouthEast
```

```bash
# Crop from top-left
magick input.png -gravity NorthWest -crop 400x300+0+0 output.png

# Crop from center
magick input.png -gravity Center -crop 400x300+0+0 output.png

# Crop from bottom-right
magick input.png -gravity SouthEast -crop 400x300+0+0 output.png
```

### Trim (Auto-Crop)

```bash
# Trim borders of single color
magick input.png -trim output.png

# Trim with fuzz tolerance (for near-matching colors)
magick input.png -fuzz 10% -trim output.png

# Trim and add padding
magick input.png -trim -bordercolor white -border 20 output.png

# Trim specific color
magick input.png -bordercolor "#FFFFFF" -border 1x1 -trim output.png
```

### Extent (Canvas Size)

```bash
# Extend canvas (add padding)
magick input.png -gravity center -background white -extent 1000x1000 output.png

# Crop to exact size (from center)
magick input.png -gravity center -extent 800x600 output.png

# Position image on larger canvas
magick input.png -gravity NorthWest -background white -extent 1000x1000 output.png
```

## Rotation and Transformation

### Rotation

```bash
# Rotate by degrees (positive = clockwise)
magick input.png -rotate 90 output.png
magick input.png -rotate 180 output.png
magick input.png -rotate -45 output.png

# Rotate with background fill
magick input.png -background white -rotate 45 output.png
magick input.png -background transparent -rotate 45 output.png

# Auto-rotate based on EXIF orientation
magick input.jpg -auto-orient output.jpg
```

### Flip and Flop

```bash
# Vertical flip (top-bottom mirror)
magick input.png -flip output.png

# Horizontal flop (left-right mirror)
magick input.png -flop output.png

# Both (180° rotation equivalent)
magick input.png -flip -flop output.png
```

### Transpose and Transverse

```bash
# Transpose (flip + rotate 90° CCW)
magick input.png -transpose output.png

# Transverse (flop + rotate 90° CCW)
magick input.png -transverse output.png
```

### Shear and Distort

```bash
# Shear
magick input.png -shear 10x0 output.png  # X shear
magick input.png -shear 0x10 output.png  # Y shear

# Perspective distort
magick input.png -distort Perspective '0,0,10,10 100,0,90,10 0,100,10,90 100,100,90,90' output.png

# Arc distort
magick input.png -distort Arc 180 output.png

# Barrel distort (lens correction)
magick input.png -distort Barrel '0 0 0 1' output.png
```

## Color Adjustments

### Brightness and Contrast

```bash
# Brightness-Contrast (both -100 to 100)
magick input.png -brightness-contrast 10x5 output.png  # Brighter, more contrast

# Level adjustment (black%, gamma, white%)
magick input.png -level 5%,1.2,95% output.png

# Auto-level (stretch histogram)
magick input.png -auto-level output.png

# Normalize (contrast stretch)
magick input.png -normalize output.png
```

### Modulate (HSB Adjustment)

```bash
# modulate brightness,saturation,hue (percentages)
magick input.png -modulate 110,100,100 output.png  # 10% brighter
magick input.png -modulate 100,150,100 output.png  # 50% more saturated
magick input.png -modulate 100,100,50 output.png   # Shift hue by 50%

# Desaturate
magick input.png -modulate 100,0,100 output.png
```

### Color Replacement

```bash
# Replace specific color
magick input.png -fill red -opaque blue output.png

# With fuzz tolerance
magick input.png -fuzz 20% -fill red -opaque blue output.png

# Transparent replacement
magick input.png -fuzz 10% -transparent white output.png
```

### Channel Operations

```bash
# Extract single channel
magick input.png -channel R -separate red_channel.png

# Combine channels
magick red.png green.png blue.png -combine output.png

# Swap channels
magick input.png -channel-fx "red<=>blue" output.png

# Adjust specific channel
magick input.png -channel R -evaluate multiply 1.2 +channel output.png
```

## Text and Annotations

### Adding Text

```bash
# Basic text
magick input.png -gravity south -pointsize 32 -annotate +0+10 "Caption" output.png

# With font and color
magick input.png \
  -font "Helvetica" \
  -pointsize 48 \
  -fill white \
  -stroke black \
  -strokewidth 2 \
  -gravity center \
  -annotate +0+0 "Text" output.png

# Multi-line text
magick input.png -gravity center -pointsize 24 -annotate +0+0 "Line1\nLine2\nLine3" output.png
```

### Text Background

```bash
# Text with background box
magick input.png \
  -gravity south \
  -fill white \
  -undercolor "rgba(0,0,0,0.5)" \
  -pointsize 24 \
  -annotate +0+20 " Caption with padding " output.png
```

### Drawing Shapes

```bash
# Rectangle
magick input.png -stroke red -strokewidth 3 -fill none -draw "rectangle 10,10 100,100" output.png

# Circle
magick input.png -stroke blue -fill none -draw "circle 100,100 150,100" output.png

# Line
magick input.png -stroke green -strokewidth 2 -draw "line 0,0 200,200" output.png

# Polygon
magick input.png -stroke black -fill yellow -draw "polygon 100,10 40,198 190,78 10,78 160,198" output.png
```

## Layer Operations

### Append Images

```bash
# Horizontal append
magick img1.png img2.png img3.png +append horizontal.png

# Vertical append
magick img1.png img2.png img3.png -append vertical.png

# With spacing
magick img1.png -bordercolor white -border 5x0 img2.png -border 5x0 img3.png +append output.png
```

### Composite Operations

```bash
# Basic overlay
magick base.png overlay.png -composite output.png

# With position
magick base.png overlay.png -geometry +100+50 -composite output.png

# With gravity
magick base.png overlay.png -gravity southeast -composite output.png

# Blend modes
magick base.png overlay.png -compose Multiply -composite output.png
magick base.png overlay.png -compose Screen -composite output.png
magick base.png overlay.png -compose Overlay -composite output.png
magick base.png overlay.png -compose SoftLight -composite output.png
```

### Alpha Compositing

```bash
# Dissolve (transparency blend)
magick base.png overlay.png -compose Dissolve -define compose:args=50 -composite output.png

# Alpha masking
magick base.png mask.png -alpha Off -compose CopyOpacity -composite output.png

# Blend with alpha
magick base.png \( overlay.png -alpha set -channel A -evaluate multiply 0.5 +channel \) -composite output.png
```

## Borders and Frames

### Simple Borders

```bash
# Add solid border
magick input.png -bordercolor black -border 10 output.png

# Asymmetric border
magick input.png -bordercolor gray -border 20x10 output.png

# Rounded corners
magick input.png \( +clone -alpha extract -draw "fill black polygon 0,0 0,15 15,0" \
  -flip -flop -draw "fill black polygon 0,0 0,15 15,0" \
  -flip -draw "fill black polygon 0,0 0,15 15,0" \
  -flop -draw "fill black polygon 0,0 0,15 15,0" \) \
  -alpha off -compose CopyOpacity -composite output.png
```

### Frame Effects

```bash
# Simple frame
magick input.png -mattecolor gray -frame 10x10+3+3 output.png

# Raised/sunken border
magick input.png -raise 5 output.png
```

## Special Effects

### Shadows

```bash
# Drop shadow
magick input.png \( +clone -background black -shadow 80x5+5+5 \) +swap -background white -layers merge +repage output.png

# Soft shadow
magick input.png \( +clone -background black -shadow 60x10+10+10 \) +swap -background transparent -layers merge +repage output.png
```

### Reflections

```bash
# Simple reflection
magick input.png \( +clone -flip -alpha on -channel A -evaluate multiply 0.3 +channel \) -append output.png

# Gradient reflection
magick input.png \( +clone -flip \) -append \( -size 1x1 xc: -size $(magick identify -format "%w"x"%h" input.png) gradient: \) -compose CopyOpacity -composite output.png
```

### Tilt-Shift

```bash
# Simulated tilt-shift
magick input.png \( +clone -blur 0x10 \) \( -size 100x100 gradient:white-black \) -compose Blur -composite output.png
```
