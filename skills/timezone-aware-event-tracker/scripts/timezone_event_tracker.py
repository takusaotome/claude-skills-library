#!/usr/bin/env python3
"""
Timezone-Aware Event Tracker

Tracks and correlates events across multiple timezones with automatic conversion.
Handles DST transitions and generates time-normalized reports.

Usage:
    python timezone_event_tracker.py parse --input events.csv --output normalized.json
    python timezone_event_tracker.py correlate --input normalized.json --window-minutes 5
    python timezone_event_tracker.py report --input normalized.json --timezones "America/Los_Angeles,Asia/Tokyo"
    python timezone_event_tracker.py dst-check --input normalized.json --year 2024
"""

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

# Use zoneinfo for Python 3.9+
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for older Python or missing tzdata
    try:
        from backports.zoneinfo import ZoneInfo
    except ImportError:
        print("Error: zoneinfo module not available. Install tzdata or use Python 3.9+", file=sys.stderr)
        sys.exit(1)


# Timezone abbreviation to IANA name mapping
TZ_ABBREVIATIONS = {
    # US timezones
    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
    "MST": "America/Denver",
    "MDT": "America/Denver",
    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "EST": "America/New_York",
    "EDT": "America/New_York",
    # Asia-Pacific
    "JST": "Asia/Tokyo",
    "KST": "Asia/Seoul",
    "SGT": "Asia/Singapore",
    "AEST": "Australia/Sydney",
    "AEDT": "Australia/Sydney",
    # Europe
    "GMT": "Europe/London",
    "BST": "Europe/London",
    "CET": "Europe/Paris",
    "CEST": "Europe/Paris",
    # Universal
    "UTC": "UTC",
    "Z": "UTC",
}


@dataclass
class Event:
    """Represents a single event with timezone information."""

    id: str
    original_timestamp: str
    normalized_timestamp: str  # ISO format UTC
    source_timezone: str
    description: str
    metadata: dict
    dst_status: str  # "standard_time", "daylight_time", or "ambiguous"
    ambiguity_warning: Optional[str] = None


@dataclass
class CorrelationGroup:
    """Group of correlated events."""

    group_id: str
    event_ids: list
    time_span_seconds: float
    pattern: str


def parse_timestamp(raw: str, default_tz: str = "UTC") -> tuple[datetime, str, str, Optional[str]]:
    """
    Parse a timestamp string and return normalized datetime.

    Returns: (datetime_utc, source_timezone, dst_status, warning)
    """
    raw = raw.strip()
    warning = None

    # Pattern 1: ISO 8601 with offset (2024-03-15T10:30:00-07:00)
    iso_offset_pattern = r"^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})([+-]\d{2}:?\d{2}|Z)$"
    match = re.match(iso_offset_pattern, raw)
    if match:
        dt_str, offset = match.groups()
        if offset == "Z":
            offset = "+00:00"
        elif len(offset) == 5 and ":" not in offset:
            offset = offset[:3] + ":" + offset[3:]
        full_str = dt_str.replace(" ", "T") + offset
        dt = datetime.fromisoformat(full_str)
        dt_utc = dt.astimezone(ZoneInfo("UTC"))
        # Determine source timezone from offset
        return dt_utc, "UTC (from offset)", "unknown", warning

    # Pattern 2: Datetime with timezone abbreviation (2024-03-15 10:30:00 PST)
    tz_abbrev_pattern = r"^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})\s+([A-Z]{2,4})$"
    match = re.match(tz_abbrev_pattern, raw)
    if match:
        dt_str, tz_abbrev = match.groups()
        tz_name = TZ_ABBREVIATIONS.get(tz_abbrev.upper(), default_tz)
        if tz_abbrev.upper() not in TZ_ABBREVIATIONS:
            warning = f"Unknown timezone abbreviation '{tz_abbrev}', using {default_tz}"

        tz = ZoneInfo(tz_name)
        # Parse naive datetime and localize
        dt_naive = datetime.fromisoformat(dt_str.replace(" ", "T"))
        try:
            dt_local = dt_naive.replace(tzinfo=tz)
        except Exception:
            dt_local = dt_naive.replace(tzinfo=tz)

        dt_utc = dt_local.astimezone(ZoneInfo("UTC"))
        dst_status = get_dst_status(dt_local, tz)
        return dt_utc, tz_name, dst_status, warning

    # Pattern 3: Just datetime, no timezone (use default)
    try:
        dt_naive = datetime.fromisoformat(raw.replace(" ", "T"))
        tz = ZoneInfo(default_tz)
        dt_local = dt_naive.replace(tzinfo=tz)
        dt_utc = dt_local.astimezone(ZoneInfo("UTC"))
        warning = f"No timezone specified, assumed {default_tz}"
        dst_status = get_dst_status(dt_local, tz)
        return dt_utc, default_tz, dst_status, warning
    except ValueError:
        pass

    # Pattern 4: Common log format (15/Mar/2024:10:30:00 -0700)
    log_pattern = r"^(\d{2})/([A-Za-z]{3})/(\d{4}):(\d{2}):(\d{2}):(\d{2})\s*([+-]\d{4})$"
    match = re.match(log_pattern, raw)
    if match:
        day, month_str, year, hour, minute, second, offset = match.groups()
        months = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }
        month = months.get(month_str, 1)
        dt_str = f"{year}-{month:02d}-{day}T{hour}:{minute}:{second}{offset[:3]}:{offset[3:]}"
        dt = datetime.fromisoformat(dt_str)
        dt_utc = dt.astimezone(ZoneInfo("UTC"))
        return dt_utc, f"UTC{offset}", "unknown", warning

    raise ValueError(f"Unable to parse timestamp: {raw}")


