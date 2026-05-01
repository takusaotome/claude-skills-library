---
layout: default
title: "Purchase Request Generator"
grand_parent: English
parent: Project & Business
nav_order: 30
lang_peer: /ja/skills/management/purchase-request-generator/
permalink: /en/skills/management/purchase-request-generator/
---

# Purchase Request Generator
{: .no_toc }

Generate formal IT/hardware purchase request documents from informal requirements. Use when creating purchase justifications, cost-benefit analyses, ROI calculations, vendor comparisons, or MARP presentation slides for management approval.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/purchase-request-generator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/purchase-request-generator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Creates formal IT/HW purchase requests with cost-benefit analysis (ROI / NPV / payback period), weighted vendor comparison matrices with scoring/ranking, MARP presentation slides for management approval, and sensitivity analysis covering break-even and risk scenarios. Four scripts cover purchase-request, CBA, vendor-comparison, and MARP-slide generation.

---

## 2. Prerequisites

- Python 3.9+
- MARP CLI (optional, for slide rendering)
- No API keys required

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=purchase-request-generator

# Or fetch the .skill package
curl -L -o purchase-request-generator.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/purchase-request-generator.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/purchase-request-generator/SKILL.md`.

---

## 5. Usage Examples

- You're writing a justification doc for a hardware/software purchase
- You need ROI / NPV / payback figures for management approval
- You're comparing 2-5 vendors and want a weighted scoring matrix
- You need MARP slides to present the request to leadership

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/purchase-request-generator/SKILL.md` open alongside this guide; it remains the authoritative source.
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

- `skills/purchase-request-generator/references/purchase_request_guide.md`

**Scripts:**

- `skills/purchase-request-generator/scripts/generate_cba.py`
- `skills/purchase-request-generator/scripts/generate_marp_slides.py`
- `skills/purchase-request-generator/scripts/generate_purchase_request.py`
- `skills/purchase-request-generator/scripts/generate_vendor_comparison.py`

**Assets:**

- `skills/purchase-request-generator/assets/marp_template.md`
