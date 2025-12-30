# Lean Principles and Fundamentals

## Introduction

Lean is a philosophy and methodology focused on maximizing customer value while minimizing waste. Originating from the Toyota Production System (TPS), Lean principles apply across manufacturing, services, healthcare, and all industries.

## Origins: Toyota Production System

### Historical Background
- Developed at Toyota Motor Corporation post-WWII
- Key architects: Taiichi Ohno, Shigeo Shingo, Eiji Toyoda
- Response to resource constraints and need for efficiency
- Evolved over decades of continuous improvement

### TPS Pillars

**Just-In-Time (JIT)**:
- Produce only what is needed, when needed, in the amount needed
- Pull systems driven by customer demand
- Minimize inventory and lead time

**Jidoka (Autonomation)**:
- Build quality at the source
- Stop and fix problems immediately
- Prevent defects from passing downstream
- Human intelligence + automation

### TPS House

```
                    ┌───────────────────────┐
                    │    Best Quality       │
                    │    Lowest Cost        │
                    │   Shortest Lead Time  │
                    │     Best Safety       │
                    │    High Morale        │
                    └───────────┬───────────┘
         ┌──────────────────────┴──────────────────────┐
         │                                              │
    ┌────┴────┐                                    ┌────┴────┐
    │  Just   │                                    │ Jidoka  │
    │ In Time │                                    │(Quality)│
    │         │                                    │         │
    │- Takt   │      Heijunka (Leveling)          │- Stop & │
    │- Flow   │      Standardized Work            │  fix    │
    │- Pull   │      Kaizen                       │- Visual │
    └─────────┘                                    └─────────┘
         │                                              │
         └──────────────────────┬──────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │      Stability        │
                    │  5S, TPM, Standard    │
                    │        Work           │
                    └───────────────────────┘
```

---

## The Five Lean Principles

### Principle 1: Define Value

**Definition**: Value is what the customer is willing to pay for.

**Key Questions**:
- What does the customer actually need?
- What would they pay for?
- What features/attributes matter most?

**Value vs. Waste**:
- Value: Transforms product/service toward what customer wants
- Waste: Consumes resources without adding value

**Application**:
- Talk to customers directly
- Understand true needs vs. assumed needs
- Define value from customer perspective, not internal

### Principle 2: Map the Value Stream

**Definition**: Identify all activities required to deliver value from order to delivery.

**Value Stream Components**:
- All process steps
- Information flows
- Material flows
- Time (processing and wait)

**Activity Categories**:
| Category | Description | Action |
|----------|-------------|--------|
| Value-Added (VA) | Transforms product, customer pays | Preserve |
| Non-Value-Added (NVA) | Pure waste | Eliminate |
| Business NVA (BNVA) | Required but no customer value | Minimize |

**Value Stream Mapping**:
- Document current state
- Identify waste and opportunities
- Design future state
- Create implementation plan

### Principle 3: Create Flow

**Definition**: Make value-adding steps flow continuously without interruption.

**Flow Obstacles**:
- Batching
- Queues and waiting
- Rework loops
- Departmental silos
- Scheduling complexity

**Flow Enablers**:
- Single-piece flow where possible
- Reduced batch sizes
- Cross-training
- Cellular layouts
- Quick changeovers (SMED)

**Benefits of Flow**:
- Reduced lead time
- Lower inventory
- Faster defect detection
- Improved quality
- Less complexity

### Principle 4: Establish Pull

**Definition**: Produce only what is needed, when needed, based on actual customer demand.

**Push vs. Pull**:
| Push | Pull |
|------|------|
| Based on forecast | Based on actual demand |
| Build to stock | Build to order |
| High inventory | Low inventory |
| Long lead times | Short lead times |

**Pull Mechanisms**:
- **Kanban**: Visual signal to replenish
- **Supermarket**: Small buffer replenished by pull
- **FIFO Lane**: First-in-first-out queue
- **Sequenced Pull**: Build in customer order

**Kanban System**:
```
[Process A] → [Kanban Signal] ← [Process B]
              "Need more!"
```
- Downstream process signals need
- Upstream produces only to replace what was consumed
- Limits work-in-process (WIP)

### Principle 5: Pursue Perfection

**Definition**: Continuously improve toward perfect value with zero waste.

**Continuous Improvement Culture**:
- Never satisfied with status quo
- Everyone participates
- Small, incremental improvements
- Respect for people

**Kaizen (Continuous Improvement)**:
- Daily problem-solving
- Standard work as baseline
- PDCA cycle for improvement
- Gemba (go and see)

**Perfection Targets**:
- Zero defects
- Zero inventory
- Zero setup time
- Zero lead time
- 100% value-added

---

## The 8 Wastes (DOWNTIME)

### D - Defects
**Description**: Products or services that don't meet specifications.

**Examples**:
- Manufacturing: Scrap, rework, inspection
- Office: Data entry errors, incorrect orders
- Healthcare: Medication errors, wrong site surgery

**Causes**:
- Inadequate training
- Poor process design
- Variation in inputs
- Unclear specifications

**Solutions**:
- Poka-yoke (mistake-proofing)
- Standard work
- Training
- Process capability improvement

### O - Overproduction
**Description**: Producing more than needed or before needed.

**Examples**:
- Manufacturing: Large batches, just-in-case production
- Office: Generating reports no one reads
- Healthcare: Unnecessary tests

**Why It's the Worst Waste**:
- Creates other wastes (inventory, motion, etc.)
- Ties up capital
- Hides problems
- Delays feedback

