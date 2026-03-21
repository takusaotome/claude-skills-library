---
layout: default
title: Hidden Contract Investigator
grand_parent: English
parent: Software Development
nav_order: 10
lang_peer: /ja/skills/dev/hidden-contract-investigator/
permalink: /en/skills/dev/hidden-contract-investigator/
---

# Hidden Contract Investigator
{: .no_toc }

Extract implicit contracts from existing code and assess reuse risk before integration.
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

Hidden Contract Investigator systematically extracts **implicit contracts** from existing code before reuse. Instead of trusting function names, comments, or type annotations at face value, it traces actual code paths to uncover real return types, hidden side effects, implicit preconditions, and environment-dependent behavior.

Many production defects originate not from new code bugs, but from **misunderstanding the actual behavior of reused code**. A function named `keepTwoDecimal()` that returns a comma-formatted string, an `isValid()` that triggers side effects, a `getUser()` that returns cached stale data -- these hidden contracts are the real source of integration failures.

## When to Use

- Reusing existing functions, modules, or services in a new feature
- Working with legacy code where names and comments may be unreliable
- Investigating actual return types, side effects, and exception paths before integration
- Assessing whether existing code assets are safe to reuse as-is
- Preparing contract tests for critical integration points
- Onboarding onto an unfamiliar codebase to understand actual behavior

## Workflows

The investigation follows six workflows:

### 1. Target Identification

Identify reuse candidates at the appropriate granularity (single function, class, service boundary, DB persistence boundary, external API). Document location, current consumers, last modification date, and test coverage. Prioritize by criticality, complexity, and staleness.

### 2. Surface Contract Recording

Record what the code **appears** to promise based on names, documentation, type annotations, and caller usage patterns. Mark everything as UNVERIFIED at this stage -- trust nothing yet.

### 3. Actual Contract Extraction

Read the actual implementation to discover the real behavioral contract: return value types and formatting, side effects (DB writes, cache updates, event emissions), hidden preconditions (call ordering, initialization state), exception paths, and environment-dependent behavior.

### 4. Mismatch Classification

Compare surface contracts against actual contracts and classify every discrepancy into six categories:

| Category | Description | Example |
|:---------|:------------|:--------|
| **Naming Mismatch** | Name implies different behavior | `keepTwoDecimal()` returns comma-formatted string |
| **Type Mismatch** | Return/parameter type differs from expectation | Annotated as `float`, actually returns `str` |
| **Scope Mismatch** | Same-named identifiers in different scopes | Module-level `config` vs function-level `config` |
| **State Dependency** | Behavior depends on external mutable state | Result changes based on global cache content |
| **Environment Dependency** | Behavior varies across environments | Works in dev (SQLite), fails in prod (PostgreSQL) |
| **Hidden Side Effect** | Undocumented writes or mutations | `calculate_total()` also updates a DB record |

Each mismatch is rated by severity, likelihood, and blast radius.

### 5. Reuse Feasibility Judgment

Apply a five-level reuse classification:

| Level | Verdict | Meaning |
|:------|:--------|:--------|
| **A** | Reuse as-is | Contracts match, behavior verified |
| **B** | Reuse with wrapper | Core logic correct, interface needs adaptation |
| **C** | Reuse with adapter | Significant interface mismatch, logic is sound |
| **D** | Contract test first | Behavior uncertain, verification needed before deciding |
| **E** | Do not reuse | Fundamental mismatch or unacceptable risk |

### 6. Verification Design

Design contract tests for critical mismatches. Define minimal test cases, boundary data sets, failure signal interpretation, and regression value.

## Key Outputs

| Deliverable | Content |
|:------------|:--------|
| Implicit Contract Sheet | Stated vs. observed contracts with evidence |
| Reuse Risk Register | Risk assessment per reuse candidate |
| Contract Verification Test Ideas | Test designs to lock down critical contracts |
| Adoption Recommendation | Reuse decision with guardrails and prerequisites |

## Resources

| Resource | Type | Purpose |
|:---------|:-----|:--------|
| `references/contract_extraction_guide.md` | Reference | Extraction methodology and evidence priority |
| `references/hidden_spec_patterns.md` | Reference | Full mismatch pattern catalog |
| `references/runtime_boundary_checklist.md` | Reference | Boundary-specific checklists |
| `references/reuse_risk_classification.md` | Reference | 5-level reuse classification framework |
| `references/environment_behavior_guide.md` | Reference | Environment-dependent behavior patterns |
| `assets/implicit_contract_sheet_template.md` | Template | Implicit contract documentation |
| `assets/reuse_risk_register_template.md` | Template | Risk register |
| `assets/contract_test_idea_template.md` | Template | Test design |
| `assets/adoption_recommendation_template.md` | Template | Adoption recommendation |

## Best Practices

- **Trust behavior over documentation** -- function names and comments drift from implementation. The code is the only source of truth.
- **Read tests first** -- test assertions are machine-verified contracts and more reliable than docstrings.
- **Read callers before comments** -- how existing callers use a function reveals the actual contract more reliably than documentation.
- **Focus on boundaries** -- the most dangerous hidden contracts live where data crosses function, module, service, DB, or serialization boundaries.
- **Every critical mismatch needs a contract test** -- contract tests verify the interface promise, not internal logic. Name them after the contract they protect.

## Related Skills

- [Critical Code Reviewer]({{ '/en/skills/dev/critical-code-reviewer/' | relative_url }}) -- review already-written code
- [TDD Developer]({{ '/en/skills/dev/tdd-developer/' | relative_url }}) -- implement contract tests
