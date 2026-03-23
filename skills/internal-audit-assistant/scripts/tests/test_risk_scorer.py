"""Tests for risk_scorer.py module."""

import json
import tempfile
from pathlib import Path

import pytest

from ..risk_scorer import (
    DEFAULT_WEIGHTS,
    AuditableEntity,
    RiskFactors,
    calculate_risk_score,
    generate_json_report,
    generate_markdown_report,
    get_audit_frequency,
    get_risk_level,
    parse_csv,
)


class TestRiskFactors:
    """Tests for RiskFactors dataclass."""

    def test_risk_factors_creation(self):
        """Test creating RiskFactors instance."""
        factors = RiskFactors(
            inherent_risk=4.0,
            control_environment=3.0,
            financial_impact=5.0,
            regulatory_impact=4.0,
            last_audit_date=2.0,
            management_concern=3.0,
        )
        assert factors.inherent_risk == 4.0
        assert factors.control_environment == 3.0
        assert factors.financial_impact == 5.0


class TestCalculateRiskScore:
    """Tests for calculate_risk_score function."""

    def test_maximum_score(self):
        """Test maximum risk score (all factors at 5)."""
        factors = RiskFactors(
            inherent_risk=5.0,
            control_environment=5.0,
            financial_impact=5.0,
            regulatory_impact=5.0,
            last_audit_date=5.0,
            management_concern=5.0,
        )
        score = calculate_risk_score(factors)
        assert score == 5.0

    def test_minimum_score(self):
        """Test minimum risk score (all factors at 1)."""
        factors = RiskFactors(
            inherent_risk=1.0,
            control_environment=1.0,
            financial_impact=1.0,
            regulatory_impact=1.0,
            last_audit_date=1.0,
            management_concern=1.0,
        )
        score = calculate_risk_score(factors)
        assert score == 1.0

    def test_weighted_calculation(self):
        """Test that weights are applied correctly."""
        # Set all factors to their weight's denominator for easy calculation
        factors = RiskFactors(
            inherent_risk=4.0,  # 0.25 weight
            control_environment=3.0,  # 0.20 weight
            financial_impact=5.0,  # 0.20 weight
            regulatory_impact=4.0,  # 0.20 weight
            last_audit_date=2.0,  # 0.10 weight
            management_concern=3.0,  # 0.05 weight
        )
        score = calculate_risk_score(factors)
        expected = 4.0 * 0.25 + 3.0 * 0.20 + 5.0 * 0.20 + 4.0 * 0.20 + 2.0 * 0.10 + 3.0 * 0.05
        assert score == round(expected, 2)

    def test_custom_weights(self):
        """Test calculation with custom weights."""
        factors = RiskFactors(
            inherent_risk=5.0,
            control_environment=1.0,
            financial_impact=1.0,
            regulatory_impact=1.0,
            last_audit_date=1.0,
            management_concern=1.0,
        )
        custom_weights = {
            "inherent_risk": 1.0,
            "control_environment": 0.0,
            "financial_impact": 0.0,
            "regulatory_impact": 0.0,
            "last_audit_date": 0.0,
            "management_concern": 0.0,
        }
        score = calculate_risk_score(factors, custom_weights)
        assert score == 5.0


class TestGetRiskLevel:
    """Tests for get_risk_level function."""

    def test_critical_level(self):
        """Test Critical risk level threshold."""
        assert get_risk_level(5.0) == "Critical"
        assert get_risk_level(4.0) == "Critical"
        assert get_risk_level(4.5) == "Critical"

    def test_high_level(self):
        """Test High risk level threshold."""
        assert get_risk_level(3.9) == "High"
        assert get_risk_level(3.0) == "High"
        assert get_risk_level(3.5) == "High"

    def test_medium_level(self):
        """Test Medium risk level threshold."""
        assert get_risk_level(2.9) == "Medium"
        assert get_risk_level(2.0) == "Medium"
        assert get_risk_level(2.5) == "Medium"

    def test_low_level(self):
        """Test Low risk level threshold."""
        assert get_risk_level(1.9) == "Low"
        assert get_risk_level(1.0) == "Low"
        assert get_risk_level(1.5) == "Low"


class TestGetAuditFrequency:
    """Tests for get_audit_frequency function."""

    def test_critical_frequency(self):
        """Test audit frequency for Critical risk."""
        assert get_audit_frequency("Critical") == "Annual (required)"

    def test_high_frequency(self):
        """Test audit frequency for High risk."""
        assert get_audit_frequency("High") == "Every 1-2 years"

    def test_medium_frequency(self):
        """Test audit frequency for Medium risk."""
        assert get_audit_frequency("Medium") == "Every 2-3 years"

    def test_low_frequency(self):
        """Test audit frequency for Low risk."""
        assert get_audit_frequency("Low") == "Every 3-5 years"

    def test_unknown_level(self):
        """Test audit frequency for unknown risk level."""
        assert get_audit_frequency("Unknown") == "N/A"


