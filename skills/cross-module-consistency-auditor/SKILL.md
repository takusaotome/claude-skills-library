---
name: cross-module-consistency-auditor
description: |
  変更が波及する全モジュール・全フローを特定し、集計ルール、状態遷移、符号反転、
  コピペ差分、表示/帳票/APIの整合性を監査するスキル。Impact Mapで変更核から
  影響範囲を可視化し、Consistency Matrixで横断整合を検証し、Copy Propagation
  Review戦略でコピペ実装を効率的にレビューする。
  Use when one change affects multiple modules, reports, flows, or copied
  implementations. Audits aggregation totals, state transitions, sign inversion,
  and cross-module consistency.
---

# Cross Module Consistency Auditor

## Overview

A structured audit skill for verifying cross-module consistency when a single change propagates across multiple modules, flows, reports, APIs, and copied implementations. This skill maps the blast radius of a change, defines consistency rules that must hold across all affected touchpoints, and produces a review strategy that avoids redundant effort on copy-paste code.

**Core Value**: Prevents the class of defects where "the fix was applied correctly in one place but missed or applied inconsistently elsewhere" -- the root cause behind aggregation mismatches, sign-inversion bugs, report-vs-drilldown discrepancies, and incomplete reverse-flow implementations.

**Scope Boundary**: This skill focuses on cross-module consistency of a known change. For single-function code quality, use `critical-code-reviewer`. For data migration QA, use `migration-validation-explorer`. For incident root cause analysis, use `incident-rca-specialist`.

## When to Use

- A specification change affects multiple screens, reports, APIs, or batch jobs
- The same logic must be replicated across multiple flows (e.g., 6 transaction types)
- Refund / void / cancellation / correction requires sign inversion or reverse journaling
- Report totals and drill-down totals must reconcile
- A canonical implementation was copied to multiple locations and you need an efficient review strategy
- A DB schema change propagates to views, stored procedures, APIs, and UI
- You need to verify that state transition rules are enforced consistently at every entry point
- Tax or rounding logic must be identical across all calculation paths

## Prerequisites

- **Change specification available**: A description of what is changing (feature spec, ticket, PR description)
- **Module inventory accessible**: Ability to identify affected modules, files, or services
- **Output specifications available**: Report definitions, API contracts, UI mockups, or export formats
- **Existing tests identifiable**: Access to test suites or test case documentation

## Inputs

- Change specification or feature description
- Implementation target list (modules, files, services)
- Related module inventory
- Report / API / UI output specifications
- Existing test cases or test suites
- (Optional) Prior review findings or RCA reports

## Outputs

1. **Change Impact Map** -- Visualizes the change kernel, source of truth, and all affected modules/outputs/tests/docs
2. **Cross-Module Consistency Matrix** -- Rules x modules grid showing expected vs actual behavior and gaps
3. **Copy Propagation Review Plan** -- Efficient review strategy separating canonical review from diff-only review
4. **Cross-Module Test Checklist** -- Consistency rules converted to testable assertions with tiers and owners
5. **Open Questions / Missing Modules List** -- Unresolved items and modules that may be affected but lack confirmation (recorded as an appendix in `assets/impact_map_template.md`)

## Workflows

### Workflow 1: Define the Change Kernel (変更核定義)

Identify the atomic unit of change and its canonical representation.

1. Extract the minimal change unit from the specification:
   - New line item type (e.g., adjustment, correction, refund)
   - New calculation rule (e.g., rounding, tax, discount)
   - New status or state transition
   - New aggregation rule or filter condition
   - Schema modification (column addition, type change, constraint)
   - Semantic change (e.g., timestamp meaning shifts from "created" to "submitted")
2. Identify the **source of truth** -- the single authoritative location where this logic is defined or should be defined
3. Document the change kernel using:
   - **What**: Precise description of the change
   - **Where**: Source of truth file/module/function
   - **Why**: Business requirement driving the change
   - **Invariant**: The consistency rule that must hold everywhere this change touches
4. If the change kernel is compound (multiple independent changes bundled), decompose into separate kernels and process each independently

### Workflow 2: Apply Impact Lenses (影響レンズ適用)

Systematically expand the blast radius using eight impact lenses.

1. For each lens below, ask "Does this change affect [lens area]?" and list affected components:
   - **Input flows**: Forms, API endpoints, file imports, message consumers that create or modify data
   - **Persistence**: Database writes, cache updates, event stores, audit logs
   - **Aggregation**: Summation, grouping, rollup, materialized views, batch calculations
   - **Display / Reports**: UI screens, dashboards, PDF reports, Excel exports, email notifications
   - **API / Export**: REST/GraphQL responses, file exports, webhook payloads, integration feeds
   - **Reverse flow**: Refund, void, cancellation, deletion, undo, correction, reversal journal entries
   - **Permission / Visibility**: Role-based access, field-level security, tenant isolation, data masking
   - **Downstream jobs**: Batch processes, scheduled tasks, sync jobs, event-driven subscribers, external system integrations
