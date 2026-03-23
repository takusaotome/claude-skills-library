# Safe Standard Definition

Use this template to document each safe-by-default standard. One standard per rule. Fill in all fields; leave none blank.

---

## Template

| Field | Value |
|-------|-------|
| **Rule Name** | `SBD-XXX: [Short descriptive name]` |
| **Risk Addressed** | [Which danger category does this rule mitigate? IBT/SC/ED/HD/HEA/UB] |
| **Forbidden Pattern** | [What specific code pattern is prohibited? Include code example.] |
| **Approved Pattern** | [What must developers use instead? Include code example.] |
| **Required Abstraction** | [Which common layer, wrapper, or service enforces this pattern?] |
| **Review Rule** | [What must code reviewers check for during review?] |
| **Test Rule** | [What contract test verifies compliance?] |
| **Exception Process** | [Level 1 (review-required), Level 2 (approval-required), or Level 3 (prohibited). Conditions for exception.] |

---

## Filled Example: Parameterized Query Enforcement

| Field | Value |
|-------|-------|
| **Rule Name** | `SBD-S01: Parameterized queries only` |
| **Risk Addressed** | IBT (Injection / Bypass / Traversal) |
| **Forbidden Pattern** | String concatenation, f-strings, or %-formatting to construct SQL queries. Example: `query = f"SELECT * FROM users WHERE id = {user_id}"` |
| **Approved Pattern** | Parameterized queries via ORM or parameter binding. Example: `cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])` or `User.objects.filter(id=user_id)` |
| **Required Abstraction** | `Repository` layer classes that encapsulate all database queries. No direct `cursor.execute()` calls outside repository modules. |
| **Review Rule** | Reviewer must verify: (1) no SQL string construction in the diff, (2) all new queries go through a repository method, (3) dynamic column/table names use allowlists not parameterization. |
| **Test Rule** | Integration test: attempt SQL injection via parameterized input and verify it is treated as data, not structure. Static test: semgrep rule `sbd-s01-sql-concatenation` must pass. |
| **Exception Process** | Level 2 (approval-required) for raw SQL with parameterized values in reporting queries. Level 3 (prohibited, no exception) for SQL with concatenated user input. ADR required for Level 2. |

---

## Filled Example: Deny-by-Default Authorization

| Field | Value |
|-------|-------|
| **Rule Name** | `SBD-S02: Deny-by-default authorization` |
| **Risk Addressed** | IBT (Injection / Bypass / Traversal), HEA (Human Error Amplification) |
| **Forbidden Pattern** | Route handlers without authorization annotations. Example: `@app.route("/admin/export") def export(): ...` with no `@require_permission` decorator. |
| **Approved Pattern** | Every route handler must have an explicit authorization annotation. Protected: `@require_permission("admin.export")`. Public: `@public` (explicit opt-out). |
| **Required Abstraction** | Global `AuthorizationMiddleware` that rejects requests to handlers missing authorization annotations. `PermissionRegistry` that defines all valid permissions. |
| **Review Rule** | Reviewer must verify: (1) every new route has an authorization annotation, (2) `@public` routes are justified in the PR description, (3) new permissions are registered in the PermissionRegistry. |
| **Test Rule** | Startup test: iterate all registered routes and assert each has an authorization annotation. Integration test: request an endpoint without valid credentials and verify 401/403 response. |
| **Exception Process** | Level 1 (review-required) for `@public` annotation on health check and documentation endpoints. Level 2 (approval-required) for webhook endpoints using alternative authentication (HMAC, IP allowlist). Level 3 (prohibited) for disabling the global middleware. |

---

## Filled Example: UTC-Aware DateTime Normalization

| Field | Value |
|-------|-------|
| **Rule Name** | `SBD-L01: UTC-aware datetime only` |
| **Risk Addressed** | SC (Silent Corruption), ED (Environment Divergence) |
| **Forbidden Pattern** | Naive datetime creation. Examples: `datetime.now()`, `datetime.utcnow()`, `datetime.strptime(s, fmt)` without timezone. |
| **Approved Pattern** | Timezone-aware datetime creation. Examples: `datetime.now(timezone.utc)`, `parse(s)` with timezone, `Clock.now()` abstraction. |
| **Required Abstraction** | `Clock` protocol/interface injected into services. Database columns use `TIMESTAMP WITH TIME ZONE`. Serialization includes timezone offset. |
| **Review Rule** | Reviewer must verify: (1) no `datetime.now()` or `datetime.utcnow()` in the diff, (2) new datetime columns use `TIMESTAMPTZ`, (3) API datetime fields include timezone offset. |
| **Test Rule** | Lint rule `sbd-l01-naive-datetime` bans `datetime.now()` and `datetime.utcnow()`. Unit test: verify all persisted datetime values have `tzinfo is not None`. |
| **Exception Process** | Level 1 (review-required) for date-only values using `date` objects. Level 1 for CLI scripts that do not persist data. Level 3 (prohibited) for `datetime.now()` in any code that writes to database or sends to API. |

---

## Usage Instructions

1. Copy the template section above for each new safe standard rule
2. Fill in all fields with specific, actionable content
3. Include actual code examples in Forbidden and Approved patterns
4. Link the Rule Name to the corresponding entry in `references/forbidden_patterns.md`
5. Ensure the Exception Process references the correct level from `references/exception_policy.md`
6. Add the completed standard to the project's coding standards document
7. Create the corresponding static analysis rule per `references/static_rule_design_guide.md`
