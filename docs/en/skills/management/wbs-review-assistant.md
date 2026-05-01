---
layout: default
title: "WBS Review Assistant"
grand_parent: English
parent: Project & Business
nav_order: 28
lang_peer: /ja/skills/management/wbs-review-assistant/
permalink: /en/skills/management/wbs-review-assistant/
---

# WBS Review Assistant
{: .no_toc }

Review WBS (Work Breakdown Structure) Excel files against requirements docs, hearing sheets, and prior decisions to identify gaps, inconsistencies, and deviations. Add review comments to Excel cells and generate summary reports.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/wbs-review-assistant.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/wbs-review-assistant){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Review and annotate Work Breakdown Structure (WBS) Excel files against project requirements, hearing sheets, and prior decisions. Automatically identify gaps, inconsistencies, deviations from agreed principles, and missing tasks. Add review comments directly to Excel cells and generate prioritized summary reports with actionable findings.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: `openpyxl`, `pandas`, `pyyaml`

---

## 3. Quick Start

```bash
# User provides files in conversation or specifies paths
# Claude will read these files to understand context
```

---

## 4. How It Works

### Step 1: Gather Review Inputs

Collect the following files:
- **WBS Excel file** (`.xlsx`) - the WBS to be reviewed
- **Requirements document** (`.pdf`, `.docx`, `.md`) - project requirements or specifications
- **Hearing sheet / meeting notes** (optional) - decisions and clarifications from stakeholder meetings
- **Review checklist** (optional) - custom review criteria YAML file

```bash
# User provides files in conversation or specifies paths
# Claude will read these files to understand context
```

### Step 2: Run WBS Review Analysis

Execute the review script to analyze the WBS against requirements:

```bash
python3 scripts/wbs_reviewer.py \
  --wbs path/to/wbs.xlsx \
  --requirements path/to/requirements.md \
  --hearing-sheet path/to/hearing_notes.md \
  --output-dir ./wbs_review_output \
  --checklist references/review_checklist.yaml

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- User requests "review this WBS against requirements"
- User provides WBS Excel file + requirement documents for gap analysis
- User asks to "check WBS consistency with hearing sheet decisions"
- User needs to validate WBS completeness before baseline approval
- User wants to annotate WBS with review comments in Excel
- Project manager needs prioritized list of WBS issues before kickoff

---

## 6. Understanding the Output

### Annotated Excel Structure

The annotated WBS Excel contains:
- **Original columns preserved** - No modification to WBS structure
- **Cell comments added** - Review findings attached to relevant cells
- **Conditional formatting** - Color-coded by severity
  - Red fill: Critical issues
  - Orange fill: Major issues
  - Yellow fill: Minor issues
- **New sheet: "Review Summary"** - Issue dashboard with filters

### Markdown Summary Report

```markdown
# WBS Review Summary

**Review Date:** YYYY-MM-DD HH:MM:SS
**WBS File:** wbs.xlsx

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/wbs-review-assistant/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: wbs_review_methodology.md, common_wbs_issues.md, review_checklist.yaml.
- Run helper scripts on test data before using them on final assets or production-bound inputs: wbs_reviewer.py, requirements_parser.py, excel_annotator.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/management/' | relative_url }}).
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

- `skills/wbs-review-assistant/references/common_wbs_issues.md`
- `skills/wbs-review-assistant/references/review_checklist.yaml`
- `skills/wbs-review-assistant/references/wbs_review_methodology.md`

**Scripts:**

- `skills/wbs-review-assistant/scripts/excel_annotator.py`
- `skills/wbs-review-assistant/scripts/requirements_parser.py`
- `skills/wbs-review-assistant/scripts/wbs_reviewer.py`
