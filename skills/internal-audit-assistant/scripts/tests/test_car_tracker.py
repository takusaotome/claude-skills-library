"""Tests for car_tracker.py module."""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from ..car_tracker import (
    CAR,
    ESCALATION_THRESHOLDS,
    calculate_days_open,
    calculate_days_overdue,
    generate_json_report,
    generate_monthly_report,
    generate_overdue_report,
    get_escalation_level,
    parse_csv,
    parse_date,
)


class TestParseDate:
    """Tests for parse_date function."""

    def test_valid_date(self):
        """Test parsing valid date string."""
        result = parse_date("2025-01-15")
        assert result == datetime(2025, 1, 15)

    def test_empty_string(self):
        """Test parsing empty string returns None."""
        assert parse_date("") is None

    def test_na_string(self):
        """Test parsing N/A returns None."""
        assert parse_date("N/A") is None
        assert parse_date("n/a") is None

    def test_none_string(self):
        """Test parsing 'none' returns None."""
        assert parse_date("none") is None
        assert parse_date("None") is None

    def test_invalid_format(self):
        """Test parsing invalid format returns None."""
        assert parse_date("01-15-2025") is None
        assert parse_date("2025/01/15") is None


class TestCAR:
    """Tests for CAR dataclass."""

    def test_car_creation(self):
        """Test creating CAR instance."""
        car = CAR(
            car_id="CAR-2025-001",
            audit_name="AP Audit",
            finding_title="Emergency PO process",
            severity="Medium",
            auditee_dept="Finance",
            owner="J. Smith",
            due_date="2025-07-30",
            status="In Progress",
            open_date="2025-04-15",
        )
        assert car.car_id == "CAR-2025-001"
        assert car.severity == "Medium"
        assert car.close_date is None


class TestCalculateDaysOpen:
    """Tests for calculate_days_open function."""

    def test_days_open_calculation(self):
        """Test calculating days open."""
        car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Test",
            severity="Medium",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-06-01",
            status="Open",
            open_date="2025-01-01",
        )
        reference = datetime(2025, 1, 31)
        days = calculate_days_open(car, reference)
        assert days == 30

    def test_days_open_no_date(self):
        """Test days open when no open date."""
        car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Test",
            severity="Medium",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-06-01",
            status="Open",
            open_date="",
        )
        reference = datetime(2025, 1, 31)
        days = calculate_days_open(car, reference)
        assert days == 0


class TestCalculateDaysOverdue:
    """Tests for calculate_days_overdue function."""

    def test_overdue_positive(self):
        """Test positive days overdue."""
        car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Test",
            severity="Medium",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-01-15",
            status="Open",
            open_date="2025-01-01",
        )
        reference = datetime(2025, 1, 25)
        days = calculate_days_overdue(car, reference)
        assert days == 10

    def test_not_yet_due(self):
        """Test negative days (not yet due)."""
        car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Test",
            severity="Medium",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-02-15",
            status="Open",
            open_date="2025-01-01",
        )
        reference = datetime(2025, 1, 15)
        days = calculate_days_overdue(car, reference)
        assert days == -31


class TestGetEscalationLevel:
    """Tests for get_escalation_level function."""

    def test_not_overdue(self):
        """Test escalation level when not overdue."""
        car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Test",
            severity="Critical",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-02-15",
            status="Open",
            open_date="2025-01-01",
        )
        assert get_escalation_level(car, 0) == 0
        assert get_escalation_level(car, -5) == 0

    def test_critical_escalation_levels(self):
        """Test escalation levels for Critical severity."""
        car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Test",
            severity="Critical",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-01-15",
            status="Open",
            open_date="2025-01-01",
        )
        # Level 1: 1 day overdue (warning)
        assert get_escalation_level(car, 1) == 2  # Critical goes straight to L2

        # Level 3: 8+ days overdue
        assert get_escalation_level(car, 8) == 3
        assert get_escalation_level(car, 15) == 3

        # Level 4: 30+ days overdue
        assert get_escalation_level(car, 30) == 4
        assert get_escalation_level(car, 60) == 4

    def test_medium_escalation_levels(self):
        """Test escalation levels for Medium severity."""
        car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Test",
            severity="Medium",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-01-15",
            status="Open",
            open_date="2025-01-01",
        )
        # Warning (1-13 days)
        assert get_escalation_level(car, 10) == 1

        # Level 2: 14+ days
        assert get_escalation_level(car, 14) == 2
        assert get_escalation_level(car, 50) == 2

        # Level 3: 60+ days
        assert get_escalation_level(car, 60) == 3

        # Level 4: 90+ days
        assert get_escalation_level(car, 90) == 4


