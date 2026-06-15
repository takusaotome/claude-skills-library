#!/usr/bin/env python3
"""
Email Thread Analyzer

Parse email threads from various formats (Gmail JSON, Outlook, EML, MBOX)
and extract structured information including participants, timeline,
action items, decisions, and status classification.
"""

import argparse
import email
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path
from typing import Optional


@dataclass
class Participant:
    """Email thread participant."""

    name: str
    email: str
    role: str  # initiator, responder, cc


@dataclass
class TimelineEvent:
    """A significant event in the thread timeline."""

    date: str  # ISO8601
    actor: str
    event_type: str  # request, response, decision, escalation, resolution
    summary: str


@dataclass
class ActionItem:
    """An action item extracted from the thread."""

    id: str
    description: str
    owner: str
    status: str  # pending, completed, cancelled
    due_date: Optional[str]
    source_message_date: str


@dataclass
class KeyDecision:
    """A decision made in the thread."""

    date: str
    decision: str
    made_by: str


@dataclass
class OutdatedInfo:
    """Information that has been superseded."""

    original_statement: str
    stated_date: str
    superseded_by: str
    superseded_date: str


@dataclass
class ThreadStatus:
    """Thread status classification."""

    classification: str  # active, resolved, stale, escalated, awaiting_response
    confidence: float
    last_action_date: str
    days_since_last_action: int


@dataclass
class DateRange:
    """Date range for the thread."""

    first_message: str
    last_message: str
    duration_days: int


@dataclass
class ThreadAnalysis:
    """Complete thread analysis result."""

    schema_version: str = "1.0"
    thread_id: str = ""
    subject: str = ""
    participants: list = field(default_factory=list)
    message_count: int = 0
    date_range: Optional[DateRange] = None
    status: Optional[ThreadStatus] = None
    timeline: list = field(default_factory=list)
    action_items: list = field(default_factory=list)
    key_decisions: list = field(default_factory=list)
    outdated_info: list = field(default_factory=list)
    analysis_timestamp: str = ""


# Action item detection patterns
COMMITMENT_PATTERNS = [
    (r"\bI will\s+(\w+.*?)(?:\.|$)", "high"),
    (r"\bI'll\s+(\w+.*?)(?:\.|$)", "high"),
    (r"\bI'm going to\s+(\w+.*?)(?:\.|$)", "high"),
    (r"\bLet me\s+(\w+.*?)(?:\.|$)", "medium"),
    (r"\bI can\s+(\w+.*?)(?:\.|$)", "medium"),
    (r"\bI'll take care of\s+(\w+.*?)(?:\.|$)", "high"),
]

REQUEST_PATTERNS = [
    (r"\bCan you\s+(\w+.*?)\??", "high"),
    (r"\bCould you\s+(\w+.*?)\??", "high"),
    (r"\bPlease\s+(\w+.*?)(?:\.|$)", "high"),
    (r"\bWould you\s+(\w+.*?)\??", "medium"),
    (r"\bAction required:\s*(.+?)(?:\.|$)", "high"),
    (r"\bTODO:\s*(.+?)(?:\.|$)", "high"),
]

DEADLINE_PATTERNS = [
    (
        r"\bby\s+((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|tomorrow|EOD|COB|end of day|end of week|EOM|EOW|\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:,?\s+\d{4})?))",
        re.IGNORECASE,
    ),
    (r"\bbefore\s+(.+?)(?:\.|,|$)", re.IGNORECASE),
    (r"\bwithin\s+(\d+\s+(?:days?|hours?|weeks?))", re.IGNORECASE),
    (r"\bdue\s+(.+?)(?:\.|,|$)", re.IGNORECASE),
    (r"\bASAP\b", re.IGNORECASE),
]

