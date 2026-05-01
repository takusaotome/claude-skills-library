#!/usr/bin/env python3
"""
Track vendor quote responses in a procurement project.

Supports logging received quotes and viewing status dashboard.
"""

import argparse
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from procurement_models import (
    ProcurementProject,
    ProcurementStatus,
    Quote,
    VendorStatus,
)


def load_project(project_dir: Path) -> ProcurementProject:
    """Load procurement project from directory."""
    config_path = project_dir / "procurement.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"No procurement project found at {project_dir}")
    return ProcurementProject.load(config_path)


def save_project(project: ProcurementProject, project_dir: Path) -> None:
    """Save procurement project to directory."""
    config_path = project_dir / "procurement.yaml"
    project.save(config_path)


def log_quote(
    project_dir: Path,
    vendor_name: str,
    quote_file: Optional[str] = None,
    amount: Optional[float] = None,
    currency: str = "JPY",
    delivery_date: Optional[str] = None,
    valid_until: Optional[str] = None,
    notes: Optional[str] = None,
) -> bool:
    """
    Log a received vendor quote.

    Returns:
        True if quote was logged, False if vendor not found
    """
    project = load_project(project_dir)

    vendor = project.get_vendor(vendor_name)
    if not vendor:
        return False

    # Create quote object
    vendor.quote = Quote(
        file_path=quote_file,
        amount=amount,
        currency=currency,
        received_date=date.today(),
        delivery_date=date.fromisoformat(delivery_date) if delivery_date else None,
        valid_until=date.fromisoformat(valid_until) if valid_until else None,
        notes=notes or "",
    )

    # Update vendor status
    vendor.status = VendorStatus.QUOTE_RECEIVED

    # Update project status if this is first quote
    if project.status == ProcurementStatus.RFQ_SENT:
        project.status = ProcurementStatus.QUOTES_RECEIVED

    # Add timeline event
    amount_str = f"{currency} {amount:,.0f}" if amount else "amount not specified"
    project.add_timeline_event(f"Quote received from {vendor_name}", f"{amount_str}")

    save_project(project, project_dir)
    return True


def mark_declined(project_dir: Path, vendor_name: str, reason: Optional[str] = None) -> bool:
    """
    Mark a vendor as declined to participate.

    Returns:
        True if status was updated, False if vendor not found
    """
    project = load_project(project_dir)

    vendor = project.get_vendor(vendor_name)
    if not vendor:
        return False

    vendor.status = VendorStatus.DECLINED
    vendor.notes = reason or vendor.notes

    project.add_timeline_event(f"Vendor declined: {vendor_name}", reason)

    save_project(project, project_dir)
    return True


def show_status(project_dir: Path) -> None:
    """Display procurement status dashboard."""
    project = load_project(project_dir)

    print("=" * 70)
    print(f"PROCUREMENT STATUS: {project.name}")
    print("=" * 70)
    print()

    # Project info
    print(f"Client: {project.client}")
    print(f"Status: {project.status.value.upper()}")
    print(f"Created: {project.created.strftime('%Y-%m-%d')}")
    print()

    # RFQ info
    if project.rfq.document_path or project.rfq.deadline:
        print("RFQ Information:")
        if project.rfq.document_path:
            print(f"  Document: {project.rfq.document_path}")
        if project.rfq.sent_date:
            print(f"  Sent: {project.rfq.sent_date}")
        if project.rfq.deadline:
            days_remaining = (project.rfq.deadline - date.today()).days
            status = f"({days_remaining} days remaining)" if days_remaining > 0 else "(PAST DUE)"
            print(f"  Deadline: {project.rfq.deadline} {status}")
        print()

    # Vendor summary
    summary = project.get_status_summary()
    print("Vendor Status Summary:")
    total = len(project.vendors)
    for status, count in summary.items():
        pct = (count / total * 100) if total > 0 else 0
        print(f"  {status}: {count} ({pct:.0f}%)")
    print(f"  Total: {total}")
    print()

    # Detailed vendor list
    print("-" * 70)
    print(f"{'Vendor':<25} {'Status':<15} {'Quote Amount':<20} {'Delivery':<10}")
    print("-" * 70)

    for vendor in project.vendors:
        amount_str = ""
        delivery_str = ""
        if vendor.quote:
            if vendor.quote.amount:
                amount_str = f"{vendor.quote.currency} {vendor.quote.amount:,.0f}"
            if vendor.quote.delivery_date:
                delivery_str = str(vendor.quote.delivery_date)

        print(f"{vendor.name:<25} {vendor.status.value:<15} {amount_str:<20} {delivery_str:<10}")

    print("-" * 70)
    print()

    # Pending actions
    pending = project.get_pending_vendors()
    if pending and project.rfq.deadline:
        days_to_deadline = (project.rfq.deadline - date.today()).days
        if 0 < days_to_deadline <= 7:
            print("⚠️  ACTION REQUIRED:")
            print(f"   {len(pending)} vendors have not responded. Deadline in {days_to_deadline} days.")
            print("   Consider sending reminder emails.")
            print()
        elif days_to_deadline <= 0:
            print("🚨 OVERDUE:")
            print(f"   {len(pending)} vendors have not responded. Deadline has passed.")
            print()

    # Recent timeline
    if project.timeline:
        print("Recent Events:")
        for event in project.timeline[-5:]:
            timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M")
            details = f" - {event.details}" if event.details else ""
            print(f"  [{timestamp}] {event.event}{details}")


