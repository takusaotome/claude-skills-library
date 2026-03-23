#!/usr/bin/env python3
"""
Corrective Action Request (CAR) Tracker

Tracks CAR lifecycle and generates status reports for internal audit follow-up.

Usage:
    python3 car_tracker.py cars.csv --report monthly
    python3 car_tracker.py cars.csv --report overdue
    python3 car_tracker.py cars.csv --format json
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


@dataclass
class CAR:
    """Corrective Action Request record."""

    car_id: str
    audit_name: str
    finding_title: str
    severity: str  # Critical, High, Medium, Low
    auditee_dept: str
    owner: str
    due_date: str  # YYYY-MM-DD
    status: str  # Open, In Progress, Pending Validation, Validated, Closed, Reopened
    open_date: str  # YYYY-MM-DD
    close_date: Optional[str] = None


# Escalation thresholds by severity (days overdue)
ESCALATION_THRESHOLDS = {
    "Critical": {"level_2": 1, "level_3": 8, "level_4": 30},
    "High": {"level_2": 7, "level_3": 30, "level_4": 60},
    "Medium": {"level_2": 14, "level_3": 60, "level_4": 90},
    "Low": {"level_2": 30, "level_3": 90, "level_4": 180},
}


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime object."""
    if not date_str or date_str.lower() in ("", "n/a", "none"):
        return None
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None


def calculate_days_open(car: CAR, reference_date: datetime) -> int:
    """Calculate days a CAR has been open."""
    open_date = parse_date(car.open_date)
    if not open_date:
        return 0
    return (reference_date - open_date).days


def calculate_days_overdue(car: CAR, reference_date: datetime) -> int:
    """Calculate days a CAR is overdue (negative if not due yet)."""
    due_date = parse_date(car.due_date)
    if not due_date:
        return 0
    return (reference_date - due_date).days


def get_escalation_level(car: CAR, days_overdue: int) -> int:
    """
    Determine escalation level based on severity and days overdue.

    Returns:
        0 = Not overdue, 1 = Warning, 2-4 = Escalation levels
    """
    if days_overdue <= 0:
        return 0  # Not overdue

    thresholds = ESCALATION_THRESHOLDS.get(car.severity, ESCALATION_THRESHOLDS["Medium"])

    if days_overdue >= thresholds["level_4"]:
        return 4
    elif days_overdue >= thresholds["level_3"]:
        return 3
    elif days_overdue >= thresholds["level_2"]:
        return 2
    else:
        return 1  # Warning (overdue but not escalated)


def parse_csv(filepath: Path) -> list[CAR]:
    """
    Parse CSV file containing CAR records.

    Expected columns:
    car_id, audit_name, finding_title, severity, auditee_dept,
    owner, due_date, status, open_date, close_date

    Args:
        filepath: Path to CSV file

    Returns:
        List of CAR instances
    """
    cars = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            car = CAR(
                car_id=row.get("car_id", ""),
                audit_name=row.get("audit_name", ""),
                finding_title=row.get("finding_title", ""),
                severity=row.get("severity", "Medium"),
                auditee_dept=row.get("auditee_dept", ""),
                owner=row.get("owner", ""),
                due_date=row.get("due_date", ""),
                status=row.get("status", "Open"),
                open_date=row.get("open_date", ""),
                close_date=row.get("close_date"),
            )
            cars.append(car)
    return cars


