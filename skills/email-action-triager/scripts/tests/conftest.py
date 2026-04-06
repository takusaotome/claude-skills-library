#!/usr/bin/env python3
"""
Pytest configuration and fixtures for email-action-triager tests.
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))

from datetime import datetime, timedelta

import pytest


@pytest.fixture
def sample_email_data():
    """Provide sample email data for testing."""
    return {
        "id": "test_001",
        "subject": "Q1 Budget Review Required",
        "sender": "cfo@company.com",
        "sender_name": "Jane Smith",
        "recipients": ["user@company.com"],
        "cc": [],
        "received_at": datetime.now() - timedelta(hours=2),
        "body_text": "Please review the attached budget by EOD tomorrow.",
        "body_html": "",
        "attachments": ["Q1_Budget.xlsx"],
        "labels": ["UNREAD", "IMPORTANT"],
    }


@pytest.fixture
def vip_email_data(sample_email_data):
    """Email from VIP sender."""
    data = sample_email_data.copy()
    data["sender"] = "ceo@company.com"
    data["sender_name"] = "CEO"
    data["subject"] = "URGENT: Board meeting preparation"
    data["body_text"] = "Need your input ASAP for the board meeting tomorrow."
    return data


@pytest.fixture
def low_priority_email_data(sample_email_data):
    """Low priority automated email."""
    data = sample_email_data.copy()
    data["sender"] = "noreply@notifications.company.com"
    data["sender_name"] = ""
    data["subject"] = "Newsletter: Weekly Digest"
    data["body_text"] = "Here is your weekly newsletter digest."
    data["attachments"] = []
    return data


@pytest.fixture
def fyi_email_data(sample_email_data):
    """FYI email where user is CC'd."""
    data = sample_email_data.copy()
    data["recipients"] = ["other@company.com"]
    data["cc"] = ["user@company.com"]
    data["subject"] = "FYI: Project update"
    data["body_text"] = "Just keeping you in the loop on the project status."
    return data


@pytest.fixture
def question_email_data(sample_email_data):
    """Email with direct question."""
    data = sample_email_data.copy()
    data["subject"] = "Quick question about the report"
    data["body_text"] = "Can you send me the Q3 report? When will it be ready?"
    data["attachments"] = []
    return data


@pytest.fixture
def default_rules():
    """Provide default business rules for testing."""
    return {
        "sender_priority": {
            "vip": ["ceo@*", "cfo@*"],
            "high": ["*-manager@*", "*@legal.*"],
            "normal": [],
            "low": ["noreply@*", "*@newsletter.*"],
        },
        "urgency_keywords": {
            "boost_high": ["URGENT", "ASAP", "CRITICAL"],
            "boost_medium": ["Important", "Priority"],
            "boost_low": ["Please review", "Reminder"],
            "reduce_medium": ["FYI", "No action required"],
            "reduce_high": ["Newsletter", "Automated"],
        },
        "deadline_patterns": {
            "relative_phrases": {
                "immediate": ["ASAP", "immediately"],
                "today": ["by EOD", "today"],
                "tomorrow": ["by tomorrow"],
                "this_week": ["by end of week", "by Friday"],
            }
        },
        "delegation_rules": {
            "enabled": True,
            "content_rules": [
                {
                    "pattern": "(server|infrastructure)",
                    "delegate_to": "devops@company.com",
                    "delegate_name": "DevOps Team",
                }
            ],
        },
        "project_associations": {"Q1-Budget": {"keywords": ["budget", "Q1"], "senders": ["*@finance.*"]}},
    }


@pytest.fixture
def temp_mbox_file(tmp_path):
    """Create a temporary MBOX file with sample emails."""
    mbox_content = """From MAILER-DAEMON Mon Jan 15 08:00:00 2024
From: sender@example.com
To: recipient@example.com
Subject: Test Email 1
Date: Mon, 15 Jan 2024 08:00:00 -0500
Content-Type: text/plain

This is a test email body.

From MAILER-DAEMON Mon Jan 15 09:00:00 2024
From: ceo@company.com
To: recipient@example.com
Subject: URGENT: Review needed
Date: Mon, 15 Jan 2024 09:00:00 -0500
Content-Type: text/plain

Please review this ASAP.

From MAILER-DAEMON Mon Jan 15 10:00:00 2024
From: noreply@newsletter.com
To: recipient@example.com
Subject: Weekly Newsletter
Date: Mon, 15 Jan 2024 10:00:00 -0500
Content-Type: text/plain

Your weekly digest.
"""
    mbox_path = tmp_path / "test.mbox"
    mbox_path.write_text(mbox_content)
    return mbox_path


@pytest.fixture
def temp_eml_dir(tmp_path):
    """Create a temporary directory with EML files."""
    eml_content = """From: sender@example.com
To: recipient@example.com
Subject: Test EML Email
Date: Mon, 15 Jan 2024 08:00:00 -0500
Content-Type: text/plain

This is a test email from an EML file.
"""
    eml_dir = tmp_path / "emails"
    eml_dir.mkdir()
    (eml_dir / "test1.eml").write_text(eml_content)
    return eml_dir
