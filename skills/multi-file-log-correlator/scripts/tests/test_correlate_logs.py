"""
Tests for multi-file-log-correlator.
"""

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest
from correlate_logs import (
    Correlation,
    Gap,
    LogCorrelator,
    LogEvent,
    LogSource,
)


class TestLogCorrelator:
    """Test the LogCorrelator class."""

    def test_parse_source_spec_minimal(self):
        """Test parsing minimal source spec with just file and name."""
        correlator = LogCorrelator()
        source = correlator.parse_source_spec("app.log:app")

        assert source.file_path == "app.log"
        assert source.name == "app"
        assert source.timezone == "UTC"
        assert source.timestamp_format is None

    def test_parse_source_spec_with_timezone(self):
        """Test parsing source spec with timezone."""
        correlator = LogCorrelator()
        source = correlator.parse_source_spec("nginx.log:nginx:America/New_York")

        assert source.file_path == "nginx.log"
        assert source.name == "nginx"
        assert source.timezone == "America/New_York"
        assert source.timestamp_format is None

    def test_parse_source_spec_full(self):
        """Test parsing full source spec with format."""
        correlator = LogCorrelator()
        source = correlator.parse_source_spec("db.log:database:UTC:%Y-%m-%d %H:%M:%S")

        assert source.file_path == "db.log"
        assert source.name == "database"
        assert source.timezone == "UTC"
        assert source.timestamp_format == "%Y-%m-%d %H:%M:%S"

    def test_parse_source_spec_invalid(self):
        """Test that invalid source spec raises error."""
        correlator = LogCorrelator()

        with pytest.raises(ValueError, match="Invalid source spec"):
            correlator.parse_source_spec("just_a_file.log")


class TestTimestampDetection:
    """Test timestamp detection and parsing."""

    def test_detect_iso8601_with_z(self):
        """Test detection of ISO 8601 timestamp with Z suffix."""
        correlator = LogCorrelator()
        line = "2025-01-15T10:30:45.123456Z INFO Application started"

        ts, ts_str, remaining = correlator._detect_timestamp(line)

        assert ts is not None
        assert ts.year == 2025
        assert ts.month == 1
        assert ts.day == 15
        assert ts.hour == 10
        assert ts.minute == 30
        assert ts.second == 45
        assert "INFO Application started" in remaining

    def test_detect_iso8601_space_separator(self):
        """Test detection of ISO 8601 with space separator."""
        correlator = LogCorrelator()
        line = "2025-01-15 10:30:45 [INFO] Processing request"

        ts, ts_str, remaining = correlator._detect_timestamp(line)

        assert ts is not None
        assert ts.year == 2025
        assert ts.hour == 10
        assert "[INFO] Processing request" in remaining

    def test_detect_apache_format(self):
        """Test detection of Apache/Nginx log format."""
        correlator = LogCorrelator()
        line = '192.168.1.1 - - [15/Jan/2025:10:30:45 +0000] "GET /api HTTP/1.1" 200'

        ts, ts_str, remaining = correlator._detect_timestamp(line)

        assert ts is not None
        assert ts.year == 2025
        assert ts.month == 1
        assert ts.day == 15

    def test_detect_java_log4j_format(self):
        """Test detection of Java/Log4j timestamp with comma milliseconds."""
        correlator = LogCorrelator()
        line = "2025-01-15 10:30:45,123 INFO com.app.Main - Starting"

        ts, ts_str, remaining = correlator._detect_timestamp(line)

        assert ts is not None
        assert ts.year == 2025


class TestLogLevelDetection:
    """Test log level detection."""

    def test_detect_error_level(self):
        """Test detection of ERROR level."""
        correlator = LogCorrelator()

        assert correlator._detect_log_level("ERROR: Something went wrong") == "ERROR"
        assert correlator._detect_log_level("[ERROR] Failed to connect") == "ERROR"
        assert correlator._detect_log_level("ERR connection refused") == "ERROR"

    def test_detect_warn_level(self):
        """Test detection of WARN level."""
        correlator = LogCorrelator()

        assert correlator._detect_log_level("WARN: Deprecated method") == "WARN"
        assert correlator._detect_log_level("[WARNING] Low memory") == "WARN"

    def test_detect_info_level(self):
        """Test detection of INFO level."""
        correlator = LogCorrelator()

        assert correlator._detect_log_level("INFO: Server started") == "INFO"
        assert correlator._detect_log_level("[INFO] Ready") == "INFO"

    def test_detect_fatal_level(self):
        """Test detection of FATAL level."""
        correlator = LogCorrelator()

        assert correlator._detect_log_level("FATAL: System crash") == "FATAL"
        assert correlator._detect_log_level("[CRITICAL] Out of memory") == "FATAL"


