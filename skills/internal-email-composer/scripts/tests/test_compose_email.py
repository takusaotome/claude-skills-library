"""Tests for compose_email.py."""

import json
from pathlib import Path

import pytest
from compose_email import (
    EmailComposer,
    EmailContext,
    EmailDraft,
    EmailType,
    Language,
    Urgency,
)


class TestEmailContext:
    """Tests for EmailContext dataclass."""

    def test_default_values(self):
        """Test that EmailContext has correct default values."""
        ctx = EmailContext(email_type=EmailType.VENDOR_RFQ, recipient_name="Test User")
        assert ctx.recipient_role == ""
        assert ctx.language == Language.JAPANESE
        assert ctx.key_points == []
        assert ctx.urgency == Urgency.NORMAL

    def test_custom_values(self):
        """Test EmailContext with custom values."""
        ctx = EmailContext(
            email_type=EmailType.TASK_DELEGATION,
            recipient_name="John Doe",
            recipient_role="Manager",
            language=Language.ENGLISH,
            key_points=["Review document", "Submit feedback"],
            urgency=Urgency.HIGH,
        )
        assert ctx.email_type == EmailType.TASK_DELEGATION
        assert ctx.recipient_name == "John Doe"
        assert ctx.language == Language.ENGLISH
        assert len(ctx.key_points) == 2


class TestEmailDraft:
    """Tests for EmailDraft dataclass."""

    def test_to_dict(self):
        """Test conversion to dictionary."""
        draft = EmailDraft(
            email_type="vendor_rfq",
            language="ja",
            generated_at="2024-12-10T14:30:00",
            subject="Test Subject",
            recipient={"name": "Test", "role": "Manager"},
            greeting="Hello",
            body="Test body",
            closing="Best regards",
            signature={"name": "Sender"},
        )
        result = draft.to_dict()

        assert result["schema_version"] == "1.0"
        assert result["email_type"] == "vendor_rfq"
        assert result["subject"] == "Test Subject"
        assert result["body"]["greeting"] == "Hello"

    def test_to_markdown(self):
        """Test conversion to markdown."""
        draft = EmailDraft(
            email_type="vendor_rfq",
            language="ja",
            generated_at="2024-12-10T14:30:00",
            subject="Test Subject",
            recipient={"name": "田中様", "role": "Manager"},
            greeting="お疲れ様です。",
            body="Test body content",
            closing="よろしくお願いいたします。",
            signature={"name": "山田", "department": "開発部"},
        )
        result = draft.to_markdown()

        assert "# Email Draft" in result
        assert "Test Subject" in result
        assert "田中様" in result
        assert "お疲れ様です。" in result
        assert "山田" in result


