# Contract Test Ideas

## Investigation Metadata

| Field | Value |
|-------|-------|
| **Investigation ID** | HCI-YYYYMMDD-NNN |
| **Target System** | [System / module name] |
| **Investigator** | [Name] |
| **Date** | [YYYY-MM-DD] |
| **Status** | Draft / In Review / Final |

---

## What is a Contract Test?

A contract test verifies the **interface promise** of a function, module, or service -- not its internal logic. Contract tests answer: "Does this code still behave the way its consumers expect?" They are the primary long-term deliverable of a hidden contract investigation.

### Contract Test vs. Unit Test

| Aspect | Contract Test | Unit Test |
|--------|--------------|-----------|
| **Tests** | Interface promise (return type, side effects, error behavior) | Internal logic correctness |
| **Named after** | The contract being protected | The function being tested |
| **Breaks when** | The behavioral contract changes | The implementation changes |
| **Value** | Prevents integration failures from hidden contract drift | Prevents logic bugs |

---

## Contract Test Register

### Test Idea 1: Return Type Contract -- `keepTwoDecimal()`

| Field | Value |
|-------|-------|
| **Contract to verify** | `keepTwoDecimal()` returns a `str` (not a numeric type). Any new caller performing arithmetic must be aware of this. |
| **Minimal test** | `assert isinstance(keepTwoDecimal(1234.5), str)` |
| **Data set** | `[0, 1234.5, -99.999, 0.1, 999999.99, None]` |
| **Failure signal** | If this test fails, the function's return type has changed -- all callers wrapping with `Decimal()` or `float()` need review. |
| **Regression value** | Prevents future developers from assuming numeric return. Catches if someone "fixes" the function to return numeric without updating callers. |
| **Connected mismatch** | Implicit Contract Sheet Subject 1, Risk R-001 |
| **Priority** | Highest -- Critical severity, High likelihood |

```python
import pytest
from utils import keepTwoDecimal

class TestKeepTwoDecimalContract:
    """Contract tests for keepTwoDecimal return type and format."""

    def test_return_type_is_string(self):
        """Contract: return value is always str, never numeric."""
        result = keepTwoDecimal(1234.5)
        assert isinstance(result, str)

    def test_return_contains_comma_formatting(self):
        """Contract: values >= 1000 include comma separators."""
        result = keepTwoDecimal(1234.5)
        assert "," in result

    def test_return_has_two_decimal_places(self):
        """Contract: always exactly 2 decimal places."""
        result = keepTwoDecimal(1.1)
        assert result.endswith(".10") or result.split(".")[-1] == "10"

    @pytest.mark.parametrize("input_val", [0, 1234.5, -99.999, 999999.99])
    def test_all_inputs_return_string(self, input_val):
        """Contract: string return holds for all valid numeric inputs."""
        result = keepTwoDecimal(input_val)
        assert isinstance(result, str)

    def test_none_input_behavior(self):
        """Contract: None input raises ValueError (not silent failure)."""
        with pytest.raises((ValueError, TypeError)):
            keepTwoDecimal(None)
```

---

### Test Idea 2: Side Effect Isolation Contract -- `getNextId()`

| Field | Value |
|-------|-------|
| **Contract to verify** | `getNextId()` mutates global state (`_counter`) and writes to audit log on every call. |
| **Minimal test** | Call twice, verify counter incremented twice and audit log has 2 entries. |
| **Data set** | N/A (stateful operation; test sequence matters) |
| **Failure signal** | If counter does not increment, internal state contract has changed. If audit log entry is missing, side effect was removed (callers depending on audit trail are affected). |
| **Regression value** | Makes the side effects visible and explicit. Catches refactoring that accidentally removes audit logging. |
| **Connected mismatch** | Risk R-002 |
| **Priority** | High -- Side effects affect test isolation and audit compliance |

