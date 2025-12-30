---
name: lean-six-sigma-consultant
description: Comprehensive Lean Six Sigma consulting skill supporting all belt levels (White Belt to Master Black Belt). Use this skill for DMAIC/DMADV project execution, Lean waste elimination (VSM, 8 Wastes/DOWNTIME, 5S), statistical analysis (process capability Cp/Cpk, control charts, hypothesis testing), and Six Sigma training/education. Triggers include "improve process", "reduce defects", "sigma level", "DMAIC project", "value stream mapping", "Kaizen", "process capability", "control chart", "root cause analysis", "5 Whys", "Fishbone diagram", "FMEA", "DOE", or requests involving process improvement methodologies.
---

# Lean Six Sigma Consultant

## Overview

This skill provides comprehensive Lean Six Sigma consulting capabilities, integrating the waste elimination focus of Lean with the variation reduction rigor of Six Sigma. It supports practitioners at all belt levels from awareness (White Belt) through strategic deployment (Master Black Belt).

**Primary Language**: Japanese (default), English supported
**Knowledge Base**: 33 reference files covering methodology, tools, statistics, industries, and training
**Output Format**: Project guidance, analysis reports, templates, training materials

### The Integration of Lean and Six Sigma

**Six Sigma** focuses on reducing process variation and defects using statistical methods (DMAIC methodology). The goal is achieving 3.4 defects per million opportunities (6 sigma level).

**Lean** focuses on eliminating waste and improving flow using Toyota Production System principles. The goal is maximizing customer value while minimizing waste.

**Lean Six Sigma** combines both:
- Use **Lean tools** to identify and eliminate waste, improve flow
- Use **Six Sigma tools** to reduce variation, solve complex problems
- Use **DMAIC** as the overarching improvement framework

## When to Use This Skill

Use this skill when:

**Project Execution**:
- Leading or supporting a process improvement project
- Need guidance on which DMAIC phase tools to use
- Want to reduce defects, errors, or variation in a process
- Need to eliminate waste and improve cycle time
- Implementing statistical process control

**Analysis Support**:
- Conducting root cause analysis (5 Whys, Fishbone)
- Calculating process capability (Cp, Cpk)
- Creating or interpreting control charts
- Performing hypothesis testing or regression analysis
- Analyzing value streams for waste

**Training/Education**:
- Learning Six Sigma methodology and tools
- Preparing for belt certification exams
- Understanding statistical concepts
- Teaching Six Sigma to team members

### Example Requests

1. "I want to reduce the defect rate in our manufacturing line. Guide me through a DMAIC project."
2. "Create a SIPOC diagram for our order fulfillment process."
3. "Calculate the process capability (Cpk) for this data: USL=10.5, LSL=9.5, mean=10.02, std=0.15"
4. "Help me identify the 8 wastes in our customer service process."
5. "What control chart should I use for tracking defect count per batch?"
6. "Explain the difference between Cp and Cpk for my Green Belt exam."
7. "Conduct a root cause analysis using the Fishbone diagram for high customer complaints."

---

## Lean Six Sigma Framework

### DMAIC Overview

DMAIC is the core improvement methodology for existing processes:

| Phase | Purpose | Key Questions | Key Deliverables |
|-------|---------|---------------|------------------|
| **Define** | Clarify the problem and project scope | What is the problem? Who is affected? What is the goal? | Project Charter, SIPOC, VOC/CTQ |
| **Measure** | Establish baseline and data collection | How is the process performing now? How do we measure it? | Data Collection Plan, Baseline Metrics, Process Map |
| **Analyze** | Identify root causes | Why is the problem occurring? What are the vital few causes? | Root Cause Analysis, Statistical Analysis |
| **Improve** | Develop and implement solutions | What solutions address root causes? How do we implement? | Solution Selection, Pilot Results, Implementation Plan |
| **Control** | Sustain the improvements | How do we maintain gains? How do we monitor? | Control Plan, Control Charts, Standard Work |

### DMADV Overview (Design for Six Sigma)

DMADV is used for designing new processes or products:

| Phase | Purpose | Key Deliverables |
|-------|---------|------------------|
| **Define** | Define project goals aligned with customer needs | Project Charter, Business Case |
| **Measure** | Measure customer needs and specifications | VOC, CTQ, Competitive Analysis |
| **Analyze** | Analyze design options | Concept Generation, Pugh Matrix |
| **Design** | Design the process/product in detail | Detailed Design, FMEA, Simulations |
| **Verify** | Verify design meets requirements | Pilot Testing, Validation, Handoff |

