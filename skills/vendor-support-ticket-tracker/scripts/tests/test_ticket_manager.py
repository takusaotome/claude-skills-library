"""Tests for ticket_manager.py."""

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml
from ticket_manager import (
    SCHEMA_VERSION,
    VALID_CATEGORIES,
    VALID_PRIORITIES,
    VALID_STATUSES,
    calculate_sla_target,
    cmd_create,
    cmd_escalate,
    cmd_init,
    cmd_list,
    cmd_report,
    cmd_show,
    cmd_stale,
    cmd_update,
    generate_report,
    get_timestamp,
    load_database,
    save_database,
)


class TestGetTimestamp:
    """Tests for get_timestamp function."""

    def test_returns_iso_format(self):
        """Timestamp should be in ISO 8601 format with Z suffix."""
        ts = get_timestamp()
        assert ts.endswith("Z")
        # Should parse without error
        datetime.fromisoformat(ts.replace("Z", "+00:00"))

    def test_returns_utc(self):
        """Timestamp should be in UTC."""
        ts = get_timestamp()
        parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        # Should be within 1 second of now
        assert abs((parsed - now).total_seconds()) < 1


class TestCalculateSlaTarget:
    """Tests for SLA target calculation."""

    def test_critical_priority_4_hours(self):
        """Critical priority should have 4-hour SLA."""
        created = "2025-06-15T10:00:00Z"
        target = calculate_sla_target("critical", created)
        expected = "2025-06-15T14:00:00Z"
        assert target == expected

    def test_high_priority_24_hours(self):
        """High priority should have 24-hour SLA."""
        created = "2025-06-15T10:00:00Z"
        target = calculate_sla_target("high", created)
        expected = "2025-06-16T10:00:00Z"
        assert target == expected

    def test_medium_priority_72_hours(self):
        """Medium priority should have 72-hour SLA."""
        created = "2025-06-15T10:00:00Z"
        target = calculate_sla_target("medium", created)
        expected = "2025-06-18T10:00:00Z"
        assert target == expected

    def test_low_priority_120_hours(self):
        """Low priority should have 120-hour (5 day) SLA."""
        created = "2025-06-15T10:00:00Z"
        target = calculate_sla_target("low", created)
        expected = "2025-06-20T10:00:00Z"
        assert target == expected


class TestDatabaseOperations:
    """Tests for load_database and save_database."""

    def test_load_nonexistent_returns_empty(self, tmp_path: Path):
        """Loading a nonexistent file should return empty database."""
        db_path = tmp_path / "nonexistent.yaml"
        data = load_database(db_path)
        assert data["schema_version"] == SCHEMA_VERSION
        assert data["tickets"] == {}

    def test_save_and_load_roundtrip(self, tmp_path: Path):
        """Data should survive save/load cycle."""
        db_path = tmp_path / "test.yaml"
        original = {
            "schema_version": SCHEMA_VERSION,
            "tickets": {
                "TEST-001": {
                    "vendor": "TestVendor",
                    "ticket_id": "TEST-001",
                    "subject": "Test issue",
                    "status": "open",
                }
            },
        }
        save_database(db_path, original)
        loaded = load_database(db_path)
        assert loaded == original

    def test_load_empty_file_returns_empty(self, tmp_path: Path):
        """Loading an empty file should return empty database."""
        db_path = tmp_path / "empty.yaml"
        db_path.write_text("")
        data = load_database(db_path)
        assert data["schema_version"] == SCHEMA_VERSION
        assert data["tickets"] == {}


