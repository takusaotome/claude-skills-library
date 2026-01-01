# Price Elasticity Analysis Guide

## Overview

Price elasticity analysis measures how sensitive customer demand is to price changes. Understanding elasticity helps optimize pricing decisions, forecast revenue impacts, and identify optimal price points for different customer segments.

This guide covers the major methodologies for measuring price elasticity in B2B IT services and consulting contexts.

---

## 1. Price Elasticity Fundamentals

### Definition

Price Elasticity of Demand (PED) measures the percentage change in quantity demanded resulting from a percentage change in price.

```
PED = (% Change in Quantity Demanded) / (% Change in Price)
     = (ΔQ/Q) / (ΔP/P)
```

### Interpretation

| Elasticity Value | Classification | Meaning |
|-----------------|----------------|---------|
| |E| > 1 | Elastic | Demand highly sensitive to price |
| |E| = 1 | Unit Elastic | Proportional change |
| |E| < 1 | Inelastic | Demand not sensitive to price |
| E = 0 | Perfectly Inelastic | No demand change (rare) |
| E = ∞ | Perfectly Elastic | Any price increase loses all demand |

### Revenue Implications

| Elasticity | Price Increase Effect | Price Decrease Effect |
|------------|----------------------|----------------------|
| Elastic (>1) | Revenue decreases | Revenue increases |
| Inelastic (<1) | Revenue increases | Revenue decreases |
| Unit Elastic (=1) | Revenue unchanged | Revenue unchanged |

---

## 2. Calculation Methods

### Point Elasticity

Measures elasticity at a specific price point:

```
E = (dQ/dP) × (P/Q)
```

**Example:**
```
At price P = $100, quantity Q = 1,000
If demand function: Q = 2000 - 10P
Then: dQ/dP = -10

E = -10 × (100/1000) = -1.0 (Unit Elastic)
```

### Arc Elasticity (Midpoint Method)

Measures elasticity over a price range, using midpoints to avoid asymmetry:

```
E = [(Q2-Q1) / ((Q2+Q1)/2)] / [(P2-P1) / ((P2+P1)/2)]
  = [(Q2-Q1) / (Q2+Q1)] × [(P2+P1) / (P2-P1)]
```

**Example:**
```
Price change: $100 → $120
Quantity change: 1,000 → 800

E = [(800-1000) / (800+1000)] × [(100+120) / (120-100)]
  = [-200 / 1800] × [220 / 20]
  = -0.111 × 11
  = -1.22 (Elastic)
```

### Revenue-Based Calculation

When only revenue data is available:

```
Revenue Elasticity = (% Change in Revenue) - (% Change in Price)

If Revenue Elasticity > 0: Demand is inelastic
If Revenue Elasticity < 0: Demand is elastic
```

---

## 3. Survey-Based Methods

### Van Westendorp Price Sensitivity Meter (PSM)

#### Overview
A survey technique that identifies acceptable price ranges by asking four price perception questions.

#### The Four Questions

1. **Too Cheap (TC)**: At what price would this be so cheap that you'd question its quality?
2. **Cheap/Bargain (C)**: At what price would you consider this a bargain?
3. **Expensive (E)**: At what price would you consider this getting expensive but still consider it?
4. **Too Expensive (TE)**: At what price would this be too expensive to consider?

#### Survey Design

```markdown
## Van Westendorp Survey Template

Product/Service: [Description with features and benefits]

For the following questions, please indicate a price in $[currency]:

1. At what price would [product] start to seem so inexpensive that you would question the quality?
   $________

2. At what price would you consider [product] a bargain—a great buy for the money?
   $________

3. At what price would [product] start to seem expensive, but you would still consider it?
   $________

4. At what price would [product] be too expensive for you to consider?
   $________

Demographic Questions:
- Company size: ________
- Industry: ________
- Role: ________
- Current spend on similar: $________
```

#### Analysis Method

1. Plot cumulative distributions for each question
2. Find intersection points:

| Intersection | Lines Crossing | Meaning |
|--------------|---------------|---------|
| Point of Marginal Cheapness (PMC) | TC and E | Lower bound of acceptable range |
| Point of Marginal Expensiveness (PME) | C and TE | Upper bound of acceptable range |
| Optimal Price Point (OPP) | TC and TE | Balance of "too cheap" and "too expensive" |
| Indifference Price Point (IPP) | C and E | Equal "bargain" and "expensive" perception |

