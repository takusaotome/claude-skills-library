---
layout: default
title: "Supply Chain Consultant"
grand_parent: English
parent: Project & Business
nav_order: 22
lang_peer: /ja/skills/management/supply-chain-consultant/
permalink: /en/skills/management/supply-chain-consultant/
---

# Supply Chain Consultant
{: .no_toc }

サプライチェーン最適化コンサルティングスキル。需要予測、在庫最適化、調達戦略、
物流ネットワーク設計、S&OP(Sales and Operations Planning)を支援。
Use when optimizing supply chain operations, improving inventory management, designing logistics networks,
or conducting supply chain risk assessments.
Triggers: "supply chain", "在庫最適化", "inventory optimization", "demand forecasting", "S&OP", "procurement strategy", "logistics network".

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/supply-chain-consultant.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/supply-chain-consultant){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Professional supply chain management consulting: demand forecasting, inventory optimization, procurement strategy, logistics network design, and S&OP.

**Primary language**: Japanese (default), English supported
**Frameworks**: SCOR (Supply Chain Operations Reference), S&OP best practices, Lean Supply Chain, Theory of Constraints
**Output format**: Supply chain analysis reports, optimization recommendations, S&OP plans, network design proposals

Use this skill when:
- Optimizing inventory levels and reducing carrying costs
- Improving demand forecasting accuracy
- Designing or redesigning logistics networks
- Developing procurement strategies
- Implementing or improving S&OP processes
- Conducting supply chain risk assessments
- Reducing supply chain costs while maintaining service levels

---

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

### Workflow 1: Demand Forecasting Optimization

**Purpose**: Improve demand forecast accuracy to reduce stockouts and excess inventory.

---

## 4. How It Works

### Workflow 1: Demand Forecasting Optimization

**Purpose**: Improve demand forecast accuracy to reduce stockouts and excess inventory.

**Decision Procedure**:
1. Assess current forecasting method, horizon, frequency, and ownership
2. Measure forecast accuracy (MAPE, Bias, Tracking Signal)
3. Segment products via ABC-XYZ analysis to determine forecasting approach per segment
4. Select forecasting technique:
   - **AX/BX**: Statistical methods (Moving Average, Exponential Smoothing)
   - **AY/BY**: Statistical + collaborative (Holt-Winters, consensus)
   - **AZ/BZ**: Demand sensing, safety stock buffers
   - **CX/CY/CZ**: Simple rules, Min-Max, or make-to-order
5. Design S&OP-integrated forecasting process
6. Monitor forecast KPIs and adjust

> **Detail**: Load `references/demand_forecasting_guide.md` for formulas, segmentation matrix, KPI dashboard template.
> **Script**: Run `scripts/generate_demand_kpi_dashboard.py` to generate a KPI dashboard from data.

---

## 5. Usage Examples

- Use **Supply Chain Consultant** when you need a structured workflow rather than an ad-hoc answer.
- Start with a small representative input before applying the workflow to production data or assets.
- Review the helper scripts and reference guides to tailor the output format to your project.

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 6 guide file(s).
- Script-assisted execution using 3 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/supply-chain-consultant/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: kpi_reference.md, sop_planning_guide.md, procurement_strategy_guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: generate_demand_kpi_dashboard.py, generate_sop_agenda.py, generate_inventory_policy.py.
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
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/supply-chain-consultant/references/demand_forecasting_guide.md`
- `skills/supply-chain-consultant/references/inventory_optimization_guide.md`
- `skills/supply-chain-consultant/references/kpi_reference.md`
- `skills/supply-chain-consultant/references/logistics_network_guide.md`
- `skills/supply-chain-consultant/references/procurement_strategy_guide.md`
- `skills/supply-chain-consultant/references/sop_planning_guide.md`

**Scripts:**

- `skills/supply-chain-consultant/scripts/generate_demand_kpi_dashboard.py`
- `skills/supply-chain-consultant/scripts/generate_inventory_policy.py`
- `skills/supply-chain-consultant/scripts/generate_sop_agenda.py`
