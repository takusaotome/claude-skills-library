#!/usr/bin/env python3
"""
Generate Markdown Summary from Thread Analysis

Takes the JSON output from analyze_thread.py and generates a
human-readable markdown summary.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def format_date(date_str: str) -> str:
    """Format ISO date string to readable format."""
    if not date_str:
        return "N/A"

    try:
        # Handle ISO format
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M")
        return date_str[:10]  # Return just date part
    except Exception:
        return date_str[:20] if date_str else "N/A"


def format_short_date(date_str: str) -> str:
    """Format date to short YYYY-MM-DD format."""
    if not date_str:
        return "N/A"

    try:
        if "T" in date_str:
            return date_str[:10]
        return date_str[:10]
    except Exception:
        return date_str[:10] if date_str else "N/A"


def get_status_emoji(classification: str) -> str:
    """Get emoji indicator for thread status."""
    emoji_map = {
        "active": "🟢",
        "resolved": "✅",
        "stale": "🟡",
        "escalated": "🔴",
        "awaiting_response": "⏳",
        "unknown": "❓",
    }
    return emoji_map.get(classification, "❓")


def generate_summary(analysis: dict) -> str:
    """Generate markdown summary from analysis data."""
    lines = []

    # Header
    subject = analysis.get("subject", "Unknown Subject")
    lines.append("# Email Thread Summary")
    lines.append("")

    # Thread metadata
    status = analysis.get("status", {})
    classification = status.get("classification", "unknown")
    status_emoji = get_status_emoji(classification)
    message_count = analysis.get("message_count", 0)

    date_range = analysis.get("date_range", {})
    duration = date_range.get("duration_days", 0)

    lines.append(f"## Thread: {subject}")
    lines.append(
        f"**Status**: {status_emoji} {classification.replace('_', ' ').title()} | "
        f"**Messages**: {message_count} | "
        f"**Duration**: {duration} days"
    )
    lines.append("")

    # Participants
    participants = analysis.get("participants", [])
    if participants:
        lines.append("## Participants")

        initiator = next((p for p in participants if p.get("role") == "initiator"), None)
        if initiator:
            lines.append(f"- **Initiator**: {initiator['name']} <{initiator['email']}>")

        responders = [p for p in participants if p.get("role") == "responder"]
        if responders:
            responder_names = ", ".join(p["name"] for p in responders[:5])
            if len(responders) > 5:
                responder_names += f" (+{len(responders) - 5} more)"
            lines.append(f"- **Responders**: {responder_names}")

        cc_list = [p for p in participants if p.get("role") == "cc"]
        if cc_list:
            cc_names = ", ".join(p["name"] for p in cc_list[:5])
            if len(cc_list) > 5:
                cc_names += f" (+{len(cc_list) - 5} more)"
            lines.append(f"- **CC**: {cc_names}")

        lines.append("")

    # Current Status section
    lines.append("## Current Status")
    days_since = status.get("days_since_last_action", 0)
    last_action = format_date(status.get("last_action_date", ""))
    confidence = status.get("confidence", 0)

    status_description = {
        "active": f"Thread is active with ongoing discussion. Last activity was {days_since} days ago.",
        "resolved": f"Thread has been resolved. Resolution confirmed {days_since} days ago.",
        "stale": f"Thread appears stale with no activity for {days_since} days. May require follow-up.",
        "escalated": f"Thread has been escalated. Escalation occurred {days_since} days ago.",
        "awaiting_response": f"Thread is awaiting a response. Request sent {days_since} days ago.",
        "unknown": "Thread status could not be determined.",
    }

    lines.append(status_description.get(classification, status_description["unknown"]))
    lines.append(f"(Confidence: {confidence:.0%}, Last action: {last_action})")
    lines.append("")

    # Timeline
    timeline = analysis.get("timeline", [])
    if timeline:
        lines.append("## Timeline")
        lines.append("| Date | Actor | Event |")
        lines.append("|------|-------|-------|")

        for event in timeline[:15]:  # Limit to 15 most recent
            date = format_short_date(event.get("date", ""))
            actor = event.get("actor", "Unknown")[:20]
            event_type = event.get("event_type", "")
            summary = event.get("summary", "")[:60]

            type_indicator = {
                "request": "📝",
                "response": "💬",
                "decision": "✓",
                "escalation": "⬆️",
                "resolution": "✅",
            }.get(event_type, "•")

            lines.append(f"| {date} | {actor} | {type_indicator} {summary} |")

        if len(timeline) > 15:
            lines.append(f"| ... | ... | (+{len(timeline) - 15} more events) |")

        lines.append("")

    # Pending Action Items
    action_items = analysis.get("action_items", [])
    pending_items = [ai for ai in action_items if ai.get("status") == "pending"]

    if pending_items:
        lines.append("## Pending Action Items")
        for item in pending_items:
            item_id = item.get("id", "")
            description = item.get("description", "")[:80]
            owner = item.get("owner", "TBD")
            due_date = item.get("due_date", "TBD")

            if due_date and due_date != "TBD":
                lines.append(f"- [ ] **[{item_id}]** {description} ({owner}, Due: {due_date})")
            else:
                lines.append(f"- [ ] **[{item_id}]** {description} ({owner})")

        lines.append("")

    # Completed Action Items (if any)
    completed_items = [ai for ai in action_items if ai.get("status") == "completed"]
    if completed_items:
        lines.append("## Completed Action Items")
        for item in completed_items[:5]:
            item_id = item.get("id", "")
            description = item.get("description", "")[:80]
            owner = item.get("owner", "")
            lines.append(f"- [x] **[{item_id}]** {description} ({owner})")

        if len(completed_items) > 5:
            lines.append(f"- ... (+{len(completed_items) - 5} more)")

        lines.append("")

    # Key Decisions
    decisions = analysis.get("key_decisions", [])
    if decisions:
        lines.append("## Key Decisions")
        for i, decision in enumerate(decisions[:10], 1):
            date = format_short_date(decision.get("date", ""))
            text = decision.get("decision", "")[:100]
            made_by = decision.get("made_by", "Unknown")
            lines.append(f"{i}. **{date}**: {text} (by {made_by})")

        if len(decisions) > 10:
            lines.append(f"   ... (+{len(decisions) - 10} more decisions)")

        lines.append("")

    # Outdated Information
    outdated = analysis.get("outdated_info", [])
    if outdated:
        lines.append("## Outdated Information")
        lines.append("The following information has been superseded:")
        lines.append("")

        for item in outdated[:5]:
            original = item.get("original_statement", "")[:50]
            superseded_by = item.get("superseded_by", "")[:80]
            superseded_date = format_short_date(item.get("superseded_date", ""))
            lines.append(f"- ~~{original}~~ superseded by: {superseded_by} ({superseded_date})")

        if len(outdated) > 5:
            lines.append(f"- ... (+{len(outdated) - 5} more)")

        lines.append("")

    # Footer
    lines.append("---")
    timestamp = analysis.get("analysis_timestamp", "")
    if timestamp:
        lines.append(f"*Generated: {format_date(timestamp)} UTC*")
    else:
        from datetime import timezone as tz

        lines.append(f"*Generated: {datetime.now(tz.utc).strftime('%Y-%m-%d %H:%M')} UTC*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate markdown summary from thread analysis JSON")
    parser.add_argument("--analysis", "-a", required=True, help="Input analysis JSON file path")
    parser.add_argument("--output", "-o", help="Output markdown file path (default: stdout)")

    args = parser.parse_args()

    # Load analysis
    analysis_path = Path(args.analysis)
    if not analysis_path.exists():
        print(f"Error: Analysis file not found: {args.analysis}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in analysis file: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate summary
    summary = generate_summary(analysis)

    # Output
    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary written to: {args.output}", file=sys.stderr)
    else:
        print(summary)


if __name__ == "__main__":
    main()
