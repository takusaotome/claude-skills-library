#!/usr/bin/env python3
"""Tests for stakeholder_analyzer.py"""

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from stakeholder_analyzer import Stakeholder, generate_report, generate_sample_csv, load_stakeholders_from_csv


class TestStakeholder:
    """Tests for Stakeholder dataclass."""

    def test_valid_stakeholder(self):
        """Test creating Stakeholder with valid values."""
        s = Stakeholder(
            name="John Smith", role="CEO", department="Executive", power=5, interest=3, impact=5, attitude=5
        )
        assert s.name == "John Smith"
        assert s.role == "CEO"
        assert s.power == 5
        assert s.attitude == 5

    def test_invalid_power_above_5(self):
        """Test that power above 5 raises ValueError."""
        with pytest.raises(ValueError, match="power must be between 1 and 5"):
            Stakeholder(name="Test", role="Role", department="Dept", power=6, interest=3, impact=3, attitude=3)

    def test_invalid_interest_below_1(self):
        """Test that interest below 1 raises ValueError."""
        with pytest.raises(ValueError, match="interest must be between 1 and 5"):
            Stakeholder(name="Test", role="Role", department="Dept", power=3, interest=0, impact=3, attitude=3)

    def test_quadrant_manage_closely(self):
        """Test quadrant assignment for high power, high interest."""
        s = Stakeholder(name="Test", role="Role", department="Dept", power=4, interest=4, impact=3, attitude=3)
        assert s.quadrant == "Manage Closely"

    def test_quadrant_keep_satisfied(self):
        """Test quadrant assignment for high power, low interest."""
        s = Stakeholder(name="Test", role="Role", department="Dept", power=4, interest=2, impact=3, attitude=3)
        assert s.quadrant == "Keep Satisfied"

    def test_quadrant_keep_informed(self):
        """Test quadrant assignment for low power, high interest."""
        s = Stakeholder(name="Test", role="Role", department="Dept", power=2, interest=4, impact=3, attitude=3)
        assert s.quadrant == "Keep Informed"

    def test_quadrant_monitor(self):
        """Test quadrant assignment for low power, low interest."""
        s = Stakeholder(name="Test", role="Role", department="Dept", power=2, interest=2, impact=3, attitude=3)
        assert s.quadrant == "Monitor"

    def test_attitude_labels(self):
        """Test attitude label mapping."""
        attitudes = {
            1: "Resistor",
            2: "Skeptic",
            3: "Neutral",
            4: "Supporter",
            5: "Champion",
        }
        for att_val, att_label in attitudes.items():
            s = Stakeholder(
                name="Test", role="Role", department="Dept", power=3, interest=3, impact=3, attitude=att_val
            )
            assert s.attitude_label == att_label

    def test_priority_score_calculation(self):
        """Test priority score calculation."""
        s = Stakeholder(
            name="Test",
            role="Role",
            department="Dept",
            power=5,
            interest=4,
            impact=3,
            attitude=2,  # Skeptic
        )
        # Priority = power + interest + impact + (6 - attitude)
        # = 5 + 4 + 3 + (6 - 2) = 16
        assert s.priority_score == 16

    def test_engagement_strategy_champion(self):
        """Test engagement strategies for champions."""
        s = Stakeholder(name="Test", role="Role", department="Dept", power=5, interest=5, impact=5, attitude=5)
        strategies = s.get_engagement_strategy()
        assert any("advocate" in st.lower() or "influence" in st.lower() for st in strategies)

    def test_engagement_strategy_resistor(self):
        """Test engagement strategies for resistors."""
        s = Stakeholder(name="Test", role="Role", department="Dept", power=3, interest=4, impact=4, attitude=1)
        strategies = s.get_engagement_strategy()
        assert any("concern" in st.lower() or "address" in st.lower() for st in strategies)


