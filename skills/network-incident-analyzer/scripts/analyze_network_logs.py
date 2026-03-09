#!/usr/bin/env python3
"""
Network Incident Analyzer

Analyzes network device logs to identify connectivity issues, latency problems,
and outages. Correlates timestamps across timezones, detects anomaly patterns,
and generates incident reports with root cause hypotheses.

Usage:
    python3 analyze_network_logs.py \
        --logs router.log firewall.log \
        --start "2024-01-15 10:00:00" \
        --end "2024-01-15 12:00:00" \
        --timezone "America/New_York" \
        --output-dir ./incident-report
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# -----------------------------------------------------------------------------
# Log Format Definitions
# -----------------------------------------------------------------------------

LOG_FORMATS = {
    "cisco_ios": {
        "pattern": r"^\*?(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?):?\s*%(\w+)-(\d)-(\w+):\s*(.+)$",
        "timestamp_format": "%b %d %H:%M:%S",
        "groups": {"timestamp": 1, "facility": 2, "severity": 3, "mnemonic": 4, "message": 5},
    },
    "junos": {
        "pattern": r"^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\w+)\[(\d+)\]:\s*(.+)$",
        "timestamp_format": "%b %d %H:%M:%S",
        "groups": {"timestamp": 1, "hostname": 2, "process": 3, "pid": 4, "message": 5},
    },
    "palo_alto": {
        "pattern": r"^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}),(\w+),(\w+),(\w+),(.+)$",
        "timestamp_format": "%b %d %H:%M:%S",
        "groups": {"timestamp": 1, "level": 2, "type": 3, "subtype": 4, "message": 5},
    },
    "f5": {
        "pattern": r"^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\w+)\s+(\w+)\[(\d+)\]:\s*(.+)$",
        "timestamp_format": "%b %d %H:%M:%S",
        "groups": {"timestamp": 1, "hostname": 2, "level": 3, "process": 4, "pid": 5, "message": 6},
    },
    "syslog_rfc3164": {
        "pattern": r"^<(\d+)>(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+?)(?:\[(\d+)\])?:\s*(.+)$",
        "timestamp_format": "%b %d %H:%M:%S",
        "groups": {"priority": 1, "timestamp": 2, "hostname": 3, "process": 4, "pid": 5, "message": 6},
    },
    "json": {
        "pattern": None,  # JSON parsing handled separately
        "timestamp_format": None,
        "groups": {},
    },
}

# Event type keywords for classification
EVENT_KEYWORDS = {
    "connection_failure": [
        "timeout",
        "connection refused",
        "unreachable",
        "no route",
        "connection failed",
        "socket error",
        "connect failed",
    ],
    "interface_state": [
        "updown",
        "link down",
        "link up",
        "interface up",
        "interface down",
        "carrier",
        "line protocol",
        "state changed",
    ],
    "bgp_event": [
        "bgp",
        "bgp peer",
        "bgp neighbor",
        "neighbor state",
        "established",
        "idle",
        "notification",
        "keepalive",
    ],
    "ospf_event": [
        "ospf",
        "adjacency",
        "neighbor",
        "full",
        "init",
        "2way",
        "exstart",
    ],
    "latency": [
        "latency",
        "delay",
        "rtt",
        "response time",
        "slow",
        "high latency",
    ],
    "error": [
        "error",
        "fail",
        "failure",
        "err",
        "critical",
        "crc",
        "collision",
        "dropped",
        "discarded",
    ],
    "security": [
        "auth",
        "authentication",
        "denied",
        "blocked",
        "acl",
        "firewall",
        "intrusion",
        "attack",
        "violation",
    ],
}


# -----------------------------------------------------------------------------
# Data Classes
# -----------------------------------------------------------------------------


@dataclass
class LogEvent:
    """Represents a single parsed log event."""

    timestamp: datetime
    device: str
    message: str
    severity: str = "info"
    event_type: str = "unknown"
    raw_line: str = ""
    log_format: str = "unknown"
    source_file: str = ""
    line_number: int = 0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "device": self.device,
            "message": self.message,
            "severity": self.severity,
            "event_type": self.event_type,
            "log_format": self.log_format,
            "source_file": self.source_file,
            "line_number": self.line_number,
            "metadata": self.metadata,
        }


@dataclass
class Anomaly:
    """Represents a detected anomaly pattern."""

    anomaly_id: str
    anomaly_type: str
    severity: str
    start_time: datetime
    end_time: datetime
    affected_devices: list
    event_count: int
    baseline_value: float = 0.0
    peak_value: float = 0.0
    threshold: float = 0.0
    events: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "anomaly_id": self.anomaly_id,
            "type": self.anomaly_type,
            "severity": self.severity,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": int((self.end_time - self.start_time).total_seconds()),
            "affected_devices": self.affected_devices,
            "event_count": self.event_count,
            "baseline_value": self.baseline_value,
            "peak_value": self.peak_value,
            "threshold_exceeded": self.threshold,
        }


@dataclass
class CorrelationCluster:
    """Represents a group of correlated events."""

    cluster_id: str
    confidence: float
    root_cause_device: str
    events: list
    hypothesis: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "cluster_id": self.cluster_id,
            "correlation_confidence": self.confidence,
            "root_cause_device": self.root_cause_device,
            "events": [
                {"timestamp": e.timestamp.isoformat(), "device": e.device, "message": e.message} for e in self.events
            ],
            "hypothesis": self.hypothesis,
        }


@dataclass
class RootCauseHypothesis:
    """Represents a root cause hypothesis with supporting evidence."""

    hypothesis: str
    confidence: float
    supporting_evidence: list
    recommended_actions: list

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


# -----------------------------------------------------------------------------
# Log Parser
# -----------------------------------------------------------------------------


class LogParser:
    """Parses network device logs in various formats."""

    def __init__(self, default_year: Optional[int] = None):
        self.default_year = default_year or datetime.now().year

    def detect_format(self, line: str) -> Optional[str]:
        """Detect the log format of a line."""
        # Try JSON first
        if line.strip().startswith("{"):
            try:
                json.loads(line)
                return "json"
            except json.JSONDecodeError:
                pass

        # Try each pattern
        for format_name, fmt in LOG_FORMATS.items():
            if fmt["pattern"] is None:
                continue
            if re.match(fmt["pattern"], line):
                return format_name

        return None

    def parse_line(
        self,
        line: str,
        format_name: str,
        source_file: str = "",
        line_number: int = 0,
        device_tz: Optional[timezone] = None,
    ) -> Optional[LogEvent]:
        """Parse a single log line."""
        if not line.strip():
            return None

        if format_name == "json":
            return self._parse_json(line, source_file, line_number, device_tz)

        fmt = LOG_FORMATS.get(format_name)
        if not fmt or not fmt["pattern"]:
            return None

        match = re.match(fmt["pattern"], line)
        if not match:
            return None

        groups = fmt["groups"]
        timestamp_str = match.group(groups["timestamp"])
        message = match.group(groups["message"])

        # Parse timestamp
        timestamp = self._parse_timestamp(timestamp_str, fmt["timestamp_format"], device_tz)
        if not timestamp:
            return None

        # Extract device name
        device = "unknown"
        if "hostname" in groups:
            device = match.group(groups["hostname"])

        # Extract severity
        severity = "info"
        if "severity" in groups:
            sev_num = int(match.group(groups["severity"]))
            severity = self._cisco_severity_to_name(sev_num)
        elif "level" in groups:
            severity = match.group(groups["level"]).lower()

        # Classify event type
        event_type = self._classify_event(message)

        # Build metadata
        metadata = {}
        for key, idx in groups.items():
            if key not in ("timestamp", "message"):
                try:
                    metadata[key] = match.group(idx)
                except (IndexError, TypeError):
                    pass

        return LogEvent(
            timestamp=timestamp,
            device=device,
            message=message,
            severity=severity,
            event_type=event_type,
            raw_line=line,
            log_format=format_name,
            source_file=source_file,
            line_number=line_number,
            metadata=metadata,
        )

    def _parse_json(
        self, line: str, source_file: str, line_number: int, device_tz: Optional[timezone] = None
    ) -> Optional[LogEvent]:
        """Parse a JSON-formatted log line."""
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            return None

        # Extract timestamp
        ts_str = data.get("timestamp") or data.get("time") or data.get("@timestamp")
        if not ts_str:
            return None

        timestamp = self._parse_iso_timestamp(ts_str)
        if not timestamp:
            return None

        return LogEvent(
            timestamp=timestamp,
            device=data.get("device") or data.get("host") or data.get("hostname") or "unknown",
            message=data.get("message") or data.get("msg") or str(data),
            severity=data.get("level") or data.get("severity") or "info",
            event_type=self._classify_event(data.get("message", "")),
            raw_line=line,
            log_format="json",
            source_file=source_file,
            line_number=line_number,
            metadata=data.get("metadata", {}),
        )

    def _parse_timestamp(self, ts_str: str, fmt: str, device_tz: Optional[timezone] = None) -> Optional[datetime]:
        """Parse a timestamp string."""
        # Remove leading asterisk (Cisco format)
        ts_str = ts_str.lstrip("*").strip()

        try:
            dt = datetime.strptime(ts_str, fmt)
            # Add year if not present
            if dt.year == 1900:
                dt = dt.replace(year=self.default_year)
                # If date is in the future, use previous year
                if dt > datetime.now():
                    dt = dt.replace(year=self.default_year - 1)

            # Apply timezone if provided
            if device_tz:
                dt = dt.replace(tzinfo=device_tz)
            else:
                dt = dt.replace(tzinfo=timezone.utc)

            return dt
        except ValueError:
            return None

    def _parse_iso_timestamp(self, ts_str: str) -> Optional[datetime]:
        """Parse an ISO 8601 timestamp."""
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(ts_str, fmt)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except ValueError:
                continue

        return None

    def _cisco_severity_to_name(self, level: int) -> str:
        """Convert Cisco severity level to name."""
        levels = {
            0: "emergency",
            1: "alert",
            2: "critical",
            3: "error",
            4: "warning",
            5: "notice",
            6: "info",
            7: "debug",
        }
        return levels.get(level, "info")

    def _classify_event(self, message: str) -> str:
        """Classify an event based on message keywords."""
        message_lower = message.lower()
        for event_type, keywords in EVENT_KEYWORDS.items():
            if any(kw in message_lower for kw in keywords):
                return event_type
        return "unknown"


# -----------------------------------------------------------------------------
# Anomaly Detector
# -----------------------------------------------------------------------------


class AnomalyDetector:
    """Detects anomaly patterns in parsed log events."""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or self._default_config()
        self.anomaly_counter = 0

    def _default_config(self) -> dict:
        """Return default anomaly detection configuration."""
        return {
            "connection_failure": {
                "spike_threshold": 50,
                "window_seconds": 60,
                "severity_multipliers": {"warning": 2, "error": 3, "critical": 5},
            },
            "interface_flapping": {
                "state_change_threshold": 3,
                "window_seconds": 300,
            },
            "error_rate": {
                "baseline_multiplier": 3,
                "baseline_window_seconds": 300,
            },
            "correlation": {
                "same_device_window_seconds": 5,
                "adjacent_device_window_seconds": 30,
                "network_wide_window_seconds": 60,
            },
        }

    def detect_anomalies(self, events: list[LogEvent]) -> list[Anomaly]:
        """Detect all anomaly patterns in the events."""
        anomalies = []

        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Detect connection failure spikes
        anomalies.extend(self._detect_connection_failures(sorted_events))

        # Detect interface flapping
        anomalies.extend(self._detect_interface_flapping(sorted_events))

        # Detect error rate spikes
        anomalies.extend(self._detect_error_spikes(sorted_events))

        return anomalies

    def _generate_anomaly_id(self) -> str:
        """Generate a unique anomaly ID."""
        self.anomaly_counter += 1
        return f"ANO-{datetime.now().strftime('%Y%m%d')}{self.anomaly_counter:05d}"

    def _detect_connection_failures(self, events: list[LogEvent]) -> list[Anomaly]:
        """Detect connection failure spike anomalies."""
        anomalies = []
        config = self.config["connection_failure"]
        window = timedelta(seconds=config["window_seconds"])

        # Filter connection failure events
        failure_events = [e for e in events if e.event_type == "connection_failure"]
        if not failure_events:
            return anomalies

        # Sliding window detection
        window_start = 0
        for i, event in enumerate(failure_events):
            # Move window start
            while window_start < i and event.timestamp - failure_events[window_start].timestamp > window:
                window_start += 1

            window_events = failure_events[window_start : i + 1]
            if len(window_events) >= config["spike_threshold"]:
                # Determine severity
                count = len(window_events)
                if count >= config["spike_threshold"] * config["severity_multipliers"]["critical"]:
                    severity = "critical"
                elif count >= config["spike_threshold"] * config["severity_multipliers"]["error"]:
                    severity = "error"
                else:
                    severity = "warning"

                affected_devices = list(set(e.device for e in window_events))

                anomalies.append(
                    Anomaly(
                        anomaly_id=self._generate_anomaly_id(),
                        anomaly_type="connection_failure_spike",
                        severity=severity,
                        start_time=window_events[0].timestamp,
                        end_time=window_events[-1].timestamp,
                        affected_devices=affected_devices,
                        event_count=count,
                        threshold=config["spike_threshold"],
                        peak_value=count,
                        events=window_events,
                    )
                )

        return self._deduplicate_anomalies(anomalies)

    def _detect_interface_flapping(self, events: list[LogEvent]) -> list[Anomaly]:
        """Detect interface flapping anomalies."""
        anomalies = []
        config = self.config["interface_flapping"]
        window = timedelta(seconds=config["window_seconds"])

        # Filter interface state events
        interface_events = [e for e in events if e.event_type == "interface_state"]
        if not interface_events:
            return anomalies

        # Group by device
        by_device: dict[str, list] = defaultdict(list)
        for event in interface_events:
            by_device[event.device].append(event)

        for device, device_events in by_device.items():
            # Sliding window detection
            window_start = 0
            for i, event in enumerate(device_events):
                while window_start < i and event.timestamp - device_events[window_start].timestamp > window:
                    window_start += 1

                window_events = device_events[window_start : i + 1]
                if len(window_events) >= config["state_change_threshold"]:
                    anomalies.append(
                        Anomaly(
                            anomaly_id=self._generate_anomaly_id(),
                            anomaly_type="interface_flapping",
                            severity="critical",
                            start_time=window_events[0].timestamp,
                            end_time=window_events[-1].timestamp,
                            affected_devices=[device],
                            event_count=len(window_events),
                            threshold=config["state_change_threshold"],
                            events=window_events,
                        )
                    )

        return self._deduplicate_anomalies(anomalies)

    def _detect_error_spikes(self, events: list[LogEvent]) -> list[Anomaly]:
        """Detect error rate spike anomalies."""
        anomalies = []
        config = self.config["error_rate"]
        window = timedelta(seconds=config["baseline_window_seconds"])

        # Filter error events
        error_events = [e for e in events if e.event_type == "error"]
        if len(error_events) < 10:  # Need enough events for baseline
            return anomalies

        # Calculate baseline
        total_duration = (error_events[-1].timestamp - error_events[0].timestamp).total_seconds()
        if total_duration <= 0:
            return anomalies

        baseline_rate = len(error_events) / (total_duration / 60)  # per minute

        # Sliding window detection
        window_start = 0
        for i, event in enumerate(error_events):
            while window_start < i and event.timestamp - error_events[window_start].timestamp > window:
                window_start += 1

            window_events = error_events[window_start : i + 1]
            window_duration = (window_events[-1].timestamp - window_events[0].timestamp).total_seconds()
            if window_duration <= 0:
                continue

            window_rate = len(window_events) / (window_duration / 60)

            if window_rate >= baseline_rate * config["baseline_multiplier"]:
                affected_devices = list(set(e.device for e in window_events))
                anomalies.append(
                    Anomaly(
                        anomaly_id=self._generate_anomaly_id(),
                        anomaly_type="error_rate_spike",
                        severity="error",
                        start_time=window_events[0].timestamp,
                        end_time=window_events[-1].timestamp,
                        affected_devices=affected_devices,
                        event_count=len(window_events),
                        baseline_value=baseline_rate,
                        peak_value=window_rate,
                        threshold=baseline_rate * config["baseline_multiplier"],
                        events=window_events,
                    )
                )

        return self._deduplicate_anomalies(anomalies)

    def _deduplicate_anomalies(self, anomalies: list[Anomaly]) -> list[Anomaly]:
        """Remove overlapping anomalies, keeping the most severe."""
        if not anomalies:
            return anomalies

        # Sort by start time
        sorted_anomalies = sorted(anomalies, key=lambda a: a.start_time)

        severity_order = {"critical": 0, "error": 1, "warning": 2, "info": 3}
        result = []

        for anomaly in sorted_anomalies:
            # Check if overlaps with existing
            overlaps = False
            for i, existing in enumerate(result):
                if existing.anomaly_type == anomaly.anomaly_type and existing.end_time >= anomaly.start_time:
                    # Overlapping - keep more severe
                    if severity_order.get(anomaly.severity, 4) < severity_order.get(existing.severity, 4):
                        result[i] = anomaly
                    overlaps = True
                    break

            if not overlaps:
                result.append(anomaly)

        return result


# -----------------------------------------------------------------------------
# Event Correlator
# -----------------------------------------------------------------------------


class EventCorrelator:
    """Correlates events across devices and time."""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {
            "same_device_window_seconds": 5,
            "adjacent_device_window_seconds": 30,
            "network_wide_window_seconds": 60,
        }
        self.cluster_counter = 0

    def correlate_events(self, events: list[LogEvent], anomalies: list[Anomaly]) -> list[CorrelationCluster]:
        """Correlate events into clusters based on temporal proximity."""
        clusters = []

        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Focus on critical event types
        critical_events = [
            e for e in sorted_events if e.event_type in ("bgp_event", "interface_state", "connection_failure")
        ]

        if not critical_events:
            return clusters

        # Sliding window clustering
        window = timedelta(seconds=self.config["network_wide_window_seconds"])
        window_start = 0

        for i, event in enumerate(critical_events):
            while window_start < i and event.timestamp - critical_events[window_start].timestamp > window:
                window_start += 1

            window_events = critical_events[window_start : i + 1]
            if len(window_events) >= 2:
                # Create cluster if multiple devices involved
                devices = set(e.device for e in window_events)
                if len(devices) >= 2:
                    cluster = self._create_cluster(window_events)
                    if cluster:
                        clusters.append(cluster)

        return self._deduplicate_clusters(clusters)

    def _generate_cluster_id(self) -> str:
        """Generate a unique cluster ID."""
        self.cluster_counter += 1
        return f"CLU-{self.cluster_counter:03d}"

    def _create_cluster(self, events: list[LogEvent]) -> Optional[CorrelationCluster]:
        """Create a correlation cluster from events."""
        if len(events) < 2:
            return None

        # Find root cause device (first event's device)
        root_device = events[0].device

        # Calculate confidence based on temporal proximity
        time_span = (events[-1].timestamp - events[0].timestamp).total_seconds()
        confidence = max(0.5, 1.0 - (time_span / 60))  # Higher confidence for tighter clusters

        # Generate hypothesis
        hypothesis = self._generate_hypothesis(events)

        return CorrelationCluster(
            cluster_id=self._generate_cluster_id(),
            confidence=round(confidence, 2),
            root_cause_device=root_device,
            events=events,
            hypothesis=hypothesis,
        )

    def _generate_hypothesis(self, events: list[LogEvent]) -> str:
        """Generate a root cause hypothesis based on event patterns."""
        event_types = [e.event_type for e in events]

        if "bgp_event" in event_types and "connection_failure" in event_types:
            return "BGP session failure triggered connectivity disruption"
        elif "interface_state" in event_types and "connection_failure" in event_types:
            return "Interface state change caused downstream connection failures"
        elif event_types.count("connection_failure") > 3:
            return "Multiple connection failures indicate network segment issue"
        elif "interface_state" in event_types:
            return "Interface state change may indicate physical or configuration issue"
        else:
            return "Correlated network events detected"

    def _deduplicate_clusters(self, clusters: list[CorrelationCluster]) -> list[CorrelationCluster]:
        """Remove duplicate or overlapping clusters."""
        if not clusters:
            return clusters

        # Sort by confidence descending
        sorted_clusters = sorted(clusters, key=lambda c: c.confidence, reverse=True)

        result = []
        seen_events = set()

        for cluster in sorted_clusters:
            # Check if events already in another cluster
            event_ids = tuple((e.timestamp, e.device, e.message) for e in cluster.events)
            if not any(eid in seen_events for eid in event_ids):
                result.append(cluster)
                seen_events.update(event_ids)

        return result


# -----------------------------------------------------------------------------
# Root Cause Analyzer
# -----------------------------------------------------------------------------


class RootCauseAnalyzer:
    """Generates root cause hypotheses from anomalies and correlations."""

    def analyze(self, anomalies: list[Anomaly], clusters: list[CorrelationCluster]) -> list[RootCauseHypothesis]:
        """Generate root cause hypotheses."""
        hypotheses = []

        # Analyze anomaly patterns
        for anomaly in anomalies:
            hypothesis = self._analyze_anomaly(anomaly)
            if hypothesis:
                hypotheses.append(hypothesis)

        # Analyze correlation clusters
        for cluster in clusters:
            hypothesis = self._analyze_cluster(cluster)
            if hypothesis:
                hypotheses.append(hypothesis)

        # Deduplicate and rank
        return self._rank_hypotheses(hypotheses)

    def _analyze_anomaly(self, anomaly: Anomaly) -> Optional[RootCauseHypothesis]:
        """Generate hypothesis from an anomaly."""
        if anomaly.anomaly_type == "connection_failure_spike":
            return RootCauseHypothesis(
                hypothesis="Network connectivity disruption caused connection failure spike",
                confidence=0.7,
                supporting_evidence=[
                    f"{anomaly.event_count} connection failures in {anomaly.affected_devices}",
                    f"Peak rate exceeded baseline by {anomaly.peak_value / max(anomaly.baseline_value, 1):.1f}x",
                ],
                recommended_actions=[
                    "Check physical connectivity and interface status",
                    "Verify routing table entries",
                    "Review firewall and ACL configurations",
                ],
            )
        elif anomaly.anomaly_type == "interface_flapping":
            return RootCauseHypothesis(
                hypothesis="Interface instability causing network disruption",
                confidence=0.85,
                supporting_evidence=[
                    f"Interface flapped {anomaly.event_count} times on {anomaly.affected_devices}",
                ],
                recommended_actions=[
                    "Check physical cable and port connections",
                    "Verify duplex and speed settings",
                    "Review interface error counters",
                    "Check for power issues on connected devices",
                ],
            )
        elif anomaly.anomaly_type == "error_rate_spike":
            return RootCauseHypothesis(
                hypothesis="Elevated error rate indicates hardware or configuration issue",
                confidence=0.65,
                supporting_evidence=[
                    f"Error rate {anomaly.peak_value:.1f}/min exceeded baseline {anomaly.baseline_value:.1f}/min",
                ],
                recommended_actions=[
                    "Review interface error counters (CRC, frame, collision)",
                    "Check for buffer overruns",
                    "Verify MTU settings across the path",
                ],
            )

        return None

    def _analyze_cluster(self, cluster: CorrelationCluster) -> Optional[RootCauseHypothesis]:
        """Generate hypothesis from a correlation cluster."""
        if cluster.confidence < 0.6:
            return None

        event_types = set(e.event_type for e in cluster.events)

        if "bgp_event" in event_types:
            return RootCauseHypothesis(
                hypothesis=cluster.hypothesis,
                confidence=cluster.confidence,
                supporting_evidence=[
                    f"BGP event on {cluster.root_cause_device} preceded {len(cluster.events) - 1} related events",
                    f"Events correlated within {(cluster.events[-1].timestamp - cluster.events[0].timestamp).total_seconds():.0f} seconds",
                ],
                recommended_actions=[
                    "Verify BGP neighbor configuration",
                    "Check upstream provider status",
                    "Review BGP session timers and keepalives",
                ],
            )

        return RootCauseHypothesis(
            hypothesis=cluster.hypothesis,
            confidence=cluster.confidence,
            supporting_evidence=[
                f"{len(cluster.events)} correlated events starting from {cluster.root_cause_device}",
            ],
            recommended_actions=[
                f"Investigate {cluster.root_cause_device} for root cause",
                "Review event logs in chronological order",
            ],
        )

    def _rank_hypotheses(self, hypotheses: list[RootCauseHypothesis]) -> list[RootCauseHypothesis]:
        """Rank and deduplicate hypotheses by confidence."""
        if not hypotheses:
            return hypotheses

        # Sort by confidence descending
        sorted_hypotheses = sorted(hypotheses, key=lambda h: h.confidence, reverse=True)

        # Deduplicate similar hypotheses
        result = []
        seen_hypotheses = set()

        for hypothesis in sorted_hypotheses:
            # Simple deduplication by hypothesis text prefix
            key = hypothesis.hypothesis[:50]
            if key not in seen_hypotheses:
                result.append(hypothesis)
                seen_hypotheses.add(key)

        return result[:5]  # Return top 5


# -----------------------------------------------------------------------------
# Report Generator
# -----------------------------------------------------------------------------


class ReportGenerator:
    """Generates incident reports in JSON and Markdown formats."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_json_report(
        self,
        events: list[LogEvent],
        anomalies: list[Anomaly],
        clusters: list[CorrelationCluster],
        hypotheses: list[RootCauseHypothesis],
        start_time: datetime,
        end_time: datetime,
        log_files: list[str],
    ) -> Path:
        """Generate JSON report."""
        # Summarize log files
        file_summaries = []
        files_events: dict[str, list] = defaultdict(list)
        for event in events:
            files_events[event.source_file].append(event)

        for log_file in log_files:
            file_events = files_events.get(log_file, [])
            if file_events:
                file_summaries.append(
                    {
                        "path": log_file,
                        "events": len(file_events),
                        "format": file_events[0].log_format if file_events else "unknown",
                    }
                )

        report = {
            "schema_version": "1.0",
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "incident_window": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
            },
            "log_files_analyzed": file_summaries,
            "total_events_parsed": len(events),
            "anomalies_detected": [a.to_dict() for a in anomalies],
            "correlated_events": [c.to_dict() for c in clusters],
            "root_cause_hypotheses": [h.to_dict() for h in hypotheses],
        }

        output_path = self.output_dir / "correlated_events.json"
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

        return output_path

    def generate_markdown_report(
        self,
        events: list[LogEvent],
        anomalies: list[Anomaly],
        clusters: list[CorrelationCluster],
        hypotheses: list[RootCauseHypothesis],
        start_time: datetime,
        end_time: datetime,
    ) -> Path:
        """Generate detailed Markdown report."""
        lines = [
            "# Network Incident Root Cause Analysis",
            "",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Incident Window**: {start_time.strftime('%Y-%m-%d %H:%M:%S')} to {end_time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## Executive Summary",
            "",
            f"- **Total Events Analyzed**: {len(events)}",
            f"- **Anomalies Detected**: {len(anomalies)}",
            f"- **Correlated Event Clusters**: {len(clusters)}",
            f"- **Root Cause Hypotheses**: {len(hypotheses)}",
            "",
        ]

        # Anomalies summary
        if anomalies:
            critical = sum(1 for a in anomalies if a.severity == "critical")
            errors = sum(1 for a in anomalies if a.severity == "error")
            lines.extend(
                [
                    "### Severity Breakdown",
                    f"- Critical: {critical}",
                    f"- Error: {errors}",
                    f"- Warning: {len(anomalies) - critical - errors}",
                    "",
                ]
            )

        # Root cause hypotheses
        if hypotheses:
            lines.extend(
                [
                    "## Root Cause Hypotheses",
                    "",
                ]
            )

            for i, hypothesis in enumerate(hypotheses, 1):
                lines.extend(
                    [
                        f"### Hypothesis {i}: {hypothesis.hypothesis}",
                        "",
                        f"**Confidence**: {hypothesis.confidence:.0%}",
                        "",
                        "**Supporting Evidence**:",
                    ]
                )
                for evidence in hypothesis.supporting_evidence:
                    lines.append(f"- {evidence}")

                lines.extend(
                    [
                        "",
                        "**Recommended Actions**:",
                    ]
                )
                for action in hypothesis.recommended_actions:
                    lines.append(f"- {action}")

                lines.append("")

        # Anomaly details
        if anomalies:
            lines.extend(
                [
                    "## Detected Anomalies",
                    "",
                ]
            )

            for anomaly in anomalies:
                duration = (anomaly.end_time - anomaly.start_time).total_seconds()
                lines.extend(
                    [
                        f"### {anomaly.anomaly_id}: {anomaly.anomaly_type}",
                        "",
                        f"- **Severity**: {anomaly.severity.upper()}",
                        f"- **Duration**: {duration:.0f} seconds",
                        f"- **Affected Devices**: {', '.join(anomaly.affected_devices)}",
                        f"- **Event Count**: {anomaly.event_count}",
                        f"- **Start Time**: {anomaly.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
                        f"- **End Time**: {anomaly.end_time.strftime('%Y-%m-%d %H:%M:%S')}",
                        "",
                    ]
                )

        # Correlation clusters
        if clusters:
            lines.extend(
                [
                    "## Event Correlation Clusters",
                    "",
                ]
            )

            for cluster in clusters:
                lines.extend(
                    [
                        f"### {cluster.cluster_id}",
                        "",
                        f"- **Confidence**: {cluster.confidence:.0%}",
                        f"- **Root Cause Device**: {cluster.root_cause_device}",
                        f"- **Hypothesis**: {cluster.hypothesis}",
                        "",
                        "**Correlated Events**:",
                        "",
                    ]
                )

                for event in cluster.events[:10]:  # Limit to 10 events
                    lines.append(f"- `{event.timestamp.strftime('%H:%M:%S')}` [{event.device}] {event.message[:80]}")

                if len(cluster.events) > 10:
                    lines.append(f"- ... and {len(cluster.events) - 10} more events")

                lines.append("")

        # Timeline
        lines.extend(
            [
                "## Incident Timeline",
                "",
                "| Time | Device | Event Type | Message |",
                "|------|--------|------------|---------|",
            ]
        )

        # Show key events (first 20)
        key_events = sorted(events, key=lambda e: e.timestamp)[:20]
        for event in key_events:
            msg = event.message[:50] + "..." if len(event.message) > 50 else event.message
            lines.append(f"| {event.timestamp.strftime('%H:%M:%S')} | {event.device} | {event.event_type} | {msg} |")

        lines.extend(
            [
                "",
                "---",
                "",
                "*Generated by network-incident-analyzer*",
            ]
        )

        output_path = self.output_dir / "root_cause_analysis.md"
        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        return output_path

    def generate_summary(
        self, anomalies: list[Anomaly], hypotheses: list[RootCauseHypothesis], start_time: datetime, end_time: datetime
    ) -> Path:
        """Generate executive summary."""
        duration = end_time - start_time

        lines = [
            "# Incident Summary",
            "",
            "## Impact Assessment",
            "",
            f"- **Incident Duration**: {duration.total_seconds() / 60:.1f} minutes",
            f"- **Anomalies Detected**: {len(anomalies)}",
        ]

        if anomalies:
            all_devices = set()
            for a in anomalies:
                all_devices.update(a.affected_devices)
            lines.append(f"- **Affected Devices**: {', '.join(sorted(all_devices))}")

        lines.extend(
            [
                "",
                "## Primary Root Cause",
                "",
            ]
        )

        if hypotheses:
            top = hypotheses[0]
            lines.extend(
                [
                    f"**{top.hypothesis}** (Confidence: {top.confidence:.0%})",
                    "",
                    "### Evidence",
                ]
            )
            for evidence in top.supporting_evidence:
                lines.append(f"- {evidence}")

            lines.extend(
                [
                    "",
                    "### Immediate Actions Required",
                ]
            )
            for action in top.recommended_actions:
                lines.append(f"1. {action}")
        else:
            lines.append("No definitive root cause identified. Manual investigation recommended.")

        lines.extend(
            [
                "",
                "## Prevention Recommendations",
                "",
                "1. Review monitoring thresholds for early detection",
                "2. Implement redundancy for single points of failure",
                "3. Document incident response procedures",
                "4. Schedule regular configuration backups",
                "",
                "---",
                f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            ]
        )

        output_path = self.output_dir / "incident_summary.md"
        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        return output_path


# -----------------------------------------------------------------------------
# Main Analyzer
# -----------------------------------------------------------------------------


class NetworkIncidentAnalyzer:
    """Main orchestrator for network incident analysis."""

    def __init__(self, output_dir: Path, config: Optional[dict] = None):
        self.parser = LogParser()
        self.detector = AnomalyDetector(config)
        self.correlator = EventCorrelator(config.get("correlation") if config else None)
        self.rca = RootCauseAnalyzer()
        self.reporter = ReportGenerator(output_dir)

    def analyze(
        self, log_files: list[str], start_time: datetime, end_time: datetime, device_tz: Optional[timezone] = None
    ) -> dict:
        """Run full analysis pipeline."""
        # Parse all log files
        all_events = []
        for log_file in log_files:
            events = self._parse_file(log_file, device_tz)
            all_events.extend(events)

        # Filter to time window
        filtered_events = [e for e in all_events if start_time <= e.timestamp <= end_time]

        if not filtered_events:
            print("Warning: No events found in time window", file=sys.stderr)

        # Detect anomalies
        anomalies = self.detector.detect_anomalies(filtered_events)

        # Correlate events
        clusters = self.correlator.correlate_events(filtered_events, anomalies)

        # Generate hypotheses
        hypotheses = self.rca.analyze(anomalies, clusters)

        # Generate reports
        json_path = self.reporter.generate_json_report(
            filtered_events, anomalies, clusters, hypotheses, start_time, end_time, log_files
        )
        md_path = self.reporter.generate_markdown_report(
            filtered_events, anomalies, clusters, hypotheses, start_time, end_time
        )
        summary_path = self.reporter.generate_summary(anomalies, hypotheses, start_time, end_time)

        return {
            "events_parsed": len(all_events),
            "events_in_window": len(filtered_events),
            "anomalies_detected": len(anomalies),
            "clusters_found": len(clusters),
            "hypotheses_generated": len(hypotheses),
            "reports": {
                "json": str(json_path),
                "analysis": str(md_path),
                "summary": str(summary_path),
            },
        }

    def _parse_file(self, log_file: str, device_tz: Optional[timezone] = None) -> list[LogEvent]:
        """Parse a single log file."""
        events = []
        path = Path(log_file)

        if not path.exists():
            print(f"Warning: File not found: {log_file}", file=sys.stderr)
            return events

        detected_format = None

        with open(path, "r", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                # Detect format from first non-empty line
                if detected_format is None:
                    detected_format = self.parser.detect_format(line)
                    if detected_format is None:
                        print(f"Warning: Could not detect format for {log_file}", file=sys.stderr)
                        return events

                event = self.parser.parse_line(line, detected_format, str(path), line_num, device_tz)
                if event:
                    events.append(event)

        return events


# -----------------------------------------------------------------------------
# CLI Entry Point
# -----------------------------------------------------------------------------


def parse_datetime(dt_str: str) -> datetime:
    """Parse a datetime string."""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    raise ValueError(f"Cannot parse datetime: {dt_str}")


def main():
    parser = argparse.ArgumentParser(description="Analyze network device logs to identify incidents and root causes")
    parser.add_argument("--logs", "-l", nargs="+", required=True, help="Log file paths to analyze")
    parser.add_argument("--start", "-s", required=True, help="Start time for analysis window (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--end", "-e", required=True, help="End time for analysis window (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--timezone", "-tz", default="UTC", help="Timezone for log timestamps (default: UTC)")
    parser.add_argument(
        "--output-dir",
        "-o",
        default="./incident-report",
        help="Output directory for reports (default: ./incident-report)",
    )
    parser.add_argument("--config", "-c", help="Path to JSON configuration file for thresholds")

    args = parser.parse_args()

    # Parse time window
    try:
        start_time = parse_datetime(args.start)
        end_time = parse_datetime(args.end)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if start_time >= end_time:
        print("Error: Start time must be before end time", file=sys.stderr)
        sys.exit(1)

    # Load config if provided
    config = None
    if args.config:
        config_path = Path(args.config)
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)

    # Run analysis
    output_dir = Path(args.output_dir)
    analyzer = NetworkIncidentAnalyzer(output_dir, config)

    print(f"Analyzing {len(args.logs)} log file(s)...")
    print(f"Time window: {start_time} to {end_time}")

    results = analyzer.analyze(args.logs, start_time, end_time)

    print("\n=== Analysis Complete ===")
    print(f"Events parsed: {results['events_parsed']}")
    print(f"Events in window: {results['events_in_window']}")
    print(f"Anomalies detected: {results['anomalies_detected']}")
    print(f"Correlation clusters: {results['clusters_found']}")
    print(f"Root cause hypotheses: {results['hypotheses_generated']}")
    print("\nReports generated:")
    for name, path in results["reports"].items():
        print(f"  - {name}: {path}")


if __name__ == "__main__":
    main()
