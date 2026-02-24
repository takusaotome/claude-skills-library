---
name: ma-standard-cost-variance
description: |
  標準原価差異分析スキル。標準原価（予定原価）と実際原価の差異を価格差異・数量差異に分解し、
  材料費・労務費・製造間接費のカテゴリ別に集計・分析する。差異の有利/不利判定、
  責任部門の特定、根本原因の仮説提示を行う。CSVデータのアップロードによる自動分析に対応。

  Use when: 製造原価の差異分析を行いたいとき。標準原価計算制度の運用、
  月次原価差異レポート作成、原価低減活動の効果測定に使用。

  Triggers: "標準原価", "原価差異", "価格差異", "数量差異", "standard cost",
  "cost variance", "price variance", "quantity variance", "予定原価",
  "操業度差異", "原価管理"
---

# Standard Cost Variance Analysis

## Overview

Analyzes the differences between standard (planned) and actual costs, decomposing variances into price and quantity components to identify root causes.

## Key Concepts

### Variance Decomposition

| Variance Type | Formula | Responsibility |
|--------------|---------|----------------|
| Price Variance | (Actual Price - Standard Price) x Actual Quantity | Purchasing / Procurement |
| Quantity Variance | (Actual Quantity - Standard Quantity) x Standard Price | Production / Manufacturing |
| Total Variance | Price Variance + Quantity Variance | Management |

### Direction Logic

| Total Variance | Direction | Meaning |
|---------------|-----------|---------|
| Positive (+) | Unfavorable | Actual cost exceeds standard |
| Negative (-) | Favorable | Actual cost below standard |
| Zero | On Standard | Actual matches standard |

### Analysis Steps

1. **Data Validation**: Verify CSV format with required columns
2. **Item-Level Variance**: Compute price and quantity variance per item
3. **Category Subtotals**: Aggregate by cost category (material/labor/overhead)
4. **Direction Assessment**: Determine favorable/unfavorable for each item
5. **Root Cause Hypotheses**: Suggest explanations for major variances

### Required CSV Format

```csv
item_name,cost_category,standard_price,actual_price,standard_quantity,actual_quantity
Eggs,material,2.50,3.20,100,105
Line Worker,labor,25.00,26.50,40,42
Equipment Depreciation,overhead,5000,5000,1,1
```

### Cost Categories

- **material**: Raw materials and components
- **labor**: Direct labor (line workers, supervisors)
- **overhead**: Manufacturing overhead (depreciation, utilities)

### Output Format

For each item:
- Item name and cost category
- Standard vs. actual price and quantity
- Price variance (with calculation basis)
- Quantity variance (with calculation basis)
- Total variance and direction

Category subtotals:
- Aggregated price variance by category
- Aggregated quantity variance by category
- Aggregated total variance by category

## Interpretation Guidelines

- Price variances suggest procurement or market issues
- Quantity variances suggest production efficiency issues
- Overhead variances may indicate capacity utilization changes
- Consider both absolute amount and percentage impact
- Look for systematic patterns across categories