class TestCorrelationIdExtraction:
    """Test correlation ID extraction."""

    def test_extract_request_id(self):
        """Test extraction of request_id."""
        correlator = LogCorrelator()

        ids = correlator._extract_correlation_ids("request_id=abc123 Processing")
        assert "abc123" in ids

        ids = correlator._extract_correlation_ids("request_id: def456")
        assert "def456" in ids

    def test_extract_trace_id(self):
        """Test extraction of trace_id."""
        correlator = LogCorrelator()

        ids = correlator._extract_correlation_ids("trace_id=xyz789 span started")
        assert "xyz789" in ids

    def test_extract_uuid(self):
        """Test extraction of UUID format."""
        correlator = LogCorrelator()

        ids = correlator._extract_correlation_ids("[550e8400-e29b-41d4-a716-446655440000] Request")
        assert "550e8400-e29b-41d4-a716-446655440000" in ids

    def test_extract_multiple_ids(self):
        """Test extraction of multiple correlation IDs."""
        correlator = LogCorrelator()

        ids = correlator._extract_correlation_ids("request_id=req123 trace_id=trace456")
        assert "req123" in ids
        assert "trace456" in ids


class TestLogFileParsing:
    """Test log file parsing."""

    def test_parse_simple_log_file(self, tmp_path):
        """Test parsing a simple log file."""
        log_content = """2025-01-15 10:00:00 INFO Application started
2025-01-15 10:00:01 INFO Processing request
2025-01-15 10:00:02 ERROR Database connection failed
2025-01-15 10:00:03 WARN Retrying connection
"""
        log_file = tmp_path / "app.log"
        log_file.write_text(log_content)

        source = LogSource(
            name="app",
            file_path=str(log_file),
            timezone="UTC",
        )
        correlator = LogCorrelator()
        correlator.parse_log_file(source)

        assert source.event_count == 4
        assert source.events[0].level == "INFO"
        assert source.events[2].level == "ERROR"
        assert "Database connection failed" in source.events[2].message

    def test_parse_log_file_with_correlation_ids(self, tmp_path):
        """Test parsing log file with correlation IDs."""
        log_content = """2025-01-15 10:00:00 INFO request_id=req123 Started
2025-01-15 10:00:01 INFO request_id=req123 Processing
2025-01-15 10:00:02 INFO request_id=req456 New request
"""
        log_file = tmp_path / "app.log"
        log_file.write_text(log_content)

        source = LogSource(
            name="app",
            file_path=str(log_file),
            timezone="UTC",
        )
        correlator = LogCorrelator()
        correlator.parse_log_file(source)

        assert source.event_count == 3
        assert "req123" in source.events[0].correlation_ids
        assert "req123" in source.events[1].correlation_ids
        assert "req456" in source.events[2].correlation_ids


class TestTimelineBuilding:
    """Test timeline building from multiple sources."""

    def test_build_timeline_from_multiple_sources(self, tmp_path):
        """Test building unified timeline from multiple log files."""
        # Create app.log
        app_log = tmp_path / "app.log"
        app_log.write_text("""2025-01-15 10:00:01 INFO App event 1
2025-01-15 10:00:03 INFO App event 2
""")

        # Create nginx.log
        nginx_log = tmp_path / "nginx.log"
        nginx_log.write_text("""2025-01-15 10:00:00 INFO Nginx event 1
2025-01-15 10:00:02 INFO Nginx event 2
""")

        correlator = LogCorrelator()
        correlator.add_source(LogSource(name="app", file_path=str(app_log), timezone="UTC"))
        correlator.add_source(LogSource(name="nginx", file_path=str(nginx_log), timezone="UTC"))

        timeline = correlator.build_timeline()

        assert len(timeline) == 4
        # Events should be sorted by timestamp
        assert timeline[0].source == "nginx"  # 10:00:00
        assert timeline[1].source == "app"  # 10:00:01
        assert timeline[2].source == "nginx"  # 10:00:02
        assert timeline[3].source == "app"  # 10:00:03