def generate_monthly_report(cars: list[CAR], reference_date: datetime) -> str:
    """
    Generate monthly CAR status report in markdown format.

    Args:
        cars: List of CAR instances
        reference_date: Reference date for calculations

    Returns:
        Markdown formatted report string
    """
    # Filter to open CARs
    open_cars = [c for c in cars if c.status not in ("Closed", "Validated")]

    # Count by severity
    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    overdue_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    dept_counts: dict = {}

    for car in open_cars:
        severity_counts[car.severity] = severity_counts.get(car.severity, 0) + 1
        days_overdue = calculate_days_overdue(car, reference_date)
        if days_overdue > 0:
            overdue_counts[car.severity] = overdue_counts.get(car.severity, 0) + 1
        dept_counts[car.auditee_dept] = dept_counts.get(car.auditee_dept, 0) + 1

    total_open = len(open_cars)
    total_overdue = sum(overdue_counts.values())

    # Build report
    lines = [
        "# Corrective Action Request (CAR) Status Report",
        "",
        f"**Report Date**: {reference_date.strftime('%Y-%m-%d')}",
        "",
        "## Executive Summary",
        "",
        f"- **Total Open CARs**: {total_open}",
        f"- **Overdue CARs**: {total_overdue}",
        f"- **On-Time Rate**: {((total_open - total_overdue) / max(total_open, 1) * 100):.0f}%",
        "",
        "## CARs by Severity",
        "",
        "| Severity | Open | Overdue | % Overdue |",
        "|----------|------|---------|-----------|",
    ]

    for sev in ["Critical", "High", "Medium", "Low"]:
        open_count = severity_counts.get(sev, 0)
        overdue_count = overdue_counts.get(sev, 0)
        pct = (overdue_count / max(open_count, 1)) * 100
        lines.append(f"| {sev} | {open_count} | {overdue_count} | {pct:.0f}% |")

    lines.extend(
        [
            "",
            "## CARs by Department",
            "",
            "| Department | Open CARs |",
            "|------------|-----------|",
        ]
    )

    for dept, count in sorted(dept_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {dept} | {count} |")

    # Overdue CARs detail
    overdue_cars = [
        (c, calculate_days_overdue(c, reference_date))
        for c in open_cars
        if calculate_days_overdue(c, reference_date) > 0
    ]
    overdue_cars.sort(key=lambda x: (-get_escalation_level(x[0], x[1]), -x[1]))

    if overdue_cars:
        lines.extend(
            [
                "",
                "## Overdue CARs Requiring Attention",
                "",
                "| CAR ID | Finding | Severity | Owner | Days Overdue | Escalation |",
                "|--------|---------|----------|-------|--------------|------------|",
            ]
        )

        for car, days in overdue_cars:
            esc_level = get_escalation_level(car, days)
            esc_text = f"Level {esc_level}" if esc_level > 0 else "Warning"
            finding_short = car.finding_title[:30] + "..." if len(car.finding_title) > 30 else car.finding_title
            lines.append(f"| {car.car_id} | {finding_short} | {car.severity} | {car.owner} | {days} | {esc_text} |")

    # Upcoming due dates (next 30 days)
    upcoming = [
        (c, parse_date(c.due_date))
        for c in open_cars
        if parse_date(c.due_date) and 0 < (parse_date(c.due_date) - reference_date).days <= 30
    ]
    upcoming.sort(key=lambda x: x[1])

    if upcoming:
        lines.extend(
            [
                "",
                "## Upcoming CARs Due (Next 30 Days)",
                "",
                "| Due Date | CAR ID | Finding | Owner |",
                "|----------|--------|---------|-------|",
            ]
        )

        for car, due in upcoming:
            finding_short = car.finding_title[:30] + "..." if len(car.finding_title) > 30 else car.finding_title
            lines.append(f"| {due.strftime('%Y-%m-%d')} | {car.car_id} | {finding_short} | {car.owner} |")

    lines.append("")
    return "\n".join(lines)


def generate_overdue_report(cars: list[CAR], reference_date: datetime) -> str:
    """
    Generate focused overdue CAR report.

    Args:
        cars: List of CAR instances
        reference_date: Reference date for calculations

    Returns:
        Markdown formatted report string
    """
    open_cars = [c for c in cars if c.status not in ("Closed", "Validated")]
    overdue_cars = [
        (c, calculate_days_overdue(c, reference_date))
        for c in open_cars
        if calculate_days_overdue(c, reference_date) > 0
    ]
    overdue_cars.sort(key=lambda x: (-get_escalation_level(x[0], x[1]), -x[1]))

    lines = [
        "# Overdue CAR Report",
        "",
        f"**Report Date**: {reference_date.strftime('%Y-%m-%d')}",
        f"**Total Overdue**: {len(overdue_cars)}",
        "",
    ]

    if not overdue_cars:
        lines.append("No overdue CARs. All corrective actions are on track.")
        return "\n".join(lines)

    for car, days in overdue_cars:
        esc_level = get_escalation_level(car, days)
        lines.extend(
            [
                f"## {car.car_id} ({car.severity}) - Escalation Level {esc_level}",
                "",
                f"- **Finding**: {car.finding_title}",
                f"- **Audit**: {car.audit_name}",
                f"- **Department**: {car.auditee_dept}",
                f"- **Owner**: {car.owner}",
                f"- **Due Date**: {car.due_date}",
                f"- **Days Overdue**: {days}",
                f"- **Status**: {car.status}",
                "",
            ]
        )

    return "\n".join(lines)


def generate_json_report(cars: list[CAR], reference_date: datetime) -> str:
    """
    Generate JSON CAR report.

    Args:
        cars: List of CAR instances
        reference_date: Reference date for calculations

    Returns:
        JSON formatted report string
    """
    results = []
    for car in cars:
        days_open = calculate_days_open(car, reference_date)
        days_overdue = calculate_days_overdue(car, reference_date)
        esc_level = get_escalation_level(car, days_overdue) if days_overdue > 0 else 0

        results.append(
            {
                "car_id": car.car_id,
                "audit_name": car.audit_name,
                "finding_title": car.finding_title,
                "severity": car.severity,
                "auditee_dept": car.auditee_dept,
                "owner": car.owner,
                "due_date": car.due_date,
                "status": car.status,
                "open_date": car.open_date,
                "close_date": car.close_date,
                "days_open": days_open,
                "days_overdue": max(0, days_overdue),
                "is_overdue": days_overdue > 0,
                "escalation_level": esc_level,
            }
        )

    return json.dumps({"report_date": reference_date.strftime("%Y-%m-%d"), "cars": results}, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Track and report on Corrective Action Requests")
    parser.add_argument("input_file", help="CSV file with CAR records")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)", default=None)
    parser.add_argument(
        "--report",
        "-r",
        choices=["monthly", "overdue"],
        default="monthly",
        help="Report type (default: monthly)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--date",
        "-d",
        help="Reference date YYYY-MM-DD (default: today)",
        default=None,
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if args.date:
        reference_date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        reference_date = datetime.now()

    cars = parse_csv(input_path)

    if args.format == "json":
        report = generate_json_report(cars, reference_date)
    elif args.report == "overdue":
        report = generate_overdue_report(cars, reference_date)
    else:
        report = generate_monthly_report(cars, reference_date)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
        print(f"Report written to: {output_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
