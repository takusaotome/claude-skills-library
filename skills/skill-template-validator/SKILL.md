---
name: skill-template-validator
description: Validate Claude skill templates against standard structure (SKILL.md, scripts/, references/, assets/), check for incorrect path references, missing frontmatter fields, and template inheritance issues. Use when creating, reviewing, or debugging skills.
---

# Skill Template Validator

## Overview

Validates Claude skill directories against the standard structure and best practices. Detects structural issues (missing directories, incorrect paths), metadata problems (missing or invalid frontmatter fields), and quality concerns (missing tests, hardcoded paths). Provides actionable fix suggestions with severity levels.

## When to Use

- After creating a new skill to verify it meets quality standards
- Before packaging a skill for distribution
- When debugging why a skill isn't being triggered correctly
- During skill review to identify improvement areas
- When migrating or updating existing skills to the latest conventions

## Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (pathlib, yaml, re, json)

## Workflow

### Step 1: Run Full Validation

Execute the validator against a skill directory to check all categories:

```bash
python3 scripts/validate_skill.py /path/to/skill-name
```

### Step 2: Review Validation Report

The script outputs a structured report with:
- Overall pass/fail status
- Severity-ranked issues (error, warning, info)
- Specific file and line references where applicable
- Actionable fix suggestions for each issue

### Step 3: Address Critical Issues First

Focus on errors (blocking issues) before warnings:

1. **Structure errors**: Missing SKILL.md, incorrect directory names
2. **Frontmatter errors**: Missing `name:` or `description:` fields
3. **Path errors**: Hardcoded absolute paths, incorrect resource references

### Step 4: Run Targeted Checks (Optional)

Run specific validation categories:

```bash
# Structure only
python3 scripts/validate_skill.py /path/to/skill-name --check structure

# Frontmatter only
python3 scripts/validate_skill.py /path/to/skill-name --check frontmatter

# Paths only
python3 scripts/validate_skill.py /path/to/skill-name --check paths
```

### Step 5: Generate JSON Report (Optional)

Output machine-readable JSON for CI/CD integration:

```bash
python3 scripts/validate_skill.py /path/to/skill-name --format json > validation-report.json
```

## Output Format

### Console Report (Default)

```
=== Skill Template Validation Report ===
Skill: skill-name
Path: /path/to/skill-name
Timestamp: 2025-01-15T10:30:00Z

STRUCTURE CHECK
  [PASS] SKILL.md exists
  [PASS] scripts/ directory exists
  [WARN] assets/ directory is empty

FRONTMATTER CHECK
  [PASS] name field matches directory name
  [PASS] description field present
  [ERROR] description is too short (< 20 chars)

PATH CHECK
  [ERROR] Hardcoded absolute path in SKILL.md line 45
  [WARN] Reference to non-existent file: references/missing.md

SUMMARY
  Errors: 2
  Warnings: 2
  Info: 0
  Status: FAIL
```

### JSON Report

```json
{
  "schema_version": "1.0",
  "skill_name": "skill-name",
  "skill_path": "/path/to/skill-name",
  "timestamp": "2025-01-15T10:30:00Z",
  "checks": {
    "structure": {
      "passed": true,
      "issues": []
    },
    "frontmatter": {
      "passed": false,
      "issues": [
        {
          "severity": "error",
          "code": "FRONT001",
          "message": "description is too short (< 20 chars)",
          "file": "SKILL.md",
          "line": 3,
          "suggestion": "Expand description to clearly explain when the skill should be triggered"
        }
      ]
    },
    "paths": {
      "passed": false,
      "issues": [...]
    }
  },
  "summary": {
    "total_errors": 2,
    "total_warnings": 2,
    "total_info": 0,
    "status": "FAIL"
  }
}
```

## Validation Categories

### 1. Structure Validation

Checks the skill directory layout:

| Check | Severity | Description |
|-------|----------|-------------|
| SKILL.md exists | Error | Required skill definition file |
| Directory name valid | Error | Must be lowercase, hyphen-separated |
| scripts/ exists | Warning | Expected for executable skills |
| references/ exists | Warning | Expected for documentation |
| tests/ exists | Warning | Expected in scripts/ directory |
| No unexpected files | Info | Flags non-standard files |

### 2. Frontmatter Validation

Checks YAML frontmatter in SKILL.md:

| Check | Severity | Description |
|-------|----------|-------------|
| Frontmatter present | Error | Must start with `---` |
| Frontmatter is first | Error | No content before frontmatter |
| name field present | Error | Required field |
| name matches directory | Error | Must match exactly |
| description present | Error | Required field |
| description length | Warning | Should be 20-200 chars |

### 3. Path Validation

Checks for path-related issues:

| Check | Severity | Description |
|-------|----------|-------------|
| No hardcoded absolute paths | Error | Use relative paths |
| No username in paths | Error | Avoid /Users/name/... |
| Resource references valid | Warning | Check files exist |
| Relative paths correct | Warning | Verify path format |

### 4. Content Quality Validation

Checks SKILL.md content quality:

| Check | Severity | Description |
|-------|----------|-------------|
| Overview section present | Warning | Should have Overview |
| When to Use section present | Warning | Should have trigger conditions |
| Workflow section present | Warning | Should have steps |
| Imperative verbs used | Info | Steps should use imperative form |

## Resources

- `scripts/validate_skill.py` -- Main validation script
- `references/validation-rules.md` -- Detailed validation rules and error codes

## Key Principles

1. **Fail Fast**: Report critical errors immediately with clear messages
2. **Actionable Feedback**: Every issue includes a specific fix suggestion
3. **Severity Levels**: Distinguish blocking errors from improvement suggestions
4. **Extensible**: Easy to add new validation rules
5. **CI-Friendly**: JSON output for automated pipelines
