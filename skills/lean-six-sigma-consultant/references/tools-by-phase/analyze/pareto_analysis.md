# Pareto Analysis Guide

## Overview

Pareto Analysis is a prioritization technique based on the Pareto Principle (80/20 rule): approximately 80% of effects come from 20% of causes. It helps focus improvement efforts on the "vital few" factors that will have the greatest impact.

## The Pareto Principle

**Original Observation**: Vilfredo Pareto observed that 80% of Italy's land was owned by 20% of the population.

**Application Examples**:
- 80% of defects come from 20% of defect types
- 80% of complaints come from 20% of customers
- 80% of sales come from 20% of products
- 80% of problems come from 20% of causes

**Important**: The exact ratio may not be 80/20, but the principle of vital few vs. trivial many applies.

---

## Purpose

- **Prioritize**: Focus on most impactful issues
- **Resource allocation**: Direct effort where it matters most
- **Communication**: Visual way to show priorities
- **Decision making**: Data-driven prioritization

---

## How to Create a Pareto Chart

### Step 1: Define Categories
Identify the categories to analyze:
- Defect types
- Problem causes
- Customer complaints
- Error sources
- Failure modes

### Step 2: Collect Data
Count occurrences in each category:
- Use existing data (quality reports, complaints)
- Collect new data (tally sheets)
- Ensure consistent time period

### Step 3: Sort Data
Arrange categories in descending order by frequency.

### Step 4: Calculate Percentages
- Individual percentage: (Count / Total) × 100
- Cumulative percentage: Running sum of percentages

### Step 5: Create Chart
- Bar chart: Categories on X-axis, count on Y-axis
- Line graph: Cumulative percentage
- 80% reference line

---

## Example: Manufacturing Defects

### Raw Data

| Defect Type | Count |
|-------------|-------|
| Scratch | 45 |
| Dimension Error | 28 |
| Missing Part | 15 |
| Color Variation | 8 |
| Surface Finish | 5 |
| Label Error | 3 |
| Other | 6 |
| **Total** | **110** |

### Sorted with Percentages

| Rank | Defect Type | Count | % | Cumulative % |
|------|-------------|-------|---|---------------|
| 1 | Scratch | 45 | 40.9% | 40.9% |
| 2 | Dimension Error | 28 | 25.5% | 66.4% |
| 3 | Missing Part | 15 | 13.6% | 80.0% |
| 4 | Color Variation | 8 | 7.3% | 87.3% |
| 5 | Surface Finish | 5 | 4.5% | 91.8% |
| 6 | Other | 6 | 5.5% | 97.3% |
| 7 | Label Error | 3 | 2.7% | 100.0% |

### Pareto Chart Visualization

```
Count                                          Cumulative %
50 │                                                   100%
   │ ████                                          ──●──
45 │ ████                                        ●
   │ ████                                     ●       80%
40 │ ████                                  ●
   │ ████          ▓▓▓▓                 ●
30 │ ████          ▓▓▓▓              ●                60%
   │ ████          ▓▓▓▓           ●
   │ ████          ▓▓▓▓        ●
20 │ ████          ▓▓▓▓     ●                         40%
   │ ████          ▓▓▓▓  ●  ░░░░
   │ ████          ▓▓▓▓●    ░░░░
10 │ ████          ▓▓▓▓     ░░░░  ▒▒▒▒               20%
   │ ████          ▓▓▓▓     ░░░░  ▒▒▒▒  ████  ░░░░
   │ ████          ▓▓▓▓     ░░░░  ▒▒▒▒  ████  ░░░░  ▓▓▓▓
 0 └────────────────────────────────────────────────  0%
   Scratch  Dimension  Missing  Color  Surface Other Label
            Error      Part     Var    Finish
   └──────── Vital Few ────────┘└───── Trivial Many ─────┘
```

### Interpretation

**Vital Few** (Top 3 categories = 80%):
1. Scratch: 40.9%
2. Dimension Error: 25.5%
3. Missing Part: 13.6%
Total: 80.0%

**Focus**: Eliminating these three defect types would address 80% of defects.

---

## Types of Pareto Charts

### By Count (Frequency)
Most common type - shows how often each category occurs.

### By Cost (Impact)
Weight categories by cost/impact, not just frequency.

**Example**:
| Defect | Count | Cost Each | Total Cost |
|--------|-------|-----------|------------|
| Scratch | 45 | $50 | $2,250 |
| Dimension | 28 | $200 | $5,600 |

Dimension becomes top priority when weighted by cost!

### Stratified Pareto
Create separate Pareto charts for different subgroups:
- By shift
- By machine
- By product
- By location

Reveals if the "vital few" differ by segment.

---

## Second-Level Pareto

### Concept
Drill down into the top category with another Pareto analysis.

### Example

**First Level**: Defect Types
- Top category: Scratch (40.9%)

**Second Level**: Scratch Causes
| Scratch Cause | Count | % |
|---------------|-------|---|
| Handling damage | 20 | 44% |
| Tooling marks | 12 | 27% |
| Material defect | 8 | 18% |
| Other | 5 | 11% |

**Focus**: Address handling damage first within scratch category.

---

## Before/After Pareto

### Purpose
Show improvement by comparing Pareto charts before and after changes.

### Example

**Before**: Total defects = 110
| Defect | Count | % |
|--------|-------|---|
| Scratch | 45 | 40.9% |
| Dimension | 28 | 25.5% |
| Missing Part | 15 | 13.6% |

**After** (addressed scratches): Total defects = 50
| Defect | Count | % |
|--------|-------|---|
| Dimension | 25 | 50.0% |
| Missing Part | 13 | 26.0% |
| Scratch | 8 | 16.0% |

Shows:
- Overall reduction: 110 → 50 (55% reduction)
- Scratch reduced from 45 to 8 (82% reduction)
- Dimension now top priority for next improvement

---

## Best Practices

### Do's
- Use consistent categories
- Specify time period and sample size
- Consider cost/impact weighting
- Stratify to find patterns
- Update after improvements
- Present visually

### Don'ts
- Don't include too many categories (combine small ones as "Other")
- Don't use when all categories are similar (not really Pareto)
- Don't compare across different time periods without normalization
- Don't ignore the "trivial many" completely (may need attention later)
- Don't assume frequencies - use actual data

---

## Pareto Analysis Checklist

- [ ] Categories clearly defined
- [ ] Data collected from representative period
- [ ] Categories sorted by frequency (or cost)
- [ ] Percentages calculated correctly
- [ ] Cumulative line included
- [ ] 80% line marked
- [ ] "Vital few" identified
- [ ] Consider stratification
- [ ] Consider cost weighting
- [ ] Action plan for top categories

---

## Common Mistakes

1. **Too many categories**: Consolidate small categories into "Other"
2. **No cumulative line**: Makes it hard to see 80/20 split
3. **Equal categories**: If all similar, Pareto doesn't apply
4. **Not using cost weighting**: Frequency alone may mislead
5. **Static analysis**: Should be updated as improvements made
6. **Ignoring trivial many**: Eventually these need attention
7. **Mixing units**: Keep categories consistent
8. **Short time period**: May not be representative
