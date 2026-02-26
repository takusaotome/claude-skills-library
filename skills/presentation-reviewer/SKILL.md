---
name: presentation-reviewer
description: >-
  Use this skill when you need to review presentation materials from an audience
  perspective to improve their quality and effectiveness. Evaluates content clarity,
  visual design, logical flow, engagement factors, and Marp technical compatibility.
  Triggers include "review my presentation", "check my slides", "presentation feedback",
  or when a user has completed a draft presentation and wants comprehensive quality review.
---

# Presentation Reviewer

## Overview

Expert presentation reviewer specializing in evaluating presentation materials from the audience's perspective. Conducts comprehensive, objective reviews that identify areas for improvement and provides actionable recommendations.

## When to Use This Skill

- Reviewing a completed draft of presentation slides before finalizing
- Ensuring a presentation meets professional standards before delivery
- Getting feedback on visual design, content structure, and flow
- Checking Marp-specific technical compatibility issues
- Evaluating content density and scannability of slides

## Prerequisites

- **Presentation File**: Marp markdown (.md) or HTML file to review
- **Checklist Reference**: `references/presentation_best_practices_checklist.md` (bundled)

## Workflow

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
| **Visual Hierarchy** | Proper use of size, color, and spacing to guide attention |
| **One Slide One Message** | Each slide focuses on exactly one main concept |
| **Color Consistency** | Colors have consistent meaning (green=success, orange=warning, blue=info) |
| **Grid Layout** | Grid systems (.grid-2, .grid-3, .grid-4) used appropriately |
| **Badge and Highlight Usage** | Badges and highlighting used for appropriate emphasis |

### Step 4: Content Density Evaluation

- Check for slides with more than 5 bullet points (recommend splitting)
- Identify text-heavy slides that could benefit from visual elements
- Evaluate if numerical data could use .metric-card styling
- Assess if process information could use step cards or timeline visualization

### Step 5: Marp Technical Compatibility Checks

**CRITICAL**: Marp has specific rendering limitations that MUST be checked.

#### 5.1 HTML div内のMarkdownレンダリング不可問題

Marp does NOT render markdown syntax inside HTML `<div>` blocks.

- **PROHIBITED**: `<div style="display: flex;">` wrapping markdown content
- **PROHIBITED**: `<div style="display: grid;">` wrapping markdown content
- **CORRECT alternatives**:
  - Multi-column text: Use CSS `columns` property on a `section` class via `<!-- _class: classname -->`
  - Two-column content: Use `.two-column` + `.column` CSS Grid classes defined in `<style>`
  - Simple comparisons: Use markdown tables (`| Left | Right |`)
- **Detection**: Search for `<div style=.*display:\s*(flex|grid)` patterns — flag as **High** severity

#### 5.2 画像サイズ未指定・サイズ不適切

All images MUST have explicit width via `![w:SIZE](path)` syntax.

- **PROHIBITED**: `![](image.png)` without width specification
- **Guidelines by diagram type**:
  - Horizontal flowcharts (LR): `w:1000` ~ `w:1150`
  - Vertical flowcharts (TB): `w:700` ~ `w:900`
  - Complex diagrams with subgraphs: Start at `w:850`
  - Simple diagrams: `w:600` ~ `w:800`
- **Detection**: Search for `!\[` without `w:` parameter — flag as **Medium** severity

#### 5.3 フッター重複（Content-Footer Overlap）

Bottom ~100px of each slide is reserved for footer.

- **High-risk patterns**:
  - Tables with 6+ rows on a single slide
  - Slides with both a heading AND a large table/list
  - Stacked content (heading + subtitle + image + table on one slide)
- **Detection**: Count content elements per slide — flag slides with heading + subtitle + image + table/list as **High** severity

#### 5.4 2段組でのHTML table罫線問題

- **PROHIBITED**: Using `<table>` for layout purposes in Marp (borders visible even with `border: none`)
- **CORRECT**: Use CSS Grid classes (`.two-column` + `.column`) defined in `<style>` block
- **Detection**: Search for `<table` used for layout — flag as **Medium** severity

#### 5.5 TOCなど長いリストのはみ出し

- TOC slides with 10+ items will overflow in single column
- **CORRECT**: Define a section class with `columns: 2; column-gap: 40px;` via `<!-- _class: toc -->`
- **Detection**: Count TOC items — flag if >8 items in single-column layout

#### 5.6 SVG vs PNG for images

- Prefer `.png` for Mermaid diagrams in Marp (SVG rendering can be inconsistent)
- If `.svg` is referenced, recommend switching to `.png` with `![w:SIZE]` syntax

### Step 6: Checklist Compliance Review

Systematically evaluate against each item in `references/presentation_best_practices_checklist.md`.

### Step 7: Compile Review Report

For each issue identified:
- Clearly describe the problem and why it matters to the audience
- Explain how it fails to meet the checklist criteria
- Provide specific, actionable recommendations for improvement
- Prioritize issues by their impact on presentation effectiveness

## Output

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

## Resources

### References

| Reference | Path | Purpose |
|-----------|------|---------|
| Presentation Best Practices Checklist | `references/presentation_best_practices_checklist.md` | Comprehensive evaluation criteria checklist |
