# IT Services Pricing Guide

## Overview

This guide provides pricing strategies specific to IT service categories: Managed Services (MSP), IT Consulting, SaaS, System Development (Custom Software), and Hardware Sales. Each category has unique pricing models, benchmarks, and best practices.

---

## 1. Managed Services Provider (MSP) Pricing

### Pricing Models

#### Per-User Pricing
```
Monthly Fee = Number of Users × Per-User Rate

Example:
- 100 users × $125/user/month = $12,500/month
```

**Pros**: Simple, predictable, scales with organization size
**Cons**: Doesn't account for device complexity

**Typical Ranges (USD, 2024-2025):**
| Service Level | Per-User/Month |
|---------------|----------------|
| Basic (monitoring, email support) | $75 - $100 |
| Standard (above + help desk) | $100 - $150 |
| Premium (above + 24/7, security) | $150 - $250 |
| Enterprise (custom SLA) | $200 - $400 |

#### Per-Device Pricing
```
Monthly Fee = Σ (Device Type × Device Rate)

Example:
- 80 workstations × $50 = $4,000
- 20 servers × $150 = $3,000
- 10 network devices × $30 = $300
Total: $7,300/month
```

**Typical Rates:**
| Device Type | Per-Device/Month |
|-------------|------------------|
| Workstation | $35 - $75 |
| Server | $100 - $300 |
| Network Device | $20 - $50 |
| Mobile Device | $10 - $30 |
| Virtual Machine | $25 - $75 |

#### Tiered Package Pricing

**Structure:**
| Tier | Target | Core Services | Add-ons | Price/User |
|------|--------|---------------|---------|------------|
| **Bronze** | SMB | Monitoring, Patching, Email Support | - | $75 |
| **Silver** | Mid-Market | Above + Help Desk, Basic Security | Backup: +$15 | $125 |
| **Gold** | Enterprise | Above + 24/7, Advanced Security, vCIO | All included | $200 |

### SLA Design and Pricing

| SLA Level | Uptime | Response Time | Price Premium |
|-----------|--------|---------------|---------------|
| Basic | 99.5% | 4 hours | Baseline |
| Standard | 99.9% | 2 hours | +15-25% |
| Premium | 99.95% | 1 hour | +40-60% |
| Mission Critical | 99.99% | 15 minutes | +100%+ |

### Add-On Services

| Service | Typical Price | Notes |
|---------|---------------|-------|
| Backup (per GB) | $0.10 - $0.30/GB/month | Cloud backup |
| Disaster Recovery | $500 - $2,000/month | Depends on RTO/RPO |
| Security Suite | $10 - $30/user/month | EDR, SIEM |
| Compliance Monitoring | $500 - $1,500/month | HIPAA, PCI, etc. |
| vCIO Services | $1,000 - $3,000/month | Strategic advisory |
| Project Work | $125 - $200/hour | Outside scope |

### Minimum Commitments

| Customer Size | Minimum Monthly |
|---------------|-----------------|
| 1-10 users | $500 - $750 |
| 11-25 users | $1,000 - $1,500 |
| 26-50 users | $2,500 - $3,000 |
| 51+ users | Per-user/device model |

---

## 2. IT Consulting Pricing

### Billing Models

#### Hourly/Time & Materials (T&M)
```
Fee = Hours Worked × Hourly Rate

Example:
- 40 hours × $175/hour = $7,000
```

**Rate Card (USD, 2024-2025):**
| Role | Hourly Rate |
|------|-------------|
| Junior Consultant | $100 - $150 |
| Consultant | $150 - $200 |
| Senior Consultant | $175 - $275 |
| Manager | $225 - $325 |
| Director | $275 - $400 |
| Partner/Principal | $350 - $600+ |

**Specialization Premium:**
| Specialization | Premium |
|----------------|---------|
| Cloud Architecture | +15-25% |
| Cybersecurity | +20-35% |
| AI/ML | +25-40% |
| SAP/Oracle | +20-30% |
| Salesforce | +15-25% |

#### Fixed-Price/Project-Based
```
Project Fee = Estimated Hours × Blended Rate × Risk Factor

Example:
- Estimated effort: 500 hours
- Blended rate: $200/hour
- Risk factor: 1.2 (moderate uncertainty)
Fee = 500 × $200 × 1.2 = $120,000
```

**Risk Factors:**
| Requirement Clarity | Risk Factor |
|---------------------|-------------|
| Highly defined | 1.0 - 1.1 |
| Mostly defined | 1.1 - 1.2 |
| Partially defined | 1.2 - 1.3 |
| Exploratory | 1.3 - 1.5 |

#### Retainer/Subscription
```
Monthly Retainer = Hours × Discounted Rate

Example:
- 40 hours/month commitment
- Standard rate: $200/hour
- Retainer discount: 15%
Monthly Fee = 40 × $200 × 0.85 = $6,800
```

