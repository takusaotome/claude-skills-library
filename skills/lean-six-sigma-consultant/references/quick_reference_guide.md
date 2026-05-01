# Lean Six Sigma Quick Reference Guide

## Sigma Level Conversion Table

| Sigma Level | DPMO | Yield % | Quality Level |
|-------------|------|---------|---------------|
| 1σ | 691,462 | 30.85% | Non-competitive |
| 2σ | 308,538 | 69.15% | Non-competitive |
| 3σ | 66,807 | 93.32% | Average |
| 4σ | 6,210 | 99.38% | Good |
| 5σ | 233 | 99.977% | Excellent |
| 6σ | 3.4 | 99.9997% | World Class |

**Note**: DPMO values include 1.5σ long-term shift.

## Process Capability Index (Cpk) Guidelines

| Cpk Value | Rating | Action Required |
|-----------|--------|-----------------|
| ≥ 2.00 | Excellent/World Class | Maintain, reduce inspection |
| 1.67 - 2.00 | Good (Six Sigma target) | Monitor, optimize |
| 1.33 - 1.67 | Acceptable | Monitor closely |
| 1.00 - 1.33 | Marginal | Improvement needed |
| 0.67 - 1.00 | Poor | Immediate action, 100% inspection |
| < 0.67 | Unacceptable | Stop production, redesign |

## Formulas

### Sigma Level Calculation
```
DPMO = (Defects / (Units × Opportunities)) × 1,000,000
Yield = 1 - (DPMO / 1,000,000)
Sigma Level = NORMSINV(Yield) + 1.5
```

### Process Capability
```
Cp = (USL - LSL) / (6σ)
Cpk = min[(USL - μ)/(3σ), (μ - LSL)/(3σ)]
```

### Control Chart Constants (X-bar/R)

| n | A₂ | D₃ | D₄ | d₂ |
|---|-----|-----|-----|-----|
| 2 | 1.880 | 0 | 3.267 | 1.128 |
| 3 | 1.023 | 0 | 2.575 | 1.693 |
| 4 | 0.729 | 0 | 2.282 | 2.059 |
| 5 | 0.577 | 0 | 2.115 | 2.326 |

**Control Limit Formulas**:
```
UCL_X = X̄̄ + A₂R̄
LCL_X = X̄̄ - A₂R̄
UCL_R = D₄R̄
LCL_R = D₃R̄
```

## DMAIC Phase Summary

| Phase | Key Question | Key Deliverables | Tollgate Check |
|-------|--------------|------------------|----------------|
| **Define** | What is the problem? | Project Charter, SIPOC, VOC/CTQ | Scope approved, team formed |
| **Measure** | How bad is it now? | Data Collection Plan, Baseline, MSA | Measurement system valid |
| **Analyze** | Why is it happening? | Root Cause Analysis, Statistical Verification | Root causes identified with data |
| **Improve** | What is the solution? | Solution Selection, FMEA, Pilot Results | Solution tested and verified |
| **Control** | How do we sustain it? | Control Plan, SPC, Standard Work | Process owner trained |

## 8 Wastes (DOWNTIME)

| Waste | Definition | Examples | Countermeasures |
|-------|------------|----------|-----------------|
| **D**efects | Rework, scrap, errors | Quality failures | Mistake-proofing (Poka-yoke) |
| **O**verproduction | Making more than needed | Large batches, just-in-case | Pull systems, Kanban |
| **W**aiting | Idle time, delays | Approval delays | Process flow optimization |
| **N**on-utilized Talent | Underused skills | Not engaging employees | Empowerment, Kaizen teams |
| **T**ransportation | Moving materials | Excess shipping | Cellular layout |
| **I**nventory | Excess stock | WIP buildup | JIT, FIFO |
| **M**otion | Unnecessary movement | Walking, reaching | 5S, ergonomics |
| **E**xtra-processing | Over-engineering | Unnecessary features | Value analysis |

## Control Chart Selection Guide

| Data Type | Subgroup | Chart Type |
|-----------|----------|------------|
| Continuous | n = 1 | I-MR (Individuals-Moving Range) |
| Continuous | n = 2-8 | X-bar/R (Mean and Range) |
| Continuous | n > 8 | X-bar/S (Mean and Std Dev) |
| Attribute (defectives) | Variable n | P chart (proportion) |
| Attribute (defectives) | Constant n | NP chart (count) |
| Attribute (defects) | Variable area | U chart (per unit) |
| Attribute (defects) | Constant area | C chart (count) |

## Western Electric Rules (Out-of-Control Detection)

1. **Rule 1**: One point beyond 3σ (UCL/LCL)
2. **Rule 2**: Two of three consecutive points beyond 2σ (same side)
3. **Rule 3**: Four of five consecutive points beyond 1σ (same side)
4. **Rule 4**: Eight consecutive points on one side of center line
5. **Rule 5**: Six consecutive points trending up or down

## Hypothesis Testing Decision Matrix

| Comparison | Test |
|------------|------|
| Two means (normal) | 2-sample t-test |
| Two means (paired) | Paired t-test |
| Multiple means | One-way ANOVA |
| Two proportions | Chi-square / Z-test |
| Relationship | Correlation / Regression |
| Multiple factors | DOE (Factorial) |

**Interpretation**:
- p-value < 0.05: Reject H₀, effect is statistically significant
- p-value ≥ 0.05: Fail to reject H₀, no significant effect

## 5S Methodology

| Step | Japanese | English | Action |
|------|----------|---------|--------|
| 1 | Seiri | Sort | Remove unnecessary items |
| 2 | Seiton | Set in Order | Organize remaining items |
| 3 | Seiso | Shine | Clean and inspect |
| 4 | Seiketsu | Standardize | Create visual standards |
| 5 | Shitsuke | Sustain | Maintain discipline |

## Belt Competency Reference

| Belt | Focus | Statistical Tools |
|------|-------|-------------------|
| White | Awareness | Basic concepts only |
| Yellow | Team support | Fishbone, 5 Whys, Pareto |
| Green | Project leader | Capability, hypothesis testing, SPC |
| Black | Expert leader | DOE, regression, ANOVA, complex analysis |
| Master Black Belt | Strategic | Program deployment, training, mentoring |
