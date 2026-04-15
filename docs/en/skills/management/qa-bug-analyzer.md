---
layout: default
title: "QA Bug Analyzer"
grand_parent: English
parent: Project & Business
nav_order: 21
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

Follow this decision tree to determine the appropriate workflow:

```
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

After analysis, always:
1. Review quality_metrics_guide.md for metric interpretation
2. Review analysis_methodology.md for analysis best practices
3. Generate comprehensive Markdown report using report_template.md

---

## 5. Usage Examples

- **User provides bug ticket data** in CSV, Excel, JSON, or Markdown format
- **Quality assessment is needed** for project reviews, milestone gates, or release readiness
- **Trend analysis is requested** to understand quality patterns over time
- **Stakeholder reporting is required** for project managers or executive leadership
- **Improvement recommendations are needed** based on objective data analysis
- **User mentions:**

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 2 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/qa-bug-analyzer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: analysis_methodology.md, quality_metrics_guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: analyze_bugs.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/management/' | relative_url }}).
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

- `skills/qa-bug-analyzer/references/analysis_methodology.md`
- `skills/qa-bug-analyzer/references/quality_metrics_guide.md`

**Scripts:**

- `skills/qa-bug-analyzer/scripts/analyze_bugs.py`
