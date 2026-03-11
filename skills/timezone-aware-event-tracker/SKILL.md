---
name: timezone-aware-event-tracker
description: Track and correlate events across multiple timezones with automatic conversion. Use when analyzing distributed system incidents, coordinating cross-regional operations, or creating time-normalized reports from logs/events spanning PST/CST/EST/JST or other timezones. Handles daylight saving transitions automatically.
---

# Timezone-Aware Event Tracker

## Overview

This skill tracks, converts, and correlates events occurring across multiple timezones with automatic timezone detection and conversion. It maintains awareness of regional time differences (PST/CST/EST/JST and others), handles daylight saving time (DST) transitions, and generates time-normalized reports. Essential for distributed team incident analysis, cross-regional operations coordination, and multi-timezone log correlation.

## When to Use

- Analyzing incidents or logs from distributed systems spanning multiple timezones
- Correlating events from teams in different regions (e.g., US West, US East, Japan)
- Creating unified timelines from events recorded in different local times
- Scheduling or reviewing cross-regional meetings and handoffs
- Generating time-normalized reports for global operations
- Investigating issues where timestamp confusion led to coordination failures

## Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: `pytz` (or use standard library `zoneinfo` on Python 3.9+)

## Workflow

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

The parser will:
- Detect timestamp formats automatically
- Identify source timezones from suffixes (PST, EST, JST) or offset notation
- Convert all times to the reference timezone
- Flag ambiguous timestamps (e.g., during DST transitions)

### Step 3: Correlate Events Across Timezones

Identify related events that occurred within specified time windows.

```bash
python3 scripts/timezone_event_tracker.py correlate \
  --input normalized_events.json \
  --window-minutes 5 \
  --output correlated_events.json
```

Correlation identifies:
- Events occurring within the same time window
- Causal chains based on timestamps
- Gaps in event sequences
- Timezone-related patterns (e.g., events clustering around shift changes)

### Step 4: Generate Timeline Report

Create a unified timeline report showing all events in multiple timezone views.

```bash
python3 scripts/timezone_event_tracker.py report \
  --input correlated_events.json \
  --timezones "America/Los_Angeles,America/New_York,Asia/Tokyo" \
  --format markdown \
  --output timeline_report.md
```

### Step 5: Analyze DST Transitions

Check if any events occurred during daylight saving transitions that may have caused confusion.

```bash
python3 scripts/timezone_event_tracker.py dst-check \
  --input normalized_events.json \
  --year 2024 \
  --output dst_analysis.json
```

## Output Format

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
      "dst_status": "standard_time"
    }
  ],
  "correlation_groups": [
    {
      "group_id": "corr-001",
      "event_ids": ["evt-001", "evt-002"],
      "time_span_seconds": 120,
      "pattern": "cascading_failure"
    }
  ]
}
```

### Markdown Timeline Report

```markdown
# Event Timeline Report

Generated: 2024-03-15T10:30:00Z

## Summary
- Total events: 15
- Time span: 2024-03-15 00:00 UTC to 2024-03-15 23:59 UTC
- Correlation groups: 3
- DST warnings: 0

## Timeline (Multi-Timezone View)

| UTC | PST (LA) | EST (NY) | JST (Tokyo) | Event | Source |
|-----|----------|----------|-------------|-------|--------|
| 10:30 | 02:30 | 05:30 | 19:30 | Server restart | ops-west |
| 10:32 | 02:32 | 05:32 | 19:32 | Alert triggered | monitoring |

## Correlation Analysis

### Group 1: Cascading Failure (2 events, 120s span)
- 10:30 UTC: Server restart initiated (ops-west)
- 10:32 UTC: Alert triggered (monitoring)

## DST Considerations

No events occurred during DST transition periods.
```

## Resources

- `scripts/timezone_event_tracker.py` -- Main CLI tool for parsing, correlating, and reporting
- `references/timezone-conversion-guide.md` -- Reference for timezone abbreviations, DST rules, and conversion best practices

## Key Principles

1. **Always normalize to UTC first** -- Use UTC as the internal reference to avoid confusion during DST transitions
2. **Preserve original timestamps** -- Keep source timestamps for audit trail and debugging
3. **Flag ambiguity explicitly** -- DST transitions create ambiguous local times; flag them rather than guess
4. **Support IANA timezone names** -- Use `America/Los_Angeles` not `PST` for unambiguous timezone handling
5. **Consider business hours** -- When correlating events, account for regional business hour patterns
