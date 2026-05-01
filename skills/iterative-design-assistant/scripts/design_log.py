#!/usr/bin/env python3
"""
Design Log Manager - Track design decisions across iterative revision cycles.

This CLI tool manages a session-local design decision log that enables:
- Recording design changes with full context
- Resolving contextual references ("like before", "前回と同じ")
- Applying previous decisions to new elements
- Generating design history reports
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Constants
DEFAULT_LOG_FILE = ".design-log.json"
SCHEMA_VERSION = "1.0"

# Valid categories for design decisions
VALID_CATEGORIES = ["color", "typography", "layout", "content", "style"]


def get_log_path(log_file: str | None = None) -> Path:
    """Get the path to the design log file."""
    if log_file:
        return Path(log_file)
    return Path.cwd() / DEFAULT_LOG_FILE


def load_log(log_path: Path) -> dict[str, Any]:
    """Load the design log from file."""
    if not log_path.exists():
        return {}
    with open(log_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_log(log_path: Path, data: dict[str, Any]) -> None:
    """Save the design log to file."""
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_id(prefix: str) -> str:
    """Generate a unique ID with the given prefix."""
    short_uuid = str(uuid.uuid4())[:8]
    return f"{prefix}_{short_uuid}"


def get_timestamp() -> str:
    """Get the current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a new design session."""
    log_path = get_log_path(args.log_file)

    if log_path.exists() and not args.force:
        print(f"Error: Log file already exists: {log_path}", file=sys.stderr)
        print("Use --force to overwrite.", file=sys.stderr)
        return 1

    session_id = generate_id("session")
    timestamp = get_timestamp()

    log_data = {
        "schema_version": SCHEMA_VERSION,
        "session": {
            "id": session_id,
            "name": args.session_name or f"Session {timestamp[:10]}",
            "document": args.document or "unknown",
            "created_at": timestamp,
            "updated_at": timestamp,
        },
        "decisions": [],
        "design_tokens": {
            "colors": {},
            "typography": {},
            "layout": {},
            "style": {},
        },
    }

    save_log(log_path, log_data)
    # Status messages go to stderr so they don't mix with downstream JSON
    # output when commands are chained in the same Python process (see
    # test_history_json_output for the failure mode this guards against).
    print(f"Initialized design session: {session_id}", file=sys.stderr)
    print(f"Log file: {log_path}", file=sys.stderr)
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    """Record a new design decision."""
    log_path = get_log_path(args.log_file)
    log_data = load_log(log_path)

    if not log_data:
        print("Error: No active design session. Run 'init' first.", file=sys.stderr)
        return 1

    if args.category not in VALID_CATEGORIES:
        print(f"Error: Invalid category '{args.category}'.", file=sys.stderr)
        print(f"Valid categories: {', '.join(VALID_CATEGORIES)}", file=sys.stderr)
        return 1

    decision_id = generate_id("dec")
    timestamp = get_timestamp()

    decision = {
        "id": decision_id,
        "timestamp": timestamp,
        "category": args.category,
        "element": args.element,
        "old_value": args.old_value,
        "new_value": args.new_value,
        "reason": args.reason or "",
        "reference": args.reference or "",
        "applied_to": [args.element] if args.element else [],
        "superseded_by": None,
    }

    log_data["decisions"].append(decision)
    log_data["session"]["updated_at"] = timestamp

    save_log(log_path, log_data)
    print(f"Recorded decision: {decision_id}")
    print(f"  Category: {args.category}")
    print(f"  Element: {args.element}")
    print(f"  Change: {args.old_value} → {args.new_value}")
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    """Query previous design decisions."""
    log_path = get_log_path(args.log_file)
    log_data = load_log(log_path)

    if not log_data:
        print("Error: No active design session.", file=sys.stderr)
        return 1

    decisions = log_data.get("decisions", [])

    # Filter by category if specified
    if args.category:
        decisions = [d for d in decisions if d.get("category") == args.category]

    # Sort by timestamp descending (most recent first)
    decisions = sorted(decisions, key=lambda d: d.get("timestamp", ""), reverse=True)

    # Limit results
    limit = args.limit or 10
    decisions = decisions[:limit]

    if not decisions:
        print("No matching decisions found.")
        return 0

    print(f"Found {len(decisions)} decision(s):\n")
    for d in decisions:
        print(f"[{d['id']}] {d['timestamp'][:19]}")
        print(f"  Category: {d['category']}")
        print(f"  Element: {d['element']}")
        print(f"  Change: {d['old_value']} → {d['new_value']}")
        if d.get("reason"):
            print(f"  Reason: {d['reason']}")
        print()

    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Search decisions by keyword."""
    log_path = get_log_path(args.log_file)
    log_data = load_log(log_path)

    if not log_data:
        print("Error: No active design session.", file=sys.stderr)
        return 1

    keyword = args.keyword.lower()
    decisions = log_data.get("decisions", [])

    # Search in element, reason, reference, and values
    matching = []
    for d in decisions:
        searchable = " ".join(
            [
                str(d.get("element", "")),
                str(d.get("reason", "")),
                str(d.get("reference", "")),
                str(d.get("old_value", "")),
                str(d.get("new_value", "")),
            ]
        ).lower()
        if keyword in searchable:
            matching.append(d)

    # Sort by timestamp descending
    matching = sorted(matching, key=lambda d: d.get("timestamp", ""), reverse=True)

    # Limit results
    limit = args.limit or 10
    matching = matching[:limit]

    if not matching:
        print(f"No decisions matching '{args.keyword}' found.")
        return 0

    print(f"Found {len(matching)} decision(s) matching '{args.keyword}':\n")
    for d in matching:
        print(f"[{d['id']}] {d['timestamp'][:19]}")
        print(f"  Category: {d['category']}")
        print(f"  Element: {d['element']}")
        print(f"  Change: {d['old_value']} → {d['new_value']}")
        if d.get("reason"):
            print(f"  Reason: {d['reason']}")
        print()

    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    """Apply a previous decision to a new element."""
    log_path = get_log_path(args.log_file)
    log_data = load_log(log_path)

    if not log_data:
        print("Error: No active design session.", file=sys.stderr)
        return 1

    # Find the decision by ID
    decisions = log_data.get("decisions", [])
    source_decision = None
    for d in decisions:
        if d["id"] == args.decision_id:
            source_decision = d
            break

    if not source_decision:
        print(f"Error: Decision '{args.decision_id}' not found.", file=sys.stderr)
        return 1

    # Record the application
    timestamp = get_timestamp()

    # Add target element to applied_to list
    if args.target_element not in source_decision.get("applied_to", []):
        source_decision.setdefault("applied_to", []).append(args.target_element)

    # Create a new decision referencing the source
    new_decision_id = generate_id("dec")
    new_decision = {
        "id": new_decision_id,
        "timestamp": timestamp,
        "category": source_decision["category"],
        "element": args.target_element,
        "old_value": None,
        "new_value": source_decision["new_value"],
        "reason": args.context or f"Applied from {args.decision_id}",
        "reference": args.decision_id,
        "applied_to": [args.target_element],
        "superseded_by": None,
    }

    log_data["decisions"].append(new_decision)
    log_data["session"]["updated_at"] = timestamp

    save_log(log_path, log_data)
    print(f"Applied {args.decision_id} to {args.target_element}")
    print(f"  Value: {source_decision['new_value']}")
    print(f"  New decision ID: {new_decision_id}")
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    """Generate a design history report."""
    log_path = get_log_path(args.log_file)
    log_data = load_log(log_path)

    if not log_data:
        print("Error: No active design session.", file=sys.stderr)
        return 1

    session = log_data.get("session", {})
    decisions = log_data.get("decisions", [])
    tokens = log_data.get("design_tokens", {})

    # Sort decisions by timestamp
    decisions = sorted(decisions, key=lambda d: d.get("timestamp", ""))

    if args.format == "json":
        output = json.dumps(log_data, indent=2, ensure_ascii=False)
    else:  # markdown
        lines = [
            f"# Design History: {session.get('name', 'Unnamed Session')}",
            "",
            f"**Document**: {session.get('document', 'Unknown')}",
            f"**Session Started**: {session.get('created_at', '')[:19]}",
            f"**Last Updated**: {session.get('updated_at', '')[:19]}",
            "",
            "## Timeline",
            "",
        ]

        for d in decisions:
            ts = d.get("timestamp", "")[:19].replace("T", " ")
            category = d.get("category", "").title()
            lines.append(f"### {ts} - {category} Change")
            lines.append(f"- **Element**: {d.get('element', 'N/A')}")
            lines.append(f"- **Change**: {d.get('old_value', 'N/A')} → {d.get('new_value', 'N/A')}")
            if d.get("reason"):
                lines.append(f"- **Reason**: {d['reason']}")
            applied = d.get("applied_to", [])
            if len(applied) > 1:
                lines.append(f"- **Applied to**: {', '.join(applied)}")
            lines.append("")

        # Design tokens section
        has_tokens = any(tokens.get(cat) for cat in tokens)
        if has_tokens:
            lines.append("## Design Tokens")
            lines.append("")
            lines.append("| Category | Token | Value |")
            lines.append("|----------|-------|-------|")
            for category, category_tokens in tokens.items():
                for token_name, token_value in category_tokens.items():
                    lines.append(f"| {category.title()} | {token_name} | {token_value} |")
            lines.append("")

        output = "\n".join(lines)

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"History written to: {output_path}")
    else:
        print(output)

    return 0


