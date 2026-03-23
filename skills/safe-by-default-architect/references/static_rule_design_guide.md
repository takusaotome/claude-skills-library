# Static Rule Design Guide

This reference provides guidance for designing static analysis rules that enforce safe-by-default standards. Good static rules catch violations early in the development cycle with minimal false positives, while bad rules annoy developers and get disabled.

**Design Principle**: A static rule that gets disabled due to false positives provides zero protection. Optimize for precision (low false positive rate) over recall (catching every possible violation).

---

## 1. Rule Classification by Tool Suitability

Different enforcement tools have different strengths. Choose the right tool for each rule.

### Lint-Suitable Rules

Lint tools (ESLint, Pylint, Ruff, RuboCop, etc.) operate on the AST (Abstract Syntax Tree) of a single file. They are best for:

- **Function/method call restrictions**: Detecting calls to forbidden functions
- **Import restrictions**: Preventing import of banned modules
- **Naming conventions**: Enforcing naming patterns that encode safety information
- **Complexity limits**: Detecting overly complex code that is likely to contain errors
- **Type annotation enforcement**: Requiring type hints on function signatures

**Examples of lint-suitable rules**:

| Rule ID | Description | Detection Method |
|---------|-------------|-----------------|
| SBD-L01 | Ban `datetime.now()` without timezone | AST: detect `datetime.now()` calls missing `tz` argument |
| SBD-L02 | Ban `datetime.utcnow()` | AST: detect calls to `utcnow()` method |
| SBD-L03 | Require type annotations on public functions | AST: check function signatures for missing annotations |
| SBD-L04 | Ban bare `except:` or `except Exception:` without re-raise | AST: detect except handlers that do not re-raise |
| SBD-L05 | Ban `os.path.join()` with variable arguments in web handlers | AST: detect `os.path.join` in handler modules |

**Lint rule design pattern**:
```python
# Pseudocode for a custom lint rule
class BanDatetimeNow(LintRule):
    message = "Use datetime.now(timezone.utc) instead of datetime.now()"
    severity = "error"

    def visit_call(self, node):
        if node.func_name == "datetime.now" and not node.has_keyword_arg("tz"):
            self.report(node)
        if node.func_name == "datetime.utcnow":
            self.report(node, message="datetime.utcnow() returns naive datetime. Use datetime.now(timezone.utc)")
```

### Semgrep-Suitable Rules

Semgrep operates on code patterns (structural matching) across files. It is best for:

- **Multi-statement patterns**: Detecting sequences of operations that form an unsafe pattern
- **Taint tracking**: Tracing data flow from untrusted sources to sensitive sinks
- **Framework-specific patterns**: Matching patterns that are idiomatic to specific frameworks
- **Cross-function analysis**: Detecting unsafe patterns that span multiple function calls
- **Autofix generation**: Providing automatic code transformations

**Examples of semgrep-suitable rules**:

| Rule ID | Description | Detection Method |
|---------|-------------|-----------------|
| SBD-S01 | Detect SQL string concatenation | Pattern: `"SELECT" + $USER_INPUT` or f-string with SQL keywords |
| SBD-S02 | Detect missing auth decorator on route handlers | Pattern: route decorator without permission decorator |
| SBD-S03 | Detect success message before await | Pattern: `showToast(...)` followed by `await ...` |
| SBD-S04 | Detect file path construction with user input | Taint: user input flows to `open()` or `Path()` |
| SBD-S05 | Detect global state access in service classes | Pattern: module-level variable access in class methods |

**Semgrep rule design pattern**:
```yaml
rules:
  - id: sbd-s01-sql-concatenation
    patterns:
      - pattern-either:
          - pattern: |
              $QUERY = f"...SELECT...{$VAR}..."
          - pattern: |
              $QUERY = "...SELECT..." + $VAR
          - pattern: |
              $QUERY = "...SELECT..." % $VAR
    message: >
      SQL query constructed via string formatting. Use parameterized queries
      or ORM instead. See: safe_pattern_catalog.md#query-construction
    severity: ERROR
    fix: |
      # Replace with parameterized query:
      # cursor.execute("SELECT ... WHERE col = %s", [$VAR])
    metadata:
      category: security
      references:
        - forbidden_patterns.md#fp-01
```

### Regex-Based Minimum Rules

When lint and semgrep are not available, regex patterns in pre-commit hooks or CI scripts provide minimum protection. Regex rules are imprecise and generate more false positives, but they are better than no enforcement.

**Examples of regex-suitable rules**:

| Rule ID | Pattern | Description | False Positive Risk |
|---------|---------|-------------|---------------------|
| SBD-R01 | `SELECT.*\+.*\$` or `SELECT.*{` | SQL concatenation in Python | Medium: matches comments, string constants |
| SBD-R02 | `datetime\.now\(\s*\)` | Naive datetime.now() call | Low: few legitimate uses |
| SBD-R03 | `except\s*:\s*$` | Bare except clause | Low: clear anti-pattern |
| SBD-R04 | `open\(.*\+` | File open with string concatenation | Medium: matches safe concatenation too |
| SBD-R05 | `\.password\s*=\s*["']` | Hardcoded password | Low: clear anti-pattern |

**Regex rule implementation**:
```bash
#!/bin/bash
# pre-commit hook: minimum safety checks
set -euo pipefail

ERRORS=0

# Check for SQL concatenation
if grep -rn --include="*.py" 'SELECT.*[+%]' --exclude-dir=tests --exclude-dir=migrations; then
    echo "ERROR: Possible SQL concatenation detected. Use parameterized queries."
    ERRORS=$((ERRORS + 1))
fi

# Check for naive datetime
if grep -rn --include="*.py" 'datetime\.now()' --exclude-dir=tests; then
    echo "ERROR: datetime.now() returns naive datetime. Use datetime.now(timezone.utc)."
    ERRORS=$((ERRORS + 1))
fi

exit $ERRORS
```

