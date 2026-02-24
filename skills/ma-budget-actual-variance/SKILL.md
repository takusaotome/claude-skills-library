---
name: ma-budget-actual-variance
description: |
  予算実績差異分析スキル。勘定科目タイプ（収益/費用）に応じた有利・不利差異の自動判定、
  差異の分解（価格差異・数量差異）、重要度ランキング、根本原因の仮説提示を行う。
  CSVデータのアップロードによる自動分析に対応。

  Use when: 予算と実績の比較分析を行いたいとき。月次・四半期の予実管理レポート作成、
  差異の原因分析、経営会議向けの予実サマリ作成に使用。

  Triggers: "予実差異", "予算実績", "budget variance", "budget vs actual",
  "予算対比", "差異分析", "variance analysis"
---

# Budget-Actual Variance Analysis

## Overview

Analyzes the differences between budgeted and actual figures, identifying favorable and unfavorable variances with account-type awareness.

## Key Concepts

### Variance Direction by Account Type

| Account Type | Actual > Budget | Actual < Budget |
|-------------|----------------|----------------|
| Revenue | Favorable (+) | Unfavorable (-) |
| Cost/Expense | Unfavorable (+) | Favorable (-) |

### Analysis Steps

1. **Data Validation**: Verify CSV format and required columns
2. **Variance Calculation**: For each line item, compute absolute and percentage variance
3. **Direction Assessment**: Determine favorable/unfavorable based on account type
4. **Materiality Ranking**: Sort by absolute variance to highlight significant items
5. **Root Cause Hypotheses**: Suggest possible explanations for major variances

### Required CSV Format

```csv
account_name,account_type,budget,actual
Sales Revenue,revenue,1000000,1200000
Material Cost,cost,400000,380000
```

### Output Format

For each account:
- Account name and type
- Budget vs. actual amounts
- Variance (absolute and percentage)
- Direction (favorable/unfavorable)
- Calculation basis (formula with actual numbers)

## Interpretation Guidelines

- Variances > 10% warrant investigation
- Revenue shortfalls are typically more critical than cost overruns
- Consider both absolute amount and percentage
- Look for offsetting variances (e.g., higher sales + higher variable costs)
