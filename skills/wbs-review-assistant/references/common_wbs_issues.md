# Common WBS Issues Pattern Library

## Purpose

Catalog of frequently encountered WBS problems with detection patterns, severity guidance, and resolution templates.

## Issue Categories

### 1. Completeness Issues

#### MISSING-REQ: Unmapped Requirements

**Description**: Requirement exists in requirements document but has no corresponding WBS task(s)

**Detection Pattern**:
- Extract all requirement IDs from requirements doc (REQ-\d+, UC-\d+, etc.)
- Search WBS task descriptions and custom fields for each ID
- Flag IDs with zero matches

**Severity**: Critical

**Example**:
```
Requirement: REQ-015 "System must support batch data import via CSV"
WBS Search Result: No tasks found containing "REQ-015" or "batch import"
```

**Resolution Template**:
```
Add task(s):
- 3.4.5 Implement CSV Batch Import (REQ-015)
  - 3.4.5.1 Design batch upload schema
  - 3.4.5.2 Develop CSV parser module
  - 3.4.5.3 Unit test batch import logic
  - 3.4.5.4 Integration test with database
```

---

#### MISSING-MILESTONE: No Phase Milestones

**Description**: Project phase lacks formal milestone or approval gate

**Detection Pattern**:
- Identify phase boundaries (1.0 → 2.0 transition)
- Check for milestone tasks (zero duration, deliverable defined)
- Flag phases with no milestone

**Severity**: Major

**Example**:
```
Phase: 2.0 Design
Last Task: 2.5 Database Schema Design
Next Task: 3.0 Development
Issue: No "Design Review" or "Design Approval" milestone
```

**Resolution Template**:
```
Add milestone:
- 2.6 Design Phase Milestone
  Duration: 0 days
  Deliverable: Design Document v1.0 (approved)
  Acceptance Criteria: Architecture review passed, stakeholder sign-off obtained
```

---

#### MISSING-TESTING: Insufficient Testing Coverage

**Description**: WBS lacks unit test, integration test, or UAT phases

**Detection Pattern**:
- Search task names for keywords: "test", "UAT", "QA", "validation"
- Calculate test task effort % of total development effort
- Flag if <15% or missing test categories

**Severity**: Critical

**Example**:
```
Total Development Tasks: 240 hours
Test Tasks Found: 16 hours (6.7%)
Missing: Integration testing, UAT
```

**Resolution Template**:
```
Add testing tasks:
- 4.3 Integration Testing
  - 4.3.1 End-to-end workflow testing
  - 4.3.2 API integration testing
  - 4.3.3 Database transaction testing
- 5.2 User Acceptance Testing
  - 5.2.1 UAT test case preparation
  - 5.2.2 UAT execution with stakeholders
  - 5.2.3 Defect remediation
```

---

### 2. Consistency Issues

#### INCONSISTENT-NUMBERING: WBS Code Hierarchy Breaks

**Description**: WBS codes skip levels or violate parent-child relationships

**Detection Pattern**:
- Parse WBS codes into numeric arrays [1,2,3] for "1.2.3"
- Check each code's parent exists (1.2.3 requires 1.2 exists)
- Check siblings are sequential (1.1, 1.2, 1.3 not 1.1, 1.3, 1.5)

**Severity**: Major

**Example**:
```
1.0 Project Initiation
1.1 Kickoff Meeting
1.3 Stakeholder Analysis  ← WRONG: Skipped 1.2
1.1.1.1 Action Item Tracking ← WRONG: Skipped 1.1.1
```

**Resolution Template**:
```
Renumber:
1.0 Project Initiation
1.1 Kickoff Meeting
1.2 Stakeholder Analysis  ← FIXED
1.1.1 Kickoff Action Items ← FIXED
1.1.1.1 Action Item Tracking
```

---

#### MISSING-EFFORT: Leaf Tasks Without Estimates

**Description**: Lowest-level tasks lack effort/duration estimates

**Detection Pattern**:
- Identify leaf tasks (tasks with no children)
- Check effort column for null/zero values
- Flag tasks missing estimates

**Severity**: Major

**Example**:
```
Task: 3.2.4 Implement Authentication API
Effort: (blank)
Issue: Cannot roll up parent task effort
```

