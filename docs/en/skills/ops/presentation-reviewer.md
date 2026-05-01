---
layout: default
title: "Presentation Reviewer"
grand_parent: English
parent: Operations & Docs
nav_order: 10
lang_peer: /ja/skills/ops/presentation-reviewer/
permalink: /en/skills/ops/presentation-reviewer/
---

# Presentation Reviewer
{: .no_toc }

Use this skill when you need to review presentation materials from an audience perspective to improve their quality and effectiveness. Evaluates content clarity, visual design, logical flow, engagement factors, and Marp technical compatibility. Triggers include "review my presentation", "check my slides", "presentation feedback", or when a user has completed a draft presentation and wants comprehensive quality review.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/presentation-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/presentation-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Expert presentation reviewer specializing in evaluating presentation materials from the audience's perspective. Conducts comprehensive, objective reviews that identify areas for improvement and provides actionable recommendations.

---

## 2. Prerequisites

- **Presentation File**: Marp markdown (.md) or HTML file to review
- **Checklist Reference**: `references/presentation_best_practices_checklist.md` (bundled)

---

## 3. Quick Start

### Step 1: Load Review Criteria

Load and examine `references/presentation_best_practices_checklist.md` to understand all evaluation criteria.

---

## 4. How It Works

### Step 1: Load Review Criteria

Load and examine `references/presentation_best_practices_checklist.md` to understand all evaluation criteria.

### Step 2: Holistic Analysis

Analyze the presentation from the audience's viewpoint:

1. **Content Structure**: Logical flow and message clarity
2. **Visual Design**: Readability, professional appearance, design element usage
3. **Audience Engagement**: Factors that support comprehension and attention
4. **Information Hierarchy**: Clarity and scannability of content structure

### Step 3: Visual Design Review

Evaluate the following visual design aspects:

| Area | What to Check |
|------|---------------|
| **Information Categorization** | Color-coded boxes (.info-box, .success-box, .warning-box, .error-box) used effectively |
| **Metrics Presentation** | Quantitative data uses visual emphasis (.metric-card, .metric-value) |
| **Process Clarity** | Step-by-step processes use clear visual progression (.step-card, .step-number) |
| **Timeline Visualization** | Schedules and timelines are visually clear (.timeline-item, .timeline-badge) |
| **Content Scannability** | Key information can be absorbed in 10 seconds or less |

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Reviewing a completed draft of presentation slides before finalizing
- Ensuring a presentation meets professional standards before delivery
- Getting feedback on visual design, content structure, and flow
- Checking Marp-specific technical compatibility issues
- Evaluating content density and scannability of slides

---

## 6. Understanding the Output

The review produces a structured report with the following sections:

| Section | Content |
|---------|---------|
| **Executive Summary** | Overall assessment and key findings |
| **Visual Design Assessment** | Evaluation of visual elements and design effectiveness |
| **Checklist Compliance Review** | Systematic evaluation against each checklist item |
| **Critical Issues** | High-priority problems that significantly impact effectiveness |
| **Marp Technical Compatibility Issues** | Marp-specific rendering problems with severity and fix recommendations |
| **Visual Improvement Recommendations** | Specific suggestions for better use of visual design elements |
| **Content Optimization Suggestions** | Recommendations for content structure and clarity |
| **Strengths** | Positive aspects that should be maintained |

**Visual Design Recommendations Format**:

- **Current Issue**: Description of the problem (e.g., "Text-heavy bullet points without visual categorization")
- **Recommended Solution**: Specific implementation guidance (e.g., "Use .info-box class to highlight key information")
- **Expected Impact**: What improvement will result (e.g., "Improves scannability and helps audience prioritize information")

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/presentation-reviewer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: presentation_best_practices_checklist.md.
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

---

## 10. Reference

**References:**

- `skills/presentation-reviewer/references/presentation_best_practices_checklist.md`
