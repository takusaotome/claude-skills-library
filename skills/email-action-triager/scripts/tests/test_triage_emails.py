#!/usr/bin/env python3
"""
Tests for email-action-triager triage_emails.py

Covers:
- Business rules and sender priority
- Urgency calculation
- Action type classification
- Deadline detection
- Email parsing
"""

from datetime import datetime, timedelta

import pytest
from triage_emails import (
    ActionClassifier,
    ActionItem,
    BusinessRules,
    EmailMessage,
    EmailParser,
    EmailTriager,
    UrgencyCalculator,
)


class TestBusinessRules:
    """Tests for BusinessRules class."""

    def test_get_sender_priority_vip(self, default_rules):
        """VIP senders should be identified correctly."""
        rules = BusinessRules()
        rules.rules = default_rules

        assert rules.get_sender_priority("ceo@company.com") == "VIP"
        assert rules.get_sender_priority("cfo@other.com") == "VIP"

    def test_get_sender_priority_low(self, default_rules):
        """Low priority senders should be identified correctly."""
        rules = BusinessRules()
        rules.rules = default_rules

        assert rules.get_sender_priority("noreply@service.com") == "LOW"
        assert rules.get_sender_priority("info@newsletter.example.com") == "LOW"

    def test_get_sender_priority_normal(self, default_rules):
        """Unmatched senders should get NORMAL priority."""
        rules = BusinessRules()
        rules.rules = default_rules

        assert rules.get_sender_priority("colleague@company.com") == "NORMAL"
        assert rules.get_sender_priority("unknown@external.com") == "NORMAL"

    def test_detect_deadline_relative_today(self, default_rules):
        """Should detect 'by EOD' as today's deadline."""
        rules = BusinessRules()
        rules.rules = default_rules

        deadline = rules.detect_deadline("Please complete this by EOD")
        assert deadline == datetime.now().strftime("%Y-%m-%d")

    def test_detect_deadline_relative_tomorrow(self, default_rules):
        """Should detect 'by tomorrow' deadline."""
        rules = BusinessRules()
        rules.rules = default_rules

        deadline = rules.detect_deadline("Need this by tomorrow")
        expected = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        assert deadline == expected

    def test_detect_deadline_explicit_date(self, default_rules):
        """Should detect explicit ISO date."""
        rules = BusinessRules()
        rules.rules = default_rules

        deadline = rules.detect_deadline("Please complete by 2024-01-20")
        assert deadline == "2024-01-20"

    def test_detect_deadline_no_deadline(self, default_rules):
        """Should return None when no deadline detected."""
        rules = BusinessRules()
        rules.rules = default_rules

        deadline = rules.detect_deadline("Just a regular email with no deadline")
        assert deadline is None

    def test_get_project_association(self, default_rules):
        """Should detect project from keywords."""
        rules = BusinessRules()
        rules.rules = default_rules

        project = rules.get_project_association(
            "Q1 Budget Review", "Please review the Q1 budget numbers", "user@company.com"
        )
        assert project == "Q1-Budget"

    def test_get_delegation_candidate(self, default_rules):
        """Should identify delegation candidates."""
        rules = BusinessRules()
        rules.rules = default_rules

        delegate = rules.get_delegation_candidate(
            "Server maintenance needed", "The infrastructure requires updates", "NORMAL"
        )
        assert delegate == "DevOps Team"

    def test_no_delegation_for_vip(self, default_rules):
        """VIP emails should not be delegated."""
        rules = BusinessRules()
        rules.rules = default_rules

        delegate = rules.get_delegation_candidate("Server issue", "Infrastructure problem", "VIP")
        assert delegate is None


