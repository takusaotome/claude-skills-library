---
layout: default
title: Vendor Estimate Creator
grand_parent: English
parent: Project & Business
nav_order: 4
lang_peer: /ja/skills/management/vendor-estimate-creator/
permalink: /en/skills/management/vendor-estimate-creator/
---

# Vendor Estimate Creator
{: .no_toc }

Create professional cost estimates for software development projects -- WBS, effort calculations, cost breakdowns, ROI analysis, and formatted estimate documents.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-workflow">Workflow</span>
<span class="badge badge-bilingual">Bilingual JA/EN</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Vendor Estimate Creator transforms RFQ documents or project requirements into comprehensive, professional cost estimates for software development projects. It covers the full estimation lifecycle: RFQ analysis, work breakdown, effort estimation using industry-standard methods, cost calculation, ROI analysis, and final document generation in Markdown format.

The skill includes reference guides for estimation methodology (4 methods), effort standards (role-based productivity, task-level benchmarks), and ROI analysis (NPV, IRR, payback period, sensitivity analysis). Output defaults to Japanese but supports English.

## When to Use

- You have received an RFQ and need to prepare a cost estimate response
- You need to calculate project effort and cost for a software development proposal
- You want to include ROI analysis to justify the investment to a client
- You need a standardized estimate format across your organization
- You are reviewing an existing estimate for completeness

## Prerequisites

- Claude Code with the `vendor-estimate-creator` skill installed
- An RFQ document, project requirements, or a description of the system to be built
- No external APIs or paid services are needed

## How It Works

The skill follows 6 sequential workflows:

1. **RFQ Analysis** -- Review the RFQ to extract project scope (screen count, API count, DB tables, batch jobs, external integrations), identify the project type, assess complexity, list unknowns, document assumptions, and evaluate risks (technical, requirements, integration) to determine contingency percentage.
2. **Work Breakdown & Task Identification** -- Define project phases (requirements, design, implementation, testing, deployment, PM, QA), create a hierarchical WBS, and validate that PM (10-15%), QA (7-11%), and contingency (10-25%) are included.
3. **Effort Estimation** -- Select the appropriate estimation method (analogous, parametric, or bottom-up) based on project maturity. Apply standard effort benchmarks per task and adjust for complexity, team proficiency, and technical risk.
4. **Cost Calculation** -- Define labor rates by role (PM, architect, senior/mid engineer), assign roles to WBS tasks, calculate per-task cost, and aggregate to a project total.
5. **ROI Analysis** -- Analyze current-state costs (As-Is), project future-state benefits (To-Be), calculate financial metrics (ROI, NPV, IRR, payback period), and run sensitivity analysis across optimistic, standard, and pessimistic scenarios.
6. **Estimate Document Generation** -- Populate a 12-section estimate template (executive summary, assumptions, WBS detail, schedule, ROI, team structure, risks, maintenance costs, payment terms, contract terms, approval).

## Usage Examples

### Example 1: Full estimate from an RFQ

```
I received an RFQ for building a customer management system.
Requirements: 30 screens, 50 APIs, 15 DB tables, 3 external
system integrations, mobile support (iOS/Android).
Technology: React + Node.js + PostgreSQL.
Create a complete cost estimate with WBS, effort, cost breakdown,
and ROI analysis.
```

### Example 2: Quick estimate for a proposal

```
We need a rough estimate for a data analytics dashboard project.
About 10 screens, 20 APIs, connecting to 2 data sources.
Team is familiar with the tech stack (Python + React).
Provide effort in person-days and cost in JPY.
```

### Example 3: ROI analysis only

```
Our current manual order processing costs 24.8M JPY/year
(labor 18M, system ops 5M, error handling 1.8M).
The new system costs 47.5M JPY to build and 3M/year to operate.
Expected improvements: processing time 30min to 5min,
error rate 5% to 0.5%.
Calculate ROI, NPV, and payback period over 5 years.
```

## Tips & Best Practices

- **Always include contingency.** Low-risk projects need 5-10%, medium 10-15%, and high-risk projects 15-25%. Omitting contingency is the most common estimation mistake.
- **Do not forget PM and QA effort.** Project management should be 10-15% and QA 7-11% of total effort. These are frequently underestimated or missing entirely.
- **Use multiple estimation methods for cross-checking.** Estimate bottom-up, then validate with parametric benchmarks or analogous project data.
- **Document every assumption.** Clearly state what is assumed about scope, technology, team composition, and constraints. Assumptions protect both vendor and client.
- **Be conservative on benefits, generous on costs.** For ROI analysis, use realistic or slightly pessimistic benefit projections and include all cost categories.
- **Check for commonly missed items.** Data migration, non-functional requirements (performance, security), integration testing, training, and documentation are often overlooked.

## Related Skills

- [Project Plan Creator]({{ '/en/skills/management/project-plan-creator/' | relative_url }}) -- The WBS and schedule from an estimate can feed directly into a project plan.
- [Business Analyst]({{ '/en/skills/management/business-analyst/' | relative_url }}) -- Requirements analysis provides the input for accurate estimation.
- [Strategic Planner]({{ '/en/skills/management/strategic-planner/' | relative_url }}) -- Strategic context helps justify the investment in a business case.
