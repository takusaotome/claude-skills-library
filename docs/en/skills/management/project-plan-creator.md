---
layout: default
title: Project Plan Creator
grand_parent: English
parent: Project & Business
nav_order: 1
lang_peer: /ja/skills/management/project-plan-creator/
permalink: /en/skills/management/project-plan-creator/
---

# Project Plan Creator
{: .no_toc }

Create comprehensive, PMBOK-aligned project plans with WBS, Gantt charts, RACI matrices, and risk management -- all in Markdown with Mermaid diagrams.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-workflow">Workflow</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Project Plan Creator transforms project requirements and stakeholder needs into a full set of PMBOK-aligned project management artifacts. It walks you through charter creation, scope definition, WBS development, scheduling with Gantt charts, resource planning with RACI matrices, and risk management planning.

Output is produced in Markdown with Mermaid diagrams, ready for rendering in any Markdown-compatible tool.

The skill is backed by a PM knowledge base of 11 reference files (544 KB) covering PMBOK 6th/7th/8th editions, DevOps/Agile best practices, IT PM guidance, and cross-framework mapping (PMBOK vs PRINCE2, ITIL 4, ISO 21502).

## When to Use

- Starting a new system development or implementation project
- Creating a Project Charter to formally authorize a project
- Developing a comprehensive Project Plan with WBS, schedule, and resource allocation
- Visualizing project structure with Mermaid diagrams (Gantt, WBS, workflows)
- Producing PMBOK-compliant project documentation

## Prerequisites

- Claude Code with the `project-plan-creator` skill installed
- Basic understanding of the project scope and stakeholders
- No external APIs or paid services are needed

## How It Works

The skill guides Claude through 7 sequential workflows:

1. **Project Charter Creation** -- Gather inputs, define objectives, scope, milestones, budget, stakeholders, and success criteria.
2. **Scope Definition & WBS** -- Expand the charter into a detailed scope statement and hierarchical Work Breakdown Structure with Mermaid diagrams.
3. **Schedule Development** -- Define activities, sequence them with dependencies (FS/SS/FF/SF), estimate durations using PERT, and produce a Mermaid Gantt chart with critical path analysis.
4. **Resource Planning & RACI** -- Define project roles, build a RACI matrix, set communication protocols, and visualize the team structure.
5. **Risk Management** -- Identify risks across categories (technical, scope, resource, integration, external), assess probability and impact, plan response strategies, and establish monitoring.
6. **Communication & Quality Planning** -- Define stakeholder communication needs, quality standards, QA process, and acceptance criteria.
7. **Integration & Document Generation** -- Merge all artifacts into a cohesive project plan using a 12-section template with 5+ Mermaid diagrams.

## Usage Examples

### Example 1: Create a project charter

```
Create a project charter for an EC site rebuild project.
Budget: 100M JPY, timeline: April to November 2026,
PM: Suzuki Hanako, sponsor: CTO Yamada.
```

### Example 2: Generate a full project plan

```
I have a CRM replacement project with 50 screens, 40 APIs,
and 3 external integrations. Create a complete project plan
including WBS, Gantt chart, RACI matrix, and risk register.
```

### Example 3: Risk management plan only

```
We're migrating our on-prem ERP to cloud.
Create a risk management plan covering technical,
data migration, and organizational change risks.
```

## Tips & Best Practices

- **Start with the Charter.** Formally authorizing the project with a charter prevents scope confusion later.
- **Use Mermaid diagrams.** They render natively in GitHub, GitLab, and many documentation tools -- no image exports needed.
- **Define RACI early.** Each deliverable should have exactly one Accountable person to avoid responsibility gaps.
- **Be conservative with schedules.** Use three-point estimation (PERT) and include buffer for critical-path activities.
- **Baseline everything.** Once the plan is approved, save it as a baseline. All changes should go through scope change control.
- **Leverage the knowledge base.** Ask Claude to consult the references for PMBOK standards, SaaS PM Q&A, or cross-framework mapping.

## Related Skills

- [Business Analyst]({{ '/en/skills/management/business-analyst/' | relative_url }}) -- Requirements elicitation and BRD creation feed into project planning.
- [Vendor Estimate Creator]({{ '/en/skills/management/vendor-estimate-creator/' | relative_url }}) -- Generate cost estimates with WBS that align with the project plan.
- [Strategic Planner]({{ '/en/skills/management/strategic-planner/' | relative_url }}) -- Strategic direction informs project objectives.