#### Interpretation

```
Acceptable Price Range: PMC to PME
Optimal Price Point: OPP
Recommended Range: Between IPP and OPP

Example Results:
- PMC: $80
- IPP: $110
- OPP: $95
- PME: $150

Recommendation: Price between $95-$110
```

#### Limitations
- Best for unfamiliar products (no reference price)
- Stated preference may differ from actual behavior
- Works better for B2C than B2B
- Minimum sample: 100-200 respondents

---

### Gabor-Granger Method

#### Overview
Directly measures willingness to pay at specific price points by showing respondents a price and asking purchase intent.

#### Survey Design

**Monadic Design** (Each respondent sees one price):
```markdown
## Gabor-Granger Survey - Monadic

Product/Service: [Description]

At a price of $[PRICE], how likely would you be to purchase [product]?

○ Definitely would purchase
○ Probably would purchase
○ Might or might not purchase
○ Probably would not purchase
○ Definitely would not purchase
```

**Sequential Design** (Each respondent sees multiple prices):
```markdown
## Gabor-Granger Survey - Sequential

Product/Service: [Description]

[Start at middle price, branch up or down based on responses]

Q1: At $1,000/month, would you subscribe? [Yes/No]
- If Yes → Q2: At $1,500/month, would you subscribe? [Yes/No]
- If No → Q2: At $700/month, would you subscribe? [Yes/No]
[Continue until price threshold identified]
```

#### Analysis

Calculate purchase probability at each price point:

```
Price    | Would Buy | Probably Buy | Total (Top 2 Box)
$500     | 45%       | 30%          | 75%
$750     | 35%       | 25%          | 60%
$1,000   | 20%       | 20%          | 40%
$1,250   | 10%       | 15%          | 25%
$1,500   | 5%        | 10%          | 15%
```

Construct demand curve and calculate revenue optimization:

```
Price    | Demand (T2B) | Revenue Index
$500     | 75%          | $375 (500 × 0.75)
$750     | 60%          | $450 (750 × 0.60)
$1,000   | 40%          | $400 (1000 × 0.40)
$1,250   | 25%          | $313 (1250 × 0.25)
$1,500   | 15%          | $225 (1500 × 0.15)

Optimal Price: $750 (maximum revenue index)
```

#### Limitations
- Price points must be realistic
- Sequential design can anchor responses
- Stated intent differs from actual purchase

---

### Conjoint Analysis (Choice-Based)

#### Overview
Measures price sensitivity in context of product features, simulating real purchase decisions where customers trade off attributes.

#### Design Elements

**Attributes and Levels Example:**

| Attribute | Level 1 | Level 2 | Level 3 | Level 4 |
|-----------|---------|---------|---------|---------|
| Price/month | $500 | $1,000 | $1,500 | $2,000 |
| Support | Email only | Email + Chat | 24/7 Phone | Dedicated |
| SLA | 99.5% | 99.9% | 99.95% | 99.99% |
| Features | Basic | Standard | Advanced | Enterprise |

**Choice Task Example:**

```
Which managed service package would you choose?

Option A          | Option B          | Option C
------------------|-------------------|------------------
$1,000/month      | $1,500/month      | $2,000/month
Email + Chat      | 24/7 Phone        | Dedicated
99.9% SLA         | 99.9% SLA         | 99.99% SLA
Standard features | Standard features | Advanced features

○ Option A    ○ Option B    ○ Option C    ○ None
```

#### Design Parameters

| Parameter | Guideline | Rationale |
|-----------|-----------|-----------|
| Attributes | 4-6 maximum | Cognitive limit |
| Levels per attribute | 3-5 | Balance precision vs. complexity |
| Choice sets | 8-15 | Respondent fatigue |
| Alternatives per set | 3-4 | Realistic choice simulation |
| Sample size | 300+ | Hierarchical Bayes estimation |

#### Analysis Outputs

1. **Part-worth utilities**: Value of each attribute level
2. **Attribute importance**: Relative weight of each attribute
3. **Willingness to pay**: Price premium for feature improvements
4. **Market simulation**: Share prediction at different configurations

**Example Output:**

