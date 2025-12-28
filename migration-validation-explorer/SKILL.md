---
name: migration-validation-explorer
description: Exploratory data-migration validation and QA ideation workflow for CRM migrations. Use when you need to discover hidden data quality risks, generate new validation angles, or turn mapping specs and validation reports into a prioritized QA backlog. Triggers include requests like "validate migration data", "find data quality issues", "create QA checklist for migration", "explore validation gaps", or when working with migration datasets that may have undiscovered risks.
---

# Migration Validation Explorer

Run structured exploratory validation cycles on migration datasets to surface latent issues and converge them into a QA-ready checklist.

## Inputs

Locate these files before starting:
- Mapping spec: `docs/data_mapping_specification*.md`
- Validation plan: `docs/migration_data_validation_plan.md`
- Validation report: `outputs/*/data_validation_report.md`
- Dataset: `outputs/migration_dataset_*`

Use `rg --files -g '*validation*'` or `rg --files -g '*mapping*spec*'` if paths vary.

## Workflow

### Step 1: Build Focus Catalog

Create 20+ candidate focus areas from specs/reports:

| Category | Examples |
|----------|----------|
| Keys/IDs | external IDs, uniqueness, formatting, nullability |
| Relationships | Account-Contact, Opportunity-Property, Invoice-LineItems |
| Normalization | address, unit number, city/state inference |
| Status/Stage | picklists, mapping tables, default fallbacks |
| Ownership | OwnerId mapping, license constraints, fallback rates |
| Dates | placeholders, timezone/format, lifecycle consistency |
| Money | currency parsing, zero vs null, rollups vs raw |
| Volume/dedup | record counts, duplicates, merge strategy |
| Edge cases | renewals, cancellations, "not applicable" flags |

### Step 2: Exploratory Cycle (x10)

For each cycle, pick one focus item randomly:

1. **Focus**: One item from catalog
2. **Diverge**: List 6-10 possible failure modes
3. **Converge**: Select top 2-3 plausible risks
4. **Verify**: Define concrete checks (queries, file diffs, thresholds)
5. **Deepen**: If verified, identify root causes + remediation

### Step 3: Cross-Pollination Cycle (x10)

Fuse two lenses into new validation angles:

**Lens Library:**
- CRM migration: external IDs, picklist drift, lookup cardinality, ownership licensing
- Real-estate domain: lease lifecycle, unit/address ambiguity, broker roles, property hierarchy
- Data pipeline: join key reuse, normalization side effects, schema drift
- QA: sampling bias, over-reliance on SF constraints, silent fallback logic

Template:
1. **Lens A + Lens B** -> new validation hypothesis
2. **Apply** to specific object/relationship
3. **Verify** with targeted checks
4. **Converge** into go/no-go or follow-up

### Step 4: Converge Into QA Backlog

Create backlog table:

| Check | Scope | Risk | Evidence | Method | Pass Criteria | Owner |
|-------|-------|------|----------|--------|---------------|-------|
| ... | ... | H/M/L | ... | ... | ... | ... |

### Step 5: Report

Output:
- **Exec summary**: Top 3 risks + decision asks
- **Technical summary**: All checks + status
- **Appendix**: Queries/paths

## Output Format

Per cycle:
```
Focus: [item]
Divergent: [hypotheses]
Converged: [risks]
Checks: [verification methods]
Actions: [next steps]
```

Final convergence:
- Prioritized risks (High/Medium/Low)
- QA backlog table
- Open questions/assumptions
