# Value Stream Mapping (VSM) Guide

## Overview

Value Stream Mapping is a Lean tool that provides a visual representation of all the steps involved in delivering a product or service from order to delivery. It shows both material and information flows, highlighting waste and opportunities for improvement.

## Purpose

- Visualize the entire value stream (end-to-end)
- Identify waste and non-value-added activities
- Calculate lead time vs. processing time
- Design an improved future state
- Create an implementation roadmap

---

## Value Stream Concepts

### What is a Value Stream?
All the actions (both value-added and non-value-added) required to bring a product or service from concept to customer.

### Value-Added Ratio

```
VA Ratio = Processing Time / Lead Time × 100

Example:
Lead Time: 20 days (total time order to delivery)
Processing Time: 4 hours (actual work time)
VA Ratio = 4 hrs / (20 days × 8 hrs/day) = 4 / 160 = 2.5%
```

Typical VA ratios:
- Manufacturing: 1-5%
- Service/Office: 1-10%
- Healthcare: 1-5%

**The goal**: Increase the ratio by reducing non-value-added time.

---

## VSM Symbols

### Process Symbols

```
┌─────────────┐
│             │
│  Process    │  Process Box: Single process step
│  Name       │  Contains: C/T, C/O, Uptime, etc.
│             │
└─────────────┘

    ▼         Inventory: Triangle shows WIP/inventory
   ___        with quantity below
   2500


    ○         Supermarket: Controlled inventory buffer
   ╱ ╲
  │   │


    ⇢         Push: Material pushed to next step


    ◀         Pull: Kanban signal


    ☐         Kaizen burst: Improvement opportunity
   ╲ ╱
```

### Information Flow

```
   ──────>    Electronic information flow

   ─ ─ ─ ─>   Manual information flow


   ┌───────┐
   │  MRP  │  Production Control: Scheduling function
   └───────┘


   OXOX      Load Leveling: Heijunka box
```

### Transportation

```
   ⛟         Shipping: External transportation


   ↔         Internal transport
```

---

## Current State Map

### Step 1: Walk the Process
- Go to the actual workplace (Gemba)
- Observe the complete process
- Talk to people doing the work
- Take notes and measurements

### Step 2: Map from Customer Backward
Start with customer demand, work backward:
1. Customer requirements
2. Final process step
3. Previous process step
4. Continue to raw materials/start

### Step 3: Collect Process Data

**Data Box Information**:
```
┌──────────────────────────┐
│      Process Name        │
├──────────────────────────┤
│ C/T (Cycle Time): 45 sec │
│ C/O (Changeover): 30 min │
│ Uptime: 85%              │
│ Batch Size: 100          │
│ Operators: 2             │
│ Shifts: 2                │
└──────────────────────────┘
```

**Key Metrics to Collect**:
| Metric | Definition |
|--------|------------|
| C/T (Cycle Time) | Time to complete one unit |
| C/O (Changeover Time) | Time to switch products |
| Uptime | % time equipment is available |
| Batch Size | Units processed together |
| WIP | Work-in-process inventory |
| # Operators | People required |
| Shifts | Hours of operation |

### Step 4: Map Information Flow
- How does the process know what to make?
- Where do schedules come from?
- How are orders communicated?

### Step 5: Add Inventory
- Show inventory between processes
- Include quantities
- Calculate days of inventory

```
Days of Inventory = Inventory Quantity / Daily Demand
```

### Step 6: Create Timeline

Draw timeline at bottom:
```
Process A    WIP    Process B    WIP    Process C
   │          │         │         │         │
   ▼          ▼         ▼         ▼         ▼
  [45s]     [2d]      [60s]     [3d]      [30s]  ← Processing Time
   └─────────┴─────────┴─────────┴─────────┘
            Lead Time = 5 days 2.25 min
            Processing Time = 2.25 min
```

---

## Future State Map

### Design Principles

**1. Produce to Takt Time**
```
Takt Time = Available Time / Customer Demand

Example:
Available: 27,000 seconds/day
Demand: 450 units/day
Takt = 27,000 / 450 = 60 seconds
```

