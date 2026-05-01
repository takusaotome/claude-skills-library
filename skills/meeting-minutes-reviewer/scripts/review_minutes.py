#!/usr/bin/env python3
"""
Meeting Minutes Reviewer

Analyzes meeting minutes documents for completeness, action item clarity,
decision documentation, and consistency with source materials.

Usage:
    python3 review_minutes.py --minutes path/to/minutes.md [--hearing-sheet path/to/source.md]
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Finding:
    """Represents a review finding."""

    severity: str  # critical, warning, suggestion
    dimension: str  # completeness, action_items, decisions, consistency, clarity
    location: str
    issue: str
    suggestion: str


@dataclass
class ReviewResult:
    """Complete review result with scores and findings."""

    schema_version: str = "1.0"
    review_timestamp: str = ""
    minutes_file: str = ""
    source_files: list = field(default_factory=list)
    overall_score: int = 0
    dimension_scores: dict = field(default_factory=dict)
    findings: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)


class MinutesReviewer:
    """Reviews meeting minutes for quality and completeness."""

    # Required sections for completeness check
    REQUIRED_SECTIONS = ["attendee", "agenda", "discussion", "decision", "action", "next"]

    # Weights for each dimension
    WEIGHTS = {"completeness": 0.25, "action_items": 0.25, "decisions": 0.20, "consistency": 0.15, "clarity": 0.15}

    # Vague language patterns to flag
    VAGUE_PATTERNS = [
        (r"\bsoon\b", "Replace 'soon' with specific date"),
        (r"\blater\b", "Replace 'later' with specific timeline"),
        (r"\bASAP\b", "Replace 'ASAP' with specific date"),
        (r"\bimprove\b(?!\s+\w+\s+(by|to)\s+\d)", "Add specific improvement target"),
        (r"\blook into\b", "Replace with specific investigation action"),
        (r"\bfollow up\b(?!\s+with\s+\w+)", "Specify who to follow up with and deadline"),
        (r"\bthe team\b\s+(will|should|to)\b", "Assign to specific individual, not 'the team'"),
        (r"\bwe\b\s+(will|should)\b", "Specify who in 'we'"),
    ]

    # Action item patterns
    ACTION_PATTERNS = [
        r"^\s*[-*]\s*\[\s*[xX ]?\s*\]",  # Checkbox format
        r"^\s*[-*]\s*@\w+",  # @mention format
        r"^\s*[-*]\s*\w+\s+(to|will|should)\s+",  # Name + verb format
        r"Action\s*:?\s*\w+",  # "Action:" prefix
        r"TODO\s*:?\s*",  # TODO prefix
    ]

    # Decision patterns
    DECISION_PATTERNS = [
        r"(?i)^#+\s*decision",
        r"(?i)decided\s+to\b",
        r"(?i)agreed\s+to\b",
        r"(?i)will\s+proceed\s+with\b",
        r"(?i)approved\s*:?\s*",
        r"(?i)resolved\s*:?\s*",
    ]

    def __init__(self, minutes_path: Path, hearing_sheet_path: Optional[Path] = None):
        """Initialize reviewer with document paths."""
        self.minutes_path = minutes_path
        self.hearing_sheet_path = hearing_sheet_path
        self.minutes_content = ""
        self.minutes_lines: list[str] = []
        self.hearing_content = ""
        self.findings: list[Finding] = []

    def load_documents(self) -> bool:
        """Load the minutes and optional source documents."""
        try:
            self.minutes_content = self.minutes_path.read_text(encoding="utf-8")
            self.minutes_lines = self.minutes_content.split("\n")
        except Exception as e:
            print(f"Error loading minutes: {e}", file=sys.stderr)
            return False

        if self.hearing_sheet_path:
            try:
                self.hearing_content = self.hearing_sheet_path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"Warning: Could not load hearing sheet: {e}", file=sys.stderr)

        return True

    def check_completeness(self) -> int:
        """Check for required sections. Returns score 0-100."""
        content_lower = self.minutes_content.lower()
        sections_found = 0
        total_sections = len(self.REQUIRED_SECTIONS)

        section_checks = {
            "attendee": [r"attendee", r"participant", r"present\s*:", r"\|.*name.*\|"],
            "agenda": [r"agenda", r"topics?\s*:", r"items?\s+discussed"],
            "discussion": [r"discussion", r"summary", r"key\s+points?", r"highlights?"],
            "decision": [r"decision", r"agreed", r"decided", r"resolved"],
            "action": [r"action\s*items?", r"next\s+actions?", r"follow\s*-?\s*ups?", r"tasks?", r"todo"],
            "next": [r"next\s+steps?", r"next\s+meeting", r"follow\s*-?\s*up\s+meeting"],
        }

        for section, patterns in section_checks.items():
            found = any(re.search(p, content_lower) for p in patterns)
            if found:
                sections_found += 1
            else:
                self.findings.append(
                    Finding(
                        severity="warning" if section in ["next"] else "critical",
                        dimension="completeness",
                        location="document",
                        issue=f"Missing required section: {section}",
                        suggestion=f"Add a clear '{section}' section to the minutes",
                    )
                )

        # Check for meeting header details
        header_items = [
            (r"date\s*:", "Meeting date"),
            (r"time\s*:", "Meeting time"),
            (r"\d{4}[-/]\d{2}[-/]\d{2}", "Date in standard format"),
        ]

        header_score = 0
        for pattern, item_name in header_items:
            if re.search(pattern, content_lower):
                header_score += 1
            else:
                self.findings.append(
                    Finding(
                        severity="warning",
                        dimension="completeness",
                        location="header",
                        issue=f"Missing or unclear: {item_name}",
                        suggestion=f"Add {item_name} to the meeting header",
                    )
                )

        # Calculate score: sections worth 70%, header worth 30%
        section_score = (sections_found / total_sections) * 70
        header_pct = (header_score / len(header_items)) * 30
        return int(section_score + header_pct)

    def check_action_items(self) -> int:
        """Check action items for completeness. Returns score 0-100."""
        action_items = []
        in_action_section = False

        for i, line in enumerate(self.minutes_lines):
            line_lower = line.lower()

            # Detect action section
            if re.search(r"(?i)action\s*items?|next\s+actions?|tasks?|todo", line_lower):
                in_action_section = True
                continue

            # Detect section end
            if in_action_section and re.match(r"^#+\s+", line) and not re.search(r"(?i)action", line):
                in_action_section = False

            # Check for action item patterns
            if any(re.search(p, line) for p in self.ACTION_PATTERNS):
                action_items.append((i + 1, line))
            elif in_action_section and re.match(r"^\s*[-*]\s+\w", line):
                action_items.append((i + 1, line))

        if not action_items:
            self.findings.append(
                Finding(
                    severity="critical",
                    dimension="action_items",
                    location="document",
                    issue="No action items found",
                    suggestion="Add action items section with owner, deadline, and description for each task",
                )
            )
            return 0

        # Check each action item for required components
        total_score = 0
        for line_num, item in action_items:
            item_score = 0
            item_lower = item.lower()

            # Check for owner (30%)
            has_owner = bool(re.search(r"@\w+|:\s*\w+\s+(to|will)|^\s*[-*]\s*\[\s*[xX ]?\s*\]\s*@?\w+", item))
            if has_owner:
                item_score += 30
            else:
                self.findings.append(
                    Finding(
                        severity="critical",
                        dimension="action_items",
                        location=f"line {line_num}",
                        issue="Action item missing owner",
                        suggestion="Add owner using format '@Name' or 'Name:'",
                    )
                )

            # Check for deadline (30%)
            has_deadline = bool(
                re.search(
                    r"\d{4}[-/]\d{2}[-/]\d{2}|"  # YYYY-MM-DD or YYYY/MM/DD
                    r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|"  # MM/DD/YYYY variants
                    r"due\s*:\s*\w+|"  # Due: keyword
                    r"by\s+\w+day|"  # by Friday
                    r"by\s+\w+\s+\d{1,2}",  # by January 15
                    item_lower,
                )
            )
            if has_deadline:
                item_score += 30
            else:
                self.findings.append(
                    Finding(
                        severity="critical",
                        dimension="action_items",
                        location=f"line {line_num}",
                        issue="Action item missing deadline",
                        suggestion="Add specific deadline using format 'Due: YYYY-MM-DD'",
                    )
                )

            # Check for clear description (40%)
            # Description should have a verb and object, minimum word count
            words = re.findall(r"\b\w+\b", item)
            has_description = len(words) >= 5
            if has_description:
                item_score += 40
            else:
                self.findings.append(
                    Finding(
                        severity="warning",
                        dimension="action_items",
                        location=f"line {line_num}",
                        issue="Action item description too brief",
                        suggestion="Expand description to clearly specify the task",
                    )
                )

            total_score += item_score

        return int(total_score / len(action_items)) if action_items else 0

    def check_decisions(self) -> int:
        """Check decision documentation. Returns score 0-100."""
        decisions = []

        for i, line in enumerate(self.minutes_lines):
            if any(re.search(p, line) for p in self.DECISION_PATTERNS):
                # Capture this line and context
                context_start = max(0, i - 2)
                context_end = min(len(self.minutes_lines), i + 5)
                context = "\n".join(self.minutes_lines[context_start:context_end])
                decisions.append((i + 1, line, context))

        if not decisions:
            self.findings.append(
                Finding(
                    severity="critical",
                    dimension="decisions",
                    location="document",
                    issue="No decisions documented",
                    suggestion="Add 'Decisions' section with clear decision statements, context, and rationale",
                )
            )
            return 0

        total_score = 0
        for line_num, decision_line, context in decisions:
            item_score = 0
            context_lower = context.lower()

            # Check for decision statement (40%)
            if re.search(r"(?i)decided|agreed|approved|resolved|will\s+(use|proceed|implement)", decision_line):
                item_score += 40
            else:
                self.findings.append(
                    Finding(
                        severity="warning",
                        dimension="decisions",
                        location=f"line {line_num}",
                        issue="Decision statement unclear",
                        suggestion="Start with clear decision verb: 'Decided to...', 'Agreed to...'",
                    )
                )

            # Check for context (25%)
            if re.search(r"context|because|since|due to|as\s+\w+\s+needs?", context_lower):
                item_score += 25
            else:
                self.findings.append(
                    Finding(
                        severity="warning",
                        dimension="decisions",
                        location=f"line {line_num}",
                        issue="Decision lacks context",
                        suggestion="Add context explaining why this decision was needed",
                    )
                )

            # Check for rationale (25%)
            if re.search(r"rationale|reason|because|chosen|selected|preferred", context_lower):
                item_score += 25
            else:
                self.findings.append(
                    Finding(
                        severity="suggestion",
                        dimension="decisions",
                        location=f"line {line_num}",
                        issue="Decision missing rationale",
                        suggestion="Add rationale explaining why this option was chosen",
                    )
                )

            # Check for alternatives mentioned (10%)
            if re.search(r"alternative|option|considered|instead|versus|vs\.?|or\s+\w+", context_lower):
                item_score += 10

            total_score += item_score

        return int(total_score / len(decisions)) if decisions else 0

    def check_consistency(self) -> int:
        """Check consistency with source materials. Returns score 0-100."""
        if not self.hearing_content:
            # No source material to compare, give neutral score
            return 80

        score = 100

        # Extract agenda items from hearing sheet
        hearing_topics = set()
        for line in self.hearing_content.split("\n"):
            # Look for numbered items, headers, or bullet points
            if re.match(r"^\s*(\d+\.?|[-*]|#+)\s+\w", line):
                # Extract key words (3+ chars)
                words = re.findall(r"\b[a-zA-Z]{3,}\b", line.lower())
                hearing_topics.update(words)

        # Check if key topics appear in minutes
        minutes_lower = self.minutes_content.lower()
        missing_topics = []
        for topic in hearing_topics:
            # Skip common words
            if topic in ["the", "and", "for", "with", "that", "this", "from", "will", "have", "been"]:
                continue
            if topic not in minutes_lower:
                missing_topics.append(topic)

        if missing_topics:
            # Deduct points based on missing topics
            deduction = min(30, len(missing_topics) * 5)
            score -= deduction
            if len(missing_topics) > 3:
                self.findings.append(
                    Finding(
                        severity="warning",
                        dimension="consistency",
                        location="document",
                        issue=f"Several agenda topics may be missing: {', '.join(missing_topics[:5])}",
                        suggestion="Ensure all agenda items are addressed in minutes",
                    )
                )

        return max(0, score)

    def check_clarity(self) -> int:
        """Check for clear, specific language. Returns score 0-100."""
        score = 100
        vague_count = 0

        for i, line in enumerate(self.minutes_lines):
            for pattern, suggestion in self.VAGUE_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    vague_count += 1
                    if vague_count <= 5:  # Limit findings
                        self.findings.append(
                            Finding(
                                severity="suggestion",
                                dimension="clarity",
                                location=f"line {i + 1}",
                                issue=f"Vague language detected: '{re.search(pattern, line, re.IGNORECASE).group()}'",
                                suggestion=suggestion,
                            )
                        )

        # Deduct points for vague language
        score -= min(40, vague_count * 5)

        # Check for ambiguous pronouns
        ambiguous_pronouns = re.findall(
            r"\b(they|it|this|these|those)\b(?!\s+(is|are|was|were|will|should|can)\b)",
            self.minutes_content,
            re.IGNORECASE,
        )
        if len(ambiguous_pronouns) > 10:
            score -= 10
            self.findings.append(
                Finding(
                    severity="suggestion",
                    dimension="clarity",
                    location="document",
                    issue="Multiple potentially ambiguous pronouns",
                    suggestion="Replace pronouns with specific nouns where antecedent is unclear",
                )
            )

        return max(0, score)

    def review(self) -> ReviewResult:
        """Perform complete review and return results."""
        if not self.load_documents():
            raise RuntimeError("Failed to load documents")

        # Calculate dimension scores
        dimension_scores = {
            "completeness": self.check_completeness(),
            "action_items": self.check_action_items(),
            "decisions": self.check_decisions(),
            "consistency": self.check_consistency(),
            "clarity": self.check_clarity(),
        }

        # Calculate overall score
        overall_score = int(sum(score * self.WEIGHTS[dim] for dim, score in dimension_scores.items()))

        # Count findings by severity
        summary = {
            "critical_count": sum(1 for f in self.findings if f.severity == "critical"),
            "warning_count": sum(1 for f in self.findings if f.severity == "warning"),
            "suggestion_count": sum(1 for f in self.findings if f.severity == "suggestion"),
        }

        return ReviewResult(
            review_timestamp=datetime.now().isoformat() + "Z",
            minutes_file=str(self.minutes_path),
            source_files=[str(self.hearing_sheet_path)] if self.hearing_sheet_path else [],
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            findings=[asdict(f) for f in self.findings],
            summary=summary,
        )


def format_markdown(result: ReviewResult) -> str:
    """Format review result as markdown report."""
    lines = [
        "# Meeting Minutes Review Report",
        "",
        f"**File**: {result.minutes_file}",
        f"**Review Date**: {result.review_timestamp[:10]}",
        "",
        f"## Overall Score: {result.overall_score}/100",
        "",
        "| Dimension | Score | Status |",
        "|-----------|-------|--------|",
    ]

    for dim, score in result.dimension_scores.items():
        status = "Pass" if score >= 80 else ("Needs Work" if score >= 60 else "Fail")
        emoji = "G" if score >= 80 else ("W" if score >= 60 else "X")
        lines.append(f"| {dim.replace('_', ' ').title()} | {score} | {emoji} {status} |")

    lines.append("")

    # Group findings by severity
    for severity in ["critical", "warning", "suggestion"]:
        severity_findings = [f for f in result.findings if f["severity"] == severity]
        if severity_findings:
            lines.append(f"## {severity.title()} Issues ({len(severity_findings)})")
            lines.append("")
            for f in severity_findings:
                lines.append(f"### {f['issue']}")
                lines.append(f"- **Location**: {f['location']}")
                lines.append(f"- **Dimension**: {f['dimension']}")
                lines.append(f"- **Suggestion**: {f['suggestion']}")
                lines.append("")

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Review meeting minutes for quality and completeness")
    parser.add_argument("--minutes", "-m", type=Path, required=True, help="Path to meeting minutes file")
    parser.add_argument("--hearing-sheet", "-s", type=Path, help="Path to source hearing sheet for consistency check")
    parser.add_argument("--output", "-o", type=Path, help="Output file path (default: stdout)")
    parser.add_argument(
        "--format", "-f", choices=["json", "markdown"], default="json", help="Output format (default: json)"
    )

    args = parser.parse_args()

    # Validate input file exists
    if not args.minutes.exists():
        print(f"Error: Minutes file not found: {args.minutes}", file=sys.stderr)
        sys.exit(1)

    if args.hearing_sheet and not args.hearing_sheet.exists():
        print(f"Warning: Hearing sheet not found: {args.hearing_sheet}", file=sys.stderr)
        args.hearing_sheet = None

    # Run review
    reviewer = MinutesReviewer(args.minutes, args.hearing_sheet)
    try:
        result = reviewer.review()
    except Exception as e:
        print(f"Error during review: {e}", file=sys.stderr)
        sys.exit(1)

    # Format output
    if args.format == "json":
        output = json.dumps(asdict(result), indent=2)
    else:
        output = format_markdown(result)

    # Write output
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"Report written to: {args.output}")
    else:
        print(output)

    # Exit with error code if critical issues found
    if result.summary["critical_count"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
