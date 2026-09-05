# Vendor Support Ticket Lifecycle Reference

## Ticket State Machine

```
┌─────────┐    vendor      ┌──────────────┐
│  open   │───acknowledges─▶│ acknowledged │
└─────────┘                 └──────────────┘
                                   │
                          work starts│
                                   ▼
                           ┌─────────────┐
              ┌────────────│ in-progress │◀──────────┐
              │            └─────────────┘           │
              │                   │                  │
    needs parts│          vendor waits│     customer responds
              ▼                   ▼                  │
    ┌────────────────┐   ┌──────────────────┐       │
    │ awaiting-parts │   │ awaiting-customer├───────┘
    └────────────────┘   └──────────────────┘
              │
    parts arrive│
              ▼
       ┌─────────────┐
       │ in-progress │──────────────────┐
       └─────────────┘                  │
                                   fix works│
                                        ▼
       ┌───────────┐   confirm    ┌──────────┐
       │  closed   │◀─────────────│ resolved │
       └───────────┘              └──────────┘

    Any state can transition to "escalated" via escalation action
```

## State Definitions

### open
- Ticket created, awaiting vendor acknowledgment
- Clock starts for SLA measurement
- Expected vendor response: 4-24 hours depending on priority

### acknowledged
- Vendor confirmed receipt of ticket
- Case number assigned
- Initial triage completed by vendor

### in-progress
- Vendor actively investigating or working on fix
- May involve remote diagnostics, log analysis, or on-site visit
- Regular updates expected (varies by vendor SLA)

### awaiting-parts
- RMA cases: replacement part ordered or in transit
- Tracking number should be logged when available
- Estimated arrival date should be recorded

### awaiting-customer
- Vendor requires customer action or information
- SLA clock typically pauses
- Auto-reminder after 3 days of inactivity

### escalated
- Issue elevated to higher support tier
- May involve vendor engineering team
- Typically triggers more aggressive SLA

### resolved
- Vendor reports issue fixed
- Customer confirmation pending
- Auto-close after 7 days if no objection

### closed
- Resolution confirmed by customer
- No further action required
- Ticket archived for historical reference

## Priority Levels

| Priority | Description | Initial Response SLA | Resolution Target |
|----------|-------------|---------------------|-------------------|
| critical | Production down, no workaround | 1 hour | 4 hours |
| high | Significant impact, workaround available | 4 hours | 24 hours |
| medium | Moderate impact, workaround acceptable | 8 hours | 72 hours |
| low | Minor issue, informational | 24 hours | 5 business days |

## Vendor-Specific Guidelines

### STX (Seagate Technology)

- Ticket prefix: `SR-YYYY-NNNNNN`
- RMA portal: Seagate Warranty Services
- SLA varies by support level (Standard/Premium/Enterprise)
- Escalation path: Support → Senior Engineer → Product Engineering

### Dell

- Ticket prefix: `DELL-NNNNNNN` or `SR-NNNNNNNNN`
- ProSupport vs Basic Support affects response times
- On-site dispatch available for enterprise contracts
- Escalation path: Support → Resolution Manager → Account Executive

### HP/HPE

- Ticket prefix: `HPE-NNNNNNNNN`
- Support Central portal for ticket tracking
- Proactive Care customers get faster response
- Escalation path: Support → Case Manager → Critical Account Manager

### Cisco

- Ticket prefix: `SR-NNNNNN-NNNNN`
- TAC (Technical Assistance Center) handles initial contact
- Severity 1-4 mapping different from priority levels
- Escalation path: TAC → BU Engineer → TAC Manager

## Escalation Triggers

Escalate a ticket when any of the following occur:

1. **SLA Breach**: Response or resolution target exceeded
2. **No Progress**: Status unchanged for threshold period (configurable, default 7 days)
3. **Recurring Issue**: Same problem returns after previous resolution
4. **Business Impact**: Impact increases beyond original assessment
5. **Customer Request**: Customer explicitly requests escalation
6. **Vendor Non-Responsive**: No response to follow-up attempts (3+ tries)

## Escalation Procedure

1. Document escalation reason in ticket timeline
2. Update ticket status to `escalated`
3. Contact vendor escalation path (phone preferred)
4. Request escalation confirmation number/case reference
5. Set follow-up reminder for next business day
6. Notify internal stakeholders if business-critical

## Timeline Entry Types

| Action Type | Description | Required Fields |
|-------------|-------------|-----------------|
| created | Ticket initially logged | subject, category, priority |
| status_change | State transition | from_status, to_status |
| note_added | Communication or update logged | notes |
| escalated | Ticket escalated | reason |
| attachment | File added to ticket | filename, description |
| contact_change | Primary contact updated | new_contact |
| sla_extended | SLA target adjusted | new_sla_target, reason |

## SLA Calculation

### SLA Clock Rules

- Clock starts at ticket creation (`open` state)
- Clock pauses when status is `awaiting-customer`
- Clock resumes when customer provides requested information
- Clock stops permanently when status is `resolved` or `closed`

### Business Hours Definition

- Default: Monday-Friday 9:00-18:00 local time
- Holidays excluded from SLA calculation
- 24/7 support contracts use calendar time

### SLA Breach Notification

- Warning at 80% of SLA target elapsed
- Breach notification when 100% reached
- Auto-escalation option when SLA breached

## Reporting Metrics

### Key Performance Indicators

| Metric | Description | Target |
|--------|-------------|--------|
| First Response Time | Time from open to acknowledged | < SLA target |
| Resolution Time | Time from open to resolved | < SLA target |
| Escalation Rate | % of tickets escalated | < 10% |
| Reopen Rate | % of tickets reopened after close | < 5% |
| Customer Satisfaction | Post-resolution survey score | > 4.0/5.0 |

### Dashboard Widgets

1. **Open Ticket Count**: By vendor, priority, status
2. **Aging Distribution**: Tickets by age bucket (0-3d, 4-7d, 8-14d, 15+d)
3. **SLA Compliance**: % meeting response/resolution targets
4. **Escalation Trend**: Escalations per week over time
5. **Stale Ticket Alert**: Tickets with no activity beyond threshold

## Integration Points

### Email Integration

Parse incoming vendor emails for:
- Ticket ID reference (regex patterns per vendor)
- Status keywords (shipped, resolved, waiting, etc.)
- Tracking numbers (carrier-specific formats)
- Scheduled dates (on-site visit, delivery ETA)

### Calendar Integration

- Create calendar events for scheduled vendor calls
- Set reminders for SLA warning thresholds
- Block time for on-site vendor visits

### Notification Integration

- Slack/Teams: New ticket, escalation, SLA warning
- Email: Daily digest of open tickets
- PagerDuty: Critical ticket escalation after hours
