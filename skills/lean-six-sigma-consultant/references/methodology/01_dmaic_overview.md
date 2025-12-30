# DMAIC Methodology Overview

## Introduction

DMAIC (Define, Measure, Analyze, Improve, Control) is the core problem-solving methodology of Six Sigma. It provides a structured, data-driven approach to improving existing processes by reducing variation and eliminating defects.

## When to Use DMAIC

Use DMAIC when:
- An existing process is not meeting performance requirements
- Root cause of problems is unknown
- Data-driven improvement is needed
- Sustainable improvement is the goal

Do NOT use DMAIC when:
- No process exists (use DMADV instead)
- Quick fix is possible without deep analysis
- Problem is simple and obvious
- Process needs complete redesign

---

## Phase 1: Define

### Purpose
Clearly articulate the problem, establish project scope, and align stakeholders.

### Key Objectives
- Define the problem with specificity
- Quantify the business impact
- Establish SMART goals
- Identify project boundaries
- Assemble the team
- Gain stakeholder buy-in

### Key Questions to Answer
1. What is the problem? (Specific, measurable)
2. Why is it important? (Business case)
3. What is the scope? (Boundaries)
4. What is the goal? (Target)
5. Who are the stakeholders?
6. What resources are needed?

### Key Deliverables

#### Project Charter
Essential elements:
- **Problem Statement**: Specific description of what, when, where, extent
- **Business Case**: Financial and strategic justification
- **Goal Statement**: SMART format (Specific, Measurable, Achievable, Relevant, Time-bound)
- **Scope**: In-scope and out-of-scope boundaries
- **Team**: Champion, process owner, team leader, members
- **Timeline**: High-level milestones

#### SIPOC Diagram
High-level process view showing:
- **Suppliers**: Who provides inputs
- **Inputs**: Materials, information, resources
- **Process**: 5-7 major steps
- **Outputs**: Deliverables
- **Customers**: Recipients of outputs

#### Voice of Customer (VOC)
Methods to capture:
- Interviews
- Surveys
- Complaint data
- Focus groups
- Market research

#### CTQ Tree
Translation from customer voice to measurable requirements:
```
Customer Need → Driver → CTQ (Measurable Specification)
```

### Tollgate Checklist
- [ ] Problem statement is specific and quantified
- [ ] Business case shows significant impact
- [ ] Goals are SMART
- [ ] Scope is appropriate (not too broad/narrow)
- [ ] Team is assembled with necessary skills
- [ ] Champion is engaged
- [ ] Stakeholders are identified

---

## Phase 2: Measure

### Purpose
Establish baseline performance and validate the measurement system.

### Key Objectives
- Define what to measure
- Validate measurement system
- Collect baseline data
- Understand current process performance
- Identify potential causes (Xs)

### Key Questions to Answer
1. How do we measure the problem?
2. Is our measurement system reliable?
3. What is current performance?
4. What is the process capability?
5. What are potential input variables?

### Key Deliverables

#### Data Collection Plan
Components:
- **Operational definitions**: Clear, unambiguous definitions
- **Data type**: Continuous or discrete
- **Sample size**: Statistically adequate
- **Sampling frequency**: How often
- **Stratification**: By shift, machine, operator, etc.
- **Responsibility**: Who collects

#### Measurement System Analysis (MSA)
Validates measurement reliability:
- **Gage R&R**: Repeatability and reproducibility study
- **Accuracy**: Comparison to known standard
- **Stability**: Consistency over time
- **Linearity**: Accuracy across measurement range

Acceptance criteria:
- Gage R&R < 10%: Excellent
- Gage R&R 10-30%: Acceptable
- Gage R&R > 30%: Unacceptable

#### Detailed Process Map
Types:
- Flowchart with decision points
- Swim lane diagram showing responsibilities
- Value stream map showing flow and timing

Include:
- All process steps
- Decision points
- Rework loops
- Wait times
- Handoffs

#### Baseline Metrics
Primary metric (Y):
- Current value
- Target value
- Entitlement (best possible)

Calculate:
- **DPMO**: Defects per million opportunities
- **Sigma Level**: Process performance
- **Process Capability**: Cp, Cpk if applicable

### Tollgate Checklist
- [ ] Measurement system validated
- [ ] Baseline data collected
- [ ] Process mapped in detail
- [ ] Baseline metrics calculated
- [ ] Potential Xs identified
- [ ] Data is stratified for analysis

---

## Phase 3: Analyze

### Purpose
Identify and verify root causes of the problem.

### Key Objectives
- Generate potential causes
- Narrow down to vital few
- Verify causes with data
- Understand cause-effect relationships

### Key Questions to Answer
1. What are potential causes?
2. Which are the vital few?
3. Is there data evidence?
4. What is the relationship?
5. Why does the problem occur?

### Key Deliverables

#### Cause Analysis
Tools:
- **Fishbone (Ishikawa) Diagram**: Organize causes into 6M categories
- **5 Whys**: Drill down to root cause
- **Fault Tree Analysis**: Logic diagram of failures

