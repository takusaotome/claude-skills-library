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

Analyzes the differences between standard (planned) and actual costs, decomposing variances into price and quantity components. Identifies responsible departments and provides root cause hypotheses for manufacturing cost management.

## When to Use This Skill

Use this skill in the following scenarios:

1. **Monthly Cost Variance Reporting** - Analyze standard vs. actual cost differences for manufacturing operations
   - 「今月の原価差異を分析して」「標準原価との乖離を計算して」
2. **Cost Reduction Effectiveness Measurement** - Evaluate whether cost reduction initiatives achieved target
   - 「原価低減活動の効果を測定して」「コスト削減の進捗を確認して」
3. **Procurement Price Monitoring** - Track material price variances against standards
   - 「材料の価格差異を確認して」「仕入価格の変動を分析して」
4. **Production Efficiency Analysis** - Identify quantity/efficiency variances in manufacturing
   - 「製造効率の差異を分析して」「数量差異の原因を特定して」
5. **Responsibility Accounting** - Assign variance responsibility to appropriate departments
   - 「差異の責任部門を特定して」「部門別の原価管理レポートを作って」

## Prerequisites

Before running this skill, ensure the following data is available:

- **Standard Cost Data**: Standard price and standard quantity per item
- **Actual Cost Data**: Actual price and actual quantity per item
- **Cost Category Classification**: Each item classified as `material`, `labor`, or `overhead`
- **Period Information**: Target analysis period

### Required CSV Format

```csv
item_name,cost_category,standard_price,actual_price,standard_quantity,actual_quantity
Eggs,material,2.50,3.20,100,105
Line Worker,labor,25.00,26.50,40,42
Equipment Depreciation,overhead,5000,5000,1,1
```

**Required Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `item_name` | string | Cost item name |
| `cost_category` | string | `material`, `labor`, or `overhead` |
| `standard_price` | numeric | Standard (planned) unit price |
| `actual_price` | numeric | Actual unit price |
| `standard_quantity` | numeric | Standard quantity for actual output |
| `actual_quantity` | numeric | Actual quantity consumed |

### Cost Categories

- **material**: Raw materials and components (e.g., flour, eggs, packaging)
- **labor**: Direct labor (e.g., line workers, supervisors)
- **overhead**: Manufacturing overhead (e.g., depreciation, utilities, maintenance)

## Workflow 1: Data Preparation

1. **Validate Input Format**: Verify CSV structure and required columns
2. **Classify Cost Items**: Confirm cost category assignments (material/labor/overhead)
3. **Verify Standard Costs**: Ensure standard costs reflect current approved standards
4. **Handle Edge Cases**: Address zero quantities, missing prices, and new items without standards

## Workflow 2: Variance Decomposition

1. **Calculate Price Variance** per item:
   - Formula: `(Actual Price - Standard Price) x Actual Quantity`
   - Responsibility: Purchasing / Procurement department

2. **Calculate Quantity Variance** per item:
   - Formula: `(Actual Quantity - Standard Quantity) x Standard Price`
   - Responsibility: Production / Manufacturing department

3. **Calculate Total Variance** per item:
   - Formula: `Price Variance + Quantity Variance`
   - Verification: Must equal `(Actual Price x Actual Quantity) - (Standard Price x Standard Quantity)`

4. **Determine Direction**:

| Total Variance | Direction | Meaning |
|---------------|-----------|---------|
| Positive (+) | Unfavorable | Actual cost exceeds standard |
| Negative (-) | Favorable | Actual cost below standard |
| Zero | On Standard | Actual matches standard |

5. **Aggregate by Category**: Compute subtotals for material, labor, and overhead

## Workflow 3: Root Cause Analysis & Responsibility Mapping

1. **Responsibility Assignment**:
   - Price variances → Purchasing/Procurement
   - Quantity variances → Production/Manufacturing
   - Overhead volume variances → Management/Planning

2. **Root Cause Hypotheses** for each material variance:
   - **Price (Unfavorable)**: Market price increase, supplier change, rush order premium, quality upgrade
   - **Price (Favorable)**: Bulk discount, new supplier negotiation, lower-grade substitution
   - **Quantity (Unfavorable)**: Waste/scrap increase, rework, equipment malfunction, skill gap
   - **Quantity (Favorable)**: Process improvement, better equipment, skill enhancement

3. **Cross-Category Analysis**: Identify interactions (e.g., cheaper material causing more waste)

4. **Trend Comparison**: Compare to prior periods for systematic patterns

5. **Action Recommendations**: Prioritized corrective actions with responsible departments

## Output

The analysis produces a structured cost variance report containing:

1. **Executive Summary**: Total variance by category, key highlights
2. **Item-Level Detail**: Price variance, quantity variance, and total per item with calculation basis
3. **Category Subtotals**: Aggregated variances by material/labor/overhead
4. **Responsibility Matrix**: Variance amounts mapped to responsible departments
5. **Root Cause Analysis**: Hypotheses and recommended actions for major variances

Output template: `assets/cost_variance_report_template_ja.md` (Japanese) or `assets/cost_variance_report_template_en.md` (English)

## Resources

### References (load into context for guidance)

- `references/第12回_予定原価という考え方_20260122.md` - Standard cost (planned cost) concepts, bakery business case study with price/quantity variance decomposition
- `references/第11回_ABCで見える店舗別損益管理の真実_20251213.md` - Activity-Based Costing methodology for store-level cost allocation and profitability analysis

### Assets (templates for output generation)

- `assets/cost_variance_report_template_ja.md` - Japanese cost variance analysis report template
- `assets/cost_variance_report_template_en.md` - English cost variance analysis report template

## Best Practices

- Always decompose total variance into price and quantity components - the total alone is insufficient
- Verify that `Price Variance + Quantity Variance = Total Variance` as a calculation check
- Consider interdependencies between price and quantity (e.g., cheaper material may increase waste)
- Update standards periodically - outdated standards produce misleading variances
- Focus on controllable variances - market-driven price changes may not be actionable at the department level
- For overhead variances, consider separating into spending, efficiency, and volume components

## Examples

### Example: Bakery Manufacturing Cost Variance

**Input Data:**
```csv
item_name,cost_category,standard_price,actual_price,standard_quantity,actual_quantity
Flour (kg),material,200,220,500,520
Eggs (unit),material,30,28,1000,1050
Baker Hourly,labor,1500,1500,160,175
Oven Electricity,overhead,50,55,200,200
```

**Analysis Output (Flour):**
- Price Variance: (220 - 200) x 520 = +10,400 (Unfavorable) → Purchasing
- Quantity Variance: (520 - 500) x 200 = +4,000 (Unfavorable) → Production
- Total Variance: +14,400 (Unfavorable)
- Root Cause: Wheat price increase (price) + recipe adjustment for new product (quantity)

**Category Summary:**
| Category | Price Variance | Quantity Variance | Total |
|----------|---------------|-------------------|-------|
| Material | +8,300 (U) | +5,500 (U) | +13,800 (U) |
| Labor | 0 | +22,500 (U) | +22,500 (U) |
| Overhead | +1,000 (U) | 0 | +1,000 (U) |
| **Total** | **+9,300 (U)** | **+28,000 (U)** | **+37,300 (U)** |
