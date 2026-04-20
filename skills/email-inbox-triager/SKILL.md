---
name: email-inbox-triager
description: Intelligent email inbox triage skill that analyzes incoming emails, classifies by urgency and action-required status, and generates prioritized daily email action plans. Use when user asks for email triage, inbox prioritization, email classification, or daily email action plans.
---

# Email Inbox Triager

## Overview

Analyze incoming emails from Gmail using gogcli integration, classify each message by urgency and action-type (response-needed, FYI, delegatable), and generate a prioritized daily action plan. The skill uses NLP-based heuristics to identify sender importance, deadline indicators, and response expectations.

## When to Use

- User requests email inbox triage or prioritization
- User asks "What emails need my attention today?"
- User wants to batch-process unread emails into action categories
- User needs to identify urgent emails requiring immediate response
- User wants to delegate or defer low-priority messages
- User asks for a daily email action plan

## Prerequisites

- Python 3.9+
- gogcli installed and authenticated (`gogcli auth status` returns OK)
- Gmail API access configured via gogcli
- No additional API keys required (uses gogcli OAuth)

## Workflow

### Step 1: Fetch Unread Emails via gogcli

Retrieve unread messages from Gmail inbox using gogcli.

```bash
# Fetch last 50 unread messages as JSON
gogcli gmail messages list --query "is:unread" --max-results 50 --format json > /tmp/unread_emails.json
```

If gogcli is not available, export emails manually to JSON with fields: `id`, `threadId`, `from`, `to`, `subject`, `snippet`, `date`, `labels`.

### Step 2: Run Email Classification Script

Analyze fetched emails and classify by urgency and action type.

```bash
python3 scripts/classify_emails.py \
  --input /tmp/unread_emails.json \
  --output /tmp/email_triage_report.json \
  --vip-domains "company.com,client.org" \
  --vip-senders "ceo@company.com,boss@company.com"
```

**Classification Categories:**

| Category | Criteria |
|----------|----------|
| `urgent-response` | VIP sender, deadline keywords, question marks, reply-expected signals |
| `response-needed` | Direct questions, action requests, not urgent |
| `fyi-read` | Newsletters, notifications, CC'd messages |
| `delegatable` | Can be forwarded to team member |
| `archive` | Promotional, automated, low-value |

### Step 3: Generate Daily Action Plan

Convert classification results into an actionable daily plan.

```bash
python3 scripts/generate_action_plan.py \
  --input /tmp/email_triage_report.json \
  --output /tmp/daily_email_plan.md \
  --time-budget 60
```

The `--time-budget` flag sets available minutes for email responses (default: 60).

### Step 4: Review and Execute Plan

1. Open `/tmp/daily_email_plan.md` to review prioritized action list
2. Process `urgent-response` emails first (estimated 5 min each)
3. Batch `response-needed` emails by topic for efficiency
4. Skim `fyi-read` items and archive after review
5. Forward `delegatable` items with context notes

## Output Format

### JSON Classification Report

```json
{
  "schema_version": "1.0",
  "generated_at": "2025-01-15T09:30:00Z",
  "total_emails": 47,
  "summary": {
    "urgent_response": 3,
    "response_needed": 8,
    "fyi_read": 20,
    "delegatable": 5,
    "archive": 11
  },
  "emails": [
    {
      "id": "msg_123",
      "thread_id": "thread_456",
      "from": "ceo@company.com",
      "subject": "Q4 Budget Review - Need Your Input by EOD",
      "snippet": "Please review the attached budget and...",
      "date": "2025-01-15T08:15:00Z",
      "classification": "urgent-response",
      "urgency_score": 95,
      "signals": ["vip_sender", "deadline_keyword", "direct_question"],
      "suggested_action": "Reply with budget feedback by 5pm",
      "estimated_minutes": 15
    }
  ]
}
```

### Markdown Daily Plan

```markdown
# Daily Email Action Plan - 2025-01-15

**Time Budget**: 60 minutes | **Emails to Process**: 16

## Urgent Response (3 emails, ~20 min)
1. **[CEO] Q4 Budget Review** - Reply with budget feedback by 5pm (15 min)
2. **[Client] Contract Question** - Clarify terms ASAP (5 min)
3. ...

## Response Needed (8 emails, ~30 min)
1. **[Team] Sprint Planning** - Confirm availability (3 min)
2. ...

## Delegate (5 emails)
- Forward "[Vendor] Invoice Query" to finance@company.com
- ...

## FYI / Read Later (20 emails)
- Skim and archive after review
```

## Resources

- `scripts/classify_emails.py` -- NLP-based email classifier with urgency scoring
- `scripts/generate_action_plan.py` -- Converts classification to daily plan
- `references/classification-rules.md` -- Detailed classification logic and signal weights
- `references/email-productivity-best-practices.md` -- Email management methodology

## Key Principles

1. **VIP-First**: Emails from known important senders always surface to the top
2. **Deadline-Aware**: Keywords like "EOD", "urgent", "ASAP" boost urgency score
3. **Batch Processing**: Group similar emails to reduce context-switching
4. **Time-Boxing**: Action plans respect declared time budgets
5. **Clear Next Actions**: Every email gets a suggested concrete action
