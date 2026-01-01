# Internal Control Methodology Guide

## Overview

This guide provides the methodology for designing, implementing, and evaluating internal controls based on the COSO Internal Control Framework (2013) and the Three Lines of Defense model.

## COSO Internal Control Framework (2013)

### Framework Structure

The COSO framework defines internal control as:

> A process, effected by an entity's board of directors, management, and other personnel, designed to provide reasonable assurance regarding the achievement of objectives.

### Objectives Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Operations** | Effectiveness and efficiency | Productivity, asset protection |
| **Reporting** | Reliability of reporting | Financial statements, internal reports |
| **Compliance** | Adherence to laws/regulations | Regulatory requirements, policies |

### Five Components and 17 Principles

#### 1. Control Environment

| Principle | Description |
|-----------|-------------|
| 1 | Demonstrates commitment to integrity and ethical values |
| 2 | Exercises oversight responsibility |
| 3 | Establishes structure, authority, and responsibility |
| 4 | Demonstrates commitment to competence |
| 5 | Enforces accountability |

**Key Elements:**
- Code of Conduct
- Board/Audit Committee charter and oversight
- Organizational structure and reporting lines
- Job descriptions and competency requirements
- Performance evaluation and incentive systems

#### 2. Risk Assessment

| Principle | Description |
|-----------|-------------|
| 6 | Specifies suitable objectives |
| 7 | Identifies and analyzes risk |
| 8 | Assesses fraud risk |
| 9 | Identifies and analyzes significant change |

**Risk Assessment Process:**

```
┌─────────────────┐
│ Set Objectives  │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Identify Risks  │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Analyze Risks   │
│ (Likelihood ×   │
│  Impact)        │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Respond to      │
│ Risks           │
└─────────────────┘
```

**Risk Response Options:**

| Response | Description | When to Use |
|----------|-------------|-------------|
| Accept | Tolerate the risk | Low risk, cost-benefit |
| Avoid | Eliminate the activity | Unacceptable risk |
| Reduce | Implement controls | Controllable risk |
| Share | Transfer to third party | Insurable/outsourceable |

#### 3. Control Activities

| Principle | Description |
|-----------|-------------|
| 10 | Selects and develops control activities |
| 11 | Selects and develops technology controls |
| 12 | Deploys through policies and procedures |

**Control Activity Types:**

| Type | Category | Examples |
|------|----------|----------|
| Authorization | Preventive | Approval limits, delegation matrix |
| Verification | Detective | Reconciliation, exception review |
| Segregation of Duties | Preventive | Separate authorization/custody/recording |
| Physical | Preventive | Access restrictions, inventory counts |
| Performance Review | Detective | Budget variance, KPI analysis |
| Information Processing | Both | System validations, edits |

**Segregation of Duties Matrix:**

| Function | Person A | Person B | Person C |
|----------|:--------:|:--------:|:--------:|
| Authorization | ✓ | | |
| Custody | | ✓ | |
| Recording | | | ✓ |
| Reconciliation | ✓ | | |

#### 4. Information & Communication

| Principle | Description |
|-----------|-------------|
| 13 | Obtains or generates relevant, quality information |
| 14 | Internally communicates information |
| 15 | Communicates with external parties |

**Information Quality Criteria:**

| Criterion | Description |
|-----------|-------------|
| Accuracy | Correct and reliable |
| Completeness | All relevant information |
| Timeliness | Available when needed |
| Accessibility | Available to those who need it |
| Protection | Secured appropriately |

#### 5. Monitoring Activities

| Principle | Description |
|-----------|-------------|
| 16 | Conducts ongoing and/or separate evaluations |
| 17 | Evaluates and communicates deficiencies |

**Monitoring Methods:**

| Method | Frequency | Owner |
|--------|-----------|-------|
| Management Review | Ongoing | Line Management |
| Self-Assessment | Quarterly | Control Owners |
| Internal Audit | Annual | Internal Audit |
| External Audit | Annual | External Auditors |

## Three Lines of Defense Model

### Model Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    GOVERNING BODY / BOARD                      │
│              AUDIT COMMITTEE / RISK COMMITTEE                  │
├──────────────────────────────────────────────────────────────┤
│                       SENIOR MANAGEMENT                        │
├──────────────┬────────────────────────┬─────────────────────┤
│   1st LINE   │       2nd LINE         │      3rd LINE       │
│              │                        │                     │
│  Operations  │  Risk Management       │  Internal Audit     │
│  Management  │  Compliance            │                     │
│              │  Financial Control     │                     │
│              │  Quality               │                     │
│              │                        │                     │
│  - Owns and  │  - Provides expertise  │  - Provides         │
│    manages   │  - Monitors and        │    independent      │
│    risks     │    challenges          │    assurance        │
│  - Implements│  - Develops policies   │  - Reports to       │
│    controls  │  - Reports on risk     │    Audit Committee  │
└──────────────┴────────────────────────┴─────────────────────┘
                         EXTERNAL AUDIT
                    REGULATORS / STAKEHOLDERS
