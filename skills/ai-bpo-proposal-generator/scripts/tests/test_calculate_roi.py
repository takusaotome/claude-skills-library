"""
Tests for calculate_roi.py
"""

import json
from pathlib import Path

import pytest
from calculate_roi import (
    BENCHMARKS,
    calculate_current_state_cost,
    calculate_future_state_cost,
    calculate_implementation_cost,
    calculate_npv,
    calculate_roi,
)


class TestCalculateCurrentStateCost:
    """Tests for current state cost calculation."""

    def test_invoice_processing_cost(self):
        """Should calculate invoice processing costs."""
        result = calculate_current_state_cost(process_type="invoice_processing", monthly_volume=1000, hourly_rate=35.0)
        assert "annual_volume" in result
        assert result["annual_volume"] == 12000
        assert "total_annual_cost_usd" in result
        assert result["total_annual_cost_usd"] > 0

    def test_includes_error_costs(self):
        """Should include error costs in total."""
        result = calculate_current_state_cost(process_type="invoice_processing", monthly_volume=1000)
        assert result["annual_error_cost_usd"] > 0
        assert result["error_rate_pct"] > 0

    def test_calculates_fte_equivalent(self):
        """Should calculate FTE equivalent correctly."""
        result = calculate_current_state_cost(process_type="invoice_processing", monthly_volume=1000)
        assert "fte_equivalent" in result
        # 12000 invoices * 15 min / 60 = 3000 hours / 2080 = ~1.44 FTE
        assert result["fte_equivalent"] > 1.0
        assert result["fte_equivalent"] < 2.0

    def test_unknown_process_uses_defaults(self):
        """Should use default benchmarks for unknown process."""
        result = calculate_current_state_cost(process_type="unknown_process", monthly_volume=100)
        assert result["total_annual_cost_usd"] > 0


class TestCalculateFutureStateCost:
    """Tests for future state cost calculation."""

    def test_includes_service_fee(self):
        """Should include service fee in total cost."""
        result = calculate_future_state_cost(
            process_type="invoice_processing",
            monthly_volume=1000,
            service_fee=60000,  # $5000/month
            automation_rate=0.85,
        )
        assert result["annual_service_fee_usd"] == 60000
        assert result["total_annual_cost_usd"] >= 60000

    def test_automation_reduces_labor(self):
        """Should reduce labor compared to current state."""
        current = calculate_current_state_cost("invoice_processing", 1000)
        future = calculate_future_state_cost("invoice_processing", 1000, 60000, 0.85)
        # Future labor cost should be less than current
        assert future["annual_labor_cost_usd"] < current["annual_labor_cost_usd"]

    def test_automation_rate_affects_result(self):
        """Higher automation rate should reduce labor costs."""
        result_low = calculate_future_state_cost("invoice_processing", 1000, 60000, 0.70)
        result_high = calculate_future_state_cost("invoice_processing", 1000, 60000, 0.95)
        assert result_high["annual_labor_cost_usd"] < result_low["annual_labor_cost_usd"]


class TestCalculateImplementationCost:
    """Tests for implementation cost calculation."""

    def test_basic_implementation_cost(self):
        """Should calculate implementation cost."""
        result = calculate_implementation_cost(service_count=3)
        assert "total_implementation_cost_usd" in result
        assert result["total_implementation_cost_usd"] > 0

    def test_complexity_affects_cost(self):
        """Higher complexity should increase costs."""
        low = calculate_implementation_cost(3, complexity="low")
        medium = calculate_implementation_cost(3, complexity="medium")
        high = calculate_implementation_cost(3, complexity="high")
        assert low["total_implementation_cost_usd"] < medium["total_implementation_cost_usd"]
        assert medium["total_implementation_cost_usd"] < high["total_implementation_cost_usd"]

    def test_service_count_affects_integration_cost(self):
        """More services should increase integration costs."""
        few = calculate_implementation_cost(service_count=2)
        many = calculate_implementation_cost(service_count=5)
        assert few["integration_development_usd"] < many["integration_development_usd"]


class TestCalculateNpv:
    """Tests for NPV calculation."""

    def test_positive_npv(self):
        """Should calculate positive NPV for good project."""
        npv = calculate_npv(annual_savings=100000, implementation_cost=75000, discount_rate=0.10, years=3)
        assert npv > 0

    def test_negative_npv(self):
        """Should calculate negative NPV for bad project."""
        npv = calculate_npv(annual_savings=10000, implementation_cost=100000, discount_rate=0.10, years=3)
        assert npv < 0

    def test_discount_rate_effect(self):
        """Higher discount rate should reduce NPV."""
        npv_low = calculate_npv(100000, 75000, 0.05, 3)
        npv_high = calculate_npv(100000, 75000, 0.15, 3)
        assert npv_high < npv_low


class TestCalculateRoi:
    """Tests for full ROI calculation."""

    def test_generates_valid_report(self, tmp_path):
        """Should generate valid ROI report from services file."""
        # Create services file
        services_data = {
            "selected_services": [
                {
                    "service_id": "fin-001",
                    "service_name": "Invoice Processing",
                    "base_monthly_fee_usd": 5000,
                    "estimated_automation_rate": 0.85,
                }
            ]
        }
        services_file = tmp_path / "services.json"
        with open(services_file, "w") as f:
            json.dump(services_data, f)

        report = calculate_roi(services_file=str(services_file), volumes={"invoices_per_month": 2000})

        assert "schema_version" in report
        assert "current_state" in report
        assert "future_state" in report
        assert "financial_summary" in report

    def test_calculates_payback_period(self, tmp_path):
        """Should calculate reasonable payback period."""
        services_data = {
            "selected_services": [
                {
                    "service_id": "fin-001",
                    "service_name": "Invoice Processing",
                    "base_monthly_fee_usd": 5000,
                    "estimated_automation_rate": 0.85,
                }
            ]
        }
        services_file = tmp_path / "services.json"
        with open(services_file, "w") as f:
            json.dump(services_data, f)

        report = calculate_roi(services_file=str(services_file))
        payback = report["financial_summary"]["payback_months"]
        assert payback > 0
        assert payback < 36  # Less than 3 years

    def test_saves_to_file(self, tmp_path):
        """Should save report to file when path provided."""
        services_data = {"selected_services": []}
        services_file = tmp_path / "services.json"
        with open(services_file, "w") as f:
            json.dump(services_data, f)

        output_file = tmp_path / "roi.json"
        calculate_roi(services_file=str(services_file), output_path=str(output_file))
        assert output_file.exists()
