# Quality Gate Matrix

**Project**: [Project Name]
**Version**: [Document Version]
**Last Updated**: [YYYY-MM-DD]
**Author**: [Name]
**Approved By**: [Name]

## Gate Summary

| Gate ID | Gate Name | Phase | Dependency |
|---------|-----------|-------|------------|
| G1 | Design Complete | Requirements -> Design | None |
| G2 | Implementation Complete | Design -> Implementation | G1 |
| G3 | Verification Complete | Implementation -> Testing | G2 |
| G4 | Release Approved | Testing -> Release | G3 |

## Gate Detail Matrix

### G1: Design Complete

| Attribute | Detail |
|-----------|--------|
| **Objective** | Confirm that requirements are unambiguous and design is peer-reviewed |
| **Required Inputs** | Approved requirements document, architecture decision records |
| **Required Evidence** | Design review sign-off, peer review comments resolved |
| **Standard Command** | N/A (document-based gate) |
| **Owner** | Tech Lead |
| **Approver** | Project Manager (must differ from Tech Lead) |
| **Pass Rule** | All mandatory design sections complete; zero open review comments with severity "blocker" |
| **Exception Rule** | Minor documentation gaps may be deferred if core architecture decisions are documented. Non-functional requirements documentation may be deferred up to 14 days. Security design review MUST NOT be deferred. |
| **Exit State** | Accepted (受入完了) |

### G2: Implementation Complete

| Attribute | Detail |
|-----------|--------|
| **Objective** | Confirm that code is written, committed, and passes basic quality checks |
| **Required Inputs** | Approved design, branch with all feature commits |
| **Required Evidence** | Commit hash, unit test results, linter results, code review approval |
| **Standard Command** | `npm test` (unit only), `npm run lint`, `npm run typecheck` |
| **Owner** | Development Lead |
| **Approver** | Tech Lead (must differ from Development Lead) |
| **Pass Rule** | All unit tests pass; linter returns zero errors; code review approved by at least 1 reviewer who is not the author |
| **Exception Rule** | Minor linter warnings in unchanged legacy code may be deferred with remediation ticket. Unit test coverage below threshold may be deferred if coverage delta for new code is above 80%. Any failing unit test MUST NOT be deferred. |
| **Exit State** | Implemented (実装完了) transitioning to Verified (検証完了) for unit scope |

### G3: Verification Complete

| Attribute | Detail |
|-----------|--------|
| **Objective** | Confirm that all standard verification commands pass and results are recorded |
| **Required Inputs** | Implementation complete (G2 passed), CI pipeline green, test environment available |
| **Required Evidence** | CI pipeline output (all stages), integration test report, E2E test report, coverage report, security scan report, performance test report (if applicable) |
| **Standard Command** | `npm test` (unit), `npm run test:integration`, `npm run test:e2e`, `npm run security:scan`, `npm run coverage:check` |
| **Owner** | QA Lead |
| **Approver** | Tech Lead + Product Owner (dual sign-off) |
| **Pass Rule** | All standard commands pass; coverage above 80%; zero critical/high security findings; all E2E scenarios pass; performance within defined thresholds |
| **Exception Rule** | Non-critical E2E failures on non-primary browsers may be deferred up to 30 days with manual verification as temporary control. Medium-severity security findings may be deferred up to 60 days with compensating controls documented. Any critical security finding, data loss risk, or core workflow failure MUST NOT be deferred. |
| **Exit State** | Verified (検証完了) |

### G4: Release Approved

| Attribute | Detail |
|-----------|--------|
| **Objective** | Confirm that the release package is ready and risks are acceptable |
| **Required Inputs** | Verification complete (G3 passed), release notes drafted, rollback plan documented, exception register reviewed |
| **Required Evidence** | Release readiness checklist (all items checked), exception register (all open items reviewed), release notes (approved by PO), rollback procedure (tested), monitoring criteria defined |
| **Standard Command** | `npm run build:production`, deployment dry-run to staging |
| **Owner** | Release Manager |
| **Approver** | Project Sponsor or Steering Committee |
| **Pass Rule** | Zero open critical exceptions; all high exceptions have temporary controls verified; release notes approved; rollback tested; monitoring alerts configured |
| **Exception Rule** | Only low-risk exceptions with verified temporary controls may remain open at release. All medium+ exceptions must be resolved or re-approved by project sponsor. Release without rollback capability is NEVER permitted. |
| **Exit State** | Accepted (受入完了) transitioning to Released (リリース完了) upon deployment |

## Standard Verification Command Set

| Command | Scope | Covers | Does NOT Cover | Gate | CI Required |
|---------|-------|--------|----------------|------|-------------|
| `npm test` | Unit tests | Individual function behavior, edge cases | Integration, E2E, performance | G2, G3 | Yes |
| `npm run test:integration` | Integration tests | API contracts, DB queries, service interactions | E2E workflows, UI behavior | G3 | Yes |
| `npm run test:e2e` | E2E tests | Full user workflows on primary browsers | Non-primary browsers, performance | G3 | Yes |
| `npm run lint` | Static analysis | Code style, basic code quality rules | Security, logic errors | G2 | Yes |
| `npm run security:scan` | Security scan | Known CVEs in dependencies, SAST findings | Runtime security, penetration testing | G3 | Yes |
| `npm run coverage:check` | Coverage report | Line and branch coverage percentage | Test quality (coverage != correctness) | G3 | Yes |
| `npm run build:production` | Build verification | Production build succeeds, no build errors | Runtime behavior | G4 | Yes |

## Expression Control Rules

| Prohibited Expression | Why Prohibited | Required Alternative |
|-----------------------|----------------|---------------------|
| "All tests pass" (when skipped tests exist) | Conceals skipped tests | "188 of 191 tests passed, 3 skipped (see EX-2026-003)" |
| "Complete" (when state is Implemented only) | Conflates implementation with verification | "Implementation complete; verification pending" |
| "All OK" (when exceptions are registered) | Conceals known limitations | "Verification complete with 2 registered exceptions (see Exception Register)" |
| "100% pass rate" (without denominator) | Misleading without scope | "100% pass rate on 188 unit tests (ref: CI Run #1234)" |
| "Quality confirmed" (without specifying by whom) | Omits accountability | "Quality verified by [name] on [date] based on [evidence ref]" |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [YYYY-MM-DD] | [Name] | Initial gate matrix |
