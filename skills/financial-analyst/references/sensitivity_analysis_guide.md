# Sensitivity and Scenario Analysis Guide

## Overview

Sensitivity and scenario analysis are essential risk assessment techniques that help decision-makers understand how changes in key assumptions affect investment outcomes. This guide covers methodology, best practices, and visualization techniques.

---

## 1. Types of Uncertainty Analysis

### 1.1 Sensitivity Analysis

Tests the impact of changing **one variable at a time** while holding others constant.

**Purpose:**
- Identify which variables have the greatest impact on outcomes
- Determine break-even points for key assumptions
- Prioritize areas for deeper research or risk mitigation

### 1.2 Scenario Analysis

Examines **multiple variables changing simultaneously** across coherent scenarios.

**Purpose:**
- Assess outcomes under different future states
- Understand correlation between variables
- Plan for distinct possible futures

### 1.3 Monte Carlo Simulation

Uses **probability distributions** for variables to generate thousands of possible outcomes.

**Purpose:**
- Quantify probability of different outcomes
- Generate confidence intervals for forecasts
- Capture complex variable interactions

---

## 2. Single-Variable Sensitivity Analysis

### 2.1 Process

1. **Identify key variables** that drive value
2. **Define range** for each variable (typically ±10-20%)
3. **Calculate outcomes** (NPV, IRR, etc.) at each point
4. **Record and analyze** results
5. **Visualize** using tornado charts or tables

### 2.2 Common Variables to Test

| Category | Variables |
|----------|-----------|
| Revenue | Growth rate, Price, Volume, Market share |
| Costs | COGS, Operating expenses, Labor costs |
| Capital | CapEx, Working capital, Depreciation |
| Financing | Discount rate, Cost of debt, Tax rate |
| Timing | Project duration, Ramp-up period |

### 2.3 Sensitivity Table Format

```
| Variable        | -20%      | -10%      | Base      | +10%      | +20%      |
|-----------------|-----------|-----------|-----------|-----------|-----------|
| Revenue         | $2.1M     | $3.5M     | $4.8M     | $6.2M     | $7.5M     |
| COGS            | $6.5M     | $5.7M     | $4.8M     | $4.0M     | $3.1M     |
| Discount Rate   | $5.8M     | $5.3M     | $4.8M     | $4.4M     | $4.0M     |
```

### 2.4 Tornado Chart

Tornado charts visualize sensitivity by showing NPV swing for each variable:

```
Revenue        |████████████████████████████| $5.4M swing
COGS           |██████████████████        | $3.4M swing
Discount Rate  |████████████              | $1.8M swing
Working Cap    |██████                    | $0.9M swing
```

**Reading Tornado Charts:**
- Longer bars = Greater sensitivity
- Variables sorted by impact magnitude
- Helps prioritize risk mitigation efforts

---

## 3. Scenario Analysis

### 3.1 Standard Scenarios

| Scenario | Description | Probability |
|----------|-------------|-------------|
| **Best Case** | Optimistic assumptions; favorable market conditions | 15-25% |
| **Base Case** | Most likely outcome; current expectations | 50-60% |
| **Worst Case** | Pessimistic assumptions; adverse conditions | 15-25% |

### 3.2 Scenario Definition Process

**Step 1: Identify scenario drivers**
- Macroeconomic factors (GDP, interest rates)
- Industry-specific factors (demand, competition)
- Company-specific factors (execution, technology)

**Step 2: Define coherent scenarios**
Scenarios should be internally consistent:
- If economy is weak → lower revenue AND lower costs
- If competition increases → lower prices AND higher marketing spend

**Step 3: Assign variable values**

| Variable | Best Case | Base Case | Worst Case |
|----------|-----------|-----------|------------|
| Revenue Growth | +15% | +10% | +3% |
| Gross Margin | 42% | 40% | 35% |
| Operating Expenses | -5% | 0% | +10% |
| CapEx | -10% | 0% | +15% |

**Step 4: Calculate outcomes**
For each scenario, calculate:
- NPV
- IRR
- Payback Period
- Key financial ratios

### 3.3 Probability-Weighted Value

```
Expected NPV = P(Best) × NPV(Best)
             + P(Base) × NPV(Base)
             + P(Worst) × NPV(Worst)

Example:
Expected NPV = 0.20 × $8M + 0.55 × $5M + 0.25 × $2M
             = $1.6M + $2.75M + $0.5M
             = $4.85M
```

---

## 4. Break-Even Analysis

### 4.1 Break-Even Point

The value of a variable where NPV = 0 (or IRR = WACC).

