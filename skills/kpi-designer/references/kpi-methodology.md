# KPI Design Methodology Reference

This document provides methodology guidance for KPI design, selection, and validation.

## SMART Criteria Validation

### Specific（具体的）
- **Pass**: Clear, unambiguous definition with exact measurement
- **Fail**: Vague or subjective description

| Criteria | Pass Example | Fail Example |
|----------|--------------|--------------|
| Clear metric name | Net Promoter Score (NPS) | Customer happiness |
| Defined formula | (Promoters - Detractors) / Total × 100 | Satisfaction level |
| Single interpretation | Revenue in USD | Performance |

### Measurable（測定可能）
- **Pass**: Quantifiable with available data source
- **Fail**: Cannot be measured or no data source exists

| Criteria | Pass Example | Fail Example |
|----------|--------------|--------------|
| Numeric output | Churn rate: 12% | "Low churn" |
| Data source exists | CRM system data | Customer feelings |
| Repeatable measurement | Monthly survey | Ad-hoc observation |

### Achievable（達成可能）
- **Pass**: Realistic given resources, timeframe, and baseline
- **Fail**: Impossible or trivially easy

| Criteria | Pass Example | Fail Example |
|----------|--------------|--------------|
| Based on historical data | 15% YoY growth (historical: 10-12%) | 500% growth in 1 month |
| Resource-feasible | With current team capacity | Requires 10x budget |
| Considers constraints | Market conditions accounted | Ignores competition |

### Relevant（関連性）
- **Pass**: Directly connected to strategic objectives
- **Fail**: Vanity metric or unrelated to goals

| Criteria | Pass Example | Fail Example |
|----------|--------------|--------------|
| Supports strategy | CAC for growth-focused company | Social followers for B2B enterprise |
| Actionable | Team can influence the metric | External factors only |
| Business impact | Affects revenue/cost/satisfaction | No clear business value |

### Time-bound（期限）
- **Pass**: Clear deadline or measurement frequency
- **Fail**: No timeline specified

| Criteria | Pass Example | Fail Example |
|----------|--------------|--------------|
| Deadline specified | By Q4 2026 | "Eventually" |
| Frequency defined | Monthly measurement | When we have time |
| Review cadence | Quarterly review meetings | No review process |

## Leading vs Lagging Indicator Classification

### Decision Tree

```
Is the metric a RESULT of past actions?
    │
    ├── YES → LAGGING INDICATOR
    │         Examples: Revenue, Churn Rate, Defect Rate
    │
    └── NO → Does the metric PREDICT future outcomes?
              │
              ├── YES → LEADING INDICATOR
              │         Examples: Pipeline Value, NPS, Training Hours
              │
              └── NO → Consider if this is truly a KPI
```

### Recommended Balance

| Level | Leading : Lagging | Rationale |
|-------|-------------------|-----------|
| Strategic | 30:70 | Results-focused |
| Tactical | 50:50 | Balanced view |
| Operational | 70:30 | Proactive control |

## KPI Ownership Assignment

### Ownership Criteria

1. **Authority**: Can the owner influence the metric?
2. **Accountability**: Is the owner responsible for outcomes?
3. **Access**: Does the owner have data access?
4. **Action**: Can the owner take corrective action?

### Typical Ownership by KPI Type

| KPI Type | Typical Owner | Escalation Path |
|----------|---------------|-----------------|
| Financial (Revenue, Profit) | CFO | CEO, Board |
| Customer (NPS, Churn) | CCO, VP Customer Success | COO |
| Product (Features, Adoption) | CPO, Product Manager | CTO |
| Operations (Cycle Time, Quality) | VP Operations | COO |
| People (Engagement, Retention) | CHRO | CEO |

## Target Setting Methods

### 1. Historical Baseline Method
```
Target = Baseline × (1 + Expected Improvement %)

Example:
- Current NPS: 30
- Expected Improvement: 20%
- Target NPS: 30 × 1.20 = 36
```

### 2. Benchmark Method
```
Target = Industry Benchmark × Adjustment Factor

Example:
- Industry Average NPS: 45
- Our Position Goal: Top quartile (+10)
- Target NPS: 55
```

### 3. Driver-Based Method
```
Target = f(Underlying Drivers)

Example:
- Revenue Target = (New Customers × ACV) + (Existing × Retention × Upsell)
- Revenue = (1000 × $10K) + (5000 × 0.9 × 1.1) = $10M + $4.95M = $14.95M
```

## Action Trigger Thresholds

### RAG Status Definition

| Status | Threshold | Action Required |
|--------|-----------|-----------------|
| 🟢 Green | ≥90% of target | Continue current approach |
| 🟡 Amber | 70-89% of target | Investigate, prepare action plan |
| 🔴 Red | <70% of target | Immediate intervention required |

### Escalation Matrix

| Status Duration | Action |
|-----------------|--------|
| Red for 1 period | Owner reviews and creates action plan |
| Red for 2 periods | Escalate to manager, weekly tracking |
| Red for 3+ periods | Executive review, resource reallocation |
