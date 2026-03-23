# Reuse Risk Classification

## Purpose

This reference defines the 5-level framework for classifying the reuse feasibility of existing code assets. Each level specifies the verdict, required actions, and decision criteria. Use during Workflow 5 (Reuse Feasibility Judgment) to produce consistent, evidence-based reuse recommendations.

---

## Classification Framework Overview

| Level | Verdict | One-Line Meaning | Typical Action Cost |
|-------|---------|-------------------|---------------------|
| **A** | Reuse as-is | Contracts match expectations, behavior is verified | Low: add contract test only |
| **B** | Reuse with wrapper | Core logic is correct, interface needs thin adaptation | Low-Medium: build wrapper + contract test |
| **C** | Reuse with adapter | Logic is sound but interface mismatch is significant | Medium: build adapter layer + integration test |
| **D** | Contract test required first | Behavior is uncertain, cannot decide without verification | Variable: write tests, then re-evaluate |
| **E** | Do not reuse / redesign | Fundamental mismatch or unacceptable hidden risk | High: implement from scratch or redesign |

---

## Level A: Reuse As-Is

### Decision Criteria

All of the following must be true:

1. **Name-behavior alignment**: The function name accurately describes what it does
2. **Type correctness**: Return type matches caller expectations (verified against implementation, not just annotation)
3. **Side effect transparency**: All side effects are documented and acceptable for the new use case
4. **No environment dependency**: Behavior is consistent across dev, staging, and production environments
5. **Test coverage exists**: Existing tests cover the code paths the new feature will exercise
6. **No mutable sharing risk**: Returned values are not references to internal mutable state

### Required Actions

- [ ] Add a **contract test** that explicitly asserts the behavioral contract the new caller depends on
- [ ] Document the contract dependency in the new feature's design notes
- [ ] Set up monitoring for contract test regression

### Example Scenario

```
Target: utils.calculate_tax(amount: Decimal, rate: Decimal) -> Decimal
Investigation findings:
  - Name accurately describes behavior
  - Returns Decimal as annotated
  - No side effects
  - Test coverage: 15 tests including edge cases
  - Works identically in all environments
Decision: Level A -- Reuse as-is
Action: Add contract test asserting return type is Decimal and value = amount * rate
```

---

## Level B: Reuse with Wrapper

### Decision Criteria

All of the following are true:

1. **Core logic is correct**: The function does what it should at its core
2. **Interface mismatch is thin**: Return type needs conversion, parameter order is awkward, or naming is misleading -- but the fix is a simple wrapper
3. **Side effects are acceptable**: Any side effects are known and tolerable
4. **No fundamental design flaw**: The function's approach is sound

AND at least one of these is true:

5. Return type needs conversion (e.g., string to number)
6. Parameters need reordering or default value adjustment
7. Function name is misleading and should be aliased
8. Error handling needs standardization (e.g., None -> raise exception)

### Required Actions

- [ ] Build a **thin wrapper function** that adapts the interface
- [ ] Name the wrapper to accurately reflect the contract the new caller depends on
- [ ] Add a **contract test** for the wrapper (tests the adapted interface)
- [ ] Document why direct use is discouraged (prevent future callers from skipping the wrapper)
- [ ] Consider deprecating direct access to the wrapped function if appropriate

### Wrapper Design Guidelines

The wrapper should:
- Have a clear, contract-accurate name
- Convert types at the boundary (e.g., `str` return -> `Decimal` return)
- Standardize error handling (e.g., convert `None` returns to explicit exceptions)
- NOT re-implement the core logic (that defeats the purpose of reuse)

```python
# BAD wrapper: re-implements logic
def get_tax_amount(amount, rate):
    return amount * rate  # Duplicates logic

# GOOD wrapper: adapts interface
def get_tax_as_decimal(amount: Decimal, rate: Decimal) -> Decimal:
    raw = legacy_calculate_tax(amount, rate)  # Reuses core logic
    if isinstance(raw, str):
        return Decimal(raw.replace(",", ""))
    return Decimal(raw)
```

### Example Scenario

```
Target: keepTwoDecimal(value) -> str  (returns "1,234.56")
Investigation findings:
  - Name suggests numeric operation, but returns formatted string
  - Core rounding logic is correct
  - No side effects
  - 3 callers exist: 2 display the string, 1 does arithmetic (bug source)
Decision: Level B -- Reuse with wrapper
Action: Create round_to_two_decimals(value) -> Decimal wrapper
  that calls keepTwoDecimal internally and strips formatting
```

---

## Level C: Reuse with Adapter

### Decision Criteria

1. **Core logic is sound**: The algorithm/business logic is correct and valuable
2. **Interface mismatch is significant**: Multiple parameters, return structure, or error model need adaptation
3. **Integration contract is complex**: The adapter must handle state management, initialization sequence, or resource lifecycle
4. **Reimplementation cost is high**: The logic is complex enough that wrapping is cheaper than rewriting

AND at least one of these is true:

5. The function requires specific initialization or teardown
6. The function's error model is incompatible with the new caller's expectations
7. The function operates on a different data model than the caller uses
8. Multiple functions must be composed to fulfill the new caller's contract

### Required Actions

- [ ] Design an **adapter layer** (class or module) that provides the new caller's expected interface
- [ ] Map data models between the caller's domain and the target's domain
- [ ] Standardize error handling across the adapter boundary
- [ ] Add **integration tests** that exercise the adapter with realistic data
- [ ] Add **contract tests** for each critical contract the adapter exposes
- [ ] Document the adapter's own contracts explicitly (the adapter is itself a new code asset)

