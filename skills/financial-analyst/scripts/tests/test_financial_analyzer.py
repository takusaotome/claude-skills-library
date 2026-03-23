"""
Tests for financial_analyzer.py
"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from financial_analyzer import (
    BudgetVarianceAnalyzer,
    DCFAnalyzer,
    FinancialData,
    FinancialRatioAnalyzer,
    RatioResult,
)


class TestFinancialRatioAnalyzer:
    """Tests for FinancialRatioAnalyzer class"""

    @pytest.fixture
    def sample_financial_data(self):
        """Sample financial data for testing"""
        return FinancialData(
            company="Test Corp",
            period="2024-Q4",
            total_assets=100_000_000,
            current_assets=40_000_000,
            cash=10_000_000,
            inventory=15_000_000,
            receivables=12_000_000,
            total_liabilities=60_000_000,
            current_liabilities=25_000_000,
            long_term_debt=30_000_000,
            total_equity=40_000_000,
            revenue=80_000_000,
            cost_of_goods_sold=48_000_000,
            gross_profit=32_000_000,
            operating_expenses=16_000_000,
            operating_income=16_000_000,
            interest_expense=2_000_000,
            net_income=10_000_000,
        )

    def test_calculate_all_ratios_returns_list(self, sample_financial_data):
        """Test that calculate_all_ratios returns a list of RatioResult"""
        analyzer = FinancialRatioAnalyzer(sample_financial_data)
        ratios = analyzer.calculate_all_ratios()

        assert isinstance(ratios, list)
        assert len(ratios) > 0
        assert all(isinstance(r, RatioResult) for r in ratios)

    def test_roe_calculation(self, sample_financial_data):
        """Test ROE calculation: Net Income / Equity"""
        analyzer = FinancialRatioAnalyzer(sample_financial_data)
        analyzer.calculate_all_ratios()

        roe = next((r for r in analyzer.ratios if r.name == "ROE"), None)
        assert roe is not None
        # 10M / 40M = 0.25 = 25%
        assert abs(roe.value - 0.25) < 0.001

    def test_current_ratio_calculation(self, sample_financial_data):
        """Test Current Ratio calculation: Current Assets / Current Liabilities"""
        analyzer = FinancialRatioAnalyzer(sample_financial_data)
        analyzer.calculate_all_ratios()

        current = next((r for r in analyzer.ratios if r.name == "Current Ratio"), None)
        assert current is not None
        # 40M / 25M = 1.6
        assert abs(current.value - 1.6) < 0.001

    def test_quick_ratio_calculation(self, sample_financial_data):
        """Test Quick Ratio calculation: (Current Assets - Inventory) / Current Liabilities"""
        analyzer = FinancialRatioAnalyzer(sample_financial_data)
        analyzer.calculate_all_ratios()

        quick = next((r for r in analyzer.ratios if r.name == "Quick Ratio"), None)
        assert quick is not None
        # (40M - 15M) / 25M = 1.0
        assert abs(quick.value - 1.0) < 0.001

    def test_safe_divide_zero_denominator(self, sample_financial_data):
        """Test safe division with zero denominator"""
        analyzer = FinancialRatioAnalyzer(sample_financial_data)

        # Positive numerator, zero denominator -> inf
        result = analyzer._safe_divide(100, 0)
        assert result == float("inf")

        # Zero numerator, zero denominator -> 0
        result = analyzer._safe_divide(0, 0)
        assert result == 0

    def test_generate_report_includes_company_info(self, sample_financial_data):
        """Test that generated report includes company information"""
        analyzer = FinancialRatioAnalyzer(sample_financial_data)
        analyzer.calculate_all_ratios()
        report = analyzer.generate_report()

        assert "Test Corp" in report
        assert "2024-Q4" in report
        assert "Financial Ratio Analysis Report" in report


class TestDCFAnalyzer:
    """Tests for DCFAnalyzer class"""

    @pytest.fixture
    def sample_dcf_data(self):
        """Sample DCF data for testing"""
        return {
            "initial_investment": 50_000_000,
            "cash_flows": [10_000_000, 15_000_000, 20_000_000, 22_000_000, 25_000_000],
            "discount_rate": 0.10,
            "terminal_growth_rate": 0.02,
        }

    def test_npv_positive_project(self, sample_dcf_data):
        """Test NPV calculation for a positive project"""
        analyzer = DCFAnalyzer(
            initial_investment=sample_dcf_data["initial_investment"],
            cash_flows=sample_dcf_data["cash_flows"],
            discount_rate=sample_dcf_data["discount_rate"],
            terminal_growth_rate=sample_dcf_data["terminal_growth_rate"],
        )
        npv = analyzer.calculate_npv(include_terminal=False)

        # NPV should be positive for this project
        assert npv > 0

    def test_npv_without_terminal_value(self, sample_dcf_data):
        """Test NPV calculation without terminal value"""
        analyzer = DCFAnalyzer(
            initial_investment=sample_dcf_data["initial_investment"],
            cash_flows=sample_dcf_data["cash_flows"],
            discount_rate=sample_dcf_data["discount_rate"],
        )

        npv_no_terminal = analyzer.calculate_npv(include_terminal=False)
        npv_with_terminal = analyzer.calculate_npv(include_terminal=True)

        # NPV with terminal should be higher
        assert npv_with_terminal > npv_no_terminal

    def test_irr_calculation(self, sample_dcf_data):
        """Test IRR calculation converges to reasonable value"""
        analyzer = DCFAnalyzer(
            initial_investment=sample_dcf_data["initial_investment"],
            cash_flows=sample_dcf_data["cash_flows"],
            discount_rate=sample_dcf_data["discount_rate"],
        )
        irr = analyzer.calculate_irr()

        # IRR should be a reasonable rate (between 0% and 100%)
        assert 0 < irr < 1.0

    def test_payback_period_simple(self):
        """Test simple payback period calculation"""
        analyzer = DCFAnalyzer(
            initial_investment=100_000,
            cash_flows=[30_000, 30_000, 30_000, 30_000, 30_000],
            discount_rate=0.10,
        )
        payback = analyzer.calculate_payback_period(discounted=False)

        # Should be between 3 and 4 years (100k / 30k per year)
        assert 3 < payback < 4

    def test_payback_period_discounted(self):
        """Test discounted payback period is longer than simple"""
        analyzer = DCFAnalyzer(
            initial_investment=100_000,
            cash_flows=[30_000, 30_000, 30_000, 30_000, 30_000],
            discount_rate=0.10,
        )
        simple = analyzer.calculate_payback_period(discounted=False)
        discounted = analyzer.calculate_payback_period(discounted=True)

        # Discounted payback should be longer
        assert discounted > simple

    def test_wacc_calculation(self):
        """Test WACC calculation"""
        analyzer = DCFAnalyzer(
            initial_investment=100_000,
            cash_flows=[30_000],
            discount_rate=0.10,
        )
        wacc = analyzer.calculate_wacc(
            equity_value=60_000,
            debt_value=40_000,
            cost_of_equity=0.12,
            cost_of_debt=0.06,
            tax_rate=0.25,
        )

        # WACC = (60/100 * 0.12) + (40/100 * 0.06 * 0.75)
        # WACC = 0.072 + 0.018 = 0.09
        assert abs(wacc - 0.09) < 0.001

    def test_generate_report_includes_metrics(self, sample_dcf_data):
        """Test that report includes key metrics"""
        analyzer = DCFAnalyzer(
            initial_investment=sample_dcf_data["initial_investment"],
            cash_flows=sample_dcf_data["cash_flows"],
            discount_rate=sample_dcf_data["discount_rate"],
        )
        report = analyzer.generate_report("Test Project")

        assert "NPV" in report
        assert "IRR" in report
        assert "Payback" in report
        assert "Test Project" in report


class TestBudgetVarianceAnalyzer:
    """Tests for BudgetVarianceAnalyzer class"""

    @pytest.fixture
    def sample_budget_data(self):
        """Sample budget vs actual data"""
        actual = {
            "Product Revenue": 85_000_000,
            "Service Revenue": 15_000_000,
            "Material Costs": 35_000_000,
            "Labor Costs": 25_000_000,
        }
        budget = {
            "Product Revenue": 80_000_000,
            "Service Revenue": 18_000_000,
            "Material Costs": 30_000_000,
            "Labor Costs": 24_000_000,
        }
        return actual, budget

    def test_calculate_variances(self, sample_budget_data):
        """Test variance calculation"""
        actual, budget = sample_budget_data
        analyzer = BudgetVarianceAnalyzer(actual, budget, threshold_pct=5.0)
        variances = analyzer.calculate_variances()

        assert len(variances) == 4

    def test_favorable_revenue_variance(self, sample_budget_data):
        """Test that higher revenue is favorable"""
        actual, budget = sample_budget_data
        analyzer = BudgetVarianceAnalyzer(actual, budget, threshold_pct=5.0)
        variances = analyzer.calculate_variances()

        product_rev = next((v for v in variances if v["item"] == "Product Revenue"), None)
        assert product_rev is not None
        assert product_rev["variance"] == 5_000_000  # 85M - 80M
        assert product_rev["favorable"] is True

    def test_unfavorable_cost_variance(self, sample_budget_data):
        """Test that higher costs are unfavorable"""
        actual, budget = sample_budget_data
        analyzer = BudgetVarianceAnalyzer(actual, budget, threshold_pct=5.0)
        variances = analyzer.calculate_variances()

        material = next((v for v in variances if v["item"] == "Material Costs"), None)
        assert material is not None
        assert material["variance"] == 5_000_000  # 35M - 30M
        assert material["favorable"] is False

    def test_material_variance_flagging(self):
        """Test that material variances are flagged correctly"""
        actual = {"Revenue": 110_000}  # 10% above budget
        budget = {"Revenue": 100_000}
        analyzer = BudgetVarianceAnalyzer(actual, budget, threshold_pct=5.0)
        variances = analyzer.calculate_variances()

        assert variances[0]["material"] is True  # 10% > 5% threshold

    def test_generate_report_includes_summary(self, sample_budget_data):
        """Test that report includes variance summary"""
        actual, budget = sample_budget_data
        analyzer = BudgetVarianceAnalyzer(actual, budget)
        report = analyzer.generate_report()

        assert "Budget Variance Analysis Report" in report
        assert "Favorable" in report
        assert "Unfavorable" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
