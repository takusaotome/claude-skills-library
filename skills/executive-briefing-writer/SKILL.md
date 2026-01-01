---
name: executive-briefing-writer
description: |
  Use this skill when creating executive-level briefing materials, board reports, management meeting presentations, or investor briefings. This skill provides the "So What? / Why Now? / What Next?" framework, data visualization guidelines optimized for executives, and professional templates for rapid document creation. Triggers include "create board report", "executive summary", "management meeting materials", "investor presentation", "one-page summary", or requests to communicate complex information to senior leadership.
---

# Executive Briefing Writer

A specialized skill for creating high-impact executive communications that drive decisions and save leadership time.

## Overview

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

## When to Use

- Creating materials for C-suite, board, or investors
- Summarizing complex information for decision-makers
- Preparing approval requests or investment proposals
- Communicating strategic initiatives or operational updates

## Available Resources

### References (Load on-demand for guidance)
- `references/executive_communication_guide.md` - Communication principles for executives
- `references/so_what_framework.md` - The So What? / Why Now? / What Next? framework
- `references/data_visualization_guidelines.md` - Data visualization best practices
- `references/action_recommendation_patterns.md` - Action recommendation patterns

### Templates (Use for document generation)
- `assets/one_page_summary_template_[ja|en].md` - One-page executive summary
- `assets/board_report_template_[ja|en].md` - Board of Directors report
- `assets/management_meeting_template_[ja|en].md` - Management meeting materials
- `assets/investor_briefing_template_[ja|en].md` - Investor briefing document

---

## Workflow 1: Purpose and Audience Definition

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

### Step 3: Define Expected Outcome

Specify what should happen after reading:

```
After reviewing this document, the reader should:
1. Understand: [Key insight or situation]
2. Believe: [Core message or conclusion]
3. Do: [Specific action or decision]
```

---

## Workflow 2: Apply the So What? Framework

### Purpose
Structure your message using the "So What? / Why Now? / What Next?" framework to ensure relevance and actionability.

### Step 1: So What? - Extract the Core Message

Ask yourself: "Why should the executive care about this?"

**Good Example**:
> "Customer churn increased 15% this quarter, putting $2.3M ARR at risk."

**Bad Example**:
> "Customer churn increased 15% this quarter." (No impact stated)

**Checklist**:
- [ ] Business impact is quantified (revenue, cost, risk, market share)
- [ ] Impact is relevant to audience's responsibilities
- [ ] Message is specific, not vague

### Step 2: Why Now? - Establish Urgency

Ask yourself: "Why does this need attention now?"

**Good Example**:
> "Q4 budget lock is in 2 weeks; delay means 6-month postponement."

**Bad Example**:
> "We should address this soon." (No specific timeline)

**Urgency Triggers**:
- Deadline approaching (budget cycle, contract renewal, regulatory)
- Window of opportunity closing (market timing, competitive move)
- Risk accelerating (trend worsening, threshold approaching)
- Dependencies requiring early decision

### Step 3: What Next? - Propose Clear Actions

Ask yourself: "What specific action do you want?"

**Good Example**:
> "Approve $150K for customer success program; implementation starts Dec 1."

**Bad Example**:
> "We recommend improving customer retention." (No specific action)

**Action Format**:
```
[ACTION VERB] + [SPECIFIC THING] + [BY WHEN/HOW MUCH]

Examples:
- Approve the $2M capital expenditure for new facility
- Decide between Option A (in-house) or Option B (outsource)
- Authorize hiring of 3 additional engineers
```

---

## Workflow 3: Structure Design

### Purpose
Organize information using the Pyramid Principle and design the document structure.

### Step 1: Apply the Pyramid Principle

Structure information from conclusion to supporting evidence:

```
Level 1: Main Message (Answer/Conclusion)
         |
Level 2: Key Supporting Points (3-5 maximum)
         |
Level 3: Evidence/Data (Only as needed)
```

**Before (Chronological - Wrong)**:
> "We analyzed customer feedback, then reviewed churn data, conducted interviews, and concluded that..."

**After (Pyramid - Correct)**:
> "Recommendation: Invest $500K in customer success. This will reduce churn by 20% based on three findings: [1] Exit interviews reveal..., [2] Data shows..., [3] Competitor analysis indicates..."

### Step 2: Design the One-Page Summary

Every executive document needs a scannable first page:

```
+--------------------------------------------+
| [TITLE] - [DATE]                           |
+--------------------------------------------+
| EXECUTIVE SUMMARY (3-5 sentences)          |
| - Core message with So What?               |
| - Why Now?                                 |
| - What Next? (Recommendation)              |
+--------------------------------------------+
| KEY METRICS          | SITUATION           |
| +---+ +---+ +---+    | Current state       |
| |KPI| |KPI| |KPI|    | Key developments    |
| +---+ +---+ +---+    |                     |
+--------------------------------------------+
| RECOMMENDATION / NEXT STEPS                |
| 1. Specific action item                    |
| 2. Timeline                                |
| 3. Required resources                      |
+--------------------------------------------+
```

### Step 3: Determine Detail Pages

Based on audience and purpose, select additional sections:

| Section | When to Include |
|---------|-----------------|
| Background/Context | If audience lacks familiarity |
| Analysis Details | If methodology matters for credibility |
| Financial Breakdown | For investment decisions |
| Risk Assessment | For high-stakes decisions |
| Implementation Plan | For project approvals |
| Appendix | For reference data |

