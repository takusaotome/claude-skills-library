#!/usr/bin/env python3
"""
Initialize a new vendor procurement project.

Creates the directory structure and initial configuration for tracking
the vendor procurement lifecycle.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from procurement_models import (
    ProcurementProject,
    ProcurementStatus,
)


def create_project_structure(output_dir: Path) -> None:
    """Create the standard project directory structure."""
    directories = [
        output_dir / "rfq",
        output_dir / "quotes",
        output_dir / "estimates",
        output_dir / "communications",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def init_procurement_project(
    project_name: str,
    client: str,
    output_dir: Path,
    description: str = "",
) -> ProcurementProject:
    """
    Initialize a new procurement project.

    Args:
        project_name: Name of the project
        client: Client organization name
        output_dir: Directory to create project structure
        description: Optional project description

    Returns:
        The initialized ProcurementProject
    """
    # Create directory structure
    create_project_structure(output_dir)

    # Create project
    project = ProcurementProject(
        name=project_name,
        client=client,
        created=datetime.now(),
        status=ProcurementStatus.INITIALIZED,
        description=description,
    )

    # Add initialization event
    project.add_timeline_event("Project initialized", f"Client: {client}")

    # Save project configuration
    config_path = output_dir / "procurement.yaml"
    project.save(config_path)

    return project


def main():
    parser = argparse.ArgumentParser(description="Initialize a new vendor procurement project")
    parser.add_argument("--project-name", required=True, help="Name of the procurement project")
    parser.add_argument("--client", required=True, help="Client organization name")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory to create project structure")
    parser.add_argument("--description", default="", help="Optional project description")

    args = parser.parse_args()

    # Check if directory already exists and has a config
    config_path = args.output_dir / "procurement.yaml"
    if config_path.exists():
        print(f"Error: Project already exists at {args.output_dir}", file=sys.stderr)
        print("Use --force to overwrite (not implemented for safety)", file=sys.stderr)
        sys.exit(1)

    try:
        project = init_procurement_project(
            project_name=args.project_name,
            client=args.client,
            output_dir=args.output_dir,
            description=args.description,
        )

        print("Procurement project initialized successfully!")
        print("")
        print(f"Project: {project.name}")
        print(f"Client: {project.client}")
        print(f"Location: {args.output_dir}")
        print("")
        print("Directory structure created:")
        print(f"  {args.output_dir}/")
        print("  ├── procurement.yaml     # Project configuration")
        print("  ├── rfq/                 # RFQ documents")
        print("  ├── quotes/              # Vendor quotes")
        print("  ├── estimates/           # Client estimates")
        print("  └── communications/      # Email records")
        print("")
        print("Next steps:")
        print("  1. Create RFQ document using vendor-rfq-creator skill")
        print("  2. Add vendors using: python3 manage_vendors.py add ...")
        print("  3. Send RFQ using: python3 send_rfq.py ...")

    except Exception as e:
        print(f"Error initializing project: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
