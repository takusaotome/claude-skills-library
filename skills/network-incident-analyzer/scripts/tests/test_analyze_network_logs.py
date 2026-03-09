"""
Tests for network-incident-analyzer script.
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from analyze_network_logs import (
    Anomaly,
    AnomalyDetector,
    CorrelationCluster,
    EventCorrelator,
    LogEvent,
    LogParser,
    NetworkIncidentAnalyzer,
    ReportGenerator,
    RootCauseAnalyzer,
    RootCauseHypothesis,
    parse_datetime,
)


class TestLogParser:
    """Tests for LogParser class."""

    def test_detect_cisco_ios_format(self):
        """Test detection of Cisco IOS log format."""
        parser = LogParser()
        line = "*Mar 15 10:23:45.123: %LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down"
        assert parser.detect_format(line) == "cisco_ios"

    def test_detect_junos_format(self):
        """Test detection of Juniper JunOS log format."""
        parser = LogParser()
        line = "Mar 15 10:23:45 router-name rpd[1234]: BGP_NEIGHBOR_STATE_CHANGED: Peer 10.0.0.1 state changed"
        assert parser.detect_format(line) == "junos"

    def test_detect_json_format(self):
        """Test detection of JSON log format."""
        parser = LogParser()
        line = '{"timestamp": "2024-03-15T10:23:45Z", "level": "error", "message": "Connection timeout"}'
        assert parser.detect_format(line) == "json"

    def test_detect_syslog_format(self):
        """Test detection of syslog RFC3164 format."""
        parser = LogParser()
        line = "<134>Mar 15 10:23:45 hostname process[1234]: Message content here"
        assert parser.detect_format(line) == "syslog_rfc3164"

    def test_detect_palo_alto_format(self):
        """Test detection of Palo Alto log format."""
        parser = LogParser()
        line = "Mar 15 10:23:45,INFO,TRAFFIC,end,some data here"
        assert parser.detect_format(line) == "palo_alto"

    def test_detect_f5_format(self):
        """Test detection of F5 BIG-IP log format."""
        parser = LogParser()
        line = "Mar 15 10:23:45 bigip-ltm01 info tmm[1234]: Rule /Common/redirect: Client redirected"
        assert parser.detect_format(line) == "f5"

    def test_parse_cisco_ios_line(self):
        """Test parsing a Cisco IOS log line."""
        parser = LogParser(default_year=2024)
        line = "*Mar 15 10:23:45.123: %LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down"

        event = parser.parse_line(line, "cisco_ios", "test.log", 1)

        assert event is not None
        assert event.severity == "error"  # Level 3
        assert "Interface GigabitEthernet0/1" in event.message
        assert event.event_type == "interface_state"
        assert event.log_format == "cisco_ios"

    def test_parse_json_line(self):
        """Test parsing a JSON log line."""
        parser = LogParser()
        line = '{"timestamp": "2024-03-15T10:23:45Z", "level": "error", "message": "Connection timeout", "device": "router-01"}'

        event = parser.parse_line(line, "json", "test.log", 1)

        assert event is not None
        assert event.device == "router-01"
        assert event.message == "Connection timeout"
        assert event.severity == "error"
        assert event.event_type == "connection_failure"

    def test_parse_empty_line_returns_none(self):
        """Test that empty lines return None."""
        parser = LogParser()
        assert parser.parse_line("", "cisco_ios", "test.log", 1) is None
        assert parser.parse_line("   ", "cisco_ios", "test.log", 1) is None

    def test_classify_event_connection_failure(self):
        """Test event classification for connection failures."""
        parser = LogParser()
        assert parser._classify_event("TCP connection timeout after 30s") == "connection_failure"
        assert parser._classify_event("Connection refused by host") == "connection_failure"

    def test_classify_event_bgp(self):
        """Test event classification for BGP events."""
        parser = LogParser()
        assert parser._classify_event("BGP peer 10.0.0.1 down") == "bgp_event"
        assert parser._classify_event("BGP neighbor state changed to Idle") == "bgp_event"

    def test_classify_event_interface(self):
        """Test event classification for interface events."""
        parser = LogParser()
        assert parser._classify_event("Interface state changed to down") == "interface_state"
        assert parser._classify_event("Link up on port Gi0/1") == "interface_state"


class TestAnomalyDetector:
    """Tests for AnomalyDetector class."""

    def _create_events(
        self, count: int, event_type: str, start_time: datetime, interval_seconds: int = 1, device: str = "router-01"
    ) -> list[LogEvent]:
        """Helper to create test events."""
        events = []
        for i in range(count):
            events.append(
                LogEvent(
                    timestamp=start_time + timedelta(seconds=i * interval_seconds),
                    device=device,
                    message=f"Test {event_type} event {i}",
                    event_type=event_type,
                )
            )
        return events

    def test_detect_connection_failure_spike(self):
        """Test detection of connection failure spike anomaly."""
        detector = AnomalyDetector()
        start_time = datetime(2024, 3, 15, 10, 0, 0, tzinfo=timezone.utc)

        # Create 60 connection failures in 30 seconds (exceeds threshold of 50/minute)
        events = self._create_events(60, "connection_failure", start_time, interval_seconds=0.5)

        anomalies = detector.detect_anomalies(events)

        assert len(anomalies) >= 1
        failure_anomalies = [a for a in anomalies if a.anomaly_type == "connection_failure_spike"]
        assert len(failure_anomalies) >= 1
        assert failure_anomalies[0].severity in ("warning", "error", "critical")

    def test_detect_interface_flapping(self):
        """Test detection of interface flapping anomaly."""
        detector = AnomalyDetector()
        start_time = datetime(2024, 3, 15, 10, 0, 0, tzinfo=timezone.utc)

        # Create 5 interface state changes in 1 minute (exceeds threshold of 3/5min)
        events = self._create_events(5, "interface_state", start_time, interval_seconds=10)

        anomalies = detector.detect_anomalies(events)

        flapping = [a for a in anomalies if a.anomaly_type == "interface_flapping"]
        assert len(flapping) >= 1
        assert flapping[0].severity == "critical"

    def test_detect_error_spike(self):
        """Test detection of error rate spike anomaly."""
        detector = AnomalyDetector()
        start_time = datetime(2024, 3, 15, 10, 0, 0, tzinfo=timezone.utc)

        # Create baseline errors (10 per 5 minutes)
        baseline = self._create_events(10, "error", start_time, interval_seconds=30)

        # Create spike (30 errors in 30 seconds)
        spike_start = start_time + timedelta(minutes=6)
        spike = self._create_events(30, "error", spike_start, interval_seconds=1)

        events = baseline + spike
        anomalies = detector.detect_anomalies(events)

        # Should detect error rate spike
        error_spikes = [a for a in anomalies if a.anomaly_type == "error_rate_spike"]
        assert len(error_spikes) >= 1

    def test_no_anomalies_below_threshold(self):
        """Test that no anomalies are detected below thresholds."""
        detector = AnomalyDetector()
        start_time = datetime(2024, 3, 15, 10, 0, 0, tzinfo=timezone.utc)

        # Create just 10 connection failures spread over 10 minutes
        events = self._create_events(10, "connection_failure", start_time, interval_seconds=60)

        anomalies = detector.detect_anomalies(events)

        # Should not detect connection failure spike
        failure_anomalies = [a for a in anomalies if a.anomaly_type == "connection_failure_spike"]
        assert len(failure_anomalies) == 0

    def test_anomaly_contains_affected_devices(self):
        """Test that anomalies include affected device information."""
        detector = AnomalyDetector()
        start_time = datetime(2024, 3, 15, 10, 0, 0, tzinfo=timezone.utc)

        # Create failures from multiple devices
        events = []
        for i in range(60):
            device = f"router-0{i % 3 + 1}"
            events.append(
                LogEvent(
                    timestamp=start_time + timedelta(seconds=i * 0.5),
                    device=device,
                    message="Connection timeout",
                    event_type="connection_failure",
                )
            )

        anomalies = detector.detect_anomalies(events)

        failure_anomalies = [a for a in anomalies if a.anomaly_type == "connection_failure_spike"]
        assert len(failure_anomalies) >= 1
        assert len(failure_anomalies[0].affected_devices) >= 2


class TestEventCorrelator:
    """Tests for EventCorrelator class."""

    def _create_cascade_events(self, start_time: datetime) -> list[LogEvent]:
        """Create a realistic cascade of correlated events."""
        return [
            LogEvent(
                timestamp=start_time,
                device="core-router-01",
                message="BGP peer 10.0.0.1 down",
                event_type="bgp_event",
            ),
            LogEvent(
                timestamp=start_time + timedelta(seconds=2),
                device="fw-edge-01",
                message="Connection timeout to upstream",
                event_type="connection_failure",
            ),
            LogEvent(
                timestamp=start_time + timedelta(seconds=5),
                device="switch-access-01",
                message="ARP timeout for gateway",
                event_type="connection_failure",
            ),
        ]

    def test_correlate_cascade_events(self):
        """Test correlation of cascading events across devices."""
        correlator = EventCorrelator()
        start_time = datetime(2024, 3, 15, 10, 23, 45, tzinfo=timezone.utc)

        events = self._create_cascade_events(start_time)
        clusters = correlator.correlate_events(events, [])

        assert len(clusters) >= 1
        assert clusters[0].root_cause_device == "core-router-01"
        assert clusters[0].confidence > 0.5

    def test_correlation_generates_hypothesis(self):
        """Test that correlation generates a hypothesis."""
        correlator = EventCorrelator()
        start_time = datetime(2024, 3, 15, 10, 23, 45, tzinfo=timezone.utc)

        events = self._create_cascade_events(start_time)
        clusters = correlator.correlate_events(events, [])

        assert len(clusters) >= 1
        assert "BGP" in clusters[0].hypothesis or "connectivity" in clusters[0].hypothesis.lower()

    def test_no_correlation_for_distant_events(self):
        """Test that events far apart in time are not correlated."""
        correlator = EventCorrelator()
        start_time = datetime(2024, 3, 15, 10, 0, 0, tzinfo=timezone.utc)

        events = [
            LogEvent(
                timestamp=start_time,
                device="router-01",
                message="BGP peer down",
                event_type="bgp_event",
            ),
            LogEvent(
                timestamp=start_time + timedelta(minutes=10),  # 10 minutes later
                device="router-02",
                message="Connection timeout",
                event_type="connection_failure",
            ),
        ]

        clusters = correlator.correlate_events(events, [])

        # Should not create a cluster for events 10 minutes apart
        assert len(clusters) == 0


class TestRootCauseAnalyzer:
    """Tests for RootCauseAnalyzer class."""

    def test_analyze_connection_failure_anomaly(self):
        """Test hypothesis generation for connection failure anomaly."""
        analyzer = RootCauseAnalyzer()

        anomaly = Anomaly(
            anomaly_id="ANO-001",
            anomaly_type="connection_failure_spike",
            severity="critical",
            start_time=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
            end_time=datetime(2024, 3, 15, 10, 5, tzinfo=timezone.utc),
            affected_devices=["router-01", "router-02"],
            event_count=150,
            baseline_value=10,
            peak_value=150,
        )

        hypotheses = analyzer.analyze([anomaly], [])

        assert len(hypotheses) >= 1
        assert hypotheses[0].confidence > 0.5
        assert len(hypotheses[0].recommended_actions) > 0

    def test_analyze_interface_flapping_anomaly(self):
        """Test hypothesis generation for interface flapping anomaly."""
        analyzer = RootCauseAnalyzer()

        anomaly = Anomaly(
            anomaly_id="ANO-002",
            anomaly_type="interface_flapping",
            severity="critical",
            start_time=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
            end_time=datetime(2024, 3, 15, 10, 5, tzinfo=timezone.utc),
            affected_devices=["switch-01"],
            event_count=10,
        )

        hypotheses = analyzer.analyze([anomaly], [])

        assert len(hypotheses) >= 1
        assert "interface" in hypotheses[0].hypothesis.lower() or "instability" in hypotheses[0].hypothesis.lower()
        assert hypotheses[0].confidence > 0.7

    def test_analyze_bgp_correlation_cluster(self):
        """Test hypothesis generation from BGP correlation cluster."""
        analyzer = RootCauseAnalyzer()

        events = [
            LogEvent(
                timestamp=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
                device="core-router",
                message="BGP peer down",
                event_type="bgp_event",
            ),
            LogEvent(
                timestamp=datetime(2024, 3, 15, 10, 0, 2, tzinfo=timezone.utc),
                device="edge-router",
                message="Connection failure",
                event_type="connection_failure",
            ),
        ]

        cluster = CorrelationCluster(
            cluster_id="CLU-001",
            confidence=0.85,
            root_cause_device="core-router",
            events=events,
            hypothesis="BGP session failure triggered connectivity disruption",
        )

        hypotheses = analyzer.analyze([], [cluster])

        assert len(hypotheses) >= 1
        assert "BGP" in hypotheses[0].hypothesis


class TestReportGenerator:
    """Tests for ReportGenerator class."""

    def test_generate_json_report(self, tmp_path: Path):
        """Test JSON report generation."""
        generator = ReportGenerator(tmp_path)

        events = [
            LogEvent(
                timestamp=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
                device="router-01",
                message="Test event",
                source_file="test.log",
                log_format="cisco_ios",
            )
        ]

        anomalies = [
            Anomaly(
                anomaly_id="ANO-001",
                anomaly_type="connection_failure_spike",
                severity="critical",
                start_time=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
                end_time=datetime(2024, 3, 15, 10, 5, tzinfo=timezone.utc),
                affected_devices=["router-01"],
                event_count=50,
            )
        ]

        output_path = generator.generate_json_report(
            events,
            anomalies,
            [],
            [],
            datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
            datetime(2024, 3, 15, 12, 0, tzinfo=timezone.utc),
            ["test.log"],
        )

        assert output_path.exists()
        with open(output_path) as f:
            report = json.load(f)

        assert report["schema_version"] == "1.0"
        assert len(report["anomalies_detected"]) == 1
        assert report["total_events_parsed"] == 1

    def test_generate_markdown_report(self, tmp_path: Path):
        """Test Markdown report generation."""
        generator = ReportGenerator(tmp_path)

        events = [
            LogEvent(
                timestamp=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
                device="router-01",
                message="Test event",
                event_type="connection_failure",
            )
        ]

        hypotheses = [
            RootCauseHypothesis(
                hypothesis="Network connectivity disruption",
                confidence=0.85,
                supporting_evidence=["Evidence 1"],
                recommended_actions=["Action 1"],
            )
        ]

        output_path = generator.generate_markdown_report(
            events,
            [],
            [],
            hypotheses,
            datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
            datetime(2024, 3, 15, 12, 0, tzinfo=timezone.utc),
        )

        assert output_path.exists()
        content = output_path.read_text()

        assert "# Network Incident Root Cause Analysis" in content
        assert "Root Cause Hypotheses" in content
        assert "Network connectivity disruption" in content

    def test_generate_summary(self, tmp_path: Path):
        """Test summary report generation."""
        generator = ReportGenerator(tmp_path)

        anomalies = [
            Anomaly(
                anomaly_id="ANO-001",
                anomaly_type="connection_failure_spike",
                severity="critical",
                start_time=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
                end_time=datetime(2024, 3, 15, 10, 30, tzinfo=timezone.utc),
                affected_devices=["router-01", "router-02"],
                event_count=100,
            )
        ]

        hypotheses = [
            RootCauseHypothesis(
                hypothesis="Primary root cause",
                confidence=0.9,
                supporting_evidence=["Evidence"],
                recommended_actions=["Action"],
            )
        ]

        output_path = generator.generate_summary(
            anomalies,
            hypotheses,
            datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
            datetime(2024, 3, 15, 10, 30, tzinfo=timezone.utc),
        )

        assert output_path.exists()
        content = output_path.read_text()

        assert "# Incident Summary" in content
        assert "Impact Assessment" in content
        assert "Primary root cause" in content


class TestNetworkIncidentAnalyzer:
    """Integration tests for NetworkIncidentAnalyzer."""

    def test_full_analysis_pipeline(self, tmp_path: Path):
        """Test complete analysis pipeline with sample log file."""
        # Create sample log file
        log_content = """*Mar 15 10:00:00.000: %BGP-3-NOTIFICATION: Peer 10.0.0.1 down