def cmd_token(args: argparse.Namespace) -> int:
    """Manage design tokens."""
    log_path = get_log_path(args.log_file)
    log_data = load_log(log_path)

    if not log_data:
        print("Error: No active design session.", file=sys.stderr)
        return 1

    tokens = log_data.setdefault("design_tokens", {})

    if args.action == "set":
        if not args.category or not args.name or not args.value:
            print("Error: --category, --name, and --value required for 'set'.", file=sys.stderr)
            return 1

        category_tokens = tokens.setdefault(args.category, {})
        category_tokens[args.name] = args.value
        log_data["session"]["updated_at"] = get_timestamp()
        save_log(log_path, log_data)
        print(f"Set token: {args.category}.{args.name} = {args.value}")

    elif args.action == "get":
        if args.category and args.name:
            value = tokens.get(args.category, {}).get(args.name)
            if value:
                print(f"{args.category}.{args.name} = {value}")
            else:
                print(f"Token not found: {args.category}.{args.name}")
        elif args.category:
            category_tokens = tokens.get(args.category, {})
            if category_tokens:
                for name, value in category_tokens.items():
                    print(f"{args.category}.{name} = {value}")
            else:
                print(f"No tokens in category: {args.category}")
        else:
            for category, category_tokens in tokens.items():
                for name, value in category_tokens.items():
                    print(f"{category}.{name} = {value}")

    elif args.action == "delete":
        if not args.category or not args.name:
            print("Error: --category and --name required for 'delete'.", file=sys.stderr)
            return 1

        if args.category in tokens and args.name in tokens[args.category]:
            del tokens[args.category][args.name]
            log_data["session"]["updated_at"] = get_timestamp()
            save_log(log_path, log_data)
            print(f"Deleted token: {args.category}.{args.name}")
        else:
            print(f"Token not found: {args.category}.{args.name}")

    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    """Resolve a contextual reference to find matching decisions."""
    log_path = get_log_path(args.log_file)
    log_data = load_log(log_path)

    if not log_data:
        print("Error: No active design session.", file=sys.stderr)
        return 1

    reference = args.reference.lower()
    decisions = log_data.get("decisions", [])

    # Detect category from reference
    detected_category = None
    category_hints = {
        "color": ["色", "color", "colour", "カラー"],
        "typography": ["フォント", "font", "text", "テキスト", "文字"],
        "layout": ["レイアウト", "layout", "位置", "spacing", "配置"],
        "style": ["スタイル", "style", "効果", "effect", "border", "shadow"],
    }

    for category, hints in category_hints.items():
        for hint in hints:
            if hint in reference:
                detected_category = category
                break
        if detected_category:
            break

    # Detect recency from reference
    recent_only = False
    recency_hints = ["前回", "さっき", "last", "before", "recent", "just"]
    for hint in recency_hints:
        if hint in reference:
            recent_only = True
            break

    # Filter and score decisions
    candidates = []
    for d in decisions:
        score = 0

        # Category match
        if detected_category and d.get("category") == detected_category:
            score += 3

        # Recency bonus (last 5 decisions)
        if recent_only:
            sorted_decisions = sorted(decisions, key=lambda x: x.get("timestamp", ""), reverse=True)
            if d in sorted_decisions[:5]:
                score += 2

        if score > 0:
            candidates.append((score, d))

    # Sort by score descending, then by timestamp descending
    candidates.sort(key=lambda x: (x[0], x[1].get("timestamp", "")), reverse=True)

    limit = args.limit or 3
    candidates = candidates[:limit]

    if not candidates:
        print(f"Could not resolve reference: '{args.reference}'")
        print("Detected category:", detected_category or "unknown")
        return 1

    print(f"Resolved '{args.reference}':\n")
    print(f"Detected category: {detected_category or 'any'}")
    print(f"Recent only: {recent_only}\n")

    for score, d in candidates:
        print(f"[{d['id']}] (confidence: {score})")
        print(f"  Category: {d['category']}")
        print(f"  Element: {d['element']}")
        print(f"  Value: {d['new_value']}")
        if d.get("reason"):
            print(f"  Reason: {d['reason']}")
        print()

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Design Log Manager - Track design decisions across revision cycles")
    parser.add_argument(
        "--log-file",
        help=f"Path to log file (default: {DEFAULT_LOG_FILE})",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new design session")
    init_parser.add_argument("--document", help="Document name/path")
    init_parser.add_argument("--session-name", help="Name for this session")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing log")

    # record command
    record_parser = subparsers.add_parser("record", help="Record a design decision")
    record_parser.add_argument("--category", required=True, choices=VALID_CATEGORIES)
    record_parser.add_argument("--element", required=True, help="Element being changed")
    record_parser.add_argument("--old-value", help="Previous value")
    record_parser.add_argument("--new-value", required=True, help="New value")
    record_parser.add_argument("--reason", help="Reason for the change")
    record_parser.add_argument("--reference", help="Reference location (e.g., slide-3)")

    # query command
    query_parser = subparsers.add_parser("query", help="Query previous decisions")
    query_parser.add_argument("--category", choices=VALID_CATEGORIES)
    query_parser.add_argument("--limit", type=int, default=10)

    # search command
    search_parser = subparsers.add_parser("search", help="Search decisions by keyword")
    search_parser.add_argument("--keyword", required=True)
    search_parser.add_argument("--limit", type=int, default=10)

    # apply command
    apply_parser = subparsers.add_parser("apply", help="Apply a previous decision")
    apply_parser.add_argument("--decision-id", required=True)
    apply_parser.add_argument("--target-element", required=True)
    apply_parser.add_argument("--context", help="Context for this application")

    # history command
    history_parser = subparsers.add_parser("history", help="Generate history report")
    history_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    history_parser.add_argument("--output", help="Output file path")

    # token command
    token_parser = subparsers.add_parser("token", help="Manage design tokens")
    token_parser.add_argument("action", choices=["set", "get", "delete"])
    token_parser.add_argument("--category", choices=VALID_CATEGORIES)
    token_parser.add_argument("--name", help="Token name")
    token_parser.add_argument("--value", help="Token value")

    # resolve command
    resolve_parser = subparsers.add_parser("resolve", help="Resolve a contextual reference")
    resolve_parser.add_argument("--reference", required=True, help="The contextual reference to resolve")
    resolve_parser.add_argument("--limit", type=int, default=3)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "init": cmd_init,
        "record": cmd_record,
        "query": cmd_query,
        "search": cmd_search,
        "apply": cmd_apply,
        "history": cmd_history,
        "token": cmd_token,
        "resolve": cmd_resolve,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
