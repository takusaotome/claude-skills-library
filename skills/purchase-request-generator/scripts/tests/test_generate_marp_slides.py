"""
Tests for generate_marp_slides.py
"""

import pytest
from generate_marp_slides import (
    format_currency,
    generate_marp_slides,
    parse_list,
)


class TestParseList:
    """Tests for list parsing."""

    def test_parse_simple_list(self):
        """Test parsing a simple comma-separated list."""
        items = parse_list("A,B,C")
        assert items == ["A", "B", "C"]

    def test_parse_with_spaces(self):
        """Test parsing with extra spaces."""
        items = parse_list("  Item 1 , Item 2 , Item 3  ")
        assert items == ["Item 1", "Item 2", "Item 3"]

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        items = parse_list("")
        assert items == []

    def test_parse_single_item(self):
        """Test parsing single item."""
        items = parse_list("Single Item")
        assert items == ["Single Item"]

    def test_parse_with_empty_items(self):
        """Test parsing with empty items between commas."""
        items = parse_list("A,,B,  ,C")
        assert items == ["A", "B", "C"]


class TestGenerateMarpSlides:
    """Tests for MARP slide generation."""

    def test_basic_slides(self):
        """Test generating basic MARP slides."""
        result = generate_marp_slides(
            title="Purchase Request: Test Product",
            product="Test Product",
            total_cost=10000,
            roi_percent=150,
            payback_months=18,
            key_benefits=["Benefit 1", "Benefit 2", "Benefit 3"],
        )

        assert "---\nmarp: true" in result
        assert "Test Product" in result
        assert "$10,000.00" in result
        assert "150%" in result
        assert "18 months" in result

    def test_slides_include_theme(self):
        """Test that slides include MARP theme configuration."""
        result = generate_marp_slides(
            title="Test",
            product="Test",
            total_cost=1000,
            roi_percent=100,
            payback_months=12,
            key_benefits=["Test"],
        )

        assert "theme: default" in result
        assert "paginate: true" in result
        assert "style:" in result

    def test_slides_with_requester_info(self):
        """Test slides with requester information."""
        result = generate_marp_slides(
            title="Purchase Request",
            product="Software",
            total_cost=5000,
            roi_percent=200,
            payback_months=6,
            key_benefits=["Efficiency"],
            requester="John Doe",
            department="Engineering",
        )

        assert "John Doe" in result
        assert "Engineering" in result

    def test_slides_with_justification(self):
        """Test slides with business justification."""
        result = generate_marp_slides(
            title="Purchase Request",
            product="Hardware",
            total_cost=20000,
            roi_percent=80,
            payback_months=30,
            key_benefits=["Performance"],
            justification="Critical infrastructure upgrade needed to support growth",
        )

        assert "Business Justification" in result
        assert "Critical infrastructure" in result

    def test_slides_with_npv(self):
        """Test slides with NPV value."""
        result = generate_marp_slides(
            title="Test",
            product="Test",
            total_cost=10000,
            roi_percent=100,
            payback_months=24,
            key_benefits=["Test"],
            npv=5000,
        )

        assert "$5,000.00" in result
        assert "NPV" in result

    def test_slides_with_risks(self):
        """Test slides with risk information."""
        result = generate_marp_slides(
            title="Test",
            product="Test",
            total_cost=10000,
            roi_percent=100,
            payback_months=24,
            key_benefits=["Test"],
            risks=["Implementation delay", "Budget overrun"],
        )

        assert "Risk Assessment" in result
        assert "Implementation delay" in result
        assert "Budget overrun" in result

    def test_slides_with_alternatives(self):
        """Test slides with alternatives considered."""
        result = generate_marp_slides(
            title="Test",
            product="Product A",
            total_cost=10000,
            roi_percent=100,
            payback_months=24,
            key_benefits=["Test"],
            alternatives=["Product B", "Product C", "Do Nothing"],
        )

        assert "Alternatives Considered" in result
        assert "Product B" in result
        assert "Product C" in result

    def test_slides_strong_recommendation(self):
        """Test recommendation for high ROI and short payback."""
        result = generate_marp_slides(
            title="Test",
            product="Test",
            total_cost=10000,
            roi_percent=200,  # High ROI
            payback_months=12,  # Short payback
            key_benefits=["Test"],
        )

        assert "Strong Approval Recommended" in result

    def test_slides_moderate_recommendation(self):
        """Test recommendation for moderate metrics."""
        result = generate_marp_slides(
            title="Test",
            product="Test",
            total_cost=10000,
            roi_percent=60,  # Moderate ROI
            payback_months=30,  # Moderate payback
            key_benefits=["Test"],
        )

        assert "Approval Recommended" in result

    def test_slides_review_recommendation(self):
        """Test recommendation for weak metrics."""
        result = generate_marp_slides(
            title="Test",
            product="Test",
            total_cost=10000,
            roi_percent=30,  # Low ROI
            payback_months=48,  # Long payback
            key_benefits=["Test"],
        )

        assert "Review Recommended" in result

    def test_slides_key_benefits_list(self):
        """Test that all key benefits are included."""
        benefits = ["Improved efficiency", "Cost savings", "Better quality", "Faster delivery"]
        result = generate_marp_slides(
            title="Test",
            product="Test",
            total_cost=10000,
            roi_percent=100,
            payback_months=24,
            key_benefits=benefits,
        )

        for benefit in benefits:
            assert benefit in result

    def test_slides_implementation_timeline(self):
        """Test that implementation timeline is included."""
        result = generate_marp_slides(
            title="Test",
            product="Test",
            total_cost=10000,
            roi_percent=100,
            payback_months=24,
            key_benefits=["Test"],
        )

        assert "Implementation Timeline" in result
        assert "Approval" in result
        assert "Procurement" in result
        assert "Go-Live" in result

    def test_slides_questions_section(self):
        """Test that questions/contact section is included."""
        result = generate_marp_slides(
            title="Test",
            product="Test",
            total_cost=10000,
            roi_percent=100,
            payback_months=24,
            key_benefits=["Test"],
            requester="Contact Person",
        )

        assert "Questions?" in result
        assert "Contact Person" in result
        assert "Supporting Documents" in result
