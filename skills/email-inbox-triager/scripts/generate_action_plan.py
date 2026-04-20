#!/usr/bin/env python3
"""
Generate daily email action plan from classification results.

Converts email triage report into an actionable daily plan with time budgeting.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class ActionPlanGenerator:
    """Generates actionable daily email plans from classification data."""

    CATEGORY_ORDER = [
        "urgent-response",
        "response-needed",
        "delegatable",
        "fyi-read",
        "archive",
    ]

    CATEGORY_LABELS = {
        "urgent-response": "Urgent Response",
        "response-needed": "Response Needed",
        "delegatable": "Delegate",
        "fyi-read": "FYI / Read Later",
        "archive": "Archive",
    }

    def __init__(self, time_budget: int = 60):
        """Initialize generator with time budget in minutes."""
        self.time_budget = time_budget

    def group_by_category(self, emails: list) -> dict:
        """Group emails by classification category."""
        groups = {cat: [] for cat in self.CATEGORY_ORDER}

        for email in emails:
            cat = email.get("classification", "fyi-read")
            if cat in groups:
                groups[cat].append(email)
            else:
                groups["fyi-read"].append(email)

        return groups

    def calculate_time_allocation(self, groups: dict) -> dict:
        """Calculate time needed per category."""
        allocation = {}

        for cat, emails in groups.items():
            total_minutes = sum(e.get("estimated_minutes", 5) for e in emails)
            allocation[cat] = {
                "count": len(emails),
                "minutes": total_minutes,
            }

        return allocation

    def format_email_line(self, email: dict, include_time: bool = True) -> str:
        """Format a single email as an action item line."""
        from_addr = email.get("from_addr", email.get("from", "Unknown"))
        # Extract name/email from "Name <email@domain.com>" format
        if "<" in from_addr:
            sender = from_addr.split("<")[0].strip()
        else:
            sender = from_addr.split("@")[0]

        subject = email.get("subject", "No subject")
        if len(subject) > 50:
            subject = subject[:47] + "..."

        action = email.get("suggested_action", "Review")
        minutes = email.get("estimated_minutes", 5)

        if include_time:
            return f"**[{sender}] {subject}** - {action} ({minutes} min)"
        else:
            return f"**[{sender}] {subject}** - {action}"

    def generate_markdown(self, report: dict) -> str:
        """Generate markdown action plan from classification report."""
        emails = report.get("emails", [])
        groups = self.group_by_category(emails)
        allocation = self.calculate_time_allocation(groups)

        # Calculate totals
        actionable_categories = ["urgent-response", "response-needed"]
        actionable_count = sum(allocation[cat]["count"] for cat in actionable_categories)
        total_time = sum(allocation[cat]["minutes"] for cat in actionable_categories)

        # Header
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        lines = [
            f"# Daily Email Action Plan - {date_str}",
            "",
            f"**Time Budget**: {self.time_budget} minutes | "
            f"**Priority Emails**: {actionable_count} | "
            f"**Estimated Time**: {total_time} min",
            "",
        ]

        # Time budget warning
        if total_time > self.time_budget:
            lines.extend(
                [
                    f"> **Warning**: Estimated time ({total_time} min) exceeds "
                    f"budget ({self.time_budget} min). Consider delegating or deferring.",
                    "",
                ]
            )

        # Urgent Response section
        urgent = groups["urgent-response"]
        if urgent:
            urgent_time = allocation["urgent-response"]["minutes"]
            lines.extend(
                [
                    f"## Urgent Response ({len(urgent)} emails, ~{urgent_time} min)",
                    "",
                ]
            )
            for i, email in enumerate(urgent, 1):
                lines.append(f"{i}. {self.format_email_line(email)}")
            lines.append("")

        # Response Needed section
        response = groups["response-needed"]
        if response:
            response_time = allocation["response-needed"]["minutes"]
            lines.extend(
                [
                    f"## Response Needed ({len(response)} emails, ~{response_time} min)",
                    "",
                ]
            )
            for i, email in enumerate(response, 1):
                lines.append(f"{i}. {self.format_email_line(email)}")
            lines.append("")

        # Delegate section
        delegate = groups["delegatable"]
        if delegate:
            lines.extend(
                [
                    f"## Delegate ({len(delegate)} emails)",
                    "",
                ]
            )
            for email in delegate:
                delegate_to = email.get("delegate_to", "appropriate team")
                subject = email.get("subject", "No subject")[:40]
                lines.append(f'- Forward "{subject}" to {delegate_to}')
            lines.append("")

        # FYI section
        fyi = groups["fyi-read"]
        if fyi:
            lines.extend(
                [
                    f"## FYI / Read Later ({len(fyi)} emails)",
                    "",
                    "- Skim and archive after review:",
                    "",
                ]
            )
            for email in fyi[:10]:  # Limit to first 10
                subject = email.get("subject", "No subject")[:50]
                lines.append(f"  - {subject}")
            if len(fyi) > 10:
                lines.append(f"  - ... and {len(fyi) - 10} more")
            lines.append("")

        # Archive section
        archive = groups["archive"]
        if archive:
            lines.extend(
                [
                    f"## Archive ({len(archive)} emails)",
                    "",
                    "- Batch archive without reading:",
                    "",
                ]
            )
            for email in archive[:5]:  # Limit to first 5
                subject = email.get("subject", "No subject")[:40]
                lines.append(f"  - {subject}")
            if len(archive) > 5:
                lines.append(f"  - ... and {len(archive) - 5} more")
            lines.append("")

        # Summary statistics
        summary = report.get("summary", {})
        lines.extend(
            [
                "---",
                "",
                "## Summary",
                "",
                "| Category | Count |",
                "|----------|-------|",
                f"| Urgent Response | {summary.get('urgent_response', 0)} |",
                f"| Response Needed | {summary.get('response_needed', 0)} |",
                f"| Delegatable | {summary.get('delegatable', 0)} |",
                f"| FYI/Read | {summary.get('fyi_read', 0)} |",
                f"| Archive | {summary.get('archive', 0)} |",
                f"| **Total** | **{report.get('total_emails', 0)}** |",
                "",
                f"*Generated at: {report.get('generated_at', 'N/A')}*",
            ]
        )

        return "\n".join(lines)

    def generate_json(self, report: dict) -> dict:
        """Generate structured JSON action plan."""
        emails = report.get("emails", [])
        groups = self.group_by_category(emails)
        allocation = self.calculate_time_allocation(groups)

        return {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "time_budget_minutes": self.time_budget,
            "summary": report.get("summary", {}),
            "time_allocation": allocation,
            "action_plan": {
                "urgent_response": [
                    {
                        "id": e["id"],
                        "from": e.get("from_addr", e.get("from", "")),
                        "subject": e["subject"],
                        "action": e.get("suggested_action", ""),
                        "minutes": e.get("estimated_minutes", 5),
                    }
                    for e in groups["urgent-response"]
                ],
                "response_needed": [
                    {
                        "id": e["id"],
                        "from": e.get("from_addr", e.get("from", "")),
                        "subject": e["subject"],
                        "action": e.get("suggested_action", ""),
                        "minutes": e.get("estimated_minutes", 5),
                    }
                    for e in groups["response-needed"]
                ],
                "delegate": [
                    {
                        "id": e["id"],
                        "subject": e["subject"],
                        "delegate_to": e.get("delegate_to", ""),
                    }
                    for e in groups["delegatable"]
                ],
                "fyi_count": len(groups["fyi-read"]),
                "archive_count": len(groups["archive"]),
            },
        }


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate daily email action plan from classification results.")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Input JSON file with classification results",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output file (markdown or JSON based on extension)",
    )
    parser.add_argument(
        "--time-budget",
        "-t",
        type=int,
        default=60,
        help="Available minutes for email responses (default: 60)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json", "auto"],
        default="auto",
        help="Output format (auto detects from file extension)",
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Load input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            report = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine output format
    output_path = Path(args.output)
    if args.format == "auto":
        if output_path.suffix.lower() in [".md", ".markdown"]:
            output_format = "markdown"
        else:
            output_format = "json"
    else:
        output_format = args.format

    # Generate plan
    generator = ActionPlanGenerator(time_budget=args.time_budget)

    if output_format == "markdown":
        content = generator.generate_markdown(report)
    else:
        content = json.dumps(generator.generate_json(report), indent=2)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Print summary
    summary = report.get("summary", {})
    urgent = summary.get("urgent_response", 0)
    response = summary.get("response_needed", 0)
    print(f"Action Plan Generated: {output_path}")
    print(f"  Priority emails: {urgent + response}")
    print(f"  Time budget: {args.time_budget} minutes")


if __name__ == "__main__":
    main()