class TestCorrelationFinding:
    """Test correlation finding."""

    def test_find_correlations_by_id(self, tmp_path):
        """Test finding correlations by correlation ID."""
        # Create app.log
        app_log = tmp_path / "app.log"
        app_log.write_text("""2025-01-15 10:00:01 INFO request_id=abc123 App processing
""")

        # Create nginx.log
        nginx_log = tmp_path / "nginx.log"
        nginx_log.write_text("""2025-01-15 10:00:00 INFO request_id=abc123 Nginx received
""")

        correlator = LogCorrelator()
        correlator.add_source(LogSource(name="app", file_path=str(app_log), timezone="UTC"))
        correlator.add_source(LogSource(name="nginx", file_path=str(nginx_log), timezone="UTC"))

        correlator.build_timeline()
        correlator.find_correlations()

        assert len(correlator.correlations) == 1
        assert "abc123" in correlator.correlations
        corr = correlator.correlations["abc123"]
        assert len(corr.events) == 2
        assert corr.total_duration_ms == 1000.0  # 1 second = 1000ms


class TestGapDetection:
    """Test gap detection."""

    def test_detect_gaps_in_logs(self, tmp_path):
        """Test detection of gaps in log files."""
        log_file = tmp_path / "app.log"
        log_file.write_text("""2025-01-15 10:00:00 INFO Event 1
2025-01-15 10:00:30 INFO Event 2
2025-01-15 10:03:00 INFO Event 3
2025-01-15 10:03:30 INFO Event 4
""")

        correlator = LogCorrelator(gap_threshold_seconds=60.0)
        correlator.add_source(LogSource(name="app", file_path=str(log_file), timezone="UTC"))
        correlator.build_timeline()
        gaps = correlator.detect_gaps()

        # Should detect gap between 10:00:30 and 10:03:00 (150 seconds)
        assert len(gaps) == 1
        assert gaps[0].source == "app"
        assert gaps[0].duration_seconds == 150.0


class TestOutputGeneration:
    """Test output generation."""

    def test_generate_summary(self, tmp_path):
        """Test summary generation."""
        log_file = tmp_path / "app.log"
        log_file.write_text("""2025-01-15 10:00:00 INFO Event 1
2025-01-15 10:00:01 INFO Event 2
""")

        correlator = LogCorrelator()
        correlator.add_source(LogSource(name="app", file_path=str(log_file), timezone="UTC"))
        correlator.build_timeline()

        summary = correlator.generate_summary()

        assert summary["total_events"] == 2
        assert len(summary["sources"]) == 1
        assert summary["sources"][0]["name"] == "app"
        assert summary["sources"][0]["event_count"] == 2

    def test_to_json(self, tmp_path):
        """Test JSON output generation."""
        log_file = tmp_path / "app.log"
        log_file.write_text("""2025-01-15 10:00:00 INFO Event 1
""")

        correlator = LogCorrelator()
        correlator.add_source(LogSource(name="app", file_path=str(log_file), timezone="UTC"))
        correlator.build_timeline()

        result = correlator.to_json()

        assert result["schema_version"] == "1.0"
        assert "generated_at" in result
        assert result["output_timezone"] == "UTC"
        assert len(result["sources"]) == 1
        assert len(result["timeline"]) == 1

    def test_to_markdown(self, tmp_path):
        """Test Markdown report generation."""
        log_file = tmp_path / "app.log"
        log_file.write_text("""2025-01-15 10:00:00 INFO Event 1
2025-01-15 10:00:01 ERROR Error occurred
""")

        correlator = LogCorrelator()
        correlator.add_source(LogSource(name="app", file_path=str(log_file), timezone="UTC"))
        correlator.build_timeline()
        correlator.detect_anomalies()

        markdown = correlator.to_markdown()

        assert "# Multi-File Log Correlation Report" in markdown
        assert "## Source Summary" in markdown
        assert "| app |" in markdown
        assert "## Timeline Sample" in markdown


class TestAnomalyDetection:
    """Test anomaly detection."""

    def test_detect_error_burst(self, tmp_path):
        """Test detection of error bursts."""
        # Create log with many errors in one minute
        errors = "\n".join([f"2025-01-15 10:00:{i:02d} ERROR Error {i}" for i in range(15)])
        log_file = tmp_path / "app.log"
        log_file.write_text(errors)

        correlator = LogCorrelator()
        correlator.add_source(LogSource(name="app", file_path=str(log_file), timezone="UTC"))
        correlator.build_timeline()
        anomalies = correlator.detect_anomalies()

        # Should detect error burst (>10 errors per minute)
        error_bursts = [a for a in anomalies if a.anomaly_type == "error_burst"]
        assert len(error_bursts) >= 1