RESOLUTION_PATTERNS = [
    r"\bthis is resolved\b",
    r"\bissue (?:has been|is) fixed\b",
    r"\bproblem solved\b",
    r"\bclosing this thread\b",
    r"\bthanks? for resolving\b",
    r"\bthank you for your help\b",
    r"\bthat worked\b",
    r"\ball set now\b",
    r"\bwe'?re good\b",
    r"\bdone\b",
    r"\bcompleted\b",
]

ESCALATION_PATTERNS = [
    r"\bescalating\s+(?:this\s+)?to\b",
    r"\blooping in\b",
    r"\badding\s+\w+\s+(?:who can|for)\b",
    r"\bURGENT\b",
    r"\bESCALATION\b",
    r"\bACTION REQUIRED\b",
    r"\bneeds? immediate attention\b",
    r"\bneed to escalate\b",
]

DECISION_PATTERNS = [
    (r"\bwe decided to\s+(.+?)(?:\.|$)", "high"),
    (r"\bthe decision is\s+(.+?)(?:\.|$)", "high"),
    (r"\bwe'?ve? agreed to\s+(.+?)(?:\.|$)", "high"),
    (r"\bfinal decision:\s*(.+?)(?:\.|$)", "high"),
    (r"\bgoing with\s+(.+?)(?:\.|$)", "medium"),
    (r"\bapproved\b", "high"),
    (r"\bconfirmed\b", "medium"),
]

SUPERSESSION_PATTERNS = [
    r"\bactually,?\s+",
    r"\bcorrection:\s*",
    r"\bupdate:\s*",
    r"\bdisregard\b",
    r"\binstead,?\s+",
    r"\bchanged to\b",
    r"\bno longer\b",
    r"\bnever mind\b",
]


def parse_gmail_json(data: dict) -> list[dict]:
    """Parse Gmail JSON export format."""
    messages = []

    # Handle single message or list
    if isinstance(data, list):
        raw_messages = data
    elif "messages" in data:
        raw_messages = data["messages"]
    else:
        raw_messages = [data]

    for msg in raw_messages:
        parsed = {
            "id": msg.get("id", ""),
            "thread_id": msg.get("threadId", ""),
            "date": "",
            "from_name": "",
            "from_email": "",
            "to": [],
            "cc": [],
            "subject": "",
            "body": "",
        }

        # Extract headers
        headers = {}
        if "payload" in msg and "headers" in msg["payload"]:
            for header in msg["payload"]["headers"]:
                headers[header["name"].lower()] = header["value"]

        parsed["subject"] = headers.get("subject", "")
        parsed["date"] = headers.get("date", "")

        # Parse From
        if "from" in headers:
            name, email_addr = parseaddr(headers["from"])
            parsed["from_name"] = name or email_addr.split("@")[0]
            parsed["from_email"] = email_addr

        # Parse To
        if "to" in headers:
            for addr in headers["to"].split(","):
                name, email_addr = parseaddr(addr.strip())
                if email_addr:
                    parsed["to"].append({"name": name, "email": email_addr})

        # Parse CC
        if "cc" in headers:
            for addr in headers["cc"].split(","):
                name, email_addr = parseaddr(addr.strip())
                if email_addr:
                    parsed["cc"].append({"name": name, "email": email_addr})

        # Extract body
        if "payload" in msg:
            parsed["body"] = extract_gmail_body(msg["payload"])

        messages.append(parsed)

    return messages


def extract_gmail_body(payload: dict) -> str:
    """Extract body text from Gmail payload."""
    import base64

    body = ""

    if "body" in payload and "data" in payload["body"]:
        try:
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
        except Exception:
            pass

    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            if mime_type == "text/plain":
                if "body" in part and "data" in part["body"]:
                    try:
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break
                    except Exception:
                        pass
            elif mime_type.startswith("multipart/"):
                body = extract_gmail_body(part)
                if body:
                    break

    return body


def parse_eml_file(file_path: Path) -> list[dict]:
    """Parse a single .eml file."""
    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f)

    return [parse_email_message(msg)]


