# Staff Planning Guide

## Table of Contents
- [Staff Requirement Calculation](#staff-requirement-calculation)
- [Shift Pattern Design](#shift-pattern-design)
- [Coverage Verification](#coverage-verification)
- [Labor Constraints](#labor-constraints)

---

## Staff Requirement Calculation

### Pipeline Overview

The staff requirement calculation follows a 4-step pipeline:

```
staff-hours -> peak -> min -> recommended
```

Each step builds on the previous, progressively refining the estimate from raw workload to actionable staffing numbers.

### Step 1: Staff-Hours Aggregation

Calculate total staff-hours required per room per day from the generated schedule:

```
staff_hours[room][day] = sum(
    (task.duration_minutes * task.required_staff) / 60
    for task in schedule
    if task.room == room and task.day == day
)
```

This gives the total person-hours of productive work needed.

### Step 2: Peak Staff Calculation

Determine the maximum number of staff needed simultaneously at any point during the day:

```
peak_staff[room][day] = max(
    sum(task.required_staff for task in active_tasks_at_time_t)
    for t in time_slots
)
```

Peak staff is always >= the maximum `required_staff` of any single task, but can be higher when tasks overlap in time.

### Step 3: Minimum Staff

The minimum staff count equals the peak requirement:

```
min_staff[room][day] = peak_staff[room][day]
```

This is the absolute minimum needed to execute the schedule without delays. Operating at minimum has no margin for error.

### Step 4: Recommended Staff

Apply a buffer coefficient to account for real-world variability:

```
recommended_staff = ceil(min_staff * buffer_coefficient)
```

**Buffer coefficient guidelines:**

| Scenario | Coefficient | Rationale |
|----------|-------------|-----------|
| Stable, experienced team | 1.05 | Minimal buffer for minor disruptions |
| Standard operations | 1.10 | Default; accounts for typical variability |
| New team or high turnover | 1.20 | Extra margin for training and ramp-up |
| Peak season or new products | 1.15 | Additional buffer for learning curve |
| Critical products (no stockout tolerance) | 1.20 | Safety margin for mission-critical items |

### Capacity Clamping

If recommended_staff exceeds the room's max_staff:

```
if recommended_staff > max_staff:
    recommended_staff = max_staff
    alert PSO-W005
```

This indicates a fundamental capacity issue that may require:
- Splitting tasks across multiple shifts
- Adding another room
- Reducing production volume

---

## Shift Pattern Design

### Standard Patterns

| Pattern ID | Name | Start | End | Break | Net Hours | Use Case |
|-----------|------|-------|-----|-------|-----------|----------|
| FULL_8H | Full Day | 08:00 | 17:00 | 12:00-13:00 | 8.0h | Standard weekday |
| EARLY_8H | Early Shift | 06:00 | 15:00 | 11:00-12:00 | 8.0h | Products needed by morning delivery |
| LATE_8H | Late Shift | 10:00 | 19:00 | 14:00-15:00 | 8.0h | Afternoon/evening production |
| SHORT_6H | Short Day | 08:00 | 14:00 | None | 6.0h | Weekend or reduced volume days |
| HALF_4H | Half Day | 08:00 | 12:00 | None | 4.0h | Peak-hour reinforcement |

### Selecting Shift Patterns

1. **Start with FULL_8H** for all weekday assignments
2. **Use SHORT_6H** for weekend days with reduced volume
3. **Add EARLY_8H** if products must be ready for early morning delivery
4. **Add LATE_8H** if afternoon production extends beyond 17:00
5. **Add HALF_4H** as supplemental coverage for peak hours only

### Multi-Shift Scenarios

For rooms that require more than max_staff across a full day, consider split shifts:

```
Shift A: EARLY_8H (06:00-15:00) - 3 staff
Shift B: LATE_8H  (10:00-19:00) - 2 staff
Overlap: 10:00-15:00 - 5 staff (handles peak concurrent tasks)
```

### Break Scheduling

- Breaks are mandatory for shifts > 6 hours (labor law compliance)
- Standard break: 60 minutes (lunch)
- Break times should not overlap with peak production periods
- Stagger breaks across staff to maintain minimum coverage

---

## Coverage Verification

### Hour-by-Hour Check

For each hour of the operating window, verify that assigned staff meets or exceeds the requirement:

```
for hour in range(shift_start, shift_end):
    assigned = count_staff_on_shift(room, day, hour)  # excluding those on break
    required = count_required_staff(room, day, hour)   # from schedule

    if assigned < required:
        gap = required - assigned
        alert PSO-W006: "Coverage gap: {room} {day} {hour}:00 - need {gap} more"
```

### Coverage Matrix

The output is a matrix showing assigned vs. required at each hour:

```
Room: BAKERY | Day: MON
Hour:    06  07  08  09  10  11  12  13  14  15  16  17
Assign:   0   0   3   3   3   3   0   3   3   3   3   0
Require:  0   0   2   2   2   3   0   2   2   2   1   0
Status:   -   -   OK  OK  OK  OK  -   OK  OK  OK  OK  -
```

### Gap Detection Severity

| Gap Size | Severity | Impact |
|----------|----------|--------|
| 1 person | Minor | Possible slowdown; tasks may take longer |
| 2 persons | Major | Some tasks cannot run concurrently; schedule delays likely |
| 3+ persons | Critical | Multiple tasks must be deferred; schedule infeasible |

### Gap Resolution Strategies

1. **Hire additional staff** for the specific time slot (HALF_4H shift)
2. **Move tasks** to adjacent time slots with surplus coverage
3. **Reassign staff** from under-utilized rooms (if cross-trained)
4. **Reschedule tasks** to a different day with available capacity

---

## Labor Constraints

### Mandatory Break Requirements

Standard labor regulations require:

| Shift Duration | Break Requirement |
|----------------|-------------------|
| <= 6 hours | No mandatory break |
| 6-8 hours | 45-minute break minimum |
| > 8 hours | 60-minute break minimum |

Breaks must be scheduled during the shift, not at the start or end.

### Maximum Continuous Work

- Maximum continuous work without break: 4-5 hours (varies by jurisdiction)
- After 4 hours of continuous work, a 15-minute rest is recommended
- Plan production tasks in blocks of 3-4 hours with natural transition points

### Weekly Hour Limits

| Category | Weekly Limit | Notes |
|----------|-------------|-------|
| Standard | 40 hours | Base contract hours |
| With overtime | 45-50 hours | Requires overtime approval |
| Maximum legal | 60 hours | Absolute cap in most jurisdictions |

### Overtime Considerations

When recommended_staff exceeds available staff:

1. **Preferred**: Adjust schedule to reduce peak requirements
2. **Acceptable**: Schedule overtime for existing staff (within legal limits)
3. **Last resort**: Hire temporary staff or outsource production

Overtime cost is typically 1.25-1.5x base rate. Factor this into cost optimization when evaluating schedule alternatives.

### Skill Requirements

Not all staff are interchangeable. Consider:

- **Certification**: HACCP-trained staff required for certain rooms
- **Experience level**: Complex products may need senior staff
- **Cross-training**: Staff trained for multiple rooms increase scheduling flexibility
- **Supervision**: At least one supervisor per shift per room for quality assurance

Track staff qualifications in a separate staff skills matrix and validate against task requirements during scheduling.
