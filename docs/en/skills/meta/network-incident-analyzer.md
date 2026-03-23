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

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/network-incident-analyzer/references/anomaly-patterns.md`
- `skills/network-incident-analyzer/references/log-formats.md`

**Scripts:**

- `skills/network-incident-analyzer/scripts/analyze_network_logs.py`
