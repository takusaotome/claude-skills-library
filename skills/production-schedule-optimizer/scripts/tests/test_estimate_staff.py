"""Tests for estimate_staff module — 3 test cases."""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from estimate_staff import StaffEstimateResult, estimate_staff
from generate_schedule import (
    DemandItem,
    Product,
    Room,
    StaffAllocation,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_products() -> list[Product]:
    return [
        Product(
            product_code="P001",
            name="Alpha",
            prep_time_min=60,
            base_qty=10,
            required_staff=2,
            shelf_life_days=7,
            room_codes=["R1"],
        ),
        Product(
            product_code="P002",
            name="Beta",
            prep_time_min=30,
            base_qty=20,
            required_staff=1,
            shelf_life_days=7,
            room_codes=["R1"],
        ),
    ]


def _make_rooms() -> list[Room]:
    return [Room(room_code="R1", name="Room One", max_staff=4)]


def _make_staff() -> list[StaffAllocation]:
    return [
        StaffAllocation(day="MON", room_code="R1", staff_count=3, shift_hours=8.0),
    ]


# ===========================================================================
# Test 1: Basic staff estimate
# ===========================================================================


def test_basic_staff_estimate():
    """Normal case: staff hours, peak, recommended are calculated."""
    products = _make_products()
    rooms = _make_rooms()
    demand = [
        DemandItem(product_code="P001", qty=20),
        DemandItem(product_code="P002", qty=40),
    ]
    staff = _make_staff()

    results = estimate_staff(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        shift_hours=8.0,
    )

    assert len(results) > 0
    # Check that results contain expected keys
    for r in results:
        assert isinstance(r, StaffEstimateResult)
        assert r.required_staff_hours >= 0
        assert r.peak_staff >= 0
        assert r.min_staff >= 0
        assert r.recommended_staff >= 0


# ===========================================================================
# Test 2: Recommended includes buffer
# ===========================================================================


def test_recommended_includes_buffer():
    """recommended = ceil(min_staff * 1.1)."""
    products = [
        Product(
            product_code="P001",
            name="Alpha",
            prep_time_min=480,  # 8 hours for base_qty=10
            base_qty=10,
            required_staff=2,
            shelf_life_days=7,
            room_codes=["R1"],
        ),
    ]
    rooms = [Room(room_code="R1", name="Room One", max_staff=10)]
    demand = [DemandItem(product_code="P001", qty=10)]
    staff = [
        StaffAllocation(day="MON", room_code="R1", staff_count=10, shift_hours=8.0),
    ]

    results = estimate_staff(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        shift_hours=8.0,
    )

    assert len(results) > 0
    for r in results:
        if r.min_staff > 0:
            expected_recommended = math.ceil(r.min_staff * 1.1)
            assert r.recommended_staff == expected_recommended, (
                f"Expected recommended={expected_recommended}, got {r.recommended_staff}"
            )


# ===========================================================================
# Test 3: Empty demand returns zero
# ===========================================================================


def test_empty_demand_returns_zero():
    """No demand -> all zeros."""
    products = _make_products()
    rooms = _make_rooms()
    demand: list[DemandItem] = []
    staff = _make_staff()

    results = estimate_staff(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff,
        shift_hours=8.0,
    )

    # All values should be zero
    for r in results:
        assert r.required_staff_hours == 0.0
        assert r.peak_staff == 0
        assert r.min_staff == 0
        assert r.recommended_staff == 0