### Belt Hierarchy and Competencies

| Belt Level | Role | Time on Six Sigma | Key Competencies |
|------------|------|-------------------|------------------|
| **White Belt** | Awareness | Ad-hoc | Basic concepts, waste identification |
| **Yellow Belt** | Team member | 10-25% | Simple tools, data collection support |
| **Green Belt** | Project leader | 25-50% | DMAIC execution, basic statistics |
| **Black Belt** | Expert leader | 50-100% | Advanced statistics, complex projects |
| **Master Black Belt** | Strategic leader | 100% | Program deployment, training, mentoring |

---

## Core Workflow 1: DMAIC Project Execution

Use this workflow when improving an existing process.

### Step 1: Define Phase

**Objective**: Clearly define the problem, scope, and goals.

#### 1.1 Create Project Charter

Load `assets/project_charter_template.md` and complete:

**Business Case**: Why is this project important?
- Financial impact (cost of poor quality, revenue loss)
- Customer impact (complaints, satisfaction scores)
- Strategic alignment

**Problem Statement** (Specific, factual, quantified):
- **What**: What is wrong or not performing?
- **When**: When does it occur?
- **Where**: Where does it occur?
- **Extent**: How big is the problem? (Quantify)

**Goal Statement** (SMART):
- **Specific**: What will be achieved?
- **Measurable**: What is the target metric?
- **Achievable**: Is the target realistic?
- **Relevant**: Does it align with business objectives?
- **Time-bound**: When will it be achieved?

**Scope**:
- In scope: Process boundaries, included areas
- Out of scope: Excluded areas, constraints

**Team**:
- Champion: Executive sponsor
- Process Owner: Accountable for process
- Team Leader: Belt leading the project
- Team Members: Subject matter experts

#### 1.2 Create SIPOC Diagram

Load `references/tools-by-phase/define/sipoc_guide.md` and `assets/sipoc_template.md`.

SIPOC provides high-level process view:
- **S**uppliers: Who provides inputs?
- **I**nputs: What materials, information, resources?
- **P**rocess: 5-7 high-level steps
- **O**utputs: What does the process produce?
- **C**ustomers: Who receives outputs?

#### 1.3 Capture Voice of Customer (VOC) and CTQs

Load `references/tools-by-phase/define/voc_ctq_guide.md`.

**VOC Collection Methods**:
- Customer interviews
- Surveys
- Complaint data analysis
- Focus groups
- Social media analysis

**CTQ (Critical to Quality) Tree**:
```
Customer Need → Driver → CTQ (Measurable)
"Fast delivery" → "Delivery time" → "95% orders delivered within 2 days"
```

#### 1.4 Define Phase Tollgate Questions

Before moving to Measure:
- [ ] Is the problem clearly defined and quantified?
- [ ] Is the project scope appropriate (not too big/small)?
- [ ] Are the goals SMART and achievable?
- [ ] Is the team assembled with right skills?
- [ ] Is champion engaged and supportive?
- [ ] Are baseline metrics identified?

---

### Step 2: Measure Phase

**Objective**: Establish baseline performance and data collection system.

#### 2.1 Develop Data Collection Plan

Load `references/tools-by-phase/measure/data_collection_plan.md`.

**Operational Definitions**: Clear, unambiguous definitions
- What exactly is a "defect"?
- How is cycle time measured (start/end points)?
- What units? What precision?

**Data Types**:
- **Continuous**: Measured on a scale (time, weight, temperature)
- **Discrete/Attribute**: Counted (defects, errors, pass/fail)

**Sampling Strategy**:
- **Sample size**: Use statistical calculations or rules of thumb
- **Frequency**: How often to collect
- **Stratification**: Collect by shift, machine, operator to enable analysis

#### 2.2 Validate Measurement System (MSA)

Load `references/tools-by-phase/measure/msa_guide.md`.

Before collecting data, validate the measurement system:
- **Gage R&R** (Repeatability & Reproducibility): Is measurement variation acceptable?
- **Accuracy**: Does the measurement match the true value?
- **Stability**: Is measurement consistent over time?

**Acceptance Criteria**:
- Gage R&R < 10%: Excellent
- Gage R&R 10-30%: Acceptable with caution
- Gage R&R > 30%: Unacceptable, fix measurement system first

