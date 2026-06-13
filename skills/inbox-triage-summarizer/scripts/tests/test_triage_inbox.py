"""
Tests for inbox triage summarizer.
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from triage_inbox import (
    Classification,
    Email,
    InboxTriager,
    ProjectConfig,
    TriageResult,
    generate_json_report,
    generate_markdown_report,
)


@pytest.fixture
def sample_emails():
    """Sample emails for testing."""
    now = datetime.now(timezone.utc)
    return [
        Email(
            id="msg_001",
            thread_id="thread_001",
            from_address="client@alpha.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="URGENT: Please review contract by EOD",
            body="Can you review the attached contract and provide feedback?",
            received_at=now - timedelta(hours=2),
            labels=["clients/alpha"],
            is_from_me=False,
        ),
        Email(
            id="msg_002",
            thread_id="thread_002",
            from_address="newsletter@marketing.com",
            to_addresses=["all@company.com"],
            cc_addresses=["me@company.com"],
            subject="FYI: Weekly newsletter",
            body="No action needed. Here's your weekly update.",
            received_at=now - timedelta(days=1),
            labels=[],
            is_from_me=False,
        ),
        Email(
            id="msg_003",
            thread_id="thread_003",
            from_address="vendor@acme.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="RE: Quote Request",
            body="Thanks for your inquiry. We'll send the quote soon.",
            received_at=now - timedelta(days=5),
            labels=[],
            is_from_me=True,  # I sent this, waiting for response
        ),
        Email(
            id="msg_004",
            thread_id="thread_004",
            from_address="boss@company.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="Please prepare Q1 report",
            body="Need you to prepare the quarterly report by Friday.",
            received_at=now - timedelta(days=2),
            labels=["internal"],
            is_from_me=False,
        ),
    ]


@pytest.fixture
def project_rules():
    """Sample project rules for testing."""
    return [
        ProjectConfig(
            id="client-alpha",
            display_name="Alpha Corp Project",
            priority="high",
            match_rules=[
                {"type": "sender_domain", "pattern": "@alpha.com"},
                {"type": "thread_label", "pattern": "clients/alpha"},
            ],
        ),
        ProjectConfig(
            id="vendor-acme",
            display_name="ACME Vendor",
            priority="medium",
            match_rules=[
                {"type": "sender_domain", "pattern": "@acme.com"},
            ],
        ),
    ]


class TestEmailClassification:
    """Tests for email classification logic."""

    def test_classify_fyi_cc_recipient(self, sample_emails):
        """Test that CC-only recipients get FYI classification."""
        triager = InboxTriager(my_email="me@company.com")
        result = triager.classify_email(sample_emails[1])  # Newsletter
        assert result == Classification.FYI

    def test_classify_fyi_explicit_pattern(self):
        """Test FYI detection from subject pattern."""
        email = Email(
            id="test",
            thread_id="test",
            from_address="sender@example.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="FYI: Project update",
            body="Just wanted to let you know about the progress.",
            received_at=datetime.now(timezone.utc),
            is_from_me=False,
        )
        triager = InboxTriager()
        result = triager.classify_email(email)
        assert result == Classification.FYI

    def test_classify_blocked_waiting(self, sample_emails):
        """Test that emails I sent are classified as blocked waiting."""
        triager = InboxTriager()
        result = triager.classify_email(sample_emails[2])  # I sent this
        assert result == Classification.BLOCKED_WAITING

    def test_classify_requires_action(self, sample_emails):
        """Test that task assignment emails are classified as requires action."""
        triager = InboxTriager()
        result = triager.classify_email(sample_emails[3])  # Boss asking for report
        assert result == Classification.REQUIRES_ACTION

    def test_classify_requires_response_question(self):
        """Test that direct questions trigger requires response."""
        email = Email(
            id="test",
            thread_id="test",
            from_address="colleague@company.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="Quick question",
            body="What do you think about this approach?",
            received_at=datetime.now(timezone.utc),
            is_from_me=False,
        )
        triager = InboxTriager()
        result = triager.classify_email(email)
        assert result == Classification.REQUIRES_RESPONSE


class TestUrgencyScoring:
    """Tests for urgency score calculation."""

    def test_urgency_score_urgent_keyword(self):
        """Test that URGENT keyword increases score."""
        email = Email(
            id="test",
            thread_id="test",
            from_address="sender@example.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="URGENT: Need response",
            body="Please respond ASAP",
            received_at=datetime.now(timezone.utc),
            is_from_me=False,
        )
        triager = InboxTriager()
        score, indicators = triager.calculate_urgency_score(email)
        assert score >= 35  # URGENT (20) + ASAP (15)
        assert "URGENT" in indicators
        assert "ASAP" in indicators

    def test_urgency_score_stale_email(self):
        """Test that old emails get staleness score boost."""
        email = Email(
            id="test",
            thread_id="test",
            from_address="sender@example.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="Regular email",
            body="Nothing urgent",
            received_at=datetime.now(timezone.utc) - timedelta(days=6),
            is_from_me=False,
        )
        triager = InboxTriager()
        score, indicators = triager.calculate_urgency_score(email)
        assert score >= 15  # Stale bonus
        assert any("stale" in ind.lower() or "days" in ind.lower() for ind in indicators)

    def test_urgency_score_eod_deadline(self):
        """Test that EOD deadline increases score."""
        email = Email(
            id="test",
            thread_id="test",
            from_address="sender@example.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="Task",
            body="Please complete by EOD",
            received_at=datetime.now(timezone.utc),
            is_from_me=False,
        )
        triager = InboxTriager()
        score, indicators = triager.calculate_urgency_score(email)
        assert score >= 20  # EOD deadline
        assert any("EOD" in ind for ind in indicators)


class TestProjectMatching:
    """Tests for project/client matching."""

    def test_match_by_sender_domain(self, sample_emails, project_rules):
        """Test project matching by sender domain."""
        triager = InboxTriager(project_rules=project_rules)
        result = triager.match_project(sample_emails[0])  # client@alpha.com
        assert result == "client-alpha"

    def test_match_by_thread_label(self, project_rules):
        """Test project matching by thread label."""
        email = Email(
            id="test",
            thread_id="test",
            from_address="unknown@example.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="Project update",
            body="Details here",
            received_at=datetime.now(timezone.utc),
            labels=["clients/alpha"],
            is_from_me=False,
        )
        triager = InboxTriager(project_rules=project_rules)
        result = triager.match_project(email)
        assert result == "client-alpha"

    def test_match_unassigned(self, project_rules):
        """Test that unmatched emails get 'unassigned' project."""
        email = Email(
            id="test",
            thread_id="test",
            from_address="random@unknown.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="Hello",
            body="General inquiry",
            received_at=datetime.now(timezone.utc),
            is_from_me=False,
        )
        triager = InboxTriager(project_rules=project_rules)
        result = triager.match_project(email)
        assert result == "unassigned"


class TestDeadlineDetection:
    """Tests for deadline extraction."""

    def test_detect_eod_deadline(self):
        """Test EOD deadline detection."""
        email = Email(
            id="test",
            thread_id="test",
            from_address="sender@example.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="Task",
            body="Please complete by EOD tomorrow",
            received_at=datetime.now(timezone.utc),
            is_from_me=False,
        )
        triager = InboxTriager()
        deadline = triager.detect_deadline(email)
        assert deadline == "EOD"

    def test_detect_date_deadline(self):
        """Test date format deadline detection."""
        email = Email(
            id="test",
            thread_id="test",
            from_address="sender@example.com",
            to_addresses=["me@company.com"],
            cc_addresses=[],
            subject="Task due by 1/20",
            body="Please finish this",
            received_at=datetime.now(timezone.utc),
            is_from_me=False,
        )
        triager = InboxTriager()
        deadline = triager.detect_deadline(email)
        assert deadline == "1/20"


class TestFullTriage:
    """Tests for full triage workflow."""

    def test_triage_single_email(self, sample_emails, project_rules):
        """Test full triage of a single email."""
        triager = InboxTriager(project_rules=project_rules, my_email="me@company.com")
        result = triager.triage_email(sample_emails[0])  # Urgent contract review

        assert isinstance(result, TriageResult)
        assert result.classification == Classification.REQUIRES_RESPONSE
        assert result.project_id == "client-alpha"
        assert result.urgency_score >= 20  # URGENT keyword
        assert "URGENT" in result.urgency_indicators
        assert result.detected_deadline == "EOD"
        assert result.recommended_action is not None

    def test_triage_multiple_emails(self, sample_emails, project_rules):
        """Test batch triage of multiple emails."""
        triager = InboxTriager(project_rules=project_rules, my_email="me@company.com")
        results = triager.triage_emails(sample_emails)

        assert len(results) == 4

        # Verify classifications
        classifications = {r.email.id: r.classification for r in results}
        assert classifications["msg_001"] == Classification.REQUIRES_RESPONSE
        assert classifications["msg_002"] == Classification.FYI
        assert classifications["msg_003"] == Classification.BLOCKED_WAITING
        assert classifications["msg_004"] == Classification.REQUIRES_ACTION


class TestReportGeneration:
    """Tests for report generation."""

    def test_json_report_structure(self, sample_emails, project_rules):
        """Test JSON report has correct structure."""
        triager = InboxTriager(project_rules=project_rules, my_email="me@company.com")
        results = triager.triage_emails(sample_emails)
        report = generate_json_report(results)

        assert "schema_version" in report
        assert report["schema_version"] == "1.0"
        assert "scan_timestamp" in report
        assert "summary" in report
        assert "total_emails" in report["summary"]
        assert report["summary"]["total_emails"] == 4
        assert "by_classification" in report["summary"]
        assert "by_project" in report["summary"]
        assert "projects" in report
        assert "action_items" in report
        assert "blocked_items" in report

    def test_markdown_report_generation(self, sample_emails, project_rules):
        """Test markdown report generation."""
        triager = InboxTriager(project_rules=project_rules, my_email="me@company.com")
        results = triager.triage_emails(sample_emails)
        report = generate_markdown_report(results)

        assert "# Inbox Triage Summary" in report
        assert "## Action Summary" in report
        assert "## By Project" in report
        assert "## Recommended Actions" in report
        assert "Total Emails" in report


class TestEmailParsing:
    """Tests for email data parsing."""

    def test_email_from_dict(self):
        """Test Email creation from dictionary."""
        data = {
            "id": "msg_123",
            "thread_id": "thread_456",
            "from": "sender@example.com",
            "to": ["recipient@example.com"],
            "cc": [],
            "subject": "Test subject",
            "body": "Test body",
            "received_at": "2024-01-15T09:00:00Z",
            "labels": ["inbox"],
        }
        email = Email.from_dict(data)

        assert email.id == "msg_123"
        assert email.thread_id == "thread_456"
        assert email.from_address == "sender@example.com"
        assert email.subject == "Test subject"
        assert email.body == "Test body"
        assert isinstance(email.received_at, datetime)

    def test_email_from_dict_alternate_keys(self):
        """Test Email creation with alternate key names."""
        data = {
            "id": "msg_123",
            "threadId": "thread_456",  # Gmail format
            "from_address": "sender@example.com",
            "to_addresses": ["recipient@example.com"],
            "cc_addresses": [],
            "subject": "Test",
            "snippet": "Body from snippet",  # Gmail format
            "date": "2024-01-15T09:00:00Z",
            "labelIds": ["INBOX"],
        }
        email = Email.from_dict(data)

        assert email.thread_id == "thread_456"
        assert email.body == "Body from snippet"
        assert "INBOX" in email.labels


class TestCLIIntegration:
    """Tests for CLI integration (file I/O)."""

    def test_json_output_roundtrip(self, tmp_path, sample_emails, project_rules):
        """Test JSON output can be written and parsed."""
        triager = InboxTriager(project_rules=project_rules, my_email="me@company.com")
        results = triager.triage_emails(sample_emails)
        report = generate_json_report(results)

        output_file = tmp_path / "triage_report.json"
        with output_file.open("w") as f:
            json.dump(report, f, indent=2)

        # Verify file can be read back
        with output_file.open() as f:
            loaded = json.load(f)

        assert loaded["summary"]["total_emails"] == 4
        assert len(loaded["action_items"]) > 0

    def test_markdown_output_write(self, tmp_path, sample_emails, project_rules):
        """Test markdown output can be written."""
        triager = InboxTriager(project_rules=project_rules, my_email="me@company.com")
        results = triager.triage_emails(sample_emails)
        report = generate_markdown_report(results)

        output_file = tmp_path / "triage_report.md"
        output_file.write_text(report)

        # Verify file exists and has content
        assert output_file.exists()
        content = output_file.read_text()
        assert "# Inbox Triage Summary" in content
