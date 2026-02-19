---
name: markdown-to-pdf
description: Convert Markdown documents to PDF. Two modes available — (1) Playwright-based conversion with Mermaid diagram support for technical documentation, and (2) fpdf2-based professional PDF generation with cover pages, themed styling, and business-quality table formatting for estimates, proposals, and reports. Use this skill when converting Markdown to PDF, generating business documents from Markdown, or converting Mermaid diagrams to images.
---

# Markdown to PDF Converter

## Overview

Convert Markdown documents into PDF with two rendering engines:

1. **Playwright mode** (`markdown_to_pdf.py`) — HTML/CSS-based rendering with Mermaid diagram support. Best for technical documentation with custom CSS styling.
2. **fpdf2 mode** (`markdown_to_fpdf.py`) — Professional PDF generation with cover pages, themed headers/footers, styled tables, and CJK font support. Best for business documents (estimates, proposals, reports).

## When to Use This Skill

Use this skill when:
- Converting Markdown files to PDF
- Creating professional business documents (estimates, proposals, cost analyses)
- Converting technical documentation with Mermaid diagrams to PDF
- Extracting Mermaid diagrams as standalone images (PNG or SVG)

**Decision Matrix — Which mode to use:**

| Need | Mode | Script |
|------|------|--------|
| Cover page, professional styling | fpdf2 | `markdown_to_fpdf.py` |
| Business documents (estimates, reports) | fpdf2 | `markdown_to_fpdf.py` |
| Themed headers/footers | fpdf2 | `markdown_to_fpdf.py` |
| Styled tables (alternating rows, header colors) | fpdf2 | `markdown_to_fpdf.py` |
| Technical docs with custom CSS | Playwright | `markdown_to_pdf.py` |
| Mermaid diagrams as primary content | Playwright | `markdown_to_pdf.py` |
| General Markdown to PDF | Either | Choose by needs |

**Typical user requests:**
- "Convert this Markdown file to PDF" → Choose based on content
- "Create a professional PDF from this estimate" → fpdf2 mode
- "Generate a PDF report with cover page" → fpdf2 mode
- "Convert this design document with diagrams to PDF" → Playwright mode
- "Export this Mermaid diagram as an image" → mermaid_to_image.py

## Quick Start

### Prerequisites

**For fpdf2 mode (professional PDFs):**
```bash
pip install fpdf2 mistune pyyaml
```

**For Playwright mode (Mermaid + CSS):**
```bash
pip install markdown2 playwright
playwright install chromium

# For Mermaid conversion:
npm install -g @mermaid-js/mermaid-cli
```

## Task 1: Convert Markdown with Mermaid to PDF (Playwright mode)

### Workflow

1. **Read the Markdown file** and identify Mermaid code blocks
2. **Execute the conversion script**:
   ```bash
   python scripts/markdown_to_pdf.py <input.md> <output.pdf>
   ```
3. **Verify the output**
4. **Deliver the PDF**

### Configuration Options

**Theme options:** `--theme default|forest|dark|neutral`

**Image format:** `--image-format png|svg` (SVG recommended)

**Background color:** `--background white|transparent|"#f0f0f0"`

**Custom styling:** `--css styles.css`

**Debugging:** `--keep-temp`

## Task 2: Convert Mermaid Diagrams to Images

### Workflow

1. **Identify the Mermaid diagram source**
2. **Execute the conversion**:
   ```bash
   python scripts/mermaid_to_image.py <input.mmd> <output.png>
   python scripts/mermaid_to_image.py --code "graph TD; A-->B" output.png
   ```
3. **Verify and deliver**

### Configuration

- `--format png|svg`
- `--theme default|forest|dark|neutral`
- `--width <pixels>` / `--height <pixels>` (PNG only)
- `--background white|transparent|<color>`

## Task 3: Convert Markdown to Professional PDF (fpdf2 mode)

### Workflow

1. **Read the Markdown file** — Check for YAML frontmatter
2. **Add frontmatter** if not present (for cover page, theme, metadata)
3. **Execute the conversion**:
   ```bash
   python scripts/markdown_to_fpdf.py input.md output.pdf
   python scripts/markdown_to_fpdf.py input.md output.pdf --theme navy
   python scripts/markdown_to_fpdf.py input.md output.pdf --theme gray --confidential
   python scripts/markdown_to_fpdf.py input.md output.pdf --no-cover
   ```
