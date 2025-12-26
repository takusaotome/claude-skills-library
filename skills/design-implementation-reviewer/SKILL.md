---
name: design-implementation-reviewer
description: Use this skill for critical code review that focuses on whether the code actually works correctly and achieves the expected results - not just whether it matches a design document. This skill assumes designs can be wrong, finds bugs the design didn't anticipate, and verifies end-to-end correctness. Triggers include "critical code review", "deep code review", "verify this implementation works", "find bugs in this code", or reviewing implementation against requirements. NOTE - Security review is OUT OF SCOPE; use a dedicated security review skill for that purpose.
---

# Critical Code Reviewer

> **IMPORTANT: Always use `ultrathink` mode when performing reviews with this skill.**

## Scope

This skill covers **general-purpose code review** focusing on correctness, logic, and goal achievement.

**In Scope:**
- Code correctness, logic errors, type safety
- Data flow, execution flow, function wiring
- Concurrency, idempotency, transaction boundaries
- Resource management, timeouts, retry logic
- API contracts, backward compatibility
- Goal achievement and design gap analysis

**Out of Scope:**
- Security vulnerabilities (SQL injection, XSS, auth bypass, etc.) → Use dedicated security review skill
- If security concerns are observed during review, note them briefly and recommend a separate security review.

## Before You Start

**Required Reading:** Before starting any review, read these references:
1. `references/review_checklist.md` - Structured checklist for systematic review
2. `references/common_gaps.md` - Common defect patterns and detection strategies

## Philosophy

> **The goal is working code that achieves expected results, not code that matches a design document.**

Design documents are references, not truth. They can be:
- Incomplete (missing edge cases)
- Incorrect (wrong assumptions)
- Outdated (requirements changed)
- Ambiguous (multiple interpretations)

This skill reviews code critically to find:
1. Bugs and defects in the code itself
2. Gaps between code and actual requirements
3. Problems the design document missed
4. Issues that only appear with real data

## Three-Layer Review Framework

```
┌─────────────────────────────────────────┐
│  Layer 3: GOAL ACHIEVEMENT              │
│  "Does this achieve the expected result?"│
├─────────────────────────────────────────┤
│  Layer 2: EXECUTION FLOW                │
│  "Does this run correctly end-to-end?"  │
├─────────────────────────────────────────┤
│  Layer 1: CODE QUALITY                  │
│  "Is there a bug in this code?"         │
└─────────────────────────────────────────┘
```

**Review order: Layer 1 → Layer 2 → Layer 3**
(Fix bugs before checking flow; fix flow before checking goals)

> **CRITICAL:** Always scan ALL three layers completely. Do not stop early even if issues are found in Layer 1. Document findings as you go, then continue to the next layer.

---

## Layer 1: Code Quality Review

### 1.1 Type Safety

**Check for type mismatches:**

```python
# BUG: Comparing string to int
if order_id == 1234:  # order_id might be "1234" (string)

# BUG: Float equality
if amount == 100.0:  # Float comparison is unreliable

# BUG: None in arithmetic
total = price * quantity  # Either could be None
```

**Detection questions:**
- What types can this variable actually contain?
- What happens if the type is unexpected?
- Are comparisons type-safe?

### 1.2 Null/NaN Handling

**Check for null propagation:**

```python
# BUG: NaN propagates silently
df['result'] = df['a'] + df['b']  # If either is NaN, result is NaN

# BUG: None in string operation
name.lower()  # Crashes if name is None

# BUG: Empty collection
items[0]  # Crashes if items is empty
```

**Detection questions:**
- What if this value is None/NaN/empty?
- Does the code check before using?
- How does null propagate through the pipeline?

### 1.3 Edge Cases

**Always check:**

| Edge Case | Question |
|-----------|----------|
| Empty | What if the list/DataFrame is empty? |
| Single | What if there's exactly one item? |
| Duplicate | What if values are duplicated? |
| Boundary | What about 0, -1, MAX_INT? |
| Special chars | What about spaces, unicode, newlines? |
| Missing | What if expected data is missing? |

### 1.4 Logic Errors

**Check for common mistakes:**

```python
# BUG: Off-by-one
for i in range(len(items) - 1):  # Misses last item?

# BUG: Wrong operator
if a and b:  # Should it be "or"?

# BUG: Inverted condition
if not is_valid:
    process()  # Should this be "if is_valid"?

# BUG: Assignment vs comparison
if result = calculate():  # SyntaxError in Python, but...
```

### 1.5 Exception Paths

**Check error handling:**

```python
# BUG: Swallowed exception
try:
    risky_operation()
except Exception:
    pass  # All errors silently ignored

# BUG: Wrong exception type
except ValueError:  # But KeyError is raised

# BUG: No error handling
data = load_file(path)  # What if file doesn't exist?
```

---

## Layer 2: Execution Flow Review

### 2.1 Function Wiring

**For each important function, verify:**

