"""Tests for procurement data models."""

from datetime import date, datetime
from pathlib import Path

import pytest
from procurement_models import (
    ProcurementProject,
    ProcurementStatus,
    Quote,
    RFQInfo,
    TimelineEvent,
    Vendor,
    VendorStatus,
)


class TestQuote:
    """Tests for Quote model."""

    def test_quote_to_dict_with_data(self):
        """Test Quote serialization with data."""
        quote = Quote(
            file_path="quotes/vendor_a.pdf",
            amount=15000000,
            currency="JPY",
            received_date=date(2024, 3, 1),
            delivery_date=date(2024, 6, 30),
        )

        result = quote.to_dict()

        assert result["file"] == "quotes/vendor_a.pdf"
        assert result["amount"] == 15000000
        assert result["currency"] == "JPY"
        assert result["received_date"] == "2024-03-01"
        assert result["delivery_date"] == "2024-06-30"

    def test_quote_to_dict_empty_returns_none(self):
        """Test that empty Quote returns None when serialized."""
        quote = Quote()
        assert quote.to_dict() is None

    def test_quote_from_dict(self):
        """Test Quote deserialization."""
        data = {
            "file": "quotes/test.pdf",
            "amount": 10000000,
            "currency": "USD",
            "received_date": "2024-03-15",
            "delivery_date": "2024-07-01",
        }

        quote = Quote.from_dict(data)

        assert quote.file_path == "quotes/test.pdf"
        assert quote.amount == 10000000
        assert quote.currency == "USD"
        assert quote.received_date == date(2024, 3, 15)
        assert quote.delivery_date == date(2024, 7, 1)

    def test_quote_from_dict_none(self):
        """Test Quote.from_dict with None input."""
        assert Quote.from_dict(None) is None


class TestVendor:
    """Tests for Vendor model."""

    def test_vendor_creation(self):
        """Test creating a vendor with required fields."""
        vendor = Vendor(
            name="Tech Solutions Inc.",
            email="sales@techsolutions.example.com",
        )

        assert vendor.name == "Tech Solutions Inc."
        assert vendor.email == "sales@techsolutions.example.com"
        assert vendor.status == VendorStatus.PENDING
        assert vendor.quote is None

    def test_vendor_to_dict(self):
        """Test Vendor serialization."""
        vendor = Vendor(
            name="Test Vendor",
            email="test@vendor.com",
            contact_name="John Doe",
            status=VendorStatus.CONTACTED,
        )

        result = vendor.to_dict()

        assert result["name"] == "Test Vendor"
        assert result["email"] == "test@vendor.com"
        assert result["contact_name"] == "John Doe"
        assert result["status"] == "contacted"

    def test_vendor_from_dict(self):
        """Test Vendor deserialization."""
        data = {
            "name": "Acme Corp",
            "email": "info@acme.com",
            "contact_name": "Jane Smith",
            "status": "quote_received",
            "quote": {
                "file": "quotes/acme.pdf",
                "amount": 5000000,
                "currency": "JPY",
                "received_date": "2024-03-10",
            },
        }

        vendor = Vendor.from_dict(data)

        assert vendor.name == "Acme Corp"
        assert vendor.status == VendorStatus.QUOTE_RECEIVED
        assert vendor.quote is not None
        assert vendor.quote.amount == 5000000


