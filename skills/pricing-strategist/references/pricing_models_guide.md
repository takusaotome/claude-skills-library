# Pricing Models Guide

## Overview

This guide provides comprehensive coverage of the four primary pricing models used in IT services and consulting: Cost-Plus, Value-Based, Competitive, and Subscription. Each model has specific applications, advantages, and limitations that make it suitable for different service types and market conditions.

---

## 1. Cost-Plus Pricing

### Definition

Cost-plus pricing sets prices by calculating total costs (direct + indirect) and adding a predetermined markup percentage to achieve target profit margins.

```
Price = Total Cost + (Total Cost × Markup %)
Price = Total Cost × (1 + Markup %)
```

### Cost Components

#### Direct Costs
- **Labor**: Salaries, wages, benefits of personnel directly involved
- **Materials**: Software licenses, hardware, consumables
- **Subcontractor/Outsourcing**: Third-party service costs
- **Travel**: Client site visits, project-related travel

#### Indirect Costs (Overhead)
- **Facilities**: Rent, utilities, maintenance
- **Administration**: HR, finance, legal, management
- **Technology**: Internal IT, tools, infrastructure
- **Marketing & Sales**: Business development costs
- **Training & Development**: Staff skill development

### Overhead Allocation Methods

| Method | Formula | Best For |
|--------|---------|----------|
| Direct Labor % | Overhead ÷ Direct Labor Cost | Labor-intensive services |
| Revenue % | Overhead ÷ Revenue | Diverse service portfolio |
| Headcount | Overhead ÷ Employees | Similar cost structures |
| Activity-Based | Overhead by activity drivers | Complex operations |

### Markup Guidelines by Service Type

| Service Type | Typical Markup | Rationale |
|--------------|----------------|-----------|
| Commodity IT Support | 10-20% | High competition, price pressure |
| Standard Development | 20-30% | Moderate differentiation |
| Specialized Services | 30-50% | Technical expertise premium |
| Strategic Consulting | 40-60% | High value, limited competition |

### Calculation Example

```
Project: Web Application Development

Direct Costs:
- Developer Labor (800 hours × $75/hr): $60,000
- Project Manager (200 hours × $100/hr): $20,000
- Software Licenses: $5,000
- Cloud Infrastructure: $3,000
Total Direct: $88,000

Indirect Costs (25% allocation):
- Overhead: $22,000
Total Cost: $110,000

Target Markup: 25%
Price: $110,000 × 1.25 = $137,500
```

### Advantages
- Simple to calculate and explain
- Ensures cost recovery
- Predictable margins
- Easy to justify in procurement contexts

### Disadvantages
- Ignores customer value perception
- No incentive for efficiency
- May leave money on table for high-value services
- Vulnerable to cost underestimation

### Best Applications
- Competitive bid situations
- Commodity services
- Government/public sector contracts
- Cost-reimbursable contracts
- Internal chargebacks

---

## 2. Value-Based Pricing

### Definition

Value-based pricing sets prices according to the economic value delivered to customers, rather than the cost of delivery. The price is a percentage of the quantified customer benefit.

```
Price = Customer Value × Value Capture Rate (typically 10-30%)
```

### Value Categories

#### Quantifiable Value

| Category | Measurement | Examples |
|----------|-------------|----------|
| **Cost Reduction** | Direct savings | Labor reduction, license consolidation, infrastructure optimization |
| **Productivity Gains** | Time × Cost | Process automation, workflow improvement, reduced errors |
| **Revenue Increase** | Additional revenue × margin | New capabilities, faster time-to-market |
| **Risk Mitigation** | Exposure × Probability | Compliance, security, disaster recovery |
| **Capital Avoidance** | Deferred/avoided investment | Cloud migration, system modernization |

#### Qualitative Value (Harder to Quantify)
- Strategic positioning
- Competitive advantage
- Employee satisfaction
- Customer experience
- Brand enhancement

### Total Economic Impact (TEI) Framework