*Mar 15 10:00:02.000: %LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down
*Mar 15 10:00:05.000: %SYS-4-ERROR: Connection timeout to 192.168.1.1
*Mar 15 10:00:06.000: %SYS-4-ERROR: Connection timeout to 192.168.1.2
*Mar 15 10:00:07.000: %SYS-4-ERROR: Connection timeout to 192.168.1.3
"""
        log_file = tmp_path / "test_router.log"
        log_file.write_text(log_content)

        output_dir = tmp_path / "output"
        analyzer = NetworkIncidentAnalyzer(output_dir)

        results = analyzer.analyze(
            [str(log_file)],
            datetime(2024, 3, 15, 9, 0, tzinfo=timezone.utc),
            datetime(2024, 3, 15, 11, 0, tzinfo=timezone.utc),
        )

        assert results["events_parsed"] >= 5
        assert "reports" in results
        assert Path(results["reports"]["json"]).exists()
        assert Path(results["reports"]["analysis"]).exists()
        assert Path(results["reports"]["summary"]).exists()


class TestParseDatetime:
    """Tests for parse_datetime utility function."""

    def test_parse_datetime_full(self):
        """Test parsing full datetime string."""
        result = parse_datetime("2024-03-15 10:30:45")
        assert result.year == 2024
        assert result.month == 3
        assert result.day == 15
        assert result.hour == 10
        assert result.minute == 30

    def test_parse_datetime_iso(self):
        """Test parsing ISO format datetime."""
        result = parse_datetime("2024-03-15T10:30:45")
        assert result.year == 2024
        assert result.hour == 10

    def test_parse_datetime_date_only(self):
        """Test parsing date-only string."""
        result = parse_datetime("2024-03-15")
        assert result.year == 2024
        assert result.month == 3
        assert result.day == 15

    def test_parse_datetime_invalid(self):
        """Test that invalid datetime raises error."""
        with pytest.raises(ValueError):
            parse_datetime("invalid-date")


class TestLogEventDataclass:
    """Tests for LogEvent dataclass."""

    def test_to_dict(self):
        """Test LogEvent to_dict conversion."""
        event = LogEvent(
            timestamp=datetime(2024, 3, 15, 10, 0, tzinfo=timezone.utc),
            device="router-01",
            message="Test message",
            severity="error",
            event_type="connection_failure",
            source_file="test.log",
            line_number=42,
        )

        d = event.to_dict()

        assert d["device"] == "router-01"
        assert d["message"] == "Test message"
        assert d["severity"] == "error"
        assert d["line_number"] == 42
        assert "2024-03-15" in d["timestamp"]
