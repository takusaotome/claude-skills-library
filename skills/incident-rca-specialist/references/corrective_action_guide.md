# Corrective Action Guide

## Overview

This guide provides a structured framework for developing effective corrective actions following root cause analysis. It covers the 3D Prevention Framework, time-horizon classification, SMART criteria application, and action ownership tracking. Use this guide during Workflow 7 (Corrective Action Planning).

---

## 1. 3D Prevention Framework

The 3D framework ensures corrective actions address prevention from three complementary angles. For each identified root cause, define actions across all three dimensions.

### Detect: Earlier Detection

**Goal**: Reduce Time to Detect (TTD) so future occurrences are caught before user impact.

**Strategies:**

| Strategy | Description | Example |
|----------|-------------|---------|
| Proactive monitoring | Add metrics and dashboards for leading indicators | CPU utilization trend alert at 70% (before 100% causes outage) |
| Alerting thresholds | Define thresholds based on SLIs/SLOs | P99 latency alert when > 200ms (SLO is 500ms) |
| Health checks | Implement deep health checks beyond simple ping | Synthetic transaction every 60s testing full checkout flow |
| Log-based detection | Alert on specific log patterns indicating emerging issues | Alert on error rate > 5% over 5-minute window |
| Anomaly detection | ML-based detection of unusual patterns | Traffic pattern anomaly detection for DDoS early warning |
| Canary deployments | Detect issues in small traffic slice before full rollout | 5% canary with automated rollback on error rate increase |
| User feedback loops | Enable rapid user-reported issue detection | In-app feedback widget with auto-categorization |

**Questions to Ask:**
- What signal would have told us this was happening before users noticed?
- What existing metrics were we not watching?
- What new metric would we need to create?
- Can we detect the precursor condition rather than the failure itself?

**Action Template:**
```
Detect Action: Add [metric/alert] for [signal] with threshold [value]
Dashboard: [name of dashboard to update/create]
Alert channel: [Slack channel / PagerDuty service]
Expected TTD improvement: From [current] to [target] minutes
```

---

### Defend: Prevention of Occurrence

**Goal**: Prevent the root cause from occurring in the first place through guardrails, validation, and automation.

**Strategies:**

| Strategy | Description | Example |
|----------|-------------|---------|
| Input validation | Validate inputs at system boundaries | Schema validation on configuration files before deployment |
| Automated testing | Add tests covering the failure scenario | Integration test simulating connection pool exhaustion |
| Code review gates | Require specific review for risky changes | Mandatory DBA review for schema migration PRs |
| Policy enforcement | Automate policy compliance | CI check that all new services include monitoring config |
| Immutable infrastructure | Prevent configuration drift | Terraform-managed infrastructure with drift detection |
| Feature flags | Control rollout with kill switches | Feature flag for new payment flow with instant disable |
| Rate limiting | Prevent resource exhaustion | Connection pool limits, request rate limits per client |
| Dependency management | Control dependency risks | Automated dependency update with security scanning |

**Questions to Ask:**
- What guardrail would have prevented this from happening?
- Can we automate the manual step that was missed?
- Can we make the "right thing" the default and the "wrong thing" harder to do?
- What validation should exist at the boundary where the error entered?

**Action Template:**
```
Defend Action: Implement [guardrail/validation] at [point in process]
Trigger: When [condition] occurs
Behavior: [block/warn/auto-correct]
Coverage: Prevents [specific failure mode]
```

---

### Degrade: Limiting Blast Radius

**Goal**: When failures do occur, limit their impact through graceful degradation, isolation, and fallback mechanisms.

**Strategies:**

| Strategy | Description | Example |
|----------|-------------|---------|
| Circuit breakers | Prevent cascading failures | Circuit breaker on payment provider calls with local queue fallback |
| Graceful degradation | Reduce functionality rather than total failure | Show cached product data when recommendation service is down |
| Bulkheads | Isolate failures to subsystems | Separate thread pools for critical vs. non-critical operations |
| Fallback mechanisms | Alternative paths when primary fails | Secondary DNS provider, CDN failover |
| Timeout enforcement | Prevent resource holding | 5s timeout on all external API calls with retry and fallback |
| Load shedding | Prioritize critical traffic | Shed non-essential API calls when load > 80% capacity |
| Multi-region/AZ | Geographic redundancy | Active-active deployment across 2+ availability zones |
| Data redundancy | Prevent data loss | Synchronous replication with automatic failover |
| Rollback automation | Quick recovery from bad deployments | Automated rollback triggered by error rate increase |

