# Incident Timeline Template

## Overview

This template provides a standardized Mermaid gantt diagram format for visualizing incident timelines, along with time metric calculation formulas and examples. Use this template during Workflow 2 (Timeline Construction).

---

## Time Metric Definitions

| Metric | Full Name | Definition | Start | End |
|--------|-----------|-----------|-------|-----|
| **TTD** | Time to Detect | Time from incident start to detection | Incident begins | Incident detected |
| **TTR** | Time to Respond | Time from detection to first response action | Incident detected | First response action taken |
| **TTM** | Time to Mitigate | Time from first response to user impact reduced | First response action | Impact mitigated (partial recovery) |
| **TTRe** | Time to Resolve | Time from mitigation to full resolution | Impact mitigated | Full service restoration |
| **TTI** | Total Time of Impact | Total duration of user-facing impact | Incident begins | Full service restoration |

### Metric Relationships

```
TTI (Total Time of Impact) = TTD + TTR + TTM + TTRe

|← TTD →|← TTR →|← TTM →|←── TTRe ──→|
|        |        |        |             |
Start   Detect  Respond  Mitigate    Resolve
```

---

## Mermaid Gantt Template

### Basic Template

Replace all `{PLACEHOLDER}` values with actual incident data.

```mermaid
gantt
    title Incident Timeline: {INCIDENT_ID} - {INCIDENT_TITLE}
    dateFormat YYYY-MM-DDTHH:mm
    axisFormat %H:%M

    section Incident Phases
    TTD: Incident Start → Detection          :crit, ttd, {INCIDENT_START}, {TTD_DURATION}
    TTR: Detection → First Response          :active, ttr, after ttd, {TTR_DURATION}
    TTM: First Response → Mitigation         :ttm, after ttr, {TTM_DURATION}
    TTRe: Mitigation → Full Resolution       :done, ttre, after ttm, {TTRE_DURATION}

    section Key Events
    {EVENT_1}: Alert triggered               :milestone, m1, {EVENT_1_TIME}, 0min
    {EVENT_2}: Incident commander assigned   :milestone, m2, {EVENT_2_TIME}, 0min
    {EVENT_3}: Root cause identified         :milestone, m3, {EVENT_3_TIME}, 0min
    {EVENT_4}: Fix deployed                  :milestone, m4, {EVENT_4_TIME}, 0min
    {EVENT_5}: Service fully restored        :milestone, m5, {EVENT_5_TIME}, 0min

    section Communications
    Internal notification sent               :milestone, c1, {INTERNAL_NOTIFY_TIME}, 0min
    Status page updated                      :milestone, c2, {STATUS_PAGE_TIME}, 0min
    Customer communication sent              :milestone, c3, {CUSTOMER_NOTIFY_TIME}, 0min
    All-clear notification                   :milestone, c4, {ALL_CLEAR_TIME}, 0min
```

### Duration Format Guide

Mermaid gantt supports these duration formats:

| Format | Example | Meaning |
|--------|---------|---------|
| `Xmin` | `15min` | 15 minutes |
| `Xh` | `2h` | 2 hours |
| Absolute time | `2025-03-15T14:37` | Specific timestamp |
| `after taskid` | `after ttd` | Starts after referenced task |

---

## Detailed Timeline Example

### Example: E-Commerce Payment Outage

```mermaid
gantt
    title Incident Timeline: INC-20250315-001 - Payment API Outage
    dateFormat YYYY-MM-DDTHH:mm
    axisFormat %H:%M

    section Incident Phases
    TTD (5 min)                              :crit, ttd, 2025-03-15T14:22, 5min
    TTR (8 min)                              :active, ttr, after ttd, 8min
    TTM (22 min)                             :ttm, after ttr, 22min
    TTRe (12 min)                            :done, ttre, after ttm, 12min

    section Key Events
    First 503 errors appear                  :milestone, e1, 2025-03-15T14:22, 0min
    Monitoring alert fires                   :milestone, e2, 2025-03-15T14:27, 0min
    On-call engineer acknowledges            :milestone, e3, 2025-03-15T14:30, 0min
    Incident channel created                 :milestone, e4, 2025-03-15T14:32, 0min
    DB connection pool identified            :milestone, e5, 2025-03-15T14:35, 0min
    Connection pool limit increased          :milestone, e6, 2025-03-15T14:42, 0min
    Traffic begins recovering                :milestone, e7, 2025-03-15T14:45, 0min
    Partial recovery confirmed               :milestone, e8, 2025-03-15T14:57, 0min
    Missing index added                      :milestone, e9, 2025-03-15T15:02, 0min
    Full service restoration                 :milestone, e10, 2025-03-15T15:09, 0min

    section Communications
    PagerDuty alert sent                     :milestone, c1, 2025-03-15T14:27, 0min
    Status page: Investigating               :milestone, c2, 2025-03-15T14:33, 0min
    Slack: #incident-20250315 created        :milestone, c3, 2025-03-15T14:32, 0min
    Status page: Identified                  :milestone, c4, 2025-03-15T14:42, 0min
    Status page: Monitoring                  :milestone, c5, 2025-03-15T14:57, 0min
    Status page: Resolved                    :milestone, c6, 2025-03-15T15:09, 0min
```