**Common Break-Even Questions:**
- What minimum revenue is needed to break even?
- What maximum cost can we absorb?
- What's the highest acceptable discount rate?

### 4.2 Break-Even Calculation

**Method: Goal-seek or iterative calculation**

Example: Find break-even revenue
```
1. Start with base case revenue = $10M, NPV = $2M
2. Reduce revenue until NPV = $0
3. Break-even revenue = $7.5M
4. Margin of safety = ($10M - $7.5M) / $10M = 25%
```

### 4.3 Margin of Safety

```
Margin of Safety = (Base Case Value - Break-even Value) / Base Case Value × 100%
```

| Margin of Safety | Risk Assessment |
|-----------------|-----------------|
| >30% | Low risk |
| 15-30% | Moderate risk |
| <15% | High risk |

---

## 5. Advanced Techniques

### 5.1 Two-Variable Sensitivity (Data Tables)

Shows NPV for combinations of two variables:

```
                    | Discount Rate
                    | 8%    | 10%   | 12%   | 14%
--------------------|-------|-------|-------|-------
Revenue   +20%      | $6.5M | $5.8M | $5.2M | $4.7M
Growth    +10%      | $5.2M | $4.8M | $4.3M | $3.9M
          0%        | $4.0M | $3.8M | $3.5M | $3.2M
          -10%      | $2.8M | $2.7M | $2.6M | $2.4M
```

### 5.2 Spider Diagram

Shows relative sensitivity of NPV to percentage changes in multiple variables on a single chart:

- X-axis: % change in variable (-20% to +20%)
- Y-axis: NPV
- Each variable is a separate line
- Steeper slope = Higher sensitivity

### 5.3 Monte Carlo Simulation Concepts

**Process:**
1. Define probability distributions for key variables
2. Generate random samples (1000-10000+ iterations)
3. Calculate NPV for each iteration
4. Analyze distribution of outcomes

**Common Distributions:**
| Variable Type | Distribution |
|--------------|--------------|
| Growth rates | Normal |
| Prices | Lognormal |
| Success/failure | Binomial |
| Project duration | Triangular, PERT |

**Outputs:**
- Mean and median NPV
- Standard deviation
- Probability of NPV > 0
- Value at Risk (VaR)
- Confidence intervals

---

## 6. Best Practices

### 6.1 Variable Selection

**Include:**
- Variables with high uncertainty
- Variables with high impact on value
- Variables management can influence

**Exclude:**
- Variables that are well-known or contractually fixed
- Variables with minimal impact
- Variables that are highly correlated (pick one)

### 6.2 Range Selection

| Confidence Level | Typical Range |
|-----------------|---------------|
| Low confidence | ±30-50% |
| Medium confidence | ±15-25% |
| High confidence | ±5-10% |

**Sources for ranges:**
- Historical variance
- Expert judgment
- Industry benchmarks
- Management guidance

### 6.3 Documentation

Always document:
- Which variables were tested and why
- Range definitions and sources
- Key assumptions
- Limitations of analysis

### 6.4 Presentation

**Lead with key insights:**
1. Which variables matter most?
2. What are the break-even points?
3. How confident are we in the base case?

**Visualization tips:**
- Use tornado charts for single-variable sensitivity
- Use scenario tables for multi-variable analysis
- Show probability-weighted expected values
- Include confidence ranges

---

## 7. Common Pitfalls

1. **Too many variables** - Focus on top 5-7 drivers
2. **Unrealistic ranges** - Base on evidence, not guesses
3. **Ignoring correlations** - Scenarios should be coherent
4. **Analysis paralysis** - Don't over-engineer; focus on insights
5. **Missing break-even** - Always calculate the safety margin
6. **No probability weighting** - Assign likelihoods to scenarios
7. **Static analysis** - Update as new information emerges

---

## 8. Quick Reference

### Sensitivity Analysis Checklist

- [ ] Identify 5-7 key value drivers
- [ ] Define realistic ranges (±10-30%)
- [ ] Calculate NPV at each test point
- [ ] Create tornado chart
- [ ] Identify break-even points
- [ ] Calculate margin of safety
- [ ] Document assumptions

### Scenario Analysis Checklist

- [ ] Define 3-4 coherent scenarios
- [ ] Assign probability weights
- [ ] Ensure internal consistency
- [ ] Calculate outcomes for each
- [ ] Compute probability-weighted value
- [ ] Document rationale for scenarios

### Risk Assessment Matrix

| Variable Impact | Low Uncertainty | High Uncertainty |
|-----------------|-----------------|------------------|
| High Impact | Monitor | Critical - Mitigate |
| Low Impact | Accept | Review periodically |
