# Labor Constraints Guide

## Weekly Hour Limits

| Category | Weekly Limit | Notes |
|----------|-------------|-------|
| Standard | 40 hours | Base contract hours |
| With overtime | 45-50 hours | Requires overtime approval |
| Maximum legal | 60 hours | Absolute cap in most jurisdictions |

## Consecutive Work Days

- **Standard limit**: 6 consecutive days maximum
- **Recommended**: 5 consecutive days with 2 days rest
- **Configurable**: `--max-consecutive-days` CLI flag

The algorithm enforces consecutive day limits as a **hard constraint** in the eligibility check. If an employee would exceed the limit by being assigned a new day, they are excluded from candidates.

## Minimum Rest Between Shifts

- **Standard**: 11 hours minimum between end of one shift and start of next
- **EU Working Time Directive**: 11 hours mandatory
- **Configurable**: `--min-rest-hours` CLI flag

### Calculation

```
rest_hours = (24 - end_hour_today) + start_hour_tomorrow
```

Example:
- LATE_8H ends at 19:00, EARLY_8H starts at 06:00
- Rest = (24 - 19) + 6 = 11 hours (borderline)
- With min_rest_hours=12, this combination is blocked

## Mandatory Break Requirements

| Shift Duration | Break Requirement |
|----------------|-------------------|
| <= 6 hours | No mandatory break |
| 6-8 hours | 45-minute break minimum |
| > 8 hours | 60-minute break minimum |

The built-in patterns comply with these requirements:
- FULL_8H, EARLY_8H, LATE_8H: 60-minute break (8h shift)
- SHORT_6H: No break (6h shift, at the threshold)
- HALF_4H: No break (4h shift)

## Supervisor Requirements

- At least one supervisor per room per shift is recommended
- The `need_supervisor` field in requirements.csv controls this
- SFT-W002 is emitted when no supervisor is assigned to a slot that requires one
- Supervisors are prioritized via the W_SUPERVISOR scoring weight

## Overnight Shifts

**Not supported** in the current version. Patterns with `start_hour >= end_hour` are rejected with SFT-E004.

Workaround for facilities with overnight operations:
1. Split into two shifts (e.g., evening 18:00-24:00 and morning 00:00-06:00)
2. Treat as separate days in the requirements
3. Handle the cross-day rest calculation manually

## Fair Distribution

### Weekend Shifts

Weekend shifts (SAT/SUN) are distributed using the W_WEEKEND scoring weight. Employees who already have weekend assignments are deprioritized for additional weekend slots.

SFT-W009 is emitted when the standard deviation of weekend shifts across employees exceeds 1.0.

### Hours Deviation

SFT-W004 is emitted when any employee's assigned hours deviate more than 4 hours from their contract hours. This indicates potential unfairness in workload distribution.

### Avoid Days

Avoid days are treated as **soft constraints**. Employees with avoid days are deprioritized (W_AVOID weight) but may still be assigned if no alternative exists. SFT-W003 notifies when this occurs.
