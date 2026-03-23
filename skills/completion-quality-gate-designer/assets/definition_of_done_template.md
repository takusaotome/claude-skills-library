# Definition of Done

**Project**: [Project Name] <!-- Example: POS Cash Rounding Phase 2 -->
**Version**: [Document Version] <!-- Example: 1.0 -->
**Last Updated**: [YYYY-MM-DD] <!-- Example: 2026-03-21 -->
**Author**: [Name] <!-- Example: QA Lead -->
**Approved By**: [Name] <!-- Example: Project Manager -->

## Purpose

This document defines what "done" means at each completion state for this project. All team members, stakeholders, and gate reviewers must use these definitions consistently. Ambiguous completion claims (e.g., "all OK," "complete") are prohibited; use the precise state names defined below.

## Completion State Definitions

### State 1: Implemented (実装完了)

**Definition**: Code is written, committed to version control, and passes the author's local checks.

| Criterion | Required | Evidence |
|-----------|----------|----------|
| Code committed to feature branch | Yes | Commit hash |
| Compilation / build succeeds locally | Yes | Build log or screenshot |
| Author self-review completed | Yes | Self-review checklist attached to PR |
| Unit tests written for new code | Yes | Test files in same commit |
| Unit tests pass locally | Yes | Local test output |

**Explicit Exclusions (NOT implied by this state)**:
- CI pipeline has NOT necessarily run
- Peer review has NOT been completed
- Integration and E2E tests have NOT been executed
- No quality assertion is made beyond "code compiles and author's tests pass"

**Permitted Language**: "Implementation complete" / "実装完了"
**Prohibited Language**: "Done" / "Complete" / "Ready" / "完了" (without qualifier)

---

### State 2: Verified (検証完了)

**Definition**: All standard verification commands have been executed in CI, results are recorded, and all mandatory criteria are met (or exceptions are formally registered).

| Criterion | Required | Evidence |
|-----------|----------|----------|
| CI pipeline passes all required status checks | Yes | CI run URL and status |
| Unit test results recorded | Yes | JUnit XML artifact from CI |
| Integration test results recorded | Yes | Test report artifact from CI |
| E2E test results recorded | Yes | Test report artifact from CI |
| Code coverage meets threshold (80%) | Yes | Coverage report artifact |
| Static analysis clean (zero errors) | Yes | Linter output artifact |
| Security scan clean (zero critical/high) | Yes | Security report artifact |
| Peer review approved | Yes | PR approval record |
| All failures resolved or registered as exceptions | Yes | Exception register (if any) |

**Explicit Exclusions (NOT implied by this state)**:
- No human acceptance decision has been made
- No stakeholder has reviewed the results
- The artifact is NOT approved for release
- Post-deployment verification has NOT occurred

**Outstanding Items Handling**:
If any criterion is not met, one of the following must apply:
1. The criterion is met after remediation (re-run CI to confirm)
2. An exception is registered with all required fields (see Exception Register)
3. The gate is blocked until the criterion is met

**Permitted Language**: "Verification complete; [N] tests passed, [M] exceptions registered" / "検証完了; 例外[M]件あり"
**Prohibited Language**: "All tests pass" (when exceptions exist) / "Quality confirmed" (no human acceptance yet)

---

### State 3: Accepted (受入完了)

**Definition**: A designated approver has reviewed the verification evidence and formally signed off.

| Criterion | Required | Evidence |
|-----------|----------|----------|
| Verification evidence reviewed by approver | Yes | Review record with approver name and date |
| Exception register reviewed and approved | Yes (if exceptions exist) | Approver sign-off on exception register |
| Acceptance criteria from requirements validated | Yes | Acceptance test results or UAT sign-off |
| Known limitations documented | Yes | Known limitations section in release notes draft |
| Approver differs from producer | Yes | Approver name differs from primary developer/QA |

**Explicit Exclusions (NOT implied by this state)**:
- The artifact has NOT been deployed to production
- Post-deployment verification has NOT occurred
- The release decision has NOT been made (acceptance is for quality; release is a separate business decision)

**Permitted Language**: "Accepted by [approver] on [date] with [N] conditions" / "[approver]が[date]に受入承認（条件[N]件）"
**Prohibited Language**: "Released" / "Shipped" / "リリース完了"

---

### State 4: Released (リリース完了)

**Definition**: The artifact has been deployed to the target production environment, and post-deployment verification confirms it is operational.

| Criterion | Required | Evidence |
|-----------|----------|----------|
| Deployment to production executed | Yes | Deployment log with timestamp and environment |
| Post-deployment smoke tests pass | Yes | Smoke test results |
| Monitoring confirms no anomalies | Yes | Monitoring dashboard screenshot or link (15-min observation minimum) |
| Release record updated | Yes | Release log entry with all metadata |
| Rollback verified as available | Yes | Rollback procedure tested pre-deployment |

**Explicit Exclusions (NOT implied by this state)**:
- All known limitations are NOT necessarily resolved (they are documented and accepted)
- Feature flags may limit user exposure (Released does not mean "available to all users")

**Permitted Language**: "Released to [environment] on [date]; post-deployment verification [passed/failed]" / "[環境]へ[date]にリリース完了; デプロイ後検証[結果]"
**Prohibited Language**: "Done" (without specifying deployment target and verification status)

---

### State 5: Exception-approved (例外承認済)

**Definition**: One or more items that would normally be required for gate passage have been formally waived with documented conditions.

| Criterion | Required | Evidence |
|-----------|----------|----------|
| Exception register entry with all required fields | Yes | Exception register |
| Risk assessment completed | Yes | Risk level in exception record |
| Temporary control in place | Yes | Description of mitigation + verification that it is active |
| Due date set | Yes | Date in exception record |
| Approver sign-off obtained | Yes | Approver name and date in exception record |
| Approver has authority for the risk level | Yes | Approver role vs escalation matrix |

**Permitted Language**: "Exception-approved: [item] deferred to [date] with [control] (approved by [name])" / "例外承認済: [項目]を[date]まで延期、[対策]実施中（[name]承認）"
**Prohibited Language**: "Complete" / "Done" / "OK" / "完了" (exception-approved is NOT complete)

## State Transition Summary

```
Implemented --[CI verification]--> Verified --[Human review]--> Accepted --[Deployment]--> Released
                                      |
                                      +-[Criteria not met]--> Exception-approved --[Approver review]--> Accepted (conditional)
```

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [YYYY-MM-DD] | [Name] | Initial DoD definitions |
