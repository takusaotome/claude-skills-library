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

Analyzes the differences between budgeted and actual figures, identifying favorable and unfavorable variances with account-type awareness. Provides materiality ranking, root cause hypotheses, and actionable recommendations for management decision-making.

## When to Use This Skill

Use this skill in the following scenarios:

1. **Monthly/Quarterly Budget Review** - Compare actual results against budget to identify significant deviations
   - 「今月の予実差異を分析して」「月次の予算対比レポートを作成して」
2. **Management Meeting Preparation** - Create executive-level variance summaries with root cause analysis
   - 「経営会議向けに予実サマリを作って」「取締役会用の業績報告資料を準備して」
3. **Cost Overrun Investigation** - Identify which line items are over budget and why
   - 「コスト超過の原因を特定して」「予算オーバーしている勘定科目を洗い出して」
4. **Revenue Shortfall Analysis** - Determine revenue gaps and contributing factors
   - 「売上未達の原因を分析して」「予算未達の要因分解をして」
5. **Rolling Forecast Adjustment** - Use variance trends to update future projections
   - 「差異トレンドから今後の見通しを修正して」「ローリングフォーキャストを更新して」

## Prerequisites

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

## Workflow 1: Data Preparation

1. **Validate Input Format**: Verify CSV structure and required columns are present
2. **Classify Accounts**: Confirm account type assignments (revenue vs. cost/expense)
3. **Period Alignment**: Ensure budget and actual figures correspond to the same period
4. **Data Cleansing**: Handle missing values, zero budgets, and currency formatting

## Workflow 2: Variance Calculation

1. **Compute Absolute Variance**: `Variance = Actual - Budget` for each line item
2. **Compute Percentage Variance**: `Variance % = (Actual - Budget) / Budget * 100`
3. **Determine Direction**: Apply account-type-aware favorable/unfavorable logic:

| Account Type | Actual > Budget | Actual < Budget |
|-------------|----------------|----------------|
| Revenue | Favorable (+) | Unfavorable (-) |
| Cost/Expense | Unfavorable (+) | Favorable (-) |

4. **Materiality Ranking**: Sort by absolute variance amount to highlight significant items
5. **Threshold Flagging**: Flag items exceeding materiality threshold (default: 10% or top 5 items)

## Workflow 3: Root Cause Analysis

1. **Pattern Identification**: Look for correlated variances (e.g., higher sales + higher variable costs)
2. **Root Cause Hypotheses**: For each material variance, suggest possible explanations:
   - Revenue variances: volume changes, pricing changes, product mix shifts, seasonal effects
   - Cost variances: input price changes, efficiency changes, activity level changes, one-time items
3. **Offsetting Analysis**: Identify variances that partially cancel each other
4. **Trend Comparison**: Compare current period variance to prior periods if data available
5. **Action Recommendations**: Prioritized corrective actions for unfavorable variances

## Output

The analysis produces a structured variance report containing:

1. **Executive Summary**: Total favorable/unfavorable variance, key highlights
2. **Variance Detail Table**: Per-account breakdown with amounts, percentages, and direction
3. **Materiality Ranking**: Top variances sorted by absolute impact
4. **Root Cause Analysis**: Hypotheses and supporting evidence for major variances
5. **Recommended Actions**: Prioritized list of corrective/follow-up actions

Output template: `skills/ma-budget-actual-variance/assets/variance_report_template_ja.md` (Japanese) or `skills/ma-budget-actual-variance/assets/variance_report_template_en.md` (English)

## Resources

### References (load into context for guidance)

- `skills/ma-budget-actual-variance/references/第08回_予算実績差異分析_20250820.md` - Comprehensive guide on budget-actual variance analysis methodology with practical bakery business examples
- `skills/ma-budget-actual-variance/references/第05回_その予算って根拠あるの_20250507.md` - Budget planning fundamentals and evidence-based budgeting approaches

### Assets (templates for output generation)

- `skills/ma-budget-actual-variance/assets/variance_report_template_ja.md` - Japanese variance analysis report template
- `skills/ma-budget-actual-variance/assets/variance_report_template_en.md` - English variance analysis report template

## Best Practices

- Always verify account type classification before calculating variance direction
- Present both absolute amounts and percentages - large percentage on a small base may not be material
- Consider the business context: seasonal patterns, one-time events, and structural changes
- Look for offsetting variances - a favorable cost variance paired with unfavorable revenue may indicate reduced activity
- When budget assumptions have changed significantly, consider rebasing before analysis
- Focus management attention on actionable variances rather than uncontrollable factors

## Examples

### Example: Bakery Business Monthly Variance

**Input Data:**
```csv
account_name,account_type,budget,actual
Bread Sales,revenue,500000,480000
Cake Sales,revenue,300000,350000
Flour Cost,cost,120000,135000
Sugar Cost,cost,80000,75000
Labor Cost,cost,200000,210000
Rent,cost,100000,100000
```

**Analysis Output (Summary):**
- Total Revenue Variance: +30,000 (Favorable) - Cake sales overperformance offsets bread shortfall
- Total Cost Variance: +40,000 (Unfavorable) - Flour cost increase and overtime labor
- Net Variance: -10,000 (Unfavorable)

**Key Findings:**
1. Cake Sales +50,000 (F): New seasonal menu drove demand
2. Flour Cost +15,000 (U): Wheat price increase due to supply shortage
3. Labor Cost +10,000 (U): Overtime to meet cake demand
4. Bread Sales -20,000 (U): Competitor opened nearby - requires strategic response
