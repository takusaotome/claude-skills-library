---
name: completion-quality-gate-designer
description: |
  工程ごとの完了判定、品質ゲート、証跡、標準検証コマンド、例外運用を設計するスキル。
  実装完了・テスト実施・品質確認完了・出荷可能を分離し、再利用可能な gate matrix を作る。
  「全OK」「完了」などの曖昧な完了表現を排除し、証跡に基づく退出条件を定義する。
  Use when defining Definition of Done, quality gates, exit criteria, release readiness gates,
  evidence requirements, exception handling, or standardized verification commands.
  Covers: definition of done, quality gate, exit criteria, release readiness, 完了判定, 品質ゲート.
  Distinct from project-completeness-scorer (which scores) -- this skill designs
  the gates and criteria themselves.
---

# Completion Quality Gate Designer

## Overview

This skill designs the structure and rules that define what "done" means at each stage of a software project. It produces reusable quality gate matrices, completion vocabulary definitions, evidence ownership mappings, exception registers, and release readiness checklists.

The core problem this skill addresses: teams often conflate "code is written" with "quality is confirmed" with "ready to ship." When these concepts are not explicitly separated, test gaps become invisible, metrics diverge across documents, and known limitations are buried under blanket "all OK" statements.

**Scope Boundary**: This skill designs gates, criteria, and governance structures. It does not execute code reviews (use `critical-code-reviewer`), score completeness (use `project-completeness-scorer`), or implement CI pipelines. It produces the specifications that those activities operate against.

## When to Use

- 新規案件の開始時に「Definition of Done」を工程別に設計したい
- テスト報告・完了サマリー・リリース判断資料の不整合をなくしたい
- 標準検証コマンドを固定し、開発者・CI・報告書で同じ定義を使いたい
- 例外的に未完了項目を持ち越すときの例外運用を決めたい
- 「実装完了」「品質確認完了」「出荷可能」を別概念として整理したい
- リリース判定の基準を決めたい / Design release readiness criteria
- Define exit criteria for project phases or milestones
- Standardize verification evidence across teams
- Create quality gates for CI/CD pipelines
- Establish exception governance for deferred items

## Inputs

- Development process definition or WBS
- Test strategy / test reports (if available)
- Existing CI pipeline definitions
- Completion summaries / release decision documents (if available)
- Approval workflow information
- Defect analysis reports (if available)

## Outputs

1. **Quality Gate Matrix** -- gates with entry/exit criteria, evidence, owners, and exception rules
2. **Definition of Done** -- completion state definitions with vocabulary separation
3. **Standard Verification Command Set** -- fixed commands for CI, developers, and reports
4. **Exception Register** -- tracked exceptions with risk, controls, and expiration
5. **Evidence-to-Owner Mapping** -- evidence items with source (auto/manual), owner, and reconciliation rules

## Prerequisites

- A project with identifiable phases, milestones, or deliverables
- Access to (or willingness to define) the project's development process, test strategy, and approval workflow
- No scripts or API keys required (v1.0 is guidance-only)

## Workflows

### Phase 1: Scope Phases and Gate Units (対象工程と判定単位を切る)

Determine the project's natural breakpoints and decide how gates will be organized.

1. Identify the project's lifecycle model (waterfall phases, sprint milestones, or deliverable-based)
2. Select one of three gate organization patterns:
   - **Phase-based**: Requirements / Design / Implementation / Testing / Release
   - **Milestone-based**: M1 Design Complete / M2 Implementation Complete / M3 Verification Complete / M4 Release Approved
   - **Deliverable-based**: Feature Spec / Code / Test Results / Runbook / Release Notes
3. Load `references/gate_patterns.md` for detailed pattern guidance
4. For each gate, assign a Gate ID (e.g., G1, G2, G3, G4) and name
5. Document gate dependencies: which gate must pass before the next can begin
6. Output: ordered list of gates with IDs, names, and dependency chain

### Phase 2: Separate Completion Vocabulary (完了の語彙を分離する)

Establish precise terminology to prevent "done" from meaning different things to different people.

