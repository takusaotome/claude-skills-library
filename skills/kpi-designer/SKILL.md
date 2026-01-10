---
name: kpi-designer
description: |
  KPI体系設計とOKR策定支援スキル。ビジネス目標に整合したKPI設計、バランススコアカード、OKRフレームワーク、
  ダッシュボード設計を提供。SMART原則、リーディング/ラギング指標の選定を支援。
  Use when designing KPI frameworks, implementing OKR methodology, or creating performance measurement systems.
  Triggers: "KPI design", "OKR", "performance metrics", "balanced scorecard", "dashboard design", "measurement framework".
---

# KPI Designer（KPI体系設計支援）

## Overview

This skill provides expert guidance for designing comprehensive KPI frameworks and implementing OKR (Objectives and Key Results) methodologies. Aligns metrics with strategic objectives and creates actionable measurement systems.

**Primary language**: Japanese (default), English supported
**Frameworks**: Balanced Scorecard, OKR, KPI Pyramid, SMART criteria
**Output format**: KPI frameworks, OKR sheets, dashboard designs, metric definitions

Use this skill when:
- Designing KPI frameworks for organizations or departments
- Implementing OKR methodology
- Creating balanced scorecards
- Designing performance dashboards
- Aligning metrics with strategy
- Improving data-driven decision making

---

## Core Concepts

### KPI (Key Performance Indicator) vs Metric

**Metric**: Any measurable value
- Example: Website visitors, revenue, employee count

**KPI**: A metric that is KEY to achieving objectives
- Aligns with strategic goals
- Actionable
- Owned by someone
- Reviewed regularly

**Not all metrics are KPIs.** Focus on the vital few, not the trivial many.

### Types of Indicators

#### Leading Indicators（先行指標）
- **Definition**: Predict future performance
- **Characteristic**: Influence outcomes, actionable
- **Examples**:
  - Sales pipeline value → Future revenue
  - Customer satisfaction → Customer retention
  - Employee engagement → Productivity

#### Lagging Indicators（遅行指標）
- **Definition**: Measure past performance
- **Characteristic**: Results-oriented, historical
- **Examples**:
  - Revenue (result of sales activities)
  - Customer churn (result of satisfaction issues)
  - Defect rate (result of quality processes)

**Best Practice**: Balance leading and lagging indicators. Leading indicators allow proactive action.

### SMART Criteria

All KPIs should be SMART:

**S - Specific（具体的）**: Clear, unambiguous
❌ "Improve customer satisfaction"
✅ "Increase NPS from 30 to 40"

**M - Measurable（測定可能）**: Quantifiable
❌ "Better quality"
✅ "Reduce defects from 5% to 2%"

**A - Achievable（達成可能）**: Realistic given resources
❌ "Increase revenue 500% in 1 month"
✅ "Increase revenue 15% in 12 months"

**R - Relevant（関連性）**: Aligned with objectives
❌ "Increase social media followers" (for a B2B enterprise software company)
✅ "Increase qualified leads from target accounts"

**T - Time-bound（期限）**: Deadline specified
❌ "Reduce costs"
✅ "Reduce costs by 10% by Q4 2026"

---

## Core Frameworks

### 1. Balanced Scorecard

**Four Perspectives**:

```
┌─────────────────┬─────────────────┐
│   Financial     │   Customer      │
│   財務の視点     │   顧客の視点     │
│                 │                 │
│ - Revenue       │ - NPS           │
│ - Profit Margin │ - Retention     │
│ - ROI           │ - Satisfaction  │
└─────────────────┴─────────────────┘
┌─────────────────┬─────────────────┐
│Internal Process │Learning & Growth│
│ 業務プロセス視点 │ 学習と成長視点   │
│                 │                 │
│ - Cycle Time    │ - Training Hours│
│ - Quality       │ - Engagement    │
│ - Innovation    │ - Skills        │
└─────────────────┴─────────────────┘
```

**How to Use**:
1. Define strategic objectives for each perspective
2. Identify KPIs for each objective
3. Set targets
4. Create strategy map (cause-effect relationships)

**Example Strategy Map**:
```
Learning & Growth: Improve Employee Skills
         ↓
Internal Process: Increase Process Efficiency
         ↓
Customer: Improve Customer Satisfaction
         ↓
Financial: Increase Revenue
```

### 2. OKR (Objectives and Key Results)

**Structure**:
```
Objective: Qualitative, aspirational goal
   ├─ Key Result 1: Quantitative, measurable outcome
   ├─ Key Result 2: Quantitative, measurable outcome
   └─ Key Result 3: Quantitative, measurable outcome
```

**Example**:
```
Objective: Become the market leader in customer satisfaction

Key Results:
1. Increase NPS from 30 to 50
2. Reduce churn rate from 15% to 8%
3. Achieve 95% on-time delivery rate
```

