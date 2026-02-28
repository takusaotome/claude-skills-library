---
name: incident-rca-specialist
description: >
  インシデント発生後の振り返りと根本原因分析を体系的に実施するスキル。
  ログファイル解析や技術デバッグが必要な場合は log-debugger を使用すること。
  本スキルはインシデント管理プロセス（タイムライン構築、影響評価、
  是正措置計画、再発防止策）に特化する。ログデータの分析ではなく、
  組織的な振り返りプロセスと是正措置の策定が主目的である。
  Use when conducting post-incident reviews without log analysis,
  creating corrective action plans, or performing organizational root cause
  analysis focused on process improvement. NOT for log file debugging.
  Triggers: "post-incident review", "corrective action plan",
  "incident report作成", "再発防止策", "RCAレポート",
  "是正措置", "インシデント振り返り"
---

# Incident RCA Specialist（インシデントRCA）

## Overview

Post-incident review and root cause analysis skill focused on organizational incident management processes. This skill provides structured methodologies for timeline construction, impact assessment, root cause analysis (5 Whys with branching, Fishbone, Fault Tree Analysis), corrective action planning with SMART criteria, and comprehensive RCA report generation.

**Scope Boundary**: This skill handles the organizational and process aspects of incident review. For log file analysis, stack trace debugging, or technical root cause investigation at the code level, use the `log-debugger` skill instead.

## When to Use

- Post-incident review / 振り返りを実施するとき
- Incident report / RCAレポートを作成するとき
- Corrective action plan を策定するとき
- 再発防止策を策定するとき
- インシデントの影響評価を実施するとき
- Fault Tree Analysis でシステム障害の構造分析を行うとき
- SLA違反の有無を評価するとき
- Lessons Learned を組織的に共有するとき

## Workflows

### Workflow 1: Incident Information Gathering（インシデント情報収集）

Collect all relevant incident details through structured interview questions.

1. Assign Incident ID in format `INC-YYYYMMDD-NNN`
2. Gather the following information:
   - **発生日時**: When was the incident first observed? (UTC and local timezone)
   - **検知方法**: How was it detected? (monitoring alert, user report, internal discovery)
   - **影響サービス**: Which services/systems were affected?
   - **影響ユーザー数**: How many users were impacted?
   - **対応経緯**: What actions were taken and by whom?
   - **復旧日時**: When was the service fully restored?
   - **関係者**: Who was involved in the response?
3. Document all raw facts without interpretation
4. Identify gaps in information and request additional data

### Workflow 2: Timeline Construction（タイムライン構築）

Build a chronological incident timeline with key metrics.

1. Organize events chronologically from first anomaly to full resolution
2. Generate a Mermaid gantt diagram using `assets/incident_timeline_template.md`
3. Calculate key time metrics:
   - **TTD** (Time to Detect): Time from incident start to detection
   - **TTR** (Time to Respond): Time from detection to first response action
   - **TTM** (Time to Mitigate): Time from first response to mitigation (impact reduced)
   - **TTRe** (Time to Resolve): Time from mitigation to full resolution
4. Identify bottlenecks in the response timeline
5. Compare metrics against organizational targets

### Workflow 3: Impact Assessment（影響評価）

Evaluate incident impact across four dimensions and assign severity.

1. Assess impact on 4 axes:
   - **ユーザー影響**: Number of affected users, user experience degradation
   - **サービス影響**: Service availability, feature availability, performance
   - **ビジネス影響**: Revenue impact, SLA violations, contractual penalties
   - **運用影響**: Operational overhead, team disruption, cascading effects
2. Load `references/incident_severity_matrix.md` and apply P0-P4 classification
3. Calculate business impact score: `affected_users x duration_hours x severity_weight`
4. Check SLA compliance for each affected service
5. Document all quantifiable impacts with evidence

### Workflow 4: RCA - 5 Whys（分岐対応版）

Perform 5 Whys analysis with branching support and evidence tracking.

1. Load `references/rca_methodologies.md` for 5 Whys branching technique
2. Start from the incident symptom as the top-level "Why"
3. For each level, ask "Why did this happen?" and document:
   - The answer (cause)
   - Supporting evidence (logs, metrics, testimonials)
   - Confidence level (High/Medium/Low)
4. When a single "Why" leads to multiple causes, create branches and explore each
5. **Human Error Decomposition Rule**: When analysis reaches "human error" or "operator mistake":
   - NEVER stop at human error as root cause
   - Continue asking: "Why was this error possible?"
   - Decompose into: Process gap / System gap / Training gap
6. Continue until reaching actionable root causes (process or system improvements)
7. Output as a numbered tree structure with evidence annotations

### Workflow 5: RCA - Fishbone Diagram（IT向け6カテゴリ）

Perform Ishikawa/Fishbone analysis with IT-specific categories.

1. Load `references/rca_methodologies.md` for IT Fishbone categories
2. Analyze causes across 6 IT-focused categories:
   - **People**: Skills, training, staffing, communication, fatigue
   - **Process**: Procedures, change management, approval flows, documentation
   - **Technology**: Infrastructure, software, configuration, capacity, dependencies
   - **Environment**: Network, data center, cloud region, security posture
   - **Data**: Data quality, integrity, migration, backup, consistency
   - **External**: Vendor issues, third-party services, regulatory, force majeure
