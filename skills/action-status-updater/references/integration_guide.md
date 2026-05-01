# Integration Guide: daily-comms-ops Workflow

This guide explains how to integrate the action-status-updater skill with the daily-comms-ops workflow for seamless action item tracking across communication channels.

## Overview

The daily-comms-ops workflow manages daily communication operations including email triage, Slack monitoring, and meeting follow-ups. The action-status-updater skill complements this by providing persistent action item tracking with natural language status updates.

## Integration Points

### 1. Action Item Creation

When daily-comms-ops identifies action items from:
- Email inbox triage
- Slack channel monitoring
- Meeting notes processing

These items can be added to the action-status-updater state:

```yaml
# daily-comms-ops output
action_items:
  - source: email
    from: sean@example.com
    subject: "Q1 Proposal Review"
    action: "Reply with feedback by Friday"
    priority: high

# Converted to action-status-updater format
action_items:
  - id: "act-001"
    channel: "email"
    assignee: "Sean"
    description: "Reply with Q1 proposal feedback"
    status: "pending"
    due_date: "2024-01-12"
    source_ref: "email:sean@example.com:2024-01-08"
```

### 2. Status Update Triggers

Natural language updates can be triggered from:

**Manual Input:**
```bash
python3 scripts/action_status_updater.py update \
  --state-file ./action_state.yaml \
  --input "Seanのproposal返信した"
```

**Batch Processing:**
```bash
# Process status updates from a file (one per line)
python3 scripts/action_status_updater.py batch-update \
  --state-file ./action_state.yaml \
  --input-file ./status_updates.txt
```

**Interactive Mode:**
```bash
python3 scripts/action_status_updater.py interactive \
  --state-file ./action_state.yaml
# > Seanのメール返信済み
# > Luさんの件は来週
# > Mike handled the report
```

### 3. Export Formats

#### daily-comms YAML Format

```yaml
# Export command
python3 scripts/action_status_updater.py export \
  --state-file ./action_state.yaml \
  --format daily-comms \
  --output ./comms_integration.yaml

# Output format
schema_version: "1.0"
export_timestamp: "2024-01-10T14:30:00Z"
pending_actions:
  - channel: email
    assignee: Sean
    description: "Reply with Q1 proposal feedback"
    due: "2024-01-12"
    priority: high

completed_today:
  - channel: email
    assignee: Mike
    description: "Send monthly report"
    completed_at: "2024-01-10T10:15:00Z"

delegated:
  - channel: slack
    original_assignee: self
    delegated_to: Lu
    description: "Review PR #234"
    delegated_at: "2024-01-10T11:00:00Z"
```

#### Slack Reminder Format

```bash
python3 scripts/action_status_updater.py export \
  --state-file ./action_state.yaml \
  --format slack \
  --output ./slack_reminder.md

# Output: Markdown formatted for Slack
*📋 Action Items Update*

*Pending (3)*
• [ ] Reply to Sean's proposal (due: Friday)
• [ ] Review Mike's PR (due: Today)
• [ ] Schedule team meeting (due: Next week)

*Completed Today (2)* ✅
• ~Monthly report sent~
• ~Responded to client inquiry~
```

#### Email Summary Format

```bash
python3 scripts/action_status_updater.py export \
  --state-file ./action_state.yaml \
  --format email \
  --output ./email_summary.html
```

## Workflow Integration Patterns

### Pattern 1: Morning Briefing

```bash
# 1. Load yesterday's state
# 2. Check for overdue items
# 3. Generate morning briefing

python3 scripts/action_status_updater.py report \
  --state-file ./action_state.yaml \
  --filter overdue,due-today \
  --format briefing
```

Output:
```markdown
## Morning Briefing - 2024-01-10

### ⚠️ Overdue (2)
1. **Reply to Sean's proposal** - Due: Jan 8 (2 days overdue)
2. **Submit expense report** - Due: Jan 9 (1 day overdue)

### 📅 Due Today (3)
1. Review Mike's PR
2. Send weekly update
3. Call client re: contract
```