class TestUrgencyCalculator:
    """Tests for UrgencyCalculator class."""

    def test_calculate_urgency_high_score(self, default_rules, vip_email_data):
        """VIP sender with URGENT keyword should get high score."""
        rules = BusinessRules()
        rules.rules = default_rules
        calc = UrgencyCalculator(rules)

        email = EmailMessage(**vip_email_data)
        score, level = calc.calculate(email, "VIP", datetime.now().strftime("%Y-%m-%d"))

        assert score >= 80
        assert level in ["CRITICAL", "HIGH"]

    def test_calculate_urgency_low_score(self, default_rules, low_priority_email_data):
        """Low priority newsletter should get low score."""
        rules = BusinessRules()
        rules.rules = default_rules
        calc = UrgencyCalculator(rules)

        email = EmailMessage(**low_priority_email_data)
        score, level = calc.calculate(email, "LOW", None)

        assert score < 50
        assert level in ["LOW", "MINIMAL"]

    def test_deadline_proximity_affects_score(self, default_rules, sample_email_data):
        """Closer deadlines should increase urgency score."""
        rules = BusinessRules()
        rules.rules = default_rules
        calc = UrgencyCalculator(rules)

        email = EmailMessage(**sample_email_data)

        # Today's deadline
        score_today, _ = calc.calculate(email, "NORMAL", datetime.now().strftime("%Y-%m-%d"))

        # Next week deadline
        next_week = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        score_next_week, _ = calc.calculate(email, "NORMAL", next_week)

        # No deadline
        score_none, _ = calc.calculate(email, "NORMAL", None)

        assert score_today > score_next_week > score_none

    def test_urgency_levels(self, default_rules, sample_email_data):
        """Should return correct urgency level strings."""
        rules = BusinessRules()
        rules.rules = default_rules
        calc = UrgencyCalculator(rules)

        valid_levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "MINIMAL"]

        email = EmailMessage(**sample_email_data)
        _, level = calc.calculate(email, "NORMAL", None)

        assert level in valid_levels


class TestActionClassifier:
    """Tests for ActionClassifier class."""

    def test_classify_automated_as_archive(self, low_priority_email_data):
        """Automated emails should be classified as ARCHIVE."""
        classifier = ActionClassifier()
        email = EmailMessage(**low_priority_email_data)

        action_type, _ = classifier.classify(email, "LOW")
        assert action_type == "ARCHIVE"

    def test_classify_question_as_respond(self, question_email_data):
        """Emails with questions should be classified as RESPOND."""
        classifier = ActionClassifier()
        email = EmailMessage(**question_email_data)

        action_type, _ = classifier.classify(email, "NORMAL")
        assert action_type == "RESPOND"

    def test_classify_review_request(self, sample_email_data):
        """Review requests with attachments should be classified as REVIEW."""
        classifier = ActionClassifier()

        data = sample_email_data.copy()
        data["body_text"] = "Please review the attached document and provide feedback."

        email = EmailMessage(**data)
        action_type, _ = classifier.classify(email, "NORMAL")

        assert action_type == "REVIEW"

    def test_classify_meeting_invite(self, sample_email_data):
        """Meeting invitations should be classified as SCHEDULE."""
        classifier = ActionClassifier()

        data = sample_email_data.copy()
        data["subject"] = "Meeting Invitation: Project Sync"
        data["attachments"] = ["invite.ics"]

        email = EmailMessage(**data)
        action_type, _ = classifier.classify(email, "NORMAL")

        assert action_type == "SCHEDULE"


class TestEmailParser:
    """Tests for EmailParser class."""

    def test_parse_mbox(self, temp_mbox_file):
        """Should parse emails from MBOX file."""
        parser = EmailParser()
        emails = parser.parse_mbox(str(temp_mbox_file), max_emails=10)

        assert len(emails) == 3
        assert emails[0].sender == "sender@example.com"
        assert emails[1].sender == "ceo@company.com"
        assert "URGENT" in emails[1].subject

    def test_parse_eml_directory(self, temp_eml_dir):
        """Should parse emails from EML files in directory."""
        parser = EmailParser()
        emails = parser.parse_eml_directory(str(temp_eml_dir), max_emails=10)

        assert len(emails) == 1
        assert emails[0].sender == "sender@example.com"
        assert "Test EML" in emails[0].subject

    def test_parse_empty_directory(self, tmp_path):
        """Should handle empty directory gracefully."""
        parser = EmailParser()
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        emails = parser.parse_eml_directory(str(empty_dir))
        assert emails == []


