---
name: qr-code-generator
description: Generate QR code images from text, URLs, or contact information using Python's qrcode library. Supports customization (size, margin, color, error correction) and batch generation.
---

# QR Code Generator

## Overview

Generate QR code images from arbitrary strings (URLs, text, contact information, etc.) using Python's qrcode library. Supports customization of size, margin (quiet zone), foreground/background colors, and error correction levels. Batch generation mode allows creating multiple QR codes from a CSV or JSON input file.

## When to Use

- User wants to generate a QR code from a URL, text, or data
- User needs to create multiple QR codes in batch from a file
- User requests a QR code with specific customization (size, colors, error correction)
- User asks to encode contact information (vCard) as a QR code
- User wants to preview a generated QR code image

## Prerequisites

- Python 3.9+
- No API keys required
- Required packages: `qrcode[pil]` (includes Pillow for PNG output)

Install dependencies:
```bash
pip install "qrcode[pil]"
```

## Workflow

### Step 1: Determine QR Code Parameters

Gather the following information from the user:
- **Data**: The string to encode (URL, text, vCard, etc.)
- **Output path**: Where to save the PNG image (default: `./qr_output.png`)
- **Box size**: Pixels per QR code module (default: 10)
- **Border**: Quiet zone width in modules (default: 4, minimum 4 per spec)
- **Fill color**: Foreground color (default: black)
- **Back color**: Background color (default: white)
- **Error correction**: L (7%), M (15%), Q (25%), H (30%) (default: M)

### Step 2: Generate Single QR Code

For a single QR code, run the generation script:

```bash
python3 scripts/generate_qr.py \
  --data "https://example.com" \
  --output "./qr_example.png" \
  --box-size 10 \
  --border 4 \
  --fill-color black \
  --back-color white \
  --error-correction M
```

### Step 3: Generate Batch QR Codes (Optional)

For multiple QR codes, prepare a CSV or JSON file with entries:

**CSV format** (`batch_input.csv`):
```csv
data,filename,box_size,error_correction
https://example1.com,qr1.png,10,M
https://example2.com,qr2.png,12,H
```

**JSON format** (`batch_input.json`):
```json
[
  {"data": "https://example1.com", "filename": "qr1.png"},
  {"data": "https://example2.com", "filename": "qr2.png", "box_size": 12}
]
```

Run batch generation:

```bash
python3 scripts/generate_qr.py \
  --batch "./batch_input.csv" \
  --output-dir "./qr_batch_output/"
```

### Step 4: Preview Generated QR Code

After generation, use the Read tool to display the generated PNG image for user verification.

### Step 5: Generate vCard QR Code (Optional)

For contact information, use the vCard format:

```bash
python3 scripts/generate_qr.py \
  --vcard \
  --name "John Doe" \
  --phone "+1-555-123-4567" \
  --email "john@example.com" \
  --output "./contact_qr.png"
```

## Output Format

### Single Generation

- PNG image file at specified output path
- Console output confirming generation with file path and QR code metadata

### Batch Generation

- Multiple PNG files in the output directory
- Summary JSON report (`batch_summary.json`):

```json
{
  "generated_at": "2026-03-17T08:00:00Z",
  "total_count": 10,
  "success_count": 10,
  "failed_count": 0,
  "files": [
    {"data": "https://example1.com", "path": "qr1.png", "status": "success"},
    {"data": "https://example2.com", "path": "qr2.png", "status": "success"}
  ]
}
```

## Resources

- `scripts/generate_qr.py` -- Main QR code generation script with CLI interface
- `references/qr-code-parameters.md` -- Detailed guide on QR code parameters and best practices

## Key Principles

1. **Default to readable QR codes**: Use sufficient box size (10+) and proper quiet zone (4+ modules)
2. **Validate data length**: QR codes have capacity limits based on error correction level
3. **Maintain contrast**: Ensure sufficient contrast between fill and background colors
4. **Preview before delivery**: Always show the generated QR code to the user for verification
