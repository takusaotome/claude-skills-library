"""
Tests for generate_vendor_comparison.py
"""

import pytest
from generate_vendor_comparison import (
    calculate_weighted_score,
    format_currency,
    generate_vendor_comparison,
    parse_criteria,
    parse_scores,
    parse_vendors,
    parse_weights,
)


class TestParseVendors:
    """Tests for vendor parsing."""

    def test_parse_single_vendor(self):
        """Test parsing a single vendor."""
        vendors = parse_vendors("Dell:5000")
        assert vendors == {"Dell": 5000.0}

    def test_parse_multiple_vendors(self):
        """Test parsing multiple vendors."""
        vendors = parse_vendors("Dell:5000,HP:4800,Lenovo:5200")
        assert len(vendors) == 3
        assert vendors["Dell"] == 5000.0
        assert vendors["HP"] == 4800.0
        assert vendors["Lenovo"] == 5200.0

    def test_parse_with_spaces(self):
        """Test parsing with extra spaces."""
        vendors = parse_vendors("  Dell : 5000 , HP : 4800  ")
        assert vendors["Dell"] == 5000.0
        assert vendors["HP"] == 4800.0

    def test_parse_invalid_price(self):
        """Test parsing with invalid price."""
        vendors = parse_vendors("Dell:5000,HP:invalid,Lenovo:5200")
        assert len(vendors) == 2
        assert "HP" not in vendors


class TestParseCriteria:
    """Tests for criteria parsing."""

    def test_parse_criteria(self):
        """Test parsing criteria list."""
        criteria = parse_criteria("Price,Quality,Support,Warranty")
        assert len(criteria) == 4
        assert criteria == ["Price", "Quality", "Support", "Warranty"]

    def test_parse_criteria_with_spaces(self):
        """Test parsing criteria with spaces."""
        criteria = parse_criteria("  Price , Quality , Support  ")
        assert criteria == ["Price", "Quality", "Support"]

    def test_parse_empty_criteria(self):
        """Test parsing empty string."""
        criteria = parse_criteria("")
        assert criteria == []


class TestParseScores:
    """Tests for score parsing."""

    def test_parse_scores_single_vendor(self):
        """Test parsing scores for single vendor."""
        vendors = {"Dell": 5000}
        criteria = ["Price", "Quality"]
        scores = parse_scores("Dell:4,5", vendors, criteria)

        assert "Dell" in scores
        assert scores["Dell"]["Price"] == 4
        assert scores["Dell"]["Quality"] == 5

    def test_parse_scores_multiple_vendors(self):
        """Test parsing scores for multiple vendors."""
        vendors = {"Dell": 5000, "HP": 4800}
        criteria = ["Price", "Quality", "Support"]
        scores = parse_scores("Dell:4,5,3|HP:5,4,4", vendors, criteria)

        assert scores["Dell"]["Price"] == 4
        assert scores["Dell"]["Quality"] == 5
        assert scores["HP"]["Price"] == 5
        assert scores["HP"]["Support"] == 4

    def test_parse_scores_unknown_vendor(self):
        """Test that unknown vendors are ignored."""
        vendors = {"Dell": 5000}
        criteria = ["Price", "Quality"]
        scores = parse_scores("Dell:4,5|Unknown:3,3", vendors, criteria)

        assert "Dell" in scores
        assert "Unknown" not in scores


class TestParseWeights:
    """Tests for weight parsing."""

    def test_parse_weights(self):
        """Test parsing weights."""
        criteria = ["Price", "Quality", "Support"]
        weights = parse_weights("40,35,25", criteria)

        assert weights["Price"] == 0.40
        assert weights["Quality"] == 0.35
        assert weights["Support"] == 0.25

    def test_parse_weights_sum(self):
        """Test that parsed weights sum correctly."""
        criteria = ["A", "B", "C", "D"]
        weights = parse_weights("30,25,25,20", criteria)

        total = sum(weights.values())
        assert abs(total - 1.0) < 0.001