---

## Workflow 4: Data Visualization

### Purpose
Present data in ways that support executive decision-making.

### Step 1: Select Appropriate Chart Types

| Message Type | Recommended Chart | Avoid |
|--------------|------------------|-------|
| Trend over time | Line chart, Area chart | Pie chart |
| Comparison | Bar chart (horizontal for many items) | 3D charts |
| Composition | Stacked bar, Treemap | Multiple pie charts |
| Distribution | Histogram, Box plot | Complex scatter |
| Relationship | Scatter plot, Bubble chart | Over-decorated visuals |

### Step 2: Apply Executive Visualization Principles

**Rule 1: One Chart, One Message**
- Each visualization should answer one question
- Include the insight in the title: "Revenue Up 23% YoY" not "Revenue Chart"

**Rule 2: Maximize Data-Ink Ratio**
- Remove gridlines, excessive labels, decorative elements
- Use color intentionally (highlight key data, gray for context)

**Rule 3: Use Consistent Formatting**
- Round numbers appropriately ($2.3M not $2,347,892)
- Use consistent units and scales
- Include context (vs. target, vs. prior period)

### Step 3: Add Annotations for Insight

Highlight what matters:
- Circle or arrow pointing to key data points
- Brief annotation explaining significance
- Compare to benchmark or target

```
Revenue ($M)
     ^
  3 -|      .-----  <- "New product launch"
     |    .-'
  2 -| ---'
     |
  1 -|
     +-----+-----+-----+-->
          Q1    Q2    Q3
```

---

## Workflow 5: Action Recommendations

### Purpose
Present recommendations in a way that facilitates executive decision-making.

### Step 1: Structure Options Clearly

When presenting options, use consistent format:

| Criteria | Option A: Build | Option B: Buy | Option C: Partner |
|----------|-----------------|---------------|-------------------|
| Cost | $500K | $800K | $300K |
| Timeline | 6 months | 2 months | 3 months |
| Control | High | Medium | Low |
| Risk | Technical risk | Vendor dependency | IP exposure |
| **Recommendation** | | **Preferred** | |

### Step 2: Highlight Risks and Trade-offs

Be explicit about what could go wrong:

```
Key Risks:
+------------------------------------------------------+
| Risk              | Impact  | Likelihood | Mitigation |
+-------------------+---------+------------+------------+
| Vendor delay      | High    | Medium     | Milestone  |
|                   |         |            | penalties  |
| Cost overrun      | Medium  | Low        | Fixed-     |
|                   |         |            | price bid  |
+------------------------------------------------------+
```

### Step 3: Make the Ask Explicit

End with a clear request:

**For Approval**:
> "Requesting approval to proceed with Option B at $800K budget. Authorization signature required below."

**For Decision**:
> "Decision required by [date]: Select Option A, B, or C. If no decision by [date], project will be delayed by [impact]."

**For Information**:
> "No action required. This report is for awareness. Questions can be directed to [contact]."

---

## Workflow 6: Document Generation and Quality Check

### Purpose
Generate the final document using templates and ensure executive-level quality.

### Step 1: Select and Load Template

Choose appropriate template based on audience and purpose:

```
Purpose: Board Report -> assets/board_report_template_[ja|en].md
Purpose: Management Meeting -> assets/management_meeting_template_[ja|en].md
Purpose: Investor Briefing -> assets/investor_briefing_template_[ja|en].md
Purpose: General Summary -> assets/one_page_summary_template_[ja|en].md
```

### Step 2: Populate Template

Fill in each section following the guidance in the template:
- Replace all placeholder text with actual content
- Ensure So What? / Why Now? / What Next? are addressed
- Verify all data visualizations follow guidelines
- Include specific recommendations and next steps

### Step 3: Executive Quality Checklist

Before finalizing, verify:

**Content Quality**:
- [ ] Main message visible in first 30 seconds
- [ ] So What? is answered with business impact
- [ ] Why Now? establishes clear urgency
- [ ] What Next? specifies concrete action
- [ ] Data supports conclusions (no gaps in logic)

**Format Quality**:
- [ ] One-page summary scannable in 60 seconds
- [ ] Charts have insight in title
- [ ] Numbers are consistently formatted
- [ ] No jargon or unexplained acronyms
- [ ] Action items are specific and dated

**Audience Alignment**:
- [ ] Appropriate for audience's time constraints
- [ ] Addresses audience's likely questions
- [ ] Recommendation within audience's authority
- [ ] Risks and trade-offs acknowledged

---

## Quick Reference

### Template Selection Guide

| Audience | Document Type | Template |
|----------|---------------|----------|
| CEO/C-Suite | Quick update | one_page_summary |
| Board of Directors | Formal proposal | board_report |
| Executive Committee | Working session | management_meeting |
| Investors/Analysts | Performance review | investor_briefing |

### Common Mistakes to Avoid

1. **Burying the lead** - Put conclusion first, not last
2. **Data dump** - Curate, don't overwhelm
3. **Vague recommendations** - Be specific about action and timeline
4. **Missing the "so what"** - Always connect to business impact
5. **Too much detail** - Executives need summary, not comprehensive analysis
