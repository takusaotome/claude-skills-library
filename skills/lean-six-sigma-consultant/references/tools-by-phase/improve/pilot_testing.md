# Pilot Testing Guide

## Overview

A pilot test is a small-scale trial of proposed solutions before full implementation. It validates that solutions work in practice and identifies issues before broad rollout.

## Purpose

- **Validate**: Confirm solution actually works
- **Refine**: Identify and fix problems
- **Learn**: Understand implementation challenges
- **De-risk**: Reduce risk of full-scale failure
- **Build support**: Generate evidence for stakeholders

---

## When to Pilot

### Always Pilot When
- Solution is new or unproven
- High risk if solution fails
- Significant investment required
- Complex implementation
- Organizational change involved
- Skeptical stakeholders

### May Skip Pilot When
- Solution is proven elsewhere
- Risk is very low
- Simple, easily reversible change
- Time-critical situation
- Very limited scope

---

## Pilot Planning

### Step 1: Define Pilot Scope

**Boundaries**:
- Which products/services?
- Which locations/departments?
- Which time period?
- Which personnel?

**Example Scope Statement**:
```
The pilot will run on Production Line 3 (Shift 1 only) for the week
of March 15-21, covering Product SKU A and B only.
```

### Step 2: Define Success Criteria

**Primary Metric**:
- Same metric as project (Y)
- What constitutes success?

**Secondary Metrics**:
- Other outcomes to monitor
- Unintended consequences

**Example Success Criteria**:
```
Success: Defect rate ≤ 4% (current baseline: 12%, target: 2%)
Secondary: Cycle time ≤ 50 minutes (no increase from current 45 min)
Failure: Any safety incident, defect rate > 12%
```

### Step 3: Plan Data Collection

**Before Pilot**:
- Baseline measurements
- Current state documentation

**During Pilot**:
- Pilot measurements
- Issues/observations log
- Participant feedback

**After Pilot**:
- Before/After comparison
- Statistical analysis
- Lessons learned

### Step 4: Prepare for Pilot

**Documentation**:
- Updated work instructions
- Training materials
- Data collection forms
- Issue escalation process

**Training**:
- Train pilot participants
- Explain purpose and process
- Define roles and responsibilities

**Communication**:
- Inform affected stakeholders
- Clarify support channels
- Set expectations

### Step 5: Define Contingency Plan

**Questions to Answer**:
- How do we know if pilot is failing?
- What triggers stopping the pilot?
- How do we revert to original process?
- Who makes the stop decision?

**Example Contingency**:
```
Stop Criteria:
- Defect rate exceeds 15%
- Any safety incident occurs
- Critical equipment failure

Revert Process:
- Notify supervisor immediately
- Switch to original procedure
- Document what happened
- Notify project team within 2 hours
```

---

## Pilot Execution

### During the Pilot

**Daily Activities**:
- Collect data per plan
- Monitor for issues
- Address problems quickly
- Log observations
- Communicate status

**Monitoring Checklist**:
- [ ] Data collection on track
- [ ] No safety issues
- [ ] Performance within expected range
- [ ] Participants engaged
- [ ] Issues documented
- [ ] Support available

### Issues and Adjustments

**Types of Issues**:
- Implementation problems (training, procedures)
- Solution problems (doesn't work as expected)
- Unintended consequences
- External factors

**Response Options**:
1. **Continue**: Issue is minor, document and continue
2. **Adjust**: Modify solution mid-pilot
3. **Pause**: Temporarily halt to address issue
4. **Stop**: Abort pilot, revert to baseline

---

## Pilot Evaluation

### Data Analysis

**Before vs. After Comparison**:
| Metric | Before (Baseline) | Pilot | Change |
|--------|------------------|-------|--------|
| Defect Rate | 12% | 3.5% | -71% |
| Cycle Time | 45 min | 47 min | +4% |

**Statistical Verification**:
- Is improvement statistically significant?
- Use appropriate test (t-test, proportion test)
- Report confidence interval

### Qualitative Evaluation

**Participant Feedback**:
- What worked well?
- What was difficult?
- Suggestions for improvement?
- Would they continue using it?

**Observation Notes**:
- Implementation challenges
- Unexpected benefits
- Sustainability concerns

### Go/No-Go Decision

**Go (Proceed to Full Implementation)**:
- Success criteria met
- Issues are manageable
- Stakeholders supportive

**No-Go (Do Not Proceed)**:
- Success criteria not met
- Serious issues discovered
- Solution fundamentally flawed

**Conditional Go (Proceed with Modifications)**:
- Partial success
- Issues can be addressed
- Modifications needed before rollout

---

## Pilot Report

### Report Structure

```
PILOT TEST REPORT
=================

1. OVERVIEW
   - Pilot scope and timeline
   - Solution tested
   - Objectives

2. METHODOLOGY
   - Data collection approach
   - Sample size
   - Analysis methods

3. RESULTS
   - Primary metric results
   - Secondary metric results
   - Statistical analysis
   - Before/After comparison

4. OBSERVATIONS
   - What worked well
   - Issues encountered
   - Participant feedback

5. LESSONS LEARNED
   - Key insights
   - Modifications needed

6. RECOMMENDATION
   - Go / No-Go / Conditional Go
   - Rationale
   - Next steps

7. APPENDICES
   - Data summary
   - Feedback forms
   - Issue log
```

---

## Scale-Up Planning

### Scaling from Pilot

**Considerations**:
- What worked in pilot that must be replicated?
- What modifications needed for scale?
- What additional training required?
- What resources needed for full rollout?
- What timeline is realistic?

### Phased Rollout

**Option 1: Big Bang**
- All at once
- Fast but risky
- Use when: Proven solution, low risk

**Option 2: Phased**
- Roll out in stages
- More controlled
- Use when: Complex solution, high risk

**Option 3: Geographic/Unit**
- Location by location
- Allows learning between phases
- Use when: Multiple sites, variation expected

### Scale-Up Checklist

- [ ] Pilot results documented
- [ ] Lessons incorporated into plan
- [ ] Work instructions updated
- [ ] Training program developed
- [ ] Resources allocated
- [ ] Timeline established
- [ ] Communication plan ready
- [ ] Support structure in place
- [ ] Measurement plan for rollout
- [ ] Control plan prepared

---

## Common Mistakes

1. **Scope too large**: Pilot should be limited
2. **No baseline**: Can't measure improvement
3. **No success criteria**: Don't know if it worked
4. **Not representative**: Pilot conditions differ from reality
5. **Ignoring issues**: Problems swept under rug
6. **Declaring success too early**: Insufficient pilot duration
7. **No contingency plan**: Not prepared if things go wrong
8. **Poor documentation**: Lessons not captured
9. **Hawthorne effect**: Extra attention skews results
10. **Scaling without learning**: Replicating pilot mistakes
