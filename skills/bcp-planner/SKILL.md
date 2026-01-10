---
name: bcp-planner
description: |
  事業継続計画（BCP）と災害復旧計画（DRP）の策定支援スキル。ビジネスインパクト分析、リスク評価、復旧戦略策定、
  BCP/DRP文書作成、テスト・訓練計画を提供。ISO 22301準拠。
  Use when developing business continuity plans, disaster recovery strategies, or conducting business impact analysis.
  Triggers: "BCP", "business continuity", "disaster recovery", "DRP", "business impact analysis", "BIA", "contingency planning".
---

# BCP Planner（事業継続計画策定支援）

## Overview

This skill transforms you into an expert business continuity planner capable of developing comprehensive BCPs and DRPs. By following ISO 22301 standards and industry best practices, you can help organizations prepare for, respond to, and recover from disruptions.

**Primary language**: Japanese (default), English supported
**Standards**: ISO 22301 (Business Continuity Management)
**Output format**: BCP/DRP documents, BIA reports, test plans, training materials

Use this skill when:
- Developing business continuity plans for organizations
- Conducting Business Impact Analysis (BIA)
- Creating disaster recovery strategies for IT systems
- Planning and conducting BCP/DRP tests and exercises
- Achieving ISO 22301 certification
- Improving organizational resilience

---

## Core Concepts

### BCP vs DRP

**BCP (Business Continuity Plan)**:
- **Scope**: Entire business operations
- **Focus**: Maintaining critical business functions during disruption
- **Includes**: People, processes, facilities, suppliers, communication
- **Objective**: Minimize business impact, maintain revenue

**DRP (Disaster Recovery Plan)**:
- **Scope**: IT systems and technology
- **Focus**: Restoring IT infrastructure and data
- **Includes**: Servers, networks, applications, data backups
- **Objective**: Restore technology operations within RTO/RPO

**Relationship**: DRP is a subset of BCP. A comprehensive BCP includes DRP as one component.

### Key Metrics

#### RTO (Recovery Time Objective)
```
Disruption → [RTO] → Service Restored

RTO = Maximum acceptable downtime

Examples:
- Tier 1 (Critical): RTO = 1 hour
- Tier 2 (Important): RTO = 8 hours
- Tier 3 (Normal): RTO = 24 hours
```

#### RPO (Recovery Point Objective)
```
Last Backup ← [RPO] → Disruption

RPO = Maximum acceptable data loss

Examples:
- RPO = 0: No data loss (synchronous replication)
- RPO = 1 hour: Hourly backups
- RPO = 24 hours: Daily backups
```

#### MTPD (Maximum Tolerable Period of Disruption)
```
MTPD = Point at which disruption becomes catastrophic

Example:
- E-commerce site: MTPD = 4 hours (beyond this, significant revenue loss and customer churn)
```

---

## Core Workflows

### Workflow 1: Business Impact Analysis (BIA)

**Purpose**: Identify critical business functions and quantify impact of disruption.

#### Step 1: Identify Business Functions

List all business functions/processes:
- **Core Functions**: Revenue-generating, mission-critical
- **Support Functions**: HR, Finance, IT, Legal
- **Management Functions**: Executive management, governance

**Example List**:
- Order Processing
- Customer Support
- Manufacturing
- Shipping/Logistics
- IT Infrastructure
- Payroll
- Financial Reporting

#### Step 2: Assess Criticality

For each function, evaluate:

**Criticality Criteria**:
1. **Revenue Impact**: How much revenue loss per hour/day?
2. **Customer Impact**: Customer satisfaction, churn risk
3. **Regulatory Impact**: Compliance violations, fines
4. **Reputational Impact**: Brand damage, media attention
5. **Operational Impact**: Dependency by other functions

**Criticality Rating**:
```
| Function | Revenue Impact | Customer Impact | Regulatory | Reputation | Overall Criticality |
|----------|----------------|-----------------|------------|------------|---------------------|
| Order Processing | Very High | High | Medium | High | **Critical** |
| Customer Support | Medium | Very High | Low | High | **High** |
| Payroll | Low | Low | High | Medium | **Medium** |
| Marketing | Low | Low | None | Low | **Low** |
```

#### Step 3: Determine Time Sensitivity

**Time Sensitivity Analysis**:

```
Impact = f(Time)

Hour 1-4: Minimal impact, workarounds possible
Hour 4-8: Moderate impact, customer frustration
Hour 8-24: Significant impact, revenue loss
Day 1-3: Severe impact, regulatory issues
Day 3+: Catastrophic, business survival threat
```

