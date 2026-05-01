#!/usr/bin/env python3
"""
Action Status Updater CLI Tool.

Track and update action item status across multiple communication channels
using natural language updates in Japanese or English.
"""

import argparse
import json
import sys
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None

# Import the NL parser module
from nl_parser import Intent, ParseResult, parse_status_update


class Status(Enum):
    """Action item status values."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELEGATED = "delegated"
    DEFERRED = "deferred"


@dataclass
class HistoryEntry:
    """A single status change history entry."""

    timestamp: str
    from_status: str
    to_status: str
    trigger: str


@dataclass
class ActionItem:
    """A single action item."""

    id: str
    channel: str
    assignee: str
    description: str
    status: str = "pending"
    created_at: str = ""
    updated_at: str = ""
    due_date: Optional[str] = None
    delegated_to: Optional[str] = None
    history: list = field(default_factory=list)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at


@dataclass
class ActionState:
    """The full action tracking state."""

    schema_version: str = "1.0"
    last_updated: str = ""
    action_items: list = field(default_factory=list)

    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = datetime.now(timezone.utc).isoformat()


def generate_id() -> str:
    """Generate a unique action item ID."""
    return f"act-{uuid.uuid4().hex[:8]}"


def load_state(state_file: Path) -> ActionState:
    """Load state from YAML file."""
    if not state_file.exists():
        return ActionState()

    if yaml is None:
        print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
        sys.exit(1)

    with open(state_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    state = ActionState(
        schema_version=data.get("schema_version", "1.0"),
        last_updated=data.get("last_updated", ""),
    )

    for item_data in data.get("action_items", []):
        item = ActionItem(
            id=item_data.get("id", generate_id()),
            channel=item_data.get("channel", ""),
            assignee=item_data.get("assignee", ""),
            description=item_data.get("description", ""),
            status=item_data.get("status", "pending"),
            created_at=item_data.get("created_at", ""),
            updated_at=item_data.get("updated_at", ""),
            due_date=item_data.get("due_date"),
            delegated_to=item_data.get("delegated_to"),
            history=item_data.get("history", []),
        )
        state.action_items.append(item)

    return state


def save_state(state: ActionState, state_file: Path) -> None:
    """Save state to YAML file."""
    if yaml is None:
        print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
        sys.exit(1)

    state.last_updated = datetime.now(timezone.utc).isoformat()

    data = {
        "schema_version": state.schema_version,
        "last_updated": state.last_updated,
        "action_items": [asdict(item) for item in state.action_items],
    }

    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def find_matching_items(state: ActionState, parse_result: ParseResult) -> list[tuple[ActionItem, float]]:
    """
    Find action items matching the parsed update.

    Returns list of (item, confidence) tuples sorted by confidence descending.
    """
    matches = []

    for item in state.action_items:
        score = 0.0

        # Person match
        if parse_result.person:
            if parse_result.person.lower() == item.assignee.lower():
                score += 0.4
            elif parse_result.person.lower() in item.assignee.lower():
                score += 0.2

        # Channel match
        if parse_result.channel:
            if parse_result.channel.lower() == item.channel.lower():
                score += 0.3

        # Keyword match in description
        if parse_result.keywords:
            desc_lower = item.description.lower()
            keyword_matches = sum(1 for kw in parse_result.keywords if kw.lower() in desc_lower)
            if keyword_matches > 0:
                score += min(0.3, keyword_matches * 0.1)

        # Prefer pending/in_progress items
        if item.status in ["pending", "in_progress"]:
            score += 0.1

        if score > 0:
            matches.append((item, score))

    # Sort by confidence descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def intent_to_status(intent: Intent) -> str:
    """Convert parsed intent to status string."""
    mapping = {
        Intent.COMPLETED: Status.COMPLETED.value,
        Intent.DELEGATED: Status.DELEGATED.value,
        Intent.DEFERRED: Status.DEFERRED.value,
        Intent.IN_PROGRESS: Status.IN_PROGRESS.value,
    }
    return mapping.get(intent, Status.PENDING.value)


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a new state file."""
    state_file = Path(args.state_file)

    if state_file.exists() and not args.force:
        print(f"State file already exists: {state_file}", file=sys.stderr)
        print("Use --force to overwrite.", file=sys.stderr)
        return 1

    state = ActionState()
    save_state(state, state_file)
    print(f"Initialized new state file: {state_file}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    """Add a new action item."""
    state_file = Path(args.state_file)
    state = load_state(state_file)

    item = ActionItem(
        id=generate_id(),
        channel=args.channel or "general",
        assignee=args.assignee or "self",
        description=args.description,
        due_date=args.due,
    )

    state.action_items.append(item)
    save_state(state, state_file)

    print(f"Added action item: {item.id}")
    print(f"  Channel: {item.channel}")
    print(f"  Assignee: {item.assignee}")
    print(f"  Description: {item.description}")
    if item.due_date:
        print(f"  Due: {item.due_date}")

    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Update action item status via natural language."""
    state_file = Path(args.state_file)
    state = load_state(state_file)

    # Parse the natural language input
    parse_result = parse_status_update(args.input)

    if args.debug:
        print("Debug - Parse result:")
        print(f"  Intent: {parse_result.intent.value}")
        print(f"  Language: {parse_result.language.value}")
        print(f"  Person: {parse_result.person}")
        print(f"  Delegatee: {parse_result.delegatee}")
        print(f"  Channel: {parse_result.channel}")
        print(f"  Keywords: {parse_result.keywords}")
        print(f"  Confidence: {parse_result.confidence:.2f}")
        print()

    if parse_result.intent == Intent.UNKNOWN:
        print("Could not determine intent from input.", file=sys.stderr)
        print(f"Input: {args.input}", file=sys.stderr)
        return 1

    # Find matching items
    matches = find_matching_items(state, parse_result)

    if not matches:
        print("No matching action items found.", file=sys.stderr)
        print(f"Input: {args.input}", file=sys.stderr)
        return 1

    # Use the best match
    best_item, confidence = matches[0]

    if args.debug:
        print(f"Debug - Matched item: {best_item.id} (confidence: {confidence:.2f})")
        print(f"  Description: {best_item.description}")
        print()

    # Warn if low confidence
    if confidence < 0.5 and not args.force:
        print(f"Low confidence match ({confidence:.2f}). Matched item:")
        print(f"  [{best_item.id}] {best_item.description}")
        print("Use --force to apply anyway, or be more specific.")
        return 1

    # Update the item
    old_status = best_item.status
    new_status = intent_to_status(parse_result.intent)

    if old_status == new_status and not args.force:
        print(f"Item already in status '{new_status}': {best_item.description}")
        return 0

    best_item.status = new_status
    best_item.updated_at = datetime.now(timezone.utc).isoformat()

    # Handle delegation
    if parse_result.intent == Intent.DELEGATED and parse_result.delegatee:
        best_item.delegated_to = parse_result.delegatee

    # Add history entry
    history_entry = {
        "timestamp": best_item.updated_at,
        "from_status": old_status,
        "to_status": new_status,
        "trigger": args.input,
    }
    best_item.history.append(history_entry)

    save_state(state, state_file)

    print(f"Updated: {best_item.description}")
    print(f"  Status: {old_status} -> {new_status}")
    if best_item.delegated_to:
        print(f"  Delegated to: {best_item.delegated_to}")

    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Generate a status report."""
    state_file = Path(args.state_file)
    state = load_state(state_file)

    if not state.action_items:
        print("No action items found.")
        return 0

    # Count by status
    status_counts = {}
    for item in state.action_items:
        status_counts[item.status] = status_counts.get(item.status, 0) + 1

    # Group by channel
    by_channel: dict[str, list[ActionItem]] = {}
    for item in state.action_items:
        if item.channel not in by_channel:
            by_channel[item.channel] = []
        by_channel[item.channel].append(item)

    if args.format == "json":
        report = {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "total": len(state.action_items),
                **status_counts,
            },
            "items": [asdict(item) for item in state.action_items],
        }
        output = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        # Markdown format
        lines = [
            "# Action Status Report",
            f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC",
            "",
            "## Summary",
            f"- Total: {len(state.action_items)}",
        ]
        for status, count in sorted(status_counts.items()):
            lines.append(f"- {status.title()}: {count}")

        lines.append("")
        lines.append("## By Channel")

        for channel, items in sorted(by_channel.items()):
            lines.append(f"\n### {channel.title()} ({len(items)} items)")
            lines.append("| Assignee | Description | Status | Due |")
            lines.append("|----------|-------------|--------|-----|")

            for item in items:
                status_icon = "✅" if item.status == "completed" else "⏳" if item.status == "pending" else "🔄"
                due = item.due_date or "-"
                lines.append(f"| {item.assignee} | {item.description} | {status_icon} {item.status} | {due} |")

        output = "\n".join(lines)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report saved to: {output_path}")
    else:
        print(output)

    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """Export action items for integration."""
    state_file = Path(args.state_file)
    state = load_state(state_file)

    if yaml is None:
        print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
        return 1

    # Prepare export data
    export_data = {
        "schema_version": "1.0",
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "pending_actions": [],
        "completed_today": [],
        "delegated": [],
    }

    today = datetime.now(timezone.utc).date().isoformat()

    for item in state.action_items:
        if item.status == "pending":
            export_data["pending_actions"].append(
                {
                    "channel": item.channel,
                    "assignee": item.assignee,
                    "description": item.description,
                    "due": item.due_date,
                }
            )
        elif item.status == "completed":
            # Check if completed today
            if item.updated_at.startswith(today):
                export_data["completed_today"].append(
                    {
                        "channel": item.channel,
                        "assignee": item.assignee,
                        "description": item.description,
                        "completed_at": item.updated_at,
                    }
                )
        elif item.status == "delegated":
            export_data["delegated"].append(
                {
                    "channel": item.channel,
                    "original_assignee": item.assignee,
                    "delegated_to": item.delegated_to or "unknown",
                    "description": item.description,
                    "delegated_at": item.updated_at,
                }
            )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(export_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"Export saved to: {output_path}")
    else:
        print(yaml.dump(export_data, allow_unicode=True, default_flow_style=False, sort_keys=False))

    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List all action items."""
    state_file = Path(args.state_file)
    state = load_state(state_file)

    if not state.action_items:
        print("No action items found.")
        return 0

    # Filter by status if specified
    items = state.action_items
    if args.status:
        items = [i for i in items if i.status == args.status]

    if not items:
        print(f"No items with status '{args.status}'.")
        return 0

    for item in items:
        status_icon = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅",
            "delegated": "👥",
            "deferred": "⏸️",
        }.get(item.status, "❓")

        print(f"{status_icon} [{item.id}] {item.description}")
        print(f"    Channel: {item.channel} | Assignee: {item.assignee} | Status: {item.status}")
        if item.due_date:
            print(f"    Due: {item.due_date}")
        if item.delegated_to:
            print(f"    Delegated to: {item.delegated_to}")
        print()

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Track and update action item status using natural language.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new state file")
    init_parser.add_argument("--state-file", required=True, help="Path to state file")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing file")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new action item")
    add_parser.add_argument("--state-file", required=True, help="Path to state file")
    add_parser.add_argument("--channel", help="Communication channel (email, slack, meeting)")
    add_parser.add_argument("--assignee", help="Person assigned to this item")
    add_parser.add_argument("--description", required=True, help="Action item description")
    add_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")

    # update command
    update_parser = subparsers.add_parser("update", help="Update status via natural language")
    update_parser.add_argument("--state-file", required=True, help="Path to state file")
    update_parser.add_argument("--input", required=True, help="Natural language status update")
    update_parser.add_argument("--force", action="store_true", help="Apply even with low confidence")
    update_parser.add_argument("--debug", action="store_true", help="Show debug information")

    # report command
    report_parser = subparsers.add_parser("report", help="Generate status report")
    report_parser.add_argument("--state-file", required=True, help="Path to state file")
    report_parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    report_parser.add_argument("--output", help="Output file path")

    # export command
    export_parser = subparsers.add_parser("export", help="Export for integration")
    export_parser.add_argument("--state-file", required=True, help="Path to state file")
    export_parser.add_argument(
        "--format", choices=["daily-comms", "slack", "email"], default="daily-comms", help="Export format"
    )
    export_parser.add_argument("--output", help="Output file path")

    # list command
    list_parser = subparsers.add_parser("list", help="List action items")
    list_parser.add_argument("--state-file", required=True, help="Path to state file")
    list_parser.add_argument("--status", help="Filter by status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "update": cmd_update,
        "report": cmd_report,
        "export": cmd_export,
        "list": cmd_list,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
