#!/usr/bin/env python3
"""Tests for readiness_calculator.py"""

import json
import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from readiness_calculator import (
    ReadinessFactors,
    generate_report,
    get_mitigation_strategies,
    get_readiness_interpretation,
)


class TestReadinessFactors:
    """Tests for ReadinessFactors dataclass."""

    def test_valid_scores(self):
        """Test creating ReadinessFactors with valid scores."""
        factors = ReadinessFactors(leadership=8, culture=6, capacity=5, history=7, resources=9)
        assert factors.leadership == 8
        assert factors.culture == 6
        assert factors.capacity == 5
        assert factors.history == 7
        assert factors.resources == 9

    def test_invalid_score_above_10(self):
        """Test that scores above 10 raise ValueError."""
        with pytest.raises(ValueError, match="leadership must be between 1 and 10"):
            ReadinessFactors(leadership=11, culture=5, capacity=5, history=5, resources=5)

    def test_invalid_score_below_1(self):
        """Test that scores below 1 raise ValueError."""
        with pytest.raises(ValueError, match="culture must be between 1 and 10"):
            ReadinessFactors(leadership=5, culture=0, capacity=5, history=5, resources=5)

    def test_weighted_score_calculation(self):
        """Test weighted score calculation."""
        factors = ReadinessFactors(
            leadership=8,  # 30% weight
            culture=6,  # 25% weight
            capacity=5,  # 20% weight
            history=7,  # 15% weight
            resources=9,  # 10% weight
        )
        # Expected: (8*30 + 6*25 + 5*20 + 7*15 + 9*10) / 100 = 6.85
        expected = (8 * 30 + 6 * 25 + 5 * 20 + 7 * 15 + 9 * 10) / 100
        assert factors.weighted_score == pytest.approx(expected)

    def test_simple_average_calculation(self):
        """Test simple average calculation."""
        factors = ReadinessFactors(leadership=10, culture=8, capacity=6, history=4, resources=2)
        assert factors.simple_average == 6.0

    def test_get_weak_factors_none(self):
        """Test get_weak_factors returns empty when all scores >= 6."""
        factors = ReadinessFactors(leadership=8, culture=7, capacity=6, history=9, resources=10)
        assert factors.get_weak_factors() == []

    def test_get_weak_factors_some(self):
        """Test get_weak_factors identifies low-scoring factors."""
        factors = ReadinessFactors(
            leadership=8,
            culture=4,  # weak
            capacity=3,  # weak
            history=7,
            resources=9,
        )
        weak = factors.get_weak_factors()
        assert len(weak) == 2
        assert ("Organizational Culture", 4) in weak
        assert ("Capacity", 3) in weak

    def test_get_status_high(self):
        """Test status for high scores."""
        factors = ReadinessFactors(leadership=8, culture=8, capacity=8, history=8, resources=8)
        assert factors.get_status(8.0) == "✅"

    def test_get_status_medium(self):
        """Test status for medium scores."""
        factors = ReadinessFactors(leadership=6, culture=6, capacity=6, history=6, resources=6)
        assert factors.get_status(6.0) == "🟡"

    def test_get_status_low(self):
        """Test status for low scores."""
        factors = ReadinessFactors(leadership=3, culture=3, capacity=3, history=3, resources=3)
        assert factors.get_status(3.0) == "🔴"

    def test_custom_weights(self):
        """Test custom weights are applied correctly."""
        custom_weights = {
            "leadership": 40,
            "culture": 20,
            "capacity": 20,
            "history": 10,
            "resources": 10,
        }
        factors = ReadinessFactors(leadership=10, culture=5, capacity=5, history=5, resources=5, weights=custom_weights)
        # Expected: (10*40 + 5*20 + 5*20 + 5*10 + 5*10) / 100 = 7.0
        assert factors.weighted_score == 7.0

    def test_invalid_weights_sum(self):
        """Test that weights not summing to 100 raise ValueError."""
        invalid_weights = {
            "leadership": 30,
            "culture": 25,
            "capacity": 20,
            "history": 15,
            "resources": 5,  # Sum = 95
        }
        with pytest.raises(ValueError, match="Weights must sum to 100"):
            ReadinessFactors(leadership=5, culture=5, capacity=5, history=5, resources=5, weights=invalid_weights)


