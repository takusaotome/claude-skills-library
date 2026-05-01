"""
Tests for email triage functionality.
"""

import json
from pathlib import Path

import pytest
from triage_emails import (
    ActionType,
    EmailAnalysis,
    Quadrant,
    Topic,
    TriageReport,
    analyze_email,
    calculate_importance_score,
    calculate_urgency_score,
    classify_topic,
    detect_deadline,
    detect_language,
    determine_action,
    determine_quadrant,
    generate_markdown_report,
    generate_summary,
    load_emails,
)


class TestUrgencyScoring:
    """Tests for urgency score calculation."""

    def test_high_urgency_keywords(self):
        """Test that urgent keywords result in high scores."""
        subject = "URGENT: Need response ASAP"
        body = "This is critical and needs immediate attention."
        score = calculate_urgency_score(subject, body)
        assert score >= 0.8

    def test_medium_urgency_keywords(self):
        """Test medium urgency patterns."""
        subject = "Please review when you get a chance"
        body = "Checking in on the project status."
        score = calculate_urgency_score(subject, body)
        assert 0.4 <= score <= 0.7

    def test_low_urgency_keywords(self):
        """Test FYI emails get low urgency."""
        subject = "FYI: Newsletter update"
        body = "No action needed, just for your information."
        score = calculate_urgency_score(subject, body)
        assert score <= 0.3

    def test_deadline_detection_in_urgency(self):
        """Test that EOD deadlines increase urgency."""
        subject = "Need this by EOD"
        body = "Please complete this task by end of day today."
        score = calculate_urgency_score(subject, body)
        assert score >= 0.8


class TestImportanceScoring:
    """Tests for importance score calculation."""

    def test_vip_sender_high_importance(self):
        """Test VIP sender patterns get high importance."""
        score = calculate_importance_score(
            from_address="ceo@company.com", to_addresses=["me@company.com"], cc_addresses=[]
        )
        assert score >= 0.9

    def test_single_recipient_bonus(self):
        """Test that being the only recipient increases importance."""
        score_single = calculate_importance_score(
            from_address="colleague@company.com", to_addresses=["me@company.com"], cc_addresses=[]
        )
        score_group = calculate_importance_score(
            from_address="colleague@company.com",
            to_addresses=["me@company.com", "other@company.com", "another@company.com", "fourth@company.com"],
            cc_addresses=[],
        )
        assert score_single > score_group

    def test_large_cc_list_decreases_importance(self):
        """Test that large CC lists decrease importance."""
        score_small_cc = calculate_importance_score(
            from_address="colleague@company.com",
            to_addresses=["me@company.com"],
            cc_addresses=["one@company.com", "two@company.com"],
        )
        score_large_cc = calculate_importance_score(
            from_address="colleague@company.com",
            to_addresses=["me@company.com"],
            cc_addresses=[f"person{i}@company.com" for i in range(15)],
        )
        assert score_small_cc > score_large_cc


class TestTopicClassification:
    """Tests for topic classification."""

    def test_client_followup_detection(self):
        """Test client-related emails are classified correctly."""
        topic = classify_topic(
            subject="Client project status update", body="Here is the latest deliverable for the customer account."
        )
        assert topic == Topic.CLIENT_FOLLOWUP

    def test_vendor_inquiry_detection(self):
        """Test vendor emails are classified correctly."""
        topic = classify_topic(
            subject="Invoice #12345", body="Please find attached the invoice for renewal of your contract."
        )
        assert topic == Topic.VENDOR_INQUIRY

    def test_meeting_scheduling_detection(self):
        """Test meeting requests are classified correctly."""
        topic = classify_topic(
            subject="Meeting request: Q4 planning", body="Please check your calendar availability for a call next week."
        )
        assert topic == Topic.MEETING_SCHEDULING

    def test_fyi_detection(self):
        """Test informational emails are classified correctly."""
        topic = classify_topic(
            subject="FYI: Company newsletter", body="Just a heads up about the latest update announcement."
        )
        assert topic == Topic.FYI_INFORMATIONAL


