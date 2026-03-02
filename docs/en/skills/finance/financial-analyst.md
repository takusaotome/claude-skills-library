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

<span class="badge badge-free">No API Required</span> <span class="badge badge-workflow">Workflow</span>

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

1. **Data Ingestion** -- provide financial data as JSON or CSV. Claude validates required fields and checks for inconsistencies.
2. **Analysis** -- depending on the workflow, Claude calculates ratios, discounted cash flows, variances, or sensitivity ranges.
3. **Interpretation** -- each metric is classified (Strong / Acceptable / Weak) with industry context and threshold-based color coding.
4. **Reporting** -- results are formatted into a professional report using bundled templates, including charts and actionable recommendations.

### Key Formulas

| Metric | Formula |
|:-------|:--------|
| ROE | Net Income / Total Equity |
| Current Ratio | Current Assets / Current Liabilities |
| NPV | -Investment + Sum(CF_t / (1+r)^t) + Terminal Value |
| IRR | Rate where NPV = 0 |
| Variance % | (Actual - Budget) / Budget x 100 |

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

## Tips & Best Practices

- **Provide complete data** -- the more fields you include (balance sheet, income statement, cash flow), the richer the analysis.
- **Specify the currency and period** -- this ensures correct formatting and period-over-period comparisons.
- **Use JSON for structured data** -- JSON input enables automatic field validation; CSV works but requires consistent column naming.
- **Combine workflows** -- run a DCF first, then apply sensitivity analysis to stress-test the key assumptions.
- **Check thresholds in context** -- ratio benchmarks vary by industry. Mention the sector if you want industry-specific interpretation.

## Related Skills

- [IT System ROI Analyzer]({{ '/en/skills/dev/it-system-roi-analyzer/' | relative_url }}) -- ROI and TCO analysis specifically for IT investments
- [Project Plan Creator]({{ '/en/skills/management/project-plan-creator/' | relative_url }}) -- project planning with budget and resource allocation
