---
name: migration-validation-explorer
description: Exploratory data-migration validation and QA ideation workflow. Use when you need to discover hidden risks, generate new validation angles, and converge mapping specs/validation reports into a prioritized QA backlog for CRM migrations.
version: 2.0
last_updated: 2025-12-28
---

# Migration Validation Explorer

A repeatable, **inventive exploratory** workflow to discover hidden risks in CRM migration data, then converge them into a QA-ready backlog.

## When to Use

- Mapping spec, validation plan, and validation report exist
- You suspect **undiscovered issues** (coverage gaps, silent failures, edge cases)
- Need to generate new validation angles beyond standard checklists
- Want automated data profiling and hypothesis testing

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

### 4. ID Normalization Is Critical
**Learned Pattern**: Float format `.0` suffix causes ID comparison failures.
```python
# ALWAYS normalize IDs before comparison
def normalize_id(id_val):
    if pd.isna(id_val):
        return None
    return str(id_val).replace('.0', '').strip()
```

---

## Workflow Overview

### Step 0: Preparation

**0.1 Establish Mission:**
- Identify business-critical flows (money, compliance, customer impact)
- Define acceptance thresholds (allowable mismatch %, max missing refs)

**0.2 Build Focus Catalog (>= 20 items):**
> Load `references/focus_catalog.md` for the full category list

Key buckets: Keys/IDs, Relationships, Normalization, Status/Stage, Ownership, Dates, Money, Volume/Dedup, Automation, Integrations, Reporting, Archiving

**0.3 Run Initial Data Profiling:**
```bash
python scripts/exploratory_profiler.py <data_file.xlsx>
```

---

### Step 1: Random Focus Cycle (x10)

Pick **one** focus item randomly. For each:

1. **Focus**: One catalog item
2. **Diverge**: Generate 6-12 failure mode hypotheses using **4 perspectives**
   > Load `references/hypothesis_generation_guide.md` for perspective prompts
3. **Prioritize**: Score hypotheses using priority formula
4. **Converge**: Select top 2-3 plausible/high-impact risks
5. **Verify**: Define minimal experiments (queries, diffs, samples)
6. **Deepen**: Root cause -> remediation -> prevention
7. **Generalize**: Apply pattern to >= 2 other objects/flows

**Output per cycle:** Use template from `assets/exploration_log_template.md`

---

### 4-Perspective Hypothesis Generation

Generate hypotheses from **4 distinct perspectives** to ensure diversity:

| Icon | Perspective | Focus Area | Example Question |
|:----:|-------------|------------|------------------|
| 🏢 | Domain Expert | Business rules, compliance | "What rule violations could occur?" |
| 💻 | Tech Implementer | Code bugs, transforms | "Where could the mapping fail?" |
| 🔍 | Edge Case Hunter | Boundaries, special cases | "What happens at extremes?" |
| 📊 | Statistical Skeptic | Distributions, outliers | "Is this concentration normal?" |

**Minimum**: 2 hypotheses per perspective = 8 total per cycle

---

### Priority Scoring

**Formula**: `Priority = Impact × Probability × Testability`

| Score | Impact | Probability | Testability |
|:-----:|--------|-------------|-------------|
| 3 | All records affected | High (>50% likely) | Simple query |
| 2 | Category affected | Medium (10-50%) | Complex conditions |
| 1 | Rare cases | Low (<10%) | Manual verification |

**Thresholds**:
- 18-27: Test immediately
- 8-17: Standard priority
- 1-7: Test if time permits

---

### Step 2: Cross-Pollination Cycle (x10)

Pick **two lenses** and fuse them into new hypotheses.

> Load `references/lens_library.md` for available lenses

1. **Lens A + Lens B** -> new hypothesis
2. **Apply** to specific object/relationship/integration
3. **Verify** with targeted checks
4. **Converge** into Go/No-Go or follow-up
5. **Generalize** into reusable test or monitoring rule

**Combination Operators**:
| Operator | Meaning | Use Case |
|:--------:|---------|----------|
| AND | Both perspectives must align | Cross-source reference integrity |
| XOR | Perspectives should differ | Inconsistency detection |
| SEQ | One precedes the other | Lifecycle state validation |
| REQ | Dependency relationship | Cascading reference checks |

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

## Automation Scripts

### Data Profiling
```bash
python scripts/exploratory_profiler.py <file.xlsx>
```
Generates comprehensive profile: null rates, distributions, potential issues.

### Hypothesis Testing
```python
from scripts.hypothesis_tester import *

# Reference integrity test
result = test_reference_integrity(
    detail_df, master_df,
    ref_col='AccountId',
    master_id_col='Id'
)

# Value concentration test
result = test_value_concentration(df, 'OwnerId', threshold=0.5)

# Generate report
report = generate_test_report(results)
```

### Perspective Combination
```bash
python scripts/perspective_combiner.py
```
Displays lens catalog and generates random perspective combinations.

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
7. **ID format consistency** (int vs float `.0` suffix)
8. **Owner concentration** (single owner >50%)

---

## Resources

| Resource | Purpose | When to Load |
|----------|---------|--------------|
| `references/focus_catalog.md` | Full focus category list | Step 0.2 |
| `references/divergence_library.md` | Failure mode patterns | Step 1 (Diverge) |
| `references/lens_library.md` | Cross-pollination lenses | Step 2 |
| `references/hypothesis_generation_guide.md` | 4-perspective prompts | Step 1 (Diverge) |
| `references/seed_examples.md` | Worked examples | When stuck |
| `assets/exploration_log_template.md` | Per-cycle output | Step 1, 2 |
| `assets/qa_backlog_template.md` | Final backlog + gates | Step 3 |
| `assets/hypothesis_worksheet.md` | Hypothesis tracking | Step 1 |
| `scripts/exploratory_profiler.py` | Data profiling | Step 0.3 |
| `scripts/hypothesis_tester.py` | Automated testing | Step 1 (Verify) |
| `scripts/perspective_combiner.py` | Lens generation | Step 2 |

---

## Output Summary

**Per-cycle output:**
```
Cycle #: [n]
Focus: [item]

DIVERGE (4 perspectives):
🏢 Domain: [2+ hypotheses]
💻 Tech: [2+ hypotheses]
🔍 Edge: [2+ hypotheses]
📊 Stats: [2+ hypotheses]

PRIORITIZE:
[Top 3 by priority score]

VERIFY:
[Checks executed, results]

CONVERGE:
Result: Pass/Fail/Unknown
Root Cause: [if issue found]
Actions: [remediation + generalization]
```

**Final deliverables:**
- Prioritized QA backlog table
- Quality gates checklist
- Open questions/assumptions
- Automated test scripts (reusable)