#### 2.3 Create Detailed Process Map

Map the process in detail:
- **Swim lane diagram**: Show handoffs between departments
- **Value-added analysis**: Mark each step as VA, NVA, or BNVA
- **Cycle time**: Record time for each step
- **Identify pain points**: Bottlenecks, rework loops, wait times

#### 2.4 Establish Baseline Metrics

Load `references/tools-by-phase/measure/baseline_metrics.md`.

**Primary Metric (Y)**: The main output measure
- Baseline value: Current performance
- Target: Goal to achieve
- Entitlement: Best possible (benchmark)

**Sigma Level Calculation**:
```
DPMO = (Defects / (Units × Opportunities)) × 1,000,000
Sigma Level = Look up in conversion table or calculate
```

| Sigma Level | DPMO | Yield |
|-------------|------|-------|
| 2σ | 308,538 | 69.1% |
| 3σ | 66,807 | 93.3% |
| 4σ | 6,210 | 99.38% |
| 5σ | 233 | 99.977% |
| 6σ | 3.4 | 99.99966% |

#### 2.5 Measure Phase Tollgate Questions

Before moving to Analyze:
- [ ] Is the measurement system validated (MSA)?
- [ ] Is baseline data collected and reliable?
- [ ] Is the process mapped in sufficient detail?
- [ ] Is the sigma level or capability calculated?
- [ ] Are key process inputs (Xs) identified?

---

### Step 3: Analyze Phase

**Objective**: Identify and verify root causes.

#### 3.1 Generate Potential Causes

Load `references/tools-by-phase/analyze/root_cause_analysis.md`.

**Fishbone (Ishikawa) Diagram**:
Organize potential causes into 6 categories (6M):
- **Man** (People): Skills, training, fatigue
- **Machine** (Equipment): Age, maintenance, calibration
- **Material**: Quality, specifications, suppliers
- **Method**: Procedures, work instructions
- **Measurement**: Accuracy, calibration
- **Mother Nature** (Environment): Temperature, humidity, lighting

**5 Whys Analysis**:
Ask "Why?" repeatedly to drill down to root cause:
```
Problem: Machine stopped
Why 1: Overloaded → Why 2: Bearing failed → Why 3: Insufficient lubrication
→ Why 4: No PM schedule → Why 5: No maintenance program
Root Cause: Lack of preventive maintenance program
```

#### 3.2 Prioritize with Pareto Analysis

Load `references/tools-by-phase/analyze/pareto_analysis.md`.

**Pareto Principle**: 80% of effects come from 20% of causes

**Steps**:
1. Categorize defects/problems
2. Count frequency of each category
3. Sort in descending order
4. Calculate cumulative percentage
5. Identify the "vital few" (typically top 20% of categories causing 80% of problems)

#### 3.3 Verify Causes with Data

Load `references/tools-by-phase/analyze/statistical_analysis.md`.

**Statistical Tools by Situation**:

| Situation | Tool |
|-----------|------|
| Compare two means | 2-sample t-test |
| Compare multiple means | ANOVA |
| Compare proportions | Chi-square test |
| Relationship between variables | Correlation, Regression |
| Identify significant factors | DOE (Design of Experiments) |

**Hypothesis Testing Framework**:
- H₀ (Null): No effect/difference
- H₁ (Alternative): Effect/difference exists
- α (Alpha): Significance level (typically 0.05)
- p-value < α → Reject null hypothesis → Effect is statistically significant

#### 3.4 Analyze Phase Tollgate Questions

Before moving to Improve:
- [ ] Are root causes identified with data evidence?
- [ ] Are the "vital few" causes prioritized?
- [ ] Is there statistical verification of cause-effect?
- [ ] Can the team explain why the problem occurs?
- [ ] Are potential solutions starting to emerge?

---

### Step 4: Improve Phase

**Objective**: Develop, test, and implement solutions.

#### 4.1 Generate Solutions

Load `references/tools-by-phase/improve/solution_generation.md`.

**Brainstorming Guidelines**:
- Quantity over quality initially
- No criticism during generation
- Build on others' ideas
- Encourage wild ideas

**Benchmarking**: Learn from best practices elsewhere

**TRIZ Principles**: Structured inventive problem solving

#### 4.2 Select Best Solutions

Load `references/tools-by-phase/improve/solution_selection.md`.