**Typical Discounts:**
| Commitment | Discount |
|------------|----------|
| 20 hours/month | 5-10% |
| 40 hours/month | 10-15% |
| 80+ hours/month | 15-25% |

#### Value-Based Consulting

```
Fee = Projected Value × Capture Rate

Example:
- Annual savings identified: $2,000,000
- Capture rate: 15%
Fee = $2,000,000 × 15% = $300,000
```

### Blended Rate Calculation

```
Blended Rate = Σ (Role % × Role Rate)

Example Team Mix:
- Partner (10%): 0.10 × $500 = $50
- Manager (20%): 0.20 × $300 = $60
- Senior (40%): 0.40 × $225 = $90
- Consultant (30%): 0.30 × $150 = $45
Blended Rate = $245/hour
```

---

## 3. SaaS Pricing

### Pricing Metrics

| Metric | Best For | Examples |
|--------|----------|----------|
| Per-Seat | Productivity tools | Slack, Salesforce |
| Per-Usage | Variable consumption | AWS, Twilio |
| Per-Feature | Modular solutions | Many vertical SaaS |
| Flat Rate | Simple products | Basecamp |
| Hybrid | Complex enterprise | Most enterprise SaaS |

### Tier Structure Design

**Good-Better-Best Framework:**

| Element | Starter | Professional | Enterprise |
|---------|---------|--------------|------------|
| **Price** | $29/user/mo | $79/user/mo | Custom |
| **Target** | SMB, trial | Core market | Large accounts |
| **Users** | 1-10 | Unlimited | Unlimited |
| **Features** | Core only | Extended | All + custom |
| **Storage** | 10 GB | 100 GB | Unlimited |
| **Support** | Email | Email + chat | Phone + CSM |
| **SLA** | None | 99.5% | 99.9% |
| **SSO** | No | Yes | Yes |
| **API Access** | Limited | Full | Full + custom |

### Annual vs. Monthly Pricing

**Standard Discount Structure:**
| Payment | Discount | Effective Price |
|---------|----------|-----------------|
| Monthly | 0% | $100/month |
| Annual (pay monthly) | 10% | $90/month |
| Annual (pay upfront) | 17% (2 mo free) | $83/month equiv |
| Multi-year | 20-30% | Negotiated |

### Enterprise Pricing

**Typical Structure:**
- Base platform fee: $X,000/month or year
- Per-user/seat fee: $X per user above included
- Usage component: $X per unit above included
- Professional services: Separate SOW

**Negotiation Factors:**
| Factor | Impact on Price |
|--------|-----------------|
| Volume (users) | 5-20% discount at scale |
| Contract length | 5-10% per year |
| Early adopter | 10-20% for references |
| Strategic account | 15-30% for expansion potential |
| Payment terms | 5-10% for upfront |

### Freemium Considerations

| Metric | Target |
|--------|--------|
| Free to Paid Conversion | 2-5% |
| Feature gate impact | Clear upgrade triggers |
| Usage limits | Enough value to hook, not enough to satisfy |
| Time limits | 14-30 day trials typical |

---

## 4. System Development (Custom Software) Pricing

### Pricing Models

#### Fixed-Price Projects
```
Price = (Estimated Effort × Rate) + Contingency + Profit

Example:
- Estimated effort: 1,000 person-days
- Average rate: $800/day
- Base: $800,000
- Contingency (20%): $160,000
- Target profit (20%): $192,000
Total Price: $1,152,000
```

**Contingency by Project Type:**
| Project Type | Contingency |
|--------------|-------------|
| Similar to past project | 10-15% |
| New technology/domain | 20-25% |
| Unclear requirements | 25-35% |
| Innovation/R&D | 35-50% |

#### Time & Materials with Cap
```
Billing = MIN(Actual Hours × Rate, Cap)

Example:
- Estimate: $500,000
- Cap: $650,000 (130% of estimate)
- If actual = $550,000: Client pays $550,000
- If actual = $700,000: Client pays $650,000
```

#### Milestone-Based
```
Payment Schedule:
- Contract signing: 20%
- Requirements complete: 15%
- Design complete: 15%
- Development 50%: 20%
- UAT ready: 15%
- Go-live: 10%
- Warranty end: 5%
```

### Rate Structures

**Role-Based Rates (USD, 2024-2025):**
| Role | Onshore | Nearshore | Offshore |
|------|---------|-----------|----------|
| Project Manager | $150-200/hr | $80-120/hr | $40-70/hr |
| Architect | $175-250/hr | $100-150/hr | $50-80/hr |
| Senior Developer | $125-175/hr | $70-100/hr | $35-55/hr |
| Developer | $100-140/hr | $50-80/hr | $25-40/hr |
| QA Engineer | $80-120/hr | $45-70/hr | $20-35/hr |
| Business Analyst | $100-150/hr | $60-90/hr | $30-50/hr |

### Integration with vendor-estimate-creator

When creating pricing for system development:
1. Use vendor-estimate-creator skill for effort estimation
2. Apply appropriate rates per role
3. Add contingency based on project risk
4. Calculate profit margin
5. Structure payment milestones

