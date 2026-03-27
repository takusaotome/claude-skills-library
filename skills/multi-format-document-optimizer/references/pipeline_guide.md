# Pipeline Configuration Guide

## Overview

This guide details the document processing pipelines available in the multi-format-document-optimizer skill. Each pipeline is designed for specific input/output combinations and optimization goals.

## Pipeline Architecture

### Core Components

| Component | Tool | Purpose |
|-----------|------|---------|
| Format Detector | Built-in | Identify input format and content type |
| Document Converter | docling | Convert DOCX/PPTX/HTML to Markdown |
| Image Extractor | PyMuPDF | Extract embedded images from PDFs |
| Image Optimizer | ImageMagick | Resize, compress, format-convert images |
| PDF Generator | markdown-to-pdf | Create final PDF output |
| PDF Rebuilder | fpdf2/PyMuPDF | Re-embed optimized images into PDF |

### Pipeline Selection Matrix

| Input Format | Target | Pipeline | Components Used |
|-------------|--------|----------|-----------------|
| PDF | Optimized PDF | `pdf_optimize` | PyMuPDF → ImageMagick → fpdf2 |
| DOCX | PDF | `docx_to_pdf` | docling → ImageMagick → markdown-to-pdf |
| PPTX | PDF | `pptx_to_pdf` | docling → ImageMagick → markdown-to-pdf |
| HTML | PDF | `html_to_pdf` | docling → ImageMagick → markdown-to-pdf |
| Scanned PDF | Searchable PDF | `ocr_optimize` | docling (OCR) → ImageMagick → fpdf2 |
| Images | PDF | `images_to_pdf` | ImageMagick → fpdf2 |
| Markdown | Optimized PDF | `md_to_pdf` | ImageMagick → markdown-to-pdf |

## Pipeline Configurations

### PDF Optimization Pipeline (`pdf_optimize`)

Extracts images from existing PDF, optimizes them, and rebuilds the document.

**Processing Steps:**

1. **Extract images** — Use PyMuPDF to extract all embedded images
2. **Analyze images** — Determine format, dimensions, color depth
3. **Optimize images** — Apply ImageMagick transformations based on preset
4. **Rebuild PDF** — Re-embed optimized images while preserving text/layout

**Configuration Options:**

```yaml
pdf_optimize:
  extract_method: pymupdf  # pymupdf | pdfimages
  preserve_layout: true
  preserve_annotations: true
  preserve_links: true
  image_optimization:
    enabled: true
    recompress_lossless: false  # Re-encode PNG→PNG with better compression
  text_handling:
    preserve_fonts: true
    subset_fonts: true  # Reduce font file size
```

**Limitations:**

- Complex layouts with overlapping elements may shift slightly
- Vector graphics are not optimized (only raster images)
- Encrypted PDFs must be decrypted first

### DOCX to PDF Pipeline (`docx_to_pdf`)

Converts Word documents to optimized PDF via Markdown intermediate.

**Processing Steps:**

1. **Convert to Markdown** — docling extracts text, tables, and images
2. **Extract images** — Save embedded images to temporary directory
3. **Optimize images** — Apply ImageMagick transformations
4. **Generate PDF** — markdown-to-pdf creates final output

**Configuration Options:**

```yaml
docx_to_pdf:
  converter: docling
  intermediate_format: markdown
  preserve_styles: best_effort  # best_effort | minimal | none
  table_handling:
    mode: accurate  # accurate | fast
    max_columns: 10
  image_handling:
    extract_embedded: true
    extract_linked: false
    default_dpi: 150
```

**Style Mapping:**

| Word Style | Markdown | PDF |
|------------|----------|-----|
| Heading 1 | `# Title` | H1 with theme color |
| Heading 2 | `## Section` | H2 with theme color |
| Bold | `**text**` | Bold font |
| Italic | `*text*` | Italic font |
| Bullet List | `- item` | Bulleted list |
| Numbered List | `1. item` | Numbered list |
| Table | Markdown table | Styled table |

### PPTX to PDF Pipeline (`pptx_to_pdf`)

Converts PowerPoint presentations to optimized PDF.

**Processing Steps:**

1. **Convert to Markdown** — docling extracts slide content
2. **Process slide images** — Extract and optimize graphics
3. **Generate PDF** — One slide per page with optimized images

**Configuration Options:**

```yaml
pptx_to_pdf:
  converter: docling
  slide_layout: one_per_page  # one_per_page | two_per_page | handout
  include_notes: false
  include_hidden_slides: false
  image_handling:
    preserve_animations: false  # Static only
    extract_charts: as_images
    chart_resolution: 300
```

### OCR Pipeline (`ocr_optimize`)

