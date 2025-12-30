# Root Cause Analysis Guide

## Overview

Root Cause Analysis (RCA) is a systematic approach to identifying the fundamental cause(s) of a problem. Rather than addressing symptoms, RCA aims to find and eliminate the underlying cause to prevent recurrence.

## Key Principles

1. **Focus on systems**: Look beyond individual blame
2. **Ask "Why" repeatedly**: Dig deeper than surface causes
3. **Use data**: Support conclusions with evidence
4. **Multiple causes**: Problems often have several root causes
5. **Verify causes**: Prove cause-effect relationship

---

## Tool 1: Fishbone Diagram (Ishikawa/Cause-and-Effect)

### What It Is
A visual tool that organizes potential causes of a problem into categories, resembling a fish skeleton.

### Structure
```
                    ┌────────────────┐
                    │                │
    Man ──────────┬─┤                │
                  │ │                │
    Machine ─────┬┼─┤    PROBLEM     │
                 ││ │   (Effect)     │
    Material ───┬┼┼─┤                │
                │││ │                │
    Method ────┬┼┼┼─┤                │
               ││││ │                │
    Measure ──┬┼┼┼┼─┤                │
              │││││ │                │
    Environment┼┼┼┼┼┤                │
              │││││ └────────────────┘
              │││││
              Head                    Tail
```

### The 6M Categories

| Category | Also Called | Examples |
|----------|-------------|----------|
| **Man** | People, Personnel | Skills, training, fatigue, attention |
| **Machine** | Equipment | Age, maintenance, calibration, wear |
| **Material** | Inputs | Quality, specifications, suppliers |
| **Method** | Process | Procedures, work instructions, sequence |
| **Measurement** | Inspection | Accuracy, calibration, technique |
| **Mother Nature** | Environment | Temperature, humidity, lighting, dust |

### How to Create

**Step 1: Define the Problem**
- Write the problem (effect) in the "head" of the fish
- Be specific and quantified

**Step 2: Draw the Structure**
- Draw main spine (backbone)
- Add category branches (ribs)
- Use 6M or customize categories

**Step 3: Brainstorm Causes**
- For each category, ask: "What could cause this?"
- Add causes as sub-branches
- Don't filter or judge during brainstorming
- Add sub-causes (causes of causes)

**Step 4: Analyze**
- Circle likely root causes
- Identify areas for investigation
- Use data to verify

### Example: High Defect Rate

```
Problem: 12% defect rate on Line 3

Man
├── New operators lack training
├── Fatigue on long shifts
└── Inconsistent technique

Machine
├── Worn tooling
├── Calibration drift
└── Vibration from nearby equipment

Material
├── Supplier quality variation
├── Material storage issues
└── Incoming inspection gaps

Method
├── Work instructions unclear
├── Setup procedure varies
└── Process parameters not optimized

Measurement
├── Gage not calibrated
├── Inspection technique varies
└── Sampling insufficient

Environment
├── Temperature fluctuation
├── Humidity affects material
└── Lighting inadequate
```

---

## Tool 2: 5 Whys Analysis

### What It Is
A simple technique of repeatedly asking "Why?" to drill down from symptoms to root cause.

### How to Use

**Step 1: State the Problem**
Start with a clear problem statement.

**Step 2: Ask "Why?"**
For each answer, ask "Why?" again.

**Step 3: Continue 5 Times (or more)**
Stop when you reach a root cause that can be acted upon.

### Example: Late Shipments

```
Problem: Shipments are frequently late

Why #1: Why are shipments late?
→ Because orders are not packed in time

Why #2: Why are orders not packed in time?
→ Because picking takes too long

Why #3: Why does picking take too long?
→ Because pickers can't find items quickly

Why #4: Why can't pickers find items quickly?
→ Because inventory locations are not accurate

Why #5: Why are inventory locations not accurate?
→ Because putaway process doesn't update system

ROOT CAUSE: Putaway process doesn't update inventory system
ACTION: Implement barcode scanning for putaway with system update
```

### Multiple Paths

Sometimes 5 Whys reveals multiple root causes:

