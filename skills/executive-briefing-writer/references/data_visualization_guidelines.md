# Data Visualization Guidelines for Executives

## Overview

This guide provides best practices for creating data visualizations that support executive decision-making. The goal is not to display all available data, but to communicate insight quickly and clearly.

## Core Principles

### Principle 1: One Chart, One Message

Every visualization should answer exactly one question. If you find yourself explaining multiple insights, split into multiple charts.

**Bad**: A complex chart showing revenue, costs, margins, and headcount over time
**Good**: Four focused charts, each with a clear insight in the title

### Principle 2: Title = Insight

Chart titles should be assertions, not descriptions.

| Type | Bad Title | Good Title |
|------|-----------|------------|
| Descriptive | "Revenue by Quarter" | "Revenue Up 23% YoY, Driven by Enterprise" |
| Observational | "Customer Satisfaction Scores" | "CSAT Recovered to 85 After Q2 Dip" |
| Actionable | "Cost Breakdown" | "IT Costs 40% Above Benchmark - Action Needed" |

### Principle 3: Maximize Data-Ink Ratio

Remove every element that doesn't add information:
- Unnecessary gridlines
- 3D effects
- Decorative images
- Redundant labels
- Chart borders

### Principle 4: Show Context, Not Just Numbers

Numbers without context are meaningless. Always show:
- Comparison to target/goal
- Trend direction (up/down)
- Benchmark or baseline
- Time period

---

## Chart Selection Guide

### By Message Type

| What You're Showing | Best Chart Types | Avoid |
|---------------------|------------------|-------|
| **Trend over time** | Line chart, Area chart | Pie chart, Bar for many periods |
| **Comparison** | Horizontal bar (many items), Column bar (few items) | Pie, 3D charts |
| **Part-to-whole** | Stacked bar, Waterfall, Treemap | Multiple pies |
| **Distribution** | Histogram, Box plot | Scatter for non-relationships |
| **Correlation** | Scatter plot, Bubble chart | Line chart |
| **Geographic** | Choropleth map, Symbol map | Over-decorated maps |
| **Process/Flow** | Sankey, Funnel | Complex network diagrams |

### By Data Characteristics

| Data Type | Recommended Approach |
|-----------|---------------------|
| **2-5 data points** | Column/bar chart, simple table |
| **6-15 data points** | Line chart, grouped bar |
| **Many categories** | Horizontal bar (sorted), treemap |
| **Time series** | Line chart, area chart |
| **Percentages (totaling 100%)** | Stacked bar, pie (max 5 slices) |
| **Two metrics comparison** | Dual-axis chart (use carefully), scatter |

---

## Formatting Standards

### Number Formatting

| Range | Format | Example |
|-------|--------|---------|
| Under 1,000 | Exact | 847 |
| 1,000 - 999,999 | Thousands (K) | 125K, 2.3K |
| 1,000,000+ | Millions (M) | 4.5M, 12.7M |
| 1,000,000,000+ | Billions (B) | 1.2B |

**Precision Rules**:
- Use 1 decimal place for numbers in the units (1.5M, not 1.53M)
- Use integers when possible (15%, not 15.3%)
- Be consistent within a document

### Currency and Units

- Always include currency symbol: $2.5M not 2.5M
- Spell out unit on first use, then abbreviate
- Use consistent units within comparisons (all in $K or all in $M)

### Percentage Formatting

| Context | Format |
|---------|--------|
| Change from baseline | +15% or -8% (always show sign) |
| Proportion | 45% (no sign) |
| Comparison | vs. target: +5pp (percentage points) |

---

## Color Usage

### Color Hierarchy

Use color intentionally to guide attention:

| Purpose | Color | Usage |
|---------|-------|-------|
| **Primary focus** | Bold/saturated color | The key data point |
| **Secondary data** | Muted/gray | Context and comparison |
| **Positive** | Green or blue | Good news, targets met |
| **Negative** | Red or orange | Concerns, targets missed |
| **Neutral** | Gray | Baseline, comparison data |

### Color Accessibility

- Ensure sufficient contrast (WCAG AA minimum)
- Don't rely on color alone (use patterns or labels)
- Test with colorblind simulation
- Limit to 5-7 colors maximum per chart

### Brand Colors

When using organizational brand colors:
- Use primary brand color for featured data
- Use secondary palette for additional categories
- Reserve accent colors for emphasis

---

## Executive Dashboard Design

### Layout Principles

```
┌────────────────────────────────────────────────────────┐
│  HEADLINE METRIC         │  STATUS SUMMARY            │
│  ┌─────────────────────┐ │  ✓ Revenue: On Track       │
│  │                     │ │  ⚠ Costs: Watch           │
│  │   $4.2M             │ │  ✗ Margin: Below Target   │
│  │   Revenue           │ │                            │
│  │   +12% vs. LY       │ │                            │
│  └─────────────────────┘ │                            │
├────────────────────────────────────────────────────────┤
│  TREND CHART                        │  BREAKDOWN       │
│  Revenue vs. Target                 │  By Region       │
│  ____/____                          │  ═══════ NA 45% │
│  ___/___                            │  ═════ EU 30%   │
│       Actual Target                 │  ═══ APAC 25%   │
├────────────────────────────────────────────────────────┤
│  KEY ACTIONS / ALERTS                                  │
│  • Action item 1                                       │
│  • Action item 2                                       │
└────────────────────────────────────────────────────────┘
```

