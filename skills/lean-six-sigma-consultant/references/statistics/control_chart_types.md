# Control Chart Types Reference

## Overview

This reference provides detailed information on control chart types, selection criteria, calculations, and interpretation.

---

## Chart Selection Matrix

### Quick Selection Guide

```
Data Type?
│
├── CONTINUOUS (Variables)
│   │
│   └── Subgroup Size?
│       │
│       ├── n = 1 individual ──────────────→ I-MR Chart
│       │
│       ├── n = 2-10 ──────────────────────→ X-bar/R Chart
│       │
│       └── n > 10 ────────────────────────→ X-bar/S Chart
│
└── DISCRETE (Attributes)
    │
    ├── Defectives (Units Pass/Fail)
    │   │
    │   ├── Sample size CONSTANT ──────────→ NP Chart
    │   │
    │   └── Sample size VARIES ────────────→ P Chart
    │
    └── Defects (Counts per unit)
        │
        ├── Area of opportunity CONSTANT ──→ C Chart
        │
        └── Area of opportunity VARIES ────→ U Chart
```

---

## Variables Charts

### I-MR Chart (Individuals and Moving Range)

**Use When**:
- Single measurements (n=1)
- Batch process (one value per batch)
- Long time between samples
- Destructive testing
- Expensive testing

**Formulas**:
```
Individuals Chart (I):
  CL = X̄
  UCL = X̄ + 2.66 × MR̄
  LCL = X̄ - 2.66 × MR̄

Moving Range Chart (MR):
  CL = MR̄
  UCL = 3.27 × MR̄
  LCL = 0
```

**Where**:
- X̄ = Average of all individual values
- MR = |Xi - Xi-1| (consecutive difference)
- MR̄ = Average of all moving ranges

**Example Data**:
| Sample | Value | MR |
|--------|-------|-----|
| 1 | 25.3 | - |
| 2 | 26.1 | 0.8 |
| 3 | 24.9 | 1.2 |
| 4 | 25.7 | 0.8 |
| 5 | 25.2 | 0.5 |

---

### X-bar/R Chart (Average and Range)

**Use When**:
- Subgroup size 2-10 (most common: 4-5)
- Regular sampling from continuous process
- Most common variables chart

**Formulas**:
```
X-bar Chart:
  CL = X̿ (grand average)
  UCL = X̿ + A₂ × R̄
  LCL = X̿ - A₂ × R̄

R Chart:
  CL = R̄ (average range)
  UCL = D₄ × R̄
  LCL = D₃ × R̄
```

**Control Chart Constants**:
| n | A₂ | D₃ | D₄ | d₂ |
|---|-----|-----|-----|-----|
| 2 | 1.880 | 0 | 3.267 | 1.128 |
| 3 | 1.023 | 0 | 2.575 | 1.693 |
| 4 | 0.729 | 0 | 2.282 | 2.059 |
| 5 | 0.577 | 0 | 2.115 | 2.326 |
| 6 | 0.483 | 0 | 2.004 | 2.534 |
| 7 | 0.419 | 0.076 | 1.924 | 2.704 |
| 8 | 0.373 | 0.136 | 1.864 | 2.847 |
| 9 | 0.337 | 0.184 | 1.816 | 2.970 |
| 10 | 0.308 | 0.223 | 1.777 | 3.078 |

---

### X-bar/S Chart (Average and Standard Deviation)

**Use When**:
- Subgroup size > 10
- More precise variation estimate needed
- Automated data collection

**Formulas**:
```
X-bar Chart:
  CL = X̿
  UCL = X̿ + A₃ × S̄
  LCL = X̿ - A₃ × S̄

S Chart:
  CL = S̄
  UCL = B₄ × S̄
  LCL = B₃ × S̄
```

**Additional Constants**:
| n | A₃ | B₃ | B₄ | c₄ |
|---|-----|-----|-----|-----|
| 10 | 0.975 | 0.284 | 1.716 | 0.9727 |
| 15 | 0.789 | 0.428 | 1.572 | 0.9823 |
| 20 | 0.680 | 0.510 | 1.490 | 0.9869 |
| 25 | 0.606 | 0.565 | 1.435 | 0.9896 |

---

## Attributes Charts

### P Chart (Proportion Defective)

**Use When**:
- Tracking proportion/percentage defective
- Sample size varies
- Each unit is pass/fail

**Formulas**:
```
CL = p̄ = Σ(defectives) / Σ(inspected)

UCL = p̄ + 3√(p̄(1-p̄)/n)
LCL = p̄ - 3√(p̄(1-p̄)/n)
```