class TestParseCSV:
    """Tests for parse_csv function."""

    def test_parse_valid_csv(self):
        """Test parsing a valid CSV file."""
        csv_content = """entity_id,entity_name,department,entity_type,last_audit,inherent_risk,control_environment,financial_impact,regulatory_impact,last_audit_date,management_concern
IT-01,Access Management,IT,System,2024-01,5,3,4,5,2,4
FIN-01,Accounts Payable,Finance,Process,2024-03,4,3,4,4,2,3"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_path = Path(f.name)

        try:
            entities = parse_csv(temp_path)
            assert len(entities) == 2
            assert entities[0].entity_id == "IT-01"
            assert entities[0].entity_name == "Access Management"
            assert entities[0].risk_factors.inherent_risk == 5.0
            assert entities[1].department == "Finance"
        finally:
            temp_path.unlink()

    def test_parse_csv_with_defaults(self):
        """Test parsing CSV with missing optional columns."""
        csv_content = """entity_id,entity_name,department,entity_type
IT-01,Access Management,IT,System"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_path = Path(f.name)

        try:
            entities = parse_csv(temp_path)
            assert len(entities) == 1
            # Default value should be 3
            assert entities[0].risk_factors.inherent_risk == 3.0
        finally:
            temp_path.unlink()


class TestGenerateMarkdownReport:
    """Tests for generate_markdown_report function."""

    def test_report_structure(self):
        """Test markdown report contains required sections."""
        factors = RiskFactors(
            inherent_risk=4.0,
            control_environment=3.0,
            financial_impact=4.0,
            regulatory_impact=4.0,
            last_audit_date=3.0,
            management_concern=3.0,
        )
        entity = AuditableEntity(
            entity_id="IT-01",
            entity_name="Access Management",
            department="IT",
            entity_type="System",
            risk_factors=factors,
        )

        report = generate_markdown_report([entity])

        assert "# Risk Assessment Matrix" in report
        assert "## Summary" in report
        assert "## Risk Matrix" in report
        assert "## Risk Factor Weights" in report
        assert "IT-01" in report
        assert "Access Management" in report

    def test_report_sorting(self):
        """Test entities are sorted by risk score descending."""
        high_risk = RiskFactors(5.0, 5.0, 5.0, 5.0, 5.0, 5.0)
        low_risk = RiskFactors(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)

        entities = [
            AuditableEntity("LOW-01", "Low Risk", "Dept", "Process", low_risk),
            AuditableEntity("HIGH-01", "High Risk", "Dept", "Process", high_risk),
        ]

        report = generate_markdown_report(entities)

        # HIGH-01 should appear before LOW-01 in the report
        high_pos = report.find("HIGH-01")
        low_pos = report.find("LOW-01")
        assert high_pos < low_pos


class TestGenerateJsonReport:
    """Tests for generate_json_report function."""

    def test_json_structure(self):
        """Test JSON report structure."""
        factors = RiskFactors(4.0, 3.0, 4.0, 4.0, 3.0, 3.0)
        entity = AuditableEntity(
            entity_id="IT-01",
            entity_name="Access Management",
            department="IT",
            entity_type="System",
            risk_factors=factors,
        )

        report_json = generate_json_report([entity])
        report = json.loads(report_json)

        assert "entities" in report
        assert "weights" in report
        assert len(report["entities"]) == 1
        assert report["entities"][0]["entity_id"] == "IT-01"
        assert "risk_score" in report["entities"][0]
        assert "risk_level" in report["entities"][0]

    def test_json_risk_factors_included(self):
        """Test JSON includes risk factor details."""
        factors = RiskFactors(4.0, 3.0, 4.0, 4.0, 3.0, 3.0)
        entity = AuditableEntity(
            entity_id="IT-01",
            entity_name="Access Management",
            department="IT",
            entity_type="System",
            risk_factors=factors,
        )

        report_json = generate_json_report([entity])
        report = json.loads(report_json)

        entity_data = report["entities"][0]
        assert "risk_factors" in entity_data
        assert entity_data["risk_factors"]["inherent_risk"] == 4.0


class TestDefaultWeights:
    """Tests for DEFAULT_WEIGHTS constant."""

    def test_weights_sum_to_one(self):
        """Test that default weights sum to 1.0."""
        total = sum(DEFAULT_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_all_weights_present(self):
        """Test all expected weight keys are present."""
        expected_keys = {
            "inherent_risk",
            "control_environment",
            "financial_impact",
            "regulatory_impact",
            "last_audit_date",
            "management_concern",
        }
        assert set(DEFAULT_WEIGHTS.keys()) == expected_keys