1. Load `references/definition_of_done_framework.md`
2. Define at minimum the following five completion states:
   - **Implemented (実装完了)**: Code is written and committed; no quality assertion implied
   - **Verified (検証完了)**: Standard verification commands have passed; evidence recorded
   - **Accepted (受入完了)**: Designated approver has reviewed evidence and signed off
   - **Released (リリース完了)**: Deployed to production and confirmed operational
   - **Exception-approved (例外承認済)**: Known incomplete items approved with conditions
3. Map each completion state to the gates defined in Phase 1
4. Define prohibited expressions (e.g., "all OK" when exceptions exist, "complete" before verification)
5. Output: vocabulary table using `assets/definition_of_done_template.md`

### Phase 3: Define Exit Criteria for Each Gate (各ゲートの退出条件を定義する)

For every gate, specify exactly what must be true before the gate can pass.

1. For each gate defined in Phase 1, specify:
   - **Required Inputs**: what artifacts must exist before evaluation begins
   - **Required Evidence**: what proof of quality must be produced
   - **Standard Command**: which verification command(s) must pass (if applicable)
   - **Owner**: who is responsible for producing the evidence
   - **Approver**: who signs off on gate passage (must differ from owner)
   - **Pass Rule**: the minimum threshold for passage (e.g., "all critical tests pass, coverage above 80%")
   - **Failure Handling**: what happens when criteria are not met (block, escalate, or exception path)
   - **Carryover Policy**: which items, if any, may be deferred to the next gate with conditions
2. Output: completed `assets/quality_gate_matrix_template.md`
3. Validate: every gate must have at least one required evidence item and one approver

### Phase 4: Pin Evidence Sources and Metrics (証跡とメトリクスの出どころを固定する)

Eliminate discrepancies by defining the single authoritative source for each metric.

1. Load `references/evidence_catalog.md` for the evidence type inventory
2. Load `references/metrics_reconciliation_guide.md` for reconciliation rules
3. For each evidence item in the gate matrix:
   - Classify as **Auto** (CI-generated, machine-readable) or **Manual** (human-authored)
   - Assign an owner responsible for accuracy
   - Define update frequency (per-commit, per-sprint, per-release)
   - Specify reconciliation rule if the same metric appears in multiple documents
4. Apply the **Auto-First Principle**: if a metric can be auto-collected, manual override is prohibited unless the auto source is demonstrably broken
5. Output: completed `assets/evidence_ownership_matrix_template.md`

### Phase 5: Fix Standard Verification Commands (標準検証コマンドを固定する)

Create a canonical command set so that "tests pass" means the same thing everywhere.

1. Inventory all verification commands currently used in the project (e.g., `npm test`, `pytest`, linters, security scanners)
2. For each command, document:
   - Exact invocation (including flags and environment)
   - What it covers (unit only, integration, E2E, security, etc.)
   - What it does NOT cover (explicit exclusions)
   - Where it runs (local, CI, both)
   - Whether it is a CI required status check
3. Assign commands to gates: which command(s) must pass for each gate
4. Define the "Standard Test Report" format: the minimum fields that a test report must contain (total tests, passed, failed, skipped, coverage, execution time, environment)
5. Output: command definition table embedded in the Quality Gate Matrix

### Phase 6: Design Exception Governance (例外運用を設計する)

Define the rules for when incomplete items can be carried forward under controlled conditions.

1. Load `references/exception_governance.md`
2. For each gate, specify:
   - **Exception-eligible items**: which types of incomplete work may be deferred
   - **Exception-ineligible items**: which must block (e.g., security vulnerabilities above threshold, data loss risks)
   - **Required exception record fields**: What, Why, Risk, Temporary Control, Due Date, Owner, Approver, Closure Evidence
   - **Escalation path**: who approves exceptions at each severity level
   - **Expiration rule**: maximum time an exception may remain open before mandatory re-review
3. Output: completed `assets/exception_register_template.md`
4. Validate: no gate may have an empty exception policy (every gate must explicitly state what is and is not deferrable)

