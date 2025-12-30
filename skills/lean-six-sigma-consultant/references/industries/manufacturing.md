# Lean Six Sigma in Manufacturing

## Overview

Manufacturing is the birthplace of both Lean (Toyota Production System) and Six Sigma (Motorola). The methodologies are particularly suited to manufacturing environments where processes are tangible, measurable, and repetitive.

## Key Manufacturing Metrics

### Overall Equipment Effectiveness (OEE)

**Formula**: OEE = Availability × Performance × Quality

**Components**:
- **Availability**: (Run Time / Planned Production Time) × 100
- **Performance**: (Ideal Cycle Time × Total Count / Run Time) × 100
- **Quality**: (Good Count / Total Count) × 100

**Benchmarks**:
| Level | OEE % | Description |
|-------|-------|-------------|
| World Class | ≥ 85% | Top performers |
| Average | 60-80% | Most manufacturers |
| Typical | 40-60% | Significant improvement opportunity |
| Low | < 40% | Major issues present |

**Loss Categories (Six Big Losses)**:
1. **Equipment Failure** (Availability)
2. **Setup/Adjustment** (Availability)
3. **Idling/Minor Stops** (Performance)
4. **Reduced Speed** (Performance)
5. **Defects in Process** (Quality)
6. **Reduced Yield** (Quality)

### SMED (Single-Minute Exchange of Die)

**Goal**: Reduce changeover time to under 10 minutes

**Process**:
1. **Document current state**: Film and time entire changeover
2. **Separate internal/external tasks**:
   - Internal: Must be done with machine stopped
   - External: Can be done while machine is running
3. **Convert internal to external**: Find ways to prep while running
4. **Streamline internal tasks**: Parallel operations, quick fasteners
5. **Streamline external tasks**: Organize, standardize

**Typical Results**:
- 50-90% reduction in changeover time
- Enables smaller batch sizes
- Reduces inventory
- Increases flexibility

### Cycle Time and Takt Time

**Takt Time**: Rate at which products must be completed to meet customer demand

```
Takt Time = Available Production Time / Customer Demand
```

**Example**:
- Available Time: 480 minutes/day
- Demand: 240 units/day
- Takt Time: 480/240 = 2 minutes/unit

**Cycle Time**: Actual time to complete one unit

**Balance**: Cycle Time should be ≤ Takt Time

### Machine Capability (Cm, Cmk)

**Cm** (Machine Capability): Potential capability of the machine
```
Cm = (USL - LSL) / (6 × σ_machine)
```

**Cmk** (Machine Capability Index): Actual capability considering centering
```
Cmk = min[(USL - μ)/(3σ), (μ - LSL)/(3σ)]
```

**Requirements**:
| Index | Minimum | Target |
|-------|---------|--------|
| Cm | 1.67 | ≥ 2.0 |
| Cmk | 1.67 | ≥ 2.0 |

**Note**: Machine capability studies use 50+ consecutive parts, short-term data.

## Manufacturing-Specific Tools

### Process FMEA (PFMEA)

**Focus**: Manufacturing process failure modes

**Key Considerations**:
- Equipment/tooling failures
- Operator errors
- Material handling issues
- Environmental factors
- Measurement system errors

**Severity Ratings** (Manufacturing):
| Rating | Effect | Example |
|--------|--------|---------|
| 10 | Safety hazard, no warning | Fire, injury risk |
| 9 | Safety with warning | Warning before failure |
| 8 | Total function loss | Product won't operate |
| 7 | Major function loss | Significant degradation |
| 6 | Partial function loss | Some features affected |
| 5 | Minor function loss | Minor degradation |
| 4 | Aesthetic issue (severe) | Obvious defect |
| 3 | Aesthetic issue (moderate) | Noticeable defect |
| 2 | Aesthetic issue (minor) | Slight defect |
| 1 | No effect | No discernible effect |

### Gage R&R for Manufacturing

**Requirements**:
| %R&R | Acceptability |
|------|---------------|
| < 10% | Excellent |
| 10-20% | Acceptable |
| 20-30% | Marginal |
| > 30% | Unacceptable |

**Typical Studies**:
- 10 parts (representative of process variation)
- 3 operators (covering all shifts)
- 3 trials each
- Random order

### Statistical Process Control

**Common Manufacturing Charts**:

| Data Type | Chart Type | When to Use |
|-----------|------------|-------------|
| Continuous, subgroups | X-bar/R | Parts measured in groups |
| Continuous, individuals | I-MR | Single measurements |
| Continuous, large n | X-bar/S | Subgroup size > 9 |
| Defective units | P, NP | Go/No-go, pass/fail |
| Defect counts | C, U | Multiple defects per unit |

