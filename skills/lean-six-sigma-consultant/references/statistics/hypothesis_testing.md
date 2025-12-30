# Hypothesis Testing Reference

## Overview

Hypothesis testing is a statistical method to determine whether there is enough evidence to support a claim about a population based on sample data.

---

## Framework

### Key Components

**Null Hypothesis (H₀)**:
- The default assumption
- States no effect, no difference, no relationship
- What we test against

**Alternative Hypothesis (H₁ or Hₐ)**:
- What we want to prove
- States there IS an effect, difference, or relationship

**Significance Level (α)**:
- Probability of rejecting H₀ when it's actually true (Type I error)
- Common values: 0.05 (5%), 0.01 (1%), 0.10 (10%)
- Chosen BEFORE analyzing data

**p-value**:
- Probability of getting results at least as extreme as observed, assuming H₀ is true
- Smaller p-value = stronger evidence against H₀

### Decision Rule

```
If p-value < α → Reject H₀ → Result is statistically significant
If p-value ≥ α → Fail to reject H₀ → Result is not significant
```

---

## Types of Errors

| | H₀ is TRUE | H₀ is FALSE |
|---|------------|-------------|
| **Reject H₀** | Type I Error (α) | Correct Decision (Power) |
| **Fail to Reject H₀** | Correct Decision | Type II Error (β) |

**Type I Error (α)**: False positive - finding an effect that doesn't exist
**Type II Error (β)**: False negative - missing an effect that does exist
**Power (1-β)**: Probability of correctly detecting a real effect

---

## Test Selection Guide

### Comparing Means

| Situation | Test |
|-----------|------|
| One sample mean vs. known value | 1-sample t-test |
| Two independent group means | 2-sample t-test |
| Two paired/matched group means | Paired t-test |
| Three or more group means | One-way ANOVA |
| Two factors | Two-way ANOVA |

### Comparing Proportions

| Situation | Test |
|-----------|------|
| One proportion vs. known value | 1-proportion test |
| Two proportions | 2-proportion test |
| Multiple proportions (contingency) | Chi-square test |

### Testing Relationships

| Situation | Test |
|-----------|------|
| Linear relationship | Correlation (Pearson) |
| Ranked relationship | Correlation (Spearman) |
| Predictive relationship | Regression |

### Testing Variance

| Situation | Test |
|-----------|------|
| Two variances | F-test, Levene's test |
| Multiple variances | Bartlett's test |

---

## Common Statistical Tests

### 1-Sample t-Test

**Purpose**: Compare sample mean to a known/target value

**Hypotheses**:
- H₀: μ = μ₀ (mean equals target)
- H₁: μ ≠ μ₀ (mean differs from target)

**Formula**:
```
t = (x̄ - μ₀) / (s / √n)

df = n - 1
```

**Example**:
```
Target fill weight: 500g
Sample: n=30, x̄=502.5g, s=5.2g

t = (502.5 - 500) / (5.2 / √30) = 2.63
p-value = 0.013

Since p < 0.05, reject H₀. Mean differs from 500g.
```

---

### 2-Sample t-Test

**Purpose**: Compare means of two independent groups

**Hypotheses**:
- H₀: μ₁ = μ₂ (means are equal)
- H₁: μ₁ ≠ μ₂ (means differ)

**Formula** (equal variances):
```
t = (x̄₁ - x̄₂) / √[s²p(1/n₁ + 1/n₂)]

s²p = [(n₁-1)s₁² + (n₂-1)s₂²] / (n₁ + n₂ - 2)

df = n₁ + n₂ - 2
```

**Example**:
```
Shift A: n=25, x̄=45.2, s=3.1
Shift B: n=30, x̄=48.5, s=3.4

t = -3.72, p-value = 0.0005

Since p < 0.05, reject H₀. Shifts differ significantly.
```

---

### Paired t-Test

**Purpose**: Compare means of paired/matched observations

**Hypotheses**:
- H₀: μd = 0 (mean difference is zero)
- H₁: μd ≠ 0 (mean difference is not zero)

**Formula**:
```
t = d̄ / (sd / √n)

Where:
d̄ = mean of differences
sd = standard deviation of differences
n = number of pairs
df = n - 1
```

**When to Use**:
- Before/after measurements on same subjects
- Matched pairs
- Same subject under two conditions

---

### One-Way ANOVA

**Purpose**: Compare means of three or more groups

**Hypotheses**:
- H₀: μ₁ = μ₂ = μ₃ = ... (all means equal)
- H₁: At least one mean differs

**Key Statistics**:
```
F = MSB / MSW

Where:
MSB = Mean Square Between groups (explained variance)
MSW = Mean Square Within groups (unexplained variance)
```