```
Attribute Importance:
- Price: 35%
- Support: 25%
- SLA: 22%
- Features: 18%

WTP for 24/7 Phone (vs. Email + Chat): $400/month
WTP for 99.99% SLA (vs. 99.9%): $250/month
WTP for Advanced Features (vs. Standard): $350/month

Price Elasticity by Segment:
- Enterprise: -0.4 (inelastic)
- Mid-market: -1.2 (elastic)
- SMB: -2.1 (highly elastic)
```

---

## 4. Regression-Based Methods

### Log-Log Regression

The standard approach for estimating price elasticity from historical data.

**Model Specification:**
```
ln(Q) = α + β₁ln(P) + β₂X₂ + β₃X₃ + ... + ε

Where:
- ln(Q) = Natural log of quantity/sales
- ln(P) = Natural log of price
- β₁ = Price elasticity coefficient
- X₂, X₃... = Control variables
```

**Interpretation:**
- β₁ directly equals elasticity (due to log-log form)
- If β₁ = -1.5, a 1% price increase leads to 1.5% quantity decrease

**Example Analysis:**

```python
# Pseudocode for elasticity estimation
import statsmodels.api as sm
import numpy as np

# Prepare data
data['ln_quantity'] = np.log(data['quantity'])
data['ln_price'] = np.log(data['price'])

# Control variables
X = data[['ln_price', 'marketing_spend', 'competitor_price', 'season_dummy']]
X = sm.add_constant(X)
y = data['ln_quantity']

# Fit model
model = sm.OLS(y, X).fit()
print(model.summary())

# Price elasticity = coefficient on ln_price
elasticity = model.params['ln_price']  # e.g., -1.2
```

### Panel Data Methods

When data spans multiple products/segments over time:

**Fixed Effects Model:**
```
ln(Qᵢₜ) = αᵢ + β₁ln(Pᵢₜ) + β₂Xᵢₜ + εᵢₜ

Where:
- αᵢ = Product/segment fixed effect
- i = Product/segment index
- t = Time index
```

**Advantages:**
- Controls for unobserved heterogeneity
- Exploits within-entity variation
- More robust elasticity estimates

### Machine Learning Approaches

For complex, non-linear elasticity patterns:

**XGBoost/Random Forest:**
- Captures non-linear price-demand relationships
- Handles interactions between variables
- Can estimate segment-specific elasticities

**Caution:**
- Requires careful feature engineering
- Risk of overfitting
- Less interpretable than regression

---

## 5. B2B-Specific Considerations

### Unique B2B Factors

| Factor | Impact on Elasticity | Consideration |
|--------|---------------------|---------------|
| Multiple decision makers | Lower elasticity | Rational, committee-based decisions |
| Switching costs | Lower elasticity | Integration, training, migration |
| Relationship value | Lower elasticity | Long-term partnership considerations |
| Budget cycles | Timing effects | Annual/quarterly budget constraints |
| Contract length | Lock-in effects | Multi-year agreements reduce sensitivity |
| Total Cost of Ownership | Beyond price | Implementation, support, maintenance |

### Adjusting Analysis for B2B

1. **Survey respondent selection**: Include all buying influences
2. **Price presentation**: Show total cost, not just unit price
3. **Comparison alternatives**: Include current state, not just competitors
4. **Time horizon**: Multi-year value consideration
5. **Segment granularity**: Elasticity varies significantly by segment

### Segment-Specific Elasticity

Typical B2B IT services elasticity patterns:

| Segment | Typical Elasticity | Characteristics |
|---------|-------------------|-----------------|
| Enterprise | -0.2 to -0.5 | Price secondary to capability/risk |
| Mid-market | -0.7 to -1.2 | Price important, balanced view |
| SMB | -1.5 to -2.5 | Price highly sensitive |
| Public Sector | -0.3 to -0.6 | Budget-constrained but inelastic within |

---

## 6. Practical Application

### Sample Size Requirements

| Method | Minimum Sample | Recommended Sample |
|--------|---------------|-------------------|
| Van Westendorp | 100 | 200+ |
| Gabor-Granger (monadic) | 50 per price point | 100 per price point |
| Gabor-Granger (sequential) | 150 | 300+ |
| Conjoint (CBC) | 200 | 400+ |
| Regression | 100 observations | 500+ observations |

### Method Selection Guide

