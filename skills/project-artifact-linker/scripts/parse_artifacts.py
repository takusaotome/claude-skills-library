#!/usr/bin/env python3
"""
Parse project artifacts (meeting minutes, WBS, requirements, decisions) and extract structured entities.

Usage:
    python3 parse_artifacts.py --input-dir /path/to/docs --output artifacts.json
    python3 parse_artifacts.py --input-file meeting.md --output artifacts.json
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
class ActionItem:
    """Represents an action item extracted from meeting minutes."""

    id: str
    description: str
    owner: Optional[str] = None
    due_date: Optional[str] = None
    source_file: str = ""
    source_line: int = 0


@dataclass
class Decision:
    """Represents a decision extracted from meeting minutes or decision logs."""

    id: str
    description: str
    date: Optional[str] = None
    rationale: Optional[str] = None
    stakeholders: list = field(default_factory=list)
    source_file: str = ""
    source_line: int = 0


@dataclass
class Meeting:
    """Represents a meeting with extracted entities."""

    id: str
    date: Optional[str] = None
    title: Optional[str] = None
    attendees: list = field(default_factory=list)
    action_items: list = field(default_factory=list)
    decisions: list = field(default_factory=list)
    topics: list = field(default_factory=list)
    source_file: str = ""


@dataclass
class WBSTask:
    """Represents a WBS task."""

    id: str
    name: str
    owner: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None
    dependencies: list = field(default_factory=list)
    source_file: str = ""
    source_line: int = 0


@dataclass
class Requirement:
    """Represents a requirement."""

    id: str
    description: str
    priority: Optional[str] = None
    acceptance_criteria: list = field(default_factory=list)
    source_file: str = ""
    source_line: int = 0


class ArtifactParser:
    """Parse various project artifacts and extract structured entities."""

    # Date patterns
    DATE_PATTERNS = [
        r"(\d{4}-\d{2}-\d{2})",  # ISO format
        r"(\d{1,2}/\d{1,2}/\d{4})",  # US format
        r"((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})",
    ]

    # Action item patterns
    ACTION_PATTERNS = [
        r"(?:ACTION|TODO|Action Item):\s*(.+?)(?:\n|$)",
        r"@(\w+)\s+(?:to|will)\s+(.+?)(?:\n|$)",
        r"(\w+)\s+will\s+(.+?)(?:by\s+(.+?))?(?:\n|$)",
    ]

    # Decision patterns
    DECISION_PATTERNS = [
        r"(?:DECISION|Decided|Agreed|Resolution):\s*(.+?)(?:\n|$)",
        r"(?:We|Team)\s+will\s+(.+?)(?:\n|$)",
    ]

    # Requirement ID patterns
    REQ_ID_PATTERN = r"(REQ-[A-Z]{2,4}-\d+|R\d+|FR-\d+|NFR-\d+|SR-\d+|PR-\d+)"

    # WBS ID patterns
    WBS_ID_PATTERN = r"(WBS-\d+(?:\.\d+)*|\d+\.\d+(?:\.\d+)*|TASK-\d+)"

    # Decision ID patterns
    DEC_ID_PATTERN = r"(DEC-\d+|D\d+|DECISION-\d+|ADR-\d+)"

    def __init__(self):
        self.meetings: list[Meeting] = []
        self.wbs_tasks: list[WBSTask] = []
        self.requirements: list[Requirement] = []
        self.decisions: list[Decision] = []
        self._action_counter = 0
        self._decision_counter = 0
        self._meeting_counter = 0

    def _generate_action_id(self) -> str:
        self._action_counter += 1
        return f"AI-{self._action_counter:03d}"

    def _generate_decision_id(self) -> str:
        self._decision_counter += 1
        return f"DEC-{self._decision_counter:03d}"

    def _generate_meeting_id(self, date: Optional[str] = None) -> str:
        self._meeting_counter += 1
        if date:
            year = date[:4] if len(date) >= 4 else datetime.now().strftime("%Y")
            return f"MTG-{year}-{self._meeting_counter:03d}"
        return f"MTG-{datetime.now().strftime('%Y')}-{self._meeting_counter:03d}"

    def _extract_date(self, text: str) -> Optional[str]:
        """Extract and normalize date from text."""
        for pattern in self.DATE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                # Try to normalize to ISO format
                try:
                    # Already ISO format
                    if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
                        return date_str
                    # US format
                    if "/" in date_str:
                        parts = date_str.split("/")
                        return f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
                    # Month name format
                    for fmt in ["%B %d, %Y", "%B %d %Y"]:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            return dt.strftime("%Y-%m-%d")
                        except ValueError:
                            continue
                except (ValueError, IndexError):
                    pass
                return date_str
        return None

    def _extract_attendees(self, text: str) -> list[str]:
        """Extract attendee names from meeting minutes."""
        attendees = []

        # Look for attendee sections
        attendee_patterns = [
            r"(?:Attendees|Participants|Present|In Attendance):\s*(.+?)(?:\n\n|\n[A-Z])",
        ]

        for pattern in attendee_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                section = match.group(1)
                # Parse comma-separated or bullet list
                if "," in section:
                    attendees.extend([name.strip() for name in section.split(",") if name.strip()])
                else:
                    # Bullet list
                    bullet_pattern = r"[-*]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
                    attendees.extend(re.findall(bullet_pattern, section))
                break

        return attendees

    def _extract_action_items(self, text: str, source_file: str) -> list[ActionItem]:
        """Extract action items from text."""
        items = []
        lines = text.split("\n")

        for line_num, line in enumerate(lines, 1):
            # Pattern 1: ACTION: description
            match = re.search(r"(?:ACTION|TODO|Action Item):\s*(.+)", line, re.IGNORECASE)
            if match:
                desc = match.group(1).strip()
                owner = None
                due_date = None

                # Try to extract owner
                owner_match = re.search(r"@(\w+)|(\w+)\s+(?:to|will)", desc)
                if owner_match:
                    owner = owner_match.group(1) or owner_match.group(2)

                # Try to extract due date
                due_match = re.search(r"by\s+(.+?)(?:\s|$)", desc, re.IGNORECASE)
                if due_match:
                    due_date = self._extract_date(due_match.group(1))

                items.append(
                    ActionItem(
                        id=self._generate_action_id(),
                        description=desc,
                        owner=owner,
                        due_date=due_date,
                        source_file=source_file,
                        source_line=line_num,
                    )
                )
                continue

            # Pattern 2: @name to/will do something
            match = re.search(r"@(\w+)\s+(?:to|will)\s+(.+)", line)
            if match:
                items.append(
                    ActionItem(
                        id=self._generate_action_id(),
                        description=match.group(2).strip(),
                        owner=match.group(1),
                        due_date=None,
                        source_file=source_file,
                        source_line=line_num,
                    )
                )

        return items

    def _extract_decisions(self, text: str, source_file: str) -> list[Decision]:
        """Extract decisions from text."""
        decisions = []
        lines = text.split("\n")
        date = self._extract_date(text)

        for line_num, line in enumerate(lines, 1):
            match = re.search(
                r"(?:DECISION|Decided|Agreed|Resolution):\s*(.+)",
                line,
                re.IGNORECASE,
            )
            if match:
                desc = match.group(1).strip()
                rationale = None

                # Try to extract rationale
                rationale_match = re.search(
                    r"(?:because|due to|reason:)\s*(.+)",
                    desc,
                    re.IGNORECASE,
                )
                if rationale_match:
                    rationale = rationale_match.group(1).strip()

                # Check for existing decision ID
                id_match = re.search(self.DEC_ID_PATTERN, line)
                dec_id = id_match.group(1) if id_match else self._generate_decision_id()

                decisions.append(
                    Decision(
                        id=dec_id,
                        description=desc,
                        date=date,
                        rationale=rationale,
                        source_file=source_file,
                        source_line=line_num,
                    )
                )

        return decisions

    def parse_meeting_minutes(self, content: str, source_file: str) -> Meeting:
        """Parse meeting minutes and extract structured data."""
        date = self._extract_date(content)
        attendees = self._extract_attendees(content)
        action_items = self._extract_action_items(content, source_file)
        decisions = self._extract_decisions(content, source_file)

        # Extract title from first heading
        title_match = re.search(r"#\s+(.+?)(?:\n|$)", content)
        title = title_match.group(1).strip() if title_match else None

        meeting = Meeting(
            id=self._generate_meeting_id(date),
            date=date,
            title=title,
            attendees=attendees,
            action_items=[asdict(ai) for ai in action_items],
            decisions=[asdict(d) for d in decisions],
            source_file=source_file,
        )

        self.meetings.append(meeting)
        return meeting

    def parse_wbs(self, content: str, source_file: str) -> list[WBSTask]:
        """Parse WBS document and extract tasks."""
        tasks = []
        lines = content.split("\n")

        # Try to parse as markdown table
        in_table = False
        headers = []
        col_indices = {}

        for line_num, line in enumerate(lines, 1):
            # Detect table header
            if "|" in line and not in_table:
                if "task" in line.lower() or "wbs" in line.lower():
                    in_table = True
                    headers = [h.strip().lower() for h in line.split("|")]
                    for i, h in enumerate(headers):
                        if "id" in h or "task id" in h or "wbs" in h:
                            col_indices["id"] = i
                        elif "name" in h or "description" in h or "task" in h:
                            col_indices["name"] = i
                        elif "owner" in h or "assignee" in h or "responsible" in h:
                            col_indices["owner"] = i
                        elif "start" in h:
                            col_indices["start"] = i
                        elif "end" in h or "due" in h:
                            col_indices["end"] = i
                        elif "status" in h:
                            col_indices["status"] = i
                    continue

            # Skip separator line
            if in_table and re.match(r"\s*\|[-:|\s]+\|\s*$", line):
                continue

            # Parse table row
            if in_table and "|" in line:
                cols = [c.strip() for c in line.split("|")]
                if len(cols) > max(col_indices.values(), default=0):
                    task_id = cols[col_indices.get("id", 0)] if "id" in col_indices else None
                    if not task_id:
                        # Try to find WBS ID in the row
                        id_match = re.search(self.WBS_ID_PATTERN, line)
                        task_id = id_match.group(1) if id_match else f"TASK-{line_num}"

                    task = WBSTask(
                        id=task_id,
                        name=cols[col_indices.get("name", 1)] if "name" in col_indices else "",
                        owner=cols[col_indices.get("owner", -1)] if "owner" in col_indices else None,
                        start_date=self._extract_date(cols[col_indices.get("start", -1)])
                        if "start" in col_indices
                        else None,
                        end_date=self._extract_date(cols[col_indices.get("end", -1)]) if "end" in col_indices else None,
                        status=cols[col_indices.get("status", -1)] if "status" in col_indices else None,
                        source_file=source_file,
                        source_line=line_num,
                    )
                    if task.name:  # Only add if we have a name
                        tasks.append(task)
                        self.wbs_tasks.append(task)

        return tasks

    def parse_requirements(self, content: str, source_file: str) -> list[Requirement]:
        """Parse requirements document and extract requirements."""
        requirements = []
        lines = content.split("\n")

        current_req = None

        for line_num, line in enumerate(lines, 1):
            # Look for requirement ID
            id_match = re.search(self.REQ_ID_PATTERN, line)
            if id_match:
                if current_req:
                    requirements.append(current_req)
                    self.requirements.append(current_req)

                # Extract priority
                priority = None
                priority_match = re.search(
                    r"(?:Priority|P):\s*(\w+)|(\[(?:High|Medium|Low|Critical)\])",
                    line,
                    re.IGNORECASE,
                )
                if priority_match:
                    priority = (priority_match.group(1) or priority_match.group(2)).strip("[]")

                # Extract description (rest of line after ID)
                desc_start = id_match.end()
                description = line[desc_start:].strip().lstrip(":").strip()

                current_req = Requirement(
                    id=id_match.group(1),
                    description=description,
                    priority=priority,
                    source_file=source_file,
                    source_line=line_num,
                )
            elif current_req and line.strip():
                # Continue description or add acceptance criteria
                if "given" in line.lower() or "when" in line.lower() or "then" in line.lower():
                    current_req.acceptance_criteria.append(line.strip())
                elif not current_req.description:
                    current_req.description = line.strip()

        # Add last requirement
        if current_req:
            requirements.append(current_req)
            self.requirements.append(current_req)

        return requirements

    def parse_file(self, file_path: Path) -> None:
        """Parse a file based on its content and name."""
        content = file_path.read_text(encoding="utf-8")
        filename = file_path.name.lower()
        rel_path = str(file_path)

        # Determine document type by filename and content
        if "meeting" in filename or "minutes" in filename:
            self.parse_meeting_minutes(content, rel_path)
        elif "wbs" in filename or "schedule" in filename or "task" in filename:
            self.parse_wbs(content, rel_path)
        elif "requirement" in filename or "req" in filename or "spec" in filename:
            self.parse_requirements(content, rel_path)
        elif "decision" in filename or "adr" in filename:
            # Parse as decision log
            decisions = self._extract_decisions(content, rel_path)
            self.decisions.extend(decisions)
        else:
            # Try to auto-detect based on content
            if re.search(r"(?:Attendees|Participants|Present):", content, re.IGNORECASE):
                self.parse_meeting_minutes(content, rel_path)
            elif re.search(self.WBS_ID_PATTERN, content):
                self.parse_wbs(content, rel_path)
            elif re.search(self.REQ_ID_PATTERN, content):
                self.parse_requirements(content, rel_path)

    def parse_directory(self, dir_path: Path) -> None:
        """Parse all supported files in a directory."""
        extensions = [".md", ".txt", ".json", ".csv"]
        for ext in extensions:
            for file_path in dir_path.rglob(f"*{ext}"):
                try:
                    self.parse_file(file_path)
                except Exception as e:
                    print(f"Warning: Failed to parse {file_path}: {e}", file=sys.stderr)

    def to_dict(self) -> dict:
        """Convert all parsed artifacts to a dictionary."""
        return {
            "schema_version": "1.0",
            "extraction_date": datetime.now().isoformat(),
            "artifacts": {
                "meetings": [asdict(m) for m in self.meetings],
                "wbs_tasks": [asdict(t) for t in self.wbs_tasks],
                "requirements": [asdict(r) for r in self.requirements],
                "decisions": [asdict(d) for d in self.decisions],
            },
        }


def main():
    parser = argparse.ArgumentParser(description="Parse project artifacts and extract structured entities")
    parser.add_argument(
        "--input-dir",
        type=Path,
        help="Directory containing project documents",
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        help="Single file to parse",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("artifacts.json"),
        help="Output JSON file path",
    )

    args = parser.parse_args()

    if not args.input_dir and not args.input_file:
        parser.error("Either --input-dir or --input-file is required")

    artifact_parser = ArtifactParser()

    if args.input_file:
        if not args.input_file.exists():
            print(f"Error: File not found: {args.input_file}", file=sys.stderr)
            sys.exit(1)
        artifact_parser.parse_file(args.input_file)

    if args.input_dir:
        if not args.input_dir.is_dir():
            print(f"Error: Directory not found: {args.input_dir}", file=sys.stderr)
            sys.exit(1)
        artifact_parser.parse_directory(args.input_dir)

    # Write output
    result = artifact_parser.to_dict()
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"Extracted artifacts written to {args.output}")

    # Print summary
    artifacts = result["artifacts"]
    print("\nSummary:")
    print(f"  Meetings: {len(artifacts['meetings'])}")
    print(f"  WBS Tasks: {len(artifacts['wbs_tasks'])}")
    print(f"  Requirements: {len(artifacts['requirements'])}")
    print(f"  Decisions: {len(artifacts['decisions'])}")


if __name__ == "__main__":
    main()
