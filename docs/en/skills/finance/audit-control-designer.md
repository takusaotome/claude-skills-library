---
layout: default
title: "Audit Control Designer"
grand_parent: English
parent: Finance & Analysis
nav_order: 2
lang_peer: /ja/skills/finance/audit-control-designer/
permalink: /en/skills/finance/audit-control-designer/
---

# Audit Control Designer
{: .no_toc }

Generate audit-ready internal control design documents from As-Is business process inventories. Produces control IDs, assertion mappings, procedures, SoD analysis, KPIs, materiality thresholds, and implementation roadmaps. Use when building internal controls for new audit engagements, SOX/J-SOX compliance, or process improvement initiatives.

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/audit-control-designer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/audit-control-designer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill transforms As-Is business process inventories into comprehensive internal control design documents. It leverages generalized patterns from real audit engagements across industries (F&B, retail, manufacturing) to produce draft control designs that cover all five audit assertions, segregation of duties, KPIs, and implementation roadmaps.

---

## 2. Prerequisites

None. This is a knowledge-based skill that uses reference documents for pattern matching and generation.

---

## 3. Quick Start

### Step 1: Confirm Context Variables

Ask the user to confirm or specify:
- Applicable accounting standard
- Industry and company scale
- Current system environment
- Regulatory requirements

---

## 4. How It Works

### Step 1: Confirm Context Variables

Ask the user to confirm or specify:
- Applicable accounting standard
- Industry and company scale
- Current system environment
- Regulatory requirements

If not specified, use defaults from the table above.

### Step 2: Read As-Is Process Inventory

Read the user-provided process inventory. Identify:
- Total number of processes
- Business domains covered
- Frequency distribution (daily/weekly/monthly)
- Manual risk indicators

### Step 3: Classify Processes into Business Patterns

Load `references/process_patterns.md` and classify each process into one or more patterns:

| Pattern | Domain | Key Processes |
|---|---|---|

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Starting internal control design from an As-Is process inventory
- Building controls for a new audit engagement (SOX, J-SOX, PCAOB)
- Designing controls for a specific business domain (AP, Inventory, COGS, Returns)
- Reviewing and strengthening existing control frameworks
- Preparing for initial audit readiness assessment

---

## 6. Understanding the Output

The output follows the template in `assets/control_design_template.md`. Key sections:

- Control IDs follow the pattern: `C-[DOMAIN]-[NN]` (e.g., C-AP-01, C-INV-01)
- Each control specifies: Type (Preventive/Detective), Assertion coverage, Procedure steps
- SoD pairs are rated High/Medium/Low risk
- KPIs include calculation formula and data source
- Roadmap uses M+N notation (months from project start)
- Open Questions are explicitly managed with options and recommendations

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/audit-control-designer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: control_templates.md, materiality_framework.md, assertion_mapping.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/finance/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.

---

## 10. Reference

**References:**

- `skills/audit-control-designer/references/accounting_standards.md`
- `skills/audit-control-designer/references/assertion_mapping.md`
- `skills/audit-control-designer/references/control_templates.md`
- `skills/audit-control-designer/references/kpi_catalog.md`
- `skills/audit-control-designer/references/materiality_framework.md`
- `skills/audit-control-designer/references/process_patterns.md`
- `skills/audit-control-designer/references/sod_patterns.md`
