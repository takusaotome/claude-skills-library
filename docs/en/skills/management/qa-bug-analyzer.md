---
layout: default
title: "QA Bug Analyzer"
grand_parent: English
parent: Project & Business
nav_order: 19
lang_peer: /ja/skills/management/qa-bug-analyzer/
permalink: /en/skills/management/qa-bug-analyzer/
---

# QA Bug Analyzer
{: .no_toc }

This skill should be used when analyzing bug ticket data to identify quality trends, assess software quality status, and provide improvement recommendations. Use when a user provides bug lists (CSV, Excel, JSON, or Markdown format) and needs comprehensive quality analysis from a QA manager perspective. Generates statistical analysis, identifies quality hotspots, provides actionable recommendations, and produces professional Markdown reports suitable for project managers and executive leadership. Ideal for IT system development, migration, and implementation projects.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/qa-bug-analyzer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/qa-bug-analyzer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill enables comprehensive bug ticket analysis from a QA management perspective. Analyze bug data to identify quality trends, assess project health, pinpoint problem areas, and generate actionable improvement recommendations. The skill produces professional Markdown reports suitable for project managers, development managers, and executive leadership.

**Key capabilities:**
- Statistical analysis of bug distributions (severity, category, module, resolution time)
- Quality trend identification and hotspot detection
- Root cause pattern analysis
- Prioritized improvement recommendations
- Professional report generation for stakeholders

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
User provides bug data
    │
    ├─→ Data in CSV/JSON format
    │   └─→ Use Automated Analysis Workflow (Section 3)
    │
    ├─→ Data in multiple Markdown files (from bug-ticket-creator)
    │   └─→ Use Markdown Aggregation Workflow (Section 4)
    │
    └─→ User wants custom analysis or specific focus
        └─→ Use Custom Analysis Workflow (Section 5)
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

- `skills/qa-bug-analyzer/references/analysis_methodology.md`
- `skills/qa-bug-analyzer/references/quality_metrics_guide.md`

**Scripts:**

- `skills/qa-bug-analyzer/scripts/analyze_bugs.py`
