"""
Tests for generate_cba.py
"""

import pytest
from generate_cba import (
    calculate_npv,
    calculate_payback_months,
    calculate_roi,
    format_currency,
    generate_cba,
    parse_benefits,
)


class TestCalculateROI:
    """Tests for ROI calculation."""

    def test_positive_roi(self):
        """Test ROI calculation with positive return."""
        roi = calculate_roi(total_benefit=15000, total_cost=10000)
        assert roi == 50.0

    def test_break_even_roi(self):
        """Test ROI calculation at break-even."""
        roi = calculate_roi(total_benefit=10000, total_cost=10000)
        assert roi == 0.0

    def test_negative_roi(self):
        """Test ROI calculation with negative return."""
        roi = calculate_roi(total_benefit=8000, total_cost=10000)
        assert roi == -20.0

    def test_high_roi(self):
        """Test ROI calculation with high return."""
        roi = calculate_roi(total_benefit=30000, total_cost=10000)
        assert roi == 200.0

    def test_zero_cost_roi(self):
        """Test ROI calculation with zero cost."""
        roi = calculate_roi(total_benefit=10000, total_cost=0)
        assert roi == 0.0


class TestCalculatePaybackMonths:
    """Tests for payback period calculation."""

    def test_standard_payback(self):
        """Test standard payback calculation."""
        months = calculate_payback_months(initial_cost=12000, monthly_benefit=1000)
        assert months == 12.0

    def test_quick_payback(self):
        """Test quick payback calculation."""
        months = calculate_payback_months(initial_cost=6000, monthly_benefit=2000)
        assert months == 3.0

    def test_fractional_payback(self):
        """Test fractional payback period."""
        months = calculate_payback_months(initial_cost=10000, monthly_benefit=3000)
        assert abs(months - 3.333) < 0.01

    def test_zero_benefit_payback(self):
        """Test payback with zero benefit."""
        months = calculate_payback_months(initial_cost=10000, monthly_benefit=0)
        assert months == float("inf")


class TestCalculateNPV:
    """Tests for NPV calculation."""

    def test_positive_npv(self):
        """Test NPV calculation with positive result."""
        npv = calculate_npv(
            initial_cost=10000,
            annual_benefit=5000,
            annual_cost=1000,
            years=5,
            discount_rate=0.10,
        )
        # Net annual cash flow = 5000 - 1000 = 4000
        # NPV should be positive
        assert npv > 0

    def test_negative_npv(self):
        """Test NPV calculation with negative result."""
        npv = calculate_npv(
            initial_cost=100000,
            annual_benefit=5000,
            annual_cost=3000,
            years=3,
            discount_rate=0.10,
        )
        # Net annual cash flow = 5000 - 3000 = 2000
        # Over 3 years, not enough to recover 100000
        assert npv < 0

    def test_npv_discount_impact(self):
        """Test that higher discount rate reduces NPV."""
        npv_low = calculate_npv(
            initial_cost=10000,
            annual_benefit=4000,
            annual_cost=0,
            years=5,
            discount_rate=0.05,
        )
        npv_high = calculate_npv(
            initial_cost=10000,
            annual_benefit=4000,
            annual_cost=0,
            years=5,
            discount_rate=0.15,
        )
        assert npv_low > npv_high

    def test_npv_years_impact(self):
        """Test that more years increases NPV for positive cash flow."""
        npv_short = calculate_npv(
            initial_cost=10000,
            annual_benefit=5000,
            annual_cost=1000,
            years=3,
            discount_rate=0.10,
        )
        npv_long = calculate_npv(
            initial_cost=10000,
            annual_benefit=5000,
            annual_cost=1000,
            years=7,
            discount_rate=0.10,
        )
        assert npv_long > npv_short


