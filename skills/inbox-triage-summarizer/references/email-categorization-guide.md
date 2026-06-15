# Email Categorization Guide

This document defines the classification criteria, action detection rules, and categorization logic used by the inbox-triage-summarizer skill.

## Classification Categories

### 1. FYI (For Your Information)

Emails that require no action from the recipient. Read and archive.

**Indicators**:
- CC/BCC recipient (not direct TO)
- Subject contains: "FYI", "For your information", "No action needed"
- Newsletter or automated notification
- Status update with no questions
- Meeting notes/minutes distribution
- Announcement or policy update

**Confidence Markers**:
- Sender is a no-reply address
- Email is part of a distribution list
- Previous messages in thread indicate completion

### 2. Requires Response

Emails that need a reply but no external deliverable.

**Indicators**:
- Direct question to recipient (contains "?")
- Request for confirmation: "Can you confirm", "Please confirm"
- Request for opinion: "What do you think", "Your thoughts"
- Request for approval: "Please approve", "Awaiting your sign-off"
- Scheduling request: "When are you available", "Can we schedule"
- Acknowledgment expected: "Please let me know", "Let me know if"

**Urgency Escalators**:
- "URGENT", "ASAP", "Time-sensitive"
- Explicit deadline: "by EOD", "before Friday", "within 24 hours"
- Escalation language: "following up", "second request", "reminder"
- VIP sender (executive, key client)

### 3. Requires Action

Emails that require work beyond just replying.

**Indicators**:
- Task assignment: "Please prepare", "Can you create", "Need you to"
- Document request: "Please send", "Attach the", "Share the file"
- Review request: "Please review", "Need your review", "Check the attached"
- Approval with work: "Review and approve", "Sign and return"
- Meeting prep: "Please prepare for", "Bring to the meeting"

**Action Keywords**:
- "Action required", "Action needed"
- "Please complete", "Please submit"
- "Deliverable", "Due by"
- "Update the", "Modify the", "Change the"

### 4. Blocked (Waiting on Others)

Threads where you've sent a message and are waiting for a response.

**Indicators**:
- Last message in thread was from you
- Contains unanswered question or request
- Waiting for external input: quote, approval, information
- Dependency on third party action

**Staleness Thresholds**:
- 2 days: Flag for monitoring
- 5 days: Recommend follow-up
- 10+ days: Escalation suggested

## Project/Client Detection

### Domain-Based Matching

Primary method for associating emails with projects.

```yaml
# Priority order:
1. Exact domain match: "user@client.com" → client project
2. Subdomain match: "user@sales.client.com" → client project
3. Partner domain: "user@agency-for-client.com" → client project (if configured)
```

### Subject-Based Matching

Secondary method using keywords and patterns.

```yaml
# Pattern types:
- Project code: "PROJ-123", "ALPHA-", "Q1-2024"
- Client name: "Alpha Corp", "Acme Inc"
- Project name: "Migration Project", "Phase 2"
```

### Thread Label Matching

For email systems with labels/folders.

```yaml
# Gmail labels:
- "clients/alpha" → client-alpha project
- "projects/migration" → migration project

# Outlook folders:
- "Projects/Alpha" → client-alpha project
```

### Sender Relationship

Use sender metadata for context.

```yaml
# Contact attributes:
- Company field: "Alpha Corp" → client-alpha
- Job title contains "Vendor" → vendor category
- Internal domain: "@mycompany.com" → internal-ops
```

## Thread Analysis

### Thread State Detection

Determine the current state of a conversation thread.

| State | Definition | Detection Rule |
|-------|------------|----------------|
| Active | Ongoing conversation | Messages within 3 days |
| Stale | Needs follow-up | No messages for 3-7 days |
| Dormant | May be abandoned | No messages for 7+ days |
| Completed | Thread concluded | Contains closing language |
| Waiting | Ball in their court | Your last message, no reply |

### Closing Language Patterns

Indicators that a thread is complete:

- "Thanks, this is resolved"
- "No further action needed"
- "Closing this thread"
- "All set, thank you"
- "This is complete"

### Re-opening Patterns

Indicators that a closed thread needs attention:

- "One more thing"
- "Following up on this"
- "Reopening this thread"
- "Sorry to bring this back"

## Urgency Scoring

### Score Components (0-100)

| Factor | Weight | Scoring |
|--------|--------|---------|
| Explicit deadline | 30 | 30 if within 24h, 20 if within 3 days, 10 if within week |
| Sender importance | 25 | 25 for exec/VIP, 15 for manager, 10 for peer, 5 for unknown |
| Language urgency | 20 | 20 for URGENT, 15 for ASAP, 10 for "when possible" |
| Thread staleness | 15 | 15 if 5+ days, 10 if 3+ days, 5 if 1+ day |
| Escalation markers | 10 | 10 for "second request", "reminder", "following up again" |

### Thresholds

- **Critical (80-100)**: Respond within 2 hours
- **High (60-79)**: Respond within 24 hours
- **Medium (40-59)**: Respond within 3 days
- **Low (0-39)**: Batch process weekly

## Classification Decision Tree

```
START
│
├─ Is recipient CC/BCC only?
│   └─ YES → FYI
│
├─ Is last message from me?
│   └─ YES → BLOCKED (waiting)
│
├─ Does it contain a task/deliverable request?
│   └─ YES → REQUIRES ACTION
│
├─ Does it contain a direct question or request for reply?
│   └─ YES → REQUIRES RESPONSE
│
├─ Is it a notification/newsletter/auto-generated?
│   └─ YES → FYI
│
└─ DEFAULT → REQUIRES RESPONSE (conservative)
```

## Integration Notes

### Export Format for email-triage-responder

When exporting action items for response drafting:

```json
{
  "export_version": "1.0",
  "source_skill": "inbox-triage-summarizer",
  "export_timestamp": "2024-01-15T09:00:00Z",
  "emails": [
    {
      "id": "msg_12345",
      "thread_id": "thread_abc",
      "classification": "requires_response",
      "urgency_score": 75,
      "project_id": "client-alpha",
      "context": {
        "thread_summary": "Discussion about Q1 deliverables",
        "sender_relationship": "primary_client_contact",
        "pending_question": "When can you send the updated timeline?"
      }
    }
  ]
}
```

### Scan History Format

Track previous scans to enable delta processing:

```json
{
  "scan_history": [
    {
      "scan_id": "scan_20240115_090000",
      "timestamp": "2024-01-15T09:00:00Z",
      "emails_processed": 87,
      "last_email_date": "2024-01-15T08:45:00Z",
      "message_ids": ["msg_001", "msg_002", "..."]
    }
  ],
  "last_scan": "scan_20240115_090000"
}
```
