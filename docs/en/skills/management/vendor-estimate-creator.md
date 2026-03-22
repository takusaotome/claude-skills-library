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

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-estimate-creator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/vendor-estimate-creator){: .btn .fs-5 .mb-4 .mb-md-0 }
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

### 4 Estimation Methods Compared

The skill supports four methods. Choose based on how much is known about the project:

| Method | When to Use | Accuracy | How It Works |
|:-------|:-----------|:---------|:-------------|
| **Analogous** | Very early stage, similar past project exists | +/- 50% | Compare with a completed project of similar size and complexity. Scale up/down based on differences. |
| **Parametric** | Planning stage, scope metrics known (screen count, API count) | +/- 30% | Multiply a productivity rate (e.g., 3 person-days per API) by quantity. Quick and data-driven. |
| **Bottom-up** | Requirements are defined, WBS is available | +/- 10% | Estimate each WBS task individually, then sum. Most accurate but most time-consuming. |
| **Three-point (PERT)** | Any stage where uncertainty range is known | Varies | Calculate `(Optimistic + 4 x Most Likely + Pessimistic) / 6` for each task. Useful for risk-adjusted estimates. |

For best results, estimate with bottom-up and cross-check with parametric benchmarks.

### Contingency Allocation

Contingency covers unknowns that cannot be estimated precisely. The percentage depends on project risk level:

| Risk Level | Contingency % | Typical Indicators |
|:-----------|:-------------|:-------------------|
| Low | 5-10% | Familiar technology, clear requirements, experienced team |
| Medium | 10-15% | Some new technology, requirements mostly defined, mixed team experience |
| High | 15-25% | New technology stack, vague requirements, many external integrations |

Contingency is applied to the sum of all phase efforts (including PM and QA), not just implementation.

### Standard Effort Allocation by Phase

A well-formed estimate distributes effort across phases. Use these ranges as a sanity check:

| Phase | Typical % of Total Effort |
|:------|:-------------------------|
| Requirements Definition | 8-12% |
| Design | 12-18% |
| Implementation | 30-40% |
| Testing | 18-25% |
| Deployment & Ops Prep | 5-8% |
| PM (cross-cutting) | 10-15% |
| QA (cross-cutting) | 7-11% |

### Labor Rate Ranges

The skill uses role-based daily rates for cost calculation. Adjust these to your market:

| Role | Rate (JPY/person-day) |
|:-----|:---------------------|
| Project Manager | 100,000 - 150,000 |
| Architect | 90,000 - 140,000 |
| Senior Engineer | 80,000 - 120,000 |
| Mid-level Engineer | 60,000 - 90,000 |

Rates are multiplied by the person-day estimate for each WBS task, then summed to produce the project total.

### Estimate Document Structure

The final output follows a 12-section template:

1. Executive Summary -- Key figures and recommendation
2. Assumptions -- All scope, technology, and team assumptions
3. WBS Detail -- Hierarchical task breakdown with effort per task
4. Project Schedule -- Timeline with milestones
5. ROI Analysis -- Current vs. future state, financial metrics
6. Team Structure -- Roles, headcount, utilization rates
7. Risks and Mitigation -- Risk register with response strategies
8. Maintenance Costs -- Annual operating and support costs
9. Payment Terms -- Milestone-based or periodic payment schedule
10. Contract Terms -- Scope change process, warranty, SLA
11. Appendix -- Detailed calculations, reference data
12. Approval -- Sign-off section for client and vendor

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

### Example 4: Estimate review and validation

```
Here is our existing estimate for a CRM migration project
(attached as estimate.md). Review it for completeness:
check if PM and QA effort are properly included,
whether contingency is appropriate, and flag any
commonly missed items.
```

### Example 5: Mobile app estimate with unfamiliar tech stack

```
We need to estimate a cross-platform mobile app (Flutter)
for a logistics company. 15 screens, real-time GPS tracking,
offline mode, push notifications. Our team has not used
Flutter before. Factor in the learning curve and recommend
an appropriate contingency level.
```

## Tips & Best Practices

- **Always include contingency.** Low-risk projects need 5-10%, medium 10-15%, and high-risk projects 15-25%. Omitting contingency is the most common estimation mistake.
- **Do not forget PM and QA effort.** Project management should be 10-15% and QA 7-11% of total effort. These are frequently underestimated or missing entirely.
- **Use multiple estimation methods for cross-checking.** Estimate bottom-up, then validate with parametric benchmarks or analogous project data.
- **Document every assumption.** Clearly state what is assumed about scope, technology, team composition, and constraints. Assumptions protect both vendor and client.
- **Be conservative on benefits, generous on costs.** For ROI analysis, use realistic or slightly pessimistic benefit projections and include all cost categories.
- **Check for commonly missed items.** Data migration, non-functional requirements (performance, security), integration testing, training, and documentation are often overlooked.

## Troubleshooting

### Estimate total seems too low compared to market rates

**Symptom**: The calculated cost is significantly below what comparable vendors charge.

**Solution**: Check for missing items: PM effort (10-15%), QA effort (7-11%), contingency (10-25%), data migration, training, documentation, and non-functional requirements testing. Also verify that labor rates reflect current market conditions -- rates from reference guides may need adjustment for your region or specialization.

### Client challenges the contingency percentage

**Symptom**: The client asks why 15-25% is added "on top" and wants it removed.

**Solution**: Explain that contingency covers identified risks and unknowns that cannot be precisely estimated at this stage. Provide the risk assessment showing the specific factors (new technology, unclear requirements, multiple integrations). Offer to reduce contingency if the client agrees to a formal scope change process -- this shifts the cost of unknowns from contingency to change requests.

### ROI analysis does not convince stakeholders

**Symptom**: Positive financial metrics (ROI, NPV) but stakeholders remain skeptical.

**Solution**: Ensure benefits are grounded in measurable current-state metrics (actual processing time, actual error rate, actual labor cost). Include sensitivity analysis showing even the pessimistic scenario is viable. Add qualitative benefits (compliance, scalability, employee satisfaction) alongside the numbers. Present a phased approach where Phase 1 delivers quick wins to prove value before committing to the full investment.

## Related Skills

- [Project Plan Creator]({{ '/en/skills/management/project-plan-creator/' | relative_url }}) -- The WBS and schedule from an estimate can feed directly into a project plan.
- [Business Analyst]({{ '/en/skills/management/business-analyst/' | relative_url }}) -- Requirements analysis provides the input for accurate estimation.
- [Strategic Planner]({{ '/en/skills/management/strategic-planner/' | relative_url }}) -- Strategic context helps justify the investment in a business case.
