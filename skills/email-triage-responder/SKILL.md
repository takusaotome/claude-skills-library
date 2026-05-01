---
name: email-triage-responder
description: Analyze inbox emails to identify action-required items, prioritize by urgency/importance, classify by topic, and draft contextual replies. Use when triaging unread emails, prioritizing inbox, generating response drafts, or tracking email response status.
---

# Email Triage Responder

## Overview

Analyze inbox emails to identify action-required items, prioritize them by urgency and importance using a 4-quadrant matrix, classify by topic (vendor inquiry, internal request, client follow-up), and generate contextual draft responses in appropriate tone and language. Integrates with Gmail/Outlook via gogcli or MCP tools to surface unread emails requiring attention.

## When to Use

- Triaging a large inbox with many unread emails
- Prioritizing which emails need immediate attention
- Classifying emails by topic or sender type
- Generating draft responses for common email types
- Tracking response status across multiple emails
- Processing emails in bulk with consistent prioritization

## Prerequisites

- Python 3.9+
- `gogcli` configured with Gmail OAuth (for Gmail integration)
- Or Outlook MCP server configured (for Outlook integration)
- No additional API keys required beyond email access

## Workflow

### Step 1: Fetch Unread Emails

Use gogcli or MCP tools to retrieve unread emails from the inbox.

```bash
# Gmail via gogcli
gogcli gmail messages list --query "is:unread" --format json --max-results 50

# Or use MCP server for Outlook
# (MCP tool invocation handled by Claude)
```

### Step 2: Parse and Analyze Emails

Run the triage script to classify and prioritize emails.

```bash
python3 scripts/triage_emails.py \
  --input emails.json \
  --output triage_report.json
```

The script performs:
1. **Urgency Detection**: Identifies time-sensitive language, deadlines, escalation markers
2. **Importance Classification**: Evaluates sender (VIP, manager, client), CC/BCC patterns
3. **Topic Classification**: Categorizes as vendor inquiry, internal request, client follow-up, FYI, etc.
4. **Action Detection**: Determines if response, review, or delegation is needed

### Step 3: Generate Priority Matrix

Categorize emails into 4 quadrants:

| Quadrant | Urgency | Importance | Action |
|----------|---------|------------|--------|
| Q1 | High | High | Respond immediately |
| Q2 | Low | High | Schedule focused time |
| Q3 | High | Low | Delegate or quick reply |
| Q4 | Low | Low | Batch process or archive |

### Step 4: Draft Contextual Responses

For each action-required email, generate a draft response:

```bash
python3 scripts/triage_emails.py \
  --input emails.json \
  --output drafts.json \
  --generate-drafts \
  --tone professional \
  --language auto
```

Draft generation considers:
- **Tone**: Professional, friendly, formal (matches sender's tone)
- **Language**: Auto-detect from original email (EN, JA, etc.)
- **Context**: Previous thread history, sender relationship
- **Action Type**: Acknowledgment, answer, request for info, delegation

### Step 5: Track Response Status

Maintain a tracking file for email response status:

```bash
python3 scripts/triage_emails.py \
  --input emails.json \
  --status-file email_status.json \
  --update-status
```

Status tracking fields:
- `email_id`: Unique identifier
- `status`: pending, draft_ready, sent, delegated, archived
- `assigned_to`: Owner if delegated
- `due_date`: Expected response deadline
- `last_updated`: Timestamp of last status change

### Step 6: Generate Summary Report

Create a triage summary for review:

```bash
python3 scripts/triage_emails.py \
  --input emails.json \
  --output triage_report.md \
  --format markdown
```

## Output Format

### JSON Report

```json
{
  "schema_version": "1.0",
  "generated_at": "2024-01-15T09:30:00Z",
  "summary": {
    "total_emails": 25,
    "action_required": 12,
    "by_quadrant": {
      "Q1_urgent_important": 3,
      "Q2_important_not_urgent": 5,
      "Q3_urgent_not_important": 2,
      "Q4_neither": 15
    },
    "by_topic": {
      "client_followup": 4,
      "internal_request": 6,
      "vendor_inquiry": 3,
      "fyi_informational": 8,
      "meeting_scheduling": 4
    }
  },
  "emails": [
    {
      "id": "msg_12345",
      "from": "client@example.com",
      "subject": "Urgent: Contract Review Needed",
      "received_at": "2024-01-15T08:00:00Z",
      "quadrant": "Q1",
      "urgency_score": 0.9,
      "importance_score": 0.85,
      "topic": "client_followup",
      "action_required": "respond",
      "detected_deadline": "2024-01-16T17:00:00Z",
      "draft_response": "Thank you for sending the contract...",
      "status": "draft_ready"
    }
  ]
}
```

### Markdown Report

```markdown
# Email Triage Report

**Generated**: 2024-01-15 09:30 AM
**Total Emails**: 25 | **Action Required**: 12

## Priority Matrix

### Q1: Urgent & Important (3 emails)
| From | Subject | Deadline | Status |
|------|---------|----------|--------|
| client@example.com | Urgent: Contract Review | Jan 16 | Draft Ready |

### Q2: Important, Not Urgent (5 emails)
...

## Topic Breakdown

- Client Follow-ups: 4
- Internal Requests: 6
- Vendor Inquiries: 3

## Recommended Actions

1. **Respond immediately** to 3 Q1 emails
2. **Schedule 30 min** for 5 Q2 emails
3. **Delegate** 2 Q3 emails to team
```

## Resources

- `scripts/triage_emails.py` -- Main triage and draft generation script
- `references/email-classification.md` -- Topic taxonomy and urgency markers
- `references/response-templates.md` -- Draft response templates by category

## Key Principles

1. **Eisenhower Matrix**: Prioritize by urgency × importance, not just recency
2. **Context-Aware Drafts**: Match tone/language to sender and relationship
3. **Actionable Outputs**: Every email gets a clear next action (respond, delegate, archive)
4. **Batch Efficiency**: Process similar emails together to reduce context switching
5. **Status Tracking**: Maintain visibility into response pipeline to prevent dropped balls
