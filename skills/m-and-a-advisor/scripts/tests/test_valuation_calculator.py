"""Tests for valuation_calculator.py"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from valuation_calculator import (
    ComparableAnalysis,
    ComparableResult,
    DCFResult,
    DCFValuation,
    SynergyNPVCalculator,
    WACCCalculator,
    WACCParameters,
)


class TestWACCParameters:
    """Tests for WACCParameters dataclass"""

    def test_cost_of_equity_calculation(self):
        """Test CAPM cost of equity calculation"""
        params = WACCParameters(
            risk_free_rate=0.04,
            equity_risk_premium=0.05,
            beta=1.2,
            size_premium=0.01,
            cost_of_debt=0.05,
            tax_rate=0.25,
            market_value_equity=100,
            market_value_debt=50,
        )
        # Re = Rf + β × ERP + Size Premium = 0.04 + 1.2 × 0.05 + 0.01 = 0.11
        assert abs(params.cost_of_equity - 0.11) < 0.0001

    def test_wacc_calculation(self):
        """Test WACC calculation"""
        params = WACCParameters(
            risk_free_rate=0.04,
            equity_risk_premium=0.05,
            beta=1.0,
            size_premium=0.01,
            cost_of_debt=0.06,
            tax_rate=0.25,
            market_value_equity=70,
            market_value_debt=30,
        )
        # Re = 0.04 + 1.0 × 0.05 + 0.01 = 0.10
        # After-tax Rd = 0.06 × (1 - 0.25) = 0.045
        # WACC = 0.7 × 0.10 + 0.3 × 0.045 = 0.07 + 0.0135 = 0.0835
        assert abs(params.wacc - 0.0835) < 0.0001

    def test_wacc_zero_total_capital(self):
        """Test WACC returns 0 when total capital is 0"""
        params = WACCParameters(
            risk_free_rate=0.04,
            equity_risk_premium=0.05,
            beta=1.0,
            size_premium=0.01,
            cost_of_debt=0.06,
            tax_rate=0.25,
            market_value_equity=0,
            market_value_debt=0,
        )
        assert params.wacc == 0


class TestWACCCalculator:
    """Tests for WACCCalculator"""

    def test_calculate_returns_all_components(self):
        """Test calculate method returns all expected components"""
        params = WACCParameters(
            risk_free_rate=0.0425,
            equity_risk_premium=0.055,
            beta=1.2,
            size_premium=0.0175,
            cost_of_debt=0.05,
            tax_rate=0.25,
            market_value_equity=100,
            market_value_debt=50,
        )
        calculator = WACCCalculator(params)
        result = calculator.calculate()

        assert "risk_free_rate" in result
        assert "equity_risk_premium" in result
        assert "beta" in result
        assert "size_premium" in result
        assert "cost_of_equity" in result
        assert "cost_of_debt_pre_tax" in result
        assert "cost_of_debt_after_tax" in result
        assert "equity_weight" in result
        assert "debt_weight" in result
        assert "wacc" in result

    def test_generate_report_contains_sections(self):
        """Test report contains expected sections"""
        params = WACCParameters(
            risk_free_rate=0.04,
            equity_risk_premium=0.05,
            beta=1.0,
            size_premium=0.01,
            cost_of_debt=0.05,
            tax_rate=0.25,
            market_value_equity=100,
            market_value_debt=50,
        )
        calculator = WACCCalculator(params)
        report = calculator.generate_report()

        assert "# WACC Calculation Report" in report
        assert "## Cost of Equity (CAPM)" in report
        assert "## Cost of Debt" in report
        assert "## WACC Calculation" in report


class TestDCFValuation:
    """Tests for DCFValuation"""

    def test_terminal_value_calculation(self):
        """Test Gordon Growth Model terminal value"""
        dcf = DCFValuation(
            fcf_projections=[100, 110, 121],
            wacc=0.10,
            terminal_growth_rate=0.02,
            net_debt=50,
        )
        # TV = FCF(n) × (1 + g) / (WACC - g) = 121 × 1.02 / 0.08 = 1542.75
        tv = dcf.calculate_terminal_value()
        assert abs(tv - 1542.75) < 0.01

    def test_terminal_value_error_when_wacc_less_than_growth(self):
        """Test error raised when WACC <= terminal growth"""
        dcf = DCFValuation(
            fcf_projections=[100],
            wacc=0.02,
            terminal_growth_rate=0.03,
            net_debt=0,
        )
        with pytest.raises(ValueError, match="WACC must be greater than terminal growth rate"):
            dcf.calculate_terminal_value()

    def test_present_value_fcf_calculation(self):
        """Test present value of FCF calculation"""
        dcf = DCFValuation(
            fcf_projections=[100, 100, 100],
            wacc=0.10,
            terminal_growth_rate=0.02,
            net_debt=0,
        )
        pv_list = dcf.calculate_pv_fcf()

        # PV1 = 100 / 1.10 = 90.909
        # PV2 = 100 / 1.21 = 82.645
        # PV3 = 100 / 1.331 = 75.131
        assert abs(pv_list[0] - 90.909) < 0.01
        assert abs(pv_list[1] - 82.645) < 0.01
        assert abs(pv_list[2] - 75.131) < 0.01

    def test_full_dcf_calculation(self):
        """Test complete DCF valuation"""
        dcf = DCFValuation(
            fcf_projections=[100, 110, 121],
            wacc=0.10,
            terminal_growth_rate=0.02,
            net_debt=200,
            shares_outstanding=10,
        )
        result = dcf.calculate()

        assert isinstance(result, DCFResult)
        assert result.pv_fcf > 0
        assert result.terminal_value > 0
        assert result.pv_terminal_value > 0
        assert result.enterprise_value > 0
        assert result.net_debt == 200
        assert result.equity_value == result.enterprise_value - result.net_debt
        assert result.per_share_value == result.equity_value / 10

    def test_sensitivity_analysis_returns_matrix(self):
        """Test sensitivity analysis returns proper matrix"""
        dcf = DCFValuation(
            fcf_projections=[100, 110, 121],
            wacc=0.10,
            terminal_growth_rate=0.02,
            net_debt=50,
        )
        matrix, wacc_values, growth_values = dcf.sensitivity_analysis(
            wacc_range=(0.08, 0.12),
            growth_range=(0.01, 0.03),
            steps=3,
        )

        assert len(wacc_values) == 3
        assert len(growth_values) == 3
        assert len(matrix) == 3
        assert len(matrix[0]) == 3

    def test_generate_report_contains_sections(self):
        """Test report contains expected sections"""
        dcf = DCFValuation(
            fcf_projections=[100, 110, 121],
            wacc=0.10,
            terminal_growth_rate=0.02,
            net_debt=50,
        )
        report = dcf.generate_report("Test Company")

        assert "# DCF Valuation Analysis" in report
        assert "Test Company" in report
        assert "## Key Assumptions" in report
        assert "## Projected Free Cash Flow" in report
        assert "## Terminal Value" in report
        assert "## Enterprise Value Bridge" in report
        assert "## Sensitivity Analysis" in report


class TestComparableAnalysis:
    """Tests for ComparableAnalysis"""

    def test_calculate_multiples(self):
        """Test trading multiples calculation"""
        target = {"ebitda": 100, "revenue": 500, "ebit": 80, "net_debt": 100}
        comps = [
            {
                "company": "Comp A",
                "enterprise_value": 1000,
                "ebitda": 100,
                "ebit": 80,
                "revenue": 400,
                "net_income": 50,
                "market_cap": 800,
            },
            {
                "company": "Comp B",
                "enterprise_value": 1500,
                "ebitda": 150,
                "ebit": 120,
                "revenue": 600,
                "net_income": 75,
                "market_cap": 1200,
            },
        ]

        analyzer = ComparableAnalysis(target, comps)
        multiples = analyzer.calculate_multiples()

        assert len(multiples) == 2
        assert multiples[0].company == "Comp A"
        assert abs(multiples[0].ev_ebitda - 10.0) < 0.01  # 1000/100
        assert abs(multiples[0].ev_revenue - 2.5) < 0.01  # 1000/400

    def test_calculate_statistics(self):
        """Test statistics calculation (mean, median)"""
        target = {"ebitda": 100, "revenue": 500, "ebit": 80, "net_debt": 100}
        comps = [
            {
                "company": "Comp A",
                "enterprise_value": 1000,
                "ebitda": 100,
                "ebit": 80,
                "revenue": 400,
                "net_income": 50,
                "market_cap": 800,
            },
            {
                "company": "Comp B",
                "enterprise_value": 1200,
                "ebitda": 100,
                "ebit": 80,
                "revenue": 400,
                "net_income": 60,
                "market_cap": 1000,
            },
        ]

        analyzer = ComparableAnalysis(target, comps)
        stats = analyzer.calculate_statistics()

        assert "ev_ebitda" in stats
        assert "mean" in stats["ev_ebitda"]
        assert "median" in stats["ev_ebitda"]
        # Mean of 10x and 12x = 11x
        assert abs(stats["ev_ebitda"]["mean"] - 11.0) < 0.01

    def test_apply_multiples_to_target(self):
        """Test implied valuation calculation"""
        target = {"ebitda": 100, "revenue": 500, "ebit": 80, "net_debt": 100}
        comps = [
            {
                "company": "Comp A",
                "enterprise_value": 1000,
                "ebitda": 100,
                "ebit": 80,
                "revenue": 500,
                "net_income": 50,
                "market_cap": 800,
            },
        ]

        analyzer = ComparableAnalysis(target, comps)
        implied = analyzer.apply_multiples_to_target()

        assert "ev_ebitda" in implied
        # Target EBITDA 100 × 10x = EV 1000, - Net Debt 100 = Equity 900
        assert abs(implied["ev_ebitda"]["equity_value_median"] - 900) < 1

    def test_generate_report_contains_sections(self):
        """Test report contains expected sections"""
        target = {"ebitda": 100, "revenue": 500, "ebit": 80, "net_debt": 100}
        comps = [
            {
                "company": "Comp A",
                "enterprise_value": 1000,
                "ebitda": 100,
                "ebit": 80,
                "revenue": 400,
                "net_income": 50,
                "market_cap": 800,
            },
        ]

        analyzer = ComparableAnalysis(target, comps)
        report = analyzer.generate_report("Target Inc")

        assert "# Comparable Companies Analysis" in report
        assert "Target Inc" in report
        assert "## Comparable Companies" in report
        assert "## Multiple Statistics" in report
        assert "## Implied Valuation" in report


class TestSynergyNPVCalculator:
    """Tests for SynergyNPVCalculator"""

    def test_calculate_annual_synergies(self):
        """Test annual synergy calculation with realization ramp"""
        synergies = [
            {
                "category": "Cost",
                "item": "Overhead reduction",
                "annual_impact": 100,
                "probability": 0.8,
                "realization_year1": 0.25,
                "realization_year2": 0.75,
                "realization_year3": 1.0,
            }
        ]
        calculator = SynergyNPVCalculator(synergies, discount_rate=0.08)
        annual = calculator.calculate_annual_synergies(years=3)

        # Y1: 100 × 0.8 × 0.25 = 20
        # Y2: 100 × 0.8 × 0.75 = 60
        # Y3: 100 × 0.8 × 1.0 = 80
        assert abs(annual[0] - 20) < 0.01
        assert abs(annual[1] - 60) < 0.01
        assert abs(annual[2] - 80) < 0.01

    def test_calculate_npv(self):
        """Test NPV calculation"""
        synergies = [
            {
                "category": "Cost",
                "item": "Test",
                "annual_impact": 100,
                "probability": 1.0,
                "realization_year1": 1.0,
                "realization_year2": 1.0,
                "realization_year3": 1.0,
            }
        ]
        calculator = SynergyNPVCalculator(synergies, discount_rate=0.10, realization_costs=50)
        npv = calculator.calculate_npv(years=3)

        # PV = 100/1.1 + 100/1.21 + 100/1.331 - 50
        # PV = 90.91 + 82.64 + 75.13 - 50 = 198.68
        assert abs(npv - 198.68) < 0.5

    def test_generate_report_contains_sections(self):
        """Test report contains expected sections"""
        synergies = [
            {
                "category": "Cost",
                "item": "Test synergy",
                "annual_impact": 100,
                "probability": 0.8,
                "realization_year1": 0.5,
                "realization_year2": 1.0,
                "realization_year3": 1.0,
            }
        ]
        calculator = SynergyNPVCalculator(synergies, discount_rate=0.08)
        report = calculator.generate_report()

        assert "# Synergy NPV Analysis" in report
        assert "## Synergy Items" in report
        assert "## Annual Synergy Realization" in report
        assert "## NPV Summary" in report
