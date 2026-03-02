---
layout: default
title: Strategic Planner
grand_parent: English
parent: Project & Business
nav_order: 3
lang_peer: /ja/skills/management/strategic-planner/
permalink: /en/skills/management/strategic-planner/
---

# Strategic Planner
{: .no_toc }

Systematic strategic planning using MBA-standard frameworks -- SWOT, PEST, Porter's Five Forces, BCG/GE Matrix, Ansoff Matrix, Business Model Canvas, and more.
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

Strategic Planner supports the creation of medium-term business plans, new business proposals, and portfolio analysis reports using well-established strategic frameworks. It covers the full planning cycle from environmental scanning through to an actionable roadmap with Mermaid Gantt charts.

Key frameworks available:

| Framework | Purpose |
|:----------|:--------|
| PEST / PESTLE | Macro-environment analysis |
| Porter's Five Forces | Industry competitive structure |
| Value Chain | Internal capability assessment |
| SWOT / Cross-SWOT | Strategy option derivation |
| Business Model Canvas / Lean Canvas | Business model design |
| BCG Matrix / GE Matrix | Portfolio investment allocation |
| Ansoff Matrix | Growth strategy direction |
| Balanced Scorecard | Strategic KPI structure |

## When to Use

- **Medium-term business plan** -- "Create a 3-year strategic plan for our manufacturing division"
- **New business proposal** -- "Design a business model for a new SaaS product"
- **Portfolio analysis** -- "Evaluate investment priorities across our 5 business units"
- **Individual framework analysis** -- "Run a SWOT analysis" or "Create a Porter's Five Forces assessment"
- **Strategic roadmap** -- "Build a Gantt-based execution roadmap for our growth strategy"

## Prerequisites

- Claude Code with the `strategic-planner` skill installed
- Knowledge of the business/industry context you want to analyze
- No external APIs or paid services are needed

## How It Works

The skill provides 7 workflows that can be used individually or combined:

1. **Strategic Context Analysis** -- PEST/PESTLE for macro trends, Porter's Five Forces for industry structure, Value Chain for internal strengths. Produces an environmental scan report.
2. **SWOT Analysis & Strategic Options** -- Consolidate findings into a SWOT matrix, then derive strategies using Cross-SWOT (SO/WO/ST/WT quadrants). Prioritize options using weighted scoring.
3. **Vision & Strategic Objectives** -- Craft a vision statement, align with mission, set strategic objectives across Balanced Scorecard perspectives (financial, customer, process, learning), and build a KPI hierarchy.
4. **Business Model Design** -- Create a Business Model Canvas (9 building blocks) or Lean Canvas (for startups/new ventures). Design the value proposition and revenue model.
5. **Portfolio Analysis** -- Apply BCG Matrix (Star/Cash Cow/Question Mark/Dog), GE/McKinsey 9-cell matrix, and Ansoff Matrix. Produce investment allocation recommendations.
6. **Strategic Initiatives & Roadmap** -- Convert strategy options into concrete initiatives, prioritize by strategic fit / feasibility / impact / urgency, build a Mermaid Gantt roadmap, and set milestones.
7. **Medium-Term Plan Integration** -- Merge all analyses into a complete plan document: executive summary, financials, investment plan, risk matrix, governance structure, and KPI dashboard.

### Typical deliverable combinations

| Deliverable | Required Workflows | Optional |
|:------------|:-------------------|:---------|
| Medium-term business plan | 1, 2, 3, 5, 6, 7 | 4 |
| New business proposal | 1, 2, 4 | 3, 6 |
| Portfolio analysis report | 1, 5 | 2 |
| SWOT analysis report | 1, 2 | -- |

## Usage Examples

### Example 1: Medium-term business plan

```
Create a 3-year medium-term business plan for a mid-size manufacturer
(annual revenue: 50B JPY). Key challenge: transition from ICE to EV
components. Include PEST, Porter 5F, SWOT, portfolio analysis,
financial targets, and execution roadmap.
```

### Example 2: New business proposal

```
Design a SaaS business model for an AI-powered document management
platform targeting SMBs. Use Lean Canvas and include a value
proposition analysis, revenue model, and key metrics.
```

### Example 3: SWOT and strategic options

```
Run a Cross-SWOT analysis for our retail chain.
Strengths: strong brand, 200 locations.
Weaknesses: no e-commerce, aging IT systems.
Opportunities: online-to-offline, subscription models.
Threats: Amazon, rising rent costs.
Derive prioritized strategic options.
```

## Tips & Best Practices

- **Ground analysis in data.** Avoid vague SWOT entries like "strong brand." Instead use measurable statements: "Brand recognition at 78% in target segment (industry average: 45%)."
- **Cross-SWOT over plain SWOT.** A plain SWOT list is descriptive; Cross-SWOT generates actionable strategy options from the intersections.
- **Limit initiatives.** A plan with 20 strategic initiatives lacks focus. Aim for 5-7 high-priority initiatives.
- **Use Mermaid Gantt for roadmaps.** The visual timeline helps stakeholders grasp phasing and dependencies at a glance.
- **Write the executive summary last.** Complete all analysis first, then distill the key messages into a concise one-page summary.
- **Validate portfolio scoring criteria upfront.** Agree on evaluation weights with stakeholders before scoring business units to avoid bias debates later.

## Related Skills

- [Business Analyst]({{ '/en/skills/management/business-analyst/' | relative_url }}) -- Detailed requirements and process analysis complement strategic-level planning.
- [Project Plan Creator]({{ '/en/skills/management/project-plan-creator/' | relative_url }}) -- Turn strategic initiatives into executable project plans.
- [Vendor Estimate Creator]({{ '/en/skills/management/vendor-estimate-creator/' | relative_url }}) -- Estimate costs for strategic investment initiatives.
