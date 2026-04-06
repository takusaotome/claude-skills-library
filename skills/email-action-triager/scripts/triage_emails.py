#!/usr/bin/env python3
"""
Email Action Triager - Main triage script

Analyzes inbox emails to identify actionable items, categorize by urgency/owner,
and generate prioritized daily action lists.

Supports:
- Gmail API integration for live inbox access
- Local file processing (MBOX, EML formats)
- Configurable business rules for prioritization
- Multiple output formats (JSON, Markdown)
"""

import argparse
import json
import mailbox
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Optional


@dataclass
class EmailMessage:
    """Represents a parsed email message."""

    id: str
    subject: str
    sender: str
    sender_name: str
    recipients: list[str]
    cc: list[str]
    received_at: datetime
    body_text: str
    body_html: str
    attachments: list[str]
    thread_id: Optional[str] = None
    labels: list[str] = field(default_factory=list)
    is_unread: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        d = asdict(self)
        d["received_at"] = self.received_at.isoformat()
        return d


@dataclass
class ActionItem:
    """Represents a triaged action item from an email."""

    id: str
    subject: str
    sender: str
    sender_name: str
    sender_priority: str
    received_at: datetime
    urgency_score: int
    urgency_level: str
    action_type: str
    deadline_detected: Optional[str]
    project_association: Optional[str]
    recommended_action: str
    suggested_response: Optional[str]
    delegation_candidate: Optional[str]
    context_tags: list[str]
    body_preview: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        d = asdict(self)
        d["received_at"] = self.received_at.isoformat()
        return d


