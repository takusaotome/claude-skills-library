"""
Tests for email classification logic.
"""

import json
from pathlib import Path

import pytest
from classify_emails import EmailClassification, EmailClassifier, TriageConfig


@pytest.fixture
def default_config():
    """Default triage configuration."""
    return TriageConfig(
        vip_domains=["company.com", "keyclient.org"],
        vip_senders=["ceo@company.com", "boss@company.com"],
    )


@pytest.fixture
def classifier(default_config):
    """Classifier instance with default config."""
    return EmailClassifier(default_config)


@pytest.fixture
def sample_emails():
    """Sample email data for testing."""
    return [
        {
            "id": "msg_1",
            "threadId": "thread_1",
            "from": "ceo@company.com",
            "to": "me@example.com",
            "subject": "Q4 Budget Review - URGENT Need Your Input by EOD",
            "snippet": "Please review the attached budget and let me know your thoughts.",
            "date": "2025-01-15T08:15:00Z",
        },
        {
            "id": "msg_2",
            "threadId": "thread_2",
            "from": "newsletter@marketing.com",
            "to": "me@example.com",
            "subject": "Weekly Newsletter - January Edition",
            "snippet": "Check out our latest updates. Unsubscribe here.",
            "date": "2025-01-15T07:00:00Z",
        },
        {
            "id": "msg_3",
            "threadId": "thread_3",
            "from": "colleague@other.com",
            "to": "me@example.com",
            "subject": "Quick question about the project",
            "snippet": "When you get a chance, could you review this document?",
            "date": "2025-01-15T09:00:00Z",
        },
        {
            "id": "msg_4",
            "threadId": "thread_4",
            "from": "vendor@supplier.com",
            "to": "me@example.com",
            "subject": "Invoice #12345 Payment Reminder",
            "snippet": "Please process the attached invoice for payment.",
            "date": "2025-01-14T14:00:00Z",
        },
        {
            "id": "msg_5",
            "threadId": "thread_5",
            "from": "noreply@system.com",
            "to": "me@example.com",
            "subject": "Automated notification",
            "snippet": "This is an automated message. Do not reply.",
            "date": "2025-01-15T06:00:00Z",
        },
    ]


class TestVIPDetection:
    """Tests for VIP sender detection."""

    def test_vip_domain_detection(self, classifier):
        """Should detect VIP domains."""
        assert classifier.is_vip_sender("John Doe <john@company.com>")
        assert classifier.is_vip_sender("contact@keyclient.org")

    def test_vip_explicit_sender(self, classifier):
        """Should detect explicit VIP senders."""
        assert classifier.is_vip_sender("CEO <ceo@company.com>")
        assert classifier.is_vip_sender("boss@company.com")

    def test_non_vip_sender(self, classifier):
        """Should return False for non-VIP senders."""
        assert not classifier.is_vip_sender("random@other.com")
        assert not classifier.is_vip_sender("newsletter@marketing.com")

    def test_case_insensitive(self, classifier):
        """VIP detection should be case-insensitive."""
        assert classifier.is_vip_sender("CEO@COMPANY.COM")
        assert classifier.is_vip_sender("Boss@Company.Com")


