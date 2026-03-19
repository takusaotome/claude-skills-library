# WBS Review Methodology

## Purpose

This document defines the systematic approach for reviewing Work Breakdown Structure (WBS) documents against project requirements, hearing sheet decisions, and industry best practices.

## Review Principles

### 1. Non-Destructive Review

- Never modify the original WBS structure or content
- Add review findings as Excel cell comments
- Use conditional formatting for visual severity indication
- Preserve original formulas and calculations

### 2. Evidence-Based Analysis

Every finding must be:
- Traceable to specific requirement ID, hearing note, or checklist criterion
- Supported by concrete evidence (cell reference, missing data, inconsistency)
- Actionable with clear recommendation

### 3. Risk-Proportionate Severity

- **Critical**: Blocker preventing WBS baseline (missing requirements, calculation errors)
- **Major**: High risk to project success (missing testing, inadequate detail)
- **Minor**: Improvement opportunity (formatting, naming conventions)

## Review Process

### Phase 1: Document Ingestion

**Objective**: Parse and normalize all input documents

1. **WBS Excel Parsing**
   - Identify WBS code column (1.0, 1.1, 1.1.1 pattern)
   - Detect task name, duration, effort, resource columns
   - Recognize hierarchy (indentation or level field)
   - Extract custom fields (status, deliverables, acceptance criteria)

2. **Requirements Extraction**
   - Parse requirement IDs (REQ-001, UC-01, etc.)
   - Extract requirement descriptions
   - Identify scope boundaries (in-scope vs out-of-scope)
   - Capture technology decisions

3. **Hearing Notes Processing**
   - Extract decisions with dates
   - Identify action items assigned to WBS
   - Capture clarifications and scope changes

### Phase 2: Traceability Analysis

**Objective**: Verify all requirements map to WBS tasks

1. **Forward Traceability** (Requirements → WBS)
   - For each requirement ID, search WBS task descriptions
   - Flag unmapped requirements as CRITICAL findings
   - Suggest candidate task names for missing work

2. **Backward Traceability** (WBS → Requirements)
   - For each WBS task, identify supporting requirement(s)
   - Flag orphan tasks (no requirement justification)
   - Validate tasks are within documented scope

3. **Hearing Notes Cross-Check**
   - Verify all decisions are reflected in WBS
   - Check action items have corresponding tasks
   - Validate clarifications updated task descriptions

### Phase 3: Structural Validation

**Objective**: Ensure WBS follows hierarchical best practices

1. **Hierarchy Checks**
   - Validate WBS code numbering (1.1 → 1.1.1, not 1.1 → 1.3)
   - Confirm 100% rule: child tasks = parent task scope
   - Check decomposition depth consistency (not 1.1 → 1.1.1.1.1.1)

2. **Phase Organization**
   - Verify project follows standard phases (Initiation, Planning, Execution, Closure)
   - Confirm milestones at phase boundaries
   - Check for testing phases (unit, integration, UAT)

3. **Deliverable Mapping**
   - Each phase must produce deliverable(s)
   - Deliverables must align with requirements
   - Documentation tasks must exist for each deliverable

### Phase 4: Content Quality Checks

**Objective**: Validate task-level data quality

1. **Effort Estimation**
   - All leaf tasks have effort estimates
   - Estimates within reasonable ranges (1-80 hours)
   - Parent task rollups = sum of children
   - Contingency buffer allocated (10-20%)

2. **Task Descriptions**
   - Clear, action-oriented task names
   - Acceptance criteria for milestones
   - Dependencies documented (predecessor/successor)
   - Resource assignments present

3. **Quality Gates**
   - Review/approval milestones defined
   - Testing coverage adequate
   - Risk mitigation tasks for high-risk areas

### Phase 5: Finding Prioritization

**Objective**: Rank findings by impact and urgency

1. **Severity Assignment**
   - Critical: Missing requirements, calculation errors
   - Major: Missing testing, inadequate decomposition
   - Minor: Formatting, naming conventions