**OKR Best Practices**:
- **Ambitious**: 70% achievement is considered success
- **Time-boxed**: Quarterly or annual cycles
- **Limited**: 3-5 Objectives, 3-5 Key Results each
- **Transparent**: Visible to entire organization
- **Not linked to compensation**: Encourages stretch goals

**OKR Cadence**:
- **Annual OKRs**: Company-wide strategic objectives
- **Quarterly OKRs**: Department/team tactical objectives
- **Weekly Check-ins**: Progress review and adjustment

### 3. KPI Pyramid

```
         ┌───────────────┐
         │ Strategic KPIs│
         │   (Lagging)   │
         └───────────────┘
              ↑
       ┌──────────────┐
       │Tactical KPIs │
       │   (Mixed)    │
       └──────────────┘
              ↑
    ┌─────────────────┐
    │Operational KPIs │
    │   (Leading)     │
    └─────────────────┘
```

**Strategic KPIs** (C-Level):
- Revenue, profit, market share
- Annual review
- Lagging indicators

**Tactical KPIs** (Managers):
- Customer acquisition cost, conversion rate
- Monthly/Quarterly review
- Mix of leading and lagging

**Operational KPIs** (Teams):
- Daily active users, response time
- Daily/Weekly review
- Leading indicators

---

## Core Workflows

### Workflow 1: KPI Framework Design

**Purpose**: Create comprehensive KPI framework aligned with strategy.

#### Step 1: Understand Strategic Objectives

**Questions to Ask**:
- What are the organization's strategic goals?
- What are the key success factors?
- What are the priorities for this year?

**Example**:
```
Strategic Objective: Increase market share from 15% to 20% in 2026

Success Factors:
- Customer acquisition
- Product innovation
- Operational efficiency
```

#### Step 2: Identify Key Drivers

For each objective, identify what drives success:

```
Objective: Increase market share to 20%
  ↓
Drivers:
- New customer acquisition
- Customer retention
- Product differentiation
- Competitive pricing
- Market expansion
```

#### Step 3: Select KPIs

For each driver, select 1-2 KPIs:

```
Driver: New Customer Acquisition
  ├─ KPI 1: Monthly new customers (Leading)
  └─ KPI 2: Customer Acquisition Cost (CAC) (Efficiency)

Driver: Customer Retention
  ├─ KPI 1: Customer Retention Rate (Lagging)
  └─ KPI 2: Net Promoter Score (NPS) (Leading)
```

**Selection Criteria**:
- Aligned with strategy? ✅
- Actionable? ✅
- Measurable? ✅
- Cost-effective to track? ✅

#### Step 4: Define Each KPI

**KPI Definition Template**:
```markdown
## KPI: Net Promoter Score (NPS)

### Definition
Percentage of promoters (9-10) minus percentage of detractors (0-6)

### Formula
NPS = (% Promoters) - (% Detractors)

### Data Source
Customer satisfaction survey (monthly)

### Owner
Head of Customer Success

### Target
- Current: 30
- Target (Q4 2026): 50
- Stretch: 60

### Frequency
Monthly measurement, quarterly review

### Action Triggers
- < 25: Red (immediate action required)
- 25-40: Yellow (monitor closely)
- > 40: Green (on track)
```

#### Step 5: Create KPI Hierarchy

**Company-Level KPIs** → **Department KPIs** → **Team KPIs**

```
Company KPI: Revenue Growth 20% YoY
  ↓
Sales Dept KPI: New Deals $5M/quarter
  ↓
Sales Team KPI: 50 qualified leads/month per rep
```

**Ensure Alignment**: Lower-level KPIs should ladder up to higher-level KPIs.

### Workflow 2: OKR Implementation

**Purpose**: Implement OKR methodology across organization.

#### Step 1: Set Company OKRs (Annual)

**CEO and Leadership Team**:
- Define 3-5 company-wide objectives
- Each objective has 3-5 key results
- Communicate to entire organization

**Example**:
```
Company OKR 2026

Objective 1: Achieve market leadership in customer satisfaction
  KR1: NPS increases from 30 to 50
  KR2: Customer churn decreases from 15% to 8%
  KR3: 95% of support tickets resolved within SLA

Objective 2: Accelerate product innovation
  KR1: Launch 3 major product features
  KR2: Achieve 80% feature adoption rate
  KR3: Reduce time-to-market from 6 months to 3 months

Objective 3: Scale revenue growth sustainably
  KR1: Revenue grows from $50M to $65M (30% growth)
  KR2: Maintain gross margin at 70%+
  KR3: CAC payback period < 12 months
```

#### Step 2: Cascade to Departments (Quarterly)