2. For each affected component, record:
   - Module/file name
   - Whether it reads or writes the affected data
   - Whether it contains a copy of the logic or references the source of truth
3. Load `references/change_impact_analysis_guide.md` for detailed techniques on tracing propagation paths

### Workflow 3: Build the Impact Map (Impact Map作成)

Create a structured impact map from the lens analysis.

1. Use the template from `assets/impact_map_template.md`
2. Fill in all sections:
   - **Change Kernel**: From Workflow 1
   - **Source of Truth**: Canonical implementation location
   - **Affected Modules**: Grouped by lens category (input/persistence/aggregation/display/API/reverse/permission/downstream)
   - **Affected Outputs**: Reports, API responses, exports, notifications
   - **Affected Tests**: Unit tests, integration tests, E2E tests, manual test cases
   - **Affected Documentation**: Technical specs, API docs, user guides, runbooks
   - **Risk Notes**: Modules with high copy count, modules with no test coverage, modules owned by other teams
3. Generate a dependency summary:
   - Count of affected modules per lens
   - Count of copy-paste implementations vs shared-reference implementations
   - Identify modules with **no current test coverage** for the affected behavior
4. Flag any modules where impact is uncertain with `[NEEDS CONFIRMATION]`

### Workflow 4: Define Consistency Rules (Consistency Rules定義)

Define the rules that must hold across all affected modules.

1. Load `references/consistency_rule_catalog.md` for the full category list
2. For each applicable category, define specific rules for this change:
   - **Aggregation totals**: Sum of parts equals whole; included/excluded items are consistent
   - **Status transitions**: Allowed transitions are identical at every entry point; guard conditions match
   - **Sign inversion**: Positive/negative symmetry for forward/reverse flows
   - **Tax / Rounding**: Same calculation method, same precision, same rounding direction everywhere
   - **Visibility / Permission**: Same data is visible/hidden to the same roles across all views
   - **Naming / Constants**: Enum values, status codes, error codes are consistent
   - **Report vs Drill-down**: Summary totals match the sum of detail rows
3. Load `references/aggregation_reconciliation_guide.md` for aggregation-specific rules
4. Load `references/reverse_flow_checklist.md` for reverse-flow-specific rules
5. Populate the consistency matrix using `assets/consistency_matrix_template.md`:
   - One row per module/flow/report/API
   - Columns: Rule, Expected Behavior, Current State, Gap, Owner
6. Mark each cell as: PASS / FAIL / NOT TESTED / NOT APPLICABLE

### Workflow 5: Design Copy Propagation Review Strategy (Copy Propagationレビュー戦略)

Create an efficient review plan for copied implementations.

1. Load `references/copy_propagation_strategy.md`
2. Identify the **canonical implementation** -- the one copy that will receive full, thorough review
3. For all other copies, determine:
   - **Allowed differences**: Intentional variations (different entity type, different field names, different error messages)
   - **Required sameness**: Logic that must be identical (calculation, validation, rounding, sign handling)
4. Define the review approach:
   - **Canonical**: Full line-by-line review with test verification
   - **Copy targets**: Diff-only review against canonical, focusing on required-sameness sections
   - **Exception documentation**: Record every detected difference and classify as allowed or suspicious
5. Populate the template from `assets/copy_propagation_review_template.md`
6. Define the **recheck trigger**: conditions under which all copies must be re-reviewed from scratch (e.g., canonical implementation changes fundamentally)
7. Assess **extraction threshold**: if copy count exceeds 3 and allowed differences are minimal, recommend extracting shared logic into a common module

### Workflow 6: Convert to Test Checklist (テスト観点変換)

Transform consistency rules into a testable checklist.

1. For each consistency rule from Workflow 4, create test assertions:
   - **Cross-module assertion**: Same input produces same output across all modules
   - **Totals reconciliation**: Report total equals sum of drill-down rows
   - **Sign inversion check**: Forward amount + reverse amount = 0 (or net expected value)
   - **Before/after snapshot diff**: State before change vs after change matches specification
   - **Report vs drill-down match**: Summary report numbers reconcile with detail views
   - **Reverse flow symmetry**: Create/refund, entry/void produce symmetric results
2. Assign each test to a tier:
   - **Unit**: Can be tested within a single module
   - **Integration**: Requires two or more modules interacting
   - **E2E**: Requires full system flow from input to output
   - **Manual**: Requires human verification (UI layout, report formatting)
3. Define test data requirements:
   - Standard case data set
   - Boundary case data set (zero amounts, maximum values, empty collections)
   - Reverse flow data set (refund after payment, void after entry)
4. Populate the template from `assets/cross_module_test_checklist_template.md`
5. Assign owners and priority based on gap analysis from Workflow 4

## Resources