class TestCmdInit:
    """Tests for init command."""

    def test_creates_new_database(self, tmp_path: Path):
        """Init should create a new database file."""
        db_path = tmp_path / "new.yaml"
        args = argparse.Namespace(db_path=str(db_path), force=False)
        result = cmd_init(args)
        assert result == 0
        assert db_path.exists()
        data = load_database(db_path)
        assert data["schema_version"] == SCHEMA_VERSION
        assert data["tickets"] == {}

    def test_fails_if_exists_without_force(self, tmp_path: Path):
        """Init should fail if database exists and force is False."""
        db_path = tmp_path / "existing.yaml"
        db_path.write_text("existing: data")
        args = argparse.Namespace(db_path=str(db_path), force=False)
        result = cmd_init(args)
        assert result == 1

    def test_overwrites_with_force(self, tmp_path: Path):
        """Init should overwrite existing database with force=True."""
        db_path = tmp_path / "existing.yaml"
        db_path.write_text("existing: data")
        args = argparse.Namespace(db_path=str(db_path), force=True)
        result = cmd_init(args)
        assert result == 0
        data = load_database(db_path)
        assert data["tickets"] == {}


class TestCmdCreate:
    """Tests for create command."""

    def test_creates_ticket(self, tmp_path: Path):
        """Create should add a new ticket to database."""
        db_path = tmp_path / "tickets.yaml"
        save_database(db_path, {"schema_version": SCHEMA_VERSION, "tickets": {}})

        args = argparse.Namespace(
            vendor="STX",
            ticket_id="SR-2025-001",
            subject="HDD failure",
            priority="high",
            category="RMA",
            contact="support@stx.com",
            notes="Initial creation",
            db_path=str(db_path),
        )
        result = cmd_create(args)
        assert result == 0

        data = load_database(db_path)
        assert "SR-2025-001" in data["tickets"]
        ticket = data["tickets"]["SR-2025-001"]
        assert ticket["vendor"] == "STX"
        assert ticket["status"] == "open"
        assert ticket["priority"] == "high"
        assert ticket["category"] == "RMA"
        assert len(ticket["timeline"]) == 1
        assert ticket["timeline"][0]["action"] == "created"

    def test_fails_duplicate_ticket(self, tmp_path: Path):
        """Create should fail if ticket ID already exists."""
        db_path = tmp_path / "tickets.yaml"
        save_database(
            db_path,
            {
                "schema_version": SCHEMA_VERSION,
                "tickets": {"SR-2025-001": {"ticket_id": "SR-2025-001"}},
            },
        )

        args = argparse.Namespace(
            vendor="STX",
            ticket_id="SR-2025-001",
            subject="New issue",
            priority="high",
            category="RMA",
            contact=None,
            notes=None,
            db_path=str(db_path),
        )
        result = cmd_create(args)
        assert result == 1

    def test_fails_invalid_priority(self, tmp_path: Path):
        """Create should fail with invalid priority."""
        db_path = tmp_path / "tickets.yaml"
        save_database(db_path, {"schema_version": SCHEMA_VERSION, "tickets": {}})

        args = argparse.Namespace(
            vendor="STX",
            ticket_id="SR-2025-001",
            subject="Test",
            priority="invalid",
            category="RMA",
            contact=None,
            notes=None,
            db_path=str(db_path),
        )
        result = cmd_create(args)
        assert result == 1

    def test_fails_invalid_category(self, tmp_path: Path):
        """Create should fail with invalid category."""
        db_path = tmp_path / "tickets.yaml"
        save_database(db_path, {"schema_version": SCHEMA_VERSION, "tickets": {}})

        args = argparse.Namespace(
            vendor="STX",
            ticket_id="SR-2025-001",
            subject="Test",
            priority="high",
            category="invalid",
            contact=None,
            notes=None,
            db_path=str(db_path),
        )
        result = cmd_create(args)
        assert result == 1


