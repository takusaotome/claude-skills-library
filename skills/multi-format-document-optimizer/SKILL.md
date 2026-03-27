---
name: multi-format-document-optimizer
description: |
  Unified document optimization skill that chains docling-converter, imagemagick-expert, and markdown-to-pdf. Automatically detects input format, applies appropriate conversion pipeline, optimizes embedded images, and produces web/print-ready output with configurable quality presets. Use when converting documents through multi-step pipelines, optimizing PDF images, creating print-ready documents from various sources, or batch processing documents with image optimization.
---

# Multi-Format Document Optimizer

## Overview

Chain multiple document processing tools (docling, ImageMagick, markdown-to-pdf) into unified conversion pipelines. Automatically detect input formats, route through appropriate converters, optimize embedded images for target use case (web/print/archive), and produce publication-ready output with a single command.

## When to Use

- Convert PDF/DOCX/PPTX to optimized PDF with compressed images
- Create web-ready documents with WebP images from source documents
- Generate print-ready PDFs with high-DPI images from mixed sources
- Batch process multiple documents through consistent optimization pipeline
- Extract, optimize, and re-embed images from existing documents
- Convert scanned documents with OCR and image enhancement
- Create archive-quality PDFs with optimized file size

**Typical user requests:**
- "Convert this PPTX to PDF and optimize images for web"
- "Make this scanned PDF smaller while keeping it readable"
- "Convert these Word docs to print-ready PDFs"
- "Batch process all documents in this folder for web publishing"
- "Optimize this PDF's embedded images"

## Prerequisites

- Python 3.9+
- docling CLI (`pip install docling`)
- ImageMagick 7+ (`brew install imagemagick` or `apt install imagemagick`)
- markdown-to-pdf dependencies:
  - fpdf2 mode: `pip install fpdf2 mistune pyyaml`
  - Playwright mode: `pip install markdown2 playwright && playwright install chromium`
- Optional: `pip install PyMuPDF` for PDF analysis

## Workflow

### Step 1: Analyze Input Document

Detect input format and assess processing requirements.

```bash
python scripts/document_optimizer.py analyze input.pdf
python scripts/document_optimizer.py analyze input.docx
python scripts/document_optimizer.py analyze ./documents/
```

Output includes:
- Detected format(s)
- Page count and dimensions
- Embedded image count and total size
- Recommended pipeline based on content

### Step 2: Select Quality Preset

Choose a quality preset based on target use case:

| Preset | Image Quality | DPI | Format | Use Case |
|--------|---------------|-----|--------|----------|
| `web` | 80% | 96 | WebP/JPEG | Online viewing, fast load |
| `print` | 95% | 300 | PNG/JPEG | Professional printing |
| `archive` | 90% | 150 | JPEG | Long-term storage, balanced |
| `minimal` | 70% | 72 | WebP | Maximum compression |
| `custom` | User-defined | User-defined | User-defined | Full control |

### Step 3: Execute Conversion Pipeline

Run the document through the optimization pipeline.

```bash
# Single document with preset
python scripts/document_optimizer.py convert input.pdf output.pdf --preset web

# With explicit preset
python scripts/document_optimizer.py convert input.docx output.pdf --preset print

# Custom settings
python scripts/document_optimizer.py convert input.pptx output.pdf \
    --image-quality 85 \
    --image-dpi 150 \
    --image-format jpeg

# Batch processing
python scripts/document_optimizer.py batch ./input_docs/ ./output/ --preset archive
```

### Step 4: Optimize Existing PDF Images

Extract, optimize, and re-embed images from an existing PDF.

```bash
python scripts/document_optimizer.py optimize-images input.pdf output.pdf --preset web
python scripts/document_optimizer.py optimize-images input.pdf output.pdf \
    --image-quality 75 \
    --max-width 1200
```

### Step 5: Verify Output

Validate the output document meets quality requirements.

```bash
python scripts/document_optimizer.py verify output.pdf
```

Output includes:
- File size comparison (before/after)
- Image quality assessment
- Page render verification
- Compression ratio achieved

## Pipeline Reference

### PDF Optimization Pipeline

```
Input PDF → Extract Images → Optimize Images → Re-embed → Output PDF
              (PyMuPDF)      (ImageMagick)     (fpdf2)
```

### Document Conversion Pipeline

```
Input (DOCX/PPTX/HTML) → Markdown (docling) → Optimize Images → PDF (markdown-to-pdf)
                                                (ImageMagick)
```

### Scanned Document Pipeline

```
Scanned PDF → OCR + Extract (docling) → Clean Images → Markdown → Optimized PDF
                                         (ImageMagick)            (fpdf2)
```