class TestUrgencyScoring:
    """Tests for urgency score calculation."""

    def test_vip_sender_boost(self, classifier):
        """VIP sender should add 30 points."""
        email = {"from": "ceo@company.com", "subject": "Hello", "snippet": "Just checking in."}
        score, signals = classifier.calculate_urgency_score(email)
        assert "vip_sender" in signals
        assert score >= 30

    def test_deadline_keywords(self, classifier):
        """Deadline keywords should boost score."""
        email = {"from": "other@example.com", "subject": "URGENT: Need this ASAP", "snippet": "Please respond."}
        score, signals = classifier.calculate_urgency_score(email)
        assert "deadline_keyword" in signals
        assert score >= 25

    def test_reply_expected(self, classifier):
        """Reply-expected phrases should boost score."""
        email = {"from": "other@example.com", "subject": "Question", "snippet": "Please let me know your thoughts."}
        score, signals = classifier.calculate_urgency_score(email)
        assert "reply_expected" in signals
        assert score >= 15

    def test_direct_question(self, classifier):
        """Direct questions should add to score."""
        email = {"from": "other@example.com", "subject": "Can you help?", "snippet": "I need assistance."}
        score, signals = classifier.calculate_urgency_score(email)
        assert "direct_question" in signals
        assert score >= 10

    def test_escalation_detection(self, classifier):
        """Escalation language should boost score."""
        email = {"from": "other@example.com", "subject": "Following up", "snippet": "This is my second request."}
        score, signals = classifier.calculate_urgency_score(email)
        assert "escalation" in signals
        assert score >= 20

    def test_fyi_indicators_reduce_score(self, classifier):
        """FYI indicators should reduce score."""
        email = {"from": "newsletter@marketing.com", "subject": "FYI", "snippet": "No action needed. Unsubscribe here."}
        score, signals = classifier.calculate_urgency_score(email)
        assert "fyi_indicator" in signals
        assert score < 30

    def test_combined_signals(self, classifier):
        """Multiple signals should stack."""
        email = {
            "from": "ceo@company.com",  # VIP +30
            "subject": "URGENT: Budget Review?",  # deadline +25, question +10
            "snippet": "Let me know your thoughts by EOD.",  # reply_expected +15
        }
        score, signals = classifier.calculate_urgency_score(email)
        assert score >= 60
        assert "vip_sender" in signals


class TestClassification:
    """Tests for email classification."""

    def test_urgent_classification(self, classifier):
        """High urgency emails should be classified as urgent-response."""
        email = {
            "id": "msg_1",
            "threadId": "thread_1",
            "from": "ceo@company.com",
            "subject": "URGENT: Need approval by EOD",
            "snippet": "Please approve this immediately.",
            "date": "2025-01-15T08:00:00Z",
        }
        result = classifier.classify_email(email)
        assert result.classification == "urgent-response"
        assert result.urgency_score >= 60

    def test_archive_classification(self, classifier):
        """Automated/newsletter emails should be classified as archive."""
        email = {
            "id": "msg_2",
            "threadId": "thread_2",
            "from": "noreply@system.com",
            "subject": "Automated notification",
            "snippet": "This is an automated message. Do not reply. Unsubscribe here.",
            "date": "2025-01-15T06:00:00Z",
        }
        result = classifier.classify_email(email)
        assert result.classification in ["archive", "fyi-read"]

    def test_response_needed_classification(self, classifier):
        """Moderate urgency emails should be classified as response-needed."""
        email = {
            "id": "msg_3",
            "threadId": "thread_3",
            "from": "colleague@other.com",
            "subject": "Quick question",
            "snippet": "Could you review this when you have time?",
            "date": "2025-01-15T09:00:00Z",
        }
        result = classifier.classify_email(email)
        assert result.classification in ["response-needed", "fyi-read"]

    def test_delegatable_classification(self, classifier):
        """Finance-related emails should be detected as delegatable."""
        email = {
            "id": "msg_4",
            "threadId": "thread_4",
            "from": "vendor@supplier.com",
            "subject": "Invoice payment request",
            "snippet": "Please process invoice #12345 for billing.",
            "date": "2025-01-14T14:00:00Z",
        }
        result = classifier.classify_email(email)
        assert result.delegate_to is not None or result.classification in ["delegatable", "response-needed"]

    def test_vip_never_archived(self, classifier):
        """VIP emails should never be classified as archive."""
        email = {
            "id": "msg_5",
            "threadId": "thread_5",
            "from": "ceo@company.com",
            "subject": "FYI - No action needed",
            "snippet": "Just sharing for your information.",
            "date": "2025-01-15T06:00:00Z",
        }
        result = classifier.classify_email(email)
        assert result.classification != "archive"


