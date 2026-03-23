# Audit Sampling Guide

## Purpose

This guide provides practical sampling methods for internal auditors to select representative test samples.

---

## Sampling Methods Overview

| Method | Type | When to Use | Projectability |
|--------|------|-------------|----------------|
| Random Sampling | Statistical | Large populations, control testing | Yes |
| Systematic Sampling | Statistical | Ordered populations, consistent intervals | Yes |
| Stratified Sampling | Statistical | Heterogeneous populations | Yes |
| Monetary Unit Sampling (MUS) | Statistical | Substantive testing, higher-value items | Yes |
| Judgmental Sampling | Non-statistical | High-risk items, targeted testing | No |
| Haphazard Sampling | Non-statistical | Quick scans, preliminary testing | No |

---

## Statistical Sampling

### Random Sampling

Select samples where each item has equal probability of selection.

**Process**:
1. Define population (e.g., all invoices in Q1)
2. Assign unique numbers to each item
3. Generate random numbers
4. Select items matching random numbers

**Use Case**: Control testing where you need statistical validity

### Sample Size Determination

For **attribute sampling** (control testing - pass/fail results):

| Confidence Level | Tolerable Error Rate | Expected Error Rate | Approximate Sample Size |
|------------------|---------------------|---------------------|------------------------|
| 90% | 10% | 0% | 22 |
| 90% | 5% | 0% | 45 |
| 95% | 10% | 0% | 29 |
| 95% | 5% | 0% | 59 |
| 95% | 5% | 1% | 93 |
| 95% | 5% | 2% | 181 |

**Key Terms**:
- **Confidence Level**: Probability that sample results reflect population (typically 90-95%)
- **Tolerable Error Rate**: Maximum error rate acceptable without concluding control failure (typically 5-10%)
- **Expected Error Rate**: Anticipated error rate based on prior audits or knowledge

### Systematic Sampling

Select every nth item from an ordered list.

**Process**:
1. Calculate interval: N (population) ÷ n (sample size)
2. Select random starting point between 1 and interval
3. Select every nth item thereafter

**Example**:
- Population: 1,000 invoices
- Sample size: 50
- Interval: 1,000 ÷ 50 = 20
- Random start: 7
- Select items: 7, 27, 47, 67, ...

**Caution**: Ensure population is not ordered in a way that creates bias

### Stratified Sampling

Divide population into homogeneous subgroups (strata) and sample from each.

**Use Case**: Population with distinct risk levels or characteristics

**Example**:
```
Population: 500 vendor payments

Strata:
- High value (>$100K): 20 payments → sample 10 (50%)
- Medium ($10K-$100K): 80 payments → sample 20 (25%)
- Low (<$10K): 400 payments → sample 30 (7.5%)

Total sample: 60 payments
```

### Monetary Unit Sampling (MUS)

Each dollar (or currency unit) has equal chance of selection; higher-value items more likely selected.

**Process**:
1. Calculate cumulative dollars
2. Determine sampling interval (total $ ÷ sample size)
3. Select random start
4. Select items containing each sampling unit

**Use Case**: Substantive testing to detect overstatements

**Example**:
```
Total population value: $1,000,000
Sample size: 50
Sampling interval: $1,000,000 ÷ 50 = $20,000
Random start: $8,500

Selection:
- $8,500 → Invoice A ($15,000 - contains $8,500)
- $28,500 → Invoice B ($50,000 - contains $28,500)
- $48,500 → Invoice B ($50,000 - also contains $48,500)
...
```

---

## Non-Statistical (Judgmental) Sampling

### When to Use Judgmental Sampling

- Testing specific high-risk items
- Following up on prior exceptions
- Investigating anomalies identified in data analytics
- Limited population size
- Preliminary testing before formal audit

### Judgmental Selection Criteria

| Criterion | Example Selection |
|-----------|-------------------|
| High-value items | Top 10 transactions by dollar amount |
| Unusual patterns | Invoices with round numbers ($10,000, $50,000) |
| Time-based | Month-end transactions, year-end entries |
| Risk indicators | New vendors, rush approvals, manual overrides |
| Prior exceptions | Items from same vendor/employee as past findings |
| Data analytics flags | Benford's Law anomalies, duplicates, gaps |

### Limitations

- Cannot project results to entire population
- Subject to auditor bias
- May not represent normal operations
- Should be supplemented with statistical sampling for key controls

---

## Sample Size Quick Reference

### Minimum Sample Sizes by Control Frequency

| Control Frequency | Minimum Sample | Notes |
|-------------------|----------------|-------|
| Multiple times daily | 25-30 | High volume, automation |
| Daily | 20-25 | Daily controls |
| Weekly | 15-20 | Weekly review cycles |
| Monthly | 5-10 | Monthly reconciliations |
| Quarterly | 2-4 | Quarterly reviews |
| Annually | 1-2 | Annual controls |

### Adjustments for Risk

| Factor | Sample Size Adjustment |
|--------|----------------------|
| Critical control (single point of failure) | +50% |
| New or recently changed control | +25% |
| Prior year exceptions | +25% |
| Reliance by external audit | +25% |
| Low-risk, stable control | -25% |

---

## Evaluation of Results

### Exception Handling

1. **Document each exception**
2. **Analyze root cause**
3. **Determine if systematic or isolated**
4. **Consider expanding sample if**:
   - Exception rate > expected
   - Exceptions suggest broader issue
   - Pattern indicates control breakdown

### Projecting Results (Statistical Sampling Only)

**Upper Error Rate Calculation**:
```
If sample of 59 items has 2 exceptions (3.4% error rate):
- At 95% confidence
- Upper error rate ≈ 9%

Conclusion: Cannot conclude tolerable error rate of 5% is met
→ Control is NOT operating effectively
```

### Documentation Requirements

For each sample:
1. Population description and size
2. Sampling method used and rationale
3. Sample size and selection criteria
4. Items selected (reference numbers)
5. Test results for each item
6. Exception details and analysis
7. Conclusion on control effectiveness

---

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Too small sample | Unreliable conclusions | Use sample size tables |
| Selection bias | Unrepresentative sample | Use random/systematic selection |
| Not testing controls at point of failure | Missing control gaps | Include high-risk periods |
| Ignoring compensating controls | Overstatement of risk | Consider full control environment |
| Not expanding for exceptions | Missing systemic issues | Investigate and expand as needed |

---

## References

- AICPA Audit Sampling Guide
- IIA Practice Guide: Sampling
- ISA 530: Audit Sampling
