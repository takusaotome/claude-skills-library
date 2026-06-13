---
name: inbox-triage-summarizer
description: Periodic inbox scan that categorizes new emails by project/client, identifies action-required items, and generates prioritized summary with FYI/requires-response/requires-action/blocked-waiting classifications. Use for inbox overview, project-based email grouping, or action item extraction.
---

# Inbox Triage Summarizer

## Overview

Perform periodic inbox scans to categorize incoming emails by project, client, or topic, then generate a prioritized summary report. Unlike email-triage-responder (which focuses on individual email analysis and draft generation), this skill provides a high-level overview of inbox state with actionable groupings and status classifications (FYI, requires-response, requires-action, blocked-waiting-on-others).

## When to Use

- Running a periodic inbox review (daily, weekly) to understand backlog
- Grouping emails by project or client for focused processing
- Identifying blocked items waiting on external responses
- Generating an executive summary of inbox state for team standup
- Feeding action-required emails to email-triage-responder for response drafting
- Tracking email conversation threads across multiple messages

## Prerequisites

- Python 3.9+
- `gogcli` configured with Gmail OAuth (for Gmail integration)
- Or Outlook MCP server configured (for Outlook integration)
- No additional API keys required beyond email access

## Workflow

### Step 1: Fetch New Emails Since Last Scan

Use gogcli or MCP tools to retrieve emails since the last triage scan.

```bash
# Gmail via gogcli - last 7 days
gogcli gmail messages list \
  --query "is:inbox after:$(date -v-7d +%Y/%m/%d)" \
  --format json --max-results 200

# Or filter by unread only
gogcli gmail messages list \
  --query "is:unread" \
  --format json --max-results 100
```

### Step 2: Parse and Categorize Emails

Run the triage summarizer script to categorize emails by project/client.

```bash
python3 scripts/triage_inbox.py \
  --input emails.json \
  --output triage_summary.json \
  --project-rules references/project-mapping.yaml
```

The script performs:
1. **Project/Client Detection**: Match sender domain, subject keywords, or thread ID to known projects
2. **Action Classification**: Assign each email to FYI, requires-response, requires-action, or blocked-waiting
3. **Thread Correlation**: Group related emails by conversation thread
4. **Staleness Detection**: Flag threads with no activity for N days

### Step 3: Generate Prioritized Summary

Create the summary report with grouped action items.

```bash
python3 scripts/triage_inbox.py \
  --input emails.json \
  --output summary_report.md \
  --format markdown \
  --group-by project
```

Grouping options:
- `project` -- Group by detected project/client
- `action` -- Group by action classification
- `sender` -- Group by sender domain
- `date` -- Group by received date

### Step 4: Export Action Items for Response Drafting

Extract action-required emails for downstream processing with email-triage-responder.

```bash
python3 scripts/triage_inbox.py \
  --input emails.json \
  --output action_items.json \
  --export-action-items \
  --classifications requires-response,requires-action
```

### Step 5: Track Scan History

Maintain scan history to enable delta-based processing.

```bash
python3 scripts/triage_inbox.py \
  --input emails.json \
  --scan-history .inbox-triage-history.json \
  --mark-scanned
```

## Output Format

### JSON Summary