### Example Metrics Summary

| Metric | Value | Target | Assessment |
|--------|-------|--------|------------|
| TTD | 5 min | < 5 min | Borderline (5 min = target limit) |
| TTR | 8 min | < 15 min | Met |
| TTM | 22 min | < 60 min | Met |
| TTRe | 12 min | < 4 hours | Met |
| TTI (Total) | 47 min | < 4 hours | Met |

---

## Extended Template: Multi-Team Response

For incidents involving multiple teams, use the team section format:

```mermaid
gantt
    title Incident Timeline: {INCIDENT_ID} - Multi-Team Response
    dateFormat YYYY-MM-DDTHH:mm
    axisFormat %H:%M

    section Incident Phases
    TTD                                      :crit, ttd, {START}, {TTD_DURATION}
    TTR                                      :active, ttr, after ttd, {TTR_DURATION}
    TTM                                      :ttm, after ttr, {TTM_DURATION}
    TTRe                                     :done, ttre, after ttm, {TTRE_DURATION}

    section SRE Team
    Alert received                           :milestone, sre1, {TIME}, 0min
    Initial triage                           :sre_triage, {TIME}, {DURATION}
    Infrastructure investigation             :sre_invest, after sre_triage, {DURATION}
    Connection pool fix applied              :milestone, sre2, {TIME}, 0min

    section Backend Team
    Paged and joined                         :milestone, be1, {TIME}, 0min
    Code-level investigation                 :be_invest, {TIME}, {DURATION}
    Hotfix developed                         :be_fix, after be_invest, {DURATION}
    Hotfix deployed                          :milestone, be2, {TIME}, 0min

    section Database Team
    Consulted on DB issues                   :milestone, db1, {TIME}, 0min
    Index analysis                           :db_analysis, {TIME}, {DURATION}
    Index applied to production              :milestone, db2, {TIME}, 0min

    section Communications
    Internal: Incident declared              :milestone, com1, {TIME}, 0min
    External: Status page updated            :milestone, com2, {TIME}, 0min
    External: Resolution communicated        :milestone, com3, {TIME}, 0min
```

---

## Bottleneck Analysis Guide

After constructing the timeline, analyze for bottlenecks:

### Common Bottleneck Patterns

| Pattern | Indicator | Typical Root Cause | Improvement |
|---------|-----------|-------------------|-------------|
| **Slow Detection** | TTD >> target | Missing monitoring, wrong thresholds | Add/tune monitoring and alerts |
| **Slow Response** | TTR >> target | On-call not available, unclear escalation | Improve on-call process, automate paging |
| **Long Diagnosis** | Large gap between Response and Mitigation | Insufficient observability, unfamiliar system | Improve runbooks, dashboards, training |
| **Delayed Mitigation** | TTM >> target despite known cause | No quick mitigation option, complex rollback | Add feature flags, rollback automation |
| **Slow Resolution** | TTRe >> target | Root fix is complex, requires development | Invest in long-term architectural resilience |
| **Communication Gaps** | Large gaps between events and comms | No communication protocol, unclear ownership | Define communication cadence and ownership |

### Bottleneck Identification Checklist

- [ ] Which phase took the longest relative to its target?
- [ ] Were there idle periods where no one was actively working?
- [ ] Were handoffs between teams smooth or delayed?
- [ ] Was escalation timely and to the right people?
- [ ] Were communications sent proactively or only reactively?
- [ ] Was the right tooling available for diagnosis?
- [ ] Were runbooks consulted and were they helpful?