**2. Create Continuous Flow**
- Link processes where possible
- Eliminate WIP between linked processes
- One-piece flow ideal

**3. Use Pull Systems**
Where flow isn't possible:
- Supermarket (controlled inventory)
- FIFO lanes
- Kanban signals

**4. Send Schedule to One Point**
- Pacemaker process (usually closest to customer)
- Upstream processes pull from pacemaker

**5. Level Production**
- Heijunka (production leveling)
- Mix model scheduling
- Smooth demand fluctuations

**6. Build in Quality**
- Jidoka (stop and fix)
- Poka-yoke (error-proofing)
- Andon systems

---

## VSM Analysis

### Identifying Waste

Look for the 8 wastes in the current state:

| Waste | VSM Indicators |
|-------|----------------|
| Defects | High scrap %, rework loops |
| Overproduction | Large inventory triangles |
| Waiting | Long lead time vs. short process time |
| Non-utilized talent | (Not visible on map) |
| Transportation | Long arrows, multiple moves |
| Inventory | Large triangles, many storage points |
| Motion | (Note during walk) |
| Extra processing | Multiple inspection steps |

### Kaizen Opportunities

Mark improvement opportunities with kaizen bursts:
```
    ☼        Kaizen burst
   ╱ ╲
  │   │
   ╲ ╱
    ▼
```

Common opportunities:
- High inventory points
- Long changeovers
- Low uptime
- Disconnected flow
- Multiple scheduling points

---

## Implementation Plan

### Creating the Roadmap

After future state design:

**1. Identify Value Stream Loops**
Break future state into manageable chunks:
- Pacemaker loop (closest to customer)
- Supporting loops (upstream)

**2. Prioritize**
- Start at pacemaker
- Work upstream
- Quick wins where possible

**3. Create Action Plan**

| Loop | Actions | Timeline | Owner |
|------|---------|----------|-------|
| Pacemaker | Implement supermarket | Month 1-2 | [Name] |
| | Establish pull | Month 2-3 | [Name] |
| Loop 2 | Reduce changeover | Month 3-4 | [Name] |
| | Create flow cell | Month 4-6 | [Name] |

### Metrics to Track

| Metric | Current | Future | Target Date |
|--------|---------|--------|-------------|
| Lead Time | 20 days | 5 days | Q4 |
| VA Ratio | 2.5% | 10% | Q4 |
| Inventory Turns | 18 | 72 | Q4 |
| First Pass Yield | 92% | 98% | Q4 |

---

## VSM Best Practices

### Do's
- Walk the actual process
- Collect real data
- Include information flow
- Involve process people
- Focus on flow, not departments
- Start with customer
- Create future state vision

### Don'ts
- Don't map from conference room
- Don't use standard times without verification
- Don't ignore information flow
- Don't try to fix everything at once
- Don't skip the timeline
- Don't confuse process map with value stream map

---

## Service/Office VSM Adaptations

### Key Differences
- Information is the "product"
- Inventory = backlog, queues, email
- Processing time may be harder to see

### Adapted Metrics

| Manufacturing | Service Equivalent |
|--------------|-------------------|
| WIP Inventory | Backlog, Queue |
| Cycle Time | Processing Time |
| Changeover | Task Switching |
| Transportation | Handoffs |
| Defects | Errors, Rework |

---

## Example Timeline

### Current State Timeline
```
Quote → Order Entry → Credit Check → Scheduling → Production → Shipping
  │         │            │             │            │           │
  ▼         ▼            ▼             ▼            ▼           ▼
[2hrs]    [3d]         [1d]          [2d]        [1d]        [1d]
          queue        queue         queue       actual       ship
                                                 production

Lead Time: 8.25 days
Processing Time: 10 hours (1.25 days)
VA Ratio: 15%
```

### Future State Timeline
```
Quote → Order/Credit → Flow Production → Ship
  │         │              │               │
  ▼         ▼              ▼               ▼
[2hrs]    [same day]     [same day]      [same day]

Lead Time: 1-2 days
Processing Time: 8 hours
VA Ratio: 50%+
```
