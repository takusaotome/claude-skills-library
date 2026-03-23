# Static Rule Candidate Specification

Use this template to specify a candidate static analysis rule before implementation. Each rule candidate should be evaluated for feasibility, false positive risk, and rollout strategy before development begins.

---

## Template

| Field | Value |
|-------|-------|
| **Rule ID** | `SBD-[L/S/R]XX` (L=Lint, S=Semgrep, R=Regex) |
| **Rule Name** | [Short descriptive name] |
| **Target Language(s)** | [Python, JavaScript, TypeScript, Java, Go, etc.] |
| **Detection Idea** | [How does the rule detect violations? Describe the pattern matching approach.] |
| **Detection Tool** | [Lint (ESLint/Ruff/RuboCop), Semgrep, Regex (pre-commit), Custom AST checker] |
| **Pattern (Positive Match)** | [Code patterns that SHOULD trigger the rule (true positives)] |
| **Pattern (Negative Match)** | [Code patterns that should NOT trigger the rule (true negatives)] |
| **False Positive Risk** | [Low / Medium / High. Describe known FP scenarios.] |
| **False Positive Mitigation** | [How to reduce FPs: scope limits, allowlists, context checks] |
| **Suggested Severity** | [ERROR / WARNING / INFO] |
| **Autofix Available** | [Yes / No. If yes, describe the automatic fix.] |
| **Suppression Syntax** | [How developers suppress the rule with justification] |
| **Related Forbidden Pattern** | [Link to `forbidden_patterns.md` entry, e.g., FP-01] |
| **Related Safe Pattern** | [Link to `safe_pattern_catalog.md` section] |
| **Rollout Plan** | [Phased rollout timeline: INFO -> WARNING -> ERROR] |
| **Estimated FP Rate** | [After codebase scan: TP count, FP count, FP%] |

---

## Filled Example: Ban Naive datetime.now()

| Field | Value |
|-------|-------|
| **Rule ID** | `SBD-L01` |
| **Rule Name** | Ban naive datetime creation |
| **Target Language(s)** | Python |
| **Detection Idea** | Detect calls to `datetime.now()` without a `tz` argument and all calls to `datetime.utcnow()`. Both return naive datetime objects that cause silent comparison failures and timezone bugs. |
| **Detection Tool** | Lint (Ruff custom rule or flake8 plugin) |
| **Pattern (Positive Match)** | `datetime.now()`, `datetime.utcnow()`, `dt.datetime.now()`, `from datetime import datetime; datetime.now()` |
| **Pattern (Negative Match)** | `datetime.now(timezone.utc)`, `datetime.now(tz=ZoneInfo("UTC"))`, `clock.now()` |
| **False Positive Risk** | Low. `datetime.now()` without timezone is almost never intentional in application code. |
| **False Positive Mitigation** | Exclude test files that deliberately test naive datetime handling. Exclude CLI-only scripts via directory filter. |
| **Suggested Severity** | ERROR (for application code), WARNING (for test code) |
| **Autofix Available** | Yes: `datetime.now()` -> `datetime.now(timezone.utc)`, `datetime.utcnow()` -> `datetime.now(timezone.utc)`. Adds `from datetime import timezone` if missing. |
| **Suppression Syntax** | `# noqa: SBD-L01 -- [justification required]` |
| **Related Forbidden Pattern** | FP-05: Mixed Naive and Aware DateTime Objects |
| **Related Safe Pattern** | Safe Pattern Catalog: Section 6 (DateTime Normalization) |
| **Rollout Plan** | Week 1-2: INFO on all files. Week 3-4: WARNING on application code. Week 5+: ERROR on application code. Legacy violations: fix within one sprint. |
| **Estimated FP Rate** | Codebase scan: 47 matches total, 44 TP, 3 FP (test fixtures) = 6.4% FP rate. Acceptable. |

---

## Filled Example: Detect Missing Auth Decorator