### Pattern 2: End-of-Day Summary

```bash
python3 scripts/action_status_updater.py report \
  --state-file ./action_state.yaml \
  --filter completed-today,delegated-today \
  --format summary
```

### Pattern 3: Weekly Review

```bash
python3 scripts/action_status_updater.py stats \
  --state-file ./action_state.yaml \
  --period week \
  --output ./weekly_stats.json
```

Output:
```json
{
  "period": "2024-W02",
  "metrics": {
    "items_created": 15,
    "items_completed": 12,
    "items_delegated": 2,
    "items_deferred": 1,
    "completion_rate": 0.80,
    "avg_completion_time_hours": 18.5
  },
  "by_channel": {
    "email": {"created": 8, "completed": 7},
    "slack": {"created": 5, "completed": 4},
    "meeting": {"created": 2, "completed": 1}
  }
}
```

## State File Management

### File Location Best Practices

```
~/.claude/
├── action_state.yaml          # Default persistent state
├── action_state_backup/       # Daily backups
│   ├── 2024-01-09.yaml
│   └── 2024-01-10.yaml
└── comms/
    └── daily_export.yaml      # daily-comms-ops integration
```

### Backup and Restore

```bash
# Create backup before major updates
python3 scripts/action_status_updater.py backup \
  --state-file ./action_state.yaml \
  --backup-dir ./backups/

# Restore from backup
python3 scripts/action_status_updater.py restore \
  --backup-file ./backups/2024-01-09.yaml \
  --state-file ./action_state.yaml
```

### State Cleanup

```bash
# Archive completed items older than 30 days
python3 scripts/action_status_updater.py cleanup \
  --state-file ./action_state.yaml \
  --archive-after 30 \
  --archive-file ./archive/completed_2024_01.yaml
```

## Error Handling

### Ambiguous Updates

When a status update cannot be matched to a specific action item:

```
$ python3 scripts/action_status_updater.py update --input "Done"

⚠️ Ambiguous update: "Done"
Multiple pending items found. Please specify:

1. [act-001] Reply to Sean's proposal (email)
2. [act-002] Review Mike's PR (slack)
3. [act-003] Send monthly report (email)

Enter item number or 'skip':
```

### Conflict Resolution

When an item is already in the target state:

```
$ python3 scripts/action_status_updater.py update --input "Seanのメール返信した"

ℹ️ Item already completed: "Reply to Sean's proposal"
   Completed at: 2024-01-10 10:15 UTC

Update anyway? (y/N):
```

## Configuration Options

### Default Config File

`~/.claude/action_updater_config.yaml`:

```yaml
# Default state file location
state_file: ~/.claude/action_state.yaml

# Auto-backup settings
backup:
  enabled: true
  directory: ~/.claude/action_state_backup/
  keep_days: 30

# Matching preferences
matching:
  fuzzy_threshold: 0.7
  prefer_recent: true
  recent_days: 7

# Export defaults
export:
  default_format: daily-comms
  output_directory: ~/.claude/comms/

# Notifications
notifications:
  overdue_warning: true
  daily_summary: true
```

## Troubleshooting

### Common Issues

1. **No matching item found**: Check person name spelling, channel keywords
2. **Multiple matches**: Use more specific description or add channel context
3. **State file corruption**: Restore from backup, validate YAML syntax
4. **Date parsing errors**: Use ISO format (YYYY-MM-DD) for due dates

### Debug Mode

```bash
python3 scripts/action_status_updater.py update \
  --state-file ./action_state.yaml \
  --input "Seanのメール返信した" \
  --debug

# Debug output shows:
# - Detected language: Japanese
# - Parsed intent: completed
# - Extracted person: Sean
# - Extracted channel: email
# - Matched items: [act-001 (confidence: 0.95)]
```
