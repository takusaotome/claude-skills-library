# Incident Severity Matrix

## Overview

This document defines the incident severity classification system (P0-P4), response expectations, SLA evaluation criteria, and business impact calculation methodology. Use this matrix during Workflow 3 (Impact Assessment) to consistently classify and quantify incident severity.

---

## Severity Classification: P0-P4

### P0: Critical / 重大障害

**Definition**: Complete service outage, data loss, or active security breach affecting all or most users.

| Dimension | Criteria |
|-----------|----------|
| **Service Impact** | Complete unavailability of a core service; no workaround exists |
| **User Impact** | All users (100%) or all users of a critical business function affected |
| **Data Impact** | Confirmed data loss, data corruption, or active data breach |
| **Security Impact** | Active security breach, unauthorized access to sensitive data |
| **Business Impact** | Direct revenue loss; regulatory/legal exposure; brand reputation risk |

**Examples:**
- Production database complete failure with no replica failover
- Payment processing completely unavailable
- Customer PII data breach confirmed
- Authentication service down (no users can log in)
- Complete data center outage for primary region

**Response Expectations:**

| Metric | Target |
|--------|--------|
| Time to Detect (TTD) | < 5 minutes |
| Time to Respond (TTR) | < 15 minutes |
| Time to Mitigate (TTM) | < 1 hour |
| Time to Resolve (TTRe) | < 4 hours |
| Communication Cadence | Every 30 minutes to stakeholders |
| Escalation | Immediate executive notification |
| Post-Incident Review | Mandatory within 48 hours |

---

### P1: High / 高

**Definition**: Major feature or service significantly degraded, affecting a large portion of users with no adequate workaround.

| Dimension | Criteria |
|-----------|----------|
| **Service Impact** | Major feature unavailable or severely degraded; limited workaround may exist |
| **User Impact** | > 50% of users affected, or a critical user segment (e.g., paying customers) |
| **Data Impact** | Potential data inconsistency; no confirmed data loss |
| **Security Impact** | Vulnerability identified with potential for exploitation |
| **Business Impact** | Significant revenue impact; SLA breach likely; customer escalations |

**Examples:**
- Search functionality returning incorrect results for 60% of queries
- API response latency > 10x normal, causing client timeouts
- Mobile app crashes on launch for iOS 17+ users (65% of base)
- Email notification service down (transactions process but no confirmations)
- Partial data replication failure between regions

**Response Expectations:**

| Metric | Target |
|--------|--------|
| Time to Detect (TTD) | < 15 minutes |
| Time to Respond (TTR) | < 30 minutes |
| Time to Mitigate (TTM) | < 2 hours |
| Time to Resolve (TTRe) | < 8 hours |
| Communication Cadence | Every 1 hour to stakeholders |
| Escalation | Engineering leadership within 30 minutes |
| Post-Incident Review | Mandatory within 1 week |

---

### P2: Medium / 中

**Definition**: Minor feature unavailable or degraded, with a reasonable workaround available.

| Dimension | Criteria |
|-----------|----------|
| **Service Impact** | Non-critical feature unavailable; workaround exists and is documented |
| **User Impact** | 10-50% of users affected, or non-critical user segment |
| **Data Impact** | No data loss; minor data display issues possible |
| **Security Impact** | Low-risk vulnerability; no active exploitation |
| **Business Impact** | Minor revenue impact; SLA may be at risk; limited customer complaints |

**Examples:**
- Report export feature failing (users can view reports in-app)
- Dashboard loading slowly (15s instead of normal 3s)
- Notification preferences not saving (notifications still work with defaults)
- Search filters not working for one specific filter type
- Image upload failing for files > 5MB (smaller files work)

**Response Expectations:**

| Metric | Target |
|--------|--------|
| Time to Detect (TTD) | < 1 hour |
| Time to Respond (TTR) | < 2 hours |
| Time to Mitigate (TTM) | < 8 hours |
| Time to Resolve (TTRe) | < 24 hours |
| Communication Cadence | Daily update to stakeholders |
| Escalation | Team lead within 2 hours |
| Post-Incident Review | Recommended within 2 weeks |

---

### P3: Low / 低

**Definition**: Cosmetic issues or minor inconvenience with minimal user impact.

| Dimension | Criteria |
|-----------|----------|
| **Service Impact** | Cosmetic or minor UX issue; all functionality works correctly |
| **User Impact** | < 10% of users affected; inconvenience only |
| **Data Impact** | No data impact |
| **Security Impact** | Informational security finding; no risk |
| **Business Impact** | No measurable business impact |

**Examples:**
- UI alignment issue on one browser version
- Incorrect timezone display in audit logs (data is correct, display is wrong)
- Slow-loading avatar images on profile page
- Tooltip text showing raw HTML in one language locale
- Minor inconsistency in exported CSV column ordering

**Response Expectations:**

| Metric | Target |
|--------|--------|
| Time to Detect (TTD) | < 24 hours |
| Time to Respond (TTR) | < 1 business day |
| Time to Resolve (TTRe) | Next sprint / release cycle |
| Communication Cadence | Weekly status if unresolved |
| Post-Incident Review | Optional |

---

### P4: Informational / 情報

**Definition**: No user impact; internal-only observation or improvement opportunity.

| Dimension | Criteria |
|-----------|----------|
| **Service Impact** | No service impact; internal tooling or process issue |
| **User Impact** | No external user impact |
| **Data Impact** | No data impact |
| **Security Impact** | No security impact |
| **Business Impact** | No business impact; potential for future improvement |

