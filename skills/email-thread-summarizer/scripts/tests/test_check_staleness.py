"""
Tests for check_staleness.py
"""

from datetime import datetime, timezone

import pytest
from check_staleness import (
    check_staleness,
    compare_action_items,
    compare_date_ranges,
    compare_decisions,
    compare_message_counts,
    compare_status,
    determine_recommendation,
)


@pytest.fixture
def cached_analysis():
    """Sample cached analysis."""
    return {
        "schema_version": "1.0",
        "thread_id": "thread123",
        "message_count": 5,
        "date_range": {
            "first_message": "2024-06-10T10:00:00Z",
            "last_message": "2024-06-15T16:00:00Z",
            "duration_days": 5,
        },
        "status": {
            "classification": "active",
            "confidence": 0.85,
            "last_action_date": "2024-06-15T16:00:00Z",
            "days_since_last_action": 2,
        },
        "action_items": [{"id": "AI-001", "description": "Review the proposal", "owner": "Bob", "status": "pending"}],
        "key_decisions": [{"date": "2024-06-15T16:00:00Z", "decision": "Go with option A", "made_by": "Alice"}],
        "analysis_timestamp": "2024-06-16T10:00:00Z",
    }


@pytest.fixture
def current_analysis():
    """Sample current analysis (same as cached initially)."""
    return {
        "schema_version": "1.0",
        "thread_id": "thread123",
        "message_count": 5,
        "date_range": {
            "first_message": "2024-06-10T10:00:00Z",
            "last_message": "2024-06-15T16:00:00Z",
            "duration_days": 5,
        },
        "status": {
            "classification": "active",
            "confidence": 0.85,
            "last_action_date": "2024-06-15T16:00:00Z",
            "days_since_last_action": 2,
        },
        "action_items": [{"id": "AI-001", "description": "Review the proposal", "owner": "Bob", "status": "pending"}],
        "key_decisions": [{"date": "2024-06-15T16:00:00Z", "decision": "Go with option A", "made_by": "Alice"}],
        "analysis_timestamp": "2024-06-17T10:00:00Z",
    }


class TestCompareMessageCounts:
    """Tests for message count comparison."""

    def test_no_new_messages(self, cached_analysis, current_analysis):
        """Test when message counts are the same."""
        reasons = compare_message_counts(cached_analysis, current_analysis)
        assert len(reasons) == 0

    def test_one_new_message(self, cached_analysis, current_analysis):
        """Test detecting one new message."""
        current_analysis["message_count"] = 6

        reasons = compare_message_counts(cached_analysis, current_analysis)

        assert len(reasons) == 1
        assert reasons[0]["type"] == "new_messages"
        assert "1 new message" in reasons[0]["description"]
        assert reasons[0]["severity"] == "medium"

    def test_many_new_messages(self, cached_analysis, current_analysis):
        """Test detecting multiple new messages."""
        current_analysis["message_count"] = 10

        reasons = compare_message_counts(cached_analysis, current_analysis)

        assert len(reasons) == 1
        assert "5 new message" in reasons[0]["description"]
        assert reasons[0]["severity"] == "high"


class TestCompareStatus:
    """Tests for status comparison."""

    def test_no_status_change(self, cached_analysis, current_analysis):
        """Test when status is unchanged."""
        reasons = compare_status(cached_analysis, current_analysis)
        assert len(reasons) == 0

    def test_active_to_resolved(self, cached_analysis, current_analysis):
        """Test detecting resolution."""
        current_analysis["status"]["classification"] = "resolved"

        reasons = compare_status(cached_analysis, current_analysis)

        assert len(reasons) == 1
        assert reasons[0]["type"] == "status_change"
        assert "resolved" in reasons[0]["description"]
        assert reasons[0]["severity"] == "high"

    def test_active_to_escalated(self, cached_analysis, current_analysis):
        """Test detecting escalation."""
        current_analysis["status"]["classification"] = "escalated"

        reasons = compare_status(cached_analysis, current_analysis)

        assert len(reasons) == 1
        assert reasons[0]["severity"] == "high"

    def test_active_to_stale(self, cached_analysis, current_analysis):
        """Test detecting stale status."""
        current_analysis["status"]["classification"] = "stale"

        reasons = compare_status(cached_analysis, current_analysis)

        assert len(reasons) == 1
        assert reasons[0]["severity"] == "medium"


class TestCompareActionItems:
    """Tests for action item comparison."""

    def test_no_new_items(self, cached_analysis, current_analysis):
        """Test when action items are unchanged."""
        reasons = compare_action_items(cached_analysis, current_analysis)
        assert len(reasons) == 0

    def test_new_action_item(self, cached_analysis, current_analysis):
        """Test detecting new action item."""
        current_analysis["action_items"].append(
            {"id": "AI-002", "description": "Send report", "owner": "Carol", "status": "pending"}
        )

        reasons = compare_action_items(cached_analysis, current_analysis)

        assert len(reasons) >= 1
        assert any(r["type"] == "action_item_update" for r in reasons)

    def test_action_item_status_change(self, cached_analysis, current_analysis):
        """Test detecting action item status change."""
        current_analysis["action_items"][0]["status"] = "completed"

        reasons = compare_action_items(cached_analysis, current_analysis)

        assert len(reasons) >= 1
        assert any("changed status" in r["description"] for r in reasons)


