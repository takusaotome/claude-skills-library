# Exception Policy Reference

This reference defines when and how exceptions to safe-by-default standards are granted. The goal is not zero exceptions (which would mean the standards are too loose) but governed, documented, and reviewable exceptions.

**Guiding Principle**: Exceptions are expected. The measure of a healthy standard is not that no one ever needs an exception, but that every exception is deliberate, documented, and periodically reviewed.

---

## 1. Exception Classification

Every exception to a safe-by-default rule falls into one of three approval levels:

### Level 1: Review-Required

**Definition**: The exception is permitted with peer code review and an inline justification comment.

**When to Apply**:
- The deviation is small in scope (single function or code block)
- The risk is well-understood and mitigated by other controls
- The alternative safe pattern is technically infeasible for this specific case
- The exception does not affect security-critical paths

**Process**:
1. Developer adds a suppression comment with rule ID and justification
2. Code reviewer verifies the justification is valid
3. No additional approval beyond normal code review
4. Exception is tracked via static rule suppression reports

**Example Scenarios**:
- Using positional tuple unpacking in a test helper that processes a fixed-format fixture
- Using `datetime.now()` in a CLI script that only runs locally and does not persist data
- Catching a broad exception at the top level of a CLI command to provide a user-friendly error message

**Documentation Format**:
```python
# Exception: SBD-L04 -- Top-level CLI error handler.
# Broad catch is intentional to prevent stack traces reaching end users.
# All caught exceptions are logged with full traceback before the user-friendly message.
try:
    main()
except Exception as e:
    logger.exception("Unhandled error in CLI")
    click.echo(f"Error: {e}. See logs for details.", err=True)
    sys.exit(1)
```

---

### Level 2: Approval-Required

**Definition**: The exception requires explicit approval from a tech lead, architect, or security team member, documented in an Architecture Decision Record (ADR).

**When to Apply**:
- The deviation is broad in scope (affects multiple functions, a module, or a service)
- The risk involves security, data integrity, or compliance
- The deviation will persist for an extended period (not a temporary workaround)
- The exception may set a precedent that other teams reference

**Process**:
1. Developer creates an ADR using `assets/architecture_decision_record_template.md`
2. ADR is reviewed and approved by the designated approver (tech lead, architect, or security)
3. Approval is recorded in the ADR (approver name, date, conditions)
4. The ADR is linked from the code via a comment
5. Exception is added to the project's exception registry
6. Exception is reviewed at the next quarterly standards review

**Example Scenarios**:
- Using raw SQL for a complex reporting query that the ORM cannot express efficiently
- Relaxing deny-by-default authorization for a public-facing API module
- Allowing direct filesystem access in a data pipeline that processes TB-scale files
- Storing timestamps in local timezone for a legacy system integration
- Using a service locator pattern in a legacy module that cannot be refactored immediately

**Documentation Format**:
```python
# Exception: SBD-S01 -- Raw SQL for reporting aggregation.
# ADR: docs/adr/2024-003-raw-sql-reporting.md
# Approved by: @architect (2024-03-15)
# Review date: 2024-06-15
# Justification: ORM cannot express window functions with PARTITION BY
# and ROWS BETWEEN. Query uses only parameterized values.
raw_query = """
    SELECT department,
           SUM(revenue) OVER (PARTITION BY department ORDER BY month
                              ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
    FROM monthly_revenue
    WHERE year = %s
"""
cursor.execute(raw_query, [year])
```

---

### Level 3: Prohibited (No Exception)

**Definition**: The pattern is never allowed regardless of circumstances. No exception process exists because the risk cannot be mitigated.

**When to Apply**:
- The pattern has a direct, exploitable security vulnerability with no mitigating controls
- The pattern violates regulatory or compliance requirements
- Safe alternatives exist for every conceivable use case

**Prohibited Patterns**:

| Pattern | Why No Exception | Alternative |
|---------|-----------------|-------------|
| SQL concatenation with user input | Always exploitable, parameterization always available | Parameterized queries |
| Committing secrets to version control | Cannot be un-committed (git history), always leakable | Environment variables, secrets manager |
| Disabling authentication middleware globally | Removes all access control, cannot be scoped | Per-route `@public` annotation |
| Logging sensitive data (passwords, tokens, PII) | Logs are widely accessible, cannot be un-logged | Mask/redact before logging |
| Eval/exec with user input | Code injection, no safe way to sandbox in most languages | Purpose-built parsers, DSLs |

---

## 2. Exception Scenarios by Category

### Raw SQL Exceptions

Raw SQL is the most commonly requested exception. Apply these criteria:

**Allowed (Level 2 - Approval Required)**:
- Database migrations (DDL statements that the ORM cannot generate)
- Complex analytical queries using window functions, CTEs, or database-specific features
- Bulk operations where ORM performance is unacceptable (after profiling proves the bottleneck)
- Vendor-mandated query patterns (e.g., specific stored procedure calls required by a third-party integration)

**Requirements for All Raw SQL Exceptions**:
- All user-supplied values must use parameter binding (never concatenation)
- The query must be tested with injection-attempt inputs
- The query must be encapsulated in a repository method (not inline in a handler)
- The exception must specify which specific queries are covered (no blanket "raw SQL is allowed in this module")

**Not Allowed (Level 3 - Prohibited)**:
- Raw SQL with string concatenation or formatting of user input (no exceptions ever)
- Raw SQL in controller/handler code (must go through repository layer)