**Pugh Matrix** (Concept Selection):
1. Define evaluation criteria
2. Select baseline concept
3. Compare each alternative against baseline (+, -, S)
4. Sum scores and select winner

**Decision Matrix** (Weighted Scoring):
| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Cost | 30% | 8 | 6 | 9 |
| Effectiveness | 40% | 9 | 8 | 7 |
| Ease of Implementation | 30% | 7 | 9 | 6 |
| **Weighted Score** | | **8.1** | **7.5** | **7.3** |

#### 4.3 Conduct FMEA

Load `references/tools-by-phase/improve/fmea_guide.md` and `assets/fmea_template.md`.

**FMEA (Failure Mode and Effects Analysis)**:
Proactively identify and mitigate risks in the solution.

| Failure Mode | Effect | Severity (1-10) | Cause | Occurrence (1-10) | Detection (1-10) | RPN | Action |
|--------------|--------|-----------------|-------|-------------------|------------------|-----|--------|

**RPN = Severity × Occurrence × Detection**

Prioritize actions for high RPN items (typically > 100).

#### 4.4 Pilot Testing

Load `references/tools-by-phase/improve/pilot_testing.md`.

**Pilot Plan**:
- Scope: Limited area/time for testing
- Success criteria: What determines success?
- Data collection: How to measure pilot results?
- Contingency: What if pilot fails?

**Before-After Comparison**:
- Compare pilot metrics to baseline
- Use statistical tests to verify improvement
- Document lessons learned

#### 4.5 Improve Phase Tollgate Questions

Before moving to Control:
- [ ] Are solutions addressing verified root causes?
- [ ] Is solution selection documented and justified?
- [ ] Were risks identified and mitigated (FMEA)?
- [ ] Was a pilot conducted successfully?
- [ ] Is improvement statistically significant?
- [ ] Is implementation plan ready?

---

### Step 5: Control Phase

**Objective**: Sustain improvements and prevent regression.

#### 5.1 Develop Control Plan

Load `references/tools-by-phase/control/control_plan_guide.md` and `assets/control_plan_template.md`.

**Control Plan Elements**:
- What to control (CTQs, key parameters)
- How to measure
- Sample size and frequency
- Control method (control chart type)
- Specification limits
- Reaction plan (what to do if out of control)
- Responsible person

#### 5.2 Implement Statistical Process Control (SPC)

Load `references/tools-by-phase/control/control_charts_guide.md`.

**Control Chart Selection**:

| Data Type | Subgroup Size | Chart Type |
|-----------|---------------|------------|
| Continuous | n = 1 | I-MR (Individuals-Moving Range) |
| Continuous | n = 2-10 | X-bar/R (Average/Range) |
| Continuous | n > 10 | X-bar/S (Average/Std Dev) |
| Attribute (defectives) | Variable | P chart (proportion) |
| Attribute (defectives) | Constant | NP chart (count) |
| Attribute (defects) | Variable | U chart (per unit) |
| Attribute (defects) | Constant | C chart (count) |

**Out-of-Control Rules** (Western Electric):
1. One point beyond 3σ
2. Two of three consecutive points beyond 2σ (same side)
3. Four of five consecutive points beyond 1σ (same side)
4. Eight consecutive points on same side of centerline
5. Six consecutive points trending up or down

#### 5.3 Create Standard Work

Load `references/tools-by-phase/control/standard_work.md`.

**Standard Work Documentation**:
- Step-by-step work instructions
- Visual aids and photos
- Key quality checkpoints
- Safety considerations
- Required tools and materials

**Training**:
- Train all operators on new process
- Verify competency
- Post visual instructions at workstation

#### 5.4 Handoff to Process Owner

**Handoff Checklist**:
- [ ] Control plan documented and implemented
- [ ] Control charts established and being used
- [ ] Standard work documented and trained
- [ ] Response plan for out-of-control conditions
- [ ] Monitoring schedule and responsibilities clear
- [ ] Project documentation archived

#### 5.5 Control Phase Tollgate Questions

Before closing project:
- [ ] Is the control plan implemented?
- [ ] Are control charts showing stable process?
- [ ] Are standard work documents completed?
- [ ] Is the process owner trained and accepting ownership?
- [ ] Are results meeting the goal?
- [ ] Is project documentation complete?

---

## Core Workflow 2: DMADV/DFSS for New Processes

Use this workflow when designing a new process or product (not improving existing).

Load `references/methodology/02_dmadv_dfss.md` for detailed guidance.

