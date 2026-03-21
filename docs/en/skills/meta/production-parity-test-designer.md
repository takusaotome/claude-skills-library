---
layout: default
title: Production Parity Test Designer
grand_parent: English
parent: Meta & Quality
nav_order: 12
lang_peer: /ja/skills/meta/production-parity-test-designer/
permalink: /en/skills/meta/production-parity-test-designer/
---

# Production Parity Test Designer
{: .no_toc }

Design test hierarchies that catch production failures before production.
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

Production Parity Test Designer ensures **production failures are caught before production**. Rather than increasing test count, this skill focuses on **which test tier should cover which production gap**, eliminating proxy metrics (tests that pass but miss real failures) and structuring a layered defense from PR CI through release packaging.

Core philosophy: **Tests exist to reproduce production failure modes.** If a test cannot fail in the same way production fails, it provides false confidence.

## When to Use

- PR CI is too lightweight to detect production divergence
- DB dialect differences exist (e.g., SQLite vs PostgreSQL)
- UI shows success but data is not persisted to the database
- Mocks hide runtime import errors
- Timezone, locale, OS, or dependency differences surface only in production
- The boundary between unit tests and smoke tests is unclear
- Past critical defects need to be structured as regression prevention tests
- Packaging or container build integrity needs to be guaranteed

## Workflows

Eight steps drive the test hierarchy design:

### Step 1: Production Gap Inventory

Enumerate all differences between dev/CI and production environments across categories: DB dialect, OS/container, dependency installation, environment variables, timezone/locale, real vs mock, serialization, and packaging/deployment.

### Step 2: Failure Mode Enumeration

For each gap, define concrete failure modes. Examples: SQLite passes but PostgreSQL throws syntax error on UPSERT; UI shows success toast but INSERT silently fails; `import cv2` works in dev but fails in production container. Classify by visibility (silent/loud), blast radius, and detection difficulty.

### Step 3: Test Tier Allocation

Assign each failure mode to the optimal test tier:

| Tier | Scope |
|:-----|:------|
| **Unit** | Pure logic, boundary values, input validation |
| **Integration** | Real DB operations, repository operations, multi-component |
| **E2E** | UI action -> persistence verification -> business-visible outcome |
| **Smoke** | Minimum parity checks in every PR |
| **Packaging** | Install, import, build, container image integrity |
| **Nightly / Heavy** | Full parity suite, performance baselines |

### Step 4: Proxy Metric Elimination

Identify and remediate tests that provide false confidence: UI-only verification (never queries DB), mock-only coverage (never tests real dependencies), coverage theater (high line coverage but no boundary testing), happy-path bias.

### Step 5: PR Smoke Suite Definition

Define the minimum production parity checks for every PR within a 2-5 minute runtime budget: DB dialect smoke, import smoke, persistence smoke, timezone smoke, and serialization smoke.

### Step 6: Adversarial Regression Backlog

Create regression tests from past defects and attack patterns. For each incident, define the exploit/failure pattern, minimal reproducible scenario, expected protected behavior, and regression scope.

### Step 7: Packaging / Dependency Integrity Checklist

Verify that the application builds, installs, and imports correctly in a production-equivalent environment: lockfile alignment, clean install, all top-level imports succeed, main entry point starts, and container image matches production.

### Step 8: Standard Command Map

Define named test commands for each execution context: local fast, PR CI required, nightly parity, staging E2E, and release packaging.

## Key Outputs

| Deliverable | Content |
|:------------|:--------|
| Production Gap Inventory | Dev/CI vs production difference list |
| Test Tier Allocation Matrix | Failure modes mapped to optimal test tiers |
| PR Smoke Suite Proposal | Minimum parity checks for every PR |
| Adversarial Regression Backlog | Regression prevention tests from past defects |
| Packaging / Dependency Integrity Checklist | Install, import, build verification |
| Standard Test Command Map | Named commands per execution context |

## Resources

| Resource | Type | Purpose |
|:---------|:-----|:--------|
| `references/production_gap_catalog.md` | Reference | Production gap taxonomy |
| `references/test_tier_strategy.md` | Reference | Tier responsibilities and tradeoffs |
| `references/adversarial_test_patterns.md` | Reference | Attack and failure pattern catalog |
| `references/persistence_verification_guide.md` | Reference | Persistence verification patterns |
| `references/packaging_integrity_guide.md` | Reference | Packaging and dependency integrity |
| `references/timezone_dialect_boundary_guide.md` | Reference | Timezone, DB dialect, locale |
| `assets/test_tier_matrix_template.md` | Template | Test tier allocation table |
| `assets/smoke_suite_template.md` | Template | Smoke suite specification |
| `assets/adversarial_regression_template.md` | Template | Regression backlog |
| `assets/packaging_checklist_template.md` | Template | Packaging checklist |
| `assets/command_map_template.md` | Template | Command map |

## Best Practices

- **Production gaps first, test count second** -- start by asking "what production failures are invisible to our current tests?" not "how many tests do we need?"
- **Persistence over presentation** -- every E2E test checking UI display must also verify the underlying data store. "Success toast appeared" is not a valid assertion.
- **Runtime budget discipline** -- PR smoke suites must have a 2-5 minute budget. Tests over budget get demoted to nightly, not skipped.
- **Mock minimization** -- do not mock your own database, file storage, or message queue. Every mock should have a corresponding integration test with the real dependency.
- **Environment parity in CI** -- CI should match production: same DB engine, same OS family, same timezone config. Use service containers, not in-memory substitutes.

## Related Skills

- [TDD Developer]({{ '/en/skills/dev/tdd-developer/' | relative_url }}) -- implement test code
- [Completion Quality Gate Designer]({{ '/en/skills/meta/completion-quality-gate-designer/' | relative_url }}) -- design quality gates
