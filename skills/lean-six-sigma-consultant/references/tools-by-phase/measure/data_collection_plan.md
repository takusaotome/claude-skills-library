# Data Collection Plan Guide

## Overview

A Data Collection Plan is a structured approach to gathering data needed for analysis in a Six Sigma project. It ensures data is collected consistently, accurately, and in sufficient quantity to support valid conclusions.

## Purpose

- Define exactly what data to collect
- Establish consistent measurement methods
- Determine sample sizes and frequency
- Assign responsibilities
- Ensure data quality and reliability

## Key Components

### 1. Operational Definitions

**What it is**: A precise, unambiguous description of what to measure and how to measure it.

**Why important**: Without clear definitions, different people measure differently, leading to unreliable data.

**Elements of an Operational Definition**:
- What is being measured
- How to measure it
- Units of measurement
- Measurement method/tool
- Criteria for classification

**Example - Defining "Defect"**:
```
Poor Definition: "A defect is a quality problem"

Good Definition: "A defect is any unit that fails one or more of the
following inspection criteria:
- Scratch visible to naked eye > 2mm in length
- Dimension outside specification (10.0 mm ± 0.1 mm)
- Missing component per BOM
Measured by: Visual inspection under standard lighting
Recorded as: Pass/Fail for each criterion"
```

**Example - Defining "Cycle Time"**:
```
Poor Definition: "How long it takes to process"

Good Definition: "Cycle time is measured from the moment a request
enters the queue (timestamp in system) to the moment the completed
work is submitted (submission timestamp), measured in minutes,
excluding weekends and holidays."
```

### 2. Data Types

Understanding data types determines analysis methods:

#### Continuous Data (Variables)
- Measured on a continuous scale
- Can take any value within a range
- Examples: time, weight, temperature, length
- Analysis: Mean, standard deviation, control charts (X-bar/R)
- **Preferred**: More information per data point

#### Discrete/Attribute Data
**Count Data**:
- Defects per unit (can be > 1 per unit)
- Examples: Scratches per panel, errors per form
- Analysis: C-chart, U-chart

**Classification Data**:
- Pass/Fail, Yes/No categories
- Examples: Defective/Non-defective, On-time/Late
- Analysis: P-chart, NP-chart

### 3. Sample Size Determination

#### For Continuous Data
Sample size depends on:
- Desired precision (margin of error)
- Confidence level (typically 95%)
- Estimated standard deviation

**Rule of Thumb**:
- Minimum 30 data points for baseline
- More is better for detecting small changes
- Consider subgroups for stratification

**Formula** (for estimating mean):
```
n = (Z × σ / E)²
Where:
n = sample size
Z = Z-value for confidence level (1.96 for 95%)
σ = estimated standard deviation
E = desired margin of error
```

#### For Attribute Data
Sample size depends on:
- Expected proportion
- Desired precision
- Confidence level

**Rule of Thumb**:
- Minimum 50 defectives to estimate proportion
- Larger samples for lower defect rates

**Formula** (for proportions):
```
n = (Z² × p × (1-p)) / E²
Where:
p = expected proportion
E = desired margin of error
```

### 4. Sampling Strategy

#### Random Sampling
- Every item has equal chance of selection
- Best for unbiased representation
- Use random number generator

#### Stratified Sampling
- Divide population into subgroups (strata)
- Sample from each stratum
- Useful when subgroups may differ

**Stratification Variables**:
- Shift (1st, 2nd, 3rd)
- Machine/equipment
- Operator
- Product type
- Day of week
- Time period

#### Systematic Sampling
- Sample every nth item
- Easy to implement
- Risk: Patterns in data may bias results

#### Consecutive Sampling
- Sample all items in a period
- Good for process studies
- May miss variation over time

### 5. Data Collection Form

**Elements to Include**:
- Date and time
- Person collecting data
- Location/machine/line
- Stratification factors
- Measurement values
- Notes/observations

**Example Form**:
```
┌────────────────────────────────────────────────────────────┐
│ DATA COLLECTION FORM - [Process Name]                      │
├────────────────────────────────────────────────────────────┤
│ Date: __________ Time: __________ Collector: _________     │
│ Shift: [ ] 1st  [ ] 2nd  [ ] 3rd                          │
│ Machine: __________ Product: __________                    │
├──────┬───────────┬───────────┬───────────┬────────────────┤
│ Item │ Measure 1 │ Measure 2 │ Pass/Fail │ Notes          │
├──────┼───────────┼───────────┼───────────┼────────────────┤
│  1   │           │           │           │                │
│  2   │           │           │           │                │
│  3   │           │           │           │                │
└──────┴───────────┴───────────┴───────────┴────────────────┘
```

## Data Collection Plan Template

| Element | Specification |
|---------|--------------|
| **Metric** | [Name of measure] |
| **Operational Definition** | [Precise definition] |
| **Data Type** | [ ] Continuous [ ] Discrete |
| **Measurement Tool** | [Equipment/method] |
| **Sample Size** | [n = X] |
| **Sampling Frequency** | [Every hour / daily / etc.] |
| **Stratification** | [By shift, machine, etc.] |
| **Collection Period** | [Start date to end date] |
| **Responsible Person** | [Name] |
| **Data Storage** | [Where data is recorded] |

## Detailed Example

### Project: Reduce Order Processing Errors

| Element | Input Data (X) | Output Data (Y) |
|---------|---------------|-----------------|
| **Metric** | Order completeness | Order accuracy rate |
| **Op. Definition** | % of required fields completed on order form | % of orders processed without errors |
| **Data Type** | Continuous (%) | Discrete (Pass/Fail) |
| **Measurement** | Field count in system | QC audit checklist |
| **Sample Size** | All orders (census) | 200 orders |
| **Frequency** | Daily | Weekly sample |
| **Stratification** | By region, order type | By region, processor |
| **Period** | 4 weeks | 4 weeks |
| **Responsible** | IT system | QC team |
| **Storage** | Database report | Excel tracker |

## Data Quality Assurance

### Before Collection
- [ ] Operational definitions reviewed and approved
- [ ] Data collectors trained
- [ ] Forms/systems tested
- [ ] MSA completed (if applicable)
- [ ] Pilot run conducted

### During Collection
- [ ] Daily/weekly data review
- [ ] Check for completeness
- [ ] Verify stratification captured
- [ ] Monitor for collection issues
- [ ] Address questions promptly

### After Collection
- [ ] Data validation and cleaning
- [ ] Check for outliers
- [ ] Verify sample size achieved
- [ ] Document data issues

## Common Mistakes

1. **Vague definitions**: Different interpretations lead to inconsistent data
2. **Insufficient sample size**: Can't detect real differences
3. **No stratification**: Miss important subgroup differences
4. **Biased sampling**: Non-representative data
5. **Poor data forms**: Missing or unclear fields
6. **No pilot test**: Discover problems too late
7. **Inconsistent timing**: Collection varies by person/time
8. **Not validating measurement system**: Data quality unknown

## Tips for Success

1. **Keep it simple**: Collect what you need, not everything
2. **Test first**: Pilot the collection process
3. **Train collectors**: Ensure everyone measures the same way
4. **Automate where possible**: System data is more consistent
5. **Stratify early**: Capture variables even if not sure they matter
6. **Review regularly**: Catch problems during collection
7. **Document everything**: Assumptions, issues, decisions
