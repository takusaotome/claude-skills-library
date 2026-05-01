---
layout: default
title: "Lean Six Sigma Consultant"
grand_parent: English
parent: Finance & Analysis
nav_order: 10
lang_peer: /ja/skills/finance/lean-six-sigma-consultant/
permalink: /en/skills/finance/lean-six-sigma-consultant/
---

# Lean Six Sigma Consultant
{: .no_toc }

Comprehensive Lean Six Sigma consulting skill supporting all belt levels (White Belt to Master Black Belt). Use this skill for DMAIC/DMADV project execution, Lean waste elimination (VSM, 8 Wastes/DOWNTIME, 5S), statistical analysis (process capability Cp/Cpk, control charts, hypothesis testing), and Six Sigma training/education. Triggers include "improve process", "reduce defects", "sigma level", "DMAIC project", "value stream mapping", "Kaizen", "process capability", "control chart", "root cause analysis", "5 Whys", "Fishbone diagram", "FMEA", "DOE", or requests involving process improvement methodologies.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/lean-six-sigma-consultant.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/lean-six-sigma-consultant){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides comprehensive Lean Six Sigma consulting capabilities, integrating the waste elimination focus of Lean with the variation reduction rigor of Six Sigma. It supports practitioners at all belt levels from awareness (White Belt) through strategic deployment (Master Black Belt).

**Primary Language**: Japanese (default), English supported
**Knowledge Base**: 33 reference files covering methodology, tools, statistics, industries, and training
**Output Format**: Project guidance, analysis reports, templates, training materials

### The Integration of Lean and Six Sigma

**Six Sigma** focuses on reducing process variation and defects using statistical methods (DMAIC methodology). The goal is achieving 3.4 defects per million opportunities (6 sigma level).

**Lean** focuses on eliminating waste and improving flow using Toyota Production System principles. The goal is maximizing customer value while minimizing waste.

**Lean Six Sigma** combines both:
- Use **Lean tools** to identify and eliminate waste, improve flow
- Use **Six Sigma tools** to reduce variation, solve complex problems
- Use **DMAIC** as the overarching improvement framework

---

## 2. Prerequisites

Before using this skill, ensure the following dependencies are installed:

```bash
# Required Python packages for statistical analysis scripts
pip install numpy scipy
```

**Scripts require**:
- Python 3.8+
- `numpy` for numerical calculations
- `scipy` for statistical functions (normal distribution, hypothesis testing)

**Optional dependencies**:
- Process measurement data in CSV format
- Specification limits (USL, LSL) for capability analysis

---

---

## 3. Quick Start

```bash
# Calculate sigma level from defect data
python scripts/sigma_calculator.py --defects 15 --units 1000 --opportunities 5

# Analyze process capability
python scripts/process_capability.py --demo

# Perform control chart analysis
python scripts/control_chart_analysis.py --demo
```

---

## 4. How It Works

This skill supports multiple workflows depending on the user's objective:

1. **DMAIC Project Execution** (Core Workflow 1)
   - Define → Measure → Analyze → Improve → Control
   - Use for improving existing processes

2. **DMADV/DFSS** (Core Workflow 2)
   - Define → Measure → Analyze → Design → Verify
   - Use for designing new processes/products

3. **Lean Waste Elimination** (Core Workflow 3)
   - Value Stream Mapping → Identify 8 Wastes → Design Future State → Kaizen
   - Use for eliminating waste and improving flow

4. **Statistical Analysis Support** (Core Workflow 4)
   - Process capability, control charts, hypothesis testing
   - Use for data-driven decision making

5. **Training/Education** (Core Workflow 6)
   - Belt-level curricula (White to Master Black Belt)
   - Use for learning and certification preparation

**Quick Start**:
```bash

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Leading or supporting a process improvement project
- Need guidance on which DMAIC phase tools to use
- Want to reduce defects, errors, or variation in a process
- Need to eliminate waste and improve cycle time
- Implementing statistical process control
- Conducting root cause analysis (5 Whys, Fishbone)

---

## 6. Understanding the Output

This skill produces the following outputs:

| Output Type | Format | Description |
|-------------|--------|-------------|
| **DMAIC Project Guidance** | Markdown/Text | Step-by-step guidance through each DMAIC phase with tollgate checklists |
| **Process Metrics Report** | JSON/Text | Sigma level, DPMO, yield, capability indices (Cp, Cpk, Pp, Ppk) |
| **Control Chart Analysis** | JSON/Text | Control limits, out-of-control detection, Western Electric rule violations |
| **Root Cause Analysis** | Markdown | Fishbone diagrams, 5 Whys analysis, Pareto charts |
| **Templates** | Markdown | Project Charter, SIPOC, FMEA, Control Plan, A3 Report |
| **Training Materials** | Markdown | Belt-level curricula, certification preparation guides |

**Example Output** (Sigma Calculator):
```
================================================================
SIGMA LEVEL ANALYSIS REPORT
================================================================

📥 INPUT DATA:

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/lean-six-sigma-consultant/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: quick_reference_guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: sigma_calculator.py, control_chart_analysis.py, process_capability.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/finance/' | relative_url }}).
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

- `skills/lean-six-sigma-consultant/references/quick_reference_guide.md`

**Scripts:**

- `skills/lean-six-sigma-consultant/scripts/control_chart_analysis.py`
- `skills/lean-six-sigma-consultant/scripts/process_capability.py`
- `skills/lean-six-sigma-consultant/scripts/sigma_calculator.py`