**Example**:
```
Function: Order Processing
- Hour 1: Minimal (orders queue)
- Hour 4: Moderate (customers call support)
- Hour 8: Significant ($50K revenue loss, customer complaints)
- Hour 24: Severe ($200K loss, media attention, customer churn)
- Day 3: Catastrophic (irreparable brand damage)

MTPD = 8 hours
RTO Target = 4 hours (before significant impact)
```

#### Step 4: Identify Dependencies

**Dependency Mapping**:

```
Business Function: Order Processing

Dependencies:
- People: Sales team, order fulfillment team
- Technology: E-commerce platform, payment gateway, inventory system
- Facilities: Warehouse, office space
- Suppliers: Payment processor, shipping carrier
- Data: Product catalog, customer database, inventory data
```

**Single Points of Failure (SPOF)**:
- Identify SPOFs that could disrupt critical functions
- Examples: Single server, key person, single supplier

#### Step 5: Calculate Financial Impact

**Financial Impact Formula**:
```
Total Impact = Direct Costs + Indirect Costs + Opportunity Costs

Direct Costs:
- Lost revenue
- Extra expenses (overtime, expedited shipping)
- Fines and penalties

Indirect Costs:
- Customer compensation
- Productivity loss
- Recovery costs

Opportunity Costs:
- Lost future revenue (customer churn)
- Competitive disadvantage
```

**Example**:
```
Function: E-commerce Website
Downtime: 8 hours

Direct Costs:
- Lost sales: $100,000
- Staff overtime: $5,000

Indirect Costs:
- Customer service calls: $3,000
- Brand damage mitigation: $10,000

Opportunity Costs:
- Customer churn (estimated): $50,000

Total 8-hour Impact: $168,000
Hourly Impact: $21,000/hour
```

#### Step 6: Prioritize Recovery

**Priority Matrix**:

```
       High Impact
         │
 Tier 1 │  Tier 1
(RTO:1h)│ (RTO:4h)
         │
  ───────┼───────
         │
 Tier 2 │  Tier 3
(RTO:8h)│(RTO:24h)
         │
     Low Criticality
```

---

### Workflow 2: Risk Assessment

**Purpose**: Identify threats and assess likelihood and impact.

#### Step 1: Identify Threats

**Threat Categories**:

1. **Natural Disasters**
   - Earthquake, flood, typhoon, fire
   - Pandemic

2. **Technology Failures**
   - Server failure, network outage
   - Data breach, ransomware

3. **Human-Caused**
   - Cyber attack, sabotage
   - Human error, strikes

4. **Supply Chain**
   - Supplier failure
   - Transportation disruption

5. **Facility-Related**
   - Power outage
   - HVAC failure, water damage

#### Step 2: Assess Likelihood and Impact

**Risk Assessment Matrix**:

```
Likelihood:
- Rare: Once in 10+ years
- Unlikely: Once in 5-10 years
- Possible: Once in 2-5 years
- Likely: Once per year
- Almost Certain: Multiple times per year

Impact:
- Insignificant: <$10K, <1 hour
- Minor: $10K-$100K, 1-4 hours
- Moderate: $100K-$500K, 4-24 hours
- Major: $500K-$5M, 1-7 days
- Catastrophic: >$5M, >7 days
```

**Risk Matrix**:

```
Impact     │ Rare │Unlikely│Possible│ Likely │Almost Certain
───────────┼──────┼────────┼────────┼────────┼──────────────
Catastrophic│Medium│  High  │Extreme │Extreme │   Extreme
Major      │ Low  │ Medium │  High  │Extreme │   Extreme
Moderate   │ Low  │  Low   │ Medium │  High  │   High
Minor      │ Low  │  Low   │  Low   │ Medium │   Medium
Insignif.  │ Low  │  Low   │  Low   │  Low   │   Low
```

**Example**:
```
| Threat | Likelihood | Impact | Risk Level | Mitigation Priority |
|--------|------------|--------|------------|---------------------|
| Ransomware | Likely | Major | Extreme | **Immediate** |
| Earthquake | Unlikely | Catastrophic | High | **High** |
| Power Outage | Almost Certain | Moderate | High | **High** |
| Key Person Unavailable | Possible | Minor | Low | **Medium** |
```

#### Step 3: Develop Mitigation Strategies

**Risk Treatment Options**:

1. **Avoid**: Eliminate the risk
   - Example: Move data center out of flood zone

2. **Reduce**: Minimize likelihood or impact
   - Example: Implement cybersecurity measures, backup systems

3. **Transfer**: Share risk with others
   - Example: Insurance, outsource to cloud provider

4. **Accept**: Accept the risk
   - Example: Low-likelihood, low-impact risks