class TestQuadrantDetermination:
    """Tests for Eisenhower Matrix quadrant assignment."""

    def test_q1_urgent_important(self):
        """Test Q1 assignment for high urgency and importance."""
        quadrant = determine_quadrant(urgency=0.9, importance=0.8)
        assert quadrant == Quadrant.Q1_URGENT_IMPORTANT

    def test_q2_important_not_urgent(self):
        """Test Q2 assignment for high importance, low urgency."""
        quadrant = determine_quadrant(urgency=0.3, importance=0.8)
        assert quadrant == Quadrant.Q2_IMPORTANT_NOT_URGENT

    def test_q3_urgent_not_important(self):
        """Test Q3 assignment for high urgency, low importance."""
        quadrant = determine_quadrant(urgency=0.8, importance=0.3)
        assert quadrant == Quadrant.Q3_URGENT_NOT_IMPORTANT

    def test_q4_neither(self):
        """Test Q4 assignment for low urgency and importance."""
        quadrant = determine_quadrant(urgency=0.3, importance=0.3)
        assert quadrant == Quadrant.Q4_NEITHER

    def test_boundary_conditions(self):
        """Test boundary at 0.6 threshold."""
        # Exactly at boundary should go to higher quadrant
        quadrant = determine_quadrant(urgency=0.6, importance=0.6)
        assert quadrant == Quadrant.Q1_URGENT_IMPORTANT


class TestActionDetermination:
    """Tests for action type determination."""

    def test_q1_always_respond(self):
        """Test Q1 emails always require response."""
        action = determine_action(Quadrant.Q1_URGENT_IMPORTANT, Topic.INTERNAL_REQUEST)
        assert action == ActionType.RESPOND

    def test_q2_approval_requires_review(self):
        """Test Q2 approvals require review action."""
        action = determine_action(Quadrant.Q2_IMPORTANT_NOT_URGENT, Topic.APPROVAL_REQUIRED)
        assert action == ActionType.REVIEW

    def test_q3_delegation_candidate(self):
        """Test Q3 delegation candidates get delegate action."""
        action = determine_action(Quadrant.Q3_URGENT_NOT_IMPORTANT, Topic.DELEGATION_CANDIDATE)
        assert action == ActionType.DELEGATE

    def test_q4_fyi_archive(self):
        """Test Q4 FYI emails can be archived."""
        action = determine_action(Quadrant.Q4_NEITHER, Topic.FYI_INFORMATIONAL)
        assert action == ActionType.ARCHIVE


class TestDeadlineDetection:
    """Tests for deadline extraction."""

    def test_date_format_detection(self):
        """Test MM/DD date format detection."""
        deadline = detect_deadline(subject="Due by 12/15", body="Please complete this task.")
        assert deadline is not None
        assert "12-15" in deadline or "12" in deadline

    def test_eod_detection(self):
        """Test end of day deadline detection."""
        deadline = detect_deadline(subject="Need by EOD", body="This is required by end of day.")
        assert deadline is not None
        assert "17:00" in deadline or "17" in deadline

    def test_day_of_week_detection(self):
        """Test day of week deadline detection."""
        deadline = detect_deadline(subject="", body="Please send this by Friday.")
        assert deadline is not None

    def test_no_deadline(self):
        """Test email without deadline returns None."""
        deadline = detect_deadline(subject="General update", body="Here is some information for you.")
        assert deadline is None


class TestLanguageDetection:
    """Tests for language detection."""

    def test_english_detection(self):
        """Test English text detection."""
        lang = detect_language("Hello, this is a test email.")
        assert lang == "en"

    def test_japanese_detection(self):
        """Test Japanese text detection."""
        lang = detect_language("こんにちは、テストメールです。")
        assert lang == "ja"

    def test_japanese_with_kanji(self):
        """Test Japanese with kanji detection."""
        lang = detect_language("本日の会議について確認します。")
        assert lang == "ja"

    def test_mixed_defaults_to_detected(self):
        """Test mixed language detection favors non-English when present."""
        lang = detect_language("Hello, これはテストです。Test complete.")
        assert lang == "ja"


class TestEmailAnalysis:
    """Tests for full email analysis."""

    def test_analyze_urgent_client_email(self):
        """Test analysis of urgent client email."""
        email = {
            "id": "msg_123",
            "from": "client@example.com",
            "subject": "URGENT: Contract review needed",
            "body": "Please review the attached contract by EOD today.",
            "to": ["me@company.com"],
            "cc": [],
            "received_at": "2024-01-15T08:00:00Z",
        }
        analysis = analyze_email(email)

        assert analysis.quadrant == "Q1"
        assert analysis.urgency_score >= 0.8
        assert analysis.action_required == ActionType.RESPOND.value
        assert analysis.detected_deadline is not None

    def test_analyze_fyi_newsletter(self):
        """Test analysis of FYI newsletter."""
        email = {
            "id": "msg_456",
            "from": "newsletter@company.com",
            "subject": "FYI: Weekly company update",
            "body": "No action needed, just for your information.",
            "to": ["all@company.com"],
            "cc": [f"person{i}@company.com" for i in range(20)],
            "received_at": "2024-01-15T09:00:00Z",
        }
        analysis = analyze_email(email)

        assert analysis.quadrant == "Q4"
        assert analysis.urgency_score <= 0.3
        assert analysis.topic == Topic.FYI_INFORMATIONAL.value

    def test_analyze_with_draft_generation(self):
        """Test analysis with draft response generation."""
        email = {
            "id": "msg_789",
            "from": "manager@company.com",
            "subject": "Please review project plan",
            "body": "Can you check this week and let me know?",
            "to": ["me@company.com"],
            "cc": [],
            "received_at": "2024-01-15T10:00:00Z",
        }
        analysis = analyze_email(email, generate_drafts=True)

        assert analysis.draft_response is not None
        assert len(analysis.draft_response) > 0
        assert analysis.status == "draft_ready"


