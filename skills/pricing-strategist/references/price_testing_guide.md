# Price Testing Guide

## Overview

Price testing uses controlled experiments to validate pricing decisions before full-scale implementation. This guide covers A/B testing, conjoint analysis, and other experimental methodologies for pricing research.

---

## 1. When to Test Pricing

### Test vs. Don't Test Decision

| Situation | Test Recommended | Rationale |
|-----------|------------------|-----------|
| New product launch | Yes | No baseline, high uncertainty |
| Major price change (>15%) | Yes | Significant revenue risk |
| New market entry | Yes | Different customer behavior |
| Tier restructuring | Yes | Complex customer impact |
| Minor adjustment (<5%) | Maybe | Lower risk, may not justify cost |
| Competitive response | Maybe | Time constraints may limit testing |
| Promotional pricing | Yes | Measure actual conversion impact |

### Testing Limitations

- **Time pressure**: Testing takes weeks/months
- **Sample size**: B2B may have limited customer base
- **Competitive visibility**: Public tests reveal strategy
- **Customer confusion**: Multiple prices can cause issues
- **Revenue risk**: Test prices may be suboptimal

---

## 2. A/B Testing for Pricing

### Basic Framework

```
Population → Random Assignment → Treatment (Price B) → Measure Outcomes
                              → Control (Price A)  → Measure Outcomes

Compare: Conversion, Revenue, ARPU, Customer Satisfaction
```

### Test Design Checklist

- [ ] Define clear hypothesis
- [ ] Select primary metric
- [ ] Calculate required sample size
- [ ] Determine test duration
- [ ] Set up random assignment
- [ ] Plan statistical analysis
- [ ] Define decision criteria
- [ ] Prepare rollback plan

### Hypothesis Formulation

**Structure:**
```
If we [change price from X to Y], then [metric] will [increase/decrease] by [amount], because [reasoning].
```

**Examples:**
```
H1: If we increase the Professional tier price from $99 to $119/month,
    conversion rate will decrease by no more than 10%,
    because our value proposition exceeds the price increase.

H0: Conversion rate will decrease by more than 10%.
```

### Sample Size Calculation

**Formula for conversion rate:**
```
n = 2 × [(Zα/2 + Zβ)² × p(1-p)] / (p1 - p2)²

Where:
- n = Sample size per group
- Zα/2 = Z-score for significance level (1.96 for 95%)
- Zβ = Z-score for power (0.84 for 80%)
- p = Pooled conversion rate
- p1, p2 = Conversion rates in each group
```

**Simplified table (80% power, 95% confidence):**

| Baseline Rate | Detectable Difference | Sample/Group |
|---------------|----------------------|--------------|
| 5% | 1 percentage point | 3,800 |
| 5% | 2 percentage points | 950 |
| 10% | 2 percentage points | 2,100 |
| 10% | 5 percentage points | 340 |
| 20% | 5 percentage points | 620 |
| 20% | 10 percentage points | 160 |

### Test Duration

**Minimum duration considerations:**
1. Achieve required sample size
2. Cover at least 1-2 business cycles
3. Account for day-of-week effects
4. Consider seasonal factors

**Formula:**
```
Duration = Sample Size Needed / (Daily Visitors × Allocation %)
```

**Example:**
```
Need: 1,000 per group
Daily visitors: 200
Allocation: 50% to each group

Duration = 1,000 / (200 × 0.5) = 10 days minimum
Recommended: 2-4 weeks to capture variation
```

### Randomization Methods

| Method | Description | Best For |
|--------|-------------|----------|
| User-based | Same user always sees same price | Returning visitors |
| Session-based | Randomize each session | Anonymous users |
| Cohort-based | New users get new price | Long-term effects |
| Geographic | Different prices by region | Regional testing |

### Statistical Analysis

**For conversion rates (binary outcome):**
```
Test: Chi-square or Z-test for proportions

H0: p_A = p_B (no difference)
H1: p_A ≠ p_B (difference exists)

Calculate:
- Conversion rate A: conversions_A / visitors_A
- Conversion rate B: conversions_B / visitors_B
- Z-statistic and p-value
- 95% confidence interval for difference

Decision: If p-value < 0.05, reject H0
```

**For revenue/ARPU (continuous outcome):**
```
Test: Two-sample t-test or Mann-Whitney U

Calculate:
- Mean revenue A and B
- t-statistic and p-value
- 95% confidence interval for difference
```

### Results Interpretation

