# Control Plan Guide

## Overview

A Control Plan is a document that describes the actions required to control a process and maintain improvements. It specifies what to monitor, how to measure, and what to do when things go wrong.

## Purpose

- Document how to maintain process performance
- Specify monitoring and measurement requirements
- Define response actions for out-of-control conditions
- Transfer ownership from project team to process owner
- Serve as reference for operators and supervisors

---

## Control Plan Elements

### 1. Process Information

**Header Section**:
- Process name
- Product/service
- Process owner
- Effective date
- Revision history

### 2. Process Step/Parameter

**What to Control**:
- Critical process inputs (Xs)
- Critical process outputs (Ys)
- Key process parameters

**Selection Criteria**:
- Linked to project's verified root causes
- Critical to Quality (CTQ)
- High risk (from FMEA)
- Requires ongoing monitoring

### 3. Specification/Requirement

**What is the target?**:
- Target value
- Tolerance (±)
- Upper Specification Limit (USL)
- Lower Specification Limit (LSL)
- Nominal is Best / Smaller is Better / Larger is Better

### 4. Measurement Method

**How to Measure**:
- Measurement equipment/gage
- Measurement technique
- Operational definition
- Reference to MSA if available

### 5. Sample Size and Frequency

**How Much and How Often**:
- Sample size (n)
- Sampling frequency
- Subgroup size for control charts

**Examples**:
| Application | Sample Size | Frequency |
|-------------|-------------|-----------|
| Production line | 5 units | Every hour |
| Service process | 20 transactions | Daily |
| Administrative | 100% audit | Weekly |

### 6. Control Method

**How to Monitor**:
- Control chart type (X-bar/R, P-chart, etc.)
- Go/No-Go gaging
- Checklist/audit
- Automated monitoring
- Visual inspection

### 7. Reaction Plan

**What to Do When Out of Control**:
- Immediate actions
- Containment steps
- Investigation process
- Escalation path
- Documentation requirements

### 8. Responsible Person

**Who is Accountable**:
- Operator (performs check)
- Supervisor (responds to issues)
- Process owner (overall accountability)

---

## Control Plan Template

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           CONTROL PLAN                                      │
├────────────────────────────────────────────────────────────────────────────┤
│ Process: _________________________ Process Owner: _________________________  │
│ Product: _________________________ Effective Date: _______________________  │
│ Revision: ________________________ Approved By: __________________________  │
├─────┬─────────┬────────┬──────────┬─────────┬────────┬────────┬───────────┤
│ #   │ Step/   │ Spec/  │ Measure  │ Sample  │Control │Reaction│ Respon-   │
│     │ Param   │ Target │ Method   │ Size/   │ Method │ Plan   │ sible     │
│     │         │        │          │ Freq    │        │        │           │
├─────┼─────────┼────────┼──────────┼─────────┼────────┼────────┼───────────┤
│ 1   │         │        │          │         │        │        │           │
├─────┼─────────┼────────┼──────────┼─────────┼────────┼────────┼───────────┤
│ 2   │         │        │          │         │        │        │           │
├─────┼─────────┼────────┼──────────┼─────────┼────────┼────────┼───────────┤
│ 3   │         │        │          │         │        │        │           │
└─────┴─────────┴────────┴──────────┴─────────┴────────┴────────┴───────────┘
```

---

## Example: Manufacturing Control Plan

| # | Step/Parameter | Specification | Measure Method | Sample | Control Method | Reaction Plan | Responsible |
|---|----------------|---------------|----------------|--------|----------------|---------------|-------------|
| 1 | Incoming Material Hardness | 58-62 HRC | Rockwell tester | 5 pcs/lot | Acceptance sampling | Quarantine, notify supplier | QC Inspector |
| 2 | Machine Temperature | 180°C ± 5°C | Thermocouple display | Continuous | SPC I-MR chart | Adjust setpoint, notify supervisor if >2σ | Operator |
| 3 | Cycle Time | ≤ 45 sec | Automated timer | 100% | Process monitoring | Stop if > 60 sec, call maintenance | Operator |
| 4 | Final Dimension | 10.0 ± 0.1 mm | Caliper (ID: CAL-001) | 5 pcs/hr | X-bar/R chart | Quarantine lot, investigate, adjust process | Operator |
| 5 | Visual Defects | Zero defects | Visual inspection | 100% | Go/No-Go | Segregate defects, log in system | Operator |

---

## Example: Service Process Control Plan

| # | Step/Parameter | Specification | Measure Method | Sample | Control Method | Reaction Plan | Responsible |
|---|----------------|---------------|----------------|--------|----------------|---------------|-------------|
| 1 | Order Completeness | 100% required fields | System validation | 100% | Automated reject | Return to customer service | System |
| 2 | Processing Time | ≤ 4 hours | Timestamp calculation | All orders | Daily report | Escalate if >8 hrs | Supervisor |
| 3 | Error Rate | ≤ 2% | QC audit sample | 50/day | P-chart (weekly) | Root cause analysis if >4% | QC Lead |
| 4 | Customer Callbacks | ≤ 5% | CRM tracking | All | Weekly trend | Process review if >8% | Manager |

---

## Reaction Plan Detail

### Structure of Reaction Plan

**Immediate Response**:
1. Stop/contain (if necessary)
2. Identify affected product/service
3. Document the issue

**Investigation**:
1. Determine scope of impact
2. Identify root cause
3. Implement correction

**Communication**:
1. Notify supervisor
2. Escalate if required
3. Document actions taken

### Reaction Plan Example

```
REACTION PLAN: Final Dimension Out of Specification

