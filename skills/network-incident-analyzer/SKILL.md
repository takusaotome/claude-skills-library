---
name: network-incident-analyzer
description: Analyze network device logs to identify connectivity issues, latency problems, and outages. Correlate timestamps across timezones, detect anomaly patterns, and generate incident reports with root cause hypotheses. Use when troubleshooting network incidents from log files.
---

# Network Incident Analyzer

## Overview

Analyzes network device logs (routers, switches, firewalls, load balancers) to identify connectivity issues, latency problems, and service outages. Automatically correlates events across multiple log files with different timestamp formats and timezones, detects anomaly patterns within specified time windows, and generates comprehensive incident reports with root cause hypotheses and remediation recommendations.

## When to Use

- Troubleshooting network connectivity issues using device logs
- Analyzing multiple log files from different network devices to find correlated events
- Investigating service outages with logs spanning multiple timezones
- Identifying patterns in network latency or packet loss from log data
- Generating incident reports with root cause analysis from raw logs
- Correlating timestamps across devices with different time formats

## Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (datetime, re, json, collections, pathlib)

## Workflow

### Step 1: Collect Log Files

Gather all relevant network device logs for the incident time window. Supported formats include:
- Cisco IOS/NX-OS logs
- Juniper JunOS logs
- Palo Alto firewall logs
- F5 load balancer logs
- Generic syslog format
- JSON-structured logs

Place log files in a working directory or provide paths directly.

### Step 2: Analyze Logs with Time Window

Run the analysis script specifying the incident time window and log files.

```bash
python3 scripts/analyze_network_logs.py \
  --logs /path/to/router.log /path/to/firewall.log \
  --start "2024-01-15 10:00:00" \
  --end "2024-01-15 12:00:00" \
  --timezone "America/New_York" \
  --output-dir ./incident-report
```

The script will:
1. Parse each log file and detect its timestamp format
2. Normalize all timestamps to UTC for correlation
3. Identify anomaly patterns (high error rates, connection failures, latency spikes)
4. Correlate events across devices within configurable time windows
5. Generate incident timeline and root cause hypotheses

### Step 3: Review Correlated Events

Examine the `correlated_events.json` output showing event clusters:

```bash
cat ./incident-report/correlated_events.json | python3 -m json.tool
```

Each cluster groups related events from different devices occurring within the correlation window.

### Step 4: Analyze Root Cause Hypotheses

Review the `root_cause_analysis.md` report containing:
- Incident timeline with key events
- Detected anomaly patterns
- Root cause hypotheses ranked by confidence
- Recommended remediation steps

### Step 5: Generate Executive Summary

For stakeholder communication, use the generated `incident_summary.md`:
- Impact assessment (duration, affected services)
- Timeline of key events
- Root cause determination
- Prevention recommendations

## Output Format

### JSON Report (correlated_events.json)

```json
{
  "schema_version": "1.0",
  "analysis_timestamp": "2024-01-15T14:30:00Z",
  "incident_window": {
    "start": "2024-01-15T15:00:00Z",
    "end": "2024-01-15T17:00:00Z"
  },
  "log_files_analyzed": [
    {"path": "router.log", "events": 1523, "format": "cisco_ios"},
    {"path": "firewall.log", "events": 842, "format": "palo_alto"}
  ],
  "anomalies_detected": [
    {
      "type": "connection_failure_spike",
      "start_time": "2024-01-15T15:23:45Z",
      "end_time": "2024-01-15T15:45:12Z",
      "severity": "critical",
      "affected_devices": ["core-router-01", "fw-edge-01"],
      "event_count": 234
    }
  ],
  "correlated_events": [
    {
      "cluster_id": "CLU-001",
      "correlation_confidence": 0.92,
      "events": [
        {"timestamp": "2024-01-15T15:23:45Z", "device": "core-router-01", "message": "BGP peer down"},
        {"timestamp": "2024-01-15T15:23:47Z", "device": "fw-edge-01", "message": "Connection timeout"}
      ]
    }
  ],
  "root_cause_hypotheses": [
    {
      "hypothesis": "BGP session failure caused cascading connectivity loss",
      "confidence": 0.85,
      "supporting_evidence": ["BGP peer down event preceded all connection failures"],
      "recommended_actions": ["Check BGP neighbor configuration", "Verify upstream provider status"]
    }
  ]
}
```

### Markdown Report (root_cause_analysis.md)

The report includes:
- Executive summary
- Incident timeline (chronological event listing)
- Anomaly pattern analysis
- Root cause hypotheses with confidence scores
- Device-by-device findings
- Remediation recommendations
- Prevention measures

## Resources

- `scripts/analyze_network_logs.py` -- Main analysis script for parsing and correlating network logs
- `references/log-formats.md` -- Supported log formats and parsing patterns
- `references/anomaly-patterns.md` -- Documented anomaly detection patterns and thresholds

## Key Principles

1. **Timezone Normalization** -- All timestamps converted to UTC before correlation to ensure accurate event sequencing across devices in different timezones
2. **Multi-Source Correlation** -- Events from different devices correlated using configurable time windows (default 30 seconds) to identify related incidents
3. **Pattern-Based Detection** -- Anomalies detected using statistical thresholds (error rate spikes, connection failure clusters, latency outliers)
4. **Hypothesis Generation** -- Root causes ranked by supporting evidence count and temporal correlation strength
5. **Actionable Output** -- Reports include specific remediation steps and prevention recommendations

## Supported Log Formats

| Format | Example Pattern | Auto-Detection |
|--------|-----------------|----------------|
| Cisco IOS | `*Mar 15 10:23:45.123: %LINK-3-UPDOWN:` | Yes |
| Juniper JunOS | `Mar 15 10:23:45 router rpd[1234]:` | Yes |
| Palo Alto | `Mar 15 10:23:45,INFO,TRAFFIC,` | Yes |
| F5 BIG-IP | `Mar 15 10:23:45 bigip info tmm[1234]:` | Yes |
| Generic Syslog | `<134>Mar 15 10:23:45 hostname process:` | Yes |
| JSON Structured | `{"timestamp": "...", "level": "...", "message": "..."}` | Yes |

## Anomaly Detection Thresholds

Default thresholds (configurable via `--config` flag):
- **Error Rate Spike**: >3x baseline error rate within 5-minute window
- **Connection Failures**: >50 failures within 1-minute window
- **Latency Anomaly**: >2 standard deviations from rolling 10-minute average
- **Device Unreachable**: No logs from device for >2 minutes after consistent activity
