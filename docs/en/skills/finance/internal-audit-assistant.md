---
layout: default
title: "Internal Audit Assistant"
grand_parent: English
parent: Finance & Analysis
nav_order: 7
lang_peer: /ja/skills/finance/internal-audit-assistant/
permalink: /en/skills/finance/internal-audit-assistant/
---

# Internal Audit Assistant
{: .no_toc }

Internal audit support skill aligned with IIA (Institute of Internal Auditors) International Standards.
Provides risk-based audit planning, audit program development, workpaper documentation, finding
development (Condition/Criteria/Cause/Effect), and Corrective Action Request (CAR) tracking.
Use when: planning annual/quarterly audits, creating risk assessment matrices, developing audit
programs and test procedures, documenting audit workpapers, writing audit findings and reports,
tracking corrective actions and follow-ups, preparing for external audits (SOX, ISO).
Triggers: "internal audit", "audit plan", "audit program", "audit workpaper", "audit finding",
"risk assessment", "CAR tracking", "corrective action", "IIA Standards", "COSO framework",
"監査計画", "監査プログラム", "監査調書", "是正措置", "リスク評価".

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/internal-audit-assistant.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/internal-audit-assistant){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides professional internal audit support aligned with IIA (Institute of Internal Auditors) International Standards for the Professional Practice of Internal Auditing. Supports risk-based audit planning, audit program development, workpaper documentation, and corrective action tracking.

**Primary language**: Japanese (default), English supported
**Framework**: IIA Standards, COSO Internal Control Framework, ISO 19011 (Audit Guidelines)
**Output format**: Audit plans, audit programs, audit workpapers, CAR (Corrective Action Request) tracking

---

---

## 2. Prerequisites

- **Knowledge**: Basic understanding of internal control frameworks (COSO, IIA Standards)
- **Access**: Organizational data for risk assessment (auditable entity list, prior audit findings)
- **Tools**: None required for documentation; optional Python for risk scoring automation

---

---

## 3. Quick Start

1. **Risk Assessment** → Calculate risk scores for auditable entities using `scripts/risk_scorer.py`
2. **Audit Planning** → Prioritize entities and allocate audit resources
3. **Program Development** → Create detailed audit procedures and test steps
4. **Fieldwork** → Execute audit program, document workpapers
5. **Reporting** → Develop findings with condition/criteria/cause/effect structure
6. **Follow-up** → Track CARs through lifecycle using `scripts/car_tracker.py`

---

## 4. How It Works

1. **Risk Assessment** → Calculate risk scores for auditable entities using `scripts/risk_scorer.py`
2. **Audit Planning** → Prioritize entities and allocate audit resources
3. **Program Development** → Create detailed audit procedures and test steps
4. **Fieldwork** → Execute audit program, document workpapers
5. **Reporting** → Develop findings with condition/criteria/cause/effect structure
6. **Follow-up** → Track CARs through lifecycle using `scripts/car_tracker.py`

---

## 5. Usage Examples

- **Annual audit planning**: "Create FY2025 internal audit plan" or "年次監査計画を作成"
- **Risk assessment**: "Assess risks for the IT department" or "リスク評価マトリクスを作成"
- **Audit program development**: "Create audit program for accounts payable" or "買掛金監査プログラムを作成"
- **Workpaper documentation**: "Help document audit findings" or "監査調書を作成"
- **CAR management**: "Track corrective actions" or "是正措置のフォローアップ"
- **External audit prep**: "Prepare for SOX audit" or "ISO監査の準備"

---

## 6. Understanding the Output

| Deliverable | Format | Description |
|-------------|--------|-------------|
| Risk Assessment Matrix | Markdown table | Weighted risk scores for all auditable entities |
| Annual Audit Plan | Markdown report | Prioritized audit schedule with resource allocation |
| Audit Program | Markdown checklist | Detailed test procedures per audit |
| Audit Workpaper | Markdown document | Test results with evidence references |
| Audit Finding | Markdown document | Condition/Criteria/Cause/Effect/Recommendation structure |
| CAR Status Report | Markdown table | Corrective action tracking dashboard |

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/internal-audit-assistant/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: sampling_guide.md, iia_standards_summary.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: risk_scorer.py, __init__.py, car_tracker.py.
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
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/internal-audit-assistant/references/iia_standards_summary.md`
- `skills/internal-audit-assistant/references/sampling_guide.md`

**Scripts:**

- `skills/internal-audit-assistant/scripts/__init__.py`
- `skills/internal-audit-assistant/scripts/car_tracker.py`
- `skills/internal-audit-assistant/scripts/risk_scorer.py`
