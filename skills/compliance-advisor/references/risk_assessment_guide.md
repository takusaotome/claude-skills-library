# Risk Assessment Guide

## Overview

This guide provides methodology for conducting risk assessments in the context of internal controls and compliance. It covers risk identification, evaluation, and response strategies.

## Risk Assessment Framework

### Definition

Risk assessment is the process of identifying, analyzing, and evaluating risks to achieving organizational objectives.

### Key Concepts

| Concept | Definition |
|---------|------------|
| **Inherent Risk** | Risk level before considering controls |
| **Residual Risk** | Risk level after considering controls |
| **Risk Appetite** | Amount of risk willing to accept |
| **Risk Tolerance** | Acceptable deviation from risk appetite |
| **Control Effectiveness** | Degree to which controls mitigate risk |

## Risk Identification

### Risk Categories

| Category | Description | Examples |
|----------|-------------|----------|
| Strategic | Threats to business model | Competition, market changes |
| Operational | Process and execution failures | Errors, inefficiency, fraud |
| Financial | Financial reporting errors | Misstatement, misclassification |
| Compliance | Regulatory violations | Non-compliance, penalties |
| Technology | IT and cyber threats | System failure, data breach |
| Reputational | Damage to reputation | Negative publicity, trust loss |

### Risk Identification Techniques

| Technique | Description | When to Use |
|-----------|-------------|-------------|
| Brainstorming | Group ideation | New processes, initial assessment |
| Interviews | SME discussions | Detailed understanding |
| Process Analysis | Walkthrough review | Process-level risks |
| Historical Review | Past incidents | Known risk areas |
| Scenario Analysis | "What if" exploration | Complex, emerging risks |
| Checklist | Structured review | Standard risk areas |

### Financial Reporting Risk Factors

| Factor | High Risk Indicators |
|--------|---------------------|
| Volume | High transaction volume |
| Complexity | Complex calculations, estimates |
| Judgment | Significant management judgment |
| Changes | New systems, processes, standards |
| Fraud | History or indicators of fraud |
| Related Parties | Significant related party transactions |

## Risk Evaluation

### Likelihood Assessment

| Rating | Level | Description | Frequency |
|--------|-------|-------------|-----------|
| 5 | Almost Certain | Expected to occur | > 1 per year |
| 4 | Likely | Will probably occur | 1 per 1-2 years |
| 3 | Possible | Might occur | 1 per 2-5 years |
| 2 | Unlikely | Could occur | 1 per 5-10 years |
| 1 | Rare | May occur in exceptional circumstances | < 1 per 10 years |

### Impact Assessment

| Rating | Level | Financial Impact | Operational Impact |
|--------|-------|-----------------|-------------------|
| 5 | Catastrophic | > $10M or > 10% of earnings | Complete process failure |
| 4 | Major | $1M - $10M | Significant disruption |
| 3 | Moderate | $100K - $1M | Noticeable impact |
| 2 | Minor | $10K - $100K | Minor inconvenience |
| 1 | Negligible | < $10K | No significant impact |

### Risk Matrix

```
Impact
    5 │  5   10   15   20   25
    4 │  4    8   12   16   20
    3 │  3    6    9   12   15
    2 │  2    4    6    8   10
    1 │  1    2    3    4    5
      └───────────────────────
         1    2    3    4    5   Likelihood
```

### Risk Rating Categories

| Score | Rating | Response Required |
|-------|--------|-------------------|
| 20-25 | Critical | Immediate action, escalate |
| 15-19 | High | Priority action required |
| 8-14 | Medium | Action plan needed |
| 4-7 | Low | Monitor, accept if appropriate |
| 1-3 | Very Low | Accept |

## Fraud Risk Assessment

### Fraud Triangle

```
                    INCENTIVE/PRESSURE
                          ▲
                         ╱ ╲
                        ╱   ╲
                       ╱     ╲
                      ╱       ╲
                     ╱  FRAUD  ╲
                    ╱           ╲
                   ╱             ╲
                  ▼───────────────▼
           OPPORTUNITY      RATIONALIZATION
```

### Fraud Risk Factors

| Factor | Examples |
|--------|----------|
| **Incentive/Pressure** | Financial targets, bonuses, personal debt |
| **Opportunity** | Weak controls, lack of oversight, system access |
| **Rationalization** | "I deserve it", "I'll pay it back", "Everyone does it" |

