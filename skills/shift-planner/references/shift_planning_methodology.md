# Shift Planning Methodology

## Algorithm Overview

The shift planner uses a **Constraint-Satisfaction Greedy Assignment** algorithm that operates in four phases.

### Phase 1: Slot Priority Sort

Requirements (day, room) are sorted by **fill difficulty**:

```
difficulty = required_staff / qualified_employee_count
```

Higher difficulty slots are filled first, ensuring scarce resources are allocated where they're most needed.

**Tie-breaking**: DAY_ORDER index (MON=0 first) → room_code ASC

### Phase 2: Greedy Assignment Loop

For each slot, up to `required_staff` employees are assigned:

1. **Hard constraint filter** (`is_eligible`):
   - Employee available on the day
   - Employee qualified for the room
   - Weekly hours not exceeded
   - Weekly days not exceeded
   - Not already assigned this day
   - Consecutive days limit respected
   - Minimum rest hours between shifts respected

2. **Priority scoring** (lower = higher priority):

| Weight | Component | Purpose |
|--------|-----------|---------|
| W_REMAINING = 10 | -(remaining_hours * 10) | Prioritize employees with more contract hours remaining |
| W_WEEKEND = 20 | +(weekend_shifts * 20) | Deprioritize employees who already have weekend shifts |
| W_AVOID = 50 | +(avoid_penalty * 50) | Deprioritize assigning to avoided days |
| W_SUPERVISOR = 100 | -(supervisor_bonus * 100) | Strongly prioritize supervisors for slots needing them |
| W_SPECIALITY = 5 | -(speciality * 5) | Slightly prioritize specialists (fewer qualifications) |
| W_PREFERENCE = 30 | +(preference_miss * 30) | Penalize non-preferred pattern assignments |

3. **Pattern selection** for each candidate:
   - Filter: pattern must overlap with requirement time window
   - Sort: (preference_match ASC, -cover_minutes DESC, pattern_id ASC)

4. **Determinism guarantee**:
   - All sort keys terminate with a string ID (employee_id or pattern_id)
   - Fixed weight constants (no randomization)
   - Identical input always produces identical output

### Phase 3: Coverage Verification

30-minute granularity check:

```
for each (day, room) in requirements:
    for t in range(start_min, end_min, step=30):
        assigned = count employees on duty at time t (excluding breaks)
        if assigned < required:
            emit SFT-W001
```

Break exclusion: employees on break (break_start <= t < break_end) are not counted.

### Phase 4: Fairness Metrics

Per-employee metrics:
- **hours_assigned**: Total net hours for the week
- **deviation**: hours_assigned - contract_hours (positive = over, negative = under)
- **weekend_shifts**: Count of SAT/SUN assignments
- **avoid_violations**: Count of assignments on avoided days

Aggregate metrics:
- **Weekend std_dev**: Standard deviation of weekend shift counts across all employees. SFT-W009 if > 1.0.

---

## Internal Time Representation

All float hour values are converted to **integer minutes** for computation:

```python
def _hour_to_min(hour: float) -> int:
    return int(round(hour * 60))
```

This eliminates floating-point boundary errors (e.g., 8.5 hours → 510 minutes exactly).

Display conversion uses `_format_hour()` to convert back to HH:MM format.

---

## Improvement Techniques

### When Coverage Gaps Exist (SFT-W001)

1. Add more employees with relevant qualifications
2. Adjust shift patterns to better cover the requirement window
3. Reduce required_staff if possible
4. Split requirements into shorter time windows

### When Fairness Issues Exist (SFT-W004, SFT-W009)

1. Balance contract_hours across employees
2. Add more weekend-available employees
3. Rotate avoided days across weeks (manual adjustment)

### When Supervisor Shortages Exist (SFT-W002)

1. Train more supervisors (cross-training)
2. Adjust requirement's need_supervisor flag where appropriate
3. Ensure supervisor available_days cover all required days
