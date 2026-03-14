"""
Tests for timezone_event_tracker.py

Tests cover:
1. Timestamp parsing with various formats and timezones
2. Event correlation within time windows
3. DST transition detection
4. Report generation
"""

import json
from datetime import datetime
from pathlib import Path

import pytest
from timezone_event_tracker import (
    TZ_ABBREVIATIONS,
    CorrelationGroup,
    Event,
    check_dst_issues,
    classify_pattern,
    correlate_events,
    generate_markdown_report,
    parse_events,
    parse_timestamp,
)

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo


class TestParseTimestamp:
    """Tests for timestamp parsing functionality."""

    def test_parse_iso_with_offset(self):
        """Test parsing ISO 8601 timestamp with offset."""
        raw = "2024-03-15T10:30:00-07:00"
        dt_utc, source_tz, dst_status, warning = parse_timestamp(raw)

        assert dt_utc.hour == 17  # 10:30 -07:00 = 17:30 UTC
        assert dt_utc.minute == 30
        assert warning is None

    def test_parse_iso_with_z_suffix(self):
        """Test parsing ISO 8601 timestamp with Z (UTC) suffix."""
        raw = "2024-03-15T10:30:00Z"
        dt_utc, source_tz, dst_status, warning = parse_timestamp(raw)

        assert dt_utc.hour == 10
        assert dt_utc.minute == 30
        assert warning is None

    def test_parse_with_timezone_abbreviation_pst(self):
        """Test parsing timestamp with PST abbreviation."""
        raw = "2024-01-15 10:30:00 PST"  # January = standard time
        dt_utc, source_tz, dst_status, warning = parse_timestamp(raw)

        # PST is UTC-8, so 10:30 PST = 18:30 UTC
        assert dt_utc.hour == 18
        assert dt_utc.minute == 30
        assert source_tz == "America/Los_Angeles"

    def test_parse_with_timezone_abbreviation_jst(self):
        """Test parsing timestamp with JST abbreviation."""
        raw = "2024-03-15 10:30:00 JST"
        dt_utc, source_tz, dst_status, warning = parse_timestamp(raw)

        # JST is UTC+9, so 10:30 JST = 01:30 UTC
        assert dt_utc.hour == 1
        assert dt_utc.minute == 30
        assert source_tz == "Asia/Tokyo"

    def test_parse_with_unknown_abbreviation(self):
        """Test parsing with unknown timezone abbreviation uses default."""
        raw = "2024-03-15 10:30:00 XYZ"
        dt_utc, source_tz, dst_status, warning = parse_timestamp(raw, default_tz="UTC")

        assert warning is not None
        assert "Unknown timezone abbreviation" in warning

    def test_parse_no_timezone_uses_default(self):
        """Test parsing timestamp without timezone uses default."""
        raw = "2024-03-15 10:30:00"
        dt_utc, source_tz, dst_status, warning = parse_timestamp(raw, default_tz="America/New_York")

        assert warning is not None
        assert "assumed" in warning.lower()
        assert source_tz == "America/New_York"

    def test_parse_log_format(self):
        """Test parsing common log format timestamp."""
        raw = "15/Mar/2024:10:30:00 -0700"
        dt_utc, source_tz, dst_status, warning = parse_timestamp(raw)

        assert dt_utc.hour == 17  # -0700 offset
        assert dt_utc.minute == 30

    def test_invalid_timestamp_raises_error(self):
        """Test that invalid timestamp raises ValueError."""
        raw = "not a timestamp"
        with pytest.raises(ValueError):
            parse_timestamp(raw)


class TestParseEvents:
    """Tests for event parsing from files."""

    def test_parse_csv_events(self, tmp_path):
        """Test parsing events from CSV file."""
        csv_content = """timestamp,description,timezone,severity
2024-03-15 10:30:00 PST,Server restart,America/Los_Angeles,info
2024-03-15 13:45:00 EST,Database backup,America/New_York,info
"""
        csv_file = tmp_path / "events.csv"
        csv_file.write_text(csv_content)

        events = parse_events(csv_file)

        assert len(events) == 2
        assert events[0].description == "Server restart"
        assert events[1].description == "Database backup"
        assert "severity" in events[0].metadata

    def test_parse_json_events(self, tmp_path):
        """Test parsing events from JSON file."""
        json_content = {
            "events": [
                {"timestamp": "2024-03-15T10:30:00-07:00", "description": "Alert triggered", "severity": "warning"},
                {"timestamp": "2024-03-15T10:35:00Z", "description": "Issue resolved"},
            ]
        }
        json_file = tmp_path / "events.json"
        json_file.write_text(json.dumps(json_content))

        events = parse_events(json_file)

        assert len(events) == 2
        assert events[0].description == "Alert triggered"

    def test_parse_events_sorted_by_time(self, tmp_path):
        """Test that parsed events are sorted chronologically."""
        csv_content = """timestamp,description
2024-03-15 15:00:00 UTC,Third event
2024-03-15 10:00:00 UTC,First event
2024-03-15 12:00:00 UTC,Second event
"""
        csv_file = tmp_path / "events.csv"
        csv_file.write_text(csv_content)

        events = parse_events(csv_file)

        assert events[0].description == "First event"
        assert events[1].description == "Second event"
        assert events[2].description == "Third event"