**ANOVA Table**:
| Source | SS | df | MS | F | p-value |
|--------|----|----|----|----|---------|
| Between | SSB | k-1 | MSB | MSB/MSW | |
| Within | SSW | N-k | MSW | | |
| Total | SST | N-1 | | | |

**Post-Hoc Tests** (if H₀ rejected):
- Tukey's HSD
- Bonferroni
- Dunnett's (compare to control)

---

### Chi-Square Test

**Purpose**: Test association between categorical variables

**Hypotheses**:
- H₀: Variables are independent
- H₁: Variables are associated

**Formula**:
```
χ² = Σ[(O - E)² / E]

Where:
O = Observed frequency
E = Expected frequency = (Row total × Column total) / Grand total
df = (rows - 1) × (columns - 1)
```

**Example**:
```
         Defective  Good   Total
Shift A     15       85     100
Shift B     25       75     100
Total       40      160     200

Expected for Shift A Defective: (100 × 40) / 200 = 20

χ² = (15-20)²/20 + (85-80)²/80 + (25-20)²/20 + (75-80)²/80
   = 1.25 + 0.31 + 1.25 + 0.31 = 3.12

df = 1, p-value = 0.077

Since p > 0.05, fail to reject H₀. No significant association.
```

---

### Correlation

**Purpose**: Measure strength of linear relationship

**Pearson Correlation (r)**:
```
r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²]
```

**Interpretation**:
| |r| | Strength |
|-----|----------|
| 0.0 - 0.2 | Very weak |
| 0.2 - 0.4 | Weak |
| 0.4 - 0.6 | Moderate |
| 0.6 - 0.8 | Strong |
| 0.8 - 1.0 | Very strong |

**Testing Significance**:
- H₀: ρ = 0 (no correlation)
- H₁: ρ ≠ 0 (correlation exists)

---

### Simple Linear Regression

**Purpose**: Model relationship between X and Y

**Model**:
```
Y = β₀ + β₁X + ε

Where:
β₀ = Intercept
β₁ = Slope (effect of X on Y)
ε = Error
```

**Key Statistics**:
- **R²**: Proportion of variance explained (0 to 1)
- **p-value for slope**: Is relationship significant?
- **Confidence intervals**: Range for predictions

---

## Assumptions

### For t-Tests and ANOVA

1. **Independence**: Observations are independent
2. **Normality**: Data approximately normal (less important with large n)
3. **Equal variances**: Groups have similar variances (for 2-sample t)

### Checking Assumptions

**Normality**:
- Histogram (visual)
- Normal probability plot
- Anderson-Darling test

**Equal Variances**:
- F-test
- Levene's test
- Compare s₁/s₂ ratio (should be < 2)

### When Assumptions Violated

**Non-normality**:
- Use larger sample (n > 30)
- Transform data (log, sqrt)
- Use non-parametric tests (Mann-Whitney, Kruskal-Wallis)

**Unequal Variances**:
- Use Welch's t-test
- Use Games-Howell post-hoc

---

## Sample Size and Power

### Power Analysis

**Power depends on**:
- Sample size (n): Larger n → higher power
- Effect size (Δ): Larger effect → higher power
- Significance level (α): Higher α → higher power
- Variance (σ): Lower variance → higher power

**General Guidelines**:
- Target power: 80% or higher
- Use power analysis software to determine sample size

### Rule of Thumb Sample Sizes

| Test | Minimum n per group |
|------|---------------------|
| t-test | 20-30 |
| ANOVA | 20 per group |
| Chi-square | 5+ expected per cell |
| Correlation | 30+ pairs |
| Regression | 10+ per predictor |

---

## Reporting Results

### Standard Format

```
A [test name] was conducted to [purpose]. Results indicated
[statistic] = [value], p = [value]. [Conclusion about H₀].
[Effect size] = [value], indicating a [small/medium/large] effect.
```

**Example**:
```
A two-sample t-test was conducted to compare cycle times between
Shift A (M=45.2, SD=3.1, n=25) and Shift B (M=48.5, SD=3.4, n=30).
Results indicated t(53) = -3.72, p < 0.001, suggesting a statistically
significant difference. Cohen's d = 1.01, indicating a large effect.
```

---

## Common Mistakes

1. **Confusing statistical and practical significance**
2. **P-hacking**: Running many tests to find significant results
3. **Ignoring assumptions**: Tests may be invalid
4. **Wrong test selection**: Using parametric when non-parametric needed
5. **Interpreting "fail to reject" as "accept H₀"**
6. **Not considering effect size**: Significance ≠ importance
7. **Small sample conclusions**: Insufficient power
