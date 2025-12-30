# Measurement System Analysis (MSA) Guide

## Overview

Measurement System Analysis (MSA) evaluates the measurement system to ensure it produces reliable, accurate data. Before using data for analysis, you must verify the measurement system itself is not a significant source of variation.

## Why MSA Matters

Consider: If your measurement system has 30% error, how can you trust decisions based on that data?

**MSA answers**:
- Is the measurement accurate?
- Is it consistent over time?
- Do different operators get the same result?
- How much variation comes from measurement vs. the actual process?

## Types of Measurement Error

### Accuracy (Bias)
- Difference between measured value and true value
- Systematic error
- Affects all measurements in same direction

### Precision (Variation)
- Spread of repeated measurements
- Random error
- Two components: Repeatability and Reproducibility

### Total Measurement Error
```
Total Variation = Process Variation + Measurement Variation
                = Process Variation + Repeatability + Reproducibility
```

## Gage R&R Study

Gage R&R (Repeatability and Reproducibility) is the most common MSA for continuous data.

### What It Measures

**Repeatability (Equipment Variation)**
- Same operator, same part, same gage, multiple measurements
- "Can the gage repeat itself?"

**Reproducibility (Appraiser Variation)**
- Different operators, same part, same gage
- "Do operators get the same result?"

### Gage R&R Study Design

**Typical Design**:
- 10 parts (covering the measurement range)
- 3 operators
- 2-3 trials per part per operator
- Total: 60-90 measurements

**Requirements**:
- Parts must represent the actual process variation
- Parts should span the specification range
- Parts must be stable (not changing during study)
- Operators should represent those who normally measure

### Conducting a Gage R&R

**Step 1: Select Parts**
- Choose 10 parts spanning the range
- Number them (hidden from operators)
- Ensure they won't change during study

**Step 2: Prepare**
- Calibrate the gage
- Train operators on the procedure
- Randomize measurement order
- Blind operators to part numbers

**Step 3: Measure**
- Each operator measures each part
- Record results
- Repeat for all trials

**Step 4: Analyze**
- Calculate repeatability (within-operator variation)
- Calculate reproducibility (between-operator variation)
- Calculate total Gage R&R
- Compare to tolerance/process variation

### Gage R&R Metrics

**%Gage R&R (Contribution to Tolerance)**
```
%Gage R&R = (Gage R&R / Tolerance) × 100
```

**%Study Variation**
```
%Study Var = (Gage R&R / Total Observed Variation) × 100
```

**Number of Distinct Categories (ndc)**
```
ndc = 1.41 × (Part Variation / Gage R&R)
```

### Acceptance Criteria

| Metric | Excellent | Acceptable | Unacceptable |
|--------|-----------|------------|--------------|
| %Gage R&R | < 10% | 10-30% | > 30% |
| ndc | ≥ 5 | 3-4 | < 3 |

**Guidelines**:
- **< 10%**: Excellent measurement system
- **10-30%**: May be acceptable depending on application
- **> 30%**: Measurement system needs improvement

### Interpreting Results

**High Repeatability Error**:
- Gage problem (worn, damaged)
- Poor technique
- Environmental conditions
- Part positioning

**High Reproducibility Error**:
- Training differences
- Different techniques
- Unclear procedures
- Operator-to-operator variation

## Other MSA Studies

### Accuracy Study (Bias)

**Purpose**: Determine if measurements are systematically off from true value.

**Method**:
1. Obtain reference standard with known value
2. Measure multiple times (20-25)
3. Calculate average of measurements
4. Compare to known value

**Bias = Average Measured Value - Reference Value**

**Acceptance**: Bias should be statistically zero or < 10% of tolerance

### Linearity Study

**Purpose**: Determine if accuracy is consistent across measurement range.

**Method**:
1. Obtain 5+ reference standards across the range
2. Measure each multiple times
3. Calculate bias at each level
4. Plot bias vs. reference value
5. Assess if bias changes with size

**Acceptance**: Slope should be statistically zero (no significant linearity)

### Stability Study

**Purpose**: Determine if measurement system is stable over time.

**Method**:
1. Select master part
2. Measure periodically over time
3. Plot on control chart
4. Check for out-of-control conditions

**Acceptance**: Control chart should show stability (no trends, shifts)

## Attribute MSA

For pass/fail, classification, or go/no-go measurements.

### Attribute Agreement Analysis

**Purpose**: Assess consistency of attribute judgments.

**Method**:
1. Select 30+ parts (mix of good, bad, borderline)
2. Multiple operators classify each part
3. Each operator classifies multiple times
4. Analyze agreement

**Metrics**:
- **Within-Appraiser Agreement**: Same person, same decision?
- **Between-Appraiser Agreement**: Different people, same decision?
- **Appraiser-to-Standard Agreement**: Matches the correct answer?

**Acceptance Criteria**:
- Kappa > 0.90: Excellent
- Kappa 0.70-0.90: Acceptable
- Kappa < 0.70: Improvement needed

### Common Causes of Poor Attribute MSA
- Unclear criteria (what is a "scratch"?)
- Poor lighting/conditions
- Borderline parts difficult to classify
- Training differences
- Fatigue

## MSA Roadmap

```
Start
  │
  ├── Is measurement continuous or attribute?
  │     │
  │     ├── Continuous → Gage R&R Study
  │     │     │
  │     │     ├── Is it accurate? → Accuracy/Bias Study
  │     │     ├── Is it linear? → Linearity Study
  │     │     └── Is it stable? → Stability Study
  │     │
  │     └── Attribute → Attribute Agreement Analysis
  │
  └── Is MSA acceptable?
        │
        ├── Yes → Proceed with data collection
        │
        └── No → Fix measurement system first
              - Improve gage
              - Improve training
              - Clarify procedures
              - Improve conditions
              - Re-run MSA
```

## Improvement Actions

### For High Repeatability
- Replace/repair gage
- Improve measurement technique
- Better fixtures/positioning
- Control environmental factors
- More specific procedures

### For High Reproducibility
- Standardize procedures
- Additional training
- Simplify measurement process
- Visual standards
- Reduce judgment required

### For Attribute Systems
- Clearer accept/reject criteria
- Visual standards with photos
- Better lighting
- Reference samples
- Training with borderline cases

## MSA Documentation

**Record**:
- Date of study
- Gage identification
- Operators involved
- Parts used
- Study design
- Results and conclusions
- Actions taken

**Frequency**:
- Initially before data collection
- After gage repair/calibration
- Periodically (annually or per schedule)
- When measurement system changes