2. **Impact Analysis**
   - Affected WBS tasks count
   - Downstream dependencies
   - Project schedule impact

3. **Recommendation Formulation**
   - Specific action to resolve
   - Suggested task structure or content
   - Traceability reference

## Common WBS Issues

### Missing Requirements Coverage

**Pattern**: Requirement documented but no WBS task addresses it

**Detection**:
- Parse requirement IDs from requirements doc
- Search WBS task descriptions for each ID
- Flag unmapped requirements

**Severity**: Critical

**Recommendation**: Add task(s) to WBS referencing the requirement

### Inconsistent WBS Numbering

**Pattern**: WBS codes skip levels or break hierarchy

**Examples**:
- 1.1 → 1.3 (skipped 1.2)
- 1.1 → 1.1.1.1 (skipped 1.1.1)

**Detection**: Parse WBS codes, validate parent-child relationships

**Severity**: Major

**Recommendation**: Renumber tasks to follow strict hierarchy

### Missing Testing Phases

**Pattern**: No unit test, integration test, or UAT tasks

**Detection**: Search task names for "test", "UAT", "validation"

**Severity**: Critical

**Recommendation**: Add testing tasks per requirement area

### Effort Rollup Errors

**Pattern**: Parent task total ≠ sum of child tasks

**Detection**: Calculate sum of child efforts, compare to parent

**Severity**: Critical

**Recommendation**: Correct parent task effort or child breakdown

### Orphan Tasks

**Pattern**: WBS task with no supporting requirement

**Detection**: Search requirements for task name keywords

**Severity**: Major (if significant), Minor (if administrative)

**Recommendation**: Add requirement or remove task if out-of-scope

### Hearing Sheet Decisions Not Reflected

**Pattern**: Decision from meeting notes not incorporated

**Detection**: Extract decisions from hearing notes, search WBS

**Severity**: Critical

**Recommendation**: Update WBS to reflect decision

## Output Formats

### Excel Cell Comments

Format:
```
[SEVERITY-ID] Issue Title
Location: Row X, Column Y
Issue: <description>
Requirement: <REQ-ID or hearing note reference>
Recommendation: <action>
```

Example:
```
[CRITICAL-001] Missing Acceptance Criteria
Location: Row 45, Column E
Issue: No acceptance criteria defined for milestone task
Requirement: REQ-012 specifies UAT pass/fail criteria required
Recommendation: Add explicit criteria: "All test cases pass, stakeholder sign-off obtained"
```

### Markdown Summary Report Sections

1. **Executive Summary**
   - Issue count by severity
   - Overall WBS readiness score (0-100)
   - Go/No-Go recommendation

2. **Top Priority Findings**
   - Top 10 issues sorted by severity + impact
   - Each with location, issue, recommendation

3. **Requirements Coverage Matrix**
   - Table: Requirement ID | Name | Mapped Tasks | Status
   - Statistics: X% coverage, Y requirements unmapped

4. **Missing Task Candidates**
   - Suggested tasks based on unmapped requirements
   - Priority ranking (high/medium/low)

5. **Detailed Findings by Category**
   - Grouped by checklist category
   - Full finding details with evidence

## Validation Thresholds

### Readiness Score Calculation

```
Base Score = 100
- Deduct 20 points per Critical issue
- Deduct 5 points per Major issue
- Deduct 1 point per Minor issue

Readiness Score = max(0, Base Score - Total Deductions)
```

### Go/No-Go Decision

- **90-100**: Ready for baseline
- **70-89**: Needs revision but usable
- **50-69**: Significant gaps, major rework required
- **<50**: Incomplete, not ready for review

## Bilingual Support

### Japanese WBS Handling

- Detect Japanese characters in task names
- Parse Japanese requirement IDs (要件-001, etc.)
- Support Japanese hearing note formats
- Generate bilingual reports (EN/JA side-by-side)

### Language Detection Strategy

1. Check WBS column headers for Japanese keywords (タスク名, 工数, 担当者)
2. Detect requirement ID patterns (REQ-001 vs 要件-001)
3. Auto-select report language based on majority language