**Solutions**:
- Pull systems
- Takt time production
- Smaller batch sizes
- Level scheduling (Heijunka)

### W - Waiting
**Description**: Idle time when materials, information, or people wait.

**Examples**:
- Manufacturing: Machine downtime, waiting for parts
- Office: Waiting for approval, system downtime
- Healthcare: Patient waiting, waiting for test results

**Causes**:
- Unbalanced workloads
- Equipment unreliability
- Large batch sizes
- Poor scheduling

**Solutions**:
- Line balancing
- TPM (Total Productive Maintenance)
- Cross-training
- Flow improvement

### N - Non-Utilized Talent
**Description**: Not using people's skills, ideas, and creativity.

**Examples**:
- Not asking for improvement ideas
- Underutilizing skills
- Top-down only decisions
- Limited training opportunities

**Impact**:
- Low engagement
- Missed improvement opportunities
- High turnover
- Knowledge not captured

**Solutions**:
- Suggestion systems
- Kaizen involvement
- Cross-functional teams
- Skill development

### T - Transportation
**Description**: Unnecessary movement of materials or products.

**Examples**:
- Manufacturing: Moving WIP between buildings
- Office: Moving files between departments
- Healthcare: Transporting patients long distances

**Causes**:
- Poor layout
- Large batch production
- Multiple storage locations
- Departmental organization

**Solutions**:
- Cellular layout
- Point-of-use storage
- Smaller batches
- Process proximity

### I - Inventory
**Description**: Excess raw materials, WIP, or finished goods.

**Examples**:
- Manufacturing: Safety stock, obsolete inventory
- Office: Backlogs, pending work
- Healthcare: Expired supplies, unused equipment

**Hidden Costs**:
- Storage space
- Handling
- Obsolescence
- Capital tied up
- Hides problems

**Solutions**:
- Pull systems
- Reduced batch sizes
- Improved reliability
- Better forecasting

### M - Motion
**Description**: Unnecessary movement of people.

**Examples**:
- Manufacturing: Walking, reaching, searching
- Office: Walking to printer, searching for files
- Healthcare: Nurses walking long distances

**Causes**:
- Poor workplace layout
- Disorganized work area
- Information not accessible
- Tools not at point of use

**Solutions**:
- 5S workplace organization
- Ergonomic design
- Tool placement
- Information accessibility

### E - Extra-Processing
**Description**: Doing more than customer requires or values.

**Examples**:
- Manufacturing: Over-polishing, unnecessary features
- Office: Multiple approvals, redundant data entry
- Healthcare: Unnecessary documentation

**Causes**:
- Unclear requirements
- Over-specification
- "That's how we've always done it"
- Lack of customer understanding

**Solutions**:
- Understand customer value
- Challenge specifications
- Simplify processes
- Eliminate redundancy

---

## Key Lean Tools

### 5S Workplace Organization

| Step | Japanese | English | Action |
|------|----------|---------|--------|
| 1 | Seiri | Sort | Remove unnecessary items |
| 2 | Seiton | Set in Order | Organize remaining items |
| 3 | Seiso | Shine | Clean and inspect |
| 4 | Seiketsu | Standardize | Create standards |
| 5 | Shitsuke | Sustain | Maintain discipline |

### Value Stream Mapping (VSM)

**Current State Map**:
- Document existing process
- Collect data (cycle time, changeover, uptime, inventory)
- Calculate lead time and VA ratio
- Identify waste and opportunities

**Future State Map**:
- Design improved process
- Apply flow, pull, leveling
- Set improvement targets
- Create implementation plan

### Kaizen Events

**Structure**:
- 3-5 day focused improvement event
- Cross-functional team
- Full-time dedication
- Make changes during event

**Phases**:
1. Preparation (before event)
2. Current state understanding (Day 1)
3. Solution development (Day 2-3)
4. Implementation (Day 3-4)
5. Sustain and celebrate (Day 5)

### Standard Work

**Components**:
- Takt time
- Work sequence
- Standard WIP
- Work instructions

**Benefits**:
- Baseline for improvement
- Consistent quality
- Training foundation
- Problem visibility

### Visual Management

**Types**:
- Status displays (production boards)
- Performance metrics
- Kanban cards/boards
- Andon lights
- Shadow boards for tools

**Principles**:
- See status at a glance
- Abnormalities visible immediately
- Enable quick response
- No searching required

---

## Lean Six Sigma Integration

### Complementary Strengths

| Lean | Six Sigma |
|------|-----------|
| Speed, waste focus | Rigor, variation focus |
| Flow and pull | Statistical analysis |
| Visual management | Data-driven decisions |
| Rapid improvement | Sustained improvement |

### When to Use Each

**Use Lean Tools When**:
- Waste is visible and obvious
- Flow problems exist
- Quick wins needed
- Process is unstable

**Use Six Sigma Tools When**:
- Variation is the problem
- Root cause is unclear
- Statistical proof needed
- Complex multi-factor issues

### Integration Approach

1. Start with Lean to stabilize and reduce obvious waste
2. Apply Six Sigma to reduce variation
3. Use DMAIC as the overall framework
4. Incorporate Lean tools within DMAIC phases

**Example Integration**:
- Define: Project charter + VOC/CTQ
- Measure: Process map + VSM + baseline data
- Analyze: Root cause + waste identification
- Improve: Solutions + Kaizen + pilot
- Control: Control plan + standard work + visual management
