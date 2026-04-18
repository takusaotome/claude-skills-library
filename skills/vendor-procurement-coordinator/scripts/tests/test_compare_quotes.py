"""Tests for compare_quotes module."""

from datetime import date, datetime

import pytest
from compare_quotes import (
    calculate_price_scores,
    format_currency,
    generate_comparison_report,
)
from procurement_models import (
    ProcurementProject,
    ProcurementStatus,
    Quote,
    Vendor,
    VendorStatus,
)


class TestCalculatePriceScores:
    """Tests for price score calculation."""

    def test_single_vendor_gets_100(self):
        """Single vendor with quote should get score of 100."""
        vendor = Vendor(
            name="Solo Vendor",
            email="solo@vendor.com",
            status=VendorStatus.QUOTE_RECEIVED,
            quote=Quote(amount=10000000, currency="JPY"),
        )

        scores = calculate_price_scores([vendor])

        assert scores["Solo Vendor"] == 100

    def test_lowest_price_gets_100(self):
        """Lowest priced vendor should get score of 100."""
        vendors = [
            Vendor(
                name="Cheap Vendor",
                email="cheap@vendor.com",
                status=VendorStatus.QUOTE_RECEIVED,
                quote=Quote(amount=8000000, currency="JPY"),
            ),
            Vendor(
                name="Expensive Vendor",
                email="expensive@vendor.com",
                status=VendorStatus.QUOTE_RECEIVED,
                quote=Quote(amount=12000000, currency="JPY"),
            ),
        ]

        scores = calculate_price_scores(vendors)

        assert scores["Cheap Vendor"] == 100
        assert scores["Expensive Vendor"] < 100

    def test_relative_scoring(self):
        """Test that scores are calculated relative to lowest price."""
        vendors = [
            Vendor(
                name="Vendor A",
                email="a@vendor.com",
                status=VendorStatus.QUOTE_RECEIVED,
                quote=Quote(amount=10000000, currency="JPY"),
            ),
            Vendor(
                name="Vendor B",
                email="b@vendor.com",
                status=VendorStatus.QUOTE_RECEIVED,
                quote=Quote(amount=20000000, currency="JPY"),  # 2x price
            ),
        ]

        scores = calculate_price_scores(vendors)

        assert scores["Vendor A"] == 100
        assert scores["Vendor B"] == 50  # Half the score for double the price

    def test_empty_list(self):
        """Test with empty vendor list."""
        scores = calculate_price_scores([])
        assert scores == {}

    def test_vendors_without_quotes(self):
        """Test that vendors without quotes are ignored."""
        vendors = [
            Vendor(
                name="No Quote",
                email="noquote@vendor.com",
                status=VendorStatus.PENDING,
            ),
            Vendor(
                name="Has Quote",
                email="hasquote@vendor.com",
                status=VendorStatus.QUOTE_RECEIVED,
                quote=Quote(amount=5000000, currency="JPY"),
            ),
        ]

        scores = calculate_price_scores(vendors)

        assert "No Quote" not in scores
        assert scores["Has Quote"] == 100


class TestFormatCurrency:
    """Tests for currency formatting."""

    def test_format_jpy(self):
        """Test JPY formatting."""
        assert format_currency(15000000, "JPY") == "¥15,000,000"
        assert format_currency(1234567, "JPY") == "¥1,234,567"

    def test_format_usd(self):
        """Test USD formatting."""
        assert format_currency(150000.50, "USD") == "$150,000.50"
        assert format_currency(1234.56, "USD") == "$1,234.56"

    def test_format_none(self):
        """Test None amount."""
        assert format_currency(None, "JPY") == "-"

    def test_format_other_currency(self):
        """Test other currency formatting."""
        assert format_currency(1000, "EUR") == "EUR 1,000.00"


class TestGenerateComparisonReport:
    """Tests for comparison report generation."""

    def test_no_quotes_received(self):
        """Test report when no quotes have been received."""
        project = ProcurementProject(
            name="No Quotes Project",
            client="Test Client",
            created=datetime.now(),
        )

        project.add_vendor(Vendor(name="Pending Vendor", email="pending@vendor.com"))

        report = generate_comparison_report(project)

        assert "No quotes received yet" in report

    def test_basic_report_structure(self):
        """Test that report has expected sections."""
        project = ProcurementProject(
            name="Test Project",
            client="Test Client",
            created=datetime.now(),
        )

        vendor = Vendor(
            name="Test Vendor",
            email="test@vendor.com",
            status=VendorStatus.QUOTE_RECEIVED,
            quote=Quote(
                amount=10000000,
                currency="JPY",
                received_date=date.today(),
                delivery_date=date(2024, 6, 30),
            ),
        )
        project.vendors.append(vendor)

        report = generate_comparison_report(project)

        assert "# Vendor Comparison Report" in report
        assert "## Project: Test Project" in report
        assert "## Summary" in report
        assert "## Price Analysis" in report
        assert "Test Vendor" in report

    def test_multiple_vendors_comparison(self):
        """Test comparison with multiple vendors."""
        project = ProcurementProject(
            name="Multi Vendor Project",
            client="Test Client",
            created=datetime.now(),
        )

        vendors = [
            Vendor(
                name="Vendor A",
                email="a@vendor.com",
                status=VendorStatus.QUOTE_RECEIVED,
                quote=Quote(amount=15000000, currency="JPY", received_date=date.today()),
            ),
            Vendor(
                name="Vendor B",
                email="b@vendor.com",
                status=VendorStatus.QUOTE_RECEIVED,
                quote=Quote(amount=18000000, currency="JPY", received_date=date.today()),
            ),
        ]

        for v in vendors:
            project.vendors.append(v)

        report = generate_comparison_report(project)

        assert "Vendor A" in report
        assert "Vendor B" in report
        assert "¥15,000,000" in report
        assert "¥18,000,000" in report
        assert "Lowest Quote" in report
        assert "Price Spread" in report

    def test_includes_pending_vendors(self):
        """Test that pending vendors are listed separately."""
        project = ProcurementProject(
            name="Mixed Status Project",
            client="Test Client",
            created=datetime.now(),
        )

        project.vendors.append(
            Vendor(
                name="Received Vendor",
                email="received@vendor.com",
                status=VendorStatus.QUOTE_RECEIVED,
                quote=Quote(amount=10000000, currency="JPY", received_date=date.today()),
            )
        )
        project.vendors.append(
            Vendor(
                name="Pending Vendor",
                email="pending@vendor.com",
                status=VendorStatus.PENDING,
            )
        )

        report = generate_comparison_report(project)

        assert "Pending Response" in report
        assert "Pending Vendor" in report

    def test_custom_weights(self):
        """Test report with custom evaluation weights."""
        project = ProcurementProject(
            name="Custom Weights Project",
            client="Test Client",
            created=datetime.now(),
        )

        project.vendors.append(
            Vendor(
                name="Test Vendor",
                email="test@vendor.com",
                status=VendorStatus.QUOTE_RECEIVED,
                quote=Quote(amount=10000000, currency="JPY", received_date=date.today()),
            )
        )

        custom_weights = {
            "price": 40,
            "delivery": 20,
            "technical": 30,
            "experience": 10,
        }

        report = generate_comparison_report(project, custom_weights)

        assert "40%" in report
        assert "20%" in report
        assert "30%" in report
        assert "10%" in report
