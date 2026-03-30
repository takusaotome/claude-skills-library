#!/usr/bin/env python3
"""
Tests for IT System ROI Calculator.
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from it_roi_calculator import (
    FinancialMetrics,
    ITROICalculator,
    ProjectData,
    format_currency,
    format_currency_jp,
)


class TestITROICalculator:
    """Test cases for ITROICalculator class."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance for tests."""
        return ITROICalculator()

    def test_calculate_roi_positive(self, calculator):
        """Test ROI calculation with positive returns."""
        total_benefits = 12_000_000
        total_investment = 7_500_000
        roi = calculator.calculate_roi(total_benefits, total_investment)
        assert roi == pytest.approx(60.0, rel=0.01)

    def test_calculate_roi_negative(self, calculator):
        """Test ROI calculation with negative returns."""
        total_benefits = 5_000_000
        total_investment = 7_500_000
        roi = calculator.calculate_roi(total_benefits, total_investment)
        assert roi == pytest.approx(-33.33, rel=0.01)

    def test_calculate_roi_zero_investment(self, calculator):
        """Test ROI calculation with zero investment (edge case)."""
        roi = calculator.calculate_roi(1_000_000, 0)
        assert roi == 0.0

    def test_calculate_npv_positive(self, calculator):
        """Test NPV calculation with positive cash flows."""
        cash_flows = [-50_000_000, 15_000_000, 20_000_000, 20_000_000, 20_000_000, 20_000_000]
        discount_rate = 0.10
        npv = calculator.calculate_npv(cash_flows, discount_rate)
        assert npv > 0

    def test_calculate_npv_negative(self, calculator):
        """Test NPV calculation with insufficient cash flows."""
        cash_flows = [-100_000_000, 10_000_000, 10_000_000, 10_000_000, 10_000_000, 10_000_000]
        discount_rate = 0.10
        npv = calculator.calculate_npv(cash_flows, discount_rate)
        assert npv < 0

    def test_calculate_npv_zero_discount_rate(self, calculator):
        """Test NPV calculation with zero discount rate."""
        cash_flows = [-50_000_000, 20_000_000, 20_000_000, 20_000_000]
        discount_rate = 0.0
        npv = calculator.calculate_npv(cash_flows, discount_rate)
        assert npv == pytest.approx(10_000_000, rel=0.01)

    def test_calculate_irr(self, calculator):
        """Test IRR calculation."""
        cash_flows = [-50_000_000, 15_000_000, 20_000_000, 20_000_000, 20_000_000, 20_000_000]
        irr = calculator.calculate_irr(cash_flows)
        assert 0.20 < irr < 0.35

    def test_calculate_payback_period_within_period(self, calculator):
        """Test payback period when recovered within the analysis period."""
        initial_investment = 50_000_000
        annual_cash_flows = [15_000_000, 20_000_000, 20_000_000, 20_000_000, 20_000_000]
        payback = calculator.calculate_payback_period(initial_investment, annual_cash_flows)
        assert 2 < payback < 3

    def test_calculate_payback_period_not_recovered(self, calculator):
        """Test payback period when investment is not recovered."""
        initial_investment = 100_000_000
        annual_cash_flows = [5_000_000, 5_000_000, 5_000_000]
        payback = calculator.calculate_payback_period(initial_investment, annual_cash_flows)
        assert payback == float("inf")

    def test_calculate_all_metrics(self, calculator):
        """Test calculation of all financial metrics."""
        initial_investment = 50_000_000
        annual_operating_cost = 5_000_000
        annual_benefits = [12_000_000, 18_000_000, 20_000_000, 20_000_000, 20_000_000]
        discount_rate = 0.10

        metrics = calculator.calculate_all_metrics(
            initial_investment, annual_operating_cost, annual_benefits, discount_rate
        )

        assert isinstance(metrics, FinancialMetrics)
        assert metrics.total_benefits == 90_000_000
        assert metrics.total_costs == 75_000_000
        assert metrics.roi > 0
        assert len(metrics.cash_flows) == 6

    def test_sensitivity_analysis(self, calculator):
        """Test sensitivity analysis with multiple scenarios."""
        project_data = ProjectData(
            project_name="Test Project",
            initial_investment=50_000_000,
            annual_operating_cost=5_000_000,
            annual_benefits={"year1": 15_000_000, "year2": 20_000_000, "year3": 20_000_000},
            discount_rate=0.10,
        )

        base_metrics = calculator.calculate_all_metrics(
            project_data.initial_investment,
            project_data.annual_operating_cost,
            list(project_data.annual_benefits.values()),
            project_data.discount_rate,
        )

        sensitivity = calculator.sensitivity_analysis(base_metrics, project_data)

        assert "optimistic" in sensitivity
        assert "base" in sensitivity
        assert "pessimistic" in sensitivity
        assert "worst_case" in sensitivity

        assert sensitivity["optimistic"].roi > sensitivity["base"].roi
        assert sensitivity["base"].roi > sensitivity["pessimistic"].roi


class TestFormatCurrency:
    """Test cases for currency formatting functions."""

    def test_format_currency_millions(self):
        """Test formatting millions."""
        assert format_currency(5_000_000) == "$5.00M"

    def test_format_currency_thousands(self):
        """Test formatting thousands."""
        assert format_currency(50_000) == "$50.0K"

    def test_format_currency_small(self):
        """Test formatting small amounts."""
        assert format_currency(500) == "$500"

    def test_format_currency_jp_oku(self):
        """Test Japanese formatting for amounts >= 1億円."""
        assert format_currency_jp(100_000_000) == "1.0億円"

    def test_format_currency_jp_man(self):
        """Test Japanese formatting for amounts in 万円."""
        assert format_currency_jp(50_000_000) == "5,000万円"


class TestProjectData:
    """Test cases for ProjectData dataclass."""

    def test_project_data_creation(self):
        """Test ProjectData instantiation."""
        project = ProjectData(
            project_name="ERP Renewal",
            initial_investment=100_000_000,
            annual_operating_cost=10_000_000,
            annual_benefits={"year1": 30_000_000, "year2": 40_000_000},
            discount_rate=0.12,
        )

        assert project.project_name == "ERP Renewal"
        assert project.initial_investment == 100_000_000
        assert project.discount_rate == 0.12


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
