---
layout: default
title: Completion Quality Gate Designer
grand_parent: English
parent: Meta & Quality
nav_order: 10
lang_peer: /ja/skills/meta/completion-quality-gate-designer/
permalink: /en/skills/meta/completion-quality-gate-designer/
---

# Completion Quality Gate Designer
{: .no_toc }

Design completion criteria, quality gates, evidence requirements, and exception governance for each project phase.
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

Completion Quality Gate Designer creates the structure and rules that define what "done" means at each stage of a software project. It produces reusable quality gate matrices, completion vocabulary definitions, evidence ownership mappings, exception registers, and release readiness checklists.

The core problem: teams often conflate "code is written" with "quality is confirmed" with "ready to ship." When these concepts are not explicitly separated, test gaps become invisible, metrics diverge across documents, and known limitations are buried under blanket "all OK" statements.

## When to Use

- Starting a new project and need to define "Definition of Done" per phase
- Test reports, completion summaries, and release decision documents are inconsistent
- You want standardized verification commands shared across developers, CI, and reports
- You need to define exception governance for carrying forward incomplete items
- You need to explicitly separate "implemented," "verified," and "releasable"
- Designing release readiness criteria or CI/CD pipeline quality gates
- Standardizing verification evidence across teams

## Workflows

Seven phases drive the quality gate design:

### Phase 1: Scope Phases and Gate Units

Select a gate organization pattern based on the project lifecycle model (waterfall, sprint milestones, or deliverable-based). Assign each gate an ID, name, and dependency chain.

### Phase 2: Separate Completion Vocabulary

Define precise terminology to prevent "done" from meaning different things to different people:

| State | Definition |
|:------|:-----------|
| **Implemented** | Code committed; no quality assertion implied |
| **Verified** | Standard verification commands passed; evidence recorded |
| **Accepted** | Designated approver reviewed evidence and signed off |
| **Released** | Deployed to production and confirmed operational |
| **Exception-approved** | Known incomplete items approved with conditions |

Prohibited expressions (e.g., "all OK" when exceptions exist) are also defined.

### Phase 3: Define Exit Criteria

For each gate, specify required inputs, evidence, standard commands, owner, approver, pass rule, failure handling, and carryover policy.

### Phase 4: Pin Evidence Sources and Metrics

Define the single authoritative source for each metric, eliminating discrepancies. Apply the **Auto-First Principle**: if a metric can be auto-collected from CI, manual override is prohibited.

### Phase 5: Fix Standard Verification Commands

Create a canonical command set so "tests pass" means the same thing everywhere. Document exact invocation, coverage scope, exclusions, execution environment, and gate assignment.

### Phase 6: Design Exception Governance

Define rules for carrying forward incomplete items under controlled conditions. Specify exception-eligible/ineligible items, required record fields (what, why, risk, temporary control, due date, owner, approver, closure evidence), escalation paths, and expiration rules.

### Phase 7: Enforce Expression Control

Prevent misleading language in reports and status communications. Define prohibited expressions, required qualifiers for each completion state, and assemble all outputs into a release readiness package.

## Key Outputs

| Deliverable | Content |
|:------------|:--------|
| Quality Gate Matrix | Gates with entry/exit criteria, evidence, owners, exception rules |
| Definition of Done | Completion state definitions with vocabulary separation |
| Standard Verification Command Set | Fixed commands for CI, developers, and reports |
| Exception Register | Tracked exceptions with risk, controls, and expiration |
| Evidence-to-Owner Mapping | Evidence items with source (auto/manual), owner, reconciliation rules |

## Resources

| Resource | Type | Purpose |
|:---------|:-----|:--------|
| `references/gate_patterns.md` | Reference | Phase-based gate patterns |
| `references/definition_of_done_framework.md` | Reference | Completion state definition framework |
| `references/evidence_catalog.md` | Reference | Evidence type inventory |
| `references/metrics_reconciliation_guide.md` | Reference | Metrics reconciliation rules |
| `references/exception_governance.md` | Reference | Exception eligibility and governance |
| `assets/quality_gate_matrix_template.md` | Template | Quality gate matrix |
| `assets/definition_of_done_template.md` | Template | Completion state definitions |
| `assets/exception_register_template.md` | Template | Exception tracking |
| `assets/release_readiness_template.md` | Template | Release decision document |
| `assets/evidence_ownership_matrix_template.md` | Template | Evidence ownership |

## Best Practices

- **Separate owner and approver** -- the person who produces evidence must never be the sole approver. For small teams, use cross-functional review.
- **Auto-first evidence collection** -- if a metric can be auto-collected from CI, do not accept manual entry as the primary source. When auto and manual conflict, auto takes precedence.
- **Exception discipline** -- every exception must have an expiration date. Exceptions require both the risk and the temporary control that mitigates it.
- **Expression precision** -- ban "all" and "complete" as standalone status words; always qualify with scope and conditions.
- **Living documents** -- revisit gate definitions at each retrospective. When a gate fails to catch a production escape, update criteria as part of the RCA corrective actions.

## Related Skills

- [Critical Code Reviewer]({{ '/en/skills/dev/critical-code-reviewer/' | relative_url }}) -- code review against gate criteria
- [Dual-Axis Skill Reviewer]({{ '/en/skills/meta/dual-axis-skill-reviewer/' | relative_url }}) -- multi-axis quality evaluation