```

### First Line: Operational Management

**Responsibilities:**
- Day-to-day risk management
- Implementing and executing controls
- Identifying and reporting issues
- Ensuring compliance with policies

**Key Activities:**
| Activity | Description |
|----------|-------------|
| Process Execution | Perform business processes |
| Control Performance | Execute assigned controls |
| Issue Identification | Report problems to 2nd line |
| Self-Assessment | Periodic control evaluation |

### Second Line: Risk and Compliance Functions

**Responsibilities:**
- Developing risk management framework
- Providing subject matter expertise
- Monitoring and challenging first line
- Reporting on risk and control status

**Key Functions:**
| Function | Role |
|----------|------|
| Risk Management | ERM framework, risk appetite |
| Compliance | Regulatory compliance, policies |
| Financial Control | SOX/J-SOX, accounting policies |
| IT Security | Information security, cyber risk |
| Quality | Quality management, inspections |

### Third Line: Internal Audit

**Responsibilities:**
- Independent assurance on control effectiveness
- Advisory services to management
- Reporting to Audit Committee
- Coordination with external auditors

**IIA Standards Alignment:**
| Standard | Requirement |
|----------|-------------|
| Independence | Report to Audit Committee |
| Objectivity | No operational responsibility |
| Proficiency | Qualified staff |
| Due Professional Care | Appropriate attention and skill |

## Control Design Principles

### Effective Control Attributes

| Attribute | Description | Test Question |
|-----------|-------------|---------------|
| Precision | Specific to the risk | Does it address the exact risk? |
| Timeliness | Performed at right time | Is timing appropriate? |
| Authority | Proper authorization | Does performer have authority? |
| Competence | Adequate skills | Is performer qualified? |
| Evidence | Documentation exists | Is there proof of performance? |

### Control Documentation Standards

**Process Narrative Requirements:**
1. Process objectives
2. Key activities and transactions
3. Systems and applications
4. Roles and responsibilities
5. Key inputs and outputs
6. Exception handling

**Flowchart Standards:**
- Use standard symbols (BPMN or similar)
- Show decision points
- Include system interactions
- Mark control points
- Identify responsible parties

**RCM Requirements:**
- Risk identification with assertions
- Control description with attributes
- Control type and frequency
- Testing procedures
- Evidence requirements

## Control Testing Methodology

### Test Design

**Testing Objectives:**
1. **Design Effectiveness** - Is the control designed to mitigate the risk?
2. **Operating Effectiveness** - Is the control operating as designed?

### Sample Selection

**Statistical Sampling:**

| Confidence Level | Sample Size Formula |
|-----------------|---------------------|
| 90% | n = ln(1-0.90) / ln(1-p) |
| 95% | n = ln(1-0.95) / ln(1-p) |

**Practical Sample Sizes:**

| Control Frequency | Min Sample | Max Sample |
|-------------------|------------|------------|
| Annual | 1 | 1 |
| Quarterly | 2 | 2 |
| Monthly | 2 | 5 |
| Weekly | 5 | 15 |
| Daily | 25 | 40 |
| Per Transaction | 25 | 60 |

### Testing Procedures

| Procedure | Nature | Evidence |
|-----------|--------|----------|
| Inquiry | Ask about process | Interview notes |
| Observation | Watch performance | Observer notes |
| Inspection | Review documents | Copies of evidence |
| Re-performance | Execute control | Re-performance results |

### Exception Handling

| Exception Type | Response |
|----------------|----------|
| Isolated | Document, assess materiality |
| Pattern | Investigate root cause |
| Systematic | Evaluate as deficiency |

## Deficiency Evaluation Framework

### Deficiency Types

| Type | Definition |
|------|------------|
| Design Deficiency | Control not designed to prevent/detect error |
| Operating Deficiency | Control not operating as designed |

### Severity Assessment

**Evaluation Factors:**

| Factor | High Severity | Low Severity |
|--------|---------------|--------------|
| Likelihood | Reasonably possible | Remote |
| Magnitude | Material | Immaterial |
| Pervasiveness | Multiple areas | Isolated |
| Detection | Not detected by others | Compensating controls |

### Deficiency Aggregation

Consider aggregating deficiencies when:
- Common root cause
- Same process or account
- Combined impact is material
- Systemic issue indicated

## Continuous Monitoring

### Monitoring Program Design

**Components:**
1. Automated monitoring rules
2. Exception dashboards
3. Key Risk Indicators (KRIs)
4. Key Control Indicators (KCIs)

### KRI Examples

| Area | Indicator | Threshold |
|------|-----------|-----------|
| Revenue | Credit memo rate | > 2% of sales |
| Procurement | Split purchase orders | > 5% of POs |
| HR | Employee turnover | > 20% annually |
| IT | Failed login attempts | > 10 per user/day |

### Implementation Approach

| Phase | Activities |
|-------|------------|
| 1. Identify | Select processes and controls |
| 2. Design | Define monitoring rules and thresholds |
| 3. Implement | Configure monitoring tools |
| 4. Operate | Review exceptions, investigate, report |
| 5. Refine | Adjust rules based on experience |
