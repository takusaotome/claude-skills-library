# Architecture Decision Record (ADR) Template

Use this template to document architectural decisions related to safe-by-default standards, including decisions to adopt safe defaults, to create exceptions, or to modify existing rules.

---

## Template

```markdown
# ADR-NNN: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Date

[YYYY-MM-DD]

## Decision Makers

| Role | Name | Approval |
|------|------|----------|
| Author | [name] | N/A |
| Reviewer | [name] | [ ] Approved / [ ] Rejected |
| Approver | [name] | [ ] Approved / [ ] Rejected |

## Context

[Describe the situation that motivates this decision. Include:]
- What problem or recurring issue has been observed?
- What evidence supports the need for a decision? (defect count, RCA references, audit findings)
- What constraints exist? (technology stack, team expertise, timeline, vendor requirements)
- What related decisions have already been made? (reference other ADRs)

## Decision

[State the decision clearly and concisely.]
- What will be done?
- What is the scope? (which modules, services, or teams are affected)
- What is the effective date?
- How will compliance be verified?

## Consequences

### Positive

- [Benefit 1: What risk is mitigated?]
- [Benefit 2: What quality attribute is improved?]
- [Benefit 3: What operational overhead is reduced?]

### Negative

- [Cost 1: What additional effort is required?]
- [Cost 2: What flexibility is reduced?]
- [Cost 3: What migration work is needed?]

### Neutral

- [Observation 1: What changes but is neither positive nor negative?]

## Exceptions

[Define any exceptions to this decision.]

| Exception | Scope | Level | Conditions | Review Date |
|-----------|-------|-------|------------|-------------|
| [Description] | [Affected files/modules] | [L1/L2] | [What must be true for exception to apply] | [YYYY-MM-DD] |

## Alternatives Considered

### Alternative 1: [Name]

- **Description**: [What was considered?]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Why rejected**: [Reason for not choosing this option]

### Alternative 2: [Name]

- **Description**: [What was considered?]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Why rejected**: [Reason for not choosing this option]

## Related Rules

| Rule ID | Relationship | Notes |
|---------|-------------|-------|
| [SBD-XXX] | [Implements / Modifies / Supersedes / Depends on] | [Brief explanation] |

## Review Schedule

- **Next review**: [YYYY-MM-DD]
- **Review frequency**: [Quarterly / Semi-annually / Annually]
- **Review criteria**: [What would trigger revision of this decision?]
```

---

## Filled Example: Adopt Parameterized Query Standard

```markdown
# ADR-001: Adopt Parameterized Query Standard

## Status

Accepted

## Date

2024-03-15

## Decision Makers

| Role | Name | Approval |
|------|------|----------|
| Author | @backend-lead | N/A |
| Reviewer | @security-engineer | [x] Approved |
| Approver | @chief-architect | [x] Approved |

## Context

Over the past 6 months, 3 SQL injection vulnerabilities were discovered in production code (INC-20240112-001, INC-20240203-002, INC-20240301-003). All three involved string concatenation to construct SQL queries in controller-level code. RCA findings (RCA-2024-Q1-Summary) identified the root cause as: no standard prohibiting raw SQL concatenation, no common query abstraction layer, and no automated detection.

The codebase currently contains approximately 15 instances of raw SQL concatenation across 8 modules. The application uses SQLAlchemy ORM but developers bypass it for perceived simplicity in ad-hoc queries.

## Decision

Effective 2024-04-01, all SQL queries in application code must use parameterized statements (ORM query builder or parameterized raw SQL). String concatenation, f-strings, %-formatting, and .format() for SQL construction are prohibited.

Scope: All Python application code in the `src/` directory. Excludes `migrations/` and `tests/`.

Compliance verification:
1. Semgrep rule `sbd-s01-sql-concatenation` enforced as ERROR in CI pipeline
2. Existing violations remediated by 2024-04-15 (tracked in JIRA epic APP-1234)
3. Quarterly audit of rule suppression comments

## Consequences

### Positive

- Eliminates SQL injection attack vector (addresses OWASP A03:2021)
- Enables database query plan caching (performance improvement)
- Centralizes query logic in repository layer (improves maintainability)

### Negative

- Requires refactoring 15 existing raw SQL instances (estimated 3 developer-days)
- Complex reporting queries require approval process to use raw parameterized SQL
- Developers must learn repository pattern (training overhead)

### Neutral

- Query logic moves from controllers to repository classes (code organization change)

## Exceptions

| Exception | Scope | Level | Conditions | Review Date |
|-----------|-------|-------|------------|-------------|
| Raw parameterized SQL for reporting | `src/reporting/queries.py` | L2 | ORM cannot express the query; all values parameterized; approved by architect | 2024-06-15 |
| Database migration DDL | `migrations/` | L1 | Standard migration framework usage; no user input | Permanent |

## Alternatives Considered

### Alternative 1: Allow raw SQL with mandatory code review

- **Description**: Permit raw SQL but require security-focused code review for all PRs containing SQL
- **Pros**: No code changes needed, flexible
- **Cons**: Human review is fallible (3 vulnerabilities already passed review), does not scale
- **Why rejected**: The existing approach (informal review) has already failed 3 times

### Alternative 2: Database-level prepared statement enforcement

- **Description**: Configure PostgreSQL to reject non-parameterized queries
- **Pros**: Enforcement at the database level is impossible to bypass
- **Cons**: Not supported by PostgreSQL for application queries, would break ORM, too restrictive
- **Why rejected**: Technically infeasible with current database configuration

## Related Rules

| Rule ID | Relationship | Notes |
|---------|-------------|-------|
| SBD-S01 | Implements | Semgrep rule enforces this ADR in CI |
| SBD-L04 | Depends on | Bare except suppression might hide SQL errors |
| FP-01 | Addresses | Directly addresses Forbidden Pattern FP-01 |

## Review Schedule

- **Next review**: 2024-06-15
- **Review frequency**: Quarterly
- **Review criteria**: New SQL injection incidents, exception request frequency exceeding 2/quarter, false positive rate exceeding 10%
```