```markdown
## A/B Test Results Summary

### Test Details
- Test Name: [Name]
- Duration: [Start] to [End]
- Sample: A=[N], B=[N]

### Primary Metric: Conversion Rate
| Variant | Conversions | Visitors | Rate | 95% CI |
|---------|-------------|----------|------|--------|
| Control (A) | [N] | [N] | [%] | [%, %] |
| Treatment (B) | [N] | [N] | [%] | [%, %] |

- Relative Difference: [%]
- p-value: [value]
- Significant: [Yes/No]

### Revenue Impact
| Variant | Total Revenue | ARPU | RPV |
|---------|--------------|------|-----|
| Control | $[amount] | $[amount] | $[amount] |
| Treatment | $[amount] | $[amount] | $[amount] |

### Decision
[Recommend implementation / Do not recommend / Need more data]

### Rationale
[Explanation of decision based on results]
```

---

## 3. Choice-Based Conjoint (CBC)

### Overview

CBC presents respondents with sets of product configurations (including price) and asks them to choose their preferred option, simulating real purchase decisions.

### Design Steps

#### Step 1: Define Attributes and Levels

**Guidelines:**
- 4-6 attributes maximum
- 3-5 levels per attribute
- Include "price" as key attribute
- Levels should be realistic and actionable

**Example - Managed Services:**

| Attribute | Level 1 | Level 2 | Level 3 | Level 4 |
|-----------|---------|---------|---------|---------|
| Price/Month | $500 | $1,000 | $1,500 | $2,000 |
| Support | Email Only | Email + Chat | Business Hours Phone | 24/7 Phone |
| Response Time | 4 hours | 2 hours | 1 hour | 30 minutes |
| Account Management | Self-Service | Shared | Dedicated Part-Time | Dedicated Full-Time |
| Included Users | 25 | 50 | 100 | Unlimited |

#### Step 2: Create Choice Tasks

**Task structure:**
- Show 3-4 product options per task
- Each option is a combination of attribute levels
- Include "None of these" option (optional but recommended)
- Use experimental design to ensure efficient estimation

**Example choice task:**

```
Which managed services package would you choose?

                    Option A      Option B      Option C
Price/Month         $1,000        $1,500        $2,000
Support             Email + Chat  Business Phone 24/7 Phone
Response Time       4 hours       1 hour        30 minutes
Account Mgmt        Shared        Dedicated PT  Dedicated FT
Users               50            100           Unlimited

○ Option A    ○ Option B    ○ Option C    ○ None of these
```

#### Step 3: Determine Number of Tasks

| Factor | Fewer Tasks | More Tasks |
|--------|-------------|------------|
| Respondent burden | Lower | Higher |
| Estimation precision | Lower | Higher |
| Completion rate | Higher | Lower |
| Recommended | 8-10 | 15-20 |

**Formula for minimum tasks:**
```
Minimum tasks ≥ (Levels × Attributes) / (Options per task - 1)
```

#### Step 4: Sample Size

**Minimum sample:**
```
n ≥ (500 × max_levels) / (tasks × options)
```

**Practical guideline:**
- Aggregate analysis: 200-300 respondents
- Segment analysis: 150-200 per segment
- Individual-level (HB): 300-500 respondents

### Analysis Methods

#### Hierarchical Bayes (HB) Estimation

**Outputs:**
1. **Part-worth utilities**: Value of each attribute level
2. **Individual-level utilities**: Personalized preferences
3. **Attribute importance**: Relative weight calculation

**Attribute Importance Calculation:**
```
Importance_i = (Max Utility_i - Min Utility_i) / Sum of all ranges × 100%
```

**Example output:**

```
Attribute Importance:
- Price: 35%
- Support: 25%
- Response Time: 18%
- Account Management: 15%
- Users: 7%

Part-Worth Utilities (Price):
- $500: +1.2
- $1,000: +0.4
- $1,500: -0.3
- $2,000: -1.3
```

#### Willingness to Pay (WTP)

**Formula:**
```
WTP for upgrade = (Utility_upgrade - Utility_base) / Price_coefficient × (-1)
```

**Example:**
```
Upgrade: From "Email Only" to "24/7 Phone"
Utility difference: 1.5 - (-0.5) = 2.0

Price coefficient: -0.0015 (per dollar)

WTP = 2.0 / 0.0015 = $1,333

Interpretation: Customers will pay up to $1,333 more per month
for 24/7 phone support vs. email only.
```

### Market Simulation

**Share of Preference Calculation:**

Using logit model:
```
Share_i = exp(Utility_i) / Σ exp(Utility_j)
```

**Example simulation:**

| Scenario | Our Product | Competitor A | Competitor B | Our Share |
|----------|-------------|--------------|--------------|-----------|
| Current | $1,000, Basic | $1,200, Standard | $800, Basic | 35% |
| Price +20% | $1,200, Basic | $1,200, Standard | $800, Basic | 28% |
| Upgrade Support | $1,000, Premium | $1,200, Standard | $800, Basic | 42% |
| Price + Upgrade | $1,200, Premium | $1,200, Standard | $800, Basic | 38% |

