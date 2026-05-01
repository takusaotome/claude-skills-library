---
layout: default
title: "Timezone Aware Event Tracker"
grand_parent: English
parent: Meta & Quality
nav_order: 22
lang_peer: /ja/skills/meta/timezone-aware-event-tracker/
permalink: /en/skills/meta/timezone-aware-event-tracker/
---

# Timezone Aware Event Tracker
{: .no_toc }

Track and correlate events across multiple timezones with automatic conversion. Use when analyzing distributed system incidents, coordinating cross-regional operations, or creating time-normalized reports from logs/events spanning PST/CST/EST/JST or other timezones. Handles daylight saving transitions automatically.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/timezone-aware-event-tracker.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/timezone-aware-event-tracker){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill tracks, converts, and correlates events occurring across multiple timezones with automatic timezone detection and conversion. It maintains awareness of regional time differences (PST/CST/EST/JST and others), handles daylight saving time (DST) transitions, and generates time-normalized reports. Essential for distributed team incident analysis, cross-regional operations coordination, and multi-timezone log correlation.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: `pytz` (or use standard library `zoneinfo` on Python 3.9+)

---

## 3. Quick Start

```bash
python3 scripts/timezone_event_tracker.py parse \
  --input events.csv \
  --output normalized_events.json \
  --reference-tz UTC
```

---

## 4. How It Works

### Step 1: Collect Event Data

Gather event data with timestamps. Events can be provided in multiple formats:
- CSV files with timestamp columns
- JSON event logs
- Plain text logs with parseable timestamps
- Manual event lists

Each event should include:
- Timestamp (in any parseable format)
- Source timezone (or auto-detect from timestamp suffix)
- Event description
- Optional: severity, source system, correlation ID

### Step 2: Parse and Normalize Events

Run the event parser to convert all timestamps to a common reference timezone (default: UTC).

```bash
python3 scripts/timezone_event_tracker.py parse \
  --input events.csv \
  --output normalized_events.json \
  --reference-tz UTC
```

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Analyzing incidents or logs from distributed systems spanning multiple timezones
- Correlating events from teams in different regions (e.g., US West, US East, Japan)
- Creating unified timelines from events recorded in different local times
- Scheduling or reviewing cross-regional meetings and handoffs
- Generating time-normalized reports for global operations
- Investigating issues where timestamp confusion led to coordination failures

---

## 6. Understanding the Output

### JSON Normalized Events

```json
{
  "schema_version": "1.0",
  "reference_timezone": "UTC",
  "generated_at": "2024-03-15T10:30:00Z",
  "events": [
    {
      "id": "evt-001",
      "original_timestamp": "2024-03-15 02:30:00 PST",
      "normalized_timestamp": "2024-03-15T10:30:00Z",
      "source_timezone": "America/Los_Angeles",
      "description": "Server restart initiated",
      "metadata": {
        "severity": "info",
        "source_system": "ops-west"
      },

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/timezone-aware-event-tracker/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: timezone-conversion-guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: timezone_event_tracker.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/timezone-aware-event-tracker/references/timezone-conversion-guide.md`

**Scripts:**

- `skills/timezone-aware-event-tracker/scripts/timezone_event_tracker.py`
