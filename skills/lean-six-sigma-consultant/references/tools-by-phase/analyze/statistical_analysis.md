# Statistical Analysis Guide

## Overview

Statistical analysis in the Analyze phase helps verify root causes with data. This guide covers common statistical tests used in Six Sigma projects.

## When to Use Statistical Tests

Use statistical tests to:
- Verify suspected causes with data
- Determine if differences are real or due to chance
- Understand relationships between variables
- Make data-driven decisions

---

## Hypothesis Testing Framework

### The Concept
Hypothesis testing determines if observed differences are statistically significant or likely due to random variation.

### Key Terms

**Null Hypothesis (H₀)**: No effect or difference exists
**Alternative Hypothesis (H₁)**: Effect or difference exists
**Alpha (α)**: Significance level (typically 0.05)
**p-value**: Probability of seeing results if H₀ is true
**Decision**: If p-value < α, reject H₀

### Decision Rule
```
If p-value < 0.05 → Reject H₀ → Statistically significant
If p-value ≥ 0.05 → Fail to reject H₀ → Not significant
```

### Practical vs Statistical Significance
- Statistical: p-value < 0.05
- Practical: Is the difference meaningful?
- Both matter for decision-making

---

## Test Selection Guide

### Decision Tree

```
What are you comparing?
│
├── Means (averages)
│   ├── 2 groups → 2-Sample t-test
│   ├── Multiple groups → ANOVA
│   └── Paired data → Paired t-test
│
├── Proportions (%)
│   ├── 2 proportions → 2-Proportion test
│   └── Categories → Chi-Square test
│
├── Relationships
│   ├── Linear relationship → Correlation
│   └── Predictive model → Regression
│
└── Variance
    └── 2 groups → F-test / Levene's test
```

---

## Common Statistical Tests

### 1. 2-Sample t-Test

**Purpose**: Compare means of two groups

**When to Use**:
- Comparing continuous metric between two groups
- Examples: Shift A vs Shift B, Before vs After

**Assumptions**:
- Data is approximately normal (or n > 30)
- Independent samples
- Similar variances (or use Welch's t-test)

**Hypotheses**:
- H₀: μ₁ = μ₂ (means are equal)
- H₁: μ₁ ≠ μ₂ (means are different)

**Example**:
```
Question: Is there a difference in cycle time between Machine A and Machine B?

Data:
Machine A: n=30, mean=45.2 min, std=4.5
Machine B: n=30, mean=48.1 min, std=5.2

Result: p-value = 0.018

Interpretation: p < 0.05, reject H₀
Conclusion: Machine B has significantly longer cycle time than Machine A
```

### 2. Paired t-Test

**Purpose**: Compare means of paired/matched data

**When to Use**:
- Before/After measurements on same units
- Matched pairs comparisons

**Hypotheses**:
- H₀: μ_diff = 0 (no difference)
- H₁: μ_diff ≠ 0 (there is a difference)

**Example**:
```
Question: Did the training improve performance?

Data: 20 employees measured before and after training
Mean difference: -2.5 (improvement)

Result: p-value = 0.003

Conclusion: Training significantly improved performance
```

### 3. ANOVA (Analysis of Variance)

**Purpose**: Compare means of three or more groups

**When to Use**:
- Comparing continuous metric across multiple groups
- Examples: Compare 4 machines, 3 shifts, 5 suppliers

**Hypotheses**:
- H₀: μ₁ = μ₂ = μ₃ = ... (all means equal)
- H₁: At least one mean is different

**Example**:
```
Question: Do defect rates differ across three suppliers?

Data:
Supplier A: mean=2.1%
Supplier B: mean=3.8%
Supplier C: mean=2.3%

ANOVA Result: p-value = 0.008

Conclusion: At least one supplier differs significantly
Follow-up: Use post-hoc tests to identify which pairs differ
```

### 4. Chi-Square Test

**Purpose**: Test association between categorical variables

**When to Use**:
- Comparing proportions across categories
- Testing independence of two categorical variables

**Hypotheses**:
- H₀: Variables are independent
- H₁: Variables are associated

**Example**:
```
Question: Is defect type related to production shift?

Data:
         Shift 1  Shift 2  Shift 3
Type A      25       40       28
Type B      35       32       45

Chi-Square Result: p-value = 0.041

Conclusion: Defect type is related to shift
```

### 5. Correlation Analysis

**Purpose**: Measure strength of linear relationship

**When to Use**:
- Exploring relationship between two continuous variables
- Determining if variables move together

**Interpretation of r (correlation coefficient)**:
- r = +1: Perfect positive correlation
- r = 0: No correlation
- r = -1: Perfect negative correlation

| |r| Value | Interpretation |
|-----------|----------------|
| 0.0 - 0.2 | Very weak |
| 0.2 - 0.4 | Weak |
| 0.4 - 0.6 | Moderate |
| 0.6 - 0.8 | Strong |
| 0.8 - 1.0 | Very strong |

**Example**:
```
Question: Is temperature related to defect rate?

Data: 50 data points of temperature and defect rate

Result: r = 0.72, p-value = 0.001

Conclusion: Strong positive correlation
Higher temperature associated with higher defect rate
```

### 6. Regression Analysis

**Purpose**: Model relationship between variables

**When to Use**:
- Predicting Y from X
- Understanding how X affects Y
- Quantifying relationships

**Simple Linear Regression**:
```
Y = β₀ + β₁X + ε

Where:
Y = Response variable
X = Predictor variable
β₀ = Intercept
β₁ = Slope (effect of X on Y)
ε = Error
```

**Example**:
```
Question: How does temperature affect defect rate?

Model: Defect Rate = 1.2 + 0.08 × Temperature

Interpretation:
- Every 1°C increase → 0.08% increase in defect rate
- R² = 0.52 (52% of variation explained)
- p-value for slope = 0.001 (significant)
```

---

## Key Statistics to Report

### For t-tests and ANOVA
- Sample sizes (n)
- Means and standard deviations
- Test statistic (t or F)
- p-value
- Confidence interval for difference

### For Chi-Square
- Observed vs expected frequencies
- Chi-square statistic
- Degrees of freedom
- p-value

### For Regression
- R² (coefficient of determination)
- Coefficients (β values)
- p-values for coefficients
- Residual analysis results

---

## Assumptions and Checks

### Normality
- Check with histogram, normal probability plot
- If not normal: use larger sample (n > 30) or non-parametric test

### Equal Variance
- Check with residual plots, Levene's test
- If unequal: use Welch's t-test or transformation

### Independence
- Data points should not influence each other
- No autocorrelation

### Sample Size
- Larger samples → more power to detect differences
- Rule of thumb: n ≥ 30 per group

---

## Common Mistakes

1. **Confusing correlation with causation**: Correlation doesn't prove cause
2. **Ignoring assumptions**: Tests may be invalid if assumptions violated
3. **P-hacking**: Running many tests increases false positives
4. **Focusing only on p-value**: Consider practical significance too
5. **Small sample conclusions**: Large samples needed for reliable results
6. **Multiple comparisons**: Adjust alpha for multiple tests (Bonferroni)
7. **Ignoring effect size**: Statistical significance ≠ large effect