class TestEmailTriager:
    """Tests for EmailTriager class."""

    def test_triage_single_email(self, sample_email_data):
        """Should triage a single email into an ActionItem."""
        triager = EmailTriager()
        email = EmailMessage(**sample_email_data)

        action_items = triager.triage_emails([email])

        assert len(action_items) == 1
        item = action_items[0]
        assert isinstance(item, ActionItem)
        assert item.id == sample_email_data["id"]
        assert item.subject == sample_email_data["subject"]

    def test_triage_sorts_by_urgency(self, sample_email_data, vip_email_data, low_priority_email_data):
        """Action items should be sorted by urgency score descending."""
        triager = EmailTriager()

        emails = [
            EmailMessage(**low_priority_email_data),
            EmailMessage(**sample_email_data),
            EmailMessage(**vip_email_data),
        ]

        action_items = triager.triage_emails(emails)

        # VIP should be first (highest urgency)
        assert action_items[0].sender == vip_email_data["sender"]
        # Low priority should be last
        assert action_items[-1].sender == low_priority_email_data["sender"]

    def test_generate_json_report(self, sample_email_data):
        """Should generate valid JSON report."""
        triager = EmailTriager()
        email = EmailMessage(**sample_email_data)
        action_items = triager.triage_emails([email])

        report = triager.generate_json_report(action_items)

        assert report["schema_version"] == "1.0"
        assert "generated_at" in report
        assert report["total_emails_processed"] == 1
        assert len(report["action_items"]) == 1
        assert "summary" in report
        assert "sender_stats" in report

    def test_generate_markdown_report(self, sample_email_data):
        """Should generate valid Markdown report."""
        triager = EmailTriager()
        email = EmailMessage(**sample_email_data)
        action_items = triager.triage_emails([email])

        report = triager.generate_markdown_report(action_items)

        assert "# Daily Email Action List" in report
        assert "## Summary" in report
        assert sample_email_data["subject"] in report

    def test_context_tags_generation(self, sample_email_data):
        """Should generate relevant context tags."""
        triager = EmailTriager()

        data = sample_email_data.copy()
        data["body_text"] = "Please review the budget report for our meeting."

        email = EmailMessage(**data)
        action_items = triager.triage_emails([email])

        tags = action_items[0].context_tags
        assert "budget" in tags or "review" in tags or "meeting" in tags

    def test_suggested_response_with_deadline(self, sample_email_data):
        """Should generate response mentioning deadline when detected."""
        triager = EmailTriager()

        data = sample_email_data.copy()
        data["body_text"] = "Please complete this by tomorrow."

        email = EmailMessage(**data)
        action_items = triager.triage_emails([email])

        suggested = action_items[0].suggested_response
        # Should contain deadline date or acknowledgment
        assert suggested is not None


class TestIntegration:
    """Integration tests for full triage workflow."""

    def test_full_workflow_mbox(self, temp_mbox_file):
        """Test complete workflow from MBOX parsing to report generation."""
        triager = EmailTriager()

        # Parse emails
        emails = triager.parser.parse_mbox(str(temp_mbox_file))
        assert len(emails) > 0

        # Triage emails
        action_items = triager.triage_emails(emails)
        assert len(action_items) == len(emails)

        # Generate JSON report
        json_report = triager.generate_json_report(action_items)
        assert json_report["total_emails_processed"] == len(emails)

        # Generate Markdown report
        md_report = triager.generate_markdown_report(action_items)
        assert "# Daily Email Action List" in md_report

    def test_empty_input_handling(self):
        """Should handle empty email list gracefully."""
        triager = EmailTriager()

        action_items = triager.triage_emails([])
        assert action_items == []

        json_report = triager.generate_json_report(action_items)
        assert json_report["total_emails_processed"] == 0

        md_report = triager.generate_markdown_report(action_items)
        assert "# Daily Email Action List" in md_report
