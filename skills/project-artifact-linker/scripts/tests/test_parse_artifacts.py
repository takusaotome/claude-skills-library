"""
Tests for parse_artifacts.py
"""

import json
from pathlib import Path

import pytest
from parse_artifacts import ArtifactParser


class TestDateExtraction:
    """Tests for date extraction functionality."""

    def test_extract_iso_date(self):
        """Test extraction of ISO format dates."""
        parser = ArtifactParser()
        text = "Meeting held on 2024-01-15"
        date = parser._extract_date(text)
        assert date == "2024-01-15"

    def test_extract_us_date_format(self):
        """Test extraction of US format dates (MM/DD/YYYY)."""
        parser = ArtifactParser()
        text = "Scheduled for 01/15/2024"
        date = parser._extract_date(text)
        assert date == "2024-01-15"

    def test_extract_month_name_date(self):
        """Test extraction of dates with month names."""
        parser = ArtifactParser()
        text = "Meeting on January 15, 2024"
        date = parser._extract_date(text)
        assert date == "2024-01-15"

    def test_no_date_returns_none(self):
        """Test that missing dates return None."""
        parser = ArtifactParser()
        text = "No date mentioned here"
        date = parser._extract_date(text)
        assert date is None


class TestAttendeeExtraction:
    """Tests for attendee extraction functionality."""

    def test_extract_comma_separated_attendees(self):
        """Test extraction of comma-separated attendees."""
        parser = ArtifactParser()
        text = """
        Attendees: Alice Smith, Bob Jones, Charlie Brown

        Discussion topics...
        """
        attendees = parser._extract_attendees(text)
        assert "Alice Smith" in attendees
        assert "Bob Jones" in attendees
        assert "Charlie Brown" in attendees

    def test_extract_bullet_list_attendees(self):
        """Test extraction of bullet-list attendees."""
        parser = ArtifactParser()
        text = """
        Participants:
        - Alice Smith
        - Bob Jones
        - Charlie Brown

        Agenda items...
        """
        attendees = parser._extract_attendees(text)
        assert "Alice Smith" in attendees
        assert "Bob Jones" in attendees


class TestActionItemExtraction:
    """Tests for action item extraction functionality."""

    def test_extract_action_keyword(self):
        """Test extraction of ACTION: style items."""
        parser = ArtifactParser()
        text = "ACTION: Review security requirements by Jan 17"
        items = parser._extract_action_items(text, "test.md")
        assert len(items) == 1
        assert "Review security requirements" in items[0].description

    def test_extract_todo_keyword(self):
        """Test extraction of TODO: style items."""
        parser = ArtifactParser()
        text = "TODO: Update documentation"
        items = parser._extract_action_items(text, "test.md")
        assert len(items) == 1
        assert "Update documentation" in items[0].description

    def test_extract_owner_from_at_mention(self):
        """Test extraction of owner from @mention."""
        parser = ArtifactParser()
        text = "@Alice to review the proposal"
        items = parser._extract_action_items(text, "test.md")
        assert len(items) == 1
        assert items[0].owner == "Alice"

    def test_action_item_has_source_info(self):
        """Test that action items include source file info."""
        parser = ArtifactParser()
        text = "ACTION: Do something"
        items = parser._extract_action_items(text, "meeting.md")
        assert len(items) == 1
        assert items[0].source_file == "meeting.md"
        assert items[0].source_line > 0


class TestDecisionExtraction:
    """Tests for decision extraction functionality."""

    def test_extract_decision_keyword(self):
        """Test extraction of DECISION: style items."""
        parser = ArtifactParser()
        text = "DECISION: Use PostgreSQL for the database"
        decisions = parser._extract_decisions(text, "test.md")
        assert len(decisions) == 1
        assert "PostgreSQL" in decisions[0].description

    def test_extract_agreed_keyword(self):
        """Test extraction of Agreed: style items."""
        parser = ArtifactParser()
        text = "Agreed: Adopt OAuth2 for authentication"
        decisions = parser._extract_decisions(text, "test.md")
        assert len(decisions) == 1
        assert "OAuth2" in decisions[0].description


