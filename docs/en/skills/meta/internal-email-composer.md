---
layout: default
title: "Internal Email Composer"
grand_parent: English
parent: Meta & Quality
nav_order: 26
lang_peer: /ja/skills/meta/internal-email-composer/
permalink: /en/skills/meta/internal-email-composer/
---

# Internal Email Composer
{: .no_toc }

Compose professional internal emails for coordination tasks like vendor RFQ forwarding, task delegation, status updates, and follow-ups. Generates bilingual (JA/EN) drafts with proper business tone.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/internal-email-composer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/internal-email-composer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Composes professional bilingual emails across 6 internal scenarios (vendor RFQ, task delegation, status update, follow-up, escalation, info request). Applies appropriate keigo levels for Japanese, professional tone for English, with 3 urgency levels driving subject prefixes and salutation choices.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=internal-email-composer

# Or fetch the .skill package
curl -L -o internal-email-composer.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/internal-email-composer.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/internal-email-composer/SKILL.md`.

---

## 5. Usage Examples

- You're forwarding vendor RFQs internally with bilingual coordination
- You delegate tasks via email and want consistent JA/EN drafts
- You send weekly status updates and need a templated tone
- You need urgency-aware subject prefixes (e.g. [URGENT])

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/internal-email-composer/SKILL.md` open alongside this guide; it remains the authoritative source.
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

- `skills/internal-email-composer/references/business-etiquette-guide.md`
- `skills/internal-email-composer/references/email-templates.md`

**Scripts:**

- `skills/internal-email-composer/scripts/compose_email.py`

**Assets:**

_(none)_