class TestCalculateWeightedScore:
    """Tests for weighted score calculation."""

    def test_calculate_weighted_score(self):
        """Test weighted score calculation."""
        scores = {"Price": 4, "Quality": 5, "Support": 3}
        weights = {"Price": 0.4, "Quality": 0.35, "Support": 0.25}

        weighted = calculate_weighted_score(scores, weights)
        # 4*0.4 + 5*0.35 + 3*0.25 = 1.6 + 1.75 + 0.75 = 4.1
        assert abs(weighted - 4.1) < 0.001

    def test_calculate_equal_weights(self):
        """Test with equal weights."""
        scores = {"A": 5, "B": 5, "C": 5}
        weights = {"A": 0.333, "B": 0.333, "C": 0.334}

        weighted = calculate_weighted_score(scores, weights)
        assert abs(weighted - 5.0) < 0.01

    def test_calculate_with_missing_criterion(self):
        """Test with missing criterion in weights."""
        scores = {"A": 4, "B": 5}
        weights = {"A": 0.5}  # B missing

        weighted = calculate_weighted_score(scores, weights)
        # Only A contributes: 4 * 0.5 = 2.0
        assert abs(weighted - 2.0) < 0.001


class TestGenerateVendorComparison:
    """Tests for vendor comparison document generation."""

    def test_basic_comparison(self):
        """Test generating a basic vendor comparison."""
        vendors = {"Dell": 5000, "HP": 4800}
        criteria = ["Price", "Quality"]
        scores = {
            "Dell": {"Price": 4, "Quality": 5},
            "HP": {"Price": 5, "Quality": 4},
        }
        weights = {"Price": 0.5, "Quality": 0.5}

        result = generate_vendor_comparison(
            vendors=vendors,
            criteria=criteria,
            scores=scores,
            weights=weights,
            product="Laptops",
        )

        assert "# Vendor Comparison Analysis" in result
        assert "Dell" in result
        assert "HP" in result
        assert "$5,000.00" in result
        assert "$4,800.00" in result
        assert "Laptops" in result

    def test_comparison_includes_recommendation(self):
        """Test that comparison includes recommendation."""
        vendors = {"Vendor A": 1000, "Vendor B": 1200}
        criteria = ["Quality"]
        scores = {
            "Vendor A": {"Quality": 5},
            "Vendor B": {"Quality": 3},
        }
        weights = {"Quality": 1.0}

        result = generate_vendor_comparison(
            vendors=vendors,
            criteria=criteria,
            scores=scores,
            weights=weights,
        )

        assert "Recommendation" in result
        assert "Vendor A" in result  # Should be recommended (higher score)

    def test_comparison_matrix_format(self):
        """Test that comparison matrix is properly formatted."""
        vendors = {"V1": 100, "V2": 200}
        criteria = ["A", "B"]
        scores = {
            "V1": {"A": 4, "B": 5},
            "V2": {"A": 3, "B": 4},
        }
        weights = {"A": 0.5, "B": 0.5}

        result = generate_vendor_comparison(
            vendors=vendors,
            criteria=criteria,
            scores=scores,
            weights=weights,
        )

        assert "## Detailed Comparison Matrix" in result
        assert "| A |" in result
        assert "| B |" in result

    def test_comparison_strengths_weaknesses(self):
        """Test that strengths and weaknesses are identified."""
        vendors = {"Vendor X": 500}
        criteria = ["Strong Point", "Weak Point", "Average"]
        scores = {
            "Vendor X": {"Strong Point": 5, "Weak Point": 2, "Average": 3},
        }
        weights = {"Strong Point": 0.33, "Weak Point": 0.33, "Average": 0.34}

        result = generate_vendor_comparison(
            vendors=vendors,
            criteria=criteria,
            scores=scores,
            weights=weights,
        )

        assert "Strengths and Weaknesses" in result
        assert "Strong Point" in result
        assert "Weak Point" in result

    def test_comparison_value_score(self):
        """Test that value score is calculated."""
        vendors = {"Cheap": 100, "Expensive": 500}
        criteria = ["Quality"]
        scores = {
            "Cheap": {"Quality": 4},
            "Expensive": {"Quality": 5},
        }
        weights = {"Quality": 1.0}

        result = generate_vendor_comparison(
            vendors=vendors,
            criteria=criteria,
            scores=scores,
            weights=weights,
        )

        assert "## Price Comparison" in result
        assert "Value Score" in result

    def test_comparison_scoring_scale(self):
        """Test that scoring scale explanation is included."""
        vendors = {"V1": 100}
        criteria = ["X"]
        scores = {"V1": {"X": 3}}
        weights = {"X": 1.0}

        result = generate_vendor_comparison(
            vendors=vendors,
            criteria=criteria,
            scores=scores,
            weights=weights,
        )

        assert "### Scoring Scale" in result
        assert "Excellent" in result
        assert "Poor" in result