| Field | Value |
|-------|-------|
| **Rule ID** | `SBD-S02` |
| **Rule Name** | Require authorization on route handlers |
| **Target Language(s)** | Python (Flask, Django, FastAPI) |
| **Detection Idea** | Find functions decorated with `@app.route`, `@router.get/post`, or `@api_view` that do NOT also have `@require_permission`, `@require_role`, or `@public` decorator. |
| **Detection Tool** | Semgrep |
| **Pattern (Positive Match)** | `@app.route("/path") def handler(): ...` without auth decorator. `@router.post("/path") async def handler(): ...` without auth decorator. |
| **Pattern (Negative Match)** | `@app.route("/path") @require_permission("scope") def handler(): ...`. `@app.route("/health") @public def health(): ...`. |
| **False Positive Risk** | Medium. Framework-specific decorators may use non-standard names. Test route definitions in test files may trigger. |
| **False Positive Mitigation** | Configure decorator name allowlist per framework. Exclude test directories. Exclude API documentation generators. |
| **Suggested Severity** | ERROR |
| **Autofix Available** | No. The correct permission cannot be inferred automatically. Rule reports the violation; developer must add the appropriate decorator. |
| **Suppression Syntax** | `# nosemgrep: sbd-s02-missing-auth -- [justification required]` |
| **Related Forbidden Pattern** | FP-02: Opt-In Authorization |
| **Related Safe Pattern** | Safe Pattern Catalog: Section 2 (Authorization) |
| **Rollout Plan** | Week 1-2: Run against codebase, catalog all existing violations. Week 3-4: WARNING on new code only (diff-based). Week 5-6: ERROR on new code. Week 7+: ERROR on all code with violation backlog tracked. |
| **Estimated FP Rate** | Codebase scan: 23 matches total, 19 TP (genuinely missing auth), 4 FP (test routes, admin CLI) = 17.4% FP rate. Add test/CLI exclusion to bring below 10%. |

---

## Filled Example: SQL Concatenation Detection

| Field | Value |
|-------|-------|
| **Rule ID** | `SBD-S01` |
| **Rule Name** | Ban SQL string concatenation |
| **Target Language(s)** | Python, JavaScript, TypeScript |
| **Detection Idea** | Detect string operations (concatenation, f-strings, format, template literals) that produce strings containing SQL keywords (SELECT, INSERT, UPDATE, DELETE, FROM, WHERE) combined with variable interpolation. |
| **Detection Tool** | Semgrep (pattern + taint mode) |
| **Pattern (Positive Match)** | `f"SELECT * FROM users WHERE id = {uid}"`, `"SELECT * FROM " + table + " WHERE id = " + id`, `query = "DELETE FROM users WHERE id = %d" % uid` |
| **Pattern (Negative Match)** | `cursor.execute("SELECT * FROM users WHERE id = %s", [uid])`, `User.objects.filter(id=uid)`, `"SELECT * FROM users"` (no variable interpolation) |
| **False Positive Risk** | Low to Medium. May match SQL-like strings in logging, comments, or documentation generators. |
| **False Positive Mitigation** | Require both SQL keyword presence AND variable interpolation. Exclude docstring and comment contexts (semgrep AST awareness). Exclude migration files. |
| **Suggested Severity** | ERROR |
| **Autofix Available** | Partial. Can suggest the parameterized form but cannot determine parameter binding syntax without knowing the database driver. Provides a comment with the suggested fix. |
| **Suppression Syntax** | `# nosemgrep: sbd-s01-sql-concatenation -- [justification required]` |
| **Related Forbidden Pattern** | FP-01: Raw SQL String Concatenation |
| **Related Safe Pattern** | Safe Pattern Catalog: Section 1 (Query Construction) |
| **Rollout Plan** | Week 1: Run full codebase scan, triage all matches. Week 2: ERROR on new code. Week 3-4: Fix existing violations (expected: 5-15 in a typical codebase). Week 5+: ERROR on all code. |
| **Estimated FP Rate** | Codebase scan: 12 matches total, 11 TP, 1 FP (SQL in log message) = 8.3% FP rate. Acceptable. |

---

## Usage Instructions

1. Create one specification per candidate rule using the template above
2. Run the detection pattern against the existing codebase before committing to implementation
3. Calculate the estimated FP rate; if above 20%, refine the pattern before proceeding
4. Get approval from the team lead before implementing ERROR-level rules
5. Follow the rollout plan strictly; do not skip the WARNING phase
6. After rollout, monitor the rule's suppression rate; if above 15%, review and refine
7. Link completed rule specifications to entries in `assets/forbidden_to_safe_mapping_template.md`
