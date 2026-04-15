---
layout: default
title: "Executive Briefing Writer"
grand_parent: English
parent: Project & Business
nav_order: 12
lang_peer: /ja/skills/management/executive-briefing-writer/
permalink: /en/skills/management/executive-briefing-writer/
---

# Executive Briefing Writer
{: .no_toc }

Use this skill when creating executive-level briefing materials, board reports, management meeting presentations, or investor briefings. This skill provides the "So What? / Why Now? / What Next?" framework, data visualization guidelines optimized for executives, and professional templates for rapid document creation. Triggers include "create board report", "executive summary", "management meeting materials", "investor presentation", "one-page summary", or requests to communicate complex information to senior leadership.

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/executive-briefing-writer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/executive-briefing-writer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill helps create:
- One-page executive summaries
- Board of Directors reports
- Management meeting materials
- Investor briefing documents

**Core Framework**: So What? / Why Now? / What Next?

**Key Principles**:
- Bottom Line Up Front (BLUF)
- 30-second rule (key message visible immediately)
- Decision-oriented structure
- Data visualization for impact

---

## 2. Prerequisites

- **Input Content**: Raw data, analysis results, or information to be communicated to executives
- **Audience Knowledge**: Understanding of who will receive the document (CEO, Board, investors, etc.)
- **Decision Context**: Clarity on what decision or action is being requested (if applicable)
- **Timeline**: Awareness of relevant deadlines or urgency factors

---

## 3. Quick Start

```bash
After reviewing this document, the reader should:
1. Understand: [Key insight or situation]
2. Believe: [Core message or conclusion]
3. Do: [Specific action or decision]
```

---

## 4. How It Works

### Purpose
Clarify what you're trying to achieve and who will receive the document. This determines structure, depth, and tone.

### Step 1: Define the Document Purpose

Identify the primary objective:

| Purpose Type | Description | Key Focus |
|--------------|-------------|-----------|
| **Decision Request** | Seeking approval or choice between options | Options, risks, recommendation |
| **Status Report** | Informing on progress or situation | Metrics, trends, deviations |
| **Proposal** | Advocating for an initiative or investment | Business case, ROI, timeline |
| **Alert/Escalation** | Raising awareness of risk or issue | Impact, urgency, mitigation |

### Step 2: Identify the Audience

Understand your audience's perspective:

| Audience | Time Available | Primary Concerns | Preferred Format |
|----------|----------------|------------------|------------------|
| CEO | Very limited | Strategic impact, risks | One-page summary |
| Board of Directors | Limited | Governance, compliance, returns | Formal report |
| Executive Committee | Moderate | Cross-functional impact | Meeting materials |
| Investors | Moderate | Returns, growth, risks | Structured briefing |

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Creating materials for C-suite, board, or investors
- Summarizing complex information for decision-makers
- Preparing approval requests or investment proposals
- Communicating strategic initiatives or operational updates

---

## 6. Understanding the Output

This skill generates **executive briefing documents** in Markdown format:
- One-page executive summaries
- Board of Directors reports
- Management meeting materials
- Investor briefing documents

Documents are created using templates from `assets/` and follow the "So What? / Why Now? / What Next?" framework.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/executive-briefing-writer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: action_recommendation_patterns.md, executive_communication_guide.md, data_visualization_guidelines.md.
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

---

## 10. Reference

**References:**

- `skills/executive-briefing-writer/references/action_recommendation_patterns.md`
- `skills/executive-briefing-writer/references/data_visualization_guidelines.md`
- `skills/executive-briefing-writer/references/executive_communication_guide.md`
- `skills/executive-briefing-writer/references/so_what_framework.md`
