---
name: project-completeness-scorer
description: Evaluate project deliverables (code, docs, config) and calculate a 0-100 completeness score with weighted criteria and prioritized action items. Use when assessing project readiness, reviewing milestones, or identifying gaps before release.
---

# Project Completeness Scorer

## Overview

This skill systematically evaluates project deliverables across multiple dimensions (functional requirements, quality standards, test coverage, documentation, deployment readiness) and produces a weighted 0-100 completeness score. It identifies gaps, ranks missing items by priority, and provides actionable next steps to reach completion.

## When to Use

- Assessing a project's readiness for release or handoff
- Reviewing milestone deliverables against acceptance criteria
- Identifying gaps in code, documentation, or configuration
- Comparing actual progress against a project checklist
- Preparing for stakeholder reviews or gate approvals
- Scoring skill development projects within this repository

## Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (json, pathlib, argparse)

## Workflow

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
2. **Quality Standards** -- Code quality, linting, formatting
3. **Test Coverage** -- Unit tests, integration tests, test results
4. **Documentation** -- README, API docs, user guides
5. **Deployment Readiness** -- Config files, CI/CD, environment setup

```bash
python3 scripts/score_project.py \
  --template skill \
  --project-path ./skills/my-skill \
  --verbose
```

### Step 3: Evaluate Each Dimension

For each evaluation dimension, check criteria against the project inventory:

1. Read `references/scoring-methodology.md` for detailed scoring rules
2. Apply dimension weights from the template
3. Calculate raw scores (0-100) per dimension
4. Compute weighted total score

### Step 4: Identify Gaps and Prioritize Actions

For each unmet criterion:

1. Classify severity (Critical / Major / Minor)
2. Estimate effort (Low / Medium / High)
3. Prioritize by impact-to-effort ratio
4. Generate actionable next steps

### Step 5: Generate Report

Produce a comprehensive report in both JSON and Markdown formats.

```bash
python3 scripts/score_project.py \
  --template skill \
  --project-path ./skills/my-skill \
  --output-dir ./reports \
  --format both
```

## Output Format

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
      ]
    }
  ],
  "gaps": [
    {
      "criterion": "At least 3 tests",
      "dimension": "Test Coverage",
      "severity": "major",
      "effort": "medium",
      "priority": 1,
      "action": "Add unit tests covering core scoring logic"
    }
  ],
  "summary": {
    "critical_gaps": 0,
    "major_gaps": 1,
    "minor_gaps": 2,
    "ready_for_release": false
  }
}
```

### Markdown Report

```markdown
# Project Completeness Report

**Project**: ./skills/my-skill
**Type**: skill
**Date**: 2026-03-16
**Overall Score**: 85/100

## Score Breakdown

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Functional Requirements | 30% | 90 | 27.0 |
| Quality Standards | 20% | 80 | 16.0 |
| Test Coverage | 25% | 70 | 17.5 |
| Documentation | 15% | 95 | 14.3 |
| Deployment Readiness | 10% | 100 | 10.0 |

## Priority Actions

1. **[Major]** Add unit tests covering core scoring logic
2. **[Minor]** Add inline code comments
3. **[Minor]** Create CHANGELOG.md

## Readiness Assessment

- Critical Gaps: 0
- Major Gaps: 1
- Minor Gaps: 2
- **Ready for Release**: No (resolve major gaps first)
```

## Resources

- `scripts/score_project.py` -- Main scoring script with CLI interface
- `references/scoring-methodology.md` -- Detailed scoring rules and dimension definitions
- `references/project-templates.md` -- Evaluation templates for different project types

## Key Principles

1. **Weighted Scoring** -- Different dimensions have different importance based on project type
2. **Actionable Gaps** -- Every gap includes a specific action to resolve it
3. **Priority Ranking** -- Gaps are ranked by impact-to-effort ratio
4. **Template-Driven** -- Flexible templates for different project types
5. **Reproducible** -- Same inputs always produce same scores
