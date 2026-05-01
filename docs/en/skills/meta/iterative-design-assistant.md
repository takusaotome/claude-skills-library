---
layout: default
title: "Iterative Design Assistant"
grand_parent: English
parent: Meta & Quality
nav_order: 27
lang_peer: /ja/skills/meta/iterative-design-assistant/
permalink: /en/skills/meta/iterative-design-assistant/
---

# Iterative Design Assistant
{: .no_toc }

Track design iteration history and apply consistent styling decisions across revision cycles. Use when handling follow-up change requests that reference previous decisions ("前回も色で良いんだけど", "same style as before").
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/iterative-design-assistant.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/iterative-design-assistant){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Maintains a session-local design decision log (JSON v1.0) across 5 categories (color/typography/layout/content/style). CLI commands cover init/record/query/search/apply/history/token/resolve. Resolves contextual references in JP and EN, manages design tokens by category namespace, and provides bidirectional traceability between decisions and elements.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=iterative-design-assistant

# Or fetch the .skill package
curl -L -o iterative-design-assistant.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/iterative-design-assistant.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/iterative-design-assistant/SKILL.md`.

---

## 5. Usage Examples

- A reviewer says "same as last time" and you need to recall what "last time" was
- You're iterating on slide / brand / layout designs across multiple sessions
- You want a queryable history of design decisions per project
- You need design tokens consistent across an iteration

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/iterative-design-assistant/SKILL.md` open alongside this guide; it remains the authoritative source.
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

- `skills/iterative-design-assistant/references/design-decision-methodology.md`

**Scripts:**

- `skills/iterative-design-assistant/scripts/design_log.py`

**Assets:**

_(none)_
