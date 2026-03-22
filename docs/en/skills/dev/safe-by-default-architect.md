---
layout: default
title: Safe By Default Architect
grand_parent: English
parent: Software Development
nav_order: 11
lang_peer: /ja/skills/dev/safe-by-default-architect/
permalink: /en/skills/dev/safe-by-default-architect/
---

# Safe By Default Architect
{: .no_toc }

Convert recurring dangerous patterns into safe architectural defaults and enforceable standards.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/safe-by-default-architect.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/safe-by-default-architect){: .btn .fs-5 .mb-4 .mb-md-0 }
<span class="badge badge-workflow">Workflow</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Safe By Default Architect converts recurring dangerous implementation patterns into **safe architectural defaults** and **enforceable standards**. Rather than catching unsafe code during review, it designs the codebase so that the safe way is the easy way and the dangerous way requires deliberate effort.

Core philosophy: **If a developer can accidentally write dangerous code, the architecture has failed.** This skill designs wrappers, abstractions, forbidden-to-safe mappings, static analysis rules, and exception governance so that safety is the default, not an opt-in behavior.

## When to Use

- Repeated defects of the same class appear across multiple PRs or services
- Raw SQL, opt-in authorization, or direct file path construction appears in controller layers
- No common service layer exists for cross-cutting concerns (auth, file I/O, datetime handling)
- You need to convert RCA findings into enforceable coding standards
- Static analysis rules (lint/semgrep/custom checks) need to be designed
- A "forbidden patterns" list needs approved alternatives
- A new project needs safe-by-default foundations from day one

## Workflows

Six workflows drive the safe-by-default design process:

### 1. Recurring Pattern Aggregation

Collect dangerous patterns from RCA reports, bug tickets, review findings, and security scan results. Record pattern name, frequency, example code, and affected components. Deduplicate and consolidate into 10-30 distinct patterns.

### 2. Danger Classification

Classify each pattern by its threat mechanism:

| Category | Description |
|:---------|:------------|
| **Injection / Bypass / Traversal** | Attacker-controlled input reaches sensitive operations |
| **Silent Corruption** | Data modified or lost without error or notification |
| **Environment Divergence** | Behavior differs between dev/staging/production |
| **Hidden Dependency** | Implicit coupling that breaks under change |
| **Human Error Amplification** | Design makes mistakes easy and recovery hard |
| **Unverifiable Behavior** | Cannot confirm correctness through testing alone |

Rank patterns by `frequency x blast_radius x detection_difficulty`.

### 3. Safe Standard Definition

For each forbidden pattern, define the approved safe alternative: the prohibited practice, the approved pattern, the required abstraction (common layer or wrapper), the minimum contract test, the static rule candidate, and the review checkpoint.

### 4. Safe Default Decision

Establish project-wide safe defaults:

| Area | Default |
|:-----|:--------|
| Query construction | ORM / parameterized queries only; raw SQL prohibited |
| Authorization | Deny-by-default; every endpoint requires explicit permission |
| File operations | Service-layer abstraction only; no direct path construction |
| Persistence confirmation | UI success message only after persistence is confirmed |
| DateTime handling | UTC-aware normalization at persistence boundary |
| Dependency loading | Explicit injection; no implicit service locator or global state |

Each default includes an escape hatch (how to override when genuinely needed) and an enforcement mechanism.

### 5. Common Layer and Exception Design

Design shared infrastructure that makes safe defaults easy. Define exception conditions classified by approval level: review-required (peer review), approval-required (tech lead/security sign-off), and prohibited (no exception allowed).

### 6. Operational Rule Deployment

Convert standards into enforceable rules: lint/semgrep rule candidates, coding standard entries, review checklist addendum, and a phased rollout plan (Warning -> Error -> Codebase-wide enforcement).

## Key Outputs

| Deliverable | Content |
|:------------|:--------|
| Safe Pattern Catalog | Approved patterns per category with rationale |
| Forbidden Pattern List | Anti-patterns with danger classification and alternatives |
| Common Layer Design | Shared services and abstraction recommendations |
| Static Rule Candidate List | Lint/semgrep rule proposals with false positive assessment |
| Exception Handling Rule | Deviation approval conditions and procedures |
| Review Checklist Addendum | Additions to existing code review checklists |

## Resources

| Resource | Type | Purpose |
|:---------|:-----|:--------|
| `references/safe_pattern_catalog.md` | Reference | Safe patterns by category |
| `references/forbidden_patterns.md` | Reference | Forbidden patterns with danger classification |
| `references/boundary_hardening_guide.md` | Reference | Boundary-specific hardening techniques |
| `references/static_rule_design_guide.md` | Reference | Static analysis rule design |
| `references/exception_policy.md` | Reference | Exception conditions and approval levels |
| `assets/safe_standard_template.md` | Template | Per-rule documentation |
| `assets/forbidden_to_safe_mapping_template.md` | Template | Forbidden-to-safe mapping table |
| `assets/static_rule_candidate_template.md` | Template | Static analysis rule specification |
| `assets/architecture_decision_record_template.md` | Template | Architecture Decision Record |

## Best Practices

- **Make the safe way the easy way** -- if the safe pattern requires more effort than the dangerous one, adoption will fail. Design wrappers that are more convenient than raw access.
- **Forbid, do not discourage** -- "Prefer ORM" is ignored; "Raw SQL triggers CI failure" is enforced. Use enforcement mechanisms, not suggestions.
- **Pair every prohibition with an alternative** -- a forbidden pattern list without approved alternatives creates frustration and workarounds.
- **Adopt incrementally** -- start with the 3-5 highest-frequency, highest-impact rules (they typically cover 80% of recurring defects). Roll out as warnings first, then errors, then codebase-wide enforcement.
- **Expect exceptions** -- zero exceptions usually means the rules are too loose. Every exception must be documented in code and tracked via ADR.

## Related Skills

- [Critical Code Reviewer]({{ '/en/skills/dev/critical-code-reviewer/' | relative_url }}) -- review existing code against standards
- [Hidden Contract Investigator]({{ '/en/skills/dev/hidden-contract-investigator/' | relative_url }}) -- investigate implicit contracts in existing code
