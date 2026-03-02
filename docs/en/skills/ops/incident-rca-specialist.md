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

### Branching 5 Whys in detail

Traditional 5 Whys follows a single causal chain. This skill extends it with a **tree structure** -- when one "Why" reveals multiple independent causes, the analysis branches and explores each path separately.

```
Symptom: Payment service returned 500 errors
 Why 1: Database connection pool exhausted
   Why 2a: Connection leak in checkout module     Why 2b: Connection limit too low
     Why 3a: Missing finally block                  Why 3b: Default config from 2 years ago
       Why 4a: No static analysis rule                Why 4b: No capacity review process
         [Process gap] [Evidence: git blame]           [Process gap] [Evidence: config history]
```

Each branch is tracked independently with:
- **Evidence annotation** -- logs, metrics, or timestamps supporting the causal link
- **Confidence level** -- High / Medium / Low for each link
- **Human Error Decomposition** -- if analysis reaches "operator mistake," it must continue: "Why was this error possible?" Decompose into Process gap, System gap, or Training gap.

### Fault Tree Analysis: AND/OR gates

FTA decomposes the top-level failure event using two types of logic gates:

**OR gate** -- the parent event occurs if **any** child event occurs:

```
        [Service outage]
             OR
        /          \
[DB failure]   [Network failure]
```

Either a database failure or a network failure alone is sufficient to cause the outage.

**AND gate** -- the parent event occurs only if **all** child events occur simultaneously:

```
        [Data corruption]
            AND
        /          \
[Write race]   [No validation]
```

Data corruption requires both a write race condition and the absence of input validation.

The skill identifies **Minimal Cut Sets** (the smallest combination of basic events causing the top event) and **Single Points of Failure** (events that appear in every cut set), then prioritizes SPOFs for corrective action.

### 3D Prevention Framework

Each corrective action is classified along three prevention dimensions:

- **Detect** -- How to discover the problem earlier (monitoring thresholds, alerting rules, observability improvements)
- **Defend** -- How to prevent occurrence entirely (input validation, guardrails, automation, safe defaults)
- **Degrade** -- How to limit blast radius when failure occurs (circuit breakers, feature flags, graceful degradation, bulkheading)

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

### Example 4: SLA compliance evaluation

```
Our SLA guarantees 99.9% uptime for the billing API. After last night's
45-minute outage, check whether we breached the SLA for this month and
calculate the remaining error budget.
```

The skill will calculate the total downtime against the SLA threshold for the period, determine whether the SLA was breached, and include the result in the impact assessment section with financial penalty estimates if applicable.

---

## Troubleshooting

### Analysis stalls at "human error"

**Symptom**: The 5 Whys chain reaches "the operator made a mistake" and the analysis feels complete, but no actionable improvement has been identified.

**Solution**: The skill enforces a Human Error Decomposition rule -- it never stops at human error. When this happens, the analysis continues by asking "Why was this error possible?" and decomposes the finding into one or more of: Process gap (missing checklist, unclear procedure), System gap (no guardrail, missing validation), or Training gap (insufficient onboarding, no runbook). If you notice the analysis stopping too early, prompt the skill with "Decompose the human error further."

### Too many branches in 5 Whys

**Symptom**: The branching 5 Whys tree becomes unwieldy with dozens of branches, making the report hard to read.

**Solution**: Focus on branches with High confidence evidence first. Prune Low-confidence branches or consolidate them into a summary note. You can also request the skill to limit the analysis to the top 3 most impactful branches and mention remaining branches as "areas for further investigation" in the report.

### Choosing the right RCA method

**Symptom**: Unsure whether to use 5 Whys, Fishbone, or FTA for a particular incident.

**Solution**: Use **5 Whys** when the incident has a relatively clear causal chain (e.g., a single misconfiguration leading to an outage). Use **Fishbone** when there are multiple contributing factors across different categories (people, process, technology). Use **FTA** for complex system failures where you need to understand the structural relationships between failure modes. The methods can be combined -- for example, use Fishbone to identify categories, then 5 Whys to drill into the most significant category.

---

## Tips & Best Practices

- **Blame-free language**: The skill frames findings as process/system improvements, never individual fault. Phrases like "the process allowed..." replace "person X failed to..."
- **Evidence-based**: Every causal claim needs supporting evidence (logs, metrics, timestamps). Confidence levels (High/Medium/Low) are assigned to each link.
- **Choose the right method**: Use 5 Whys for straightforward incidents, Fishbone when multiple contributing factors are suspected, and FTA for complex structural failures. Methods can be combined.
- **SMART actions**: Vague actions like "improve monitoring" will be refined to specific, measurable items with deadlines and owners.
- **Bilingual output**: Reports can be generated in either Japanese or English using the bundled templates.

---

## Related Skills

- **log-debugger** -- Log file analysis and technical root cause investigation at the code level
- [operations-manual-creator]({{ '/en/skills/ops/operations-manual-creator/' | relative_url }}) -- Create structured operations manuals and SOPs
- **project-manager** -- Project health checks and PMBOK-based management
