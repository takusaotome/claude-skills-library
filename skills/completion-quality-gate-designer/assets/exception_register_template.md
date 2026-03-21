# Exception Register

**Project**: [Project Name]
**Version**: [Document Version]
**Last Updated**: [YYYY-MM-DD]
**Register Owner**: [Name / Role]

## Summary

| Status | Count |
|--------|-------|
| Open | [N] |
| Resolution Pending | [N] |
| Closed | [N] |
| Expired | [N] |
| **Total** | **[N]** |

## Open Exceptions

| Exception ID | Gate ID | Item Description | Reason | Risk Level | Risk Description | Temporary Control | Due Date | Owner | Approver | Approval Date | Closure Evidence Required | Status |
|-------------|---------|-----------------|--------|------------|------------------|-------------------|----------|-------|----------|---------------|--------------------------|--------|
| EX-2026-001 | G3 | E2E tests for payment flow not executed on Safari | Safari test environment unavailable due to infrastructure migration | Medium | Payment flow may fail on Safari; estimated 8% of user base affected | Manual QA verification performed on Safari (session #12); monitoring alert configured for payment errors by browser type | 2026-04-15 | QA Lead (Tanaka) | PM (Suzuki) | 2026-03-20 | CI pipeline showing Safari E2E tests passing; test report attached | Open |
| EX-2026-002 | G3 | Code coverage at 78% (threshold: 80%) | New utility module added without tests in final sprint | Low | Utility module handles non-critical formatting; no business logic | Module is isolated with no side effects; manual review of all 4 functions completed | 2026-04-01 | Dev Lead (Yamada) | Tech Lead (Sato) | 2026-03-21 | Coverage report showing 80%+ with new tests for utility module | Open |
| [EX-YYYY-NNN] | [Gate] | [What is incomplete] | [Why it cannot be completed now] | [Low/Medium/High] | [What could go wrong] | [What mitigation is in place RIGHT NOW] | [YYYY-MM-DD] | [Name] | [Name] | [YYYY-MM-DD] | [What evidence will confirm resolution] | [Status] |

## Closed Exceptions

| Exception ID | Gate ID | Item Description | Original Due Date | Actual Closure Date | Closure Evidence | Closed By |
|-------------|---------|------------------|--------------------|---------------------|------------------|-----------|
| EX-2026-000 | G2 | TypeScript strict mode migration for legacy module | 2026-03-10 | 2026-03-08 | PR #245 merged; CI Run #892 shows zero type errors | Tech Lead (Sato) |
| [EX-YYYY-NNN] | [Gate] | [Description] | [Date] | [Date] | [Evidence reference] | [Name] |

## Expired Exceptions (REQUIRES IMMEDIATE ACTION)

| Exception ID | Gate ID | Item Description | Due Date | Days Overdue | Owner | Escalation Authority | Action Required |
|-------------|---------|------------------|----------|--------------|-------|---------------------|-----------------|
| (none) | | | | | | | |

## Exception Governance Quick Reference

### Risk Level Definitions

| Risk Level | Definition | Approver Authority | Max Duration |
|------------|------------|--------------------|-------------|
| Low | No user-facing impact; cosmetic or internal-only | Team Lead | 90 days |
| Medium | Limited user impact; workaround available | Project Manager | 60 days |
| High | Significant user impact; degraded experience | Project Sponsor | 30 days |
| Critical | NOT ELIGIBLE for exception -- must block the gate | N/A | N/A |

### Mandatory Fields Checklist

Before submitting an exception for approval, verify ALL fields are populated:

- [ ] Exception ID assigned
- [ ] Gate ID specified
- [ ] Item description is specific and actionable
- [ ] Reason explains why it cannot be completed now
- [ ] Risk level assigned (Low/Medium/High)
- [ ] Risk description states what could go wrong in concrete terms
- [ ] Temporary control describes what is in place RIGHT NOW (not planned)
- [ ] Due date is within the maximum duration for the risk level
- [ ] Owner is named (specific person, not a team)
- [ ] Approver is named and differs from the owner
- [ ] Closure evidence is defined: what artifact will prove resolution

### Renewal Tracking

| Exception ID | Original Due Date | Renewal Date | New Due Date | Renewal Approver | Renewal Reason |
|-------------|-------------------|--------------|--------------|------------------|----------------|
| (none currently) | | | | | |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [YYYY-MM-DD] | [Name] | Initial exception register |
