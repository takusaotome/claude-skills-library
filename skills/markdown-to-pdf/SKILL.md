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

**Mermaid control:** `--no-strict-mermaid` (allow fallback), `--debug-mermaid` (verbose output)

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
- `--use-playwright` — Force Playwright backend
- `--debug` — Print detailed debug output

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
| ` ```mermaid``` ` | Mermaid → PNG image (strict: fail on error, `--no-strict-mermaid`: fallback to code block) |
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
| `--no-strict-mermaid` | Allow Mermaid fallback to code block on failure (default: strict) |
| `--debug-mermaid` | Print detailed Mermaid conversion debug output |

### Font Requirements

Fonts are auto-discovered per platform with **TrueType outline preference** (best fpdf2 compatibility):

- **macOS:** UDEVGothic or Noto Sans JP (TTF) — install to `~/Library/Fonts/`
  - Hiragino Kaku Gothic (CFF outlines) is used as fallback but may cause garbled CJK text
  - Recommended: `brew install --cask font-udev-gothic` or download [Noto Sans JP TTF](https://fonts.google.com/noto/specimen/Noto+Sans+JP)
- **Windows:** Yu Gothic Regular/Bold (usually TrueType, pre-installed)
- **Linux:** Noto Sans CJK (`sudo apt install fonts-noto-cjk`)

Manual override: `--font-regular /path/to/font.ttc --font-bold /path/to/bold.ttc`

**CFF compatibility note:** Fonts with CFF outlines (e.g., Hiragino Sans on macOS) may produce garbled CJK text in fpdf2-generated PDFs. The tool warns on stderr when CFF fonts are detected. Install a TrueType CJK font to resolve.

## Resources

### `scripts/markdown_to_fpdf.py`

Professional PDF generation from Markdown with fpdf2. Supports YAML frontmatter, cover pages, themed styling, data/info tables, and CJK fonts.

### `scripts/markdown_to_pdf.py`

HTML/CSS-based Markdown to PDF with Mermaid diagram support via Playwright.

### `scripts/mermaid_renderer.py`

Unified Mermaid rendering engine with mmdc/Playwright backends, SHA256 caching, error categorization, and strict/permissive mode support.

### `scripts/mermaid_to_image.py`

CLI wrapper for `mermaid_renderer.py`. Converts Mermaid diagram code to PNG/SVG images.

### `scripts/themes.py`

Theme definitions (navy, gray) and cross-platform CJK font discovery.

### `references/mermaid_guide.md`

Comprehensive Mermaid diagram syntax reference.

### `references/fpdf_styling_guide.md`

fpdf2 professional PDF styling guide — frontmatter fields, theme options, table modes, font requirements.

### `assets/sample_frontmatter.yaml`

Sample YAML frontmatter templates for estimates, internal documents, and simple reports.

## Important: CJK Font Rendering Issues

**Key fact:** CFF-outline fonts can produce PDFs where **text extraction is correct but visual rendering is garbled**. Do NOT rely on text extraction alone to judge PDF correctness.

### Diagnosis Flow

1. **Check stderr** for `Warning: Using CFF-outline font` or `Warning: CFF outlines detected`.
2. **If CFF warning is present** → the PDF likely has garbled CJK rendering, even if text extraction looks correct. This is a real compatibility issue between CFF outlines and fpdf2.
   - **Fix:** Install a TrueType CJK font (with `glyf` table):
     - macOS: UDEVGothic (`brew install --cask font-udev-gothic`) or Noto Sans JP TTF
     - Linux: `sudo apt install fonts-noto-cjk` (if CFF variant, use Noto Sans JP TTF instead)
     - Windows: Yu Gothic is usually TrueType (pre-installed)
   - Re-run PDF generation after installing. Confirm no CFF warning appears.
3. **If no CFF warning was emitted** → the font is TrueType and CJK rendering is correct in the actual PDF.
   - Claude Code's Read tool preview may still show garbled glyphs — this is a **preview rendering limitation only**, not a PDF defect.
   - **Do NOT switch to Playwright mode** as a workaround.
   - The `fsSelection bit 5 (bold)` warning is cosmetic and does not affect output.
   - Only investigate further if the user reports rendering problems in a standard PDF viewer (Preview.app, Adobe Acrobat, Chrome).

## Markdown Limitations for fpdf2 Mode

**Tables inside list items are NOT supported.** The mistune parser cannot recognize Markdown tables that are indented inside list items (`- item` followed by indented `| table |`). Tables must be placed at the top level (no leading spaces/indentation) to be parsed and rendered correctly.

**Before conversion, check for and fix:**
- Tables indented under `- ` list items → Move to top level
- Tables indented under `>` blockquotes → Move to top level

## Troubleshooting

### fpdf2 mode: Font not found

If automatic font discovery fails, specify fonts manually:
```bash
python scripts/markdown_to_fpdf.py input.md output.pdf \
    --font-regular /path/to/regular.ttc \
    --font-bold /path/to/bold.ttc
```

### Mermaid conversion fails (strict mode)

By default, Mermaid conversion failures halt PDF generation. Error messages include diagnostic information and fix suggestions.

**Common errors and fixes:**

| Error Category | Fix |
|---------------|-----|
| `mmdc_not_found` | `npm install -g @mermaid-js/mermaid-cli` |
| `browser_launch_failed` | `pip install playwright && playwright install chromium` |
| `syntax_error` | Check syntax at [mermaid.live](https://mermaid.live/) |
| `timeout` | Simplify diagram or increase `--timeout` |

**To allow graceful fallback** (renders code block instead of failing):
```bash
python scripts/markdown_to_fpdf.py input.md output.pdf --no-strict-mermaid
```

### Playwright mode: Mermaid diagrams not rendering

Install mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`

Or install Playwright: `pip install playwright && playwright install chromium`

Note: The Playwright Mermaid backend requires CDN access (`cdn.jsdelivr.net`) to load the Mermaid library.

### Playwright mode: Poor image quality

Use SVG format: `--image-format svg` (recommended)

## Tips

1. **Business documents** → Use fpdf2 mode with frontmatter for professional output
2. **Technical docs with diagrams** → Use Playwright mode with SVG format
3. **Use `<!-- pagebreak -->`** for clean section transitions in fpdf2 mode
4. **Use `<!-- info-table -->`** for key-value tables in fpdf2 mode
5. **Preview Mermaid** at [mermaid.live](https://mermaid.live/) before conversion
6. **Mermaid Gantt chart font sizes** → fpdf2 mode renders Mermaid at 1200px width then scales to A4 page width (190mm). To ensure readability, use `fontSize: 16` or larger in the `%%{init: ...}%%` block. Recommended settings for Gantt charts:
   ```
   'gantt': { 'fontSize': 18, 'sectionFontSize': 20, 'barHeight': 30, 'leftPadding': 180 }
   ```