```
Year 1-3 TEI Calculation

Benefits:
├── Cost Savings
│   ├── Labor Reduction: [Amount]
│   ├── License Consolidation: [Amount]
│   └── Operational Efficiency: [Amount]
├── Productivity Gains
│   ├── Time Saved × Hourly Rate: [Amount]
│   └── Error Reduction: [Amount]
├── Revenue Impact
│   ├── New Revenue Enabled: [Amount]
│   └── Faster Time-to-Market: [Amount]
└── Risk Avoidance
    ├── Compliance Penalty Avoided: [Amount]
    └── Downtime Prevention: [Amount]

Total Gross Benefits: [Sum]
Less: Investment Cost: [Price]
Net Benefits: [Difference]
ROI: [Net Benefits / Investment] × 100%
NPV (at discount rate): [Calculated]
Payback Period: [Months/Years]
```

### Value Capture Rate Guidelines

| Factor | Lower Rate (10-15%) | Higher Rate (25-30%) |
|--------|---------------------|----------------------|
| Competition | Many alternatives | Few/no alternatives |
| Differentiation | Moderate | High uniqueness |
| Relationship | New customer | Strategic partner |
| Risk Profile | Customer bears risk | Provider bears risk |
| Value Certainty | Uncertain outcomes | Proven outcomes |

### Value Discovery Questions

**Business Impact Questions**
1. What is this problem costing you annually?
2. How many people are affected by this issue?
3. What happens if this problem isn't solved in the next 12 months?
4. How much revenue are you losing to competitors due to this gap?

**Current State Questions**
1. How many hours per week are spent on this process?
2. What is the error rate and cost per error?
3. How long does [process] take currently?
4. What systems are you paying for that could be eliminated?

**Success Metrics Questions**
1. How will you measure success for this initiative?
2. What KPIs are tied to executive compensation?
3. What would "exceeding expectations" look like?

### Calculation Example

```
Cloud Migration Project

Customer Current State:
- On-premise infrastructure cost: $500,000/year
- IT staff maintaining infrastructure: 4 FTEs × $120,000 = $480,000
- Downtime costs (historical): $200,000/year
- Total annual cost: $1,180,000

Post-Migration State:
- Cloud infrastructure: $300,000/year
- IT staff (reduced): 2 FTEs × $120,000 = $240,000
- Downtime (improved): $50,000/year
- Total annual cost: $590,000

Annual Savings: $590,000
3-Year Value (NPV at 10%): $1,467,000

Value Capture Rate: 20%
Recommended Price: $293,400
```

### Advantages
- Captures fair share of value created
- Aligns incentives with customer outcomes
- Higher profit potential
- Differentiates from commodity competitors

### Disadvantages
- Requires extensive discovery
- Value can be disputed
- Longer sales cycles
- Not suitable for all services

### Best Applications
- Strategic consulting
- Digital transformation
- Custom software development
- Business process optimization
- Technology advisory

---

## 3. Competitive Pricing

### Definition

Competitive pricing sets prices based on market positioning relative to competitors, using competitor prices as the primary reference point.

```
Price = Competitor Reference Price × Positioning Factor
```

### Positioning Strategies

| Strategy | Price Position | When to Use |
|----------|---------------|-------------|
| **Premium** | 110-150% of market | Strong brand, superior quality, unique capabilities |
| **Parity** | 95-105% of market | Similar offerings, compete on service/relationship |
| **Penetration** | 70-90% of market | Market entry, volume play, cost advantage |
| **Economy** | 60-80% of market | Cost leadership, minimum service |

### Competitive Intelligence Framework

#### Data Collection Sources
1. **Public Information**
   - Published rate cards
   - Website pricing pages
   - Industry reports
   - Job postings (salary → rate inference)

2. **Market Intelligence**
   - Lost deal feedback
   - Customer conversations
   - Partner/vendor insights
   - Industry conferences

3. **Formal Research**
   - RFP response analysis
   - Win/loss analysis
   - Mystery shopping
   - Third-party research

#### Competitive Price Matrix

```
| Competitor | Basic Service | Standard | Premium | Notes |
|------------|---------------|----------|---------|-------|
| Competitor A | $X | $Y | $Z | Market leader |
| Competitor B | $X | $Y | $Z | Low-cost player |
| Competitor C | $X | $Y | $Z | Premium positioning |
| Market Average | $X | $Y | $Z | Benchmark |
| Our Current | $X | $Y | $Z | Current position |
| Our Target | $X | $Y | $Z | Proposed position |
```

