#!/usr/bin/env python3
"""
Data models for vendor procurement coordination.

This module defines the core data structures for managing procurement projects,
vendors, quotes, and tracking status.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml


class ProcurementStatus(Enum):
    """Status of the overall procurement project."""

    INITIALIZED = "initialized"
    RFQ_SENT = "rfq_sent"
    QUOTES_RECEIVED = "quotes_received"
    EVALUATION = "evaluation"
    COMPLETED = "completed"


class VendorStatus(Enum):
    """Status of an individual vendor in the procurement process."""

    PENDING = "pending"
    CONTACTED = "contacted"
    QUOTE_RECEIVED = "quote_received"
    DECLINED = "declined"
    SELECTED = "selected"
    CONTRACTED = "contracted"
    WITHDRAWN = "withdrawn"


@dataclass
class Quote:
    """Represents a vendor's quote/proposal."""

    file_path: Optional[str] = None
    amount: Optional[float] = None
    currency: str = "JPY"
    received_date: Optional[date] = None
    valid_until: Optional[date] = None
    delivery_date: Optional[date] = None
    notes: str = ""

    def to_dict(self) -> dict:
        """Convert quote to dictionary for YAML serialization."""
        if self.file_path is None and self.amount is None:
            return None
        return {
            "file": self.file_path,
            "amount": self.amount,
            "currency": self.currency,
            "received_date": self.received_date.isoformat() if self.received_date else None,
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "delivery_date": self.delivery_date.isoformat() if self.delivery_date else None,
            "notes": self.notes if self.notes else None,
        }

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional["Quote"]:
        """Create Quote from dictionary."""
        if data is None:
            return None
        return cls(
            file_path=data.get("file"),
            amount=data.get("amount"),
            currency=data.get("currency", "JPY"),
            received_date=date.fromisoformat(data["received_date"]) if data.get("received_date") else None,
            valid_until=date.fromisoformat(data["valid_until"]) if data.get("valid_until") else None,
            delivery_date=date.fromisoformat(data["delivery_date"]) if data.get("delivery_date") else None,
            notes=data.get("notes", ""),
        )


@dataclass
class Vendor:
    """Represents a vendor in the procurement process."""

    name: str
    email: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    status: VendorStatus = VendorStatus.PENDING
    quote: Optional[Quote] = None
    contacted_date: Optional[date] = None
    notes: str = ""

    def to_dict(self) -> dict:
        """Convert vendor to dictionary for YAML serialization."""
        return {
            "name": self.name,
            "email": self.email,
            "contact_name": self.contact_name,
            "phone": self.phone,
            "status": self.status.value,
            "quote": self.quote.to_dict() if self.quote else None,
            "contacted_date": self.contacted_date.isoformat() if self.contacted_date else None,
            "notes": self.notes if self.notes else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Vendor":
        """Create Vendor from dictionary."""
        return cls(
            name=data["name"],
            email=data["email"],
            contact_name=data.get("contact_name"),
            phone=data.get("phone"),
            status=VendorStatus(data.get("status", "pending")),
            quote=Quote.from_dict(data.get("quote")),
            contacted_date=date.fromisoformat(data["contacted_date"]) if data.get("contacted_date") else None,
            notes=data.get("notes", ""),
        )


@dataclass
class TimelineEvent:
    """Represents an event in the procurement timeline."""

    timestamp: datetime
    event: str
    details: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert event to dictionary for YAML serialization."""
        return {
            "date": self.timestamp.isoformat(),
            "event": self.event,
            "details": self.details if self.details else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TimelineEvent":
        """Create TimelineEvent from dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data["date"]),
            event=data["event"],
            details=data.get("details"),
        )