def get_pending_reminders(project_dir: Path) -> list[dict]:
    """Get list of vendors needing reminder emails."""
    project = load_project(project_dir)

    if not project.rfq.deadline:
        return []

    pending = project.get_pending_vendors()
    days_to_deadline = (project.rfq.deadline - date.today()).days

    return [
        {
            "vendor_name": v.name,
            "email": v.email,
            "contact_name": v.contact_name,
            "days_remaining": days_to_deadline,
            "deadline": str(project.rfq.deadline),
        }
        for v in pending
    ]


def main():
    parser = argparse.ArgumentParser(description="Track vendor quote responses")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Log quote
    log_parser = subparsers.add_parser("log", help="Log a received quote")
    log_parser.add_argument("--project-dir", required=True, type=Path)
    log_parser.add_argument("--vendor-name", required=True)
    log_parser.add_argument("--quote-file", help="Path to quote document")
    log_parser.add_argument("--amount", type=float, help="Quote amount")
    log_parser.add_argument("--currency", default="JPY")
    log_parser.add_argument("--delivery-date", help="Proposed delivery date (YYYY-MM-DD)")
    log_parser.add_argument("--valid-until", help="Quote validity date (YYYY-MM-DD)")
    log_parser.add_argument("--notes", help="Additional notes")

    # Mark declined
    decline_parser = subparsers.add_parser("decline", help="Mark vendor as declined")
    decline_parser.add_argument("--project-dir", required=True, type=Path)
    decline_parser.add_argument("--vendor-name", required=True)
    decline_parser.add_argument("--reason", help="Reason for declining")

    # Show status
    status_parser = subparsers.add_parser("status", help="Show status dashboard")
    status_parser.add_argument("--project-dir", required=True, type=Path)

    # Get pending reminders
    reminder_parser = subparsers.add_parser("pending", help="List vendors needing reminders")
    reminder_parser.add_argument("--project-dir", required=True, type=Path)

    args = parser.parse_args()

    try:
        if args.command == "log":
            if log_quote(
                args.project_dir,
                args.vendor_name,
                args.quote_file,
                args.amount,
                args.currency,
                args.delivery_date,
                args.valid_until,
                args.notes,
            ):
                print(f"Quote from '{args.vendor_name}' logged successfully.")
            else:
                print(f"Vendor '{args.vendor_name}' not found.", file=sys.stderr)
                sys.exit(1)

        elif args.command == "decline":
            if mark_declined(args.project_dir, args.vendor_name, args.reason):
                print(f"Vendor '{args.vendor_name}' marked as declined.")
            else:
                print(f"Vendor '{args.vendor_name}' not found.", file=sys.stderr)
                sys.exit(1)

        elif args.command == "status":
            show_status(args.project_dir)

        elif args.command == "pending":
            pending = get_pending_reminders(args.project_dir)
            if pending:
                print(f"Vendors needing reminders ({len(pending)}):")
                for p in pending:
                    print(f"  - {p['vendor_name']} <{p['email']}> ({p['days_remaining']} days to deadline)")
            else:
                print("No pending reminders needed.")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