### Differentiation Factors

Justify premium over competitors:

| Factor | Value Add | Premium Justification |
|--------|-----------|----------------------|
| Expertise | Specialized skills | +10-20% |
| Track Record | Proven results | +5-15% |
| Methodology | Proprietary approach | +10-25% |
| Technology | Advanced tools | +5-15% |
| Support | Superior service | +5-10% |
| Risk Reduction | Guarantees, SLAs | +5-15% |

### Calculation Example

```
IT Managed Services - Per User Pricing

Competitor Analysis:
- Competitor A (Premium): $150/user/month
- Competitor B (Standard): $100/user/month
- Competitor C (Budget): $75/user/month
Market Average: $108/user/month

Our Positioning: Standard+ with security focus
- Base: Market average $108
- Security differentiation: +15%
- Target Price: $124/user/month
```

### Advantages
- Market-validated pricing
- Easy to communicate
- Reduces price objections
- Quick to implement

### Disadvantages
- Race to bottom risk
- Ignores own costs
- Ignores customer value
- Follows, doesn't lead

### Best Applications
- Commodity services
- Market entry
- High competition markets
- Price-sensitive segments

---

## 4. Subscription/Recurring Pricing

### Definition

Subscription pricing charges recurring fees (monthly, annually) for ongoing access to services, rather than one-time project fees.

```
Monthly Recurring Revenue (MRR) = Users × Price per User
Annual Recurring Revenue (ARR) = MRR × 12
```

### Subscription Models

#### Per-Seat/Per-User
- **Model**: Fixed fee per licensed user
- **Best for**: Productivity tools, collaboration platforms
- **Example**: $20/user/month

#### Per-Unit/Per-Device
- **Model**: Fixed fee per managed device/asset
- **Best for**: MSP, device management
- **Example**: $50/device/month

#### Usage-Based
- **Model**: Variable fee based on consumption
- **Best for**: Cloud services, API calls
- **Example**: $0.10/API call + $100 base

#### Tiered/Feature-Based
- **Model**: Different packages at different prices
- **Best for**: SaaS, differentiated offerings
- **Example**: Basic $99, Pro $299, Enterprise Custom

### Tier Design Principles

#### Good-Better-Best Framework

| Element | Good | Better | Best |
|---------|------|--------|------|
| **Purpose** | Entry point | Main offering | Premium/Enterprise |
| **Target** | SMB, trials | Core market | Large/strategic |
| **Price** | Anchor low | 1.5-2x Good | 2.5-4x Good |
| **Features** | Core only | Extended | Full + custom |
| **Support** | Self-service | Email + chat | Phone + dedicated |
| **SLA** | None | Standard | Premium |

#### Psychological Pricing Tactics

1. **Anchoring**: Place expensive option first
2. **Decoy Effect**: Middle option looks most attractive
3. **Charm Pricing**: $99 vs $100
4. **Annual Discount**: 2 months free = 17% discount

### Metrics for Subscription Businesses

| Metric | Formula | Target |
|--------|---------|--------|
| MRR | Sum of monthly fees | Growing |
| ARR | MRR × 12 | Growing |
| ARPU | Revenue / Users | Stable or growing |
| Churn | Lost customers / Total | <5% monthly |
| LTV | ARPU × Average Lifespan | >3× CAC |
| CAC | Sales+Marketing / New Customers | <1/3 LTV |

### Calculation Example

```
MSP Subscription Pricing

Service Tiers:
- Bronze (Basic): $75/user/month
  - 99.5% SLA, email support, basic monitoring

- Silver (Standard): $125/user/month
  - 99.9% SLA, email + chat, full monitoring, security basics

- Gold (Premium): $200/user/month
  - 99.95% SLA, 24/7 phone, full security suite, dedicated account manager

Customer: 100 users on Silver
MRR: 100 × $125 = $12,500
ARR: $12,500 × 12 = $150,000

Upgrade potential:
- Move 30% to Gold: 30 × $200 = $6,000 + 70 × $125 = $8,750
- New MRR: $14,750 (+18%)
```

### Advantages
- Predictable revenue
- Higher customer lifetime value
- Easier capacity planning
- Better customer relationships