---

## 2. False Positive Reduction Strategies

False positives are the primary reason static rules get disabled. Invest significant effort in reducing them.

### Strategy 1: Scope Limitation

Limit where the rule applies to reduce false matches:

- **File path filtering**: Only apply the rule to source files, excluding tests, migrations, generated code, and vendored dependencies
- **Function/class filtering**: Only apply to specific module types (e.g., "handlers", "controllers", "services")
- **Language-aware parsing**: Use AST-based detection instead of regex when possible (regex matches inside comments and strings)

### Strategy 2: Allowlist/Suppression Mechanism

Every rule must have a suppression mechanism with mandatory justification:

```python
# Suppress with justification (required format)
cursor.execute(raw_sql)  # noqa: SBD-S01 -- migration script, no user input

# Suppress at file level
# sbd-disable: SBD-S01 -- This file is a database migration script
```

Design rules so that:
- Suppression requires a rule ID (no blanket suppression)
- Suppression requires a justification comment (enforced by the rule itself)
- Suppression comments are auditable (can be collected and reviewed)

### Strategy 3: Contextual Awareness

Reduce false positives by understanding context:

- **Test code exclusion**: Many forbidden patterns are legitimate in test code (e.g., deliberately testing error handling). Exclude test directories or reduce severity to "warning" in tests.
- **Migration exclusion**: Database migrations legitimately use raw SQL. Exclude migration directories.
- **Comment/string awareness**: Regex rules match inside comments and strings. Use AST-based tools when possible.
- **Import tracking**: A `datetime.now()` call is only dangerous when it comes from the `datetime` module, not a custom `datetime` wrapper.

### Strategy 4: Graduated Severity

Not all violations are equal. Use severity levels to prioritize:

| Severity | Meaning | CI Behavior | Response Required |
|----------|---------|-------------|-------------------|
| ERROR | Must fix before merge | Blocks CI pipeline | Immediate fix or approved exception |
| WARNING | Should fix, review required | Does not block CI | Fix in current sprint or justify |
| INFO | Consider fixing | Not shown in CI by default | Track for tech debt review |

New rules should start at WARNING level during a trial period, then be promoted to ERROR after confirming low false positive rates.

---

## 3. Rule Design Process

Follow this process for each new static rule:

### Step 1: Define the Violation

Write a precise description of what constitutes a violation:
- What specific code pattern is forbidden?
- What are the boundary conditions?
- What are known false positive scenarios?

### Step 2: Choose the Detection Tool

Select the most appropriate tool based on the rule classification above:
- Simple function/method bans -> Lint
- Multi-statement patterns or taint tracking -> Semgrep
- Minimum protection when better tools are unavailable -> Regex

### Step 3: Write the Rule

Implement the rule in the chosen tool's format:
- Include a clear error message explaining why the pattern is forbidden
- Include a reference link to the safe alternative documentation
- Include autofix when possible

### Step 4: Test Against Existing Codebase

Before enabling the rule:
1. Run against the full codebase in report-only mode
2. Count violations and categorize them as true positives vs false positives
3. Calculate the false positive rate: `FP / (TP + FP)`
4. Target: FP rate below 10% for ERROR severity, below 20% for WARNING severity
5. If FP rate is too high, refine the rule or reduce scope

### Step 5: Plan Rollout

Design a phased rollout:
1. **Week 1-2**: Rule enabled as INFO, collect feedback
2. **Week 3-4**: Rule promoted to WARNING, developers fix new violations
3. **Week 5+**: Rule promoted to ERROR, blocks CI on violation
4. **Ongoing**: Existing violations tracked as tech debt with migration plan

### Step 6: Monitor and Maintain

After rollout:
- Track violation count over time (should trend toward zero)
- Track suppression count (increasing suppressions may indicate rule needs refinement)
- Track false positive reports from developers
- Review and update the rule quarterly

---

## 4. Rule Documentation Standard

Every static rule must be documented with the following fields:

| Field | Description | Example |
|-------|-------------|---------|
| Rule ID | Unique identifier | SBD-L01 |
| Tool | Detection tool | Ruff, Semgrep, pre-commit |
| Severity | ERROR / WARNING / INFO | ERROR |
| Category | Security, reliability, maintainability | Security |
| Description | What the rule detects | Naive datetime.now() call without timezone argument |
| Rationale | Why this is dangerous | Link to forbidden_patterns.md |
| Safe Alternative | What to do instead | Link to safe_pattern_catalog.md |
| False Positive Scenarios | Known FP cases | Test files, fixture generators |
| Suppression | How to suppress | `# noqa: SBD-L01 -- justification` |
| Autofix | Whether autofix is available | Yes: replaces with `datetime.now(timezone.utc)` |
| Rollout Status | Current rollout phase | ERROR since 2024-Q2 |

---

## 5. Recommended Starter Rule Set

For teams starting from zero, implement these five rules first (highest impact, lowest false positive rate):

| Priority | Rule | Tool | FP Risk | Impact |
|----------|------|------|---------|--------|
| 1 | Ban SQL string concatenation | Semgrep | Low | Prevents SQL injection |
| 2 | Ban bare except/catch-all | Lint | Low | Prevents silent corruption |
| 3 | Ban naive datetime creation | Lint | Low | Prevents timezone bugs |
| 4 | Require auth decorator on routes | Semgrep | Medium | Prevents auth bypass |
| 5 | Ban direct file path construction in handlers | Semgrep | Medium | Prevents path traversal |

This starter set covers the five most common categories of recurring defects while maintaining a manageable false positive rate. Add rules incrementally based on defect data.
