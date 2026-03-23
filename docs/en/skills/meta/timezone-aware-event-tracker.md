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

- `skills/timezone-aware-event-tracker/references/timezone-conversion-guide.md`

**Scripts:**

- `skills/timezone-aware-event-tracker/scripts/timezone_event_tracker.py`
