# Baseline Metrics and Sigma Level Calculation

## Overview

Baseline metrics establish current process performance before improvement. They provide the starting point against which improvement will be measured.

## Key Baseline Metrics

### Defect-Based Metrics

#### DPU (Defects Per Unit)
The average number of defects per unit produced.

```
DPU = Total Defects / Total Units
```

**Example**:
- 150 defects found in 1,000 units
- DPU = 150 / 1,000 = 0.15 defects per unit

#### DPO (Defects Per Opportunity)
The probability of a defect occurring at any opportunity.

```
DPO = Total Defects / (Total Units × Opportunities Per Unit)
```

**Example**:
- 150 defects in 1,000 units
- Each unit has 10 opportunities for defects
- DPO = 150 / (1,000 × 10) = 0.015

#### DPMO (Defects Per Million Opportunities)
Defects per opportunity scaled to one million.

```
DPMO = DPO × 1,000,000
```

**Example**:
- DPO = 0.015
- DPMO = 0.015 × 1,000,000 = 15,000 DPMO

### Yield Metrics

#### First Pass Yield (FPY)
Percentage of units that pass through a process step without defects on first attempt.

```
FPY = (Units without defects) / (Total units) × 100
```

**Example**:
- 950 units pass inspection on first attempt out of 1,000
- FPY = 950 / 1,000 × 100 = 95%

#### Rolled Throughput Yield (RTY)
Probability of passing through all process steps without defects.

```
RTY = FPY₁ × FPY₂ × FPY₃ × ... × FPYₙ
```

**Example**:
- Step 1: 95% FPY
- Step 2: 90% FPY
- Step 3: 98% FPY
- RTY = 0.95 × 0.90 × 0.98 = 83.8%

#### Final Yield (Traditional)
Percentage of acceptable units at the end (includes rework).

```
Final Yield = Good Units Output / Total Units Input × 100
```

**Limitation**: Hides rework and scrap in process

### Sigma Level

#### What is Sigma Level?
Sigma level is a metric that describes how many standard deviations fit between the process mean and the specification limit. Higher sigma = better quality.

#### Sigma Level Table

| Sigma Level | DPMO | Yield | Process Capability |
|-------------|------|-------|-------------------|
| 1σ | 691,462 | 30.9% | Very poor |
| 2σ | 308,538 | 69.1% | Poor |
| 3σ | 66,807 | 93.3% | Average |
| 4σ | 6,210 | 99.38% | Good |
| 5σ | 233 | 99.977% | Very good |
| 6σ | 3.4 | 99.99966% | World class |

*Note: These values include 1.5σ shift (industry standard assumption)*

#### Calculating Sigma Level

**From DPMO**:
```
Sigma Level = NORMSINV(1 - DPMO/1,000,000) + 1.5
```

**From Yield**:
```
Sigma Level = NORMSINV(Yield) + 1.5
```

**Quick Reference**:
| DPMO Range | Approximate Sigma |
|------------|------------------|
| 500,000+ | < 1.5σ |
| 300,000-500,000 | 1.5-2.0σ |
| 100,000-300,000 | 2.0-2.5σ |
| 50,000-100,000 | 2.5-3.0σ |
| 10,000-50,000 | 3.0-3.5σ |
| 5,000-10,000 | 3.5-4.0σ |
| 1,000-5,000 | 4.0-4.5σ |
| 100-1,000 | 4.5-5.0σ |
| 10-100 | 5.0-5.5σ |
| < 10 | > 5.5σ |

### The 1.5 Sigma Shift

**Why the shift?**
Processes naturally drift over time. The 1.5σ shift accounts for long-term variation that isn't captured in short-term studies.

**Short-term vs Long-term**:
- Short-term: σ_st (from Gage R&R, process studies)
- Long-term: σ_lt ≈ σ_st + 1.5σ shift

**In practice**:
- A process measured at 4.5σ short-term
- Expected to perform at 3.0σ long-term (4.5 - 1.5 = 3.0)

---

## Identifying Opportunities

### What is an Opportunity?
An opportunity is a chance for a defect to occur. Proper opportunity counting is critical for DPMO calculation.

### Guidelines for Counting Opportunities

