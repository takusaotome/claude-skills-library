# Control Charts Guide

## Overview

Control charts are statistical tools used to monitor process performance over time. They distinguish between normal variation (common cause) and abnormal variation (special cause), enabling timely response to process changes.

## Purpose

- Monitor process stability over time
- Detect special cause variation early
- Prevent defects before they occur
- Provide data-driven decision making
- Maintain process improvements

---

## Control Chart Structure

```
UCL ─────────────────────────────────── Upper Control Limit
                    ○
           ○             ○
      ○         ○              ○
CL ──●────●─────●────●────●─────●──── Center Line (Mean)
           ○         ○
                ○
LCL ─────────────────────────────────── Lower Control Limit
     1    2    3    4    5    6    7   Time/Sample
```

**Components**:
- **Center Line (CL)**: Process average
- **Upper Control Limit (UCL)**: +3σ from center
- **Lower Control Limit (LCL)**: -3σ from center
- **Data Points**: Individual measurements or subgroup statistics

---

## Control Chart Selection

### Decision Tree

```
What type of data?
│
├── Continuous (Variables)
│   │
│   └── What is subgroup size?
│       ├── n = 1 → I-MR Chart
│       ├── n = 2-10 → X-bar/R Chart
│       └── n > 10 → X-bar/S Chart
│
└── Discrete (Attributes)
    │
    └── Counting what?
        ├── Defective Units (Pass/Fail)
        │   ├── Sample size varies → P Chart
        │   └── Sample size constant → NP Chart
        │
        └── Number of Defects
            ├── Opportunity varies → U Chart
            └── Opportunity constant → C Chart
```

---

## Variables Control Charts

### I-MR Chart (Individuals and Moving Range)

**When to Use**:
- Subgroup size = 1 (individual measurements)
- Slow production rate
- Destructive testing
- Long time between samples

**Calculations**:
```
X Chart (Individuals):
CL = X̄ (average of all individuals)
UCL = X̄ + 2.66 × MR̄
LCL = X̄ - 2.66 × MR̄

MR Chart (Moving Range):
CL = MR̄ (average moving range)
UCL = 3.27 × MR̄
LCL = 0
```

**Example Application**: Daily temperature reading, batch yields

### X-bar/R Chart (Average and Range)

**When to Use**:
- Subgroup size 2-10
- Most common control chart
- Production processes with regular sampling

**Calculations**:
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

**Constants Table**:
| n | A₂ | D₃ | D₄ |
|---|-----|-----|-----|
| 2 | 1.880 | 0 | 3.267 |
| 3 | 1.023 | 0 | 2.575 |
| 4 | 0.729 | 0 | 2.282 |
| 5 | 0.577 | 0 | 2.115 |
| 6 | 0.483 | 0 | 2.004 |
| 7 | 0.419 | 0.076 | 1.924 |
| 8 | 0.373 | 0.136 | 1.864 |
| 9 | 0.337 | 0.184 | 1.816 |
| 10 | 0.308 | 0.223 | 1.777 |

### X-bar/S Chart (Average and Standard Deviation)

**When to Use**:
- Subgroup size > 10
- When more precise estimate of variation needed
- Automated data collection

---

## Attributes Control Charts

### P Chart (Proportion Defective)

**When to Use**:
- Tracking proportion of defective units
- Sample size can vary
- Pass/fail classification

**Calculations**:
```
CL = p̄ (average proportion defective)
UCL = p̄ + 3 × √(p̄(1-p̄)/n)
LCL = p̄ - 3 × √(p̄(1-p̄)/n)
```

**Example**: % of orders with errors (varying order volume)

### NP Chart (Number of Defectives)

**When to Use**:
- Tracking count of defective units
- Sample size must be constant
- Simpler to interpret than P chart

**Calculations**:
```
CL = n × p̄
UCL = n × p̄ + 3 × √(n × p̄ × (1-p̄))
LCL = n × p̄ - 3 × √(n × p̄ × (1-p̄))
```

**Example**: Number of defective parts per 100 inspected

### C Chart (Count of Defects)