4. **Verify the output**
5. **Deliver the PDF**

### YAML Frontmatter

Add frontmatter at the top of the Markdown file to control cover page, theme, and metadata:

```yaml
---
title: 御見積書
subtitle: AI プラットフォーム PoC サポート
theme: navy
document_number: FSAI-2026-0001
date: 2026年2月17日
author: 山田 太郎
company: FujiSoft America, Inc.
recipient: Client Inc.
confidential: false
cover: true
header_text: "FSAI-2026-0001 | FujiSoft America, Inc."
---
```

For detailed field reference, see `references/fpdf_styling_guide.md`.

### Markdown Features Supported

| Markdown | Rendered As |
|----------|------------|
| `# H1` | Section title (bold, underlined, theme color) |
| `## H2` | Subsection title (bold, theme color) |
| `### H3` | Sub-subsection title |
| `**bold**` / `*italic*` | Inline formatting via `multi_cell(markdown=True)` |
| `- item` | Bulleted list |
| `\| table \|` | Styled table (data_table by default) |
| ` ```code``` ` | Code block (gray background) |
| ` ```mermaid``` ` | Mermaid → image (fallback to code block) |
| `<!-- pagebreak -->` | Page break |
| `---` | Horizontal rule |
| `<!-- info-table -->` | Override next table to info_table style |

### Table Styles

**Data Table (default):** Multi-column table with colored header row and alternating row colors.

**Info Table:** Use `<!-- info-table -->` comment before a table for key-value style rendering:

```markdown
<!-- info-table -->
| Key | Value |
|-----|-------|
| Phase 1 | $5,000 |
| Phase 2 | TBD |
```

### Themes

- **`navy`** — Client-facing documents (deep navy primary, blue-gray accents)
- **`gray`** — Internal documents (dark gray primary, light gray accents)

### CLI Options

```bash
python scripts/markdown_to_fpdf.py input.md output.pdf [options]
```

| Option | Description |
|--------|-------------|
| `--theme navy\|gray` | Color theme (default: from frontmatter or navy) |
| `--confidential` | Mark as confidential |
| `--no-cover` | Suppress cover page |
| `--font-regular PATH` | Custom regular font |
| `--font-bold PATH` | Custom bold font |

### Font Requirements

Fonts are auto-discovered per platform:
- **macOS:** Hiragino Kaku Gothic W3/W6
- **Windows:** Yu Gothic Regular/Bold
- **Linux:** Noto Sans CJK (`sudo apt install fonts-noto-cjk`)

Manual override: `--font-regular /path/to/font.ttc --font-bold /path/to/bold.ttc`

## Resources

### `scripts/markdown_to_fpdf.py`

Professional PDF generation from Markdown with fpdf2. Supports YAML frontmatter, cover pages, themed styling, data/info tables, and CJK fonts.

### `scripts/markdown_to_pdf.py`

HTML/CSS-based Markdown to PDF with Mermaid diagram support via Playwright.

### `scripts/mermaid_to_image.py`

Converts Mermaid diagram code to PNG/SVG images.

### `scripts/themes.py`

Theme definitions (navy, gray) and cross-platform CJK font discovery.

### `references/mermaid_guide.md`

Comprehensive Mermaid diagram syntax reference.

### `references/fpdf_styling_guide.md`

fpdf2 professional PDF styling guide — frontmatter fields, theme options, table modes, font requirements.

### `assets/sample_frontmatter.yaml`

Sample YAML frontmatter templates for estimates, internal documents, and simple reports.

## Troubleshooting

### fpdf2 mode: Font not found

If automatic font discovery fails, specify fonts manually:
```bash
python scripts/markdown_to_fpdf.py input.md output.pdf \
    --font-regular /path/to/regular.ttc \
    --font-bold /path/to/bold.ttc
```

### Playwright mode: Mermaid diagrams not rendering

Install mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`

Or install Playwright: `pip install playwright && playwright install chromium`

### Playwright mode: Poor image quality

Use SVG format: `--image-format svg` (recommended)

## Tips

1. **Business documents** → Use fpdf2 mode with frontmatter for professional output
2. **Technical docs with diagrams** → Use Playwright mode with SVG format
3. **Use `<!-- pagebreak -->`** for clean section transitions in fpdf2 mode
4. **Use `<!-- info-table -->`** for key-value tables in fpdf2 mode
5. **Preview Mermaid** at [mermaid.live](https://mermaid.live/) before conversion
