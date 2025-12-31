---
name: financial-analyst
description: Professional financial analysis skill for investment decisions, budgeting, financial statement analysis, and business plan evaluation. Use this skill when you need to analyze financial ratios (profitability, safety, efficiency), calculate DCF/NPV/IRR valuations, perform budget variance analysis, or conduct sensitivity/scenario analysis. Triggers include "analyze financial statements", "calculate DCF", "investment evaluation", "budget variance", "財務分析", "投資評価", "予算差異分析".
---

# Financial Analyst

## Overview

A comprehensive financial analysis toolkit that enables systematic evaluation of financial health, investment opportunities, and business performance. This skill combines quantitative analysis with professional reporting to support informed decision-making.

**Core Capabilities:**
- Financial ratio analysis (Profitability, Safety/Liquidity, Efficiency)
- DCF/NPV/IRR investment evaluation
- Budget variance analysis with root cause decomposition
- Sensitivity and scenario analysis for risk assessment

**Output Formats:**
- Structured analysis reports (Markdown)
- Visualization charts (PNG via matplotlib/seaborn)
- Summary tables with interpretation

---

## When to Use This Skill

Use this skill when you need to:

1. **Analyze Financial Statements**
   - "Analyze these financial statements and calculate key ratios"
   - "What's the financial health of this company based on their balance sheet?"
   - "この会社の財務諸表から収益性を分析してください"

2. **Evaluate Investment Opportunities**
   - "Calculate the NPV and IRR for this investment project"
   - "Perform a DCF valuation for this acquisition target"
   - "この投資案件のDCF評価を行ってください"

3. **Analyze Budget Performance**
   - "Compare actual vs budget and identify variances"
   - "What's causing the budget overrun in Q3?"
   - "予算差異分析を行い、原因を特定してください"

4. **Assess Risk and Scenarios**
   - "Run a sensitivity analysis on revenue assumptions"
   - "What happens to NPV under different scenarios?"
   - "感度分析でリスク要因を評価してください"

---

## Core Workflow 1: Financial Statement Analysis

Analyze financial ratios from structured data to assess company health.

### Input Requirements

Accept data in JSON or CSV format:

```json
{
  "company": "ABC Corp",
  "period": "2024-Q4",
  "balance_sheet": {
    "total_assets": 100000000,
    "current_assets": 40000000,
    "cash": 10000000,
    "inventory": 15000000,
    "receivables": 12000000,
    "total_liabilities": 60000000,
    "current_liabilities": 25000000,
    "long_term_debt": 30000000,
    "total_equity": 40000000
  },
  "income_statement": {
    "revenue": 80000000,
    "cost_of_goods_sold": 48000000,
    "gross_profit": 32000000,
    "operating_expenses": 16000000,
    "operating_income": 16000000,
    "interest_expense": 2000000,
    "net_income": 10000000
  }
}
```

### Step 1: Load and Validate Data

Read the input file and validate required fields:
- Ensure all balance sheet items are present
- Verify income statement completeness
- Check for negative values that shouldn't be negative

### Step 2: Calculate Financial Ratios

**Profitability Ratios:**

| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| ROE (Return on Equity) | Net Income / Total Equity | >15% is generally good |
| ROA (Return on Assets) | Net Income / Total Assets | >5% is acceptable |
| Gross Margin | Gross Profit / Revenue | Industry-dependent |
| Operating Margin | Operating Income / Revenue | >10% is strong |
| Net Profit Margin | Net Income / Revenue | >5% is healthy |

**Safety/Liquidity Ratios:**

| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| Current Ratio | Current Assets / Current Liabilities | >1.5 is healthy |
| Quick Ratio | (Current Assets - Inventory) / Current Liabilities | >1.0 is acceptable |
| Debt-to-Equity | Total Liabilities / Total Equity | <1.0 is conservative |
| Interest Coverage | Operating Income / Interest Expense | >3.0 provides safety margin |

**Efficiency Ratios:**

| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| Asset Turnover | Revenue / Total Assets | Higher is more efficient |
| Inventory Turnover | COGS / Inventory | Higher means faster sales |
| Receivables Turnover | Revenue / Receivables | Higher means faster collection |
| Working Capital Turnover | Revenue / (Current Assets - Current Liabilities) | Measures working capital efficiency |

### Step 3: Generate Interpretation

For each ratio:
1. Calculate the value
2. Classify as: Strong (green), Acceptable (yellow), or Weak (red)
3. Provide industry context if available
4. Note any significant deviations from norms

