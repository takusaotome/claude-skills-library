---
name: ma-cvp-break-even
description: |
  CVP（Cost-Volume-Profit）分析・損益分岐点分析スキル。固定費・変動費の構造分析、
  限界利益率の算出、損益分岐点売上高/数量の計算、安全余裕率の評価、
  目標利益達成に必要な売上高のシミュレーションを行う。多品目分析にも対応。

  Use when: 損益分岐点を知りたいとき、新規事業や価格変更の採算シミュレーション、
  固定費削減・変動費率改善の効果試算、What-if分析に使用。

  Triggers: "損益分岐点", "CVP", "break-even", "限界利益", "contribution margin",
  "安全余裕率", "margin of safety", "固変分解", "変動費率"
---

# CVP / Break-Even Analysis

## Overview

Cost-Volume-Profit analysis determines the relationship between costs, volume, and profit to find the break-even point and plan for target profits. Supports single-product and multi-product scenarios with what-if simulation capabilities.

## When to Use This Skill

Use this skill in the following scenarios:

1. **Break-Even Point Calculation** - Determine the sales volume needed to cover all costs
   - 「損益分岐点を計算して」「何個売れば元が取れる？」
2. **New Business/Product Feasibility** - Evaluate whether a new venture can be profitable
   - 「新商品の採算シミュレーションをして」「新規事業の損益分岐点を出して」
3. **Pricing Decision Support** - Analyze the profit impact of price changes
   - 「値上げしたら利益はどう変わる？」「価格設定のシミュレーションをして」
4. **Cost Structure Optimization** - Evaluate fixed cost reduction or variable cost improvement scenarios
   - 「固定費を削減したらどうなる？」「変動費率を改善した場合の効果は？」
5. **What-If / Sensitivity Analysis** - Model multiple scenarios for management decision-making
   - 「売上が10%減ったら利益はどうなる？」「What-if分析をして」

## Prerequisites

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

## Workflow 1: Cost Structure Analysis

1. **Identify Cost Behavior**: Classify all costs as fixed or variable
2. **Calculate Unit Contribution Margin**: `Unit CM = Selling Price - Variable Cost per Unit`
3. **Calculate CM Ratio**: `CM Ratio = Unit CM / Selling Price`
4. **Assess Cost Structure**: Determine operating leverage (fixed cost proportion)
5. **For Multi-Product**: Calculate weighted average CM ratio using sales mix

### Key Formulas

| Metric | Formula |
|--------|---------|
| Unit Contribution Margin | Selling Price - Variable Cost per Unit |
| Contribution Margin Ratio | CM / Sales |
| Total Contribution Margin | Sales - Total Variable Costs |

## Workflow 2: Break-Even Calculation

1. **Break-Even in Units**: `BEP (units) = Fixed Costs / Unit CM`
2. **Break-Even in Sales**: `BEP (sales) = Fixed Costs / CM Ratio`
3. **Target Profit Sales**: `Required Sales = (Fixed Costs + Target Profit) / CM Ratio`
4. **Margin of Safety**:
   - Amount: `Current Sales - Break-Even Sales`
   - Ratio: `(Current Sales - BEP) / Current Sales * 100%`
5. **Multi-Product BEP**: Use weighted average CM ratio, note constant sales mix assumption

### Margin of Safety Interpretation

| Margin of Safety Ratio | Risk Level | Interpretation |
|------------------------|------------|----------------|
| > 40% | Low | Strong buffer above break-even |
| 20% - 40% | Moderate | Adequate but monitor closely |
| 10% - 20% | Elevated | Limited margin, corrective action needed |
| < 10% | High | Near break-even, urgent attention required |

## Workflow 3: Scenario Analysis & Decision Support

1. **Price Change Scenarios**: Model profit impact of price increases/decreases
2. **Cost Structure Changes**: Simulate fixed cost reduction or variable cost improvement
3. **Volume Sensitivity**: Show profit at different volume levels (e.g., 80%, 90%, 100%, 110%, 120%)
4. **Operating Leverage Analysis**: How profit changes amplify relative to revenue changes
5. **Decision Recommendations**: Summarize findings with actionable recommendations

## Output

The analysis produces a structured CVP report containing:

1. **Cost Structure Summary**: Fixed costs, variable costs, CM ratio breakdown
2. **Break-Even Analysis**: BEP in units and sales, with visualization data
3. **Margin of Safety Assessment**: Current position relative to break-even
4. **Scenario Analysis Table**: Multiple what-if scenarios with profit projections
5. **Decision Recommendations**: Prioritized actions based on analysis

Output template: `skills/ma-cvp-break-even/assets/cvp_analysis_template_ja.md` (Japanese) or `skills/ma-cvp-break-even/assets/cvp_analysis_template_en.md` (English)

## Resources

### References (load into context for guidance)

- `references/第09回_損益分岐点って要は元を取るライン_20251005.md` - Break-even analysis fundamentals with practical bakery business examples, margin of safety concepts
- `references/第10回_差額原価収益分析_20251104.md` - Differential cost-revenue analysis for make-or-buy and special order decisions

### Assets (templates for output generation)

- `skills/ma-cvp-break-even/assets/cvp_analysis_template_ja.md` - Japanese CVP analysis report template
- `skills/ma-cvp-break-even/assets/cvp_analysis_template_en.md` - English CVP analysis report template

## Best Practices

- Always verify cost classification (fixed vs. variable) - misclassification leads to incorrect BEP
- CVP analysis assumes linear cost behavior within the relevant range
- For multi-product analysis, clearly state the sales mix assumption
- Present margin of safety alongside BEP to convey the risk context
- Include sensitivity analysis - single-point BEP is less useful than a range of scenarios
- Remember CVP limitations: single-period model, constant prices, no inventory changes

## Examples

### Example: Bakery Break-Even Analysis

**Input:**
- Selling Price per unit (bread loaf): ¥350
- Variable Cost per unit: ¥150
- Fixed Costs (monthly): ¥600,000
- Current Monthly Volume: 5,000 loaves

**Analysis:**
- Unit CM: ¥350 - ¥150 = ¥200
- CM Ratio: ¥200 / ¥350 = 57.1%
- BEP (units): ¥600,000 / ¥200 = 3,000 loaves
- BEP (sales): ¥600,000 / 0.571 = ¥1,050,000
- Current Sales: ¥1,750,000
- Margin of Safety: (¥1,750,000 - ¥1,050,000) / ¥1,750,000 = 40.0% (Low Risk)

**Scenario Analysis:**
| Scenario | Volume | Revenue | Profit | MoS |
|----------|--------|---------|--------|-----|
| Base Case | 5,000 | ¥1,750K | ¥400K | 40% |
| Price +10% | 5,000 | ¥1,925K | ¥575K | 47% |
| Volume -20% | 4,000 | ¥1,400K | ¥200K | 25% |
| Fixed Cost -10% | 5,000 | ¥1,750K | ¥460K | 44% |