---

## 4. Van Westendorp Price Sensitivity Meter

### Application in Testing

Use Van Westendorp to:
- Establish price range before A/B test
- Validate price points for Gabor-Granger
- Identify psychological price barriers

### Enhanced Van Westendorp with Newton-Miller-Smith

Add purchase intent questions:

1. **Standard 4 questions** (too cheap, bargain, expensive, too expensive)
2. **At [optimal price], how likely would you buy?** (5-point scale)
3. **At [expensive price], how likely would you buy?** (5-point scale)

**Output:**
- Standard Van Westendorp intersections
- Revenue-optimal price (accounting for purchase probability)

---

## 5. Experimental Design Best Practices

### Control Variables

| Variable | Control Method |
|----------|---------------|
| Seasonality | Run test over comparable period |
| Day of week | Include multiple weeks |
| Marketing | Keep campaigns constant |
| Product changes | Freeze features during test |
| Competitive | Monitor competitor pricing |

### Validity Threats

| Threat | Description | Mitigation |
|--------|-------------|------------|
| Selection bias | Non-random assignment | True randomization |
| History | External events | Short test, control group |
| Maturation | Natural changes | Control group comparison |
| Novelty | Response to change itself | Allow settling period |
| Contamination | Customers see both prices | User-level randomization |

### Ethical Considerations

1. **Price discrimination**: Ensure legal compliance
2. **Customer perception**: Consider brand impact if discovered
3. **Fairness**: Consider if price difference is justifiable
4. **Refund policy**: Be prepared to honor lower price if discovered
5. **Transparency**: Consider disclosure requirements

---

## 6. Implementation Recommendations

### Pre-Test Preparation

- [ ] Define success metrics and decision criteria
- [ ] Calculate sample size requirements
- [ ] Set up tracking and analytics
- [ ] Brief stakeholders on test design
- [ ] Prepare rollback procedure
- [ ] Document current baseline metrics

### During Test

- [ ] Monitor sample sizes daily
- [ ] Check for data quality issues
- [ ] Watch for external factors
- [ ] Avoid peeking at results prematurely
- [ ] Document any anomalies

### Post-Test Actions

- [ ] Wait for full duration before analysis
- [ ] Perform planned statistical tests
- [ ] Calculate confidence intervals
- [ ] Segment analysis (if powered)
- [ ] Document learnings
- [ ] Make implementation decision
- [ ] Plan rollout (if positive)

### Decision Framework

```
Statistical Significance + Practical Significance = Decision

If p < 0.05 AND effect size meaningful:
  → Implement winning variant

If p < 0.05 BUT effect size small:
  → Consider business context, may not be worth change

If p ≥ 0.05:
  → No significant difference detected
  → Consider: Was test powered properly?
  → May default to control or run longer test
```

---

## 7. Reporting Template

```markdown
## Price Test Results Report

### Executive Summary
- Test: [Name]
- Objective: [Objective]
- Result: [Summary - positive/negative/inconclusive]
- Recommendation: [Action]

### Test Design
- Methodology: [A/B / Conjoint / Other]
- Duration: [Dates]
- Sample: Control [N], Treatment [N]
- Primary Metric: [Metric]
- Secondary Metrics: [List]

### Results

#### Primary Metric
| Variant | Value | 95% CI | vs. Control |
|---------|-------|--------|-------------|
| Control | [X] | [Y, Z] | - |
| Treatment | [X] | [Y, Z] | [+/-X%] |

Statistical Significance: p = [value]
Practically Significant: [Yes/No]

#### Revenue Impact
- Control revenue/user: $[X]
- Treatment revenue/user: $[X]
- Projected annual impact: $[X]

#### Secondary Metrics
[Table of secondary metrics]

### Segmentation Analysis
[If applicable, results by segment]

### Recommendation
[Implement / Do not implement / Extend test]

### Rationale
[Detailed explanation]

### Next Steps
1. [Step 1]
2. [Step 2]

### Appendix
- Statistical details
- Raw data summary
- Test configuration
```

---

## Summary

| Method | Best For | Sample Needed | Duration | Cost |
|--------|----------|---------------|----------|------|
| A/B Test | Specific price comparison | 1,000+ per variant | 2-4 weeks | Medium |
| Conjoint | Multi-attribute tradeoffs | 300-500 | Survey-based | High |
| Van Westendorp | Price range discovery | 100-200 | Survey-based | Low |
| Gabor-Granger | Price point testing | 150+ per point | Survey-based | Medium |

### Key Principles

1. **Test before committing**: Major pricing changes deserve validation
2. **Power properly**: Underpowered tests waste resources
3. **Patience pays**: Don't peek early; wait for full sample
4. **Segment when possible**: Aggregate hides differences
5. **Consider context**: Statistical significance ≠ business significance
