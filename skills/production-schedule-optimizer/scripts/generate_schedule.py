"""
Production Schedule Generator

CLI and library for generating weekly production schedules using a
greedy bin-packing algorithm.  Reads 4 CSV inputs (products, rooms,
demand, staff) and outputs a Markdown timetable.

Usage:
    python3 generate_schedule.py \
        --products products.csv \
        --rooms rooms.csv \
        --demand demand.csv \
        --staff staff.csv \
        --week-start 2026-02-23 \
        --work-hours 8:00-22:00 \
        --lunch-break 12:00-13:00 \
        --output schedule.md
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

# =============================================================================
# Data Models (plain dataclasses, no pydantic)
# =============================================================================


@dataclass
class Product:
    product_code: str
    name: str
    prep_time_min: float
    base_qty: float
    required_staff: int
    shelf_life_days: int
    room_codes: List[str]


@dataclass
class Room:
    room_code: str
    name: str
    max_staff: int


@dataclass
class DemandItem:
    product_code: str
    qty: float


@dataclass
class StaffAllocation:
    day: str  # MON-SUN
    room_code: str
    staff_count: int
    shift_hours: float


@dataclass
class ScheduleEntry:
    day: str
    room_code: str
    product_code: str
    product_name: str
    start_hour: float
    duration_minutes: float
    end_hour: float
    qty: float
    staff: int


@dataclass
class ScheduleAlert:
    level: str  # ERROR, WARNING
    code: str  # PSO-E001, PSO-W001, etc.
    message: str


@dataclass
class ScheduleResult:
    entries: List[ScheduleEntry]
    alerts: List[ScheduleAlert]
    week_start: str = ""


# =============================================================================
# Day ordering constant
# =============================================================================

DAY_ORDER = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


# =============================================================================
# Core calculation functions
# =============================================================================


def calc_production_count(shelf_life_days: int) -> int:
    """Calculate how many production runs per week from shelf life.

    Args:
        shelf_life_days: Shelf life in days.  Must be > 0.

    Returns:
        Number of production runs per week (1-7).

    Raises:
        ValueError: If shelf_life_days <= 0.
    """
    if shelf_life_days <= 0:
        raise ValueError("shelf_life_days must be > 0")
    return min(math.ceil(7 / shelf_life_days), 7)


def distribute_production_days(
    shelf_life_days: int,
    available_days: List[str],
) -> List[str]:
    """Distribute production days evenly across available days.

    Args:
        shelf_life_days: Shelf life in days.
        available_days: Ordered list of available day labels (MON-SUN).

    Returns:
        Subset of available_days, evenly spaced.
    """
    if not available_days:
        return []
    count = calc_production_count(shelf_life_days)
    if count >= len(available_days):
        return list(available_days)
    step = len(available_days) / count
    return [available_days[int(i * step)] for i in range(count)]


# =============================================================================
# Validation
# =============================================================================


def validate_inputs(
    products: List[Product],
    rooms: List[Room],
    demand: List[DemandItem],
    staff: List[StaffAllocation],
) -> List[ScheduleAlert]:
    """Validate all inputs before schedule generation.

    Returns a list of ScheduleAlert objects.  Any alert with level
    ``ERROR`` means the input set is invalid and scheduling should
    not proceed.
    """
    alerts: List[ScheduleAlert] = []
    room_codes = {r.room_code for r in rooms}

    for p in products:
        if p.shelf_life_days <= 0:
            alerts.append(
                ScheduleAlert(
                    level="ERROR",
                    code="PSO-E001",
                    message=f"Product {p.product_code}: shelf_life_days must be > 0 (got {p.shelf_life_days})",
                )
            )
        if p.base_qty <= 0:
            alerts.append(
                ScheduleAlert(
                    level="ERROR",
                    code="PSO-E002",
                    message=f"Product {p.product_code}: base_qty must be > 0 (got {p.base_qty})",
                )
            )
        if p.prep_time_min <= 0:
            alerts.append(
                ScheduleAlert(
                    level="ERROR",
                    code="PSO-E003",
                    message=f"Product {p.product_code}: prep_time_min must be > 0 (got {p.prep_time_min})",
                )
            )
        if p.required_staff <= 0:
            alerts.append(
                ScheduleAlert(
                    level="ERROR",
                    code="PSO-E004",
                    message=f"Product {p.product_code}: required_staff must be > 0 (got {p.required_staff})",
                )
            )
        for rc in p.room_codes:
            if rc not in room_codes:
                alerts.append(
                    ScheduleAlert(
                        level="ERROR",
                        code="PSO-E006",
                        message=f"Product {p.product_code}: unknown room_code '{rc}'",
                    )
                )

    for r in rooms:
        if r.max_staff <= 0:
            alerts.append(
                ScheduleAlert(
                    level="ERROR",
                    code="PSO-E005",
                    message=f"Room {r.room_code}: max_staff must be > 0 (got {r.max_staff})",
                )
            )

    for d in demand:
        if math.isnan(d.qty):
            alerts.append(
                ScheduleAlert(
                    level="WARNING",
                    code="PSO-W002",
                    message=f"Demand for {d.product_code}: qty is NaN/missing, skipping",
                )
            )
        elif d.qty <= 0:
            alerts.append(
                ScheduleAlert(
                    level="WARNING",
                    code="PSO-W001",
                    message=f"Demand for {d.product_code}: qty <= 0 (got {d.qty}), skipping",
                )
            )

    return alerts


# =============================================================================
# Lunch break helpers
# =============================================================================


def _skip_lunch(hour: float, lunch_start: float, lunch_end: float) -> float:
    """Advance start hour past the lunch break if it falls within."""
    if lunch_start <= hour < lunch_end:
        return lunch_end
    return hour


def _calc_end_hour(
    start: float,
    duration_hours: float,
    lunch_start: float,
    lunch_end: float,
) -> float:
    """Calculate end hour, adding lunch break duration if the task spans it."""
    end = start + duration_hours
    if start < lunch_start < end:
        end += lunch_end - lunch_start
    return end


# =============================================================================
# Schedule generation
# =============================================================================


def generate_schedule(
    products: List[Product],
    rooms: List[Room],
    demand: List[DemandItem],
    staff: List[StaffAllocation],
    work_start: float = 8.0,
    work_end: float = 22.0,
    lunch_start: float = 12.0,
    lunch_end: float = 13.0,
    week_start: str = "",
) -> ScheduleResult:
    """Generate a weekly production schedule using greedy bin-packing.

    Args:
        products: Product definitions.
        rooms: Room definitions.
        demand: Demand items.
        staff: Staff allocations per (day, room).
        work_start: Work day start hour (default 8.0).
        work_end: Work day end hour (default 22.0).
        lunch_start: Lunch break start hour (default 12.0).
        lunch_end: Lunch break end hour (default 13.0).
        week_start: ISO date string for the week start (informational).

    Returns:
        ScheduleResult with entries and alerts.
    """
    alerts: List[ScheduleAlert] = []
    entries: List[ScheduleEntry] = []

    product_map = {p.product_code: p for p in products}
    room_map = {r.room_code: r for r in rooms}

    # Build staff allocation index: (day, room) -> StaffAllocation
    alloc_index: dict = {}
    for a in staff:
        alloc_index[(a.day, a.room_code)] = a

    # Determine available days from staff allocations (with staff_count > 0)
    available_days_set = {a.day for a in staff if a.staff_count > 0}
    available_days = [d for d in DAY_ORDER if d in available_days_set]

    # Track room time usage: (day, room) -> next available start hour
    room_schedule: dict = {}
    for day in available_days:
        for rc in room_map:
            room_schedule[(day, rc)] = work_start

    # Track staff-hours usage: (day, room) -> total staff-hours consumed
    staff_used: dict = {}
    for day in available_days:
        for rc in room_map:
            staff_used[(day, rc)] = 0.0

    # Step 1: Build tasks from demand
    tasks: list = []
    for d in demand:
        product = product_map.get(d.product_code)
        if product is None:
            continue

        # Check for NaN/missing demand
        if math.isnan(d.qty):
            alerts.append(
                ScheduleAlert(
                    level="WARNING",
                    code="PSO-W002",
                    message=f"Demand for {d.product_code}: qty is NaN/missing, skipping",
                )
            )
            continue

        # Check for zero/negative demand
        if d.qty <= 0:
            alerts.append(
                ScheduleAlert(
                    level="WARNING",
                    code="PSO-W001",
                    message=f"Demand for {d.product_code}: qty <= 0 (got {d.qty}), skipping",
                )
            )
            continue

        # Determine production days
        prod_days = distribute_production_days(product.shelf_life_days, available_days)
        if not prod_days:
            continue

        production_count = len(prod_days)
        per_run_qty = d.qty / production_count

        # Calculate per-run duration and staff hours
        per_run_duration = (per_run_qty / product.base_qty) * product.prep_time_min
        per_run_staff_hours = (per_run_duration * product.required_staff) / 60.0
        total_staff_hours = (d.qty / product.base_qty) * product.prep_time_min * product.required_staff / 60.0

        # Allowed rooms (only those that exist in room_map)
        allowed_rooms = [rc for rc in product.room_codes if rc in room_map]

        tasks.append(
            {
                "product": product,
                "demand_qty": d.qty,
                "production_days": prod_days,
                "per_run_qty": per_run_qty,
                "per_run_duration": per_run_duration,
                "per_run_staff_hours": per_run_staff_hours,
                "total_staff_hours": total_staff_hours,
                "allowed_rooms": allowed_rooms,
            }
        )

    # Step 2: Sort tasks deterministically
    # total_staff_hours DESC -> shelf_life_days ASC -> product_code ASC
    tasks.sort(
        key=lambda t: (
            -t["total_staff_hours"],
            t["product"].shelf_life_days,
            t["product"].product_code,
        )
    )

    # Step 3: Greedy assignment
    for task in tasks:
        product: Product = task["product"]
        assigned_count = 0

        for prod_day in task["production_days"]:
            # Filter to allowed rooms for this day
            day_rooms = task["allowed_rooms"]
            if not day_rooms:
                continue

            # Find best room: remaining_capacity DESC -> room_code ASC
            best_room: Optional[str] = None
            best_remaining = -1.0

            # Sort candidates by room_code for deterministic tie-breaking
            for room_code in sorted(day_rooms):
                alloc = alloc_index.get((prod_day, room_code))
                if alloc is None:
                    continue
                if alloc.staff_count < product.required_staff:
                    continue

                # Check room max_staff constraint
                room_def = room_map.get(room_code)
                if room_def and product.required_staff > room_def.max_staff:
                    continue

                # Check time availability
                current_end = room_schedule.get((prod_day, room_code), work_start)
                effective_start = _skip_lunch(current_end, lunch_start, lunch_end)
                task_duration_hours = task["per_run_duration"] / 60.0
                end_after_task = _calc_end_hour(effective_start, task_duration_hours, lunch_start, lunch_end)

                if end_after_task > work_end:
                    continue

                # Calculate remaining capacity (staff-hours)
                total_staff_hours_available = alloc.staff_count * alloc.shift_hours
                used = staff_used.get((prod_day, room_code), 0.0)
                remaining = total_staff_hours_available - used

                if remaining < task["per_run_staff_hours"]:
                    continue

                if remaining > best_remaining:
                    best_remaining = remaining
                    best_room = room_code

            if best_room is not None:
                start_hour = room_schedule.get((prod_day, best_room), work_start)
                start_hour = _skip_lunch(start_hour, lunch_start, lunch_end)

                task_duration_hours = task["per_run_duration"] / 60.0
                end_hour = _calc_end_hour(start_hour, task_duration_hours, lunch_start, lunch_end)

                entry = ScheduleEntry(
                    day=prod_day,
                    room_code=best_room,
                    product_code=product.product_code,
                    product_name=product.name,
                    start_hour=start_hour,
                    duration_minutes=round(task["per_run_duration"], 2),
                    end_hour=round(end_hour, 4),
                    qty=round(task["per_run_qty"], 4),
                    staff=product.required_staff,
                )
                entries.append(entry)

                # Update room schedule (advance the timeline)
                room_schedule[(prod_day, best_room)] = end_hour

                # Update staff usage
                staff_used[(prod_day, best_room)] = (
                    staff_used.get((prod_day, best_room), 0.0) + task["per_run_staff_hours"]
                )
                assigned_count += 1

        # Check for partial/zero assignment
        ideal_count = calc_production_count(product.shelf_life_days)
        expected_count = max(ideal_count, len(task["production_days"]))
        if assigned_count < expected_count:
            if assigned_count == 0:
                msg = f"Could not assign {product.product_code} to any slot. Required qty: {task['demand_qty']}"
            else:
                assigned_qty = round(task["per_run_qty"] * assigned_count, 4)
                msg = (
                    f"Partial assignment for {product.product_code}: "
                    f"{assigned_count}/{expected_count} days assigned "
                    f"({assigned_qty}/{task['demand_qty']})"
                )
            alerts.append(
                ScheduleAlert(
                    level="WARNING",
                    code="PSO-W004",
                    message=msg,
                )
            )

    return ScheduleResult(entries=entries, alerts=alerts, week_start=week_start)


# =============================================================================
# CSV Parsers
# =============================================================================


def parse_products(filepath: str) -> List[Product]:
    """Parse products.csv file."""
    products = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(
                Product(
                    product_code=row["product_code"].strip(),
                    name=row["name"].strip(),
                    prep_time_min=float(row["prep_time_min"]),
                    base_qty=float(row["base_qty"]),
                    required_staff=int(row["required_staff"]),
                    shelf_life_days=int(row["shelf_life_days"]),
                    room_codes=[rc.strip() for rc in row["room_codes"].split(";") if rc.strip()],
                )
            )
    return products


def parse_rooms(filepath: str) -> List[Room]:
    """Parse rooms.csv file."""
    rooms = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rooms.append(
                Room(
                    room_code=row["room_code"].strip(),
                    name=row["name"].strip(),
                    max_staff=int(row["max_staff"]),
                )
            )
    return rooms


def parse_demand(filepath: str) -> List[DemandItem]:
    """Parse demand.csv file."""
    items = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qty_str = row.get("qty", "").strip()
            if not qty_str:
                items.append(DemandItem(product_code=row["product_code"].strip(), qty=float("nan")))
            else:
                try:
                    qty = float(qty_str)
                except ValueError:
                    qty = float("nan")
                items.append(DemandItem(product_code=row["product_code"].strip(), qty=qty))
    return items


def parse_staff(filepath: str) -> Tuple[List[StaffAllocation], List[ScheduleAlert]]:
    """Parse staff.csv file.

    Returns:
        Tuple of (allocations, alerts).  Alerts contain PSO-W003 warnings
        for rows where staff_count was missing or invalid (clamped to 0).
    """
    allocs: List[StaffAllocation] = []
    alerts: List[ScheduleAlert] = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            staff_str = row.get("staff_count", "").strip()
            clamped = False
            try:
                staff_count = int(staff_str) if staff_str else 0
                if not staff_str:
                    clamped = True
            except ValueError:
                staff_count = 0
                clamped = True
            if clamped:
                day = row["day"].strip().upper()
                rc = row["room_code"].strip()
                alerts.append(
                    ScheduleAlert(
                        level="WARNING",
                        code="PSO-W003",
                        message=f"Staff ({day}, {rc}): staff_count missing/invalid, clamped to 0",
                    )
                )
            allocs.append(
                StaffAllocation(
                    day=row["day"].strip().upper(),
                    room_code=row["room_code"].strip(),
                    staff_count=staff_count,
                    shift_hours=float(row["shift_hours"]),
                )
            )
    return allocs, alerts


# =============================================================================
# Markdown output
# =============================================================================


def _format_hour(h: float) -> str:
    """Convert decimal hour to HH:MM string."""
    hours = int(h)
    minutes = int(round((h - hours) * 60))
    return f"{hours:02d}:{minutes:02d}"


def render_markdown(result: ScheduleResult) -> str:
    """Render schedule result as a Markdown document."""
    lines: List[str] = []
    lines.append(f"# Production Schedule (Week of {result.week_start})")
    lines.append("")

    # Group entries by day
    by_day: dict = {}
    for entry in result.entries:
        by_day.setdefault(entry.day, []).append(entry)

    for day in DAY_ORDER:
        day_entries = by_day.get(day, [])
        if not day_entries:
            continue
        lines.append(f"## {day}")
        lines.append("")
        lines.append("| Time | Room | Product | Qty | Staff | Duration |")
        lines.append("|------|------|---------|-----|-------|----------|")
        # Sort by start_hour, then room, then product
        day_entries.sort(key=lambda e: (e.start_hour, e.room_code, e.product_code))
        for e in day_entries:
            start = _format_hour(e.start_hour)
            end = _format_hour(e.end_hour)
            dur = f"{e.duration_minutes:.0f}min"
            lines.append(f"| {start}-{end} | {e.room_code} | {e.product_name} | {e.qty:.1f} | {e.staff} | {dur} |")
        lines.append("")

    # Alerts section
    if result.alerts:
        lines.append("## Alerts")
        lines.append("")
        for a in result.alerts:
            lines.append(f"- [{a.level}] {a.code}: {a.message}")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================


def _parse_time_range(s: str) -> tuple:
    """Parse 'HH:MM-HH:MM' into (start_float, end_float)."""
    parts = s.split("-")
    if len(parts) != 2:
        raise ValueError(f"Invalid time range: {s}")
    start_parts = parts[0].split(":")
    end_parts = parts[1].split(":")
    start = int(start_parts[0]) + int(start_parts[1]) / 60.0
    end = int(end_parts[0]) + int(end_parts[1]) / 60.0
    return start, end


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate a weekly production schedule from CSV inputs.")
    parser.add_argument("--products", required=True, help="Path to products.csv")
    parser.add_argument("--rooms", required=True, help="Path to rooms.csv")
    parser.add_argument("--demand", required=True, help="Path to demand.csv")
    parser.add_argument("--staff", required=True, help="Path to staff.csv")
    parser.add_argument("--week-start", required=True, help="Week start date (YYYY-MM-DD)")
    parser.add_argument("--work-hours", default="8:00-22:00", help="Work hours range (default: 8:00-22:00)")
    parser.add_argument("--lunch-break", default="12:00-13:00", help="Lunch break range (default: 12:00-13:00)")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")

    args = parser.parse_args()

    # Parse CSV files
    products = parse_products(args.products)
    rooms = parse_rooms(args.rooms)
    demand = parse_demand(args.demand)
    staff_allocs, staff_parse_alerts = parse_staff(args.staff)

    # Parse time ranges
    work_start, work_end = _parse_time_range(args.work_hours)
    lunch_start, lunch_end = _parse_time_range(args.lunch_break)

    # Validate inputs
    validation_alerts = staff_parse_alerts + validate_inputs(products, rooms, demand, staff_allocs)
    errors = [a for a in validation_alerts if a.level == "ERROR"]
    if errors:
        print("Validation errors:", file=sys.stderr)
        for e in errors:
            print(f"  [{e.code}] {e.message}", file=sys.stderr)
        sys.exit(1)

    # Generate schedule
    result = generate_schedule(
        products=products,
        rooms=rooms,
        demand=demand,
        staff=staff_allocs,
        work_start=work_start,
        work_end=work_end,
        lunch_start=lunch_start,
        lunch_end=lunch_end,
        week_start=args.week_start,
    )

    # Add validation warnings to result
    warnings = [a for a in validation_alerts if a.level == "WARNING"]
    result.alerts = warnings + result.alerts

    # Render output
    md = render_markdown(result)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Schedule written to {args.output}")
    else:
        print(md)


if __name__ == "__main__":
    main()
