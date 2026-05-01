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

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Investigating incidents involving multiple services (frontend, API, database, cache)
- Analyzing distributed system failures across microservices
- Building event timelines from logs with different timestamp formats
- Correlating infrastructure logs with application logs
- Detecting timing anomalies between system components
- Tracing request flows across multiple services

---

## 6. Understanding the Output

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

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/multi-file-log-correlator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: timestamp_formats.md, correlation_methodology.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: correlate_logs.py.
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

- `skills/multi-file-log-correlator/references/correlation_methodology.md`
- `skills/multi-file-log-correlator/references/timestamp_formats.md`

**Scripts:**

- `skills/multi-file-log-correlator/scripts/correlate_logs.py`
