"""Tests for log_analyzer.py"""

import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from log_analyzer import (
    JSONLogParser,
    LogAnalyzer,
    LogCorrelator,
    LogEntry,
    LogParser,
    TimelineEvent,
)


class TestLogParser:
    """Tests for LogParser class."""

    def test_parse_line_basic(self):
        parser = LogParser()
        entry = parser.parse_line("2025-01-15 10:30:45 ERROR Something went wrong", 1)
        assert entry.line_number == 1
        assert entry.level == "ERROR"
        assert entry.timestamp is not None
        assert entry.timestamp.year == 2025

    def test_extract_timestamp_iso_format(self):
        parser = LogParser()
        entry = parser.parse_line("2025-01-15T10:30:45Z INFO message", 1)
        assert entry.timestamp is not None
        assert entry.timestamp.hour == 10

    def test_extract_timestamp_common_format(self):
        parser = LogParser()
        entry = parser.parse_line("2025-01-15 14:30:00 DEBUG test", 1)
        assert entry.timestamp is not None
        assert entry.timestamp.minute == 30

    def test_extract_level_fatal(self):
        parser = LogParser()
        entry = parser.parse_line("FATAL: System crash", 1)
        assert entry.level == "FATAL"

    def test_extract_level_warning(self):
        parser = LogParser()
        entry = parser.parse_line("WARN: Low memory", 1)
        assert entry.level == "WARN"

    def test_extract_level_case_insensitive(self):
        parser = LogParser()
        entry = parser.parse_line("error: something failed", 1)
        assert entry.level == "ERROR"

    def test_no_level_found(self):
        parser = LogParser()
        entry = parser.parse_line("Just a plain message", 1)
        assert entry.level is None


class TestJSONLogParser:
    """Tests for JSONLogParser class."""

    def test_parse_json_line(self):
        parser = JSONLogParser()
        log_line = json.dumps(
            {"timestamp": "2025-01-15T10:30:45Z", "level": "error", "message": "Database connection failed"}
        )
        entry = parser.parse_line(log_line, 1)
        assert entry.level == "ERROR"
        assert "Database connection failed" in entry.message

    def test_parse_json_with_ts_field(self):
        parser = JSONLogParser()
        log_line = json.dumps({"ts": "2025-01-15 10:30:45", "severity": "WARNING", "msg": "High latency detected"})
        entry = parser.parse_line(log_line, 1)
        assert entry.level == "WARNING"
        assert "High latency" in entry.message

    def test_parse_invalid_json_falls_back(self):
        parser = JSONLogParser()
        entry = parser.parse_line("Not JSON: 2025-01-15 ERROR failure", 1)
        assert entry.level == "ERROR"


class TestLogAnalyzer:
    """Tests for LogAnalyzer class."""

    @pytest.fixture
    def sample_log_file(self):
        """Create a temporary log file for testing."""
        content = """2025-01-15 10:00:00 INFO Application started
2025-01-15 10:00:05 DEBUG Loading configuration
2025-01-15 10:00:10 WARN Deprecated API used
2025-01-15 10:00:15 ERROR Connection timeout to database
2025-01-15 10:00:20 ERROR Failed to process request
2025-01-15 10:00:25 FATAL OutOfMemoryError
2025-01-15 10:00:30 INFO Recovery completed
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            f.write(content)
            return f.name

    def test_load_file(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        assert len(analyzer.entries) == 7
        Path(sample_log_file).unlink()

    def test_detect_errors(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        errors = analyzer.detect_errors()
        assert len(errors) >= 3  # ERROR, ERROR, FATAL
        Path(sample_log_file).unlink()

    def test_detect_warnings(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        warnings = analyzer.detect_warnings()
        assert len(warnings) >= 1
        Path(sample_log_file).unlink()

    def test_search_keywords(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        results = analyzer.search_keywords(["timeout", "memory"])
        assert len(results) >= 2
        Path(sample_log_file).unlink()

    def test_search_pattern(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        results = analyzer.search_pattern(r"Connection.*timeout")
        assert len(results) >= 1
        Path(sample_log_file).unlink()

    def test_get_context(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        errors = analyzer.detect_errors()
        if errors:
            context = analyzer.get_context(errors[0], before=2, after=2)
            assert len(context) >= 1
        Path(sample_log_file).unlink()

    def test_analyze_frequency(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        freq = analyzer.analyze_frequency()
        assert isinstance(freq, dict)
        Path(sample_log_file).unlink()

    def test_analyze_time_distribution(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        dist = analyzer.analyze_time_distribution()
        assert isinstance(dist, dict)
        Path(sample_log_file).unlink()

    def test_generate_timeline(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        timeline = analyzer.generate_timeline()
        assert isinstance(timeline, list)
        for event in timeline:
            assert isinstance(event, TimelineEvent)
        Path(sample_log_file).unlink()

    def test_analyze_returns_result(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        result = analyzer.analyze()
        assert result.total_lines == 7
        assert result.error_count >= 3
        Path(sample_log_file).unlink()

    def test_generate_report_markdown(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        report = analyzer.generate_report(format="markdown")
        assert "# Log Analysis Report" in report
        assert "## Summary" in report
        Path(sample_log_file).unlink()

    def test_generate_report_json(self, sample_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(sample_log_file)
        report = analyzer.generate_report(format="json")
        data = json.loads(report)
        assert "summary" in data
        assert "total_lines" in data["summary"]
        Path(sample_log_file).unlink()


class TestLogCorrelator:
    """Tests for LogCorrelator class."""

    @pytest.fixture
    def multi_log_files(self):
        """Create multiple log files for correlation testing."""
        app_log = """2025-01-15 10:00:00 ERROR Database connection failed
