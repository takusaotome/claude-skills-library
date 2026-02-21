"""Tests for generate_schedule module — 11 test cases."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from generate_schedule import (
    DemandItem,
    Product,
    Room,
    ScheduleAlert,
    ScheduleEntry,
    ScheduleResult,
    StaffAllocation,
    calc_production_count,
    distribute_production_days,
    generate_schedule,
    parse_staff,
    validate_inputs,
)

# ---------------------------------------------------------------------------
# Helper: build minimal valid inputs for reuse across tests
# ---------------------------------------------------------------------------


def _make_products() -> list[Product]:
    """3 products across 2 rooms."""
    return [
        Product(
            product_code="P001",
            name="Alpha",
            prep_time_min=60,
            base_qty=10,
            required_staff=2,
            shelf_life_days=3,
            room_codes=["R1"],
        ),
        Product(
            product_code="P002",
            name="Beta",
            prep_time_min=30,
            base_qty=20,
            required_staff=1,
            shelf_life_days=7,
            room_codes=["R2"],
        ),
        Product(
            product_code="P003",
            name="Gamma",
            prep_time_min=45,
            base_qty=15,
            required_staff=2,
            shelf_life_days=2,
            room_codes=["R1", "R2"],
        ),
    ]


def _make_rooms() -> list[Room]:
    return [
        Room(room_code="R1", name="Room One", max_staff=4),
        Room(room_code="R2", name="Room Two", max_staff=3),
    ]


def _make_demand() -> list[DemandItem]:
    return [
        DemandItem(product_code="P001", qty=30),
        DemandItem(product_code="P002", qty=40),
        DemandItem(product_code="P003", qty=45),
    ]


def _make_staff(days: list[str] | None = None) -> list[StaffAllocation]:
    """Staff allocations for MON-FRI by default."""
    if days is None:
        days = ["MON", "TUE", "WED", "THU", "FRI"]
    allocs = []
    for d in days:
        for rc in ["R1", "R2"]:
            allocs.append(StaffAllocation(day=d, room_code=rc, staff_count=3, shift_hours=8.0))
    return allocs


# ===========================================================================
# Test 1: Basic schedule generation
# ===========================================================================


def test_basic_schedule_generation():
    """3 products, 2 rooms -> entries generated."""
    products = _make_products()
    rooms = _make_rooms()
    demand = _make_demand()
    staff = _make_staff()

    result = generate_schedule(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        work_start=8.0,
        work_end=22.0,
        lunch_start=12.0,
        lunch_end=13.0,
    )

    assert isinstance(result, ScheduleResult)
    assert len(result.entries) > 0, "Should generate at least one entry"
    # All entries should reference valid product codes
    valid_codes = {p.product_code for p in products}
    for e in result.entries:
        assert e.product_code in valid_codes


# ===========================================================================
# Test 2: Shelf-life frequency
# ===========================================================================


def test_shelf_life_frequency():
    """shelf_life=2 -> 4/week, shelf_life=7 -> 1/week."""
    assert calc_production_count(2) == 4
    assert calc_production_count(7) == 1
    assert calc_production_count(1) == 7
    assert calc_production_count(3) == 3


# ===========================================================================
# Test 3: Deterministic output
# ===========================================================================


def test_deterministic_output():
    """Same input twice -> same entries (day, room, product, start, duration, qty)."""
    products = _make_products()
    rooms = _make_rooms()
    demand = _make_demand()
    staff = _make_staff()

    kwargs = dict(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        work_start=8.0,
        work_end=22.0,
        lunch_start=12.0,
        lunch_end=13.0,
    )
    r1 = generate_schedule(**kwargs)
    r2 = generate_schedule(**kwargs)

    def _key(e: ScheduleEntry):
        return (e.day, e.room_code, e.product_code, e.start_hour, e.duration_minutes, e.qty)

    assert sorted(map(_key, r1.entries)) == sorted(map(_key, r2.entries))


# ===========================================================================
# Test 4: shelf_life_days=0 rejects
# ===========================================================================


def test_shelf_life_zero_rejects():
    """shelf_life_days=0 -> PSO-E001 ValueError."""
    products = [
        Product(
            product_code="BAD",
            name="Bad Item",
            prep_time_min=30,
            base_qty=10,
            required_staff=1,
            shelf_life_days=0,
            room_codes=["R1"],
        ),
    ]
    rooms = [Room(room_code="R1", name="Room One", max_staff=4)]
    demand = [DemandItem(product_code="BAD", qty=10)]
    staff = _make_staff()

    alerts = validate_inputs(products, rooms, demand, staff)
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "PSO-E001" in error_codes


# ===========================================================================
# Test 5: base_qty=0 rejects
# ===========================================================================


def test_base_qty_zero_rejects():
    """base_qty=0 -> PSO-E002."""
    products = [
        Product(
            product_code="BAD",
            name="Bad Item",
            prep_time_min=30,
            base_qty=0,
            required_staff=1,
            shelf_life_days=3,
            room_codes=["R1"],
        ),
    ]
    rooms = [Room(room_code="R1", name="Room One", max_staff=4)]
    demand = [DemandItem(product_code="BAD", qty=10)]
    staff = _make_staff()

    alerts = validate_inputs(products, rooms, demand, staff)
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "PSO-E002" in error_codes


# ===========================================================================
# Test 6: demand qty=0 skips with warning
# ===========================================================================


def test_demand_zero_skips():
    """qty=0 -> skip + PSO-W001 warning."""
    products = [
        Product(
            product_code="P001",
            name="Alpha",
            prep_time_min=60,
            base_qty=10,
            required_staff=2,
            shelf_life_days=3,
            room_codes=["R1"],
        ),
    ]
    rooms = [Room(room_code="R1", name="Room One", max_staff=4)]
    demand = [DemandItem(product_code="P001", qty=0)]
    staff = _make_staff()

    result = generate_schedule(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        work_start=8.0,
        work_end=22.0,
        lunch_start=12.0,
        lunch_end=13.0,
    )

    # No entries for zero-demand products
    assert len(result.entries) == 0
    # Should have a PSO-W001 warning
    warning_codes = [a.code for a in result.alerts if a.level == "WARNING"]
    assert "PSO-W001" in warning_codes


# ===========================================================================
# Test 7: Room capacity constraint
# ===========================================================================


def test_room_capacity_constraint():
    """max_staff=2, required_staff=3 -> should go to a different room."""
    products = [
        Product(
            product_code="BIG",
            name="Big Task",
            prep_time_min=60,
            base_qty=10,
            required_staff=3,
            shelf_life_days=7,
            room_codes=["SMALL", "BIG"],
        ),
    ]
    rooms = [
        Room(room_code="SMALL", name="Small Room", max_staff=2),
        Room(room_code="BIG", name="Big Room", max_staff=5),
    ]
    demand = [DemandItem(product_code="BIG", qty=10)]
    staff = [
        StaffAllocation(day="MON", room_code="SMALL", staff_count=2, shift_hours=8.0),
        StaffAllocation(day="MON", room_code="BIG", staff_count=5, shift_hours=8.0),
    ]

    result = generate_schedule(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        work_start=8.0,
        work_end=22.0,
        lunch_start=12.0,
        lunch_end=13.0,
    )

    # Task should be assigned to BIG room, not SMALL
    assert len(result.entries) > 0
    for e in result.entries:
        assert e.room_code == "BIG", f"Expected BIG room but got {e.room_code}"


# ===========================================================================
# Test 8: Staff allocation constraint
# ===========================================================================


def test_staff_allocation_constraint():
    """Insufficient staff -> partial assign + warning."""
    # Product needs 3 staff but only 1 available in the room
    products = [
        Product(
            product_code="P001",
            name="Alpha",
            prep_time_min=60,
            base_qty=10,
            required_staff=3,
            shelf_life_days=7,
            room_codes=["R1"],
        ),
    ]
    rooms = [Room(room_code="R1", name="Room One", max_staff=5)]
    demand = [DemandItem(product_code="P001", qty=10)]
    # Only 1 staff available — not enough for required_staff=3
    staff = [
        StaffAllocation(day="MON", room_code="R1", staff_count=1, shift_hours=8.0),
    ]

    result = generate_schedule(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        work_start=8.0,
        work_end=22.0,
        lunch_start=12.0,
        lunch_end=13.0,
    )

    # Task should NOT be assigned (staff_count < required_staff)
    assert len(result.entries) == 0
    # Should have a warning about unassigned task
    assert len(result.alerts) > 0
    has_warning = any(a.level == "WARNING" for a in result.alerts)
    assert has_warning, "Should warn about insufficient staff"


# ===========================================================================
# Test 9: Lunch break skip
# ===========================================================================


def test_lunch_break_skip():
    """Task at 11:30 lasting 90min -> skips 12-13, resumes at 13:00."""
    # We need a scenario where a task starts near lunch and must skip
    # Product with known duration: qty=10, base_qty=10, prep_time=90 -> 90 min
    products = [
        Product(
            product_code="LONG",
            name="Long Task",
            prep_time_min=90,
            base_qty=10,
            required_staff=1,
            shelf_life_days=7,
            room_codes=["R1"],
        ),
        # First product fills time until 11:30
        # 210 min = 3.5 hours from 8:00 -> ends at 11:30
        Product(
            product_code="FILL",
            name="Fill Task",
            prep_time_min=210,
            base_qty=10,
            required_staff=1,
            shelf_life_days=7,
            room_codes=["R1"],
        ),
    ]
    rooms = [Room(room_code="R1", name="Room One", max_staff=4)]
    demand = [
        DemandItem(product_code="FILL", qty=10),
        DemandItem(product_code="LONG", qty=10),
    ]
    staff = [
        StaffAllocation(day="MON", room_code="R1", staff_count=3, shift_hours=14.0),
    ]

    result = generate_schedule(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        work_start=8.0,
        work_end=22.0,
        lunch_start=12.0,
        lunch_end=13.0,
    )

    # Find the LONG task entry
    long_entries = [e for e in result.entries if e.product_code == "LONG"]
    assert len(long_entries) >= 1, "LONG task should be scheduled"
    entry = long_entries[0]

    # FILL task: 210min from 8:00 -> occupies 8:00-11:30 (3.5 hours)
    # But lunch skip: 8:00-12:00 = 4 hours = 240min, then skip 12-13, resume 13:00
    # Actually: FILL task start=8.0, dur=210min=3.5h, end_calc: 8.0+3.5=11.5
    # Since start(8.0) < lunch(12.0) < end(11.5)? No, 11.5 < 12.0, so no lunch skip for FILL
    # FILL ends at 11.5 (11:30)
    # LONG task starts at 11.5, but 11.5 < 12.0 so no lunch skip on start
    # LONG dur=90min=1.5h, end=11.5+1.5=13.0
    # Since start(11.5) < lunch(12.0) < end(13.0), lunch is spanned -> end = 13.0 + 1.0 = 14.0
    # So the task should show start at 11.5, and effective end at 14.0

    assert entry.start_hour == 11.5, f"Expected start 11.5 but got {entry.start_hour}"
    assert entry.duration_minutes == 90, f"Expected duration 90 but got {entry.duration_minutes}"
    # end_hour accounts for lunch skip: 11.5 + 1.5 + 1.0 (lunch) = 14.0
    assert entry.end_hour == 14.0, f"Expected end 14.0 but got {entry.end_hour}"


# ===========================================================================
# Test 10: Day-room override placeholder
# ===========================================================================


def test_day_room_override():
    """Weekend staff only in MEAT -> entries only in MEAT room on SAT/SUN."""
    products = [
        Product(
            product_code="P001",
            name="Meat Product",
            prep_time_min=60,
            base_qty=10,
            required_staff=2,
            shelf_life_days=1,  # daily -> all 7 days
            room_codes=["MEAT", "COLD"],
        ),
    ]
    rooms = [
        Room(room_code="MEAT", name="Meat Room", max_staff=5),
        Room(room_code="COLD", name="Cold Room", max_staff=3),
    ]
    demand = [DemandItem(product_code="P001", qty=70)]
    # Weekdays: both rooms staffed; Weekends: only MEAT staffed
    staff = []
    for d in ["MON", "TUE", "WED", "THU", "FRI"]:
        staff.append(StaffAllocation(day=d, room_code="MEAT", staff_count=3, shift_hours=8.0))
        staff.append(StaffAllocation(day=d, room_code="COLD", staff_count=3, shift_hours=8.0))
    for d in ["SAT", "SUN"]:
        staff.append(StaffAllocation(day=d, room_code="MEAT", staff_count=2, shift_hours=6.0))
        staff.append(StaffAllocation(day=d, room_code="COLD", staff_count=0, shift_hours=6.0))

    result = generate_schedule(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        work_start=8.0,
        work_end=22.0,
        lunch_start=12.0,
        lunch_end=13.0,
    )

    # Weekend entries should only be in MEAT (COLD has 0 staff)
    weekend_entries = [e for e in result.entries if e.day in ("SAT", "SUN")]
    for e in weekend_entries:
        assert e.room_code == "MEAT", f"Weekend entry in {e.room_code}, expected MEAT"


# ===========================================================================
# Test 11: Invalid room code rejects
# ===========================================================================


def test_invalid_room_code_rejects():
    """Unknown room code -> PSO-E006."""
    products = [
        Product(
            product_code="P001",
            name="Alpha",
            prep_time_min=60,
            base_qty=10,
            required_staff=2,
            shelf_life_days=3,
            room_codes=["NONEXISTENT"],
        ),
    ]
    rooms = [Room(room_code="R1", name="Room One", max_staff=4)]
    demand = [DemandItem(product_code="P001", qty=10)]
    staff = _make_staff()

    alerts = validate_inputs(products, rooms, demand, staff)
    error_codes = [a.code for a in alerts if a.level == "ERROR"]
    assert "PSO-E006" in error_codes


# ===========================================================================
# Test 12: NaN demand qty -> PSO-W002 warning (no crash)
# ===========================================================================


def test_nan_demand_skips_with_warning():
    """qty=NaN -> skip + PSO-W002 warning, no crash."""
    products = [
        Product(
            product_code="P001",
            name="Alpha",
            prep_time_min=60,
            base_qty=10,
            required_staff=2,
            shelf_life_days=3,
            room_codes=["R1"],
        ),
    ]
    rooms = [Room(room_code="R1", name="Room One", max_staff=4)]
    demand = [DemandItem(product_code="P001", qty=float("nan"))]
    staff = _make_staff()

    # validate_inputs should detect NaN
    alerts = validate_inputs(products, rooms, demand, staff)
    warning_codes = [a.code for a in alerts if a.level == "WARNING"]
    assert "PSO-W002" in warning_codes

    # generate_schedule should not crash
    result = generate_schedule(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        work_start=8.0,
        work_end=22.0,
        lunch_start=12.0,
        lunch_end=13.0,
    )

    assert len(result.entries) == 0
    warning_codes = [a.code for a in result.alerts if a.level == "WARNING"]
    assert "PSO-W002" in warning_codes


# ===========================================================================
# Test 13: parse_staff missing staff_count -> PSO-W003
# ===========================================================================


def test_parse_staff_w003(tmp_path):
    """Missing staff_count in CSV -> PSO-W003 warning, clamped to 0."""
    csv_file = tmp_path / "staff.csv"
    csv_file.write_text(
        "day,room_code,staff_count,shift_hours\n"
        "MON,R1,3,8.0\n"
        "MON,R2,,8.0\n"  # missing staff_count
        "TUE,R1,abc,8.0\n"  # invalid staff_count
    )

    allocs, alerts = parse_staff(str(csv_file))

    # Should have 3 allocations
    assert len(allocs) == 3

    # First row: valid -> staff_count=3
    assert allocs[0].staff_count == 3

    # Second row: missing -> clamped to 0
    assert allocs[1].staff_count == 0

    # Third row: invalid -> clamped to 0
    assert allocs[2].staff_count == 0

    # Should have 2 PSO-W003 warnings (missing + invalid)
    w003_alerts = [a for a in alerts if a.code == "PSO-W003"]
    assert len(w003_alerts) == 2
