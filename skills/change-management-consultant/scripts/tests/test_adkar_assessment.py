#!/usr/bin/env python3
"""Tests for adkar_assessment.py"""

import json
import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from adkar_assessment import ADKARScore, generate_report, get_recommendations


class TestADKARScore:
    """Tests for ADKARScore dataclass."""

    def test_valid_scores(self):
        """Test creating ADKARScore with valid scores."""
        score = ADKARScore(awareness=8, desire=4, knowledge=2, ability=0, reinforcement=0, stakeholder="Test Group")
        assert score.awareness == 8
        assert score.desire == 4
        assert score.knowledge == 2
        assert score.ability == 0
        assert score.reinforcement == 0
        assert score.stakeholder == "Test Group"

    def test_invalid_score_above_10(self):
        """Test that scores above 10 raise ValueError."""
        with pytest.raises(ValueError, match="awareness must be between 0 and 10"):
            ADKARScore(awareness=11, desire=5, knowledge=5, ability=5, reinforcement=5)

    def test_invalid_score_below_0(self):
        """Test that scores below 0 raise ValueError."""
        with pytest.raises(ValueError, match="desire must be between 0 and 10"):
            ADKARScore(awareness=5, desire=-1, knowledge=5, ability=5, reinforcement=5)

    def test_total_calculation(self):
        """Test total score calculation."""
        score = ADKARScore(awareness=8, desire=6, knowledge=4, ability=2, reinforcement=0)
        assert score.total == 20

    def test_average_calculation(self):
        """Test average score calculation."""
        score = ADKARScore(awareness=10, desire=8, knowledge=6, ability=4, reinforcement=2)
        assert score.average == 6.0

    def test_barrier_point_identification(self):
        """Test barrier point is lowest score."""
        score = ADKARScore(awareness=8, desire=4, knowledge=2, ability=5, reinforcement=6)
        assert score.barrier_point == "Knowledge"

    def test_barrier_point_first_element_wins_tie(self):
        """Test barrier point selection with tied scores."""
        score = ADKARScore(awareness=3, desire=3, knowledge=5, ability=5, reinforcement=5)
        # With ties, the first element alphabetically wins (Awareness before Desire)
        assert score.barrier_point == "Awareness"

    def test_barrier_score(self):
        """Test barrier score value."""
        score = ADKARScore(awareness=8, desire=4, knowledge=2, ability=5, reinforcement=6)
        assert score.barrier_score == 2

    def test_get_status_high(self):
        """Test status for high scores."""
        score = ADKARScore(awareness=8, desire=8, knowledge=8, ability=8, reinforcement=8)
        assert score.get_status(8) == "✅"
        assert score.get_status(10) == "✅"

    def test_get_status_medium(self):
        """Test status for medium scores."""
        score = ADKARScore(awareness=5, desire=5, knowledge=5, ability=5, reinforcement=5)
        assert score.get_status(5) == "🟡"
        assert score.get_status(7) == "🟡"

    def test_get_status_low(self):
        """Test status for low scores."""
        score = ADKARScore(awareness=3, desire=3, knowledge=3, ability=3, reinforcement=3)
        assert score.get_status(3) == "🔴"
        assert score.get_status(0) == "🔴"


class TestGetRecommendations:
    """Tests for get_recommendations function."""

    def test_awareness_recommendations(self):
        """Test recommendations for Awareness barrier."""
        recs = get_recommendations("Awareness", 2)
        assert len(recs) == 5
        assert any("business case" in r.lower() for r in recs)

    def test_desire_recommendations(self):
        """Test recommendations for Desire barrier."""
        recs = get_recommendations("Desire", 3)
        assert len(recs) == 5
        assert any("wiifm" in r.lower() for r in recs)

    def test_knowledge_recommendations(self):
        """Test recommendations for Knowledge barrier."""
        recs = get_recommendations("Knowledge", 4)
        assert len(recs) == 3
        assert any("training" in r.lower() for r in recs)

    def test_ability_recommendations(self):
        """Test recommendations for Ability barrier."""
        recs = get_recommendations("Ability", 5)
        assert len(recs) == 3
        assert any("practice" in r.lower() for r in recs)

    def test_reinforcement_recommendations(self):
        """Test recommendations for Reinforcement barrier."""
        recs = get_recommendations("Reinforcement", 6)
        assert len(recs) == 2
        assert any("celebrate" in r.lower() or "recognize" in r.lower() for r in recs)

    def test_low_score_more_recommendations(self):
        """Test that lower scores get more recommendations."""
        low_score_recs = get_recommendations("Awareness", 2)
        high_score_recs = get_recommendations("Awareness", 7)
        assert len(low_score_recs) > len(high_score_recs)


class TestGenerateReport:
    """Tests for generate_report function."""

    def test_markdown_format(self):
        """Test markdown report generation."""
        score = ADKARScore(awareness=8, desire=4, knowledge=2, ability=0, reinforcement=0)
        report = generate_report(score, "markdown")

        assert "# ADKAR Assessment Report" in report
        assert "Stakeholder" in report
        assert "Awareness" in report
        assert "Barrier Point" in report
        assert "Knowledge" in report  # barrier point

    def test_json_format(self):
        """Test JSON report generation."""
        score = ADKARScore(awareness=8, desire=4, knowledge=2, ability=0, reinforcement=0, stakeholder="Sales Team")
        report = generate_report(score, "json")

        data = json.loads(report)
        assert data["stakeholder"] == "Sales Team"
        assert data["scores"]["awareness"] == 8
        assert data["barrier_point"] == "Knowledge"
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0

    def test_high_readiness_interpretation(self):
        """Test interpretation for high readiness."""
        score = ADKARScore(awareness=9, desire=8, knowledge=9, ability=8, reinforcement=8)
        report = generate_report(score, "markdown")
        assert "High Change Readiness" in report

    def test_low_readiness_interpretation(self):
        """Test interpretation for low readiness."""
        score = ADKARScore(awareness=3, desire=2, knowledge=2, ability=1, reinforcement=0)
        report = generate_report(score, "markdown")
        assert "Critical" in report or "Low Readiness" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
