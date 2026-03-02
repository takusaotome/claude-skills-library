---
layout: default
title: Incident RCA Specialist
grand_parent: English
parent: Operations & Docs
nav_order: 1
lang_peer: /ja/skills/ops/incident-rca-specialist/
permalink: /en/skills/ops/incident-rca-specialist/
---

# Incident RCA Specialist
{: .no_toc }

Systematic post-incident review and root cause analysis for organizational incident management.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-workflow">Workflow</span>
<span class="badge badge-bilingual">Bilingual</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Incident RCA Specialist conducts structured post-incident reviews focused on organizational processes, not log-level debugging. It provides methodologies for timeline construction, impact assessment, root cause analysis (5 Whys, Fishbone, Fault Tree Analysis), corrective action planning with SMART criteria, and bilingual RCA report generation.

The skill enforces a blame-free culture -- analysis never stops at "human error" but always decomposes further into process, system, or training gaps.

**Scope boundary:** This skill handles organizational and process aspects of incident review. For log file analysis or stack trace debugging, use the `log-debugger` skill instead.

---

## When to Use

- Conducting a post-incident review or retrospective
- Creating an incident report or RCA document
- Developing corrective action plans after an outage
- Building recurrence prevention strategies
- Evaluating SLA compliance after an incident
- Performing Fault Tree Analysis for complex system failures
- Sharing Lessons Learned across the organization

---

## Prerequisites

- **Claude Code** installed and running
- **incident-rca-specialist** skill installed (`cp -r ./skills/incident-rca-specialist ~/.claude/skills/`)
- No external APIs or additional tools required

---

## How It Works

The skill follows an 8-step workflow:

1. **Information Gathering** -- Collect incident details through structured questions (timeline, affected services, user count, response actions)
2. **Timeline Construction** -- Build a chronological timeline with Mermaid Gantt diagram and calculate TTD/TTR/TTM/TTRe metrics
3. **Impact Assessment** -- Evaluate impact across four dimensions (user, service, business, operational) and assign P0-P4 severity
4. **RCA: 5 Whys** -- Branching 5 Whys analysis with evidence tracking; human errors are always decomposed into process/system/training gaps
5. **RCA: Fishbone** -- Ishikawa analysis with six IT-specific categories (People, Process, Technology, Environment, Data, External)
6. **RCA: Fault Tree Analysis** -- Top-down failure decomposition using AND/OR gates, minimal cut sets, and Single Point of Failure identification
7. **Corrective Action Planning** -- Three time horizons (immediate/short-term/long-term) with the 3D Prevention Framework (Detect, Defend, Degrade) and SMART criteria
8. **Report Generation** -- Complete RCA report in Japanese or English using bundled templates

---

## Usage Examples

### Example 1: Full post-incident review

```
Our payment service was down for 2 hours yesterday (Feb 28, 14:00-16:00 UTC).
About 5,000 users were affected. The monitoring alert fired 20 minutes after
the first error. Please conduct a full RCA.
```

The skill will walk you through information gathering, build a timeline with metrics, assess impact, run 5 Whys analysis, propose corrective actions, and generate the final report.

### Example 2: Corrective action plan only

```
We already identified the root cause of last week's database failover incident
(misconfigured connection pool limits). Please create a corrective action plan
with immediate, short-term, and long-term measures.
```

The skill will apply the 3D Prevention Framework (Detect/Defend/Degrade) and produce SMART corrective actions across three time horizons.

### Example 3: Fault Tree Analysis

```
Our CI/CD pipeline has had three deployment failures this month from different
causes. Please perform a Fault Tree Analysis to identify single points of
failure and minimal cut sets.
```

The skill will decompose the top event using AND/OR gates, generate a Mermaid FTA diagram, and highlight SPOFs for priority remediation.

---

## Tips & Best Practices

- **Blame-free language**: The skill frames findings as process/system improvements, never individual fault. Phrases like "the process allowed..." replace "person X failed to..."
- **Evidence-based**: Every causal claim needs supporting evidence (logs, metrics, timestamps). Confidence levels (High/Medium/Low) are assigned to each link.
- **Choose the right method**: Use 5 Whys for straightforward incidents, Fishbone when multiple contributing factors are suspected, and FTA for complex structural failures. Methods can be combined.
- **SMART actions**: Vague actions like "improve monitoring" will be refined to specific, measurable items with deadlines and owners.
- **Bilingual output**: Reports can be generated in either Japanese or English using the bundled templates.

---

## Related Skills

- [log-debugger]({{ '/en/skills/ops/log-debugger/' | relative_url }}) -- Log file analysis and technical root cause investigation at the code level
- [operations-manual-creator]({{ '/en/skills/ops/operations-manual-creator/' | relative_url }}) -- Create structured operations manuals and SOPs
- [project-manager]({{ '/en/skills/management/project-manager/' | relative_url }}) -- Project health checks and PMBOK-based management