### Step 4: Visualize Results

Generate a radar chart showing:
- All three ratio categories
- Comparison to benchmarks
- Strengths and weaknesses at a glance

### Step 5: Output Report

Use `assets/financial_report_template_ja.md` or `assets/financial_report_template_en.md` as the template. Include:
- Executive summary with key findings
- Detailed ratio table with interpretations
- Visualization charts
- Recommendations based on analysis

---

## Core Workflow 2: Investment Evaluation (DCF)

Perform Discounted Cash Flow analysis for investment decisions.

### Input Requirements

```json
{
  "project_name": "New Factory Investment",
  "initial_investment": 50000000,
  "projected_cash_flows": [10000000, 15000000, 20000000, 22000000, 25000000],
  "terminal_growth_rate": 0.02,
  "discount_rate": 0.10,
  "analysis_years": 5
}
```

### Step 1: Calculate NPV

```
NPV = -Initial Investment + Σ(CFt / (1 + r)^t) + Terminal Value / (1 + r)^n

Where:
- CFt = Cash flow at time t
- r = Discount rate
- n = Number of years
```

**Terminal Value Methods:**
1. **Gordon Growth Model**: CF_n × (1 + g) / (r - g)
2. **Exit Multiple**: Final Year EBITDA × Industry Multiple

### Step 2: Calculate IRR

Find the discount rate where NPV = 0 using Newton-Raphson iteration:

```python
def calculate_irr(cash_flows, guess=0.10, tolerance=0.0001):
    rate = guess
    for _ in range(100):
        npv = sum(cf / (1 + rate)**i for i, cf in enumerate(cash_flows))
        if abs(npv) < tolerance:
            return rate
        derivative = sum(-i * cf / (1 + rate)**(i+1) for i, cf in enumerate(cash_flows))
        rate = rate - npv / derivative
    return rate
```

### Step 3: Calculate WACC (if components provided)

```
WACC = (E/V × Re) + (D/V × Rd × (1 - Tc))

Where:
- E = Market value of equity
- D = Market value of debt
- V = E + D
- Re = Cost of equity
- Rd = Cost of debt
- Tc = Tax rate
```

### Step 4: Calculate Payback Period

Simple Payback:
```
Payback = Years until cumulative cash flow >= initial investment
```

Discounted Payback:
```
Payback = Years until cumulative discounted cash flow >= initial investment
```

### Step 5: Investment Decision Criteria

| Metric | Accept Criteria | Interpretation |
|--------|-----------------|----------------|
| NPV | > 0 | Project creates value |
| IRR | > WACC (or hurdle rate) | Returns exceed cost of capital |
| Payback | < Target period | Quick capital recovery |

Refer to `references/dcf_methodology.md` for detailed methodology.

---

## Core Workflow 3: Budget Variance Analysis

Compare actual results to budget and identify causes.

### Input Requirements

Two data files: `actual.csv` and `budget.csv` with matching structure:

```csv
category,item,amount
Revenue,Product Sales,85000000
Revenue,Service Revenue,15000000
Cost,Material Costs,35000000
Cost,Labor Costs,25000000
Expenses,Marketing,8000000
Expenses,Administration,5000000
```

### Step 1: Calculate Variances

For each line item:
```
Variance = Actual - Budget
Variance % = (Actual - Budget) / Budget × 100
```

Classify variances:
- **Favorable**: Revenue > Budget or Cost < Budget
- **Unfavorable**: Revenue < Budget or Cost > Budget

### Step 2: Decompose Variances

For volume-driven items, decompose into:
- **Price Variance**: (Actual Price - Budget Price) × Actual Quantity
- **Volume Variance**: (Actual Quantity - Budget Quantity) × Budget Price
- **Mix Variance**: For multi-product analysis

### Step 3: Identify Material Variances

Flag items where:
- Variance % exceeds threshold (typically 5-10%)
- Absolute variance is significant
- Trend indicates persistent deviation

### Step 4: Root Cause Analysis

For each material variance, document:
1. Category and item
2. Variance amount and percentage
3. Potential causes (internal/external)
4. Recommended corrective actions

### Step 5: Generate Variance Report

Use `assets/budget_variance_template_ja.md` or `assets/budget_variance_template_en.md`:
- Summary dashboard with key variances
- Waterfall chart showing variance buildup
- Detailed variance table by category
- Action items and recommendations

---

## Core Workflow 4: Sensitivity and Scenario Analysis

