---
name: audit-doc-checker
description: >
  Review audit-related documents (control design documents, bottleneck analyses,
  requirements definitions, etc.) for quality, scoring them 0-100 with a severity-rated
  findings list. Use when reviewing audit documents, checking control design quality,
  or verifying cross-document consistency. Supports documents governed by US GAAP,
  IFRS, or J-GAAP.
---

# Audit Document Quality Checker

## Overview

This skill reviews audit-related documents against 12 quality check categories and produces a structured quality score (0-100) with a detailed findings list. Each finding includes severity (High/Medium/Low), location in the document, description, and recommended fix.

## When to Use

- Reviewing a control design document before submission to external auditors
- Checking the quality of a bottleneck analysis or risk assessment report
- Verifying consistency across audit-related documentation (terminology, currency, accounting standards)
- Validating that a document covers all required audit assertions (C/A/V/CO/E)
- Ensuring open questions and TBD items are properly tracked
- Pre-publication quality gate for any document that will be used in an audit context

## Prerequisites

None. This is a knowledge-based skill that uses reference documents to guide the review.

## Workflow

### Step 1: Identify the Target Document

Read the document to be reviewed. Determine the document type:

| Document Type | Description | Priority Categories |
|---|---|---|
| Control Design Document | Internal control procedures, SoD analysis, KPIs | Categories 5, 7, 8 (weighted higher) |
| Bottleneck Analysis | Process bottleneck identification and risk assessment | Categories 3, 5, 6 |
| Requirements Definition | Business or system requirements for audit-related systems | Categories 3, 6, 9 |
| Audit Report | Findings, recommendations, management responses | Categories 1, 9, 12 |
| Process Inventory | As-Is or To-Be process documentation | Categories 4, 9, 11 |

### Step 2: Load Check Rules

Load `references/check_rules.md` to obtain the 12 check categories and their detailed rules.

### Step 3: Analyze Against 12 Categories

Systematically review the document against each of the 12 categories:

1. **Terminology Consistency** (10 pts)
2. **Currency/Unit Consistency** (10 pts)
3. **Accounting Standards Alignment** (15 pts)
4. **Section Numbering/Cross-References** (5 pts)
5. **Control Logic Consistency** (15 pts)
6. **Materiality Criteria Application** (10 pts)
7. **Assertion Coverage** (10 pts)
8. **SoD Analysis Presence** (5 pts)
9. **Open Items Management** (10 pts)
10. **Preventive/Detective Classification** (5 pts)
11. **Success Criteria Definition** (5 pts)
12. **Metadata Freshness** (5 pts)

For each category, record findings with severity:
- **High**: Audit risk — could lead to material misstatement or regulatory non-compliance
- **Medium**: Quality gap — reduces document reliability but not immediately dangerous
- **Low**: Cosmetic — formatting, minor inconsistencies that don't affect substance

### Step 4: Calculate Score

Load `references/scoring_model.md` and apply the scoring model:

1. Determine the document type (Step 1) and look up the multiplier table in `references/scoring_model.md` Section 4
2. For each category, calculate weighted deductions: `Weighted_Deduction = Σ (Severity_Points × Multiplier)` where Severity_Points are High=5, Medium=3, Low=1 and Multiplier is ×1.5 (priority), ×1.0 (standard), or ×0.5 (lower-priority)
3. Calculate category score: `Category_Score = max(Base_Points - Weighted_Deduction, 0)`
4. Sum all 12 category scores for the total (0-100)

### Step 5: Generate Output

Use `assets/review_output_template.md` to format the final output:

1. Score summary table
2. Category-by-category score breakdown
3. Findings list (sorted by severity, then category)
4. Overall assessment paragraph

## Output Format

The output follows the template in `assets/review_output_template.md` and includes:

- **Total Score**: 0-100 with quality tier label
- **Score Tiers**: 90+ (High Quality), 70-89 (Improvement Recommended), 50-69 (Revision Required), <50 (Critical Risk)
- **Category Breakdown**: Per-category score and finding count
- **Findings Table**: Severity, category, location, description, recommended fix
- **Overall Assessment**: 1-2 paragraph summary with prioritized action items

## Quality Tier Definitions

| Tier | Score Range | Meaning | Recommended Action |
|---|---|---|---|
| High Quality | 90-100 | Ready for audit submission | Minor polish only |
| Improvement Recommended | 70-89 | Fundamentally sound but has gaps | Address Medium/High findings |
| Revision Required | 50-69 | Significant gaps that undermine reliability | Major revision before use |
| Critical Risk | 0-49 | Document is not audit-ready | Rebuild with proper framework |

## Resources

| Type | File | Purpose | When to Load |
|------|------|---------|-------------|
| Reference | `references/check_rules.md` | 12 check categories with detailed rules, severity criteria, and examples | Step 3: Load before analyzing the document |
| Reference | `references/scoring_model.md` | Scoring calculation: base points, deduction rules, document-type multipliers, tier definitions | Step 4: Load before calculating score |
| Asset | `assets/review_output_template.md` | Output template with placeholder variables for structured review results | Step 5: Use as output format |

## Integration with audit-control-designer

This skill can be used to review documents generated by the `audit-control-designer` skill. The recommended workflow is:

1. Generate control design with `audit-control-designer`
2. Review the generated document with `audit-doc-checker`
3. Address findings and iterate until score reaches 70+
