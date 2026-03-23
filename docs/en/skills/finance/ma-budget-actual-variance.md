---
layout: default
title: "MA Budget Actual Variance"
grand_parent: English
parent: Finance & Analysis
nav_order: 11
lang_peer: /ja/skills/finance/ma-budget-actual-variance/
permalink: /en/skills/finance/ma-budget-actual-variance/
---

# MA Budget Actual Variance
{: .no_toc }

予算実績差異分析スキル。勘定科目タイプ（収益/費用）に応じた有利・不利差異の自動判定、
差異の分解（価格差異・数量差異）、重要度ランキング、根本原因の仮説提示を行う。
CSVデータのアップロードによる自動分析に対応。

Use when: 予算と実績の比較分析を行いたいとき。月次・四半期の予実管理レポート作成、
差異の原因分析、経営会議向けの予実サマリ作成に使用。

Triggers: "予実差異", "予算実績", "budget variance", "budget vs actual",
"予算対比", "差異分析", "variance analysis"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ma-budget-actual-variance.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ma-budget-actual-variance){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Analyzes the differences between budgeted and actual figures, identifying favorable and unfavorable variances with account-type awareness. Provides materiality ranking, root cause hypotheses, and actionable recommendations for management decision-making.

---

## 2. Prerequisites

Before running this skill, ensure the following data is available:

- **Budget Data**: Approved budget figures by account (CSV or manual input)
- **Actual Data**: Actual performance figures for the same period
- **Account Classification**: Each account must be classified as `revenue` or `cost`/`expense`
- **Period Information**: Target analysis period (month, quarter, or year)

### Required CSV Format

```csv
account_name,account_type,budget,actual
Sales Revenue,revenue,1000000,1200000
Material Cost,cost,400000,380000
Labor Cost,cost,300000,320000
```

**Required Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `account_name` | string | Account or line item name |
| `account_type` | string | `revenue` or `cost` (determines favorable/unfavorable logic) |
| `budget` | numeric | Budgeted amount |
| `actual` | numeric | Actual amount |

---

## 3. Quick Start

1. **Validate Input Format**: Verify CSV structure and required columns are present
2. **Classify Accounts**: Confirm account type assignments (revenue vs. cost/expense)
3. **Period Alignment**: Ensure budget and actual figures correspond to the same period
4. **Data Cleansing**: Handle missing values, zero budgets, and currency formatting

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

- `skills/ma-budget-actual-variance/references/第05回_その予算って根拠あるの_20250507.md`
- `skills/ma-budget-actual-variance/references/第08回_予算実績差異分析_20250820.md`