class TestParseCSV:
    """Tests for parse_csv function."""

    def test_parse_valid_csv(self):
        """Test parsing valid CAR CSV file."""
        csv_content = """car_id,audit_name,finding_title,severity,auditee_dept,owner,due_date,status,open_date,close_date
CAR-2025-001,AP Audit,Emergency PO,Medium,Finance,J. Smith,2025-07-30,In Progress,2025-04-15,
CAR-2025-002,IT Audit,Access Control,High,IT,K. Lee,2025-06-15,Overdue,2025-03-01,"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_path = Path(f.name)

        try:
            cars = parse_csv(temp_path)
            assert len(cars) == 2
            assert cars[0].car_id == "CAR-2025-001"
            assert cars[0].severity == "Medium"
            assert cars[1].auditee_dept == "IT"
        finally:
            temp_path.unlink()


class TestGenerateMonthlyReport:
    """Tests for generate_monthly_report function."""

    def test_report_structure(self):
        """Test monthly report contains required sections."""
        car = CAR(
            car_id="CAR-2025-001",
            audit_name="AP Audit",
            finding_title="Emergency PO process",
            severity="Medium",
            auditee_dept="Finance",
            owner="J. Smith",
            due_date="2025-07-30",
            status="In Progress",
            open_date="2025-04-15",
        )
        reference = datetime(2025, 5, 31)
        report = generate_monthly_report([car], reference)

        assert "# Corrective Action Request (CAR) Status Report" in report
        assert "## Executive Summary" in report
        assert "## CARs by Severity" in report
        assert "## CARs by Department" in report

    def test_overdue_section_included(self):
        """Test overdue CARs section when overdue items exist."""
        car = CAR(
            car_id="CAR-2025-001",
            audit_name="AP Audit",
            finding_title="Emergency PO process",
            severity="High",
            auditee_dept="Finance",
            owner="J. Smith",
            due_date="2025-05-01",
            status="In Progress",
            open_date="2025-04-15",
        )
        reference = datetime(2025, 5, 31)
        report = generate_monthly_report([car], reference)

        assert "## Overdue CARs Requiring Attention" in report
        assert "CAR-2025-001" in report

    def test_closed_cars_excluded(self):
        """Test closed CARs are excluded from open count."""
        open_car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Open Finding",
            severity="Medium",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-06-01",
            status="Open",
            open_date="2025-04-01",
        )
        closed_car = CAR(
            car_id="CAR-002",
            audit_name="Test",
            finding_title="Closed Finding",
            severity="Medium",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-05-01",
            status="Closed",
            open_date="2025-03-01",
            close_date="2025-05-01",
        )
        reference = datetime(2025, 5, 15)
        report = generate_monthly_report([open_car, closed_car], reference)

        assert "Total Open CARs**: 1" in report


class TestGenerateOverdueReport:
    """Tests for generate_overdue_report function."""

    def test_no_overdue_message(self):
        """Test message when no CARs are overdue."""
        car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Test",
            severity="Medium",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-06-01",
            status="Open",
            open_date="2025-04-01",
        )
        reference = datetime(2025, 5, 15)
        report = generate_overdue_report([car], reference)

        assert "No overdue CARs" in report

    def test_overdue_cars_listed(self):
        """Test overdue CARs are listed with details."""
        car = CAR(
            car_id="CAR-2025-001",
            audit_name="AP Audit",
            finding_title="Emergency PO process gap",
            severity="High",
            auditee_dept="Finance",
            owner="J. Smith",
            due_date="2025-05-01",
            status="In Progress",
            open_date="2025-04-15",
        )
        reference = datetime(2025, 5, 31)
        report = generate_overdue_report([car], reference)

        assert "CAR-2025-001" in report
        assert "High" in report
        assert "Finance" in report
        assert "J. Smith" in report


class TestGenerateJsonReport:
    """Tests for generate_json_report function."""

    def test_json_structure(self):
        """Test JSON report structure."""
        car = CAR(
            car_id="CAR-2025-001",
            audit_name="AP Audit",
            finding_title="Emergency PO process",
            severity="Medium",
            auditee_dept="Finance",
            owner="J. Smith",
            due_date="2025-07-30",
            status="In Progress",
            open_date="2025-04-15",
        )
        reference = datetime(2025, 5, 31)
        report_json = generate_json_report([car], reference)
        report = json.loads(report_json)

        assert "report_date" in report
        assert "cars" in report
        assert len(report["cars"]) == 1
        assert report["cars"][0]["car_id"] == "CAR-2025-001"

    def test_json_computed_fields(self):
        """Test JSON includes computed fields."""
        car = CAR(
            car_id="CAR-001",
            audit_name="Test",
            finding_title="Test",
            severity="High",
            auditee_dept="IT",
            owner="Test",
            due_date="2025-05-01",
            status="Open",
            open_date="2025-04-15",
        )
        reference = datetime(2025, 5, 31)
        report_json = generate_json_report([car], reference)
        report = json.loads(report_json)

        car_data = report["cars"][0]
        assert "days_open" in car_data
        assert "days_overdue" in car_data
        assert "is_overdue" in car_data
        assert "escalation_level" in car_data
        assert car_data["is_overdue"] is True
        assert car_data["days_overdue"] == 30


class TestEscalationThresholds:
    """Tests for ESCALATION_THRESHOLDS constant."""

    def test_all_severities_present(self):
        """Test all severity levels have thresholds."""
        expected = {"Critical", "High", "Medium", "Low"}
        assert set(ESCALATION_THRESHOLDS.keys()) == expected

    def test_all_levels_present(self):
        """Test all escalation levels defined for each severity."""
        for severity, thresholds in ESCALATION_THRESHOLDS.items():
            assert "level_2" in thresholds
            assert "level_3" in thresholds
            assert "level_4" in thresholds

    def test_critical_has_shortest_thresholds(self):
        """Test Critical severity has shortest escalation thresholds."""
        critical = ESCALATION_THRESHOLDS["Critical"]
        low = ESCALATION_THRESHOLDS["Low"]
        assert critical["level_2"] < low["level_2"]
        assert critical["level_3"] < low["level_3"]
        assert critical["level_4"] < low["level_4"]
