# Email Prioritization Framework

## Overview

This framework defines the methodology for analyzing emails, extracting actionable items, and prioritizing them for efficient inbox management. It combines multiple signals to generate a composite urgency score and recommended action.

## Prioritization Model

### Multi-Factor Urgency Scoring

The urgency score is a weighted composite of five factors:

```
Urgency Score = (S × 0.30) + (D × 0.25) + (K × 0.20) + (T × 0.15) + (A × 0.10)

Where:
  S = Sender Priority Score (0-100)
  D = Deadline Proximity Score (0-100)
  K = Keyword Urgency Score (0-100)
  T = Thread Activity Score (0-100)
  A = Age Score (0-100)
```

### Factor Definitions

#### 1. Sender Priority Score (S)

Based on configured sender tiers:

| Tier | Score | Examples |
|------|-------|----------|
| VIP | 100 | CEO, Board members, Key clients |
| High | 75 | Direct manager, Legal, Important partners |
| Normal | 50 | Colleagues, Regular contacts |
| Low | 25 | Newsletters, Automated systems |
| Unknown | 40 | New senders (require attention) |

**Configuration patterns:**
- Exact match: `john.doe@company.com`
- Domain wildcard: `*@vip-client.com`
- Local part wildcard: `ceo@*`
- Combined: `*-exec@*.company.com`

#### 2. Deadline Proximity Score (D)

Calculated based on detected deadline relative to current time:

| Timeframe | Score | Description |
|-----------|-------|-------------|
| Overdue | 100 | Deadline has passed |
| Today | 95 | Due today |
| Tomorrow | 85 | Due within 24-48 hours |
| This week | 70 | Due within 7 days |
| Next week | 50 | Due within 14 days |
| This month | 30 | Due within 30 days |
| No deadline | 20 | No deadline detected |

**Deadline detection patterns:**
- ISO dates: `2024-01-15`, `01/15/2024`, `January 15, 2024`
- Relative: `by EOD`, `end of week`, `by Friday`, `within 24 hours`
- Contextual: `before our call`, `prior to the meeting`

#### 3. Keyword Urgency Score (K)

Based on presence of urgency indicators in subject and body:

| Keywords | Score Boost |
|----------|-------------|
| URGENT, ASAP, CRITICAL | +40 |
| Important, Priority, Time-sensitive | +25 |
| Please review, Action required | +15 |
| FYI, For your information | -20 |
| Automated, Notification | -30 |

**Scoring calculation:**
- Base score: 50
- Add/subtract based on keyword presence
- Cap between 0-100

#### 4. Thread Activity Score (T)

Based on email thread dynamics:

| Condition | Score |
|-----------|-------|
| "Waiting on you" indicator | 90 |
| Multiple recent replies (last 24h) | 80 |
| You're only recipient + question asked | 75 |
| Recent forward to you | 70 |
| Standard thread activity | 50 |
| No thread (standalone email) | 40 |
| Large CC list, passive | 20 |

#### 5. Age Score (A)

Older unanswered emails get higher priority:

| Age | Score |
|-----|-------|
| > 7 days unanswered | 100 |
| 4-7 days | 80 |
| 2-3 days | 60 |
| 1 day | 40 |
| Today | 20 |

## Urgency Level Classification

Based on composite urgency score:

| Score Range | Level | Recommended Response Time |
|-------------|-------|---------------------------|
| 90-100 | CRITICAL | Within 1 hour |
| 75-89 | HIGH | Within 4 hours |
| 50-74 | MEDIUM | Within 24 hours |
| 25-49 | LOW | Within 48-72 hours |
| 0-24 | MINIMAL | When convenient / Archive |

## Action Type Assignment

### Decision Tree

```
1. Is sender unknown AND contains link/attachment?
   → REVIEW (potential security)

2. Does email contain explicit question to you?
   → RESPOND

3. Does email request approval/sign-off?
   → REVIEW

4. Does email contain meeting invitation?
   → SCHEDULE

5. Does email describe task that could be delegated?
   → DELEGATE (if delegation rules match)
   → TASK (otherwise)

6. Is email CC'd to you with no direct ask?
   → FYI

7. Is email automated notification?
   → ARCHIVE

8. Default
   → REVIEW
```

### Delegation Detection

Email is a delegation candidate when:
1. Content matches another team member's expertise area
2. Sender is not VIP (VIP emails require personal response)
3. Task type is in delegatable categories:
   - Technical questions (→ Technical Lead)
   - Administrative requests (→ Admin Assistant)
   - Customer support (→ Support Team)
   - Scheduling logistics (→ Executive Assistant)

## Project Association

### Keyword Matching

Projects are associated via:
1. **Subject line tags**: `[Project-Alpha]`, `RE: Project Alpha`
2. **Thread context**: Previous messages mention project
3. **Sender domain**: `*@project-client.com`
4. **Body keywords**: Project-specific terminology

### Configuration Example

```yaml
project_associations:
  Q1-Budget:
    keywords: ["budget", "Q1 planning", "fiscal"]
    senders: ["*@finance.company.com"]

  Client-Acme:
    keywords: ["Acme", "Acme Corp", "acme project"]
    senders: ["*@acme.com"]
```

## Response Template Selection

Templates are selected based on:
1. **Action type**: Each action type has default templates
2. **Sender tier**: More formal for VIP/external
3. **Content analysis**: Specific templates for common scenarios

### Template Categories

| Category | Trigger | Example Template |
|----------|---------|------------------|
| Acknowledgment | Deadline request | "Thank you. I'll have this completed by [DATE]." |
| Clarification | Unclear request | "Could you please clarify [SPECIFIC POINT]?" |
| Delegation | Will forward | "I'm looping in [NAME] who handles this area." |
| Deferral | Busy period | "I'll review this after [DATE/EVENT]." |
| Completion | Task done | "Done. Please let me know if you need anything else." |

## Best Practices

### Daily Triage Workflow

1. **First pass (5 min)**: Scan CRITICAL items, respond or acknowledge
2. **Second pass (15 min)**: Process HIGH priority, delegate where possible
3. **Batch processing (30 min)**: Handle MEDIUM items in focused blocks
4. **End of day (5 min)**: Review LOW items, archive or schedule for later

### Sender Priority Maintenance

- Review VIP list monthly
- Add new important contacts immediately
- Remove inactive contacts quarterly
- Update domain patterns when organizations change

### Deadline Accuracy

- Confirm detected deadlines for CRITICAL items
- Account for timezone differences
- Consider buffer time for review cycles
- Flag ambiguous deadlines for clarification

## Metrics and Optimization

### Key Performance Indicators

| Metric | Target | Description |
|--------|--------|-------------|
| Response Time (CRITICAL) | < 1 hour | 95th percentile |
| Response Time (HIGH) | < 4 hours | 95th percentile |
| Inbox Zero Frequency | Daily | End of day empty inbox |
| Delegation Rate | 15-25% | Appropriate delegation |
| False Positive Rate | < 5% | Misclassified urgency |

### Continuous Improvement

1. Track override frequency (manual urgency changes)
2. Analyze response time vs. predicted urgency
3. Refine keyword weights based on actual outcomes
4. Update sender tiers based on interaction patterns
