# Batch Processing Guide

## mogrify - In-Place Batch Processing

`mogrify` is the primary tool for batch operations. It modifies files in-place by default.

### Basic Usage

```bash
# Resize all JPEGs in current directory
mogrify -resize 800x *.jpg

# Convert all PNGs to JPEG
mogrify -format jpg *.png

# Apply quality setting to all JPEGs
mogrify -quality 85 *.jpg

# Multiple operations
mogrify -resize 800x -quality 85 *.jpg
```

### Output to Different Directory

```bash
# Process and output to new directory
mkdir -p output
mogrify -path output -resize 50% *.jpg

# Convert format to new directory
mogrify -path converted -format jpg *.png

# Preserve directory structure
find . -name "*.png" -exec sh -c 'mkdir -p "output/$(dirname "{}")" && mogrify -path "output/$(dirname "{}")" -format jpg "{}"' \;
```

### Format Conversion

```bash
# PNG to JPEG
mogrify -format jpg -quality 90 *.png

# JPEG to WebP
mogrify -format webp -quality 80 *.jpg

# All images to PNG
mogrify -format png *.jpg *.gif *.bmp

# Note: Original files remain, new files created with new extension
```

## Shell Loop Patterns

### Basic For Loop

```bash
# Process each file with custom output naming
for f in *.jpg; do
    magick "$f" -resize 800x "resized_$f"
done

# Different output directory
mkdir -p thumbnails
for f in *.jpg; do
    magick "$f" -thumbnail 200x200 "thumbnails/$f"
done

# Change extension
for f in *.png; do
    magick "$f" "${f%.png}.jpg"
done
```

### With Counter

```bash
# Sequential numbering
i=1
for f in *.jpg; do
    magick "$f" -resize 400x "$(printf "image_%03d.jpg" $i)"
    ((i++))
done

# Preserve original name with suffix
for f in *.png; do
    base="${f%.png}"
    magick "$f" -resize 50% "${base}_small.png"
done
```

### Conditional Processing

```bash
# Process only large images
for f in *.jpg; do
    width=$(magick identify -format "%w" "$f")
    if [ "$width" -gt 1920 ]; then
        magick "$f" -resize 1920x "$f"
        echo "Resized: $f"
    fi
done

# Skip already processed
for f in *.jpg; do
    if [ ! -f "output/${f}" ]; then
        magick "$f" -resize 800x "output/$f"
    fi
done
```

## find + exec Patterns

### Recursive Processing

```bash
# Find and resize all JPEGs recursively
find . -name "*.jpg" -exec magick {} -resize 800x {} \;

# Output to flat directory
mkdir -p output
find . -name "*.png" -exec sh -c 'magick "$1" "output/$(basename "$1")"' _ {} \;

# Preserve subdirectory structure
find . -name "*.jpg" -exec sh -c '
    dir=$(dirname "{}")
    mkdir -p "output/$dir"
    magick "{}" -resize 50% "output/{}"
' \;
```

### With Progress

```bash
# Count and process
total=$(find . -name "*.jpg" | wc -l)
current=0
find . -name "*.jpg" | while read f; do
    ((current++))
    echo "Processing $current/$total: $f"
    magick "$f" -resize 800x "$f"
done
```

## xargs for Performance

### Basic Parallel Processing

```bash
# Process 4 files at a time
find . -name "*.jpg" | xargs -P 4 -I {} magick {} -resize 800x {}

# With directory output
find . -name "*.jpg" | xargs -P 4 -I {} sh -c 'magick "$1" -resize 800x "output/$(basename "$1")"' _ {}
```

### Handling Special Characters

```bash
# Use null delimiter for filenames with spaces
find . -name "*.jpg" -print0 | xargs -0 -P 4 -I {} magick {} -resize 800x {}

# Safely handle all filename characters
find . -name "*.jpg" -print0 | xargs -0 -n 1 -P 4 sh -c 'magick "$0" -resize 800x "output/$(basename "$0")"'
```

## GNU Parallel

For maximum performance with many files:

```bash
# Basic parallel processing
parallel magick {} -resize 800x output/{/} ::: *.jpg

# With progress bar
parallel --bar magick {} -resize 800x output/{/} ::: *.jpg

# Recursive with find
find . -name "*.jpg" | parallel magick {} -resize 800x {}

# Specify number of jobs
parallel -j 8 magick {} -thumbnail 200x200 thumbs/{/} ::: *.jpg

# Complex operations
parallel "magick {} -resize 800x -quality 85 output/{/.}.jpg" ::: *.png
```

## Error Handling

### Basic Error Handling

```bash
# Continue on error
for f in *.jpg; do
    magick "$f" -resize 800x "output/$f" 2>/dev/null || echo "Failed: $f"
done

# Log errors
for f in *.jpg; do
    if ! magick "$f" -resize 800x "output/$f" 2>>errors.log; then
        echo "$f" >> failed_files.txt
    fi
done
```

### Validation Before Processing

```bash
# Check if valid image
for f in *.jpg; do
    if magick identify "$f" >/dev/null 2>&1; then
        magick "$f" -resize 800x "output/$f"
    else
        echo "Invalid image: $f"
    fi
done
```

### Retry Logic

```bash
# Retry failed conversions
MAX_RETRIES=3
for f in *.jpg; do
    attempt=1
    while [ $attempt -le $MAX_RETRIES ]; do
        if magick "$f" -resize 800x "output/$f" 2>/dev/null; then
            break
        fi
        echo "Retry $attempt for $f"
        ((attempt++))
        sleep 1
    done
done
```

