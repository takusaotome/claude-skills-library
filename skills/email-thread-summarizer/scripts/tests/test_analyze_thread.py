"""
Tests for analyze_thread.py
"""

import json
from datetime import datetime, timezone

import pytest
from analyze_thread import (
    ActionItem,
    Participant,
    analyze_thread,
    classify_thread_status,
    detect_superseded_info,
    extract_action_items,
    extract_decisions,
    extract_participants,
    parse_gmail_json,
    parse_outlook_json,
)


@pytest.fixture
def sample_gmail_message():
    """Sample Gmail JSON message."""
    return {
        "id": "msg123",
        "threadId": "thread456",
        "payload": {
            "headers": [
                {"name": "Subject", "value": "Project Update"},
                {"name": "From", "value": "Alice Smith <alice@example.com>"},
                {"name": "To", "value": "Bob Jones <bob@example.com>"},
                {"name": "Cc", "value": "Carol Lee <carol@example.com>"},
                {"name": "Date", "value": "Mon, 10 Jun 2024 10:00:00 +0000"},
            ],
            "body": {
                "data": "SGVsbG8gQm9iLCBjYW4geW91IHJldmlldyB0aGUgZG9jdW1lbnQgYnkgRnJpZGF5Pw=="  # "Hello Bob, can you review the document by Friday?"
            },
        },
    }


@pytest.fixture
def sample_outlook_message():
    """Sample Outlook/Graph API JSON message."""
    return {
        "id": "outlook123",
        "conversationId": "conv456",
        "subject": "Meeting Request",
        "receivedDateTime": "2024-06-11T14:30:00Z",
        "from": {"emailAddress": {"name": "David Chen", "address": "david@example.com"}},
        "toRecipients": [{"emailAddress": {"name": "Eve Wilson", "address": "eve@example.com"}}],
        "ccRecipients": [],
        "body": {"contentType": "text", "content": "I will schedule the meeting for next week."},
    }


@pytest.fixture
def sample_thread_messages():
    """Sample parsed messages for a thread."""
    return [
        {
            "id": "msg1",
            "thread_id": "thread1",
            "date": "2024-06-10T10:00:00Z",
            "from_name": "Alice",
            "from_email": "alice@example.com",
            "to": [{"name": "Bob", "email": "bob@example.com"}],
            "cc": [],
            "subject": "Project Discussion",
            "body": "Hi Bob, can you review the proposal by Friday? Thanks!",
        },
        {
            "id": "msg2",
            "thread_id": "thread1",
            "date": "2024-06-11T09:00:00Z",
            "from_name": "Bob",
            "from_email": "bob@example.com",
            "to": [{"name": "Alice", "email": "alice@example.com"}],
            "cc": [],
            "subject": "Re: Project Discussion",
            "body": "Sure, I will review it by Thursday. Let me know if you need anything else.",
        },
        {
            "id": "msg3",
            "thread_id": "thread1",
            "date": "2024-06-12T15:00:00Z",
            "from_name": "Bob",
            "from_email": "bob@example.com",
            "to": [{"name": "Alice", "email": "alice@example.com"}],
            "cc": [],
            "subject": "Re: Project Discussion",
            "body": "Review completed. The proposal looks good. This is resolved.",
        },
    ]


class TestParseGmailJson:
    """Tests for Gmail JSON parsing."""

    def test_parse_single_message(self, sample_gmail_message):
        """Test parsing a single Gmail message."""
        messages = parse_gmail_json(sample_gmail_message)

        assert len(messages) == 1
        msg = messages[0]
        assert msg["id"] == "msg123"
        assert msg["thread_id"] == "thread456"
        assert msg["subject"] == "Project Update"
        assert msg["from_name"] == "Alice Smith"
        assert msg["from_email"] == "alice@example.com"
        assert len(msg["to"]) == 1
        assert msg["to"][0]["email"] == "bob@example.com"
        assert len(msg["cc"]) == 1
        assert msg["cc"][0]["email"] == "carol@example.com"

    def test_parse_message_list(self, sample_gmail_message):
        """Test parsing a list of Gmail messages."""
        messages = parse_gmail_json([sample_gmail_message, sample_gmail_message])
        assert len(messages) == 2

    def test_parse_messages_dict(self, sample_gmail_message):
        """Test parsing Gmail messages in dict format."""
        messages = parse_gmail_json({"messages": [sample_gmail_message]})
        assert len(messages) == 1


class TestParseOutlookJson:
    """Tests for Outlook JSON parsing."""

    def test_parse_single_message(self, sample_outlook_message):
        """Test parsing a single Outlook message."""
        messages = parse_outlook_json(sample_outlook_message)

        assert len(messages) == 1
        msg = messages[0]
        assert msg["id"] == "outlook123"
        assert msg["thread_id"] == "conv456"
        assert msg["subject"] == "Meeting Request"
        assert msg["from_name"] == "David Chen"
        assert msg["from_email"] == "david@example.com"
        assert len(msg["to"]) == 1
        assert msg["to"][0]["email"] == "eve@example.com"

    def test_parse_value_list(self, sample_outlook_message):
        """Test parsing Outlook messages in Graph API value format."""
        messages = parse_outlook_json({"value": [sample_outlook_message]})
        assert len(messages) == 1


class TestExtractParticipants:
    """Tests for participant extraction."""

    def test_extract_all_participants(self, sample_thread_messages):
        """Test extracting all unique participants."""
        participants = extract_participants(sample_thread_messages)

        emails = {p.email for p in participants}
        assert "alice@example.com" in emails
        assert "bob@example.com" in emails

    def test_initiator_role(self, sample_thread_messages):
        """Test that first sender is marked as initiator."""
        participants = extract_participants(sample_thread_messages)

        alice = next((p for p in participants if p.email == "alice@example.com"), None)
        assert alice is not None
        assert alice.role == "initiator"

    def test_responder_role(self, sample_thread_messages):
        """Test that other senders are marked as responders."""
        participants = extract_participants(sample_thread_messages)

        bob = next((p for p in participants if p.email == "bob@example.com"), None)
        assert bob is not None
        assert bob.role == "responder"