```markdown
□ Function is defined
□ Function is called (not dead code)
□ Called with correct arguments (not None/placeholder)
□ Return value is captured and used
□ Called in correct order (dependencies satisfied)
```

**Red flags:**

```python
# Dead function
def important_helper():  # Defined but never called
    ...

# Placeholder arguments
process(data, config=None, lookup=None)  # Always None

# Ignored return
validate(data)  # Return value discarded
process(data)   # Proceeds regardless
```

### 2.2 Data Flow Tracing

**Trace data from input to output:**

```
Input → Transform A → Transform B → Join → Output
  ↓         ↓            ↓          ↓        ↓
 Check    Check        Check      Check    Check
```

**At each step, verify:**
- Data shape (columns, rows)
- Data types
- Value ranges
- Null presence

### 2.3 Join/Merge Correctness

**Critical checks for every join:**

```python
# Check 1: Key types match
left['key'].dtype == right['key'].dtype

# Check 2: Key normalization symmetric
left['key'] = normalize(left['key'])
right['key'] = normalize(right['key'])  # Both sides!

# Check 3: Join type appropriate
df.merge(..., how='left')  # Should it be inner? outer?

# Check 4: Duplicate keys handled
# 1:1? 1:N? N:M? What's expected?
```

### 2.4 Order Dependencies

**Check execution order:**

```python
# BUG: Use before create
df['full'] = df['first'] + df['last']
df['first'] = clean(df['first'])  # Too late!

# BUG: Overwrite before use
df['status'] = map_status(df['status'])  # Original lost
if df['status'] == 'ORIGINAL':  # Never matches
```

### 2.5 Concurrency & Race Conditions

**Check for concurrent access issues:**
- Shared mutable state without synchronization
- Time-of-check to time-of-use (TOCTOU) bugs
- Lost updates in read-modify-write patterns

### 2.6 Idempotency

**Verify operations can be safely retried:**
- Is the operation idempotent? If not, what happens on retry?
- Are there side effects that compound on retry?
- Is there a unique key or deduplication mechanism?

### 2.7 Transaction Boundaries

**Check transaction scope:**
- Are related operations in the same transaction?
- What happens on partial failure?
- Are commits/rollbacks handled correctly?

### 2.8 Resource Management

**Check resource lifecycle:**
- Are connections, files, locks properly closed/released?
- Are there potential resource leaks on error paths?
- Is there proper cleanup in finally blocks?

### 2.9 Timeouts & Retry Logic

**Check timeout handling:**
- Are there timeouts for external calls?
- Is retry logic correct (backoff, max attempts)?
- What happens when timeout/retry is exhausted?

### 2.10 API Contracts & Backward Compatibility

**Check API boundaries:**
- Are input/output contracts documented and enforced?
- Does the change break existing callers?
- Are default values safe for existing clients?

---

## Layer 3: Goal Achievement Review

### 3.1 Expected Results Definition

**Before reviewing, clarify:**

```markdown
What is the EXPECTED RESULT?
- Input: [describe input data]
- Output: [describe expected output]
- Success criteria: [how do we know it worked?]
```

**Do NOT rely solely on design document.** Ask:
- What does the user actually need?
- What would a correct result look like?
- How would we verify success?

### 3.2 Real Data Validation

**Design assumptions vs reality:**

```markdown
Design assumes: "Order numbers are unique integers"
Reality check: Do they contain strings? Nulls? Duplicates?

Design assumes: "All records have addresses"
Reality check: What percentage actually have addresses?

Design assumes: "State is 2-letter code"
Reality check: Does data contain full names? Typos?
```

**Verification approach:**
```python
# Profile the actual data
df['column'].value_counts()
df['column'].isna().sum()
df['column'].dtype
df['column'].str.len().describe()
```

### 3.3 Success Rate Analysis

**Quantify outcomes:**

```markdown
□ What percentage of records are processed successfully?
□ What percentage fail or are skipped?
□ Is the success rate acceptable for the goal?
```

**Example:**
```
Design goal: "Match opportunities to properties by address"
Implementation: Address matching function exists ✓
Actual result: 5% match rate
Verdict: Goal NOT achieved (even though implementation is "correct")
```

### 3.4 End-to-End Verification

**Trace a specific record through the entire pipeline:**

```markdown
Test Record: Order #12345
1. Input stage: Present? Values correct?
2. Transform A: Applied correctly?
3. Transform B: Applied correctly?
4. Join: Matched to correct record?
5. Output: Final result correct?
```

### 3.5 Design Document Critique

**Evaluate the design itself:**

```markdown
□ Does the design address all requirements?
□ Are the assumptions in the design valid?
□ What edge cases did the design miss?
□ What would make this design fail?
```

**Output design issues found:**
```markdown
### Design Gap: [description]
The design assumes X, but the actual data shows Y.
Recommendation: Update design to handle Y.
```

---

## Critical Thinking Techniques

### Technique 1: Assume It's Broken

Start with the assumption that the code has bugs. Your job is to find them.

