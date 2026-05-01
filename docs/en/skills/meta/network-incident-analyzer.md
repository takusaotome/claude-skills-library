---
layout: default
title: "Network Incident Analyzer"
grand_parent: English
parent: Meta & Quality
nav_order: 17
lang_peer: /ja/skills/meta/network-incident-analyzer/
permalink: /en/skills/meta/network-incident-analyzer/
---

# Network Incident Analyzer
{: .no_toc }

Analyze network device logs to identify connectivity issues, latency problems, and outages. Correlate timestamps across timezones, detect anomaly patterns, and generate incident reports with root cause hypotheses. Use when troubleshooting network incidents from log files.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/network-incident-analyzer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/network-incident-analyzer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Analyzes network device logs (routers, switches, firewalls, load balancers) to identify connectivity issues, latency problems, and service outages. Automatically correlates events across multiple log files with different timestamp formats and timezones, detects anomaly patterns within specified time windows, and generates comprehensive incident reports with root cause hypotheses and remediation recommendations.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (datetime, re, json, collections, pathlib)

---

## 3. Quick Start

```bash
python3 scripts/analyze_network_logs.py \
  --logs /path/to/router.log /path/to/firewall.log \
  --start "2024-01-15 10:00:00" \
  --end "2024-01-15 12:00:00" \
  --timezone "America/New_York" \
  --output-dir ./incident-report
```

---

## 4. How It Works

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

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Troubleshooting network connectivity issues using device logs
- Analyzing multiple log files from different network devices to find correlated events
- Investigating service outages with logs spanning multiple timezones
- Identifying patterns in network latency or packet loss from log data
- Generating incident reports with root cause analysis from raw logs
- Correlating timestamps across devices with different time formats

---

## 6. Understanding the Output

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

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/network-incident-analyzer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: anomaly-patterns.md, log-formats.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: analyze_network_logs.py.
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

- `skills/network-incident-analyzer/references/anomaly-patterns.md`
- `skills/network-incident-analyzer/references/log-formats.md`

**Scripts:**

- `skills/network-incident-analyzer/scripts/analyze_network_logs.py`
