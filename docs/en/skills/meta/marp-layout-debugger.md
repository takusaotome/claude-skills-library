---
layout: default
title: "MARP Layout Debugger"
grand_parent: English
parent: Meta & Quality
nav_order: 28
lang_peer: /ja/skills/meta/marp-layout-debugger/
permalink: /en/skills/meta/marp-layout-debugger/
---

# MARP Layout Debugger
{: .no_toc }

Diagnose and fix MARP slide layout issues including whitespace problems, box alignment, bullet formatting, and CSS rendering inconsistencies. Useful when MARP slides have visual layout problems or need CSS optimization.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/marp-layout-debugger.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/marp-layout-debugger){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Analyzes MARP source for layout issues (whitespace, alignment, bullet/overflow problems), proposes fixes from a CSS fix catalog and layout-pattern reference, and emits a diff report showing before/after. Aimed at recovering existing decks rather than authoring from scratch.

---

## 2. Prerequisites

- Python 3.9+
- MARP CLI (optional, for rendering)
- No API keys required

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=marp-layout-debugger

# Or fetch the .skill package
curl -L -o marp-layout-debugger.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/marp-layout-debugger.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/marp-layout-debugger/SKILL.md`.

---

## 5. Usage Examples

- A MARP slide has weird whitespace, overflow, or alignment issues
- You're cleaning up auto-generated MARP decks (e.g. from generators)
- You need a CSS fix recipe for a specific MARP layout pattern
- You want a before/after diff to review proposed CSS changes

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/marp-layout-debugger/SKILL.md` open alongside this guide; it remains the authoritative source.
- Read the most relevant reference file first (see Section 10) instead of trying to absorb all of them.
- Run scripts on test data before applying to production-bound inputs.
- Preserve intermediate outputs so you can explain assumptions and trace decisions.

---

## 8. Combining with Other Skills

- Pair with adjacent skills in the same category to cover the planning → execution → review arc.
- Browse the Meta & Quality category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).
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

- `skills/marp-layout-debugger/references/css-fix-catalog.md`
- `skills/marp-layout-debugger/references/marp-layout-patterns.md`

**Scripts:**

- `skills/marp-layout-debugger/scripts/analyze_marp_layout.py`
- `skills/marp-layout-debugger/scripts/fix_marp_layout.py`
- `skills/marp-layout-debugger/scripts/generate_diff_report.py`

**Assets:**

_(none)_
