# Lean Six Sigma in Services and Transactional Processes

## Overview

Applying Lean Six Sigma to services requires adaptation from manufacturing origins. Service processes are often invisible, variable by nature, and heavily dependent on human interaction. This guide covers best practices for transactional and service environments.

## Key Differences from Manufacturing

| Aspect | Manufacturing | Services |
|--------|--------------|----------|
| Product | Tangible | Intangible |
| Inventory | Physical goods | Information/queues |
| Defects | Visible, measurable | Often hidden |
| Cycle Time | Consistent | Highly variable |
| Customer Contact | Low during production | Often high throughout |
| Process Visibility | Observable | Often invisible |
| Standardization | High | Low to moderate |

## Service Quality Metrics

### Accuracy Metrics

**Transaction Accuracy Rate**:
```
Accuracy = (Error-free transactions / Total transactions) × 100
```

**Error Categories**:
- Data entry errors
- Missing information
- Incorrect processing
- Late delivery
- Communication errors

**Typical Targets**:
| Process Type | Accuracy Target |
|--------------|-----------------|
| Data entry | 99.5-99.9% |
| Order processing | 99.0-99.5% |
| Financial transactions | 99.9%+ |
| Customer service | 95-99% |

### Speed Metrics

**Cycle Time**: Total time from request to completion

**Processing Time**: Actual work time (value-add)

**Wait Time**: Time in queues between steps

**Touch Time**: Time actually working on item

**Efficiency Ratio**:
```
Efficiency = Processing Time / Cycle Time × 100
```

**Typical Service Efficiency**: 1-10% (vs. 20-40% in manufacturing)

### Customer Satisfaction Metrics

**Net Promoter Score (NPS)**:
- Promoters (9-10): Would recommend
- Passives (7-8): Satisfied but vulnerable
- Detractors (0-6): Unhappy customers

```
NPS = % Promoters - % Detractors
```

**Customer Effort Score (CES)**:
How easy was it to get your issue resolved? (1-7 scale)

**First Contact Resolution (FCR)**:
```
FCR = Issues resolved on first contact / Total issues × 100
```

### Service Level Metrics

**Service Level Agreement (SLA) Compliance**:
```
SLA Compliance = (Transactions within SLA / Total transactions) × 100
```

**Common SLA Dimensions**:
- Response time
- Resolution time
- Availability
- Error rate

## Service-Specific Tools

### Service Blueprinting

**Elements**:
1. **Physical Evidence**: Tangibles customer sees
2. **Customer Actions**: What customer does
3. **Onstage Actions**: Visible employee actions
4. **Backstage Actions**: Invisible support activities
5. **Support Processes**: Systems and processes

**Key Lines**:
- Line of Interaction: Between customer and onstage
- Line of Visibility: Between onstage and backstage
- Line of Internal Interaction: Between backstage and support

### Swim Lane Process Maps

**Format**: Horizontal lanes for each role/department

**Benefits**:
- Shows handoffs clearly
- Identifies ownership
- Reveals wait times
- Highlights complexity

**Elements per Lane**:
- Process steps (rectangles)
- Decisions (diamonds)
- Delays (D symbol)
- Documents (rectangle with wavy bottom)

### Transaction Sampling

**Challenges**:
- No physical product to inspect
- Transactions vary in complexity
- Data often in multiple systems

**Approaches**:
1. **Random sampling**: For baseline
2. **Stratified sampling**: By type, source, processor
3. **Time-based sampling**: Capture all in a period
4. **Error-focused**: Review all errors

**Sample Size Considerations**:
- Larger samples for lower error rates
- Include all transaction types
- Cover all time periods
- Include all processors

## Service Value Stream Mapping

### Key Differences

**What Flows**: Information, work items, requests

**Inventory Symbol**: Queue/backlog of work items

**Process Time**: Often estimated or measured via sampling

**Wait Time**: Time in queue between steps

### Service VSM Metrics

| Metric | Description |
|--------|-------------|
| Processing Time | Time actually working |
| Queue Time | Time waiting |
| Lead Time | Total time in system |
| %C&A | Percent Complete and Accurate |
| Rework % | Percent requiring rework |
| Batch Size | Items processed together |
| Queue Size | Items waiting |

### %Complete and Accurate (%C&A)

**Definition**: Percent of work received that is complete and accurate (no rework needed)

**Calculation**:
```
%C&A = Work received without defects / Total work received × 100
```

**Rolled %C&A**: Product of %C&A at each step
```
Rolled %C&A = %C&A₁ × %C&A₂ × %C&A₃ × ... × %C&Aₙ
```

## Common Service Projects

### Processing Time Reduction

**Typical Approach**:
1. **Define**: Current vs. target processing time
2. **Measure**: Time studies, queue analysis
3. **Analyze**: Value-add vs. non-value-add
4. **Improve**: Eliminate waste, automate, parallel process
5. **Control**: Standard work, visual management

**Sources of Delay**:
- Waiting for information
- Multiple approvals
- Batch processing
- System limitations
- Unclear requirements

