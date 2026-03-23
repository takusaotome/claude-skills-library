---
layout: default
title: "Project Completeness Scorer"
grand_parent: English
parent: Meta & Quality
nav_order: 18
lang_peer: /ja/skills/meta/project-completeness-scorer/
permalink: /en/skills/meta/project-completeness-scorer/
---

# Project Completeness Scorer
{: .no_toc }

Evaluate project deliverables (code, docs, config) and calculate a 0-100 completeness score with weighted criteria and prioritized action items. Use when assessing project readiness, reviewing milestones, or identifying gaps before release.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/project-completeness-scorer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/project-completeness-scorer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill systematically evaluates project deliverables across multiple dimensions (functional requirements, quality standards, test coverage, documentation, deployment readiness) and produces a weighted 0-100 completeness score. It identifies gaps, ranks missing items by priority, and provides actionable next steps to reach completion.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (json, pathlib, argparse)

---

## 3. Quick Start

```bash
# List available templates
python3 scripts/score_project.py --list-templates

# Use a specific template
python3 scripts/score_project.py --template skill --project-path ./skills/my-skill
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

- `skills/project-completeness-scorer/references/project-templates.md`
- `skills/project-completeness-scorer/references/scoring-methodology.md`

**Scripts:**

- `skills/project-completeness-scorer/scripts/score_project.py`
