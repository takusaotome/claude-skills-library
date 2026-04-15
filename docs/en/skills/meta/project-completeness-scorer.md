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

### Step 1: Select Project Template

Determine the project type and load the appropriate evaluation template.

Supported project types:
- `skill` -- Claude skill development (SKILL.md, scripts, tests, references)
- `webapp` -- Web application (frontend, backend, API, tests, docs)
- `library` -- Reusable library/package (code, tests, docs, packaging)
- `document` -- Documentation-only project (structure, completeness, quality)
- `custom` -- User-defined criteria from JSON file

```bash
# List available templates
python3 scripts/score_project.py --list-templates

# Use a specific template
python3 scripts/score_project.py --template skill --project-path ./skills/my-skill
```

### Step 2: Gather Project Artifacts

Scan the project directory to inventory existing files and categorize them by evaluation dimension:

1. **Functional Requirements** -- Core deliverables and features

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Assessing a project's readiness for release or handoff
- Reviewing milestone deliverables against acceptance criteria
- Identifying gaps in code, documentation, or configuration
- Comparing actual progress against a project checklist
- Preparing for stakeholder reviews or gate approvals
- Scoring skill development projects within this repository

---

## 6. Understanding the Output

### JSON Report

```json
{
  "schema_version": "1.0",
  "project_path": "./skills/my-skill",
  "project_type": "skill",
  "timestamp": "2026-03-16T08:00:00Z",
  "overall_score": 85,
  "dimensions": [
    {
      "name": "Functional Requirements",
      "weight": 0.30,
      "raw_score": 90,
      "weighted_score": 27.0,
      "criteria": [
        {"name": "SKILL.md exists", "met": true, "severity": "critical"},
        {"name": "Scripts directory exists", "met": true, "severity": "major"}

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/project-completeness-scorer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: scoring-methodology.md, project-templates.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: score_project.py.
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

- `skills/project-completeness-scorer/references/project-templates.md`
- `skills/project-completeness-scorer/references/scoring-methodology.md`

**Scripts:**

- `skills/project-completeness-scorer/scripts/score_project.py`