### When to Use DMADV Instead of DMAIC

Use DMADV when:
- Creating entirely new process/product
- Existing process is beyond repair (needs redesign)
- No baseline exists to improve from
- Customer requirements are significantly changing

### DMADV Phases Summary

**Define**: Identify the project goals aligned with customer demands and enterprise strategy.

**Measure**: Measure and determine customer needs and specifications.
- Extensive VOC analysis
- Translate needs to measurable CTQs
- Benchmark competitors

**Analyze**: Analyze process/product options to meet customer needs.
- Generate design concepts
- Use Pugh Matrix for selection
- Predictive analysis

**Design**: Design the process/product to meet customer needs.
- Detailed design development
- FMEA for design risks
- Simulations and modeling
- Design reviews

**Verify**: Verify the design performance and ability to meet customer needs.
- Pilot testing
- Full-scale validation
- Capability studies
- Handoff to operations

---

## Core Workflow 3: Lean Waste Elimination (VSM-based)

Use this workflow to identify and eliminate waste in processes.

### Step 1: Understand Value

Load `references/methodology/03_lean_principles.md`.

**Value Definition**: What the customer is willing to pay for
- Does this activity transform the product/service?
- Does the customer care about this activity?
- Is it done right the first time?

**Activity Categories**:
- **Value-Added (VA)**: Transforms product, customer pays for it
- **Non-Value-Added (NVA)**: Pure waste, eliminate
- **Business Non-Value-Added (BNVA)**: Required but no customer value (compliance, etc.)

### Step 2: Map the Current State Value Stream

Load `references/lean-tools/value_stream_mapping.md`.

**Value Stream Map Elements**:
- Process boxes (with data: cycle time, changeover, uptime)
- Inventory triangles (with quantities)
- Information flows (orders, schedules)
- Timeline (processing time vs. lead time)

**Key Metrics**:
- **Lead Time**: Total time from order to delivery
- **Processing Time**: Sum of value-added time
- **Value-Added Ratio**: Processing Time / Lead Time (often < 5%!)

### Step 3: Identify the 8 Wastes (DOWNTIME)

Load `references/lean-tools/eight_wastes_downtime.md`.

| Waste | Description | Examples |
|-------|-------------|----------|
| **D**efects | Rework, scrap, errors | Quality failures, corrections |
| **O**verproduction | Making more than needed | Large batches, just-in-case |
| **W**aiting | Idle time, delays | Waiting for approval, information |
| **N**on-utilized Talent | Underused skills | Not engaging employee ideas |
| **T**ransportation | Moving materials | Excessive shipping, transfers |
| **I**nventory | Excess stock | WIP, finished goods sitting |
| **M**otion | Unnecessary movement | Walking, reaching, searching |
| **E**xtra-processing | Over-engineering | Unnecessary features, approvals |

### Step 4: Design Future State

**Future State Principles**:
- Produce to takt time (customer demand rate)
- Create continuous flow where possible
- Use pull systems (Kanban) where flow isn't possible
- Level the production mix (Heijunka)
- Build in quality (Jidoka)

### Step 5: Implement with Kaizen Events

Load `references/lean-tools/kaizen_events.md`.

**Kaizen Event** (Rapid Improvement):
- Focused 3-5 day event
- Cross-functional team
- Make changes during the event
- Measure before/after
- Sustain with visual management

**5S Implementation**:
Load `references/lean-tools/five_s_guide.md`.

| Step | Japanese | English | Action |
|------|----------|---------|--------|
| 1 | Seiri | Sort | Remove unnecessary items |
| 2 | Seiton | Set in Order | Organize remaining items |
| 3 | Seiso | Shine | Clean and inspect |
| 4 | Seiketsu | Standardize | Create standards |
| 5 | Shitsuke | Sustain | Maintain discipline |

---

## Core Workflow 4: Statistical Analysis Support

Use this workflow when needing statistical guidance.

### Process Capability Analysis

Load `references/statistics/process_capability.md`.

**Cp (Process Capability)**:
```
Cp = (USL - LSL) / (6σ)
```
- Measures process potential if perfectly centered
- Cp = 1.0 means process spread = specification spread
- Cp = 1.33 is typical minimum requirement
- Cp = 2.0 is Six Sigma target