class TestGetMitigationStrategies:
    """Tests for get_mitigation_strategies function."""

    def test_leadership_strategies(self):
        """Test mitigation strategies for Leadership Commitment."""
        strategies = get_mitigation_strategies("Leadership Commitment")
        assert len(strategies) > 0
        assert any("executive" in s.lower() or "leadership" in s.lower() for s in strategies)

    def test_culture_strategies(self):
        """Test mitigation strategies for Organizational Culture."""
        strategies = get_mitigation_strategies("Organizational Culture")
        assert len(strategies) > 0
        assert any("cultur" in s.lower() for s in strategies)

    def test_capacity_strategies(self):
        """Test mitigation strategies for Capacity."""
        strategies = get_mitigation_strategies("Capacity")
        assert len(strategies) > 0
        assert any("phase" in s.lower() or "resource" in s.lower() for s in strategies)

    def test_history_strategies(self):
        """Test mitigation strategies for Change History."""
        strategies = get_mitigation_strategies("Change History")
        assert len(strategies) > 0
        assert any("past" in s.lower() for s in strategies)

    def test_resources_strategies(self):
        """Test mitigation strategies for Resources."""
        strategies = get_mitigation_strategies("Resources")
        assert len(strategies) > 0
        assert any("resource" in s.lower() for s in strategies)

    def test_unknown_factor(self):
        """Test that unknown factors return empty list."""
        strategies = get_mitigation_strategies("Unknown Factor")
        assert strategies == []


class TestGetReadinessInterpretation:
    """Tests for get_readiness_interpretation function."""

    def test_high_readiness(self):
        """Test interpretation for high readiness score."""
        level, desc, rec = get_readiness_interpretation(8.5)
        assert level == "High Readiness"
        assert "proceed" in rec.lower() or "confidence" in rec.lower()

    def test_moderate_readiness(self):
        """Test interpretation for moderate readiness score."""
        level, desc, rec = get_readiness_interpretation(7.0)
        assert level == "Moderate Readiness"
        assert "attention" in rec.lower() or "gap" in rec.lower()

    def test_low_readiness(self):
        """Test interpretation for low readiness score."""
        level, desc, rec = get_readiness_interpretation(5.0)
        assert level == "Low Readiness"
        assert "preparation" in rec.lower() or "delay" in rec.lower()

    def test_critical_readiness(self):
        """Test interpretation for critical readiness score."""
        level, desc, rec = get_readiness_interpretation(3.0)
        assert level == "Critical Risk"
        assert "reassess" in rec.lower() or "not ready" in desc.lower()


class TestGenerateReport:
    """Tests for generate_report function."""

    def test_markdown_format(self):
        """Test markdown report generation."""
        factors = ReadinessFactors(leadership=8, culture=6, capacity=5, history=7, resources=9)
        report = generate_report(factors, "markdown")

        assert "# Change Readiness Assessment Report" in report
        assert "Leadership Commitment" in report
        assert "Organizational Culture" in report
        assert "Mitigation Strategies" in report or "Risk Areas" in report

    def test_json_format(self):
        """Test JSON report generation."""
        factors = ReadinessFactors(leadership=8, culture=4, capacity=3, history=7, resources=9)
        report = generate_report(factors, "json")

        data = json.loads(report)
        assert "scores" in data
        assert data["scores"]["leadership"] == 8
        assert "weighted_score" in data
        assert "weak_factors" in data
        assert len(data["weak_factors"]) == 2  # culture and capacity

    def test_report_includes_weak_factors(self):
        """Test that report identifies weak factors."""
        factors = ReadinessFactors(
            leadership=8,
            culture=3,  # weak
            capacity=5,
            history=7,
            resources=9,
        )
        report = generate_report(factors, "markdown")
        assert "Organizational Culture" in report
        assert "Requires immediate attention" in report or "3/10" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
