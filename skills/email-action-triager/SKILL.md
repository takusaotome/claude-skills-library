---
name: email-action-triager
description: Analyze inbox emails to identify actionable items, categorize by urgency/owner, and generate prioritized daily action lists. Use when processing unread/flagged emails, creating task lists from inbox, identifying urgent communications, or planning email-based workflow. Triggers on "triage my inbox", "email action items", "prioritize emails", "what emails need action".
---

# Email Action Triager

## Overview

Email Action Triager analyzes inbox emails to extract actionable items, categorize them by urgency and owner, and generate prioritized daily action lists. It applies business rules including sender priority scoring, deadline detection, project association, and context-aware prioritization to transform a chaotic inbox into a structured task list with recommended responses or delegation suggestions.

## When to Use

- Triaging a backlog of unread emails to identify what needs action
- Creating a daily action list from inbox communications
- Identifying urgent emails that require immediate response
- Categorizing emails by project, sender priority, or deadline
- Generating delegation recommendations for team emails
- Analyzing email patterns to optimize response workflows
- Processing Gmail exports or API data for action extraction

## Prerequisites

- Python 3.9+
- Gmail API credentials (OAuth2) for live inbox access, OR email export files (MBOX/EML)
- Environment variables:
  - `GMAIL_CREDENTIALS_PATH` -- Path to OAuth2 credentials JSON (optional, for API access)
  - `GMAIL_TOKEN_PATH` -- Path to token storage (optional, defaults to `~/.gmail_token.json`)
- Dependencies: `google-auth`, `google-auth-oauthlib`, `google-api-python-client` (for Gmail API)

## Workflow

### Step 1: Configure Email Source

Choose between Gmail API access or local email file processing.

**For Gmail API:**
```bash
# Set credentials path
export GMAIL_CREDENTIALS_PATH=/path/to/credentials.json

# First run will prompt OAuth2 authorization
python3 scripts/triage_emails.py --source gmail --max-emails 100
```

**For Local Email Files:**
```bash
# Process MBOX export
python3 scripts/triage_emails.py --source file --input emails.mbox

# Process EML files in directory
python3 scripts/triage_emails.py --source file --input ./email_folder/
```

### Step 2: Apply Business Rules Configuration

Create or update the business rules configuration file to customize prioritization.

```bash
# Generate default config
python3 scripts/triage_emails.py --generate-config > email_rules.yaml

# Run with custom rules
python3 scripts/triage_emails.py --source gmail --rules email_rules.yaml
```

**Configuration includes:**
- Sender priority tiers (VIP, High, Normal, Low)
- Project keyword associations
- Deadline detection patterns
- Auto-delegation rules
- Response template triggers

### Step 3: Run Triage Analysis

Execute the triage process to analyze emails and generate action items.

```bash
python3 scripts/triage_emails.py \
  --source gmail \
  --max-emails 100 \
  --rules email_rules.yaml \
  --output-format json \
  --output triage_results.json
```

### Step 4: Generate Daily Action List

Create a prioritized daily action list from triage results.

```bash
python3 scripts/triage_emails.py \
  --source gmail \
  --max-emails 100 \
  --rules email_rules.yaml \
  --output-format markdown \
  --output daily_actions.md
```

### Step 5: Review and Execute Actions

Review the generated action list and execute recommended actions:
- Respond to urgent emails using suggested response templates
- Delegate identified items to appropriate team members
- Archive or snooze low-priority items
- Update project tracking systems with extracted tasks

## Output Format

### JSON Report

```json
{
  "schema_version": "1.0",
  "generated_at": "2024-01-15T09:30:00Z",
  "total_emails_processed": 100,
  "action_items": [
    {
      "id": "msg_001",
      "subject": "Q1 Budget Review Required",
      "sender": "cfo@company.com",
      "sender_priority": "VIP",
      "received_at": "2024-01-15T08:00:00Z",
      "urgency_score": 95,
      "urgency_level": "CRITICAL",
      "action_type": "RESPOND",
      "deadline_detected": "2024-01-16",
      "project_association": "Q1-Budget",
      "recommended_action": "Review attached budget and provide feedback",
      "suggested_response": "Thank you for sharing. I'll review and respond by EOD tomorrow.",
      "delegation_candidate": null,
      "context_tags": ["budget", "review", "deadline"]
    }
  ],
  "summary": {
    "critical": 3,
    "high": 12,
    "medium": 45,
    "low": 40,
    "delegatable": 8,
    "fyi_only": 25
  },
  "sender_stats": {
    "vip_senders": 5,
    "high_priority_senders": 15,
    "new_senders": 8
  }
}
```

