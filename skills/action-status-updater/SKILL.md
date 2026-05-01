---
name: action-status-updater
description: Track and update action item status from natural language updates like 'Seanのメールには返信しておいた' or 'Lu対応予定'. Integrates with daily-comms-ops workflow. Use when managing action items across communication channels.
---

# Action Status Updater

## Overview

Track and update action item status across multiple communication channels using natural language updates. Accept status updates in Japanese or English (e.g., 'Seanのメールには返信しておいた', 'Delegated to Mike'), parse intent and target, and maintain persistent action tracking state. Integrates with daily-comms-ops workflow to reduce manual status tracking overhead.

## When to Use

- Updating action item status via natural language input
- Marking items as completed, delegated, deferred, or in-progress
- Tracking action items across email, Slack, meetings, and other channels
- Generating action item status reports
- Integrating status updates into daily-comms-ops workflow
- Bulk status updates from meeting notes or status check-ins

## Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: `pyyaml` (for state persistence)

## Workflow

### Step 1: Initialize or Load Action State

Load existing action items from the persistent state file, or initialize a new state if none exists.

```bash
python3 scripts/action_status_updater.py init \
  --state-file ./action_state.yaml
```

### Step 2: Add New Action Items

Add action items from various sources (email, Slack, meetings). Each item includes source channel, assignee, due date, and description.

```bash
python3 scripts/action_status_updater.py add \
  --state-file ./action_state.yaml \
  --channel email \
  --assignee "Sean" \
  --description "Reply to proposal inquiry" \
  --due "2024-01-15"
```

### Step 3: Update Status via Natural Language

Parse natural language status updates and apply them to matching action items. Supports Japanese and English input.

```bash
python3 scripts/action_status_updater.py update \
  --state-file ./action_state.yaml \
  --input "Seanのメールには返信しておいた"
```

Supported update patterns:
- **Completed**: "返信した", "完了", "done", "finished", "sent"
- **Delegated**: "〜に依頼", "delegated to", "assigned to"
- **Deferred**: "延期", "later", "postponed", "来週"
- **In-Progress**: "対応中", "working on", "進行中"

### Step 4: Generate Status Report

Generate a summary report of all action items with their current status.

```bash
python3 scripts/action_status_updater.py report \
  --state-file ./action_state.yaml \
  --format markdown \
  --output ./action_report.md
```

### Step 5: Integrate with daily-comms-ops

Export action items in a format compatible with daily-comms-ops workflow for seamless integration.

```bash
python3 scripts/action_status_updater.py export \
  --state-file ./action_state.yaml \
  --format daily-comms \
  --output ./comms_integration.yaml
```

## Output Format

### YAML State File

```yaml
schema_version: "1.0"
last_updated: "2024-01-10T14:30:00Z"
action_items:
  - id: "act-001"
    channel: "email"
    assignee: "Sean"
    description: "Reply to proposal inquiry"
    status: "completed"
    created_at: "2024-01-08T09:00:00Z"
    updated_at: "2024-01-10T14:30:00Z"
    due_date: "2024-01-15"
    history:
      - timestamp: "2024-01-10T14:30:00Z"
        from_status: "pending"
        to_status: "completed"
        trigger: "Seanのメールには返信しておいた"
```

### Markdown Report

```markdown
# Action Status Report
Generated: 2024-01-10 14:30 UTC

## Summary
- Total: 15
- Completed: 8
- In Progress: 4
- Pending: 2
- Delegated: 1

## By Channel

### Email (5 items)
| Assignee | Description | Status | Due |
|----------|-------------|--------|-----|
| Sean | Reply to proposal | ✅ Completed | 2024-01-15 |

### Slack (3 items)
...
```

### JSON Report

```json
{
  "schema_version": "1.0",
  "generated_at": "2024-01-10T14:30:00Z",
  "summary": {
    "total": 15,
    "completed": 8,
    "in_progress": 4,
    "pending": 2,
    "delegated": 1
  },
  "items": [...]
}
```

## Natural Language Parsing

The skill uses pattern matching to extract intent and target from natural language updates:

### Intent Detection

| Intent | Japanese Patterns | English Patterns |
|--------|------------------|------------------|
| Completed | 返信した, 完了, 済み, 終わった | done, finished, completed, sent, replied |
| Delegated | 〜に依頼, 〜にお願い, 〜に任せた | delegated to, assigned to, handed off to |
| Deferred | 延期, 来週, 後で, 保留 | postponed, deferred, later, next week |
| In-Progress | 対応中, 進行中, やってる | working on, in progress, handling |

### Target Extraction

- Person names: "Sean", "Luさん", "田中さん"
- Channel keywords: "メール", "Slack", "email", "meeting"
- Partial description matching

## Resources

- `scripts/action_status_updater.py` -- Main CLI tool for action item management
- `scripts/nl_parser.py` -- Natural language parsing module for Japanese/English
- `references/status_patterns.md` -- Comprehensive patterns for intent detection
- `references/integration_guide.md` -- Guide for daily-comms-ops integration

## Key Principles

1. **Minimal Friction**: Accept natural language updates without rigid syntax
2. **Bilingual Support**: First-class support for Japanese and English patterns
3. **Persistent State**: All updates are tracked with full history
4. **Integration Ready**: Export formats compatible with daily-comms-ops workflow
5. **Fuzzy Matching**: Tolerant matching for person names and descriptions