class TestParseBenefits:
    """Tests for benefits parsing."""

    def test_parse_single_benefit(self):
        """Test parsing a single benefit."""
        benefits = parse_benefits("Time Savings:5000")
        assert len(benefits) == 1
        assert benefits[0] == ("Time Savings", 5000.0)

    def test_parse_multiple_benefits(self):
        """Test parsing multiple benefits."""
        benefits = parse_benefits("Time Savings:5000,Cost Reduction:3000,Error Prevention:2000")
        assert len(benefits) == 3
        assert benefits[0] == ("Time Savings", 5000.0)
        assert benefits[1] == ("Cost Reduction", 3000.0)
        assert benefits[2] == ("Error Prevention", 2000.0)

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        benefits = parse_benefits("")
        assert len(benefits) == 0

    def test_parse_with_spaces(self):
        """Test parsing with extra spaces."""
        benefits = parse_benefits("  Benefit One : 1000 , Benefit Two : 2000  ")
        assert len(benefits) == 2
        assert benefits[0] == ("Benefit One", 1000.0)
        assert benefits[1] == ("Benefit Two", 2000.0)

    def test_parse_invalid_value(self):
        """Test parsing with invalid numeric value."""
        benefits = parse_benefits("Valid:1000,Invalid:abc,Also Valid:2000")
        assert len(benefits) == 2
        assert benefits[0] == ("Valid", 1000.0)
        assert benefits[1] == ("Also Valid", 2000.0)


class TestGenerateCBA:
    """Tests for CBA document generation."""

    def test_basic_cba(self):
        """Test generating a basic CBA document."""
        result = generate_cba(
            product="Server Upgrade",
            total_cost=50000,
            useful_life_years=5,
            annual_benefit=20000,
            benefit_description="Improved performance and reliability",
        )

        assert "# Cost-Benefit Analysis" in result
        assert "Server Upgrade" in result
        assert "$50,000.00" in result
        assert "Improved performance" in result
        assert "ROI" in result
        assert "Payback" in result
        assert "NPV" in result

    def test_cba_with_operating_costs(self):
        """Test CBA with annual operating costs."""
        result = generate_cba(
            product="Cloud Service",
            total_cost=10000,
            useful_life_years=3,
            annual_benefit=8000,
            benefit_description="Scalable infrastructure",
            annual_operating_cost=2000,
        )

        assert "Operating/Maintenance" in result
        assert "$2,000.00" in result

    def test_cba_with_training_cost(self):
        """Test CBA with training cost."""
        result = generate_cba(
            product="New Software",
            total_cost=15000,
            useful_life_years=4,
            annual_benefit=10000,
            benefit_description="Process automation",
            training_cost=3000,
        )

        assert "Training" in result
        assert "$3,000.00" in result

    def test_cba_with_benefits_breakdown(self):
        """Test CBA with detailed benefits breakdown."""
        result = generate_cba(
            product="CRM System",
            total_cost=30000,
            useful_life_years=5,
            annual_benefit=15000,
            benefit_description="Customer relationship improvements",
            benefits_breakdown="Sales Increase:8000,Time Savings:4000,Error Reduction:3000",
        )

        assert "Sales Increase" in result
        assert "Time Savings" in result
        assert "Error Reduction" in result

    def test_cba_recommendation_strong(self):
        """Test CBA generates strong recommendation for good ROI."""
        result = generate_cba(
            product="High ROI Investment",
            total_cost=10000,
            useful_life_years=3,
            annual_benefit=10000,  # 200% ROI
            benefit_description="High return investment",
        )

        assert "APPROVE" in result

    def test_cba_sensitivity_analysis(self):
        """Test CBA includes sensitivity analysis."""
        result = generate_cba(
            product="Test Product",
            total_cost=10000,
            useful_life_years=3,
            annual_benefit=5000,
            benefit_description="Test benefits",
        )

        assert "## Sensitivity Analysis" in result
        assert "Break-Even" in result
        assert "Benefit -20%" in result
        assert "Cost +20%" in result

    def test_cba_assumptions_section(self):
        """Test CBA includes assumptions."""
        result = generate_cba(
            product="Test",
            total_cost=5000,
            useful_life_years=3,
            annual_benefit=3000,
            benefit_description="Test",
        )

        assert "## Assumptions" in result
        assert "Useful life of 3 years" in result
