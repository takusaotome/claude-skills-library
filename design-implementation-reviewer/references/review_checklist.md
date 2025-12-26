# Critical Code Review Checklist

> **Note:** This checklist supports general-purpose code review. Security review is out of scope - use a dedicated security review checklist for that purpose.

## Pre-Review: Preparation

```markdown
□ References loaded (review_checklist.md, common_gaps.md)
□ Using ultrathink mode for thorough analysis

## Expected Results (fill before reviewing)

**What should this code do?**
_______________________________________

**What is the input?**
_______________________________________

**What is the expected output?**
_______________________________________

**How do we know it succeeded?**
_______________________________________
```

---

## Layer 1: Code Quality

### 1.1 Type Safety
```markdown
□ All comparisons are type-safe
□ No implicit type coercion issues
□ Numeric types handled correctly (int/float/str)
□ Boolean conditions are explicit

Issues found:
- [ ] _______________________________________
```

### 1.2 Null/NaN Handling
```markdown
□ All potential None values checked before use
□ NaN propagation considered in calculations
□ Empty collections checked before access
□ Default values are appropriate (not masking bugs)

Issues found:
- [ ] _______________________________________
```

### 1.3 Edge Cases
```markdown
□ Empty input handled
□ Single-item input handled
□ Duplicate values handled
□ Boundary values tested (0, -1, max)
□ Special characters handled (space, unicode)
□ Missing/optional data handled

Issues found:
- [ ] _______________________________________
```

### 1.4 Logic Correctness
```markdown
□ No off-by-one errors
□ Operators correct (and/or, ==/>=/<=)
□ Conditions not inverted
□ Loop bounds correct
□ Early returns don't skip needed processing

Issues found:
- [ ] _______________________________________
```

### 1.5 Exception Handling
```markdown
□ Exceptions not silently swallowed
□ Correct exception types caught
□ Resources cleaned up on error
□ Error messages are useful

Issues found:
- [ ] _______________________________________
```

---

## Layer 2: Execution Flow

### 2.1 Function Wiring
```markdown
For each key function:

| Function | Defined? | Called? | Args OK? | Return used? |
|----------|----------|---------|----------|--------------|
|          | □        | □       | □        | □            |
|          | □        | □       | □        | □            |
|          | □        | □       | □        | □            |

Dead functions found:
- [ ] _______________________________________

Placeholder arguments found:
- [ ] _______________________________________
```

### 2.2 Data Flow
```markdown
□ Data shape preserved correctly through pipeline
□ Column names match at each handoff
□ Data types consistent through transformations
□ No unintended data loss

Trace path:
Input → _______ → _______ → _______ → Output
        □         □         □
```

### 2.3 Join/Merge Correctness
```markdown
For each join:

| Join | Key types match? | Both normalized? | Cardinality? |
|------|------------------|------------------|--------------|
|      | □                | □                |              |
|      | □                | □                |              |

Issues found:
- [ ] _______________________________________
```

### 2.4 Order Dependencies
```markdown
□ Values created before used
□ Original data preserved if needed later
□ Dependencies satisfied before dependent code runs

Issues found:
- [ ] _______________________________________
```

### 2.5 Concurrency & Race Conditions
```markdown
□ No shared mutable state without synchronization
□ No time-of-check to time-of-use (TOCTOU) bugs
□ Read-modify-write operations are atomic or locked

Issues found:
- [ ] _______________________________________
```

### 2.6 Idempotency
```markdown
□ Operations can be safely retried without side effects
□ Duplicate requests handled (unique key/deduplication)
□ Side effects don't compound on retry

Issues found:
- [ ] _______________________________________
```

### 2.7 Transaction Boundaries
```markdown
□ Related operations in same transaction
□ Partial failure handled correctly
□ Commit/rollback logic correct

Issues found:
- [ ] _______________________________________
```

### 2.8 Resource Management
```markdown
□ Connections/files/locks properly closed/released
□ No resource leaks on error paths
□ Cleanup in finally blocks or context managers

Issues found:
- [ ] _______________________________________
```

### 2.9 Timeouts & Retry Logic
```markdown
□ External calls have timeouts
□ Retry logic uses backoff and max attempts
□ Exhausted retries handled gracefully

Issues found:
- [ ] _______________________________________
```

### 2.10 API Contracts & Backward Compatibility
```markdown
□ Input/output contracts documented and enforced
□ Change doesn't break existing callers
□ Default values safe for existing clients

Issues found:
- [ ] _______________________________________
```

---

## Layer 3: Goal Achievement

### 3.1 Real Data Validation
```markdown
| Assumption | Reality Check | Valid? |
|------------|---------------|--------|
|            |               | □      |
|            |               | □      |
|            |               | □      |

Data profiling commands used:
- df['col'].value_counts()
- df['col'].isna().sum()
- df['col'].dtype
```

### 3.2 Success Rate
```markdown
Total records: _______
Successfully processed: _______ (___%)
Failed/skipped: _______ (___%)

Is this acceptable? □ Yes □ No

If No, why:
_______________________________________
```

### 3.3 End-to-End Trace
```markdown
Test record: _______________________

□ Stage 1: Input present and correct
□ Stage 2: Transform A applied correctly
□ Stage 3: Transform B applied correctly
□ Stage 4: Join matched correctly
□ Stage 5: Output is correct

Issues found:
_______________________________________
```

### 3.4 Design Gaps Found
```markdown
| Design Assumption | Actual Reality | Impact |
|-------------------|----------------|--------|
|                   |                |        |
|                   |                |        |

Recommendations for design update:
_______________________________________
```

---

## Findings Summary

| # | Layer | Severity | Description | Location | Test Plan? |
|---|-------|----------|-------------|----------|------------|
| 1 |       |          |             |          | □          |
| 2 |       |          |             |          | □          |
| 3 |       |          |             |          | □          |
| 4 |       |          |             |          | □          |
| 5 |       |          |             |          | □          |

> **Reminder:** Critical and High severity findings MUST include a Test Plan.

---

## Review Scope & Assumptions

```markdown
**Files Reviewed:**
- _______________________________________
- _______________________________________

**Assumptions Made:**
- _______________________________________

**Unknowns / Not Verified:**
- _______________________________________

**Security Concerns (for separate review):**
- _______________________________________
```

---

## Verification Commands

```bash
# Find function definitions
grep -n "def function_name" file.py

# Find function calls
grep -n "function_name(" file.py | grep -v "def "

# Find None arguments
grep -n "=None" file.py

# Find all column references
grep -oE "\['[^']+'\]" file.py | sort | uniq

# Profile data
python -c "import pandas as pd; df=pd.read_excel('file.xlsx'); print(df.info())"
```

---

## Sign-Off

```markdown
Reviewer: _______________________
Date: ___________________________

Review confidence:
□ High - Thorough review, all layers checked
□ Medium - Key paths checked, some areas not verified
□ Low - Quick review, more verification needed

Outstanding concerns:
_______________________________________
```
