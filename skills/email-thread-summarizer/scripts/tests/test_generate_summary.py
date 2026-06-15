"""
Tests for generate_summary.py
"""

from datetime import datetime

import pytest
from generate_summary import (
    format_date,
    format_short_date,
    generate_summary,
    get_status_emoji,
)


class TestFormatDate:
    """Tests for date formatting functions."""

    def test_format_iso_date(self):
        """Test formatting ISO8601 date."""
        result = format_date("2024-06-10T14:30:00Z")
        assert "2024-06-10" in result
        assert "14:30" in result

    def test_format_date_only(self):
        """Test formatting date-only string."""
        result = format_date("2024-06-10")
        assert "2024-06-10" in result

    def test_format_empty_date(self):
        """Test formatting empty date."""
        result = format_date("")
        assert result == "N/A"

    def test_format_none_date(self):
        """Test formatting None date."""
        result = format_date(None)
        assert result == "N/A"

    def test_format_short_date(self):
        """Test short date formatting."""
        result = format_short_date("2024-06-10T14:30:00Z")
        assert result == "2024-06-10"


class TestGetStatusEmoji:
    """Tests for status emoji function."""

    def test_active_emoji(self):
        """Test active status emoji."""
        assert get_status_emoji("active") == "🟢"

    def test_resolved_emoji(self):
        """Test resolved status emoji."""
        assert get_status_emoji("resolved") == "✅"

    def test_stale_emoji(self):
        """Test stale status emoji."""
        assert get_status_emoji("stale") == "🟡"

    def test_escalated_emoji(self):
        """Test escalated status emoji."""
        assert get_status_emoji("escalated") == "🔴"

    def test_awaiting_response_emoji(self):
        """Test awaiting response status emoji."""
        assert get_status_emoji("awaiting_response") == "⏳"

    def test_unknown_emoji(self):
        """Test unknown status emoji."""
        assert get_status_emoji("something_else") == "❓"


class TestGenerateSummary:
    """Tests for summary generation."""

    @pytest.fixture
    def sample_analysis(self):
        """Sample analysis data for testing."""
        return {
            "schema_version": "1.0",
            "thread_id": "thread123",
            "subject": "Project Update Discussion",
            "participants": [
                {"name": "Alice Smith", "email": "alice@example.com", "role": "initiator"},
                {"name": "Bob Jones", "email": "bob@example.com", "role": "responder"},
                {"name": "Carol Lee", "email": "carol@example.com", "role": "cc"},
            ],
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
            "timeline": [
                {
                    "date": "2024-06-10T10:00:00Z",
                    "actor": "Alice Smith",
                    "event_type": "request",
                    "summary": "Initial project discussion request",
                },
                {
                    "date": "2024-06-12T14:00:00Z",
                    "actor": "Bob Jones",
                    "event_type": "response",
                    "summary": "Provided initial feedback",
                },
                {
                    "date": "2024-06-15T16:00:00Z",
                    "actor": "Alice Smith",
                    "event_type": "decision",
                    "summary": "Decided to proceed with option A",
                },
            ],
            "action_items": [
                {
                    "id": "AI-001",
                    "description": "Review the updated proposal",
                    "owner": "Bob Jones",
                    "status": "pending",
                    "due_date": "2024-06-20",
                    "source_message_date": "2024-06-15T16:00:00Z",
                },
                {
                    "id": "AI-002",
                    "description": "Send budget estimates",
                    "owner": "Carol Lee",
                    "status": "completed",
                    "due_date": None,
                    "source_message_date": "2024-06-12T14:00:00Z",
                },
            ],
            "key_decisions": [
                {
                    "date": "2024-06-15T16:00:00Z",
                    "decision": "Proceed with option A for the project implementation",
                    "made_by": "Alice Smith",
                }
            ],
            "outdated_info": [
                {
                    "original_statement": "Budget is $5000",
                    "stated_date": "2024-06-10T10:00:00Z",
                    "superseded_by": "Budget increased to $7000",
                    "superseded_date": "2024-06-14T11:00:00Z",
                }
            ],
            "analysis_timestamp": "2024-06-17T10:00:00Z",
        }

    def test_summary_has_header(self, sample_analysis):
        """Test that summary has proper header."""
        summary = generate_summary(sample_analysis)

        assert "# Email Thread Summary" in summary
        assert "Project Update Discussion" in summary

    def test_summary_has_status(self, sample_analysis):
        """Test that summary includes status information."""
        summary = generate_summary(sample_analysis)

        assert "Status" in summary
        assert "Active" in summary
        assert "🟢" in summary

    def test_summary_has_participants(self, sample_analysis):
        """Test that summary lists participants."""
        summary = generate_summary(sample_analysis)

        assert "Participants" in summary
        assert "Alice Smith" in summary
        assert "Initiator" in summary

    def test_summary_has_timeline(self, sample_analysis):
        """Test that summary includes timeline."""
        summary = generate_summary(sample_analysis)

        assert "Timeline" in summary
        assert "2024-06-10" in summary
        assert "Alice Smith" in summary

    def test_summary_has_action_items(self, sample_analysis):
        """Test that summary includes action items."""
        summary = generate_summary(sample_analysis)

        assert "Pending Action Items" in summary
        assert "AI-001" in summary
        assert "Bob Jones" in summary

    def test_summary_has_decisions(self, sample_analysis):
        """Test that summary includes decisions."""
        summary = generate_summary(sample_analysis)

        assert "Key Decisions" in summary
        assert "option A" in summary

    def test_summary_has_outdated_info(self, sample_analysis):
        """Test that summary includes outdated information."""
        summary = generate_summary(sample_analysis)

        assert "Outdated Information" in summary
        assert "$5000" in summary or "Budget" in summary

    def test_summary_has_footer(self, sample_analysis):
        """Test that summary has footer with timestamp."""
        summary = generate_summary(sample_analysis)

        assert "Generated:" in summary

    def test_resolved_status_description(self, sample_analysis):
        """Test resolved status generates appropriate description."""
        sample_analysis["status"]["classification"] = "resolved"
        summary = generate_summary(sample_analysis)

        assert "resolved" in summary.lower()
        assert "✅" in summary

    def test_empty_analysis(self):
        """Test handling of minimal analysis data."""
        minimal = {
            "schema_version": "1.0",
            "thread_id": "",
            "subject": "",
            "participants": [],
            "message_count": 0,
            "status": {
                "classification": "unknown",
                "confidence": 0,
                "last_action_date": "",
                "days_since_last_action": 0,
            },
            "timeline": [],
            "action_items": [],
            "key_decisions": [],
            "outdated_info": [],
            "analysis_timestamp": "",
        }

        summary = generate_summary(minimal)

        # Should still generate valid markdown
        assert "# Email Thread Summary" in summary

    def test_many_participants_truncated(self, sample_analysis):
        """Test that many participants are truncated."""
        # Add many responders
        for i in range(10):
            sample_analysis["participants"].append(
                {"name": f"User{i}", "email": f"user{i}@example.com", "role": "responder"}
            )

        summary = generate_summary(sample_analysis)

        # Should show truncation indicator
        assert "more" in summary.lower()
