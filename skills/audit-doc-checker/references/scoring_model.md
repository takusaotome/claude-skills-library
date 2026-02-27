# Scoring Model — Audit Document Quality Checker

This document defines the scoring model used to calculate the quality score for audit-related documents.

---

## 1. Category Point Allocation

Total: 100 points across 12 categories.

| # | Category | Points | Weight Rationale |
|---|---|---|---|
| 1 | Terminology Consistency | 10 | Communication clarity affects all stakeholders |
| 2 | Currency/Unit Consistency | 10 | Quantitative accuracy is fundamental to audit work |
| 3 | Accounting Standards Alignment | 15 | Core compliance — incorrect standard invalidates the entire document |
| 4 | Section Numbering/Cross-References | 5 | Navigation aid; lower impact on substance |
| 5 | Control Logic Consistency | 15 | Core substance — contradictory controls create audit gaps |
| 6 | Materiality Criteria Application | 10 | Threshold framework drives control design decisions |
| 7 | Assertion Coverage | 10 | Fundamental audit requirement — gaps are material weaknesses |
| 8 | SoD Analysis Presence | 5 | Important but binary (present or absent) |
| 9 | Open Items Management | 10 | Intellectual honesty and risk transparency |
| 10 | Preventive/Detective Classification | 5 | Best practice but not always required in early-stage documents |
| 11 | Success Criteria Definition | 5 | Important for roadmap execution but secondary to control design |
| 12 | Metadata Freshness | 5 | Administrative quality; low impact on substance |

---

## 2. Severity-Based Deduction Rules

For each finding, deduct points from the relevant category:

| Severity | Deduction per Finding | Meaning |
|---|---|---|
| **High** | -5 points | Audit risk — could lead to material misstatement or regulatory non-compliance |
| **Medium** | -3 points | Quality gap — reduces reliability but not immediately dangerous |
| **Low** | -1 point | Cosmetic — formatting or minor inconsistency |

### Floor Rule

Each category score has a **floor of 0**. A category cannot receive a negative score regardless of the number of findings.

Example: Category 3 (Accounting Standards Alignment, 15 pts) with 4 High findings:
- Raw deduction: 4 × -5 = -20
- Floor applied: max(15 - 20, 0) = **0 points**

### No Ceiling Bonus

No category can exceed its allocated points. Finding zero issues in a category results in the full point allocation — no bonus points are awarded.

---

## 3. Total Score Calculation

```
Total Score = Σ max(Category_Points[i] - Σ Deductions[i], 0) for i in 1..12
```

### Score Tiers

| Tier | Score Range | Label | Interpretation |
|---|---|---|---|
| A | 90-100 | High Quality | Document is audit-ready with minor polish |
| B | 70-89 | Improvement Recommended | Fundamentally sound; address Medium/High findings |
| C | 50-69 | Revision Required | Significant gaps undermine reliability |
| D | 0-49 | Critical Risk | Document is not audit-ready; rebuild required |

---

## 4. Document-Type Weighting Adjustments

Different document types have different priority categories. Weighting is applied by multiplying each category's deduction points by a multiplier **before** subtracting from the category's base allocation.

### Multiplier Rules

| Classification | Multiplier | Effect |
|---|---|---|
| **Priority category** | ×1.5 | Deductions hit harder (a High finding costs 7.5 pts instead of 5) |
| **Standard category** | ×1.0 | No change (default) |
| **Lower-priority category** | ×0.5 | Deductions are halved (a High finding costs 2.5 pts instead of 5) |

**Calculation**:
```
Weighted_Deduction = Σ (Severity_Deduction × Multiplier) for each finding in the category
Category_Score = max(Category_Base_Points - Weighted_Deduction, 0)
Total_Score = Σ Category_Score for all 12 categories
```

Note: Multipliers apply to deductions only. Base point allocations remain unchanged.

### Control Design Document

| Category | Classification | Multiplier | Rationale |
|---|---|---|---|
| 5. Control Logic | Priority | ×1.5 | Core content of the document |
| 7. Assertion Coverage | Priority | ×1.5 | Must be comprehensive |
| 8. SoD Analysis | Priority | ×1.5 | Expected to be thorough |
| 11. Success Criteria | Lower priority | ×0.5 | May be in a separate roadmap |
| 12. Metadata Freshness | Lower priority | ×0.5 | Less critical for working drafts |
| All others | Standard | ×1.0 | |