**Questions to ask:**
- What could go wrong here?
- What input would break this?
- What assumption might be false?

### Technique 2: Trace the Unhappy Path

```markdown
For each operation, ask:
- What if it fails?
- What if the result is empty?
- What if the result is unexpected?
```

### Technique 3: The "Five Whys" for Bugs

When you find something suspicious:
```
1. Why is this value None? → Because the lookup failed
2. Why did the lookup fail? → Because the key wasn't found
3. Why wasn't the key found? → Because normalization differs
4. Why does normalization differ? → Left side normalized, right not
5. Why only left side? → Developer forgot right side
```

### Technique 4: Boundary Testing

For any numeric operation:
```markdown
Test with: 0, 1, -1, very large, very small
Test with: empty, single item, many items
Test with: null, empty string, whitespace
```

### Technique 5: Data Shape Verification

At each pipeline stage, verify:
```python
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Nulls: {df.isna().sum()}")
print(f"Sample:\n{df.head()}")
```

---

## Review Output Format

### Output Structure

Reviews MUST be structured in this order:
1. **Review Scope / Assumptions / Unknowns** (defines what was reviewed)
2. **Findings** (Critical → High → Medium → Low)
3. **Open Questions** (if any remain after review)

> **Rationale:** Declaring scope first prevents omissions - reviewers explicitly state what was/wasn't examined before listing findings.

### Review Scope Template

```markdown
## Review Scope

**Files Reviewed:**
- file1.py (lines X-Y)
- file2.py (full)

**Assumptions Made:**
- [Assumption 1 - e.g., "Assuming single-threaded execution"]
- [Assumption 2]

**Unknowns / Not Verified:**
- [Unknown 1 - e.g., "Database isolation level not confirmed"]
- [Unknown 2]

**Out of Scope:**
- Security review (recommend separate security audit)
```

### Finding Template

```markdown
## [Layer] Finding: [Short Description]

**Severity:** Critical / High / Medium / Low

**Location:** file.py:123

**Problem:**
[What is wrong]

**Evidence:**
[Code snippet or data showing the problem]

**Impact:**
[What fails or produces wrong results]

**Root Cause:**
[Why this happened]

**Fix:**
[How to correct it]

**Test Plan (required for Critical/High):**
[How to verify the fix works - specific test cases or verification steps]

**Design Gap (if applicable):**
[What the design missed or got wrong]
```

> **NOTE:** For Critical and High severity findings, the **Test Plan** field is mandatory. Provide specific test cases or verification steps.

### Severity Definitions

| Severity | Definition | Test Plan |
|----------|------------|-----------|
| Critical | Code will crash or produce completely wrong results | Required |
| High | Significant portion of data affected incorrectly | Required |
| Medium | Edge cases mishandled or minor data issues | Optional |
| Low | Style, performance, or maintainability issues | Optional |

### Open Questions Template

```markdown
## Open Questions

- [Question 1 - e.g., "What is the expected behavior when X?"]
- [Question 2]
```

---

## Review Checklist Summary

### Pre-Review
```markdown
□ Read references/review_checklist.md
□ Read references/common_gaps.md
□ Define expected result (input → output → success criteria)
```

### Layer 1: Code Quality
```markdown
□ Type safety verified
□ Null/NaN handling checked
□ Edge cases considered
□ Logic correctness verified
□ Exception paths reviewed
```

### Layer 2: Execution Flow
```markdown
□ All functions actually called (not dead code)
□ Arguments are real values (not None/placeholder)
□ Return values captured and used
□ Data flows correctly through pipeline
□ Joins are correct (types, normalization, cardinality)
□ Order dependencies satisfied
□ Concurrency/race conditions checked
□ Idempotency verified
□ Transaction boundaries correct
□ Resources properly managed (no leaks)
□ Timeouts and retry logic verified
□ API contracts and backward compatibility checked
```

### Layer 3: Goal Achievement
```markdown
□ Expected result clearly defined
□ Real data validated against assumptions
□ Success rate quantified and acceptable
□ End-to-end trace verified
□ Design gaps identified
```

### Post-Review
```markdown
□ Critical/High findings include Test Plan
□ Review Scope/Assumptions/Unknowns documented
□ Security concerns noted for separate review (if any)
```

---

## Usage

```bash
# Invoke the skill (always uses ultrathink mode)
/design-implementation-reviewer

# Or with natural language
"Critically review this implementation - find bugs, not just design mismatches"
"Does this code actually work? Check everything."
"Review this code assuming it has bugs - find them"
```

> **Reminder:** This skill always uses `ultrathink` mode for thorough analysis. Security review is out of scope - recommend a dedicated security review skill if security concerns are observed.

## Key Mindset

1. **Skepticism**: Assume both code AND design can be wrong
2. **Empiricism**: Verify with actual data, not just logic
3. **Completeness**: Check all paths, not just happy path
4. **Pragmatism**: Goal is working code, not matching documents
5. **Curiosity**: Ask "what if?" constantly
