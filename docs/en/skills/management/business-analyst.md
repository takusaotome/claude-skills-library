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

## Tips & Best Practices

- **Use multiple elicitation techniques.** Combine interviews (for depth) with workshops (for consensus) and surveys (for breadth) to get comprehensive requirements.
- **Quantify the current state first.** Before building a business case, measure baseline metrics -- cost per transaction, error rates, cycle times. This makes improvement claims credible.
- **Distinguish needs from solutions.** Requirements should describe *what* is needed, not *how* to build it. "Reduce order processing time by 50%" is better than "Build a web form."
- **Run the financial script for accuracy.** Use `business_analysis.py financial --investment X --annual-benefit Y --years N --sensitivity` for reliable ROI/NPV calculations instead of manual math.
- **Prioritize ruthlessly.** Apply MoSCoW with a budget: Must Have should be around 40% of requirements, not 80%.

## Related Skills

- [Project Plan Creator]({{ '/en/skills/management/project-plan-creator/' | relative_url }}) -- Turn approved requirements into a full project plan with WBS and Gantt.
- [Strategic Planner]({{ '/en/skills/management/strategic-planner/' | relative_url }}) -- Strategic analysis (SWOT, PEST) provides context for business cases.
- [Vendor Estimate Creator]({{ '/en/skills/management/vendor-estimate-creator/' | relative_url }}) -- Estimate costs for the solutions identified in your business case.
