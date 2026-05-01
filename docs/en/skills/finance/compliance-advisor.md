---
layout: default
title: "Compliance Advisor"
grand_parent: English
parent: Finance & Analysis
nav_order: 4
lang_peer: /ja/skills/finance/compliance-advisor/
permalink: /en/skills/finance/compliance-advisor/
---

# Compliance Advisor
{: .no_toc }

コンプライアンス・内部統制支援の専門スキル。J-SOX/SOX対応、リスクコントロールマトリクス（RCM）作成、
内部監査計画策定をサポート。内部統制の整備・運用評価から監査対応まで一貫した支援を提供。
日英両言語のテンプレートを提供し、グローバル企業にも対応。COSO内部統制フレームワーク（2013年版）に準拠。

Use when: creating J-SOX/SOX compliance documentation, building risk control matrices,
planning internal audits, or assessing internal control effectiveness.

Triggers: "J-SOX", "SOX", "内部統制", "コンプライアンス", "RCM", "リスクコントロールマトリクス",
"内部監査", "compliance", "internal control", "internal audit", "risk assessment", "COSO"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/compliance-advisor.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/compliance-advisor){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides comprehensive support for compliance, internal controls, and audit activities. It covers J-SOX (Japan) and SOX (US) compliance, Risk Control Matrix (RCM) development, and internal audit planning based on the COSO Internal Control Framework (2013).

### Key Capabilities

| Capability | Description |
|------------|-------------|
| J-SOX/SOX Compliance | Evaluate and document internal controls over financial reporting |
| RCM Development | Build Risk Control Matrices mapping risks to controls |
| Internal Audit | Plan and execute risk-based internal audits |
| Regulatory Response | Assess gaps and create remediation plans |

### Supported Frameworks

- **COSO Internal Control Framework (2013)** - 5 components, 17 principles
- **J-SOX** (金融商品取引法) - Japanese internal control requirements
- **SOX Section 404** - US Sarbanes-Oxley compliance
- **IIA Standards** - Internal audit professional standards

### Supported Languages

- **Japanese (日本語)**: Templates for domestic compliance
- **English**: Templates for global/US compliance

---

## 2. Prerequisites

- Understanding of the organization's business processes and control environment
- Access to relevant process documentation, policies, and prior audit reports
- Knowledge of applicable regulatory requirements (J-SOX, SOX, etc.)

---

## 3. Quick Start

Use this workflow when establishing or evaluating internal controls over financial reporting.

### Step 1: Determine Evaluation Scope

---

## 4. How It Works

Use this workflow when establishing or evaluating internal controls over financial reporting.

### Step 1: Determine Evaluation Scope

Identify the scope of internal control evaluation:

**Scoping Criteria:**

| Criterion | Description | Threshold |
|-----------|-------------|-----------|
| Quantitative | Financial significance | > 5% of consolidated revenue/assets |
| Qualitative | Fraud risk, complexity | High inherent risk areas |
| Locations | Significant subsidiaries | Coverage of 70%+ of key metrics |

**Scope Documentation:**

```markdown

---

## 5. Usage Examples

- **J-SOX/SOX Compliance**
- "J-SOX対応の評価範囲を決定したい"
- "Create SOX Section 404 documentation"
- **RCM Development**
- "リスクコントロールマトリクスを作成してください"
- "Build an RCM for the procure-to-pay process"

---

## 6. Understanding the Output

This skill provides **conversational guidance and advisory support**. It does not generate standalone files automatically. Outputs include:

- Compliance assessment recommendations and gap analyses
- Risk Control Matrix structures and content guidance
- Internal audit planning frameworks and procedures
- Regulatory response strategies and remediation advice

Templates in `assets/` can be used as starting points when formal documentation is needed.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/compliance-advisor/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: risk_assessment_guide.md, internal_control_methodology.md, jsox_sox_framework.md.
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

- `skills/compliance-advisor/references/internal_control_methodology.md`
- `skills/compliance-advisor/references/jsox_sox_framework.md`
- `skills/compliance-advisor/references/risk_assessment_guide.md`
