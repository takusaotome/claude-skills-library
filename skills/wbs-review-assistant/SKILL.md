---
name: wbs-review-assistant
description: Review WBS (Work Breakdown Structure) Excel files against requirements docs, hearing sheets, and prior decisions to identify gaps, inconsistencies, and deviations. Add review comments to Excel cells and generate summary reports.
---

# WBS Review Assistant

## Overview

Review and annotate Work Breakdown Structure (WBS) Excel files against project requirements, hearing sheets, and prior decisions. Automatically identify gaps, inconsistencies, deviations from agreed principles, and missing tasks. Add review comments directly to Excel cells and generate prioritized summary reports with actionable findings.

## When to Use

- User requests "review this WBS against requirements"
- User provides WBS Excel file + requirement documents for gap analysis
- User asks to "check WBS consistency with hearing sheet decisions"
- User needs to validate WBS completeness before baseline approval
- User wants to annotate WBS with review comments in Excel
- Project manager needs prioritized list of WBS issues before kickoff

## Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: `openpyxl`, `pandas`, `pyyaml`

## Workflow

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
```

**Parameters:**
- `--wbs` - Path to WBS Excel file
- `--requirements` - Path to requirements document
- `--hearing-sheet` - (Optional) Path to hearing notes
- `--output-dir` - Directory for output files
- `--checklist` - (Optional) Custom review criteria YAML

### Step 3: Review Generated Outputs

The script generates:

1. **Annotated WBS Excel** (`wbs_annotated_YYYYMMDD_HHMMSS.xlsx`)
   - Original WBS with review comments added to cells
   - Color-coded severity (Red=Critical, Orange=Major, Yellow=Minor)
   - Comment threads with finding ID references

2. **Summary Report** (`wbs_review_summary_YYYYMMDD_HHMMSS.md`)
   - Executive summary with issue count by severity
   - Prioritized findings list with recommendations
   - Coverage analysis (requirements mapped to WBS tasks)
   - Missing task candidates

3. **Gap Analysis JSON** (`wbs_gaps_YYYYMMDD_HHMMSS.json`)
   - Machine-readable findings with structured data
   - Traceability matrix (requirements → WBS tasks)
   - Validation results for each checklist criterion

### Step 4: Present Findings to User

Provide a concise summary:
- Total issue count by severity (Critical / Major / Minor)
- Top 5 prioritized findings
- Overall WBS readiness assessment
- Link to annotated Excel and full report

## Output Format

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
**Requirements:** requirements.md

## Executive Summary

- **Critical Issues:** N
- **Major Issues:** N
- **Minor Issues:** N
- **Overall Readiness:** [Ready / Needs Revision / Incomplete]

## Top Priority Findings

### [CRITICAL-001] Missing Acceptance Criteria for Phase 2
**Location:** Row 45, Task "User Acceptance Testing"
**Issue:** No acceptance criteria defined despite requirement REQ-012
**Recommendation:** Add explicit UAT pass/fail criteria based on REQ-012

...

## Requirements Coverage Analysis

| Requirement ID | Requirement Name | Mapped Tasks | Status |
|----------------|------------------|--------------|--------|
| REQ-001 | User Authentication | Task 1.2.1, 1.2.3 | ✓ Covered |
| REQ-005 | Data Migration | (none) | ✗ Missing |

## Missing Task Candidates

1. **Data migration validation** (from REQ-005)
2. **Security audit milestone** (from hearing notes 2025-12-10)
```

### JSON Gap Analysis

```json
{
  "schema_version": "1.0",
  "review_timestamp": "2026-03-19T08:00:00Z",
  "wbs_file": "wbs.xlsx",
  "summary": {
    "total_tasks": 120,
    "critical_issues": 3,
    "major_issues": 8,
    "minor_issues": 15,
    "readiness_score": 75
  },
  "findings": [
    {
      "id": "CRITICAL-001",
      "severity": "critical",
      "category": "missing_acceptance_criteria",
      "location": "Row 45, Column E",
      "task_name": "User Acceptance Testing",
      "issue": "No acceptance criteria defined",
      "requirement_ref": "REQ-012",
      "recommendation": "Add explicit UAT pass/fail criteria"
    }
  ],
  "traceability_matrix": [
    {
      "requirement_id": "REQ-001",
      "requirement_name": "User Authentication",
      "mapped_tasks": ["1.2.1", "1.2.3"],
      "coverage_status": "covered"
    }
  ],
  "missing_tasks": [
    {
      "source": "REQ-005",
      "suggested_task": "Data migration validation",
      "priority": "high"
    }
  ]
}
```

## Resources

- `scripts/wbs_reviewer.py` -- Main WBS review engine with gap analysis logic
- `scripts/excel_annotator.py` -- Excel comment injection and formatting utilities
- `scripts/requirements_parser.py` -- Extract requirements from various document formats
- `references/review_checklist.yaml` -- Default WBS review criteria and validation rules
- `references/wbs_review_methodology.md` -- Review principles and best practices
- `references/common_wbs_issues.md` -- Pattern library of frequent WBS problems
- `assets/review_template.xlsx` -- Template for "Review Summary" sheet structure

## Key Principles

1. **Non-Destructive Review** - Never modify original WBS structure; only add comments and formatting
2. **Requirement Traceability** - Every requirement must map to at least one WBS task
3. **Evidence-Based Findings** - All issues must reference specific requirement IDs or hearing notes
4. **Prioritized Actionability** - Findings sorted by severity and impact on project success
5. **Bilingual Support** - Handle Japanese and English WBS/requirements seamlessly