**Resolution Template**:
```
Estimate required:
- 3.2.4 Implement Authentication API → 24 hours
  Basis: Similar API tasks averaged 20-28 hours
```

---

#### ROLLUP-ERROR: Parent Effort ≠ Sum of Children

**Description**: Parent task total doesn't match sum of child tasks

**Detection Pattern**:
- For each parent task, sum child efforts
- Compare to parent's effort value
- Flag if difference >0.1 hours

**Severity**: Critical

**Example**:
```
2.0 Design Phase: 80 hours (stated)
  2.1 UI Design: 24 hours
  2.2 API Design: 16 hours
  2.3 DB Design: 32 hours
  Sum: 72 hours ← MISMATCH (should be 80)
```

**Resolution Template**:
```
Options:
1. Correct parent: 2.0 Design Phase → 72 hours
2. Add missing child task(s) totaling 8 hours
3. Adjust child estimates to sum to 80 hours
```

---

### 3. Alignment Issues

#### HEARING-DECISION-MISSING: Decision Not Reflected

**Description**: Hearing sheet decision not incorporated into WBS

**Detection Pattern**:
- Extract decisions from hearing notes (marked with keywords: "決定", "合意", "decided")
- Search WBS for decision-related keywords or task changes
- Flag unmatched decisions

**Severity**: Critical

**Example**:
```
Hearing Note (2025-11-15):
"Decided: Use PostgreSQL instead of MySQL due to JSON support requirements"

WBS Search: No tasks reference PostgreSQL; Task 3.3.2 still says "MySQL setup"
```

**Resolution Template**:
```
Update WBS:
- 3.3.2 Database Setup → PostgreSQL Database Setup
- Add: 3.3.2.1 PostgreSQL JSON type schema design
- Update: 3.5.4 Database testing → PostgreSQL-specific tests
```

---

#### OUT-OF-SCOPE-TASK: Task Not in Requirements

**Description**: WBS includes task with no supporting requirement

**Detection Pattern**:
- For each WBS task, search requirements document for keywords
- Flag tasks with no keyword matches and no hearing note justification

**Severity**: Major (if significant), Minor (if administrative)

**Example**:
```
Task: 4.7 Implement blockchain integration
Requirements Doc: No mention of "blockchain"
Hearing Notes: No decision authorizing this scope
```

**Resolution Template**:
```
Options:
1. Remove task if truly out-of-scope
2. Add requirement (if missing from doc but agreed)
3. Clarify if task supports existing requirement indirectly
```

---

#### TECH-CHOICE-MISMATCH: Technology Inconsistency

**Description**: WBS uses different technology than requirements specify

**Detection Pattern**:
- Extract technology stack from requirements (frameworks, languages, platforms)
- Search WBS for technology keywords
- Flag inconsistencies

**Severity**: Major

**Example**:
```
Requirements: "Frontend framework: React"
WBS Task 2.3.1: "Angular component development"
Issue: Technology mismatch
```

**Resolution Template**:
```
Update WBS:
- 2.3.1 Angular component development → React component development
- Verify all related tasks use React (not Angular)
```

---

### 4. Quality Issues

#### NO-ACCEPTANCE-CRITERIA: Milestone Without Criteria

**Description**: Milestone task lacks acceptance criteria definition

**Detection Pattern**:
- Identify milestone tasks (duration=0 or marked as milestone)
- Check for acceptance criteria field
- Flag if blank or generic

**Severity**: Major

**Example**:
```
Task: 3.9 Development Phase Milestone
Acceptance Criteria: (blank)
Issue: No criteria for phase completion
```

**Resolution Template**:
```
Add criteria:
- All development tasks completed
- Code review passed (0 critical defects)
- Unit test coverage >80%
- Integration tests passing
- Technical debt log reviewed and prioritized
```

---

#### MISSING-DOCUMENTATION: No Doc Tasks for Deliverables

**Description**: Deliverable produced but no documentation task

**Detection Pattern**:
- Identify tasks producing deliverables (API, module, report)
- Check for corresponding documentation tasks
- Flag missing doc tasks

**Severity**: Major

