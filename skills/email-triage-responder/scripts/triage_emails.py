#!/usr/bin/env python3
"""
Email Triage and Response Draft Generator

Analyzes emails to classify by topic, prioritize by urgency/importance,
and generate contextual draft responses.
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional


class Quadrant(Enum):
    """Eisenhower Matrix quadrants."""

    Q1_URGENT_IMPORTANT = "Q1"
    Q2_IMPORTANT_NOT_URGENT = "Q2"
    Q3_URGENT_NOT_IMPORTANT = "Q3"
    Q4_NEITHER = "Q4"


class Topic(Enum):
    """Email topic categories."""

    CLIENT_FOLLOWUP = "client_followup"
    INTERNAL_REQUEST = "internal_request"
    VENDOR_INQUIRY = "vendor_inquiry"
    MEETING_SCHEDULING = "meeting_scheduling"
    FYI_INFORMATIONAL = "fyi_informational"
    APPROVAL_REQUIRED = "approval_required"
    ESCALATION = "escalation"
    DELEGATION_CANDIDATE = "delegation_candidate"


class ActionType(Enum):
    """Required action types."""

    RESPOND = "respond"
    REVIEW = "review"
    DELEGATE = "delegate"
    ARCHIVE = "archive"


class Status(Enum):
    """Email processing status."""

    PENDING = "pending"
    DRAFT_READY = "draft_ready"
    SENT = "sent"
    DELEGATED = "delegated"
    ARCHIVED = "archived"


@dataclass
class EmailAnalysis:
    """Analysis result for a single email."""

    id: str
    from_address: str
    subject: str
    received_at: str
    quadrant: str
    urgency_score: float
    importance_score: float
    topic: str
    action_required: str
    detected_deadline: Optional[str] = None
    draft_response: Optional[str] = None
    status: str = "pending"
    language: str = "en"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class TriageReport:
    """Complete triage report."""

    schema_version: str = "1.0"
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    summary: dict = field(default_factory=dict)
    emails: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "summary": self.summary,
            "emails": [e.to_dict() if isinstance(e, EmailAnalysis) else e for e in self.emails],
        }


# Urgency detection patterns
URGENCY_HIGH_PATTERNS = [
    r"\b(urgent|asap|immediately|critical|emergency)\b",
    r"\b(by eod|end of day|within 24 hours|today)\b",
    r"\b(second request|following up again|still waiting)\b",
    r"\[urgent\]|\[action required\]|\[time sensitive\]",
]

URGENCY_MEDIUM_PATTERNS = [
    r"\b(this week|when you get a chance|soon)\b",
    r"\b(please review|let me know|can you check)\b",
    r"\b(before our meeting|for tomorrow)\b",
    r"\b(checking in|wanted to follow up)\b",
]

URGENCY_LOW_PATTERNS = [
    r"\b(fyi|for your information|no action needed)\b",
    r"\b(for your records|next quarter|eventually)\b",
    r"\b(newsletter|announcement|digest)\b",
]

# Topic detection patterns
TOPIC_PATTERNS = {
    Topic.CLIENT_FOLLOWUP: [
        r"\b(client|customer|account)\b",
        r"\b(project status|deliverable|milestone)\b",
    ],
    Topic.INTERNAL_REQUEST: [
        r"\b(request|need|please|can you|would you)\b",
        r"\b(help with|assist|support)\b",
    ],
    Topic.VENDOR_INQUIRY: [
        r"\b(invoice|quote|proposal|pricing)\b",
        r"\b(renewal|contract|vendor|supplier)\b",
    ],
    Topic.MEETING_SCHEDULING: [
        r"\b(meeting|call|schedule|availability)\b",
        r"\b(calendar|invite|conference)\b",
    ],
    Topic.FYI_INFORMATIONAL: [
        r"\b(fyi|for your information|heads up)\b",
        r"\b(newsletter|update|announcement)\b",
    ],
    Topic.APPROVAL_REQUIRED: [
        r"\b(approve|approval|sign off)\b",
        r"\b(authorize|confirm|permission)\b",
    ],
    Topic.ESCALATION: [
        r"\b(escalate|escalation|urgent|asap)\b",
        r"\b(immediately|critical|blocked)\b",
    ],
}

# VIP sender patterns (customize per organization)
VIP_PATTERNS = [
    r"ceo@|cfo@|cto@|president@",
    r"vp[-_]|vice[-_]president",
    r"director@|board@",
]

# Deadline detection patterns
DEADLINE_PATTERNS = [
    r"by\s+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)",
    r"by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    r"by\s+(eod|end of day|cob|close of business)",
    r"deadline[:\s]+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)",
    r"due[:\s]+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)",
]


def detect_language(text: str) -> str:
    """Detect language from text content."""
    # Check for Japanese characters
    if re.search(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]", text):
        return "ja"
    # Check for Chinese (no Japanese kana)
    if re.search(r"[\u4E00-\u9FAF]", text) and not re.search(r"[\u3040-\u309F\u30A0-\u30FF]", text):
        return "zh"
    # Default to English
    return "en"


def calculate_urgency_score(subject: str, body: str) -> float:
    """Calculate urgency score from 0.0 to 1.0."""
    text = f"{subject} {body}".lower()
    score = 0.3  # Base score

    # Check high urgency patterns
    for pattern in URGENCY_HIGH_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            score = max(score, 0.85)
            break

    # Check medium urgency patterns
    for pattern in URGENCY_MEDIUM_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            score = max(score, 0.55)
            break

    # Check low urgency patterns (decreases score)
    for pattern in URGENCY_LOW_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            score = min(score, 0.2)
            break

    return round(score, 2)


def calculate_importance_score(from_address: str, to_addresses: list, cc_addresses: list) -> float:
    """Calculate importance score from 0.0 to 1.0."""
    score = 0.5  # Base score

    # Check for VIP sender
    for pattern in VIP_PATTERNS:
        if re.search(pattern, from_address.lower()):
            score = max(score, 0.9)
            break

    # Direct recipient bonus
    if len(to_addresses) == 1:
        score += 0.15  # Only recipient
    elif len(to_addresses) <= 3:
        score += 0.1  # Small group

    # Large CC list decreases importance
    if len(cc_addresses) > 10:
        score -= 0.1

    return round(min(1.0, max(0.0, score)), 2)


def classify_topic(subject: str, body: str) -> Topic:
    """Classify email into topic category."""
    text = f"{subject} {body}".lower()

    topic_scores = {}
    for topic, patterns in TOPIC_PATTERNS.items():
        topic_scores[topic] = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                topic_scores[topic] += 1

    # Return topic with highest score, default to INTERNAL_REQUEST
    if max(topic_scores.values()) > 0:
        return max(topic_scores, key=topic_scores.get)
    return Topic.INTERNAL_REQUEST


def determine_quadrant(urgency: float, importance: float) -> Quadrant:
    """Determine Eisenhower Matrix quadrant."""
    if urgency >= 0.6 and importance >= 0.6:
        return Quadrant.Q1_URGENT_IMPORTANT
    elif urgency < 0.6 and importance >= 0.6:
        return Quadrant.Q2_IMPORTANT_NOT_URGENT
    elif urgency >= 0.6 and importance < 0.6:
        return Quadrant.Q3_URGENT_NOT_IMPORTANT
    else:
        return Quadrant.Q4_NEITHER


def determine_action(quadrant: Quadrant, topic: Topic) -> ActionType:
    """Determine required action based on quadrant and topic."""
    if quadrant == Quadrant.Q1_URGENT_IMPORTANT:
        return ActionType.RESPOND
    elif quadrant == Quadrant.Q2_IMPORTANT_NOT_URGENT:
        if topic == Topic.APPROVAL_REQUIRED:
            return ActionType.REVIEW
        return ActionType.RESPOND
    elif quadrant == Quadrant.Q3_URGENT_NOT_IMPORTANT:
        if topic == Topic.DELEGATION_CANDIDATE:
            return ActionType.DELEGATE
        return ActionType.RESPOND
    else:
        if topic == Topic.FYI_INFORMATIONAL:
            return ActionType.ARCHIVE
        return ActionType.RESPOND


def detect_deadline(subject: str, body: str) -> Optional[str]:
    """Extract deadline from email content."""
    text = f"{subject} {body}"

    for pattern in DEADLINE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            deadline_text = match.group(1)
            # Try to parse as date
            try:
                # Handle various formats
                if "/" in deadline_text:
                    parts = deadline_text.split("/")
                    if len(parts) == 2:
                        month, day = int(parts[0]), int(parts[1])
                        year = datetime.now().year
                        deadline = datetime(year, month, day, 17, 0)  # Default 5 PM
                        return deadline.isoformat() + "Z"
                elif deadline_text.lower() in ["eod", "end of day", "cob", "close of business"]:
                    deadline = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
                    return deadline.isoformat() + "Z"
                else:
                    # Day of week
                    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                    if deadline_text.lower() in days:
                        target_day = days.index(deadline_text.lower())
                        today = datetime.now()
                        days_ahead = target_day - today.weekday()
                        if days_ahead <= 0:
                            days_ahead += 7
                        deadline = today + timedelta(days=days_ahead)
                        deadline = deadline.replace(hour=17, minute=0, second=0, microsecond=0)
                        return deadline.isoformat() + "Z"
            except (ValueError, IndexError):
                pass

    return None


def generate_draft_response(
    email: dict, analysis: EmailAnalysis, tone: str = "professional", sender_name: str = "User"
) -> str:
    """Generate a contextual draft response."""
    topic = analysis.topic
    action = analysis.action_required
    language = analysis.language

    # Basic templates
    templates = {
        "acknowledge": {
            "en": {
                "professional": f"Thank you for your email regarding {email.get('subject', 'your inquiry')}.\n\nI've received your message and will review it shortly. I'll follow up with a detailed response by {{deadline}}.\n\nBest regards,\n{sender_name}",
                "friendly": f"Thanks for reaching out about {email.get('subject', 'this')}!\n\nGot it - I'll take a look and get back to you soon.\n\nCheers,\n{sender_name}",
            },
            "ja": {
                "professional": f"{email.get('subject', 'お問い合わせ')}についてメールをいただきありがとうございます。\n\nメッセージを受領いたしました。確認の上、{{deadline}}までに詳細をご連絡いたします。\n\nよろしくお願いいたします。\n{sender_name}",
            },
        },
        "respond": {
            "en": {
                "professional": f"Thank you for your email.\n\nRegarding {email.get('subject', 'your inquiry')}:\n\n[Your response here]\n\nPlease let me know if you have any questions.\n\nBest regards,\n{sender_name}",
                "friendly": f"Thanks for your email!\n\nAbout {email.get('subject', 'this')}:\n\n[Your response here]\n\nLet me know if you need anything else!\n\nCheers,\n{sender_name}",
            },
            "ja": {
                "professional": f"メールをいただきありがとうございます。\n\n{email.get('subject', 'お問い合わせ')}について:\n\n[回答内容]\n\nご不明な点がございましたら、お気軽にお問い合わせください。\n\nよろしくお願いいたします。\n{sender_name}",
            },
        },
        "delegate": {
            "en": {
                "professional": f"Thank you for your email.\n\nI'm forwarding this to [colleague name] who handles [area] and is best positioned to assist you.\n\nThey will follow up with you directly.\n\nBest regards,\n{sender_name}",
            },
            "ja": {
                "professional": f"メールをいただきありがとうございます。\n\n[担当分野]を担当している[同僚名]に転送いたします。直接ご連絡させていただきます。\n\nよろしくお願いいたします。\n{sender_name}",
            },
        },
    }

    # Select template based on action
    if action == ActionType.DELEGATE.value:
        template_key = "delegate"
    elif analysis.quadrant in [Quadrant.Q1_URGENT_IMPORTANT.value, "Q1"]:
        template_key = "respond"
    else:
        template_key = "acknowledge"

    # Get template for language and tone
    lang_templates = templates.get(template_key, templates["acknowledge"])
    tone_templates = lang_templates.get(language, lang_templates.get("en", {}))
    template = tone_templates.get(tone, tone_templates.get("professional", ""))

    # Replace deadline placeholder
    if analysis.detected_deadline:
        try:
            deadline_dt = datetime.fromisoformat(analysis.detected_deadline.replace("Z", "+00:00"))
            deadline_str = deadline_dt.strftime("%B %d")
        except ValueError:
            deadline_str = "end of week"
    else:
        deadline_str = "end of week"

    template = template.replace("{{deadline}}", deadline_str)

    return template


def analyze_email(email: dict, generate_drafts: bool = False, tone: str = "professional") -> EmailAnalysis:
    """Analyze a single email and return analysis."""
    subject = email.get("subject", "")
    body = email.get("body", email.get("snippet", ""))
    from_address = email.get("from", email.get("from_address", ""))
    to_addresses = email.get("to", [])
    cc_addresses = email.get("cc", [])

    # Calculate scores
    urgency = calculate_urgency_score(subject, body)
    importance = calculate_importance_score(from_address, to_addresses, cc_addresses)

    # Classify
    quadrant = determine_quadrant(urgency, importance)
    topic = classify_topic(subject, body)
    action = determine_action(quadrant, topic)
    deadline = detect_deadline(subject, body)
    language = detect_language(f"{subject} {body}")

    analysis = EmailAnalysis(
        id=email.get("id", email.get("message_id", "unknown")),
        from_address=from_address,
        subject=subject,
        received_at=email.get("received_at", email.get("date", datetime.utcnow().isoformat() + "Z")),
        quadrant=quadrant.value,
        urgency_score=urgency,
        importance_score=importance,
        topic=topic.value,
        action_required=action.value,
        detected_deadline=deadline,
        status="pending",
        language=language,
    )

    # Generate draft if requested
    if generate_drafts and action != ActionType.ARCHIVE:
        analysis.draft_response = generate_draft_response(email, analysis, tone)
        analysis.status = "draft_ready"

    return analysis


def generate_summary(analyses: list) -> dict:
    """Generate summary statistics from analyses."""
    total = len(analyses)
    action_required = sum(1 for a in analyses if a.action_required != ActionType.ARCHIVE.value)

    by_quadrant = {
        "Q1_urgent_important": 0,
        "Q2_important_not_urgent": 0,
        "Q3_urgent_not_important": 0,
        "Q4_neither": 0,
    }

    by_topic = {}

    for analysis in analyses:
        # Count quadrants
        q = analysis.quadrant
        if q == "Q1":
            by_quadrant["Q1_urgent_important"] += 1
        elif q == "Q2":
            by_quadrant["Q2_important_not_urgent"] += 1
        elif q == "Q3":
            by_quadrant["Q3_urgent_not_important"] += 1
        else:
            by_quadrant["Q4_neither"] += 1

        # Count topics
        topic = analysis.topic
        by_topic[topic] = by_topic.get(topic, 0) + 1

    return {
        "total_emails": total,
        "action_required": action_required,
        "by_quadrant": by_quadrant,
        "by_topic": by_topic,
    }


def generate_markdown_report(report: TriageReport) -> str:
    """Generate markdown format report."""
    lines = [
        "# Email Triage Report",
        "",
        f"**Generated**: {report.generated_at}",
        f"**Total Emails**: {report.summary.get('total_emails', 0)} | **Action Required**: {report.summary.get('action_required', 0)}",
        "",
        "## Priority Matrix",
        "",
    ]

    # Group by quadrant
    quadrants = {
        "Q1": ("Q1: Urgent & Important", []),
        "Q2": ("Q2: Important, Not Urgent", []),
        "Q3": ("Q3: Urgent, Not Important", []),
        "Q4": ("Q4: Neither Urgent nor Important", []),
    }

    for email in report.emails:
        # `email` may be either an EmailAnalysis dataclass (typical when called
        # programmatically) or a plain dict (when reloaded from JSON). Branch
        # on the type before reaching for `.get(...)` — the previous code did
        # the dict-only call first and crashed on the dataclass path.
        if isinstance(email, EmailAnalysis):
            q = email.quadrant
        else:
            q = email.get("quadrant", "Q4")
        if q in quadrants:
            quadrants[q][1].append(email)

    for q_key, (q_name, emails) in quadrants.items():
        if emails:
            lines.append(f"### {q_name} ({len(emails)} emails)")
            lines.append("")
            lines.append("| From | Subject | Action | Status |")
            lines.append("|------|---------|--------|--------|")
            for email in emails:
                if isinstance(email, EmailAnalysis):
                    from_addr = email.from_address
                    subject = email.subject[:40] + "..." if len(email.subject) > 40 else email.subject
                    action = email.action_required
                    status = email.status
                else:
                    from_addr = email.get("from_address", "")
                    subj = email.get("subject", "")
                    subject = subj[:40] + "..." if len(subj) > 40 else subj
                    action = email.get("action_required", "")
                    status = email.get("status", "pending")
                lines.append(f"| {from_addr} | {subject} | {action} | {status} |")
            lines.append("")

    # Topic breakdown
    lines.append("## Topic Breakdown")
    lines.append("")
    by_topic = report.summary.get("by_topic", {})
    for topic, count in sorted(by_topic.items(), key=lambda x: -x[1]):
        topic_display = topic.replace("_", " ").title()
        lines.append(f"- {topic_display}: {count}")
    lines.append("")

    # Recommended actions
    lines.append("## Recommended Actions")
    lines.append("")
    q1_count = report.summary.get("by_quadrant", {}).get("Q1_urgent_important", 0)
    q2_count = report.summary.get("by_quadrant", {}).get("Q2_important_not_urgent", 0)
    q3_count = report.summary.get("by_quadrant", {}).get("Q3_urgent_not_important", 0)

    if q1_count > 0:
        lines.append(f"1. **Respond immediately** to {q1_count} Q1 emails")
    if q2_count > 0:
        lines.append(f"2. **Schedule focused time** for {q2_count} Q2 emails")
    if q3_count > 0:
        lines.append(f"3. **Delegate or quick reply** to {q3_count} Q3 emails")

    return "\n".join(lines)


def load_emails(input_path: Path) -> list:
    """Load emails from JSON file."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle both list and dict with "emails" key
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "emails" in data:
        return data["emails"]
    elif isinstance(data, dict) and "messages" in data:
        return data["messages"]
    else:
        return [data]


