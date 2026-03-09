---
name: multi-file-log-correlator
description: |
  Correlate events across multiple log files from different sources, systems, or time periods.
  Build unified timelines, identify causal relationships between events, and highlight anomalies
  that span multiple data sources. Supports timezone normalization and gap detection.

  Use when analyzing logs from multiple systems (frontend, backend, database, infrastructure),
  investigating distributed system failures, or building event timelines across services.

  Triggers: "correlate these logs", "build timeline from multiple logs", "cross-system analysis",
  "find related events across logs", "multi-source log analysis", "distributed trace analysis"
---

# Multi-File Log Correlator

## Overview

This skill correlates events across multiple log files from different sources, systems, or time periods. It builds unified timelines, identifies causal relationships between events, and highlights anomalies that span multiple data sources. The skill handles timezone normalization, timestamp format differences, and gap detection to provide a comprehensive view of distributed system behavior.

**Key Capabilities:**
- Unified timeline construction from heterogeneous log sources
- Causal relationship inference between events across systems
- Timezone normalization and timestamp alignment
- Gap and anomaly detection across multiple data sources
- Correlation ID tracking and distributed trace reconstruction

## When to Use

- Investigating incidents involving multiple services (frontend, API, database, cache)
- Analyzing distributed system failures across microservices
- Building event timelines from logs with different timestamp formats
- Correlating infrastructure logs with application logs
- Detecting timing anomalies between system components
- Tracing request flows across multiple services
- Post-mortem analysis requiring multi-source log correlation

## Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: pandas, python-dateutil (for timezone handling)

## Workflow

### Step 1: Inventory Log Files

Identify all log files to correlate. Document their source system, timezone, and timestamp format.

```bash
# List available log files
ls -la /path/to/logs/

# Check first few lines to identify format
head -5 app.log nginx.log database.log
```

### Step 2: Parse and Normalize Timestamps

Run the correlator with timezone and format configuration.

```bash
python3 scripts/correlate_logs.py \
  --logs app.log:app:UTC:"%Y-%m-%d %H:%M:%S" \
  --logs nginx.log:nginx:America/New_York:"%d/%b/%Y:%H:%M:%S %z" \
  --logs database.log:db:UTC:"%Y-%m-%dT%H:%M:%S.%fZ" \
  --output-tz UTC \
  --output timeline.json
```

### Step 3: Build Unified Timeline

The script generates a merged, time-ordered event sequence with source attribution.

```bash
# View timeline summary
python3 scripts/correlate_logs.py \
  --logs app.log:app \
  --logs nginx.log:nginx \
  --summary
```

### Step 4: Detect Correlations

Identify events that are causally related using correlation IDs, request IDs, or temporal proximity.

```bash
python3 scripts/correlate_logs.py \
  --logs app.log:app \
  --logs nginx.log:nginx \
  --correlation-field request_id \
  --time-window 5s \
  --output correlations.json
```

### Step 5: Identify Gaps and Anomalies

Detect missing data periods and timing anomalies across sources.

```bash
python3 scripts/correlate_logs.py \
  --logs app.log:app \
  --logs nginx.log:nginx \
  --detect-gaps \
  --gap-threshold 60s \
  --output gaps_report.json
```

### Step 6: Generate Correlation Report

Produce a comprehensive Markdown report with timeline visualization.

```bash
python3 scripts/correlate_logs.py \
  --logs app.log:app:UTC \
  --logs nginx.log:nginx:America/New_York \
  --logs database.log:db:UTC \
  --full-report \
  --output correlation_report.md
```

## Output Format

### JSON Timeline

```json
{
  "schema_version": "1.0",
  "generated_at": "2025-01-15T10:30:00Z",
  "output_timezone": "UTC",
  "sources": [
    {
      "name": "app",
      "file": "app.log",
      "original_tz": "UTC",
      "events_count": 1523,
      "time_range": {
        "start": "2025-01-15T08:00:00Z",
        "end": "2025-01-15T10:00:00Z"
      }
    }
  ],
  "timeline": [
    {
      "timestamp": "2025-01-15T08:00:01.234Z",
      "source": "nginx",
      "level": "INFO",
      "message": "GET /api/users 200",
      "correlation_ids": ["req-abc123"]
    }
  ],
  "correlations": [
    {
      "correlation_id": "req-abc123",
      "events": [
        {"source": "nginx", "timestamp": "...", "message": "..."},
        {"source": "app", "timestamp": "...", "message": "..."},
        {"source": "db", "timestamp": "...", "message": "..."}
      ],
      "total_duration_ms": 245
    }
  ],
  "gaps": [
    {
      "source": "app",
      "gap_start": "2025-01-15T09:15:00Z",
      "gap_end": "2025-01-15T09:17:30Z",
      "duration_seconds": 150
    }
  ],
  "anomalies": [
    {
      "type": "timing_anomaly",
      "description": "Database response 500ms after app request (expected <100ms)",
      "events": ["..."]
    }
  ]
}
```

### Markdown Report

The Markdown report includes:
- **Executive Summary**: Key findings and correlation statistics
- **Source Inventory**: List of log files with metadata
- **Unified Timeline**: Time-ordered event listing with source attribution
- **Correlation Analysis**: Grouped events by correlation ID
- **Gap Analysis**: Missing data periods and coverage statistics
- **Anomaly Findings**: Timing issues, sequence violations, unexpected patterns
- **Mermaid Sequence Diagram**: Visual representation of cross-system flows

## Resources

- `scripts/correlate_logs.py` -- Main correlation engine with CLI interface
- `references/correlation_methodology.md` -- Correlation techniques and best practices
- `references/timestamp_formats.md` -- Common log timestamp formats reference

## Key Principles

1. **Normalize Early**: Convert all timestamps to a common timezone immediately
2. **Preserve Source Attribution**: Every event must retain its origin system
3. **Handle Imperfect Data**: Gracefully process logs with missing or malformed timestamps
4. **Detect Gaps Explicitly**: Missing data is as important as present data
5. **Enable Filtering**: Support time ranges, severity levels, and correlation ID filtering

## Differences from log-debugger

| Aspect | log-debugger | multi-file-log-correlator |
|--------|--------------|---------------------------|
| Focus | Single-file RCA, error analysis | Multi-file correlation, timeline building |
| Primary Output | Root cause report | Unified timeline, correlation map |
| Key Feature | 5 Whys, Fishbone analysis | Cross-source correlation, gap detection |
| Use Case | "Why did this error happen?" | "How did events flow across systems?" |