### Error Reduction

**Approach**:
1. **Define**: Error types, rates, impact
2. **Measure**: Error tracking, sampling
3. **Analyze**: Root cause by error type
4. **Improve**: Error-proofing, training, systems
5. **Control**: Verification steps, audits

**Error-Proofing Techniques**:
- Required fields
- Drop-down lists
- Validation rules
- Checklists
- Verification steps
- System alerts

### Customer Complaint Reduction

**Approach**:
1. **Define**: Pareto of complaint types
2. **Measure**: Complaint rates, CSAT scores
3. **Analyze**: Root cause by complaint type
4. **Improve**: Process redesign, training
5. **Control**: Monitoring, rapid response

**Voice of Customer Methods**:
- Surveys (transactional, relationship)
- Focus groups
- Customer interviews
- Social media monitoring
- Complaint analysis
- Lost customer analysis

## Service Eight Wastes (DOWNTIME)

| Waste | Service Examples |
|-------|------------------|
| **D**efects | Errors, rework, corrections |
| **O**verproduction | Reports no one reads, unnecessary approvals |
| **W**aiting | Queue time, waiting for information |
| **N**on-utilized talent | Overqualified workers on simple tasks |
| **T**ransportation | Unnecessary handoffs, routing |
| **I**nventory | Backlogs, pending work, emails |
| **M**otion | Searching for files, switching systems |
| **E**xtra-processing | Redundant data entry, over-checking |

## Service-Specific Considerations

### Data Collection Challenges

**Problems**:
- Transactions not tracked
- Multiple systems involved
- Manual processes
- Inconsistent coding
- Incomplete records

**Solutions**:
- Temporary tracking sheets
- System queries/reports
- Sampling studies
- Time observation studies
- Email/ticket analysis

### Measurement System Analysis

**Service MSA Focus**:
- Consistency of coding/classification
- Attribute agreement analysis
- Evaluator agreement (for subjective measures)

**Attribute Agreement Analysis**:
- Multiple evaluators
- Same items, evaluated independently
- Compare to known correct answer (if available)
- Calculate agreement % and Kappa

### Process Variation

**Sources in Services**:
- Different customer requirements
- Different complexity levels
- Different processors/styles
- Interruptions
- Time of day/week effects

**Approaches**:
- Standardize where possible
- Classify transaction types
- Analyze separately then combine
- Account for complexity

## Best Practices for Service LSS

### Project Selection

1. **High-volume, repetitive processes**: Better for statistical analysis
2. **Customer-impacting**: Clear business case
3. **Measurable**: Can track before/after
4. **Controllable**: Within team's influence
5. **Bounded scope**: Clear start and end

### Team Composition

- Process workers (do the work)
- Process experts (know the exceptions)
- IT representative (system changes)
- Customer-facing representative
- Support function representatives

### Data-Driven Approach

**Even in Services**:
- Measure before improving
- Use data to identify root causes
- Pilot with measurement
- Verify results with data

**When Data is Limited**:
- Start collecting immediately
- Use sampling
- Estimate with validation
- Combine quantitative and qualitative

### Change Management

**Service environments often require more**:
- Communication (many people involved)
- Training (behavior change needed)
- Reinforcement (habits are strong)
- Leadership support (visible commitment)

## Technology Integration

### Robotic Process Automation (RPA)

**Good Candidates**:
- High volume
- Rule-based
- Stable process
- Structured data

**Caution**:
- Automate good processes only
- "Paving the cow path" risk
- Maintenance requirements

### Workflow Systems

**Benefits**:
- Automatic routing
- Status visibility
- Queue management
- Performance tracking
- SLA monitoring

**Lean Six Sigma + Workflow**:
1. Improve process first
2. Then automate/systematize
3. Avoid automating waste

## Service Industry Examples

### Financial Services

**Common Projects**:
- Loan processing time
- Error reduction in transactions
- Customer onboarding
- Claims processing
- Account maintenance accuracy

### Healthcare (Administrative)

**Common Projects**:
- Patient registration
- Insurance verification
- Billing accuracy
- Appointment scheduling
- Medical records processing

### Call Centers

**Common Projects**:
- First call resolution
- Average handle time
- Customer satisfaction
- Agent productivity
- Escalation reduction

### Human Resources

**Common Projects**:
- Time to hire
- Onboarding process
- Payroll accuracy
- Benefits enrollment
- Performance review cycle

## Common Pitfalls

### Underestimating Variation

Service processes naturally vary more than manufacturing. Account for this in:
- Sample sizes
- Control limits
- Improvement targets
- Measurement systems

### Ignoring the Human Element

Services are people-intensive. Success requires:
- Buy-in from workers
- Addressing concerns
- Training and support
- Recognition and rewards

### Over-Standardizing

Balance standardization with flexibility:
- Standardize routine work
- Allow judgment for exceptions
- Empower workers to solve problems
- Maintain customer focus

### Measuring the Wrong Things

Ensure metrics:
- Matter to customers
- Drive right behaviors
- Can be acted upon
- Are worth the measurement cost
