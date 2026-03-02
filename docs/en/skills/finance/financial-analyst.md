---
layout: default
title: Financial Analyst
grand_parent: English
parent: Finance & Analysis
nav_order: 1
lang_peer: /ja/skills/finance/financial-analyst/
permalink: /en/skills/finance/financial-analyst/
---

# Financial Analyst
{: .no_toc }

Comprehensive financial analysis for investment decisions, budgeting, and business evaluation.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-workflow">Workflow</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Financial Analyst provides a systematic toolkit for evaluating financial health, investment opportunities, and business performance. It combines quantitative analysis with professional reporting across four core workflows:

| Workflow | Purpose |
|:---------|:--------|
| **Financial Statement Analysis** | Calculate profitability, liquidity, and efficiency ratios with benchmarks |
| **Investment Evaluation (DCF)** | NPV, IRR, WACC, and payback period calculations |
| **Budget Variance Analysis** | Actual vs. budget comparison with root-cause decomposition |
| **Sensitivity & Scenario Analysis** | Risk assessment through variable stress testing |

Outputs include structured Markdown reports, visualization charts (PNG via matplotlib/seaborn), and summary tables with interpretations.

## When to Use

- **Analyze financial statements** -- calculate key ratios and assess company health from balance sheet and income statement data
- **Evaluate investment opportunities** -- run DCF valuations, compute NPV/IRR, and compare against hurdle rates
- **Review budget performance** -- identify material variances and decompose them into price, volume, and mix components
- **Assess risk** -- perform single-variable sensitivity analysis, multi-scenario modeling, and break-even calculations

## Prerequisites

- Claude Code installed and running
- The `financial-analyst` skill copied to `~/.claude/skills/`
- Financial data in JSON or CSV format (balance sheet, income statement, cash flow projections, or budget files)

No external API keys are required. The bundled Python script (`financial_analyzer.py`) uses standard libraries plus matplotlib/seaborn for charts.

## How It Works

### 1. Data Ingestion

Provide financial data as JSON or CSV. Claude validates required fields (balance sheet, income statement) and checks for inconsistencies such as negative values, mismatched totals, or missing periods. If fields are missing, Claude reports which ones are absent before proceeding.

### 2. Ratio Calculation and Analysis

Depending on the workflow, Claude calculates one or more of the following:

- **Financial ratios** -- profitability (ROE, ROA, margins), safety/liquidity (current ratio, quick ratio, D/E, interest coverage), and efficiency (asset turnover, inventory turnover, receivables turnover).
- **Discounted cash flows** -- NPV, IRR, and payback period using projected cash flows and a discount rate.
- **Budget variances** -- line-by-line actual vs. budget comparison, decomposed into price, volume, and mix components.
- **Sensitivity ranges** -- single-variable and multi-variable stress tests on key assumptions.

### 3. Interpretation and Classification

Each metric is classified into one of three levels:

| Level | Color | Meaning |
|:------|:------|:--------|
| Strong | Green | Exceeds benchmark; no action required |
| Acceptable | Yellow | Within normal range; monitor |
| Weak | Red | Below threshold; corrective action recommended |

Industry context is applied when the user specifies a sector. Without a sector, general cross-industry benchmarks are used.

### 4. Visualization

Claude generates charts using matplotlib/seaborn:

- **Radar chart** for ratio analysis (shows strengths and weaknesses at a glance)
- **Waterfall chart** for budget variance (cumulative contribution of each line item)
- **Tornado chart** for sensitivity analysis (variables ranked by NPV impact)
- **Bar/line charts** for trend comparisons across periods

### 5. Report Generation

Results are formatted into a professional Markdown report using bundled templates (`financial_report_template_en.md` or `financial_report_template_ja.md`). Each report includes an executive summary, detailed tables, embedded charts, and actionable recommendations.

### Key Formulas