class TestCompareDecisions:
    """Tests for decision comparison."""

    def test_no_new_decisions(self, cached_analysis, current_analysis):
        """Test when decisions are unchanged."""
        reasons = compare_decisions(cached_analysis, current_analysis)
        assert len(reasons) == 0

    def test_new_decision(self, cached_analysis, current_analysis):
        """Test detecting new decision."""
        current_analysis["key_decisions"].append(
            {"date": "2024-06-17T10:00:00Z", "decision": "Increased budget", "made_by": "Manager"}
        )

        reasons = compare_decisions(cached_analysis, current_analysis)

        assert len(reasons) == 1
        assert reasons[0]["type"] == "decision_change"
        assert "1 new decision" in reasons[0]["description"]


class TestCompareDateRanges:
    """Tests for date range comparison."""

    def test_no_new_messages_by_date(self, cached_analysis, current_analysis):
        """Test when last message dates are the same."""
        new_messages = compare_date_ranges(cached_analysis, current_analysis)
        assert new_messages == 0

    def test_newer_messages_detected(self, cached_analysis, current_analysis):
        """Test detecting newer messages by date."""
        current_analysis["date_range"]["last_message"] = "2024-06-18T10:00:00Z"
        current_analysis["message_count"] = 8

        new_messages = compare_date_ranges(cached_analysis, current_analysis)
        assert new_messages == 3


class TestDetermineRecommendation:
    """Tests for recommendation determination."""

    def test_no_reasons_ignore(self):
        """Test no reasons returns ignore."""
        recommendation = determine_recommendation([], 0)
        assert recommendation == "ignore"

    def test_high_severity_refresh(self):
        """Test high severity returns refresh."""
        reasons = [{"severity": "high", "type": "status_change"}]
        recommendation = determine_recommendation(reasons, 0)
        assert recommendation == "refresh"

    def test_many_new_messages_refresh(self):
        """Test many new messages returns refresh."""
        reasons = [{"severity": "low", "type": "new_messages"}]
        recommendation = determine_recommendation(reasons, 5)
        assert recommendation == "refresh"

    def test_medium_severity_review(self):
        """Test medium severity returns review."""
        reasons = [{"severity": "medium", "type": "action_item_update"}]
        recommendation = determine_recommendation(reasons, 0)
        assert recommendation == "review"

    def test_low_severity_only_ignore(self):
        """Test low severity only returns ignore."""
        reasons = [{"severity": "low", "type": "something"}]
        recommendation = determine_recommendation(reasons, 0)
        assert recommendation == "ignore"


class TestCheckStaleness:
    """Tests for full staleness check."""

    def test_not_stale_when_identical(self, cached_analysis, current_analysis):
        """Test identical analyses are not stale."""
        report = check_staleness(cached_analysis, current_analysis)

        assert report["is_stale"] is False
        assert len(report["staleness_reasons"]) == 0
        assert report["recommendation"] == "ignore"

    def test_stale_with_new_messages(self, cached_analysis, current_analysis):
        """Test staleness detected with new messages."""
        current_analysis["message_count"] = 8
        current_analysis["date_range"]["last_message"] = "2024-06-18T10:00:00Z"

        report = check_staleness(cached_analysis, current_analysis)

        assert report["is_stale"] is True
        assert report["new_messages_since_cache"] == 3
        assert report["recommendation"] in ["review", "refresh"]

    def test_stale_with_status_change(self, cached_analysis, current_analysis):
        """Test staleness detected with status change."""
        current_analysis["status"]["classification"] = "resolved"

        report = check_staleness(cached_analysis, current_analysis)

        assert report["is_stale"] is True
        assert any(r["type"] == "status_change" for r in report["staleness_reasons"])
        assert report["recommendation"] == "refresh"

    def test_report_schema_version(self, cached_analysis, current_analysis):
        """Test report has correct schema version."""
        report = check_staleness(cached_analysis, current_analysis)
        assert report["schema_version"] == "1.0"

    def test_report_has_dates(self, cached_analysis, current_analysis):
        """Test report includes date information."""
        report = check_staleness(cached_analysis, current_analysis)

        assert "cached_summary_date" in report
        assert "current_thread_date" in report

    def test_multiple_staleness_reasons(self, cached_analysis, current_analysis):
        """Test detecting multiple staleness reasons."""
        current_analysis["message_count"] = 8
        current_analysis["status"]["classification"] = "escalated"
        current_analysis["key_decisions"].append(
            {"date": "2024-06-17T10:00:00Z", "decision": "New decision", "made_by": "VP"}
        )

        report = check_staleness(cached_analysis, current_analysis)

        assert report["is_stale"] is True
        assert len(report["staleness_reasons"]) >= 2
        assert report["recommendation"] == "refresh"
