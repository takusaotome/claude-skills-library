# Copy Propagation Review Strategy

## Purpose

This reference provides a structured approach to reviewing code that has been copied (propagated) across multiple modules. Instead of reviewing every copy with equal depth -- which dilutes reviewer attention and misses subtle differences -- this strategy focuses deep review on the canonical implementation and applies efficient diff-based review to all copies.

## The Problem with Uniform Copy Review

When the same logic is implemented in N locations (e.g., 6 transaction flows), reviewing all N implementations with the same depth has several failure modes:

1. **Attention fatigue**: By the 4th copy, the reviewer is skimming rather than reading carefully
2. **Anchoring bias**: After approving the first copy, the reviewer assumes the rest are identical
3. **Inconsistency blindness**: Small differences between copies (a missing line, a different constant, a swapped condition) become invisible when reading similar code repeatedly
4. **Time waste**: 80% of each copy is identical to the canonical; reviewing it again adds no value

## The Canonical + Diff Strategy

### Phase 1: Identify the Canonical Implementation

Select one implementation as the **canonical** -- the one that will receive full, exhaustive review. Selection criteria:

- **Most complete**: Choose the implementation that covers the most edge cases
- **Most representative**: Choose the flow that is most commonly executed in production
- **Best tested**: Choose the implementation with the strongest existing test coverage
- **First written**: Often the first implementation received the most careful attention

If these criteria conflict, prefer the most complete and most representative implementation.

### Phase 2: Full Review of Canonical

Review the canonical implementation with maximum rigor:

1. **Line-by-line code review**: Every line of the affected logic
2. **Logic verification**: Trace through the logic with concrete examples
3. **Edge case analysis**: Zero values, null inputs, maximum values, empty collections
4. **Error handling**: What happens when the operation fails partway through?
5. **Test verification**: Run existing tests; write new tests for uncovered scenarios
6. **Sign and rounding**: Verify mathematical operations produce correct results
7. **State management**: Verify preconditions, postconditions, and invariants

Document the canonical review findings as the baseline.

### Phase 3: Diff Review of Each Copy

For each non-canonical copy:

1. **Generate a diff** between the copy and the canonical implementation
   - Use `diff`, IDE comparison, or manual side-by-side reading
   - Focus on the sections that implement the changed logic, not boilerplate

2. **Classify each difference**:

   | Classification | Meaning | Action |
   |---------------|---------|--------|
   | **Allowed** | Intentional, documented variation (different entity type, field name) | Record in review template, no action needed |
   | **Suspicious** | Difference that might indicate a bug or oversight | Investigate, determine if allowed or defect |
   | **Defect** | Unintentional divergence from canonical | File bug, require fix |
   | **Missing** | Logic present in canonical but absent in copy | Determine if omission is intentional or defect |
   | **Extra** | Logic present in copy but absent in canonical | Determine if addition is flow-specific or pollution |

3. **Check required-sameness sections**: For sections that MUST be identical (calculation formulas, validation rules, rounding logic), verify byte-for-byte equivalence or semantically equivalent implementation.

4. **Document findings** in the copy propagation review template.

### Phase 4: Exception Documentation

For each copy, maintain a record of:

- **Copy identifier**: Module name, file path, function name
- **Allowed differences**: List of intentional variations with rationale
- **Detected differences**: List of differences found during diff review
- **Classification**: Each difference marked as Allowed / Suspicious / Defect / Missing / Extra
- **Resolution**: For non-Allowed differences, the action taken

This documentation serves as the audit trail and as reference material for future changes.

## Determining Allowed vs Required-Sameness Sections

### Typically Allowed to Differ
- Entity type identifiers (transaction type, document type, flow identifier)
- Database table or collection names specific to the flow
- Error messages and log messages (may reference flow-specific context)
- Event names or queue names for flow-specific events
- UI labels and display strings
- Flow-specific precondition checks (e.g., "layaway must have deposit paid" but "sale has no such check")

### Typically Required to Be Same
- Calculation formulas (tax, rounding, discount, surcharge)
- Validation logic (range checks, format validation, business rule enforcement)
- Data transformation logic (type conversion, normalization)
- Sign handling (positive for forward, negative for reverse)
- Rounding mode and precision
- Included/excluded item filters for aggregation
- Permission and visibility checks (unless role-based variation is intentional)

### Gray Areas (Require Explicit Decision)
- Error handling strategy (retry, skip, abort) -- may be flow-specific or may need consistency
- Logging level and detail -- may vary by flow criticality
- Performance optimizations (caching, batch size) -- may vary by flow volume
- Default values for optional parameters -- may differ by flow context

Document gray-area decisions explicitly so that future reviewers understand the rationale.

## Recheck Trigger Conditions

Define conditions under which **all copies must be re-reviewed from scratch** (not just diff-reviewed):

1. **Canonical implementation fundamentally changes**: If the core algorithm or approach changes, diffs against the old canonical are no longer valid
2. **New required-sameness rule is discovered**: A previously-allowed difference is reclassified as required-sameness
3. **Defect found in canonical post-review**: If the canonical had a bug, all copies must be checked for the same bug
4. **New copy is added**: Review the new copy against canonical; also verify that the new copy's differences do not reveal overlooked issues in existing copies

## Extraction Threshold

When copy-paste code should be refactored into a shared module:

### Quantitative Indicators
- **Copy count >= 4**: More than 3 copies of the same logic strongly indicates extraction opportunity
- **Required-sameness ratio > 80%**: If more than 80% of the code must be identical, the differences can likely be parameterized
- **Change frequency > 1/quarter**: If the shared logic changes more than once per quarter, each change requires N reviews

### Qualitative Indicators
- Copies frequently diverge unintentionally (history of copy-paste bugs)
- New team members copy the wrong version as a starting point
- Allowed differences are small and easily parameterized (entity type, table name)
- The logic is complex enough that correctness is difficult to verify (tax calculation, rounding)

### Extraction Approach
1. Create a shared module/function/class with the common logic
2. Parameterize the allowed differences (entity type, table name, flow-specific settings)
3. Replace each copy with a call to the shared module, passing flow-specific parameters
4. Verify that all existing tests still pass
5. Add tests for the shared module that cover all parameterized variations
6. Delete the now-redundant copy-specific tests that tested the same logic

### When NOT to Extract
- Copies are expected to diverge significantly in the future
- Performance constraints require flow-specific optimization
- Organizational boundaries prevent shared code ownership
- The logic is simple enough that copy-paste risk is minimal (1-2 lines of code)

## Review Efficiency Metrics

Track these metrics to evaluate the effectiveness of the copy propagation review strategy:

| Metric | Formula | Target |
|--------|---------|--------|
| Review time saved | `(N-1) * canonical_review_time * 0.7` | Meaningful reduction vs uniform review |
| Defect detection rate | `defects_found / total_differences` | Higher than uniform review |
| False positive rate | `suspicious_resolved_as_allowed / total_suspicious` | Decreasing over time |
| Recheck frequency | `full_recheck_events / quarter` | Minimize through extraction |
