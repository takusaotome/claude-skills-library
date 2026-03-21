---
layout: default
title: Cross Module Consistency Auditor
grand_parent: English
parent: Meta & Quality
nav_order: 11
lang_peer: /ja/skills/meta/cross-module-consistency-auditor/
permalink: /en/skills/meta/cross-module-consistency-auditor/
---

# Cross Module Consistency Auditor
{: .no_toc }

Audit cross-module consistency when a single change propagates across multiple modules and flows.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-workflow">Workflow</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Cross Module Consistency Auditor verifies **cross-module consistency** when a single change propagates across multiple modules, flows, reports, APIs, and copied implementations. It maps the blast radius of a change, defines consistency rules that must hold across all affected touchpoints, and produces a review strategy that avoids redundant effort on copy-paste code.

The class of defects this skill prevents: "the fix was applied correctly in one place but missed or applied inconsistently elsewhere" -- the root cause behind aggregation mismatches, sign-inversion bugs, report-vs-drilldown discrepancies, and incomplete reverse-flow implementations.

## When to Use

- A specification change affects multiple screens, reports, APIs, or batch jobs
- The same logic must be replicated across multiple flows (e.g., 6 transaction types)
- Refund, void, or cancellation requires sign inversion or reverse journaling
- Report totals and drill-down totals must reconcile
- A canonical implementation was copied to multiple locations and needs efficient review
- A DB schema change propagates to views, stored procedures, APIs, and UI
- State transition rules must be enforced consistently at every entry point
- Tax or rounding logic must be identical across all calculation paths

## Workflows

Six workflows drive the cross-module audit:

### 1. Define the Change Kernel

Identify the atomic unit of change and its canonical representation. Document the change (What), source of truth location (Where), business requirement (Why), and the invariant that must hold everywhere (Invariant). Decompose compound changes into separate kernels.

### 2. Apply Impact Lenses

Systematically expand the blast radius using eight lenses:

| Lens | Scope |
|:-----|:------|
| Input flows | Forms, API endpoints, file imports |
| Persistence | DB writes, cache updates, audit logs |
| Aggregation | Summation, grouping, rollup, materialized views |
| Display / Reports | UI screens, dashboards, PDF, Excel, email |
| API / Export | REST/GraphQL responses, file exports |
| Reverse flow | Refund, void, cancellation, reversal journal |
| Permission / Visibility | Role-based access, tenant isolation |
| Downstream jobs | Batch processes, sync jobs, external integrations |

### 3. Build the Impact Map

Create a structured impact map from the lens analysis covering affected modules, outputs, tests, and documentation. Flag modules with no test coverage and uncertain impact.

### 4. Define Consistency Rules

Define rules that must hold across all affected modules: aggregation totals, status transitions, sign inversion, tax/rounding, visibility/permissions, naming/constants, and report-vs-drilldown matching. Populate a rules x modules matrix with PASS/FAIL/NOT TESTED/NOT APPLICABLE ratings.

### 5. Design Copy Propagation Review Strategy

Create an efficient review plan for copied implementations. Perform full review on the canonical implementation; review other copies via diff only. Clearly separate allowed differences (entity types, field names) from required sameness (calculation, validation, sign handling). Recommend shared module extraction when copy count exceeds 3 with minimal differences.

### 6. Convert to Test Checklist

Transform consistency rules into testable assertions: cross-module assertions, totals reconciliation, sign inversion checks, report-vs-drilldown matching, and reverse flow symmetry. Assign each test to Unit, Integration, E2E, or Manual tiers.

## Key Outputs

| Deliverable | Content |
|:------------|:--------|
| Change Impact Map | Visualization from change kernel to affected modules, outputs, tests, docs |
| Cross-Module Consistency Matrix | Rules x modules grid with expected vs actual behavior and gaps |
| Copy Propagation Review Plan | Canonical review + diff-only review strategy |
| Cross-Module Test Checklist | Consistency rules as testable assertions with tiers and owners |
| Open Questions / Missing Modules List | Unresolved items and unconfirmed affected modules |

## Resources

| Resource | Type | Purpose |
|:---------|:-----|:--------|
| `references/change_impact_analysis_guide.md` | Reference | Propagation path tracing techniques |
| `references/consistency_rule_catalog.md` | Reference | Consistency rule category catalog |
| `references/copy_propagation_strategy.md` | Reference | Canonical review and diff review strategy |
| `references/aggregation_reconciliation_guide.md` | Reference | Total/subtotal/drill-down reconciliation |
| `references/reverse_flow_checklist.md` | Reference | Reverse flow symmetry checklist |
| `assets/impact_map_template.md` | Template | Impact map |
| `assets/consistency_matrix_template.md` | Template | Consistency matrix |
| `assets/copy_propagation_review_template.md` | Template | Copy propagation review plan |
| `assets/cross_module_test_checklist_template.md` | Template | Test checklist |

## Best Practices

- **Source of truth discipline** -- every piece of logic should have exactly one canonical location. Track copies in the impact map. When copy count exceeds 3, recommend extraction to a shared module.
- **Completeness over depth** -- identifying all affected modules is more important than deeply analyzing one. Apply all 8 impact lenses systematically; do not skip lenses that "probably" do not apply.
- **Reverse flow is not optional** -- every forward flow that creates data should have an identified reverse flow. If none exists, document it as a gap. Test reverse flows with the same rigor as forward flows.
- **Consistency rules must be testable** -- a rule that cannot be expressed as a pass/fail assertion is too vague. Reference specific modules, fields, and expected values.

## Related Skills

- [Critical Code Reviewer]({{ '/en/skills/dev/critical-code-reviewer/' | relative_url }}) -- single-module code quality review
- [Hidden Contract Investigator]({{ '/en/skills/dev/hidden-contract-investigator/' | relative_url }}) -- implicit contract investigation
