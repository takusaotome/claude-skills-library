---
layout: default
title: "KPI Designer"
grand_parent: English
parent: Project & Business
nav_order: 15
lang_peer: /ja/skills/management/kpi-designer/
permalink: /en/skills/management/kpi-designer/
---

# KPI Designer
{: .no_toc }

KPI体系設計とOKR策定支援スキル。ビジネス目標に整合したKPI設計、バランススコアカード、OKRフレームワーク、
ダッシュボード設計を提供。SMART原則、リーディング/ラギング指標の選定を支援。
Use when designing KPI frameworks, implementing OKR methodology, or creating performance measurement systems.
Triggers: "KPI design", "OKR", "performance metrics", "balanced scorecard", "dashboard design", "measurement framework".

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/kpi-designer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/kpi-designer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides expert guidance for designing comprehensive KPI frameworks and implementing OKR (Objectives and Key Results) methodologies. Aligns metrics with strategic objectives and creates actionable measurement systems.

**Primary language**: Japanese (default), English supported
**Frameworks**: Balanced Scorecard, OKR, KPI Pyramid, SMART criteria
**Output format**: KPI frameworks, OKR sheets, dashboard designs, metric definitions

---

## 2. Prerequisites

- Strategic objectives or business goals defined (or provided by user)
- Stakeholder context (industry, department, organizational level)
- Access to current metrics/data sources (optional, for baseline)

---

## 3. Quick Start

```bash
1. Gather Requirements  ──→  2. Design Framework  ──→  3. Define KPIs
       │                            │                        │
       ▼                            ▼                        ▼
   - Objectives               - Select framework        - SMART validation
   - Industry context         - BSC / OKR / Pyramid     - Leading/Lagging mix
   - Stakeholder level        - Hierarchy design        - Owner assignment

4. Generate Deliverables  ──→  5. Review & Refine
       │                              │
       ▼                              ▼
   - KPI Framework Doc            - Stakeholder feedback
   - OKR Template                 - Alignment check
   - Dashboard Spec               - Data feasibility
```

---

## 4. How It Works

```
1. Gather Requirements  ──→  2. Design Framework  ──→  3. Define KPIs
       │                            │                        │
       ▼                            ▼                        ▼
   - Objectives               - Select framework        - SMART validation
   - Industry context         - BSC / OKR / Pyramid     - Leading/Lagging mix
   - Stakeholder level        - Hierarchy design        - Owner assignment

4. Generate Deliverables  ──→  5. Review & Refine
       │                              │
       ▼                              ▼
   - KPI Framework Doc            - Stakeholder feedback
   - OKR Template                 - Alignment check
   - Dashboard Spec               - Data feasibility
```

### Quick Start Example

```bash
# Generate a KPI framework document
python3 scripts/generate_kpi_framework.py \
  --objectives "Increase revenue 20%, Improve customer satisfaction, Reduce churn" \
  --industry "SaaS" \
  --level "Company" \

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Designing KPI frameworks for organizations or departments
- Implementing OKR methodology
- Creating balanced scorecards
- Designing performance dashboards
- Aligning metrics with strategy
- Improving data-driven decision making

---

## 6. Understanding the Output

| Deliverable | Format | Description |
|-------------|--------|-------------|
| KPI Framework Document | Markdown | Hierarchical KPI structure with definitions |
| OKR Template | Markdown | Quarterly OKR sheet with check-in format |
| Dashboard Design Spec | Markdown | Layout, chart types, drill-down design |
| KPI Validation Report | Markdown | SMART criteria assessment per KPI |

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/kpi-designer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: industry-kpis.md, kpi-methodology.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: generate_kpi_framework.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/management/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/kpi-designer/references/industry-kpis.md`
- `skills/kpi-designer/references/kpi-methodology.md`

**Scripts:**

- `skills/kpi-designer/scripts/generate_kpi_framework.py`
