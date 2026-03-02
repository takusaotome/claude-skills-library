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

### Charter Creation in Detail

The charter workflow collects business case, benefits plan, high-level requirements, and organizational assets. It then produces a 12-section document covering project purpose, scope boundaries (in/out of scope), key deliverables with milestone dates, budget breakdown, stakeholder register, risk summary, and success criteria. A helper script `generate_project_charter.py` can scaffold the Markdown skeleton.

### WBS and Scope Management

Scope is decomposed into a hierarchical WBS using the pattern: Phase -> Deliverable -> Work Package. The skill generates both a Mermaid `graph TD` diagram for visual hierarchy and a tabular WBS with IDs, task names, deliverables, owners, and durations. A scope change control process is also defined with a Mermaid flowchart showing the CCB (Change Control Board) approval path.

### Schedule and Gantt Charts

Activities are sequenced using four dependency types (FS, SS, FF, SF). Durations are estimated with PERT three-point estimation: `(Optimistic + 4 x Most Likely + Pessimistic) / 6`. The result is a Mermaid `gantt` chart with sections for each phase, milestone markers, and critical path identification. Schedule compression techniques (crashing and fast tracking) are applied when needed.

### RACI Matrix Construction

Every deliverable is mapped against project roles. Each row must have exactly one A (Accountable) to ensure clear decision authority. The skill also generates a Mermaid organization chart showing the reporting structure and a communication plan table defining meeting cadence, participants, and format.

### Risk Register and Monitoring

Risks are categorized into five groups: technical, scope/requirements, resource, integration, and external. Each risk is assessed on probability and impact (High/Medium/Low) and assigned a response strategy: Avoid, Mitigate, Transfer, or Accept. A Mermaid flowchart visualizes the continuous monitoring loop from identification through response and effectiveness measurement.

## 5 Mermaid Diagram Types

The skill produces five distinct Mermaid diagram types within a single project plan:

| Diagram | Mermaid Type | Purpose |
|---------|-------------|---------|
| **Gantt Chart** | `gantt` | Project schedule with task dependencies and milestones |
| **WBS Hierarchy** | `graph TD` | Top-down decomposition of project into work packages |
| **RACI / Org Chart** | `graph TD` | Team structure and reporting lines |
| **Risk Monitoring** | `graph LR` | Continuous risk identification-analysis-response loop |
| **Change Control** | `graph TD` | Scope change request approval workflow via CCB |

## PMBOK Mapping

The 7 workflows map to PMBOK knowledge areas as follows:

| Workflow | PMBOK Knowledge Area | Process Group |
|----------|---------------------|---------------|
| 1. Charter Creation | Integration Management | Initiating |
| 2. Scope & WBS | Scope Management | Planning |
| 3. Schedule & Gantt | Schedule Management | Planning |
| 4. RACI & Resources | Resource Management | Planning |
| 5. Risk Management | Risk Management | Planning |
| 6. Comm & Quality | Communications + Quality Mgmt | Planning |
| 7. Integration | Integration Management | Planning |

The skill's knowledge base also covers cross-framework mapping to PRINCE2, ITIL 4, and ISO 21502, letting you adapt artifacts for organizations using those methodologies.

## Helper Scripts

The skill includes two Python scripts that generate Markdown scaffolds:

- **`generate_project_charter.py`** -- Produces a project charter skeleton with all 12 sections pre-filled with placeholders. Pass project name, PM name, dates, and budget as arguments.

  ```
  python3 scripts/generate_project_charter.py \
    --project "EC Site Rebuild" --pm "Suzuki Hanako" \
    --start-date 2026-04-01 --end-date 2026-11-30 \
    --budget 100000000 --output /tmp/charter.md
  ```

- **`generate_wbs.py`** -- Creates a WBS template in Markdown with a Mermaid hierarchy diagram. Specify the project name and phase names.

  ```
  python3 scripts/generate_wbs.py \
    --project "EC Site Rebuild" \
    --phases "Requirements,Design,Implementation,Testing,Deployment" \
    --output /tmp/wbs.md
  ```

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

### Example 4: WBS and Gantt chart for an Agile project

```
Generate a WBS and Gantt chart for a 6-sprint mobile app
project. Include sprints of 2 weeks each, with design
in Sprint 1-2, core features in Sprint 3-4, and polish
plus release in Sprint 5-6.
```

### Example 5: RACI matrix for a cross-functional team

```
We have 4 departments involved: Engineering, Product,
QA, and Ops. Create a RACI matrix for a microservices
migration covering design review, implementation,
testing, deployment, and post-launch monitoring.
```

## Tips & Best Practices

- **Start with the Charter.** Formally authorizing the project with a charter prevents scope confusion later.
- **Use Mermaid diagrams.** They render natively in GitHub, GitLab, and many documentation tools -- no image exports needed.
- **Define RACI early.** Each deliverable should have exactly one Accountable person to avoid responsibility gaps.
- **Be conservative with schedules.** Use three-point estimation (PERT) and include buffer for critical-path activities.
- **Baseline everything.** Once the plan is approved, save it as a baseline. All changes should go through scope change control.
- **Leverage the knowledge base.** Ask Claude to consult the references for PMBOK standards, SaaS PM Q&A, or cross-framework mapping.

## Troubleshooting

### Mermaid Gantt chart does not render

**Symptom**: The Gantt chart appears as raw text instead of a rendered diagram.

**Solution**: Ensure the code block is fenced with ` ```mermaid `. Some Markdown renderers (e.g., older GitHub Enterprise versions) do not support Mermaid natively. In that case, use the `markdown-to-pdf` skill to convert to PDF with Mermaid rendering, or export via the Mermaid CLI.

### RACI matrix has no Accountable person for a row

**Symptom**: A deliverable row in the RACI table contains only R, C, and I but no A.

**Solution**: Every row must have exactly one A (Accountable). Ask Claude to re-check the matrix: "Verify that each row in the RACI matrix has exactly one A." If a deliverable genuinely has shared accountability, split it into sub-deliverables with clear single ownership.

### Project plan is too long or overwhelming

**Symptom**: The generated plan exceeds what stakeholders are willing to read.

**Solution**: Request a specific subset of workflows instead of the full 7-step plan. For example, ask for "charter and Gantt chart only" or "risk register only." You can also ask Claude to produce an executive summary section at the top of the plan.

## Related Skills

- [Business Analyst]({{ '/en/skills/management/business-analyst/' | relative_url }}) -- Requirements elicitation and BRD creation feed into project planning.
- [Vendor Estimate Creator]({{ '/en/skills/management/vendor-estimate-creator/' | relative_url }}) -- Generate cost estimates with WBS that align with the project plan.
- [Strategic Planner]({{ '/en/skills/management/strategic-planner/' | relative_url }}) -- Strategic direction informs project objectives.