@dataclass
class RFQInfo:
    """Information about the RFQ document."""

    document_path: Optional[str] = None
    sent_date: Optional[date] = None
    deadline: Optional[date] = None
    qa_deadline: Optional[date] = None

    def to_dict(self) -> dict:
        """Convert RFQ info to dictionary for YAML serialization."""
        return {
            "document": self.document_path,
            "sent_date": self.sent_date.isoformat() if self.sent_date else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "qa_deadline": self.qa_deadline.isoformat() if self.qa_deadline else None,
        }

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> "RFQInfo":
        """Create RFQInfo from dictionary."""
        if data is None:
            return cls()
        return cls(
            document_path=data.get("document"),
            sent_date=date.fromisoformat(data["sent_date"]) if data.get("sent_date") else None,
            deadline=date.fromisoformat(data["deadline"]) if data.get("deadline") else None,
            qa_deadline=date.fromisoformat(data["qa_deadline"]) if data.get("qa_deadline") else None,
        )


@dataclass
class ProcurementProject:
    """Represents a complete procurement project."""

    name: str
    client: str
    created: datetime
    status: ProcurementStatus = ProcurementStatus.INITIALIZED
    rfq: RFQInfo = field(default_factory=RFQInfo)
    vendors: list[Vendor] = field(default_factory=list)
    timeline: list[TimelineEvent] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> dict:
        """Convert project to dictionary for YAML serialization."""
        return {
            "project": {
                "name": self.name,
                "client": self.client,
                "created": self.created.isoformat(),
                "status": self.status.value,
                "description": self.description if self.description else None,
            },
            "rfq": self.rfq.to_dict(),
            "vendors": [v.to_dict() for v in self.vendors],
            "timeline": [e.to_dict() for e in self.timeline],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProcurementProject":
        """Create ProcurementProject from dictionary."""
        project_data = data.get("project", {})
        return cls(
            name=project_data["name"],
            client=project_data["client"],
            created=datetime.fromisoformat(project_data["created"]),
            status=ProcurementStatus(project_data.get("status", "initialized")),
            rfq=RFQInfo.from_dict(data.get("rfq")),
            vendors=[Vendor.from_dict(v) for v in data.get("vendors", [])],
            timeline=[TimelineEvent.from_dict(e) for e in data.get("timeline", [])],
            description=project_data.get("description", ""),
        )

    def save(self, path: Path) -> None:
        """Save project to YAML file."""
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    @classmethod
    def load(cls, path: Path) -> "ProcurementProject":
        """Load project from YAML file."""
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    def add_timeline_event(self, event: str, details: Optional[str] = None) -> None:
        """Add an event to the timeline."""
        self.timeline.append(
            TimelineEvent(
                timestamp=datetime.now(),
                event=event,
                details=details,
            )
        )

    def get_vendor(self, name: str) -> Optional[Vendor]:
        """Find a vendor by name."""
        for vendor in self.vendors:
            if vendor.name.lower() == name.lower():
                return vendor
        return None

    def add_vendor(self, vendor: Vendor) -> bool:
        """Add a vendor to the project. Returns False if vendor already exists."""
        if self.get_vendor(vendor.name):
            return False
        self.vendors.append(vendor)
        self.add_timeline_event(f"Vendor added: {vendor.name}")
        return True

    def update_vendor_status(self, name: str, status: VendorStatus) -> bool:
        """Update a vendor's status. Returns False if vendor not found."""
        vendor = self.get_vendor(name)
        if not vendor:
            return False
        old_status = vendor.status
        vendor.status = status
        self.add_timeline_event(f"Vendor status updated: {name}", f"{old_status.value} -> {status.value}")
        return True

    def get_pending_vendors(self) -> list[Vendor]:
        """Get vendors who haven't responded yet."""
        return [v for v in self.vendors if v.status in (VendorStatus.PENDING, VendorStatus.CONTACTED)]

    def get_received_quotes(self) -> list[Vendor]:
        """Get vendors who have submitted quotes."""
        return [v for v in self.vendors if v.status == VendorStatus.QUOTE_RECEIVED]

    def get_status_summary(self) -> dict:
        """Get summary of vendor statuses."""
        summary = {}
        for status in VendorStatus:
            count = len([v for v in self.vendors if v.status == status])
            if count > 0:
                summary[status.value] = count
        return summary