```
Has historical price/sales data?
├─ Yes → Regression analysis
│        └─ Multiple products/segments? → Panel data methods
└─ No → Survey-based methods
        ├─ New product, price range unknown → Van Westendorp
        ├─ Existing product, testing specific prices → Gabor-Granger
        └─ Feature-price tradeoffs important → Conjoint
```

### Common Pitfalls

1. **Ignoring segments**: Aggregate elasticity masks segment differences
2. **Static analysis**: Elasticity changes over time and conditions
3. **Stated vs. revealed**: Survey responses ≠ actual behavior
4. **Competitive response**: Doesn't account for competitor reaction
5. **Non-price factors**: Other variables affect demand

---

## 7. Revenue Optimization

### Price Optimization Formula

For a single product with known elasticity:

```
Optimal Price = Marginal Cost × (E / (E + 1))

Where E = |Price Elasticity| (absolute value)
```

**Example:**
```
Marginal Cost: $50
Elasticity: -2.0

Optimal Price = $50 × (2.0 / (2.0 + 1))
              = $50 × (2.0 / 3.0)
              = $50 × 0.667
              = $33.33

Wait—this is below cost! The formula gives the theoretical optimum.
For inelastic demand, price can be higher.

If Elasticity: -0.5
Optimal Price = $50 × (0.5 / (0.5 + 1))
              = $50 × (0.5 / 1.5)
              = $50 × 0.333
              = $16.67

This formula only works for E < -1 (elastic demand).
For inelastic demand, pricing is less constrained by demand sensitivity.
```

### Revenue Curve Analysis

Build revenue curve from demand estimates:

```
| Price | Demand | Revenue | Margin | Profit |
|-------|--------|---------|--------|--------|
| $80   | 1,200  | $96,000 | $30    | $36,000|
| $100  | 1,000  | $100,000| $50    | $50,000|
| $120  | 800    | $96,000 | $70    | $56,000|
| $140  | 600    | $84,000 | $90    | $54,000|
| $160  | 400    | $64,000 | $110   | $44,000|

Revenue-maximizing price: $100
Profit-maximizing price: $120
```

### Sensitivity Analysis

Test elasticity uncertainty:

```
| Scenario | Elasticity | Optimal Price | Revenue | Profit |
|----------|------------|---------------|---------|--------|
| Pessimistic | -1.8 | $100 | $100K | $50K |
| Base Case | -1.2 | $120 | $96K | $56K |
| Optimistic | -0.8 | $140 | $84K | $54K |
```

---

## 8. Reporting Template

```markdown
## Price Elasticity Analysis Report

### Executive Summary
- Product/Service: [Name]
- Analysis Method: [Method used]
- Key Finding: Demand is [elastic/inelastic] with elasticity of [value]
- Optimal Price Range: $[low] - $[high]
- Revenue Impact: [X]% revenue change for 10% price increase

### Methodology
- Method: [Van Westendorp/Gabor-Granger/Conjoint/Regression]
- Sample Size: [N]
- Data Period: [Dates]
- Segments Analyzed: [List]

### Key Findings

#### Overall Elasticity
- Point estimate: [Value]
- 95% Confidence Interval: [Range]
- Interpretation: [Elastic/Inelastic/Unit Elastic]

#### Segment Analysis
| Segment | Elasticity | Optimal Price | Notes |
|---------|------------|---------------|-------|
| [Seg 1] | [Value] | $[Price] | [Notes] |
| [Seg 2] | [Value] | $[Price] | [Notes] |

#### Revenue Optimization
| Price Point | Expected Demand | Revenue | Profit |
|-------------|-----------------|---------|--------|
| $[Price 1] | [Demand] | $[Rev] | $[Prof] |
| $[Price 2] | [Demand] | $[Rev] | $[Prof] |

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

### Limitations
- [Limitation 1]
- [Limitation 2]

### Appendix
- Survey instrument
- Statistical output
- Raw data summary
```

---

## Summary

| Method | Best For | Data Required | Accuracy | Cost |
|--------|----------|---------------|----------|------|
| Van Westendorp | New products | Survey (100+) | Medium | Low |
| Gabor-Granger | Price point testing | Survey (150+) | Medium | Medium |
| Conjoint | Feature-price tradeoffs | Survey (300+) | High | High |
| Regression | Historical analysis | Transaction data | High | Low |
| Panel Data | Multi-product | Panel data | High | Low |