class TestCorrelateEvents:
    """Tests for event correlation functionality."""

    def test_correlate_events_within_window(self):
        """Test that events within window are grouped together."""
        events = [
            Event(
                id="evt-001",
                original_timestamp="2024-03-15 10:00:00 UTC",
                normalized_timestamp="2024-03-15T10:00:00+00:00",
                source_timezone="UTC",
                description="First event",
                metadata={},
                dst_status="standard_time",
            ),
            Event(
                id="evt-002",
                original_timestamp="2024-03-15 10:02:00 UTC",
                normalized_timestamp="2024-03-15T10:02:00+00:00",
                source_timezone="UTC",
                description="Second event",
                metadata={},
                dst_status="standard_time",
            ),
        ]

        groups = correlate_events(events, window_minutes=5)

        assert len(groups) == 1
        assert len(groups[0].event_ids) == 2
        assert groups[0].time_span_seconds == 120  # 2 minutes

    def test_correlate_events_outside_window(self):
        """Test that events outside window are not grouped."""
        events = [
            Event(
                id="evt-001",
                original_timestamp="2024-03-15 10:00:00 UTC",
                normalized_timestamp="2024-03-15T10:00:00+00:00",
                source_timezone="UTC",
                description="First event",
                metadata={},
                dst_status="standard_time",
            ),
            Event(
                id="evt-002",
                original_timestamp="2024-03-15 10:10:00 UTC",
                normalized_timestamp="2024-03-15T10:10:00+00:00",
                source_timezone="UTC",
                description="Second event",
                metadata={},
                dst_status="standard_time",
            ),
        ]

        groups = correlate_events(events, window_minutes=5)

        # No groups because events are 10 minutes apart (> 5 minute window)
        assert len(groups) == 0

    def test_correlate_empty_events(self):
        """Test correlation with empty event list."""
        groups = correlate_events([], window_minutes=5)
        assert groups == []


class TestClassifyPattern:
    """Tests for event pattern classification."""

    def test_classify_cascading_failure(self):
        """Test classification of rapid cascading events."""
        events = [
            Event(
                id=f"evt-{i}",
                original_timestamp=f"2024-03-15 10:00:{i:02d} UTC",
                normalized_timestamp=f"2024-03-15T10:00:{i:02d}+00:00",
                source_timezone="UTC",
                description=f"Event {i}",
                metadata={},
                dst_status="standard_time",
            )
            for i in range(5)  # 5 events, 1 second apart
        ]

        pattern = classify_pattern(events)
        assert pattern == "cascading_failure"

    def test_classify_single_event(self):
        """Test classification of single event."""
        events = [
            Event(
                id="evt-001",
                original_timestamp="2024-03-15 10:00:00 UTC",
                normalized_timestamp="2024-03-15T10:00:00+00:00",
                source_timezone="UTC",
                description="Single event",
                metadata={},
                dst_status="standard_time",
            )
        ]

        pattern = classify_pattern(events)
        assert pattern == "single_event"


class TestDSTCheck:
    """Tests for DST transition detection."""

    def test_check_dst_issues_with_la_timezone(self):
        """Test DST check for Los Angeles timezone."""
        events = [
            Event(
                id="evt-001",
                original_timestamp="2024-03-10 02:30:00 PST",
                normalized_timestamp="2024-03-10T10:30:00+00:00",
                source_timezone="America/Los_Angeles",
                description="Event on DST transition",
                metadata={},
                dst_status="standard_time",
            )
        ]

        result = check_dst_issues(events, 2024)

        # Los Angeles has DST transitions
        assert "America/Los_Angeles" in result["timezones_checked"]
        assert len(result["dst_transitions"].get("America/Los_Angeles", [])) == 2

    def test_check_dst_issues_no_dst_timezone(self):
        """Test DST check for timezone without DST (Japan)."""
        events = [
            Event(
                id="evt-001",
                original_timestamp="2024-03-10 10:00:00 JST",
                normalized_timestamp="2024-03-10T01:00:00+00:00",
                source_timezone="Asia/Tokyo",
                description="Event in Japan",
                metadata={},
                dst_status="standard_time",
            )
        ]

        result = check_dst_issues(events, 2024)

        # Tokyo has no DST transitions
        assert "Asia/Tokyo" in result["timezones_checked"]
        assert len(result["dst_transitions"].get("Asia/Tokyo", [])) == 0


class TestReportGeneration:
    """Tests for report generation."""

    def test_generate_markdown_report(self):
        """Test markdown report generation."""
        events = [
            Event(
                id="evt-001",
                original_timestamp="2024-03-15 10:00:00 UTC",
                normalized_timestamp="2024-03-15T10:00:00+00:00",
                source_timezone="UTC",
                description="Test event",
                metadata={"source_system": "test"},
                dst_status="standard_time",
            )
        ]
        groups = []
        timezones = ["America/Los_Angeles", "Asia/Tokyo"]
        generated_at = datetime(2024, 3, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC"))

        report = generate_markdown_report(events, groups, timezones, generated_at)

        assert "# Event Timeline Report" in report
        assert "Total events: 1" in report
        assert "Test event" in report
        assert "Los_Angel" in report  # Truncated timezone name


class TestTimezoneAbbreviations:
    """Tests for timezone abbreviation mapping."""

    def test_common_abbreviations_mapped(self):
        """Test that common abbreviations are mapped to IANA names."""
        assert TZ_ABBREVIATIONS["PST"] == "America/Los_Angeles"
        assert TZ_ABBREVIATIONS["EST"] == "America/New_York"
        assert TZ_ABBREVIATIONS["JST"] == "Asia/Tokyo"
        assert TZ_ABBREVIATIONS["UTC"] == "UTC"

    def test_dst_variants_mapped_same(self):
        """Test that DST variants map to same timezone."""
        assert TZ_ABBREVIATIONS["PST"] == TZ_ABBREVIATIONS["PDT"]
        assert TZ_ABBREVIATIONS["EST"] == TZ_ABBREVIATIONS["EDT"]