class TestEmailComposer:
    """Tests for EmailComposer class."""

    @pytest.fixture
    def composer(self):
        """Create EmailComposer instance."""
        return EmailComposer()

    def test_compose_vendor_rfq_japanese(self, composer):
        """Test composing vendor RFQ email in Japanese."""
        ctx = EmailContext(
            email_type=EmailType.VENDOR_RFQ,
            recipient_name="田中様",
            recipient_role="調達部マネージャー",
            language=Language.JAPANESE,
            key_points=["AWS見積依頼", "3社からの回収"],
            deadline="12月20日",
            project_name="AWSインフラ移行",
            sender_name="山田太郎",
            sender_department="システム開発部",
        )
        draft = composer.compose(ctx)

        assert draft.email_type == "vendor_rfq"
        assert draft.language == "ja"
        assert "見積依頼" in draft.subject
        assert "AWSインフラ移行" in draft.subject
        assert "お疲れ様です" in draft.greeting
        assert "AWS見積依頼" in draft.body
        assert "12月20日" in draft.body

    def test_compose_vendor_rfq_english(self, composer):
        """Test composing vendor RFQ email in English."""
        ctx = EmailContext(
            email_type=EmailType.VENDOR_RFQ,
            recipient_name="John",
            recipient_role="Procurement Manager",
            language=Language.ENGLISH,
            key_points=["AWS infrastructure quotes", "3 vendor responses"],
            deadline="December 20",
            project_name="AWS Migration",
            sender_name="Taro Yamada",
            sender_department="IT Department",
        )
        draft = composer.compose(ctx)

        assert draft.email_type == "vendor_rfq"
        assert draft.language == "en"
        assert "RFQ Request" in draft.subject
        assert "AWS Migration" in draft.subject
        assert "Dear John" in draft.greeting
        assert "AWS infrastructure quotes" in draft.body

    def test_compose_task_delegation_japanese(self, composer):
        """Test composing task delegation email in Japanese."""
        ctx = EmailContext(
            email_type=EmailType.TASK_DELEGATION,
            recipient_name="佐藤さん",
            language=Language.JAPANESE,
            key_points=["資料作成", "レビュー"],
            deadline="12月15日",
            sender_name="山田",
        )
        draft = composer.compose(ctx)

        assert "【依頼】" in draft.subject
        assert "作業をお願い" in draft.body
        assert "よろしくお願いいたします" in draft.closing

    def test_compose_status_update_english(self, composer):
        """Test composing status update email in English."""
        ctx = EmailContext(
            email_type=EmailType.STATUS_UPDATE,
            recipient_name="Team",
            language=Language.ENGLISH,
            project_name="Q4 Project",
            key_points=["Milestone 1 completed", "On track for delivery"],
            sender_name="Jane",
        )
        draft = composer.compose(ctx)

        assert "Status Update:" in draft.subject
        assert "Q4 Project" in draft.subject
        assert "status update" in draft.body.lower()

    def test_compose_follow_up_japanese(self, composer):
        """Test composing follow-up email in Japanese."""
        ctx = EmailContext(
            email_type=EmailType.FOLLOW_UP,
            recipient_name="鈴木様",
            language=Language.JAPANESE,
            key_points=["先日の見積依頼"],
            sender_name="山田",
        )
        draft = composer.compose(ctx)

        assert "【再送】" in draft.subject
        assert "確認のため" in draft.body

    def test_compose_escalation_english(self, composer):
        """Test composing escalation email in English."""
        ctx = EmailContext(
            email_type=EmailType.ESCALATION,
            recipient_name="Director Smith",
            language=Language.ENGLISH,
            key_points=["Blocked dependency", "Need executive decision"],
            project_name="Critical Project",
            urgency=Urgency.URGENT,
        )
        draft = composer.compose(ctx)

        assert "[Escalation]" in draft.subject
        assert "URGENT:" in draft.subject
        assert "escalate" in draft.body.lower()

    def test_compose_info_request_japanese(self, composer):
        """Test composing info request email in Japanese."""
        ctx = EmailContext(
            email_type=EmailType.INFO_REQUEST,
            recipient_name="情報システム部御中",
            language=Language.JAPANESE,
            key_points=["サーバー構成情報", "ネットワーク図"],
            deadline="12月18日",
            sender_name="企画部 田中",
        )
        draft = composer.compose(ctx)

        assert "【情報提供のお願い】" in draft.subject
        assert "情報をご提供いただきたく" in draft.body

    def test_urgency_prefix_japanese(self, composer):
        """Test urgency prefixes in Japanese."""
        ctx_high = EmailContext(
            email_type=EmailType.VENDOR_RFQ, recipient_name="Test", language=Language.JAPANESE, urgency=Urgency.HIGH
        )
        draft_high = composer.compose(ctx_high)
        assert "【至急】" in draft_high.subject

        ctx_urgent = EmailContext(
            email_type=EmailType.VENDOR_RFQ, recipient_name="Test", language=Language.JAPANESE, urgency=Urgency.URGENT
        )
        draft_urgent = composer.compose(ctx_urgent)
        assert "【緊急】" in draft_urgent.subject

    def test_urgency_prefix_english(self, composer):
        """Test urgency prefixes in English."""
        ctx_high = EmailContext(
            email_type=EmailType.TASK_DELEGATION, recipient_name="Test", language=Language.ENGLISH, urgency=Urgency.HIGH
        )
        draft_high = composer.compose(ctx_high)
        assert "Time-Sensitive:" in draft_high.subject

        ctx_urgent = EmailContext(
            email_type=EmailType.TASK_DELEGATION,
            recipient_name="Test",
            language=Language.ENGLISH,
            urgency=Urgency.URGENT,
        )
        draft_urgent = composer.compose(ctx_urgent)
        assert "URGENT:" in draft_urgent.subject

    def test_attachments_included(self, composer):
        """Test that attachments are included in body."""
        ctx = EmailContext(
            email_type=EmailType.VENDOR_RFQ,
            recipient_name="Test",
            language=Language.JAPANESE,
            attachments=["RFQ文書.pdf", "仕様書.xlsx"],
        )
        draft = composer.compose(ctx)

        assert "【添付資料】" in draft.body
        assert "RFQ文書.pdf" in draft.body
        assert "仕様書.xlsx" in draft.body

    def test_key_points_formatting_japanese(self, composer):
        """Test key points are formatted with Japanese bullets."""
        ctx = EmailContext(
            email_type=EmailType.TASK_DELEGATION,
            recipient_name="Test",
            language=Language.JAPANESE,
            key_points=["タスク1", "タスク2"],
        )
        draft = composer.compose(ctx)

        assert "・タスク1" in draft.body
        assert "・タスク2" in draft.body

    def test_key_points_formatting_english(self, composer):
        """Test key points are formatted with English bullets."""
        ctx = EmailContext(
            email_type=EmailType.TASK_DELEGATION,
            recipient_name="Test",
            language=Language.ENGLISH,
            key_points=["Task 1", "Task 2"],
        )
        draft = composer.compose(ctx)

        assert "- Task 1" in draft.body
        assert "- Task 2" in draft.body


