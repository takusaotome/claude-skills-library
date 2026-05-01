---
layout: default
title: "QR Code Generator"
grand_parent: English
parent: Software Development
nav_order: 24
lang_peer: /ja/skills/dev/qr-code-generator/
permalink: /en/skills/dev/qr-code-generator/
---

# QR Code Generator
{: .no_toc }

Generate QR code images from text, URLs, or contact information using Python's qrcode library. Supports customization (size, margin, color, error correction) and batch generation.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/qr-code-generator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/qr-code-generator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Generate QR code images from arbitrary strings (URLs, text, contact information, etc.) using Python's qrcode library. Supports customization of size, margin (quiet zone), foreground/background colors, and error correction levels. Batch generation mode allows creating multiple QR codes from a CSV or JSON input file.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Required packages: `qrcode[pil]` (includes Pillow for PNG output)

Install dependencies:
```bash
pip install "qrcode[pil]"
```

---

## 3. Quick Start

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

---

## 4. How It Works

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

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- User wants to generate a QR code from a URL, text, or data
- User needs to create multiple QR codes in batch from a file
- User requests a QR code with specific customization (size, colors, error correction)
- User asks to encode contact information (vCard) as a QR code
- User wants to preview a generated QR code image

---

## 6. Understanding the Output

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

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/qr-code-generator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: qr-code-parameters.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: generate_qr.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/qr-code-generator/references/qr-code-parameters.md`

**Scripts:**

- `skills/qr-code-generator/scripts/generate_qr.py`