**Control Limit Calculation** (X-bar/R):
```
UCL_Xbar = X̄ + A₂R̄
LCL_Xbar = X̄ - A₂R̄
UCL_R = D₄R̄
LCL_R = D₃R̄
```

## Common Manufacturing Projects

### Scrap/Rework Reduction

**Typical Approach**:
1. **Define**: Pareto of defect types, cost impact
2. **Measure**: Defect rates by operation, shift, product
3. **Analyze**: Fishbone for top defects, correlation analysis
4. **Improve**: Process parameter optimization, training
5. **Control**: SPC, inspection protocols

**Key Metrics**:
- Scrap rate (%)
- Cost of scrap ($)
- Rework hours
- First Pass Yield

### Equipment Downtime Reduction

**Approach**:
1. **Define**: Pareto of downtime causes, OEE baseline
2. **Measure**: MTBF, MTTR, frequency by failure mode
3. **Analyze**: Root cause for top failures
4. **Improve**: TPM, preventive maintenance, spare parts
5. **Control**: Maintenance schedules, condition monitoring

**Key Metrics**:
- MTBF (Mean Time Between Failures)
- MTTR (Mean Time To Repair)
- Availability %
- Unplanned downtime hours

### Throughput Improvement

**Approach**:
1. **Define**: Current vs. required capacity
2. **Measure**: Cycle times, bottlenecks, WIP
3. **Analyze**: Constraint identification, line balance
4. **Improve**: SMED, batch size reduction, flow optimization
5. **Control**: Standard work, visual management

**Key Metrics**:
- Units per hour/day
- Cycle time
- Lead time
- WIP levels

## Manufacturing Value Stream Mapping

### Key Elements

**Material Flow**:
- Inventory quantities
- Batch sizes
- Transportation
- Wait times

**Information Flow**:
- Production scheduling
- Order processing
- Communication methods

**Timeline**:
- Process time (value-add)
- Wait time (non-value-add)
- Lead time (total)

### Manufacturing Symbols

```
[Customer/Supplier]: Factory icons
[Process Box]: Contains cycle time, changeover, OEE
[Inventory Triangle]: Shows quantity, days of supply
[Push Arrow]: Traditional batch movement
[Pull Symbol]: Kanban signal
[Supermarket]: Kanban stock point
[FIFO Lane]: First-in-first-out flow
```

### Example Metrics in Process Boxes

| Metric | Description |
|--------|-------------|
| C/T | Cycle Time |
| C/O | Changeover Time |
| Uptime | Availability % |
| Batch | Batch size |
| Operators | Number of workers |
| Shift | Shifts worked |

## Industry Standards and Certifications

### Quality Management Systems

- **ISO 9001**: Quality Management System
- **IATF 16949**: Automotive Quality Management
- **AS9100**: Aerospace Quality Management
- **ISO 13485**: Medical Device Quality Management

### Process Capability Requirements

| Industry | Typical Cpk Requirement |
|----------|------------------------|
| General Manufacturing | ≥ 1.33 |
| Automotive | ≥ 1.67 |
| Aerospace | ≥ 1.67 to 2.0 |
| Medical Devices | ≥ 1.33 (process validated) |
| Semiconductor | ≥ 2.0 |

### APQP (Advanced Product Quality Planning)

**Five Phases**:
1. Plan and Define Program
2. Product Design and Development
3. Process Design and Development
4. Product and Process Validation
5. Feedback, Assessment, and Corrective Action

**Core Tools**:
- FMEA
- Control Plan
- MSA
- SPC
- PPAP (Production Part Approval Process)

## Best Practices

### For DMAIC Projects

1. **Always include operators**: They know the process best
2. **Use real production data**: Don't rely on trial data alone
3. **Consider shift-to-shift variation**: Different shifts, different results
4. **Account for warm-up effects**: First parts may differ
5. **Test solutions under production conditions**: Lab success ≠ floor success

### For Lean Implementation

1. **Start with 5S**: Foundation for everything else
2. **Map before improving**: Understand current state
3. **Follow the product**: Walk the actual flow
4. **Question everything**: "Why?" for each step
5. **Involve everyone**: Operators, engineers, management

### For Sustaining Improvements

1. **Visual management**: Make abnormalities obvious
2. **Standard work**: Document the best method
3. **Daily management**: Regular process checks
4. **Layered audits**: Different levels, different frequencies
5. **Continuous training**: Maintain and build skills

## Common Pitfalls

### Project Selection

- Starting too big (company-wide vs. focused)
- Ignoring constraint operations
- Not involving maintenance team
- Underestimating data collection time

### Implementation

- Optimizing individual operations vs. flow
- Not running pilots under production conditions
- Skipping control phase
- Inadequate training for operators

### Sustainability

- Removing controls too soon
- Not updating procedures
- No response plan for out-of-control
- Lack of management follow-through