def update_status_file(status_file: Path, analyses: list) -> None:
    """Update or create status tracking file."""
    existing = {}
    if status_file.exists():
        with open(status_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            existing = {e["email_id"]: e for e in data.get("emails", [])}

    # Update with new analyses
    for analysis in analyses:
        email_id = analysis.id
        existing[email_id] = {
            "email_id": email_id,
            "status": analysis.status,
            "assigned_to": None,
            "due_date": analysis.detected_deadline,
            "last_updated": datetime.utcnow().isoformat() + "Z",
        }

    # Write back
    output = {
        "schema_version": "1.0",
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "emails": list(existing.values()),
    }

    with open(status_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Email Triage and Response Draft Generator")
    parser.add_argument("--input", "-i", type=Path, required=True, help="Input JSON file with emails")
    parser.add_argument("--output", "-o", type=Path, help="Output file path (JSON or Markdown based on extension)")
    parser.add_argument(
        "--format", "-f", choices=["json", "markdown"], default="json", help="Output format (default: json)"
    )
    parser.add_argument(
        "--generate-drafts", action="store_true", help="Generate draft responses for action-required emails"
    )
    parser.add_argument(
        "--tone",
        choices=["professional", "friendly", "formal"],
        default="professional",
        help="Tone for draft responses (default: professional)",
    )
    parser.add_argument("--status-file", type=Path, help="Path to status tracking file")
    parser.add_argument("--update-status", action="store_true", help="Update status tracking file")

    args = parser.parse_args()

    # Validate input
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Load and analyze emails
    try:
        emails = load_emails(args.input)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
        sys.exit(1)

    analyses = [analyze_email(email, args.generate_drafts, args.tone) for email in emails]

    # Generate report
    summary = generate_summary(analyses)
    report = TriageReport(
        summary=summary,
        emails=analyses,
    )

    # Output
    if args.format == "markdown" or (args.output and args.output.suffix == ".md"):
        output_content = generate_markdown_report(report)
    else:
        output_content = json.dumps(report.to_dict(), indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"Report written to: {args.output}")
    else:
        print(output_content)

    # Update status file if requested
    if args.update_status and args.status_file:
        update_status_file(args.status_file, analyses)
        print(f"Status file updated: {args.status_file}")

    sys.exit(0)


if __name__ == "__main__":
    main()
