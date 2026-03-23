---
layout: default
title: "Multi File Log Correlator"
grand_parent: English
parent: Meta & Quality
nav_order: 16
lang_peer: /ja/skills/meta/multi-file-log-correlator/
permalink: /en/skills/meta/multi-file-log-correlator/
---

# Multi File Log Correlator
{: .no_toc }

Correlate events across multiple log files from different sources, systems, or time periods.
Build unified timelines, identify causal relationships between events, and highlight anomalies
that span multiple data sources. Supports timezone normalization and gap detection.

Use when analyzing logs from multiple systems (frontend, backend, database, infrastructure),
investigating distributed system failures, or building event timelines across services.

Triggers: "correlate these logs", "build timeline from multiple logs", "cross-system analysis",
"find related events across logs", "multi-source log analysis", "distributed trace analysis"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/multi-file-log-correlator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/multi-file-log-correlator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill correlates events across multiple log files from different sources, systems, or time periods. It builds unified timelines, identifies causal relationships between events, and highlights anomalies that span multiple data sources. The skill handles timezone normalization, timestamp format differences, and gap detection to provide a comprehensive view of distributed system behavior.

**Key Capabilities:**
- Unified timeline construction from heterogeneous log sources
- Causal relationship inference between events across systems
- Timezone normalization and timestamp alignment
- Gap and anomaly detection across multiple data sources
- Correlation ID tracking and distributed trace reconstruction

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: pandas, python-dateutil (for timezone handling)

---

## 3. Quick Start

```bash
# List available log files
ls -la /path/to/logs/

# Check first few lines to identify format
head -5 app.log nginx.log database.log
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

- `skills/multi-file-log-correlator/references/correlation_methodology.md`
- `skills/multi-file-log-correlator/references/timestamp_formats.md`

**Scripts:**

- `skills/multi-file-log-correlator/scripts/correlate_logs.py`
