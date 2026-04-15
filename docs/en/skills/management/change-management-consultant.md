---
layout: default
title: "Change Management Consultant"
grand_parent: English
parent: Project & Business
nav_order: 8
lang_peer: /ja/skills/management/change-management-consultant/
permalink: /en/skills/management/change-management-consultant/
---

# Change Management Consultant
{: .no_toc }

組織変革管理の専門コンサルタントスキル。システム導入、組織変革、DXプロジェクトにおける変革管理を支援。
ADKAR、Kotter 8-Stepフレームワークに基づき、ステークホルダー影響度分析、コミュニケーション計画、抵抗管理戦略を提供。
Use when managing organizational change, system implementations, digital transformation projects, or improving user adoption rates.
Triggers: "change management", "organizational change", "system implementation", "user adoption", "change strategy", "stakeholder engagement".

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/change-management-consultant.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/change-management-consultant){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill transforms you into an expert change management consultant capable of planning, implementing, and sustaining organizational changes. By leveraging proven frameworks like ADKAR and Kotter's 8-Step Process, you can help organizations successfully navigate system implementations, business transformations, and cultural shifts.

**Primary language**: Japanese (default), English supported
**Frameworks**: ADKAR, Kotter 8-Step, Prosci Methodology
**Output format**: Change management plans, stakeholder analysis, communication strategies, training plans

---

---

## 2. Prerequisites

- **Stakeholder information**: List of key stakeholders, their roles, and departments
- **Project scope**: Clear understanding of what is changing (system, process, structure)
- **Timeline**: Project milestones and target go-live date
- **Organizational context**: Company culture, past change history, current challenges
- **Executive sponsorship**: Identified project sponsor with authority

**Optional but helpful**:
- Organization chart
- Previous change initiative outcomes
- Employee survey data
- Current training infrastructure

---

---

## 3. Quick Start

```bash
1. Readiness Assessment → 2. Stakeholder Analysis → 3. Communication Planning
                                    ↓
                         4. Resistance Management
                                    ↓
                    5. Training & Capability Building
                                    ↓
                      6. Metrics & Measurement
```

---

## 4. How It Works

This skill provides 6 core workflows that can be executed individually or combined:

| # | Workflow | Purpose | Key Output |
|---|----------|---------|------------|
| 1 | Change Readiness Assessment | Evaluate organization's preparedness | Readiness score (0-10), mitigation plan |
| 2 | Stakeholder Analysis | Identify and analyze stakeholders | Stakeholder map, engagement strategies |
| 3 | Communication Planning | Develop communication strategy | Communication calendar, key messages |
| 4 | Resistance Management | Address opposition to change | Resistance analysis, conversion tactics |
| 5 | Training & Capability Building | Ensure skills for new state | Training needs matrix, training plan |
| 6 | Change Metrics & Measurement | Track progress and success | Dashboard, KPIs, adoption tracking |

**Typical execution flow**:
```
1. Readiness Assessment → 2. Stakeholder Analysis → 3. Communication Planning
                                    ↓
                         4. Resistance Management
                                    ↓
                    5. Training & Capability Building
                                    ↓
                      6. Metrics & Measurement
```

---

## 5. Usage Examples

- Planning system implementations (ERP, CRM, new technology)
- Managing organizational restructuring or M&A integration
- Leading digital transformation initiatives
- Improving user adoption rates for new processes or systems
- Addressing resistance to change
- Developing change readiness and capability

---

## 6. Understanding the Output

This skill produces the following deliverables:

| Deliverable | Format | Description |
|-------------|--------|-------------|
| Change Management Plan | Markdown | Comprehensive plan covering all aspects of change |
| Stakeholder Engagement Plan | Markdown table | Power/Interest mapping with engagement strategies |
| Communication Calendar | Markdown table | Timeline of communications with audience and channel |
| ADKAR Assessment | Markdown | Individual/group assessment against ADKAR model |
| Training Needs Matrix | Markdown table | Gap analysis with training recommendations |
| Change Dashboard | Markdown | Progress metrics and status indicators |
| Resistance Management Plan | Markdown | Resistance sources and mitigation strategies |

**Example command execution**:

```bash
# Generate ADKAR assessment for a stakeholder group
python3 skills/change-management-consultant/scripts/adkar_assessment.py \
  --stakeholder "Sales Team" \

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/change-management-consultant/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: adkar_framework.md, kotter_8_step.md, resistance_patterns.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: stakeholder_analyzer.py, readiness_calculator.py, adkar_assessment.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/management/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/change-management-consultant/references/adkar_framework.md`
- `skills/change-management-consultant/references/kotter_8_step.md`
- `skills/change-management-consultant/references/resistance_patterns.md`

**Scripts:**

- `skills/change-management-consultant/scripts/adkar_assessment.py`
- `skills/change-management-consultant/scripts/readiness_calculator.py`
- `skills/change-management-consultant/scripts/stakeholder_analyzer.py`
