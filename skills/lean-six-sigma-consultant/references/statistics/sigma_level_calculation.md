# Sigma Level Calculation Guide

## Overview

Sigma level is a metric used in Six Sigma to express process capability in terms of standard deviations from the mean. A higher sigma level indicates better quality performance.

---

## Key Metrics

### Defect Terminology

| Term | Abbreviation | Definition |
|------|--------------|------------|
| Unit | - | One item produced or one service transaction |
| Defect | - | Any nonconformance to specification |
| Defect Opportunity | - | Any chance for a defect to occur |
| Defective | - | A unit with one or more defects |

### Defect Metrics

**DPU (Defects Per Unit)**:
```
DPU = Total Defects / Total Units
```

**DPO (Defects Per Opportunity)**:
```
DPO = Total Defects / (Total Units × Opportunities Per Unit)
```

**DPMO (Defects Per Million Opportunities)**:
```
DPMO = DPO × 1,000,000
```

---

## Sigma Level Conversion

### DPMO to Sigma Table

| Sigma Level | DPMO | Yield | Cpk |
|-------------|------|-------|-----|
| 1.0σ | 691,462 | 30.85% | 0.33 |
| 1.5σ | 500,000 | 50.00% | 0.50 |
| 2.0σ | 308,538 | 69.15% | 0.67 |
| 2.5σ | 158,655 | 84.13% | 0.83 |
| 3.0σ | 66,807 | 93.32% | 1.00 |
| 3.5σ | 22,750 | 97.73% | 1.17 |
| 4.0σ | 6,210 | 99.38% | 1.33 |
| 4.5σ | 1,350 | 99.87% | 1.50 |
| 5.0σ | 233 | 99.977% | 1.67 |
| 5.5σ | 32 | 99.997% | 1.83 |
| 6.0σ | 3.4 | 99.99966% | 2.00 |

*Note: Values include 1.5σ shift*

### Calculation Formulas

**From DPMO to Sigma**:
```
Z = NORMSINV(1 - DPMO/1,000,000)
Sigma = Z + 1.5
```

**From Sigma to DPMO**:
```
Z = Sigma - 1.5
DPMO = (1 - NORMSDIST(Z)) × 1,000,000
```

**From Yield to Sigma**:
```
Z = NORMSINV(Yield)
Sigma = Z + 1.5
```

---

## The 1.5 Sigma Shift

### What is It?
The 1.5σ shift is a standard assumption in Six Sigma that processes naturally drift over time.

### Why Use It?
- Short-term studies show better capability than long-term performance
- Accounts for process drift, shift changes, seasonal variation
- Industry standard for consistent benchmarking

### Short-term vs Long-term

| | Short-term | Long-term |
|---|------------|-----------|
| Measurement | Within subgroups | Overall |
| Variation | σ_within | σ_overall |
| Indices | Cp, Cpk | Pp, Ppk |
| Sigma | Zsτ | Zlt = Zsτ - 1.5 |

**Example**:
```
Short-term sigma: 4.5σ
Long-term sigma: 4.5 - 1.5 = 3.0σ
Expected long-term DPMO: 66,807
```

---

## Yield Calculations

### First Pass Yield (FPY)

Percentage of units that pass through without any defects on first attempt.

```
FPY = (Units In - Defective Units) / Units In × 100

OR

FPY = (1 - DPU) for small DPU
FPY = e^(-DPU) for larger DPU (Poisson approximation)
```

### Rolled Throughput Yield (RTY)

Probability of passing through entire process without defects.

```
RTY = FPY₁ × FPY₂ × FPY₃ × ... × FPYₙ
```

**Example**:
```
Process with 4 steps:
Step 1: FPY = 95%
Step 2: FPY = 98%
Step 3: FPY = 92%
Step 4: FPY = 97%

RTY = 0.95 × 0.98 × 0.92 × 0.97 = 83.1%
```

### Yield Types Comparison

```
Final Yield: What comes out good (includes rework)
          = Good Units / Total Input

First Pass Yield: Good without rework at each step
               = Passed First Time / Total Input

Rolled Throughput Yield: Probability through all steps
                       = Product of FPYs
```

**Hidden Factory**: Gap between Final Yield and RTY represents rework

---

## Calculation Examples

### Example 1: Manufacturing

