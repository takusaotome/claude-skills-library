---
layout: default
title: Data Scientist
grand_parent: English
parent: Software Development
nav_order: 3
lang_peer: /ja/skills/dev/data-scientist/
permalink: /en/skills/dev/data-scientist/
---

# Data Scientist
{: .no_toc }

End-to-end data science workflow with automated EDA, model comparison, and time series analysis.
{: .fs-6 .fw-300 }

<span class="badge badge-scripts">Python Scripts</span> <span class="badge badge-workflow">Workflow</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Data Scientist provides a comprehensive, end-to-end data science workflow -- from exploratory data analysis through model training, evaluation, and reporting. The skill includes three Python automation scripts that handle the heavy lifting while Claude guides you through methodological decisions and interprets results.

**Core capabilities:**

- **Automated EDA** -- data quality assessment, distribution analysis, correlation exploration, and visualization generation
- **Model comparison** -- train and evaluate 7-9 algorithms (regression or classification) in a single command
- **Time series analysis** -- stationarity tests, seasonal decomposition, ACF/PACF, and multi-model forecasting
- **Professional reporting** -- structured analysis reports with executive summaries and business recommendations

## When to Use

- **Exploratory analysis** -- understand patterns, distributions, and relationships in tabular data
- **Predictive modeling** -- build classification or regression models and compare algorithms
- **Time series forecasting** -- analyze temporal data and forecast future values
- **Feature engineering** -- create and select optimal features for your models
- **Model evaluation** -- compare algorithms, interpret feature importance, check for overfitting
- **Reporting** -- generate comprehensive analysis reports for stakeholders

## Prerequisites

- Claude Code installed and running
- The `data-scientist` skill copied to `~/.claude/skills/`
- Python 3 with common data science libraries: `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `statsmodels`

Install dependencies:

```bash
pip install pandas scikit-learn matplotlib seaborn statsmodels
```

No external API keys are required.

## How It Works

The skill follows a 7-step workflow:

1. **Problem Definition** -- define the business problem, success criteria, and problem type (classification, regression, time series, clustering)
2. **Data Understanding** -- run automated EDA to assess quality, distributions, correlations, and outliers
3. **Data Preparation** -- feature engineering, encoding, scaling, and feature selection
4. **Model Training** -- automated comparison across multiple algorithms with cross-validation
5. **Model Evaluation** -- performance metrics, confusion matrices, residual analysis, feature importance
6. **Insights** -- translate findings into actionable business recommendations
7. **Communication** -- generate a structured report using the included template

### Bundled Scripts

| Script | Purpose |
|:-------|:--------|
| `auto_eda.py` | Automated EDA with data quality reports, distribution charts, and correlation analysis |
| `model_comparison.py` | Train and compare multiple ML models for regression or classification |
| `timeseries_analysis.py` | Stationarity tests, decomposition, ACF/PACF, and forecasting |

## Usage Examples

### Example 1: Explore a dataset

```
Analyze the file sales_data.csv. Run EDA, identify data quality issues,
and tell me which features are most correlated with revenue.
```

Claude runs `auto_eda.py`, reviews the output, and highlights key patterns, quality issues, and feature relationships.

### Example 2: Build and compare models

```
I have customer_data.csv with a "churned" column.
Build classification models to predict churn and recommend the best one.
```

Claude runs `model_comparison.py` for classification, evaluates F1/ROC-AUC across algorithms, analyzes the confusion matrix, and provides a recommendation with feature importance insights.

### Example 3: Forecast a time series

```
Using daily_revenue.csv (columns: date, revenue), forecast the next 90 days.
Show me confidence intervals and identify any seasonality.
```

Claude runs `timeseries_analysis.py`, reviews decomposition and stationarity tests, compares ARIMA vs exponential smoothing, and produces a forecast with confidence intervals.

## Tips & Best Practices

- **Start with EDA** -- always run exploratory analysis before jumping into modeling. It reveals data quality issues and informs feature engineering.
- **Specify the target column** -- tell Claude which column you want to predict so it can select the right problem type automatically.
- **Watch for data leakage** -- ensure features are created using only training data. Claude checks for this, but mentioning temporal constraints helps.
- **Don't rely on a single metric** -- for classification, check precision, recall, F1, and ROC-AUC together. For imbalanced data, avoid accuracy as the primary metric.
- **Iterate on features** -- after the first model comparison, use feature importance to guide further engineering.
- **Request a report** -- ask Claude to generate a structured analysis report for stakeholder communication.

### Problem Type Selection Guide

| Problem | Type | Key Metrics |
|:--------|:-----|:------------|
| Predict a number (price, revenue) | Regression | RMSE, MAE, R-squared |
| Predict a category (churn, fraud) | Classification | F1, ROC-AUC, Precision/Recall |
| Forecast future values | Time Series | MASE, MAE, coverage |
| Find groups in data | Clustering | Silhouette score, inertia |

## Related Skills

- [Critical Code Reviewer]({{ '/en/skills/dev/critical-code-reviewer/' | relative_url }}) -- review the quality of your analysis scripts
- [TDD Developer]({{ '/en/skills/dev/tdd-developer/' | relative_url }}) -- write tests for data processing pipelines