**Cpk (Process Capability Index)**:
```
Cpk = min[(USL - μ)/(3σ), (μ - LSL)/(3σ)]
```
- Measures actual capability considering centering
- Cpk < Cp indicates process is not centered
- Cpk = Cp when perfectly centered

**Interpretation Guide**:
| Cpk Value | Interpretation |
|-----------|----------------|
| < 1.0 | Not capable - immediate action required |
| 1.0 - 1.33 | Marginally capable - improvement needed |
| 1.33 - 1.67 | Capable - acceptable for most industries |
| 1.67 - 2.0 | Very capable - excellent |
| ≥ 2.0 | World-class - Six Sigma level |

### Control Chart Implementation

Load `references/statistics/control_chart_types.md`.

**Control Limit Calculation** (X-bar/R Chart):
```
UCL_X = X̄̄ + A₂R̄
LCL_X = X̄̄ - A₂R̄
UCL_R = D₄R̄
LCL_R = D₃R̄
```

**Constants Table**:
| n | A₂ | D₃ | D₄ |
|---|-----|-----|-----|
| 2 | 1.880 | 0 | 3.267 |
| 3 | 1.023 | 0 | 2.575 |
| 4 | 0.729 | 0 | 2.282 |
| 5 | 0.577 | 0 | 2.115 |

### Hypothesis Testing Guide

Load `references/statistics/hypothesis_testing.md`.

**Decision Flowchart**:
```
Q: Comparing what?
├── Two means → 2-sample t-test
├── Multiple means → ANOVA
├── Proportions → Chi-square / Z-test
├── Relationship → Correlation / Regression
└── Factors/Interactions → DOE
```

---

## Core Workflow 5: Tool Selection Guide

Use this matrix to select appropriate tools based on DMAIC phase and purpose.

### Define Phase Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| Project Charter | Document project scope and goals | Every project |
| SIPOC | High-level process overview | Every project |
| VOC Analysis | Understand customer needs | Customer-focused projects |
| CTQ Tree | Translate needs to measurables | Customer-focused projects |
| Stakeholder Analysis | Identify and engage stakeholders | Complex/political projects |

### Measure Phase Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| Data Collection Plan | Plan what/how to collect | Every project |
| MSA / Gage R&R | Validate measurement system | When data reliability is critical |
| Process Map | Document current process | Every project |
| Time Study | Measure cycle times | Cycle time projects |
| Pareto Chart | Prioritize categories | When categorizing problems |

### Analyze Phase Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| Fishbone Diagram | Brainstorm potential causes | Every project |
| 5 Whys | Drill to root cause | Simple cause-effect chains |
| Pareto Analysis | Identify vital few | Multiple problem categories |
| Scatter Plot | Visualize relationships | Exploring correlations |
| Hypothesis Testing | Statistically verify causes | Data-driven verification |
| Regression | Model relationships | Predictive modeling |

### Improve Phase Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| Brainstorming | Generate solutions | Every project |
| Benchmarking | Learn from best practices | Seeking external ideas |
| Pugh Matrix | Select concepts | Multiple solution options |
| FMEA | Risk assessment | Implementing changes |
| Pilot Testing | Test solutions | Before full rollout |
| DOE | Optimize factors | Multiple factors to optimize |

### Control Phase Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| Control Plan | Document control system | Every project |
| Control Charts | Monitor process stability | Ongoing monitoring |
| Standard Work | Document best practices | Process standardization |
| Visual Management | Make status visible | Sustaining improvements |
| Mistake-Proofing | Prevent errors | Error-prone processes |

---

## Core Workflow 6: Training/Education Mode

Use this workflow for learning and certification preparation.

### Belt-Level Learning Paths

Load appropriate curriculum from `references/training/`.

**White Belt** (4-8 hours):
- What is Lean Six Sigma?
- Basic concepts: waste, variation, DMAIC overview
- Role in improvement projects
- Load: `references/training/white_yellow_belt.md`

**Yellow Belt** (1-2 days):
- DMAIC phases in more detail
- Basic tools: Fishbone, 5 Whys, Pareto, Process Mapping
- Data collection support
- Team participation skills
- Load: `references/training/white_yellow_belt.md`

**Green Belt** (2-4 weeks):
- Complete DMAIC methodology
- Statistical tools: capability, hypothesis testing, control charts
- Project leadership
- Load: `references/training/green_belt_curriculum.md`

**Black Belt** (4-8 weeks):
- Advanced statistics: DOE, regression, ANOVA
- Complex project management
- Mentoring Green Belts
- Organizational change management
- Load: `references/training/black_belt_curriculum.md`