class TestCLIIntegration:
    """Tests for CLI functionality."""

    def test_output_json_format(self, tmp_path):
        """Test JSON output format via composer."""
        composer = EmailComposer()
        ctx = EmailContext(email_type=EmailType.VENDOR_RFQ, recipient_name="Test", language=Language.JAPANESE)
        draft = composer.compose(ctx)
        json_output = json.dumps(draft.to_dict(), ensure_ascii=False)

        # Verify it's valid JSON
        parsed = json.loads(json_output)
        assert parsed["schema_version"] == "1.0"
        assert "email_type" in parsed
        assert "body" in parsed

    def test_output_file_write(self, tmp_path):
        """Test writing output to file."""
        composer = EmailComposer()
        ctx = EmailContext(email_type=EmailType.VENDOR_RFQ, recipient_name="Test", language=Language.JAPANESE)
        draft = composer.compose(ctx)
        markdown_output = draft.to_markdown()

        output_file = tmp_path / "email_draft.md"
        output_file.write_text(markdown_output, encoding="utf-8")

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "# Email Draft" in content


class TestAllEmailTypes:
    """Test all email types have proper templates."""

    @pytest.fixture
    def composer(self):
        """Create EmailComposer instance."""
        return EmailComposer()

    @pytest.mark.parametrize("email_type", list(EmailType))
    def test_all_types_have_japanese_templates(self, composer, email_type):
        """Test all email types work with Japanese."""
        ctx = EmailContext(
            email_type=email_type, recipient_name="テスト", language=Language.JAPANESE, sender_name="送信者"
        )
        draft = composer.compose(ctx)
        assert draft.email_type == email_type.value
        assert draft.language == "ja"
        assert len(draft.subject) > 0
        assert len(draft.greeting) > 0
        assert len(draft.closing) > 0

    @pytest.mark.parametrize("email_type", list(EmailType))
    def test_all_types_have_english_templates(self, composer, email_type):
        """Test all email types work with English."""
        ctx = EmailContext(
            email_type=email_type, recipient_name="Test", language=Language.ENGLISH, sender_name="Sender"
        )
        draft = composer.compose(ctx)
        assert draft.email_type == email_type.value
        assert draft.language == "en"
        assert len(draft.subject) > 0
        assert len(draft.greeting) > 0
        assert len(draft.closing) > 0
