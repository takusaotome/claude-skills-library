#!/usr/bin/env python3
"""
Manage vendors in a procurement project.

Supports adding, editing, removing, and importing vendors from CSV.
"""

import argparse
import csv
import sys
from datetime import date
from pathlib import Path
from typing import Optional

from procurement_models import (
    ProcurementProject,
    Vendor,
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


def add_vendor(
    project_dir: Path,
    vendor_name: str,
    contact_email: str,
    contact_name: Optional[str] = None,
    phone: Optional[str] = None,
    notes: Optional[str] = None,
) -> bool:
    """
    Add a vendor to the procurement project.

    Returns:
        True if vendor was added, False if vendor already exists
    """
    project = load_project(project_dir)

    vendor = Vendor(
        name=vendor_name,
        email=contact_email,
        contact_name=contact_name,
        phone=phone,
        status=VendorStatus.PENDING,
        notes=notes or "",
    )

    if not project.add_vendor(vendor):
        return False

    save_project(project, project_dir)
    return True


def remove_vendor(project_dir: Path, vendor_name: str) -> bool:
    """
    Remove a vendor from the procurement project.

    Returns:
        True if vendor was removed, False if not found
    """
    project = load_project(project_dir)

    vendor = project.get_vendor(vendor_name)
    if not vendor:
        return False

    project.vendors.remove(vendor)
    project.add_timeline_event(f"Vendor removed: {vendor_name}")
    save_project(project, project_dir)
    return True


def update_vendor(
    project_dir: Path,
    vendor_name: str,
    new_email: Optional[str] = None,
    new_contact_name: Optional[str] = None,
    new_phone: Optional[str] = None,
    new_status: Optional[str] = None,
    new_notes: Optional[str] = None,
) -> bool:
    """
    Update vendor information.

    Returns:
        True if vendor was updated, False if not found
    """
    project = load_project(project_dir)

    vendor = project.get_vendor(vendor_name)
    if not vendor:
        return False

    changes = []
    if new_email:
        vendor.email = new_email
        changes.append("email")
    if new_contact_name:
        vendor.contact_name = new_contact_name
        changes.append("contact_name")
    if new_phone:
        vendor.phone = new_phone
        changes.append("phone")
    if new_status:
        vendor.status = VendorStatus(new_status)
        changes.append("status")
    if new_notes is not None:
        vendor.notes = new_notes
        changes.append("notes")

    if changes:
        project.add_timeline_event(f"Vendor updated: {vendor_name}", f"Changed: {', '.join(changes)}")
        save_project(project, project_dir)

    return True


def import_vendors(project_dir: Path, csv_file: Path) -> tuple[int, int]:
    """
    Import vendors from CSV file.

    CSV format: vendor_name,contact_email,contact_name,phone

    Returns:
        Tuple of (added_count, skipped_count)
    """
    project = load_project(project_dir)

    added = 0
    skipped = 0

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vendor = Vendor(
                name=row["vendor_name"],
                email=row["contact_email"],
                contact_name=row.get("contact_name"),
                phone=row.get("phone"),
                status=VendorStatus.PENDING,
            )
            if project.add_vendor(vendor):
                added += 1
            else:
                skipped += 1

    if added > 0:
        project.add_timeline_event("Vendors imported from CSV", f"Added: {added}, Skipped: {skipped}")
        save_project(project, project_dir)

    return added, skipped


def list_vendors(project_dir: Path, status_filter: Optional[str] = None) -> list[Vendor]:
    """
    List vendors in the project.

    Args:
        project_dir: Project directory
        status_filter: Optional status to filter by

    Returns:
        List of vendors matching criteria
    """
    project = load_project(project_dir)

    if status_filter:
        target_status = VendorStatus(status_filter)
        return [v for v in project.vendors if v.status == target_status]

    return project.vendors


def print_vendor_table(vendors: list[Vendor]) -> None:
    """Print vendors in table format."""
    if not vendors:
        print("No vendors found.")
        return

    # Header
    print(f"{'Vendor Name':<30} {'Contact':<25} {'Email':<35} {'Status':<15}")
    print("-" * 105)

    for v in vendors:
        contact = v.contact_name or "-"
        print(f"{v.name:<30} {contact:<25} {v.email:<35} {v.status.value:<15}")


def main():
    parser = argparse.ArgumentParser(description="Manage vendors in a procurement project")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add vendor
    add_parser = subparsers.add_parser("add", help="Add a vendor")
    add_parser.add_argument("--project-dir", required=True, type=Path)
    add_parser.add_argument("--vendor-name", required=True)
    add_parser.add_argument("--contact-email", required=True)
    add_parser.add_argument("--contact-name")
    add_parser.add_argument("--phone")
    add_parser.add_argument("--notes")

    # Remove vendor
    remove_parser = subparsers.add_parser("remove", help="Remove a vendor")
    remove_parser.add_argument("--project-dir", required=True, type=Path)
    remove_parser.add_argument("--vendor-name", required=True)

    # Update vendor
    update_parser = subparsers.add_parser("update", help="Update vendor info")
    update_parser.add_argument("--project-dir", required=True, type=Path)
    update_parser.add_argument("--vendor-name", required=True)
    update_parser.add_argument("--email")
    update_parser.add_argument("--contact-name")
    update_parser.add_argument("--phone")
    update_parser.add_argument("--status", choices=[s.value for s in VendorStatus])
    update_parser.add_argument("--notes")

    # Import vendors
    import_parser = subparsers.add_parser("import", help="Import vendors from CSV")
    import_parser.add_argument("--project-dir", required=True, type=Path)
    import_parser.add_argument("--csv-file", required=True, type=Path)

    # List vendors
    list_parser = subparsers.add_parser("list", help="List vendors")
    list_parser.add_argument("--project-dir", required=True, type=Path)
    list_parser.add_argument("--status", choices=[s.value for s in VendorStatus])

    args = parser.parse_args()

    try:
        if args.command == "add":
            if add_vendor(
                args.project_dir,
                args.vendor_name,
                args.contact_email,
                args.contact_name,
                args.phone,
                args.notes,
            ):
                print(f"Vendor '{args.vendor_name}' added successfully.")
            else:
                print(f"Vendor '{args.vendor_name}' already exists.", file=sys.stderr)
                sys.exit(1)

        elif args.command == "remove":
            if remove_vendor(args.project_dir, args.vendor_name):
                print(f"Vendor '{args.vendor_name}' removed.")
            else:
                print(f"Vendor '{args.vendor_name}' not found.", file=sys.stderr)
                sys.exit(1)

        elif args.command == "update":
            if update_vendor(
                args.project_dir,
                args.vendor_name,
                args.email,
                args.contact_name,
                args.phone,
                args.status,
                args.notes,
            ):
                print(f"Vendor '{args.vendor_name}' updated.")
            else:
                print(f"Vendor '{args.vendor_name}' not found.", file=sys.stderr)
                sys.exit(1)

        elif args.command == "import":
            added, skipped = import_vendors(args.project_dir, args.csv_file)
            print(f"Import complete: {added} added, {skipped} skipped")

        elif args.command == "list":
            vendors = list_vendors(args.project_dir, args.status)
            print_vendor_table(vendors)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