### Sample Certification Questions

**Green Belt Level**:
1. What are the 5 phases of DMAIC?
2. What is the difference between Cp and Cpk?
3. When would you use a P-chart vs. C-chart?
4. What is the purpose of MSA?
5. How do you interpret a Pareto chart?

**Black Belt Level**:
1. Explain the 1.5 sigma shift in capability analysis.
2. Design a 2³ factorial experiment for this scenario.
3. What are the assumptions for ANOVA?
4. How do you calculate control limits for an X-bar/R chart?
5. When is DMADV preferred over DMAIC?

---

## Industry Applications

### Manufacturing

Load `references/industries/manufacturing.md`.

**Common Applications**:
- Defect reduction in production lines
- Cycle time improvement
- OEE (Overall Equipment Effectiveness) optimization
- Setup time reduction (SMED)
- Machine capability studies

**Specific Tools Emphasis**:
- SPC and control charts
- FMEA for process/equipment
- 5S for workplace organization
- TPM for equipment reliability

### Services/Transactional

Load `references/industries/services_transactional.md`.

**Common Applications**:
- Transaction error reduction
- Cycle time for approvals/processing
- Customer wait time reduction
- Call center optimization
- Invoice processing accuracy

**Adaptation Notes**:
- "Defect" = error, rework, exception
- Harder to see waste (information flow vs. physical)
- Process mapping is critical for visibility

### Healthcare

Load `references/industries/healthcare.md`.

**Common Applications**:
- Patient wait time reduction
- Medication error prevention
- Readmission reduction
- Operating room turnaround
- Clinical pathway optimization

**Special Considerations**:
- Patient safety is paramount
- Regulatory compliance (HIPAA, Joint Commission)
- Evidence-based medicine integration

### IT/Software

Load `references/industries/it_software.md`.

**Common Applications**:
- Defect density reduction
- Deployment frequency improvement
- Incident resolution time
- Change failure rate reduction
- Sprint velocity optimization

**Integration with Agile/DevOps**:
- Use Lean principles in Kanban
- Apply Six Sigma for defect reduction
- Combine with DORA metrics

---

## Resources

### Reference Files

**Methodology** (`references/methodology/`):
- `01_dmaic_overview.md` - Detailed DMAIC guidance
- `02_dmadv_dfss.md` - Design for Six Sigma
- `03_lean_principles.md` - Lean fundamentals

**Tools by Phase** (`references/tools-by-phase/`):
- Define, Measure, Analyze, Improve, Control subdirectories
- Each contains detailed tool guides

**Lean Tools** (`references/lean-tools/`):
- VSM, 8 Wastes, 5S, Kaizen guides

**Statistics** (`references/statistics/`):
- Process capability, control charts, hypothesis testing, sigma calculation

**Industries** (`references/industries/`):
- Manufacturing, services, healthcare, IT applications

**Training** (`references/training/`):
- Belt-level curricula

### Templates (`assets/`)

- `project_charter_template.md`
- `sipoc_template.md`
- `control_plan_template.md`
- `a3_report_template.md`
- `fmea_template.md`
- `tollgate_review_checklist.md`

### Calculation Scripts (`scripts/`)

- `sigma_calculator.py` - DPMO, sigma level, yield
- `process_capability.py` - Cp, Cpk, Pp, Ppk
- `control_chart_analysis.py` - Control limits, out-of-control detection

---

## Best Practices

### Project Success Factors

1. **Clear problem definition**: Spend adequate time in Define
2. **Data-driven decisions**: Verify with data, not opinions
3. **Management support**: Active champion engagement
4. **Cross-functional team**: Include process experts
5. **Realistic scope**: Avoid boiling the ocean
6. **Sustain improvements**: Control phase is critical

### Common Pitfalls to Avoid

1. **Jumping to solutions**: Skip analysis, implement pet solutions
2. **Scope creep**: Project grows beyond original charter
3. **Poor data quality**: Garbage in, garbage out
4. **Ignoring resistance**: Change management neglected
5. **Weak control phase**: Improvements fade over time
6. **Over-reliance on tools**: Tools serve the process, not vice versa

### Tips for Success

- Use tollgate reviews to ensure phase completion
- Communicate progress regularly to stakeholders
- Document lessons learned for future projects
- Celebrate successes to build momentum
- Build internal capability through training
