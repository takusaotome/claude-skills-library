# Critical Code Review Checklist

## Pre-Review: Define Expected Results

```markdown
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

| # | Layer | Severity | Description | Location |
|---|-------|----------|-------------|----------|
| 1 |       |          |             |          |
| 2 |       |          |             |          |
| 3 |       |          |             |          |
| 4 |       |          |             |          |
| 5 |       |          |             |          |

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
