---
layout: default
title: "Patent Analyst"
grand_parent: English
parent: Project & Business
nav_order: 17
lang_peer: /ja/skills/management/patent-analyst/
permalink: /en/skills/management/patent-analyst/
---

# Patent Analyst
{: .no_toc }

特許分析・知的財産戦略支援スキル。先行技術調査、特許性評価、特許ポートフォリオ分析、
侵害リスク評価、ライセンス戦略策定を支援。特許出願戦略の立案から権利化まで包括的にサポート。
Use when conducting prior art searches, evaluating patentability, analyzing patent portfolios,
assessing infringement risks, or developing IP strategies.
Triggers: "patent search", "prior art", "特許調査", "patentability", "FTO", "特許ポートフォリオ", "IP strategy", "patent landscape".

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/patent-analyst.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/patent-analyst){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides professional patent analysis and intellectual property (IP) strategy support. Helps organizations conduct prior art searches, evaluate patentability, analyze competitor patent portfolios, assess freedom-to-operate (FTO), and develop comprehensive IP strategies for competitive advantage.

**Primary language**: Japanese (default), English supported
**Patent Databases**: USPTO, EPO, JPO, WIPO, Google Patents, Espacenet, PatentScope
**Analysis Tools**: Patent citation analysis, technology landscape mapping, patent valuation
**Output format**: Prior art reports, patentability opinions, FTO analysis, IP strategy recommendations, patent landscape reports

Use this skill when:
- Conducting novelty searches before patent filing
- Evaluating patentability of inventions
- Performing freedom-to-operate (FTO) analysis before product launch
- Analyzing competitor patent portfolios
- Developing patent filing strategies
- Assessing patent infringement risks
- Preparing patent prosecution responses (Office Actions)
- Conducting due diligence for M&A or licensing

---

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

### Workflow 1: Prior Art Search (Novelty Search)

**Purpose**: Conduct comprehensive search to determine if an invention is novel and non-obvious before filing a patent application.

---

## 4. How It Works

### Workflow 1: Prior Art Search (Novelty Search)

**Purpose**: Conduct comprehensive search to determine if an invention is novel and non-obvious before filing a patent application.

#### Step 1: Understand the Invention

**Invention Disclosure Meeting**:
- **Participants**: Inventor(s), Patent Attorney/Agent, Patent Analyst
- **Duration**: 1-2 hours
- **Objective**: Understand technical details, problem solved, advantages, key features

**Key Information to Gather**:
```markdown

---

## 5. Usage Examples

- Use **Patent Analyst** when you need a structured workflow rather than an ad-hoc answer.
- Start with a small representative input before applying the workflow to production data or assets.
- Review the helper scripts and reference guides to tailor the output format to your project.

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Guidance derived directly from the skill instructions.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/patent-analyst/SKILL.md` open while working; it remains the authoritative source for the full procedure.
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

---

## 10. Reference

This skill uses built-in Claude capabilities without external scripts or references.