**Mitigation Plan Example**:
```
Risk: Ransomware Attack
Current Level: Extreme (Likely × Major)

Mitigation Actions:
1. Implement MFA (Multi-Factor Authentication)
2. Deploy EDR (Endpoint Detection and Response)
3. Conduct security awareness training
4. Implement immutable backups (air-gapped)
5. Develop incident response plan

Residual Risk: Medium (Unlikely × Moderate)
Cost: $150,000
Expected Benefit: Avoid $5M loss
ROI: 33:1
```

---

### Workflow 3: Recovery Strategy Development

**Purpose**: Define how to recover critical functions within RTO/RPO.

#### Step 1: Recovery Strategy Options

**For IT Systems**:

1. **Hot Site** (RTO: minutes to hours)
   - Fully operational duplicate site
   - Real-time replication
   - High cost, immediate failover

2. **Warm Site** (RTO: hours to days)
   - Partially equipped site
   - Periodic data sync
   - Medium cost, moderate setup time

3. **Cold Site** (RTO: days to weeks)
   - Empty facility with infrastructure
   - No equipment pre-installed
   - Low cost, long setup time

4. **Cloud-Based DR** (RTO: hours)
   - Cloud infrastructure (AWS, Azure, GCP)
   - Pay-as-you-go
   - Scalable, cost-effective

**For Business Functions**:

1. **Alternate Work Location**
   - Remote work (VPN, collaboration tools)
   - Alternate office space
   - Co-working spaces

2. **Manual Workarounds**
   - Paper-based processes
   - Manual data entry
   - Temporary manual procedures

3. **Outsourcing**
   - Temporary staffing
   - Third-party service providers

4. **Inventory/Stockpiling**
   - Safety stock
   - Pre-positioned supplies

#### Step 2: Cost-Benefit Analysis

**Recovery Strategy Comparison**:

```
| Strategy | RTO | RPO | Setup Cost | Annual Cost | Pros | Cons |
|----------|-----|-----|------------|-------------|------|------|
| Hot Site | 1h | 0 | $500K | $200K/yr | Immediate recovery | Very expensive |
| Warm Site | 4-8h | 1h | $200K | $100K/yr | Balanced | Some downtime |
| Cold Site | 1-7d | 24h | $50K | $20K/yr | Cost-effective | Long recovery |
| Cloud DR | 2-4h | 1h | $100K | $50K/yr | Scalable, modern | Dependency on cloud |
```

**Recommendation**:
For critical systems (Tier 1), use Cloud DR or Warm Site.
For non-critical systems (Tier 3), use Cold Site or accept longer RTO.

#### Step 3: Define Recovery Procedures

**Recovery Procedure Template**:

```markdown
## Recovery Procedure: [System/Function Name]

### Objective
Restore [System/Function] to operational state within [RTO].

### Scope
- Systems: [List of servers, applications, databases]
- Data: [List of datasets and backup sources]
- Dependencies: [Prerequisites for recovery]

### Roles and Responsibilities
- **Recovery Manager**: [Name]
- **Technical Lead**: [Name]
- **Communication Lead**: [Name]

### Pre-Requisites
- [ ] Disaster declared by [Authority]
- [ ] Recovery site accessible
- [ ] Recovery team mobilized

### Recovery Steps

#### Phase 1: Assessment (0-30 minutes)
1. Assess extent of damage
2. Determine recovery strategy (primary vs. alternate site)
3. Activate recovery team

#### Phase 2: Infrastructure Recovery (30min - 2 hours)
1. Provision cloud resources OR activate alternate site
2. Restore network connectivity
3. Restore storage systems

#### Phase 3: Data Recovery (2 - 4 hours)
1. Identify most recent viable backup
2. Restore database from backup
3. Validate data integrity

#### Phase 4: Application Recovery (4 - 6 hours)
1. Deploy application servers
2. Configure applications
3. Perform smoke tests

#### Phase 5: Validation (6 - 8 hours)
1. End-to-end testing
2. User acceptance testing
3. Performance validation

#### Phase 6: Cutover (8 hours)
1. Update DNS/routing
2. Notify users
3. Monitor closely

### Rollback Plan
If recovery fails, rollback to [previous state] by [procedure].

### Checklists
- [ ] All systems operational
- [ ] Data integrity confirmed
- [ ] Users can access
- [ ] Performance acceptable
```

---

### Workflow 4: BCP/DRP Documentation

**Purpose**: Create comprehensive, actionable BCP/DRP documents.

#### BCP Document Structure

