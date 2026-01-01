#!/usr/bin/env python3
"""
Log Analyzer - A tool for analyzing system logs and finding root causes.

Usage:
    python log_analyzer.py analyze <logfile> [--config <config.yaml>]
    python log_analyzer.py search <logfile> --keywords <keywords> [--context <lines>]
    python log_analyzer.py search <logfile> --pattern <regex> [--context <lines>]
    python log_analyzer.py timeline <logfile> [--from <datetime>] [--to <datetime>]
    python log_analyzer.py report <logfile> [--output <file>] [--format <md|json>]
    python log_analyzer.py correlate <logfile1> <logfile2> [<logfile3>...]
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Tuple

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class LogEntry:
    """Represents a single log entry."""
    line_number: int
    raw: str
    timestamp: Optional[datetime] = None
    level: Optional[str] = None
    message: str = ""
    source: str = ""
    extra: Dict = field(default_factory=dict)


@dataclass
class TimelineEvent:
    """Represents an event in the timeline."""
    timestamp: datetime
    event: str
    source: str
    level: str
    line_number: int


@dataclass
class AnalysisResult:
    """Represents the result of log analysis."""
    total_lines: int
    error_count: int
    warning_count: int
    entries: List[LogEntry]
    frequency: Dict[str, int]
    time_distribution: Dict[str, int]


# =============================================================================
# Log Parsers
# =============================================================================

class LogParser:
    """Base class for log parsers."""

    # Common timestamp patterns
    TIMESTAMP_PATTERNS = [
        # ISO 8601: 2025-01-15T10:30:45.123Z
        (r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)',
         '%Y-%m-%dT%H:%M:%S'),
        # Common: 2025-01-15 10:30:45
        (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', '%Y-%m-%d %H:%M:%S'),
        # Syslog: Jan 15 10:30:45
        (r'([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', '%b %d %H:%M:%S'),
        # Unix timestamp: 1705312245
        (r'\b(\d{10})\b', 'unix'),
        # With milliseconds: 2025-01-15 10:30:45,123
        (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})', '%Y-%m-%d %H:%M:%S,%f'),
    ]

    # Common log level patterns
    LEVEL_PATTERNS = [
        r'\b(FATAL|CRITICAL)\b',
        r'\b(ERROR|ERR)\b',
        r'\b(WARN(?:ING)?)\b',
        r'\b(INFO)\b',
        r'\b(DEBUG)\b',
        r'\b(TRACE)\b',
    ]

    LEVEL_PRIORITY = {
        'FATAL': 0, 'CRITICAL': 0,
        'ERROR': 1, 'ERR': 1,
        'WARNING': 2, 'WARN': 2,
        'INFO': 3,
        'DEBUG': 4,
        'TRACE': 5,
    }

    def parse_line(self, line: str, line_number: int) -> LogEntry:
        """Parse a single log line."""
        entry = LogEntry(line_number=line_number, raw=line.strip(), message=line.strip())

        # Extract timestamp
        entry.timestamp = self._extract_timestamp(line)

        # Extract log level
        entry.level = self._extract_level(line)

        return entry

    def _extract_timestamp(self, line: str) -> Optional[datetime]:
        """Extract timestamp from log line."""
        for pattern, fmt in self.TIMESTAMP_PATTERNS:
            match = re.search(pattern, line)
            if match:
                ts_str = match.group(1)
                try:
                    if fmt == 'unix':
                        return datetime.fromtimestamp(int(ts_str))
                    # Handle ISO format with timezone
                    if 'T' in ts_str and (ts_str.endswith('Z') or '+' in ts_str or '-' in ts_str[-6:]):
                        ts_str = ts_str.replace('Z', '+00:00')
                        if '.' in ts_str:
                            return datetime.fromisoformat(ts_str.split('.')[0])
                        return datetime.fromisoformat(ts_str)
                    return datetime.strptime(ts_str.split('.')[0].split(',')[0], fmt.split('.')[0].split(',')[0])
                except (ValueError, OSError):
                    continue
        return None

    def _extract_level(self, line: str) -> Optional[str]:
        """Extract log level from log line."""
        for pattern in self.LEVEL_PATTERNS:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        return None


class JSONLogParser(LogParser):
    """Parser for JSON-formatted logs."""

    def parse_line(self, line: str, line_number: int) -> LogEntry:
        """Parse a JSON log line."""
        entry = LogEntry(line_number=line_number, raw=line.strip())

        try:
            data = json.loads(line)
            entry.extra = data

            # Extract common fields
            for ts_field in ['timestamp', 'time', '@timestamp', 'ts', 'datetime']:
                if ts_field in data:
                    ts_val = data[ts_field]
                    if isinstance(ts_val, (int, float)):
                        entry.timestamp = datetime.fromtimestamp(ts_val)
                    elif isinstance(ts_val, str):
                        entry.timestamp = self._extract_timestamp(ts_val)
                    break

            for level_field in ['level', 'severity', 'log_level', 'loglevel']:
                if level_field in data:
                    entry.level = str(data[level_field]).upper()
                    break

            for msg_field in ['message', 'msg', 'text', 'log']:
                if msg_field in data:
                    entry.message = str(data[msg_field])
                    break

        except json.JSONDecodeError:
            entry.message = line.strip()
            entry.timestamp = self._extract_timestamp(line)
            entry.level = self._extract_level(line)

        return entry


# =============================================================================
# Log Analyzer
# =============================================================================

class LogAnalyzer:
    """Main log analyzer class."""

    DEFAULT_ERROR_KEYWORDS = [
        'error', 'exception', 'failed', 'failure', 'fatal', 'critical',
        'crash', 'panic', 'abort', 'timeout', 'refused', 'denied',
        'traceback', 'stacktrace', 'segfault', 'oom', 'killed'
    ]

    DEFAULT_WARNING_KEYWORDS = [
        'warn', 'warning', 'deprecated', 'slow', 'retry', 'skip',
        'invalid', 'missing', 'not found', 'unavailable'
    ]

    def __init__(self, config: Optional[Dict] = None):
        """Initialize the analyzer with optional configuration."""
        self.config = config or {}
        self.entries: List[LogEntry] = []
        self.parser = LogParser()
        self.source_name = ""

        # Load custom keywords from config
        self.error_keywords = self.config.get('error_keywords', self.DEFAULT_ERROR_KEYWORDS)
        self.warning_keywords = self.config.get('warning_keywords', self.DEFAULT_WARNING_KEYWORDS)

    def load_file(self, file_path: str) -> None:
        """Load and parse a log file."""
        path = Path(file_path)
        self.source_name = path.name

        # Auto-detect JSON format
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            first_line = f.readline().strip()
            if first_line.startswith('{'):
                self.parser = JSONLogParser()
            f.seek(0)

            for line_number, line in enumerate(f, 1):
                if line.strip():
                    entry = self.parser.parse_line(line, line_number)
                    entry.source = self.source_name
                    self.entries.append(entry)

    def load_stdin(self) -> None:
        """Load log from stdin."""
        self.source_name = "stdin"
        lines = sys.stdin.readlines()

        if lines and lines[0].strip().startswith('{'):
            self.parser = JSONLogParser()

        for line_number, line in enumerate(lines, 1):
            if line.strip():
                entry = self.parser.parse_line(line, line_number)
                entry.source = self.source_name
                self.entries.append(entry)

    def detect_errors(self, keywords: Optional[List[str]] = None) -> List[LogEntry]:
        """Detect error entries based on keywords and log level."""
        keywords = keywords or self.error_keywords
        pattern = re.compile('|'.join(keywords), re.IGNORECASE)

        errors = []
        for entry in self.entries:
            # Check log level
            if entry.level in ('FATAL', 'CRITICAL', 'ERROR', 'ERR'):
                errors.append(entry)
            # Check keywords in message
            elif pattern.search(entry.message) or pattern.search(entry.raw):
                errors.append(entry)

        return errors

    def detect_warnings(self, keywords: Optional[List[str]] = None) -> List[LogEntry]:
        """Detect warning entries."""
        keywords = keywords or self.warning_keywords
        pattern = re.compile('|'.join(keywords), re.IGNORECASE)

        warnings = []
        for entry in self.entries:
            if entry.level in ('WARNING', 'WARN'):
                warnings.append(entry)
            elif pattern.search(entry.message) or pattern.search(entry.raw):
                if entry not in self.detect_errors():
                    warnings.append(entry)

        return warnings

    def search_pattern(self, pattern: str, case_insensitive: bool = True) -> List[LogEntry]:
        """Search for entries matching a regex pattern."""
        flags = re.IGNORECASE if case_insensitive else 0
        regex = re.compile(pattern, flags)

        return [entry for entry in self.entries if regex.search(entry.raw)]

    def search_keywords(self, keywords: List[str], case_insensitive: bool = True) -> List[LogEntry]:
        """Search for entries containing any of the keywords."""
        pattern = '|'.join(re.escape(kw) for kw in keywords)
        return self.search_pattern(pattern, case_insensitive)

    def get_context(self, entry: LogEntry, before: int = 5, after: int = 5) -> List[LogEntry]:
        """Get surrounding context for an entry."""
        idx = None
        for i, e in enumerate(self.entries):
            if e.line_number == entry.line_number and e.source == entry.source:
                idx = i
                break

        if idx is None:
            return [entry]

        start = max(0, idx - before)
        end = min(len(self.entries), idx + after + 1)
        return self.entries[start:end]

    def analyze_frequency(self) -> Dict[str, int]:
        """Analyze error message frequency."""
        # Normalize messages for grouping
        counter = Counter()

        for entry in self.detect_errors():
            # Remove timestamps, numbers for grouping
            normalized = re.sub(r'\d+', 'N', entry.message)
            normalized = re.sub(r'0x[a-fA-F0-9]+', 'ADDR', normalized)
            normalized = normalized[:200]  # Truncate for grouping
            counter[normalized] += 1

        return dict(counter.most_common(20))

    def analyze_time_distribution(self) -> Dict[str, int]:
        """Analyze error distribution over time."""
        distribution = defaultdict(int)

        for entry in self.detect_errors():
            if entry.timestamp:
                hour_key = entry.timestamp.strftime('%Y-%m-%d %H:00')
                distribution[hour_key] += 1

        return dict(sorted(distribution.items()))

    def generate_timeline(self,
                         from_time: Optional[datetime] = None,
                         to_time: Optional[datetime] = None) -> List[TimelineEvent]:
        """Generate a timeline of significant events."""
        events = []

        for entry in self.entries:
            if entry.timestamp is None:
                continue

            if from_time and entry.timestamp < from_time:
                continue
            if to_time and entry.timestamp > to_time:
                continue

            # Only include errors and warnings in timeline
            if entry.level in ('FATAL', 'CRITICAL', 'ERROR', 'ERR', 'WARNING', 'WARN'):
                events.append(TimelineEvent(
                    timestamp=entry.timestamp,
                    event=entry.message[:200],
                    source=entry.source,
                    level=entry.level or 'UNKNOWN',
                    line_number=entry.line_number
                ))

        return sorted(events, key=lambda e: e.timestamp)

    def analyze(self) -> AnalysisResult:
        """Perform comprehensive analysis."""
        errors = self.detect_errors()
        warnings = self.detect_warnings()

        return AnalysisResult(
            total_lines=len(self.entries),
            error_count=len(errors),
            warning_count=len(warnings),
            entries=errors,
            frequency=self.analyze_frequency(),
            time_distribution=self.analyze_time_distribution()
        )

    def generate_report(self, format: str = "markdown") -> str:
        """Generate analysis report."""
        result = self.analyze()

        if format == "json":
            return self._generate_json_report(result)
        return self._generate_markdown_report(result)

    def _generate_markdown_report(self, result: AnalysisResult) -> str:
        """Generate Markdown format report."""
        lines = [
            "# Log Analysis Report",
            "",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Source**: {self.source_name}",
            "",
            "## Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Lines | {result.total_lines:,} |",
            f"| Errors | {result.error_count:,} |",
            f"| Warnings | {result.warning_count:,} |",
            f"| Error Rate | {result.error_count / max(result.total_lines, 1) * 100:.2f}% |",
            "",
        ]

        if result.frequency:
            lines.extend([
                "## Top Error Patterns",
                "",
                "| Count | Pattern |",
                "|-------|---------|",
            ])
            for pattern, count in list(result.frequency.items())[:10]:
                # Escape pipe characters for markdown
                safe_pattern = pattern.replace('|', '\\|')[:100]
                lines.append(f"| {count} | {safe_pattern} |")
            lines.append("")

        if result.time_distribution:
            lines.extend([
                "## Error Distribution by Hour",
                "",
                "| Time | Count |",
                "|------|-------|",
            ])
            for hour, count in list(result.time_distribution.items())[:24]:
                lines.append(f"| {hour} | {count} |")
            lines.append("")

        if result.entries:
            lines.extend([
                "## Sample Errors",
                "",
            ])
            for entry in result.entries[:10]:
                ts = entry.timestamp.strftime('%Y-%m-%d %H:%M:%S') if entry.timestamp else 'N/A'
                lines.extend([
                    f"### Line {entry.line_number} ({ts})",
                    "",
                    "```",
                    entry.raw[:500],
                    "```",
                    "",
                ])

        return '\n'.join(lines)

    def _generate_json_report(self, result: AnalysisResult) -> str:
        """Generate JSON format report."""
        data = {
            "generated": datetime.now().isoformat(),
            "source": self.source_name,
            "summary": {
                "total_lines": result.total_lines,
                "error_count": result.error_count,
                "warning_count": result.warning_count,
                "error_rate": result.error_count / max(result.total_lines, 1)
            },
            "top_patterns": result.frequency,
            "time_distribution": result.time_distribution,
            "sample_errors": [
                {
                    "line_number": e.line_number,
                    "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                    "level": e.level,
                    "message": e.message[:500]
                }
                for e in result.entries[:20]
            ]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)


# =============================================================================
# Multi-Log Correlator
# =============================================================================

class LogCorrelator:
    """Correlate events across multiple log files."""

    def __init__(self):
        self.analyzers: List[LogAnalyzer] = []

    def add_log(self, file_path: str, config: Optional[Dict] = None) -> None:
        """Add a log file for correlation."""
        analyzer = LogAnalyzer(config)
        analyzer.load_file(file_path)
        self.analyzers.append(analyzer)

    def find_correlations(self, time_window_seconds: int = 60) -> List[Dict]:
        """Find correlated events across logs."""
        # Collect all error events with timestamps
        all_events = []
        for analyzer in self.analyzers:
            for entry in analyzer.detect_errors():
                if entry.timestamp:
                    all_events.append({
                        'timestamp': entry.timestamp,
                        'source': entry.source,
                        'message': entry.message,
                        'line_number': entry.line_number
                    })

        # Sort by timestamp
        all_events.sort(key=lambda e: e['timestamp'])

        # Find clusters within time window
        correlations = []
        i = 0
        while i < len(all_events):
            cluster = [all_events[i]]
            j = i + 1

            while j < len(all_events):
                delta = (all_events[j]['timestamp'] - cluster[0]['timestamp']).total_seconds()
                if delta <= time_window_seconds:
                    cluster.append(all_events[j])
                    j += 1
                else:
                    break

            # Only report clusters with events from multiple sources
            sources = set(e['source'] for e in cluster)
            if len(sources) > 1:
                correlations.append({
                    'start_time': cluster[0]['timestamp'].isoformat(),
                    'end_time': cluster[-1]['timestamp'].isoformat(),
                    'sources': list(sources),
                    'event_count': len(cluster),
                    'events': cluster
                })

            i = j if j > i + 1 else i + 1

        return correlations

    def generate_unified_timeline(self) -> List[TimelineEvent]:
        """Generate a unified timeline from all logs."""
        all_events = []

        for analyzer in self.analyzers:
            all_events.extend(analyzer.generate_timeline())

        return sorted(all_events, key=lambda e: e.timestamp)


# =============================================================================
# CLI Interface
# =============================================================================

def load_config(config_path: str) -> Dict:
    """Load configuration from YAML file."""
    if not YAML_AVAILABLE:
        print("Warning: PyYAML not installed. Using default configuration.", file=sys.stderr)
        return {}

    path = Path(config_path)
    if not path.exists():
        return {}

    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}


def cmd_analyze(args):
    """Handle analyze command."""
    config = load_config(args.config) if args.config else {}
    analyzer = LogAnalyzer(config)

    if args.logfile == '-':
        analyzer.load_stdin()
    else:
        analyzer.load_file(args.logfile)

    if args.summary:
        result = analyzer.analyze()
        print(f"Total lines: {result.total_lines:,}")
        print(f"Errors: {result.error_count:,}")
        print(f"Warnings: {result.warning_count:,}")
        print(f"Error rate: {result.error_count / max(result.total_lines, 1) * 100:.2f}%")
    else:
        errors = analyzer.detect_errors()
        for entry in errors:
            ts = entry.timestamp.strftime('%Y-%m-%d %H:%M:%S') if entry.timestamp else 'N/A'
            print(f"[{ts}] Line {entry.line_number}: {entry.message[:200]}")


def cmd_search(args):
    """Handle search command."""
    config = load_config(args.config) if args.config else {}
    analyzer = LogAnalyzer(config)

    if args.logfile == '-':
        analyzer.load_stdin()
    else:
        analyzer.load_file(args.logfile)

    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',')]
        results = analyzer.search_keywords(keywords)
    elif args.pattern:
        results = analyzer.search_pattern(args.pattern)
    else:
        print("Error: --keywords or --pattern required", file=sys.stderr)
        sys.exit(1)

    for entry in results:
        if args.context > 0:
            context = analyzer.get_context(entry, before=args.context, after=args.context)
            print(f"--- Match at line {entry.line_number} ---")
            for ctx_entry in context:
                marker = ">>>" if ctx_entry.line_number == entry.line_number else "   "
                print(f"{marker} {ctx_entry.line_number}: {ctx_entry.raw}")
            print()
        else:
            ts = entry.timestamp.strftime('%Y-%m-%d %H:%M:%S') if entry.timestamp else 'N/A'
            print(f"[{ts}] Line {entry.line_number}: {entry.raw[:200]}")


def cmd_timeline(args):
    """Handle timeline command."""
    config = load_config(args.config) if args.config else {}
    analyzer = LogAnalyzer(config)
    analyzer.load_file(args.logfile)

    from_time = None
    to_time = None

    if args.from_time:
        from_time = datetime.strptime(args.from_time, '%Y-%m-%d %H:%M')
    if args.to_time:
        to_time = datetime.strptime(args.to_time, '%Y-%m-%d %H:%M')

    events = analyzer.generate_timeline(from_time, to_time)

    print("| Timestamp | Level | Source | Event |")
    print("|-----------|-------|--------|-------|")
    for event in events:
        ts = event.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        msg = event.event[:80].replace('|', '\\|')
        print(f"| {ts} | {event.level} | {event.source} | {msg} |")


def cmd_report(args):
    """Handle report command."""
    config = load_config(args.config) if args.config else {}
    analyzer = LogAnalyzer(config)

    if args.logfile == '-':
        analyzer.load_stdin()
    else:
        analyzer.load_file(args.logfile)

    report = analyzer.generate_report(format=args.format)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)


def cmd_correlate(args):
    """Handle correlate command."""
    correlator = LogCorrelator()

    for logfile in args.logfiles:
        correlator.add_log(logfile)

    correlations = correlator.find_correlations(time_window_seconds=args.window)

    if args.format == 'json':
        print(json.dumps(correlations, indent=2, ensure_ascii=False))
    else:
        print("# Correlation Analysis\n")
        if not correlations:
            print("No correlations found within the time window.")
        else:
            for i, corr in enumerate(correlations, 1):
                print(f"## Correlation {i}")
                print(f"- Time: {corr['start_time']} to {corr['end_time']}")
                print(f"- Sources: {', '.join(corr['sources'])}")
                print(f"- Events: {corr['event_count']}")
                print()
                for event in corr['events'][:5]:
                    print(f"  - [{event['source']}] {event['message'][:100]}")
                if len(corr['events']) > 5:
                    print(f"  ... and {len(corr['events']) - 5} more")
                print()


def main():
    parser = argparse.ArgumentParser(
        description='Log Analyzer - Analyze system logs and find root causes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze app.log --summary
  %(prog)s search app.log --keywords "timeout,error"
  %(prog)s search app.log --pattern "Connection.*refused" --context 5
  %(prog)s timeline app.log --from "2025-01-01 10:00" --to "2025-01-01 12:00"
  %(prog)s report app.log --output report.md
  %(prog)s correlate app.log nginx.log db.log --window 60
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # analyze command
    p_analyze = subparsers.add_parser('analyze', help='Analyze log file for errors')
    p_analyze.add_argument('logfile', help='Log file to analyze (use - for stdin)')
    p_analyze.add_argument('--config', '-c', help='Configuration file (YAML)')
    p_analyze.add_argument('--summary', '-s', action='store_true', help='Show summary only')

    # search command
    p_search = subparsers.add_parser('search', help='Search for patterns in log')
    p_search.add_argument('logfile', help='Log file to search')
    p_search.add_argument('--keywords', '-k', help='Comma-separated keywords to search')
    p_search.add_argument('--pattern', '-p', help='Regex pattern to search')
    p_search.add_argument('--context', '-C', type=int, default=0, help='Lines of context')
    p_search.add_argument('--config', '-c', help='Configuration file (YAML)')

    # timeline command
    p_timeline = subparsers.add_parser('timeline', help='Generate event timeline')
    p_timeline.add_argument('logfile', help='Log file to analyze')
    p_timeline.add_argument('--from', dest='from_time', help='Start time (YYYY-MM-DD HH:MM)')
    p_timeline.add_argument('--to', dest='to_time', help='End time (YYYY-MM-DD HH:MM)')
    p_timeline.add_argument('--config', '-c', help='Configuration file (YAML)')

    # report command
    p_report = subparsers.add_parser('report', help='Generate analysis report')
    p_report.add_argument('logfile', help='Log file to analyze (use - for stdin)')
    p_report.add_argument('--output', '-o', help='Output file')
    p_report.add_argument('--format', '-f', choices=['md', 'json'], default='md', help='Output format')
    p_report.add_argument('--config', '-c', help='Configuration file (YAML)')

    # correlate command
    p_correlate = subparsers.add_parser('correlate', help='Correlate events across multiple logs')
    p_correlate.add_argument('logfiles', nargs='+', help='Log files to correlate')
    p_correlate.add_argument('--window', '-w', type=int, default=60, help='Time window in seconds')
    p_correlate.add_argument('--format', '-f', choices=['md', 'json'], default='md', help='Output format')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        'analyze': cmd_analyze,
        'search': cmd_search,
        'timeline': cmd_timeline,
        'report': cmd_report,
        'correlate': cmd_correlate,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
