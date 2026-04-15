---
layout: default
title: "BCP Planner"
grand_parent: English
parent: Operations & Docs
nav_order: 5
lang_peer: /ja/skills/ops/bcp-planner/
permalink: /en/skills/ops/bcp-planner/
---

# BCP Planner
{: .no_toc }

事業継続計画（BCP）と災害復旧計画（DRP）の策定支援スキル。ビジネスインパクト分析、リスク評価、復旧戦略策定、
BCP/DRP文書作成、テスト・訓練計画を提供。ISO 22301準拠。
Use when developing business continuity plans, disaster recovery strategies, or conducting business impact analysis.
Triggers: "BCP", "business continuity", "disaster recovery", "DRP", "business impact analysis", "BIA", "contingency planning".

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/bcp-planner.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/bcp-planner){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill transforms you into an expert business continuity planner capable of developing comprehensive BCPs and DRPs. By following ISO 22301 standards and industry best practices, you can help organizations prepare for, respond to, and recover from disruptions.

**Primary language**: Japanese (default), English supported
**Standards**: ISO 22301 (Business Continuity Management)
**Output format**: BCP/DRP documents, BIA reports, test plans, training materials

Use this skill when:
- Developing business continuity plans for organizations
- Conducting Business Impact Analysis (BIA)
- Creating disaster recovery strategies for IT systems
- Planning and conducting BCP/DRP tests and exercises
- Achieving ISO 22301 certification
- Improving organizational resilience

---

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
| Function | Revenue Impact | Customer Impact | Regulatory | Reputation | Overall Criticality |
|----------|----------------|-----------------|------------|------------|---------------------|
| Order Processing | Very High | High | Medium | High | **Critical** |
| Customer Support | Medium | Very High | Low | High | **High** |
| Payroll | Low | Low | High | Medium | **Medium** |
| Marketing | Low | Low | None | Low | **Low** |
```

---

## 4. How It Works

### Workflow 1: Business Impact Analysis (BIA)

**Purpose**: Identify critical business functions and quantify impact of disruption.

#### Step 1: Identify Business Functions

List all business functions/processes:
- **Core Functions**: Revenue-generating, mission-critical
- **Support Functions**: HR, Finance, IT, Legal
- **Management Functions**: Executive management, governance

**Example List**:
- Order Processing
- Customer Support
- Manufacturing
- Shipping/Logistics
- IT Infrastructure
- Payroll
- Financial Reporting

#### Step 2: Assess Criticality

For each function, evaluate:

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Use **BCP Planner** when you need a structured workflow rather than an ad-hoc answer.
- Start with a small representative input before applying the workflow to production data or assets.
- Review the helper scripts and reference guides to tailor the output format to your project.

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Guidance derived directly from the skill instructions.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/bcp-planner/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/ops/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.

---

## 10. Reference

This skill uses built-in Claude capabilities without external scripts or references.