class TestExtractActionItems:
    """Tests for action item extraction."""

    def test_extract_request_action(self, sample_thread_messages):
        """Test extracting action items from request patterns."""
        items = extract_action_items(sample_thread_messages)

        # Should find "can you review the proposal"
        review_items = [i for i in items if "review" in i.description.lower()]
        assert len(review_items) >= 1

    def test_extract_commitment_action(self, sample_thread_messages):
        """Test extracting action items from commitment patterns."""
        items = extract_action_items(sample_thread_messages)

        # Should find "I will review it by Thursday"
        will_items = [i for i in items if "review" in i.description.lower()]
        assert len(will_items) >= 1

    def test_action_item_has_id(self, sample_thread_messages):
        """Test that action items have unique IDs."""
        items = extract_action_items(sample_thread_messages)

        if items:
            ids = [i.id for i in items]
            assert len(ids) == len(set(ids))  # All IDs are unique
            assert all(id.startswith("AI-") for id in ids)


class TestExtractDecisions:
    """Tests for decision extraction."""

    def test_extract_decisions(self):
        """Test extracting decisions from messages."""
        messages = [
            {
                "id": "msg1",
                "date": "2024-06-10T10:00:00Z",
                "from_name": "Alice",
                "from_email": "alice@example.com",
                "body": "We decided to go with vendor A for this project.",
            }
        ]

        decisions = extract_decisions(messages)

        assert len(decisions) >= 1
        assert any("vendor" in d.decision.lower() for d in decisions)


class TestClassifyThreadStatus:
    """Tests for thread status classification."""

    def test_resolved_status(self, sample_thread_messages):
        """Test detecting resolved status."""
        status = classify_thread_status(sample_thread_messages)
        assert status.classification == "resolved"

    def test_active_status(self):
        """Test detecting active status."""
        messages = [
            {
                "id": "msg1",
                "date": datetime.now(timezone.utc).isoformat(),
                "from_name": "Alice",
                "from_email": "alice@example.com",
                "body": "Just checking in on the project.",
            }
        ]

        status = classify_thread_status(messages)
        assert status.classification in ["active", "awaiting_response"]

    def test_escalated_status(self):
        """Test detecting escalated status."""
        messages = [
            {
                "id": "msg1",
                "date": datetime.now(timezone.utc).isoformat(),
                "from_name": "Alice",
                "from_email": "alice@example.com",
                "body": "URGENT: Escalating this to the VP for immediate attention.",
            }
        ]

        status = classify_thread_status(messages)
        assert status.classification == "escalated"

    def test_awaiting_response_status(self):
        """Test detecting awaiting response status."""
        messages = [
            {
                "id": "msg1",
                "date": datetime.now(timezone.utc).isoformat(),
                "from_name": "Alice",
                "from_email": "alice@example.com",
                "body": "Can you please update me on the status?",
            }
        ]

        status = classify_thread_status(messages)
        assert status.classification == "awaiting_response"


class TestDetectSupersededInfo:
    """Tests for superseded information detection."""

    def test_detect_correction(self):
        """Test detecting correction patterns."""
        messages = [
            {"id": "msg1", "date": "2024-06-10T10:00:00Z", "from_name": "Alice", "body": "The meeting is at 2pm."},
            {
                "id": "msg2",
                "date": "2024-06-10T11:00:00Z",
                "from_name": "Alice",
                "body": "Correction: the meeting is at 3pm.",
            },
        ]

        outdated = detect_superseded_info(messages)

        assert len(outdated) >= 1
        assert any("3pm" in o.superseded_by for o in outdated)

    def test_detect_update(self):
        """Test detecting update patterns."""
        messages = [
            {"id": "msg1", "date": "2024-06-10T10:00:00Z", "from_name": "Bob", "body": "Budget is $5000."},
            {
                "id": "msg2",
                "date": "2024-06-10T11:00:00Z",
                "from_name": "Bob",
                "body": "Update: budget has been increased to $7000.",
            },
        ]

        outdated = detect_superseded_info(messages)

        assert len(outdated) >= 1


class TestAnalyzeThread:
    """Tests for complete thread analysis."""

    def test_full_analysis(self, sample_thread_messages):
        """Test complete thread analysis."""
        analysis = analyze_thread(sample_thread_messages)

        assert analysis.schema_version == "1.0"
        assert analysis.subject == "Project Discussion"
        assert analysis.message_count == 3
        assert len(analysis.participants) >= 2
        assert analysis.status is not None
        assert len(analysis.timeline) >= 3
        assert analysis.analysis_timestamp

    def test_empty_thread(self):
        """Test analysis of empty thread."""
        analysis = analyze_thread([])

        assert analysis.message_count == 0
        assert analysis.participants == []

    def test_thread_id_override(self, sample_thread_messages):
        """Test thread ID can be overridden."""
        analysis = analyze_thread(sample_thread_messages, "custom-thread-id")

        assert analysis.thread_id == "custom-thread-id"

    def test_date_range_calculation(self, sample_thread_messages):
        """Test date range is correctly calculated."""
        analysis = analyze_thread(sample_thread_messages)

        assert analysis.date_range is not None
        assert "first_message" in analysis.date_range
        assert "last_message" in analysis.date_range
        assert "duration_days" in analysis.date_range