**Questions to Ask:**
- If this happens again, how can we limit the impact to fewer users?
- What is the smallest possible blast radius we can achieve?
- What can we serve from cache or fallback when the primary path fails?
- Can we isolate this component so its failure does not cascade?

**Action Template:**
```
Degrade Action: Implement [mechanism] for [service/component]
Failure mode: When [condition] occurs
Behavior: [degrade to / fallback to / shed]
Expected impact reduction: From [current blast radius] to [target blast radius]
```

---

## 2. Time-Horizon Classification

### Immediate Actions (即時対応) — 24-48 hours

**Characteristics:**
- Tactical fixes to prevent recurrence of the exact same failure
- Low risk, high confidence
- Can be implemented by the on-call or incident response team
- Do not require architectural changes

**Types:**
| Type | Example | Typical Effort |
|------|---------|---------------|
| Configuration fix | Increase connection pool size, adjust timeout | 1-2 hours |
| Monitoring addition | Add missing alert, update threshold | 2-4 hours |
| Runbook update | Document new failure mode and response steps | 2-4 hours |
| Hotfix deployment | Targeted code fix for the specific bug | 4-8 hours |
| Access/permission fix | Update IAM roles, adjust security groups | 1-2 hours |
| Communication update | Update status page, incident notification list | 1-2 hours |

### Short-Term Actions (短期対策) — 1-4 weeks

**Characteristics:**
- Systematic fixes addressing the process or system gap
- Moderate effort, may require sprint planning
- Cross-team coordination may be needed
- Includes validation and testing

**Types:**
| Type | Example | Typical Effort |
|------|---------|---------------|
| Process improvement | Add DB review step to deployment checklist | 1-2 weeks |
| Test coverage | Add integration tests for the failure scenario | 1-2 weeks |
| Automation | Automate manual validation step that was missed | 2-3 weeks |
| Tooling enhancement | Improve monitoring dashboard, add health checks | 1-2 weeks |
| Training | Conduct team training on new procedures | 1 week |
| Documentation | Comprehensive runbook for the service | 1-2 weeks |

### Long-Term Actions (長期対策) — 1-3 months

**Characteristics:**
- Architectural or organizational changes addressing systemic issues
- Significant effort requiring project planning
- May require budget approval
- Addresses classes of failures, not just this instance

**Types:**
| Type | Example | Typical Effort |
|------|---------|---------------|
| Architecture redesign | Migrate to multi-AZ deployment | 1-3 months |
| Platform migration | Move from manual to automated infrastructure | 2-3 months |
| Organizational change | Establish SRE team, define on-call rotation | 1-2 months |
| Tool replacement | Replace legacy monitoring with modern observability platform | 2-3 months |
| Capacity planning | Implement automated scaling with load testing | 1-2 months |
| Resilience engineering | Chaos engineering program, game days | 2-3 months |

---

## 3. SMART Criteria for Corrective Actions

Every corrective action MUST pass the SMART test before inclusion in the report.

### S - Specific（具体的）

**Bad**: "Improve monitoring"
**Good**: "Add P99 latency alert for payment-api service with threshold 500ms and 5-minute evaluation window, routing to #payment-oncall Slack channel and PagerDuty"

**Checklist:**
- [ ] What exactly will be changed/added/removed?
- [ ] Which specific system, service, or process?
- [ ] What is the precise configuration or implementation?

### M - Measurable（測定可能）

**Bad**: "Reduce incident response time"
**Good**: "Reduce TTD from 45 minutes (current) to < 5 minutes by implementing synthetic monitoring"

**Checklist:**
- [ ] What is the current state (baseline)?
- [ ] What is the target state (goal)?
- [ ] How will success be measured?
- [ ] What metric or evidence will confirm completion?

### A - Achievable（達成可能）

**Bad**: "Achieve 100% uptime"
**Good**: "Achieve 99.95% availability for payment-api by adding redundancy to the database layer"

**Checklist:**
- [ ] Are the required resources (people, budget, tools) available?
- [ ] Is the timeline realistic given other commitments?
- [ ] Does the team have the skills to implement this?
- [ ] Are there known blockers or dependencies?

