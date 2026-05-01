---
name: meeting-minutes-reviewer
description: Review meeting minutes documents for completeness, action item clarity, decision documentation, and consistency with source materials like hearing sheets. Use when validating meeting minutes quality or preparing minutes for distribution.
---

# Meeting Minutes Reviewer

## Overview

Review meeting minutes documents to ensure they meet quality standards for completeness, clarity, and traceability. Validate that all decisions are properly documented, action items have clear owners and deadlines, and content aligns with source materials such as hearing sheets or project artifacts.

## When to Use

- After drafting meeting minutes and before distribution
- When reviewing minutes created by others for quality assurance
- When validating that minutes accurately reflect source materials (hearing sheets, transcripts)
- When ensuring action items meet trackability standards
- When preparing minutes for formal project documentation or audit trails

## Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (json, re, pathlib)

## Workflow

### Step 1: Gather Input Documents

Collect the meeting minutes document and any source materials:

1. **Meeting minutes file** (Markdown or plain text)
2. **Source materials** (optional):
   - Hearing sheet or agenda
   - Transcript or notes
   - Related project artifacts

### Step 2: Run Automated Analysis

Execute the review script to analyze the minutes:

```bash
python3 scripts/review_minutes.py \
  --minutes path/to/minutes.md \
  --hearing-sheet path/to/hearing_sheet.md \
  --output review_report.json
```

Parameters:
- `--minutes`: Path to the meeting minutes file (required)
- `--hearing-sheet`: Path to source hearing sheet for consistency check (optional)
- `--output`: Output path for JSON report (default: stdout)
- `--format`: Output format: `json` or `markdown` (default: json)

### Step 3: Review Quality Scores

Examine the quality scores across 5 dimensions:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 25% | Required sections present and populated |
| Action Items | 25% | All items have owner, deadline, description |
| Decisions | 20% | Decisions documented with context and rationale |
| Consistency | 15% | Alignment with source materials |
| Clarity | 15% | Clear language, no ambiguity |

### Step 4: Address Findings

Review the specific findings and recommendations:

1. **Critical Issues** — Must fix before distribution
2. **Warnings** — Should fix for quality
3. **Suggestions** — Nice-to-have improvements

### Step 5: Generate Feedback Report

Create a structured feedback document for minutes authors:

```bash
python3 scripts/review_minutes.py \
  --minutes path/to/minutes.md \
  --format markdown \
  --output feedback_report.md
```

## Output Format

### JSON Report

```json
{
  "schema_version": "1.0",
  "review_timestamp": "2025-01-15T10:30:00Z",
  "minutes_file": "path/to/minutes.md",
  "source_files": ["path/to/hearing_sheet.md"],
  "overall_score": 85,
  "dimension_scores": {
    "completeness": 90,
    "action_items": 80,
    "decisions": 85,
    "consistency": 85,
    "clarity": 85
  },
  "findings": [
    {
      "severity": "critical",
      "dimension": "action_items",
      "location": "line 45",
      "issue": "Action item missing deadline",
      "suggestion": "Add specific deadline date"
    }
  ],
  "summary": {
    "critical_count": 1,
    "warning_count": 3,
    "suggestion_count": 5
  }
}
```

### Markdown Report

```markdown
# Meeting Minutes Review Report

**File**: minutes.md
**Review Date**: 2025-01-15

## Overall Score: 85/100

| Dimension | Score | Status |
|-----------|-------|--------|
| Completeness | 90 | ✅ Good |
| Action Items | 80 | ⚠️ Needs Work |
| Decisions | 85 | ✅ Good |
| Consistency | 85 | ✅ Good |
| Clarity | 85 | ✅ Good |

## Critical Issues (1)

### Action item missing deadline
- **Location**: Line 45
- **Issue**: Action item lacks a specific deadline
- **Suggestion**: Add deadline in format "Due: YYYY-MM-DD"

## Warnings (3)
...

## Suggestions (5)
...
```

## Resources

- `scripts/review_minutes.py` — Main review script with quality analysis
- `references/review-criteria.md` — Detailed scoring criteria and quality standards
- `references/meeting-minutes-checklist.md` — Complete checklist for meeting minutes

## Key Principles

1. **Actionability** — Every action item must have an owner, deadline, and clear description
2. **Traceability** — Decisions should link back to discussion context
3. **Completeness** — All required sections present with meaningful content
4. **Consistency** — Content aligns with source materials and project terminology
5. **Clarity** — No ambiguous language; concrete over vague