Each department creates OKRs that support company OKRs:

**Product Team OKR (Q1 2026)**:
```
Objective: Deliver high-impact features that drive adoption

KR1: Ship Feature A by Jan 31 with 0 critical bugs
KR2: Achieve 60% adoption of Feature A by end of Q1
KR3: User satisfaction with new features: 4.5/5 stars

Alignment: Supports Company Objective 2 (Product Innovation)
```

#### Step 3: Individual OKRs (Optional)

Some organizations cascade to individuals, others keep it at team level.

**Individual OKR (Product Manager)**:
```
Objective: Successfully launch Feature A

KR1: Complete user research with 20 customers by Jan 10
KR2: Deliver detailed product spec by Jan 20
KR3: Achieve 80% positive feedback in beta testing
```

#### Step 4: Weekly Check-Ins

**Meeting Format (15-30 minutes)**:
1. Review progress on each Key Result (% complete)
2. Discuss blockers and risks
3. Adjust priorities if needed
4. Update confidence level (on track / at risk / off track)

**Example Check-In**:
```
KR1: Ship Feature A by Jan 31 (70% complete, ON TRACK)
- This week: Completed backend integration
- Next week: Frontend UI and testing
- Blockers: None

KR2: Achieve 60% adoption by Q1 end (20% complete, AT RISK)
- Current adoption: 12%
- Concern: Marketing campaign delayed
- Action: Accelerate go-to-market plan
```

#### Step 5: Quarterly Review and Retrospective

**Review**:
- Score each Key Result (0-100%)
- 70%+ = Success (remember, OKRs are aspirational)
- Discuss what worked, what didn't

**Retrospective Questions**:
- Were OKRs too easy or too hard?
- Did we focus on the right things?
- What should we change next quarter?

### Workflow 3: Dashboard Design

**Purpose**: Create actionable, user-friendly KPI dashboards.

#### Step 1: Audience Analysis

**Executive Dashboard**: High-level, strategic KPIs
- Frequency: Monthly review
- Metrics: 5-10 KPIs
- Format: Summary tiles, trend charts

**Manager Dashboard**: Tactical KPIs, drill-down capability
- Frequency: Weekly review
- Metrics: 15-20 KPIs
- Format: Departmental views, comparison charts

**Operational Dashboard**: Real-time operational metrics
- Frequency: Daily monitoring
- Metrics: 20-30 KPIs
- Format: Real-time updates, alerts

#### Step 2: Dashboard Layout Principles

**Information Hierarchy**:
```
┌─────────────────────────────────────┐
│ Most Important KPI (Large, Top-Left)│
├──────────────┬──────────────────────┤
│ Secondary KPI│ Supporting Chart     │
├──────────────┼──────────────────────┤
│ Tertiary KPI │ Trend Analysis       │
└──────────────┴──────────────────────┘
```

**Visual Encoding**:
- **RAG Status**: Red (bad), Amber (caution), Green (good)
- **Trend Arrows**: ↑ (improving), → (stable), ↓ (declining)
- **Sparklines**: Mini trend charts

**Example Executive Dashboard**:
```
┌─────────────────────────────────────────┐
│ Revenue:  $5.2M  ↑ 15% MoM  🟢          │
├───────────────────┬─────────────────────┤
│ NPS: 42  ↑ +5 🟢  │ [Trend Chart]       │
├───────────────────┼─────────────────────┤
│ Churn: 12% → 🟡   │ [Cohort Analysis]   │
├───────────────────┼─────────────────────┤
│ CAC: $850 ↓ 🟢    │ [Funnel Chart]      │
└───────────────────┴─────────────────────┘
```

#### Step 3: Chart Selection

**KPI Type** → **Best Chart Type**:

| KPI Type | Chart Type | Example |
|----------|------------|---------|
| Single Value | Big Number Tile | Revenue: $5.2M |
| Trend Over Time | Line Chart | Revenue trend (12 months) |
| Comparison | Bar Chart | Sales by region |
| Part-of-Whole | Pie/Donut Chart | Market share by product |
| Distribution | Histogram | Customer age distribution |
| Relationship | Scatter Plot | CAC vs. LTV |
| Progress | Gauge/Progress Bar | OKR completion: 75% |

#### Step 4: Drill-Down Design

**Dashboard Layers**:
```
Layer 1: Overview (Executive)
   ↓ Click
Layer 2: Department Detail (Manager)
   ↓ Click
Layer 3: Operational Detail (Analyst)
```

**Example Drill-Down**:
```
Layer 1: Revenue $5.2M ↑ 15%
   ↓
Layer 2: Revenue by Product
   - Product A: $2.5M ↑ 20%
   - Product B: $1.8M ↑ 10%
   - Product C: $0.9M ↑ 5%
   ↓
Layer 3: Product A Revenue by Customer Segment
   - Enterprise: $1.5M
   - Mid-Market: $0.8M
   - SMB: $0.2M
```