def parse_mbox_file(file_path: Path) -> list[dict]:
    """Parse an mbox file containing multiple messages."""
    import mailbox

    messages = []
    mbox = mailbox.mbox(str(file_path))

    for msg in mbox:
        messages.append(parse_email_message(msg))

    return messages


def parse_email_message(msg: email.message.Message) -> dict:
    """Parse a single email.message.Message object."""
    parsed = {
        "id": msg.get("Message-ID", ""),
        "thread_id": msg.get("References", "").split()[0] if msg.get("References") else "",
        "date": msg.get("Date", ""),
        "from_name": "",
        "from_email": "",
        "to": [],
        "cc": [],
        "subject": msg.get("Subject", ""),
        "body": "",
    }

    # Parse From
    from_header = msg.get("From", "")
    name, email_addr = parseaddr(from_header)
    parsed["from_name"] = name or (email_addr.split("@")[0] if email_addr else "")
    parsed["from_email"] = email_addr

    # Parse To
    to_header = msg.get("To", "")
    for addr in to_header.split(","):
        name, email_addr = parseaddr(addr.strip())
        if email_addr:
            parsed["to"].append({"name": name, "email": email_addr})

    # Parse CC
    cc_header = msg.get("Cc", "")
    if cc_header:
        for addr in cc_header.split(","):
            name, email_addr = parseaddr(addr.strip())
            if email_addr:
                parsed["cc"].append({"name": name, "email": email_addr})

    # Extract body
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    parsed["body"] = payload.decode("utf-8", errors="replace")
                    break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            parsed["body"] = payload.decode("utf-8", errors="replace")

    return parsed


