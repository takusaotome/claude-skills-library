# DMADV / Design for Six Sigma (DFSS)

## Introduction

DMADV (Define, Measure, Analyze, Design, Verify) is the Six Sigma methodology for designing new products, services, or processes. Also known as Design for Six Sigma (DFSS), it builds quality into the design from the beginning rather than improving an existing process.

## When to Use DMADV vs DMAIC

### Use DMADV When:
- Creating a new product, service, or process
- Current process is fundamentally broken and needs redesign
- Customer requirements have changed significantly
- No baseline exists to improve from
- Starting from a clean slate is more efficient

### Use DMAIC When:
- Improving an existing process
- Baseline performance data exists
- Process structure should be maintained
- Incremental improvement is sufficient

### Decision Guide
```
Is there an existing process?
├── No → Use DMADV
└── Yes → Can it be improved?
    ├── Yes → Use DMAIC
    └── No (too broken) → Use DMADV
```

---

## Phase 1: Define

### Purpose
Identify the project goals and customer requirements aligned with business strategy.

### Key Activities

#### 1.1 Identify Business Opportunity
- Market analysis
- Competitive landscape
- Strategic alignment
- Business case development

#### 1.2 Define Project Scope
- Project charter with goals
- Resource requirements
- Timeline and milestones
- Risk assessment

#### 1.3 Assemble Team
- Champion/sponsor
- Project leader
- Cross-functional team members
- Subject matter experts

### Key Deliverables
- Project charter
- Business case
- High-level requirements
- Stakeholder analysis
- Project plan

### Tollgate Questions
- Is there a clear business need?
- Are goals aligned with strategy?
- Is the scope well-defined?
- Are resources committed?

---

## Phase 2: Measure

### Purpose
Translate customer needs into measurable design requirements (CTQs).

### Key Activities

#### 2.1 Voice of Customer (VOC) Collection
**Methods**:
- Customer interviews
- Focus groups
- Surveys and questionnaires
- Market research
- Competitive analysis
- Complaint/feedback data
- Social media analysis

**Types of Customer Needs**:
- **Stated needs**: What customers explicitly say
- **Implied needs**: Expected but not stated
- **Latent needs**: Unrecognized desires

#### 2.2 Kano Analysis
Categorize requirements:
- **Must-be (Basic)**: Expected, dissatisfaction if missing
- **One-dimensional (Performance)**: More is better
- **Attractive (Delight)**: Unexpected positive features
- **Indifferent**: No impact on satisfaction
- **Reverse**: Causes dissatisfaction if present

#### 2.3 CTQ Development
Translate VOC to measurable specifications:

```
VOC → Need → Driver → CTQ → Target/Specification
"Fast service" → Speed → Response time → Call answered in < 30 sec
```

**CTQ Tree Structure**:
```
Customer Need (VOC)
├── Driver 1
│   ├── CTQ 1.1 (Measurable)
│   └── CTQ 1.2 (Measurable)
└── Driver 2
    ├── CTQ 2.1 (Measurable)
    └── CTQ 2.2 (Measurable)
```

#### 2.4 Competitive Benchmarking
- Identify competitors
- Compare performance on key CTQs
- Identify gaps and opportunities
- Set competitive targets

### Key Deliverables
- VOC documentation
- Kano analysis
- CTQ tree with specifications
- Competitive benchmark data
- Prioritized requirements

### Tollgate Questions
- Are customer needs thoroughly understood?
- Are CTQs measurable and specific?
- Are targets competitive?
- Are requirements prioritized?

---

## Phase 3: Analyze

### Purpose
Develop design concepts and select the best option to meet requirements.

### Key Activities

#### 3.1 Concept Generation
**Methods**:
- Brainstorming
- Benchmarking best practices
- TRIZ (Theory of Inventive Problem Solving)
- Morphological analysis
- Mind mapping

**TRIZ Principles** (Key examples):
- Segmentation: Divide into independent parts
- Taking out: Extract interfering part
- Asymmetry: Change symmetric to asymmetric
- Merging: Combine similar operations
- Universality: Make part perform multiple functions

#### 3.2 Concept Screening
**Pugh Matrix**:
1. Define evaluation criteria
2. Select baseline (datum) concept
3. Compare alternatives to baseline
4. Score: + (better), - (worse), S (same)
5. Sum scores to identify best concepts

#### 3.3 Concept Selection
**Decision Matrix**:
| Criteria | Weight | Concept A | Concept B | Concept C |
|----------|--------|-----------|-----------|-----------|
| Meets CTQ1 | 30% | 9 | 7 | 8 |
| Cost | 25% | 6 | 8 | 7 |
| Feasibility | 20% | 8 | 9 | 6 |
| Time to market | 15% | 7 | 8 | 9 |
| Risk | 10% | 8 | 7 | 5 |
| **Weighted Total** | | **7.45** | **7.75** | **7.15** |

#### 3.4 High-Level Design
- System architecture
- Functional requirements
- Technical specifications
- Interface definitions

### Key Deliverables
- Multiple design concepts
- Pugh matrix analysis
- Decision matrix with rationale
- Selected concept documentation
- High-level design specifications

### Tollgate Questions
- Were multiple concepts generated?
- Is selection criteria-based and documented?
- Does selected concept meet CTQs?
- Is high-level design feasible?

---

## Phase 4: Design

### Purpose
Develop detailed design that meets all requirements and specifications.

### Key Activities

#### 4.1 Detailed Design Development
- Technical specifications
- Process flow design
- System architecture details
- Interface specifications
- Materials and components

#### 4.2 Design FMEA
Failure Mode and Effects Analysis for design:

| Component | Failure Mode | Effect | S | Cause | O | Detection | D | RPN | Action |
|-----------|--------------|--------|---|-------|---|-----------|---|-----|--------|
| [Part] | [How it fails] | [Impact] | 1-10 | [Why] | 1-10 | [How detected] | 1-10 | S×O×D | [Mitigation] |

**Severity (S)**: Impact of failure (1=minor, 10=catastrophic)
**Occurrence (O)**: Likelihood of cause (1=rare, 10=inevitable)
**Detection (D)**: Ability to detect before customer (1=certain, 10=impossible)

Priority actions for RPN > 100 or high severity items.

#### 4.3 Design Optimization
**Methods**:
- Design of Experiments (DOE)
- Simulation and modeling
- Tolerance analysis
- Robust design (Taguchi methods)

**Robust Design Principles**:
- Design to be insensitive to variation
- Identify critical parameters
- Set optimal parameter values
- Widen tolerances where possible

#### 4.4 Design Reviews
**Review Types**:
- Preliminary Design Review (PDR)
- Critical Design Review (CDR)
- Final Design Review (FDR)

**Review Checklist**:
- Does design meet all CTQs?
- Are risks identified and mitigated?
- Is design producible/implementable?
- Are costs within budget?
- Is documentation complete?

### Key Deliverables
- Detailed design documentation
- Design FMEA
- Optimization results
- Design review approvals
- Test plan

### Tollgate Questions
- Does detailed design meet specifications?
- Are failure modes addressed?
- Is design optimized and robust?
- Have design reviews been passed?

---

## Phase 5: Verify

### Purpose
Verify that the design meets customer requirements and perform handoff.

### Key Activities

#### 5.1 Pilot/Prototype Testing
**Types of Testing**:
- Functional testing: Does it work?
- Performance testing: Does it meet specs?
- Stress testing: What are the limits?
- User acceptance testing: Do customers accept it?

**Test Plan Elements**:
- Test objectives
- Test cases mapped to CTQs
- Pass/fail criteria
- Test environment
- Resources and timeline

#### 5.2 Process Capability Studies
Verify the design can be produced consistently:
- Collect data from pilot production
- Calculate Cp, Cpk
- Compare to requirements (typically Cpk ≥ 1.33)
- Identify capability gaps

#### 5.3 Full-Scale Validation
- Scale up production/implementation
- Monitor performance
- Validate against CTQs
- Document results

#### 5.4 Implementation and Handoff
**Handoff Package**:
- Design documentation
- Process specifications
- Control plan
- Standard operating procedures
- Training materials
- Support contacts

**Training**:
- Operations/production staff
- Support/maintenance teams
- End users (if applicable)

### Key Deliverables
- Test results and analysis
- Capability study results
- Validation report
- Implementation documentation
- Training records
- Lessons learned

### Tollgate Questions
- Do test results meet requirements?
- Is process capability acceptable?
- Is full-scale validation successful?
- Is handoff complete?
- Are lessons documented?

---

## DFSS Tools Summary

### Define Phase Tools
- Project Charter
- Business Case
- Stakeholder Analysis
- Risk Assessment

### Measure Phase Tools
- VOC Collection Methods
- Kano Analysis
- CTQ Tree / QFD
- Benchmarking

### Analyze Phase Tools
- Brainstorming / TRIZ
- Pugh Matrix
- Decision Matrix
- Concept Modeling

### Design Phase Tools
- Design FMEA
- DOE
- Simulation
- Tolerance Analysis
- Design Reviews

### Verify Phase Tools
- Test Planning
- Pilot Testing
- Capability Studies
- Validation Protocols

---

## Quality Function Deployment (QFD)

Also known as "House of Quality," QFD is a structured approach to translate customer requirements into technical specifications.

### House of Quality Structure

```
         ┌─────────────┐
         │ Correlation │ ← Technical requirement relationships
         │   Matrix    │
┌────────┼─────────────┼────────┐
│Customer│ Relationship│ Compet.│
│ Needs  │   Matrix    │Analysis│
│ (WHATs)│ (HOW/WHAT)  │        │
├────────┼─────────────┼────────┤
│Weights │  Technical  │Targets │
│        │Requirements │        │
│        │  (HOWs)     │        │
└────────┴─────────────┴────────┘
```

### QFD Process
1. Identify customer needs (WHATs)
2. Prioritize needs (importance weights)
3. Develop technical requirements (HOWs)
4. Relate HOWs to WHATs (relationship matrix)
5. Identify correlations between HOWs
6. Benchmark competition
7. Set technical targets

---

## DMADV vs Other DFSS Methodologies

Several DFSS variations exist:

| Methodology | Phases | Focus |
|-------------|--------|-------|
| **DMADV** | Define, Measure, Analyze, Design, Verify | General new design |
| **IDOV** | Identify, Design, Optimize, Verify | Technology/product design |
| **DCCDI** | Define, Customer, Concept, Design, Implement | Customer-centric design |

All share common principles:
- Start with customer requirements
- Develop multiple concepts
- Make data-driven decisions
- Build quality into design
- Verify before launch

---

## Integration with Product Development

DMADV can integrate with existing product development processes:

### Stage-Gate Integration
| Stage-Gate | DMADV Phase |
|------------|-------------|
| Scoping | Define |
| Build Business Case | Define/Measure |
| Development | Analyze/Design |
| Testing & Validation | Verify |
| Launch | Verify (handoff) |

### Agile Integration
- Use DMADV phases as epic structure
- Break Design phase into sprints
- Apply iterative prototyping in Analyze/Design
- Use continuous verification in Verify