### R - Relevant（関連性）

**Bad**: "Migrate entire infrastructure to Kubernetes" (when incident was about a missing alert)
**Good**: "Add connection pool monitoring to prevent undetected resource exhaustion"

**Checklist:**
- [ ] Does this action directly address an identified root cause?
- [ ] Would this action have prevented or mitigated this specific incident?
- [ ] Is the effort proportional to the risk being addressed?

### T - Time-bound（期限付き）

**Bad**: "Implement when possible"
**Good**: "Complete by 2025-04-15. Milestone 1: Design review by 2025-04-01. Milestone 2: Implementation by 2025-04-10. Milestone 3: Testing and deployment by 2025-04-15."

**Checklist:**
- [ ] Is there a clear deadline?
- [ ] Are there intermediate milestones?
- [ ] Is the deadline aligned with the time-horizon classification?

---

## 4. Action Ownership and Tracking

### Ownership Rules

1. **Single owner per action**: Every action must have exactly one accountable person
2. **Owner authority**: The owner must have authority to execute or escalate
3. **Owner acceptance**: The owner must acknowledge and accept the assignment
4. **Escalation path**: Define who to escalate to if blocked

### Tracking Cadence

| Time Horizon | Review Cadence | Review Forum |
|-------------|---------------|-------------|
| Immediate | Daily until complete | Standup / Slack update |
| Short-term | Weekly | Sprint review / team meeting |
| Long-term | Bi-weekly | Engineering review / leadership meeting |

### Status Definitions

| Status | Definition | Action Required |
|--------|-----------|-----------------|
| Not Started | Action acknowledged but work not begun | Verify start date is approaching |
| In Progress | Active work underway | Review progress at next cadence |
| Blocked | Cannot proceed due to dependency | Escalate to remove blocker |
| In Review | Implementation complete, pending validation | Review and validate |
| Completed | Action verified as effective | Close with evidence of completion |
| Deferred | Postponed with leadership approval | Document reason, set new target date |
| Cancelled | No longer relevant | Document reason for cancellation |

### Completion Criteria

An action is considered complete when:
1. The implementation is deployed to production
2. The effectiveness can be demonstrated (e.g., alert fires correctly in test)
3. Documentation is updated to reflect the change
4. The owner confirms completion with evidence
5. A reviewer validates the completion

---

## 5. Corrective Action Examples by Root Cause Type

### Root Cause: Missing Monitoring

| 3D | Action | Timeline | SMART Target |
|----|--------|----------|-------------|
| Detect | Add service health dashboard with key SLIs | Immediate | Dashboard live within 48h with 5 SLI panels |
| Detect | Configure P99 latency alert at 500ms threshold | Immediate | Alert tested and verified within 24h |
| Defend | Add monitoring config as required field in service template | Short-term | CI blocks service deployment without monitoring config by Sprint 12 |
| Degrade | Implement synthetic monitoring with automated failover trigger | Long-term | Synthetic checks every 60s with auto-failover within 2min by Q2 |

### Root Cause: Process Gap (No Review)

| 3D | Action | Timeline | SMART Target |
|----|--------|----------|-------------|
| Detect | Add PR label for "requires-DBA-review" when migration files changed | Immediate | GitHub Action deployed within 48h |
| Defend | Make DBA review mandatory for schema changes in CI pipeline | Short-term | CI gate blocking merges without DBA approval by Sprint 12 |
| Defend | Create database change runbook with performance checklist | Short-term | Runbook published and team trained within 2 weeks |
| Degrade | Implement schema migration rollback automation | Long-term | Automated rollback tested and deployed by Q2 |

### Root Cause: Single Point of Failure

| 3D | Action | Timeline | SMART Target |
|----|--------|----------|-------------|
| Detect | Add SPOF detection to architecture review checklist | Immediate | Checklist updated within 48h |
| Defend | Deploy service to 2+ availability zones | Long-term | Multi-AZ deployment complete with failover tested by Q3 |
| Degrade | Implement circuit breaker pattern for dependent services | Short-term | Circuit breakers on top 5 critical dependencies within 3 weeks |
| Degrade | Add local cache as fallback for external service calls | Short-term | Cache layer with 5-minute TTL implemented within 2 weeks |
