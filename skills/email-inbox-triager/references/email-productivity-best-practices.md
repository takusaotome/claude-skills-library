# Email Productivity Best Practices

This reference document outlines proven methodologies for email management that inform the triage workflow.

## The 4D Email Processing Framework

### 1. Delete (Archive)
**When**: Email has no actionable content or future reference value.
- Marketing emails already reviewed
- Notifications from systems you monitor elsewhere
- Social media alerts
- Outdated announcements

**Rule**: If in doubt, archive rather than delete (searchable later).

### 2. Do
**When**: Response takes < 2 minutes.
- Quick confirmations
- Yes/no questions
- Brief acknowledgments
- Simple forwarding

**Rule**: Handle immediately to avoid reprocessing overhead.

### 3. Delegate
**When**: Someone else is better suited to respond.
- Topic outside your expertise
- Request for another department
- Routine tasks assignable to team

**Forward template**:
```
Hi [Name],

Forwarding this request as it falls within your area.
[Brief context if needed]

Original request from [Sender] regarding [Topic].

Thanks,
[Your name]
```

### 4. Defer
**When**: Response requires > 2 minutes or external input.
- Complex questions needing research
- Requests requiring approval from others
- Tasks dependent on other work completing

**Rule**: Add to task list with specific deadline; do NOT leave in inbox.

## Time-Boxing Email Sessions

### Recommended Schedule

| Session | Time | Duration | Focus |
|---------|------|----------|-------|
| Morning | 9:00 AM | 30 min | Triage + urgent responses |
| Midday | 12:30 PM | 15 min | Quick responses only |
| Afternoon | 4:00 PM | 30 min | Clear inbox, plan tomorrow |

### Anti-Patterns to Avoid

1. **Constant checking**: Disable notifications; check on schedule
2. **Inbox as task list**: Move actionable items to proper task system
3. **Reply-all abuse**: Only include necessary recipients
4. **Email for chat**: Use Slack/Teams for quick back-and-forth

## VIP Management Strategy

### Tier 1: Immediate Response (< 1 hour)
- Direct manager
- Executive leadership
- Key client escalations
- Time-sensitive operational issues

### Tier 2: Same-Day Response (< 4 hours)
- Cross-functional leadership
- Important clients
- Direct reports with blockers

### Tier 3: Standard SLA (< 24 hours)
- Colleagues
- Routine client communication
- External partners

## Email Triage Mental Model

```
┌─────────────────────────────────────────────────────────────┐
│                    INCOMING EMAIL                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Is it for me?  │
                    └─────────────────┘
                       │           │
                      Yes          No
                       │           │
                       ▼           ▼
              ┌────────────┐   ┌──────────┐
              │ Action     │   │ Archive  │
              │ required?  │   │ or FYI   │
              └────────────┘   └──────────┘
                 │       │
                Yes      No
                 │       │
                 ▼       ▼
         ┌──────────┐ ┌──────────┐
         │ < 2 min? │ │ FYI/Read │
         └──────────┘ └──────────┘
            │     │
           Yes    No
            │     │
            ▼     ▼
       ┌──────┐ ┌──────────┐
       │ Do   │ │ Delegate │
       │ Now  │ │ or Defer │
       └──────┘ └──────────┘
```

## Batch Processing Efficiency

### Group by Response Type
1. **Quick acknowledgments**: Batch similar confirmations
2. **Meeting scheduling**: Handle all calendar requests together
3. **Document reviews**: Allocate focused time block
4. **Complex responses**: One at a time with full attention

### Template Library

Maintain templates for common responses:

**Acknowledgment**:
> Thanks for sending this. I'll review and get back to you by [date].

**Clarification request**:
> Before I can proceed, could you clarify:
> 1. [Question 1]
> 2. [Question 2]

**Delegation notice**:
> I've forwarded this to [Name] who handles [Topic]. They'll follow up directly.

**Decline with alternative**:
> I'm unable to take this on right now. Have you considered [alternative]?

## Metrics for Email Health

### Personal KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Inbox zero frequency | Daily | End of day inbox count |
| Response time (urgent) | < 2 hours | Time from receipt to reply |
| Response time (standard) | < 24 hours | Time from receipt to reply |
| Unread email age | < 48 hours | Oldest unread email |
| Processing time | < 1 hour/day | Total email handling time |

### Warning Signs

- Unread count > 50: Triage immediately
- Oldest unread > 1 week: Declare email bankruptcy (archive all, start fresh)
- > 2 hours/day on email: Investigate root causes

## Integration with Task Management

### Email → Task Conversion

When deferring an email:
1. Create task with clear action verb
2. Include email link/reference
3. Set deadline based on sender expectations
4. Add to appropriate project/context

**Bad task**: "Reply to John's email"
**Good task**: "Send Q4 budget numbers to John by Friday"

### Follow-Up Tracking

For emails awaiting response:
1. BCC yourself or use "Send Later" with reminder
2. Add "Waiting For" tag/label
3. Review waiting items weekly
4. Send polite follow-up after SLA expires

## Email Writing for Better Responses

### Subject Line Best Practices

- **Action-oriented**: "Decision Needed: Q4 Budget by Friday"
- **Specific**: "Project Alpha Status Update - Week 12"
- **Searchable**: Include keywords for future retrieval

### Structure for Clarity

```
[One-line summary of ask]

[2-3 sentences of context]

[Specific questions or action items, numbered]

[Clear deadline if applicable]
```

### Reduce Back-and-Forth

- Anticipate questions and answer them preemptively
- Offer specific options rather than open-ended questions
- Include all necessary attachments/links
- Specify preferred response format

## Reference: Common Urgency Indicators

### High Urgency Keywords
- "Urgent", "ASAP", "Critical", "Emergency"
- "Today", "EOD", "End of day"
- "Immediately", "Right away"
- "Deadline", "Time-sensitive"
- "Escalation", "Priority"

### Moderate Urgency Keywords
- "This week", "By Friday"
- "When you get a chance"
- "Reminder", "Following up"
- "Quick question", "Brief ask"

### Low Urgency Indicators
- "FYI", "No action needed"
- "When convenient"
- "For your information"
- "Just sharing", "Thought you might like"