### Adapter Design Guidelines

- Use the Adapter pattern: separate interface translation from business logic
- Keep the adapter stateless if possible
- Make the adapter's dependency on the target explicit (constructor injection)
- Version the adapter if the target's interface is expected to change

### Example Scenario

```
Target: LegacyReportGenerator class (generates PDF reports)
Investigation findings:
  - Report logic is correct and complex (2000+ lines)
  - Requires 5-step initialization sequence
  - Returns file path as string, but new system needs byte stream
  - Error handling via return codes, new system uses exceptions
  - Uses module-level config, new system uses dependency injection
Decision: Level C -- Reuse with adapter
Action: Create ReportAdapter class that:
  - Handles initialization in constructor
  - Converts file path return to byte stream
  - Translates return codes to exceptions
  - Accepts config via constructor injection
```

---

## Level D: Contract Test Required First

### Decision Criteria

At least one of the following is true:

1. **Insufficient evidence**: Cannot determine behavior from code, tests, or callers alone
2. **Conflicting evidence**: Tests suggest one contract, callers assume another, code does a third
3. **Complex branching**: Too many conditional paths to reason about without execution
4. **Environment-dependent behavior**: Behavior may differ across environments but not yet verified
5. **No existing tests**: Cannot rely on test-verified contracts

### Required Actions

- [ ] Design and execute **contract tests** for the specific behaviors the new caller depends on
- [ ] Execute tests in multiple environments if environment dependency is suspected
- [ ] Record all findings in the Implicit Contract Sheet
- [ ] **Re-evaluate**: After testing, reclassify as Level A, B, C, or E

### Contract Test Design for Level D

Focus tests on answering specific unknowns:

```
Unknown: "Does get_price() return cents or dollars?"
Test: assert get_price(item_costing_1234_cents) in (1234, 12.34)
     -> reveals unit contract

Unknown: "Does save_order() commit the transaction?"
Test: save_order(order); check if rollback is possible
     -> reveals commit contract

Unknown: "Does format_date() handle timezone-naive input?"
Test: format_date(datetime(2025, 1, 1))  # naive
     -> reveals timezone contract (error or assumption)
```

### Escalation Path

If contract tests reveal:
- Contract matches expectations -> Reclassify as **Level A**
- Contract needs thin adaptation -> Reclassify as **Level B**
- Contract needs significant adaptation -> Reclassify as **Level C**
- Contract is fundamentally incompatible -> Reclassify as **Level E**

---

## Level E: Do Not Reuse / Redesign

### Decision Criteria

At least one of the following is true:

1. **Fundamental type mismatch**: The function returns a fundamentally different type than needed, and wrapping would be fragile
2. **Unacceptable side effects**: The function has side effects that cannot be tolerated in the new context
3. **Tight coupling**: The function is tightly coupled to a specific context that cannot be adapted
4. **State corruption risk**: Using the function introduces risk of corrupting shared state
5. **Maintenance hazard**: The function is so poorly structured that any adapter would be more complex than a clean rewrite
6. **Security or compliance concern**: The function handles data in ways that violate requirements

### Required Actions

- [ ] Document the specific reasons reuse is rejected (evidence-based, not opinion)
- [ ] Extract any reusable **ideas** from the target (algorithms, business rules) without reusing the code itself
- [ ] Design the replacement with explicit contracts from the start
- [ ] Add contract tests for the replacement that cover the same failure modes found during investigation
- [ ] Consider whether the original code should be deprecated or refactored (organizational improvement)

### Example Scenario

```
Target: generate_invoice_pdf(order_id)
Investigation findings:
  - Queries DB directly (not through repository layer)
  - Modifies order status as a side effect of generation
  - Hardcodes company name and tax rate
  - Catches all exceptions and returns empty PDF
  - No tests exist
  - Used by 1 caller that compensates for the status mutation
Decision: Level E -- Do not reuse
Reason: Side effects are unacceptable, exception swallowing hides failures,
  and adapting would require more code than reimplementing
Action: Reimplement invoice generation with clean contracts,
  extract tax calculation logic as a separate, reusable function
```

---

## Decision Flow

Use this decision tree when the level is not immediately obvious:

```
Start: Is the target's behavior fully understood?
  NO  -> Level D (test first, then re-evaluate)
  YES -> Continue

Does the name accurately describe the behavior?
  AND return type matches expectations?
  AND no unacceptable side effects?
  AND tests exist?
    ALL YES -> Level A (reuse as-is)
    SOME NO -> Continue

Is the mismatch thin (type conversion, naming, error model)?
  YES -> Level B (wrapper)
  NO  -> Continue

Is the core logic sound despite significant interface mismatch?
  YES -> Level C (adapter)
  NO  -> Level E (do not reuse)
```

---

## Risk Register Integration

For each Level B-E classification, add an entry to the Reuse Risk Register (`assets/reuse_risk_register_template.md`) with:

- The specific risks identified during investigation
- The failure mode if the risk materializes
- The severity and likelihood ratings
- The mitigation strategy (wrapper, adapter, contract test, or reimplementation)
- The owner responsible for implementing the mitigation

Level A assets only need a contract test entry -- no risk register entry is required unless specific edge cases were noted during investigation.