3. Use the detailed checklist for each category to identify potential causes
4. Generate a Mermaid graph diagram representing the fishbone structure
5. Prioritize identified causes by likelihood and impact

### Workflow 6: RCA - Fault Tree Analysis

Perform systematic top-down failure analysis using FTA methodology.

1. Load `references/fault_tree_analysis_guide.md`
2. Define the **Top Event** (the incident/failure that occurred)
3. Decompose into intermediate events using AND/OR gates:
   - **AND gate**: All child events must occur for parent to occur
   - **OR gate**: Any child event is sufficient for parent to occur
4. Continue decomposition until reaching **basic events** (undividable root causes)
5. Identify **Minimal Cut Sets**: smallest combinations of basic events causing the top event
6. Identify **Single Points of Failure (SPOF)**: basic events appearing in all cut sets
7. Generate FTA tree as Mermaid graph (graph TD)
8. Prioritize SPOFs for corrective action

### Workflow 7: Corrective Action Planning（是正措置計画）

Develop structured corrective actions with SMART criteria.

1. Load `references/corrective_action_guide.md`
2. Classify actions into three time horizons:
   - **即時対応** (Immediate): Actions within 24-48 hours
   - **短期対策** (Short-term): Actions within 1-4 weeks
   - **長期対策** (Long-term): Actions within 1-3 months
3. Apply **3D Prevention Framework** to each root cause:
   - **Detect**: How to detect this earlier (monitoring, alerting, observability)
   - **Defend**: How to prevent occurrence (validation, guardrails, automation)
   - **Degrade**: How to limit blast radius (circuit breakers, graceful degradation)
4. Apply SMART criteria to each action:
   - **S**pecific: Clear, unambiguous description
   - **M**easurable: Quantifiable success criteria
   - **A**chievable: Realistic within resource constraints
   - **R**elevant: Directly addresses identified root cause
   - **T**ime-bound: Clear deadline and milestones
5. Assign ownership and tracking using `assets/corrective_action_tracker.md`

### Workflow 8: RCA Report Generation（レポート出力）

Generate comprehensive RCA report integrating all workflow outputs.

1. Select language template:
   - Japanese: `assets/rca_report_template_ja.md`
   - English: `assets/rca_report_template_en.md`
2. Populate all sections from previous workflow outputs:
   - Executive summary from Impact Assessment
   - Timeline from Timeline Construction
   - Impact evaluation from Impact Assessment
   - Root cause analysis from Workflows 4, 5, and/or 6
   - Corrective actions from Corrective Action Planning
3. Add Lessons Learned section:
   - What went well in the response
   - What could be improved
   - Process improvement recommendations
4. Prepare approval/review section with stakeholder sign-off table
5. Output as complete Markdown document

## Resources

| File | Type | Purpose | When to Load |
|------|------|---------|--------------|
| `references/rca_methodologies.md` | Reference | 5 Whys branching, Human Error Decomposition, Fishbone categories, method selection guide | Workflow 4, 5 |
| `references/incident_severity_matrix.md` | Reference | P0-P4 classification, SLA evaluation, business impact formula | Workflow 3 |
| `references/corrective_action_guide.md` | Reference | 3D Prevention Framework, SMART criteria, action classification | Workflow 7 |
| `references/fault_tree_analysis_guide.md` | Reference | FTA methodology, gates, minimal cut sets, SPOF identification, Mermaid notation | Workflow 6 |
| `assets/rca_report_template_ja.md` | Template | Japanese RCA report template with all sections | Workflow 8 |
| `assets/rca_report_template_en.md` | Template | English RCA report template with all sections | Workflow 8 |
| `assets/incident_timeline_template.md` | Template | Mermaid gantt template for incident timeline with TTD/TTR/TTM/TTRe | Workflow 2 |
| `assets/corrective_action_tracker.md` | Template | Corrective action tracking table with SMART criteria and 3D classification | Workflow 7 |

## Best Practices

### Blame-Free Culture
- Focus on **process and system improvements**, not individual fault
- Use language like "the process allowed..." instead of "person X failed to..."
- When analysis reaches human error, always decompose further into process/system/training gaps
- Frame findings as opportunities for organizational improvement

### Evidence-Based Analysis
- Every causal claim must be supported by evidence (logs, metrics, timestamps, testimonials)
- Assign confidence levels to each causal link (High/Medium/Low)
- Distinguish between confirmed facts and hypotheses
- Document information gaps and unresolved questions

### SMART Criteria for Actions
- Every corrective action must pass the SMART test before inclusion in the report
- Vague actions like "improve monitoring" must be refined to "add latency P99 alert threshold at 500ms for service X by 2025-04-01"
- Each action must have a single accountable owner
- Track progress with measurable milestones

### Method Selection
- Use **5 Whys** for straightforward incidents with a clear causal chain
- Use **Fishbone** when multiple contributing factors across categories are suspected
- Use **FTA** for complex system failures requiring structural analysis of failure modes
- Combine methods when needed: Fishbone to identify categories, then 5 Whys to drill into each
