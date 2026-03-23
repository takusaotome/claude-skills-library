# Adoption Recommendation

## Investigation Metadata

| Field | Value |
|-------|-------|
| **Investigation ID** | HCI-YYYYMMDD-NNN |
| **Project / Feature** | [New feature requiring reuse] |
| **Investigator** | [Name] |
| **Date** | [YYYY-MM-DD] |
| **Status** | Draft / In Review / Final |

---

## Recommendation Summary

| # | Reuse Candidate | Reuse Decision | Guardrail Required | Est. Effort |
|---|-----------------|:--------------:|:------------------:|:-----------:|
| 1 | `keepTwoDecimal()` | B -- Wrapper | Yes | 2h |
| 2 | `getNextId()` | B -- Wrapper | Yes | 4h |
| 3 | `ConfigManager.get_allowed_hosts()` | B -- Wrapper | Yes | 1h |
| 4 | | | | |
| 5 | | | | |

### Decision Legend

| Level | Meaning |
|-------|---------|
| **A** | Reuse as-is (add contract test only) |
| **B** | Reuse with wrapper (thin interface adaptation) |
| **C** | Reuse with adapter (significant interface layer) |
| **D** | Undecided -- contract test needed first |
| **E** | Do not reuse -- redesign required |

---

## Detailed Recommendations

### Recommendation 1: `keepTwoDecimal(value)`

| Aspect | Detail |
|--------|--------|
| **Reuse decision** | **Level B** -- Reuse with wrapper |
| **Rationale** | Core rounding logic is correct. Name and return type are misleading (returns formatted string, not number). Wrapper provides correct interface for arithmetic callers. |
| **Guardrail** | New callers requiring numeric results MUST use the wrapper function, never call `keepTwoDecimal` directly for arithmetic. |
| **Wrapper needed?** | YES -- `round_to_decimal(value: float) -> Decimal` that strips formatting from `keepTwoDecimal` output. |
| **Rename needed?** | RECOMMENDED -- Rename original to `format_two_decimal()` to accurately reflect its string-formatting behavior. Requires updating 2 existing display callers. |
| **Contract test needed?** | YES -- Test asserting wrapper returns `Decimal` type and original returns `str` type (prevents future regression in either direction). |
| **Documentation needed?** | YES -- Add docstring to both original and wrapper clarifying the distinction between formatting and arithmetic use cases. |
| **Prerequisites before reuse** | 1. Implement wrapper function. 2. Add contract tests. 3. Update callers guide. |
| **Risk if ignored** | Critical -- Arithmetic on formatted string will cause TypeError or silent data corruption. This exact pattern caused incident INC-20250115-003. |

---

### Recommendation 2: `getNextId()`

| Aspect | Detail |
|--------|--------|
| **Reuse decision** | **Level B** -- Reuse with wrapper |
| **Rationale** | ID generation logic is correct. Hidden side effects (global counter mutation, audit logging) make it unsafe for test environments and concurrent access. |
| **Guardrail** | NEVER call in performance-sensitive loops (audit log write on every call). In tests, use the injectable wrapper to avoid global state pollution. |
| **Wrapper needed?** | YES -- `generate_id(counter: Counter, audit: AuditLog) -> int` with dependency injection for testability. |
| **Rename needed?** | OPTIONAL -- Name is acceptable if side effects are documented. |
| **Contract test needed?** | YES -- Test asserting sequential calls produce unique IDs; test asserting audit log is written; test asserting counter increment. |
| **Documentation needed?** | YES -- Document all side effects in docstring. Add warning about test environment usage. |
| **Prerequisites before reuse** | 1. Create injectable wrapper. 2. Add contract tests for side effects. 3. Update test fixtures to use injectable version. |
| **Risk if ignored** | High -- Test pollution from global state; missing audit entries if side effect is accidentally removed in refactoring. |

---

### Recommendation 3: `ConfigManager.get_allowed_hosts()`

