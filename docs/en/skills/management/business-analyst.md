---
layout: default
title: Business Analyst
grand_parent: English
parent: Project & Business
nav_order: 2
lang_peer: /ja/skills/management/business-analyst/
permalink: /en/skills/management/business-analyst/
---

# Business Analyst
{: .no_toc }

Professional business analysis aligned with BABOK Guide v3 -- requirements elicitation, process mapping, stakeholder analysis, business cases, and gap analysis.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/business-analyst.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/business-analyst){: .btn .fs-5 .mb-4 .mb-md-0 }
<span class="badge badge-scripts">Scripts</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Business Analyst provides comprehensive business analysis capabilities aligned with the BABOK (Business Analysis Body of Knowledge) Guide v3 from the International Institute of Business Analysis (IIBA). It covers all 6 knowledge areas: Planning and Monitoring, Elicitation and Collaboration, Requirements Life Cycle Management, Strategy Analysis, Requirements Analysis and Design Definition, and Solution Evaluation.

The skill includes a Python script (`business_analysis.py`) for financial analysis (ROI, NPV, IRR), business metrics calculation, data profiling, and weighted option comparison.

## When to Use

- **Gather requirements** from stakeholders via interviews, workshops, or surveys
- **Create a Business Requirements Document (BRD)** for a new system or process
- **Develop a business case** with ROI, NPV, and payback period analysis
- **Map business processes** using BPMN notation and identify inefficiencies
- **Perform stakeholder analysis** with power/interest matrices and engagement strategies
- **Conduct gap analysis** comparing current and desired state capabilities
- **Prioritize requirements** using MoSCoW, value vs. complexity, or Kano model

## Prerequisites

- Claude Code with the `business-analyst` skill installed
- No external APIs required
- Python 3 for running `business_analysis.py` (optional -- only needed for automated financial calculations)

## How It Works

The skill provides 5 core workflows:

1. **Requirements Elicitation** -- Plan the approach (interviews, workshops, surveys, observation, prototyping), prepare questions, conduct sessions, categorize requirements (business, stakeholder, functional, non-functional), validate, and document using a BRD template.
2. **Business Process Analysis** -- Map the current (As-Is) process with BPMN/swimlane diagrams, measure cycle time and error rates, identify waste (TIMWOOD), perform root cause analysis (5 Whys, Fishbone), design the future (To-Be) process, and quantify improvements.
3. **Stakeholder Analysis & Engagement** -- Identify all stakeholders, classify them using a Power/Interest matrix, develop tailored engagement strategies, and build a RACI matrix.
4. **Business Case Development** -- Define the problem, identify 3-5 solution options, analyze costs and benefits, calculate ROI/NPV/Payback/IRR (optionally via `business_analysis.py`), compare options with weighted scoring, and make a recommendation.
5. **Gap Analysis** -- Document current state capabilities and metrics, define future state targets, identify gaps (process, technology, people, data, policy), prioritize with an Impact vs. Effort matrix, and develop an action plan.

### BABOK 6 Knowledge Areas

The skill is structured around the six knowledge areas defined by BABOK Guide v3:

| Knowledge Area | Focus | Key Techniques |
|---------------|-------|----------------|
| **BA Planning & Monitoring** | Define the BA approach and track its execution | Stakeholder list, BA plan, governance model |
| **Elicitation & Collaboration** | Gather information and confirm it with stakeholders | Interviews, workshops, surveys, observation, prototyping, document analysis |
| **Requirements Life Cycle Mgmt** | Trace, maintain, and prioritize requirements | MoSCoW, value vs. complexity, traceability matrix, change control |
| **Strategy Analysis** | Understand the business need and justify investment | SWOT, PESTLE, value chain, current/future state analysis |
| **Requirements Analysis & Design** | Specify and model requirements, define solution design | Use cases, user stories, data models, process models, acceptance criteria |
| **Solution Evaluation** | Assess whether the delivered solution meets objectives | Performance metrics, KPIs, benefit realization tracking |

### Elicitation Techniques at a Glance

Choosing the right technique depends on the situation:

| Technique | Best When | Participants | Output |
|-----------|-----------|-------------|--------|
| **Interviews** | Deep understanding needed from specific individuals | 1-3 people | Detailed notes, requirements |
| **Workshops** | Consensus required across functions | 6-15 people | Agreed requirements, process maps |
| **Surveys** | Large user base or quantitative data needed | 50+ people | Prioritized lists, statistics |
| **Observation** | Process is poorly documented or tacit | 1-5 sessions | As-Is process map, pain points |
| **Document Analysis** | Existing documentation or legacy system available | Analyst only | Requirements derived from docs |
| **Prototyping** | Requirements are abstract or UI-focused | 3-8 people | Validated mockups, refined requirements |

### Financial Analysis with business_analysis.py

The bundled Python script automates key calculations:

```
python scripts/business_analysis.py financial \
  --investment 10000000 \
  --annual-benefit 3000000 \
  --annual-cost 500000 \
  --years 5 \
  --sensitivity
```