### Information Hierarchy

1. **Hero Metrics** (top): 1-3 most important numbers, large font
2. **Status Indicators**: Traffic light or similar quick-scan indicators
3. **Trend Charts**: Show movement and trajectory
4. **Breakdowns**: Drill-down into composition
5. **Actions/Alerts**: Highlighted issues requiring attention

### Dashboard Dos and Don'ts

**Do**:
- Start with the question "What decision does this support?"
- Include target/benchmark lines on charts
- Use consistent time periods
- Provide date of last update
- Allow for appropriate white space

**Don't**:
- Pack in too many visualizations
- Use inconsistent scales across similar charts
- Mix too many chart types
- Forget to show trend direction
- Omit data source

---

## Annotation Best Practices

### When to Annotate

Add annotations for:
- Unusual data points (spikes, dips)
- Key events affecting the data
- Target or threshold lines
- The "so what" of the chart

### Annotation Styles

```
Revenue Growth

     ^
  12%├         ○←── "Q3: New product launch"
     │      ·  │
   8%├    ·    │
     │  ·      │
   4%├·        │
     │         │
   0%├─────────┼────────────────→
        Q1  Q2 │Q3  Q4
               │
        ···································
        Target Line at 6%
```

### Annotation Guidelines

- Place annotations near but not on the data
- Use leader lines to connect annotation to data point
- Keep annotation text brief (max 10 words)
- Use consistent annotation style throughout document

---

## Before and After Examples

### Example 1: Revenue Trend

**Before** (Problems):
```
           Revenue by Quarter
    ┌────────────────────────────────┐
    │  ████  ████  ████  ████       │
    │  Q1    Q2    Q3    Q4         │
    │  $2.1M $2.3M $2.4M $2.7M      │
    └────────────────────────────────┘
    3D bars, no trend line, no context
```

**After** (Improved):
```
    Revenue Up 29% YoY, Exceeding Target

         $M
     3.0 ├──────────────·─────── Target $2.5M
         │            ●
     2.5 ├          ●
         │        ●
     2.0 ├      ●
         │
         └──────┬────┬────┬────┬──→
                Q1   Q2   Q3   Q4

    ● Actual    · Target
```

### Example 2: Comparison Chart

**Before** (Problems):
```
         Market Share
    ┌─────────────────────┐
    │   ┌───┐             │
    │   │   │  Comp A 35% │
    │   │   │             │
    │   │   │  Us 28%     │
    │   │   │             │
    │   │   │  Comp B 22% │
    │   │   │             │
    │   │   │  Other 15%  │
    │   └───┘             │
    └─────────────────────┘
    Pie chart for comparison
```

**After** (Improved):
```
    We're #2 in Market Share, Gap Closing

    Competitor A  ████████████████  35%
    Us (2024)     ████████████ (+5) 28%  ← Up from 23%
    Competitor B  ██████████        22%
    Other         ██████            15%

    Change vs. 2023: Us +5pp, Comp A -3pp
```

### Example 3: Multi-variable Comparison

**Before** (Problems):
```
    Complex chart with 4 y-axes,
    12 data series, and unclear message
```

**After** (Improved):
```
    SEPARATE INTO FOCUSED PANELS:

    Panel 1: "Revenue Growth Accelerating"
    [Clean line chart with target]

    Panel 2: "Margins Stable at 42%"
    [Simple trend line]

    Panel 3: "Customer Acquisition Cost Up 15%"
    [Bar chart with benchmark line]
```

---

## Visualization Checklist

Before including a chart in executive materials:

**Message Clarity**:
- [ ] Chart answers one specific question
- [ ] Title states the insight (not just the topic)
- [ ] Main message is clear in 5 seconds

**Design Quality**:
- [ ] Removed all unnecessary elements (chartjunk)
- [ ] Colors used intentionally
- [ ] Text is legible at final size
- [ ] Consistent style with other charts in document

**Data Integrity**:
- [ ] Y-axis starts at appropriate value (usually 0 for bar charts)
- [ ] Time series is consistent (no missing periods)
- [ ] Numbers are accurate and current
- [ ] Source is cited

**Executive Appropriateness**:
- [ ] Level of detail matches audience
- [ ] Context is provided (vs. target, vs. prior period)
- [ ] Supporting data is in appendix if needed
- [ ] Connects to the "So What?"

---

## Tools and Resources

### Recommended Tools

| Tool | Best For | Notes |
|------|----------|-------|
| Excel | Quick charts, data analysis | Most accessible |
| PowerPoint/Google Slides | Presentation charts | Formatting control |
| Tableau | Interactive dashboards | Advanced analysis |
| Power BI | Corporate dashboards | Microsoft ecosystem |
| Python (matplotlib, seaborn) | Reproducible charts | Technical teams |

### Color Palette Resources

- ColorBrewer: Sequential, diverging, qualitative palettes
- Coolors: Palette generation and accessibility check
- Viz Palette: Test palettes for accessibility

### References

- Tufte, Edward. "The Visual Display of Quantitative Information"
- Few, Stephen. "Show Me the Numbers"
- Cairo, Alberto. "The Functional Art"
- Knaflic, Cole Nussbaumer. "Storytelling with Data"