### Markdown Report (Daily Action List)

```markdown
# Daily Email Action List
Generated: 2024-01-15 09:30 AM

## Summary
- **Critical**: 3 items requiring immediate action
- **High Priority**: 12 items for today
- **Delegatable**: 8 items to assign to team

---

## CRITICAL (Act Now)

### 1. Q1 Budget Review Required
- **From**: CFO (VIP)
- **Deadline**: Tomorrow (Jan 16)
- **Action**: Review attached budget and provide feedback
- **Suggested Response**: "Thank you for sharing. I'll review and respond by EOD tomorrow."

---

## HIGH PRIORITY (Today)

### 2. Client Meeting Confirmation
- **From**: sales@partner.com (High)
- **Project**: Client-Acme
- **Action**: Confirm attendance and prepare agenda
- **Delegation**: Consider assigning to PM

---

## DELEGATION CANDIDATES

| Email | Suggested Assignee | Reason |
|-------|-------------------|--------|
| Server maintenance schedule | DevOps Lead | Technical infrastructure |
| New hire onboarding docs | HR Coordinator | Standard process |

---

## FYI ONLY (No Action Required)

- Newsletter: Industry Weekly Digest
- Auto-notification: Build succeeded
- CC'd: Team meeting notes
```

## Resources

- `scripts/triage_emails.py` -- Main triage script with Gmail API integration and local file processing
- `references/email_prioritization_framework.md` -- Business rules and prioritization methodology
- `references/action_type_taxonomy.md` -- Classification of email action types
- `assets/default_rules.yaml` -- Default business rules configuration template

## Key Principles

1. **Action-First Classification** -- Every email is classified by required action, not just importance
2. **Context-Aware Prioritization** -- Combine sender priority, deadline detection, and project context
3. **Delegation Intelligence** -- Identify items that can be delegated based on content and role patterns
4. **Response Templates** -- Provide suggested responses to accelerate action execution
5. **Zero Inbox Philosophy** -- Every email gets a clear disposition: act, delegate, defer, or archive

## Urgency Scoring Algorithm

The urgency score (0-100) is calculated using weighted factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Sender Priority | 30% | VIP=100, High=75, Normal=50, Low=25 |
| Deadline Proximity | 25% | Days until deadline (closer = higher) |
| Keywords | 20% | Urgent, ASAP, deadline, critical, etc. |
| Thread Activity | 15% | Recent replies, waiting on you |
| Age | 10% | Older unanswered = higher urgency |

## Action Type Taxonomy

| Type | Description | Example |
|------|-------------|---------|
| RESPOND | Direct reply required | Answer a question |
| REVIEW | Read and approve/reject | Document review request |
| DELEGATE | Forward to appropriate person | Technical question for team |
| SCHEDULE | Add meeting/event | Meeting invitation |
| TASK | Create external task | Action item from email |
| FYI | Information only | Newsletter, CC'd email |
| ARCHIVE | No action needed | Automated notifications |

## Sender Priority Configuration

Configure sender priorities in `email_rules.yaml`:

```yaml
sender_priority:
  vip:
    - "*@executive.company.com"
    - "ceo@*"
    - "specific.person@partner.com"
  high:
    - "*@client.com"
    - "*@legal.company.com"
  low:
    - "*@newsletter.com"
    - "noreply@*"
```

## Deadline Detection Patterns

The skill detects deadlines using:
- Explicit dates: "by January 15", "due 1/15/2024"
- Relative phrases: "by EOD", "by end of week", "within 24 hours"
- Calendar references: "before our meeting on Monday"
- Urgency markers: "ASAP", "urgent", "time-sensitive"
