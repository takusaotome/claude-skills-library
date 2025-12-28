---
name: migration-validation-explorer
description: Exploratory data-migration validation and QA ideation workflow. Use when you need to discover hidden risks, generate new validation angles, and converge mapping specs/validation reports into a prioritized QA backlog for CRM migrations.
version: 1.2
last_updated: 2025-12-28
---

# Migration Validation Explorer

A repeatable, **inventive exploratory** workflow to discover hidden risks in CRM migration data, then converge them into a QA-ready backlog.

## When to Use

- Mapping spec, validation plan, and validation report exist
- You suspect **undiscovered issues** (coverage gaps, silent failures, edge cases)
- Need to generate new validation angles beyond standard checklists

## What "Detection" Means

1. **Spec ambiguity**: contradiction, missing rule, unclear definition
2. **Verification-ready hypothesis**: concrete check (query/diff/sample) with pass/fail criteria
3. **Coverage gap**: existing validation misses this area or only tests happy path
4. **Behavioral risk**: data matches but system behavior will diverge (approvals, reports, integrations)

---

## Inputs Required

**Minimum:**
- Mapping spec (latest)
- Data model/schema (objects, fields, relationships)
- Validation plan + report(s)
- Dataset extracts (legacy + transformed + loaded)

**Locate files:**
```bash
rg --files -g '*validation*report*'
rg --files -g '*mapping*spec*'
```

---

## Core Principles

### 1. Triangulate: Never Trust a Single Oracle
Use >= 2 oracles per check:
- Record counts by segment
- Sum checks (money) + reconciliation
- Referential integrity
- UI views vs admin queries
- Report totals vs drill-down

### 2. "Missing" Might Mean "Not Visible"
Always validate both:
- **Admin view** (truth of storage)
- **Business-user view** (truth of operation)

### 3. Convergence Is a Product
Every cycle must produce:
- A runnable check, OR
- A clarified rule, OR
- A regression test, OR
- A monitoring metric

---

## Workflow Overview

### Step 0: Preparation

**0.1 Establish Mission:**
- Identify business-critical flows (money, compliance, customer impact)
- Define acceptance thresholds (allowable mismatch %, max missing refs)

**0.2 Build Focus Catalog (>= 20 items):**
> Load `references/focus_catalog.md` for the full category list

Key buckets: Keys/IDs, Relationships, Normalization, Status/Stage, Ownership, Dates, Money, Volume/Dedup, Automation, Integrations, Reporting, Archiving

---

### Step 1: Random Focus Cycle (x10)

Pick **one** focus item randomly. For each:

1. **Focus**: One catalog item
2. **Diverge**: Generate 6-12 failure mode hypotheses
   > Load `references/divergence_library.md` for failure mode patterns
3. **Converge**: Select top 2-3 plausible/high-impact risks
4. **Verify**: Define minimal experiments (queries, diffs, samples)
5. **Deepen**: Root cause -> remediation -> prevention
6. **Generalize**: Apply pattern to >= 2 other objects/flows

**Output per cycle:** Use template from `assets/exploration_log_template.md`

---

### Step 2: Cross-Pollination Cycle (x10)

Pick **two lenses** and fuse them into new hypotheses.

> Load `references/lens_library.md` for available lenses

1. **Lens A + Lens B** -> new hypothesis
2. **Apply** to specific object/relationship/integration
3. **Verify** with targeted checks
4. **Converge** into Go/No-Go or follow-up
5. **Generalize** into reusable test or monitoring rule

---

### Step 3: Converge Into QA Backlog

Create backlog using `assets/qa_backlog_template.md`:

| Check | Scope | Risk | Evidence | Method | Pass Criteria | Owner | Status |
|-------|-------|------|----------|--------|---------------|-------|--------|

**Risk scoring:** Impact x Likelihood x Detectability (H/M/L)

---

## Root Cause Taxonomy

When issue is verified, classify:

**Root Cause:**
- Spec/definition (ambiguous rule)
- Mapping/transform (wrong mapping, missing branch)
- Load/automation (triggers suppressed/over-fired)
- Operations/monitoring (silent failures)

**Remediation:**
- Data fix (backfill, re-transform)
- Design fix (model, field types, security)
- Process fix (migration mode, runbook)
- Monitoring fix (reconciliations, alerts)

---

## Quick Start: High-Impact Checks

If you must prioritize, start here:
> See `references/seed_examples.md` for detailed examples

1. Month-end boundaries (timezone/DateTime)
2. Invoice totals + lifecycle status
3. Cross-department view correctness
4. Migration-mode automation control
5. Integration retry idempotency
6. Archive usability (searchable + permissioned)

---

## Resources

| Resource | Purpose | When to Load |
|----------|---------|--------------|
| `references/focus_catalog.md` | Full focus category list | Step 0.2 |
| `references/divergence_library.md` | Failure mode patterns | Step 1 (Diverge) |
| `references/lens_library.md` | Cross-pollination lenses | Step 2 |
| `references/seed_examples.md` | Worked examples | When stuck |
| `assets/exploration_log_template.md` | Per-cycle output | Step 1, 2 |
| `assets/qa_backlog_template.md` | Final backlog + gates | Step 3 |

---

## Output Summary

**Per-cycle output:**
```
Cycle #: [n]
Focus: [item]
Divergent: [6-12 hypotheses]
Converged: [top 2-3 risks]
Checks: [verification methods]
Result: Pass/Fail/Unknown
Actions: [remediation + generalization]
```

**Final deliverables:**
- Prioritized QA backlog table
- Quality gates checklist
- Open questions/assumptions