def get_dst_status(dt: datetime, tz: ZoneInfo) -> str:
    """Determine DST status for a datetime in a timezone."""
    if dt.tzinfo is None:
        return "unknown"

    try:
        dst_offset = dt.dst()
        if dst_offset is None:
            return "unknown"
        elif dst_offset.total_seconds() > 0:
            return "daylight_time"
        else:
            return "standard_time"
    except Exception:
        return "unknown"


def get_dst_transitions(year: int, tz_name: str) -> list[tuple[datetime, str]]:
    """Get DST transition dates for a timezone in a given year."""
    tz = ZoneInfo(tz_name)
    transitions = []

    # Check each day of the year for offset changes
    current_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    prev_offset = None
    while current_date <= end_date:
        dt = datetime(current_date.year, current_date.month, current_date.day, 12, 0, tzinfo=tz)
        current_offset = dt.utcoffset()

        if prev_offset is not None and current_offset != prev_offset:
            # Transition found
            transition_type = "spring_forward" if current_offset > prev_offset else "fall_back"
            transitions.append(
                (datetime(current_date.year, current_date.month, current_date.day, tzinfo=tz), transition_type)
            )

        prev_offset = current_offset
        current_date += timedelta(days=1)

    return transitions


def parse_events(input_file: Path, reference_tz: str = "UTC") -> list[Event]:
    """Parse events from CSV or JSON file."""
    events = []

    if input_file.suffix.lower() == ".csv":
        with open(input_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                # Expect columns: timestamp, description, [timezone], [severity], [source]
                raw_ts = row.get("timestamp", "")
                description = row.get("description", "")
                source_tz_hint = row.get("timezone", reference_tz)

                try:
                    dt_utc, source_tz, dst_status, warning = parse_timestamp(raw_ts, source_tz_hint)
                except ValueError as e:
                    print(f"Warning: Skipping row {i + 1}: {e}", file=sys.stderr)
                    continue

                metadata = {}
                if "severity" in row:
                    metadata["severity"] = row["severity"]
                if "source" in row:
                    metadata["source_system"] = row["source"]

                event = Event(
                    id=f"evt-{i + 1:04d}",
                    original_timestamp=raw_ts,
                    normalized_timestamp=dt_utc.isoformat(),
                    source_timezone=source_tz,
                    description=description,
                    metadata=metadata,
                    dst_status=dst_status,
                    ambiguity_warning=warning,
                )
                events.append(event)

    elif input_file.suffix.lower() == ".json":
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle both list of events and object with "events" key
        event_list = data if isinstance(data, list) else data.get("events", [])

        for i, item in enumerate(event_list):
            raw_ts = item.get("timestamp", item.get("original_timestamp", ""))
            description = item.get("description", "")
            source_tz_hint = item.get("timezone", item.get("source_timezone", reference_tz))

            try:
                dt_utc, source_tz, dst_status, warning = parse_timestamp(raw_ts, source_tz_hint)
            except ValueError as e:
                print(f"Warning: Skipping item {i + 1}: {e}", file=sys.stderr)
                continue

            metadata = item.get("metadata", {})
            if "severity" in item:
                metadata["severity"] = item["severity"]
            if "source" in item:
                metadata["source_system"] = item["source"]

            event = Event(
                id=item.get("id", f"evt-{i + 1:04d}"),
                original_timestamp=raw_ts,
                normalized_timestamp=dt_utc.isoformat(),
                source_timezone=source_tz,
                description=description,
                metadata=metadata,
                dst_status=dst_status,
                ambiguity_warning=warning,
            )
            events.append(event)

    else:
        raise ValueError(f"Unsupported file format: {input_file.suffix}")

    # Sort events by normalized timestamp
    events.sort(key=lambda e: e.normalized_timestamp)

    return events


def correlate_events(events: list[Event], window_minutes: int = 5) -> list[CorrelationGroup]:
    """Group events that occur within the specified time window."""
    if not events:
        return []

    groups = []
    window = timedelta(minutes=window_minutes)

    # Sort by timestamp
    sorted_events = sorted(events, key=lambda e: e.normalized_timestamp)

    current_group_events = [sorted_events[0]]
    group_counter = 1

    for event in sorted_events[1:]:
        current_time = datetime.fromisoformat(event.normalized_timestamp)
        group_start_time = datetime.fromisoformat(current_group_events[0].normalized_timestamp)

        if current_time - group_start_time <= window:
            current_group_events.append(event)
        else:
            # Close current group if it has multiple events
            if len(current_group_events) > 1:
                start = datetime.fromisoformat(current_group_events[0].normalized_timestamp)
                end = datetime.fromisoformat(current_group_events[-1].normalized_timestamp)
                span = (end - start).total_seconds()

                groups.append(
                    CorrelationGroup(
                        group_id=f"corr-{group_counter:03d}",
                        event_ids=[e.id for e in current_group_events],
                        time_span_seconds=span,
                        pattern=classify_pattern(current_group_events),
                    )
                )
                group_counter += 1

            current_group_events = [event]

    # Handle last group
    if len(current_group_events) > 1:
        start = datetime.fromisoformat(current_group_events[0].normalized_timestamp)
        end = datetime.fromisoformat(current_group_events[-1].normalized_timestamp)
        span = (end - start).total_seconds()

        groups.append(
            CorrelationGroup(
                group_id=f"corr-{group_counter:03d}",
                event_ids=[e.id for e in current_group_events],
                time_span_seconds=span,
                pattern=classify_pattern(current_group_events),
            )
        )

    return groups


def classify_pattern(events: list[Event]) -> str:
    """Classify the pattern of a group of events."""
    if len(events) <= 1:
        return "single_event"

    # Check for cascading pattern (rapid succession)
    if len(events) >= 3:
        timestamps = [datetime.fromisoformat(e.normalized_timestamp) for e in events]
        intervals = [(timestamps[i + 1] - timestamps[i]).total_seconds() for i in range(len(timestamps) - 1)]
        avg_interval = sum(intervals) / len(intervals)

        if avg_interval < 60:  # Less than 1 minute average
            return "cascading_failure"
        elif avg_interval < 300:  # Less than 5 minutes
            return "rapid_sequence"

    # Check for simultaneous events
    timestamps = [datetime.fromisoformat(e.normalized_timestamp) for e in events]
    if all(t == timestamps[0] for t in timestamps):
        return "simultaneous"

    return "related_events"


def generate_report(
    events: list[Event], groups: list[CorrelationGroup], timezones: list[str], format: str = "markdown"
) -> str:
    """Generate a timeline report in the specified format."""
    now = datetime.now(ZoneInfo("UTC"))

    if format == "markdown":
        return generate_markdown_report(events, groups, timezones, now)
    elif format == "json":
        return generate_json_report(events, groups, timezones, now)
    else:
        raise ValueError(f"Unsupported format: {format}")


def generate_markdown_report(
    events: list[Event], groups: list[CorrelationGroup], timezones: list[str], generated_at: datetime
) -> str:
    """Generate a Markdown timeline report."""
    lines = [
        "# Event Timeline Report",
        "",
        f"Generated: {generated_at.isoformat()}",
        "",
        "## Summary",
        "",
        f"- Total events: {len(events)}",
    ]

    if events:
        first = datetime.fromisoformat(events[0].normalized_timestamp)
        last = datetime.fromisoformat(events[-1].normalized_timestamp)
        lines.append(f"- Time span: {first.strftime('%Y-%m-%d %H:%M')} UTC to {last.strftime('%Y-%m-%d %H:%M')} UTC")

    lines.extend(
        [
            f"- Correlation groups: {len(groups)}",
            f"- DST warnings: {sum(1 for e in events if e.ambiguity_warning)}",
            "",
            "## Timeline (Multi-Timezone View)",
            "",
        ]
    )

    # Build table header
    tz_names = ["UTC"] + timezones
    header = "| UTC |"
    separator = "|-----|"
    for tz in timezones:
        short_name = tz.split("/")[-1][:8]
        header += f" {short_name} |"
        separator += "---------|"
    header += " Event | Source |"
    separator += "-------|--------|"

    lines.append(header)
    lines.append(separator)

    # Build table rows
    for event in events:
        dt_utc = datetime.fromisoformat(event.normalized_timestamp)
        row = f"| {dt_utc.strftime('%H:%M')} |"

        for tz_name in timezones:
            try:
                tz = ZoneInfo(tz_name)
                dt_local = dt_utc.astimezone(tz)
                row += f" {dt_local.strftime('%H:%M')} |"
            except Exception:
                row += " N/A |"

        source = event.metadata.get("source_system", "-")
        desc = event.description[:30] + "..." if len(event.description) > 30 else event.description
        row += f" {desc} | {source} |"
        lines.append(row)

    lines.extend(["", "## Correlation Analysis", ""])

    event_map = {e.id: e for e in events}
    for group in groups:
        lines.append(
            f"### {group.group_id}: {group.pattern.replace('_', ' ').title()} ({len(group.event_ids)} events, {group.time_span_seconds:.0f}s span)"
        )
        for eid in group.event_ids:
            if eid in event_map:
                e = event_map[eid]
                dt = datetime.fromisoformat(e.normalized_timestamp)
                lines.append(
                    f"- {dt.strftime('%H:%M:%S')} UTC: {e.description} ({e.metadata.get('source_system', 'unknown')})"
                )
        lines.append("")

    # DST warnings section
    dst_warnings = [e for e in events if e.ambiguity_warning]
    lines.extend(["## DST Considerations", ""])
    if dst_warnings:
        for e in dst_warnings:
            lines.append(f"- {e.id}: {e.ambiguity_warning}")
    else:
        lines.append("No events occurred during DST transition periods.")

    return "\n".join(lines)


def generate_json_report(
    events: list[Event], groups: list[CorrelationGroup], timezones: list[str], generated_at: datetime
) -> str:
    """Generate a JSON report."""
    report = {
        "schema_version": "1.0",
        "reference_timezone": "UTC",
        "generated_at": generated_at.isoformat(),
        "display_timezones": timezones,
        "summary": {
            "total_events": len(events),
            "correlation_groups": len(groups),
            "dst_warnings": sum(1 for e in events if e.ambiguity_warning),
        },
        "events": [asdict(e) for e in events],
        "correlation_groups": [asdict(g) for g in groups],
    }
    return json.dumps(report, indent=2)


def check_dst_issues(events: list[Event], year: int) -> dict:
    """Check for events that may have occurred during DST transitions."""
    # Get unique timezones from events
    unique_timezones = set(e.source_timezone for e in events if e.source_timezone != "UTC")

    issues = []
    transitions_info = {}

    for tz_name in unique_timezones:
        if tz_name.startswith("UTC"):
            continue
        try:
            transitions = get_dst_transitions(year, tz_name)
            if transitions:
                transitions_info[tz_name] = [{"date": t[0].strftime("%Y-%m-%d"), "type": t[1]} for t in transitions]

                # Check if any events fall on transition dates
                transition_dates = set(t[0].date() for t in transitions)
                for event in events:
                    if event.source_timezone == tz_name:
                        event_date = datetime.fromisoformat(event.normalized_timestamp).date()
                        if event_date in transition_dates:
                            issues.append(
                                {
                                    "event_id": event.id,
                                    "timezone": tz_name,
                                    "date": str(event_date),
                                    "warning": "Event occurred on DST transition date",
                                }
                            )
        except Exception as e:
            print(f"Warning: Could not check DST for {tz_name}: {e}", file=sys.stderr)

    return {
        "year": year,
        "timezones_checked": list(unique_timezones),
        "dst_transitions": transitions_info,
        "issues": issues,
    }


def cmd_parse(args):
    """Handle parse command."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    events = parse_events(input_path, args.reference_tz)

    output = {
        "schema_version": "1.0",
        "reference_timezone": args.reference_tz,
        "generated_at": datetime.now(ZoneInfo("UTC")).isoformat(),
        "events": [asdict(e) for e in events],
    }

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        print(f"Parsed {len(events)} events to {output_path}")
    else:
        print(json.dumps(output, indent=2))

    return 0


def cmd_correlate(args):
    """Handle correlate command."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    events = [Event(**e) for e in data.get("events", [])]
    groups = correlate_events(events, args.window_minutes)

    output = {
        "schema_version": "1.0",
        "reference_timezone": data.get("reference_timezone", "UTC"),
        "generated_at": datetime.now(ZoneInfo("UTC")).isoformat(),
        "correlation_window_minutes": args.window_minutes,
        "events": [asdict(e) for e in events],
        "correlation_groups": [asdict(g) for g in groups],
    }

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        print(f"Found {len(groups)} correlation groups, saved to {output_path}")
    else:
        print(json.dumps(output, indent=2))

    return 0


def cmd_report(args):
    """Handle report command."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    events = [Event(**e) for e in data.get("events", [])]
    groups = [CorrelationGroup(**g) for g in data.get("correlation_groups", [])]
    timezones = [tz.strip() for tz in args.timezones.split(",")]

    report = generate_report(events, groups, timezones, args.format)

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {output_path}")
    else:
        print(report)

    return 0


def cmd_dst_check(args):
    """Handle dst-check command."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    events = [Event(**e) for e in data.get("events", [])]
    result = check_dst_issues(events, args.year)

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"DST analysis saved to {output_path}")
    else:
        print(json.dumps(result, indent=2))

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Timezone-Aware Event Tracker - Track and correlate events across timezones"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Parse command
    parse_parser = subparsers.add_parser("parse", help="Parse events and normalize timestamps")
    parse_parser.add_argument("--input", "-i", required=True, help="Input file (CSV or JSON)")
    parse_parser.add_argument("--output", "-o", help="Output JSON file")
    parse_parser.add_argument("--reference-tz", default="UTC", help="Reference timezone (default: UTC)")

    # Correlate command
    correlate_parser = subparsers.add_parser("correlate", help="Correlate events within time windows")
    correlate_parser.add_argument("--input", "-i", required=True, help="Input JSON file (from parse)")
    correlate_parser.add_argument("--output", "-o", help="Output JSON file")
    correlate_parser.add_argument("--window-minutes", "-w", type=int, default=5, help="Correlation window in minutes")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate timeline report")
    report_parser.add_argument("--input", "-i", required=True, help="Input JSON file")
    report_parser.add_argument("--output", "-o", help="Output file")
    report_parser.add_argument(
        "--timezones",
        "-t",
        default="America/Los_Angeles,America/New_York,Asia/Tokyo",
        help="Comma-separated list of timezones to display",
    )
    report_parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format")

    # DST check command
    dst_parser = subparsers.add_parser("dst-check", help="Check for DST-related issues")
    dst_parser.add_argument("--input", "-i", required=True, help="Input JSON file")
    dst_parser.add_argument("--output", "-o", help="Output JSON file")
    dst_parser.add_argument("--year", "-y", type=int, default=datetime.now().year, help="Year to check DST transitions")

    args = parser.parse_args()

    if args.command == "parse":
        return cmd_parse(args)
    elif args.command == "correlate":
        return cmd_correlate(args)
    elif args.command == "report":
        return cmd_report(args)
    elif args.command == "dst-check":
        return cmd_dst_check(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
