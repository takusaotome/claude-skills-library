#!/usr/bin/env python3
"""Tests for kotter_assessment.py"""

import json
import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from kotter_assessment import KotterScore, generate_report, get_recommendations


class TestKotterScore:
    """Tests for KotterScore dataclass."""

    def test_valid_scores(self):
        """Test creating KotterScore with valid scores."""
        score = KotterScore(
            urgency=4,
            coalition=3,
            vision=4,
            communicate=2,
            empower=2,
            wins=1,
            sustain=1,
            anchor=1,
        )
        assert score.urgency == 4
        assert score.coalition == 3
        assert score.vision == 4
        assert score.communicate == 2
        assert score.empower == 2
        assert score.wins == 1
        assert score.sustain == 1
        assert score.anchor == 1

    def test_invalid_score_above_5(self):
        """Test that scores above 5 raise ValueError."""
        with pytest.raises(ValueError, match="urgency must be between 1 and 5"):
            KotterScore(
                urgency=6,
                coalition=3,
                vision=3,
                communicate=3,
                empower=3,
                wins=3,
                sustain=3,
                anchor=3,
            )

    def test_invalid_score_below_1(self):
        """Test that scores below 1 raise ValueError."""
        with pytest.raises(ValueError, match="coalition must be between 1 and 5"):
            KotterScore(
                urgency=3,
                coalition=0,
                vision=3,
                communicate=3,
                empower=3,
                wins=3,
                sustain=3,
                anchor=3,
            )

    def test_total_calculation(self):
        """Test total score calculation."""
        score = KotterScore(
            urgency=5,
            coalition=4,
            vision=4,
            communicate=3,
            empower=3,
            wins=2,
            sustain=2,
            anchor=1,
        )
        assert score.total == 24

    def test_max_score(self):
        """Test max score is 40."""
        score = KotterScore(
            urgency=5,
            coalition=5,
            vision=5,
            communicate=5,
            empower=5,
            wins=5,
            sustain=5,
            anchor=5,
        )
        assert score.max_score == 40
        assert score.total == 40

    def test_percentage_calculation(self):
        """Test percentage calculation."""
        score = KotterScore(
            urgency=4,
            coalition=4,
            vision=4,
            communicate=4,
            empower=4,
            wins=4,
            sustain=4,
            anchor=4,
        )
        # Total = 32, percentage = 32/40 * 100 = 80%
        assert score.percentage == 80.0

    def test_current_phase_phase1(self):
        """Test current phase identification for Phase 1."""
        score = KotterScore(
            urgency=2,
            coalition=2,
            vision=2,
            communicate=1,
            empower=1,
            wins=1,
            sustain=1,
            anchor=1,
        )
        assert "Phase 1" in score.current_phase

    def test_current_phase_phase2(self):
        """Test current phase identification for Phase 2."""
        score = KotterScore(
            urgency=4,
            coalition=4,
            vision=4,
            communicate=2,
            empower=2,
            wins=2,
            sustain=1,
            anchor=1,
        )
        assert "Phase 2" in score.current_phase

    def test_current_phase_phase3(self):
        """Test current phase identification for Phase 3."""
        score = KotterScore(
            urgency=4,
            coalition=4,
            vision=4,
            communicate=4,
            empower=4,
            wins=4,
            sustain=3,
            anchor=3,
        )
        assert "Phase 3" in score.current_phase

    def test_weakest_step_early_step(self):
        """Test weakest step identification for early low-scoring step."""
        score = KotterScore(
            urgency=2,
            coalition=4,
            vision=4,
            communicate=4,
            empower=4,
            wins=4,
            sustain=4,
            anchor=4,
        )
        num, name, step_score = score.weakest_step
        assert num == 1
        assert "Urgency" in name
        assert step_score == 2

    def test_weakest_step_all_good(self):
        """Test weakest step when all scores >= 3."""
        score = KotterScore(
            urgency=3,
            coalition=4,
            vision=5,
            communicate=3,
            empower=4,
            wins=3,
            sustain=4,
            anchor=5,
        )
        num, name, step_score = score.weakest_step
        # Should return the lowest (urgency, communicate, or wins at 3)
        assert step_score == 3

    def test_get_status_high(self):
        """Test status for high scores."""
        score = KotterScore(
            urgency=4,
            coalition=4,
            vision=4,
            communicate=4,
            empower=4,
            wins=4,
            sustain=4,
            anchor=4,
        )
        assert score.get_status(4) == "✅"
        assert score.get_status(5) == "✅"

    def test_get_status_medium(self):
        """Test status for medium scores."""
        score = KotterScore(
            urgency=3,
            coalition=3,
            vision=3,
            communicate=3,
            empower=3,
            wins=3,
            sustain=3,
            anchor=3,
        )
        assert score.get_status(3) == "🟡"

    def test_get_status_low(self):
        """Test status for low scores."""
        score = KotterScore(
            urgency=2,
            coalition=2,
            vision=2,
            communicate=2,
            empower=2,
            wins=2,
            sustain=2,
            anchor=2,
        )
        assert score.get_status(2) == "🔴"
        assert score.get_status(1) == "🔴"


