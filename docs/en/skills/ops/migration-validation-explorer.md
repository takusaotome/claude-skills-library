---
layout: default
title: "Migration Validation Explorer"
grand_parent: English
parent: Operations & Docs
nav_order: 9
lang_peer: /ja/skills/ops/migration-validation-explorer/
permalink: /en/skills/ops/migration-validation-explorer/
---

# Migration Validation Explorer
{: .no_toc }

Exploratory data-migration validation and QA ideation workflow. Use when you need to discover hidden risks, generate new validation angles, and converge mapping specs/validation reports into a prioritized QA backlog for CRM migrations. Version 2.0, updated 2025-12-28.

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/migration-validation-explorer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/migration-validation-explorer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

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

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
python scripts/exploratory_profiler.py <data_file.xlsx>
```

---

## 4. How It Works

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/migration-validation-explorer/references/divergence_library.md`
- `skills/migration-validation-explorer/references/focus_catalog.md`
- `skills/migration-validation-explorer/references/hypothesis_generation_guide.md`
- `skills/migration-validation-explorer/references/lens_library.md`
- `skills/migration-validation-explorer/references/seed_examples.md`

**Scripts:**

- `skills/migration-validation-explorer/scripts/exploratory_profiler.py`
- `skills/migration-validation-explorer/scripts/hypothesis_tester.py`
- `skills/migration-validation-explorer/scripts/perspective_combiner.py`