```
Data:
- Units produced: 10,000
- Total defects found: 150
- Opportunities per unit: 10 (10 things that could go wrong)

Calculations:
DPU = 150 / 10,000 = 0.015 defects per unit
DPO = 150 / (10,000 × 10) = 0.0015
DPMO = 0.0015 × 1,000,000 = 1,500 DPMO

Sigma Level:
Z = NORMSINV(1 - 0.0015) = 2.97
Sigma = 2.97 + 1.5 = 4.47σ
```

### Example 2: Service Process

```
Data:
- Orders processed: 5,000
- Orders with errors: 200
- Defining opportunities: Order is either correct or has errors (1 opp)

Calculations:
DPU = 200 / 5,000 = 0.04
DPO = 200 / (5,000 × 1) = 0.04
DPMO = 0.04 × 1,000,000 = 40,000 DPMO

Sigma Level:
Z = NORMSINV(1 - 0.04) = 1.75
Sigma = 1.75 + 1.5 = 3.25σ
```

### Example 3: Multiple Opportunity Types

```
Data:
- Forms processed: 1,000
- Opportunities per form:
  - Name: 1
  - Address: 1
  - Account #: 1
  - Amount: 1
  - Date: 1
  Total: 5 opportunities

- Defects found: 75

Calculations:
DPO = 75 / (1,000 × 5) = 0.015
DPMO = 15,000

Sigma = 3.67σ
```

---

## Counting Opportunities

### Guidelines

**Good Opportunity**:
- Customer cares about it
- Independent (not caused by another defect)
- Can be measured/checked
- Consistent across products

**Not an Opportunity**:
- Internal preference only
- Dependent on another
- Can't be verified
- Varies arbitrarily

### Example: Order Fulfillment

| Opportunity | Description |
|-------------|-------------|
| 1 | Correct item shipped |
| 2 | Correct quantity |
| 3 | Undamaged |
| 4 | On time |
| 5 | Correct address |
| 6 | Correct invoice |

Total: 6 opportunities per order

### Impact of Opportunity Count

```
Same process, different opportunity counts:

Scenario A: 5 opportunities
- 50 defects in 1,000 units
- DPMO = 50/(1,000×5) × 1M = 10,000
- Sigma = 3.83σ

Scenario B: 20 opportunities
- 50 defects in 1,000 units
- DPMO = 50/(1,000×20) × 1M = 2,500
- Sigma = 4.32σ
```

**Important**: Be consistent with opportunity counting for valid comparisons.

---

## Benchmarking Sigma Levels

### Typical Industry Performance

| Industry/Process | Typical Sigma |
|------------------|---------------|
| World-class manufacturing | 5-6σ |
| Average manufacturing | 3-4σ |
| Service industry | 2-3σ |
| Healthcare (general) | 2.5-3.5σ |
| Airlines (baggage) | 3.5-4σ |
| Airline (fatalities) | 6+ σ |
| IRS tax advice | ~1σ |

### Six Sigma Goals

| Goal | DPMO | Yield |
|------|------|-------|
| 6σ short-term | 0.002 | 99.9999998% |
| 6σ long-term | 3.4 | 99.99966% |

---

## Quick Reference Card

### Conversions

```
DPU = Defects / Units
DPO = Defects / (Units × Opportunities)
DPMO = DPO × 1,000,000
Yield = 1 - DPO (or e^-DPU)
Sigma = NORMSINV(Yield) + 1.5
```

### Common DPMO to Sigma

| DPMO | Sigma |
|------|-------|
| 500,000 | 1.5σ |
| 300,000 | 2.0σ |
| 66,807 | 3.0σ |
| 6,210 | 4.0σ |
| 233 | 5.0σ |
| 3.4 | 6.0σ |

### Sigma to Cpk

```
Cpk ≈ Sigma / 3

Example: 4.5σ → Cpk ≈ 1.5
```

---

## Common Mistakes

1. **Inconsistent opportunity counts**: Comparing apples to oranges
2. **Forgetting the 1.5σ shift**: Not industry standard
3. **Mixing short-term and long-term**: Different measures
4. **Too many/few opportunities**: Artificially inflates/deflates sigma
5. **Not distinguishing defects from defectives**: Different calculations
6. **Assuming one defect per unit**: Units can have multiple defects