IMMEDIATE (Within 15 minutes):
1. Stop production
2. Quarantine last 1 hour of production
3. Record readings and time on Control Chart

INVESTIGATION (Within 1 hour):
1. Check tool condition
2. Verify machine settings
3. Review material lot
4. Identify root cause

CORRECTIVE ACTION:
1. If tool wear: Replace tool, verify first piece
2. If settings drift: Adjust and verify
3. If material issue: Segregate lot, notify QC

DOCUMENTATION:
1. Complete Nonconformance Report
2. Update Control Chart with notes
3. Log in Corrective Action system if repeat issue

ESCALATION:
- Notify Supervisor immediately
- Notify Quality Manager if >3 occurrences/week
- Notify Engineering if root cause unclear
```

---

## Control Plan Development Process

### Step 1: Identify What to Control
- Review verified root causes from Analyze
- Review FMEA high-risk items
- Identify CTQs and key process parameters

### Step 2: Determine Specifications
- Use customer requirements (CTQs)
- Use process capability data
- Consider current performance

### Step 3: Define Measurement Method
- Reference MSA results
- Specify tools and techniques
- Document operational definitions

### Step 4: Set Sample Size and Frequency
- Based on risk level
- Consider process stability
- Balance cost vs. detection ability

### Step 5: Select Control Method
- Match to data type
- Consider automation potential
- Ensure practical implementation

### Step 6: Develop Reaction Plans
- Cover all out-of-control scenarios
- Include clear escalation paths
- Ensure plans are actionable

### Step 7: Assign Responsibility
- Clear ownership for each item
- Training on responsibilities
- Backup/coverage plan

### Step 8: Review and Approve
- Process owner sign-off
- Stakeholder review
- Training verification

---

## Linking FMEA to Control Plan

| FMEA Input | Control Plan Output |
|------------|---------------------|
| High RPN items | Priority control items |
| Prevention controls | Process controls |
| Detection controls | Measurement methods |
| Recommended actions | Reaction plans |

---

## Control Plan Maintenance

### Review Triggers
- Process change
- Equipment change
- Product change
- Quality issue occurrence
- Regular scheduled review (annual)

### Update Process
1. Identify needed change
2. Draft revision
3. Review with stakeholders
4. Approve changes
5. Train affected personnel
6. Update effective date
7. Archive previous version

---

## Common Mistakes

1. **Too detailed**: Overwhelming, not followed
2. **Too vague**: Doesn't provide clear guidance
3. **No reaction plans**: Doesn't say what to do
4. **Not maintained**: Becomes outdated
5. **Not trained**: Operators don't know it exists
6. **No ownership**: Nobody accountable
7. **Disconnected from FMEA**: Misses risks
8. **Unrealistic frequency**: Can't sustain monitoring
