"""
Tests for the meeting asset preparer script.
"""

from pathlib import Path

import pytest
from prepare_meeting import (
    AgendaItem,
    Attendee,
    MeetingConfig,
    get_bilingual_text,
)


class TestBilingualText:
    """Tests for bilingual text generation."""

    def test_english_only(self):
        """Test English-only mode returns English text."""
        result = get_bilingual_text("Hello", "こんにちは", "en")
        assert result == "Hello"

    def test_japanese_only(self):
        """Test Japanese-only mode returns Japanese text."""
        result = get_bilingual_text("Hello", "こんにちは", "ja")
        assert result == "こんにちは"

    def test_bilingual_mode(self):
        """Test bilingual mode returns both languages."""
        result = get_bilingual_text("Hello", "こんにちは", "bilingual")
        assert result == "Hello / こんにちは"

    def test_default_to_english(self):
        """Test unknown language defaults to English."""
        result = get_bilingual_text("Hello", "こんにちは", "unknown")
        assert result == "Hello"


class TestMeetingConfig:
    """Tests for MeetingConfig dataclass."""

    def test_basic_creation(self):
        """Test basic MeetingConfig creation."""
        config = MeetingConfig(
            title="Test Meeting",
            date="2026-03-15",
            time="14:00",
            timezone="JST",
        )
        assert config.title == "Test Meeting"
        assert config.date == "2026-03-15"
        assert config.time == "14:00"
        assert config.timezone == "JST"
        assert config.duration_minutes == 60  # default
        assert config.language == "en"  # default

    def test_with_attendees(self):
        """Test MeetingConfig with attendees."""
        attendees = [
            Attendee(name="Alice", role="Product Owner"),
            Attendee(name="Bob", role="Developer"),
        ]
        config = MeetingConfig(
            title="Sprint Review",
            date="2026-03-15",
            time="14:00",
            attendees=attendees,
        )
        assert len(config.attendees) == 2
        assert config.attendees[0].name == "Alice"
        assert config.attendees[0].role == "Product Owner"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = MeetingConfig(
            title="Test Meeting",
            date="2026-03-15",
            time="14:00",
            timezone="JST",
            duration_minutes=90,
            language="bilingual",
            objectives=["Review progress", "Plan next steps"],
        )
        result = config.to_dict()

        assert "meeting" in result
        meeting = result["meeting"]
        assert meeting["title"] == "Test Meeting"
        assert meeting["date"] == "2026-03-15"
        assert meeting["time"] == "14:00"
        assert meeting["timezone"] == "JST"
        assert meeting["duration_minutes"] == 90
        assert meeting["language"] == "bilingual"
        assert len(meeting["objectives"]) == 2

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "meeting": {
                "title": "Loaded Meeting",
                "date": "2026-04-01",
                "time": "10:00",
                "timezone": "EST",
                "duration_minutes": 45,
                "language": "ja",
                "attendees": [
                    {"name": "Carol", "role": "Manager"},
                ],
                "objectives": ["Discuss budget"],
            }
        }
        config = MeetingConfig.from_dict(data)

        assert config.title == "Loaded Meeting"
        assert config.date == "2026-04-01"
        assert config.time == "10:00"
        assert config.timezone == "EST"
        assert config.duration_minutes == 45
        assert config.language == "ja"
        assert len(config.attendees) == 1
        assert config.attendees[0].name == "Carol"
        assert config.attendees[0].role == "Manager"

    def test_from_dict_with_simple_attendees(self):
        """Test creation from dictionary with simple attendee strings."""
        data = {
            "meeting": {
                "title": "Simple Meeting",
                "date": "2026-04-01",
                "time": "10:00",
                "attendees": ["Alice", "Bob"],
            }
        }
        config = MeetingConfig.from_dict(data)

        assert len(config.attendees) == 2
        assert config.attendees[0].name == "Alice"
        assert config.attendees[1].name == "Bob"


class TestAgendaItem:
    """Tests for AgendaItem dataclass."""

    def test_basic_creation(self):
        """Test basic AgendaItem creation."""
        item = AgendaItem(
            topic="Sprint Goals",
            duration_minutes=15,
            presenter="Alice",
        )
        assert item.topic == "Sprint Goals"
        assert item.duration_minutes == 15
        assert item.presenter == "Alice"
        assert item.notes == ""  # default

    def test_with_notes(self):
        """Test AgendaItem with notes."""
        item = AgendaItem(
            topic="Demo",
            duration_minutes=30,
            presenter="Bob",
            notes="Include live demo of new feature",
        )
        assert item.notes == "Include live demo of new feature"


class TestAttendee:
    """Tests for Attendee dataclass."""

    def test_basic_creation(self):
        """Test basic Attendee creation."""
        attendee = Attendee(name="Alice")
        assert attendee.name == "Alice"
        assert attendee.role == ""  # default
        assert attendee.email == ""  # default

    def test_with_all_fields(self):
        """Test Attendee with all fields."""
        attendee = Attendee(
            name="Bob",
            role="Developer",
            email="bob@example.com",
        )
        assert attendee.name == "Bob"
        assert attendee.role == "Developer"
        assert attendee.email == "bob@example.com"


class TestRoundTrip:
    """Tests for round-trip serialization."""

    def test_config_round_trip(self):
        """Test that config survives serialization round-trip."""
        original = MeetingConfig(
            title="Round Trip Test",
            date="2026-05-01",
            time="15:00",
            timezone="UTC",
            duration_minutes=120,
            language="bilingual",
            objectives=["Test serialization", "Verify data integrity"],
            attendees=[
                Attendee(name="Test User", role="Tester", email="test@example.com"),
            ],
            agenda_items=[
                AgendaItem(topic="First Topic", duration_minutes=30, presenter="Test User"),
            ],
        )

        # Convert to dict and back
        data = original.to_dict()
        restored = MeetingConfig.from_dict(data)

        assert restored.title == original.title
        assert restored.date == original.date
        assert restored.time == original.time
        assert restored.timezone == original.timezone
        assert restored.duration_minutes == original.duration_minutes
        assert restored.language == original.language
        assert restored.objectives == original.objectives
        assert len(restored.attendees) == len(original.attendees)
        assert restored.attendees[0].name == original.attendees[0].name