```json
{
  "schema_version": "1.0",
  "scan_timestamp": "2024-01-15T09:00:00Z",
  "scan_period": {
    "start": "2024-01-08T00:00:00Z",
    "end": "2024-01-15T09:00:00Z"
  },
  "summary": {
    "total_emails": 87,
    "new_since_last_scan": 32,
    "by_classification": {
      "fyi": 45,
      "requires_response": 18,
      "requires_action": 12,
      "blocked_waiting": 8,
      "unknown": 4
    },
    "by_project": {
      "client-alpha": 15,
      "internal-ops": 22,
      "vendor-acme": 8,
      "unassigned": 42
    }
  },
  "projects": [
    {
      "project_id": "client-alpha",
      "display_name": "Alpha Corp Project",
      "email_count": 15,
      "action_required_count": 5,
      "blocked_count": 2,
      "oldest_unanswered": "2024-01-10T14:30:00Z",
      "threads": [
        {
          "thread_id": "thread_abc123",
          "subject": "Q1 Deliverables Review",
          "participants": ["alice@alpha.com", "bob@mycompany.com"],
          "message_count": 4,
          "last_message_from": "alice@alpha.com",
          "classification": "requires_response",
          "staleness_days": 3
        }
      ]
    }
  ],
  "action_items": [
    {
      "email_id": "msg_12345",
      "thread_id": "thread_abc123",
      "project_id": "client-alpha",
      "from": "alice@alpha.com",
      "subject": "Q1 Deliverables Review",
      "classification": "requires_response",
      "detected_deadline": "2024-01-17",
      "urgency_indicators": ["waiting for your feedback", "by EOW"],
      "recommended_action": "Reply with status update on deliverables"
    }
  ],
  "blocked_items": [
    {
      "email_id": "msg_67890",
      "thread_id": "thread_xyz789",
      "project_id": "vendor-acme",
      "waiting_on": "vendor@acme.com",
      "last_sent": "2024-01-12T10:00:00Z",
      "days_waiting": 3,
      "subject": "License Renewal Quote Request",
      "recommended_action": "Send follow-up if no response by Jan 16"
    }
  ]
}
```

### Markdown Report

```markdown
# Inbox Triage Summary

**Scan Period**: Jan 8 - Jan 15, 2024
**Total Emails**: 87 | **New Since Last Scan**: 32

## Action Summary

| Classification | Count | % |
|----------------|-------|---|
| FYI (no action) | 45 | 52% |
| Requires Response | 18 | 21% |
| Requires Action | 12 | 14% |
| Blocked (waiting) | 8 | 9% |
| Unknown | 4 | 4% |

## By Project

### Client Alpha (15 emails, 5 action required)

**Blocked**: 2 threads waiting on external response

| Subject | From | Classification | Staleness |
|---------|------|----------------|-----------|
| Q1 Deliverables Review | alice@alpha.com | Requires Response | 3 days |
| Contract Amendment | legal@alpha.com | Requires Action | 1 day |

### Internal Ops (22 emails, 3 action required)

...

## Recommended Actions

1. **Respond** to 5 client-alpha emails (oldest: 3 days)
2. **Follow up** on 2 blocked vendor threads (waiting 3+ days)
3. **Batch process** 12 FYI emails from internal-ops

## Integration with email-triage-responder

Action items exported to `action_items.json` for response drafting:
- 18 emails classified as requires-response
- 12 emails classified as requires-action

Run: `python3 ../email-triage-responder/scripts/triage_emails.py --input action_items.json --generate-drafts`
```

## Project Mapping Configuration

Create `references/project-mapping.yaml` to define project detection rules:

```yaml
projects:
  - id: client-alpha
    display_name: Alpha Corp Project
    match_rules:
      - type: sender_domain
        pattern: "@alpha.com"
      - type: subject_contains
        pattern: "Alpha|ALPHA-"
      - type: thread_label
        pattern: "client/alpha"

  - id: vendor-acme
    display_name: ACME Vendor
    match_rules:
      - type: sender_domain
        pattern: "@acme.com"
      - type: subject_contains
        pattern: "ACME|License"

default_project: unassigned
```

## Resources

- `scripts/triage_inbox.py` -- Main inbox triage and summarization script
- `references/email-categorization-guide.md` -- Classification criteria and action detection rules
- `references/project-mapping.yaml` -- Example project/client detection configuration

## Key Principles

1. **Project-Centric View**: Group emails by project/client for focused batch processing
2. **Clear Action Classification**: Every email gets one of four action states (FYI/response/action/blocked)
3. **Thread Awareness**: Track conversation threads, not just individual messages
4. **Staleness Tracking**: Surface threads that need follow-up based on age
5. **Integration Ready**: Export format compatible with email-triage-responder for response drafting