class TestProcurementProject:
    """Tests for ProcurementProject model."""

    def test_project_creation(self):
        """Test creating a new procurement project."""
        project = ProcurementProject(
            name="ERP Modernization",
            client="Acme Corporation",
            created=datetime(2024, 2, 1, 10, 0),
        )

        assert project.name == "ERP Modernization"
        assert project.client == "Acme Corporation"
        assert project.status == ProcurementStatus.INITIALIZED
        assert len(project.vendors) == 0
        assert len(project.timeline) == 0

    def test_add_vendor(self):
        """Test adding a vendor to the project."""
        project = ProcurementProject(
            name="Test Project",
            client="Test Client",
            created=datetime.now(),
        )

        vendor = Vendor(name="Vendor A", email="a@vendor.com")
        result = project.add_vendor(vendor)

        assert result is True
        assert len(project.vendors) == 1
        assert project.vendors[0].name == "Vendor A"
        assert len(project.timeline) == 1

    def test_add_duplicate_vendor(self):
        """Test that duplicate vendors are rejected."""
        project = ProcurementProject(
            name="Test Project",
            client="Test Client",
            created=datetime.now(),
        )

        vendor1 = Vendor(name="Vendor A", email="a@vendor.com")
        vendor2 = Vendor(name="vendor a", email="different@email.com")  # Same name, different case

        project.add_vendor(vendor1)
        result = project.add_vendor(vendor2)

        assert result is False
        assert len(project.vendors) == 1

    def test_get_vendor(self):
        """Test finding a vendor by name."""
        project = ProcurementProject(
            name="Test Project",
            client="Test Client",
            created=datetime.now(),
        )

        vendor = Vendor(name="Tech Solutions", email="info@tech.com")
        project.add_vendor(vendor)

        found = project.get_vendor("Tech Solutions")
        assert found is not None
        assert found.name == "Tech Solutions"

        # Case insensitive
        found_lower = project.get_vendor("tech solutions")
        assert found_lower is not None

        # Not found
        not_found = project.get_vendor("Unknown Vendor")
        assert not_found is None

    def test_update_vendor_status(self):
        """Test updating vendor status."""
        project = ProcurementProject(
            name="Test Project",
            client="Test Client",
            created=datetime.now(),
        )

        vendor = Vendor(name="Vendor A", email="a@vendor.com")
        project.add_vendor(vendor)

        result = project.update_vendor_status("Vendor A", VendorStatus.CONTACTED)

        assert result is True
        assert project.vendors[0].status == VendorStatus.CONTACTED

    def test_get_status_summary(self):
        """Test getting vendor status summary."""
        project = ProcurementProject(
            name="Test Project",
            client="Test Client",
            created=datetime.now(),
        )

        project.add_vendor(Vendor(name="V1", email="v1@test.com"))
        project.add_vendor(Vendor(name="V2", email="v2@test.com"))
        project.add_vendor(Vendor(name="V3", email="v3@test.com"))

        project.update_vendor_status("V1", VendorStatus.CONTACTED)
        project.update_vendor_status("V2", VendorStatus.QUOTE_RECEIVED)

        summary = project.get_status_summary()

        assert summary.get("pending") == 1
        assert summary.get("contacted") == 1
        assert summary.get("quote_received") == 1

    def test_save_and_load(self, tmp_path):
        """Test project persistence to YAML."""
        project = ProcurementProject(
            name="Persistence Test",
            client="Test Client",
            created=datetime(2024, 1, 15, 9, 30),
            status=ProcurementStatus.RFQ_SENT,
        )

        vendor = Vendor(
            name="Test Vendor",
            email="test@vendor.com",
            status=VendorStatus.CONTACTED,
        )
        project.add_vendor(vendor)

        # Save
        config_path = tmp_path / "procurement.yaml"
        project.save(config_path)

        assert config_path.exists()

        # Load
        loaded = ProcurementProject.load(config_path)

        assert loaded.name == "Persistence Test"
        assert loaded.client == "Test Client"
        assert loaded.status == ProcurementStatus.RFQ_SENT
        assert len(loaded.vendors) == 1
        assert loaded.vendors[0].name == "Test Vendor"
        assert loaded.vendors[0].status == VendorStatus.CONTACTED

    def test_get_pending_vendors(self):
        """Test getting vendors who haven't responded."""
        project = ProcurementProject(
            name="Test Project",
            client="Test Client",
            created=datetime.now(),
        )

        project.add_vendor(Vendor(name="V1", email="v1@test.com"))  # PENDING
        project.add_vendor(Vendor(name="V2", email="v2@test.com"))
        project.add_vendor(Vendor(name="V3", email="v3@test.com"))

        project.update_vendor_status("V2", VendorStatus.CONTACTED)
        project.update_vendor_status("V3", VendorStatus.QUOTE_RECEIVED)

        pending = project.get_pending_vendors()

        assert len(pending) == 2
        names = [v.name for v in pending]
        assert "V1" in names
        assert "V2" in names
        assert "V3" not in names

    def test_get_received_quotes(self):
        """Test getting vendors who have submitted quotes."""
        project = ProcurementProject(
            name="Test Project",
            client="Test Client",
            created=datetime.now(),
        )

        project.add_vendor(Vendor(name="V1", email="v1@test.com"))
        project.add_vendor(Vendor(name="V2", email="v2@test.com"))

        project.update_vendor_status("V1", VendorStatus.QUOTE_RECEIVED)

        received = project.get_received_quotes()

        assert len(received) == 1
        assert received[0].name == "V1"
