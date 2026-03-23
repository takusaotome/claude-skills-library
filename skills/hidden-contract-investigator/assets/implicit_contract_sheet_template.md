# Implicit Contract Sheet

## Investigation Metadata

| Field | Value |
|-------|-------|
| **Investigation ID** | HCI-YYYYMMDD-NNN |
| **Target System** | [System / module name] |
| **Investigator** | [Name] |
| **Date** | [YYYY-MM-DD] |
| **Status** | Draft / In Review / Final |

---

## Contract Inventory

### Notation Guide

- **Stated contract**: What the name, docs, types, and callers suggest the function does
- **Observed contract**: What the implementation actually does (verified by reading code and/or running tests)
- **Evidence**: Specific code references, test results, or observations that prove the observed contract
- **Risk**: What can go wrong if a new caller relies on the stated contract instead of the observed contract
- **Suggested usage rule**: How the new caller should use (or avoid) this function

### Contract Records

#### Subject 1: `keepTwoDecimal(value)`

| Aspect | Stated Contract | Observed Contract | Match? |
|--------|----------------|-------------------|--------|
| **Name implies** | Rounds numeric value to 2 decimal places | Formats value as comma-separated string with 2 decimals | NO |
| **Return type** | `float` (implied by name) | `str` (e.g., `"1,234.56"`) | NO |
| **Side effects** | None expected | None observed | YES |
| **Null handling** | Not documented | Raises `ValueError` on `None` input | UNKNOWN->VERIFIED |
| **Caller assumption** | Return value is usable in arithmetic | Return value causes `TypeError` in arithmetic | NO |

**Evidence**: `utils.py:42` -- `return "{:,.2f}".format(value)` returns formatted string. `test_utils.py:88` -- `assertEqual(keepTwoDecimal(1234.5), "1,234.50")` confirms string return.

**Risk**: HIGH -- Any caller performing arithmetic on the return value will get `TypeError` (string + number) or silent corruption (string concatenation instead of addition).

**Mismatch category**: Naming Mismatch, Type Mismatch

**Severity**: Critical | **Likelihood**: High

**Suggested usage rule**: NEVER use the return value in arithmetic. If numeric result is needed, wrap in a new function that strips formatting and returns `Decimal`. Consider renaming to `formatTwoDecimal()`.

---

#### Subject 2: [function/class/module name]

| Aspect | Stated Contract | Observed Contract | Match? |
|--------|----------------|-------------------|--------|
| **Name implies** | [What the name suggests] | [What the code actually does] | YES/NO |
| **Return type** | [Expected type] | [Actual type] | YES/NO |
| **Side effects** | [Expected side effects] | [Actual side effects] | YES/NO |
| **Null handling** | [Expected null behavior] | [Actual null behavior] | YES/NO |
| **Caller assumption** | [How callers use it] | [Whether that usage is safe] | YES/NO |

**Evidence**: [Code references, test results, or observations]

**Risk**: [Impact description]

**Mismatch category**: [Naming / Type / Scope / State / Environment / Hidden Side Effect]

**Severity**: Critical / High / Medium / Low | **Likelihood**: High / Medium / Low

**Suggested usage rule**: [How to safely use or avoid]

---

## Summary Table

| # | Subject | Mismatch Categories | Severity | Likelihood | Reuse Level |
|---|---------|--------------------|---------:|:-----------|:------------|
| 1 | `keepTwoDecimal(value)` | Naming, Type | Critical | High | B (wrapper) |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

---

## Unresolved Questions

| # | Question | Blocking? | Next Step |
|---|----------|:---------:|-----------|
| 1 | [Question about unclear behavior] | Yes/No | [Action to resolve] |
| 2 | | | |

---

## Notes

- All "Match? = NO" entries require further action (wrapper, adapter, contract test, or avoidance)
- "UNKNOWN->VERIFIED" means the stated contract was silent, but investigation confirmed the actual behavior
- Populate one Subject section per reuse candidate investigated
