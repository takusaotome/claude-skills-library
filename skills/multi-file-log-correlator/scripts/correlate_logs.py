#!/usr/bin/env python3
"""
Multi-File Log Correlator

Correlates events across multiple log files from different sources, systems,
or time periods. Builds unified timelines, identifies causal relationships
between events, and highlights anomalies that span multiple data sources.

Usage:
    python3 correlate_logs.py \
        --logs app.log:app:UTC:"%Y-%m-%d %H:%M:%S" \
        --logs nginx.log:nginx:America/New_York \
        --output-tz UTC \
        --output timeline.json
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Attempt to import optional dependencies
try:
    from dateutil import parser as dateutil_parser
    from dateutil import tz as dateutil_tz

    HAS_DATEUTIL = True
except ImportError:
    HAS_DATEUTIL = False


@dataclass
class LogEvent:
    """Represents a single log event."""

    timestamp: datetime
    source: str
    level: str
    message: str
    raw_line: str
    line_number: int
    correlation_ids: List[str] = field(default_factory=list)
    original_timestamp_str: str = ""


@dataclass
class LogSource:
    """Configuration for a log source."""

    name: str
    file_path: str
    timezone: str = "UTC"
    timestamp_format: Optional[str] = None
    events: List[LogEvent] = field(default_factory=list)
    event_count: int = 0
    time_range_start: Optional[datetime] = None
    time_range_end: Optional[datetime] = None


@dataclass
class Correlation:
    """A group of correlated events."""

    correlation_id: str
    events: List[LogEvent] = field(default_factory=list)
    total_duration_ms: float = 0.0


@dataclass
class Gap:
    """A gap in log coverage."""

    source: str
    gap_start: datetime
    gap_end: datetime
    duration_seconds: float


@dataclass
class Anomaly:
    """An anomaly detected in the logs."""

    anomaly_type: str
    description: str
    events: List[LogEvent] = field(default_factory=list)
    severity: str = "warning"


# Common timestamp patterns for auto-detection
TIMESTAMP_PATTERNS = [
    # ISO 8601 with microseconds and Z
    (
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)",
        "%Y-%m-%dT%H:%M:%S.%fZ",
    ),
    # ISO 8601 with Z
    (r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)", "%Y-%m-%dT%H:%M:%SZ"),
    # ISO 8601 with timezone offset
    (
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})",
        "%Y-%m-%dT%H:%M:%S%z",
    ),
    # ISO 8601 space separator with milliseconds
    (
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})",
        "%Y-%m-%d %H:%M:%S,%f",
    ),
    # ISO 8601 space separator
    (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", "%Y-%m-%d %H:%M:%S"),
    # Apache/Nginx format
    (
        r"(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})",
        "%d/%b/%Y:%H:%M:%S %z",
    ),
    # Syslog format (no year)
    (r"([A-Za-z]{3}\s+\d{1,2} \d{2}:\d{2}:\d{2})", "%b %d %H:%M:%S"),
]

# Common correlation ID patterns
CORRELATION_ID_PATTERNS = [
    r"request_id[=:]\s*[\"']?([a-zA-Z0-9_-]+)",
    r"req_id[=:]\s*[\"']?([a-zA-Z0-9_-]+)",
    r"trace_id[=:]\s*[\"']?([a-zA-Z0-9_-]+)",
    r"correlation_id[=:]\s*[\"']?([a-zA-Z0-9_-]+)",
    r"x-correlation-id[=:]\s*[\"']?([a-zA-Z0-9_-]+)",
    r"transaction_id[=:]\s*[\"']?([a-zA-Z0-9_-]+)",
    r"txn_id[=:]\s*[\"']?([a-zA-Z0-9_-]+)",
    r"\[([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\]",  # UUID
]

# Log level patterns
LOG_LEVEL_PATTERNS = [
    (r"\b(FATAL|CRITICAL)\b", "FATAL"),
    (r"\b(ERROR|ERR)\b", "ERROR"),
    (r"\b(WARN|WARNING)\b", "WARN"),
    (r"\b(INFO)\b", "INFO"),
    (r"\b(DEBUG|TRACE)\b", "DEBUG"),
]


class LogCorrelator:
    """Main class for correlating events across multiple log files."""

    def __init__(
        self,
        output_timezone: str = "UTC",
        time_window_seconds: float = 5.0,
        gap_threshold_seconds: float = 60.0,
    ):
        self.output_timezone = output_timezone
        self.time_window_seconds = time_window_seconds
        self.gap_threshold_seconds = gap_threshold_seconds
        self.sources: List[LogSource] = []
        self.timeline: List[LogEvent] = []
        self.correlations: Dict[str, Correlation] = {}
        self.gaps: List[Gap] = []
        self.anomalies: List[Anomaly] = []

    def parse_source_spec(self, spec: str) -> LogSource:
        """Parse a source specification string.

        Format: file_path:name[:timezone[:format]]
        Example: app.log:app:UTC:%Y-%m-%d %H:%M:%S
        """
        parts = spec.split(":", 3)
        if len(parts) < 2:
            raise ValueError(f"Invalid source spec '{spec}'. Format: file_path:name[:timezone[:format]]")

        file_path = parts[0]
        name = parts[1]
        tz = parts[2] if len(parts) > 2 else "UTC"
        fmt = parts[3] if len(parts) > 3 else None

        return LogSource(
            name=name,
            file_path=file_path,
            timezone=tz,
            timestamp_format=fmt,
        )

    def _detect_timestamp(self, line: str, default_format: Optional[str] = None) -> Tuple[Optional[datetime], str, str]:
        """Detect and parse timestamp from a log line.

        Returns (timestamp, timestamp_string, remaining_line) or (None, "", line).
        """
        if default_format:
            # Try the specified format first
            for pattern, fmt in TIMESTAMP_PATTERNS:
                if fmt == default_format:
                    match = re.search(pattern, line)
                    if match:
                        ts_str = match.group(1)
                        try:
                            ts = datetime.strptime(ts_str, fmt)
                            remaining = line[: match.start()] + line[match.end() :]
                            return ts, ts_str, remaining.strip()
                        except ValueError:
                            pass

        # Try all patterns
        for pattern, fmt in TIMESTAMP_PATTERNS:
            match = re.search(pattern, line)
            if match:
                ts_str = match.group(1)
                try:
                    # Handle %f for milliseconds (pad to 6 digits)
                    if "%f" in fmt and "," in ts_str:
                        ts_str_clean = ts_str.replace(",", ".")
                        parts = ts_str_clean.split(".")
                        if len(parts) == 2:
                            ts_str_clean = parts[0] + "." + parts[1].ljust(6, "0")
                            fmt_clean = fmt.replace(",", ".")
                            ts = datetime.strptime(ts_str_clean, fmt_clean)
                        else:
                            ts = datetime.strptime(ts_str, fmt)
                    else:
                        ts = datetime.strptime(ts_str, fmt)
                    remaining = line[: match.start()] + line[match.end() :]
                    return ts, ts_str, remaining.strip()
                except ValueError:
                    continue

        # Try dateutil as fallback
        if HAS_DATEUTIL:
            try:
                # Look for timestamp-like pattern at start of line
                match = re.match(r"^[\[\]]*([0-9T:\-+. /]+[A-Za-z]*\d*[:\d]*)", line[:50])
                if match:
                    ts_str = match.group(1).strip("[]")
                    ts = dateutil_parser.parse(ts_str)
                    remaining = line[match.end() :].strip()
                    return ts, ts_str, remaining
            except (ValueError, dateutil_parser.ParserError):
                pass

        return None, "", line

    def _detect_log_level(self, line: str) -> str:
        """Detect log level from a line."""
        for pattern, level in LOG_LEVEL_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return level
        return "INFO"

    def _extract_correlation_ids(self, line: str) -> List[str]:
        """Extract correlation IDs from a log line."""
        ids = []
        for pattern in CORRELATION_ID_PATTERNS:
            matches = re.findall(pattern, line, re.IGNORECASE)
            ids.extend(matches)
        return list(set(ids))

    def _normalize_timestamp(self, ts: datetime, source_tz: str, target_tz: str) -> datetime:
        """Normalize a timestamp to the target timezone."""
        if ts.tzinfo is None:
            # Naive datetime - assume source timezone
            if HAS_DATEUTIL:
                source_tzinfo = dateutil_tz.gettz(source_tz)
                ts = ts.replace(tzinfo=source_tzinfo)
            else:
                # Fallback: treat as UTC
                ts = ts.replace(tzinfo=timezone.utc)

        # Convert to target timezone
        if HAS_DATEUTIL:
            target_tzinfo = dateutil_tz.gettz(target_tz)
            ts = ts.astimezone(target_tzinfo)
        else:
            ts = ts.astimezone(timezone.utc)

        return ts

    def parse_log_file(self, source: LogSource) -> None:
        """Parse a log file and extract events."""
        path = Path(source.file_path)
        if not path.exists():
            print(f"Warning: File not found: {source.file_path}", file=sys.stderr)
            return

        events = []
        line_number = 0

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line_number += 1
                line = line.rstrip("\n\r")
                if not line.strip():
                    continue

                ts, ts_str, remaining = self._detect_timestamp(line, source.timestamp_format)
                if ts is None:
                    continue  # Skip lines without parseable timestamp

                # Normalize timestamp
                ts = self._normalize_timestamp(ts, source.timezone, self.output_timezone)

                level = self._detect_log_level(remaining)
                correlation_ids = self._extract_correlation_ids(line)

                event = LogEvent(
                    timestamp=ts,
                    source=source.name,
                    level=level,
                    message=remaining,
                    raw_line=line,
                    line_number=line_number,
                    correlation_ids=correlation_ids,
                    original_timestamp_str=ts_str,
                )
                events.append(event)

        source.events = events
        source.event_count = len(events)
        if events:
            source.time_range_start = min(e.timestamp for e in events)
            source.time_range_end = max(e.timestamp for e in events)

    def add_source(self, source: LogSource) -> None:
        """Add a log source and parse its file."""
        self.parse_log_file(source)
        self.sources.append(source)

    def build_timeline(self) -> List[LogEvent]:
        """Build a unified timeline from all sources."""
        all_events = []
        for source in self.sources:
            all_events.extend(source.events)

        # Sort by timestamp, then by source name for stability
        all_events.sort(key=lambda e: (e.timestamp, e.source))
        self.timeline = all_events
        return self.timeline

    def find_correlations(self, correlation_field: Optional[str] = None) -> None:
        """Find correlated events across sources."""
        id_to_events: Dict[str, List[LogEvent]] = defaultdict(list)

        for event in self.timeline:
            for cid in event.correlation_ids:
                id_to_events[cid].append(event)

        # Also correlate by time proximity if no explicit IDs
        if not id_to_events:
            self._correlate_by_time()
            return

        # Build correlations
        for cid, events in id_to_events.items():
            if len(events) > 1:
                # Check if events span multiple sources
                sources = set(e.source for e in events)
                if len(sources) > 1:
                    events_sorted = sorted(events, key=lambda e: e.timestamp)
                    duration_ms = (events_sorted[-1].timestamp - events_sorted[0].timestamp).total_seconds() * 1000

                    self.correlations[cid] = Correlation(
                        correlation_id=cid,
                        events=events_sorted,
                        total_duration_ms=duration_ms,
                    )

    def _correlate_by_time(self) -> None:
        """Correlate events by temporal proximity when no correlation IDs are present."""
        window = timedelta(seconds=self.time_window_seconds)
        corr_id = 0

        for i, event in enumerate(self.timeline):
            # Find events within the time window
            related = [event]
            for j in range(i + 1, len(self.timeline)):
                other = self.timeline[j]
                if other.timestamp - event.timestamp > window:
                    break
                if other.source != event.source:
                    related.append(other)

            if len(related) > 1:
                sources = set(e.source for e in related)
                if len(sources) > 1:
                    cid = f"time_corr_{corr_id}"
                    corr_id += 1
                    duration_ms = (related[-1].timestamp - related[0].timestamp).total_seconds() * 1000

                    self.correlations[cid] = Correlation(
                        correlation_id=cid,
                        events=related,
                        total_duration_ms=duration_ms,
                    )

    def detect_gaps(self) -> List[Gap]:
        """Detect gaps in log coverage for each source."""
        self.gaps = []
        threshold = timedelta(seconds=self.gap_threshold_seconds)

        for source in self.sources:
            if len(source.events) < 2:
                continue

            sorted_events = sorted(source.events, key=lambda e: e.timestamp)
            for i in range(1, len(sorted_events)):
                prev = sorted_events[i - 1]
                curr = sorted_events[i]
                gap_duration = curr.timestamp - prev.timestamp

                if gap_duration > threshold:
                    self.gaps.append(
                        Gap(
                            source=source.name,
                            gap_start=prev.timestamp,
                            gap_end=curr.timestamp,
                            duration_seconds=gap_duration.total_seconds(),
                        )
                    )

        return self.gaps

    def detect_anomalies(self) -> List[Anomaly]:
        """Detect anomalies in the correlated logs."""
        self.anomalies = []

        # Detect timing anomalies in correlations
        for corr in self.correlations.values():
            if corr.total_duration_ms > 5000:  # > 5 seconds
                self.anomalies.append(
                    Anomaly(
                        anomaly_type="timing_anomaly",
                        description=f"Correlation {corr.correlation_id} took {corr.total_duration_ms:.0f}ms (> 5000ms threshold)",
                        events=corr.events,
                        severity="warning",
                    )
                )

        # Detect error bursts
        error_counts: Dict[str, int] = defaultdict(int)
        for event in self.timeline:
            if event.level in ("ERROR", "FATAL"):
                minute_key = event.timestamp.strftime("%Y-%m-%d %H:%M")
                error_counts[minute_key] += 1

        for minute, count in error_counts.items():
            if count > 10:  # > 10 errors per minute
                self.anomalies.append(
                    Anomaly(
                        anomaly_type="error_burst",
                        description=f"High error rate at {minute}: {count} errors/minute",
                        events=[],
                        severity="error" if count > 50 else "warning",
                    )
                )

        return self.anomalies

    def generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of the correlation analysis."""
        return {
            "sources": [
                {
                    "name": s.name,
                    "file": s.file_path,
                    "timezone": s.timezone,
                    "event_count": s.event_count,
                    "time_range": {
                        "start": s.time_range_start.isoformat() if s.time_range_start else None,
                        "end": s.time_range_end.isoformat() if s.time_range_end else None,
                    },
                }
                for s in self.sources
            ],
            "total_events": len(self.timeline),
            "correlations_found": len(self.correlations),
            "gaps_detected": len(self.gaps),
            "anomalies_detected": len(self.anomalies),
        }

    def to_json(self) -> Dict[str, Any]:
        """Export the correlation results as JSON-serializable dict."""
        return {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "output_timezone": self.output_timezone,
            "sources": [
                {
                    "name": s.name,
                    "file": s.file_path,
                    "original_tz": s.timezone,
                    "events_count": s.event_count,
                    "time_range": {
                        "start": s.time_range_start.isoformat() if s.time_range_start else None,
                        "end": s.time_range_end.isoformat() if s.time_range_end else None,
                    },
                }
                for s in self.sources
            ],
            "timeline": [
                {
                    "timestamp": e.timestamp.isoformat(),
                    "source": e.source,
                    "level": e.level,
                    "message": e.message[:500],  # Truncate long messages
                    "correlation_ids": e.correlation_ids,
                }
                for e in self.timeline[:1000]  # Limit for JSON output
            ],
            "correlations": [
                {
                    "correlation_id": c.correlation_id,
                    "events": [
                        {
                            "source": e.source,
                            "timestamp": e.timestamp.isoformat(),
                            "message": e.message[:200],
                        }
                        for e in c.events
                    ],
                    "total_duration_ms": c.total_duration_ms,
                }
                for c in self.correlations.values()
            ],
            "gaps": [
                {
                    "source": g.source,
                    "gap_start": g.gap_start.isoformat(),
                    "gap_end": g.gap_end.isoformat(),
                    "duration_seconds": g.duration_seconds,
                }
                for g in self.gaps
            ],
            "anomalies": [
                {
                    "type": a.anomaly_type,
                    "description": a.description,
                    "severity": a.severity,
                }
                for a in self.anomalies
            ],
        }

    def to_markdown(self) -> str:
        """Generate a Markdown report."""
        lines = []
        lines.append("# Multi-File Log Correlation Report")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
        lines.append(f"**Output Timezone:** {self.output_timezone}")
        lines.append("")

        # Source Summary
        lines.append("## Source Summary")
        lines.append("")
        lines.append("| Source | File | Timezone | Events | Time Range |")
        lines.append("|--------|------|----------|--------|------------|")
        for s in self.sources:
            time_range = ""
            if s.time_range_start and s.time_range_end:
                time_range = f"{s.time_range_start.strftime('%H:%M:%S')} - {s.time_range_end.strftime('%H:%M:%S')}"
            lines.append(f"| {s.name} | {s.file_path} | {s.timezone} | {s.event_count} | {time_range} |")
        lines.append("")

        # Correlation Statistics
        lines.append("## Correlation Statistics")
        lines.append("")
        lines.append(f"- **Total Events:** {len(self.timeline)}")
        lines.append(f"- **Correlations Found:** {len(self.correlations)}")
        lines.append(f"- **Gaps Detected:** {len(self.gaps)}")
        lines.append(f"- **Anomalies Detected:** {len(self.anomalies)}")
        lines.append("")

        # Top Correlations
        if self.correlations:
            lines.append("## Top Correlations")
            lines.append("")
            sorted_corrs = sorted(
                self.correlations.values(),
                key=lambda c: c.total_duration_ms,
                reverse=True,
            )[:10]
            for corr in sorted_corrs:
                lines.append(f"### {corr.correlation_id} ({corr.total_duration_ms:.0f}ms)")
                lines.append("")
                for event in corr.events:
                    lines.append(
                        f"- **{event.source}** [{event.timestamp.strftime('%H:%M:%S.%f')[:-3]}] {event.message[:100]}"
                    )
                lines.append("")

        # Gaps
        if self.gaps:
            lines.append("## Detected Gaps")
            lines.append("")
            lines.append("| Source | Gap Start | Gap End | Duration |")
            lines.append("|--------|-----------|---------|----------|")
            for gap in self.gaps[:20]:
                lines.append(
                    f"| {gap.source} | {gap.gap_start.strftime('%H:%M:%S')} | {gap.gap_end.strftime('%H:%M:%S')} | {gap.duration_seconds:.0f}s |"
                )
            lines.append("")

        # Anomalies
        if self.anomalies:
            lines.append("## Detected Anomalies")
            lines.append("")
            for anomaly in self.anomalies:
                severity_icon = "⚠️" if anomaly.severity == "warning" else "🚨"
                lines.append(f"- {severity_icon} **{anomaly.anomaly_type}**: {anomaly.description}")
            lines.append("")

        # Timeline Sample
        lines.append("## Timeline Sample (First 50 Events)")
        lines.append("")
        lines.append("```")
        for event in self.timeline[:50]:
            ts_str = event.timestamp.strftime("%H:%M:%S.%f")[:-3]
            lines.append(f"[{ts_str}] [{event.source:10}] [{event.level:5}] {event.message[:80]}")
        lines.append("```")
        lines.append("")

        return "\n".join(lines)


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Correlate events across multiple log files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic correlation with two log files
  python3 correlate_logs.py --logs app.log:app --logs nginx.log:nginx

  # With timezone and format specification
  python3 correlate_logs.py \\
    --logs 'app.log:app:UTC:%Y-%m-%d %H:%M:%S' \\
    --logs 'nginx.log:nginx:America/New_York:%d/%b/%Y:%H:%M:%S %z'

  # Generate JSON output
  python3 correlate_logs.py --logs app.log:app --logs db.log:db --output result.json

  # Generate Markdown report
  python3 correlate_logs.py --logs app.log:app --full-report --output report.md
        """,
    )
    parser.add_argument(
        "--logs",
        action="append",
        required=True,
        help="Log source spec: file_path:name[:timezone[:format]]",
    )
    parser.add_argument(
        "--output-tz",
        default="UTC",
        help="Output timezone (default: UTC)",
    )
    parser.add_argument(
        "--time-window",
        default="5s",
        help="Time window for proximity correlation (default: 5s)",
    )
    parser.add_argument(
        "--gap-threshold",
        default="60s",
        help="Gap threshold for detection (default: 60s)",
    )
    parser.add_argument(
        "--correlation-field",
        help="Field name to use for correlation (e.g., request_id)",
    )
    parser.add_argument(
        "--detect-gaps",
        action="store_true",
        help="Detect gaps in log coverage",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary only",
    )
    parser.add_argument(
        "--full-report",
        action="store_true",
        help="Generate full Markdown report",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    # Parse time window and gap threshold
    def parse_duration(s: str) -> float:
        """Parse duration string like '5s', '1m', '500ms' to seconds."""
        s = s.strip().lower()
        if s.endswith("ms"):
            return float(s[:-2]) / 1000
        elif s.endswith("s"):
            return float(s[:-1])
        elif s.endswith("m"):
            return float(s[:-1]) * 60
        elif s.endswith("h"):
            return float(s[:-1]) * 3600
        else:
            return float(s)

    time_window = parse_duration(args.time_window)
    gap_threshold = parse_duration(args.gap_threshold)

    # Create correlator
    correlator = LogCorrelator(
        output_timezone=args.output_tz,
        time_window_seconds=time_window,
        gap_threshold_seconds=gap_threshold,
    )

    # Parse and add sources
    for log_spec in args.logs:
        source = correlator.parse_source_spec(log_spec)
        correlator.add_source(source)

    # Build timeline
    correlator.build_timeline()

    # Find correlations
    correlator.find_correlations(args.correlation_field)

    # Detect gaps if requested
    if args.detect_gaps:
        correlator.detect_gaps()

    # Detect anomalies
    correlator.detect_anomalies()

    # Generate output
    if args.summary:
        summary = correlator.generate_summary()
        output = json.dumps(summary, indent=2)
    elif args.full_report:
        output = correlator.to_markdown()
    else:
        result = correlator.to_json()
        output = json.dumps(result, indent=2)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding="utf-8")
        print(f"Output written to: {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
