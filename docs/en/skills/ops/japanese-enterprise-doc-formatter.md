---
layout: default
title: "Japanese Enterprise Document Formatter"
grand_parent: English
parent: Operations & Docs
nav_order: 13
lang_peer: /ja/skills/ops/japanese-enterprise-doc-formatter/
permalink: /en/skills/ops/japanese-enterprise-doc-formatter/
---

# Japanese Enterprise Document Formatter
{: .no_toc }

Format documents for Japanese enterprise approval workflows including ringi (稟議), purchase requests (購入申請), and internal proposals. Handles bilingual requirements, proper keigo levels, required approval sections, and corporate template compliance.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/japanese-enterprise-doc-formatter.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/japanese-enterprise-doc-formatter){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Formats 5 enterprise document types (稟議書 / 購入申請書 / 提案書 / 報告書 / 依頼書) with 4 keigo levels (最上級 / 上級 / 標準 / 基本). Includes section validation with completeness scoring, bilingual output with English summaries, and approval-section generation appropriate to each document type.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=japanese-enterprise-doc-formatter

# Or fetch the .skill package
curl -L -o japanese-enterprise-doc-formatter.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/japanese-enterprise-doc-formatter.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/japanese-enterprise-doc-formatter/SKILL.md`.

---

## 5. Usage Examples

- You're drafting 稟議書 / 購入申請書 / 提案書 for Japanese approval flows
- You need automatic keigo-level normalization across document types
- You want section validation against required structures (e.g. 背景/目的/効果/費用/承認)
- You produce bilingual versions for cross-regional approval chains

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/japanese-enterprise-doc-formatter/SKILL.md` open alongside this guide; it remains the authoritative source.
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

- `skills/japanese-enterprise-doc-formatter/references/document_types.md`
- `skills/japanese-enterprise-doc-formatter/references/keigo_guide.md`
- `skills/japanese-enterprise-doc-formatter/references/section_templates.md`

**Scripts:**

- `skills/japanese-enterprise-doc-formatter/scripts/format_document.py`
- `skills/japanese-enterprise-doc-formatter/scripts/transform_keigo.py`
- `skills/japanese-enterprise-doc-formatter/scripts/validate_sections.py`

**Assets:**

_(none)_
