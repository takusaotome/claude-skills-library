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

1. **Validate Input Format**: Verify CSV structure and required columns are present
2. **Classify Accounts**: Confirm account type assignments (revenue vs. cost/expense)
3. **Period Alignment**: Ensure budget and actual figures correspond to the same period
4. **Data Cleansing**: Handle missing values, zero budgets, and currency formatting

---

## 5. Usage Examples

- **Monthly/Quarterly Budget Review** - Compare actual results against budget to identify significant deviations
- 「今月の予実差異を分析して」「月次の予算対比レポートを作成して」
- **Management Meeting Preparation** - Create executive-level variance summaries with root cause analysis
- 「経営会議向けに予実サマリを作って」「取締役会用の業績報告資料を準備して」
- **Cost Overrun Investigation** - Identify which line items are over budget and why
- 「コスト超過の原因を特定して」「予算オーバーしている勘定科目を洗い出して」

---

## 6. Understanding the Output

The analysis produces a structured variance report containing:

1. **Executive Summary**: Total favorable/unfavorable variance, key highlights
2. **Variance Detail Table**: Per-account breakdown with amounts, percentages, and direction
3. **Materiality Ranking**: Top variances sorted by absolute impact
4. **Root Cause Analysis**: Hypotheses and supporting evidence for major variances
5. **Recommended Actions**: Prioritized list of corrective/follow-up actions

Output template: `assets/variance_report_template_ja.md` (Japanese) or `assets/variance_report_template_en.md` (English)

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/ma-budget-actual-variance/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: 第05回_その予算って根拠あるの_20250507.md, 第08回_予算実績差異分析_20250820.md.
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

- `skills/ma-budget-actual-variance/references/第05回_その予算って根拠あるの_20250507.md`
- `skills/ma-budget-actual-variance/references/第08回_予算実績差異分析_20250820.md`