class TestGetRecommendations:
    """Tests for get_recommendations function."""

    def test_step1_recommendations(self):
        """Test recommendations for Step 1."""
        recs = get_recommendations(1, 2)
        assert len(recs) == 5
        assert any("urgency" in r.lower() or "threat" in r.lower() for r in recs)

    def test_step2_recommendations(self):
        """Test recommendations for Step 2."""
        recs = get_recommendations(2, 2)
        assert len(recs) == 5
        assert any("coalition" in r.lower() or "leader" in r.lower() for r in recs)

    def test_step6_recommendations(self):
        """Test recommendations for Step 6."""
        recs = get_recommendations(6, 2)
        assert len(recs) == 5
        assert any("win" in r.lower() for r in recs)

    def test_low_score_more_recommendations(self):
        """Test that lower scores get more recommendations."""
        low_score_recs = get_recommendations(1, 2)
        high_score_recs = get_recommendations(1, 4)
        assert len(low_score_recs) > len(high_score_recs)

    def test_moderate_score_recommendations(self):
        """Test recommendations for moderate score."""
        recs = get_recommendations(3, 3)
        assert len(recs) == 3


class TestGenerateReport:
    """Tests for generate_report function."""

    def test_markdown_format(self):
        """Test markdown report generation."""
        score = KotterScore(
            urgency=4,
            coalition=3,
            vision=4,
            communicate=2,
            empower=2,
            wins=1,
            sustain=1,
            anchor=1,
        )
        report = generate_report(score, "markdown")

        assert "# Kotter 8-Step Change Assessment Report" in report
        assert "Create Urgency" in report
        assert "Build Guiding Coalition" in report
        assert "Priority Focus" in report

    def test_json_format(self):
        """Test JSON report generation."""
        score = KotterScore(
            urgency=4,
            coalition=3,
            vision=4,
            communicate=2,
            empower=2,
            wins=1,
            sustain=1,
            anchor=1,
        )
        report = generate_report(score, "json")

        data = json.loads(report)
        assert "scores" in data
        assert data["scores"]["step1_urgency"] == 4
        assert "weakest_step" in data
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0

    def test_strong_progress_interpretation(self):
        """Test interpretation for high progress."""
        score = KotterScore(
            urgency=5,
            coalition=4,
            vision=4,
            communicate=4,
            empower=4,
            wins=4,
            sustain=4,
            anchor=4,
        )
        report = generate_report(score, "markdown")
        assert "Strong Progress" in report

    def test_critical_gaps_interpretation(self):
        """Test interpretation for low progress."""
        score = KotterScore(
            urgency=1,
            coalition=1,
            vision=1,
            communicate=1,
            empower=1,
            wins=1,
            sustain=1,
            anchor=1,
        )
        report = generate_report(score, "markdown")
        assert "Critical Gaps" in report

    def test_report_includes_japanese(self):
        """Test that report includes Japanese translations."""
        score = KotterScore(
            urgency=3,
            coalition=3,
            vision=3,
            communicate=3,
            empower=3,
            wins=3,
            sustain=3,
            anchor=3,
        )
        report = generate_report(score, "markdown")
        assert "危機感を高める" in report  # Step 1 Japanese
        assert "変革推進チームを作る" in report  # Step 2 Japanese


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