class TestBatchClassification:
    """Tests for batch email classification."""

    def test_classify_emails_returns_report(self, classifier, sample_emails):
        """Should return properly structured report."""
        report = classifier.classify_emails(sample_emails)

        assert "schema_version" in report
        assert "generated_at" in report
        assert "total_emails" in report
        assert "summary" in report
        assert "emails" in report

        assert report["total_emails"] == len(sample_emails)

    def test_summary_counts(self, classifier, sample_emails):
        """Summary should contain all category counts."""
        report = classifier.classify_emails(sample_emails)
        summary = report["summary"]

        assert "urgent_response" in summary
        assert "response_needed" in summary
        assert "fyi_read" in summary
        assert "delegatable" in summary
        assert "archive" in summary

        # Sum of categories should equal total
        total = sum(summary.values())
        assert total == report["total_emails"]

    def test_emails_sorted_by_urgency(self, classifier, sample_emails):
        """Emails should be sorted by urgency score descending."""
        report = classifier.classify_emails(sample_emails)
        emails = report["emails"]

        scores = [e["urgency_score"] for e in emails]
        assert scores == sorted(scores, reverse=True)


class TestDelegationDetection:
    """Tests for delegation target detection."""

    def test_finance_delegation(self, classifier):
        """Should detect finance-related emails."""
        email = {"subject": "Invoice #123", "snippet": "Please process this payment."}
        target = classifier.detect_delegation_target(email)
        assert target == "finance@"

    def test_hr_delegation(self, classifier):
        """Should detect HR-related emails."""
        email = {"subject": "Vacation Request", "snippet": "I'd like to request leave."}
        target = classifier.detect_delegation_target(email)
        assert target == "hr@"

    def test_it_delegation(self, classifier):
        """Should detect IT-related emails."""
        email = {"subject": "Password Reset", "snippet": "I need my password reset."}
        target = classifier.detect_delegation_target(email)
        assert target == "it@"

    def test_no_delegation(self, classifier):
        """Should return None when no delegation match."""
        email = {"subject": "General question", "snippet": "How are you doing?"}
        target = classifier.detect_delegation_target(email)
        assert target is None


class TestTimeEstimation:
    """Tests for response time estimation."""

    def test_urgent_base_time(self, classifier):
        """Urgent emails should have higher base time."""
        result = classifier.classify_email(
            {
                "id": "1",
                "threadId": "1",
                "from": "ceo@company.com",
                "subject": "URGENT",
                "snippet": "Need this ASAP",
                "date": "2025-01-15",
            }
        )
        assert result.estimated_minutes >= 10

    def test_fyi_low_time(self, classifier):
        """FYI emails should have minimal time."""
        result = classifier.classify_email(
            {
                "id": "1",
                "threadId": "1",
                "from": "noreply@system.com",
                "subject": "FYI notification",
                "snippet": "Automated message. Unsubscribe.",
                "date": "2025-01-15",
            }
        )
        assert result.estimated_minutes <= 3


class TestCLIIntegration:
    """Tests for CLI functionality."""

    def test_json_file_processing(self, classifier, sample_emails, tmp_path):
        """Should process JSON input file correctly."""
        # Write sample emails to temp file
        input_file = tmp_path / "emails.json"
        with open(input_file, "w") as f:
            json.dump(sample_emails, f)

        # Load and process
        with open(input_file, "r") as f:
            loaded_emails = json.load(f)

        report = classifier.classify_emails(loaded_emails)
        assert report["total_emails"] == 5

    def test_dict_with_messages_key(self, classifier, sample_emails):
        """Should handle dict with 'messages' key."""
        # This tests the format returned by some email APIs
        data = {"messages": sample_emails}

        # Extract messages (simulating CLI behavior)
        emails = data.get("messages", [])
        report = classifier.classify_emails(emails)

        assert report["total_emails"] == 5