class BusinessRules:
    """Manages business rules for email prioritization."""

    def __init__(self, rules_path: Optional[str] = None):
        """Initialize with optional rules file path."""
        self.rules = self._load_default_rules()
        if rules_path and Path(rules_path).exists():
            self._merge_rules(rules_path)

    def _load_default_rules(self) -> dict:
        """Load default business rules."""
        return {
            "sender_priority": {
                "vip": ["ceo@*", "cfo@*", "cto@*"],
                "high": ["*-manager@*", "*@legal.*"],
                "normal": [],
                "low": ["noreply@*", "no-reply@*", "*@newsletter.*"],
            },
            "urgency_keywords": {
                "boost_high": ["URGENT", "ASAP", "CRITICAL", "EMERGENCY"],
                "boost_medium": ["Important", "Priority", "Action required"],
                "boost_low": ["Please review", "Follow up", "Reminder"],
                "reduce_medium": ["FYI", "For your information", "No action required"],
                "reduce_high": ["Automated", "Newsletter", "Digest"],
            },
            "deadline_patterns": {
                "relative_phrases": {
                    "immediate": ["ASAP", "immediately", "urgent"],
                    "today": ["by EOD", "by end of day", "today"],
                    "tomorrow": ["by tomorrow", "by EOD tomorrow"],
                    "this_week": ["by end of week", "by EOW", "by Friday"],
                    "next_week": ["by next week", "early next week"],
                }
            },
            "delegation_rules": {"enabled": True, "content_rules": []},
            "project_associations": {},
            "auto_archive": {"enabled": True, "patterns": []},
        }

    def _merge_rules(self, rules_path: str) -> None:
        """Merge custom rules from YAML file."""
        try:
            import yaml

            with open(rules_path, "r") as f:
                custom_rules = yaml.safe_load(f)
            self._deep_merge(self.rules, custom_rules)
        except ImportError:
            print("Warning: PyYAML not installed. Using default rules.", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Could not load rules file: {e}", file=sys.stderr)

    def _deep_merge(self, base: dict, override: dict) -> None:
        """Deep merge override into base dict."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get_sender_priority(self, sender: str) -> str:
        """Determine sender priority tier."""
        sender_lower = sender.lower()
        for tier in ["vip", "high", "low"]:
            patterns = self.rules["sender_priority"].get(tier, [])
            for pattern in patterns:
                if self._match_pattern(sender_lower, pattern.lower()):
                    return tier.upper()
        return "NORMAL"

    def _match_pattern(self, email: str, pattern: str) -> bool:
        """Match email against wildcard pattern."""
        regex = pattern.replace(".", r"\.").replace("*", ".*")
        return bool(re.match(f"^{regex}$", email))

    def detect_deadline(self, text: str) -> Optional[str]:
        """Detect deadline from email text."""
        text_lower = text.lower()

        # Check relative phrases
        phrases = self.rules["deadline_patterns"].get("relative_phrases", {})
        now = datetime.now()

        for timeframe, keywords in phrases.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    if timeframe == "immediate" or timeframe == "today":
                        return now.strftime("%Y-%m-%d")
                    elif timeframe == "tomorrow":
                        return (now + timedelta(days=1)).strftime("%Y-%m-%d")
                    elif timeframe == "this_week":
                        days_until_friday = (4 - now.weekday()) % 7
                        return (now + timedelta(days=days_until_friday)).strftime("%Y-%m-%d")
                    elif timeframe == "next_week":
                        days_until_next_monday = (7 - now.weekday()) % 7 + 7
                        return (now + timedelta(days=days_until_next_monday)).strftime("%Y-%m-%d")

        # Check for explicit dates (simplified pattern)
        date_patterns = [
            r"\b(\d{4}-\d{2}-\d{2})\b",  # YYYY-MM-DD
            r"\b(\d{1,2}/\d{1,2}/\d{4})\b",  # MM/DD/YYYY
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return None

    def get_project_association(self, subject: str, body: str, sender: str) -> Optional[str]:
        """Detect project association from email content."""
        combined_text = f"{subject} {body}".lower()

        for project, config in self.rules.get("project_associations", {}).items():
            # Check keywords
            keywords = config.get("keywords", [])
            for keyword in keywords:
                if keyword.lower() in combined_text:
                    return project

            # Check sender patterns
            senders = config.get("senders", [])
            for pattern in senders:
                if self._match_pattern(sender.lower(), pattern.lower()):
                    return project

        return None

    def get_delegation_candidate(self, subject: str, body: str, sender_priority: str) -> Optional[str]:
        """Determine if email should be delegated and to whom."""
        if not self.rules["delegation_rules"].get("enabled", False):
            return None

        # Don't delegate VIP emails
        if sender_priority == "VIP":
            return None

        combined_text = f"{subject} {body}"
        for rule in self.rules["delegation_rules"].get("content_rules", []):
            pattern = rule.get("pattern", "")
            if re.search(pattern, combined_text, re.IGNORECASE):
                return rule.get("delegate_name")

        return None


class UrgencyCalculator:
    """Calculates urgency scores for emails."""

    WEIGHTS = {"sender": 0.30, "deadline": 0.25, "keywords": 0.20, "thread": 0.15, "age": 0.10}

    SENDER_SCORES = {"VIP": 100, "HIGH": 75, "NORMAL": 50, "LOW": 25}

    def __init__(self, rules: BusinessRules):
        """Initialize with business rules."""
        self.rules = rules

    def calculate(self, email: EmailMessage, sender_priority: str, deadline: Optional[str]) -> tuple[int, str]:
        """Calculate urgency score and level."""
        scores = {
            "sender": self._sender_score(sender_priority),
            "deadline": self._deadline_score(deadline),
            "keywords": self._keyword_score(email.subject, email.body_text),
            "thread": self._thread_score(email),
            "age": self._age_score(email.received_at),
        }

        weighted_score = sum(scores[factor] * weight for factor, weight in self.WEIGHTS.items())

        urgency_score = int(min(100, max(0, weighted_score)))
        urgency_level = self._score_to_level(urgency_score)

        return urgency_score, urgency_level

    def _sender_score(self, priority: str) -> float:
        """Get sender priority score."""
        return self.SENDER_SCORES.get(priority, 50)

    def _deadline_score(self, deadline: Optional[str]) -> float:
        """Calculate deadline proximity score."""
        if not deadline:
            return 20

        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
            today = datetime.now().date()
            days_until = (deadline_date - today).days

            if days_until < 0:
                return 100  # Overdue
            elif days_until == 0:
                return 95  # Today
            elif days_until == 1:
                return 85  # Tomorrow
            elif days_until <= 7:
                return 70  # This week
            elif days_until <= 14:
                return 50  # Next week
            elif days_until <= 30:
                return 30  # This month
            else:
                return 20
        except ValueError:
            return 20

    def _keyword_score(self, subject: str, body: str) -> float:
        """Calculate keyword urgency score."""
        combined = f"{subject} {body}".lower()
        score = 50  # Base score

        keywords = self.rules.rules.get("urgency_keywords", {})

        for keyword in keywords.get("boost_high", []):
            if keyword.lower() in combined:
                score += 40
                break

        for keyword in keywords.get("boost_medium", []):
            if keyword.lower() in combined:
                score += 25
                break

        for keyword in keywords.get("boost_low", []):
            if keyword.lower() in combined:
                score += 15
                break

        for keyword in keywords.get("reduce_medium", []):
            if keyword.lower() in combined:
                score -= 20
                break

        for keyword in keywords.get("reduce_high", []):
            if keyword.lower() in combined:
                score -= 30
                break

        return max(0, min(100, score))

    def _thread_score(self, email: EmailMessage) -> float:
        """Calculate thread activity score."""
        # Simplified - in production would analyze thread history
        if len(email.recipients) == 1 and "?" in email.body_text:
            return 75  # Direct question
        elif len(email.cc) > 5:
            return 20  # Large CC, likely FYI
        return 50

    def _age_score(self, received_at: datetime) -> float:
        """Calculate age-based urgency score."""
        # Handle timezone-aware vs naive datetimes
        now = datetime.now()
        if received_at.tzinfo is not None:
            # Make received_at naive by removing timezone
            received_at = received_at.replace(tzinfo=None)
        age_days = (now - received_at).days

        if age_days > 7:
            return 100
        elif age_days >= 4:
            return 80
        elif age_days >= 2:
            return 60
        elif age_days >= 1:
            return 40
        else:
            return 20

    def _score_to_level(self, score: int) -> str:
        """Convert numeric score to urgency level."""
        if score >= 90:
            return "CRITICAL"
        elif score >= 75:
            return "HIGH"
        elif score >= 50:
            return "MEDIUM"
        elif score >= 25:
            return "LOW"
        else:
            return "MINIMAL"


class ActionClassifier:
    """Classifies emails into action types."""

    def classify(self, email: EmailMessage, sender_priority: str) -> tuple[str, str]:
        """
        Classify email action type and generate recommended action.

        Returns:
            tuple of (action_type, recommended_action)
        """
        subject_lower = email.subject.lower()
        body_lower = email.body_text.lower()
        combined = f"{subject_lower} {body_lower}"

        # Check for automated emails -> ARCHIVE
        if self._is_automated(email):
            return "ARCHIVE", "Auto-archive notification email"

        # Check if CC'd only -> FYI
        if not self._is_direct_recipient(email):
            return "FYI", "Review for awareness, no action required"

        # Check for meeting invitations -> SCHEDULE
        if self._is_meeting_invite(email):
            return "SCHEDULE", "Review and respond to meeting invitation"

        # Check for direct questions -> RESPOND
        if self._has_direct_question(combined):
            return "RESPOND", "Answer the question in email"

        # Check for review requests -> REVIEW
        if self._is_review_request(combined, email.attachments):
            return "REVIEW", "Review attached document and provide feedback"

        # Check for approval requests -> REVIEW
        if self._is_approval_request(combined):
            return "REVIEW", "Review and approve/reject request"

        # Default to TASK if actionable content detected
        if self._has_task_indicators(combined):
            return "TASK", "Create task from email content"

        # Default
        return "RESPOND", "Review and respond as appropriate"

    def _is_automated(self, email: EmailMessage) -> bool:
        """Check if email is automated."""
        sender_lower = email.sender.lower()
        automated_patterns = ["noreply", "no-reply", "notifications@", "alerts@", "mailer-daemon"]
        return any(p in sender_lower for p in automated_patterns)

    def _is_direct_recipient(self, email: EmailMessage) -> bool:
        """Check if user is in To: field (not just CC)."""
        # In production, would check against user's email
        return len(email.recipients) > 0

    def _is_meeting_invite(self, email: EmailMessage) -> bool:
        """Check if email is a meeting invitation."""
        for attachment in email.attachments:
            if attachment.lower().endswith(".ics"):
                return True
        meeting_keywords = ["meeting invitation", "calendar invite", "you have been invited"]
        return any(kw in email.subject.lower() for kw in meeting_keywords)

    def _has_direct_question(self, text: str) -> bool:
        """Check if email contains direct question."""
        question_patterns = [r"\?", r"can you", r"could you", r"would you", r"please let me know", r"what do you think"]
        return any(re.search(p, text, re.IGNORECASE) for p in question_patterns)

    def _is_review_request(self, text: str, attachments: list[str]) -> bool:
        """Check if email requests document review."""
        if not attachments:
            return False
        review_keywords = ["please review", "for your review", "feedback", "comments"]
        return any(kw in text for kw in review_keywords)

    def _is_approval_request(self, text: str) -> bool:
        """Check if email requests approval."""
        approval_keywords = ["please approve", "for approval", "need your approval", "sign off"]
        return any(kw in text for kw in approval_keywords)

    def _has_task_indicators(self, text: str) -> bool:
        """Check if email contains task indicators."""
        task_keywords = ["please prepare", "please update", "please create", "action item"]
        return any(kw in text for kw in task_keywords)


class EmailParser:
    """Parses emails from various sources."""

    def parse_mbox(self, mbox_path: str, max_emails: int = 100) -> list[EmailMessage]:
        """Parse emails from MBOX file."""
        emails = []
        mbox = mailbox.mbox(mbox_path)

        for i, message in enumerate(mbox):
            if i >= max_emails:
                break
            try:
                email = self._parse_message(message, f"mbox_{i}")
                if email:
                    emails.append(email)
            except Exception as e:
                print(f"Warning: Could not parse message {i}: {e}", file=sys.stderr)

        return emails

    def parse_eml_directory(self, dir_path: str, max_emails: int = 100) -> list[EmailMessage]:
        """Parse EML files from directory."""
        emails = []
        eml_files = list(Path(dir_path).glob("*.eml"))[:max_emails]

        for eml_path in eml_files:
            try:
                with open(eml_path, "rb") as f:
                    msg = BytesParser(policy=policy.default).parse(f)
                email = self._parse_message(msg, eml_path.stem)
                if email:
                    emails.append(email)
            except Exception as e:
                print(f"Warning: Could not parse {eml_path}: {e}", file=sys.stderr)

        return emails

    def _parse_message(self, msg, msg_id: str) -> Optional[EmailMessage]:
        """Parse a single email message."""
        try:
            # Extract sender
            sender_full = msg.get("From", "")
            sender_name, sender_email = self._parse_address(sender_full)

            # Extract recipients
            to_field = msg.get("To", "")
            recipients = self._parse_address_list(to_field)

            # Extract CC
            cc_field = msg.get("Cc", "")
            cc = self._parse_address_list(cc_field)

            # Extract date
            date_str = msg.get("Date", "")
            received_at = self._parse_date(date_str)

            # Extract body
            body_text, body_html = self._extract_body(msg)

            # Extract attachments
            attachments = self._extract_attachments(msg)

            return EmailMessage(
                id=msg_id,
                subject=msg.get("Subject", "(No Subject)"),
                sender=sender_email,
                sender_name=sender_name,
                recipients=recipients,
                cc=cc,
                received_at=received_at,
                body_text=body_text,
                body_html=body_html,
                attachments=attachments,
            )
        except Exception as e:
            print(f"Warning: Error parsing message: {e}", file=sys.stderr)
            return None

    def _parse_address(self, addr_str: str) -> tuple[str, str]:
        """Parse email address into name and email."""
        if not addr_str:
            return "", ""

        # Try format: "Name" <email@example.com> or Name <email@example.com>
        match = re.match(r'^"?([^"<]*?)"?\s*<([^>]+)>$', addr_str.strip())
        if match:
            name = match.group(1).strip()
            email = match.group(2).strip()
            return name, email

        # Try format: email@example.com (bare email)
        if "@" in addr_str and "<" not in addr_str:
            return "", addr_str.strip()

        return "", addr_str.strip()

    def _parse_address_list(self, addr_str: str) -> list[str]:
        """Parse comma-separated email addresses."""
        if not addr_str:
            return []
        addresses = []
        for addr in addr_str.split(","):
            _, email = self._parse_address(addr)
            if email:
                addresses.append(email)
        return addresses

    def _parse_date(self, date_str: str) -> datetime:
        """Parse email date string."""
        if not date_str:
            return datetime.now()

        # Try common date formats
        formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str[:31], fmt)
            except ValueError:
                continue

        return datetime.now()

    def _extract_body(self, msg) -> tuple[str, str]:
        """Extract text and HTML body from message."""
        body_text = ""
        body_html = ""

        def get_payload_text(part) -> str:
            """Get text content from a message part, handling both APIs."""
            # Try modern API first (email.message.EmailMessage)
            if hasattr(part, "get_content"):
                try:
                    return part.get_content()
                except Exception:
                    pass
            # Fall back to legacy API (mailbox.mboxMessage)
            payload = part.get_payload(decode=True)
            if payload:
                charset = part.get_content_charset() or "utf-8"
                try:
                    return payload.decode(charset)
                except (UnicodeDecodeError, LookupError):
                    return payload.decode("utf-8", errors="replace")
            return ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain" and not body_text:
                    body_text = get_payload_text(part)
                elif content_type == "text/html" and not body_html:
                    body_html = get_payload_text(part)
        else:
            content_type = msg.get_content_type()
            if content_type == "text/plain":
                body_text = get_payload_text(msg)
            elif content_type == "text/html":
                body_html = get_payload_text(msg)

        return body_text, body_html

    def _extract_attachments(self, msg) -> list[str]:
        """Extract attachment filenames."""
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                # Handle both modern and legacy API
                disposition = part.get_content_disposition()
                if disposition is None:
                    disposition = part.get("Content-Disposition", "")
                if "attachment" in str(disposition):
                    filename = part.get_filename()
                    if filename:
                        attachments.append(filename)
        return attachments


class EmailTriager:
    """Main email triage orchestrator."""

    def __init__(self, rules_path: Optional[str] = None):
        """Initialize triager with optional rules file."""
        self.rules = BusinessRules(rules_path)
        self.urgency_calc = UrgencyCalculator(self.rules)
        self.classifier = ActionClassifier()
        self.parser = EmailParser()

    def triage_emails(self, emails: list[EmailMessage]) -> list[ActionItem]:
        """Triage list of emails into action items."""
        action_items = []

        for email in emails:
            action_item = self._triage_single(email)
            action_items.append(action_item)

        # Sort by urgency score descending
        action_items.sort(key=lambda x: x.urgency_score, reverse=True)

        return action_items

    def _triage_single(self, email: EmailMessage) -> ActionItem:
        """Triage a single email."""
        # Get sender priority
        sender_priority = self.rules.get_sender_priority(email.sender)

        # Detect deadline
        deadline = self.rules.detect_deadline(f"{email.subject} {email.body_text}")

        # Calculate urgency
        urgency_score, urgency_level = self.urgency_calc.calculate(email, sender_priority, deadline)

        # Classify action type
        action_type, recommended_action = self.classifier.classify(email, sender_priority)

        # Get project association
        project = self.rules.get_project_association(email.subject, email.body_text, email.sender)

        # Check delegation
        delegation = self.rules.get_delegation_candidate(email.subject, email.body_text, sender_priority)

        # Generate context tags
        tags = self._generate_tags(email, action_type, deadline)

        # Generate suggested response
        suggested_response = self._generate_response(action_type, deadline, delegation)

        # Body preview
        body_preview = email.body_text[:200] if email.body_text else ""

        return ActionItem(
            id=email.id,
            subject=email.subject,
            sender=email.sender,
            sender_name=email.sender_name,
            sender_priority=sender_priority,
            received_at=email.received_at,
            urgency_score=urgency_score,
            urgency_level=urgency_level,
            action_type=action_type,
            deadline_detected=deadline,
            project_association=project,
            recommended_action=recommended_action,
            suggested_response=suggested_response,
            delegation_candidate=delegation,
            context_tags=tags,
            body_preview=body_preview,
        )

    def _generate_tags(self, email: EmailMessage, action_type: str, deadline: Optional[str]) -> list[str]:
        """Generate context tags for email."""
        tags = [action_type.lower()]

        if deadline:
            tags.append("deadline")

        if email.attachments:
            tags.append("has-attachment")

        # Add keyword-based tags
        combined = f"{email.subject} {email.body_text}".lower()
        tag_keywords = {
            "budget": ["budget", "cost", "expense"],
            "review": ["review", "feedback", "comments"],
            "meeting": ["meeting", "call", "sync"],
            "urgent": ["urgent", "asap", "critical"],
        }

        for tag, keywords in tag_keywords.items():
            if any(kw in combined for kw in keywords):
                tags.append(tag)

        return list(set(tags))

    def _generate_response(self, action_type: str, deadline: Optional[str], delegation: Optional[str]) -> Optional[str]:
        """Generate suggested response text."""
        if action_type == "ARCHIVE" or action_type == "FYI":
            return None

        if delegation:
            return f"I'm looping in {delegation} who can better assist with this."

        if deadline:
            return f"Thank you. I'll have this completed by {deadline}."

        responses = {
            "RESPOND": "Thank you for your email. I'll get back to you shortly.",
            "REVIEW": "I'll review this and provide feedback.",
            "SCHEDULE": "I'll check my calendar and confirm.",
            "TASK": "Noted. I'll add this to my task list.",
            "DELEGATE": "I'll forward this to the appropriate person.",
        }

        return responses.get(action_type)

    def generate_json_report(self, action_items: list[ActionItem]) -> dict:
        """Generate JSON report from action items."""
        summary = {
            "critical": sum(1 for a in action_items if a.urgency_level == "CRITICAL"),
            "high": sum(1 for a in action_items if a.urgency_level == "HIGH"),
            "medium": sum(1 for a in action_items if a.urgency_level == "MEDIUM"),
            "low": sum(1 for a in action_items if a.urgency_level == "LOW"),
            "delegatable": sum(1 for a in action_items if a.delegation_candidate),
            "fyi_only": sum(1 for a in action_items if a.action_type == "FYI"),
        }

        sender_stats = {
            "vip_senders": len(set(a.sender for a in action_items if a.sender_priority == "VIP")),
            "high_priority_senders": len(set(a.sender for a in action_items if a.sender_priority == "HIGH")),
            "unique_senders": len(set(a.sender for a in action_items)),
        }

        return {
            "schema_version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "total_emails_processed": len(action_items),
            "action_items": [a.to_dict() for a in action_items],
            "summary": summary,
            "sender_stats": sender_stats,
        }

    def generate_markdown_report(self, action_items: list[ActionItem]) -> str:
        """Generate Markdown daily action list."""
        lines = [
            "# Daily Email Action List",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}",
            "",
            "## Summary",
        ]

        # Summary counts
        critical = [a for a in action_items if a.urgency_level == "CRITICAL"]
        high = [a for a in action_items if a.urgency_level == "HIGH"]
        delegatable = [a for a in action_items if a.delegation_candidate]

        lines.extend(
            [
                f"- **Critical**: {len(critical)} items requiring immediate action",
                f"- **High Priority**: {len(high)} items for today",
                f"- **Delegatable**: {len(delegatable)} items to assign to team",
                "",
                "---",
                "",
            ]
        )

        # Critical section
        if critical:
            lines.append("## CRITICAL (Act Now)")
            lines.append("")
            for i, item in enumerate(critical, 1):
                lines.extend(self._format_action_item(i, item))

        # High priority section
        if high:
            lines.append("## HIGH PRIORITY (Today)")
            lines.append("")
            for i, item in enumerate(high, 1):
                lines.extend(self._format_action_item(i, item))

        # Delegation candidates
        if delegatable:
            lines.extend(
                [
                    "## DELEGATION CANDIDATES",
                    "",
                    "| Email | Suggested Assignee | Reason |",
                    "|-------|-------------------|--------|",
                ]
            )
            for item in delegatable:
                lines.append(f"| {item.subject[:40]}... | {item.delegation_candidate} | {item.recommended_action} |")
            lines.append("")

        # FYI section
        fyi_items = [a for a in action_items if a.action_type == "FYI"]
        if fyi_items:
            lines.extend(["## FYI ONLY (No Action Required)", ""])
            for item in fyi_items:
                lines.append(f"- {item.subject}")
            lines.append("")

        return "\n".join(lines)

    def _format_action_item(self, num: int, item: ActionItem) -> list[str]:
        """Format single action item for markdown."""
        lines = [
            f"### {num}. {item.subject}",
            f"- **From**: {item.sender_name or item.sender} ({item.sender_priority})",
        ]

        if item.deadline_detected:
            lines.append(f"- **Deadline**: {item.deadline_detected}")

        if item.project_association:
            lines.append(f"- **Project**: {item.project_association}")

        lines.append(f"- **Action**: {item.recommended_action}")

        if item.suggested_response:
            lines.append(f'- **Suggested Response**: "{item.suggested_response}"')

        if item.delegation_candidate:
            lines.append(f"- **Delegation**: Consider assigning to {item.delegation_candidate}")

        lines.extend(["", "---", ""])
        return lines


def generate_default_config() -> str:
    """Generate default configuration YAML."""
    # Read from assets if available, otherwise generate minimal config
    script_dir = Path(__file__).parent.parent
    default_rules_path = script_dir / "assets" / "default_rules.yaml"

    if default_rules_path.exists():
        return default_rules_path.read_text()

    return """# Email Action Triager - Default Configuration
schema_version: "1.0"

sender_priority:
  vip: []
  high: []
  low:
    - "noreply@*"
    - "no-reply@*"

urgency_keywords:
  boost_high: ["URGENT", "ASAP", "CRITICAL"]
  boost_medium: ["Important", "Priority"]
  reduce_high: ["Newsletter", "Digest"]

delegation_rules:
  enabled: false
  content_rules: []

project_associations: {}
"""


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Email Action Triager - Analyze inbox emails and generate action lists"
    )
    parser.add_argument(
        "--source", choices=["gmail", "file"], default="file", help="Email source (gmail API or local file)"
    )
    parser.add_argument("--input", help="Input file path (MBOX file or directory of EML files)")
    parser.add_argument("--max-emails", type=int, default=100, help="Maximum number of emails to process")
    parser.add_argument("--rules", help="Path to business rules YAML file")
    parser.add_argument("--output-format", choices=["json", "markdown"], default="json", help="Output format")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument("--generate-config", action="store_true", help="Generate default configuration file and exit")

    args = parser.parse_args()

    # Handle config generation
    if args.generate_config:
        print(generate_default_config())
        return 0

    # Validate input
    if args.source == "file" and not args.input:
        print("Error: --input required when source is 'file'", file=sys.stderr)
        return 1

    if args.source == "gmail":
        print("Error: Gmail API integration requires google-auth packages.", file=sys.stderr)
        print("Install with: pip install google-auth google-auth-oauthlib google-api-python-client", file=sys.stderr)
        print("For now, export emails to MBOX and use --source file", file=sys.stderr)
        return 1

    # Initialize triager
    triager = EmailTriager(args.rules)

    # Parse emails
    input_path = Path(args.input)
    if input_path.is_file() and input_path.suffix.lower() in [".mbox", ".mbox"]:
        emails = triager.parser.parse_mbox(str(input_path), args.max_emails)
    elif input_path.is_dir():
        emails = triager.parser.parse_eml_directory(str(input_path), args.max_emails)
    else:
        print(f"Error: Cannot process input: {args.input}", file=sys.stderr)
        return 1

    if not emails:
        print("Warning: No emails found to process", file=sys.stderr)
        return 0

    # Triage emails
    action_items = triager.triage_emails(emails)

    # Generate report
    if args.output_format == "json":
        report = triager.generate_json_report(action_items)
        output = json.dumps(report, indent=2)
    else:
        output = triager.generate_markdown_report(action_items)

    # Write output
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
