# Metrics Reconciliation Guide

This document establishes rules for maintaining a single source of truth for quality metrics, resolving discrepancies between manual and automated data sources, and preventing the divergence that causes confusion in gate reviews and release decisions.

## 1. The Reconciliation Problem

In a typical project, the same metric (e.g., "number of tests passed") may appear in multiple places:

- CI pipeline output
- Test report document
- Completion summary
- Release decision document
- Project dashboard
- Status meeting slides

When these sources are updated independently, they inevitably diverge. A gate reviewer sees "188 tests" in one document and "192 tests" in another, and cannot determine which is authoritative. This divergence is not merely an annoyance -- it undermines confidence in all quality claims.

### Real-World Divergence Scenarios

**Scenario 1: Count Mismatch**
The CI reports 188 passing tests. The test report (authored manually) states 192 tests. The discrepancy is caused by the report author counting test cases from the test plan rather than actual executions. Four test cases were not automated yet.

**Scenario 2: Stale Data**
The project dashboard shows 82% code coverage. The CI pipeline (run 2 hours later) shows 79% coverage because a new module with no tests was added. The dashboard was last synced yesterday.

**Scenario 3: Scope Mismatch**
The completion summary states "all tests pass." The CI shows unit tests passing but E2E tests failing. The summary author only checked the unit test job.

**Scenario 4: Rounding Discrepancy**
One report shows 85.7% coverage, another shows 86%. Both are technically correct but at different precision levels. A gate criterion of "85% minimum" passes in both cases, but the inconsistency raises questions about data reliability.

## 2. The Auto-First Principle

### Rule: Automated Sources Take Precedence

When both an automated source and a manual source exist for the same metric, the automated source is the authoritative value unless the automated source is demonstrably broken.

### Precedence Hierarchy

| Priority | Source Type | Example | When Authoritative |
|----------|-----------|---------|-------------------|
| 1 (Highest) | CI pipeline output | GitHub Actions job log, artifact report | Always, unless pipeline is demonstrably misconfigured |
| 2 | Automated dashboard | SonarQube, Codecov, Datadog | When synced within the reconciliation window |
| 3 | Manual report referencing auto source | Test report that quotes CI numbers | When the reference is traceable to a specific CI run |
| 4 (Lowest) | Manual count or estimate | "We ran approximately 200 tests" | Only when no automated source exists |

### Overriding an Automated Source

If the automated source is believed to be incorrect, the following process applies:

1. Document the specific error in the automated source (e.g., "CI double-counted parameterized tests")
2. File a bug/issue against the CI configuration
3. Record the corrected value with explicit annotation: "CI reports 188; actual is 184 due to [issue ID]; manual count verified by [name]"
4. Register this as an evidence quality exception in the exception register
5. Fix the automated source before the next gate review

## 3. Single Source of Truth (SSOT) Designation

### How to Designate SSOT

For each metric that appears in quality gate evidence, designate exactly one source as the SSOT.

| Metric | Recommended SSOT | Rationale |
|--------|-----------------|-----------|
| Test count (total/passed/failed/skipped) | CI pipeline test stage output | Deterministic, reproducible, versioned |
| Code coverage percentage | CI coverage report artifact | Computed from actual execution, not estimated |
| Static analysis findings | CI static analysis stage output | Consistent rule set, no manual filtering |
| Security vulnerability count | Security scanner CI stage output | Automated scanning covers full dependency tree |
| Build status | CI pipeline final status | Definitive pass/fail determination |
| Performance metrics | Load test CI stage output | Reproducible test conditions |
| Review approval status | Version control platform API | Immutable approval record |
| Exception count | Exception register (manual) | Exceptions are inherently manual decisions |
| UAT results | UAT sign-off form (manual) | Inherently requires human judgment |

### SSOT Documentation Format

For each metric, document the SSOT in the Evidence Ownership Matrix:

```
Metric: Test Pass Count
SSOT: CI Pipeline - Test Stage - JUnit XML Report
Location: artifacts/test-results/junit.xml (published per CI run)
Update frequency: Per commit (on PR) or per merge (on main)
Reconciliation rule: All downstream documents must reference this artifact by CI run ID
```

## 4. Reconciliation Rules

### Rule 1: Reference, Don't Replicate

Downstream documents (test reports, completion summaries, release decision documents) should reference the SSOT rather than replicating the number.

**Good**: "Test results: 188 passed, 0 failed, 3 skipped (ref: CI Run #1234, job test-unit)"
**Bad**: "Test results: 188 passed, 0 failed, 3 skipped" (no reference to source)

### Rule 2: Timestamp and Version All Citations

