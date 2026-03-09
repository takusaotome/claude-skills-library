# Log Correlation Methodology

## Overview

Log correlation is the process of linking related events across multiple log sources to build a comprehensive understanding of system behavior. This document describes the methodologies and techniques used by the multi-file-log-correlator skill.

## Correlation Techniques

### 1. Correlation ID Matching

The most reliable correlation method when correlation IDs are present in logs.

**Common Correlation ID Fields:**
- `request_id` / `req_id`
- `trace_id` / `span_id` (OpenTelemetry/Jaeger)
- `correlation_id` / `x-correlation-id`
- `transaction_id` / `txn_id`
- `session_id`

**Example:**
```
# nginx.log
[2025-01-15 10:00:01] request_id=abc123 GET /api/users 200

# app.log
[2025-01-15 10:00:01.100] [INFO] [request_id=abc123] Processing user request

# database.log
[2025-01-15T10:00:01.150Z] [req:abc123] SELECT * FROM users WHERE id = 42
```

**Implementation:**
1. Extract correlation IDs from each log entry using regex patterns
2. Build an index: correlation_id → list of events
3. Merge events with matching IDs into correlation groups

### 2. Temporal Proximity Correlation

When explicit correlation IDs are absent, use time-based correlation.

**Time Window Strategy:**
- Define a maximum time window (e.g., 5 seconds)
- Events within the window may be causally related
- Shorter windows = higher precision, lower recall
- Longer windows = higher recall, lower precision

**Considerations:**
- Account for clock skew between systems (typically ±1 second)
- Consider network latency for distributed systems
- Order of events within the window provides causality hints

**Example Configuration:**
```yaml
correlation:
  time_window: 5s
  clock_skew_tolerance: 1s
  require_sequence: false  # If true, enforce expected event order
```

### 3. Semantic Correlation

Match events based on content similarity or shared attributes.

**Attributes to Match:**
- User ID / Account ID
- IP Address
- Resource identifier (file path, database table, API endpoint)
- Error codes or exception types
- Session tokens

**Example:**
```
# Match events affecting the same user
[nginx] user_id=12345 POST /api/orders
[app] userId: 12345 - Order created: ORD-789
[email] Sending confirmation to user 12345
```

### 4. Causal Chain Inference

Infer relationships based on expected system architecture.

**Example Flow:**
```
nginx → app-server → cache → database
         ↓
       message-queue → worker
```

**Implementation:**
1. Define expected call patterns
2. Match events that follow the pattern
3. Flag deviations as anomalies

## Timeline Construction

### Timestamp Normalization

**Step 1: Parse Timestamps**
- Support multiple formats (ISO 8601, syslog, Apache, custom)
- Handle millisecond/microsecond precision
- Extract timezone information

**Step 2: Convert to Common Timezone**
- Convert all timestamps to a reference timezone (typically UTC)
- Preserve original timestamp for reporting

**Step 3: Handle Ambiguous Timestamps**
- Timestamps without timezone: assume source's default timezone
- Timestamps without year: infer from context
- Malformed timestamps: log warning, attempt best-effort parsing

### Merge Algorithm

```python
def merge_timelines(sources: List[LogSource]) -> Timeline:
    """Merge multiple log sources into a unified timeline."""
    all_events = []
    for source in sources:
        for event in source.events:
            event.source = source.name
            event.normalized_ts = normalize_timestamp(
                event.timestamp,
                source.timezone,
                target_tz='UTC'
            )
            all_events.append(event)

    # Sort by normalized timestamp, then by source order for ties
    all_events.sort(key=lambda e: (e.normalized_ts, source_priority[e.source]))

    return Timeline(events=all_events)
```

## Gap Detection

### Definition

A gap is a period where expected log events are missing from a source.

### Detection Methods

**1. Fixed Interval Gaps**
- Compare actual intervals between events to expected intervals
- Flag intervals exceeding threshold (e.g., > 60 seconds)

**2. Cross-Source Gaps**
- If Source A has events but Source B has none during a period
- May indicate connectivity issues or system failures

**3. Pattern-Based Gaps**
- Expected periodic events (heartbeats, health checks) missing
- Scheduled jobs that didn't run

### Gap Classification

| Gap Type | Description | Typical Cause |
|----------|-------------|---------------|
| Silent Gap | No events from any source | System-wide outage |
| Partial Gap | Missing from some sources | Service-specific failure |
| Delayed Gap | Events arrive after expected time | Processing backlog |
| Truncated Gap | Gap at start/end of log file | Log rotation, file truncation |

## Anomaly Detection

### Timing Anomalies

**Unexpected Latency:**
```
Normal: nginx → app (5ms) → db (20ms)
Anomaly: nginx → app (5ms) → db (2000ms)  # 100x expected latency
```

**Out-of-Order Events:**
```
Expected: request → process → response
Observed: response → request  # Causality violation
```

### Volume Anomalies

**Sudden Drop:**
```
Normal rate: 100 events/minute
Anomaly: 5 events/minute  # 95% drop
```

**Sudden Spike:**
```
Normal rate: 100 events/minute
Anomaly: 5000 events/minute  # 50x increase
```

### Content Anomalies

- Error rate exceeding threshold
- New error types appearing
- Unusual request patterns

## Best Practices

### 1. Timezone Handling

- Always store timezone information with log sources
- Default to UTC when timezone is unknown
- Document assumptions in reports

### 2. Clock Synchronization

- Ensure NTP is configured on all systems
- Account for clock drift in correlation windows
- Consider using correlation IDs to overcome clock issues

### 3. Performance Considerations

- For large log files, use streaming/chunked processing
- Build indexes for correlation IDs before correlation
- Limit time ranges to reduce memory usage

### 4. Validation

- Cross-check correlation results with known request flows
- Verify gap detection against system metrics
- Validate anomaly thresholds against historical baselines

## Reporting

### Essential Report Sections

1. **Source Summary**: Files, timezones, event counts
2. **Timeline Overview**: Start/end times, total duration
3. **Correlation Statistics**: Match rate, orphan events
4. **Gap Analysis**: Coverage percentage, gap durations
5. **Anomaly Summary**: Types, severity, affected events

### Visualization

- Mermaid sequence diagrams for request flows
- Timeline charts for gap visualization
- Heatmaps for event density across sources