---

## Deliverable Templates

### 1. KPI Framework Document

```markdown
# KPI Framework: [Organization/Department]

## Strategic Objectives
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

## KPI Hierarchy

### Tier 1: Strategic KPIs (Executive)
| KPI | Owner | Current | Target | Frequency |
|-----|-------|---------|--------|-----------|
| Revenue Growth | CFO | 15% YoY | 20% YoY | Monthly |
| Customer Retention | CCO | 85% | 92% | Quarterly |
| NPS | CCO | 30 | 50 | Monthly |

### Tier 2: Tactical KPIs (Managers)
[Similar table structure]

### Tier 3: Operational KPIs (Teams)
[Similar table structure]

## KPI Definitions
[Detailed definition for each KPI using template above]

## Dashboard Access
- Executive Dashboard: [Link]
- Manager Dashboard: [Link]
- Operational Dashboard: [Link]

## Governance
- Review Frequency: Monthly
- Owner: [Name]
- Update Process: [Description]
```

### 2. OKR Template

```markdown
# OKRs: Q[X] 20XX

## Company OKRs

### Objective 1: [Aspirational Goal]
**Why this matters**: [Brief explanation]

**Key Results**:
1. [Measurable outcome 1]
   - Current: [Baseline]
   - Target: [Goal]
   - Owner: [Name]

2. [Measurable outcome 2]
   ...

3. [Measurable outcome 3]
   ...

**Initiatives** (How we'll achieve this):
- [Initiative A]
- [Initiative B]

---

[Repeat for Objectives 2-5]

---

## Department OKRs

### Sales Department

**Objective**: [Supports Company Objective X]

**Key Results**:
1. ...
2. ...
3. ...

---

## Weekly Check-In Template

Date: [Date]
Attendees: [Names]

### KR1: [Description]
- Progress: X% complete
- Status: 🟢 On Track / 🟡 At Risk / 🔴 Off Track
- This Week: [Accomplishments]
- Next Week: [Plans]
- Blockers: [Issues]
```

### 3. Dashboard Design Specification

```markdown
# Dashboard Design Spec: [Dashboard Name]

## Audience
- Primary: [Executive/Manager/Analyst]
- Use Case: [Purpose]
- Frequency: [How often viewed]

## Layout

### Section 1: Key Metrics (Top)
- Revenue (Big Number, Trend)
- NPS (Big Number, YoY Comparison)
- Churn Rate (Gauge)

### Section 2: Performance Trends (Middle)
- Revenue Trend (12-month line chart)
- Customer Acquisition (Bar chart by month)

### Section 3: Detailed Breakdown (Bottom)
- Revenue by Product (Stacked bar)
- Geographic Performance (Map)

## Interactivity
- Drill-down: Revenue → Product → Customer Segment
- Filters: Date range, region, product
- Export: PDF, Excel

## Data Refresh
- Real-time: [Which KPIs]
- Daily: [Which KPIs]
- Weekly: [Which KPIs]

## Tool
[Tableau / Power BI / Looker / Custom]
```

---

## Best Practices

### 1. Less is More
Focus on vital few KPIs, not trivial many. Aim for 5-10 KPIs per dashboard.

### 2. Balance Leading and Lagging
Include both to enable proactive management.

### 3. Align with Strategy
Every KPI should tie back to a strategic objective.

### 4. Make it Actionable
If a KPI goes red, what action should be taken? Define this upfront.

### 5. Review and Refine
KPIs should evolve with the business. Review annually.

### 6. Ensure Data Quality
Garbage in, garbage out. Validate data sources.

### 7. Train Users
Educate teams on how to interpret and act on KPIs.

### 8. Automate Data Collection
Manual data entry leads to errors and delays.

---

## Common Pitfalls

### ❌ Vanity Metrics
Metrics that look good but don't drive decisions.
**Example**: Social media followers (if not linked to business outcomes)

### ❌ Too Many KPIs
Information overload, no focus.
**Solution**: Prioritize ruthlessly.

### ❌ Lagging Indicators Only
Can't take proactive action.
**Solution**: Balance with leading indicators.

### ❌ No Ownership
Nobody responsible for driving improvement.
**Solution**: Assign clear owners.

### ❌ Set-and-Forget
KPIs never reviewed or updated.
**Solution**: Regular review cadence.

---

このスキルの目的は、データドリブンな意思決定を可能にし、組織のパフォーマンスを継続的に向上させることです。適切なKPI設計とOKRの実装を通じて、戦略実行を加速してください。