| Aspect | Detail |
|--------|--------|
| **Reuse decision** | **Level B** -- Reuse with wrapper |
| **Rationale** | Configuration management logic is correct. Returns mutable internal reference, allowing external code to bypass validation and modify security-critical state. |
| **Guardrail** | Callers MUST NOT modify the returned list. Defensive copy should be enforced at the source. |
| **Wrapper needed?** | YES -- Fix at source: change `return self._allowed_hosts` to `return list(self._allowed_hosts)`. Alternatively, return `tuple` for immutability. |
| **Rename needed?** | NO -- Name accurately describes the function's purpose. |
| **Contract test needed?** | YES -- Test asserting that modifying the returned collection does not affect subsequent calls to `get_allowed_hosts()`. |
| **Documentation needed?** | YES -- Add note that returned value is a copy (after fix) and should not be cached for long periods. |
| **Prerequisites before reuse** | 1. Fix mutable sharing in source. 2. Add mutation isolation contract test. |
| **Risk if ignored** | Critical -- External code can inject arbitrary hosts into the allow list, creating a security vulnerability. |

---

### Recommendation N: [Function/Module name]

| Aspect | Detail |
|--------|--------|
| **Reuse decision** | **Level [A-E]** -- [Verdict] |
| **Rationale** | [Evidence-based justification] |
| **Guardrail** | [What callers must do or avoid] |
| **Wrapper needed?** | YES/NO -- [Description if yes] |
| **Rename needed?** | YES/NO/RECOMMENDED -- [Description if yes] |
| **Contract test needed?** | YES/NO -- [Description if yes] |
| **Documentation needed?** | YES/NO -- [Description if yes] |
| **Prerequisites before reuse** | [Ordered list of actions before reuse is safe] |
| **Risk if ignored** | [Severity] -- [Description of what happens] |

---

## Implementation Plan

### Phase 1: Immediate (Before Feature Development Starts)

| # | Action | Owner | Target Date | Dependencies |
|---|--------|-------|:-----------:|-------------|
| 1 | Create `round_to_decimal()` wrapper | | | None |
| 2 | Add return type contract test for `keepTwoDecimal` | | | Action 1 |
| 3 | Fix mutable sharing in `get_allowed_hosts()` | | | None |
| 4 | Add mutation isolation contract test | | | Action 3 |

### Phase 2: During Feature Development

| # | Action | Owner | Target Date | Dependencies |
|---|--------|-------|:-----------:|-------------|
| 5 | Create injectable `generate_id()` wrapper | | | None |
| 6 | Add side effect contract tests for `getNextId` | | | Action 5 |
| 7 | Integrate all wrappers into new feature code | | | Actions 1-6 |

### Phase 3: Post-Implementation

| # | Action | Owner | Target Date | Dependencies |
|---|--------|-------|:-----------:|-------------|
| 8 | Rename `keepTwoDecimal` -> `format_two_decimal` (codebase-wide) | | | All callers updated |
| 9 | Document all hidden contracts in team knowledge base | | | Investigation complete |
| 10 | Schedule contract test review for next quarter | | | Actions 2,4,6 committed |

---

## Acceptance Criteria

The investigation is complete and reuse is approved when:

- [ ] All Level A-C reuse candidates have contract tests committed to the test suite
- [ ] All wrapper/adapter code is implemented and tested
- [ ] All Critical and High severity risks in the Risk Register have mitigations in progress
- [ ] Adoption recommendations have been reviewed by the tech lead
- [ ] Implementation plan has assigned owners and target dates
- [ ] Documentation updates are drafted (docstrings, knowledge base, caller guide)

---

## Stakeholder Sign-off

| Role | Name | Decision | Date |
|------|------|----------|------|
| Tech Lead | | Approve / Reject / Modify | |
| Feature Owner | | Approve / Reject / Modify | |
| QA Lead | | Approve / Reject / Modify | |

---

## Notes

- Revisit this recommendation if the target code is modified before reuse occurs (contracts may have changed)
- Schedule a follow-up investigation if any Level D candidates remain undecided after contract testing
- Contract tests are the primary long-term artifact -- ensure they remain in CI and are not deleted during test cleanup
