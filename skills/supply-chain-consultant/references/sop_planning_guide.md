# Sales & Operations Planning (S&OP) Guide

## S&OP Cycle (Monthly)

```
Week 1: Data Gathering
|- Update demand forecast (Demand Planning)
|- Update supply plan (Supply Planning)
|- Gather financial projections (Finance)

Week 2: Demand Review Meeting
|- Present statistical baseline forecast
|- Marketing input (promotions, new products)
|- Sales input (market intelligence)
|- Output: Consensus demand plan

Week 3: Supply Review Meeting
|- Assess capacity vs. demand
|- Identify constraints (materials, labor, equipment)
|- Develop supply scenarios
|- Output: Supply plan options

Week 4: Pre-S&OP Meeting
|- Integrate demand and supply plans
|- Identify gaps and trade-offs
|- Prepare recommendations for executive team
|- Output: Executive S&OP agenda

Week 5 (Start of Month): Executive S&OP Meeting
|- Review demand/supply balance
|- Make strategic decisions (capacity investment, product portfolio)
|- Approve final plan
|- Output: Authorized operating plan for execution
```

---

## S&OP Deliverables

### 1. Demand Plan (by Product Family)

| Product Family | [M-1] Actual | [M] Fcst | [M+1] Fcst | [M+2] Fcst | [M+3] Fcst | [Q] Total |
|----------------|------------|----------|----------|----------|----------|----------|
| Product Line A | [value] | [value] | [value] | [value] | [value] | [total] |
| Product Line B | [value] | [value] | [value] | [value] | [value] | [total] |
| Product Line C | [value] | [value] | [value] | [value] | [value] | [total] |
| **Total** | **[value]** | **[value]** | **[value]** | **[value]** | **[value]** | **[total]** |

**Key Assumptions**: List growth drivers, seasonal factors, phase-outs.

### 2. Supply Plan (by Product Family)

| Product Family | [M] Plan | [M+1] Plan | [M+2] Plan | [M+3] Plan | [Q] Total | Capacity |
|----------------|----------|----------|----------|----------|----------|----------|
| Product Line A | [value] | [value] | [value] | [value] | [total] | [cap] |
| Product Line B | [value] | [value] | [value] | [value] | [total] | [cap] |
| Product Line C | [value] | [value] | [value] | [value] | [total] | [cap] |
| **Total** | **[value]** | **[value]** | **[value]** | **[value]** | **[total]** | **[cap]** |

**Capacity Utilization**: [value]% (target range: 85-95%)
**Constraints**: [identify any]

### 3. Inventory Plan

| Product Family | [M-1] Ending | [M] Plan | [M+1] Plan | [M+2] Plan | [M+3] Plan | Target DOI |
|----------------|------------|----------|----------|----------|----------|------------|
| Product Line A | [value] | [value] | [value] | [value] | [value] | [days] |
| Product Line B | [value] | [value] | [value] | [value] | [value] | [days] |
| Product Line C | [value] | [value] | [value] | [value] | [value] | [days] |
| **Total** | **[value]** | **[value]** | **[value]** | **[value]** | **[value]** | **[days]** |

### 4. Gap Analysis and Scenarios

```markdown
# S&OP Gap Analysis - [Month]

## Demand-Supply Balance
- **Demand Plan**: [value] units
- **Current Supply Plan**: [value] units
- **Gap**: [value] units ([Surplus/Shortage])

## Scenarios

### Scenario 1: [Name] (Recommended)
- **Action**: [description]
- **Cost**: $[value]
- **Pros**: [list]
- **Cons**: [list]
- **Decision**: [Approved/Rejected] by [role]

### Scenario 2: [Name]
- **Action**: [description]
- **Cost**: $[value]
- **Pros**: [list]
- **Cons**: [list]
- **Decision**: [Approved/Rejected] - [reason]
```

---

## Executive S&OP Meeting Agenda Template

Use `scripts/generate_sop_agenda.py` to generate, or use the template below:

```markdown
# Executive S&OP Meeting Agenda
**Date**: YYYY-MM-DD
**Time**: [start] - [end]
**Attendees**: CEO, CFO, COO, VP Sales, VP Marketing, VP Supply Chain

---

## 1. Previous Meeting Follow-Up (10 min)
- Review action items from previous S&OP meeting
- Status of ongoing projects

## 2. Business Review (15 min)
- Financial performance vs. plan (CFO)
- Market trends and competitive landscape (VP Marketing)
- Key customer feedback (VP Sales)

## 3. Demand Review (20 min)
- Next-quarter demand plan by product family
- Forecast accuracy review (last 3 months)
- Key assumptions and risks
- **Decision Required**: Approve demand plan

## 4. Supply Review (20 min)
- Next-quarter supply plan and capacity utilization
- Supply constraints and bottlenecks
- Inventory plan and targets
- **Decision Required**: Approve supply plan

## 5. Gap Analysis & Trade-Offs (20 min)
- Demand-supply gap analysis
- Scenario analysis
- **Decision Required**: Approve resolution plan

## 6. New Product Launch Review (15 min)
- Launch readiness assessment
- Demand ramp-up assumptions
- Supply readiness (materials, capacity, training)
- **Decision Required**: Approve launch date or delay

## 7. Strategic Topics (15 min)
- [Topic 1]
- [Topic 2]
- **Decision Required**: [specific decision]

## 8. Wrap-Up (5 min)
- Summary of decisions made
- Action items and owners
- Next meeting: YYYY-MM-DD

---

**Pre-Read Materials** (distributed 2 days before meeting):
- S&OP Demand Plan
- S&OP Supply Plan
- Gap Analysis & Scenarios
- Financial Summary
```
