---
layout: default
title: "Data Visualization Expert"
grand_parent: English
parent: Operations & Docs
nav_order: 7
lang_peer: /ja/skills/ops/data-visualization-expert/
permalink: /en/skills/ops/data-visualization-expert/
---

# Data Visualization Expert
{: .no_toc }

Professional data visualization skill specialized in creating reader-friendly, accessible, and aesthetically pleasing charts and dashboards. Use this skill when you need to create visualizations, choose appropriate chart types, design color schemes, create dashboards, or apply design best practices for data communication. Expertise includes visualization principles, color theory, typography, layout design, and accessibility guidelines.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/data-visualization-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/data-visualization-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Create publication-quality, accessible, and reader-friendly data visualizations that communicate insights effectively. This skill provides comprehensive guidance on visualization design principles, chart selection, color theory, dashboard design, and best practices for professional data communication.

---

## 2. Prerequisites

Before using this skill, ensure:

- **Python 3.8+** with the following packages installed:
  - `matplotlib>=3.5.0`
  - `seaborn>=0.12.0`
  - `pandas>=1.3.0`
  - `numpy>=1.20.0`
- **Japanese Font Support** (optional, for Japanese text):
  - macOS: Built-in (Hiragino Sans)
  - Windows: Built-in (Yu Gothic, Meiryo)
  - Linux: Install `fonts-noto-cjk` or `fonts-takao`
- **Input Data**: CSV files with headers for chart creation scripts

Install dependencies:
```bash
pip install matplotlib seaborn pandas numpy
```

---

## 3. Quick Start

```bash
1. Understand the Goal
   ↓
2. Analyze the Data
   ↓
3. Select Chart Type
   ↓
4. Choose Color Palette
   ↓
5. Apply Design Principles
   ↓
6. Add Context & Annotations
   ↓
7. Ensure Accessibility
   ↓
8. Review & Refine
```

---

## 4. How It Works

Follow this systematic approach when creating visualizations:

```
1. Understand the Goal
   ↓
2. Analyze the Data
   ↓
3. Select Chart Type
   ↓
4. Choose Color Palette
   ↓
5. Apply Design Principles
   ↓
6. Add Context & Annotations
   ↓
7. Ensure Accessibility
   ↓
8. Review & Refine
```

---

## 5. Usage Examples

- **Chart Creation:** Creating any type of chart or graph
- **Chart Selection:** Choosing the right visualization for your data
- **Color Design:** Selecting color palettes and ensuring accessibility
- **Dashboard Design:** Creating executive dashboards or operational monitors
- **Visual Design:** Improving readability and aesthetic appeal
- **Accessibility:** Ensuring visualizations work for colorblind viewers

---

## 6. Understanding the Output

This skill produces the following outputs:

| Output Type | Format | Description |
|-------------|--------|-------------|
| **Chart Images** | PNG, PDF, SVG | Publication-quality visualizations (300 DPI default) |
| **Dashboards** | PNG, PDF | Multi-chart layouts with KPI cards |
| **Code Snippets** | Python | Ready-to-execute matplotlib/seaborn code |

### Output Characteristics

- **Resolution**: 300 DPI (configurable via `--dpi` flag)
- **Color Mode**: RGB with white background
- **Font Embedding**: Supported for PDF output
- **File Naming**: User-specified via `--output` parameter

### Example Output Locations

```bash

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/data-visualization-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: dashboard_design.md, chart_selection_guide.md, visualization_principles.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: create_visualization.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/ops/' | relative_url }}).
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

- `skills/data-visualization-expert/references/chart_selection_guide.md`
- `skills/data-visualization-expert/references/dashboard_design.md`
- `skills/data-visualization-expert/references/visualization_principles.md`

**Scripts:**

- `skills/data-visualization-expert/scripts/create_visualization.py`