| Metric | Formula |
|:-------|:--------|
| ROE | Net Income / Total Equity |
| ROA | Net Income / Total Assets |
| Current Ratio | Current Assets / Current Liabilities |
| Quick Ratio | (Current Assets - Inventory) / Current Liabilities |
| D/E Ratio | Total Liabilities / Total Equity |
| NPV | -Investment + Sum(CF_t / (1+r)^t) + Terminal Value |
| IRR | Rate where NPV = 0 (Newton-Raphson iteration) |
| WACC | (E/V x Re) + (D/V x Rd x (1 - Tc)) |
| Variance % | (Actual - Budget) / Budget x 100 |

## Industry Benchmark Reference

Ratio thresholds vary significantly by sector. The table below provides representative benchmarks for common industries.

### Profitability Benchmarks

| Sector | Gross Margin | Operating Margin | Net Margin | ROE |
|:-------|:-------------|:-----------------|:-----------|:----|
| Technology / SaaS | 60--80% | 15--30% | 10--25% | 15--30% |
| Manufacturing | 25--40% | 8--15% | 5--10% | 10--18% |
| Retail | 25--35% | 3--8% | 2--5% | 12--20% |
| Financial Services | 40--60% | 25--40% | 15--30% | 10--15% |
| Healthcare / Pharma | 50--70% | 15--25% | 10--20% | 12--22% |
| Utilities | 30--50% | 15--25% | 8--15% | 8--12% |

### Liquidity and Leverage Benchmarks

| Sector | Current Ratio | Quick Ratio | D/E Ratio | Interest Coverage |
|:-------|:-------------|:------------|:----------|:-----------------|
| Technology / SaaS | 2.0--4.0 | 1.5--3.0 | 0.2--0.8 | 10+ |
| Manufacturing | 1.5--2.5 | 0.8--1.5 | 0.5--1.5 | 4--8 |
| Retail | 1.2--2.0 | 0.5--1.0 | 0.8--2.0 | 3--6 |
| Financial Services | N/A | N/A | 2.0--10.0 | 2--5 |
| Healthcare / Pharma | 1.5--3.0 | 1.0--2.0 | 0.3--1.0 | 6--12 |
| Utilities | 0.8--1.2 | 0.5--0.8 | 1.0--2.5 | 2--4 |

Mention the sector in your prompt (e.g., "This is a SaaS company") to receive sector-specific interpretations.

## DCF Step-by-Step Detail

### Calculating WACC

WACC (Weighted Average Cost of Capital) is the discount rate used for DCF valuations. It blends the cost of equity and after-tax cost of debt weighted by their proportion in the capital structure.

```
WACC = (E/V x Re) + (D/V x Rd x (1 - Tc))

Where:
  E  = Market value of equity
  D  = Market value of debt
  V  = E + D (total firm value)
  Re = Cost of equity (often from CAPM: Rf + Beta x Market Risk Premium)
  Rd = Cost of debt (yield on existing debt or new issuance rate)
  Tc = Corporate tax rate
```

**Typical input example:**

| Component | Value |
|:----------|:------|
| Equity value (E) | $600M |
| Debt value (D) | $400M |
| Cost of equity (Re) | 12% |
| Cost of debt (Rd) | 5% |
| Tax rate (Tc) | 25% |
| **WACC** | **(600/1000 x 12%) + (400/1000 x 5% x 0.75) = 8.7%** |

### Terminal Value Approaches

The DCF model projects explicit cash flows for a finite horizon (typically 5--10 years). Beyond that, a terminal value captures the remaining value. Two methods are supported:

**1. Gordon Growth Model (Perpetuity Growth)**

```
Terminal Value = CF_n x (1 + g) / (WACC - g)
```

Best used when the company is expected to grow at a stable rate indefinitely. The growth rate (g) should not exceed long-term GDP growth (typically 2--3%).

**2. Exit Multiple Method**

```
Terminal Value = Final Year EBITDA x Industry EV/EBITDA Multiple
```

Best used when comparable transactions or trading multiples are available. Common multiples by sector:

| Sector | Typical EV/EBITDA |
|:-------|:-----------------|
| Technology | 15--25x |
| Manufacturing | 8--12x |
| Retail | 6--10x |
| Healthcare | 12--18x |
| Utilities | 8--12x |

