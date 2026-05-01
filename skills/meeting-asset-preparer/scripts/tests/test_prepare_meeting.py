"""
Tests for the meeting asset preparer script.
"""

import subprocess
import sys
import tempfile
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
        # Verify agenda_items are restored
        assert len(restored.agenda_items) == len(original.agenda_items)
        assert restored.agenda_items[0].topic == original.agenda_items[0].topic
        assert restored.agenda_items[0].duration_minutes == original.agenda_items[0].duration_minutes
        assert restored.agenda_items[0].presenter == original.agenda_items[0].presenter


class TestCLI:
    """Tests for CLI commands."""

    @pytest.fixture
    def script_path(self) -> Path:
        """Get path to the prepare_meeting.py script."""
        return Path(__file__).resolve().parents[1] / "prepare_meeting.py"

    @pytest.fixture
    def temp_dir(self, tmp_path: Path) -> Path:
        """Create a temporary directory for test outputs."""
        return tmp_path

    def test_init_creates_config_file(self, script_path: Path, temp_dir: Path):
        """Test that init command creates a valid config file."""
        output_file = temp_dir / "meeting_config.yaml"
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "init",
                "--title",
                "Test Meeting",
                "--date",
                "2026-04-15",
                "--time",
                "14:00",
                "--timezone",
                "JST",
                "--attendees",
                "Alice,Bob",
                "--language",
                "bilingual",
                "--output",
                str(output_file),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert output_file.exists()
        content = output_file.read_text()
        assert "Test Meeting" in content
        assert "2026-04-15" in content

    def test_generate_agenda_creates_markdown(self, script_path: Path, temp_dir: Path):
        """Test that generate-agenda creates a valid markdown file."""
        # First create a config file
        config_file = temp_dir / "config.yaml"
        subprocess.run(
            [
                sys.executable,
                str(script_path),
                "init",
                "--title",
                "Sprint Review",
                "--date",
                "2026-04-15",
                "--time",
                "10:00",
                "--language",
                "en",
                "--output",
                str(config_file),
            ],
            capture_output=True,
        )

        # Generate agenda
        agenda_file = temp_dir / "agenda.md"
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "generate-agenda",
                "--config",
                str(config_file),
                "--topics",
                "Opening,Demo,Q&A",
                "--durations",
                "5,20,10",
                "--output",
                str(agenda_file),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert agenda_file.exists()
        content = agenda_file.read_text()
        assert "Meeting Agenda" in content
        assert "Opening" in content
        assert "Demo" in content
        assert "Q&A" in content

    def test_create_decision_log_creates_template(self, script_path: Path, temp_dir: Path):
        """Test that create-decision-log creates a valid template."""
        config_file = temp_dir / "config.yaml"
        subprocess.run(
            [
                sys.executable,
                str(script_path),
                "init",
                "--title",
                "Planning Session",
                "--date",
                "2026-04-20",
                "--time",
                "09:00",
                "--output",
                str(config_file),
            ],
            capture_output=True,
        )

        decision_log = temp_dir / "decisions.md"
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "create-decision-log",
                "--config",
                str(config_file),
                "--output",
                str(decision_log),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert decision_log.exists()
        content = decision_log.read_text()
        assert "Decision Log" in content
        assert "Planning Session" in content

    def test_create_action_items_creates_template(self, script_path: Path, temp_dir: Path):
        """Test that create-action-items creates a valid template."""
        config_file = temp_dir / "config.yaml"
        subprocess.run(
            [
                sys.executable,
                str(script_path),
                "init",
                "--title",
                "Weekly Sync",
                "--date",
                "2026-04-21",
                "--time",
                "15:00",
                "--output",
                str(config_file),
            ],
            capture_output=True,
        )

        action_items = temp_dir / "actions.md"
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "create-action-items",
                "--config",
                str(config_file),
                "--output",
                str(action_items),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert action_items.exists()
        content = action_items.read_text()
        assert "Action Items" in content
        assert "Weekly Sync" in content

    def test_no_command_shows_help(self, script_path: Path):
        """Test that running without command shows help."""
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "usage:" in result.stdout.lower() or "Meeting Asset Preparer" in result.stdout
