---
name: email-thread-summarizer
description: Analyze email threads to extract current status, pending actions, timeline of events, and identify stale/outdated information. Use when asked to summarize email conversations, find outstanding action items in email chains, or detect when a thread summary is out of date.
---

# Email Thread Summarizer

## Overview

Analyze email threads to extract structured intelligence: current status, pending actions, timeline of key events, and identification of stale/outdated information. The skill parses both Gmail (via gogcli) and Outlook email exports, producing actionable summaries with staleness detection for cached thread states.

## When to Use

- User asks to summarize an email thread or conversation chain
- User needs to identify outstanding action items from an email exchange
- User wants a timeline of key events/decisions from a long email thread
- User needs to detect if a previously cached thread summary is outdated
- User asks to analyze email thread status (resolved, pending, stale, escalated)
- User provides `.eml`, `.mbox`, or JSON email export files for analysis

## Prerequisites

- Python 3.9+
- No API keys required (works with exported email files)
- For live Gmail access: `gogcli` must be configured (see gogcli-expert skill)
- For live Outlook access: Microsoft Graph API token or exported `.eml` files
- Standard library plus `python-dateutil` for date parsing

## Workflow

### Step 1: Collect Email Thread Data

Obtain the email thread data from one of these sources:

**Option A: Gmail via gogcli**
```bash
gogcli gmail messages search --query "thread:THREAD_ID" --format json > thread_export.json
```

**Option B: Outlook via Graph API export**
```bash
# Export conversation to .eml files in a folder
```

**Option C: Direct file input**
- Provide `.eml`, `.mbox`, or JSON files containing the thread

### Step 2: Parse and Analyze Thread

Run the thread analyzer to extract structured information:

```bash
python3 scripts/analyze_thread.py \
  --input thread_export.json \
  --format gmail \
  --output thread_analysis.json
```

Supported formats: `gmail`, `outlook`, `eml`, `mbox`

### Step 3: Generate Summary Report

Generate a human-readable summary with action items:

```bash
python3 scripts/generate_summary.py \
  --analysis thread_analysis.json \
  --output thread_summary.md
```

### Step 4: Check for Staleness (Optional)

Compare current thread state against a cached summary to detect drift:

```bash
python3 scripts/check_staleness.py \
  --cached previous_summary.json \
  --current thread_analysis.json \
  --output staleness_report.json
```

### Step 5: Present Findings

Present the summary to the user with:
- Thread status classification (Active, Resolved, Stale, Escalated, Awaiting Response)
- Timeline of key events with dates
- List of pending action items with owners
- Staleness warnings if cached summary is outdated

## Output Format

### JSON Analysis Report

```json
{
  "schema_version": "1.0",
  "thread_id": "string",
  "subject": "string",
  "participants": [
    {"name": "string", "email": "string", "role": "initiator|responder|cc"}
  ],
  "message_count": 0,
  "date_range": {
    "first_message": "ISO8601",
    "last_message": "ISO8601",
    "duration_days": 0
  },
  "status": {
    "classification": "active|resolved|stale|escalated|awaiting_response",
    "confidence": 0.0,
    "last_action_date": "ISO8601",
    "days_since_last_action": 0
  },
  "timeline": [
    {
      "date": "ISO8601",
      "actor": "string",
      "event_type": "request|response|decision|escalation|resolution",
      "summary": "string"
    }
  ],
  "action_items": [
    {
      "id": "string",
      "description": "string",
      "owner": "string",
      "status": "pending|completed|cancelled",
      "due_date": "ISO8601|null",
      "source_message_date": "ISO8601"
    }
  ],
  "key_decisions": [
    {
      "date": "ISO8601",
      "decision": "string",
      "made_by": "string"
    }
  ],
  "outdated_info": [
    {
      "original_statement": "string",
      "stated_date": "ISO8601",
      "superseded_by": "string",
      "superseded_date": "ISO8601"
    }
  ],
  "analysis_timestamp": "ISO8601"
}
```

### Staleness Report

```json
{
  "schema_version": "1.0",
  "is_stale": true,
  "staleness_reasons": [
    {
      "type": "new_messages|status_change|action_item_update|decision_change",
      "description": "string",
      "severity": "low|medium|high"
    }
  ],
  "cached_summary_date": "ISO8601",
  "current_thread_date": "ISO8601",
  "new_messages_since_cache": 0,
  "recommendation": "refresh|review|ignore"
}
```

### Markdown Summary

```markdown
# Email Thread Summary

## Thread: [Subject]
**Status**: [Classification] | **Messages**: [N] | **Duration**: [X days]

## Participants
- **Initiator**: Name <email>
- **Responders**: Name1, Name2

## Current Status
[One paragraph describing current thread state]

## Timeline
| Date | Actor | Event |
|------|-------|-------|
| YYYY-MM-DD | Name | Summary |

## Pending Action Items
- [ ] [AI-001] Description (Owner, Due: YYYY-MM-DD)
- [ ] [AI-002] Description (Owner, Due: TBD)

## Key Decisions
1. **YYYY-MM-DD**: Decision text (by Name)

## Outdated Information
- ~~Original statement~~ superseded by: New information (YYYY-MM-DD)

---
*Generated: YYYY-MM-DD HH:MM UTC*
```

## Status Classification Logic

| Status | Criteria |
|--------|----------|
| **Active** | Last message within 3 business days, no clear resolution |
| **Resolved** | Contains resolution language ("resolved", "closed", "done", "thank you for...") |
| **Stale** | No activity for 7+ business days, has pending items |
| **Escalated** | Contains escalation indicators (CC to manager, "escalating", urgent markers) |
| **Awaiting Response** | Last message is a question or request, no response yet |

## Resources

- `scripts/analyze_thread.py` -- Parse email thread and extract structured data
- `scripts/generate_summary.py` -- Generate human-readable markdown summary
- `scripts/check_staleness.py` -- Compare cached vs current thread state
- `references/thread_analysis_patterns.md` -- Patterns for identifying action items, decisions, and status

## Key Principles

1. **Preserve context**: Always attribute statements to specific participants and dates
2. **Detect supersession**: Identify when later messages contradict or update earlier statements
3. **Action item extraction**: Use NLP patterns to find commitments, requests, and deadlines
4. **Staleness is signal**: An outdated summary can lead to missed follow-ups or duplicate work
5. **Multi-format support**: Handle Gmail JSON, Outlook exports, and raw .eml files uniformly
