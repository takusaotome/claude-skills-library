#!/usr/bin/env python3
"""
Vendor Support Ticket Tracker - CLI Tool

Track vendor support tickets and RMA cases across multiple vendors.
Maintains ticket state, communication timeline, pending actions, and escalation status.

Usage:
    python ticket_manager.py init --db-path ./tickets.yaml
    python ticket_manager.py create --vendor STX --ticket-id SR-2025-001234 --subject "HDD failure" --priority high --category RMA --db-path ./tickets.yaml
    python ticket_manager.py update --ticket-id SR-2025-001234 --status awaiting-parts --notes "Parts shipping" --db-path ./tickets.yaml
    python ticket_manager.py report --output ./report.md --db-path ./tickets.yaml
    python ticket_manager.py stale --days 7 --db-path ./tickets.yaml
    python ticket_manager.py escalate --ticket-id SR-2025-001234 --reason "No response" --db-path ./tickets.yaml
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import yaml

SCHEMA_VERSION = "1.0"

VALID_STATUSES = [
    "open",
    "acknowledged",
    "in-progress",
    "awaiting-parts",
    "awaiting-customer",
    "escalated",
    "resolved",
    "closed",
]

VALID_PRIORITIES = ["critical", "high", "medium", "low"]

VALID_CATEGORIES = ["RMA", "support", "warranty", "incident", "inquiry"]


def get_timestamp() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_database(db_path: Path) -> dict:
    """Load ticket database from YAML file."""
    if not db_path.exists():
        return {"schema_version": SCHEMA_VERSION, "tickets": {}}

    with open(db_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if data is None:
        return {"schema_version": SCHEMA_VERSION, "tickets": {}}

    return data


def save_database(db_path: Path, data: dict) -> None:
    """Save ticket database to YAML file."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with open(db_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def calculate_sla_target(priority: str, created_at: str) -> str:
    """Calculate SLA target based on priority level."""
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

    sla_hours = {
        "critical": 4,
        "high": 24,
        "medium": 72,
        "low": 120,  # 5 business days approximated
    }

    target = created + timedelta(hours=sla_hours.get(priority, 72))
    return target.strftime("%Y-%m-%dT%H:%M:%SZ")


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a new ticket database."""
    db_path = Path(args.db_path)

    if db_path.exists() and not args.force:
        print(f"Database already exists at {db_path}. Use --force to overwrite.", file=sys.stderr)
        return 1

    data = {"schema_version": SCHEMA_VERSION, "tickets": {}}
    save_database(db_path, data)
    print(f"Initialized ticket database at {db_path}")
    return 0


def cmd_create(args: argparse.Namespace) -> int:
    """Create a new ticket."""
    db_path = Path(args.db_path)
    data = load_database(db_path)

    if args.ticket_id in data["tickets"]:
        print(f"Ticket {args.ticket_id} already exists.", file=sys.stderr)
        return 1

    if args.priority not in VALID_PRIORITIES:
        print(f"Invalid priority: {args.priority}. Valid: {VALID_PRIORITIES}", file=sys.stderr)
        return 1

    if args.category not in VALID_CATEGORIES:
        print(f"Invalid category: {args.category}. Valid: {VALID_CATEGORIES}", file=sys.stderr)
        return 1

    now = get_timestamp()
    sla_target = calculate_sla_target(args.priority, now)

    ticket = {
        "vendor": args.vendor,
        "ticket_id": args.ticket_id,
        "subject": args.subject,
        "category": args.category,
        "priority": args.priority,
        "status": "open",
        "contact": args.contact or "",
        "created_at": now,
        "updated_at": now,
        "sla_target": sla_target,
        "escalated": False,
        "timeline": [
            {
                "timestamp": now,
                "action": "created",
                "notes": args.notes or f"Ticket created: {args.subject}",
            }
        ],
    }

    data["tickets"][args.ticket_id] = ticket
    save_database(db_path, data)
    print(f"Created ticket {args.ticket_id} for vendor {args.vendor}")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Update a ticket's status or add notes."""
    db_path = Path(args.db_path)
    data = load_database(db_path)

    if args.ticket_id not in data["tickets"]:
        print(f"Ticket {args.ticket_id} not found.", file=sys.stderr)
        return 1

    ticket = data["tickets"][args.ticket_id]
    now = get_timestamp()

    if args.status:
        if args.status not in VALID_STATUSES:
            print(f"Invalid status: {args.status}. Valid: {VALID_STATUSES}", file=sys.stderr)
            return 1

        old_status = ticket["status"]
        ticket["status"] = args.status
        ticket["updated_at"] = now

        timeline_entry = {
            "timestamp": now,
            "action": "status_change",
            "from_status": old_status,
            "to_status": args.status,
            "notes": args.notes or f"Status changed from {old_status} to {args.status}",
        }
        ticket["timeline"].append(timeline_entry)
        print(f"Updated ticket {args.ticket_id}: {old_status} -> {args.status}")
    elif args.notes:
        ticket["updated_at"] = now
        timeline_entry = {
            "timestamp": now,
            "action": "note_added",
            "notes": args.notes,
        }
        ticket["timeline"].append(timeline_entry)
        print(f"Added note to ticket {args.ticket_id}")
    else:
        print("No changes specified. Use --status or --notes.", file=sys.stderr)
        return 1

    save_database(db_path, data)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Generate a status report for tickets."""
    db_path = Path(args.db_path)
    data = load_database(db_path)

    tickets = data.get("tickets", {})

    # Apply filters
    filter_statuses = None
    if args.filter_status:
        filter_statuses = [s.strip() for s in args.filter_status.split(",")]

    filter_vendor = args.filter_vendor

    filtered_tickets = {}
    for tid, ticket in tickets.items():
        if filter_statuses and ticket["status"] not in filter_statuses:
            continue
        if filter_vendor and ticket["vendor"].lower() != filter_vendor.lower():
            continue
        filtered_tickets[tid] = ticket

    # Generate report
    report = generate_report(filtered_tickets)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {output_path}")
    else:
        print(report)

    return 0


def generate_report(tickets: dict) -> str:
    """Generate markdown status report."""
    now = get_timestamp()

    lines = [
        "# Vendor Support Ticket Status Report",
        f"Generated: {now}",
        "",
    ]

    # Summary stats
    total = len(tickets)
    high_priority = sum(1 for t in tickets.values() if t["priority"] in ["critical", "high"])
    escalated = sum(1 for t in tickets.values() if t.get("escalated", False))

    # Calculate stale (>7 days)
    now_dt = datetime.now(timezone.utc)
    stale_count = 0
    for t in tickets.values():
        updated = datetime.fromisoformat(t["updated_at"].replace("Z", "+00:00"))
        if (now_dt - updated).days > 7:
            stale_count += 1

    lines.extend(
        [
            "## Summary",
            f"- Total Open: {total}",
            f"- High Priority: {high_priority}",
            f"- Escalated: {escalated}",
            f"- Stale (>7 days): {stale_count}",
            "",
        ]
    )

    # Group by vendor
    by_vendor: dict = {}
    for tid, t in tickets.items():
        vendor = t["vendor"]
        if vendor not in by_vendor:
            by_vendor[vendor] = []
        by_vendor[vendor].append(t)

    lines.append("## Open Tickets by Vendor")
    lines.append("")

    for vendor, vendor_tickets in sorted(by_vendor.items()):
        lines.append(f"### {vendor} ({len(vendor_tickets)} ticket{'s' if len(vendor_tickets) != 1 else ''})")
        lines.append("")
        lines.append("| Ticket ID | Subject | Priority | Status | Age | Last Update |")
        lines.append("|-----------|---------|----------|--------|-----|-------------|")

        for t in vendor_tickets:
            created = datetime.fromisoformat(t["created_at"].replace("Z", "+00:00"))
            age_days = (now_dt - created).days
            last_update = t["updated_at"][:10]
            subject = t["subject"][:30] + "..." if len(t["subject"]) > 30 else t["subject"]

            lines.append(
                f"| {t['ticket_id']} | {subject} | {t['priority']} | {t['status']} | {age_days}d | {last_update} |"
            )

        lines.append("")

    # Tickets requiring follow-up
    follow_up = []
    for tid, t in tickets.items():
        updated = datetime.fromisoformat(t["updated_at"].replace("Z", "+00:00"))
        days_since = (now_dt - updated).days

        if days_since > 7:
            follow_up.append((t, days_since, "stale"))
        elif t.get("escalated", False):
            follow_up.append((t, days_since, "escalated"))

    if follow_up:
        lines.append("## Tickets Requiring Follow-Up")
        lines.append("")
        for i, (t, days, reason) in enumerate(follow_up, 1):
            if reason == "stale":
                lines.append(
                    f"{i}. **{t['ticket_id']}** ({t['vendor']}) - Stale for {days} days, last status: {t['status']}"
                )
            else:
                lines.append(f"{i}. **{t['ticket_id']}** ({t['vendor']}) - Escalated, no response for {days} days")
        lines.append("")

    return "\n".join(lines)


def cmd_stale(args: argparse.Namespace) -> int:
    """Find stale tickets with no activity beyond threshold."""
    db_path = Path(args.db_path)
    data = load_database(db_path)

    threshold_days = args.days
    now_dt = datetime.now(timezone.utc)

    stale_tickets = []
    for tid, ticket in data.get("tickets", {}).items():
        # Skip closed tickets
        if ticket["status"] == "closed":
            continue

        updated = datetime.fromisoformat(ticket["updated_at"].replace("Z", "+00:00"))
        days_since = (now_dt - updated).days

        if days_since >= threshold_days:
            stale_tickets.append((tid, ticket, days_since))

    if not stale_tickets:
        print(f"No stale tickets found (threshold: {threshold_days} days)")
        return 0

    print(f"Stale Tickets (no activity for {threshold_days}+ days):")
    print("")
    for tid, ticket, days in sorted(stale_tickets, key=lambda x: -x[2]):
        print(f"  {tid} ({ticket['vendor']}) - {days} days since last update")
        print(f"    Status: {ticket['status']} | Priority: {ticket['priority']}")
        print(f"    Subject: {ticket['subject']}")
        print("")

    return 0


def cmd_escalate(args: argparse.Namespace) -> int:
    """Escalate a ticket."""
    db_path = Path(args.db_path)
    data = load_database(db_path)

    if args.ticket_id not in data["tickets"]:
        print(f"Ticket {args.ticket_id} not found.", file=sys.stderr)
        return 1

    ticket = data["tickets"][args.ticket_id]
    now = get_timestamp()

    old_status = ticket["status"]
    ticket["status"] = "escalated"
    ticket["escalated"] = True
    ticket["updated_at"] = now

    timeline_entry = {
        "timestamp": now,
        "action": "escalated",
        "from_status": old_status,
        "to_status": "escalated",
        "reason": args.reason,
        "notes": f"Escalated: {args.reason}",
    }
    ticket["timeline"].append(timeline_entry)

    save_database(db_path, data)
    print(f"Escalated ticket {args.ticket_id}: {args.reason}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    """Show details for a specific ticket."""
    db_path = Path(args.db_path)
    data = load_database(db_path)

    if args.ticket_id not in data["tickets"]:
        print(f"Ticket {args.ticket_id} not found.", file=sys.stderr)
        return 1

    ticket = data["tickets"][args.ticket_id]

    print(f"Ticket: {ticket['ticket_id']}")
    print(f"Vendor: {ticket['vendor']}")
    print(f"Subject: {ticket['subject']}")
    print(f"Category: {ticket['category']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Escalated: {ticket.get('escalated', False)}")
    print(f"Contact: {ticket.get('contact', 'N/A')}")
    print(f"Created: {ticket['created_at']}")
    print(f"Updated: {ticket['updated_at']}")
    print(f"SLA Target: {ticket.get('sla_target', 'N/A')}")
    print("")
    print("Timeline:")
    for entry in ticket.get("timeline", []):
        print(f"  [{entry['timestamp']}] {entry['action']}")
        if "notes" in entry:
            print(f"    {entry['notes']}")

    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List all tickets."""
    db_path = Path(args.db_path)
    data = load_database(db_path)

    tickets = data.get("tickets", {})

    if not tickets:
        print("No tickets found.")
        return 0

    print("All Tickets:")
    print("")
    print(f"{'ID':<20} {'Vendor':<10} {'Priority':<10} {'Status':<18} {'Subject':<30}")
    print("-" * 90)

    for tid, t in sorted(tickets.items(), key=lambda x: x[1]["updated_at"], reverse=True):
        subject = t["subject"][:30] + "..." if len(t["subject"]) > 30 else t["subject"]
        print(f"{tid:<20} {t['vendor']:<10} {t['priority']:<10} {t['status']:<18} {subject:<30}")

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Vendor Support Ticket Tracker CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize ticket database")
    init_parser.add_argument("--db-path", required=True, help="Path to ticket database YAML file")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing database")

    # create command
    create_parser = subparsers.add_parser("create", help="Create a new ticket")
    create_parser.add_argument("--vendor", required=True, help="Vendor name (e.g., STX, Dell, HP)")
    create_parser.add_argument("--ticket-id", required=True, help="Vendor ticket ID")
    create_parser.add_argument("--subject", required=True, help="Ticket subject/description")
    create_parser.add_argument("--priority", required=True, choices=VALID_PRIORITIES, help="Priority level")
    create_parser.add_argument("--category", required=True, choices=VALID_CATEGORIES, help="Ticket category")
    create_parser.add_argument("--contact", help="Vendor contact email")
    create_parser.add_argument("--notes", help="Initial notes")
    create_parser.add_argument("--db-path", required=True, help="Path to ticket database YAML file")

    # update command
    update_parser = subparsers.add_parser("update", help="Update ticket status or add notes")
    update_parser.add_argument("--ticket-id", required=True, help="Ticket ID to update")
    update_parser.add_argument("--status", choices=VALID_STATUSES, help="New status")
    update_parser.add_argument("--notes", help="Notes to add")
    update_parser.add_argument("--db-path", required=True, help="Path to ticket database YAML file")

    # report command
    report_parser = subparsers.add_parser("report", help="Generate status report")
    report_parser.add_argument("--output", help="Output file path (default: stdout)")
    report_parser.add_argument("--filter-status", help="Comma-separated status filter")
    report_parser.add_argument("--filter-vendor", help="Filter by vendor name")
    report_parser.add_argument("--db-path", required=True, help="Path to ticket database YAML file")

    # stale command
    stale_parser = subparsers.add_parser("stale", help="Find stale tickets")
    stale_parser.add_argument("--days", type=int, default=7, help="Days threshold (default: 7)")
    stale_parser.add_argument("--db-path", required=True, help="Path to ticket database YAML file")

    # escalate command
    escalate_parser = subparsers.add_parser("escalate", help="Escalate a ticket")
    escalate_parser.add_argument("--ticket-id", required=True, help="Ticket ID to escalate")
    escalate_parser.add_argument("--reason", required=True, help="Escalation reason")
    escalate_parser.add_argument("--db-path", required=True, help="Path to ticket database YAML file")

    # show command
    show_parser = subparsers.add_parser("show", help="Show ticket details")
    show_parser.add_argument("--ticket-id", required=True, help="Ticket ID to show")
    show_parser.add_argument("--db-path", required=True, help="Path to ticket database YAML file")

    # list command
    list_parser = subparsers.add_parser("list", help="List all tickets")
    list_parser.add_argument("--db-path", required=True, help="Path to ticket database YAML file")

    args = parser.parse_args()

    commands = {
        "init": cmd_init,
        "create": cmd_create,
        "update": cmd_update,
        "report": cmd_report,
        "stale": cmd_stale,
        "escalate": cmd_escalate,
        "show": cmd_show,
        "list": cmd_list,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
