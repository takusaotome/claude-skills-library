#!/usr/bin/env python3
"""
Check Staleness of Cached Thread Summary

Compare a cached thread analysis against the current thread state
to detect drift and determine if the cache is stale.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_iso_date(date_str: str) -> datetime | None:
    """Parse ISO8601 date string to datetime."""
    if not date_str:
        return None

    try:
        if date_str.endswith("Z"):
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None


def compare_message_counts(cached: dict, current: dict) -> list[dict]:
    """Check for new messages since cache."""
    reasons = []

    cached_count = cached.get("message_count", 0)
    current_count = current.get("message_count", 0)

    if current_count > cached_count:
        new_messages = current_count - cached_count
        severity = "high" if new_messages >= 3 else "medium" if new_messages >= 1 else "low"
        reasons.append(
            {
                "type": "new_messages",
                "description": f"{new_messages} new message(s) since cache was created",
                "severity": severity,
            }
        )

    return reasons


def compare_status(cached: dict, current: dict) -> list[dict]:
    """Check for status changes."""
    reasons = []

    cached_status = cached.get("status", {}).get("classification", "unknown")
    current_status = current.get("status", {}).get("classification", "unknown")

    if cached_status != current_status:
        # Status changes from active to resolved/escalated are high severity
        if current_status in ["resolved", "escalated"] and cached_status == "active":
            severity = "high"
        elif current_status == "stale" and cached_status == "active":
            severity = "medium"
        else:
            severity = "low"

        reasons.append(
            {
                "type": "status_change",
                "description": f"Status changed from '{cached_status}' to '{current_status}'",
                "severity": severity,
            }
        )

    return reasons


def compare_action_items(cached: dict, current: dict) -> list[dict]:
    """Check for action item changes."""
    reasons = []

    cached_items = {ai["id"]: ai for ai in cached.get("action_items", [])}
    current_items = {ai["id"]: ai for ai in current.get("action_items", [])}

    # Check for new action items
    new_item_ids = set(current_items.keys()) - set(cached_items.keys())
    if new_item_ids:
        reasons.append(
            {
                "type": "action_item_update",
                "description": f"{len(new_item_ids)} new action item(s) identified",
                "severity": "medium",
            }
        )

    # Check for status changes in existing items
    status_changes = 0
    for item_id, current_item in current_items.items():
        if item_id in cached_items:
            cached_item = cached_items[item_id]
            if cached_item.get("status") != current_item.get("status"):
                status_changes += 1

    if status_changes > 0:
        reasons.append(
            {
                "type": "action_item_update",
                "description": f"{status_changes} action item(s) changed status",
                "severity": "medium",
            }
        )

    return reasons


def compare_decisions(cached: dict, current: dict) -> list[dict]:
    """Check for new decisions."""
    reasons = []

    cached_decisions = len(cached.get("key_decisions", []))
    current_decisions = len(current.get("key_decisions", []))

    if current_decisions > cached_decisions:
        new_decisions = current_decisions - cached_decisions
        reasons.append(
            {
                "type": "decision_change",
                "description": f"{new_decisions} new decision(s) made since cache",
                "severity": "high" if new_decisions >= 2 else "medium",
            }
        )

    return reasons


def compare_date_ranges(cached: dict, current: dict) -> int:
    """Calculate number of new messages based on date range."""
    cached_last = cached.get("date_range", {}).get("last_message", "")
    current_last = current.get("date_range", {}).get("last_message", "")

    cached_date = parse_iso_date(cached_last)
    current_date = parse_iso_date(current_last)

    if cached_date and current_date and current_date > cached_date:
        return current.get("message_count", 0) - cached.get("message_count", 0)

    return 0


def determine_recommendation(reasons: list[dict], new_messages: int) -> str:
    """Determine recommendation based on staleness reasons."""
    if not reasons:
        return "ignore"

    # Check for high severity reasons
    high_severity = any(r["severity"] == "high" for r in reasons)
    medium_severity = any(r["severity"] == "medium" for r in reasons)

    if high_severity or new_messages >= 3:
        return "refresh"
    elif medium_severity or new_messages >= 1:
        return "review"
    else:
        return "ignore"


def check_staleness(cached: dict, current: dict) -> dict:
    """Compare cached and current analysis to detect staleness."""
    reasons = []

    # Run all comparisons
    reasons.extend(compare_message_counts(cached, current))
    reasons.extend(compare_status(cached, current))
    reasons.extend(compare_action_items(cached, current))
    reasons.extend(compare_decisions(cached, current))

    # Calculate new messages
    new_messages = compare_date_ranges(cached, current)

    # Determine if stale
    is_stale = len(reasons) > 0

    # Get recommendation
    recommendation = determine_recommendation(reasons, new_messages)

    return {
        "schema_version": "1.0",
        "is_stale": is_stale,
        "staleness_reasons": reasons,
        "cached_summary_date": cached.get("analysis_timestamp", ""),
        "current_thread_date": current.get("date_range", {}).get("last_message", ""),
        "new_messages_since_cache": max(new_messages, 0),
        "recommendation": recommendation,
    }


def main():
    parser = argparse.ArgumentParser(description="Check if cached thread summary is stale compared to current state")
    parser.add_argument("--cached", "-c", required=True, help="Cached analysis JSON file path")
    parser.add_argument("--current", "-u", required=True, help="Current analysis JSON file path")
    parser.add_argument("--output", "-o", help="Output staleness report JSON file path (default: stdout)")

    args = parser.parse_args()

    # Load cached analysis
    cached_path = Path(args.cached)
    if not cached_path.exists():
        print(f"Error: Cached file not found: {args.cached}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(cached_path, "r", encoding="utf-8") as f:
            cached = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in cached file: {e}", file=sys.stderr)
        sys.exit(1)

    # Load current analysis
    current_path = Path(args.current)
    if not current_path.exists():
        print(f"Error: Current file not found: {args.current}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(current_path, "r", encoding="utf-8") as f:
            current = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in current file: {e}", file=sys.stderr)
        sys.exit(1)

    # Check staleness
    report = check_staleness(cached, current)

    # Output
    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Staleness report written to: {args.output}", file=sys.stderr)
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))

    # Exit with code indicating staleness
    sys.exit(0 if not report["is_stale"] else 1)


if __name__ == "__main__":
    main()
