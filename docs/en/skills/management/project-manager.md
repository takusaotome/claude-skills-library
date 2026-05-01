---
layout: default
title: "Project Manager"
grand_parent: English
parent: Project & Business
nav_order: 20
lang_peer: /ja/skills/management/project-manager/
permalink: /en/skills/management/project-manager/
---

# Project Manager
{: .no_toc }

Professional project management skill aligned with PMBOK® 6th/7th Edition standards. Use this skill when you need to define requirements (ISO/IEC/IEEE 29148), review project plans, generate progress reports with Earned Value Management (EVM), conduct risk analysis, estimate costs, or provide project health assessments. Ideal for creating comprehensive project documentation, analyzing project performance metrics (SPI, CPI, EAC), managing risks across 14 categories, and ensuring stakeholder alignment. Triggers: "create project plan", "analyze project health", "calculate EVM", "risk assessment", "requirements definition", "progress report", "cost estimation", or requests involving PMBOK knowledge areas.

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/project-manager.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/project-manager){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides comprehensive project management capabilities aligned with PMBOK® (Project Management Body of Knowledge) 6th and 7th Edition standards. It integrates proven methodologies, best practices, and templates to support project managers in delivering successful projects on time, within budget, and meeting quality expectations.

The skill is structured around PMBOK's **10 Knowledge Areas** and **5 Process Groups**, with particular emphasis on:

- **Requirements Engineering** (ISO/IEC/IEEE 29148 compliant)
- **Earned Value Management (EVM)** for objective progress tracking
- **Risk Management** using three-phase structured approach
- **Stakeholder Management** and communication planning
- **Cost Estimation and Control** with forecasting
- **Quality Management** with metrics and continuous improvement

This skill is designed for both experienced project managers seeking to standardize their approach and those new to formal project management who need structured guidance.

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
FR-001: User Login
- Priority: Must Have
- User Story: As a customer, I want to log in securely so that I can access my account
- Acceptance Criteria:
  - Given valid credentials
  - When user submits login form
  - Then system authenticates within 2 seconds
  - And logs the event
```

---

## 4. How It Works

Use this workflow when starting a new project or phase requiring detailed requirements documentation.

### Step 1: Understand Project Context

**Ask these questions:**
1. What business problem are we solving?
2. Who are the key stakeholders?
3. What are the business goals and success criteria?
4. What are the constraints (budget, timeline, resources)?
5. Are there regulatory or compliance requirements?

### Step 2: Gather Requirements

**Information Gathering Methods:**
- **Interviews**: One-on-one with stakeholders
- **Workshops**: Facilitated group sessions
- **Surveys**: Structured questionnaires
- **Document Analysis**: Review existing documentation
- **Observation**: Watch current processes
- **Prototyping**: Show mockups to elicit feedback

**Use the Requirements Definition Template** from `assets/requirements_definition_template.md`

### Step 3: Document Requirements

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- **Define Requirements**: "Create a requirements definition document for our CRM implementation project"
- **Review Project Plans**: "Review this project plan and identify risks and missing elements"
- **Generate Progress Reports**: "Create a monthly progress report with EVM analysis"
- **Conduct Risk Analysis**: "Perform a comprehensive risk assessment for this project"
- **Estimate Costs**: "Estimate project costs using bottom-up estimation approach"
- **Assess Project Health**: "Analyze current project health based on these metrics"

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 2 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/project-manager/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: risk_management_guide.md, pmbok_knowledge_areas.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: project_health_check.py.
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
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/project-manager/references/pmbok_knowledge_areas.md`
- `skills/project-manager/references/risk_management_guide.md`

**Scripts:**

- `skills/project-manager/scripts/project_health_check.py`