## Logging and Progress

### Simple Progress

```bash
# Counter-based progress
total=$(ls -1 *.jpg 2>/dev/null | wc -l)
count=0
for f in *.jpg; do
    ((count++))
    echo -ne "Processing: $count/$total\r"
    magick "$f" -resize 800x "output/$f"
done
echo "Complete: $count files processed"
```

### Detailed Logging

```bash
#!/bin/bash
LOG_FILE="processing.log"
ERROR_LOG="errors.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting batch processing"

for f in *.jpg; do
    if magick "$f" -resize 800x "output/$f" 2>>"$ERROR_LOG"; then
        log "OK: $f"
    else
        log "FAIL: $f"
    fi
done

log "Processing complete"
```

### With Statistics

```bash
#!/bin/bash
success=0
failed=0
start_time=$(date +%s)

for f in *.jpg; do
    if magick "$f" -resize 800x "output/$f" 2>/dev/null; then
        ((success++))
    else
        ((failed++))
    fi
done

end_time=$(date +%s)
duration=$((end_time - start_time))

echo "=== Summary ==="
echo "Successful: $success"
echo "Failed: $failed"
echo "Duration: ${duration}s"
```

## Common Batch Operations

### Thumbnail Generation

```bash
#!/bin/bash
# Generate thumbnails with consistent size
mkdir -p thumbnails

for f in *.jpg; do
    # Square thumbnail with center crop
    magick "$f" -thumbnail 200x200^ -gravity center -extent 200x200 "thumbnails/$f"
done
```

### Web Optimization

```bash
#!/bin/bash
mkdir -p web

for f in *.jpg; do
    # Optimize for web
    magick "$f" \
        -resize "1920x1080>" \
        -strip \
        -interlace Plane \
        -quality 85 \
        "web/$f"
done

for f in *.png; do
    # Convert PNG to optimized WebP
    magick "$f" \
        -resize "1920x1080>" \
        -quality 80 \
        "web/${f%.png}.webp"
done
```

### Contact Sheet

```bash
# Create contact sheet from all images
magick montage *.jpg -tile 5x -geometry 200x200+5+5 -background white contact_sheet.jpg
```

### Watermarking

```bash
#!/bin/bash
WATERMARK="watermark.png"
mkdir -p watermarked

for f in *.jpg; do
    magick "$f" "$WATERMARK" -gravity southeast -composite "watermarked/$f"
done
```

### Format Standardization

```bash
#!/bin/bash
# Convert all images to standardized format
mkdir -p standardized

for f in *.{jpg,jpeg,png,gif,bmp,tiff}; do
    [ -f "$f" ] || continue
    base="${f%.*}"
    magick "$f" -resize "2000x2000>" -colorspace sRGB -quality 90 "standardized/${base}.jpg"
done
```

## Performance Tips

### Memory Management

```bash
# Limit memory usage
for f in *.jpg; do
    magick -limit memory 1GB -limit map 2GB "$f" -resize 800x "output/$f"
done

# Check available resources
magick -list resource
```

### Disk-Based Processing

```bash
# Use disk for very large files
magick -limit memory 256MB -limit area 128MB "$f" -resize 800x "output/$f"
```

### Optimal Parallelism

```bash
# Number of parallel jobs = CPU cores
CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu)
find . -name "*.jpg" | xargs -P "$CORES" -I {} magick {} -resize 800x output/{}
```

### Avoid Redundant Operations

```bash
# Check if processing needed
for f in *.jpg; do
    output="output/$f"
    if [ ! -f "$output" ] || [ "$f" -nt "$output" ]; then
        magick "$f" -resize 800x "$output"
    fi
done
```

## Complete Batch Script Template

```bash
#!/bin/bash
# Batch Image Processor
# Usage: ./batch_process.sh <input_dir> <output_dir> <operation>

set -e

INPUT_DIR="${1:-.}"
OUTPUT_DIR="${2:-./output}"
OPERATION="${3:-resize}"

# Configuration
MAX_JOBS=$(nproc 2>/dev/null || echo 4)
LOG_FILE="batch_$(date +%Y%m%d_%H%M%S).log"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Logging function
log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Process function
process_image() {
    local input="$1"
    local output="$OUTPUT_DIR/$(basename "$input")"

    case "$OPERATION" in
        resize)
            magick "$input" -resize 800x "$output"
            ;;
        thumbnail)
            magick "$input" -thumbnail 200x200^ -gravity center -extent 200x200 "$output"
            ;;
        optimize)
            magick "$input" -strip -interlace Plane -quality 85 "$output"
            ;;
        webp)
            output="${output%.*}.webp"
            magick "$input" -quality 80 "$output"
            ;;
        *)
            echo "Unknown operation: $OPERATION"
            return 1
            ;;
    esac
}

export -f process_image log
export OUTPUT_DIR OPERATION LOG_FILE

# Main processing
log "Starting batch processing"
log "Input: $INPUT_DIR"
log "Output: $OUTPUT_DIR"
log "Operation: $OPERATION"
log "Parallel jobs: $MAX_JOBS"

# Find and process images
find "$INPUT_DIR" -maxdepth 1 -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" \) -print0 | \
    xargs -0 -P "$MAX_JOBS" -I {} bash -c 'process_image "$@"' _ {}

log "Processing complete"
```