| Resource | Type | Purpose | When to Load |
|----------|------|---------|--------------|
| `references/change_impact_analysis_guide.md` | Reference | Source of truth identification, propagation path tracing, upstream/downstream distinction | Workflow 2 |
| `references/consistency_rule_catalog.md` | Reference | Full catalog of consistency rule categories with examples | Workflow 4 |
| `references/copy_propagation_strategy.md` | Reference | Canonical review, diff review, exception handling, extraction threshold | Workflow 5 |
| `references/aggregation_reconciliation_guide.md` | Reference | Total vs subtotal vs drill-down reconciliation, refund/void reversal rules | Workflow 4 |
| `references/reverse_flow_checklist.md` | Reference | Create/update/delete symmetry, entry/refund/void/suspend patterns | Workflow 4 |
| `assets/impact_map_template.md` | Template | Change impact map with all sections | Workflow 3 |
| `assets/consistency_matrix_template.md` | Template | Cross-module consistency matrix | Workflow 4 |
| `assets/copy_propagation_review_template.md` | Template | Copy propagation review plan | Workflow 5 |
| `assets/cross_module_test_checklist_template.md` | Template | Test checklist derived from consistency rules | Workflow 6 |

## Worked Example: Multi-Flow Rounding Change

This example illustrates the full workflow for a cash rounding rule change that affects 6 transaction flows.

**Scenario**: A POS system needs to add cash rounding (round to nearest 0.05) to all cash payment transactions. The system has 6 transaction flows: Sale, Return, Exchange, Layaway Payment, Layaway Pickup, and Account Payment.

**Step 1 -- Change Kernel**:
- What: Insert cash rounding adjustment line when payment method is cash
- Where: `payment_calculator.apply_cash_rounding()` (source of truth)
- Invariant: `rounded_total = round_to_increment(original_total, Decimal("0.05"))` and `adjustment = rounded_total - original_total` (use decimal/fixed-point arithmetic — never float for monetary calculations)

**Step 2 -- Impact Lenses**:
- Input flows: 6 transaction entry screens
- Persistence: transaction_lines table, adjustment_lines table
- Aggregation: Daily cash summary, shift report, GL posting
- Display: Receipt, transaction detail screen
- API: POS-to-HQ sync payload
- Reverse flow: Return must reverse the rounding adjustment
- Permission: N/A (all cashiers see rounding)
- Downstream: HQ consolidation, tax filing extract

**Step 3 -- Impact Map**: 6 input modules, 2 persistence modules, 3 aggregation modules, 4 display modules, 1 API module, 1 reverse flow module = 17 total touchpoints.

**Step 4 -- Consistency Rules**:
- Rule 1: All 6 flows use identical rounding formula
- Rule 2: Rounding adjustment appears as a distinct line item (not merged into product lines)
- Rule 3: Return flow reverses rounding with opposite sign
- Rule 4: Daily cash summary includes rounding adjustments in total
- Rule 5: Receipt displays rounding adjustment as separate line
- Rule 6: HQ sync payload includes rounding adjustment line

**Step 5 -- Copy Propagation Review**:
- Canonical: Sale flow (full review)
- Copy targets: Return, Exchange, Layaway Payment, Layaway Pickup, Account Payment (diff review)
- Allowed differences: Transaction type enum, flow-specific validation
- Required sameness: Rounding formula, adjustment line creation, sign handling

**Step 6 -- Test Checklist**:
- Unit: Rounding formula produces correct result for boundary values (0.01, 0.02, 0.03, 0.04, 0.05)
- Integration: Each flow creates correct adjustment line in DB
- E2E: Receipt total matches DB total for each flow
- Cross-module: Daily summary total = sum of all transaction totals (including rounding adjustments)
- Reverse: Sale(100.03) + Return(100.03) rounding adjustments net to zero

## Best Practices

### Source of Truth Discipline
- Every piece of logic should have exactly one source of truth
- Copies should be documented and tracked in the impact map
- When copy count exceeds 3 with minimal allowed differences, recommend extraction to shared module
- Review the source of truth first and most thoroughly; review copies via diff

### Completeness Over Depth
- It is more important to identify all affected modules than to deeply analyze one module
- Use the 8 impact lenses systematically -- do not skip lenses because they "probably" do not apply
- Flag uncertain modules with `[NEEDS CONFIRMATION]` rather than omitting them
- An incomplete impact map is the primary cause of post-deployment consistency bugs

### Reverse Flow Is Not Optional
- Every forward flow that creates data should have an identified reverse flow
- If no reverse flow exists, document this as a gap (it may be intentional or it may be a missing requirement)
- Reverse flows must be sign-symmetric: the sum of forward and reverse operations should produce the expected net result
- Test reverse flows with the same rigor as forward flows

### Consistency Rules Must Be Testable
- A consistency rule that cannot be expressed as a pass/fail assertion is too vague
- Each rule should reference specific modules, specific fields, and specific expected values
- Prefer automated assertions over manual verification
- Every FAIL in the consistency matrix should produce a ticket or action item with an owner