class TestMeetingParsing:
    """Tests for complete meeting minutes parsing."""

    def test_parse_complete_meeting(self, tmp_path):
        """Test parsing a complete meeting minutes document."""
        parser = ArtifactParser()
        content = """
# Project Kickoff Meeting

Date: 2024-01-15

Attendees: Alice Smith, Bob Jones

## Discussion

We discussed the project timeline and deliverables.

ACTION: @Alice to create project plan by 2024-01-22

DECISION: Use agile methodology for project execution

## Next Steps

Schedule follow-up meeting.
"""
        meeting = parser.parse_meeting_minutes(content, "kickoff.md")

        assert meeting.date == "2024-01-15"
        assert "Alice Smith" in meeting.attendees
        assert "Bob Jones" in meeting.attendees
        assert len(meeting.action_items) == 1
        assert len(meeting.decisions) == 1


class TestWBSParsing:
    """Tests for WBS document parsing."""

    def test_parse_wbs_table(self, tmp_path):
        """Test parsing a WBS markdown table."""
        parser = ArtifactParser()
        content = """
# Work Breakdown Structure

| Task ID | Task Name | Owner | Start | End | Status |
|---------|-----------|-------|-------|-----|--------|
| WBS-1.1 | Requirements Analysis | Alice | 2024-01-15 | 2024-01-30 | In Progress |
| WBS-1.2 | Design Phase | Bob | 2024-02-01 | 2024-02-15 | Pending |
"""
        tasks = parser.parse_wbs(content, "wbs.md")

        assert len(tasks) == 2
        assert tasks[0].id == "WBS-1.1"
        assert tasks[0].name == "Requirements Analysis"
        assert tasks[0].owner == "Alice"
        assert tasks[1].id == "WBS-1.2"


class TestRequirementsParsing:
    """Tests for requirements document parsing."""

    def test_parse_requirements(self):
        """Test parsing requirements with IDs."""
        parser = ArtifactParser()
        content = """
# Requirements Document

REQ-SEC-001: The system shall support OAuth2 authentication
Priority: High

REQ-PERF-001: Response time shall be less than 200ms
Priority: Medium
"""
        reqs = parser.parse_requirements(content, "requirements.md")

        assert len(reqs) == 2
        assert reqs[0].id == "REQ-SEC-001"
        assert "OAuth2" in reqs[0].description
        assert reqs[0].priority == "High"


class TestDirectoryParsing:
    """Tests for parsing directories of documents."""

    def test_parse_directory(self, tmp_path):
        """Test parsing a directory with multiple documents."""
        # Create test files
        meeting_file = tmp_path / "meeting-2024-01-15.md"
        meeting_file.write_text("""
# Weekly Meeting

Date: 2024-01-15
Attendees: Alice, Bob

ACTION: Review specs
""")

        wbs_file = tmp_path / "wbs.md"
        wbs_file.write_text("""
| Task ID | Task Name | Owner |
|---------|-----------|-------|
| WBS-1.1 | Design | Alice |
""")

        parser = ArtifactParser()
        parser.parse_directory(tmp_path)

        result = parser.to_dict()
        assert len(result["artifacts"]["meetings"]) == 1
        assert len(result["artifacts"]["wbs_tasks"]) == 1


class TestOutputFormat:
    """Tests for output format and schema."""

    def test_output_has_schema_version(self):
        """Test that output includes schema version."""
        parser = ArtifactParser()
        parser.parse_meeting_minutes("# Meeting\nDate: 2024-01-15", "test.md")
        result = parser.to_dict()

        assert "schema_version" in result
        assert result["schema_version"] == "1.0"

    def test_output_has_extraction_date(self):
        """Test that output includes extraction timestamp."""
        parser = ArtifactParser()
        result = parser.to_dict()

        assert "extraction_date" in result
        # Should be ISO format
        assert "T" in result["extraction_date"]

    def test_output_structure(self):
        """Test that output has expected structure."""
        parser = ArtifactParser()
        result = parser.to_dict()

        assert "artifacts" in result
        assert "meetings" in result["artifacts"]
        assert "wbs_tasks" in result["artifacts"]
        assert "requirements" in result["artifacts"]
        assert "decisions" in result["artifacts"]
