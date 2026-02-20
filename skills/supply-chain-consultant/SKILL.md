---
name: supply-chain-consultant
description: |
  サプライチェーン最適化コンサルティングスキル。需要予測、在庫最適化、調達戦略、
  物流ネットワーク設計、S&OP(Sales and Operations Planning)を支援。
  Use when optimizing supply chain operations, improving inventory management, designing logistics networks,
  or conducting supply chain risk assessments.
  Triggers: "supply chain", "在庫最適化", "inventory optimization", "demand forecasting", "S&OP", "procurement strategy", "logistics network".
---

# Supply Chain Consultant

## Overview

Professional supply chain management consulting: demand forecasting, inventory optimization, procurement strategy, logistics network design, and S&OP.

**Primary language**: Japanese (default), English supported
**Frameworks**: SCOR (Supply Chain Operations Reference), S&OP best practices, Lean Supply Chain, Theory of Constraints
**Output format**: Supply chain analysis reports, optimization recommendations, S&OP plans, network design proposals

Use this skill when:
- Optimizing inventory levels and reducing carrying costs
- Improving demand forecasting accuracy
- Designing or redesigning logistics networks
- Developing procurement strategies
- Implementing or improving S&OP processes
- Conducting supply chain risk assessments
- Reducing supply chain costs while maintaining service levels

---

## Core Framework: SCOR Model

### SCOR (Supply Chain Operations Reference Model)

SCOR is the global standard for supply chain process modeling (APICS).

**SCOR Structure**:
```
Level 1: Process Types
|- Plan: Demand/Supply planning, S&OP
|- Source: Procurement, supplier management
|- Make: Manufacturing, production planning
|- Deliver: Order fulfillment, logistics, warehousing
|- Return: Returns management, reverse logistics
|- Enable: Support processes (IT, finance, HR, quality)

Level 2: Process Categories (30 categories across 6 process types)
Level 3: Process Elements (Detailed activities)
Level 4: Implementation (Company-specific practices)
```

**SCOR Performance Attributes**:
1. **Reliability**: On-Time Delivery, Perfect Order %
2. **Responsiveness**: Order Fulfillment Lead Time, Supply Chain Cycle Time
3. **Agility**: Upside flexibility, Downside adaptability
4. **Cost**: Total Supply Chain Cost, Cost of Goods Sold
5. **Assets**: Cash-to-Cash Cycle Time, Inventory Days of Supply

---

## Workflows

### Workflow 1: Demand Forecasting Optimization

**Purpose**: Improve demand forecast accuracy to reduce stockouts and excess inventory.

**Decision Procedure**:
1. Assess current forecasting method, horizon, frequency, and ownership
2. Measure forecast accuracy (MAPE, Bias, Tracking Signal)
3. Segment products via ABC-XYZ analysis to determine forecasting approach per segment
4. Select forecasting technique:
   - **AX/BX**: Statistical methods (Moving Average, Exponential Smoothing)
   - **AY/BY**: Statistical + collaborative (Holt-Winters, consensus)
   - **AZ/BZ**: Demand sensing, safety stock buffers
   - **CX/CY/CZ**: Simple rules, Min-Max, or make-to-order
5. Design S&OP-integrated forecasting process
6. Monitor forecast KPIs and adjust

> **Detail**: Load `references/demand_forecasting_guide.md` for formulas, segmentation matrix, KPI dashboard template.
> **Script**: Run `scripts/generate_demand_kpi_dashboard.py` to generate a KPI dashboard from data.

---

### Workflow 2: Inventory Optimization

**Purpose**: Determine optimal inventory levels to balance cost and service level.

**Decision Procedure**:
1. Analyze current inventory health (Turnover, DOI, Carrying Cost, Service Level)
2. Identify excess (>90 days) and obsolete (>180 days) inventory
3. Calculate Safety Stock per SKU:
   - `SS = Z * sigma_DLT` where `sigma_DLT = sqrt(LT * sigma_D^2 + D_avg^2 * sigma_LT^2)`
   - `sigma_DLT` = demand variability over lead time (composite)
   - `sigma_D` = daily demand std dev, `sigma_LT` = lead time std dev (days)
