# fpdf2 Professional PDF Styling Guide

## Overview

This guide documents the fpdf2-based professional PDF rendering mode (`markdown_to_fpdf.py`), which converts Markdown documents with YAML frontmatter into business-quality PDFs with cover pages, themed styling, and professional table formatting.

## YAML Frontmatter Specification

The frontmatter block must appear at the top of the Markdown file, enclosed in `---` delimiters:

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

### Field Reference

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | string | (none) | Document title (cover page and metadata) |
| `subtitle` | string | (none) | Subtitle shown below title on cover |
| `theme` | string | `navy` | Color theme: `navy` or `gray` |
| `document_number` | string | (none) | Document ID shown in header |
| `date` | string | (none) | Issue date shown on cover |
| `author` | string | (none) | Author name shown on cover |
| `company` | string | (none) | Issuing company shown on cover and header |
| `recipient` | string | (none) | Recipient shown on cover |
| `confidential` | bool | `false` | Adds "CONFIDENTIAL" badge and footer |
| `cover` | bool | `false` | Generate cover page |
| `header_text` | string | auto | Custom header text (auto-generated from document_number + company if omitted) |

## Theme Options

### Navy Theme (`navy`)

Client-facing documents (estimates, proposals, reports).

| Element | Color (RGB) |
|---------|------------|
| Primary | (0, 51, 102) — Deep navy |
| Primary Light | (230, 238, 247) — Light blue-gray |
| Table Header BG | (0, 51, 102) — Navy |
| Table Header FG | (255, 255, 255) — White |
| Table Alt Row | (230, 238, 247) — Light blue-gray |

### Gray Theme (`gray`)

Internal documents (cost analysis, internal memos).

| Element | Color (RGB) |
|---------|------------|
| Primary | (60, 60, 60) — Dark gray |
| Primary Light | (240, 240, 240) — Light gray |
| Table Header BG | (60, 60, 60) — Dark gray |
| Table Header FG | (255, 255, 255) — White |
| Table Alt Row | (240, 240, 240) — Light gray |

## Table Rendering

### Data Table (default)

All tables are rendered as data tables by default with:
- Colored header row (theme-colored background, white bold text)
- Alternating row colors
- Auto-calculated column widths based on content
- Automatic text wrapping for long content
- Automatic page breaks with header repetition

### Info Table (override)

For key-value style tables, add `<!-- info-table -->` comment immediately before the table:

```markdown
<!-- info-table -->
| Key | Value |
|-----|-------|
| Phase 1 | $5,000 |
| Phase 2 | TBD |
```

Info tables use the same styling engine but are visually suited for 2-column key-value layouts.

## Page Breaks

Use HTML comments for explicit page breaks:

```markdown
Content before break.

<!-- pagebreak -->

Content after break (new page).
```

The standard Markdown `---` (thematic break) renders as a horizontal rule, not a page break.

## Font Requirements

### macOS
- **Hiragino Kaku Gothic W3** (regular) — pre-installed
- **Hiragino Kaku Gothic W6** (bold) — pre-installed

### Windows
- **Yu Gothic Regular/Bold** — pre-installed on Windows 10+

### Linux
- **Noto Sans CJK** — install via `sudo apt install fonts-noto-cjk`

### Manual Override

If automatic font discovery fails, specify fonts explicitly:

```bash
python markdown_to_fpdf.py input.md output.pdf \
    --font-regular /path/to/regular.ttc \
    --font-bold /path/to/bold.ttc
```

## Mermaid Diagram Rendering

In fpdf2 mode, Mermaid code blocks (` ```mermaid `) are converted to PNG images via the `MermaidRenderer` class and embedded in the PDF.

### Backend Priority

1. **mmdc** (mermaid-cli) — preferred. Install: `npm install -g @mermaid-js/mermaid-cli`
2. **Playwright** — fallback. Install: `pip install playwright && playwright install chromium`

In AUTO mode (default), mmdc is tried first. If it fails for reasons other than syntax errors, Playwright is attempted as a fallback. Syntax errors are never retried with a different backend.

### Strict vs Permissive Mode

- **Strict (default):** Mermaid conversion failure raises `MermaidRenderError` and halts PDF generation. This ensures diagrams are always present in the output.
- **Permissive (`--no-strict-mermaid`):** Mermaid conversion failure falls back to rendering the diagram source as a code block. Useful when mmdc/Playwright may not be available.

### Constraints

- PNG format is used (SVG embedding in fpdf2 is not supported without `fpdf2[svg]`)
- The Playwright backend requires CDN access (`cdn.jsdelivr.net`) to load the Mermaid JavaScript library
- A shared `MermaidRenderer` instance is used per document for cache efficiency

## Best Practices for Business Documents

1. **Always use frontmatter** for estimates and proposals — it enables cover pages and consistent headers
2. **Use `<!-- info-table -->`** for summary/overview tables at the beginning of sections
3. **Use `<!-- pagebreak -->`** before major sections to ensure clean page transitions
4. **Keep table cells concise** — very long cell content works but impacts readability
5. **Use `navy` theme** for client-facing documents, `gray` for internal
6. **Set `confidential: true`** for internal cost analyses and sensitive documents