class TestLoadStakeholdersFromCSV:
    """Tests for load_stakeholders_from_csv function."""

    def test_load_valid_csv(self):
        """Test loading stakeholders from valid CSV."""
        csv_content = """name,role,department,power,interest,impact,attitude
John Smith,CEO,Executive,5,3,5,5
Jane Doe,CIO,IT,5,5,5,4"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            f.flush()

            stakeholders = load_stakeholders_from_csv(f.name)

            assert len(stakeholders) == 2
            assert stakeholders[0].name == "John Smith"
            assert stakeholders[1].name == "Jane Doe"
            assert stakeholders[0].attitude == 5
            assert stakeholders[1].attitude == 4

            Path(f.name).unlink()

    def test_load_csv_with_mixed_case_headers(self):
        """Test loading CSV with mixed-case headers."""
        csv_content = """Name,Role,Department,Power,Interest,Impact,Attitude
Test User,Manager,Sales,3,4,3,3"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            f.flush()

            stakeholders = load_stakeholders_from_csv(f.name)

            assert len(stakeholders) == 1
            assert stakeholders[0].name == "Test User"

            Path(f.name).unlink()

    def test_load_csv_skips_invalid_rows(self, capsys):
        """Test that invalid rows are skipped with warning."""
        csv_content = """name,role,department,power,interest,impact,attitude
Valid User,Manager,Sales,3,4,3,3
Invalid User,Manager,Sales,10,4,3,3"""  # power=10 is invalid

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            f.flush()

            stakeholders = load_stakeholders_from_csv(f.name)

            assert len(stakeholders) == 1
            assert stakeholders[0].name == "Valid User"

            captured = capsys.readouterr()
            assert "Warning" in captured.err or "Skipping" in captured.err

            Path(f.name).unlink()


class TestGenerateSampleCSV:
    """Tests for generate_sample_csv function."""

    def test_sample_csv_format(self):
        """Test that sample CSV has correct format."""
        sample = generate_sample_csv()

        assert "name,role,department,power,interest,impact,attitude" in sample
        assert "CEO" in sample or "CIO" in sample

    def test_sample_csv_is_valid(self):
        """Test that sample CSV can be loaded."""
        sample = generate_sample_csv()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(sample)
            f.flush()

            stakeholders = load_stakeholders_from_csv(f.name)
            assert len(stakeholders) > 0

            Path(f.name).unlink()


class TestGenerateReport:
    """Tests for generate_report function."""

    def get_sample_stakeholders(self):
        """Get sample stakeholders for testing."""
        return [
            Stakeholder("CEO", "Chief Executive", "Executive", 5, 3, 5, 5),
            Stakeholder("Manager", "Department Manager", "Sales", 3, 4, 4, 2),
            Stakeholder("User", "End User", "Finance", 1, 4, 2, 3),
        ]

    def test_markdown_format(self):
        """Test markdown report generation."""
        stakeholders = self.get_sample_stakeholders()
        report = generate_report(stakeholders, "markdown")

        assert "# Stakeholder Analysis Report" in report
        assert "Power-Interest Matrix" in report
        assert "CEO" in report
        assert "Manager" in report

    def test_json_format(self):
        """Test JSON report generation."""
        stakeholders = self.get_sample_stakeholders()
        report = generate_report(stakeholders, "json")

        data = json.loads(report)
        assert "summary" in data
        assert "stakeholders" in data
        assert len(data["stakeholders"]) == 3
        assert data["summary"]["total_stakeholders"] == 3

    def test_empty_stakeholders(self):
        """Test report generation with no stakeholders."""
        report = generate_report([], "markdown")
        assert "No stakeholders" in report

    def test_report_includes_quadrants(self):
        """Test that report includes all quadrant sections."""
        stakeholders = self.get_sample_stakeholders()
        report = generate_report(stakeholders, "markdown")

        assert "Manage Closely" in report
        assert "Keep Satisfied" in report
        assert "Keep Informed" in report
        assert "Monitor" in report

    def test_report_identifies_at_risk_stakeholders(self):
        """Test that report identifies resistors/skeptics."""
        stakeholders = self.get_sample_stakeholders()
        report = generate_report(stakeholders, "markdown")

        # Manager is a skeptic (attitude=2)
        assert "Stakeholders Requiring Conversion" in report or "Skeptic" in report

    def test_report_sorted_by_priority(self):
        """Test that JSON stakeholders are sorted by priority."""
        stakeholders = self.get_sample_stakeholders()
        report = generate_report(stakeholders, "json")

        data = json.loads(report)
        priorities = [s["priority_score"] for s in data["stakeholders"]]
        assert priorities == sorted(priorities, reverse=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