### Migration and Schema Change Exceptions

Database migrations often require patterns that would normally be forbidden:

**Allowed (Level 1 - Review Required)**:
- Raw DDL statements (`CREATE TABLE`, `ALTER TABLE`, `CREATE INDEX`) in migration files
- Direct column/table references by string name in migration scripts
- Positional argument usage in migration framework APIs (framework-mandated pattern)

**Requirements**:
- Migration files must be in a designated migrations directory (not mixed with application code)
- Migration files should be excluded from most static rules by directory convention
- Migrations must be tested in a staging environment before production deployment

### Reporting and Analytics Exceptions

Reporting workloads have different performance and capability requirements:

**Allowed (Level 2 - Approval Required)**:
- Raw SQL with complex aggregations, window functions, and CTEs
- Read-only database connections that bypass ORM for performance
- Materialized views or denormalized tables for dashboard performance

**Requirements**:
- Reporting queries must use read-only database connections
- All parameters must use parameterized binding
- Query results must not be used to modify application state
- Performance gains must be documented (before/after benchmarks)

### Vendor and Integration Constraints

Third-party integrations sometimes mandate specific patterns:

**Allowed (Level 2 - Approval Required)**:
- Vendor-required authentication patterns that deviate from deny-by-default (e.g., webhook endpoints with HMAC verification instead of token auth)
- Vendor SDK patterns that use global state or implicit configuration
- Legacy protocol support (e.g., SOAP/XML handling that requires different serialization patterns)

**Requirements**:
- Vendor-mandated deviations must be isolated in a dedicated integration module
- The integration module's boundary must enforce safe patterns for all data entering the main application
- Vendor documentation supporting the requirement must be linked in the ADR

---

## 3. Exception Registry

Every project using safe-by-default standards should maintain an exception registry. This is a living document that tracks all active exceptions.

### Registry Format

| ID | Rule | Level | Scope | Justification | Approver | Granted | Review By | Status |
|----|------|-------|-------|---------------|----------|---------|-----------|--------|
| EX-001 | SBD-S01 | L2 | `reporting/queries.py` | Window function aggregation | @architect | 2024-03-15 | 2024-06-15 | Active |
| EX-002 | SBD-L01 | L1 | `cli/commands.py` | CLI-only, no persistence | Peer review | 2024-04-01 | 2024-07-01 | Active |
| EX-003 | SBD-S02 | L2 | `webhooks/stripe.py` | Stripe webhook uses HMAC, not token auth | @security | 2024-02-01 | 2024-05-01 | Active |

### Registry Review Process

1. **Quarterly review**: All active exceptions are reviewed every quarter
2. **Expiration**: Exceptions granted more than 12 months ago must be re-approved or retired
3. **Trend analysis**: If the same rule accumulates many exceptions, consider whether the rule needs refinement
4. **Closure**: When the underlying constraint is removed (e.g., ORM now supports the needed feature), close the exception and migrate the code

---

## 4. Exception Request Workflow

When a developer needs an exception:

### For Level 1 (Review-Required):
1. Add suppression comment with rule ID and justification in the code
2. Mention the exception in the PR description
3. Reviewer validates the justification during normal code review
4. If approved, merge as normal

### For Level 2 (Approval-Required):
1. Create an ADR using `assets/architecture_decision_record_template.md`
2. Submit the ADR as a separate PR or as part of the implementation PR
3. Request review from the designated approver (tech lead, architect, or security)
4. Approver reviews the ADR, may request changes or suggest alternatives
5. Once approved, add the exception to the exception registry
6. Add an inline code comment linking to the ADR
7. Set a review date (default: 3 months from approval)

### For Level 3 (Prohibited):
1. No exception request is possible
2. If the developer believes the prohibition is incorrect, raise it as a standards revision proposal
3. Standards revision requires consensus from the architecture team and security team
4. If approved, the pattern is reclassified from Level 3 to Level 2 with specific conditions

---

## 5. Anti-Patterns in Exception Governance

Avoid these common failure modes:

### Too Few Exceptions (Rules Are Too Loose)
- **Symptom**: No one ever requests exceptions
- **Root Cause**: Rules are vague or do not cover enough patterns
- **Fix**: Tighten rules, add more specific patterns, review defect data for gaps

### Too Many Exceptions (Rules Do Not Fit the Codebase)
- **Symptom**: More than 20% of a rule's matches are suppressed
- **Root Cause**: Rule does not account for legitimate use cases in this codebase
- **Fix**: Refine the rule to reduce false positives, or split into multiple narrower rules

### Exception Without Justification
- **Symptom**: Suppression comments that say only `# noqa` with no explanation
- **Root Cause**: Developers treat suppression as a way to silence warnings, not as a documented exception
- **Fix**: Require justification in suppression comments (enforce via meta-rule)

### Exception Without Expiration
- **Symptom**: Exceptions granted years ago that no one reviews
- **Root Cause**: No review cycle, no registry
- **Fix**: Maintain the exception registry, enforce quarterly reviews

### Blanket Module-Level Exception
- **Symptom**: An entire module is excluded from a rule
- **Root Cause**: Laziness or the module genuinely needs different rules
- **Fix**: If the module genuinely needs different rules, create a separate rule configuration for that module type. If laziness, require per-function exceptions.
