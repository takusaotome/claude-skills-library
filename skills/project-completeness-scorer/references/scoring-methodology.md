# Scoring Methodology

This document defines the detailed scoring rules, dimension definitions, and weighting system for project completeness evaluation.

## Scoring Philosophy

The project completeness score reflects how well a project meets its intended deliverables across multiple dimensions. A score of 100 indicates all criteria are fully met; 0 indicates no criteria are met.

### Score Interpretation

| Score Range | Status | Meaning |
|-------------|--------|---------|
| 90-100 | Production-Ready | All critical and major criteria met; minor polish only |
| 80-89 | Release-Ready | Ready with known minor gaps; acceptable for release |
| 70-79 | Near-Complete | Major work done; some gaps require attention |
| 60-69 | In-Progress | Core functionality present; significant gaps remain |
| 40-59 | Early Stage | Partial implementation; substantial work needed |
| 0-39 | Initial | Minimal progress; mostly placeholder or scaffold |

## Evaluation Dimensions

### 1. Functional Requirements (Default Weight: 30%)

Measures whether the core deliverables and features exist and are complete.

**Criteria Examples:**
- Core files/modules exist
- Required functionality implemented
- API endpoints working
- User flows complete
- Integration points functional

**Scoring Rules:**
- Each criterion is binary (met/not met) or percentage-based
- Critical criteria missing = max 60% on dimension
- All criteria met = 100%

### 2. Quality Standards (Default Weight: 20%)

Measures code quality, maintainability, and adherence to best practices.

**Criteria Examples:**
- Linting passes (no errors)
- Consistent code formatting
- No hardcoded secrets
- Error handling present
- Logging implemented
- Type hints used (where applicable)

**Scoring Rules:**
- Each quality criterion is scored 0-100%
- Dimension score = average of all criteria
- Critical violations (secrets, security) cap score at 50%

### 3. Test Coverage (Default Weight: 25%)

Measures test presence, coverage, and test health.

**Criteria Examples:**
- Test directory exists
- Test configuration present (pytest.ini, conftest.py)
- Minimum number of test files
- Tests pass successfully
- Coverage percentage (if measurable)
- Edge cases covered

**Scoring Rules:**
- No tests = 0%
- Tests exist but fail = max 40%
- Tests pass, low coverage = 50-70%
- Tests pass, good coverage = 70-90%
- Tests pass, excellent coverage + edge cases = 90-100%

### 4. Documentation (Default Weight: 15%)

Measures documentation completeness and quality.

**Criteria Examples:**
- README exists and is substantive
- API documentation present
- Inline code comments
- Usage examples
- Configuration documentation
- CHANGELOG/version history

**Scoring Rules:**
- No README = max 30%
- README exists, minimal content = 40-60%
- README complete, no API docs = 60-80%
- Full documentation suite = 80-100%

### 5. Deployment Readiness (Default Weight: 10%)

Measures readiness for deployment, distribution, or handoff.

**Criteria Examples:**
- Configuration files present
- Environment setup documented
- CI/CD pipeline configured
- Build scripts working
- Package manifest (pyproject.toml, package.json)
- License file present

**Scoring Rules:**
- No deployment config = 0-30%
- Partial config = 30-60%
- Config present, not tested = 60-80%
- Full deployment readiness = 80-100%

## Weighted Score Calculation

```
overall_score = sum(dimension_score * dimension_weight) for all dimensions
```

Example:
```
Functional: 90 * 0.30 = 27.0
Quality:    80 * 0.20 = 16.0
Testing:    70 * 0.25 = 17.5
Docs:       95 * 0.15 = 14.25
Deploy:    100 * 0.10 = 10.0
----------------------------
Total:              = 84.75 → 85
```

## Gap Classification

### Severity Levels

| Severity | Definition | Score Impact |
|----------|------------|--------------|
| Critical | Blocks release or represents security risk | Caps dimension at 60% |
| Major | Significant functionality or quality gap | -10 to -20 points |
| Minor | Polish items, nice-to-have | -1 to -5 points |

### Effort Levels

| Effort | Definition | Time Estimate |
|--------|------------|---------------|
| Low | Quick fix, simple addition | < 1 hour |
| Medium | Moderate work required | 1-4 hours |
| High | Significant development needed | > 4 hours |

### Priority Calculation

Priority is calculated using an impact-to-effort ratio:

```
impact = severity_weight * dimension_weight * 100
priority_score = impact / effort_multiplier

Severity weights: Critical=3, Major=2, Minor=1
Effort multipliers: Low=1, Medium=2, High=4
```

Higher priority_score = higher priority to address.

## Criterion Types

### Binary Criteria

Simple yes/no check.

```json
{
  "name": "SKILL.md exists",
  "type": "binary",
  "check": "file_exists",
  "path": "SKILL.md",
  "severity": "critical"
}
```

### Count Criteria

Minimum count requirement.

```json
{
  "name": "At least 3 test files",
  "type": "count",
  "check": "file_count",
  "pattern": "scripts/tests/test_*.py",
  "minimum": 3,
  "severity": "major"
}
```

### Percentage Criteria

Percentage-based scoring.

```json
{
  "name": "Test coverage",
  "type": "percentage",
  "check": "coverage_report",
  "thresholds": {
    "excellent": 90,
    "good": 70,
    "acceptable": 50,
    "poor": 30
  },
  "severity": "major"
}
```

### Content Criteria

Check file content for required elements.

```json
{
  "name": "README has usage section",
  "type": "content",
  "check": "contains_heading",
  "file": "README.md",
  "pattern": "## Usage|## How to Use",
  "severity": "minor"
}
```

## Custom Weighting

Users can override default weights via template or CLI:

```bash
python3 scripts/score_project.py \
  --template skill \
  --weights '{"functional": 0.40, "quality": 0.15, "testing": 0.25, "docs": 0.10, "deploy": 0.10}'
```

Weights must sum to 1.0.