## CLI Options

### `analyze` Command

```bash
python scripts/document_optimizer.py analyze <input> [options]

Options:
  --format json|text     Output format (default: text)
  --verbose              Include detailed image analysis
```

### `convert` Command

```bash
python scripts/document_optimizer.py convert <input> <output> [options]

Options:
  --preset PRESET        Quality preset: web|print|archive|minimal|custom
  --image-quality N      JPEG/WebP quality 0-100 (default: preset-dependent)
  --image-dpi N          Target DPI for images (default: preset-dependent)
  --image-format FMT     Output image format: jpeg|png|webp (default: preset-dependent)
  --max-width N          Maximum image width in pixels
  --max-height N         Maximum image height in pixels
  --ocr                  Enable OCR for scanned documents
  --ocr-lang LANG        OCR language (default: en,ja)
  --keep-temp            Retain intermediate files for debugging
  --verbose              Print detailed progress
```

### `batch` Command

```bash
python scripts/document_optimizer.py batch <input_dir> <output_dir> [options]

Options:
  --preset PRESET        Quality preset for all documents
  --pattern GLOB         File pattern to match (default: *.pdf,*.docx,*.pptx)
  --parallel N           Number of parallel workers (default: 4)
  --skip-existing        Skip files that already exist in output
```

### `optimize-images` Command

```bash
python scripts/document_optimizer.py optimize-images <input.pdf> <output.pdf> [options]

Options:
  --preset PRESET        Quality preset
  --image-quality N      Target quality 0-100
  --max-width N          Maximum width in pixels
  --max-height N         Maximum height in pixels
  --strip-metadata       Remove EXIF/XMP metadata from images
```

### `verify` Command

```bash
python scripts/document_optimizer.py verify <document> [options]

Options:
  --format json|text     Output format
  --check-images         Verify image quality metrics
  --reference FILE       Compare against reference document
```

## Output Format

### Analysis JSON

```json
{
  "schema_version": "1.0",
  "input_file": "document.pdf",
  "format": "pdf",
  "page_count": 15,
  "file_size_bytes": 5242880,
  "images": {
    "count": 12,
    "total_bytes": 4500000,
    "formats": ["jpeg", "png"],
    "max_resolution": "3000x2000"
  },
  "recommended_pipeline": "pdf_optimize",
  "recommended_preset": "web",
  "estimated_output_size_bytes": 1048576
}
```

### Conversion Report

```json
{
  "schema_version": "1.0",
  "input_file": "document.docx",
  "output_file": "document.pdf",
  "pipeline": "docx_to_pdf",
  "preset": "web",
  "input_size_bytes": 8388608,
  "output_size_bytes": 1572864,
  "compression_ratio": 0.19,
  "images_processed": 8,
  "processing_time_seconds": 12.5,
  "status": "success"
}
```

## Quality Presets Detail

### Web Preset

Optimized for fast loading on web pages and online viewers.

- Image format: WebP (JPEG fallback)
- Quality: 80%
- DPI: 96
- Max dimensions: 1920x1080
- Strip metadata: Yes

### Print Preset

High quality for professional printing.

- Image format: PNG (photos as JPEG 95%)
- Quality: 95%
- DPI: 300
- Max dimensions: No limit
- Strip metadata: No (preserve color profiles)

### Archive Preset

Balanced quality and size for long-term storage.

- Image format: JPEG
- Quality: 90%
- DPI: 150
- Max dimensions: 2400x2400
- Strip metadata: Preserve essential only

### Minimal Preset

Maximum compression for constrained environments.

- Image format: WebP
- Quality: 70%
- DPI: 72
- Max dimensions: 1280x720
- Strip metadata: Yes

## Resources

- `scripts/document_optimizer.py` — Main CLI tool for document optimization pipelines
- `references/pipeline_guide.md` — Detailed pipeline configurations and customization options
- `references/image_optimization_guide.md` — Image optimization strategies and quality settings

## Integration with Other Skills

This skill integrates with:
- **docling-converter** — Document format conversion and OCR
- **imagemagick-expert** — Image processing and optimization
- **markdown-to-pdf** — Final PDF generation with professional styling

The optimizer automatically invokes these tools in the appropriate sequence based on input format and target preset.

## Key Principles

1. **Single command, complete pipeline** — Analyze, convert, and optimize in one step
2. **Preset-driven simplicity** — Sensible defaults for common use cases
3. **Format-aware routing** — Automatic pipeline selection based on input type
4. **Quality-preserving compression** — Optimize size without visible quality loss
5. **Batch-friendly** — Process entire directories with consistent settings