class TestCmdUpdate:
    """Tests for update command."""

    def test_updates_status(self, tmp_path: Path):
        """Update should change ticket status."""
        db_path = tmp_path / "tickets.yaml"
        save_database(
            db_path,
            {
                "schema_version": SCHEMA_VERSION,
                "tickets": {
                    "SR-2025-001": {
                        "ticket_id": "SR-2025-001",
                        "status": "open",
                        "updated_at": "2025-06-10T10:00:00Z",
                        "timeline": [],
                    }
                },
            },
        )

        args = argparse.Namespace(
            ticket_id="SR-2025-001",
            status="acknowledged",
            notes="Vendor confirmed",
            db_path=str(db_path),
        )
        result = cmd_update(args)
        assert result == 0

        data = load_database(db_path)
        ticket = data["tickets"]["SR-2025-001"]
        assert ticket["status"] == "acknowledged"
        assert len(ticket["timeline"]) == 1
        assert ticket["timeline"][0]["action"] == "status_change"
        assert ticket["timeline"][0]["from_status"] == "open"
        assert ticket["timeline"][0]["to_status"] == "acknowledged"

    def test_adds_note_without_status_change(self, tmp_path: Path):
        """Update should add note without changing status."""
        db_path = tmp_path / "tickets.yaml"
        save_database(
            db_path,
            {
                "schema_version": SCHEMA_VERSION,
                "tickets": {
                    "SR-2025-001": {
                        "ticket_id": "SR-2025-001",
                        "status": "open",
                        "updated_at": "2025-06-10T10:00:00Z",
                        "timeline": [],
                    }
                },
            },
        )

        args = argparse.Namespace(
            ticket_id="SR-2025-001",
            status=None,
            notes="Added a follow-up note",
            db_path=str(db_path),
        )
        result = cmd_update(args)
        assert result == 0

        data = load_database(db_path)
        ticket = data["tickets"]["SR-2025-001"]
        assert ticket["status"] == "open"  # Unchanged
        assert len(ticket["timeline"]) == 1
        assert ticket["timeline"][0]["action"] == "note_added"

    def test_fails_nonexistent_ticket(self, tmp_path: Path):
        """Update should fail if ticket doesn't exist."""
        db_path = tmp_path / "tickets.yaml"
        save_database(db_path, {"schema_version": SCHEMA_VERSION, "tickets": {}})

        args = argparse.Namespace(
            ticket_id="NONEXISTENT",
            status="acknowledged",
            notes=None,
            db_path=str(db_path),
        )
        result = cmd_update(args)
        assert result == 1

    def test_fails_invalid_status(self, tmp_path: Path):
        """Update should fail with invalid status."""
        db_path = tmp_path / "tickets.yaml"
        save_database(
            db_path,
            {
                "schema_version": SCHEMA_VERSION,
                "tickets": {
                    "SR-2025-001": {
                        "ticket_id": "SR-2025-001",
                        "status": "open",
                        "updated_at": "2025-06-10T10:00:00Z",
                        "timeline": [],
                    }
                },
            },
        )

        args = argparse.Namespace(
            ticket_id="SR-2025-001",
            status="invalid-status",
            notes=None,
            db_path=str(db_path),
        )
        result = cmd_update(args)
        assert result == 1


class TestCmdEscalate:
    """Tests for escalate command."""

    def test_escalates_ticket(self, tmp_path: Path):
        """Escalate should mark ticket as escalated."""
        db_path = tmp_path / "tickets.yaml"
        save_database(
            db_path,
            {
                "schema_version": SCHEMA_VERSION,
                "tickets": {
                    "SR-2025-001": {
                        "ticket_id": "SR-2025-001",
                        "status": "in-progress",
                        "escalated": False,
                        "updated_at": "2025-06-10T10:00:00Z",
                        "timeline": [],
                    }
                },
            },
        )

        args = argparse.Namespace(
            ticket_id="SR-2025-001",
            reason="No response for 10 days",
            db_path=str(db_path),
        )
        result = cmd_escalate(args)
        assert result == 0

        data = load_database(db_path)
        ticket = data["tickets"]["SR-2025-001"]
        assert ticket["status"] == "escalated"
        assert ticket["escalated"] is True
        assert len(ticket["timeline"]) == 1
        assert ticket["timeline"][0]["action"] == "escalated"
        assert ticket["timeline"][0]["reason"] == "No response for 10 days"

    def test_fails_nonexistent_ticket(self, tmp_path: Path):
        """Escalate should fail if ticket doesn't exist."""
        db_path = tmp_path / "tickets.yaml"
        save_database(db_path, {"schema_version": SCHEMA_VERSION, "tickets": {}})

        args = argparse.Namespace(
            ticket_id="NONEXISTENT",
            reason="Test",
            db_path=str(db_path),
        )
        result = cmd_escalate(args)
        assert result == 1


