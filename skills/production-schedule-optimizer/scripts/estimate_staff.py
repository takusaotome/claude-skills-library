"""
Staff Requirement Estimator

CLI and library for estimating minimum staff requirements per (day, room)
based on product demand and production parameters.

Usage:
    python3 estimate_staff.py \
        --products products.csv \
        --demand demand.csv \
        --rooms rooms.csv \
        --shift-hours 8 \
        --output staff_estimate.md
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from typing import List

from generate_schedule import (
    DAY_ORDER,
    DemandItem,
    Product,
    Room,
    StaffAllocation,
    calc_production_count,
    distribute_production_days,
    parse_demand,
    parse_products,
    parse_rooms,
)

# Buffer coefficient: recommended_staff = ceil(min_staff * BUFFER)
STAFF_BUFFER_COEFFICIENT = 1.1


@dataclass
class StaffEstimateResult:
    """Staff estimation result for a single (day, room) combination."""

    day: str
    room_code: str
    required_staff_hours: float
    peak_staff: int
    min_staff: int
    recommended_staff: int
    task_count: int = 0


def estimate_staff(
    products: List[Product],
    rooms: List[Room],
    demand: List[DemandItem],
    staff: List[StaffAllocation],
    shift_hours: float = 8.0,
) -> List[StaffEstimateResult]:
    """Estimate staff requirements per (day, room).

    For each (day, room) combination, calculates:
    - required_staff_hours: total staff-hours needed
    - peak_staff: max concurrent staff (from required_staff of assigned products)
    - min_staff: max(peak, ceil(hours / shift_hours))
    - recommended_staff: ceil(min_staff * 1.1)

    Args:
        products: Product definitions.
        rooms: Room definitions.
        demand: Demand items.
        staff: Staff allocations (used to determine available days).
        shift_hours: Hours per shift for capacity calculation.

    Returns:
        List of StaffEstimateResult, one per (day, room).
    """
    product_map = {p.product_code: p for p in products}
    room_map = {r.room_code: r for r in rooms}

    # Determine available days from staff allocations
    available_days_set = {a.day for a in staff if a.staff_count > 0}
    available_days = [d for d in DAY_ORDER if d in available_days_set]

    # Build staff allocation index for shift_hours lookup
    alloc_index: dict = {}
    for a in staff:
        alloc_index[(a.day, a.room_code)] = a

    # Initialize accumulators: (day, room) -> {staff_hours, peak, tasks}
    accum: dict = {}
    for day in DAY_ORDER:
        for rc in room_map:
            accum[(day, rc)] = {
                "staff_hours": 0.0,
                "peak": 0,
                "tasks": 0,
            }

    # Process each demand item
    for d in demand:
        product = product_map.get(d.product_code)
        if product is None:
            continue
        if d.qty <= 0:
            continue

        # Distribute production days
        prod_days = distribute_production_days(product.shelf_life_days, available_days)
        if not prod_days:
            continue

        per_run_qty = d.qty / len(prod_days)

        # Calculate per-run staff hours
        per_run_duration = (per_run_qty / product.base_qty) * product.prep_time_min
        per_run_staff_hours = (per_run_duration * product.required_staff) / 60.0

        # Determine allowed rooms
        allowed_rooms = [rc for rc in product.room_codes if rc in room_map]
        if not allowed_rooms:
            continue

        # Accumulate per (day, room)
        for day in prod_days:
            day_rooms = allowed_rooms

            if not day_rooms:
                continue

            # Split staff hours evenly across allowed rooms
            split_hours = per_run_staff_hours / len(day_rooms)
            for rc in day_rooms:
                accum[(day, rc)]["staff_hours"] += split_hours
                accum[(day, rc)]["tasks"] += 1
                # Peak: track max concurrent staff from any single task
                accum[(day, rc)]["peak"] = max(
                    accum[(day, rc)]["peak"],
                    product.required_staff,
                )

    # Compute final estimates
    results: List[StaffEstimateResult] = []
    for day in DAY_ORDER:
        for rc in room_map:
            data = accum[(day, rc)]
            alloc = alloc_index.get((day, rc))
            effective_shift = alloc.shift_hours if alloc else shift_hours

            peak = data["peak"]
            hours = data["staff_hours"]
            throughput = math.ceil(hours / effective_shift) if hours > 0 else 0
            min_staff = max(peak, throughput)
            recommended = math.ceil(min_staff * STAFF_BUFFER_COEFFICIENT) if min_staff > 0 else 0

            results.append(
                StaffEstimateResult(
                    day=day,
                    room_code=rc,
                    required_staff_hours=round(hours, 4),
                    peak_staff=peak,
                    min_staff=min_staff,
                    recommended_staff=recommended,
                    task_count=data["tasks"],
                )
            )

    return results


def render_staff_markdown(
    results: List[StaffEstimateResult],
    shift_hours: float,
) -> str:
    """Render staff estimation results as Markdown."""
    lines: list = []
    lines.append("# Staff Requirement Estimate")
    lines.append("")
    lines.append(f"Shift hours: {shift_hours}")
    lines.append(f"Buffer coefficient: {STAFF_BUFFER_COEFFICIENT}")
    lines.append("")

    # Group by day
    by_day: dict = {}
    for r in results:
        by_day.setdefault(r.day, []).append(r)

    for day in DAY_ORDER:
        day_results = by_day.get(day, [])
        if not day_results:
            continue
        # Only show days/rooms with actual work
        active = [r for r in day_results if r.task_count > 0]
        if not active:
            continue

        lines.append(f"## {day}")
        lines.append("")
        lines.append("| Room | Staff-Hours | Peak | Min Staff | Recommended | Tasks |")
        lines.append("|------|------------|------|-----------|-------------|-------|")
        for r in sorted(active, key=lambda x: x.room_code):
            lines.append(
                f"| {r.room_code} | {r.required_staff_hours:.1f} | "
                f"{r.peak_staff} | {r.min_staff} | {r.recommended_staff} | {r.task_count} |"
            )
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Estimate staff requirements from product demand.")
    parser.add_argument("--products", required=True, help="Path to products.csv")
    parser.add_argument("--demand", required=True, help="Path to demand.csv")
    parser.add_argument("--rooms", required=True, help="Path to rooms.csv")
    parser.add_argument("--shift-hours", type=float, default=8.0, help="Shift hours per staff (default: 8)")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")

    args = parser.parse_args()

    products = parse_products(args.products)
    demand = parse_demand(args.demand)
    rooms = parse_rooms(args.rooms)

    # Build dummy staff allocations for all days/rooms (used for available_days detection)
    staff_allocs: List[StaffAllocation] = []
    for day in DAY_ORDER:
        for room in rooms:
            staff_allocs.append(
                StaffAllocation(
                    day=day,
                    room_code=room.room_code,
                    staff_count=room.max_staff,
                    shift_hours=args.shift_hours,
                )
            )

    results = estimate_staff(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff_allocs,
        shift_hours=args.shift_hours,
    )

    md = render_staff_markdown(results, args.shift_hours)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Staff estimate written to {args.output}")
    else:
        print(md)


if __name__ == "__main__":
    main()
