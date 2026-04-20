#!/usr/bin/env python3
"""
Email classifier for inbox triage.

Analyzes emails and classifies by urgency and action type using NLP-based heuristics.
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class EmailClassification:
    """Classification result for a single email."""

    id: str
    thread_id: str
    from_addr: str
    subject: str
    snippet: str
    date: str
    classification: str
    urgency_score: int
    signals: list = field(default_factory=list)
    suggested_action: str = ""
    estimated_minutes: int = 5
    delegate_to: Optional[str] = None


@dataclass
class TriageConfig:
    """Configuration for email triage."""

    vip_domains: list = field(default_factory=list)
    vip_senders: list = field(default_factory=list)


class EmailClassifier:
    """Classifies emails based on urgency and action type."""

    # Urgency signal patterns and weights
    DEADLINE_PATTERNS = [
        (r"\bEOD\b", 25),
        (r"\bASAP\b", 25),
        (r"\burgent\b", 25),
        (r"\bdeadline\b", 20),
        (r"\bby tomorrow\b", 20),
        (r"\bimmediately\b", 25),
        (r"\bcritical\b", 25),
        (r"\bemergency\b", 30),
        (r"\btime[- ]sensitive\b", 20),
    ]

    REPLY_EXPECTED_PATTERNS = [
        (r"please reply", 15),
        (r"let me know", 15),
        (r"your thoughts\??", 15),
        (r"awaiting your", 15),
        (r"get back to me", 15),
        (r"need your input", 20),
        (r"your feedback", 15),
    ]

    ESCALATION_PATTERNS = [
        (r"following up", 20),
        (r"second request", 25),
        (r"still waiting", 20),
        (r"reminder:", 15),
        (r"haven't heard", 20),
        (r"third time", 30),
    ]

    # FYI/Newsletter patterns (negative scoring)
    FYI_PATTERNS = [
        (r"unsubscribe", -25),
        (r"noreply@", -20),
        (r"notification", -15),
        (r"\bfyi\b", -20),
        (r"no action needed", -25),
        (r"automated message", -25),
        (r"do not reply", -20),
    ]

    # Delegation keywords by department
    DELEGATION_KEYWORDS = {
        "finance@": ["invoice", "payment", "billing", "expense", "receipt", "budget"],
        "hr@": ["leave", "vacation", "benefits", "onboarding", "pto", "payroll"],
        "it@": ["access", "password", "system", "software", "hardware", "login"],
        "legal@": ["contract", "agreement", "compliance", "nda", "terms"],
        "support@": ["ticket", "issue", "bug", "problem", "error"],
    }

    def __init__(self, config: TriageConfig):
        """Initialize classifier with configuration."""
        self.config = config

    def is_vip_sender(self, from_addr: str) -> bool:
        """Check if sender is a VIP."""
        from_lower = from_addr.lower()

        # Check explicit VIP senders
        for vip in self.config.vip_senders:
            if vip.lower() in from_lower:
                return True

        # Check VIP domains
        for domain in self.config.vip_domains:
            if f"@{domain.lower()}" in from_lower or f"<{domain.lower()}" in from_lower:
                return True

        return False

    def calculate_urgency_score(self, email: dict) -> tuple[int, list]:
        """Calculate urgency score and collect signals."""
        score = 0
        signals = []

        text = f"{email.get('subject', '')} {email.get('snippet', '')}".lower()
        from_addr = email.get("from", "").lower()

        # VIP sender check
        if self.is_vip_sender(from_addr):
            score += 30
            signals.append("vip_sender")

        # Deadline keywords
        for pattern, weight in self.DEADLINE_PATTERNS:
            if re.search(pattern, text, re.I):
                score += weight
                signals.append("deadline_keyword")
                break

        # Reply-expected signals
        for pattern, weight in self.REPLY_EXPECTED_PATTERNS:
            if re.search(pattern, text, re.I):
                score += weight
                signals.append("reply_expected")
                break

        # Direct question
        subject = email.get("subject", "")
        if "?" in subject or re.search(r"\byou\b.*\?", text, re.I):
            score += 10
            signals.append("direct_question")

        # Escalation signals
        for pattern, weight in self.ESCALATION_PATTERNS:
            if re.search(pattern, text, re.I):
                score += weight
                signals.append("escalation")
                break

        # Apply FYI/negative signals
        for pattern, weight in self.FYI_PATTERNS:
            if re.search(pattern, text, re.I):
                score += weight  # weight is negative
                signals.append("fyi_indicator")

        return max(0, min(score, 100)), signals

    def detect_delegation_target(self, email: dict) -> Optional[str]:
        """Detect if email can be delegated and to whom."""
        text = f"{email.get('subject', '')} {email.get('snippet', '')}".lower()

        for target, keywords in self.DELEGATION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return target

        return None

    def is_cc_recipient(self, email: dict, user_email: str = "") -> bool:
        """Check if user is CC'd rather than direct recipient."""
        cc_field = email.get("cc", "")
        to_field = email.get("to", "")

        # If user_email provided, check explicit CC
        if user_email:
            return user_email.lower() in cc_field.lower()

        # Heuristic: if 'to' field has many recipients, might be CC-like
        to_count = to_field.count("@") if to_field else 0
        return to_count > 3

    def estimate_response_time(self, classification: str, email: dict, signals: list) -> int:
        """Estimate minutes needed to handle email."""
        base_times = {
            "urgent-response": 10,
            "response-needed": 5,
            "fyi-read": 1,
            "delegatable": 2,
            "archive": 0,
        }

        minutes = base_times.get(classification, 5)

        # Adjustments
        if "attachment" in str(email.get("labels", [])).lower():
            minutes += 5

        text = f"{email.get('subject', '')} {email.get('snippet', '')}"
        question_count = text.count("?")
        if question_count > 2:
            minutes += 5

        return minutes

    def generate_suggested_action(self, classification: str, email: dict, delegate_to: Optional[str]) -> str:
        """Generate suggested action text."""
        subject = email.get("subject", "")[:50]

        actions = {
            "urgent-response": f"Reply immediately to '{subject}'",
            "response-needed": f"Draft response to '{subject}'",
            "fyi-read": f"Skim and archive '{subject}'",
            "delegatable": f"Forward to {delegate_to or 'appropriate team'}",
            "archive": f"Archive '{subject}'",
        }

        return actions.get(classification, "Review email")

    def classify_email(self, email: dict) -> EmailClassification:
        """Classify a single email."""
        urgency_score, signals = self.calculate_urgency_score(email)
        delegate_to = self.detect_delegation_target(email)
        is_cc = self.is_cc_recipient(email)

        # Determine classification based on score and signals
        if urgency_score >= 60:
            classification = "urgent-response"
        elif urgency_score >= 30:
            classification = "response-needed"
        elif delegate_to and urgency_score < 50:
            classification = "delegatable"
        elif is_cc or "fyi_indicator" in signals or urgency_score < 10:
            if urgency_score < 0:
                classification = "archive"
            else:
                classification = "fyi-read"
        else:
            classification = "response-needed"

        # VIP override: never archive VIP emails
        if "vip_sender" in signals and classification == "archive":
            classification = "fyi-read"

        estimated_minutes = self.estimate_response_time(classification, email, signals)
        suggested_action = self.generate_suggested_action(classification, email, delegate_to)

        return EmailClassification(
            id=email.get("id", ""),
            thread_id=email.get("threadId", email.get("thread_id", "")),
            from_addr=email.get("from", ""),
            subject=email.get("subject", ""),
            snippet=email.get("snippet", ""),
            date=email.get("date", ""),
            classification=classification,
            urgency_score=urgency_score,
            signals=signals,
            suggested_action=suggested_action,
            estimated_minutes=estimated_minutes,
            delegate_to=delegate_to,
        )

    def classify_emails(self, emails: list) -> dict:
        """Classify a list of emails and return triage report."""
        classifications = [self.classify_email(email) for email in emails]

        # Sort by urgency score descending
        classifications.sort(key=lambda x: x.urgency_score, reverse=True)

        # Build summary
        summary = {
            "urgent_response": 0,
            "response_needed": 0,
            "fyi_read": 0,
            "delegatable": 0,
            "archive": 0,
        }

        for c in classifications:
            key = c.classification.replace("-", "_")
            summary[key] = summary.get(key, 0) + 1

        return {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_emails": len(emails),
            "summary": summary,
            "emails": [asdict(c) for c in classifications],
        }


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Classify emails by urgency and action type for inbox triage.")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Input JSON file with email data",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output JSON file for classification results",
    )
    parser.add_argument(
        "--vip-domains",
        default="",
        help="Comma-separated list of VIP domains",
    )
    parser.add_argument(
        "--vip-senders",
        default="",
        help="Comma-separated list of VIP sender emails",
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Load input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            emails = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Handle both list and dict with 'messages' key
    if isinstance(emails, dict):
        emails = emails.get("messages", [])

    if not isinstance(emails, list):
        print("Error: Expected list of emails or dict with 'messages' key", file=sys.stderr)
        sys.exit(1)

    # Build config
    config = TriageConfig(
        vip_domains=[d.strip() for d in args.vip_domains.split(",") if d.strip()],
        vip_senders=[s.strip() for s in args.vip_senders.split(",") if s.strip()],
    )

    # Classify
    classifier = EmailClassifier(config)
    report = classifier.classify_emails(emails)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Print summary
    summary = report["summary"]
    print(f"Email Triage Complete: {report['total_emails']} emails classified")
    print(f"  Urgent Response: {summary['urgent_response']}")
    print(f"  Response Needed: {summary['response_needed']}")
    print(f"  FYI/Read: {summary['fyi_read']}")
    print(f"  Delegatable: {summary['delegatable']}")
    print(f"  Archive: {summary['archive']}")
    print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()
