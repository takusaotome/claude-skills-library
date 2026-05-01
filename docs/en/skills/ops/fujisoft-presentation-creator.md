---
layout: default
title: "Fujisoft Presentation Creator"
grand_parent: English
parent: Operations & Docs
nav_order: 8
lang_peer: /ja/skills/ops/fujisoft-presentation-creator/
permalink: /en/skills/ops/fujisoft-presentation-creator/
---

# Fujisoft Presentation Creator
{: .no_toc }

This skill should be used when creating professional presentation materials, slide decks, or proposal documents following FUJISOFT America's corporate template standards. Triggers include requests like "create a presentation", "make slides", "prepare proposal materials", "FUJISOFT template", or when MARP-format Markdown presentations are needed with consistent corporate branding. The skill provides a complete MARP template with CSS styling, visual design components, and quality assurance workflows.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/fujisoft-presentation-creator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/fujisoft-presentation-creator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill enables creation of professional, high-quality presentation materials using FUJISOFT America's corporate slide template. The template is built on MARP (Markdown Presentation Ecosystem), enabling efficient slide creation through Markdown while maintaining consistent corporate branding and design standards.

---

## 2. Prerequisites

- **MARP CLI**: Install via `npm install -g @marp-team/marp-cli` for command-line export
- **Node.js**: Required for visual review tools (v16+ recommended)
- **VS Code/Cursor with Marp Extension** (optional): For live preview and GUI export

---

## 3. Quick Start

### Step 1: Understand Requirements

Before creating slides, gather the following information:

---

## 4. How It Works

### Step 1: Understand Requirements

Before creating slides, gather the following information:

1. **Purpose**: Information sharing, decision-making, or action promotion
2. **Audience**: Executives, technical staff, sales prospects, etc.
3. **Key Messages**: Main points to convey (limit to 3-5)
4. **Time Constraint**: Presentation duration including Q&A
5. **Output Format**: PDF, HTML, or editable PPTX

### Step 2: Create Presentation Structure

Follow the Guy Kawasaki 10-20-30 Rule as a guideline:
- **10 slides** maximum for optimal engagement
- **20 minutes** presentation time
- **30pt** minimum font size

Typical presentation structure:
1. Cover Page (title, subtitle, company info)
2. Executive Summary / Agenda
3. Current Situation / Problem Statement
4. Proposed Solution
5. Technical Architecture / Approach
6. Implementation Timeline

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Creating client proposals and technical presentations
- Preparing project progress reports
- Building sales presentations
- Developing seminar or workshop materials
- Any external-facing presentation requiring FUJISOFT America branding

---

## 6. Understanding the Output

This skill generates **MARP-format Markdown files** (`.md`) that can be exported to:
- **PDF** (recommended for distribution)
- **HTML** (for web viewing)
- **PPTX** (editable PowerPoint format)

The output follows FUJISOFT America's corporate branding and design standards.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/fujisoft-presentation-creator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: presentation_best_practices_checklist.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/ops/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.

---

## 10. Reference

**References:**

- `skills/fujisoft-presentation-creator/references/presentation_best_practices_checklist.md`
