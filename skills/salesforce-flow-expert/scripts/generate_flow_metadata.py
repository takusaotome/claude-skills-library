#!/usr/bin/env python3
"""
Salesforce Flow Metadata Generator

Generate correct Flow-meta.xml files with proper structure and API version compatibility.

Usage:
    python3 generate_flow_metadata.py <flow_file.flow> [options]

Example:
    python3 generate_flow_metadata.py MyFlow.flow --type recordTriggeredFlow --api-version 60.0 --status Draft
"""

import argparse
import sys
from pathlib import Path
from typing import Optional


class FlowMetadataGenerator:
    """Generate Flow metadata files"""

    VALID_FLOW_TYPES = {
        "screenFlow": "Flow",
        "recordTriggeredFlow": "AutoLaunchedFlow",
        "scheduleTriggeredFlow": "AutoLaunchedFlow",
        "autolaunched": "AutoLaunchedFlow",
    }

    def __init__(self, flow_file: str, flow_type: str, api_version: str = "60.0", status: str = "Draft"):
        """
        Initialize metadata generator

        Args:
            flow_file: Path to Flow definition file (.flow)
            flow_type: Type of Flow (screenFlow, recordTriggeredFlow, etc.)
            api_version: Salesforce API version (default: 60.0)
            status: Flow status (Draft or Active, default: Draft)
        """
        self.flow_file = Path(flow_file)
        self.flow_type = flow_type
        self.api_version = api_version
        self.status = status

        # Validate inputs
        self._validate_inputs()

        # Derive flow name and label
        self.flow_name = self.flow_file.stem
        self.flow_label = self._generate_label()

    def _validate_inputs(self):
        """Validate input parameters"""
        # Check flow file exists
        if not self.flow_file.exists():
            print(f"ERROR: Flow file not found: {self.flow_file}")
            sys.exit(1)

        # Check flow type
        if self.flow_type not in self.VALID_FLOW_TYPES:
            print(f"ERROR: Invalid flow type: {self.flow_type}")
            print(f"Valid types: {', '.join(self.VALID_FLOW_TYPES.keys())}")
            sys.exit(1)

        # Check status
        if self.status not in ["Draft", "Active", "Obsolete", "InvalidDraft"]:
            print(f"ERROR: Invalid status: {self.status}")
            print("Valid statuses: Draft, Active, Obsolete, InvalidDraft")
            sys.exit(1)

        # Check API version format
        try:
            version = float(self.api_version)
            if version < 50.0 or version > 70.0:
                print(f"WARNING: API version {self.api_version} may be out of typical range (50.0-70.0)")
        except ValueError:
            print(f"ERROR: Invalid API version format: {self.api_version}")
            print("Expected format: 60.0")
            sys.exit(1)

    def _generate_label(self) -> str:
        """Generate human-readable label from filename"""
        # Convert MyFlowName to My Flow Name
        label = self.flow_name.replace("_", " ").replace("-", " ")

        # Add spaces before capital letters (camelCase to Title Case)
        import re

        label = re.sub(r"([a-z])([A-Z])", r"\1 \2", label)

        return label

    def generate_metadata(self) -> str:
        """
        Generate Flow metadata XML content

        Returns:
            XML metadata content as string
        """
        process_type = self.VALID_FLOW_TYPES[self.flow_type]

        # Base metadata
        metadata_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<Flow xmlns="http://soap.sforce.com/2006/04/metadata">',
            f"    <apiVersion>{self.api_version}</apiVersion>",
            "    <description>Flow created via generate_flow_metadata.py</description>",
            f"    <label>{self.flow_label}</label>",
            f"    <processType>{process_type}</processType>",
            f"    <status>{self.status}</status>",
        ]

        # Add type-specific metadata
        if self.flow_type == "recordTriggeredFlow":
            metadata_lines.extend(
                [
                    "    <!-- Record-Triggered Flow Configuration -->",
                    "    <!-- Uncomment and configure triggerType: -->",
                    "    <!-- <triggerType>RecordAfterSave</triggerType> -->",
                    "    <!-- <triggerType>RecordBeforeSave</triggerType> -->",
                    "    <!-- Add start configuration for triggers -->",
                ]
            )

        elif self.flow_type == "scheduleTriggeredFlow":
            metadata_lines.extend(
                [
                    "    <!-- Schedule-Triggered Flow Configuration -->",
                    "    <!-- Add scheduledPaths in start element -->",
                    "    <!-- Example: Daily at 2:00 AM -->",
                ]
            )

        metadata_lines.append("</Flow>")

        return "\n".join(metadata_lines)

    def write_metadata_file(self, output_path: Optional[str] = None) -> Path:
        """
        Write metadata to file

        Args:
            output_path: Custom output path (default: same as flow file with -meta.xml)

        Returns:
            Path to written metadata file
        """
        if output_path:
            metadata_file = Path(output_path)
        else:
            # Default: FlowName.flow-meta.xml
            metadata_file = self.flow_file.parent / f"{self.flow_name}.flow-meta.xml"

        # Generate metadata content
        content = self.generate_metadata()

        # Write to file
        with open(metadata_file, "w", encoding="utf-8") as f:
            f.write(content)

        return metadata_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate Salesforce Flow metadata file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Flow Types:
  screenFlow               Screen Flow (user interaction)
  recordTriggeredFlow      Record-Triggered Flow (before/after save)
  scheduleTriggeredFlow    Schedule-Triggered Flow (time-based)
  autolaunched            Autolaunched Flow (called by other automation)

Examples:
  # Generate metadata for Screen Flow
  python3 generate_flow_metadata.py MyScreenFlow.flow --type screenFlow

  # Generate metadata for Record-Triggered Flow
  python3 generate_flow_metadata.py MyTrigger.flow --type recordTriggeredFlow --status Active

  # Generate with custom API version and output path
  python3 generate_flow_metadata.py MyFlow.flow --type autolaunched --api-version 61.0 --output custom-meta.xml
        """,
    )

    parser.add_argument("flow_file", help="Path to Flow definition file (.flow)")
    parser.add_argument(
        "--type",
        required=True,
        choices=["screenFlow", "recordTriggeredFlow", "scheduleTriggeredFlow", "autolaunched"],
        help="Type of Flow",
    )
    parser.add_argument("--api-version", default="60.0", help="Salesforce API version (default: 60.0)")
    parser.add_argument(
        "--status",
        default="Draft",
        choices=["Draft", "Active", "Obsolete", "InvalidDraft"],
        help="Flow status (default: Draft)",
    )
    parser.add_argument("--output", "-o", help="Output metadata file path (default: <flow_name>.flow-meta.xml)")

    args = parser.parse_args()

    # Generate metadata
    generator = FlowMetadataGenerator(
        flow_file=args.flow_file, flow_type=args.type, api_version=args.api_version, status=args.status
    )

    metadata_file = generator.write_metadata_file(output_path=args.output)

    # Success message
    print("✅ Flow metadata generated successfully!")
    print(f"   Flow Name: {generator.flow_name}")
    print(f"   Flow Type: {args.type} → processType: {generator.VALID_FLOW_TYPES[args.type]}")
    print(f"   API Version: {args.api_version}")
    print(f"   Status: {args.status}")
    print(f"   Output: {metadata_file}")
    print()
    print("Next steps:")
    print(f"  1. Review metadata: cat {metadata_file}")
    print(f"  2. Validate Flow: python3 validate_flow.py {metadata_file}")
    print(f"  3. Deploy to org: python3 deploy_flow.py --source-dir {metadata_file.parent} --target-org <org-alias>")


if __name__ == "__main__":
    main()
