---
layout: default
title: "Skill Designer"
grand_parent: English
parent: Meta & Quality
nav_order: 20
lang_peer: /ja/skills/meta/skill-designer/
permalink: /en/skills/meta/skill-designer/
---

# Skill Designer
{: .no_toc }

Design new Claude skills from structured idea specifications. Use when the skill auto-generation pipeline needs to produce a Claude CLI prompt that creates a complete skill directory (SKILL.md, references, scripts, tests) following repository conventions.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/skill-designer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/skill-designer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Generate a comprehensive Claude CLI prompt from a structured skill idea
specification. The prompt instructs Claude to create a complete skill directory
following repository conventions: SKILL.md with YAML frontmatter, reference
documents, helper scripts, and test scaffolding.

---

## 2. Prerequisites

- Python 3.9+
- No external API keys required
- Reference files must exist under `references/`

---

## 3. Quick Start

```bash
python3 scripts/build_design_prompt.py \
  --idea-json /tmp/idea.json \
  --skill-name "my-new-skill" \
  --project-root .
```

---

## 4. How It Works

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/skill-designer/references/quality-checklist.md`
- `skills/skill-designer/references/skill-structure-guide.md`
- `skills/skill-designer/references/skill-template.md`

**Scripts:**

- `skills/skill-designer/scripts/build_design_prompt.py`
