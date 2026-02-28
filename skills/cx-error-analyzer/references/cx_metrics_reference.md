# CX Metrics Reference

## Overview

This reference provides the metrics framework, formulas, benchmarks, and calculation methods for quantifying the business impact of error experiences. Use this guide to translate CX evaluation scores into tangible business metrics and to estimate the ROI of error UX improvements.

---

## Core CX Metrics and Error Correlation

### CES (Customer Effort Score)

**Definition:** Measures the effort a customer must expend to accomplish a task or resolve an issue. Typically measured on a 1-7 scale ("How easy was it to handle your request?").

**Error Correlation:**
- Each error encountered during a task increases perceived effort by 0.5-1.5 CES points
- Unrecoverable errors increase effort by 2.0+ CES points
- Poor error messages add 0.3-0.8 CES points compared to helpful messages
- Errors during checkout/submission have 2x the CES impact of discovery-stage errors

**CES Impact Estimation Formula:**
```
CES_Impact = Base_CES + SUM(Error_CES_Penalties)

Error_CES_Penalty = CX_Score * CES_Multiplier

CES_Multiplier by Journey Stage:
  Discovery:  0.15
  Onboarding: 0.25
  Core Task:  0.30
  Checkout:   0.40
  Support:    0.35
```

**Industry Benchmarks:**
| CES Score | Interpretation |
|-----------|----------------|
| 1.0 - 2.0 | Excellent (very low effort) |
| 2.1 - 3.5 | Good |
| 3.6 - 5.0 | Needs improvement |
| 5.1 - 7.0 | Poor (high effort, churn risk) |

### CSAT (Customer Satisfaction Score)

**Definition:** Measures overall satisfaction, typically on a 1-5 scale ("How satisfied are you with your experience?").

**Error Impact on CSAT:**
- Users who encounter 0 errors: Average CSAT 4.2
- Users who encounter 1 error (well-handled): Average CSAT 3.6
- Users who encounter 1 error (poorly handled): Average CSAT 2.8
- Users who encounter 2+ errors: Average CSAT 2.1

**CSAT Impact Estimation Formula:**
```
CSAT_Impact = -0.3 * Number_of_Errors - 0.2 * Average_CX_Score

Adjusted_CSAT = Base_CSAT + CSAT_Impact
(floor at 1.0)
```

**CSAT Benchmarks by Industry:**
| Industry | Top Quartile | Median | Bottom Quartile |
|----------|-------------|--------|-----------------|
| SaaS | 4.3+ | 3.8 | 3.2 |
| E-Commerce | 4.1+ | 3.6 | 3.0 |
| Financial Services | 3.9+ | 3.4 | 2.8 |
| Healthcare | 3.8+ | 3.3 | 2.7 |
| Telecommunications | 3.5+ | 3.0 | 2.4 |

### NPS (Net Promoter Score)

**Definition:** Measures likelihood to recommend on a 0-10 scale. NPS = %Promoters (9-10) - %Detractors (0-6).

**Error Impact on NPS:**
- A single critical error experience (CX Score 4.0+) shifts a user from Promoter to Passive or Detractor
- Poorly handled errors are the #2 driver of Detractor scores (after product reliability)
- Well-handled error recovery can create "service recovery paradox" -- higher loyalty than no-error baseline

**NPS Impact Estimation:**
```
NPS_Shift per Critical Error (CX Score 4.0+):
  Per 1% of users affected: NPS decreases by 2-4 points

NPS_Shift per Significant Error (CX Score 3.0-3.9):
  Per 1% of users affected: NPS decreases by 0.5-1.5 points
```

---

## Support Ticket Cost Analysis

### Cost Per Ticket Calculation

```
Cost_Per_Ticket = Average_Handling_Time (minutes) * Cost_Per_Minute

Cost_Per_Minute = (Annual_Support_Salary + Benefits + Overhead) / (Working_Minutes_Per_Year)
```

**Typical Cost Per Ticket by Tier:**

| Support Tier | Avg Handling Time | Cost Per Ticket (USD) |
|-------------|-------------------|-----------------------|
| Self-Service (FAQ/KB) | 3-5 min user time | $0.10 - $0.50 |
| Tier 1 (Chat/Email) | 8-15 min | $5 - $15 |
| Tier 2 (Technical) | 20-45 min | $15 - $40 |
| Tier 3 (Engineering) | 60-120+ min | $50 - $200 |
| Phone Support | 10-25 min | $10 - $30 |

