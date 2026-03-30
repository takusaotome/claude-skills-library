---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    background-color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  h1 {
    color: #1a365d;
    border-bottom: 3px solid #2b6cb0;
    padding-bottom: 10px;
  }
  h2 {
    color: #2b6cb0;
  }
  table {
    font-size: 0.8em;
    margin: 0 auto;
  }
  th {
    background-color: #2b6cb0;
    color: white;
  }
  .highlight {
    background-color: #bee3f8;
    padding: 5px 15px;
    border-radius: 5px;
  }
  .metric-box {
    background-color: #e2e8f0;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
  }
  .green { color: #22543d; }
  .red { color: #c53030; }
  .blue { color: #2b6cb0; }
---

# Purchase Request: {{PRODUCT_NAME}}

## {{DEPARTMENT}} | {{DATE}}

**Request ID:** {{REQUEST_ID}}
**Requester:** {{REQUESTER_NAME}}

---

# Executive Summary

## Request Overview

- **Product:** {{PRODUCT_NAME}}
- **Vendor:** {{VENDOR_NAME}}
- **Quantity:** {{QUANTITY}}
- **Total Cost:** ${{TOTAL_COST}}

## Key Metrics

| ROI | Payback Period | NPV |
|:---:|:---:|:---:|
| **{{ROI_PERCENT}}%** | **{{PAYBACK_MONTHS}} months** | **${{NPV}}** |

---

# Business Justification

## Problem Statement

{{PROBLEM_STATEMENT}}

## Proposed Solution

{{SOLUTION_DESCRIPTION}}

## Impact of Not Purchasing

{{IMPACT_OF_DELAY}}

---

# Cost Analysis

## Total Cost of Ownership ({{TCO_YEARS}} Years)

| Cost Category | Amount |
|---------------|-------:|
| Initial Purchase | ${{INITIAL_COST}} |
| Annual Operating | ${{ANNUAL_OPERATING}} |
| Training | ${{TRAINING_COST}} |
| **Total TCO** | **${{TOTAL_TCO}}** |

---

# Benefit Analysis

## Quantified Benefits

| Benefit | Annual Value |
|---------|-------------:|
| {{BENEFIT_1_NAME}} | ${{BENEFIT_1_VALUE}} |
| {{BENEFIT_2_NAME}} | ${{BENEFIT_2_VALUE}} |
| {{BENEFIT_3_NAME}} | ${{BENEFIT_3_VALUE}} |
| **Total Annual Benefit** | **${{TOTAL_ANNUAL_BENEFIT}}** |

---

# Financial Analysis

## ROI Calculation

```
ROI = (Total Benefits - Total Costs) / Total Costs × 100
    = (${{TOTAL_BENEFITS}} - ${{TOTAL_COSTS}}) / ${{TOTAL_COSTS}} × 100
    = {{ROI_PERCENT}}%
```

## Payback Period

```
Payback = Initial Cost / Monthly Benefit
        = ${{INITIAL_COST}} / ${{MONTHLY_BENEFIT}}
        = {{PAYBACK_MONTHS}} months
```

---

# Vendor Comparison

## Evaluation Matrix

| Criterion | Weight | {{VENDOR_1}} | {{VENDOR_2}} | {{VENDOR_3}} |
|-----------|:------:|:------------:|:------------:|:------------:|
| Price | 30% | {{V1_PRICE}} | {{V2_PRICE}} | {{V3_PRICE}} |
| Quality | 25% | {{V1_QUALITY}} | {{V2_QUALITY}} | {{V3_QUALITY}} |
| Support | 20% | {{V1_SUPPORT}} | {{V2_SUPPORT}} | {{V3_SUPPORT}} |
| Warranty | 15% | {{V1_WARRANTY}} | {{V2_WARRANTY}} | {{V3_WARRANTY}} |
| Delivery | 10% | {{V1_DELIVERY}} | {{V2_DELIVERY}} | {{V3_DELIVERY}} |
| **Total** | | **{{V1_TOTAL}}** | **{{V2_TOTAL}}** | **{{V3_TOTAL}}** |

---

# Implementation Timeline

## Project Milestones

| Phase | Timeline | Status |
|-------|----------|--------|
| Approval | Week 1 | Pending |
| Procurement | Week 2-3 | - |
| Delivery | Week 4 | - |
| Installation | Week 5 | - |
| Training | Week 6 | - |
| Go-Live | Week 7 | - |

---

# Risk Assessment

## Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|:-----------:|:------:|------------|
| {{RISK_1}} | {{PROB_1}} | {{IMPACT_1}} | {{MITIGATION_1}} |
| {{RISK_2}} | {{PROB_2}} | {{IMPACT_2}} | {{MITIGATION_2}} |
| {{RISK_3}} | {{PROB_3}} | {{IMPACT_3}} | {{MITIGATION_3}} |

---

# Alternatives Considered

## Options Evaluated

| Option | Cost | Pros | Cons |
|--------|------|------|------|
| **Recommended** | ${{OPT1_COST}} | {{OPT1_PROS}} | {{OPT1_CONS}} |
| Alternative 1 | ${{OPT2_COST}} | {{OPT2_PROS}} | {{OPT2_CONS}} |
| Alternative 2 | ${{OPT3_COST}} | {{OPT3_PROS}} | {{OPT3_CONS}} |
| Do Nothing | $0 | No cost | {{STATUS_QUO_CONS}} |

---

# Budget Information

## Funding Source

- **Budget Code:** {{BUDGET_CODE}}
- **Fiscal Year:** {{FISCAL_YEAR}}
- **Available Budget:** ${{AVAILABLE_BUDGET}}
- **Requested Amount:** ${{TOTAL_COST}}
- **Remaining After:** ${{REMAINING_BUDGET}}

---

# Approval Request

## Recommendation

<div class="highlight">

**Approve the purchase of {{PRODUCT_NAME}} for ${{TOTAL_COST}}**

</div>

## Approval Routing

| Approver | Role | Status |
|----------|------|--------|
| {{APPROVER_1}} | {{ROLE_1}} | Pending |
| {{APPROVER_2}} | {{ROLE_2}} | Pending |
| {{APPROVER_3}} | {{ROLE_3}} | Pending |

---

# Questions?

## Contact Information

**Requester:** {{REQUESTER_NAME}}
**Email:** {{REQUESTER_EMAIL}}
**Phone:** {{REQUESTER_PHONE}}

**Supporting Documents:**
- Vendor Quote(s)
- Product Specifications
- Cost-Benefit Analysis (detailed)

---

# Appendix: Supporting Data

## Additional Financial Details

| Metric | Value |
|--------|-------|
| Discount Rate Used | {{DISCOUNT_RATE}}% |
| Useful Life | {{USEFUL_LIFE}} years |
| Salvage Value | ${{SALVAGE_VALUE}} |
| Internal Rate of Return | {{IRR}}% |

## Assumptions

1. {{ASSUMPTION_1}}
2. {{ASSUMPTION_2}}
3. {{ASSUMPTION_3}}