**Note**: Control limits change with sample size. Use average n or variable limits.

**Example**:
| Day | Inspected (n) | Defective | p = Def/n |
|-----|---------------|-----------|-----------|
| 1 | 200 | 12 | 0.060 |
| 2 | 180 | 8 | 0.044 |
| 3 | 220 | 15 | 0.068 |

---

### NP Chart (Number of Defectives)

**Use When**:
- Counting defective units
- Sample size is CONSTANT
- Easier to interpret than P chart

**Formulas**:
```
CL = n × p̄

UCL = np̄ + 3√(np̄(1-p̄))
LCL = np̄ - 3√(np̄(1-p̄))
```

**Example**: Sample size always 100
| Day | Defective |
|-----|-----------|
| 1 | 6 |
| 2 | 4 |
| 3 | 8 |

---

### C Chart (Count of Defects)

**Use When**:
- Counting defects (not defective units)
- Same area of opportunity
- Multiple defects possible per unit

**Formulas**:
```
CL = c̄ = Total defects / Number of samples

UCL = c̄ + 3√c̄
LCL = c̄ - 3√c̄
```

**Example**: Defects per car body (same size car)
| Car | Defects |
|-----|---------|
| 1 | 3 |
| 2 | 5 |
| 3 | 2 |

---

### U Chart (Defects Per Unit)

**Use When**:
- Counting defects per unit
- Sample size or opportunity varies
- Normalize for different sizes

**Formulas**:
```
CL = ū = Total defects / Total units

UCL = ū + 3√(ū/n)
LCL = ū - 3√(ū/n)
```

**Example**: Errors per invoice (invoices vary in complexity)
| Day | Invoices | Errors | u = Errors/Invoices |
|-----|----------|--------|---------------------|
| 1 | 50 | 8 | 0.16 |
| 2 | 75 | 10 | 0.13 |
| 3 | 40 | 7 | 0.18 |

---

## Out-of-Control Rules

### Western Electric Rules (Primary)

| Rule | Description | Pattern |
|------|-------------|---------|
| 1 | 1 point beyond 3σ | Single outlier |
| 2 | 2 of 3 points beyond 2σ (same side) | Near-limit cluster |
| 3 | 4 of 5 points beyond 1σ (same side) | Small shift |
| 4 | 8 consecutive points same side of CL | Process shift |

### Additional Rules (Nelson/Zone)

| Rule | Description |
|------|-------------|
| 5 | 6 consecutive points trending up or down |
| 6 | 14 consecutive points alternating up/down |
| 7 | 15 consecutive points within ±1σ |
| 8 | 8 points outside ±1σ on both sides |

### Zone Definitions

```
        UCL ──────────────── Zone A (Beyond 2σ)
        +2σ ──────────────── Zone B (1σ to 2σ)
        +1σ ──────────────── Zone C (Within 1σ)
        CL  ────────────────
        -1σ ──────────────── Zone C
        -2σ ──────────────── Zone B
        LCL ──────────────── Zone A
```

---

## Interpretation Guide

### Common Patterns and Causes

**Single Point Beyond Limits**:
- Measurement error
- Material issue
- Equipment malfunction
- Setup error

**Shift in Level**:
- New operator
- Equipment change
- Different material lot
- Process adjustment

**Trend (6+ points trending)**:
- Tool wear
- Environmental drift
- Gradual deterioration
- Fatigue effects

**Cycles**:
- Temperature fluctuation
- Shift changes
- Maintenance cycles
- Seasonal effects

**Hugging Center Line**:
- Mixed streams
- Stratified sampling
- Calculation error
- Over-adjustment

**Hugging Control Limits**:
- Mixed processes
- Different machines combined
- Measurement resolution

---

## Chart Selection Summary Table

| Chart | Data Type | Sample Size | Best For |
|-------|-----------|-------------|----------|
| I-MR | Continuous | n=1 | Batch, slow process |
| X-bar/R | Continuous | n=2-10 | Most common |
| X-bar/S | Continuous | n>10 | Large samples |
| P | Attribute | Variable | % defective |
| NP | Attribute | Constant | # defective |
| C | Attribute | Constant area | # defects |
| U | Attribute | Variable area | Defects/unit |

---

## Implementation Checklist

- [ ] Determine data type (continuous vs. attribute)
- [ ] Determine subgroup size or sample approach
- [ ] Select appropriate chart type
- [ ] Collect baseline data (20-25+ subgroups)
- [ ] Calculate control limits
- [ ] Plot data and control limits
- [ ] Add zone lines if using zone rules
- [ ] Train users on interpretation
- [ ] Establish response procedures
- [ ] Create documentation
