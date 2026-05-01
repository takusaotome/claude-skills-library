---
layout: default
title: "Vendor Procurement Coordinator"
grand_parent: English
parent: Meta & Quality
nav_order: 29
lang_peer: /ja/skills/meta/vendor-procurement-coordinator/
permalink: /en/skills/meta/vendor-procurement-coordinator/
---

# Vendor Procurement Coordinator
{: .no_toc }

End-to-end vendor procurement workflow orchestrating RFQ creation, email sending, vendor response tracking, and client-facing estimate generation. Coordinates between vendor-rfq-creator and vendor-estimate-creator skills with email automation and status tracking.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-procurement-coordinator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/vendor-procurement-coordinator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Initializes a procurement project with a standard directory structure (rfq/, quotes/, estimates/, communications/), manages vendors (add/edit/remove/CSV import) with status tracking, logs quote responses with amount/currency/delivery date/validity period, provides Japanese/English RFQ email templates and reminder templates, generates vendor comparison reports with price scoring, and emits a complete timeline for audit trail.

---

## 2. Prerequisites

- Python 3.9+
- PyYAML
- No API keys required

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=vendor-procurement-coordinator

# Or fetch the .skill package
curl -L -o vendor-procurement-coordinator.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-procurement-coordinator.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/vendor-procurement-coordinator/SKILL.md`.

---

## 5. Usage Examples

- You manage vendor RFQs end-to-end (request → quote → client estimate)
- You coordinate multiple vendors and need a single procurement state
- You send bilingual (JA/EN) RFQ emails and reminders on a cadence
- You need an audit trail of every procurement event

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/vendor-procurement-coordinator/SKILL.md` open alongside this guide; it remains the authoritative source.
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

- `skills/vendor-procurement-coordinator/references/procurement_workflow_guide.md`
- `skills/vendor-procurement-coordinator/references/vendor_evaluation_criteria.md`

**Scripts:**

- `skills/vendor-procurement-coordinator/scripts/compare_quotes.py`
- `skills/vendor-procurement-coordinator/scripts/init_procurement.py`
- `skills/vendor-procurement-coordinator/scripts/manage_vendors.py`
- `skills/vendor-procurement-coordinator/scripts/procurement_models.py`
- `skills/vendor-procurement-coordinator/scripts/track_responses.py`

**Assets:**

- `skills/vendor-procurement-coordinator/assets/reminder_email.md`
- `skills/vendor-procurement-coordinator/assets/rfq_email_en.md`
- `skills/vendor-procurement-coordinator/assets/rfq_email_ja.md`
