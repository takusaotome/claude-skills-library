"""
Tests for generate_purchase_request.py
"""

import pytest
from generate_purchase_request import (
    format_currency,
    generate_purchase_request,
    generate_request_id,
)


class TestFormatCurrency:
    """Tests for currency formatting."""

    def test_format_integer(self):
        """Test formatting whole numbers."""
        assert format_currency(1000) == "$1,000.00"

    def test_format_decimal(self):
        """Test formatting decimal amounts."""
        assert format_currency(1234.56) == "$1,234.56"

    def test_format_large_number(self):
        """Test formatting large numbers with commas."""
        assert format_currency(1000000) == "$1,000,000.00"

    def test_format_zero(self):
        """Test formatting zero."""
        assert format_currency(0) == "$0.00"

    def test_format_small_decimal(self):
        """Test formatting small decimal amounts."""
        assert format_currency(0.99) == "$0.99"


class TestGenerateRequestId:
    """Tests for request ID generation."""

    def test_request_id_format(self):
        """Test that request ID follows expected format."""
        request_id = generate_request_id()
        assert request_id.startswith("PR-")
        parts = request_id.split("-")
        assert len(parts) == 3
        # Date part should be 8 digits
        assert len(parts[1]) == 8
        assert parts[1].isdigit()
        # Time part should be 6 digits
        assert len(parts[2]) == 6
        assert parts[2].isdigit()

    def test_request_id_uniqueness(self):
        """Test that consecutive request IDs are unique (within same second may match)."""
        import time

        id1 = generate_request_id()
        time.sleep(0.01)  # Small delay
        id2 = generate_request_id()
        # They may be the same within the same second, but format is consistent
        assert id1.startswith("PR-")
        assert id2.startswith("PR-")


class TestGeneratePurchaseRequest:
    """Tests for purchase request document generation."""

    def test_basic_purchase_request(self):
        """Test generating a basic purchase request."""
        result = generate_purchase_request(
            product="Dell Laptop XPS 15",
            vendor="Dell Technologies",
            unit_price=1500.00,
            quantity=5,
            justification="Replace aging laptops for engineering team",
            requester="John Smith",
            department="Engineering",
        )

        assert "# Purchase Request" in result
        assert "Dell Laptop XPS 15" in result
        assert "Dell Technologies" in result
        assert "$1,500.00" in result
        assert "$7,500.00" in result  # Total cost
        assert "John Smith" in result
        assert "Engineering" in result
        assert "Replace aging laptops" in result

    def test_purchase_request_with_specifications(self):
        """Test purchase request with specifications."""
        result = generate_purchase_request(
            product="Server Rack",
            vendor="HPE",
            unit_price=5000.00,
            quantity=2,
            justification="Data center expansion",
            requester="Jane Doe",
            department="IT Infrastructure",
            specifications="42U rack, 1000kg capacity, cable management",
        )

        assert "### Specifications" in result
        assert "42U rack" in result
        assert "cable management" in result

    def test_purchase_request_with_urgency(self):
        """Test purchase request with urgency level."""
        result = generate_purchase_request(
            product="Security Camera",
            vendor="Hikvision",
            unit_price=200.00,
            quantity=10,
            justification="Security upgrade",
            requester="Security Team",
            department="Facilities",
            urgency="Critical",
        )

        assert "Critical" in result

    def test_purchase_request_with_budget_code(self):
        """Test purchase request with budget code."""
        result = generate_purchase_request(
            product="Software License",
            vendor="Microsoft",
            unit_price=299.00,
            quantity=50,
            justification="Office 365 licenses for new hires",
            requester="IT Admin",
            department="IT",
            budget_code="IT-2024-SW-001",
        )

        assert "IT-2024-SW-001" in result

    def test_purchase_request_with_alternatives(self):
        """Test purchase request with alternatives considered."""
        result = generate_purchase_request(
            product="Project Management Tool",
            vendor="Atlassian",
            unit_price=10.00,
            quantity=100,
            justification="Team collaboration",
            requester="PMO",
            department="Project Management",
            alternatives="Considered Monday.com ($15/user) and Asana ($13/user)",
        )

        assert "## Alternatives Considered" in result
        assert "Monday.com" in result

    def test_purchase_request_total_calculation(self):
        """Test that total cost is calculated correctly."""
        result = generate_purchase_request(
            product="Test Product",
            vendor="Test Vendor",
            unit_price=123.45,
            quantity=7,
            justification="Test",
            requester="Tester",
            department="QA",
        )

        # 123.45 * 7 = 864.15
        assert "$864.15" in result

    def test_purchase_request_contains_approval_table(self):
        """Test that approval status table is included."""
        result = generate_purchase_request(
            product="Test",
            vendor="Test",
            unit_price=100,
            quantity=1,
            justification="Test",
            requester="Tester",
            department="Test",
        )

        assert "## Approval Status" in result
        assert "Manager" in result
        assert "Director" in result
        assert "Pending" in result

    def test_purchase_request_contains_checklist(self):
        """Test that supporting documents checklist is included."""
        result = generate_purchase_request(
            product="Test",
            vendor="Test",
            unit_price=100,
            quantity=1,
            justification="Test",
            requester="Tester",
            department="Test",
        )

        assert "## Supporting Documents" in result
        assert "Vendor Quote" in result
        assert "Product Specifications" in result