**Example**:
```
Task: 3.4 Payment Gateway Integration
Deliverable: Payment module
Documentation Task: (not found)
Issue: No API documentation or user guide task
```

**Resolution Template**:
```
Add documentation:
- 3.4.5 Payment Gateway Documentation
  - 3.4.5.1 API specification document
  - 3.4.5.2 Integration guide for developers
  - 3.4.5.3 Error handling reference
```

---

#### NO-REVIEW-GATE: Missing Code Review Tasks

**Description**: Development tasks lack formal review/QA steps

**Detection Pattern**:
- Identify development tasks (coding, implementation)
- Check for review tasks ("code review", "peer review")
- Flag if review tasks <5% of dev tasks

**Severity**: Major

**Example**:
```
Development Tasks: 45 tasks (180 hours)
Code Review Tasks: 0 tasks
Issue: No quality gate before testing phase
```

**Resolution Template**:
```
Add review tasks:
- 3.8 Code Review Sprint
  - 3.8.1 Peer review all modules
  - 3.8.2 Security review (authentication/authorization)
  - 3.8.3 Performance review (critical paths)
  Effort: 18 hours (10% of dev effort)
```

---

### 5. Estimation Issues

#### UNREALISTIC-ESTIMATE: Task Effort Out of Range

**Description**: Task estimate too large (>80 hours) or too small (<1 hour for complex work)

**Detection Pattern**:
- Check leaf task efforts
- Flag if >80 hours (should be decomposed)
- Flag if <1 hour for non-trivial tasks

**Severity**: Major

**Example**:
```
Task: 3.2 Implement User Management Module
Effort: 120 hours
Issue: Single task too large, needs breakdown
```

**Resolution Template**:
```
Decompose task:
- 3.2 User Management Module (parent)
  - 3.2.1 User registration API (24h)
  - 3.2.2 Login/logout API (16h)
  - 3.2.3 Password reset flow (20h)
  - 3.2.4 Role management (24h)
  - 3.2.5 User profile CRUD (20h)
  - 3.2.6 Integration testing (16h)
  Total: 120h (same, but properly decomposed)
```

---

#### NO-CONTINGENCY: Missing Risk Buffer

**Description**: Project has no contingency/buffer allocation

**Detection Pattern**:
- Calculate total project effort
- Search for tasks containing "contingency", "buffer", "reserve"
- Flag if buffer <10% or missing

**Severity**: Minor

**Example**:
```
Total Project Effort: 500 hours
Contingency Tasks: 0 hours (0%)
Issue: No buffer for unknowns or risks
```

**Resolution Template**:
```
Add contingency:
- 6.5 Project Contingency Reserve
  Effort: 50-75 hours (10-15% of total)
  Justification: Risk mitigation, scope clarifications, rework
```

---

## Issue Prioritization Framework

### Priority = Severity × Impact

**Impact Factors**:
- Affected task count
- Downstream dependencies
- Schedule impact (critical path vs non-critical)
- Deliverable risk

**Prioritization Matrix**:

| Severity | High Impact | Medium Impact | Low Impact |
|----------|-------------|---------------|------------|
| Critical | P1 (Fix now) | P1 (Fix now) | P2 (Fix soon) |
| Major | P1 (Fix now) | P2 (Fix soon) | P3 (Review) |
| Minor | P2 (Fix soon) | P3 (Review) | P4 (Optional) |

## Resolution Response Templates

### For Missing Requirements

```
Action Required: Add task(s) to WBS

Affected Requirement: [REQ-ID] [Requirement Name]
Suggested Tasks:
- [WBS Code] [Task Name] ([REQ-ID])
  Effort: [X hours]
  Resource: [Role]
  Justification: [Why this task addresses the requirement]
```

### For Inconsistencies

```
Action Required: Correct WBS structure

Current State: [Description of problem]
Expected State: [Corrected structure]
Impact: [What breaks if not fixed]
Recommendation: [Specific renumbering or restructuring steps]
```

### For Alignment Issues

```
Action Required: Align WBS with decision

Decision Source: [Hearing note date] or [Requirements section]
Decision Content: [What was decided]
Current WBS: [How WBS contradicts decision]
Required Change: [What to update in WBS]
```