### NPV Decision Framework

After computing NPV, IRR, and payback period, apply the following decision criteria:

| Metric | Accept | Reject | Notes |
|:-------|:-------|:-------|:------|
| NPV | > 0 | < 0 | Higher NPV = more value created |
| IRR | > WACC | < WACC | Margin above WACC indicates safety buffer |
| Payback | < Target period | > Target period | Simple payback ignores time value; use discounted payback for rigor |

## Usage Examples

### Example 1: Financial ratio analysis

```
Analyze these financial statements and calculate key ratios.
Data: financial_data.json
Focus on profitability and liquidity.
```

Claude reads the JSON, calculates all ratio categories, generates a radar chart, and outputs a report with severity-coded interpretations.

### Example 2: DCF valuation

```
Perform a DCF valuation for this acquisition target.
Initial investment: $50M
Projected cash flows: $10M, $15M, $20M, $22M, $25M over 5 years
Discount rate: 10%, terminal growth: 2%
```

Claude calculates NPV, IRR, payback period, and provides a go/no-go recommendation with sensitivity ranges.

### Example 3: Budget variance analysis

```
Compare actual.csv and budget.csv.
Identify all variances over 5% and provide root cause analysis.
```

Claude merges the two files, flags material variances, decomposes them into price and volume components, and generates a waterfall chart.

### Example 4: Sensitivity analysis on a DCF model

```
Run a sensitivity analysis on the factory investment DCF.
Vary revenue growth (+/-20%) and discount rate (+/-3pp).
Show a tornado chart and identify the break-even revenue level.
```

Claude produces a tornado chart ranking variables by NPV impact, a data table with NPV at each test point, and the break-even revenue where NPV equals zero.

### Example 5: Multi-period trend analysis

```
Analyze the financial statements for FY2022, FY2023, and FY2024.
Show year-over-year ratio trends and highlight any deteriorating metrics.
```

Claude calculates ratios for each period, generates trend line charts, and flags metrics that show consistent decline across periods.

## Troubleshooting

### Incomplete ratio results

**Symptom**: Some ratios appear as "N/A" or are missing from the report.

**Solution**: Ensure all required fields are present in the input data. The minimum required fields are: `total_assets`, `current_assets`, `total_liabilities`, `current_liabilities`, `total_equity`, `revenue`, `cost_of_goods_sold`, `operating_income`, and `net_income`. If a field is missing, the ratios that depend on it will be skipped.

### NPV calculation seems incorrect

**Symptom**: NPV value does not match manual calculation.

**Solution**: Check that (1) the initial investment is entered as a positive number (the script negates it internally), (2) cash flows are in the same currency units as the investment, and (3) the discount rate is expressed as a decimal (e.g., 0.10 for 10%, not 10). Also verify whether terminal value is included -- omitting it for a going-concern business will significantly understate value.

### Charts not generated

**Symptom**: The report contains tables but no PNG chart files.

**Solution**: The `financial_analyzer.py` script requires `matplotlib` and `seaborn`. Install them with `pip install matplotlib seaborn` (or `uv pip install matplotlib seaborn`). If running in a headless environment, set the matplotlib backend with `export MPLBACKEND=Agg` before execution.

## Tips & Best Practices

- **Provide complete data** -- the more fields you include (balance sheet, income statement, cash flow), the richer the analysis.
- **Specify the currency and period** -- this ensures correct formatting and period-over-period comparisons.
- **Use JSON for structured data** -- JSON input enables automatic field validation; CSV works but requires consistent column naming.
- **Combine workflows** -- run a DCF first, then apply sensitivity analysis to stress-test the key assumptions.
- **Check thresholds in context** -- ratio benchmarks vary by industry. Mention the sector if you want industry-specific interpretation.

## Related Skills

- **IT System ROI Analyzer** -- ROI and TCO analysis specifically for IT investments
- [Project Plan Creator]({{ '/en/skills/management/project-plan-creator/' | relative_url }}) -- project planning with budget and resource allocation
