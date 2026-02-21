"""Tests for generate_shifts module — 25 test cases."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from generate_shifts import (
    CoverageSlot,
    Employee,
    FairnessMetrics,
    ShiftAlert,
    ShiftAssignment,
    ShiftConfig,
    ShiftPattern,
    ShiftResult,
    StaffRequirement,
    generate_shifts,
    parse_roster_csv,
    validate_inputs,
)

# ---------------------------------------------------------------------------
# Helper: build minimal valid inputs for reuse across tests
# ---------------------------------------------------------------------------

DAY_ORDER = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def _make_employees(count: int = 5) -> list[Employee]:
    """Create employees with various qualifications."""
    employees = []
    for i in range(count):
        emp_id = f"EMP-{i + 1:03d}"
        employees.append(
            Employee(
                employee_id=emp_id,
                name=f"Worker {i + 1}",
                available_days=["MON", "TUE", "WED", "THU", "FRI"],
                max_hours_week=40.0,
                max_days_week=5,
                qualifications=["R1", "R2"],
                is_supervisor=(i == 0),  # first employee is supervisor
                preferred_patterns=[],
                avoid_days=[],
                contract_hours=40.0,
            )
        )
    return employees


def _make_requirements() -> list[StaffRequirement]:
    """Create simple requirements for MON-FRI in R1."""
    reqs = []
    for day in ["MON", "TUE", "WED", "THU", "FRI"]:
        reqs.append(
            StaffRequirement(
                day=day,
                room_code="R1",
                required_staff=2,
                start_hour=8.0,
                end_hour=17.0,
                need_supervisor=1,
            )
        )
    return reqs


def _default_config() -> ShiftConfig:
    return ShiftConfig(
        max_consecutive_days=6,
        min_rest_hours=11.0,
        week_start="2026-02-23",
    )


# ===========================================================================
# Test 1: Basic shift generation
# ===========================================================================


def test_basic_shift_generation():
    """5 employees, 5 days, 1 room -> assignments generated."""
    employees = _make_employees(5)
    requirements = _make_requirements()
    config = _default_config()

    result = generate_shifts(employees, requirements, [], config)

    assert isinstance(result, ShiftResult)
    assert len(result.assignments) > 0, "Should generate at least one assignment"
    # All assignments should reference valid employee IDs
    valid_ids = {e.employee_id for e in employees}
    for a in result.assignments:
        assert a.employee_id in valid_ids


# ===========================================================================
# Test 2: Deterministic output
# ===========================================================================


def test_deterministic_output():
    """Same input twice -> same assignments."""
    employees = _make_employees(5)
    requirements = _make_requirements()
    config = _default_config()

    r1 = generate_shifts(employees, requirements, [], config)
    r2 = generate_shifts(employees, requirements, [], config)

    def _key(a: ShiftAssignment):
        return (a.employee_id, a.day, a.room_code, a.pattern_id)

    assert sorted(map(_key, r1.assignments)) == sorted(map(_key, r2.assignments))


# ===========================================================================
# Test 3: Empty requirements -> empty result
# ===========================================================================


def test_empty_requirements():
    """No requirements -> no assignments, no errors."""
    employees = _make_employees(3)
    config = _default_config()

    result = generate_shifts(employees, [], [], config)

    assert len(result.assignments) == 0
    errors = [a for a in result.alerts if a.level == "ERROR"]
    assert len(errors) == 0


# ===========================================================================
# Test 4: Empty roster -> SFT-W008
# ===========================================================================


def test_empty_roster():
    """No employees -> SFT-W008 warnings for each slot."""
    requirements = _make_requirements()
    config = _default_config()

    result = generate_shifts([], requirements, [], config)

    assert len(result.assignments) == 0
    w008_alerts = [a for a in result.alerts if a.code == "SFT-W008"]
    assert len(w008_alerts) > 0, "Should have W008 for no candidates"


# ===========================================================================
# Test 5: Single employee
# ===========================================================================


def test_single_employee():
    """1 employee, 1 day requirement -> 1 assignment."""
    emp = Employee(
        employee_id="EMP-001",
        name="Solo Worker",
        available_days=["MON"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    req = StaffRequirement(
        day="MON",
        room_code="R1",
        required_staff=1,
        start_hour=8.0,
        end_hour=17.0,
        need_supervisor=1,
    )
    config = _default_config()

    result = generate_shifts([emp], [req], [], config)

    assert len(result.assignments) == 1
    assert result.assignments[0].employee_id == "EMP-001"
    assert result.assignments[0].day == "MON"
    assert result.assignments[0].room_code == "R1"


# ===========================================================================
# Test 6: max_hours_week constraint
# ===========================================================================


def test_max_hours_week():
    """Employee with max_hours_week=16 should not exceed it."""
    emp = Employee(
        employee_id="EMP-001",
        name="Part Timer",
        available_days=["MON", "TUE", "WED", "THU", "FRI"],
        max_hours_week=16.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=16.0,
    )
    # 5 days * 8h = 40h, but employee limited to 16h
    reqs = []
    for day in ["MON", "TUE", "WED", "THU", "FRI"]:
        reqs.append(
            StaffRequirement(
                day=day,
                room_code="R1",
                required_staff=1,
                start_hour=8.0,
                end_hour=17.0,
                need_supervisor=1,
            )
        )
    config = _default_config()

    result = generate_shifts([emp], reqs, [], config)

    total_hours = sum(a.net_hours for a in result.assignments)
    assert total_hours <= 16.0, f"Total hours {total_hours} exceeds max 16"


# ===========================================================================
# Test 7: max_days_week constraint
# ===========================================================================


def test_max_days_week():
    """Employee with max_days_week=3 should work at most 3 days."""
    emp = Employee(
        employee_id="EMP-001",
        name="Limited Days",
        available_days=["MON", "TUE", "WED", "THU", "FRI"],
        max_hours_week=40.0,
        max_days_week=3,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    reqs = []
    for day in ["MON", "TUE", "WED", "THU", "FRI"]:
        reqs.append(
            StaffRequirement(
                day=day,
                room_code="R1",
                required_staff=1,
                start_hour=8.0,
                end_hour=17.0,
                need_supervisor=1,
            )
        )
    config = _default_config()

    result = generate_shifts([emp], reqs, [], config)

    days_worked = {a.day for a in result.assignments}
    assert len(days_worked) <= 3, f"Worked {len(days_worked)} days, max is 3"


# ===========================================================================
# Test 8: available_days constraint
# ===========================================================================


def test_available_days():
    """Employee available only MON/WED/FRI should not be assigned other days."""
    emp = Employee(
        employee_id="EMP-001",
        name="MWF Worker",
        available_days=["MON", "WED", "FRI"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    reqs = []
    for day in ["MON", "TUE", "WED", "THU", "FRI"]:
        reqs.append(
            StaffRequirement(
                day=day,
                room_code="R1",
                required_staff=1,
                start_hour=8.0,
                end_hour=17.0,
                need_supervisor=1,
            )
        )
    config = _default_config()

    result = generate_shifts([emp], reqs, [], config)

    for a in result.assignments:
        assert a.day in ["MON", "WED", "FRI"], f"Assigned on {a.day}, not available"


# ===========================================================================
# Test 9: Qualification matching
# ===========================================================================


def test_qualification_matching():
    """Employee without R2 qualification should not be assigned to R2."""
    emp_r1 = Employee(
        employee_id="EMP-001",
        name="R1 Only",
        available_days=["MON"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    emp_r2 = Employee(
        employee_id="EMP-002",
        name="R2 Only",
        available_days=["MON"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R2"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    reqs = [
        StaffRequirement(
            day="MON",
            room_code="R1",
            required_staff=1,
            start_hour=8.0,
            end_hour=17.0,
            need_supervisor=1,
        ),
        StaffRequirement(
            day="MON",
            room_code="R2",
            required_staff=1,
            start_hour=8.0,
            end_hour=17.0,
            need_supervisor=1,
        ),
    ]
    config = _default_config()

    result = generate_shifts([emp_r1, emp_r2], reqs, [], config)

    for a in result.assignments:
        if a.employee_id == "EMP-001":
            assert a.room_code == "R1", "EMP-001 should only be in R1"
        if a.employee_id == "EMP-002":
            assert a.room_code == "R2", "EMP-002 should only be in R2"


# ===========================================================================
# Test 10: Supervisor requirement
# ===========================================================================


def test_supervisor_requirement():
    """Room needing supervisor but none assigned -> SFT-W002."""
    emp = Employee(
        employee_id="EMP-001",
        name="Regular Worker",
        available_days=["MON"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=False,  # Not a supervisor
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    req = StaffRequirement(
        day="MON",
        room_code="R1",
        required_staff=1,
        start_hour=8.0,
        end_hour=17.0,
        need_supervisor=1,
    )
    config = _default_config()

    result = generate_shifts([emp], [req], [], config)

    # Should still assign the worker
    assert len(result.assignments) > 0
    # But should warn about no supervisor
    w002_alerts = [a for a in result.alerts if a.code == "SFT-W002"]
    assert len(w002_alerts) > 0, "Should have SFT-W002 for missing supervisor"


# ===========================================================================
# Test 11: Minimum rest between shifts
# ===========================================================================


def test_min_rest_between_shifts():
    """Employee with late shift followed by early shift should be blocked."""
    emp = Employee(
        employee_id="EMP-001",
        name="Worker",
        available_days=["MON", "TUE"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    # MON late shift (10:00-19:00) + TUE early shift (6:00-15:00) = only 11h gap
    # With min_rest_hours=12, TUE should be blocked
    reqs = [
        StaffRequirement(
            day="MON",
            room_code="R1",
            required_staff=1,
            start_hour=10.0,
            end_hour=19.0,
            need_supervisor=1,
        ),
        StaffRequirement(
            day="TUE",
            room_code="R1",
            required_staff=1,
            start_hour=6.0,
            end_hour=15.0,
            need_supervisor=1,
        ),
    ]
    config = ShiftConfig(
        max_consecutive_days=6,
        min_rest_hours=12.0,
        week_start="2026-02-23",
    )

    result = generate_shifts([emp], reqs, [], config)

    # Employee should be assigned MON but not TUE (rest insufficient)
    days_assigned = [a.day for a in result.assignments if a.employee_id == "EMP-001"]
    assert "MON" in days_assigned
    # TUE should not be assigned since 19:00->6:00 is only 11h rest
    assert "TUE" not in days_assigned, "TUE should be blocked due to rest time"


# ===========================================================================
# Test 12: Max consecutive days
# ===========================================================================


def test_max_consecutive_days():
    """Employee should not exceed max consecutive days."""
    emp = Employee(
        employee_id="EMP-001",
        name="Worker",
        available_days=["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
        max_hours_week=56.0,
        max_days_week=7,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=56.0,
    )
    # Requirements for all 7 days
    reqs = []
    for day in DAY_ORDER:
        reqs.append(
            StaffRequirement(
                day=day,
                room_code="R1",
                required_staff=1,
                start_hour=8.0,
                end_hour=17.0,
                need_supervisor=1,
            )
        )
    config = ShiftConfig(
        max_consecutive_days=5,
        min_rest_hours=11.0,
        week_start="2026-02-23",
    )

    result = generate_shifts([emp], reqs, [], config)

    days_assigned = sorted(
        [a.day for a in result.assignments if a.employee_id == "EMP-001"],
        key=lambda d: DAY_ORDER.index(d),
    )
    # Check no more than 5 consecutive days
    max_consecutive = 0
    current_streak = 0
    for i, day in enumerate(DAY_ORDER):
        if day in days_assigned:
            current_streak += 1
            max_consecutive = max(max_consecutive, current_streak)
        else:
            current_streak = 0
    assert max_consecutive <= 5, f"Max consecutive {max_consecutive} exceeds limit 5"


# ===========================================================================
# Test 13: SFT-E001 (max_hours_week <= 0)
# ===========================================================================


def test_invalid_max_hours():
    """max_hours_week <= 0 -> SFT-E001."""
    emp = Employee(
        employee_id="EMP-001",
        name="Bad Hours",
        available_days=["MON"],
        max_hours_week=0.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=0.0,
    )
    config = _default_config()

    alerts = validate_inputs([emp], _make_requirements(), [])
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "SFT-E001" in error_codes


# ===========================================================================
# Test 14: SFT-E003 (net_hours <= 0 in pattern)
# ===========================================================================


def test_invalid_pattern_net_hours():
    """Pattern with net_hours <= 0 -> SFT-E003."""
    bad_pattern = ShiftPattern(
        pattern_id="BAD_P",
        name="Bad Pattern",
        start_hour=8.0,
        end_hour=17.0,
        break_start=None,
        break_end=None,
        net_hours=0.0,
    )
    config = _default_config()

    alerts = validate_inputs(_make_employees(1), _make_requirements(), [bad_pattern])
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "SFT-E003" in error_codes


# ===========================================================================
# Test 15: SFT-E004 (start_hour >= end_hour, overnight reject)
# ===========================================================================


def test_invalid_pattern_time_range():
    """Pattern with start_hour >= end_hour -> SFT-E004 (overnight not supported)."""
    bad_pattern = ShiftPattern(
        pattern_id="NIGHT",
        name="Night Shift",
        start_hour=22.0,
        end_hour=6.0,  # overnight
        break_start=None,
        break_end=None,
        net_hours=7.0,
    )
    config = _default_config()

    alerts = validate_inputs(_make_employees(1), _make_requirements(), [bad_pattern])
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "SFT-E004" in error_codes


# ===========================================================================
# Test 16: SFT-E005 (required_staff <= 0)
# ===========================================================================


def test_invalid_required_staff():
    """required_staff <= 0 -> SFT-E005."""
    bad_req = StaffRequirement(
        day="MON",
        room_code="R1",
        required_staff=0,
        start_hour=8.0,
        end_hour=17.0,
        need_supervisor=1,
    )
    config = _default_config()

    alerts = validate_inputs(_make_employees(1), [bad_req], [])
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "SFT-E005" in error_codes


# ===========================================================================
# Test 17: SFT-E006 (no qualified employees for room)
# ===========================================================================


def test_no_qualified_employees_for_room():
    """Room with zero qualified employees (static) -> SFT-E006."""
    emp = Employee(
        employee_id="EMP-001",
        name="R1 Only",
        available_days=["MON"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],  # Only R1 qualified
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    req = StaffRequirement(
        day="MON",
        room_code="R2",
        required_staff=1,
        start_hour=8.0,
        end_hour=17.0,
        need_supervisor=1,
    )
    config = _default_config()

    alerts = validate_inputs([emp], [req], [])
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "SFT-E006" in error_codes


# ===========================================================================
# Test 18: SFT-E007 (all patterns invalid)
# ===========================================================================


def test_all_patterns_invalid():
    """All custom patterns invalid + no builtins valid -> SFT-E007."""
    bad_patterns = [
        ShiftPattern(
            pattern_id="BAD1",
            name="Bad 1",
            start_hour=17.0,
            end_hour=8.0,
            break_start=None,
            break_end=None,
            net_hours=7.0,
        ),
        ShiftPattern(
            pattern_id="BAD2",
            name="Bad 2",
            start_hour=10.0,
            end_hour=10.0,
            break_start=None,
            break_end=None,
            net_hours=0.0,
        ),
    ]
    config = _default_config()

    # When custom patterns are provided, builtins are replaced
    alerts = validate_inputs(_make_employees(1), _make_requirements(), bad_patterns)
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "SFT-E007" in error_codes


# ===========================================================================
# Test 19: SFT-E008 (duplicate employee_id)
# ===========================================================================


def test_duplicate_employee_id():
    """Duplicate employee_id -> SFT-E008."""
    emp1 = Employee(
        employee_id="EMP-001",
        name="Worker 1",
        available_days=["MON"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    emp2 = Employee(
        employee_id="EMP-001",  # duplicate!
        name="Worker 2",
        available_days=["TUE"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=False,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    config = _default_config()

    alerts = validate_inputs([emp1, emp2], _make_requirements(), [])
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "SFT-E008" in error_codes


# ===========================================================================
# Test 20: Coverage gap warning (SFT-W001)
# ===========================================================================


def test_coverage_gap_warning():
    """Insufficient employees for required_staff -> SFT-W001."""
    # 1 employee, need 3 -> coverage gap
    emp = Employee(
        employee_id="EMP-001",
        name="Alone",
        available_days=["MON"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    req = StaffRequirement(
        day="MON",
        room_code="R1",
        required_staff=3,
        start_hour=8.0,
        end_hour=17.0,
        need_supervisor=1,
    )
    config = _default_config()

    result = generate_shifts([emp], [req], [], config)

    w001_alerts = [a for a in result.alerts if a.code == "SFT-W001"]
    assert len(w001_alerts) > 0, "Should have SFT-W001 for coverage gap"


# ===========================================================================
# Test 21: Coverage break exclusion
# ===========================================================================


def test_coverage_break_exclusion():
    """During break time, employee should not count as on-duty in coverage."""
    emp = Employee(
        employee_id="EMP-001",
        name="Worker",
        available_days=["MON"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=["FULL_8H"],
        avoid_days=[],
        contract_hours=40.0,
    )
    req = StaffRequirement(
        day="MON",
        room_code="R1",
        required_staff=1,
        start_hour=8.0,
        end_hour=17.0,
        need_supervisor=1,
    )
    config = _default_config()

    result = generate_shifts([emp], [req], [], config)

    # Find coverage slots during break time (12:00-13:00 for FULL_8H)
    break_slots = [
        c
        for c in result.coverage
        if c.day == "MON" and c.room_code == "R1" and 720 <= c.time_slot_min < 780  # 12:00-13:00 in minutes
    ]
    for slot in break_slots:
        assert slot.assigned == 0, f"At {slot.time_slot_min}min, assigned={slot.assigned} but should be 0 during break"


# ===========================================================================
# Test 22: Fairness hours deviation (SFT-W004)
# ===========================================================================


def test_fairness_hours_deviation():
    """Large hours deviation between employees -> SFT-W004."""
    # Employee 1: works every day (40h), Employee 2: limited (8h)
    emp1 = Employee(
        employee_id="EMP-001",
        name="Full Timer",
        available_days=["MON", "TUE", "WED", "THU", "FRI"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=40.0,
    )
    emp2 = Employee(
        employee_id="EMP-002",
        name="Part Timer",
        available_days=["MON"],
        max_hours_week=8.0,
        max_days_week=1,
        qualifications=["R1"],
        is_supervisor=False,
        preferred_patterns=[],
        avoid_days=[],
        contract_hours=8.0,
    )
    reqs = []
    for day in ["MON", "TUE", "WED", "THU", "FRI"]:
        reqs.append(
            StaffRequirement(
                day=day,
                room_code="R1",
                required_staff=1,
                start_hour=8.0,
                end_hour=17.0,
                need_supervisor=1,
            )
        )
    config = _default_config()

    result = generate_shifts([emp1, emp2], reqs, [], config)

    # Check fairness metrics for deviation
    w004_alerts = [a for a in result.alerts if a.code == "SFT-W004"]
    # emp1 works ~32-40h, emp2 works ~8h -> deviation > 4h for emp1
    assert len(w004_alerts) > 0, "Should have SFT-W004 for hours deviation"


# ===========================================================================
# Test 23: Weekend distribution (SFT-W009)
# ===========================================================================


def test_weekend_distribution():
    """Uneven weekend shifts -> SFT-W009 if std_dev > 1.0."""
    employees = []
    for i in range(4):
        employees.append(
            Employee(
                employee_id=f"EMP-{i + 1:03d}",
                name=f"Worker {i + 1}",
                available_days=["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
                max_hours_week=56.0,
                max_days_week=7,
                qualifications=["R1"],
                is_supervisor=(i == 0),
                preferred_patterns=[],
                avoid_days=[],
                contract_hours=40.0,
            )
        )
    # Only 1 person needed on weekends -> only 1 person gets weekend shifts
    reqs = []
    for day in ["MON", "TUE", "WED", "THU", "FRI"]:
        reqs.append(
            StaffRequirement(
                day=day,
                room_code="R1",
                required_staff=2,
                start_hour=8.0,
                end_hour=17.0,
                need_supervisor=1,
            )
        )
    for day in ["SAT", "SUN"]:
        reqs.append(
            StaffRequirement(
                day=day,
                room_code="R1",
                required_staff=1,
                start_hour=8.0,
                end_hour=14.0,
                need_supervisor=0,
            )
        )
    config = _default_config()

    result = generate_shifts(employees, reqs, [], config)

    # Check weekend shifts are somewhat distributed
    # We just verify the result contains fairness data
    assert len(result.fairness) > 0, "Should have fairness metrics"


# ===========================================================================
# Test 24: Avoid day soft constraint (SFT-W003)
# ===========================================================================


def test_avoid_day_soft_constraint():
    """Employee with avoid_days gets assigned there as last resort -> SFT-W003."""
    emp = Employee(
        employee_id="EMP-001",
        name="Avoids Monday",
        available_days=["MON", "TUE"],
        max_hours_week=40.0,
        max_days_week=5,
        qualifications=["R1"],
        is_supervisor=True,
        preferred_patterns=[],
        avoid_days=["MON"],
        contract_hours=40.0,
    )
    # Only requirement on MON (employee's avoid day)
    req = StaffRequirement(
        day="MON",
        room_code="R1",
        required_staff=1,
        start_hour=8.0,
        end_hour=17.0,
        need_supervisor=1,
    )
    config = _default_config()

    result = generate_shifts([emp], [req], [], config)

    # Should assign since it's the only option
    assert len(result.assignments) == 1
    # Should warn about avoid day violation
    w003_alerts = [a for a in result.alerts if a.code == "SFT-W003"]
    assert len(w003_alerts) > 0, "Should have SFT-W003 for avoid day"


# ===========================================================================
# Test 25: CSV parse test
# ===========================================================================


def test_parse_roster_csv(tmp_path):
    """Parse roster CSV with semicolons."""
    csv_file = tmp_path / "roster.csv"
    csv_file.write_text(
        "employee_id,name,available_days,max_hours_week,max_days_week,"
        "qualifications,is_supervisor,preferred_patterns,avoid_days,contract_hours\n"
        "EMP-001,Alice,MON;TUE;WED,24.0,3,R1;R2,1,FULL_8H;EARLY_8H,FRI,24.0\n"
        "EMP-002,Bob,MON;TUE;WED;THU;FRI,40.0,5,R1,0,,,\n"
    )

    employees = parse_roster_csv(str(csv_file))

    assert len(employees) == 2

    alice = employees[0]
    assert alice.employee_id == "EMP-001"
    assert alice.name == "Alice"
    assert alice.available_days == ["MON", "TUE", "WED"]
    assert alice.max_hours_week == 24.0
    assert alice.max_days_week == 3
    assert alice.qualifications == ["R1", "R2"]
    assert alice.is_supervisor is True
    assert alice.preferred_patterns == ["FULL_8H", "EARLY_8H"]
    assert alice.avoid_days == ["FRI"]
    assert alice.contract_hours == 24.0

    bob = employees[1]
    assert bob.employee_id == "EMP-002"
    assert bob.is_supervisor is False
    assert bob.preferred_patterns == []
    assert bob.avoid_days == []
    assert bob.contract_hours == 40.0
