---
layout: default
title: Markdown to PDF
grand_parent: English
parent: Operations & Docs
nav_order: 3
lang_peer: /ja/skills/ops/markdown-to-pdf/
permalink: /en/skills/ops/markdown-to-pdf/
---

# Markdown to PDF
{: .no_toc }

Convert Markdown documents to professional PDFs with two rendering engines -- Playwright for technical docs and fpdf2 for business documents.
{: .fs-6 .fw-300 }

<span class="badge badge-scripts">Python Scripts</span>
<span class="badge badge-workflow">Workflow</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Markdown to PDF provides two rendering engines for converting Markdown to PDF:

1. **Playwright mode** -- HTML/CSS-based rendering with full Mermaid diagram support. Best for technical documentation with custom CSS styling.
2. **fpdf2 mode** -- Professional PDF generation with cover pages, themed headers/footers, styled tables, and CJK font support. Best for business documents such as estimates, proposals, and reports.

Both modes support Mermaid diagram conversion, code blocks, and standard Markdown formatting.

---

## When to Use

- Converting Markdown files to PDF
- Creating professional business documents (estimates, proposals, reports) with cover pages
- Converting technical documentation with Mermaid diagrams to PDF
- Generating themed PDFs with corporate styling (navy or gray themes)
- Extracting Mermaid diagrams as standalone PNG or SVG images

---

## Prerequisites

- **Claude Code** installed and running
- **markdown-to-pdf** skill installed (`cp -r ./skills/markdown-to-pdf ~/.claude/skills/`)

**For fpdf2 mode (business PDFs):**
```bash
pip install fpdf2 mistune pyyaml
```

**For Playwright mode (technical docs with Mermaid):**
```bash
pip install markdown2 playwright
playwright install chromium
npm install -g @mermaid-js/mermaid-cli
```

---

## How It Works

### Engine comparison

| Feature | fpdf2 (`markdown_to_fpdf.py`) | Playwright (`markdown_to_pdf.py`) |
|:--------|:------------------------------|:----------------------------------|
| **Best for** | Business documents (estimates, proposals, reports) | Technical docs with custom CSS |
| **Cover page** | Built-in with YAML frontmatter | Not supported |
| **Themes** | navy, gray (headers/footers/tables) | Custom CSS files |
| **Table styling** | Alternating rows, colored headers, info-table mode | Standard HTML tables |
| **Mermaid support** | Renders to PNG via mmdc, embedded in PDF | Full support via mmdc or Playwright backend |
| **CJK fonts** | Auto-discovery with TrueType preference | Uses system fonts via browser |
| **Page breaks** | `<!-- pagebreak -->` comment | CSS `page-break-before` |
| **Dependencies** | `fpdf2`, `mistune`, `pyyaml` | `markdown2`, `playwright`, `chromium` |
| **Confidential mark** | `--confidential` flag | Manual CSS |

### Choosing a mode

| Need | Mode | Script |
|:-----|:-----|:-------|
| Cover page, professional styling | fpdf2 | `markdown_to_fpdf.py` |
| Business documents (estimates, reports) | fpdf2 | `markdown_to_fpdf.py` |
| Themed headers/footers | fpdf2 | `markdown_to_fpdf.py` |
| Styled tables (alternating rows) | fpdf2 | `markdown_to_fpdf.py` |
| Technical docs with custom CSS | Playwright | `markdown_to_pdf.py` |
| Mermaid diagrams as primary content | Playwright | `markdown_to_pdf.py` |

### fpdf2 mode workflow

1. Add YAML frontmatter to your Markdown file (title, subtitle, theme, etc.)
2. Run the conversion:
   ```bash
   python scripts/markdown_to_fpdf.py input.md output.pdf --theme navy
   ```
3. Verify the output PDF

### Playwright mode workflow

1. Run the conversion:
   ```bash
   python scripts/markdown_to_pdf.py input.md output.pdf
   ```
2. Mermaid code blocks are automatically converted to images
3. Verify the output PDF

### Mermaid diagram support

Both engines can convert Mermaid code blocks into images. The rendering pipeline:

1. Mermaid code blocks (` ```mermaid `) are detected in the Markdown source
2. Each block is rendered to PNG (or SVG in Playwright mode) using `mermaid_renderer.py`
3. The rendered image replaces the code block in the final PDF
4. SHA256-based caching avoids re-rendering unchanged diagrams

Supported Mermaid diagram types include flowcharts, sequence diagrams, Gantt charts, class diagrams, state diagrams, ER diagrams, and pie charts. Preview diagrams at [mermaid.live](https://mermaid.live/) before conversion.

**Strict vs. permissive mode**: By default, Mermaid syntax errors halt PDF generation. Use `--no-strict-mermaid` to fall back to rendering the raw code block instead of failing.

### Page break and special syntax

| Syntax | Mode | Effect |
|:-------|:-----|:-------|
| `<!-- pagebreak -->` | fpdf2 | Insert a page break |
| `<!-- info-table -->` | fpdf2 | Render the next table as key-value info-table style |
| `---` | fpdf2 | Horizontal rule |
| ` ```mermaid ` | Both | Render Mermaid diagram as image |

---

## Usage Examples

### Example 1: Professional business estimate

```
Convert this estimate to a professional PDF with a cover page.
Use the navy theme and mark it as confidential.
```

The skill will add frontmatter, run `markdown_to_fpdf.py --theme navy --confidential`, and produce a polished business PDF.

### Example 2: Technical documentation with diagrams

```
Convert our API design document to PDF. It contains several
Mermaid sequence diagrams that need to render properly.
```

The skill will use Playwright mode with SVG format for high-quality diagram rendering.

### Example 3: Export a Mermaid diagram

```
Export this Mermaid flowchart as a PNG image:

graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
```

The skill will use `mermaid_to_image.py` to produce a standalone PNG.

### Example 4: Internal report with gray theme

```
Convert this monthly operations report to PDF.
Use the gray theme (internal document) and add page breaks
between sections. No cover page needed.
```

The skill will run `markdown_to_fpdf.py --theme gray --no-cover`, using `<!-- pagebreak -->` markers for section transitions and the gray theme for internal document styling.

---

## Troubleshooting

### CJK text appears garbled in fpdf2 mode

**Symptom**: Japanese, Chinese, or Korean characters render as boxes or random symbols in the generated PDF, even though text extraction tools show the correct text.

**Solution**: This is caused by CFF-outline fonts (e.g., Hiragino Sans on macOS). Install a TrueType CJK font: `brew install --cask font-udev-gothic` (macOS) or `sudo apt install fonts-noto-cjk` (Linux). Check stderr for "Warning: Using CFF-outline font" to confirm. After installing, re-run the conversion and confirm no CFF warning appears.

### Mermaid conversion fails in strict mode

**Symptom**: PDF generation halts with an error message about Mermaid syntax or missing tools.

**Solution**: Check the error category in the output. If `mmdc_not_found`, install mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`. If `syntax_error`, validate your diagram at [mermaid.live](https://mermaid.live/). If `browser_launch_failed`, install Playwright: `pip install playwright && playwright install chromium`. To allow graceful fallback (renders code block instead of failing), add `--no-strict-mermaid`.

### Tables inside list items are not rendered

**Symptom**: A Markdown table that is indented under a list item (`- item`) or blockquote (`>`) does not appear in the PDF.

**Solution**: The fpdf2 mode's mistune parser cannot recognize indented tables. Move the table to the top level (no leading spaces or indentation). This is a known limitation of fpdf2 mode.

---

## Tips & Best Practices

- **Business documents**: Use fpdf2 mode with YAML frontmatter for cover pages and themed styling
- **Technical docs with diagrams**: Use Playwright mode with `--image-format svg` for high-quality output
- **Page breaks**: Use `<!-- pagebreak -->` for clean section transitions in fpdf2 mode
- **Key-value tables**: Use `<!-- info-table -->` before a table for info-table styling in fpdf2 mode
- **CJK fonts**: Install TrueType CJK fonts (UDEVGothic or Noto Sans JP) to avoid garbled text. CFF-outline fonts like Hiragino can cause rendering issues.
- **Mermaid preview**: Preview diagrams at [mermaid.live](https://mermaid.live/) before conversion
- **Themes**: `navy` for client-facing documents, `gray` for internal documents

---

## Related Skills

- [operations-manual-creator]({{ '/en/skills/ops/operations-manual-creator/' | relative_url }}) -- Create operations manuals, then convert to PDF with this skill
- [technical-spec-writer]({{ '/en/skills/ops/technical-spec-writer/' | relative_url }}) -- Write technical specifications with Mermaid diagrams
- [presentation-reviewer]({{ '/en/skills/ops/presentation-reviewer/' | relative_url }}) -- Review presentations before converting to PDF
