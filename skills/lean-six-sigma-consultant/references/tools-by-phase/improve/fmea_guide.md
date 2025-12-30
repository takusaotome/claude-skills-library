# FMEA (Failure Mode and Effects Analysis) Guide

## Overview

FMEA is a systematic, proactive method for identifying potential failure modes, their effects, and their causes. It helps prioritize risks and develop actions to prevent failures before they occur.

## Types of FMEA

| Type | Focus | When Used |
|------|-------|-----------|
| **Design FMEA (DFMEA)** | Product design failures | During product development |
| **Process FMEA (PFMEA)** | Process failures | During process development/improvement |
| **System FMEA** | System-level failures | For complex systems |

---

## FMEA Components

### 1. Failure Mode
**What could go wrong?**
- How could the process/product fail?
- What could go wrong at each step?
- What could deviate from specification?

**Examples**:
- Part installed incorrectly
- Dimension out of tolerance
- Missing operation
- Wrong material used

### 2. Effect
**What happens when it fails?**
- Impact on customer
- Impact on downstream operations
- Impact on product function

**Examples**:
- Product doesn't work
- Customer complaint
- Production stoppage
- Safety hazard

### 3. Severity (S)
**How bad is the effect?**

Rating scale (1-10):

| Rating | Criteria | Description |
|--------|----------|-------------|
| 10 | Hazardous | Safety issue, no warning |
| 9 | Hazardous | Safety issue, with warning |
| 8 | Very High | Product inoperable |
| 7 | High | Performance severely affected |
| 6 | Moderate | Performance degraded |
| 5 | Low | Performance moderately affected |
| 4 | Very Low | Minor performance impact |
| 3 | Minor | Nuisance, fit/finish issue |
| 2 | Very Minor | Barely noticeable |
| 1 | None | No discernible effect |

### 4. Cause
**Why would it fail?**
- Root cause of the failure mode
- What triggers the failure?

**Examples**:
- Operator error
- Equipment malfunction
- Material variation
- Unclear instructions

### 5. Occurrence (O)
**How likely is the cause?**

Rating scale (1-10):

| Rating | Probability | Cpk Equivalent | Description |
|--------|-------------|----------------|-------------|
| 10 | Very High | < 0.33 | Failure almost inevitable |
| 9 | | | |
| 8 | High | ≈ 0.33 | Frequent failures |
| 7 | | ≈ 0.51 | |
| 6 | Moderate | ≈ 0.67 | Occasional failures |
| 5 | | ≈ 0.83 | |
| 4 | | ≈ 1.00 | |
| 3 | Low | ≈ 1.17 | Few failures |
| 2 | | ≈ 1.33 | Very few failures |
| 1 | Remote | ≥ 1.67 | Failure unlikely |

### 6. Current Controls
**What prevents or detects this failure?**

**Prevention Controls**: Stop failure from occurring
- Poka-yoke (error-proofing)
- Procedures
- Training
- Design constraints

**Detection Controls**: Find failure before it reaches customer
- Inspection
- Testing
- Monitoring
- Audit

### 7. Detection (D)
**How likely is detection before customer impact?**

Rating scale (1-10):

| Rating | Likelihood | Description |
|--------|------------|-------------|
| 10 | Almost impossible | No detection method |
| 9 | Very Remote | Very unlikely to detect |
| 8 | Remote | Unlikely to detect |
| 7 | Very Low | Low chance of detection |
| 6 | Low | May detect |
| 5 | Moderate | Moderate chance |
| 4 | Moderately High | Good chance |
| 3 | High | Likely to detect |
| 2 | Very High | Very likely to detect |
| 1 | Almost Certain | Will detect |

### 8. Risk Priority Number (RPN)

**RPN = Severity × Occurrence × Detection**

- Range: 1 to 1,000
- Higher RPN = Higher priority for action

**Typical Thresholds**:
- RPN > 100-125: Action required
- RPN > 200: High priority action
- High Severity (≥8): Action regardless of RPN