class TestReportGeneration:
    """Tests for report generation."""

    def test_summary_generation(self):
        """Test summary statistics generation."""
        analyses = [
            EmailAnalysis(
                id="1",
                from_address="a@test.com",
                subject="Test 1",
                received_at="2024-01-15T08:00:00Z",
                quadrant="Q1",
                urgency_score=0.9,
                importance_score=0.9,
                topic="client_followup",
                action_required="respond",
            ),
            EmailAnalysis(
                id="2",
                from_address="b@test.com",
                subject="Test 2",
                received_at="2024-01-15T09:00:00Z",
                quadrant="Q4",
                urgency_score=0.2,
                importance_score=0.2,
                topic="fyi_informational",
                action_required="archive",
            ),
            EmailAnalysis(
                id="3",
                from_address="c@test.com",
                subject="Test 3",
                received_at="2024-01-15T10:00:00Z",
                quadrant="Q2",
                urgency_score=0.4,
                importance_score=0.8,
                topic="internal_request",
                action_required="respond",
            ),
        ]
        summary = generate_summary(analyses)

        assert summary["total_emails"] == 3
        assert summary["action_required"] == 2  # Excludes archived
        assert summary["by_quadrant"]["Q1_urgent_important"] == 1
        assert summary["by_quadrant"]["Q2_important_not_urgent"] == 1
        assert summary["by_quadrant"]["Q4_neither"] == 1
        assert summary["by_topic"]["client_followup"] == 1
        assert summary["by_topic"]["fyi_informational"] == 1

    def test_markdown_report_generation(self):
        """Test markdown report generation."""
        analyses = [
            EmailAnalysis(
                id="1",
                from_address="client@test.com",
                subject="Urgent request",
                received_at="2024-01-15T08:00:00Z",
                quadrant="Q1",
                urgency_score=0.9,
                importance_score=0.9,
                topic="client_followup",
                action_required="respond",
            ),
        ]
        report = TriageReport(
            summary=generate_summary(analyses),
            emails=analyses,
        )
        markdown = generate_markdown_report(report)

        assert "# Email Triage Report" in markdown
        assert "## Priority Matrix" in markdown
        assert "Q1: Urgent & Important" in markdown
        assert "client@test.com" in markdown


class TestFileOperations:
    """Tests for file loading operations."""

    def test_load_emails_from_list(self, tmp_path):
        """Test loading emails from JSON array."""
        emails_data = [
            {"id": "1", "from": "a@test.com", "subject": "Test 1"},
            {"id": "2", "from": "b@test.com", "subject": "Test 2"},
        ]
        input_file = tmp_path / "emails.json"
        input_file.write_text(json.dumps(emails_data))

        emails = load_emails(input_file)
        assert len(emails) == 2
        assert emails[0]["id"] == "1"

    def test_load_emails_from_dict_with_emails_key(self, tmp_path):
        """Test loading emails from dict with 'emails' key."""
        emails_data = {
            "emails": [
                {"id": "1", "from": "a@test.com", "subject": "Test 1"},
            ]
        }
        input_file = tmp_path / "emails.json"
        input_file.write_text(json.dumps(emails_data))

        emails = load_emails(input_file)
        assert len(emails) == 1

    def test_load_emails_from_dict_with_messages_key(self, tmp_path):
        """Test loading emails from dict with 'messages' key (gogcli format)."""
        emails_data = {
            "messages": [
                {"id": "1", "from": "a@test.com", "subject": "Test 1"},
            ]
        }
        input_file = tmp_path / "emails.json"
        input_file.write_text(json.dumps(emails_data))

        emails = load_emails(input_file)
        assert len(emails) == 1
