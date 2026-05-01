---
layout: default
title: "AI-BPO Proposal Generator"
grand_parent: English
parent: Project & Business
nav_order: 29
lang_peer: /ja/skills/management/ai-bpo-proposal-generator/
permalink: /en/skills/management/ai-bpo-proposal-generator/
---

# AI-BPO Proposal Generator
{: .no_toc }

Generate AI-powered BPO service proposals for Japanese companies in the US market. Includes service module selection, ROI estimation, implementation roadmap, and bilingual proposal documents.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ai-bpo-proposal-generator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ai-bpo-proposal-generator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Selects from 15 AI service modules across 5 BPO categories (F&A, HR/Payroll, Customer Support, Data Processing, Procurement), computes current vs. future-state ROI / NPV / payback, and emits a bilingual proposal with phased implementation roadmap and 3 industry bundles.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=ai-bpo-proposal-generator

# Or fetch the .skill package
curl -L -o ai-bpo-proposal-generator.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ai-bpo-proposal-generator.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/ai-bpo-proposal-generator/SKILL.md`.

---

## 5. Usage Examples

- You're proposing AI-driven BPO services to Japanese clients in the US
- You need bilingual (JA/EN) proposal documents with ROI calculations
- You want a structured intake → service selection → roadmap → proposal flow
- You need industry-specific service bundles (F&A, HR, CS, etc.)

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/ai-bpo-proposal-generator/SKILL.md` open alongside this guide; it remains the authoritative source.
- Read the most relevant reference file first (see Section 10) instead of trying to absorb all of them.
- Run scripts on test data before applying to production-bound inputs.
- Preserve intermediate outputs so you can explain assumptions and trace decisions.

---

## 8. Combining with Other Skills

- Pair with adjacent skills in the same category to cover the planning → execution → review arc.
- Browse the Project & Business category for neighboring workflows: [category index]({{ '/en/skills/management/' | relative_url }}).
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

- `skills/ai-bpo-proposal-generator/references/client-intake-template.md`
- `skills/ai-bpo-proposal-generator/references/roi-methodology.md`
- `skills/ai-bpo-proposal-generator/references/service-catalog.md`

**Scripts:**

- `skills/ai-bpo-proposal-generator/scripts/calculate_roi.py`
- `skills/ai-bpo-proposal-generator/scripts/generate_proposal.py`
- `skills/ai-bpo-proposal-generator/scripts/generate_roadmap.py`
- `skills/ai-bpo-proposal-generator/scripts/select_services.py`

**Assets:**

_(none)_
