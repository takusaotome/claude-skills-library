---
layout: default
title: "ESG Reporter"
grand_parent: English
parent: Finance & Analysis
nav_order: 6
lang_peer: /ja/skills/finance/esg-reporter/
permalink: /en/skills/finance/esg-reporter/
---

# ESG Reporter
{: .no_toc }

ESG(環境・社会・ガバナンス)レポート作成支援スキル。GRI、SASB、TCFD、CDP等の国際基準に準拠した
サステナビリティレポート作成、マテリアリティ分析、KPI設定、データ収集・開示をサポート。
Use when creating sustainability reports, conducting materiality assessments, setting ESG targets,
or preparing disclosures aligned with GRI, SASB, TCFD, CDP, or CSRD standards.
Triggers: "ESG report", "sustainability report", "TCFD", "GRI", "SASB", "CDP", "materiality assessment", "carbon footprint".

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/esg-reporter.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/esg-reporter){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides professional ESG (Environmental, Social, Governance) reporting and sustainability disclosure support. Helps organizations create comprehensive sustainability reports aligned with international standards including GRI, SASB, TCFD, CDP, and emerging EU CSRD (Corporate Sustainability Reporting Directive).

**Primary language**: Japanese (default), English supported
**Standards Supported**: GRI, SASB, TCFD, CDP, CSRD/ESRS, ISSB (IFRS S1/S2)
**Output format**: Sustainability reports, materiality matrices, ESG KPI dashboards, TCFD disclosures, CDP responses

---

---

## 2. Prerequisites

- **Data Requirements**:
  - Energy consumption data (electricity, fuel, natural gas)
  - Emissions data or source data to calculate Scope 1, 2, and 3 emissions
  - Water and waste management data
  - Employee demographics and safety records (for social metrics)
  - Governance policies and board composition

- **Optional Tools**:
  - Python 3.x with pandas (for data processing)
  - Access to emission factor databases (IPCC, EPA, IEA)

- **Knowledge Prerequisites**:
  - Basic understanding of ESG concepts
  - Access to company operational data

---

---

## 3. Quick Start

```bash
┌─────────────────────────────────────────────────────────────────┐
│                    ESG REPORTING WORKFLOW                        │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  MATERIALITY  │    │ DATA COLLECT  │    │   FRAMEWORK   │
│  ASSESSMENT   │    │ & MANAGEMENT  │    │   SELECTION   │
│  (Workflow 1) │    │  (Workflow 2) │    │ (GRI/TCFD/CDP)│
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        └─────────────────────┼─────────────────────┘
                              ▼
        ┌─────────────────────────────────────────┐
        │           REPORT GENERATION              │
        │  ┌─────────┬──────────┬───────────────┐ │
        │  │  TCFD   │   GRI    │     CDP       │ │
        │  │  Report │  Report  │   Response    │ │
        │  │(Wkfl 3) │(Wkfl 4)  │  (Wkfl 5)     │ │
        │  └─────────┴──────────┴───────────────┘ │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │        ASSURANCE & PUBLICATION           │
        │   Third-party verification → Publish     │
        └─────────────────────────────────────────┘
```

---

## 4. How It Works

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/esg-reporter/references/emission-factors.md`
- `skills/esg-reporter/references/gri-standards-guide.md`
- `skills/esg-reporter/references/tcfd-framework.md`

**Scripts:**

- `skills/esg-reporter/scripts/calculate_emissions.py`
