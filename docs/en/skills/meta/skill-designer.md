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

### Step 1: Prepare Idea Specification

Accept a JSON file (`--idea-json`) containing:
- `title`: Human-readable idea name
- `description`: What the skill does
- `category`: Skill category (e.g., business-analysis, developer-tooling)

Accept a normalized skill name (`--skill-name`) that will be used as the
directory name and YAML frontmatter `name:` field.

### Step 2: Build Design Prompt

Run the prompt builder:

```bash
python3 scripts/build_design_prompt.py \
  --idea-json /tmp/idea.json \
  --skill-name "my-new-skill" \
  --project-root .
```

The script:
1. Loads the idea JSON
2. Reads all three reference files (structure guide, quality checklist, template)

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- The skill auto-generation pipeline selects an idea from the backlog and needs
- A developer wants to bootstrap a new business/professional skill from a JSON idea specification
- Quality review of generated skills requires awareness of the scoring rubric

---

## 6. Understanding the Output

The script outputs a plain-text prompt to stdout. Exit code 0 on success,
1 if required reference files are missing.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/skill-designer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: skill-structure-guide.md, quality-checklist.md, skill-template.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: build_design_prompt.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/skill-designer/references/quality-checklist.md`
- `skills/skill-designer/references/skill-structure-guide.md`
- `skills/skill-designer/references/skill-template.md`

**Scripts:**

- `skills/skill-designer/scripts/build_design_prompt.py`
