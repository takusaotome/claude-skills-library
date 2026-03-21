# Reuse Risk Register

## Investigation Metadata

| Field | Value |
|-------|-------|
| **Investigation ID** | HCI-YYYYMMDD-NNN |
| **Project / Feature** | [New feature or project that requires reuse] |
| **Investigator** | [Name] |
| **Date** | [YYYY-MM-DD] |
| **Status** | Draft / In Review / Final |

---

## Risk Register

### Risk Severity Scale

| Level | Definition | Example |
|-------|-----------|---------|
| **Critical** | Data loss, financial error, security breach, or system outage | Arithmetic on formatted string produces wrong invoice total |
| **High** | Feature malfunction visible to users, requiring hotfix | Function returns None instead of raising exception, causing blank page |
| **Medium** | Degraded behavior detectable through monitoring or QA | Timezone-naive datetime causes off-by-one-day in reports |
| **Low** | Cosmetic issue or minor inconvenience, workaround available | Function name is misleading but behavior is correct |

### Risk Likelihood Scale

| Level | Definition | Triggering Condition |
|-------|-----------|---------------------|
| **High** | Will occur on normal usage paths | Every caller exercising the mismatched contract will hit this |
| **Medium** | Occurs under specific but realistic conditions | Triggered by edge cases, specific data patterns, or environment differences |
| **Low** | Requires unusual circumstances to trigger | Only manifests under rare race conditions or extreme input values |

---

## Registered Risks

| # | Asset | Risk Type | Failure Mode | Severity | Likelihood | Risk Score | Mitigation | Owner | Status |
|---|-------|-----------|-------------|:--------:|:----------:|:----------:|-----------|-------|--------|
| R-001 | `keepTwoDecimal()` | Type Mismatch | Arithmetic on return value causes TypeError or silent string concatenation instead of numeric addition | Critical | High | Critical | Build `round_to_decimal()` wrapper that strips formatting; add contract test asserting numeric return type | [Dev name] | Open |
| R-002 | `getNextId()` | Hidden Side Effect | Calling function in test environment mutates global counter and writes audit log, causing test pollution | High | Medium | High | Inject counter via parameter; mock audit log in tests; add contract test for side effect isolation | [Dev name] | Open |
| R-003 | `ConfigManager.get_allowed_hosts()` | Mutable Sharing | Caller appending to returned list modifies internal state, allowing unvalidated hosts | Critical | Medium | Critical | Return `list(self._allowed_hosts)` copy; add contract test verifying modification isolation | [Dev name] | Open |
| R-004 | | | | | | | | | |
| R-005 | | | | | | | | | |

---

## Risk Score Matrix

Use severity and likelihood to determine the combined risk score:

|  | **High Likelihood** | **Medium Likelihood** | **Low Likelihood** |
|:----|:---:|:---:|:---:|
| **Critical Severity** | Critical | Critical | High |
| **High Severity** | Critical | High | Medium |
| **Medium Severity** | High | Medium | Low |
| **Low Severity** | Medium | Low | Low |

---

## Mitigation Tracking

| Risk # | Mitigation Action | Target Date | Completed Date | Verification |
|--------|------------------|:-----------:|:--------------:|-------------|
| R-001 | Create `round_to_decimal()` wrapper | YYYY-MM-DD | | Contract test passes |
| R-001 | Add contract test for return type | YYYY-MM-DD | | CI green |
| R-001 | Deprecate direct arithmetic use of `keepTwoDecimal` | YYYY-MM-DD | | Linter rule added |
| R-002 | Refactor `getNextId()` to accept counter parameter | YYYY-MM-DD | | Unit test passes |
| R-003 | Return defensive copy from `get_allowed_hosts()` | YYYY-MM-DD | | Mutation test passes |

---

## Risk Summary Statistics

| Metric | Count |
|--------|:-----:|
| Total risks identified | |
| Critical risks | |
| High risks | |
| Medium risks | |
| Low risks | |
| Mitigated risks | |
| Open risks | |
| Accepted risks | |

---

## Acceptance Decisions

Risks that have been reviewed and accepted (will not be mitigated):

| Risk # | Asset | Risk Description | Acceptance Rationale | Approved By | Date |
|--------|-------|-----------------|---------------------|-------------|------|
| | | | | | |

---

## Notes

- Every risk with severity Critical or High must have a mitigation plan with owner and target date
- Medium risks should have mitigation plans; Low risks may be accepted with rationale
- Risk scores should be re-evaluated after mitigation is implemented
- Connect each risk to the corresponding entry in the Implicit Contract Sheet for traceability
