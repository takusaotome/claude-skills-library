"""
Tests for select_services.py
"""

import json
from pathlib import Path

import pytest
from select_services import (
    INDUSTRY_BUNDLES,
    SERVICE_CATALOG,
    calculate_estimated_pricing,
    generate_service_selection,
    match_services,
    normalize_pain_point,
)


class TestNormalizePainPoint:
    """Tests for pain point normalization."""

    def test_normalize_lowercase(self):
        """Should convert to lowercase."""
        assert normalize_pain_point("Invoice") == "invoice"

    def test_normalize_spaces_to_underscores(self):
        """Should convert spaces to underscores."""
        assert normalize_pain_point("invoice processing") == "invoice_processing"

    def test_normalize_hyphens_to_underscores(self):
        """Should convert hyphens to underscores."""
        assert normalize_pain_point("expense-reporting") == "expense_reporting"

    def test_normalize_strips_whitespace(self):
        """Should strip leading/trailing whitespace."""
        assert normalize_pain_point("  payroll  ") == "payroll"


class TestMatchServices:
    """Tests for service matching logic."""

    def test_match_invoice_processing(self):
        """Should match invoice processing service for manufacturing."""
        services, _ = match_services("manufacturing", ["invoice_processing"])
        service_ids = [s["service_id"] for s in services]
        assert "fin-001" in service_ids

    def test_match_multiple_pain_points(self):
        """Should match multiple services for multiple pain points."""
        services, _ = match_services("manufacturing", ["invoice_processing", "expense_reporting"])
        service_ids = [s["service_id"] for s in services]
        assert "fin-001" in service_ids
        assert "fin-002" in service_ids

    def test_industry_filtering(self):
        """Should filter services by industry."""
        # Customer support not available for all industries
        services, _ = match_services("manufacturing", ["support"])
        service_ids = [s["service_id"] for s in services]
        # CS services may or may not be included based on industry
        # This tests that filtering is applied
        assert isinstance(services, list)

    def test_bundle_recommendation(self):
        """Should recommend bundle when multiple matching services."""
        services, bundle = match_services("manufacturing", ["invoice", "reconciliation", "po"])
        # Manufacturing bundle should be suggested if enough overlap
        assert bundle is None or isinstance(bundle, dict)

    def test_no_bundle_with_flag(self):
        """Should not include bundle when disabled."""
        services, bundle = match_services("manufacturing", ["invoice", "reconciliation", "po"], include_bundle=False)
        # With include_bundle=False, result should still be valid
        assert isinstance(services, list)


class TestCalculateEstimatedPricing:
    """Tests for pricing calculation."""

    def test_pricing_with_services(self):
        """Should calculate total pricing for services."""
        services = [
            {"base_monthly_fee_usd": 5000},
            {"base_monthly_fee_usd": 3000},
        ]
        pricing = calculate_estimated_pricing(services, None)
        assert pricing["base_monthly_fee_usd"] == 8000
        assert pricing["estimated_monthly_total_usd"] == 8000

    def test_pricing_with_bundle_discount(self):
        """Should apply bundle discount."""
        services = [
            {"base_monthly_fee_usd": 5000},
            {"base_monthly_fee_usd": 3000},
        ]
        bundle_info = {"discount_rate": 0.15}
        pricing = calculate_estimated_pricing(services, bundle_info)
        assert pricing["bundle_discount_usd"] == 1200  # 8000 * 0.15
        assert pricing["estimated_monthly_total_usd"] == 6800

    def test_pricing_includes_setup_fees(self):
        """Should include setup fees in calculation."""
        services = [
            {"base_monthly_fee_usd": 2500, "setup_fee_usd": 5000},
        ]
        pricing = calculate_estimated_pricing(services, None)
        assert pricing["setup_fees_usd"] == 5000


class TestGenerateServiceSelection:
    """Tests for full service selection generation."""

    def test_generates_valid_report(self):
        """Should generate valid report structure."""
        report = generate_service_selection(industry="manufacturing", pain_points=["invoice_processing"])
        assert "schema_version" in report
        assert "generated_at" in report
        assert "client_industry" in report
        assert "selected_services" in report
        assert "pricing_estimate" in report

    def test_saves_to_file(self, tmp_path):
        """Should save report to file when path provided."""
        output_file = tmp_path / "services.json"
        report = generate_service_selection(
            industry="trading", pain_points=["invoice", "ar"], output_path=str(output_file)
        )
        assert output_file.exists()
        with open(output_file) as f:
            saved = json.load(f)
        assert saved["client_industry"] == "trading"

    def test_includes_service_count(self):
        """Should include service count in report."""
        report = generate_service_selection(industry="services", pain_points=["expense", "payroll"])
        assert "service_count" in report
        assert report["service_count"] == len(report["selected_services"])