---

## FMEA Process

### Step 1: Prepare
- Assemble cross-functional team
- Define scope (product/process)
- Gather relevant documentation
- Use FMEA form

### Step 2: Identify Failure Modes
For each process step or product component:
- What could go wrong?
- List all potential failure modes
- Be comprehensive

### Step 3: Determine Effects
For each failure mode:
- What is the impact?
- Who is affected?
- Rate Severity (1-10)

### Step 4: Identify Causes
For each failure mode:
- Why would this happen?
- What is the root cause?
- Rate Occurrence (1-10)

### Step 5: List Current Controls
- What prevents this failure?
- What detects this failure?
- Rate Detection (1-10)

### Step 6: Calculate RPN
RPN = S × O × D

### Step 7: Prioritize and Plan Actions
- Rank by RPN (highest first)
- Consider high Severity items
- Develop recommended actions
- Assign responsibility and timing

### Step 8: Implement and Re-evaluate
- Implement actions
- Re-score S, O, D
- Calculate new RPN
- Verify improvement

---

## FMEA Table Format

| Process Step | Failure Mode | Effect | S | Cause | O | Controls | D | RPN | Action | Owner | Due | New S | New O | New D | New RPN |
|-------------|--------------|--------|---|-------|---|----------|---|-----|--------|-------|-----|-------|-------|-------|---------|
| [Step] | [Mode] | [Effect] | [1-10] | [Cause] | [1-10] | [Controls] | [1-10] | [SxOxD] | [Action] | [Name] | [Date] | | | | |

---

## Example: Assembly Process FMEA

| Step | Failure Mode | Effect | S | Cause | O | Controls | D | RPN | Action |
|------|--------------|--------|---|-------|---|----------|---|-----|--------|
| Install screw | Missing screw | Part loose, falls off | 8 | Operator error | 5 | Visual check | 6 | 240 | Add torque verification |
| Install screw | Wrong screw | Thread damage | 6 | Similar parts | 4 | None | 8 | 192 | Separate bins, color code |
| Apply adhesive | Insufficient adhesive | Bond failure | 7 | Clogged nozzle | 3 | Weight check | 5 | 105 | PM schedule for nozzle |
| Apply adhesive | Excess adhesive | Appearance defect | 4 | No dispense control | 6 | Visual inspection | 3 | 72 | Monitor, no action |

---

## Action Types

### Reduce Severity
- Difficult to change (often design-driven)
- May require product redesign
- Add safety features

### Reduce Occurrence
**Prevention focused**:
- Improve process capability
- Add poka-yoke
- Better materials
- More training
- Improved procedures

### Reduce Detection
**Detection improvement**:
- Add inspection points
- Implement testing
- Use sensors/automation
- Earlier detection (upstream)

**Priority**: Prevention > Detection

---

## Best Practices

### Do's
- Include cross-functional team
- Be comprehensive in failure modes
- Update FMEA as changes occur
- Focus on prevention, not just detection
- Use consistent rating criteria
- Document assumptions

### Don'ts
- Don't do FMEA alone
- Don't set arbitrary RPN thresholds only
- Don't ignore high Severity items
- Don't skip re-evaluation after actions
- Don't assume one cause per failure
- Don't treat FMEA as one-time exercise

---

## When to Use FMEA in Six Sigma

### Improve Phase
- Assess risks of proposed solutions
- Identify potential failure modes of new process
- Prioritize control measures needed

### Control Phase
- Input to Control Plan
- Identify what to monitor
- Define reaction plans

### DMADV Design Phase
- Proactive risk assessment
- Design for reliability
- Build in controls from start

---

## FMEA vs. Other Tools

| Tool | Focus | Timing |
|------|-------|--------|
| FMEA | Potential failures | Proactive (before) |
| Fishbone | Problem causes | Reactive (after) |
| 5 Whys | Root cause | Reactive (after) |
| Control Plan | Monitoring | Control phase |