This outputs ROI, NPV, IRR, and payback period with optional sensitivity analysis showing how results change when assumptions shift by +/- 10-20%.

### Requirements Categorization

The skill organizes requirements into four layers to ensure nothing is missed:

| Category | Question it Answers | Example |
|:---------|:-------------------|:--------|
| **Business Requirements** | WHY is this needed? | "Reduce order processing time by 50%" |
| **Stakeholder Requirements** | WHO needs WHAT? | "Sales reps need mobile access to customer data" |
| **Functional Requirements** | WHAT does the system do? | "System shall validate credit limit before accepting an order" |
| **Non-Functional Requirements** | HOW WELL must it perform? | "95% of transactions must respond within 2 seconds" |

Each requirement is assigned an ID, linked to a business objective (traceability), and validated against a checklist: clear, complete, consistent, testable, traceable, feasible, and necessary.

### Prioritization Frameworks

The skill supports three prioritization approaches:

- **MoSCoW** -- Must Have (~40%), Should Have (~30%), Could Have (~20%), Won't Have (~10%). Best for scope negotiation with stakeholders.
- **Value vs. Complexity** -- Plot requirements on a 2x2 matrix. High value + low complexity items are quick wins; low value + high complexity items should be dropped.
- **Kano Model** -- Classify into Basic (must exist), Performance (more is better), and Excitement (unexpected delighters). Useful for product-oriented projects.

## Usage Examples

### Example 1: Create a business case

```
Create a business case for automating our invoice processing.
Initial investment: 10M JPY, expected annual savings: 3M JPY,
analysis period: 5 years. Include sensitivity analysis.
```

### Example 2: Map a business process

```
Map our current customer onboarding process (takes 10 days,
25% error rate) and design a future-state process targeting
2-day onboarding with under 5% error rate.
```

### Example 3: Requirements elicitation plan

```
I need to gather requirements from 5 departments for a new
customer portal. Help me plan the elicitation approach,
select techniques, and prepare interview questions.
```

### Example 4: Stakeholder analysis and engagement strategy

```
We're starting a digital transformation project affecting
6 departments. Identify likely stakeholders, create a
power/interest matrix, and develop engagement strategies
for champions, skeptics, and blockers.
```

### Example 5: Gap analysis for CRM migration

```
We currently use spreadsheets for customer management
(500 records, manual entry, no reporting). We want to
move to a CRM that handles 10K records, automated workflows,
and real-time dashboards. Perform a gap analysis.
```

## Tips & Best Practices

- **Use multiple elicitation techniques.** Combine interviews (for depth) with workshops (for consensus) and surveys (for breadth) to get comprehensive requirements.
- **Quantify the current state first.** Before building a business case, measure baseline metrics -- cost per transaction, error rates, cycle times. This makes improvement claims credible.
- **Distinguish needs from solutions.** Requirements should describe *what* is needed, not *how* to build it. "Reduce order processing time by 50%" is better than "Build a web form."
- **Run the financial script for accuracy.** Use `business_analysis.py financial --investment X --annual-benefit Y --years N --sensitivity` for reliable ROI/NPV calculations instead of manual math.
- **Prioritize ruthlessly.** Apply MoSCoW with a budget: Must Have should be around 40% of requirements, not 80%.

## Troubleshooting

### Stakeholders cannot agree on requirements

**Symptom**: Conflicting requirements from different departments with no resolution in sight.

**Solution**: Facilitate a structured requirements workshop with all conflicting parties present. Use MoSCoW to force prioritization ("If you can only have 10 features, which ones?"). If consensus is still not possible, escalate to the executive sponsor with a clear options-and-trade-offs summary and let them decide.

### Business case gets rejected

**Symptom**: The financial analysis shows positive ROI but the proposal is still declined.

**Solution**: Understand the specific objections. Common causes include: ROI too low relative to other competing investments, payback period too long, risks perceived as too high, or weak strategic alignment. Consider reducing scope for a Phase 1 pilot, strengthening the risk mitigation section, or reframing the case around strategic value rather than pure cost savings.

### Cannot quantify benefits

**Symptom**: The project delivers "soft" benefits (better user experience, improved morale) that are hard to put a number on.

**Solution**: Establish baseline measurements now, even rough ones. Use proxy metrics (e.g., reduced support tickets as a proxy for improved usability). Present a range (conservative to optimistic) rather than a single number. Include qualitative benefits alongside the quantitative analysis, clearly labeled.

## Related Skills

- [Project Plan Creator]({{ '/en/skills/management/project-plan-creator/' | relative_url }}) -- Turn approved requirements into a full project plan with WBS and Gantt.
- [Strategic Planner]({{ '/en/skills/management/strategic-planner/' | relative_url }}) -- Strategic analysis (SWOT, PEST) provides context for business cases.
- [Vendor Estimate Creator]({{ '/en/skills/management/vendor-estimate-creator/' | relative_url }}) -- Estimate costs for the solutions identified in your business case.