```
Problem: Machine stopped

Why? Fuse blew
├── Why? Overloaded
│   ├── Why? Bearing failed
│   │   ├── Why? Insufficient lubrication
│   │   │   └── Why? No PM schedule
│   │   │       ROOT CAUSE #1: No preventive maintenance
│   │   │
│   │   └── Why? Wrong lubricant used
│   │       └── Why? Not specified in procedure
│   │           ROOT CAUSE #2: Incomplete work instructions
```

### Guidelines

**Do's**:
- Focus on process, not people
- Follow each path to a root cause
- Support with data where possible
- Stop when you can take action
- Consider multiple paths

**Don'ts**:
- Don't stop at symptoms
- Don't blame individuals
- Don't accept vague answers
- Don't guess - verify with data
- Don't give up after 5 (may need more)

---

## Tool 3: Fault Tree Analysis (FTA)

### What It Is
A top-down, deductive analysis that maps how failures combine to cause a problem using logical gates.

### Structure

Uses logic gates:
- **AND gate**: All events must occur
- **OR gate**: Any event causes failure

### Example: System Failure

```
                System Failure
                     │
                [OR Gate]
           ┌─────────┴─────────┐
           │                    │
    Hardware Failure      Software Error
           │                    │
       [OR Gate]           [OR Gate]
     ┌────┴────┐         ┌────┴────┐
     │         │         │         │
   Power    Component   Bug      Config
   Failure   Failure            Error
```

### When to Use
- Complex systems with multiple failure modes
- Safety-critical analysis
- Understanding how failures combine
- Risk assessment

---

## Tool 4: Pareto Analysis

### What It Is
A prioritization tool based on the 80/20 rule: 80% of effects come from 20% of causes.

### How to Create

**Step 1: Categorize Problems**
List all categories of defects/problems.

**Step 2: Count Frequency**
Count occurrences in each category.

**Step 3: Sort and Calculate**
- Sort descending by frequency
- Calculate cumulative percentage

**Step 4: Create Chart**
- Bar chart showing frequency
- Line showing cumulative %

### Example: Defect Types

| Defect Type | Count | % | Cumulative % |
|-------------|-------|---|---------------|
| Scratch | 45 | 45% | 45% |
| Dimension | 25 | 25% | 70% |
| Missing part | 15 | 15% | 85% |
| Color | 8 | 8% | 93% |
| Other | 7 | 7% | 100% |
| **Total** | **100** | | |

### Interpretation
- Focus on "vital few": Scratch and Dimension cause 70% of defects
- Address these first for maximum impact

---

## Verifying Root Causes

### Why Verify?
- Brainstormed causes are hypotheses
- Must prove cause-effect with data
- Avoid solving wrong problem

### Verification Methods

**1. Data Analysis**
- Correlation: Do cause and effect move together?
- Stratification: Is problem worse when cause is present?
- Before/After: Did problem change when cause changed?

**2. Hypothesis Testing**
- t-test: Compare means when cause present/absent
- Chi-square: Compare proportions
- ANOVA: Compare multiple groups

**3. Experimentation**
- Deliberately manipulate potential cause
- Observe effect on problem
- Control other variables

### Verification Questions
- Is there data showing correlation?
- Does the cause precede the effect?
- When cause is removed, does effect decrease?
- Is there a plausible mechanism?

---

## Documentation

### Root Cause Statement

A good root cause statement:
- Describes the fundamental cause
- Explains why the problem occurred
- Points to actionable solutions
- Is verified with data

**Format**:
```
The root cause of [PROBLEM] is [ROOT CAUSE] as evidenced by [DATA/PROOF].
```

**Example**:
```
The root cause of the high defect rate (12%) is worn tooling that exceeds
the replacement criteria, as evidenced by:
- 80% of defects correlate with Tool #3 usage
- Tool measurement shows 0.15mm wear (spec: max 0.10mm)
- Defect rate dropped from 12% to 2% after tool replacement
```

---

## Common Mistakes

1. **Stopping at symptoms**: "Operator error" is not a root cause
2. **Blaming people**: Focus on systems and processes
3. **Single cause focus**: Problems often have multiple causes
4. **No verification**: Assuming causes without data
5. **Too shallow**: Not asking "Why?" enough times
6. **Too deep**: Going beyond actionable causes
7. **Skipping brainstorming**: Missing potential causes
8. **Not involving SMEs**: Missing key insights
