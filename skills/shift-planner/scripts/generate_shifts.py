"""
Shift Planner — Constraint-Satisfaction Greedy Assignment Engine

CLI and library for generating weekly employee shift schedules.
Reads roster, requirements, and optional shift-pattern CSVs, then outputs
a Markdown report with assignments, coverage matrix, fairness metrics,
and alerts.

Usage:
    python3 generate_shifts.py \
        --roster roster.csv \
        --requirements requirements.csv \
        --patterns shift_patterns.csv \
        --week-start 2026-02-23 \
        --max-consecutive-days 6 \
        --min-rest-hours 11 \
        --output shifts.md
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# =============================================================================
# Constants
# =============================================================================

DAY_ORDER = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
WEEKEND_DAYS = {"SAT", "SUN"}

# Priority score weights (fixed for determinism)
W_REMAINING = 10
W_WEEKEND = 20
W_AVOID = 50
W_SUPERVISOR = 100
W_SPECIALITY = 5
W_PREFERENCE = 30


# =============================================================================
# Data Models (9 dataclasses)
# =============================================================================


@dataclass
class Employee:
    employee_id: str
    name: str
    available_days: List[str]
    max_hours_week: float
    max_days_week: int
    qualifications: List[str]
    is_supervisor: bool
    preferred_patterns: List[str]
    avoid_days: List[str]
    contract_hours: float


@dataclass
class ShiftPattern:
    pattern_id: str
    name: str
    start_hour: float
    end_hour: float
    break_start: Optional[float]
    break_end: Optional[float]
    net_hours: float


@dataclass
class StaffRequirement:
    day: str
    room_code: str
    required_staff: int
    start_hour: float = 8.0
    end_hour: float = 17.0
    need_supervisor: int = 1


@dataclass
class ShiftAssignment:
    employee_id: str
    employee_name: str
    day: str
    room_code: str
    pattern_id: str
    start_hour: float
    end_hour: float
    break_start: Optional[float]
    break_end: Optional[float]
    net_hours: float


@dataclass
class CoverageSlot:
    day: str
    room_code: str
    time_slot_min: int  # minutes from midnight
    assigned: int
    required: int


@dataclass
class FairnessMetrics:
    employee_id: str
    employee_name: str
    hours_assigned: float
    contract_hours: float
    deviation: float
    days_assigned: int
    weekend_shifts: int
    avoid_violations: int


@dataclass
class ShiftAlert:
    level: str  # ERROR, WARNING
    code: str  # SFT-E001, SFT-W001, etc.
    message: str


@dataclass
class ShiftResult:
    assignments: List[ShiftAssignment]
    coverage: List[CoverageSlot]
    fairness: List[FairnessMetrics]
    alerts: List[ShiftAlert]
    week_start: str = ""


@dataclass
class ShiftConfig:
    max_consecutive_days: int = 6
    min_rest_hours: float = 11.0
    week_start: str = ""


# =============================================================================
# Built-in shift patterns
# =============================================================================

BUILTIN_PATTERNS = [
    ShiftPattern(
        pattern_id="FULL_8H",
        name="Full Day",
        start_hour=8.0,
        end_hour=17.0,
        break_start=12.0,
        break_end=13.0,
        net_hours=8.0,
    ),
    ShiftPattern(
        pattern_id="EARLY_8H",
        name="Early Shift",
        start_hour=6.0,
        end_hour=15.0,
        break_start=11.0,
        break_end=12.0,
        net_hours=8.0,
    ),
    ShiftPattern(
        pattern_id="LATE_8H",
        name="Late Shift",
        start_hour=10.0,
        end_hour=19.0,
        break_start=14.0,
        break_end=15.0,
        net_hours=8.0,
    ),
    ShiftPattern(
        pattern_id="SHORT_6H",
        name="Short Day",
        start_hour=8.0,
        end_hour=14.0,
        break_start=None,
        break_end=None,
        net_hours=6.0,
    ),
    ShiftPattern(
        pattern_id="HALF_4H",
        name="Half Day",
        start_hour=8.0,
        end_hour=12.0,
        break_start=None,
        break_end=None,
        net_hours=4.0,
    ),
]


# =============================================================================
# Time helpers
# =============================================================================


def _hour_to_min(hour: float) -> int:
    """Convert decimal hour to integer minutes."""
    return int(round(hour * 60))


def _format_hour(hour: float) -> str:
    """Convert decimal hour to HH:MM string."""
    total_min = _hour_to_min(hour)
    h = total_min // 60
    m = total_min % 60
    return f"{h:02d}:{m:02d}"


# =============================================================================
# Validation
# =============================================================================


def validate_inputs(
    employees: List[Employee],
    requirements: List[StaffRequirement],
    patterns: List[ShiftPattern],
) -> List[ShiftAlert]:
    """Validate all inputs before shift generation.

    Returns a list of ShiftAlert objects. Any alert with level ERROR
    means the input set is invalid and scheduling should not proceed.
    """
    alerts: List[ShiftAlert] = []

    # E008: Duplicate employee_id
    seen_ids: set = set()
    for emp in employees:
        if emp.employee_id in seen_ids:
            alerts.append(
                ShiftAlert(
                    level="ERROR",
                    code="SFT-E008",
                    message=f"Duplicate employee_id: {emp.employee_id}",
                )
            )
        seen_ids.add(emp.employee_id)

    # E001: max_hours_week <= 0
    for emp in employees:
        if emp.max_hours_week <= 0:
            alerts.append(
                ShiftAlert(
                    level="ERROR",
                    code="SFT-E001",
                    message=f"Employee {emp.employee_id}: max_hours_week must be > 0 (got {emp.max_hours_week})",
                )
            )

    # E002: max_days_week <= 0
    for emp in employees:
        if emp.max_days_week <= 0:
            alerts.append(
                ShiftAlert(
                    level="ERROR",
                    code="SFT-E002",
                    message=f"Employee {emp.employee_id}: max_days_week must be > 0 (got {emp.max_days_week})",
                )
            )

    # E005: required_staff <= 0 in requirements
    for req in requirements:
        if req.required_staff <= 0:
            alerts.append(
                ShiftAlert(
                    level="ERROR",
                    code="SFT-E005",
                    message=f"Requirement ({req.day}, {req.room_code}): required_staff must be > 0 (got {req.required_staff})",
                )
            )

    # Determine effective patterns
    effective_patterns = patterns if patterns else BUILTIN_PATTERNS

    # E003: net_hours <= 0 in patterns
    valid_patterns = []
    for p in effective_patterns:
        if p.net_hours <= 0:
            alerts.append(
                ShiftAlert(
                    level="ERROR",
                    code="SFT-E003",
                    message=f"Pattern {p.pattern_id}: net_hours must be > 0 (got {p.net_hours})",
                )
            )
        elif p.start_hour >= p.end_hour:
            alerts.append(
                ShiftAlert(
                    level="ERROR",
                    code="SFT-E004",
                    message=f"Pattern {p.pattern_id}: start_hour ({p.start_hour}) >= end_hour ({p.end_hour}). Overnight shifts not supported.",
                )
            )
        else:
            valid_patterns.append(p)

    # E007: No valid patterns
    if len(valid_patterns) == 0 and len(requirements) > 0:
        alerts.append(
            ShiftAlert(
                level="ERROR",
                code="SFT-E007",
                message="No valid shift patterns available (all patterns rejected by E003/E004).",
            )
        )

    # E006: Room with zero qualified employees (static, roster non-empty only)
    if len(employees) > 0:
        all_qualifications: set = set()
        for emp in employees:
            all_qualifications.update(emp.qualifications)

        required_rooms = {req.room_code for req in requirements}
        for room_code in sorted(required_rooms):
            if room_code not in all_qualifications:
                alerts.append(
                    ShiftAlert(
                        level="ERROR",
                        code="SFT-E006",
                        message=f"Room {room_code}: no employee has qualification for this room.",
                    )
                )

    return alerts


# =============================================================================
# Greedy Assignment Engine
# =============================================================================


def _compute_difficulty(
    req: StaffRequirement,
    employees: List[Employee],
) -> float:
    """Compute slot difficulty = required_staff / qualified_count."""
    qualified = sum(1 for emp in employees if req.room_code in emp.qualifications and req.day in emp.available_days)
    if qualified == 0:
        return float("inf")
    return req.required_staff / qualified


def _is_eligible(
    emp: Employee,
    day: str,
    room_code: str,
    pattern: ShiftPattern,
    state: Dict,
    config: ShiftConfig,
) -> bool:
    """Check hard constraints for assigning emp to (day, room, pattern)."""
    emp_state = state[emp.employee_id]

    # Available day
    if day not in emp.available_days:
        return False

    # Qualification
    if room_code not in emp.qualifications:
        return False

    # Max hours
    if emp_state["hours_assigned"] + pattern.net_hours > emp.max_hours_week:
        return False

    # Max days
    if day not in emp_state["days_set"] and len(emp_state["days_set"]) >= emp.max_days_week:
        return False

    # Already assigned this day
    if day in emp_state["days_set"]:
        return False

    # Consecutive days check
    day_idx = DAY_ORDER.index(day)
    consecutive_before = 0
    for i in range(1, config.max_consecutive_days + 1):
        prev_idx = day_idx - i
        if prev_idx < 0:
            break
        if DAY_ORDER[prev_idx] in emp_state["days_set"]:
            consecutive_before += 1
        else:
            break
    consecutive_after = 0
    for i in range(1, config.max_consecutive_days + 1):
        next_idx = day_idx + i
        if next_idx >= len(DAY_ORDER):
            break
        if DAY_ORDER[next_idx] in emp_state["days_set"]:
            consecutive_after += 1
        else:
            break
    if consecutive_before + 1 + consecutive_after > config.max_consecutive_days:
        return False

    # Min rest hours between shifts
    pattern_end_min = _hour_to_min(pattern.end_hour)
    pattern_start_min = _hour_to_min(pattern.start_hour)
    min_rest_min = _hour_to_min(config.min_rest_hours)

    # Check previous day's shift end
    if day_idx > 0:
        prev_day = DAY_ORDER[day_idx - 1]
        prev_end = emp_state.get("last_shift_end", {}).get(prev_day)
        if prev_end is not None:
            # Rest = (24h - prev_end) + pattern_start
            rest_min = (1440 - prev_end) + pattern_start_min
            if rest_min < min_rest_min:
                return False

    # Check next day's shift start
    if day_idx < len(DAY_ORDER) - 1:
        next_day = DAY_ORDER[day_idx + 1]
        next_start = emp_state.get("next_shift_start", {}).get(next_day)
        if next_start is not None:
            rest_min = (1440 - pattern_end_min) + next_start
            if rest_min < min_rest_min:
                return False

    return True


def _compute_priority_score(
    emp: Employee,
    day: str,
    pattern: ShiftPattern,
    state: Dict,
) -> Tuple[float, str]:
    """Compute priority score for sorting candidates. Lower = higher priority.

    Returns (score, employee_id) for deterministic tie-breaking.
    """
    emp_state = state[emp.employee_id]
    remaining_hours = emp.contract_hours - emp_state["hours_assigned"]

    weekend_shifts = emp_state["weekend_count"]
    avoid_penalty = 1 if day in emp.avoid_days else 0
    supervisor_bonus = 1 if emp.is_supervisor else 0
    speciality = 10 - len(emp.qualifications)
    preference_miss = 0 if (not emp.preferred_patterns or pattern.pattern_id in emp.preferred_patterns) else 1

    score = (
        -(remaining_hours * W_REMAINING)
        + (weekend_shifts * W_WEEKEND)
        + (avoid_penalty * W_AVOID)
        - (supervisor_bonus * W_SUPERVISOR)
        - (speciality * W_SPECIALITY)
        + (preference_miss * W_PREFERENCE)
    )

    return (score, emp.employee_id)


def _select_pattern(
    emp: Employee,
    req: StaffRequirement,
    patterns: List[ShiftPattern],
) -> Optional[ShiftPattern]:
    """Select best pattern for this slot. Sort by (preference_match, -cover_time, pattern_id)."""
    # Filter patterns that fit within the requirement time window
    candidates = []
    for p in patterns:
        p_start_min = _hour_to_min(p.start_hour)
        p_end_min = _hour_to_min(p.end_hour)
        req_start_min = _hour_to_min(req.start_hour)
        req_end_min = _hour_to_min(req.end_hour)

        # Pattern must overlap with requirement window
        overlap_start = max(p_start_min, req_start_min)
        overlap_end = min(p_end_min, req_end_min)
        if overlap_start >= overlap_end:
            continue
        candidates.append(p)

    if not candidates:
        return None

    def sort_key(p: ShiftPattern):
        pref_match = 0 if (emp.preferred_patterns and p.pattern_id in emp.preferred_patterns) else 1
        # Cover time = overlap with requirement window (excluding break)
        p_start_min = _hour_to_min(p.start_hour)
        p_end_min = _hour_to_min(p.end_hour)
        req_start_min = _hour_to_min(req.start_hour)
        req_end_min = _hour_to_min(req.end_hour)
        overlap_start = max(p_start_min, req_start_min)
        overlap_end = min(p_end_min, req_end_min)
        cover_min = overlap_end - overlap_start
        # Subtract break overlap
        if p.break_start is not None and p.break_end is not None:
            b_start = _hour_to_min(p.break_start)
            b_end = _hour_to_min(p.break_end)
            break_overlap_start = max(b_start, overlap_start)
            break_overlap_end = min(b_end, overlap_end)
            if break_overlap_start < break_overlap_end:
                cover_min -= break_overlap_end - break_overlap_start
        return (pref_match, -cover_min, p.pattern_id)

    candidates.sort(key=sort_key)
    return candidates[0]


def generate_shifts(
    employees: List[Employee],
    requirements: List[StaffRequirement],
    patterns: List[ShiftPattern],
    config: ShiftConfig,
) -> ShiftResult:
    """Generate weekly shift assignments using constraint-satisfaction greedy algorithm.

    Args:
        employees: Employee roster.
        requirements: Staff requirements per (day, room).
        patterns: Shift pattern definitions (empty = use builtins).
        config: Scheduling configuration.

    Returns:
        ShiftResult with assignments, coverage, fairness, and alerts.
    """
    alerts: List[ShiftAlert] = []
    assignments: List[ShiftAssignment] = []

    # Validate inputs
    validation_alerts = validate_inputs(employees, requirements, patterns)
    errors = [a for a in validation_alerts if a.level == "ERROR"]
    if errors:
        return ShiftResult(
            assignments=[],
            coverage=[],
            fairness=[],
            alerts=validation_alerts,
            week_start=config.week_start,
        )

    # Add validation warnings
    alerts.extend([a for a in validation_alerts if a.level == "WARNING"])

    # Use builtin patterns if none provided
    effective_patterns = patterns if patterns else BUILTIN_PATTERNS

    # Early return for empty requirements
    if not requirements:
        fairness = _compute_fairness(employees, assignments, alerts)
        return ShiftResult(
            assignments=assignments,
            coverage=[],
            fairness=fairness,
            alerts=alerts,
            week_start=config.week_start,
        )

    # Initialize employee state
    state: Dict[str, Dict] = {}
    for emp in employees:
        state[emp.employee_id] = {
            "hours_assigned": 0.0,
            "days_set": set(),
            "weekend_count": 0,
            "last_shift_end": {},  # day -> end_min
            "next_shift_start": {},  # day -> start_min
            "avoid_violations": 0,
            "assignments": [],
        }

    # Phase 1: Sort slots by difficulty (hardest first)
    sorted_reqs = sorted(
        requirements,
        key=lambda r: (
            -_compute_difficulty(r, employees),
            DAY_ORDER.index(r.day) if r.day in DAY_ORDER else 99,
            r.room_code,
        ),
    )

    # Phase 2: Greedy assignment loop
    # For each slot, assign required_staff employees
    slot_assignments: Dict[Tuple[str, str], List[ShiftAssignment]] = {}

    for req in sorted_reqs:
        slot_key = (req.day, req.room_code)
        slot_assignments[slot_key] = []
        assigned_count = 0

        for _ in range(req.required_staff):
            # Find eligible candidates
            candidates = []
            for emp in employees:
                # Try each pattern
                best_pattern = _select_pattern(emp, req, effective_patterns)
                if best_pattern is None:
                    continue
                if not _is_eligible(emp, req.day, req.room_code, best_pattern, state, config):
                    continue
                # Check not already assigned to this slot
                already_in_slot = any(a.employee_id == emp.employee_id for a in slot_assignments[slot_key])
                if already_in_slot:
                    continue

                score = _compute_priority_score(emp, req.day, best_pattern, state)
                candidates.append((score, emp, best_pattern))

            if not candidates:
                # W008: No candidates for this slot position
                if assigned_count == 0:
                    alerts.append(
                        ShiftAlert(
                            level="WARNING",
                            code="SFT-W008",
                            message=f"({req.day}, {req.room_code}): no eligible candidates available.",
                        )
                    )
                break

            # Sort by priority score (lower first), tie-break by employee_id
            candidates.sort(key=lambda c: c[0])
            best_score, best_emp, best_pattern = candidates[0]

            # Create assignment
            assignment = ShiftAssignment(
                employee_id=best_emp.employee_id,
                employee_name=best_emp.name,
                day=req.day,
                room_code=req.room_code,
                pattern_id=best_pattern.pattern_id,
                start_hour=best_pattern.start_hour,
                end_hour=best_pattern.end_hour,
                break_start=best_pattern.break_start,
                break_end=best_pattern.break_end,
                net_hours=best_pattern.net_hours,
            )
            assignments.append(assignment)
            slot_assignments[slot_key].append(assignment)
            assigned_count += 1

            # Update state
            emp_state = state[best_emp.employee_id]
            emp_state["hours_assigned"] += best_pattern.net_hours
            emp_state["days_set"].add(req.day)
            emp_state["last_shift_end"][req.day] = _hour_to_min(best_pattern.end_hour)
            emp_state["next_shift_start"][req.day] = _hour_to_min(best_pattern.start_hour)
            emp_state["assignments"].append(assignment)
            if req.day in WEEKEND_DAYS:
                emp_state["weekend_count"] += 1

            # W003: Avoid day violation
            if req.day in best_emp.avoid_days:
                emp_state["avoid_violations"] += 1
                alerts.append(
                    ShiftAlert(
                        level="WARNING",
                        code="SFT-W003",
                        message=f"Employee {best_emp.employee_id} assigned to avoid day {req.day} ({req.room_code}).",
                    )
                )

        # W002: Supervisor check
        if req.need_supervisor == 1 and assigned_count > 0:
            has_supervisor = any(
                a.employee_id in {e.employee_id for e in employees if e.is_supervisor}
                for a in slot_assignments[slot_key]
            )
            if not has_supervisor:
                alerts.append(
                    ShiftAlert(
                        level="WARNING",
                        code="SFT-W002",
                        message=f"({req.day}, {req.room_code}): no supervisor assigned (need_supervisor=1).",
                    )
                )

    # Phase 3: Coverage verification
    coverage = _verify_coverage(requirements, assignments, effective_patterns)
    # Check for coverage gaps
    for slot in coverage:
        if slot.assigned < slot.required:
            # Only emit one W001 per (day, room) — dedup
            pass

    # Emit W001 per (day, room) with gap
    coverage_gaps: Dict[Tuple[str, str], List[int]] = {}
    for slot in coverage:
        if slot.assigned < slot.required:
            key = (slot.day, slot.room_code)
            coverage_gaps.setdefault(key, []).append(slot.time_slot_min)

    for (day, room), gaps in sorted(coverage_gaps.items()):
        gap_times = ", ".join(_format_hour(m / 60.0) for m in gaps[:5])
        if len(gaps) > 5:
            gap_times += f" ... ({len(gaps)} slots)"
        alerts.append(
            ShiftAlert(
                level="WARNING",
                code="SFT-W001",
                message=f"Coverage gap at ({day}, {room}): {gap_times}",
            )
        )

    # Phase 4: Fairness metrics
    fairness = _compute_fairness(employees, assignments, alerts)

    # Post-audit: W006 consecutive days, W007 rest hours
    _post_audit(employees, assignments, config, alerts)

    return ShiftResult(
        assignments=assignments,
        coverage=coverage,
        fairness=fairness,
        alerts=alerts,
        week_start=config.week_start,
    )


# =============================================================================
# Coverage Verification (30-min slots)
# =============================================================================


def _verify_coverage(
    requirements: List[StaffRequirement],
    assignments: List[ShiftAssignment],
    patterns: List[ShiftPattern],
) -> List[CoverageSlot]:
    """Verify coverage at 30-minute granularity."""
    coverage: List[CoverageSlot] = []

    for req in requirements:
        req_start_min = _hour_to_min(req.start_hour)
        req_end_min = _hour_to_min(req.end_hour)

        # Generate 30-min time slots
        for t_min in range(req_start_min, req_end_min, 30):
            # Count assigned employees on duty at this time
            on_duty = 0
            for a in assignments:
                if a.day != req.day or a.room_code != req.room_code:
                    continue
                a_start = _hour_to_min(a.start_hour)
                a_end = _hour_to_min(a.end_hour)
                if a_start <= t_min < a_end:
                    # Check if on break
                    if a.break_start is not None and a.break_end is not None:
                        b_start = _hour_to_min(a.break_start)
                        b_end = _hour_to_min(a.break_end)
                        if b_start <= t_min < b_end:
                            continue  # On break
                    on_duty += 1

            coverage.append(
                CoverageSlot(
                    day=req.day,
                    room_code=req.room_code,
                    time_slot_min=t_min,
                    assigned=on_duty,
                    required=req.required_staff,
                )
            )

    return coverage


# =============================================================================
# Fairness Metrics
# =============================================================================


def _compute_fairness(
    employees: List[Employee],
    assignments: List[ShiftAssignment],
    alerts: List[ShiftAlert],
) -> List[FairnessMetrics]:
    """Compute per-employee fairness metrics."""
    fairness: List[FairnessMetrics] = []

    # Build assignment index per employee
    emp_assignments: Dict[str, List[ShiftAssignment]] = {}
    for a in assignments:
        emp_assignments.setdefault(a.employee_id, []).append(a)

    weekend_counts: List[int] = []

    for emp in employees:
        emp_assgns = emp_assignments.get(emp.employee_id, [])
        hours = sum(a.net_hours for a in emp_assgns)
        days = len({a.day for a in emp_assgns})
        weekend = sum(1 for a in emp_assgns if a.day in WEEKEND_DAYS)
        avoid_viol = sum(1 for a in emp_assgns if a.day in emp.avoid_days)
        deviation = hours - emp.contract_hours

        fm = FairnessMetrics(
            employee_id=emp.employee_id,
            employee_name=emp.name,
            hours_assigned=hours,
            contract_hours=emp.contract_hours,
            deviation=deviation,
            days_assigned=days,
            weekend_shifts=weekend,
            avoid_violations=avoid_viol,
        )
        fairness.append(fm)
        weekend_counts.append(weekend)

        # W004: Hours deviation > 4h
        if abs(deviation) > 4.0:
            alerts.append(
                ShiftAlert(
                    level="WARNING",
                    code="SFT-W004",
                    message=f"Employee {emp.employee_id}: hours deviation {deviation:+.1f}h from contract ({emp.contract_hours}h).",
                )
            )

        # W005: Zero assignments
        if hours == 0 and emp.max_hours_week > 0:
            alerts.append(
                ShiftAlert(
                    level="WARNING",
                    code="SFT-W005",
                    message=f"Employee {emp.employee_id}: no shifts assigned (idle).",
                )
            )

    # W009: Weekend shift standard deviation > 1.0
    if len(weekend_counts) >= 2:
        mean_wk = sum(weekend_counts) / len(weekend_counts)
        variance = sum((w - mean_wk) ** 2 for w in weekend_counts) / len(weekend_counts)
        std_dev = math.sqrt(variance)
        if std_dev > 1.0:
            alerts.append(
                ShiftAlert(
                    level="WARNING",
                    code="SFT-W009",
                    message=f"Weekend shift distribution uneven (std_dev={std_dev:.2f} > 1.0).",
                )
            )

    return fairness


# =============================================================================
# Post-Audit (W006, W007)
# =============================================================================


def _post_audit(
    employees: List[Employee],
    assignments: List[ShiftAssignment],
    config: ShiftConfig,
    alerts: List[ShiftAlert],
) -> None:
    """Post-audit for consecutive days and rest hours violations."""
    emp_assignments: Dict[str, List[ShiftAssignment]] = {}
    for a in assignments:
        emp_assignments.setdefault(a.employee_id, []).append(a)

    for emp in employees:
        emp_assgns = emp_assignments.get(emp.employee_id, [])
        if not emp_assgns:
            continue

        days_assigned = sorted(
            {a.day for a in emp_assgns},
            key=lambda d: DAY_ORDER.index(d),
        )

        # W006: Consecutive days check
        max_consecutive = 0
        current_streak = 0
        for day in DAY_ORDER:
            if day in days_assigned:
                current_streak += 1
                max_consecutive = max(max_consecutive, current_streak)
            else:
                current_streak = 0
        if max_consecutive > config.max_consecutive_days:
            alerts.append(
                ShiftAlert(
                    level="WARNING",
                    code="SFT-W006",
                    message=f"Employee {emp.employee_id}: {max_consecutive} consecutive days (limit {config.max_consecutive_days}).",
                )
            )

        # W007: Rest hours check
        for i in range(len(DAY_ORDER) - 1):
            curr_day = DAY_ORDER[i]
            next_day = DAY_ORDER[i + 1]
            curr_assgns = [a for a in emp_assgns if a.day == curr_day]
            next_assgns = [a for a in emp_assgns if a.day == next_day]
            if curr_assgns and next_assgns:
                curr_end = max(_hour_to_min(a.end_hour) for a in curr_assgns)
                next_start = min(_hour_to_min(a.start_hour) for a in next_assgns)
                rest_min = (1440 - curr_end) + next_start
                if rest_min < _hour_to_min(config.min_rest_hours):
                    alerts.append(
                        ShiftAlert(
                            level="WARNING",
                            code="SFT-W007",
                            message=f"Employee {emp.employee_id}: insufficient rest between {curr_day} and {next_day} ({rest_min / 60:.1f}h < {config.min_rest_hours}h).",
                        )
                    )


# =============================================================================
# CSV Parsers
# =============================================================================


def _parse_semicolons(value: str) -> List[str]:
    """Split semicolon-separated value into list, stripping whitespace."""
    if not value or not value.strip():
        return []
    return [v.strip() for v in value.split(";") if v.strip()]


def parse_roster_csv(filepath: str) -> List[Employee]:
    """Parse roster.csv file."""
    employees = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contract_str = row.get("contract_hours", "").strip()
            max_hours = float(row["max_hours_week"])
            contract_hours = float(contract_str) if contract_str else max_hours

            employees.append(
                Employee(
                    employee_id=row["employee_id"].strip(),
                    name=row["name"].strip(),
                    available_days=_parse_semicolons(row["available_days"]),
                    max_hours_week=max_hours,
                    max_days_week=int(row["max_days_week"]),
                    qualifications=_parse_semicolons(row["qualifications"]),
                    is_supervisor=int(row["is_supervisor"]) == 1,
                    preferred_patterns=_parse_semicolons(row.get("preferred_patterns", "")),
                    avoid_days=_parse_semicolons(row.get("avoid_days", "")),
                    contract_hours=contract_hours,
                )
            )
    return employees


def parse_requirements_csv(filepath: str) -> List[StaffRequirement]:
    """Parse requirements.csv file."""
    reqs = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start_str = row.get("start_hour", "").strip()
            end_str = row.get("end_hour", "").strip()
            sup_str = row.get("need_supervisor", "").strip()

            reqs.append(
                StaffRequirement(
                    day=row["day"].strip().upper(),
                    room_code=row["room_code"].strip(),
                    required_staff=int(row["required_staff"]),
                    start_hour=float(start_str) if start_str else 8.0,
                    end_hour=float(end_str) if end_str else 17.0,
                    need_supervisor=int(sup_str) if sup_str else 1,
                )
            )
    return reqs


def parse_patterns_csv(filepath: str) -> List[ShiftPattern]:
    """Parse shift_patterns.csv file."""
    patterns = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bs_str = row.get("break_start", "").strip()
            be_str = row.get("break_end", "").strip()

            patterns.append(
                ShiftPattern(
                    pattern_id=row["pattern_id"].strip(),
                    name=row["name"].strip(),
                    start_hour=float(row["start_hour"]),
                    end_hour=float(row["end_hour"]),
                    break_start=float(bs_str) if bs_str else None,
                    break_end=float(be_str) if be_str else None,
                    net_hours=float(row["net_hours"]),
                )
            )
    return patterns


# =============================================================================
# Markdown Output
# =============================================================================


def render_markdown(result: ShiftResult) -> str:
    """Render shift result as a Markdown document."""
    lines: List[str] = []
    lines.append(f"# Shift Schedule (Week of {result.week_start})")
    lines.append("")

    # Section 1: Shift Assignment Table (by day)
    lines.append("## Shift Assignments")
    lines.append("")

    by_day: Dict[str, List[ShiftAssignment]] = {}
    for a in result.assignments:
        by_day.setdefault(a.day, []).append(a)

    for day in DAY_ORDER:
        day_assgns = by_day.get(day, [])
        if not day_assgns:
            continue
        lines.append(f"### {day}")
        lines.append("")
        lines.append("| Employee | Room | Shift | Start | End | Break | Hours |")
        lines.append("|----------|------|-------|-------|-----|-------|-------|")
        day_assgns.sort(key=lambda a: (a.room_code, a.start_hour, a.employee_id))
        for a in day_assgns:
            start = _format_hour(a.start_hour)
            end = _format_hour(a.end_hour)
            brk = ""
            if a.break_start is not None and a.break_end is not None:
                brk = f"{_format_hour(a.break_start)}-{_format_hour(a.break_end)}"
            lines.append(
                f"| {a.employee_name} ({a.employee_id}) | {a.room_code} "
                f"| {a.pattern_id} | {start} | {end} | {brk} | {a.net_hours:.1f} |"
            )
        lines.append("")

    # Section 2: Coverage Matrix
    lines.append("## Coverage Matrix")
    lines.append("")

    if result.coverage:
        # Group by (day, room)
        cov_groups: Dict[Tuple[str, str], List[CoverageSlot]] = {}
        for c in result.coverage:
            cov_groups.setdefault((c.day, c.room_code), []).append(c)

        for day, room in sorted(
            cov_groups.keys(), key=lambda k: (DAY_ORDER.index(k[0]) if k[0] in DAY_ORDER else 99, k[1])
        ):
            slots = sorted(cov_groups[(day, room)], key=lambda c: c.time_slot_min)
            lines.append(f"### {day} - {room}")
            lines.append("")
            # Build time headers
            time_headers = [_format_hour(s.time_slot_min / 60.0) for s in slots]
            lines.append("| Metric | " + " | ".join(time_headers) + " |")
            lines.append("|--------" + "".join("| ---" for _ in slots) + " |")
            assigned_row = "| Assigned | " + " | ".join(str(s.assigned) for s in slots) + " |"
            required_row = "| Required | " + " | ".join(str(s.required) for s in slots) + " |"
            status_row = (
                "| Status | "
                + " | ".join("OK" if s.assigned >= s.required else f"**GAP({s.required - s.assigned})**" for s in slots)
                + " |"
            )
            lines.append(assigned_row)
            lines.append(required_row)
            lines.append(status_row)
            lines.append("")
    else:
        lines.append("No coverage data.")
        lines.append("")

    # Section 3: Fairness Report
    lines.append("## Fairness Report")
    lines.append("")

    if result.fairness:
        lines.append("| Employee | Hours | Contract | Deviation | Days | Weekend | Violations |")
        lines.append("|----------|-------|----------|-----------|------|---------|------------|")
        for fm in sorted(result.fairness, key=lambda f: f.employee_id):
            lines.append(
                f"| {fm.employee_name} ({fm.employee_id}) "
                f"| {fm.hours_assigned:.1f} | {fm.contract_hours:.1f} "
                f"| {fm.deviation:+.1f} | {fm.days_assigned} "
                f"| {fm.weekend_shifts} | {fm.avoid_violations} |"
            )
        lines.append("")
    else:
        lines.append("No fairness data.")
        lines.append("")

    # Section 4: Alerts
    lines.append("## Alerts")
    lines.append("")

    if result.alerts:
        for a in result.alerts:
            lines.append(f"- [{a.level}] {a.code}: {a.message}")
        lines.append("")
    else:
        lines.append("No alerts.")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate weekly employee shift schedules from CSV inputs.")
    parser.add_argument("--roster", required=True, help="Path to roster.csv")
    parser.add_argument("--requirements", required=True, help="Path to requirements.csv")
    parser.add_argument("--patterns", default=None, help="Path to shift_patterns.csv (optional)")
    parser.add_argument("--week-start", required=True, help="Week start date (YYYY-MM-DD)")
    parser.add_argument("--max-consecutive-days", type=int, default=6, help="Max consecutive work days (default: 6)")
    parser.add_argument(
        "--min-rest-hours", type=float, default=11.0, help="Min rest hours between shifts (default: 11.0)"
    )
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")

    args = parser.parse_args()

    # Parse CSV files
    employees = parse_roster_csv(args.roster)
    requirements = parse_requirements_csv(args.requirements)
    patterns = parse_patterns_csv(args.patterns) if args.patterns else []

    config = ShiftConfig(
        max_consecutive_days=args.max_consecutive_days,
        min_rest_hours=args.min_rest_hours,
        week_start=args.week_start,
    )

    # Generate shifts
    result = generate_shifts(employees, requirements, patterns, config)

    # Check for errors
    errors = [a for a in result.alerts if a.level == "ERROR"]
    if errors:
        print("Validation errors:", file=sys.stderr)
        for e in errors:
            print(f"  [{e.code}] {e.message}", file=sys.stderr)
        sys.exit(1)

    # Render output
    md = render_markdown(result)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Shift schedule written to {args.output}")
    else:
        print(md)


if __name__ == "__main__":
    main()