**Rules**:
1. Must be something customer cares about
2. Must be independent (one defect doesn't cause another)
3. Must be measurable/checkable
4. Should be consistent across products

**Example - Order Processing**:
Opportunities per order:
1. Customer name correct
2. Address correct
3. Product SKU correct
4. Quantity correct
5. Price correct
6. Shipping method correct
7. Payment processed
8. Delivery date correct

Total: 8 opportunities per order

**Common Mistake**: Counting too many or too few opportunities artificially changes DPMO

---

## Establishing Baseline

### Step 1: Define Metrics
- Primary metric (Y): Main measure of success
- Supporting metrics: Related measures
- Consequential metrics: To avoid unintended impact

### Step 2: Collect Data
- Sufficient sample size (minimum 30)
- Representative time period
- Proper stratification
- Validated measurement system (MSA)

### Step 3: Calculate Baseline

**Baseline Calculation Example**:

```
Project: Reduce Invoice Processing Errors

Data Collection:
- Period: 4 weeks
- Total invoices: 2,000
- Total errors found: 120
- Opportunities per invoice: 10

Calculations:
DPU = 120 / 2,000 = 0.06 defects per invoice
DPO = 120 / (2,000 × 10) = 0.006
DPMO = 0.006 × 1,000,000 = 6,000 DPMO
Sigma Level ≈ 4.0σ

FPY = (2,000 - 120) / 2,000 = 94%
(Assuming one error makes invoice defective)

Baseline Summary:
- Error rate: 6%
- DPMO: 6,000
- Sigma: 4.0σ
- FPY: 94%
```

### Step 4: Stratify Baseline

Break down baseline by key variables:

| Stratification | Error Rate | DPMO | Sigma |
|----------------|------------|------|-------|
| Overall | 6% | 6,000 | 4.0σ |
| Region A | 4% | 4,000 | 4.1σ |
| Region B | 8% | 8,000 | 3.9σ |
| Processor Type 1 | 5% | 5,000 | 4.1σ |
| Processor Type 2 | 10% | 10,000 | 3.8σ |

---

## Setting Targets

### Target Setting Guidelines

**Factors to Consider**:
1. Current baseline (where are we?)
2. Entitlement (what's theoretically possible?)
3. Benchmark (what do others achieve?)
4. Business need (what's required?)
5. Project scope and resources

**Typical Improvement Targets**:
- Green Belt project: 50-70% reduction in defects
- Black Belt project: 70-90% reduction in defects

### Entitlement

**Definition**: Best performance achievable with current resources

**How to Determine**:
- Best historical performance
- Best shift/operator/machine
- Theoretical limit
- Industry benchmark

**Example**:
```
Baseline: 6% error rate
Best historical month: 3% error rate
Industry benchmark: 1% error rate
Theoretical (perfect): 0%

Entitlement: 1-3% (achievable best)
Target: 2% (50-70% reduction from baseline)
```

---

## Reporting Baseline

### Baseline Summary Format

```
┌────────────────────────────────────────────────┐
│           BASELINE SUMMARY                      │
├────────────────────────────────────────────────┤
│ Primary Metric (Y): Invoice Error Rate          │
│                                                 │
│ Baseline:     6.0%                              │
│ Target:       2.0%                              │
│ Entitlement:  1.0%                              │
│                                                 │
│ DPMO:         6,000                             │
│ Sigma Level:  4.0σ                              │
│ FPY:          94%                               │
│                                                 │
│ Data Period:  Jan 1 - Jan 28, 2024             │
│ Sample Size:  2,000 invoices                    │
├────────────────────────────────────────────────┤
│ Improvement Goal: 67% reduction in errors       │
└────────────────────────────────────────────────┘
```

### Visualization

**Run Chart**: Show baseline performance over time
- X-axis: Time period
- Y-axis: Metric value
- Reference line: Baseline average

**Pareto Chart**: Show defect categories
- Identify biggest contributors
- Focus improvement efforts

---

## Common Mistakes

1. **Insufficient data**: Not enough samples for reliable baseline
2. **Wrong time period**: Not representative (holiday, unusual events)
3. **Inconsistent definition**: Defect defined differently by data sources
4. **Ignoring MSA**: Measurement error inflates or hides real issues
5. **Too few opportunities**: Inflates DPMO
6. **Too many opportunities**: Deflates DPMO
7. **Not stratifying**: Missing important subgroup differences
8. **Moving target**: Changing definition during project