Assess risk by varying key assumptions.

### Step 1: Identify Key Variables

Common sensitivity variables:
- Revenue growth rate
- Cost inflation
- Discount rate
- Market size
- Price elasticity

### Step 2: Single-Variable Sensitivity

For each key variable:
1. Define range: Base ± 10%, ± 20%
2. Calculate NPV at each point
3. Record results

```
| Variable     | -20%    | -10%    | Base    | +10%    | +20%    |
|-------------|---------|---------|---------|---------|---------|
| Revenue     | $2.1M   | $3.5M   | $4.8M   | $6.2M   | $7.5M   |
| Costs       | $6.5M   | $5.7M   | $4.8M   | $4.0M   | $3.1M   |
```

### Step 3: Generate Tornado Chart

Rank variables by impact on NPV:
- Calculate NPV swing (high case - low case)
- Sort by swing magnitude
- Visualize as horizontal bar chart

### Step 4: Multi-Variable Scenario Analysis

Define scenarios:
- **Best Case**: Favorable assumptions
- **Base Case**: Expected assumptions
- **Worst Case**: Conservative assumptions

For each scenario:
1. Set all variable values
2. Calculate NPV, IRR, Payback
3. Assess probability

### Step 5: Break-Even Analysis

Calculate break-even points:
- Revenue required for NPV = 0
- Cost level where IRR = WACC
- Volume needed to recover investment

Refer to `references/sensitivity_analysis_guide.md` for methodology details.

---

## Python Script Usage

The `scripts/financial_analyzer.py` provides CLI automation:

### Financial Ratio Analysis
```bash
python financial_analyzer.py ratios <input.json> --output report.md --visualize
```

### DCF Valuation
```bash
python financial_analyzer.py dcf <project.json> --discount-rate 0.10 --terminal-method gordon
```

### Budget Variance
```bash
python financial_analyzer.py variance <actual.csv> <budget.csv> --threshold 5
```

### Sensitivity Analysis
```bash
python financial_analyzer.py sensitivity <model.json> --variables revenue,costs --range 20
```

---

## Best Practices

### Data Quality

1. **Verify source data** before analysis
2. **Standardize formats** (currency, units, dates)
3. **Document assumptions** clearly
4. **Cross-check calculations** with known values

### Analysis Rigor

1. **Use multiple metrics** - No single metric tells the whole story
2. **Consider industry context** - Benchmarks vary by sector
3. **Account for timing** - NPV is time-sensitive
4. **Stress test assumptions** - Challenge optimistic projections

### Reporting

1. **Lead with key findings** - Executive summary first
2. **Visualize data** - Charts communicate faster than tables
3. **Provide recommendations** - Analysis should drive action
4. **Document limitations** - Be transparent about uncertainties

---

## Resources

### Scripts
- `scripts/financial_analyzer.py` - Main analysis automation script

### References
- `references/financial_ratios_guide.md` - Detailed ratio definitions and benchmarks
- `references/dcf_methodology.md` - DCF calculation methodology
- `references/sensitivity_analysis_guide.md` - Sensitivity/scenario analysis guide

### Templates
- `assets/financial_report_template_ja.md` - Japanese financial report template
- `assets/financial_report_template_en.md` - English financial report template
- `assets/budget_variance_template_ja.md` - Japanese variance report template
- `assets/budget_variance_template_en.md` - English variance report template

---

## Quick Reference

### Financial Ratio Formulas

| Category | Ratio | Formula |
|----------|-------|---------|
| Profitability | ROE | Net Income / Equity |
| Profitability | ROA | Net Income / Assets |
| Profitability | Gross Margin | Gross Profit / Revenue |
| Profitability | Operating Margin | Operating Income / Revenue |
| Safety | Current Ratio | Current Assets / Current Liabilities |
| Safety | Quick Ratio | (Current Assets - Inventory) / Current Liabilities |
| Safety | D/E Ratio | Total Debt / Equity |
| Efficiency | Asset Turnover | Revenue / Assets |
| Efficiency | Inventory Turnover | COGS / Inventory |

### Investment Metrics

| Metric | Accept If | Reject If |
|--------|-----------|-----------|
| NPV | > 0 | < 0 |
| IRR | > WACC | < WACC |
| Payback | < Target | > Target |

### Variance Classification

| Variance Type | Favorable | Unfavorable |
|--------------|-----------|-------------|
| Revenue | Actual > Budget | Actual < Budget |
| Cost | Actual < Budget | Actual > Budget |