def parse_outlook_json(data: dict) -> list[dict]:
    """Parse Outlook/Microsoft Graph API JSON format."""
    messages = []

    # Handle single message or list
    if isinstance(data, list):
        raw_messages = data
    elif "value" in data:
        raw_messages = data["value"]
    else:
        raw_messages = [data]

    for msg in raw_messages:
        parsed = {
            "id": msg.get("id", ""),
            "thread_id": msg.get("conversationId", ""),
            "date": msg.get("receivedDateTime", msg.get("sentDateTime", "")),
            "from_name": "",
            "from_email": "",
            "to": [],
            "cc": [],
            "subject": msg.get("subject", ""),
            "body": "",
        }

        # Parse From
        if "from" in msg and "emailAddress" in msg["from"]:
            parsed["from_name"] = msg["from"]["emailAddress"].get("name", "")
            parsed["from_email"] = msg["from"]["emailAddress"].get("address", "")

        # Parse To
        for recipient in msg.get("toRecipients", []):
            if "emailAddress" in recipient:
                parsed["to"].append(
                    {
                        "name": recipient["emailAddress"].get("name", ""),
                        "email": recipient["emailAddress"].get("address", ""),
                    }
                )

        # Parse CC
        for recipient in msg.get("ccRecipients", []):
            if "emailAddress" in recipient:
                parsed["cc"].append(
                    {
                        "name": recipient["emailAddress"].get("name", ""),
                        "email": recipient["emailAddress"].get("address", ""),
                    }
                )

        # Extract body
        if "body" in msg:
            body_content = msg["body"].get("content", "")
            # Strip HTML if present
            if msg["body"].get("contentType") == "html":
                body_content = re.sub(r"<[^>]+>", "", body_content)
            parsed["body"] = body_content

        messages.append(parsed)

    return messages


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse various date formats to datetime."""
    if not date_str:
        return None

    # Try ISO8601 format first
    try:
        if date_str.endswith("Z"):
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return datetime.fromisoformat(date_str)
    except ValueError:
        pass

    # Try email date format
    try:
        return parsedate_to_datetime(date_str)
    except (TypeError, ValueError):
        pass

    # Try dateutil as fallback
    try:
        from dateutil.parser import parse as dateutil_parse

        return dateutil_parse(date_str)
    except Exception:
        pass

    return None


def extract_participants(messages: list[dict]) -> list[Participant]:
    """Extract unique participants with roles."""
    participants_map = {}
    initiator_email = None

    # Sort by date to find initiator
    sorted_messages = sorted(messages, key=lambda m: parse_date(m["date"]) or datetime.min.replace(tzinfo=timezone.utc))

    if sorted_messages:
        initiator_email = sorted_messages[0]["from_email"].lower()

    for i, msg in enumerate(sorted_messages):
        # Add sender
        sender_email = msg["from_email"].lower()
        if sender_email and sender_email not in participants_map:
            role = "initiator" if sender_email == initiator_email else "responder"
            participants_map[sender_email] = Participant(
                name=msg["from_name"] or sender_email.split("@")[0], email=sender_email, role=role
            )

        # Add To recipients
        for recipient in msg.get("to", []):
            email_addr = recipient["email"].lower()
            if email_addr and email_addr not in participants_map:
                participants_map[email_addr] = Participant(
                    name=recipient["name"] or email_addr.split("@")[0], email=email_addr, role="responder"
                )

        # Add CC recipients
        for recipient in msg.get("cc", []):
            email_addr = recipient["email"].lower()
            if email_addr and email_addr not in participants_map:
                participants_map[email_addr] = Participant(
                    name=recipient["name"] or email_addr.split("@")[0], email=email_addr, role="cc"
                )

    return list(participants_map.values())


def extract_action_items(messages: list[dict]) -> list[ActionItem]:
    """Extract action items from messages."""
    action_items = []
    item_id = 0

    for msg in messages:
        body = msg.get("body", "")
        msg_date = msg.get("date", "")
        sender = msg.get("from_name", "") or msg.get("from_email", "")

        # Check commitment patterns (sender commits)
        for pattern, confidence in COMMITMENT_PATTERNS:
            matches = re.findall(pattern, body, re.IGNORECASE)
            for match in matches:
                item_id += 1
                action_items.append(
                    ActionItem(
                        id=f"AI-{item_id:03d}",
                        description=match.strip()[:200],
                        owner=sender,
                        status="pending",
                        due_date=extract_deadline_from_context(body, match),
                        source_message_date=msg_date,
                    )
                )

        # Check request patterns (someone else should act)
        for pattern, confidence in REQUEST_PATTERNS:
            matches = re.findall(pattern, body, re.IGNORECASE)
            for match in matches:
                item_id += 1
                # Try to identify the target of the request
                owner = "TBD"
                to_recipients = msg.get("to", [])
                if to_recipients:
                    owner = to_recipients[0].get("name", "") or to_recipients[0].get("email", "")

                action_items.append(
                    ActionItem(
                        id=f"AI-{item_id:03d}",
                        description=match.strip()[:200],
                        owner=owner,
                        status="pending",
                        due_date=extract_deadline_from_context(body, match),
                        source_message_date=msg_date,
                    )
                )

    return action_items


def extract_deadline_from_context(body: str, action_text: str) -> Optional[str]:
    """Try to extract a deadline from the context around an action item."""
    # Find the sentence containing the action
    sentences = re.split(r"[.!?]\s+", body)
    for sentence in sentences:
        if action_text.lower() in sentence.lower():
            # Check for deadline patterns
            for pattern, flags in DEADLINE_PATTERNS:
                if isinstance(flags, int):
                    match = re.search(pattern, sentence, flags)
                else:
                    match = re.search(pattern, sentence)
                if match:
                    return match.group(1) if match.lastindex else match.group(0)
    return None


def extract_decisions(messages: list[dict]) -> list[KeyDecision]:
    """Extract key decisions from messages."""
    decisions = []

    for msg in messages:
        body = msg.get("body", "")
        msg_date = msg.get("date", "")
        sender = msg.get("from_name", "") or msg.get("from_email", "")

        for pattern, confidence in DECISION_PATTERNS:
            matches = re.findall(pattern, body, re.IGNORECASE)
            for match in matches:
                if isinstance(match, str) and len(match) > 3:
                    decisions.append(KeyDecision(date=msg_date, decision=match.strip()[:300], made_by=sender))

    return decisions


def extract_timeline(messages: list[dict]) -> list[TimelineEvent]:
    """Build timeline of significant events."""
    timeline = []

    sorted_messages = sorted(messages, key=lambda m: parse_date(m["date"]) or datetime.min.replace(tzinfo=timezone.utc))

    for msg in sorted_messages:
        body = msg.get("body", "")
        msg_date = msg.get("date", "")
        sender = msg.get("from_name", "") or msg.get("from_email", "")

        # Determine event type
        event_type = "response"
        summary = ""

        # Check for resolution
        for pattern in RESOLUTION_PATTERNS:
            if re.search(pattern, body, re.IGNORECASE):
                event_type = "resolution"
                summary = "Thread resolved"
                break

        # Check for escalation
        if event_type == "response":
            for pattern in ESCALATION_PATTERNS:
                if re.search(pattern, body, re.IGNORECASE):
                    event_type = "escalation"
                    summary = "Thread escalated"
                    break

        # Check for decision
        if event_type == "response":
            for pattern, _ in DECISION_PATTERNS:
                match = re.search(pattern, body, re.IGNORECASE)
                if match:
                    event_type = "decision"
                    summary = f"Decision: {match.group(1)[:100] if match.lastindex else 'made'}"
                    break

        # Check for request
        if event_type == "response":
            for pattern, _ in REQUEST_PATTERNS:
                if re.search(pattern, body, re.IGNORECASE):
                    event_type = "request"
                    summary = "Request made"
                    break

        # Default summary from subject/first line
        if not summary:
            first_line = body.split("\n")[0][:100] if body else msg.get("subject", "")[:100]
            summary = first_line

        timeline.append(TimelineEvent(date=msg_date, actor=sender, event_type=event_type, summary=summary))

    return timeline


def detect_superseded_info(messages: list[dict]) -> list[OutdatedInfo]:
    """Detect information that has been superseded by later messages."""
    outdated = []

    sorted_messages = sorted(messages, key=lambda m: parse_date(m["date"]) or datetime.min.replace(tzinfo=timezone.utc))

    for i, msg in enumerate(sorted_messages):
        body = msg.get("body", "")
        msg_date = msg.get("date", "")

        # Check for supersession patterns
        for pattern in SUPERSESSION_PATTERNS:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                # Find the superseded content
                context_start = match.end()
                context_end = min(context_start + 200, len(body))
                new_info = body[context_start:context_end].split(".")[0].strip()

                if new_info and i > 0:
                    # Reference the previous message as the source of superseded info
                    prev_msg = sorted_messages[i - 1]
                    outdated.append(
                        OutdatedInfo(
                            original_statement="[Previous statement]",
                            stated_date=prev_msg.get("date", ""),
                            superseded_by=new_info[:200],
                            superseded_date=msg_date,
                        )
                    )

    return outdated


def classify_thread_status(messages: list[dict]) -> ThreadStatus:
    """Classify the overall status of the thread."""
    if not messages:
        return ThreadStatus(classification="unknown", confidence=0.0, last_action_date="", days_since_last_action=0)

    sorted_messages = sorted(messages, key=lambda m: parse_date(m["date"]) or datetime.min.replace(tzinfo=timezone.utc))

    last_msg = sorted_messages[-1]
    last_date = parse_date(last_msg["date"])
    last_body = last_msg.get("body", "")

    now = datetime.now(timezone.utc)
    days_since = (now - last_date).days if last_date else 0

    # Check for resolution
    for pattern in RESOLUTION_PATTERNS:
        if re.search(pattern, last_body, re.IGNORECASE):
            return ThreadStatus(
                classification="resolved",
                confidence=0.9,
                last_action_date=last_msg["date"],
                days_since_last_action=days_since,
            )

    # Check for escalation
    for pattern in ESCALATION_PATTERNS:
        if re.search(pattern, last_body, re.IGNORECASE):
            return ThreadStatus(
                classification="escalated",
                confidence=0.85,
                last_action_date=last_msg["date"],
                days_since_last_action=days_since,
            )

    # Check for awaiting response (last message is a question)
    if "?" in last_body or any(re.search(p, last_body, re.IGNORECASE) for p, _ in REQUEST_PATTERNS):
        return ThreadStatus(
            classification="awaiting_response",
            confidence=0.8,
            last_action_date=last_msg["date"],
            days_since_last_action=days_since,
        )

    # Check for stale (7+ days with pending items)
    if days_since >= 7:
        return ThreadStatus(
            classification="stale",
            confidence=0.75,
            last_action_date=last_msg["date"],
            days_since_last_action=days_since,
        )

    # Default to active
    return ThreadStatus(
        classification="active", confidence=0.7, last_action_date=last_msg["date"], days_since_last_action=days_since
    )


def analyze_thread(messages: list[dict], thread_id: str = "") -> ThreadAnalysis:
    """Perform complete thread analysis."""
    if not messages:
        return ThreadAnalysis(thread_id=thread_id, analysis_timestamp=datetime.now(timezone.utc).isoformat())

    # Sort messages by date
    sorted_messages = sorted(messages, key=lambda m: parse_date(m["date"]) or datetime.min.replace(tzinfo=timezone.utc))

    # Extract subject from first message
    subject = sorted_messages[0].get("subject", "")

    # Get thread ID if not provided
    if not thread_id:
        thread_id = sorted_messages[0].get("thread_id", sorted_messages[0].get("id", ""))

    # Calculate date range
    first_date = parse_date(sorted_messages[0]["date"])
    last_date = parse_date(sorted_messages[-1]["date"])
    duration = (last_date - first_date).days if first_date and last_date else 0

    date_range = DateRange(
        first_message=sorted_messages[0]["date"], last_message=sorted_messages[-1]["date"], duration_days=duration
    )

    return ThreadAnalysis(
        thread_id=thread_id,
        subject=subject,
        participants=[asdict(p) for p in extract_participants(messages)],
        message_count=len(messages),
        date_range=asdict(date_range),
        status=asdict(classify_thread_status(messages)),
        timeline=[asdict(e) for e in extract_timeline(messages)],
        action_items=[asdict(a) for a in extract_action_items(messages)],
        key_decisions=[asdict(d) for d in extract_decisions(messages)],
        outdated_info=[asdict(o) for o in detect_superseded_info(messages)],
        analysis_timestamp=datetime.now(timezone.utc).isoformat(),
    )


def main():
    parser = argparse.ArgumentParser(description="Analyze email thread and extract structured information")
    parser.add_argument("--input", "-i", required=True, help="Input file path (JSON, EML, or MBOX)")
    parser.add_argument(
        "--format",
        "-f",
        choices=["gmail", "outlook", "eml", "mbox"],
        default="gmail",
        help="Input format (default: gmail)",
    )
    parser.add_argument("--output", "-o", help="Output JSON file path (default: stdout)")
    parser.add_argument("--thread-id", help="Thread ID to use (overrides auto-detection)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Parse input based on format
    try:
        if args.format in ["gmail", "outlook"]:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if args.format == "gmail":
                messages = parse_gmail_json(data)
            else:
                messages = parse_outlook_json(data)

        elif args.format == "eml":
            messages = parse_eml_file(input_path)

        elif args.format == "mbox":
            messages = parse_mbox_file(input_path)

        else:
            print(f"Error: Unsupported format: {args.format}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error parsing input: {e}", file=sys.stderr)
        sys.exit(1)

    # Perform analysis
    analysis = analyze_thread(messages, args.thread_id or "")

    # Output result
    result = asdict(analysis)

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Analysis written to: {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