Every metric citation must include:
- The value
- The source (SSOT reference)
- The timestamp or version (CI run number, commit hash, report generation date)

This allows any reader to verify the number independently and detect staleness.

### Rule 3: Define the Reconciliation Window

Metrics that are auto-collected at different times may legitimately differ. Define a reconciliation window: the maximum acceptable time gap between the SSOT value and the citing document.

| Document Type | Reconciliation Window | Rationale |
|---------------|----------------------|-----------|
| Test report for gate review | Same CI run as the release candidate | Must reflect the exact build being evaluated |
| Project dashboard | Within 24 hours | Acceptable lag for monitoring purposes |
| Status meeting slides | Within current sprint | Slides are summary-level; exact numbers less critical |
| Release decision document | Same CI run as the release candidate | Must be precise and current |

### Rule 4: Discrepancy Resolution Process

When a discrepancy is discovered between two sources:

1. **Identify the SSOT** for the metric in question
2. **Check timestamps**: Is the non-SSOT value simply stale?
3. **Check scope**: Are the two sources measuring different things? (e.g., unit tests vs all tests)
4. **Check methodology**: Are the sources counting differently? (e.g., test cases vs test executions)
5. **Resolve**:
   - If the SSOT is correct: Update the non-SSOT source with a reference to the SSOT value
   - If the SSOT appears incorrect: Follow the "Overriding an Automated Source" process (Section 2)
   - If the discrepancy reveals a scope or methodology mismatch: Clarify definitions and update both sources

### Rule 5: Prohibited Reconciliation Practices

The following practices are prohibited:

- **Averaging**: "The CI says 188 and the report says 192, so let's call it 190" -- NO
- **Choosing the better number**: "The CI says 79% coverage but the old report says 82%, let's use 82%" -- NO
- **Ignoring the discrepancy**: "Close enough" -- NO. Every discrepancy must be explained and resolved.
- **Manual override without documentation**: Changing a number without recording why -- NO

## 5. Metric Consistency Checklist

Before any gate review, verify the following for all metrics cited in the gate evidence:

| Check | How to Verify | Action if Failed |
|-------|--------------|-----------------|
| All metrics reference an SSOT | Evidence Ownership Matrix is complete | Designate SSOT before proceeding |
| All citations include source and timestamp | Grep evidence documents for unreferenced numbers | Add references to all bare numbers |
| SSOT values are within reconciliation window | Compare SSOT timestamps to gate review date | Refresh stale data or document the lag |
| No unexplained discrepancies | Cross-reference metrics across all gate documents | Resolve per Rule 4 |
| Coverage has not decreased since last gate | Compare current SSOT to previous gate record | Investigate regression |
| Test count has not decreased since last gate | Compare current SSOT to previous gate record | Investigate missing tests |
| No manually overridden auto-metrics | Check exception register for evidence quality exceptions | Verify justification or restore auto value |

## 6. Tools and Automation Recommendations

### For CI-Based SSOT

- Publish test results as artifacts (JUnit XML, JSON) in every CI run
- Use standardized report formats that include metadata (timestamp, commit hash, environment)
- Configure dashboards to pull from artifact storage, not from pipeline logs

### For Manual Metrics

- Use structured forms (not free-text) for manual evidence
- Include mandatory fields for source reference and timestamp
- Review manual entries during gate review for completeness

### For Reconciliation Automation (Future)

- Implement a reconciliation script that compares metric values across documents and flags discrepancies
- Integrate reconciliation into the CI pipeline as a pre-gate check
- Generate a reconciliation report as part of the gate evidence package

## 7. Example Reconciliation Scenario

### Situation
A gate review reveals three different test counts:
- CI pipeline: 188 passed, 0 failed, 3 skipped
- Test report: 192 test cases documented
- Completion summary: "all 192 tests passed"

### Resolution
1. **SSOT**: CI pipeline (Priority 1 source)
2. **Root cause**: The test report documents 192 test cases in the test plan. 4 of those are manual test cases not yet automated. The CI runs 191 automated tests (188 passed + 3 skipped).
3. **Completion summary error**: "all 192 tests passed" is incorrect because (a) only 188 passed (3 were skipped), and (b) 4 manual test cases are not reflected in the CI count.
4. **Corrected statement**: "188 of 191 automated tests passed, 3 skipped (ref: CI Run #1234). 4 manual test cases executed separately (ref: UAT Session #5). Total: 192 test cases, 188 auto-passed, 4 manually verified, 3 auto-skipped (see Exception EX-2026-003 for skip justification)."
5. **Action**: Update the completion summary with the corrected statement. Update the evidence ownership matrix to clarify that test count SSOT is CI for automated tests and UAT log for manual tests.