```python
class TestGetNextIdContract:
    """Contract tests for getNextId side effects."""

    def test_sequential_calls_produce_different_ids(self):
        """Contract: each call returns a new, different ID."""
        id1 = getNextId()
        id2 = getNextId()
        assert id1 != id2

    def test_call_increments_global_counter(self):
        """Contract: global _counter is mutated on each call."""
        import module_under_test
        before = module_under_test._counter
        getNextId()
        after = module_under_test._counter
        assert after == before + 1

    def test_call_writes_audit_log(self, mock_audit_log):
        """Contract: audit log is written on each call."""
        getNextId()
        assert mock_audit_log.record.called
```

---

### Test Idea 3: Mutable Sharing Contract -- `ConfigManager.get_allowed_hosts()`

| Field | Value |
|-------|-------|
| **Contract to verify** | `get_allowed_hosts()` returns a reference to internal list (not a copy). Modifying the return value modifies internal state. |
| **Minimal test** | `hosts = cm.get_allowed_hosts(); hosts.append("x"); assert "x" in cm.get_allowed_hosts()` |
| **Data set** | N/A (tests mutation behavior) |
| **Failure signal** | If mutation test fails after a fix, the function now returns a copy (desired behavior). If it passes, the mutable sharing contract still holds (dangerous). |
| **Regression value** | Detects whether the mutable sharing vulnerability has been fixed. Serves as a regression test to prevent reintroduction. |
| **Connected mismatch** | Risk R-003 |
| **Priority** | High -- Mutable sharing can cause security and data integrity issues |

```python
class TestGetAllowedHostsContract:
    """Contract tests for ConfigManager.get_allowed_hosts mutation behavior."""

    def test_external_mutation_does_not_affect_internal_state(self):
        """Contract: returned list should be a copy, not internal reference.
        NOTE: This test currently FAILS (documenting the existing contract).
        After fix, this test should PASS."""
        cm = ConfigManager()
        hosts = cm.get_allowed_hosts()
        hosts.append("evil.com")
        assert "evil.com" not in cm.get_allowed_hosts()
```

---

### Test Idea 4: [Contract description]

| Field | Value |
|-------|-------|
| **Contract to verify** | [Specific behavioral contract] |
| **Minimal test** | [Simplest assertion that would catch a violation] |
| **Data set** | [Input values that exercise the contract boundary] |
| **Failure signal** | [What a test failure means -- which contract broke and who is affected] |
| **Regression value** | [How this test prevents future incidents] |
| **Connected mismatch** | [Reference to Implicit Contract Sheet / Risk Register entry] |
| **Priority** | [Highest / High / Medium / Low] |

---

## Test Priority Summary

| Priority | Test Count | Description |
|----------|:----------:|-------------|
| Highest | | Critical severity mismatches that will definitely cause failures |
| High | | High severity mismatches that affect data integrity or user experience |
| Medium | | Medium severity mismatches that degrade quality but have workarounds |
| Low | | Low severity mismatches with minimal impact |

---

## Environment-Specific Tests

For environment-dependent contracts, specify which environments each test should run in:

| Test | Dev | CI | Staging | Prod-like |
|------|:---:|:--:|:-------:|:---------:|
| Return type contract | Yes | Yes | Yes | - |
| DB dialect round-trip | - | Yes | Yes | - |
| Timezone handling | Yes | Yes | Yes | - |
| Mock vs. real API | - | - | Yes | - |
| Performance contract | - | - | - | Yes |

---

## Traceability Matrix

Connect every contract test to the mismatch that motivated it:

| Test ID | Mismatch (Contract Sheet) | Risk (Risk Register) | Reuse Level |
|---------|--------------------------|---------------------|-------------|
| CT-001 | Subject 1: Return type | R-001 | B (wrapper) |
| CT-002 | Subject 2: Side effects | R-002 | B (wrapper) |
| CT-003 | Subject 3: Mutable sharing | R-003 | B (wrapper) |
| CT-004 | | | |

---

## Notes

- Contract tests should be committed to the test suite alongside the integration code
- Name test files with a `contract_` prefix (e.g., `test_contract_keep_two_decimal.py`) for easy identification
- Contract tests should fail loudly when the underlying contract changes, prompting investigation rather than silent adaptation
- Review contract tests when the target function is modified -- a passing contract test after a change confirms compatibility