```markdown
# Business Continuity Plan

## 1. Executive Summary
- Purpose and scope
- Key risks and mitigation strategies
- Recovery priorities

## 2. Plan Governance
- Plan owner and approval authority
- Review and update schedule
- Distribution list

## 3. Business Impact Analysis
- Critical functions and RTOs
- Financial impact analysis
- Dependencies

## 4. Risk Assessment
- Threat scenarios
- Risk ratings
- Mitigation strategies

## 5. Recovery Strategies
- Recovery options for each critical function
- Cost-benefit analysis
- Chosen strategies

## 6. Emergency Response Procedures
- Incident detection and notification
- Escalation procedures
- Initial response actions

## 7. Recovery Procedures
- Step-by-step recovery instructions
- Role assignments
- Resource requirements

## 8. Communication Plan
- Internal communication (employees)
- External communication (customers, suppliers, media, regulators)
- Communication templates

## 9. Contact Lists
- Emergency contacts (24/7)
- Vendors and suppliers
- Key stakeholders

## 10. Training and Testing
- Training program
- Test schedule (tabletop, simulation, full)
- Test results and lessons learned

## 11. Plan Maintenance
- Review triggers
- Update procedures
- Version control

## Appendices
- Detailed technical recovery procedures
- Vendor contracts and SLAs
- Floor plans and facility information
- Forms and templates
```

#### DRP Document Structure

```markdown
# Disaster Recovery Plan

## 1. Introduction
- Purpose, scope, objectives
- Assumptions and constraints

## 2. Disaster Scenarios
- Natural disasters
- Technology failures
- Cyber attacks

## 3. Roles and Responsibilities
- DR Team structure
- RACI matrix

## 4. Disaster Declaration
- Criteria for declaring disaster
- Authority and approval process

## 5. Notification Procedures
- Call tree
- Notification templates
- 24/7 contact information

## 6. Recovery Priorities
- System tier classification (Tier 1, 2, 3)
- Recovery sequence

## 7. Recovery Procedures
- Infrastructure recovery
- Data recovery
- Application recovery
- Network recovery

## 8. Recovery Sites
- Primary data center
- Alternate site (Hot/Warm/Cold)
- Cloud DR environment

## 9. Data Backup and Restoration
- Backup schedule
- Backup verification
- Restoration procedures

## 10. Testing and Maintenance
- Test types and frequency
- Test scenarios
- Plan update procedures

## 11. Vendor Management
- Critical vendors and SLAs
- Escalation procedures

## Appendices
- System inventory
- Network diagrams
- Configuration details
- Backup schedules
```

---

### Workflow 5: Testing and Training

**Purpose**: Validate BCP/DRP effectiveness and train personnel.

#### Test Types

**1. Tabletop Exercise**
- **Description**: Discussion-based walkthrough
- **Participants**: Key personnel in a conference room
- **Duration**: 2-4 hours
- **Frequency**: Quarterly
- **Benefit**: Low cost, identifies gaps in plan
- **Limitation**: No actual recovery

**Example Scenario**:
```
"At 2 AM, the primary data center experiences a fire in the server room.
Initial reports indicate all servers are offline. What do you do?"

Discussion points:
- Who declares the disaster?
- How do you notify the recovery team?
- What is the recovery sequence?
- What are the communication procedures?
```

**2. Walkthrough Test**
- **Description**: Step-by-step review of procedures
- **Participants**: DR team
- **Duration**: Half day
- **Frequency**: Semi-annually
- **Benefit**: Validates procedures without disruption
- **Limitation**: No hands-on execution

**3. Simulation/Parallel Test**
- **Description**: Partial recovery in test environment
- **Participants**: Technical team
- **Duration**: 1-2 days
- **Frequency**: Annually
- **Benefit**: Hands-on validation without disrupting production
- **Limitation**: May not reflect production complexity

**4. Full Interruption Test**
- **Description**: Actual failover to DR site
- **Participants**: All stakeholders
- **Duration**: 1-3 days
- **Frequency**: Every 2-3 years (high risk)
- **Benefit**: Most realistic test
- **Limitation**: High risk, potential for production impact

#### Training Program

**Training Components**:

1. **Awareness Training** (All employees)
   - What is BCP/DRP?
   - Individual responsibilities
   - Emergency contacts
   - Frequency: Annually

2. **Role-Based Training** (DR team members)
   - Detailed recovery procedures
   - Hands-on practice
   - Frequency: Semi-annually

3. **Leadership Training** (Executives, managers)
   - Decision-making during crisis
   - Communication and media handling
   - Frequency: Annually

#### Lessons Learned Process

After each test or actual incident:

**1. Immediate Debrief** (Within 24 hours)
   - What worked?
   - What didn't work?
   - Immediate corrective actions