class TestGenerateReport:
    """Tests for report generation."""

    def test_empty_tickets_report(self):
        """Report with no tickets should have zero counts."""
        report = generate_report({})
        assert "Total Open: 0" in report
        assert "High Priority: 0" in report
        assert "Escalated: 0" in report

    def test_report_groups_by_vendor(self):
        """Report should group tickets by vendor."""
        tickets = {
            "STX-001": {
                "ticket_id": "STX-001",
                "vendor": "STX",
                "subject": "Issue 1",
                "priority": "high",
                "status": "open",
                "escalated": False,
                "created_at": "2025-06-15T10:00:00Z",
                "updated_at": "2025-06-15T10:00:00Z",
            },
            "DELL-001": {
                "ticket_id": "DELL-001",
                "vendor": "Dell",
                "subject": "Issue 2",
                "priority": "medium",
                "status": "open",
                "escalated": False,
                "created_at": "2025-06-15T10:00:00Z",
                "updated_at": "2025-06-15T10:00:00Z",
            },
        }
        report = generate_report(tickets)
        assert "### STX" in report
        assert "### Dell" in report
        assert "STX-001" in report
        assert "DELL-001" in report

    def test_report_counts_high_priority(self):
        """Report should count high and critical priority tickets."""
        tickets = {
            "T1": {
                "ticket_id": "T1",
                "vendor": "V",
                "subject": "S",
                "priority": "critical",
                "status": "open",
                "escalated": False,
                "created_at": "2025-06-15T10:00:00Z",
                "updated_at": "2025-06-15T10:00:00Z",
            },
            "T2": {
                "ticket_id": "T2",
                "vendor": "V",
                "subject": "S",
                "priority": "high",
                "status": "open",
                "escalated": False,
                "created_at": "2025-06-15T10:00:00Z",
                "updated_at": "2025-06-15T10:00:00Z",
            },
            "T3": {
                "ticket_id": "T3",
                "vendor": "V",
                "subject": "S",
                "priority": "low",
                "status": "open",
                "escalated": False,
                "created_at": "2025-06-15T10:00:00Z",
                "updated_at": "2025-06-15T10:00:00Z",
            },
        }
        report = generate_report(tickets)
        assert "High Priority: 2" in report


class TestCmdStale:
    """Tests for stale ticket detection."""

    def test_finds_stale_tickets(self, tmp_path: Path):
        """Stale command should find tickets with no recent activity."""
        db_path = tmp_path / "tickets.yaml"
        old_date = (datetime.now(timezone.utc) - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        save_database(
            db_path,
            {
                "schema_version": SCHEMA_VERSION,
                "tickets": {
                    "SR-2025-001": {
                        "ticket_id": "SR-2025-001",
                        "vendor": "STX",
                        "subject": "Old issue",
                        "priority": "high",
                        "status": "in-progress",
                        "updated_at": old_date,
                    }
                },
            },
        )

        args = argparse.Namespace(days=7, db_path=str(db_path))
        result = cmd_stale(args)
        assert result == 0

    def test_excludes_closed_tickets(self, tmp_path: Path):
        """Stale command should exclude closed tickets."""
        db_path = tmp_path / "tickets.yaml"
        old_date = (datetime.now(timezone.utc) - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        save_database(
            db_path,
            {
                "schema_version": SCHEMA_VERSION,
                "tickets": {
                    "SR-2025-001": {
                        "ticket_id": "SR-2025-001",
                        "vendor": "STX",
                        "subject": "Closed issue",
                        "priority": "high",
                        "status": "closed",
                        "updated_at": old_date,
                    }
                },
            },
        )

        args = argparse.Namespace(days=7, db_path=str(db_path))
        # Should return 0 and print "No stale tickets"
        result = cmd_stale(args)
        assert result == 0