---

## 5. Hardware Sales Pricing

### Margin Structures

| Product Category | Typical Margin | Notes |
|------------------|----------------|-------|
| Commodity PCs | 5-12% | Volume-driven |
| Workstations | 10-18% | Higher touch |
| Servers | 12-25% | Solution selling |
| Storage | 15-30% | High complexity |
| Networking | 15-25% | Brand varies |
| Security Appliances | 20-35% | Expertise premium |
| Peripherals | 15-25% | Convenience markup |

### Pricing Strategies

#### Cost-Plus
```
Price = Acquisition Cost × (1 + Markup %)

Example:
- Server cost: $5,000
- Target markup: 22%
Price = $5,000 × 1.22 = $6,100
```

#### Bundle Pricing
```
Bundle Price < Sum of Individual Prices

Example:
- Server: $6,000
- Configuration: $500
- Installation: $800
- 3-year support: $2,000
Individual total: $9,300
Bundle price: $8,500 (9% discount)
```

#### Solution Pricing
```
Package hardware with services:
- Hardware (low margin): $10,000 at 15%
- Services (high margin): $5,000 at 50%
Blended margin: 27%
```

### Volume Discounts

| Volume Tier | Discount |
|-------------|----------|
| 1-5 units | List price |
| 6-20 units | 5-10% |
| 21-50 units | 10-15% |
| 51-100 units | 15-20% |
| 100+ units | Negotiated |

### Lifecycle Pricing

**Recurring Revenue Opportunities:**
| Service | Pricing Model | Margin |
|---------|---------------|--------|
| Warranty Extension | Annual fee (% of HW) | 40-60% |
| Maintenance | Annual/monthly | 50-70% |
| Managed Services | Per-device/month | 40-60% |
| Refresh Cycle | Lease/subscription | Variable |

---

## 6. Cross-Service Bundling

### Bundle Strategies

**Example: Full IT Outsource Bundle**
```
Components:
1. Hardware refresh (servers, network)
2. Cloud migration services
3. Managed services contract
4. Security as a service
5. Help desk support

Pricing:
- Individual component total: $25,000/month
- Bundle price: $21,000/month (16% discount)
- Lock-in: 3-year contract
- Benefit: Predictable spend, single vendor
```

### Land and Expand

**Initial Engagement → Expansion Path:**
```
Year 1: Assessment Project ($50,000)
         ↓
Year 2: Cloud Migration ($200,000)
         ↓
Year 3: Managed Services ($15,000/month)
         ↓
Year 4: Digital Transformation ($500,000)
```

---

## 7. Geographic Considerations

### Regional Rate Differences

| Region | Rate Index | Notes |
|--------|------------|-------|
| US - NYC/SF | 1.3-1.5x | Premium markets |
| US - Average | 1.0x | Baseline |
| US - Lower cost | 0.8-0.9x | Regional markets |
| Western Europe | 0.9-1.1x | Similar to US |
| Eastern Europe | 0.4-0.6x | Nearshore option |
| India | 0.25-0.4x | Major offshore |
| Latin America | 0.5-0.7x | Nearshore, timezone aligned |

### Global Pricing Strategy

**Options:**
1. **Uniform Global**: Same USD price everywhere
2. **PPP Adjusted**: Prices reflect local purchasing power
3. **Market-Based**: Prices reflect local competitive dynamics
4. **Tiered Markets**: 2-3 price tiers based on economic development

---

## 8. Pricing Governance

### Discount Authority

| Deal Value | Max Discount | Approver |
|------------|--------------|----------|
| < $50K | 10% | Sales Rep |
| $50K - $200K | 15% | Sales Manager |
| $200K - $500K | 20% | Director |
| > $500K | 25% | VP/Executive |

### Price Exception Process

1. Sales identifies need for exception
2. Document business justification
3. Calculate impact on profitability
4. Submit to appropriate approver
5. Track exception for pattern analysis

### Annual Price Review

- Market benchmark analysis
- Cost structure changes
- Competitive positioning review
- Value delivery assessment
- Customer feedback incorporation
- Price increase communication plan

---

## Summary Tables

### Quick Reference by Service Type

| Service | Primary Model | Typical Margin | Contract Length |
|---------|---------------|----------------|-----------------|
| MSP | Per-user/device | 30-50% | 1-3 years |
| Consulting | T&M or Fixed | 35-55% | Project-based |
| SaaS | Per-seat subscription | 70-85% gross | Monthly/Annual |
| System Dev | Fixed or T&M | 20-35% | Project |
| Hardware | Cost-plus | 10-25% | One-time + support |

### Common Mistakes to Avoid

1. **MSP**: Underpricing to win, then failing to deliver
2. **Consulting**: Not including non-billable time in rates
3. **SaaS**: Too many tiers, confusing customers
4. **Development**: Underestimating scope, eating overruns
5. **Hardware**: Competing on price alone, no differentiation