---

## Filled Example: Exception for Legacy Integration Module

```markdown
# ADR-007: Exception for Legacy SOAP Integration Module

## Status

Accepted

## Date

2024-05-10

## Decision Makers

| Role | Name | Approval |
|------|------|----------|
| Author | @integration-lead | N/A |
| Reviewer | @backend-lead | [x] Approved |
| Approver | @chief-architect | [x] Approved |

## Context

The `src/integrations/legacy_erp/` module integrates with a vendor ERP system via SOAP/XML. The vendor SDK (erp-connector v2.3) uses a service locator pattern internally and requires module-level initialization. This conflicts with safe default SBD-S05 (no global state access) and SBD constructor injection standard.

The vendor has no plans to update the SDK to support dependency injection. Wrapping the SDK would require reimplementing the SOAP client, which is not justified given the integration is scheduled for replacement in Q4 2024.

## Decision

Grant Level 2 exception for `src/integrations/legacy_erp/` module to use the vendor SDK's service locator pattern. The exception is scoped to the integration boundary only. All data exiting the integration module into the main application must be validated and converted to domain types.

## Consequences

### Positive

- Avoids unnecessary reimplementation of vendor SDK wrapper
- Maintains integration stability during transition period

### Negative

- Integration module is harder to test (requires SDK mocking at module level)
- Exception may be referenced as precedent by other teams

### Neutral

- Integration module has different coding standards from the rest of the application

## Exceptions

| Exception | Scope | Level | Conditions | Review Date |
|-----------|-------|-------|------------|-------------|
| Service locator pattern | `src/integrations/legacy_erp/` only | L2 | Vendor SDK mandates; boundary validation enforced; replacement planned Q4 2024 | 2024-08-10 |

## Alternatives Considered

### Alternative 1: Wrap vendor SDK in DI-compatible adapter

- **Description**: Create a thin adapter that initializes the SDK internally and exposes DI-compatible interfaces
- **Pros**: Rest of codebase sees clean DI interface
- **Cons**: Significant effort (estimated 2 weeks), adapter must track SDK API changes
- **Why rejected**: Integration is being replaced in Q4; wrapper investment is not justified

## Related Rules

| Rule ID | Relationship | Notes |
|---------|-------------|-------|
| SBD-S05 | Exception to | Global state access permitted in scoped module |
| FP-08 | Exception to | Implicit dependency via vendor SDK |

## Review Schedule

- **Next review**: 2024-08-10
- **Review frequency**: Quarterly until Q4 2024 replacement
- **Review criteria**: Vendor SDK update availability, replacement project timeline changes
```

---

## Usage Instructions

1. Create a new ADR file: `docs/adr/ADR-NNN-descriptive-name.md`
2. Use sequential numbering (ADR-001, ADR-002, etc.)
3. Fill in all sections; do not leave any section blank
4. For exception ADRs, always specify a review date (default: 3 months from approval)
5. Link the ADR from the code that uses the exception (inline comment with ADR reference)
6. Add the ADR to the exception registry per `references/exception_policy.md`
7. Store ADRs in version control alongside the code they govern
8. When an ADR is superseded, update its status and reference the new ADR