### Phase 7: Enforce Expression Control (表現統制を設計する)

Prevent misleading language in reports and status communications.

1. Define a **Prohibited Expressions List** specific to this project:
   - "All OK" or "all tests passed" when any exception is registered
   - "Complete" or "done" when the item is only at Implemented state (not yet Verified)
   - "All PASS" when only a subset of standard commands was executed
   - Percentage claims (e.g., "100% pass rate") without specifying the denominator and scope
2. Define **Required Qualifiers** for each completion state:
   - Implemented: "Implementation complete; verification pending"
   - Verified: "Standard verification passed per [command set]; [N] exceptions registered"
   - Accepted: "Accepted by [approver] on [date]; [N] known limitations documented"
   - Released: "Deployed to [environment] on [date]; post-deployment verification [status]"
3. Specify where expression rules apply: test reports, completion summaries, release decision documents, status emails, dashboards
4. Output: Expression control rules section in the Quality Gate Matrix or as a standalone appendix
5. Final deliverable: assemble all outputs into a coherent **Release Readiness Package** using `assets/release_readiness_template.md`

## Resources

| File | Type | Purpose | When to Load |
|------|------|---------|--------------|
| `references/gate_patterns.md` | Reference | Phase-based gate patterns, enforcement mechanisms, required status checks, sign-off separation | Phase 1 |
| `references/definition_of_done_framework.md` | Reference | Implemented/Verified/Accepted/Released definitions, common misuse patterns, JP/EN terminology | Phase 2 |
| `references/evidence_catalog.md` | Reference | Evidence types: test results, CI logs, static analysis, manual verification, exception approvals | Phase 4 |
| `references/metrics_reconciliation_guide.md` | Reference | Manual vs auto update priority, discrepancy resolution, single source of truth rules | Phase 4 |
| `references/exception_governance.md` | Reference | Exception eligibility, escalation, expiration, closure criteria | Phase 6 |
| `assets/quality_gate_matrix_template.md` | Template | Gate ID / Phase / Objective / Required Inputs / Evidence / Command / Owner / Approver / Pass Rule / Exception Rule / Exit State | Phase 3, Phase 5 |
| `assets/definition_of_done_template.md` | Template | Completion state definitions with explicit exclusions and outstanding items | Phase 2 |
| `assets/exception_register_template.md` | Template | Exception tracking with risk, temporary controls, due dates, closure evidence | Phase 6 |
| `assets/release_readiness_template.md` | Template | Release decision document with open criticals, known limitations, test scope, conditions | Phase 7 |
| `assets/evidence_ownership_matrix_template.md` | Template | Evidence item / Source type / Owner / Frequency / Reconciliation rule | Phase 4 |

## Best Practices

### Separate Roles: Owner vs Approver
- The person who produces evidence must never be the sole approver of that evidence
- Gate sign-off requires at least one person who did not produce the artifacts being evaluated
- For small teams, use cross-functional review (developer reviews test plan, QA reviews release notes)

### Auto-First Evidence Collection
- If a metric can be auto-collected from CI, do not accept manual entry as the primary source
- Manual metrics are permissible only for items that cannot be automated (e.g., UX review outcomes, stakeholder sign-offs)
- When auto and manual values conflict, the auto value takes precedence unless the auto source is demonstrably broken (and this must be documented as an exception)

### Exception Discipline
- Every exception must have an expiration date; open-ended exceptions are prohibited
- Exceptions must specify both the risk and the temporary control that mitigates it
- An exception without a named approver is not an exception -- it is an uncontrolled gap
- Track exception closure as rigorously as defect closure

### Expression Precision
- Ban "all" and "complete" as standalone status words; always qualify with scope and conditions
- Reports must state what was tested, what was not tested, and what is known to be broken
- A release recommendation must explicitly list conditions under which the recommendation would change

### Living Documents
- Gate definitions are not write-once artifacts; revisit them at each retrospective
- When a gate fails to catch a defect that escapes to production, update the gate criteria as part of the RCA corrective actions
- Version-control all gate definitions alongside the project code