Processes scanned documents with OCR and image enhancement.

**Processing Steps:**

1. **Analyze pages** — Detect if pages are scanned images
2. **Enhance images** — Deskew, despeckle, enhance contrast
3. **Perform OCR** — Extract text layer using docling
4. **Generate searchable PDF** — Combine text layer with optimized images

**Configuration Options:**

```yaml
ocr_optimize:
  ocr_engine: ocrmac  # ocrmac | tesseract | rapidocr
  ocr_language: [en, ja]
  image_preprocessing:
    deskew: true
    despeckle: true
    enhance_contrast: auto
    remove_background: false
  output:
    text_layer: overlay  # overlay | replace
    image_quality: 85
```

**Image Enhancement Commands:**

```bash
# Deskew scanned page
magick input.png -deskew 40% output.png

# Despeckle (remove noise)
magick input.png -despeckle output.png

# Enhance contrast for OCR
magick input.png -normalize -sharpen 0x1 output.png

# Combined preprocessing
magick input.png -deskew 40% -despeckle -normalize output.png
```

## Image Optimization Strategies

### Format Selection

| Content Type | Web | Print | Archive |
|-------------|-----|-------|---------|
| Photographs | WebP 80% | JPEG 95% | JPEG 90% |
| Screenshots | WebP 85% | PNG | JPEG 85% |
| Diagrams | WebP 90% | PNG | PNG |
| Text-heavy | WebP 85% | PNG | PNG |
| Mixed | WebP 80% | JPEG 90% | JPEG 85% |

### Resolution Scaling

Calculate target dimensions based on final output size:

```
Target DPI × Page Width (inches) = Pixel Width
```

Examples for A4 page (8.27" width):
- Web (96 DPI): 794 pixels
- Archive (150 DPI): 1240 pixels
- Print (300 DPI): 2481 pixels

### Quality-Size Tradeoffs

| Quality | Typical Compression | Visual Impact |
|---------|---------------------|---------------|
| 95% | 5:1 | Imperceptible |
| 90% | 8:1 | Minimal |
| 85% | 12:1 | Slight on close inspection |
| 80% | 15:1 | Noticeable on zoom |
| 70% | 25:1 | Visible artifacts |

## Advanced Configuration

### Custom Pipeline Definition

Create custom pipelines by chaining components:

```yaml
custom_pipeline:
  name: high_quality_archive
  steps:
    - component: format_detector
    - component: docling_converter
      options:
        table_mode: accurate
        ocr_enabled: true
    - component: image_optimizer
      options:
        format: jpeg
        quality: 92
        max_dimension: 3000
        strip_metadata: false
    - component: pdf_generator
      mode: fpdf2
      options:
        theme: navy
        cover: true
```

### Conditional Processing

Apply different settings based on content analysis:

```yaml
conditional_rules:
  - condition: image_count > 20
    apply:
      parallel_processing: true
      image_quality: 80  # Reduce for many images

  - condition: total_image_size > 50MB
    apply:
      preset: archive
      max_dimension: 2000

  - condition: page_count > 100
    apply:
      subset_fonts: true
      compress_text: true
```

### Batch Processing Configuration

```yaml
batch:
  parallel_workers: 4
  error_handling: continue  # continue | stop
  logging:
    level: info
    file: batch_processing.log
  output:
    naming: preserve  # preserve | sequential | datestamp
    overwrite: false
  filters:
    min_size: 1KB
    max_size: 100MB
    exclude_patterns:
      - "*.tmp"
      - "~$*"
```

## Troubleshooting

### Pipeline Selection Issues

**Symptom:** Wrong pipeline selected for input file.

**Solution:** Force pipeline selection:
```bash
python scripts/document_optimizer.py convert input.pdf output.pdf \
    --pipeline pdf_optimize
```

### Image Quality Degradation

**Symptom:** Output images look worse than expected.

**Solutions:**
1. Increase quality setting: `--image-quality 95`
2. Use lossless format: `--image-format png`
3. Disable resizing: `--max-width 0 --max-height 0`

### Large Output File Size

**Symptom:** Optimized file is larger than original.

**Causes:**
- Lossless images converted to higher quality
- Small images upscaled
- Font subsetting disabled

**Solutions:**
1. Use `minimal` preset for maximum compression
2. Enable font subsetting in configuration
3. Reduce max dimensions to match actual display size

### OCR Quality Issues

**Symptom:** OCR text is incorrect or garbled.

**Solutions:**
1. Preprocess images: `--image-preprocessing enhance`
2. Specify correct language: `--ocr-lang ja`
3. Use higher resolution source: minimum 300 DPI recommended
4. Try different OCR engine: `--ocr-engine tesseract`
