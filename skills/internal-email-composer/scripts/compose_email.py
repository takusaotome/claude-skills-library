#!/usr/bin/env python3
"""
Internal Email Composer

Generates professional internal email drafts for common coordination tasks
in bilingual (Japanese/English) format with proper business tone.
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class EmailType(Enum):
    """Supported email types."""

    VENDOR_RFQ = "vendor_rfq"
    TASK_DELEGATION = "task_delegation"
    STATUS_UPDATE = "status_update"
    FOLLOW_UP = "follow_up"
    ESCALATION = "escalation"
    INFO_REQUEST = "info_request"


class Language(Enum):
    """Supported languages."""

    JAPANESE = "ja"
    ENGLISH = "en"


class Urgency(Enum):
    """Email urgency levels."""

    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class EmailContext:
    """Context for email generation."""

    email_type: EmailType
    recipient_name: str
    recipient_role: str = ""
    recipient_department: str = ""
    language: Language = Language.JAPANESE
    key_points: list = field(default_factory=list)
    deadline: str = ""
    attachments: list = field(default_factory=list)
    urgency: Urgency = Urgency.NORMAL
    sender_name: str = ""
    sender_department: str = ""
    sender_contact: str = ""
    project_name: str = ""
    additional_context: dict = field(default_factory=dict)


@dataclass
class EmailDraft:
    """Generated email draft."""

    email_type: str
    language: str
    generated_at: str
    subject: str
    recipient: dict
    greeting: str
    body: str
    closing: str
    signature: dict

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "schema_version": "1.0",
            "email_type": self.email_type,
            "language": self.language,
            "generated_at": self.generated_at,
            "subject": self.subject,
            "recipient": self.recipient,
            "body": {"greeting": self.greeting, "main_content": self.body, "closing": self.closing},
            "signature": self.signature,
        }

    def to_markdown(self) -> str:
        """Convert to markdown format."""
        lines = [
            "# Email Draft",
            "",
            f"**Type**: {self.email_type}",
            f"**Language**: {self.language}",
            f"**Generated**: {self.generated_at}",
            "",
            "---",
            "",
            "## Subject",
            self.subject,
            "",
            "## To",
            f"{self.recipient.get('name', '')}",
        ]
        if self.recipient.get("role"):
            lines[-1] += f"（{self.recipient['role']}）"

        lines.extend(
            [
                "",
                "## Body",
                "",
                self.greeting,
                "",
                self.body,
                "",
                self.closing,
                "",
                "---",
            ]
        )

        if self.signature:
            if self.signature.get("name"):
                lines.append(self.signature["name"])
            if self.signature.get("department"):
                lines.append(self.signature["department"])
            if self.signature.get("contact"):
                lines.append(self.signature["contact"])

        return "\n".join(lines)


class EmailComposer:
    """Main email composition engine."""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> dict:
        """Load email templates."""
        return {
            EmailType.VENDOR_RFQ: {
                Language.JAPANESE: {
                    "subject_prefix": "見積依頼の件",
                    "greeting": "お疲れ様です。{sender_department}の{sender_name}です。",
                    "intro": "{project_name}に関する見積依頼書を送付いたします。\n下記の内容をご確認の上、各ベンダーへのご連絡をお願いできますでしょうか。",
                    "closing": "ご不明点がございましたら、お気軽にお問い合わせください。\nよろしくお願いいたします。",
                },
                Language.ENGLISH: {
                    "subject_prefix": "RFQ Request",
                    "greeting": "Dear {recipient_name},\n\nI hope this email finds you well.",
                    "intro": "I am writing to forward the Request for Quotation (RFQ) documents for the {project_name} project. Could you please coordinate with the vendors to obtain their quotes?",
                    "closing": "Please let me know if you have any questions or need additional information.\n\nBest regards,",
                },
            },
            EmailType.TASK_DELEGATION: {
                Language.JAPANESE: {
                    "subject_prefix": "【依頼】",
                    "greeting": "お疲れ様です。{sender_name}です。",
                    "intro": "下記の作業をお願いしたくご連絡いたしました。",
                    "closing": "ご質問や不明点がございましたら、いつでもお声がけください。\nお忙しいところ恐れ入りますが、よろしくお願いいたします。",
                },
                Language.ENGLISH: {
                    "subject_prefix": "Task Request:",
                    "greeting": "Hi {recipient_name},\n\nI hope you're doing well.",
                    "intro": "I'd like to request your assistance with the following task.",
                    "closing": "Please feel free to reach out if you have any questions or need clarification.\n\nThank you for your help.\n\nBest regards,",
                },
            },
            EmailType.STATUS_UPDATE: {
                Language.JAPANESE: {
                    "subject_prefix": "【進捗報告】",
                    "greeting": "各位\n\nお疲れ様です。{sender_name}です。",
                    "intro": "{project_name}の進捗状況をご報告いたします。",
                    "closing": "ご質問がございましたらお知らせください。",
                },
                Language.ENGLISH: {
                    "subject_prefix": "Status Update:",
                    "greeting": "Team,",
                    "intro": "Please find below the status update for the {project_name} project.",
                    "closing": "Please let me know if you have any questions.\n\nRegards,",
                },
            },
            EmailType.FOLLOW_UP: {
                Language.JAPANESE: {
                    "subject_prefix": "【再送】",
                    "greeting": "お疲れ様です。{sender_name}です。",
                    "intro": "先日お送りした件について、確認のためご連絡いたしました。",
                    "closing": "お忙しいところ恐れ入りますが、ご確認・ご対応いただけますと幸いです。\n何かお手伝いできることがございましたら、お知らせください。\n\nよろしくお願いいたします。",
                },
                Language.ENGLISH: {
                    "subject_prefix": "Follow-up:",
                    "greeting": "Dear {recipient_name},\n\nI hope this email finds you well.",
                    "intro": "I wanted to follow up on my previous email regarding the matter below.",
                    "closing": "I understand you may have a busy schedule. Please let me know if you need any additional information or if there's anything I can do to help.\n\nThank you for your attention to this matter.\n\nBest regards,",
                },
            },
            EmailType.ESCALATION: {
                Language.JAPANESE: {
                    "subject_prefix": "【エスカレーション】",
                    "greeting": "お疲れ様です。{sender_name}です。",
                    "intro": "下記の件について、エスカレーションのためご連絡いたします。",
                    "closing": "ご多用のところ恐れ入りますが、ご支援いただけますと幸いです。\n詳細についてご説明が必要でしたら、いつでもお時間を頂戴できればと存じます。\n\nよろしくお願いいたします。",
                },
                Language.ENGLISH: {
                    "subject_prefix": "[Escalation]",
                    "greeting": "Dear {recipient_name},",
                    "intro": "I am writing to escalate an issue that requires your attention and support.",
                    "closing": "I would appreciate your guidance on how to proceed. Please let me know if you would like to schedule a meeting to discuss this further.\n\nThank you for your attention to this urgent matter.\n\nBest regards,",
                },
            },
            EmailType.INFO_REQUEST: {
                Language.JAPANESE: {
                    "subject_prefix": "【情報提供のお願い】",
                    "greeting": "お疲れ様です。{sender_name}です。",
                    "intro": "下記の情報をご提供いただきたくお願いいたします。",
                    "closing": "ご不明点がございましたら、お気軽にお問い合わせください。\nお手数をおかけしますが、よろしくお願いいたします。",
                },
                Language.ENGLISH: {
                    "subject_prefix": "Information Request:",
                    "greeting": "Dear {recipient_name},\n\nI hope this message finds you well.",
                    "intro": "I am reaching out to request the following information.",
                    "closing": "Please let me know if you have any questions or need clarification on the request.\n\nThank you in advance for your assistance.\n\nBest regards,",
                },
            },
        }

    def _get_urgency_prefix(self, urgency: Urgency, language: Language) -> str:
        """Get urgency prefix for subject line."""
        if urgency == Urgency.NORMAL:
            return ""
        if language == Language.JAPANESE:
            return "【至急】" if urgency == Urgency.HIGH else "【緊急】"
        return "Time-Sensitive: " if urgency == Urgency.HIGH else "URGENT: "

    def _format_key_points(self, key_points: list, language: Language) -> str:
        """Format key points as bullet list."""
        if not key_points:
            return ""

        bullet = "・" if language == Language.JAPANESE else "- "
        return "\n".join(f"{bullet}{point}" for point in key_points)

    def _build_subject(self, ctx: EmailContext, template: dict) -> str:
        """Build email subject line."""
        urgency_prefix = self._get_urgency_prefix(ctx.urgency, ctx.language)
        subject_prefix = template["subject_prefix"]

        if ctx.project_name:
            if ctx.language == Language.JAPANESE:
                subject = f"{urgency_prefix}{subject_prefix}（{ctx.project_name}）"
            else:
                subject = f"{urgency_prefix}{subject_prefix} {ctx.project_name}"
        else:
            subject = f"{urgency_prefix}{subject_prefix}"

        return subject

    def _build_body(self, ctx: EmailContext, template: dict) -> str:
        """Build email body content."""
        body_parts = []

        # Introduction
        intro = template["intro"].format(
            project_name=ctx.project_name or "the project",
            sender_name=ctx.sender_name,
            sender_department=ctx.sender_department,
        )
        body_parts.append(intro)

        # Key points section
        if ctx.key_points:
            if ctx.language == Language.JAPANESE:
                body_parts.append("\n【依頼内容】")
            else:
                body_parts.append("\n**Request Details:**")
            body_parts.append(self._format_key_points(ctx.key_points, ctx.language))

        # Deadline
        if ctx.deadline:
            if ctx.language == Language.JAPANESE:
                body_parts.append(f"\n【期限】\n{ctx.deadline}")
            else:
                body_parts.append(f"\n**Deadline:** {ctx.deadline}")

        # Attachments
        if ctx.attachments:
            if ctx.language == Language.JAPANESE:
                body_parts.append(f"\n【添付資料】\n{self._format_key_points(ctx.attachments, ctx.language)}")
            else:
                body_parts.append(f"\n**Attachments:**\n{self._format_key_points(ctx.attachments, ctx.language)}")

        return "\n".join(body_parts)

    def compose(self, ctx: EmailContext) -> EmailDraft:
        """Compose email draft from context."""
        template = self.templates.get(ctx.email_type, {}).get(ctx.language, {})

        if not template:
            raise ValueError(f"No template found for {ctx.email_type.value} in {ctx.language.value}")

        # Build greeting
        greeting = template["greeting"].format(
            recipient_name=ctx.recipient_name,
            sender_name=ctx.sender_name or "Your Name",
            sender_department=ctx.sender_department or "Your Department",
        )

        # Build subject
        subject = self._build_subject(ctx, template)

        # Build body
        body = self._build_body(ctx, template)

        # Build closing
        closing = template["closing"]

        # Build signature
        signature = {}
        if ctx.sender_name:
            signature["name"] = ctx.sender_name
        if ctx.sender_department:
            signature["department"] = ctx.sender_department
        if ctx.sender_contact:
            signature["contact"] = ctx.sender_contact

        return EmailDraft(
            email_type=ctx.email_type.value,
            language=ctx.language.value,
            generated_at=datetime.now().isoformat(),
            subject=subject,
            recipient={"name": ctx.recipient_name, "role": ctx.recipient_role, "department": ctx.recipient_department},
            greeting=greeting,
            body=body,
            closing=closing,
            signature=signature,
        )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Compose professional internal business emails",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Vendor RFQ email in Japanese
  python3 compose_email.py --type vendor_rfq --recipient-name "田中様" \\
    --language ja --key-points "AWS見積依頼" --deadline "12月20日"

  # Task delegation email in English
  python3 compose_email.py --type task_delegation --recipient-name "John" \\
    --language en --key-points "Review Q4 budget report" --deadline "Dec 15"
        """,
    )

    parser.add_argument(
        "--type", "-t", type=str, required=True, choices=[e.value for e in EmailType], help="Email type"
    )
    parser.add_argument("--recipient-name", "-r", type=str, required=True, help="Recipient name")
    parser.add_argument("--recipient-role", type=str, default="", help="Recipient role/title")
    parser.add_argument("--recipient-department", type=str, default="", help="Recipient department")
    parser.add_argument(
        "--language",
        "-l",
        type=str,
        default="ja",
        choices=[e.value for e in Language],
        help="Email language (default: ja)",
    )
    parser.add_argument("--key-points", "-k", type=str, nargs="+", default=[], help="Key points to include")
    parser.add_argument("--deadline", "-d", type=str, default="", help="Response/action deadline")
    parser.add_argument("--attachments", "-a", type=str, nargs="+", default=[], help="List of attachments")
    parser.add_argument(
        "--urgency",
        "-u",
        type=str,
        default="normal",
        choices=[e.value for e in Urgency],
        help="Urgency level (default: normal)",
    )
    parser.add_argument("--sender-name", type=str, default="", help="Sender name")
    parser.add_argument("--sender-department", type=str, default="", help="Sender department")
    parser.add_argument("--sender-contact", type=str, default="", help="Sender contact info")
    parser.add_argument("--project-name", "-p", type=str, default="", help="Project name for context")
    parser.add_argument("--output", "-o", type=str, help="Output file path (default: stdout)")
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        default="markdown",
        choices=["markdown", "json"],
        help="Output format (default: markdown)",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Build context
    ctx = EmailContext(
        email_type=EmailType(args.type),
        recipient_name=args.recipient_name,
        recipient_role=args.recipient_role,
        recipient_department=args.recipient_department,
        language=Language(args.language),
        key_points=args.key_points,
        deadline=args.deadline,
        attachments=args.attachments,
        urgency=Urgency(args.urgency),
        sender_name=args.sender_name,
        sender_department=args.sender_department,
        sender_contact=args.sender_contact,
        project_name=args.project_name,
    )

    # Compose email
    composer = EmailComposer()
    try:
        draft = composer.compose(ctx)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Format output
    if args.format == "json":
        output = json.dumps(draft.to_dict(), ensure_ascii=False, indent=2)
    else:
        output = draft.to_markdown()

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding="utf-8")
        print(f"Email draft written to: {output_path}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