**2. Formal Review** (Within 1 week)
   - Root cause analysis
   - Comprehensive findings
   - Recommendations

**3. Plan Updates** (Within 1 month)
   - Incorporate lessons learned
   - Update procedures
   - Retrain as needed

---

## Deliverable Templates

### 1. Business Impact Analysis Report

```markdown
# Business Impact Analysis Report

## Executive Summary
- Scope and methodology
- Key findings
- Critical functions and RTOs
- Recommendations

## Critical Business Functions

| Function | Criticality | MTPD | RTO Target | Financial Impact (per day) |
|----------|-------------|------|------------|----------------------------|
| Order Processing | Critical | 4 hours | 2 hours | $500,000 |
| Customer Support | High | 8 hours | 4 hours | $50,000 |
| Payroll | Medium | 3 days | 24 hours | $10,000 |

## Dependencies and SPOFs
[Detailed dependency mapping]

## Recommendations
1. Implement hot site for Order Processing system
2. Enhance backup procedures to achieve RPO of 1 hour
3. Cross-train staff to eliminate key person dependencies
```

### 2. Risk Assessment Report

```markdown
# Risk Assessment Report

## Risk Register

| Risk ID | Threat | Likelihood | Impact | Risk Level | Mitigation Strategy | Residual Risk |
|---------|--------|------------|--------|------------|---------------------|---------------|
| R-001 | Ransomware | Likely | Major | Extreme | EDR, MFA, backups | Medium |
| R-002 | Data Center Fire | Unlikely | Catastrophic | High | DR site, cloud | Low |
| R-003 | Key Person Loss | Possible | Moderate | Medium | Cross-training | Low |

## High-Priority Risks
[Detailed mitigation plans for Extreme and High risks]
```

### 3. Test Report

```markdown
# BCP/DRP Test Report

## Test Overview
- **Test Type**: Simulation
- **Date**: 2025-01-15
- **Duration**: 4 hours
- **Scenario**: Ransomware attack on primary systems
- **Participants**: 12 (DR team, IT, business stakeholders)

## Test Objectives
1. Validate DR site activation procedures
2. Test data restoration from backups
3. Verify communication procedures

## Test Results
- ✅ DR site activated successfully (Target: 2 hours, Actual: 1.5 hours)
- ⚠️  Data restoration took longer than expected (Target: 4 hours, Actual: 6 hours)
- ✅ Communication procedures effective

## Issues Identified
1. Backup restoration script outdated
2. One team member unaware of role
3. Network bandwidth at DR site insufficient

## Corrective Actions
1. Update restoration scripts and test monthly
2. Conduct refresher training for all team members
3. Upgrade DR site network to 1Gbps

## Recommendation
Plan is generally effective. Address identified issues and retest in 6 months.
```

---

## Best Practices

### 1. Executive Sponsorship
BCP/DRP requires visible support from top management.

### 2. Regular Updates
Review and update plans at least annually, or after major changes.

### 3. Realistic RTOs
Set achievable RTOs based on actual recovery capabilities, not wishful thinking.

### 4. Test Regularly
Untested plans are unreliable. Test at least annually.

### 5. Keep It Simple
Plans should be clear and actionable, not overly complex.

### 6. 24/7 Accessibility
Store plans in multiple locations (cloud, physical, off-site).

### 7. Vendor Management
Ensure critical vendors have their own BCPs and understand your RTOs.

### 8. Communication is Key
Clear, timely communication during incidents is critical.

### 9. Learn and Improve
Every test and incident is an opportunity to improve the plan.

### 10. Culture of Preparedness
Embed resilience into organizational culture, not just a document.

---

## Integration with ISO 22301

ISO 22301 is the international standard for Business Continuity Management Systems (BCMS).

**Key Requirements**:
1. **Context of the Organization**: Understand internal/external issues
2. **Leadership**: Management commitment and policy
3. **Planning**: BIA, risk assessment, objectives
4. **Support**: Resources, competence, awareness, communication
5. **Operation**: Implement BC strategies and procedures
6. **Performance Evaluation**: Monitor, measure, analyze, evaluate
7. **Improvement**: Continual improvement

**Certification Process**:
- Gap analysis
- Develop BCMS documentation
- Implement processes
- Internal audit
- Management review
- External audit (Stage 1 & Stage 2)
- Certification (valid 3 years with annual surveillance)

---

このスキルの目的は、組織のレジリエンス（回復力）を高め、あらゆる中断に対して準備し、迅速に回復できる能力を構築することです。包括的なBCP/DRPを策定し、定期的にテストし、継続的に改善してください。