### Bottleneck Analysis / Risk Assessment

| Category | Classification | Multiplier | Rationale |
|---|---|---|---|
| 3. Accounting Standards | Priority | ×1.5 | Risk context depends on correct standard |
| 5. Control Logic | Priority | ×1.5 | Recommended controls must be logically sound |
| 6. Materiality Criteria | Priority | ×1.5 | Impact assessment requires materiality |
| 8. SoD Analysis | Lower priority | ×0.5 | May not be the focus |
| 10. Classification | Lower priority | ×0.5 | May not apply |
| All others | Standard | ×1.0 | |

### Requirements Definition

| Category | Classification | Multiplier | Rationale |
|---|---|---|---|
| 3. Accounting Standards | Priority | ×1.5 | Requirements must reflect correct standard |
| 6. Materiality Criteria | Priority | ×1.5 | System thresholds must align |
| 9. Open Items | Priority | ×1.5 | Requirements often have many TBDs |
| 5. Control Logic | Lower priority | ×0.5 | Controls may not be defined yet |
| 8. SoD Analysis | Lower priority | ×0.5 | Typically addressed in design phase |
| All others | Standard | ×1.0 | |

### Process Inventory (As-Is / To-Be)

| Category | Classification | Multiplier | Rationale |
|---|---|---|---|
| 1. Terminology | Priority | ×1.5 | Process naming is critical |
| 4. Section Numbering | Priority | ×1.5 | Process IDs must be sequential |
| 9. Open Items | Priority | ×1.5 | Many items may need confirmation |
| 5. Control Logic | Lower priority | ×0.5 | Controls not yet designed |
- Category 7: Assertion Coverage — not applicable to process inventory

---

## 5. Multiple Finding Interaction Rules

### Same Category, Same Location

If multiple findings in the same category relate to the same document location, count the highest severity only to avoid over-penalizing a single issue.

Example: A paragraph has both a terminology inconsistency (Medium, -3) and a currency inconsistency (High, -5) — count both because they are different categories. But if the same paragraph has two terminology issues, count only the higher-severity one.

### Systemic Issues

If a finding appears in 5+ locations within the same category, treat it as a single systemic finding at one severity level higher than individual occurrences (capped at High).

Example: The same abbreviation is used without definition in 7 locations — instead of 7 × Low (-1), treat as 1 × Medium (-3) systemic finding.

---

## 6. Review Output Scoring Example

### Input: Control Design Document with the following findings

| # | Severity | Category | Description |
|---|---|---|---|
| 1 | High | 3 | J-GAAP standard cited but document claims US GAAP |
| 2 | High | 5 | Cut-off rule is TBD but expected outcome says "established" |
| 3 | Medium | 1 | "External auditor" and "audit firm" used interchangeably |
| 4 | Medium | 6 | Performance Materiality not defined |
| 5 | Medium | 7 | Cut-off assertion has no direct KPI |
| 6 | Low | 4 | Change log references section 8.1 instead of 8.3 |
| 7 | Low | 12 | Version metadata says v4 but content is v5 |

### Score Calculation

| Category | Points | Deduction | Score |
|---|---|---|---|
| 1. Terminology | 10 | -3 (1 Medium) | 7 |
| 2. Currency/Unit | 10 | 0 | 10 |
| 3. Accounting Standards | 15 | -5 (1 High) | 10 |
| 4. Section Numbering | 5 | -1 (1 Low) | 4 |
| 5. Control Logic | 15 | -5 (1 High) | 10 |
| 6. Materiality | 10 | -3 (1 Medium) | 7 |
| 7. Assertion Coverage | 10 | -3 (1 Medium) | 7 |
| 8. SoD Analysis | 5 | 0 | 5 |
| 9. Open Items | 10 | 0 | 10 |
| 10. Classification | 5 | 0 | 5 |
| 11. Success Criteria | 5 | 0 | 5 |
| 12. Metadata | 5 | -1 (1 Low) | 4 |
| **Total** | **100** | **-21** | **84** |

**Result: 84/100 — Improvement Recommended (Tier B)**

Priority actions: Fix accounting standard reference (High), resolve control logic contradiction (High), then address Medium findings.