**When to Use**:
- Counting defects (not defective units)
- Same area of opportunity
- Multiple defects possible per unit

**Calculations**:
```
CL = c̄ (average defect count)
UCL = c̄ + 3 × √c̄
LCL = c̄ - 3 × √c̄
```

**Example**: Number of scratches per car body

### U Chart (Defects Per Unit)

**When to Use**:
- Counting defects per unit
- Area of opportunity varies
- Normalize for different sample sizes

**Calculations**:
```
CL = ū (average defects per unit)
UCL = ū + 3 × √(ū/n)
LCL = ū - 3 × √(ū/n)
```

**Example**: Errors per invoice (varying invoice complexity)

---

## Out-of-Control Rules

### Western Electric Rules

| Rule | Description | Pattern |
|------|-------------|---------|
| 1 | 1 point beyond 3σ | Single outlier |
| 2 | 2 of 3 consecutive points beyond 2σ (same side) | Near-outlier cluster |
| 3 | 4 of 5 consecutive points beyond 1σ (same side) | Shift starting |
| 4 | 8 consecutive points on same side of CL | Process shift |

### Additional Rules (Nelson Rules)

| Rule | Description |
|------|-------------|
| 5 | 6 consecutive points trending up or down |
| 6 | 14 consecutive points alternating up/down |
| 7 | 15 consecutive points within ±1σ |

### Visual Interpretation

```
Pattern: Process Shift
         ─────UCL─────────────────
                    ○ ○ ○ ○
              ○ ○ ○
         ─────CL──────────────────
    ○ ○ ○
         ─────LCL─────────────────

Pattern: Trend
         ─────UCL─────────────────
                          ○
                       ○
                    ○
         ─────CL──○───────────────
               ○
            ○
         ─────LCL─────────────────

Pattern: Cyclic
         ─────UCL─────────────────
            ○        ○        ○
         ─────CL──────────────────
               ○        ○
         ─────LCL─────────────────
```

---

## Control Chart Implementation

### Step 1: Select Appropriate Chart
- Match to data type
- Consider sample size
- Evaluate practical constraints

### Step 2: Collect Data
- Minimum 20-25 subgroups for initial setup
- Ensure process is stable during collection
- Record all stratification factors

### Step 3: Calculate Control Limits
- Use formulas for selected chart type
- Calculate center line and limits
- Set up chart template

### Step 4: Plot Data
- Plot points in time sequence
- Draw center line and limits
- Add zone lines (±1σ, ±2σ) for rule application

### Step 5: Interpret and Respond
- Check for out-of-control signals
- Investigate special causes
- Document findings and actions

### Step 6: Maintain and Update
- Regular data plotting
- Periodic limit recalculation
- Update when process changes

---

## Response to Out-of-Control

### When Signal Detected

1. **Verify**: Confirm data is correct
2. **Investigate**: Find the special cause
3. **Act**: Remove special cause if bad, lock in if good
4. **Document**: Record findings and actions

### Common Special Causes

| Signal | Possible Causes |
|--------|-----------------|
| Single point beyond limits | Measurement error, material issue, setup error |
| Shift in level | Process change, new operator, equipment adjustment |
| Trend | Tool wear, gradual drift, environmental change |
| Cycles | Rotation of operators, temperature cycles |
| Hugging center | Different streams mixed, data manipulation |

---

## Best Practices

### Do's
- Choose correct chart type
- Collect sufficient baseline data
- Plot in real-time (or near real-time)
- Investigate all signals
- Keep charts visible
- Train all users
- Update limits when process changes

### Don'ts
- Don't recalculate limits with every point
- Don't ignore signals
- Don't use with unstable process
- Don't plot old data without marking
- Don't remove points without documentation
- Don't use attribute charts for continuous data

---

## Common Mistakes

1. **Wrong chart type**: Using X-bar/R for attribute data
2. **Insufficient data**: Setting limits with too few points
3. **Ignoring signals**: Not investigating out-of-control
4. **Over-reacting**: Adjusting for common cause variation
5. **Stale limits**: Not updating after process change
6. **No context**: Not recording what happened
7. **Infrequent plotting**: Losing real-time value
