#!/usr/bin/env python3
"""
Inbox Triage Summarizer

Categorizes emails by project/client, identifies action-required items,
and generates prioritized summary reports.

Usage:
    python triage_inbox.py --input emails.json --output summary.json
    python triage_inbox.py --input emails.json --output report.md --format markdown
    python triage_inbox.py --input emails.json --export-action-items --output actions.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class Classification(Enum):
    """Email action classification."""

    FYI = "fyi"
    REQUIRES_RESPONSE = "requires_response"
    REQUIRES_ACTION = "requires_action"
    BLOCKED_WAITING = "blocked_waiting"
    UNKNOWN = "unknown"


@dataclass
class Email:
    """Parsed email data."""

    id: str
    thread_id: str
    from_address: str
    to_addresses: list[str]
    cc_addresses: list[str]
    subject: str
    body: str
    received_at: datetime
    labels: list[str] = field(default_factory=list)
    is_from_me: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Email":
        """Create Email from dictionary."""
        received_at = data.get("received_at") or data.get("date", "")
        if isinstance(received_at, str):
            try:
                received_at = datetime.fromisoformat(received_at.replace("Z", "+00:00"))
            except ValueError:
                received_at = datetime.now(timezone.utc)

        return cls(
            id=data.get("id", ""),
            thread_id=data.get("thread_id", data.get("threadId", "")),
            from_address=data.get("from", data.get("from_address", "")),
            to_addresses=data.get("to", data.get("to_addresses", [])),
            cc_addresses=data.get("cc", data.get("cc_addresses", [])),
            subject=data.get("subject", ""),
            body=data.get("body", data.get("snippet", "")),
            received_at=received_at,
            labels=data.get("labels", data.get("labelIds", [])),
            is_from_me=data.get("is_from_me", False),
        )


@dataclass
class TriageResult:
    """Result of email triage analysis."""

    email: Email
    classification: Classification
    project_id: str
    urgency_score: int
    urgency_indicators: list[str]
    detected_deadline: str | None
    recommended_action: str
    thread_state: str
    staleness_days: int


@dataclass
class ProjectConfig:
    """Project matching configuration."""

    id: str
    display_name: str
    priority: str
    match_rules: list[dict[str, Any]]


class InboxTriager:
    """Inbox triage and summarization engine."""

    # Classification patterns
    FYI_PATTERNS = [
        r"\bFYI\b",
        r"\bfor your information\b",
        r"\bno action needed\b",
        r"\bno action required\b",
        r"\bjust wanted to let you know\b",
    ]

    ACTION_PATTERNS = [
        r"\bplease prepare\b",
        r"\bcan you create\b",
        r"\bneed you to\b",
        r"\bplease send\b",
        r"\bplease review\b",
        r"\baction required\b",
        r"\baction needed\b",
        r"\bplease complete\b",
        r"\bplease submit\b",
        r"\bdeliverable\b",
        r"\bdue by\b",
    ]

    RESPONSE_PATTERNS = [
        r"\bcan you confirm\b",
        r"\bplease confirm\b",
        r"\bwhat do you think\b",
        r"\byour thoughts\b",
        r"\bplease approve\b",
        r"\blet me know\b",
        r"\bwhen are you available\b",
        r"\bcan we schedule\b",
        r"\?$",  # Ends with question mark
    ]

    URGENCY_PATTERNS = [
        (r"\bURGENT\b", 20),
        (r"\bASAP\b", 15),
        (r"\btime[- ]sensitive\b", 15),
        (r"\bby EOD\b", 20),
        (r"\bby end of day\b", 20),
        (r"\bwithin 24 hours\b", 25),
        (r"\bbefore Friday\b", 10),
        (r"\bfollowing up\b", 10),
        (r"\bsecond request\b", 15),
        (r"\breminder\b", 10),
    ]

    def __init__(
        self,
        project_rules: list[ProjectConfig] | None = None,
        my_email: str | None = None,
    ):
        self.project_rules = project_rules or []
        self.my_email = my_email or ""

    def classify_email(self, email: Email) -> Classification:
        """Determine the action classification for an email."""
        subject_body = f"{email.subject} {email.body}".lower()

        # Check if I sent the last message (blocked waiting)
        if email.is_from_me:
            return Classification.BLOCKED_WAITING

        # Check if I'm only CC'd (FYI)
        if email.cc_addresses and self.my_email:
            if self.my_email.lower() in [cc.lower() for cc in email.cc_addresses]:
                if self.my_email.lower() not in [to.lower() for to in email.to_addresses]:
                    return Classification.FYI

        # Check for FYI patterns
        for pattern in self.FYI_PATTERNS:
            if re.search(pattern, subject_body, re.IGNORECASE):
                return Classification.FYI

        # Check for action patterns (stronger than response)
        for pattern in self.ACTION_PATTERNS:
            if re.search(pattern, subject_body, re.IGNORECASE):
                return Classification.REQUIRES_ACTION

        # Check for response patterns
        for pattern in self.RESPONSE_PATTERNS:
            if re.search(pattern, subject_body, re.IGNORECASE):
                return Classification.REQUIRES_RESPONSE

        # Default to requires_response (conservative)
        return Classification.REQUIRES_RESPONSE

    def calculate_urgency_score(self, email: Email) -> tuple[int, list[str]]:
        """Calculate urgency score (0-100) and list indicators found."""
        subject_body = f"{email.subject} {email.body}"
        score = 0
        indicators: list[str] = []

        # Check urgency patterns
        for pattern, points in self.URGENCY_PATTERNS:
            if re.search(pattern, subject_body, re.IGNORECASE):
                score += points
                match = re.search(pattern, subject_body, re.IGNORECASE)
                if match:
                    indicators.append(match.group(0))

        # Staleness factor
        now = datetime.now(timezone.utc)
        if email.received_at.tzinfo is None:
            email_time = email.received_at.replace(tzinfo=timezone.utc)
        else:
            email_time = email.received_at
        age_days = (now - email_time).days

        if age_days >= 5:
            score += 15
            indicators.append(f"stale ({age_days} days)")
        elif age_days >= 3:
            score += 10
            indicators.append(f"aging ({age_days} days)")
        elif age_days >= 1:
            score += 5

        return min(score, 100), indicators

    def detect_deadline(self, email: Email) -> str | None:
        """Extract deadline from email text."""
        subject_body = f"{email.subject} {email.body}"

        # Common deadline patterns
        patterns = [
            r"by (\d{1,2}/\d{1,2}(?:/\d{2,4})?)",
            r"due (?:by |on )?(\d{1,2}/\d{1,2}(?:/\d{2,4})?)",
            r"before (\w+ \d{1,2})",
            r"by (EOD|end of day|COB|close of business)",
            r"within (\d+ (?:hour|day|week)s?)",
        ]

        for pattern in patterns:
            match = re.search(pattern, subject_body, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def match_project(self, email: Email) -> str:
        """Match email to a project based on rules."""
        for project in self.project_rules:
            for rule in project.match_rules:
                rule_type = rule.get("type", "")
                pattern = rule.get("pattern", "")
                case_insensitive = rule.get("case_insensitive", False)
                flags = re.IGNORECASE if case_insensitive else 0

                if rule_type == "sender_domain":
                    if re.search(pattern, email.from_address, flags):
                        return project.id

                elif rule_type == "subject_contains":
                    if re.search(pattern, email.subject, flags):
                        return project.id

                elif rule_type == "thread_label":
                    for label in email.labels:
                        if re.search(pattern, label, flags):
                            return project.id

        return "unassigned"

    def calculate_staleness(self, email: Email) -> int:
        """Calculate days since email was received."""
        now = datetime.now(timezone.utc)
        if email.received_at.tzinfo is None:
            email_time = email.received_at.replace(tzinfo=timezone.utc)
        else:
            email_time = email.received_at
        return (now - email_time).days

    def recommend_action(self, classification: Classification, urgency_score: int) -> str:
        """Generate recommended action based on classification and urgency."""
        if classification == Classification.FYI:
            return "Read and archive"
        elif classification == Classification.BLOCKED_WAITING:
            if urgency_score >= 60:
                return "Send follow-up reminder"
            else:
                return "Monitor for response"
        elif classification == Classification.REQUIRES_ACTION:
            if urgency_score >= 80:
                return "Complete task immediately"
            elif urgency_score >= 60:
                return "Complete task within 24 hours"
            else:
                return "Schedule time to complete"
        else:  # REQUIRES_RESPONSE
            if urgency_score >= 80:
                return "Respond immediately"
            elif urgency_score >= 60:
                return "Respond within 24 hours"
            else:
                return "Respond within 3 days"

    def triage_email(self, email: Email) -> TriageResult:
        """Perform full triage analysis on an email."""
        classification = self.classify_email(email)
        urgency_score, urgency_indicators = self.calculate_urgency_score(email)
        project_id = self.match_project(email)
        deadline = self.detect_deadline(email)
        staleness = self.calculate_staleness(email)
        recommended_action = self.recommend_action(classification, urgency_score)

        # Determine thread state
        if staleness >= 7:
            thread_state = "dormant"
        elif staleness >= 3:
            thread_state = "stale"
        else:
            thread_state = "active"

        return TriageResult(
            email=email,
            classification=classification,
            project_id=project_id,
            urgency_score=urgency_score,
            urgency_indicators=urgency_indicators,
            detected_deadline=deadline,
            recommended_action=recommended_action,
            thread_state=thread_state,
            staleness_days=staleness,
        )

    def triage_emails(self, emails: list[Email]) -> list[TriageResult]:
        """Triage multiple emails."""
        return [self.triage_email(email) for email in emails]


def generate_json_report(results: list[TriageResult], scan_start: datetime | None = None) -> dict[str, Any]:
    """Generate JSON summary report."""
    now = datetime.now(timezone.utc)

    # Count by classification
    by_classification: dict[str, int] = {c.value: 0 for c in Classification}
    for r in results:
        by_classification[r.classification.value] += 1

    # Count by project
    by_project: dict[str, int] = {}
    for r in results:
        by_project[r.project_id] = by_project.get(r.project_id, 0) + 1

    # Group results by project
    projects_data: dict[str, dict[str, Any]] = {}
    for r in results:
        if r.project_id not in projects_data:
            projects_data[r.project_id] = {
                "project_id": r.project_id,
                "display_name": r.project_id.replace("-", " ").title(),
                "email_count": 0,
                "action_required_count": 0,
                "blocked_count": 0,
                "oldest_unanswered": None,
                "threads": [],
            }

        pd = projects_data[r.project_id]
        pd["email_count"] += 1

        if r.classification in [
            Classification.REQUIRES_ACTION,
            Classification.REQUIRES_RESPONSE,
        ]:
            pd["action_required_count"] += 1
        if r.classification == Classification.BLOCKED_WAITING:
            pd["blocked_count"] += 1

        # Track oldest unanswered
        if r.classification != Classification.FYI:
            received_str = r.email.received_at.isoformat()
            if pd["oldest_unanswered"] is None or received_str < pd["oldest_unanswered"]:
                pd["oldest_unanswered"] = received_str

    # Extract action items
    action_items = []
    for r in results:
        if r.classification in [
            Classification.REQUIRES_ACTION,
            Classification.REQUIRES_RESPONSE,
        ]:
            action_items.append(
                {
                    "email_id": r.email.id,
                    "thread_id": r.email.thread_id,
                    "project_id": r.project_id,
                    "from": r.email.from_address,
                    "subject": r.email.subject,
                    "classification": r.classification.value,
                    "urgency_score": r.urgency_score,
                    "detected_deadline": r.detected_deadline,
                    "urgency_indicators": r.urgency_indicators,
                    "recommended_action": r.recommended_action,
                }
            )

    # Extract blocked items
    blocked_items = []
    for r in results:
        if r.classification == Classification.BLOCKED_WAITING:
            blocked_items.append(
                {
                    "email_id": r.email.id,
                    "thread_id": r.email.thread_id,
                    "project_id": r.project_id,
                    "waiting_on": r.email.to_addresses[0] if r.email.to_addresses else "",
                    "last_sent": r.email.received_at.isoformat(),
                    "days_waiting": r.staleness_days,
                    "subject": r.email.subject,
                    "recommended_action": r.recommended_action,
                }
            )

    return {
        "schema_version": "1.0",
        "scan_timestamp": now.isoformat(),
        "scan_period": {
            "start": scan_start.isoformat() if scan_start else None,
            "end": now.isoformat(),
        },
        "summary": {
            "total_emails": len(results),
            "by_classification": by_classification,
            "by_project": by_project,
        },
        "projects": list(projects_data.values()),
        "action_items": sorted(action_items, key=lambda x: x["urgency_score"], reverse=True),
        "blocked_items": sorted(blocked_items, key=lambda x: x["days_waiting"], reverse=True),
    }


def generate_markdown_report(results: list[TriageResult], scan_start: datetime | None = None) -> str:
    """Generate markdown summary report."""
    now = datetime.now(timezone.utc)
    lines: list[str] = []

    # Header
    lines.append("# Inbox Triage Summary\n")
    if scan_start:
        lines.append(f"**Scan Period**: {scan_start.strftime('%b %d')} - {now.strftime('%b %d, %Y')}")
    lines.append(f"**Total Emails**: {len(results)}\n")

    # Classification summary
    by_classification: dict[str, int] = {c.value: 0 for c in Classification}
    for r in results:
        by_classification[r.classification.value] += 1

    lines.append("## Action Summary\n")
    lines.append("| Classification | Count | % |")
    lines.append("|----------------|-------|---|")
    for cls, count in by_classification.items():
        pct = round(count / len(results) * 100) if results else 0
        label = cls.replace("_", " ").title()
        lines.append(f"| {label} | {count} | {pct}% |")
    lines.append("")

    # Group by project
    by_project: dict[str, list[TriageResult]] = {}
    for r in results:
        if r.project_id not in by_project:
            by_project[r.project_id] = []
        by_project[r.project_id].append(r)

    lines.append("## By Project\n")
    for project_id, project_results in sorted(by_project.items()):
        action_count = sum(
            1
            for r in project_results
            if r.classification in [Classification.REQUIRES_ACTION, Classification.REQUIRES_RESPONSE]
        )
        blocked_count = sum(1 for r in project_results if r.classification == Classification.BLOCKED_WAITING)

        project_name = project_id.replace("-", " ").title()
        lines.append(f"### {project_name} ({len(project_results)} emails, {action_count} action required)\n")

        if blocked_count > 0:
            lines.append(f"**Blocked**: {blocked_count} threads waiting on response\n")

        # Table of action items
        action_results = [
            r for r in project_results if r.classification not in [Classification.FYI, Classification.BLOCKED_WAITING]
        ]
        if action_results:
            lines.append("| Subject | From | Classification | Staleness |")
            lines.append("|---------|------|----------------|-----------|")
            for r in sorted(action_results, key=lambda x: x.urgency_score, reverse=True)[:5]:
                cls_label = r.classification.value.replace("_", " ").title()
                staleness = f"{r.staleness_days} days" if r.staleness_days > 0 else "Today"
                subject = r.email.subject[:40] + "..." if len(r.email.subject) > 40 else r.email.subject
                lines.append(f"| {subject} | {r.email.from_address} | {cls_label} | {staleness} |")
            lines.append("")

    # Recommended actions
    lines.append("## Recommended Actions\n")
    action_items = [
        r for r in results if r.classification in [Classification.REQUIRES_ACTION, Classification.REQUIRES_RESPONSE]
    ]
    action_items.sort(key=lambda x: x.urgency_score, reverse=True)

    if action_items:
        high_urgency = [r for r in action_items if r.urgency_score >= 60]
        if high_urgency:
            lines.append(f"1. **Respond immediately** to {len(high_urgency)} high-urgency emails")

        by_project_action: dict[str, int] = {}
        for r in action_items:
            by_project_action[r.project_id] = by_project_action.get(r.project_id, 0) + 1

        for project_id, count in sorted(by_project_action.items(), key=lambda x: x[1], reverse=True)[:3]:
            project_name = project_id.replace("-", " ").title()
            lines.append(f"2. **Process {count} emails** from {project_name}")

    blocked = [r for r in results if r.classification == Classification.BLOCKED_WAITING]
    if blocked:
        stale_blocked = [r for r in blocked if r.staleness_days >= 3]
        if stale_blocked:
            lines.append(f"3. **Follow up** on {len(stale_blocked)} blocked threads (waiting 3+ days)")

    return "\n".join(lines)


def load_project_rules(rules_path: Path) -> list[ProjectConfig]:
    """Load project matching rules from YAML file."""
    if not YAML_AVAILABLE:
        print("Warning: PyYAML not installed, skipping project rules", file=sys.stderr)
        return []

    if not rules_path.exists():
        return []

    with rules_path.open() as f:
        data = yaml.safe_load(f)

    projects = []
    for p in data.get("projects", []):
        projects.append(
            ProjectConfig(
                id=p.get("id", ""),
                display_name=p.get("display_name", p.get("id", "")),
                priority=p.get("priority", "medium"),
                match_rules=p.get("match_rules", []),
            )
        )
    return projects


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Inbox triage and summarization tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=Path,
        help="Input JSON file with emails",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        type=Path,
        help="Output file path",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "markdown"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--project-rules",
        "-p",
        type=Path,
        help="Path to project mapping YAML file",
    )
    parser.add_argument(
        "--export-action-items",
        action="store_true",
        help="Export only action-required items",
    )
    parser.add_argument(
        "--classifications",
        type=str,
        help="Comma-separated list of classifications to include in export",
    )
    parser.add_argument(
        "--my-email",
        type=str,
        help="Your email address for CC detection",
    )
    parser.add_argument(
        "--group-by",
        choices=["project", "action", "sender", "date"],
        default="project",
        help="Grouping for output (default: project)",
    )

    args = parser.parse_args()

    # Load input
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1

    with args.input.open() as f:
        raw_data = json.load(f)

    # Handle both list and dict with 'emails' key
    if isinstance(raw_data, list):
        emails_data = raw_data
    elif isinstance(raw_data, dict) and "emails" in raw_data:
        emails_data = raw_data["emails"]
    else:
        print("Error: Invalid input format. Expected list or dict with 'emails' key.", file=sys.stderr)
        return 1

    emails = [Email.from_dict(e) for e in emails_data]

    # Load project rules
    project_rules: list[ProjectConfig] = []
    if args.project_rules:
        project_rules = load_project_rules(args.project_rules)

    # Run triage
    triager = InboxTriager(project_rules=project_rules, my_email=args.my_email)
    results = triager.triage_emails(emails)

    # Filter if exporting action items
    if args.export_action_items:
        allowed: set[str] = {"requires_response", "requires_action"}
        if args.classifications:
            allowed = set(args.classifications.split(","))
        results = [r for r in results if r.classification.value in allowed]

    # Generate output
    if args.format == "json":
        report = generate_json_report(results)
        with args.output.open("w") as f:
            json.dump(report, f, indent=2)
    else:
        report = generate_markdown_report(results)
        args.output.write_text(report)

    print(f"Triage complete. {len(results)} emails processed.", file=sys.stderr)
    print(f"Output written to: {args.output}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
