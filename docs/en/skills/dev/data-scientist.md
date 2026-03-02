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

<span class="badge badge-scripts">Python Scripts</span>
<span class="badge badge-workflow">Workflow</span>

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

```
1. Problem Definition
       |
2. Data Understanding (EDA)
       |
3. Data Preparation & Feature Engineering
       |
4. Model Selection & Training
       |
5. Model Evaluation & Interpretation
       |
6. Insights & Recommendations
       |
7. Communication & Deployment
```

### Step 1: Problem Definition

Claude helps you translate the business question into a data science problem. This determines the problem type (classification, regression, time series, clustering), success criteria, and constraints (interpretability, latency, data volume). Claude asks clarifying questions such as "What business decision will this analysis inform?" and "Is model interpretability important?".

### Step 2: Data Understanding

Claude runs `auto_eda.py` to generate a comprehensive data profile, then reviews the output to identify quality issues, important patterns, and feature relationships. Manual follow-up analysis targets specific hypotheses that emerge from the automated report.

### Step 3: Data Preparation

Based on EDA findings, Claude applies feature engineering strategies: mathematical transformations for skewed distributions, encoding for categorical variables, interaction features, time-based features (lag, rolling statistics), and aggregation features. Feature selection methods (variance threshold, correlation filtering, tree-based importance) reduce dimensionality.

### Step 4: Model Training

Claude runs `model_comparison.py` to train and evaluate 7-9 algorithms automatically, using cross-validation for robust assessment. The script handles train/test splitting, hyperparameter defaults, and metric calculation.

### Step 5: Model Evaluation

Claude analyzes the comparison results, checks for overfitting (train vs. test score gap), reviews confusion matrices or residual plots, and interprets feature importance. SHAP values and partial dependence plots provide deeper model interpretation when needed.

### Step 6-7: Insights and Communication

Claude translates technical findings into business recommendations, quantifies impact, and generates a structured report using the included `analysis_report_template.md`.

### Bundled Scripts

| Script | Purpose | Key Outputs |
|:-------|:--------|:------------|
| `auto_eda.py` | Automated EDA: data quality, distributions, correlations | Text report, distribution charts, correlation heatmap |
| `model_comparison.py` | Train and compare 7-9 ML algorithms (regression or classification) | Performance comparison table, best model recommendation, feature importance |
| `timeseries_analysis.py` | Time series diagnostics and forecasting | Stationarity tests (ADF/KPSS), seasonal decomposition, ACF/PACF, forecasts with confidence intervals |

**Script usage:**

```bash
# EDA
python scripts/auto_eda.py data.csv --target target_col --output eda_results/

# Model comparison (regression)
python scripts/model_comparison.py data.csv price --problem-type regression --output model_results/

# Model comparison (classification)
python scripts/model_comparison.py data.csv churn --problem-type classification --output model_results/

# Time series
python scripts/timeseries_analysis.py sales.csv revenue --date-col date --forecast-periods 30 --output ts_results/
```

### Model Selection Flow

Claude selects the modeling approach based on problem characteristics:

| Factor | Small data (<10k rows) | Large data (>1M rows) |
|:-------|:----------------------|:----------------------|
| Interpretability needed | Linear/Logistic Regression, Decision Tree | Linear models with regularization |
| Maximum accuracy | Random Forest, SVM with cross-validation | Gradient Boosting (XGBoost, LightGBM) |
| Imbalanced classes | Balanced Random Forest, SMOTE + simple model | Class-weighted Gradient Boosting |
| Time series | ARIMA, Exponential Smoothing | XGBoost with lag features, Prophet |

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

### Example 4: Feature engineering guidance

```
I have a customer dataset with signup_date, last_login, total_purchases,
and product_category. Help me engineer features for a churn prediction model.
```

Claude creates RFM features (recency, frequency, monetary), tenure-based features, login frequency metrics, and category-interaction features, referencing the bundled `feature_engineering.md` guide.

### Example 5: Full analysis report

```
Analyze marketing_campaign.csv and generate a complete report
for the marketing team. They need to know which channels drive conversions.
```

Claude runs EDA, builds a classification model, interprets feature importance with SHAP, and generates a structured report using `analysis_report_template.md` with non-technical language.

## Troubleshooting

### auto_eda.py fails with missing dependencies

**Symptom**: Script raises `ModuleNotFoundError` for `pandas`, `seaborn`, or `statsmodels`.

**Solution**: Install all required libraries: `pip install pandas scikit-learn matplotlib seaborn statsmodels`. If using a virtual environment, ensure it is activated before running the script.

### Model comparison shows overfitting

**Symptom**: Training scores are high but test scores are significantly lower across all models.

**Solution**: This usually indicates data leakage or insufficient data. Check that no future information leaks into features (especially with time-based data). Try reducing model complexity, adding regularization, or collecting more training samples. Claude will flag this pattern automatically and suggest corrective actions.

### Time series forecast ignores seasonality

**Symptom**: The forecast line is flat or trending but misses clear weekly or monthly patterns visible in the raw data.

**Solution**: Ensure the `--date-col` parameter correctly identifies the date column, and that dates are in a parseable format. If seasonality is present but weak, explicitly tell Claude: "There is weekly seasonality in this data." Claude will adjust the decomposition and model parameters accordingly.

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
