# Process Capability Analysis

## Overview

Process capability measures how well a process meets customer specifications. It compares the spread of process output to the width of the specification limits.

## Prerequisites

Before conducting capability analysis:
1. **Process stability**: Process must be in statistical control (no special causes)
2. **Normal distribution**: Data should be approximately normal
3. **Validated measurement system**: MSA shows acceptable Gage R&R

---

## Capability vs. Performance

| Term | Symbol | Variation Used | Time Frame |
|------|--------|----------------|------------|
| Capability | Cp, Cpk | Within-subgroup (σ_within) | Short-term |
| Performance | Pp, Ppk | Overall (σ_overall) | Long-term |

**Why the difference?**
- Short-term (within-subgroup) variation: Common cause only
- Long-term (overall) variation: Includes shift and drift

---

## Capability Indices

### Cp (Potential Capability)

**What it measures**: Process potential if perfectly centered

**Formula**:
```
Cp = (USL - LSL) / (6σ)

Where:
USL = Upper Specification Limit
LSL = Lower Specification Limit
σ = Within-subgroup standard deviation
```

**Interpretation**:
- Cp = 1.0: Process spread equals specification spread
- Cp > 1.0: Process fits within specifications (with margin)
- Cp < 1.0: Process spread exceeds specifications

**Limitations**:
- Does not consider process centering
- Process could be off-center and still have high Cp

### Cpk (Process Capability Index)

**What it measures**: Actual capability considering both variation and centering

**Formula**:
```
Cpk = min(Cpu, Cpl)

Where:
Cpu = (USL - μ) / (3σ)   ← Upper capability
Cpl = (μ - LSL) / (3σ)   ← Lower capability
μ = Process mean
```

**Interpretation**:
- Cpk accounts for how close mean is to nearest specification
- Cpk ≤ Cp always (Cpk = Cp when perfectly centered)
- Cpk can be negative if mean is outside specifications

### Pp (Performance Potential)

**Formula**:
```
Pp = (USL - LSL) / (6σ_overall)

Where σ_overall = overall standard deviation (all data)
```

### Ppk (Performance Index)

**Formula**:
```
Ppk = min(Ppu, Ppl)

Where:
Ppu = (USL - μ) / (3σ_overall)
Ppl = (μ - LSL) / (3σ_overall)
```

---

## Estimation Methods

### Within-Subgroup Standard Deviation (σ_within)

**Method 1: R-bar/d2** (Most common)
```
σ_within = R̄ / d2

Where:
R̄ = Average range of subgroups
d2 = Control chart constant based on subgroup size
```

**d2 Constants**:
| n | d2 |
|---|-----|
| 2 | 1.128 |
| 3 | 1.693 |
| 4 | 2.059 |
| 5 | 2.326 |
| 6 | 2.534 |
| 7 | 2.704 |
| 8 | 2.847 |
| 9 | 2.970 |
| 10 | 3.078 |

**Method 2: S-bar/c4**
```
σ_within = S̄ / c4

Where:
S̄ = Average standard deviation of subgroups
c4 = Control chart constant
```

### Overall Standard Deviation (σ_overall)

**Sample standard deviation of all data**:
```
σ_overall = √[Σ(xi - x̄)² / (n-1)]
```

---

## Interpretation Guidelines

### Cpk Value Interpretation

| Cpk Value | Interpretation | Action |
|-----------|----------------|--------|
| < 1.00 | Not capable | Immediate improvement required |
| 1.00 - 1.33 | Marginally capable | Process at risk, improve |
| 1.33 - 1.67 | Capable | Acceptable for most industries |
| 1.67 - 2.00 | Very capable | Excellent performance |
| ≥ 2.00 | World-class | Six Sigma level |

### Industry Standards

| Industry | Typical Cpk Requirement |
|----------|------------------------|
| General manufacturing | ≥ 1.33 |
| Automotive (critical) | ≥ 1.67 |
| Aerospace | ≥ 1.67 - 2.00 |
| Pharmaceutical | ≥ 1.33 - 1.67 |
| Medical devices | ≥ 1.33 - 1.67 |
| Safety-critical | ≥ 2.00 |

