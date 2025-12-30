# Voice of Customer (VOC) and CTQ Guide

## Overview

Voice of Customer (VOC) captures what customers want and need from a product or service. Critical to Quality (CTQ) translates those needs into specific, measurable requirements that the process must meet.

## The VOC to CTQ Flow

```
VOC (What customers say)
    ↓
Customer Needs (What they actually need)
    ↓
Drivers (Key factors)
    ↓
CTQs (Measurable specifications)
```

---

## Part 1: Voice of Customer (VOC)

### What is VOC?

VOC is the customer's voice expressing their needs, wants, and expectations regarding a product or service. It includes:

- **Stated needs**: What customers explicitly tell us
- **Implied needs**: What they expect but don't say
- **Latent needs**: Needs they don't know they have

### Why Collect VOC?

- Ensure improvements matter to customers
- Prioritize what to focus on
- Set meaningful targets
- Avoid solving the wrong problem
- Build customer-centric culture

### VOC Collection Methods

#### 1. Interviews
**Best for**: Deep understanding, complex needs

**Guidelines**:
- Use open-ended questions
- Listen more than talk
- Probe for underlying needs
- Record and transcribe

**Sample Questions**:
- "What is most important to you when using [product/service]?"
- "What frustrates you most about the current process?"
- "If you could change one thing, what would it be?"
- "Tell me about a time when [experience] went well/poorly."

#### 2. Surveys
**Best for**: Large population, quantitative data

**Guidelines**:
- Keep surveys short (< 10 questions)
- Use mix of closed and open questions
- Include rating scales for prioritization
- Test before deploying

**Sample Survey Questions**:
```
On a scale of 1-5, how important is [attribute] to you?
[ ] 1-Not important  [ ] 2  [ ] 3-Neutral  [ ] 4  [ ] 5-Very important

How satisfied are you with [attribute] today?
[ ] 1-Very dissatisfied  [ ] 2  [ ] 3-Neutral  [ ] 4  [ ] 5-Very satisfied
```

#### 3. Focus Groups
**Best for**: Exploring ideas, group dynamics

**Guidelines**:
- 6-10 participants
- Skilled facilitator
- Structured discussion guide
- Record for later analysis

#### 4. Complaint Analysis
**Best for**: Understanding failures

**Data Sources**:
- Customer service logs
- Return/refund data
- Social media complaints
- Online reviews

#### 5. Observation
**Best for**: Understanding actual behavior

**Guidelines**:
- Watch customers use product/service
- Note pain points
- Ask clarifying questions
- Document systematically

#### 6. Data Mining
**Best for**: Patterns in existing data

**Sources**:
- Transaction records
- Usage data
- Support tickets
- Website analytics

### VOC Analysis

#### Affinity Diagram
Group similar VOC statements:

```
Delivery Speed          |  Product Quality       |  Customer Service
- "Takes too long"      |  - "Product arrived    |  - "Hard to reach
- "I need it faster"    |    damaged"            |    support"
- "Next-day would       |  - "Quality varies"    |  - "Wait times are
  be great"             |  - "Doesn't match      |    too long"
                        |    description"        |
```

#### Prioritization
Use importance vs. satisfaction matrix:

```
                    Low Satisfaction    High Satisfaction
High Importance     [PRIORITY 1]        [Maintain]
Low Importance      [Priority 2]        [Low priority]
```

---

## Part 2: Critical to Quality (CTQ)

### What is CTQ?

CTQ (Critical to Quality) is a measurable characteristic of a product or process that must be met to satisfy customer requirements. CTQs translate the voice of customer into specific, measurable targets.

### CTQ Characteristics

Good CTQs are:
- **Measurable**: Can be quantified
- **Specific**: Clear what to measure
- **Achievable**: Realistic to achieve
- **Customer-driven**: Linked to VOC
- **Actionable**: Can be improved

### CTQ Tree Structure

```
Customer Need (VOC)
├── Driver 1
│   ├── CTQ 1.1 [Measurable]
│   └── CTQ 1.2 [Measurable]
├── Driver 2
│   ├── CTQ 2.1 [Measurable]
│   └── CTQ 2.2 [Measurable]
└── Driver 3
    └── CTQ 3.1 [Measurable]
```

### How to Develop CTQs

#### Step 1: Identify Customer Need
Start with VOC statement:
> "I want fast delivery"

#### Step 2: Identify Drivers
What drives that need?
- Delivery time
- Delivery reliability
- Tracking visibility

#### Step 3: Define CTQs
For each driver, create measurable specifications:

| Driver | CTQ | Specification |
|--------|-----|---------------|
| Delivery time | Order-to-delivery time | ≤ 2 days |
| Delivery reliability | On-time delivery rate | ≥ 98% |
| Tracking visibility | Tracking update frequency | Every 4 hours |

### CTQ Examples by Industry

#### Manufacturing
| VOC | Driver | CTQ | Specification |
|-----|--------|-----|---------------|
| "Product works correctly" | Functionality | Defect rate | ≤ 0.1% |
| "Consistent quality" | Reliability | Process capability | Cpk ≥ 1.33 |
| "Fits properly" | Dimensions | Dimensional accuracy | ± 0.01 mm |

#### Service
| VOC | Driver | CTQ | Specification |
|-----|--------|-----|---------------|
| "Don't make me wait" | Response time | Call answer time | ≤ 30 seconds |
| "Get it right the first time" | Accuracy | First call resolution | ≥ 85% |
| "Easy to work with" | Simplicity | Steps to complete | ≤ 3 steps |

#### Healthcare
| VOC | Driver | CTQ | Specification |
|-----|--------|-----|---------------|
| "See doctor quickly" | Access | Wait time | ≤ 15 minutes |
| "Safe treatment" | Safety | Medication error rate | 0 errors |
| "Clear communication" | Information | Patient understanding | 100% informed |

### CTQ Specification Types

#### Single-Sided Specification
Only upper or lower limit matters:
- **USL only**: "Delivery time ≤ 2 days" (lower is better)
- **LSL only**: "Uptime ≥ 99.9%" (higher is better)

#### Two-Sided Specification
Both limits matter:
- "Dimension = 10.0 mm ± 0.1 mm" (USL = 10.1, LSL = 9.9)
- "Temperature = 72°F ± 2°F"

#### Target-Based Specification
Nominal is best:
- "Fill volume = 500 ml (target), ± 5 ml acceptable"

### CTQ Validation

Before finalizing CTQs, validate:

1. **Customer validation**: Confirm CTQ reflects actual need
2. **Measurability**: Confirm we can measure it
3. **Achievability**: Confirm target is realistic
4. **Business alignment**: Confirm it matters to the business

### CTQ Selection Criteria

Prioritize CTQs that are:
- Highest customer importance
- Largest current gap (low satisfaction)
- Impactful to business
- Measurable with available data
- Within project scope

---

## Part 3: Connecting VOC, CTQ, and Project

### CTQ Becomes Primary Metric (Y)

The most important CTQ often becomes the project's primary metric:

```
VOC: "Orders take too long"
↓
CTQ: Order-to-delivery time ≤ 2 days
↓
Primary Metric (Y): Average order-to-delivery time
  Baseline: 5.2 days
  Target: 2.0 days
```

### CTQ Drives Process Focus

The CTQ tells us what to measure and improve:

```
CTQ: Defect rate ≤ 0.1%
↓
Focus: What causes defects? (Root cause analysis in Analyze phase)
↓
Improvement: Reduce causes of defects
```

### Multiple CTQs

If multiple CTQs exist:
1. Prioritize based on importance and gap
2. Select 1-2 primary CTQs for the project
3. Others become secondary metrics or future projects

---

## Common Mistakes

### VOC Mistakes
1. **Assuming you know**: Not actually asking customers
2. **Leading questions**: Biasing responses
3. **Wrong customers**: Asking non-representative sample
4. **Not digging deeper**: Accepting surface-level answers
5. **Ignoring implied needs**: Only capturing stated needs

### CTQ Mistakes
1. **Not measurable**: "Make customers happy" - how do you measure?
2. **Too vague**: "Good quality" - need specific metric
3. **Internal focus**: Measure what matters to company, not customer
4. **Impossible target**: Specification can't be achieved
5. **Too many CTQs**: Dilutes focus - prioritize!

---

## Tools and Templates

### VOC Collection Template

| Customer Segment | VOC Statement | Need Category | Importance (1-5) |
|-----------------|---------------|---------------|------------------|
| [Segment] | "[Quote]" | [Category] | [Rating] |

### CTQ Tree Template

```
Need: [Customer need statement]
├── Driver: [Driver 1]
│   └── CTQ: [Measurable requirement]
│       └── Spec: [Target and tolerance]
├── Driver: [Driver 2]
│   └── CTQ: [Measurable requirement]
│       └── Spec: [Target and tolerance]
```

### CTQ Summary Table

| VOC | Driver | CTQ | Measurement | LSL | Target | USL |
|-----|--------|-----|-------------|-----|--------|-----|
| [Voice] | [Driver] | [CTQ name] | [How measured] | [Lower] | [Target] | [Upper] |
