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

## 5. Usage Examples

- Mapping spec, validation plan, and validation report exist
- You suspect **undiscovered issues** (coverage gaps, silent failures, edge cases)
- Need to generate new validation angles beyond standard checklists
- Want automated data profiling and hypothesis testing

---

## 6. Understanding the Output

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

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/migration-validation-explorer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: hypothesis_generation_guide.md, lens_library.md, divergence_library.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: perspective_combiner.py, hypothesis_tester.py, exploratory_profiler.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/ops/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

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