### Common Fraud Schemes

| Scheme | Process | Red Flags |
|--------|---------|-----------|
| Fictitious Sales | Revenue | Unusual sales patterns, credit memos |
| Ghost Employees | Payroll | No tax filings, same address |
| Kickbacks | Procurement | Sole source, premium pricing |
| Expense Fraud | Reimbursement | Duplicate receipts, round numbers |
| Inventory Theft | Inventory | Shrinkage, discrepancies |

### Fraud Risk Response

| Response | Description |
|----------|-------------|
| Preventive Controls | Segregation of duties, authorization |
| Detective Controls | Exception monitoring, reconciliation |
| Culture | Ethics training, whistleblower hotline |
| Oversight | Management review, internal audit |

## Control Effectiveness Assessment

### Control Rating Scale

| Rating | Score | Definition |
|--------|-------|------------|
| Effective | 3 | Operating as designed, no exceptions |
| Needs Improvement | 2 | Minor gaps, mostly operating |
| Ineffective | 1 | Significant gaps, not operating |
| Not Applicable | 0 | Control does not exist |

### Residual Risk Calculation

**Formula:** Residual Risk = Inherent Risk Rating × (1 - Control Effectiveness %)

| Inherent Risk | Control Effectiveness | Residual Risk |
|---------------|----------------------|---------------|
| High (20) | Effective (80%) | Low (4) |
| High (20) | Needs Improvement (50%) | Medium (10) |
| High (20) | Ineffective (20%) | High (16) |
| Medium (12) | Effective (80%) | Low (2.4) |

### Control Effectiveness Factors

| Factor | Assessment Questions |
|--------|---------------------|
| Design | Is control designed to address the risk? |
| Coverage | Does control cover all relevant transactions? |
| Timing | Is control performed at the right time? |
| Competence | Does performer have necessary skills? |
| Authority | Does performer have proper authorization? |
| Evidence | Is control performance documented? |

## Risk Appetite and Tolerance

### Risk Appetite Definition

| Appetite Level | Description | Example |
|----------------|-------------|---------|
| Risk Averse | Avoid risk, accept lower returns | Regulated industries |
| Risk Neutral | Balance risk and return | Most organizations |
| Risk Seeking | Accept higher risk for returns | Startups, ventures |

### Risk Tolerance Statement

**Example Format:**
```
Category: Financial Reporting
Risk Appetite: Low
Risk Tolerance: No material misstatement in financial statements
Threshold: < 5% of pre-tax income, < 2% of total assets
```

## Risk Monitoring and Reporting

### Key Risk Indicators (KRIs)

| Category | KRI | Threshold |
|----------|-----|-----------|
| Credit | Past-due receivables | > 5% of AR |
| Liquidity | Current ratio | < 1.5 |
| Operations | Order error rate | > 2% |
| IT | System downtime | > 99.9% uptime |
| HR | Employee turnover | > 20% annually |

### Risk Reporting Structure

| Report | Audience | Frequency | Content |
|--------|----------|-----------|---------|
| Risk Dashboard | Management | Monthly | KRIs, status |
| Risk Summary | Executive | Quarterly | Top risks, trends |
| Risk Deep Dive | Audit Committee | Quarterly | Detailed analysis |
| Annual Risk Report | Board | Annual | Comprehensive review |

### Risk Register Template

| Risk ID | Risk Description | Category | Inherent Risk | Controls | Control Rating | Residual Risk | Owner | Status |
|---------|-----------------|----------|---------------|----------|----------------|---------------|-------|--------|
| R-001 | [Description] | [Category] | H/M/L | [Controls] | [Rating] | H/M/L | [Name] | [Status] |

## Risk Assessment Best Practices

### Do's

1. **Use consistent methodology** across the organization
2. **Involve process owners** in risk identification
3. **Consider both quantitative and qualitative** factors
4. **Document assumptions** and rationale
5. **Update regularly** and after significant changes
6. **Link to controls** and testing activities

### Don'ts

1. **Don't ignore qualitative risks** that are hard to quantify
2. **Don't assess in isolation** without context
3. **Don't set and forget** risk assessments
4. **Don't underestimate** fraud risk
5. **Don't rely solely on historical data** for emerging risks