### Error-Driven Support Volume Estimation

```
Monthly_Tickets_Per_Error = Monthly_Error_Occurrences * Contact_Rate

Contact_Rate by CX Score Tier:
  Critical (4.0-5.0):    15-30% of affected users contact support
  Significant (3.0-3.9):  5-15% of affected users contact support
  Moderate (2.0-2.9):     1-5% of affected users contact support
  Minor (1.0-1.9):       <1% of affected users contact support
```

### Annual Support Cost Per Error Scenario

```
Annual_Support_Cost = Monthly_Tickets * 12 * Avg_Cost_Per_Ticket

Example:
  Error occurs 500 times/month
  CX Score: 4.2 (Critical) → Contact Rate: 20%
  Monthly tickets: 500 * 0.20 = 100 tickets
  Avg handling: Tier 1 (12 min) = $10/ticket
  Annual cost: 100 * 12 * $10 = $12,000/year
```

---

## Customer Churn Risk Analysis

### Churn Probability by Error Severity

| CX Score Tier | Single Occurrence Churn Risk | Repeated Occurrence Churn Risk |
|---------------|-----------------------------|---------------------------------|
| Critical (4.0-5.0) | 5-15% | 25-40% |
| Significant (3.0-3.9) | 2-5% | 10-20% |
| Moderate (2.0-2.9) | 0.5-2% | 3-8% |
| Minor (1.0-1.9) | <0.5% | 1-3% |

### Churn Revenue Impact

```
Annual_Churn_Revenue_Risk = Affected_Users * Churn_Probability * Average_Customer_LTV

Example:
  Affected users per year: 5,000
  CX Score: 3.5 (Significant) → Churn Risk: 3%
  Average Customer LTV: $500
  Annual churn revenue risk: 5,000 * 0.03 * $500 = $75,000/year
```

### Churn Risk Amplifiers

- **New users** (first 30 days): Churn risk is 2-3x higher
- **Users on trial/free tier**: Churn risk is 3-5x higher (lower switching cost)
- **Errors during onboarding**: Churn risk is 2x higher than during established usage
- **Repeated errors** (same error 3+ times): Churn risk compounds by 1.5x per additional occurrence
- **Errors with financial impact**: Churn risk is 2x higher

---

## Error Rate Benchmarks by Industry

### Acceptable Error Rates

| Metric | Excellent | Good | Needs Improvement | Poor |
|--------|-----------|------|-------------------|------|
| Overall error rate (% of requests) | <0.1% | 0.1-0.5% | 0.5-2% | >2% |
| Client-side error rate | <0.5% | 0.5-1% | 1-3% | >3% |
| Checkout error rate | <0.5% | 0.5-1.5% | 1.5-3% | >3% |
| API error rate (5xx) | <0.01% | 0.01-0.1% | 0.1-0.5% | >0.5% |
| Login failure rate | <1% | 1-3% | 3-5% | >5% |

### Industry-Specific Benchmarks

| Industry | Acceptable Error Rate | Critical Threshold | Notes |
|----------|----------------------|--------------------|-------|
| Financial Services | <0.05% | >0.2% | Regulatory requirements, high trust sensitivity |
| E-Commerce | <0.3% | >1% | Direct revenue impact per error |
| SaaS (B2B) | <0.1% | >0.5% | Enterprise SLA requirements |
| Healthcare | <0.05% | >0.1% | Patient safety, regulatory compliance |
| Media/Content | <1% | >3% | Lower direct impact but affects engagement |
| Gaming | <0.5% | >2% | User expectation varies by game type |

---

## ROI Calculation for Error UX Improvements

### ROI Formula

```
ROI = (Total_Annual_Benefit - Improvement_Cost) / Improvement_Cost * 100

Total_Annual_Benefit = Reduced_Support_Cost + Prevented_Churn_Revenue + Increased_Conversion_Revenue
```

### Benefit Category 1: Reduced Support Cost

```
Reduced_Support_Cost = Current_Annual_Tickets * Expected_Reduction_Rate * Cost_Per_Ticket

Expected_Reduction_Rate by Improvement Type:
  Improved error message only:           20-40% reduction in tickets for that error
  Improved message + recovery flow:      40-60% reduction
  Inline validation (prevent error):     70-90% reduction
  Auto-recovery implementation:          80-95% reduction
```

