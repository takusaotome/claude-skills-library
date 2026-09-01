---
layout: default
title: "Vendor Support Ticket Tracker"
grand_parent: English
parent: Meta & Quality
nav_order: 32
lang_peer: /ja/skills/meta/vendor-support-ticket-tracker/
permalink: /en/skills/meta/vendor-support-ticket-tracker/
---

# Vendor Support Ticket Tracker
{: .no_toc }

Track vendor support tickets and RMA cases across multiple vendors. Use when managing support ticket lifecycle, updating ticket status from vendor emails, generating status reports, or identifying tickets needing follow-up.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-support-ticket-tracker.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/vendor-support-ticket-tracker){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Track and manage vendor support tickets and RMA cases across multiple vendors (STX, Dell, HP, etc.). Maintains ticket state, communication timeline, pending actions, and escalation status. Integrates with email to auto-update ticket status from vendor responses and generates status reports identifying tickets requiring follow-up.

---

## 2. When to Use

- Creating a new vendor support ticket or RMA case
- Updating ticket status from vendor email responses
- Generating status reports for open tickets
- Identifying stale tickets requiring follow-up
- Reviewing escalation history for a specific ticket
- Tracking SLA compliance across vendors

---

## 3. Prerequisites

- Python 3.9+
- No API keys required (local YAML-based storage)
- Optional: `gogcli-expert` skill for Gmail integration
- PyYAML package for ticket state persistence

---

## 4. Quick Start

```bash
python3 scripts/ticket_manager.py init \
  --db-path ./tickets.yaml
```

---

## 5. Workflow

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

---

## 6. Resources

**References:**

- `skills/vendor-support-ticket-tracker/references/ticket-lifecycle.md`

**Scripts:**

- `skills/vendor-support-ticket-tracker/scripts/ticket_manager.py`