#### Data Analysis
Tools based on data type:

**Graphical Analysis**:
- Pareto chart: Prioritize categories
- Scatter plot: Visualize relationships
- Box plot: Compare groups
- Histogram: Distribution shape

**Statistical Analysis**:
- Hypothesis testing: Verify differences
- Correlation: Measure relationships
- Regression: Model relationships
- ANOVA: Compare multiple groups

#### Verified Root Causes
For each verified cause, document:
- The cause statement
- Data evidence
- Statistical significance (if applicable)
- Impact on the problem

### Tollgate Checklist
- [ ] Multiple potential causes generated
- [ ] Causes prioritized to vital few
- [ ] Data evidence supports causes
- [ ] Statistical verification completed
- [ ] Root cause can be clearly explained
- [ ] Team agrees on verified causes

---

## Phase 4: Improve

### Purpose
Develop, test, and implement solutions that address root causes.

### Key Objectives
- Generate solution ideas
- Select best solutions
- Pilot test solutions
- Implement at full scale
- Verify improvement

### Key Questions to Answer
1. What solutions address root causes?
2. Which solution is best?
3. What are the risks?
4. How do we test it?
5. Did it work?

### Key Deliverables

#### Solution Generation
Methods:
- Brainstorming
- Benchmarking
- TRIZ (inventive problem solving)
- Process redesign

#### Solution Selection
Tools:
- **Criteria-based matrix**: Weighted scoring
- **Pugh Matrix**: Concept comparison
- **Impact/Effort Matrix**: Prioritization

Selection criteria:
- Effectiveness at addressing root cause
- Feasibility of implementation
- Cost
- Risk
- Speed
- Sustainability

#### Risk Assessment (FMEA)
Failure Mode and Effects Analysis:
- Identify potential failure modes
- Assess severity, occurrence, detection
- Calculate RPN (Risk Priority Number)
- Develop mitigation actions

#### Pilot Plan
Elements:
- Scope of pilot
- Duration
- Success criteria
- Data collection
- Contingency plan

#### Implementation Plan
Elements:
- Tasks and timeline
- Resources required
- Training needs
- Communication plan
- Change management

### Tollgate Checklist
- [ ] Solutions address verified root causes
- [ ] Selection criteria documented
- [ ] Risks assessed and mitigated
- [ ] Pilot completed successfully
- [ ] Improvement verified with data
- [ ] Implementation plan ready

---

## Phase 5: Control

### Purpose
Sustain the improvements and prevent regression.

### Key Objectives
- Standardize the improved process
- Implement monitoring systems
- Document and train
- Hand off to process owner
- Close project

### Key Questions to Answer
1. How do we maintain gains?
2. How do we detect problems?
3. What do we do if problems occur?
4. Who is responsible ongoing?
5. Is the project complete?

### Key Deliverables

#### Control Plan
Components:
- Process step/parameter to control
- Specification/target
- Measurement method
- Sample size and frequency
- Control method (chart type)
- Reaction plan
- Responsible person

#### Statistical Process Control (SPC)
- Select appropriate control chart
- Calculate control limits
- Train operators on interpretation
- Define out-of-control rules
- Establish response procedures

#### Standard Work
Documentation:
- Work instructions
- Visual aids
- Training materials
- Checklists

#### Process Owner Handoff
Transfer package:
- Updated process documentation
- Control plan
- Control chart templates
- Response procedures
- Training records
- Project summary

### Tollgate Checklist
- [ ] Control plan implemented
- [ ] Control charts in use
- [ ] Standard work documented
- [ ] Training completed
- [ ] Process owner accepts ownership
- [ ] Results meet goals
- [ ] Project documentation complete

---

## DMAIC Timeline Guidelines

Typical project durations:

| Project Complexity | Duration |
|-------------------|----------|
| Simple (Green Belt) | 2-3 months |
| Moderate (Green Belt) | 3-4 months |
| Complex (Black Belt) | 4-6 months |
| Very Complex (Black Belt) | 6-12 months |

Phase time allocation (approximate):
- Define: 10-15%
- Measure: 20-25%
- Analyze: 20-25%
- Improve: 25-30%
- Control: 15-20%

---

## Success Factors

### Critical Success Factors
1. **Clear problem definition**: Invest time in Define
2. **Strong sponsorship**: Engaged champion
3. **Data-driven approach**: Decisions based on data
4. **Cross-functional team**: Right expertise
5. **Realistic scope**: Achievable in timeframe
6. **Sustained control**: Don't skip Control phase

### Common Failure Modes
1. Jumping to solutions without analysis
2. Scope too broad
3. Poor data quality
4. Lack of management support
5. Ignoring change management
6. Weak control phase

---

## Integration with Lean

DMAIC can incorporate Lean tools:
- Use Value Stream Mapping in Measure/Analyze
- Apply 5S in Improve
- Implement Kanban in Improve/Control
- Use Kaizen events within DMAIC phases
- Apply waste elimination throughout

The combination (Lean Six Sigma) leverages:
- Lean's speed and waste focus
- Six Sigma's rigor and variation focus
