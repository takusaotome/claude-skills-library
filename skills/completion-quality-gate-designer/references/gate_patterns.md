# Gate Patterns Reference

This document provides reusable gate patterns organized by project lifecycle model, along with enforcement mechanisms and sign-off separation rules.

## 1. Phase-Based Gate Pattern

The most common pattern for projects with distinct lifecycle phases. Each phase boundary becomes a gate.

### Standard Phase Gates

| Gate ID | Gate Name | Preceding Phase | Following Phase | Typical Artifacts |
|---------|-----------|-----------------|-----------------|-------------------|
| G1 | Design Complete | Requirements | Design | Approved requirements doc, architecture decision records |
| G2 | Implementation Complete | Design | Implementation | Code committed, unit tests written, static analysis clean |
| G3 | Verification Complete | Implementation | Testing | All standard commands pass, test report generated, coverage met |
| G4 | Release Approved | Testing | Release | Release readiness checklist signed, exception register reviewed |

### Phase Gate Characteristics

- **G1 - Design Complete**: Ensures that requirements are unambiguous and design is peer-reviewed before coding begins. Entry criteria include approved requirements; exit criteria include signed-off design documents and identified test scenarios.
- **G2 - Implementation Complete**: Confirms that code is written, committed, and passes basic quality checks (linting, compilation, unit tests). This gate explicitly does NOT assert integration or E2E quality.
- **G3 - Verification Complete**: The most critical gate. Confirms that all standard verification commands have been executed, results are recorded, and any failures are either resolved or registered as exceptions. This is where "Implemented" transitions to "Verified."
- **G4 - Release Approved**: The decision gate. Confirms that the release package is ready, known limitations are documented, rollback plan exists, and a designated authority has approved the release.

## 2. Milestone-Based Gate Pattern

Suitable for agile or iterative projects where phases overlap. Gates are tied to milestones rather than phase boundaries.

### Standard Milestone Gates

| Gate ID | Milestone | Definition | Key Question |
|---------|-----------|------------|--------------|
| M1 | Design Milestone | Core architecture decisions finalized | Can we build this without major rework? |
| M2 | Feature Milestone | All planned features implemented | Is the code functionally complete? |
| M3 | Quality Milestone | All verification activities complete | Is the code production-quality? |
| M4 | Ship Milestone | Release decision made | Are we confident enough to deploy? |

### Milestone Gate Characteristics

Milestone gates differ from phase gates in that multiple milestones may be in progress simultaneously for different features. The gate applies to the aggregate state of the project at the milestone checkpoint.

## 3. Deliverable-Based Gate Pattern

Useful for documentation-heavy projects or projects where the primary concern is artifact completeness.

### Standard Deliverable Gates

| Gate ID | Deliverable | Required State | Verification Method |
|---------|-------------|----------------|---------------------|
| D1 | Feature Specification | Approved by stakeholders | Sign-off record |
| D2 | Source Code | Passes all standard commands | CI pipeline output |
| D3 | Test Results | Full scope executed, results recorded | Test report artifact |
| D4 | Operations Runbook | Reviewed by operations team | Review sign-off |
| D5 | Release Notes | Approved by product owner | Sign-off record |

## 4. Enforcement Mechanisms

A gate that is not enforced is merely a suggestion. Choose enforcement mechanisms appropriate to the project context.

### Technical Enforcement (Automated)

These mechanisms prevent progression without human intervention:

- **CI Required Status Checks**: Configure branch protection rules so that pull requests cannot merge unless specified checks pass. Map each check to a gate criterion.
- **Pipeline Stage Gates**: In CI/CD pipelines, configure stages that block deployment unless previous stages succeed. Artifact promotion (e.g., moving a Docker image from staging to production registry) serves as a technical gate.
- **Automated Test Thresholds**: Set coverage thresholds, mutation testing thresholds, or performance benchmarks that fail the build if not met.
- **Static Analysis Rules**: Configure linters and security scanners as blocking checks. Define severity thresholds (e.g., zero critical findings, fewer than N high findings).

### Process Enforcement (Manual)

These mechanisms require human action but do not have automated blocking:

- **Sign-off Forms**: Require a named individual to record their approval with date and any conditions. The sign-off must be a separate artifact, not just a verbal agreement.
- **Review Meetings**: Scheduled gate review sessions where evidence is presented and the gate decision is made collectively. Minutes must record the decision and any exceptions.
- **Checklist Completion**: A mandatory checklist that must be completed and attached to the gate record before progression. Checklists should be versioned and specific to each gate.

### Hybrid Enforcement (Recommended)

The most robust approach combines technical and process enforcement:

1. Automated checks block the PR/deployment pipeline (technical)
2. A human reviewer verifies the automated results and checks for items that automation cannot assess (process)
3. The gate record documents both the automated results and the human sign-off

## 5. Sign-off Separation Rules

### The Producer-Approver Separation Principle

The person who produces an artifact must not be the sole approver of that artifact. This is the most fundamental governance rule for quality gates.

| Artifact Type | Producer | Approver (Must Differ) |
|---------------|----------|------------------------|
| Code | Developer | Peer reviewer or tech lead |
| Test Plan | QA engineer | Development lead or product owner |
| Test Results | QA engineer or CI system | Development lead (for results) |
| Release Package | Build engineer | Release manager |
| Exception Record | Requestor | Gate owner or project manager |

### Multi-Level Sign-off

For high-risk gates (especially G4 Release Approved), consider multi-level sign-off:

1. **Technical sign-off**: Confirms that technical criteria are met (tech lead)
2. **Quality sign-off**: Confirms that quality criteria are met (QA lead)
3. **Business sign-off**: Confirms that business risk is acceptable (product owner or project sponsor)

Each level addresses a different concern. Collapsing them into a single sign-off creates blind spots.

### Conflict Resolution

When an approver disagrees with the gate outcome:
1. Document the objection with specific criteria references
2. Escalate to the gate escalation authority (defined per gate)
3. The escalation authority may override, but the objection remains in the gate record
4. Overrides are tracked as a category of exception

## 6. Common Anti-Patterns

### Gate Theater
- **Symptom**: Gates exist on paper but are routinely bypassed or rubber-stamped
- **Root Cause**: Gate criteria are too vague or too numerous to evaluate meaningfully
- **Fix**: Reduce criteria to the essential minimum; make each criterion measurable; audit gate records periodically

### Bottleneck Gates
- **Symptom**: A single person is the approver for all gates, creating a throughput bottleneck
- **Root Cause**: Approval authority is not delegated appropriately
- **Fix**: Define approval delegation rules; train multiple approvers; allow peer approval for lower-risk gates

### Phantom Evidence
- **Symptom**: Gate records reference evidence that does not exist or cannot be located
- **Root Cause**: Evidence storage is not standardized; evidence is ephemeral (e.g., terminal output not captured)
- **Fix**: Require all evidence to be stored in a durable, addressable location (artifact repository, wiki page, issue tracker); validate evidence links at gate review

### Scope Creep at Gates
- **Symptom**: Gate reviews expand to cover topics outside the gate's scope, causing delays and confusion
- **Root Cause**: Gate scope is not clearly defined
- **Fix**: Each gate must have a written scope statement; the gate facilitator enforces scope; out-of-scope items are captured as action items for the appropriate forum