**Examples:**
- Internal monitoring false positive alert
- Development environment instability
- Internal documentation inconsistency
- Non-critical dependency deprecation notice
- Build pipeline intermittent failure (retries succeed)

**Response Expectations:**

| Metric | Target |
|--------|--------|
| Time to Resolve (TTRe) | Backlog prioritization |
| Post-Incident Review | Not required |

---

## SLA Violation Evaluation

### SLA Compliance Check Procedure

For each affected service, evaluate against its SLA commitments:

1. **Identify applicable SLA**:
   - Service-specific SLA (if exists)
   - General platform SLA
   - Customer contract SLA (if applicable)

2. **Calculate downtime / degradation**:
   ```
   Downtime = Resolution_Time - Incident_Start_Time
   Degradation_Period = Time where performance < SLA threshold
   ```

3. **Evaluate against SLA targets**:

   | SLA Tier | Availability Target | Monthly Downtime Budget | Applicable Services |
   |----------|--------------------|-----------------------|-------------------|
   | Tier 1 | 99.99% | 4.3 minutes | Core payment, auth |
   | Tier 2 | 99.95% | 21.6 minutes | API, primary features |
   | Tier 3 | 99.9% | 43.2 minutes | Secondary features |
   | Tier 4 | 99.5% | 3.6 hours | Internal tools, batch |

4. **Determine SLA violation status**:
   - **Violated**: Downtime exceeds monthly budget
   - **At Risk**: Downtime > 50% of monthly budget remaining
   - **Compliant**: Downtime within budget

5. **Calculate remaining SLA budget**:
   ```
   Remaining_Budget = Monthly_Budget - (Previous_Downtime + Current_Incident_Downtime)
   ```

---

## Business Impact Calculation

### Impact Score Formula

```
Business_Impact_Score = Affected_Users x Duration_Hours x Severity_Weight x Revenue_Factor
```

### Severity Weights

| Severity | Weight | Description |
|----------|--------|-------------|
| P0 | 10.0 | Complete outage / data loss |
| P1 | 5.0 | Major degradation |
| P2 | 2.0 | Minor degradation with workaround |
| P3 | 0.5 | Cosmetic / inconvenience |
| P4 | 0.1 | Internal only |

### Revenue Factor

| Service Type | Revenue Factor | Rationale |
|-------------|---------------|-----------|
| Revenue-generating (payments, subscriptions) | 3.0 | Direct revenue loss |
| Customer-facing (portal, app) | 2.0 | Customer satisfaction, churn risk |
| Internal productivity (tools, CI/CD) | 1.0 | Operational cost |
| Non-critical (docs, static content) | 0.5 | Minimal business impact |

### Example Calculation

```
Incident: Payment API P1 outage
- Affected Users: 15,000
- Duration: 2.5 hours
- Severity Weight: 5.0 (P1)
- Revenue Factor: 3.0 (revenue-generating)

Business_Impact_Score = 15,000 x 2.5 x 5.0 x 3.0 = 562,500

Impact Category:
  > 100,000  → Critical Business Impact
  10,000-100,000 → High Business Impact
  1,000-10,000 → Medium Business Impact
  < 1,000 → Low Business Impact

Result: Critical Business Impact (562,500)
```

---

## 4-Axis Impact Assessment Template

Use this table when conducting impact assessment:

| Axis | Dimension | Assessment | Score (1-5) | Evidence |
|------|-----------|------------|-------------|----------|
| ユーザー影響 | Affected user count | {count} users | | |
| ユーザー影響 | User experience degradation | {description} | | |
| ユーザー影響 | User segment criticality | {segment details} | | |
| サービス影響 | Service availability | {uptime % during incident} | | |
| サービス影響 | Feature availability | {affected features} | | |
| サービス影響 | Performance degradation | {latency/throughput metrics} | | |
| ビジネス影響 | Revenue impact | {estimated $} | | |
| ビジネス影響 | SLA violation | {status and details} | | |
| ビジネス影響 | Contractual/legal exposure | {description} | | |
| ビジネス影響 | Brand/reputation risk | {description} | | |
| 運用影響 | Operational overhead | {person-hours spent} | | |
| 運用影響 | Team disruption | {teams affected, context switches} | | |
| 運用影響 | Cascading effects | {downstream impacts} | | |
| 運用影響 | Recovery complexity | {effort to fully resolve} | | |

### Scoring Guide

| Score | Label | Description |
|-------|-------|-------------|
| 1 | Negligible | No measurable impact |
| 2 | Minor | Small impact, easily managed |
| 3 | Moderate | Noticeable impact, requires attention |
| 4 | Major | Significant impact, urgent response needed |
| 5 | Severe | Critical impact, existential risk to service/business |

### Aggregate Impact Score

```
Aggregate = (User_Score x 0.30) + (Service_Score x 0.25) + (Business_Score x 0.30) + (Ops_Score x 0.15)
```

| Aggregate Score | Classification | Action Required |
|----------------|---------------|-----------------|
| 4.0 - 5.0 | Critical | Executive review, mandatory RCA, corrective actions within 1 week |
| 3.0 - 3.9 | High | Leadership review, mandatory RCA, corrective actions within 2 weeks |
| 2.0 - 2.9 | Medium | Team review, recommended RCA, corrective actions within 1 month |
| 1.0 - 1.9 | Low | Document and track, optional RCA |
