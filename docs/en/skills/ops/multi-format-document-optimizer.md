---
layout: default
title: "Multi-Format Document Optimizer"
grand_parent: English
parent: Operations & Docs
nav_order: 14
lang_peer: /ja/skills/ops/multi-format-document-optimizer/
permalink: /en/skills/ops/multi-format-document-optimizer/
---

# Multi-Format Document Optimizer
{: .no_toc }

Unified document optimization skill that chains docling-converter, imagemagick-expert, and markdown-to-pdf. Auto-detects input format, applies the appropriate conversion pipeline, optimizes embedded images, and produces web/print-ready output with configurable quality presets.
{: .fs-6 .fw-300 }

<span class="badge badge-free">docling + ImageMagick + markdown-to-pdf</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/multi-format-document-optimizer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/multi-format-document-optimizer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Detects format and routes through pipelines (pdf_optimize / docx_to_pdf / pptx_to_pdf etc.) with 4 quality presets — web (80% / 96dpi / WebP), print (95% / 300dpi), archive (90% / 150dpi), minimal (70% / 72dpi). Supports CLI commands analyze/convert/batch/optimize-images/verify, PDF image extraction & re-embedding via PyMuPDF, and parallel batch workers.

---

## 2. Prerequisites

- Python 3.9+
- docling CLI (`pip install docling`)
- ImageMagick 7+
- fpdf2 / Playwright + chromium
- PyMuPDF (optional)

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=multi-format-document-optimizer

# Or fetch the .skill package
curl -L -o multi-format-document-optimizer.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/multi-format-document-optimizer.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/multi-format-document-optimizer/SKILL.md`.

---

## 5. Usage Examples

- You need to convert PPTX/DOCX to PDF and shrink embedded images for web
- You're batch-processing a directory of mixed-format documents
- You want web vs. print vs. archive quality presets as a single CLI flag
- You need to verify output quality after optimization

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/multi-format-document-optimizer/SKILL.md` open alongside this guide; it remains the authoritative source.
- Read the most relevant reference file first (see Section 10) instead of trying to absorb all of them.
- Run scripts on test data before applying to production-bound inputs.
- Preserve intermediate outputs so you can explain assumptions and trace decisions.

---

## 8. Combining with Other Skills

- Pair with adjacent skills in the same category to cover the planning → execution → review arc.
- Browse the Operations & Docs category for neighboring workflows: [category index]({{ '/en/skills/ops/' | relative_url }}).
- See the full English skill catalog: [skill catalog]({{ '/en/skill-catalog/' | relative_url }}).

---

## 9. Troubleshooting

- Re-check prerequisites first; missing runtime dependencies are the most common failure mode.
- Run helper scripts on a minimal input before applying them to a full dataset.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata.
- Confirm Python version (3.9+) and required packages are installed in the active environment.
- When output looks incomplete, re-read the relevant reference file to verify the input contract.

---

## 10. Reference

**References:**

- `skills/multi-format-document-optimizer/references/image_optimization_guide.md`
- `skills/multi-format-document-optimizer/references/pipeline_guide.md`

**Scripts:**

- `skills/multi-format-document-optimizer/scripts/document_optimizer.py`

**Assets:**

_(none)_
