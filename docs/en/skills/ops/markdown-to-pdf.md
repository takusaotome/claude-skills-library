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
