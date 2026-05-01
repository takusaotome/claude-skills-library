---
name: marp-layout-debugger
description: Diagnose and fix MARP slide layout issues including whitespace problems, box alignment, bullet formatting, and CSS rendering inconsistencies. Use when MARP slides have visual layout problems or need CSS optimization.
---

# MARP Layout Debugger

## Overview

Diagnoses and fixes common MARP slide layout issues including whitespace problems, box alignment, bullet formatting inconsistencies, and responsive design issues. Provides visual diff comparisons and automated CSS fixes for common rendering problems. Outputs actionable fix recommendations with before/after comparisons.

## When to Use

- MARP slides have unexpected whitespace or spacing issues
- Box elements are misaligned or overlap incorrectly
- Bullet points have inconsistent indentation or formatting
- Content overflows slide boundaries
- CSS styles render differently than expected
- Need to validate MARP CSS against best practices
- Converting presentations and encountering layout problems

## Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: `pyyaml` (for frontmatter parsing), `re` (standard library)

## Workflow

### Step 1: Analyze MARP File for Issues

Parse the MARP markdown file and detect layout issues across multiple categories.

```bash
python3 scripts/analyze_marp_layout.py \
  --input path/to/slides.md \
  --output analysis_report.json
```

The analyzer checks for:
- Whitespace anomalies (double blank lines, trailing spaces, inconsistent indentation)
- Box alignment issues (flexbox misuse, margin/padding conflicts)
- Bullet formatting (mixed list styles, incorrect nesting)
- Overflow risks (long code blocks, wide tables, oversized images)
- CSS specificity conflicts and redundant rules

### Step 2: Review Issue Report

Read the generated JSON report to understand detected issues.

```json
{
  "file": "slides.md",
  "timestamp": "2026-04-03T08:00:00Z",
  "total_issues": 12,
  "issues_by_category": {
    "whitespace": 3,
    "alignment": 4,
    "bullets": 2,
    "overflow": 2,
    "css": 1
  },
  "issues": [
    {
      "id": "WS001",
      "category": "whitespace",
      "severity": "medium",
      "line": 45,
      "description": "Double blank line creates excessive gap",
      "suggestion": "Remove one blank line",
      "auto_fixable": true
    }
  ]
}
```

### Step 3: Apply Automatic Fixes

Apply auto-fixable issues to generate a corrected MARP file.

```bash
python3 scripts/fix_marp_layout.py \
  --input path/to/slides.md \
  --report analysis_report.json \
  --output fixed_slides.md \
  --auto-only
```

### Step 4: Generate Visual Diff Report

Create a side-by-side comparison showing original vs. fixed content.

```bash
python3 scripts/generate_diff_report.py \
  --original path/to/slides.md \
  --fixed fixed_slides.md \
  --output diff_report.md
```

### Step 5: Manual Review and Additional Fixes

For non-auto-fixable issues, apply manual fixes based on the recommendations in the analysis report. Common manual interventions include:
- Restructuring complex flexbox layouts
- Adjusting custom CSS for specific viewport sizes
- Refactoring deeply nested bullet structures

## Output Format

### JSON Analysis Report

```json
{
  "schema_version": "1.0",
  "file": "slides.md",
  "timestamp": "2026-04-03T08:00:00Z",
  "total_issues": 12,
  "auto_fixable_count": 8,
  "manual_review_count": 4,
  "issues_by_category": {
    "whitespace": 3,
    "alignment": 4,
    "bullets": 2,
    "overflow": 2,
    "css": 1
  },
  "issues": [
    {
      "id": "WS001",
      "category": "whitespace",
      "severity": "low|medium|high",
      "line": 45,
      "column": 0,
      "description": "Description of the issue",
      "suggestion": "How to fix it",
      "auto_fixable": true,
      "context": "surrounding code snippet"
    }
  ],
  "css_analysis": {
    "total_rules": 25,
    "redundant_rules": 2,
    "specificity_warnings": 1
  }
}
```

### Markdown Diff Report

```markdown
# MARP Layout Diff Report

## Summary
- **Original file**: slides.md
- **Fixed file**: fixed_slides.md
- **Issues fixed**: 8
- **Issues remaining**: 4

## Changes by Category

### Whitespace Fixes
| Line | Original | Fixed |
|------|----------|-------|
| 45   | `\n\n\n` | `\n\n` |

### Alignment Fixes
...

## Remaining Manual Issues
1. **Line 78**: Complex flexbox layout needs restructuring
   - Suggestion: Simplify to single-direction flex container
```

## Resources

- `scripts/analyze_marp_layout.py` -- Main analysis engine detecting layout issues
- `scripts/fix_marp_layout.py` -- Automated fix application
- `scripts/generate_diff_report.py` -- Visual diff report generator
- `references/marp-layout-patterns.md` -- Common MARP layout patterns and anti-patterns
- `references/css-fix-catalog.md` -- Catalog of CSS fixes for common issues

## Key Principles

1. **Non-destructive analysis** -- Never modify original files without explicit confirmation
2. **Severity-based prioritization** -- High severity issues (overflow, broken layouts) first
3. **Auto-fix safety** -- Only automatically fix issues with no risk of semantic changes
4. **Preserve author intent** -- Fixes should maintain the original visual intent
5. **Comprehensive reporting** -- Always provide context and reasoning for each fix

## Issue Categories

### Whitespace Issues (WS)
- WS001: Double or triple blank lines
- WS002: Trailing whitespace on lines
- WS003: Inconsistent indentation (tabs vs spaces)
- WS004: Missing blank line before/after headers

### Alignment Issues (AL)
- AL001: Flexbox direction mismatch
- AL002: Margin collapse causing unexpected gaps
- AL003: Absolute positioning overflow
- AL004: Grid alignment inconsistency

### Bullet Issues (BL)
- BL001: Mixed list markers (- and * in same list)
- BL002: Incorrect nesting level
- BL003: Missing space after marker
- BL004: Inconsistent nested indentation

### Overflow Issues (OF)
- OF001: Code block exceeds slide width
- OF002: Image dimensions exceed container
- OF003: Table width overflow
- OF004: Long URLs break layout

### CSS Issues (CS)
- CS001: Redundant rule (overridden elsewhere)
- CS002: High specificity causing cascade problems
- CS003: !important overuse
- CS004: Missing vendor prefixes for older browsers