2025-01-15 10:00:05 ERROR Retry failed
"""
        db_log = """2025-01-15 10:00:01 ERROR Max connections reached
2025-01-15 10:00:02 FATAL Connection pool exhausted
"""
        files = []
        for name, content in [("app.log", app_log), ("db.log", db_log)]:
            with tempfile.NamedTemporaryFile(mode="w", suffix=f"_{name}", delete=False) as f:
                f.write(content)
                files.append(f.name)
        return files

    def test_add_log(self, multi_log_files):
        correlator = LogCorrelator()
        for f in multi_log_files:
            correlator.add_log(f)
        assert len(correlator.analyzers) == 2
        for f in multi_log_files:
            Path(f).unlink()

    def test_find_correlations(self, multi_log_files):
        correlator = LogCorrelator()
        for f in multi_log_files:
            correlator.add_log(f)
        correlations = correlator.find_correlations(time_window_seconds=60)
        assert isinstance(correlations, list)
        for f in multi_log_files:
            Path(f).unlink()

    def test_generate_unified_timeline(self, multi_log_files):
        correlator = LogCorrelator()
        for f in multi_log_files:
            correlator.add_log(f)
        timeline = correlator.generate_unified_timeline()
        assert isinstance(timeline, list)
        # Events should be sorted by timestamp
        if len(timeline) > 1:
            for i in range(len(timeline) - 1):
                assert timeline[i].timestamp <= timeline[i + 1].timestamp
        for f in multi_log_files:
            Path(f).unlink()


class TestLogEntry:
    """Tests for LogEntry dataclass."""

    def test_create_log_entry(self):
        entry = LogEntry(
            line_number=1,
            raw="2025-01-15 ERROR test",
            timestamp=datetime(2025, 1, 15, 10, 0, 0),
            level="ERROR",
            message="test",
        )
        assert entry.line_number == 1
        assert entry.level == "ERROR"

    def test_log_entry_defaults(self):
        entry = LogEntry(line_number=1, raw="test")
        assert entry.timestamp is None
        assert entry.level is None
        assert entry.message == ""
        assert entry.extra == {}


class TestJSONLogAutoDetect:
    """Tests for auto-detection of JSON log format."""

    @pytest.fixture
    def json_log_file(self):
        """Create a JSON log file."""
        lines = [
            json.dumps({"timestamp": "2025-01-15T10:00:00Z", "level": "ERROR", "message": "fail"}),
            json.dumps({"timestamp": "2025-01-15T10:00:01Z", "level": "INFO", "message": "ok"}),
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            f.write("\n".join(lines))
            return f.name

    def test_auto_detect_json(self, json_log_file):
        analyzer = LogAnalyzer()
        analyzer.load_file(json_log_file)
        assert isinstance(analyzer.parser, JSONLogParser)
        assert len(analyzer.entries) == 2
        Path(json_log_file).unlink()