---

## Relationship Between Cpk and Defect Rate

| Cpk | Sigma Level | DPMO | Yield |
|-----|-------------|------|-------|
| 0.33 | 1σ | 317,400 | 68.3% |
| 0.50 | 1.5σ | 133,600 | 86.6% |
| 0.67 | 2σ | 45,500 | 95.4% |
| 1.00 | 3σ | 2,700 | 99.73% |
| 1.33 | 4σ | 64 | 99.9937% |
| 1.50 | 4.5σ | 3.4 | 99.99966% |
| 2.00 | 6σ | 0.002 | 99.9999998% |

*Note: Values assume 1.5σ shift*

---

## One-Sided Specifications

### Upper Specification Only (USL)

**CPU (Upper Capability)**:
```
Cpu = (USL - μ) / (3σ)
```
Use when: Smaller is better (defect count, errors)

### Lower Specification Only (LSL)

**CPL (Lower Capability)**:
```
Cpl = (μ - LSL) / (3σ)
```
Use when: Larger is better (strength, yield)

---

## Capability Analysis Process

### Step 1: Verify Stability
- Plot control chart
- Confirm no special causes
- Process must be in control

### Step 2: Collect Data
- Minimum 100 data points recommended
- 25+ subgroups for control chart
- Random sampling across production

### Step 3: Check Normality
- Histogram
- Normal probability plot
- Anderson-Darling test

### Step 4: Calculate Indices
- Calculate σ_within and σ_overall
- Calculate Cp, Cpk, Pp, Ppk
- Include confidence intervals if needed

### Step 5: Interpret Results
- Compare to requirements
- Identify improvement opportunities
- Document findings

---

## Non-Normal Data

### When Data is Not Normal

Options:
1. **Transform data**: Box-Cox transformation
2. **Use non-normal capability**: Weibull, lognormal
3. **Use percentile method**: Based on actual distribution

### Percentile Method

```
Cpk = min[(USL - P50)/(P99.865 - P50), (P50 - LSL)/(P50 - P0.135)]

Where:
P50 = 50th percentile (median)
P99.865 = 99.865th percentile
P0.135 = 0.135th percentile
```

---

## Improving Capability

### Strategies to Increase Cpk

**Center the Process** (If Cp > Cpk):
- Adjust mean toward target
- Reduce bias in measurement

**Reduce Variation** (If Cp ≈ Cpk but both low):
- Identify and reduce variation sources
- Improve process consistency
- Better materials/equipment

**Widen Specifications** (Last resort):
- Review customer requirements
- Challenge specifications
- Design changes

### Priority Based on Cp and Cpk

| Cp | Cpk | Priority |
|----|-----|----------|
| High | High | Monitor and maintain |
| High | Low | Center the process |
| Low | Low | Reduce variation |
| Low | High | (Not possible) |

---

## Reporting Capability

### Capability Report Format

```
PROCESS CAPABILITY REPORT

Process: _______________
Date: _________________
Spec: _________________

Sample Size: n = ___
Mean (μ): ___________
Std Dev (σ_within): ___________
Std Dev (σ_overall): ___________

SPECIFICATIONS
LSL: ___________
Target: ___________
USL: ___________

CAPABILITY INDICES
Cp: _____ [Potential]
Cpk: _____ [Actual]
Cpu: _____ [Upper]
Cpl: _____ [Lower]

PERFORMANCE INDICES
Pp: _____
Ppk: _____

DEFECT ESTIMATION
Expected DPMO: _____
Expected Yield: _____

CONCLUSION
[Capable/Not Capable]
[Recommended actions]
```

---

## Common Mistakes

1. **Analyzing unstable process**: Must be in control first
2. **Ignoring non-normality**: Results may be misleading
3. **Too few samples**: Insufficient precision
4. **Using Pp/Ppk for short-term**: Should use Cp/Cpk
5. **Confusing Cp with Cpk**: Cp ignores centering
6. **Not considering measurement error**: Inflates observed variation
