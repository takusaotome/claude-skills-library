# QA Backlog Template

Use this template for Step 3: Converge Into QA Backlog.

---

## Project Information

**Project:** [Project Name]
**Migration Phase:** [Phase]
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Owner:** [Name]

---

## QA Backlog

| # | Check Name | Scope | Risk | Evidence | Method | Pass Criteria | Owner | Status |
|---|------------|-------|------|----------|--------|---------------|-------|--------|
| 1 |            |       | H    |          |        |               |       | New    |
| 2 |            |       | H    |          |        |               |       | New    |
| 3 |            |       | M    |          |        |               |       | New    |
| 4 |            |       | M    |          |        |               |       | New    |
| 5 |            |       | L    |          |        |               |       | New    |

### Column Definitions

- **Check Name:** Short descriptive name for the check
- **Scope:** Object/field/flow/integration affected
- **Risk:** Impact x Likelihood x Detectability (H/M/L)
- **Evidence:** Source document (spec/report) or discovery cycle #
- **Method:** Query/Diff/UI Test/Sample Review/Integration Test
- **Pass Criteria:** Specific threshold or condition for pass
- **Owner:** Person responsible for execution
- **Status:** New / In Progress / Blocked / Done / Won't Fix

---

## Risk Scoring Guide

### Impact
- **H (High):** Revenue impact, compliance violation, data loss
- **M (Medium):** Operational disruption, manual workaround needed
- **L (Low):** Cosmetic, minor inconvenience

### Likelihood
- **H (High):** Will definitely occur based on evidence
- **M (Medium):** May occur under certain conditions
- **L (Low):** Unlikely but possible

### Detectability
- **H (Hard to detect):** Silent failure, no error logged
- **M (Medium):** Requires specific query/test to find
- **L (Easy to detect):** Obvious error, user will report

---

## Quality Gates

Pre-go-live gates (all must pass):

| Gate | Criteria | Status | Evidence |
|------|----------|--------|----------|
| **Data Completeness** | Record counts match within X% tolerance | | |
| **Referential Integrity** | No orphaned children on critical relationships | | |
| **Financial Reconciliation** | Invoice/billing totals match exactly | | |
| **Security Verification** | Persona-based access tests pass | | |
| **Automation Readiness** | Triggers/flows tested in migration mode OFF | | |
| **Integration Idempotency** | Retry tests show no duplicates | | |
| **Report Accuracy** | Key reports match source within tolerance | | |
| **Archive Accessibility** | Archived data searchable and restorable | | |

---

## Open Questions

| # | Question | Impact if Unresolved | Owner | Due Date | Status |
|---|----------|---------------------|-------|----------|--------|
| 1 |          |                     |       |          | Open   |
| 2 |          |                     |       |          | Open   |

---

## Assumptions

| # | Assumption | Risk if Wrong | Validation Plan |
|---|------------|---------------|-----------------|
| 1 |            |               |                 |
| 2 |            |               |                 |

---

## Executive Summary

### Top 3 Risks

1. **[Risk Name]**
   - Impact:
   - Mitigation:
   - Decision needed:

2. **[Risk Name]**
   - Impact:
   - Mitigation:
   - Decision needed:

3. **[Risk Name]**
   - Impact:
   - Mitigation:
   - Decision needed:

### Go/No-Go Recommendation

**Recommendation:** [ ] Go | [ ] Conditional Go | [ ] No-Go

**Conditions (if Conditional):**


**Rationale:**


---

## Appendix: Queries and Scripts

### Data Completeness Queries
```sql
-- Source count

-- Target count

-- Comparison
```

### Orphan Detection Queries
```sql
-- Children without parents

-- Parents without children (where required)
```

### Financial Reconciliation Queries
```sql
-- Source totals

-- Target totals

-- Variance
```

---

## Revision History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
|      | 1.0     |        | Initial |