### Benefit Category 2: Prevented Churn Revenue

```
Prevented_Churn_Revenue = Affected_Users * Churn_Reduction * Average_LTV

Churn_Reduction by Improvement Type:
  Improved error message only:           10-20% of error-driven churn prevented
  Improved message + recovery flow:      30-50% of error-driven churn prevented
  Full error experience redesign:        50-70% of error-driven churn prevented
```

### Benefit Category 3: Increased Conversion Revenue

```
Increased_Conversion_Revenue = Monthly_Affected_Sessions * Conversion_Recovery_Rate * Avg_Order_Value * 12

Conversion_Recovery_Rate:
  Checkout error fix:                    30-50% of abandoned sessions recovered
  Onboarding error fix:                  20-40% of drop-offs recovered
  Search/discovery error fix:            10-25% of lost sessions recovered
```

### Implementation Cost Estimation

| Improvement Type | Typical Effort | Estimated Cost |
|-----------------|----------------|----------------|
| Error message text update | 0.5-1 day | $500 - $1,000 |
| Validation logic improvement | 1-3 days | $1,000 - $3,000 |
| Recovery flow redesign | 3-7 days | $3,000 - $7,000 |
| Auto-save implementation | 5-10 days | $5,000 - $10,000 |
| Error monitoring + alerting setup | 2-5 days | $2,000 - $5,000 |
| Full error experience redesign | 10-20 days | $10,000 - $20,000 |

### ROI Calculation Example

**Scenario: Improving checkout payment error (ERR-007)**

```
Current State:
  Monthly occurrences: 800
  CX Score: 4.3 (Critical)
  Contact rate: 25% → 200 tickets/month
  Avg ticket cost: $12 (Tier 1)
  Annual support cost: 200 * 12 * $12 = $28,800
  Affected users/year: 9,600
  Churn risk: 10% → 960 churned users
  Avg LTV: $300
  Annual churn cost: 960 * $300 = $288,000
  Checkout abandonment recovery: 800 * 0.35 * $75 * 12 = $252,000 potential

Improvement: Improved message + retry flow + alternative payment
  Cost: $5,000 (5 days engineering)
  Support reduction: 50% → saves $14,400/year
  Churn reduction: 40% → prevents 384 churns → saves $115,200/year
  Conversion recovery: 30% → recovers $75,600/year

ROI Calculation:
  Total annual benefit: $14,400 + $115,200 + $75,600 = $205,200
  ROI = ($205,200 - $5,000) / $5,000 * 100 = 4,004%
  Payback period: $5,000 / ($205,200 / 12) = 0.29 months ≈ 9 days
```

---

## Composite CX Health Score

### Calculating Organization-Level Error CX Health

```
Error_CX_Health = 100 - (Weighted_Average_CX_Score - 1) / 4 * 100

Scale: 0-100 (higher = healthier)
  90-100: Excellent error CX
  70-89:  Good error CX
  50-69:  Needs improvement
  30-49:  Poor error CX
  0-29:   Critical - immediate action required
```

### Tracking Improvement Over Time

**Key Metrics to Track Monthly:**

| Metric | Formula | Target Trend |
|--------|---------|--------------|
| Average CX Score | Mean of all error CX Scores | Decreasing |
| Critical Error Count | Count of errors with CX Score 4.0+ | Decreasing |
| Error Resolution Rate | Errors improved this period / Total errors | Increasing |
| Support Ticket Rate | Error-related tickets / Total error occurrences | Decreasing |
| Recovery Success Rate | Users who recovered / Users who encountered errors | Increasing |
| Error-Driven Churn | Churned users citing errors / Total churned users | Decreasing |

### Dashboard Recommendations

1. **Real-Time Error CX Dashboard**
   - Current error rates by category and severity
   - CX Score distribution (pie chart by tier)
   - Top 5 worst CX errors (sorted by weighted score)
   - Trend lines for key metrics

2. **Monthly CX Error Report**
   - Month-over-month comparison of CX Health Score
   - New errors identified and classified
   - Improvements completed and their measured impact
   - Next period priority queue

3. **Quarterly Business Impact Review**
   - Cumulative ROI of error improvements
   - Support cost savings achieved
   - Churn prevention impact
   - CSAT/NPS trends correlated with error improvements
