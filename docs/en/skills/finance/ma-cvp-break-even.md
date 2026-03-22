---
layout: default
title: "MA CVP Break Even"
grand_parent: English
parent: Finance & Analysis
nav_order: 12
lang_peer: /ja/skills/finance/ma-cvp-break-even/
permalink: /en/skills/finance/ma-cvp-break-even/
---

# MA CVP Break Even
{: .no_toc }

CVP（Cost-Volume-Profit）分析・損益分岐点分析スキル。固定費・変動費の構造分析、
限界利益率の算出、損益分岐点売上高/数量の計算、安全余裕率の評価、
目標利益達成に必要な売上高のシミュレーションを行う。多品目分析にも対応。

Use when: 損益分岐点を知りたいとき、新規事業や価格変更の採算シミュレーション、
固定費削減・変動費率改善の効果試算、What-if分析に使用。

Triggers: "損益分岐点", "CVP", "break-even", "限界利益", "contribution margin",
"安全余裕率", "margin of safety", "固変分解", "変動費率"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ma-cvp-break-even.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ma-cvp-break-even){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Cost-Volume-Profit analysis determines the relationship between costs, volume, and profit to find the break-even point and plan for target profits. Supports single-product and multi-product scenarios with what-if simulation capabilities.

---

## 2. Prerequisites

Before running this skill, ensure the following data is available:

- **Revenue Data**: Selling price per unit and/or total sales amount
- **Variable Cost Data**: Variable cost per unit or total variable costs
- **Fixed Cost Data**: Total fixed costs for the analysis period
- **Volume Data**: Current or projected sales volume (units)
- **For Multi-Product**: Sales mix ratios for each product

### Input Data Format

**Single Product:**
| Parameter | Example |
|-----------|---------|
| Selling Price per Unit | $500 |
| Variable Cost per Unit | $300 |
| Total Fixed Costs | $1,000,000 |
| Current Sales Volume | 8,000 units |

**Multi-Product (CSV):**
```csv
product_name,selling_price,variable_cost,sales_mix_ratio
Product A,500,300,0.60
Product B,800,500,0.30
Product C,200,120,0.10
```

---

## 3. Quick Start

1. **Identify Cost Behavior**: Classify all costs as fixed or variable
2. **Calculate Unit Contribution Margin**: `Unit CM = Selling Price - Variable Cost per Unit`
3. **Calculate CM Ratio**: `CM Ratio = Unit CM / Selling Price`
4. **Assess Cost Structure**: Determine operating leverage (fixed cost proportion)
5. **For Multi-Product**: Calculate weighted average CM ratio using sales mix

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

- `skills/ma-cvp-break-even/references/第09回_損益分岐点って要は元を取るライン_20251005.md`
- `skills/ma-cvp-break-even/references/第10回_差額原価収益分析_20251104.md`
