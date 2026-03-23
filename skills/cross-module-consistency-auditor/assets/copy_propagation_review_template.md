# Copy Propagation Review Plan

## Change Reference

| Attribute | Value |
|-----------|-------|
| **Change ID** | [Ticket/PR/Feature ID] |
| **Change Kernel** | [Brief description] |
| **Total Copy Count** | [N copies including canonical] |
| **Extraction Recommended?** | [YES/NO -- YES if copies >= 4 and required-sameness > 80%] |

---

## Canonical Implementation

| Attribute | Value |
|-----------|-------|
| **Module** | [Module name] |
| **File** | [File path] |
| **Function/Class** | [Function or class name] |
| **Selection Rationale** | [Why this was chosen as canonical: most complete, most representative, best tested, first written] |

### Canonical Review Checklist

| Review Area | Status | Findings |
|-------------|--------|----------|
| Line-by-line logic review | [Done/Pending] | [Findings or "No issues"] |
| Edge case analysis (zero, null, max, empty) | [Done/Pending] | [Findings] |
| Error handling review | [Done/Pending] | [Findings] |
| Sign and rounding verification | [Done/Pending] | [Findings] |
| State management (pre/post conditions) | [Done/Pending] | [Findings] |
| Test coverage verification | [Done/Pending] | [Findings] |
| Test execution results | [Done/Pending] | [Pass/Fail details] |

### Canonical Review Result

| Attribute | Value |
|-----------|-------|
| **Verdict** | [APPROVED / APPROVED WITH CONDITIONS / REJECTED] |
| **Conditions** | [List any conditions that must be met] |
| **Reviewer** | [Name] |
| **Date** | [Date] |

---

## Copy Targets

### Copy 1: [Module Name]

| Attribute | Value |
|-----------|-------|
| **Module** | [Module name] |
| **File** | [File path] |
| **Function/Class** | [Function or class name] |

#### Allowed Differences

| Location | Canonical | This Copy | Rationale |
|----------|-----------|-----------|-----------|
| Line 15: entity type | `TransactionType.SALE` | `TransactionType.RETURN` | Flow-specific entity type |
| Line 42: error message | "Sale processing failed" | "Return processing failed" | Flow-specific message |
| [Location] | [Canonical code] | [Copy code] | [Why difference is allowed] |

#### Detected Differences (Requiring Investigation)

| Location | Canonical | This Copy | Classification | Resolution |
|----------|-----------|-----------|----------------|------------|
| Line 28: rounding | `round(amount, 2)` | `int(amount)` | **DEFECT** | Must use same rounding as canonical |
| [Location] | [Canonical code] | [Copy code] | [Allowed/Suspicious/Defect/Missing/Extra] | [Action] |

#### Required-Sameness Verification

| Section | Identical to Canonical? | Notes |
|---------|------------------------|-------|
| Calculation formula | [YES/NO] | [Details if NO] |
| Validation logic | [YES/NO] | [Details if NO] |
| Sign handling | [YES/NO] | [Details if NO] |
| Rounding behavior | [YES/NO] | [Details if NO] |
| Included/excluded filters | [YES/NO] | [Details if NO] |

#### Copy 1 Review Result

| Attribute | Value |
|-----------|-------|
| **Verdict** | [APPROVED / APPROVED WITH CONDITIONS / REJECTED] |
| **Defects Found** | [Count] |
| **Reviewer** | [Name] |
| **Date** | [Date] |

---

### Copy 2: [Module Name]

| Attribute | Value |
|-----------|-------|
| **Module** | [Module name] |
| **File** | [File path] |
| **Function/Class** | [Function or class name] |

#### Allowed Differences

| Location | Canonical | This Copy | Rationale |
|----------|-----------|-----------|-----------|
| [Location] | [Canonical code] | [Copy code] | [Rationale] |

#### Detected Differences (Requiring Investigation)

| Location | Canonical | This Copy | Classification | Resolution |
|----------|-----------|-----------|----------------|------------|
| [Location] | [Canonical code] | [Copy code] | [Classification] | [Action] |

#### Required-Sameness Verification

| Section | Identical to Canonical? | Notes |
|---------|------------------------|-------|
| Calculation formula | [YES/NO] | [Details] |
| Validation logic | [YES/NO] | [Details] |
| Sign handling | [YES/NO] | [Details] |
| Rounding behavior | [YES/NO] | [Details] |
| Included/excluded filters | [YES/NO] | [Details] |

#### Copy 2 Review Result

| Attribute | Value |
|-----------|-------|
| **Verdict** | [APPROVED / APPROVED WITH CONDITIONS / REJECTED] |
| **Defects Found** | [Count] |
| **Reviewer** | [Name] |
| **Date** | [Date] |

---

(Repeat Copy section for each additional copy target.)

---

## Recheck Trigger Conditions

The following conditions require **full re-review of all copies** (not just diff review):

| Trigger | Description | Likelihood | Last Occurred |
|---------|-------------|------------|---------------|
| Canonical fundamental change | Core algorithm or approach changes in canonical | [H/M/L] | [Date or N/A] |
| New required-sameness rule | A previously-allowed difference is reclassified | [H/M/L] | [Date or N/A] |
| Post-review canonical defect | Bug found in canonical after initial review | [H/M/L] | [Date or N/A] |
| New copy added | A new copy of the logic is created | [H/M/L] | [Date or N/A] |

---

## Extraction Assessment

| Factor | Value | Threshold | Recommendation |
|--------|-------|-----------|----------------|
| Copy count | [N] | >= 4 | [EXTRACT / KEEP COPIES] |
| Required-sameness ratio | [N%] | > 80% | [EXTRACT / KEEP COPIES] |
| Change frequency | [N/quarter] | > 1/quarter | [EXTRACT / KEEP COPIES] |
| Unintentional divergence history | [YES/NO] | YES | [EXTRACT / KEEP COPIES] |
| **Overall Recommendation** | | | **[EXTRACT to shared module / KEEP as copies with diff review]** |

### Extraction Plan (if recommended)

| Step | Action | Owner | Status |
|------|--------|-------|--------|
| 1 | Create shared module with parameterized logic | [Owner] | [Status] |
| 2 | Define parameters for allowed differences | [Owner] | [Status] |
| 3 | Replace Copy 1 with shared module call | [Owner] | [Status] |
| 4 | Replace Copy 2 with shared module call | [Owner] | [Status] |
| 5 | Verify all existing tests pass | [Owner] | [Status] |
| 6 | Add shared module tests for all parameter variations | [Owner] | [Status] |

---

## Summary

| Metric | Value |
|--------|-------|
| Total copies reviewed | [N] |
| Total differences found | [N] |
| Allowed differences | [N] |
| Defects found | [N] |
| Suspicious items (under investigation) | [N] |
| Missing logic (in canonical but absent in copy) | [N] |
| Extra logic (in copy but absent in canonical) | [N] |
| Review time saved (estimated) | [N hours vs uniform review] |
