---
layout: default
title: "Audit Doc Checker"
grand_parent: English
parent: Finance & Analysis
nav_order: 3
lang_peer: /ja/skills/finance/audit-doc-checker/
permalink: /en/skills/finance/audit-doc-checker/
---

# Audit Doc Checker
{: .no_toc }

Review audit-related documents (control design documents, bottleneck analyses, requirements definitions, etc.) for quality, scoring them 0-100 with a severity-rated findings list. Use when reviewing audit documents, checking control design quality, or verifying cross-document consistency. Supports documents governed by US GAAP, IFRS, or J-GAAP.

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/audit-doc-checker.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/audit-doc-checker){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill reviews audit-related documents against 12 quality check categories and produces a structured quality score (0-100) with a detailed findings list. Each finding includes severity (High/Medium/Low), location in the document, description, and recommended fix.

---

## 2. Prerequisites

None. This is a knowledge-based skill that uses reference documents to guide the review.

---

## 3. Quick Start

### Step 1: Identify the Target Document

Read the document to be reviewed. Determine the document type:

---

## 4. How It Works

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

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Reviewing a control design document before submission to external auditors
- Checking the quality of a bottleneck analysis or risk assessment report
- Verifying consistency across audit-related documentation (terminology, currency, accounting standards)
- Validating that a document covers all required audit assertions (C/A/V/CO/E)
- Ensuring open questions and TBD items are properly tracked
- Pre-publication quality gate for any document that will be used in an audit context

---

## 6. Understanding the Output

The output follows the template in `assets/review_output_template.md` and includes:

- **Total Score**: 0-100 with quality tier label
- **Score Tiers**: 90+ (High Quality), 70-89 (Improvement Recommended), 50-69 (Revision Required), <50 (Critical Risk)
- **Category Breakdown**: Per-category score and finding count
- **Findings Table**: Severity, category, location, description, recommended fix
- **Overall Assessment**: 1-2 paragraph summary with prioritized action items

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/audit-doc-checker/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: scoring_model.md, check_rules.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/finance/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.

---

## 10. Reference

**References:**

- `skills/audit-doc-checker/references/check_rules.md`
- `skills/audit-doc-checker/references/scoring_model.md`
