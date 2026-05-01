"""
Tests for the action status updater CLI module.
"""

from datetime import datetime, timezone
from pathlib import Path

import pytest

# Mock yaml if not available
try:
    import yaml
except ImportError:
    yaml = None

from action_status_updater import (
    ActionItem,
    ActionState,
    find_matching_items,
    generate_id,
    intent_to_status,
    load_state,
    save_state,
)
from nl_parser import Intent, Language, ParseResult


class TestGenerateId:
    """Tests for ID generation."""

    def test_id_format(self):
        """Test that generated IDs have correct format."""
        id = generate_id()
        assert id.startswith("act-")
        assert len(id) == 12  # "act-" + 8 hex chars

    def test_ids_unique(self):
        """Test that generated IDs are unique."""
        ids = [generate_id() for _ in range(100)]
        assert len(set(ids)) == 100


class TestActionItem:
    """Tests for ActionItem dataclass."""

    def test_default_values(self):
        """Test default value initialization."""
        item = ActionItem(
            id="act-001",
            channel="email",
            assignee="Sean",
            description="Test item",
        )

        assert item.status == "pending"
        assert item.created_at != ""
        assert item.updated_at != ""
        assert item.due_date is None
        assert item.delegated_to is None
        assert item.history == []

    def test_custom_values(self):
        """Test custom value initialization."""
        item = ActionItem(
            id="act-002",
            channel="slack",
            assignee="Mike",
            description="Another item",
            status="completed",
            due_date="2024-01-15",
        )

        assert item.status == "completed"
        assert item.due_date == "2024-01-15"


class TestActionState:
    """Tests for ActionState dataclass."""

    def test_default_values(self):
        """Test default state initialization."""
        state = ActionState()

        assert state.schema_version == "1.0"
        assert state.last_updated != ""
        assert state.action_items == []

    def test_with_items(self):
        """Test state with action items."""
        item = ActionItem(
            id="act-001",
            channel="email",
            assignee="Sean",
            description="Test",
        )
        state = ActionState(action_items=[item])

        assert len(state.action_items) == 1
        assert state.action_items[0].id == "act-001"


@pytest.mark.skipif(yaml is None, reason="pyyaml not installed")
class TestStatePersistence:
    """Tests for state file persistence."""

    def test_save_and_load(self, tmp_path: Path):
        """Test saving and loading state."""
        state_file = tmp_path / "test_state.yaml"

        # Create state with items
        item = ActionItem(
            id="act-001",
            channel="email",
            assignee="Sean",
            description="Reply to proposal",
            due_date="2024-01-15",
        )
        state = ActionState(action_items=[item])

        # Save
        save_state(state, state_file)
        assert state_file.exists()

        # Load
        loaded_state = load_state(state_file)

        assert loaded_state.schema_version == "1.0"
        assert len(loaded_state.action_items) == 1
        assert loaded_state.action_items[0].id == "act-001"
        assert loaded_state.action_items[0].assignee == "Sean"
        assert loaded_state.action_items[0].description == "Reply to proposal"

    def test_load_nonexistent(self, tmp_path: Path):
        """Test loading from nonexistent file."""
        state_file = tmp_path / "nonexistent.yaml"
        state = load_state(state_file)

        assert state.schema_version == "1.0"
        assert state.action_items == []

    def test_save_creates_parent_dirs(self, tmp_path: Path):
        """Test that save creates parent directories."""
        state_file = tmp_path / "subdir" / "nested" / "state.yaml"
        state = ActionState()

        save_state(state, state_file)

        assert state_file.exists()


class TestFindMatchingItems:
    """Tests for action item matching."""

    def create_test_state(self) -> ActionState:
        """Create a test state with sample items."""
        return ActionState(
            action_items=[
                ActionItem(
                    id="act-001",
                    channel="email",
                    assignee="Sean",
                    description="Reply to proposal inquiry",
                    status="pending",
                ),
                ActionItem(
                    id="act-002",
                    channel="slack",
                    assignee="Mike",
                    description="Review PR #234",
                    status="pending",
                ),
                ActionItem(
                    id="act-003",
                    channel="email",
                    assignee="Sean",
                    description="Send monthly report",
                    status="completed",
                ),
                ActionItem(
                    id="act-004",
                    channel="meeting",
                    assignee="Lu",
                    description="Schedule team sync",
                    status="pending",
                ),
            ]
        )

    def test_match_by_person(self):
        """Test matching by person name."""
        state = self.create_test_state()
        parse_result = ParseResult(
            intent=Intent.COMPLETED,
            language=Language.JAPANESE,
            person="Sean",
            channel=None,
            keywords=[],
            confidence=0.9,
            raw_input="Seanの件は完了",
        )

        matches = find_matching_items(state, parse_result)

        assert len(matches) >= 1
        # Should prefer pending items
        assert matches[0][0].id in ["act-001", "act-003"]

    def test_match_by_channel(self):
        """Test matching by channel."""
        state = self.create_test_state()
        parse_result = ParseResult(
            intent=Intent.COMPLETED,
            language=Language.ENGLISH,
            person=None,
            channel="slack",
            keywords=[],
            confidence=0.9,
            raw_input="Slack task done",
        )

        matches = find_matching_items(state, parse_result)

        assert len(matches) >= 1
        assert matches[0][0].channel == "slack"

    def test_match_by_person_and_channel(self):
        """Test matching by both person and channel."""
        state = self.create_test_state()
        parse_result = ParseResult(
            intent=Intent.COMPLETED,
            language=Language.JAPANESE,
            person="Sean",
            channel="email",
            keywords=[],
            confidence=0.9,
            raw_input="Seanのメール返信した",
        )

        matches = find_matching_items(state, parse_result)

        assert len(matches) >= 1
        # Best match should be Sean + email + pending
        assert matches[0][0].id == "act-001"

    def test_match_by_keywords(self):
        """Test matching by description keywords."""
        state = self.create_test_state()
        parse_result = ParseResult(
            intent=Intent.COMPLETED,
            language=Language.ENGLISH,
            person=None,
            channel=None,
            keywords=["report"],
            confidence=0.9,
            raw_input="Report sent",
        )

        matches = find_matching_items(state, parse_result)

        assert len(matches) >= 1
        # Should find the monthly report item
        assert any(m[0].id == "act-003" for m in matches)

    def test_low_confidence_matches(self):
        """Test that non-matching criteria result in low confidence scores."""
        state = self.create_test_state()
        parse_result = ParseResult(
            intent=Intent.COMPLETED,
            language=Language.ENGLISH,
            person="NonExistent",
            channel="phone",
            keywords=["xyz"],
            confidence=0.9,
            raw_input="xyz",
        )

        matches = find_matching_items(state, parse_result)

        # Pending items get a small boost, but no real matches
        # All matches should have very low confidence (0.1 from pending status only)
        for item, confidence in matches:
            assert confidence <= 0.1


class TestIntentToStatus:
    """Tests for intent to status conversion."""

    def test_completed(self):
        """Test completed intent conversion."""
        assert intent_to_status(Intent.COMPLETED) == "completed"

    def test_delegated(self):
        """Test delegated intent conversion."""
        assert intent_to_status(Intent.DELEGATED) == "delegated"

    def test_deferred(self):
        """Test deferred intent conversion."""
        assert intent_to_status(Intent.DEFERRED) == "deferred"

    def test_in_progress(self):
        """Test in-progress intent conversion."""
        assert intent_to_status(Intent.IN_PROGRESS) == "in_progress"

    def test_unknown(self):
        """Test unknown intent defaults to pending."""
        assert intent_to_status(Intent.UNKNOWN) == "pending"
