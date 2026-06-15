---
name: vendor-support-ticket-tracker
description: Track vendor support tickets and RMA cases across multiple vendors. Use when managing support ticket lifecycle, updating ticket status from vendor emails, generating status reports, or identifying tickets needing follow-up.
---

# Vendor Support Ticket Tracker

## Overview

Track and manage vendor support tickets and RMA cases across multiple vendors (STX, Dell, HP, etc.). Maintains ticket state, communication timeline, pending actions, and escalation status. Integrates with email to auto-update ticket status from vendor responses and generates status reports identifying tickets requiring follow-up.

## When to Use

- Creating a new vendor support ticket or RMA case
- Updating ticket status from vendor email responses
- Generating status reports for open tickets
- Identifying stale tickets requiring follow-up
- Reviewing escalation history for a specific ticket
- Tracking SLA compliance across vendors

## Prerequisites

- Python 3.9+
- No API keys required (local YAML-based storage)
- Optional: `gogcli-expert` skill for Gmail integration
- PyYAML package for ticket state persistence

## Workflow

### Step 1: Initialize Ticket Database

Check for existing ticket database or create a new one.

```bash
python3 scripts/ticket_manager.py init \
  --db-path ./tickets.yaml
```

### Step 2: Create New Ticket

Register a new vendor support ticket or RMA case.

```bash
python3 scripts/ticket_manager.py create \
  --vendor "STX" \
  --ticket-id "SR-2025-001234" \
  --subject "HDD failure - server rack 12" \
  --priority "high" \
  --category "RMA" \
  --contact "support@stx.com" \
  --db-path ./tickets.yaml
```

### Step 3: Update Ticket Status from Email

Parse vendor email response and update ticket timeline. Run this after receiving vendor correspondence.

```bash
python3 scripts/ticket_manager.py update \
  --ticket-id "SR-2025-001234" \
  --status "awaiting-parts" \
  --notes "Vendor confirmed RMA approved. Parts shipping 2025-06-18." \
  --db-path ./tickets.yaml
```

### Step 4: Generate Status Report

Generate a markdown status report for all open tickets or filtered by vendor/priority.

```bash
python3 scripts/ticket_manager.py report \
  --output ./vendor-ticket-report.md \
  --filter-status "open,awaiting-parts,escalated" \
  --db-path ./tickets.yaml
```

### Step 5: Identify Stale Tickets

Find tickets with no activity beyond a threshold (default: 7 days).

```bash
python3 scripts/ticket_manager.py stale \
  --days 7 \
  --db-path ./tickets.yaml
```

### Step 6: Escalate Ticket

Mark a ticket for escalation and add escalation notes.

```bash
python3 scripts/ticket_manager.py escalate \
  --ticket-id "SR-2025-001234" \
  --reason "No response for 10 days despite P1 priority" \
  --db-path ./tickets.yaml
```

## Ticket States

| State | Description |
|-------|-------------|
| `open` | Newly created, awaiting vendor acknowledgment |
| `acknowledged` | Vendor has confirmed receipt |
| `in-progress` | Vendor actively working on issue |
| `awaiting-parts` | RMA: waiting for replacement parts shipment |
| `awaiting-customer` | Vendor waiting for customer response/action |
| `escalated` | Issue escalated to higher support tier |
| `resolved` | Issue resolved, pending confirmation |
| `closed` | Ticket closed after resolution confirmed |

## Output Format

### Ticket Database (YAML)

```yaml
schema_version: "1.0"
tickets:
  SR-2025-001234:
    vendor: "STX"
    ticket_id: "SR-2025-001234"
    subject: "HDD failure - server rack 12"
    category: "RMA"
    priority: "high"
    status: "awaiting-parts"
    contact: "support@stx.com"
    created_at: "2025-06-10T09:30:00Z"
    updated_at: "2025-06-15T14:20:00Z"
    sla_target: "2025-06-17T09:30:00Z"
    escalated: false
    timeline:
      - timestamp: "2025-06-10T09:30:00Z"
        action: "created"
        notes: "Submitted RMA request for failed HDD"
      - timestamp: "2025-06-11T10:15:00Z"
        action: "status_change"
        from_status: "open"
        to_status: "acknowledged"
        notes: "Vendor acknowledged ticket"
      - timestamp: "2025-06-15T14:20:00Z"
        action: "status_change"
        from_status: "acknowledged"
        to_status: "awaiting-parts"
        notes: "RMA approved. Parts shipping 2025-06-18."
```

### Status Report (Markdown)

```markdown
# Vendor Support Ticket Status Report
Generated: 2025-06-15T15:00:00Z

## Summary
- Total Open: 5
- High Priority: 2
- Escalated: 1
- Stale (>7 days): 1

## Open Tickets by Vendor

### STX (2 tickets)

| Ticket ID | Subject | Priority | Status | Age | Last Update |
|-----------|---------|----------|--------|-----|-------------|
| SR-2025-001234 | HDD failure - rack 12 | high | awaiting-parts | 5d | 2025-06-15 |
| SR-2025-001180 | Memory error alerts | medium | in-progress | 8d | 2025-06-14 |

### Dell (1 ticket)

| Ticket ID | Subject | Priority | Status | Age | Last Update |
|-----------|---------|----------|--------|-----|-------------|
| DELL-9876543 | RAID controller failure | high | escalated | 12d | 2025-06-13 |

## Tickets Requiring Follow-Up

1. **SR-2025-001180** (STX) - Stale for 8 days, last status: in-progress
2. **DELL-9876543** (Dell) - Escalated, no response for 2 days
```

## Email Integration

### Auto-Update from Email Thread

Use with `gogcli-expert` skill to fetch vendor emails and auto-update tickets:

1. Search Gmail for vendor support threads
2. Parse latest response for status indicators
3. Update ticket timeline automatically

Common status indicators in vendor emails:
- "RMA approved" → `awaiting-parts`
- "Parts shipped" → `awaiting-parts` with tracking info
- "Issue resolved" → `resolved`
- "Waiting for your response" → `awaiting-customer`
- "Escalated to Tier 2" → `escalated`

## Resources

- `scripts/ticket_manager.py` -- CLI tool for ticket CRUD operations and reporting
- `references/ticket-lifecycle.md` -- Vendor ticket states, SLA guidelines, escalation procedures

## Key Principles

1. Every vendor communication must be logged in the ticket timeline
2. Stale ticket detection runs on configurable thresholds (default 7 days)
3. Escalation requires documented reason and triggers notification
4. Status reports are generated in Markdown for easy sharing
5. YAML storage enables version control and diff tracking of ticket changes
