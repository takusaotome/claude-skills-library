---
layout: default
title: "PCI DSS Compliance Consultant"
grand_parent: English
parent: Finance & Analysis
nav_order: 15
lang_peer: /ja/skills/finance/pci-dss-compliance-consultant/
permalink: /en/skills/finance/pci-dss-compliance-consultant/
---

# PCI DSS Compliance Consultant
{: .no_toc }

PCI DSS 4.0.1 compliance audit support skill. Provides expert guidance for Cardholder Data Environment (CDE) scoping, gap analysis, audit preparation, SAQ completion support, and remediation planning. Includes SOC 2 mapping for combined audit efficiency. Use when preparing for PCI DSS audits, conducting gap analysis, creating remediation plans, or answering SAQ questionnaires for payment card compliance.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/pci-dss-compliance-consultant.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/pci-dss-compliance-consultant){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides comprehensive support for organizations preparing for PCI DSS (Payment Card Industry Data Security Standard) compliance assessments. It covers all 12 requirements of PCI DSS 4.0.1 and includes integration with SOC 2 for organizations pursuing combined audits.

### Key Dates

| Milestone | Date | Impact |
|-----------|------|--------|
| PCI DSS 3.2.1 Retirement | April 1, 2024 | v4.0 mandatory |
| v4.0.1 Release | June 2024 | Minor clarifications |
| Future-Dated Requirements | March 31, 2025 | 51 requirements become mandatory |

### Compliance Levels (Annual Transaction Volume)

| Level | Visa/Mastercard | Assessment Type |
|-------|-----------------|-----------------|
| Level 1 | 6M+ transactions | On-site QSA assessment |
| Level 2 | 1M - 6M transactions | SAQ + quarterly scans |
| Level 3 | 20K - 1M e-commerce | SAQ + quarterly scans |
| Level 4 | < 20K e-commerce | SAQ + quarterly scans |

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

### 1. Scoping and Gap Analysis

**Purpose**: Define CDE boundaries and identify compliance gaps

---

## 4. How It Works

### 1. Scoping and Gap Analysis

**Purpose**: Define CDE boundaries and identify compliance gaps

**Process**:
1. Identify all systems that store, process, or transmit cardholder data
2. Map data flows and identify connected systems
3. Review current security controls against each PCI DSS requirement
4. Document gaps with severity and remediation priority
5. Generate gap analysis report

**Reference**: Load `references/gap_analysis_template.md` for structured analysis

**Key Questions**:
- Where does cardholder data enter your environment?
- How does it flow through systems?
- Where is it stored (even temporarily)?
- Who/what has access to it?
- How is it transmitted externally?

### 2. Requirement Guidance

**Purpose**: Provide detailed explanations of PCI DSS requirements

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- **Prepare for QSA audits** - Get comprehensive checklists and evidence requirements
- **Conduct gap analysis** - Compare current security posture against PCI DSS 4.0.1 requirements
- **Understand specific requirements** - Get detailed explanations of any of the 281 sub-requirements
- **Select appropriate SAQ type** - Determine which Self-Assessment Questionnaire applies
- **Create remediation plans** - Develop prioritized action plans for compliance gaps
- **Map to SOC 2** - Identify overlapping controls for combined audit efficiency

---

## 6. Understanding the Output

### Compliance Report
Use `assets/compliance_report_template.md` for:
- Executive summary
- Scope description
- Requirement-by-requirement status
- Gap summary
- Recommendations

### Remediation Plan
Use `assets/remediation_plan_template.md` for:
- Gap identification
- Remediation actions
- Resource requirements
- Timeline
- Success criteria

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/pci-dss-compliance-consultant/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: gap_analysis_template.md, evidence_collection_guide.md, audit_preparation_checklist.md.
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
- Confirm the expected Python version and required packages are installed in the active environment.

---

## 10. Reference

**References:**

- `skills/pci-dss-compliance-consultant/references/audit_preparation_checklist.md`
- `skills/pci-dss-compliance-consultant/references/evidence_collection_guide.md`
- `skills/pci-dss-compliance-consultant/references/gap_analysis_template.md`
- `skills/pci-dss-compliance-consultant/references/pci_dss_4_requirements.md`
- `skills/pci-dss-compliance-consultant/references/saq_selection_guide.md`
- `skills/pci-dss-compliance-consultant/references/soc2_pci_mapping.md`