### Disadvantages
- Requires ongoing value delivery
- Churn management critical
- Cash flow timing (vs. project fees)
- Harder for large one-time needs

### Best Applications
- SaaS products
- Managed services (MSP)
- Ongoing support contracts
- Maintenance agreements
- Retainer-based consulting

---

## 5. Hybrid Pricing Models

### Common Hybrid Patterns

#### Base + Variable
```
Monthly Fee = Base Fee + (Usage × Rate)

Example: Cloud MSP
- Base: $2,000/month (management, support)
- Variable: $50/server + $10/TB storage
- Total: $2,000 + (20 servers × $50) + (100TB × $10) = $4,000/month
```

#### Fixed + Success Fee
```
Total Fee = Fixed Component + (Success Fee × Achievement Rate)

Example: Sales Optimization Consulting
- Fixed fee: $100,000 (discovery, implementation)
- Success fee: 10% of incremental revenue above baseline
- If +$500,000 revenue achieved: $100,000 + $50,000 = $150,000
```

#### License + Services
```
Total = License Fee + Implementation + Annual Support

Example: Enterprise Software
- Perpetual License: $500,000
- Implementation: $200,000
- Annual Support (20%): $100,000/year
```

#### T&M with Cap
```
Fee = MIN(Actual Hours × Rate, Cap)

Example: Application Development
- Rate: $150/hour
- Estimate: 500 hours = $75,000
- Cap: $90,000 (120% of estimate)
- If actual = 700 hours: Pay $90,000 (capped)
```

---

## 6. Pricing Model Selection Framework

### Decision Matrix

| Factor | Cost-Plus | Value-Based | Competitive | Subscription |
|--------|-----------|-------------|-------------|--------------|
| Value Measurable | Low | High | Medium | Medium |
| Competition | High | Low | High | Medium |
| Relationship | Transactional | Strategic | Either | Ongoing |
| Service Type | Commodity | Custom | Standard | Continuous |
| Risk Appetite | Provider | Shared | Market | Balanced |

### Service Type Recommendations

| Service Category | Primary Model | Secondary Model |
|-----------------|---------------|-----------------|
| Infrastructure (commodity) | Cost-Plus | Competitive |
| Managed Services | Subscription | Competitive |
| Strategic Consulting | Value-Based | Fixed + Success |
| Custom Development | Value-Based | T&M with Cap |
| SaaS | Subscription (Tiered) | Usage-Based |
| Hardware/Product | Competitive | Cost-Plus |
| Staff Augmentation | Competitive | Cost-Plus |
| Training | Competitive | Value-Based |

### Selection Checklist

- [ ] Can customer value be quantified? → Consider Value-Based
- [ ] Is service ongoing/continuous? → Consider Subscription
- [ ] Is market pricing well-established? → Consider Competitive
- [ ] Are costs predictable and clear? → Consider Cost-Plus
- [ ] Is customer relationship strategic? → Consider Value-Based
- [ ] Is service commoditized? → Consider Competitive/Cost-Plus

---

## 7. Best Practices

### General Principles

1. **Match Model to Value**: Strategic services deserve value-based pricing
2. **Know Your Costs**: Even value-based needs cost floor awareness
3. **Understand Competition**: Market context always matters
4. **Segment Pricing**: Different models for different customer types
5. **Review Regularly**: Pricing should evolve with market

### Common Mistakes to Avoid

1. **Cost-Plus for Everything**: Leaves money on table for high-value services
2. **Ignoring Costs**: Value-based doesn't mean ignore profitability
3. **Price Wars**: Competing solely on price destroys margins
4. **Complexity Overload**: Too many pricing variables confuse customers
5. **Static Pricing**: Never reviewing prices as market changes

---

## Summary Table

| Model | Formula | Best For | Key Advantage | Key Risk |
|-------|---------|----------|---------------|----------|
| Cost-Plus | Cost × (1+Markup) | Commodity, Bids | Simple, cost recovery | Leaves value on table |
| Value-Based | Value × Capture% | Strategic, Custom | High margin potential | Requires discovery |
| Competitive | Competitor × Position | Standard, Entry | Market validated | Race to bottom |
| Subscription | Users × Monthly Fee | SaaS, Managed | Predictable revenue | Churn risk |