4. Calculate EOQ: `EOQ = sqrt(2 * D * S / H)`
5. Set Reorder Point: `ROP = (D_avg * LT) + SS`
6. Assign inventory policy by ABC category:
   - **A items**: Continuous Review (s, Q) with precise EOQ/SS
   - **B items**: Periodic Review (R, S), weekly cycle
   - **C items**: Min-Max or Two-Bin, monthly cycle

> **Detail**: Load `references/inventory_optimization_guide.md` for full formulas, worked examples, and policy templates.
> **Script**: Run `scripts/generate_inventory_policy.py` to generate inventory policy tables from data.

---

### Workflow 3: Sales & Operations Planning (S&OP)

**Purpose**: Balance demand and supply at aggregate level, align cross-functional plans.

**Decision Procedure**:
1. Establish monthly S&OP cycle (5 meetings across 5 weeks)
2. Week 1: Gather demand forecast, supply plan, financial projections
3. Week 2: Demand Review — consensus demand plan
4. Week 3: Supply Review — capacity vs. demand, constraints, supply scenarios
5. Week 4: Pre-S&OP — integrate plans, identify gaps, prepare executive recommendations
6. Week 5: Executive S&OP — strategic decisions, approve final plan
7. Produce 4 deliverables: Demand Plan, Supply Plan, Inventory Plan, Gap Analysis with Scenarios

> **Detail**: Load `references/sop_planning_guide.md` for templates, agenda, and scenario analysis format.
> **Script**: Run `scripts/generate_sop_agenda.py` to generate a meeting agenda.

---

### Workflow 4: Logistics Network Design

**Purpose**: Optimize distribution network to minimize cost while meeting service level requirements.

**Decision Procedure**:
1. Map current network (plants, DCs, customer locations, demand distribution)
2. Analyze cost structure (inbound/outbound transport, warehouse, inventory carrying)
3. Measure service levels by region (lead time, OTD, fill rate)
4. Define optimization objective: Minimize total cost subject to service level, capacity, and continuity constraints
5. Model scenarios:
   - Baseline (current state)
   - DC consolidation (reduce fixed costs, assess service impact)
   - DC addition (improve underserved regions, calculate ROI)
   - Direct ship for high-volume customers (bypass DCs)
6. Evaluate trade-offs: cost savings vs. service level impact
7. Create implementation roadmap with phased rollout

> **Detail**: Load `references/logistics_network_guide.md` for cost templates, scenario analysis, and design recommendation format.

---

### Workflow 5: Procurement Strategy Development

**Purpose**: Develop strategic sourcing approach to optimize cost, quality, and supply risk.

**Decision Procedure**:
1. Conduct spend analysis (category breakdown, supplier concentration, tail spend)
2. Build supplier performance scorecards (Quality PPM, OTD%, Cost Trend)
3. Classify categories using Kraljic Matrix:
   - **Strategic** (High Risk, High Impact): Partnership, long-term contracts
   - **Bottleneck** (High Risk, Low Impact): Supply security, safety stock
   - **Leverage** (Low Risk, High Impact): Competitive bidding, consolidation
   - **Non-Critical** (Low Risk, Low Impact): Simplify, automate
4. Develop risk mitigation plans for strategic/bottleneck items
5. Create contingency plans for supply disruptions

> **Detail**: Load `references/procurement_strategy_guide.md` for Kraljic matrix, scorecard templates, and risk mitigation plan format.

---

## KPI Quick Reference

> **Full reference**: Load `references/kpi_reference.md` for all KPIs, benchmarks, best practices, and common pitfalls.

| Area | Key Metric | Target |
|------|-----------|--------|
| Delivery | On-Time Delivery (OTD) | >=95% |
| Delivery | Perfect Order Rate | >=90% |
| Inventory | Inventory Turnover | Industry benchmark |
| Inventory | Days of Inventory | 45-60 days |
| Demand | MAPE | <20% |
| Procurement | Supplier OTD | >=95% |
| Procurement | Supplier Quality | <500 PPM |
| Financial | Supply Chain Cost % Revenue | 8-12% |

---

このスキルの目的は、組織のサプライチェーンを最適化し、コスト削減とサービスレベル向上を両立させることです。需要予測、在庫管理、S&OP、物流ネットワーク、調達戦略の各領域において、データに基づいた意思決定と継続的改善を推進してください。
