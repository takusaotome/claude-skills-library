#!/usr/bin/env python3
"""
Meeting Asset Preparer - CLI tool for preparing comprehensive meeting assets.

This script generates meeting agendas, decision logs, action item templates,
and reference material indices. Supports bilingual (Japanese/English) output.

Usage:
    python3 prepare_meeting.py init --title "Meeting" --date "2026-03-15" ...
    python3 prepare_meeting.py compile-refs --config meeting_config.yaml ...
    python3 prepare_meeting.py generate-agenda --config meeting_config.yaml ...
    python3 prepare_meeting.py create-decision-log --config meeting_config.yaml ...
    python3 prepare_meeting.py create-action-items --config meeting_config.yaml ...
    python3 prepare_meeting.py package --config meeting_config.yaml ...
"""

import argparse
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class Attendee:
    """Represents a meeting attendee."""

    name: str
    role: str = ""
    email: str = ""


@dataclass
class AgendaItem:
    """Represents an agenda item."""

    topic: str
    duration_minutes: int
    presenter: str = ""
    notes: str = ""


@dataclass
class MeetingConfig:
    """Meeting configuration data."""

    title: str
    date: str
    time: str
    timezone: str = "UTC"
    duration_minutes: int = 60
    attendees: list[Attendee] = field(default_factory=list)
    objectives: list[str] = field(default_factory=list)
    language: str = "en"  # en, ja, or bilingual
    agenda_items: list[AgendaItem] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        return {
            "meeting": {
                "title": self.title,
                "date": self.date,
                "time": self.time,
                "timezone": self.timezone,
                "duration_minutes": self.duration_minutes,
                "attendees": [{"name": a.name, "role": a.role, "email": a.email} for a in self.attendees],
                "objectives": self.objectives,
                "language": self.language,
                "agenda_items": [
                    {
                        "topic": item.topic,
                        "duration_minutes": item.duration_minutes,
                        "presenter": item.presenter,
                        "notes": item.notes,
                    }
                    for item in self.agenda_items
                ],
            }
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MeetingConfig":
        """Create from dictionary (loaded from YAML)."""
        meeting = data.get("meeting", data)
        config = cls(
            title=meeting.get("title", "Untitled Meeting"),
            date=meeting.get("date", ""),
            time=meeting.get("time", ""),
            timezone=meeting.get("timezone", "UTC"),
            duration_minutes=meeting.get("duration_minutes", 60),
            objectives=meeting.get("objectives", []),
            language=meeting.get("language", "en"),
        )
        for att in meeting.get("attendees", []):
            if isinstance(att, dict):
                config.attendees.append(
                    Attendee(
                        name=att.get("name", ""),
                        role=att.get("role", ""),
                        email=att.get("email", ""),
                    )
                )
            else:
                config.attendees.append(Attendee(name=str(att)))
        for item in meeting.get("agenda_items", []):
            if isinstance(item, dict):
                config.agenda_items.append(
                    AgendaItem(
                        topic=item.get("topic", ""),
                        duration_minutes=item.get("duration_minutes", 15),
                        presenter=item.get("presenter", ""),
                        notes=item.get("notes", ""),
                    )
                )
        return config


def get_bilingual_text(en: str, ja: str, language: str) -> str:
    """Return text based on language setting."""
    if language == "ja":
        return ja
    elif language == "bilingual":
        return f"{en} / {ja}"
    else:
        return en


def init_meeting(args) -> int:
    """Initialize a meeting configuration file."""
    attendees = []
    if args.attendees:
        for name in args.attendees.split(","):
            attendees.append(Attendee(name=name.strip()))

    config = MeetingConfig(
        title=args.title,
        date=args.date,
        time=args.time or "09:00",
        timezone=args.timezone or "UTC",
        duration_minutes=args.duration or 60,
        attendees=attendees,
        objectives=args.objectives.split(",") if args.objectives else [],
        language=args.language or "en",
    )

    output_path = Path(args.output)
    if yaml:
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False, allow_unicode=True)
    else:
        # Fallback to simple text format if pyyaml not installed
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Meeting Configuration\n")
            f.write(f"title: {config.title}\n")
            f.write(f"date: {config.date}\n")
            f.write(f"time: {config.time}\n")
            f.write(f"timezone: {config.timezone}\n")
            f.write(f"duration_minutes: {config.duration_minutes}\n")
            f.write(f"language: {config.language}\n")
            f.write(f"attendees: {', '.join(a.name for a in config.attendees)}\n")

    print(f"Meeting configuration created: {output_path}", file=sys.stderr)
    return 0


def load_config(config_path: str) -> Optional[MeetingConfig]:
    """Load meeting configuration from file."""
    path = Path(config_path)
    if not path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        return None

    with open(path, "r", encoding="utf-8") as f:
        if yaml:
            data = yaml.safe_load(f)
        else:
            # Simple fallback parser
            data = {"meeting": {}}
            for line in f:
                if ":" in line and not line.startswith("#"):
                    key, value = line.split(":", 1)
                    data["meeting"][key.strip()] = value.strip()

    return MeetingConfig.from_dict(data)


def compile_refs(args) -> int:
    """Compile reference materials from project directory."""
    config = load_config(args.config)
    if not config:
        return 1

    project_dir = Path(args.project_dir) if args.project_dir else Path(".")
    output_path = Path(args.output)

    # Find relevant documents
    references = []
    patterns = ["*.md", "*.pdf", "*.docx", "*.xlsx"]
    subdirs = ["estimates", "specs", "docs", "notes", "meetings", "decisions"]

    for subdir in subdirs:
        subdir_path = project_dir / subdir
        if subdir_path.exists():
            for pattern in patterns:
                for file_path in subdir_path.glob(pattern):
                    references.append(
                        {
                            "title": file_path.stem.replace("-", " ").replace("_", " "),
                            "path": str(file_path.relative_to(project_dir)),
                            "category": subdir,
                            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d"),
                        }
                    )

    # Generate reference index
    lang = config.language
    title = get_bilingual_text("Reference Materials", "参考資料", lang)

    lines = [
        f"# {title}\n",
        f"**{get_bilingual_text('Meeting', '会議', lang)}**: {config.title}",
        f"**{get_bilingual_text('Date', '日時', lang)}**: {config.date}\n",
        "---\n",
    ]

    if references:
        # Group by category
        categories = {}
        for ref in references:
            cat = ref["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(ref)

        for cat, refs in sorted(categories.items()):
            cat_title = get_bilingual_text(cat.title(), cat.title(), lang)
            lines.append(f"## {cat_title}\n")
            lines.append(
                f"| {get_bilingual_text('Document', '文書', lang)} | "
                f"{get_bilingual_text('Path', 'パス', lang)} | "
                f"{get_bilingual_text('Modified', '更新日', lang)} |"
            )
            lines.append("|----------|------|----------|")
            for ref in refs:
                lines.append(f"| {ref['title']} | [{ref['path']}]({ref['path']}) | {ref['modified']} |")
            lines.append("")
    else:
        lines.append(
            f"_{get_bilingual_text('No reference materials found in project directory.', 'プロジェクトディレクトリに参考資料が見つかりませんでした。', lang)}_\n"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Reference index created: {output_path}", file=sys.stderr)
    return 0


def generate_agenda(args) -> int:
    """Generate meeting agenda."""
    config = load_config(args.config)
    if not config:
        return 1

    output_path = Path(args.output)
    lang = config.language

    # Parse topics and durations
    agenda_items = []
    if args.topics:
        topics = [t.strip() for t in args.topics.split(",")]
        durations = [15] * len(topics)  # Default 15 minutes
        if args.durations:
            duration_list = [int(d.strip()) for d in args.durations.split(",")]
            for i, d in enumerate(duration_list):
                if i < len(durations):
                    durations[i] = d

        presenters = [""] * len(topics)
        if args.presenters:
            presenter_list = [p.strip() for p in args.presenters.split(",")]
            for i, p in enumerate(presenter_list):
                if i < len(presenters):
                    presenters[i] = p

        for i, topic in enumerate(topics):
            agenda_items.append(
                AgendaItem(
                    topic=topic,
                    duration_minutes=durations[i],
                    presenter=presenters[i] if i < len(presenters) else "",
                )
            )
    else:
        agenda_items = config.agenda_items

    # Generate agenda markdown
    lines = [
        f"# {get_bilingual_text('Meeting Agenda', '会議アジェンダ', lang)}\n",
        f"**{get_bilingual_text('Title', 'タイトル', lang)}**: {config.title}",
        f"**{get_bilingual_text('Date', '日時', lang)}**: {config.date} {config.time} {config.timezone}",
        f"**{get_bilingual_text('Duration', '所要時間', lang)}**: {config.duration_minutes} {get_bilingual_text('minutes', '分', lang)}\n",
        "---\n",
    ]

    # Objectives
    if config.objectives:
        lines.append(f"## {get_bilingual_text('Objectives', '目的', lang)}\n")
        for obj in config.objectives:
            lines.append(f"- {obj}")
        lines.append("")

    # Attendees
    if config.attendees:
        lines.append(f"## {get_bilingual_text('Attendees', '参加者', lang)}\n")
        lines.append(f"| {get_bilingual_text('Name', '名前', lang)} | {get_bilingual_text('Role', '役割', lang)} |")
        lines.append("|------|------|")
        for att in config.attendees:
            lines.append(f"| {att.name} | {att.role} |")
        lines.append("")

    # Agenda items
    lines.append(f"## {get_bilingual_text('Agenda Items', '議題', lang)}\n")
    lines.append(
        f"| # | {get_bilingual_text('Topic', '議題', lang)} | "
        f"{get_bilingual_text('Duration', '時間', lang)} | "
        f"{get_bilingual_text('Presenter', '担当', lang)} |"
    )
    lines.append("|---|-------|----------|-----------|")
    for i, item in enumerate(agenda_items, 1):
        lines.append(f"| {i} | {item.topic} | {item.duration_minutes} min | {item.presenter} |")
    lines.append("")

    # Total time
    total_minutes = sum(item.duration_minutes for item in agenda_items)
    lines.append(
        f"**{get_bilingual_text('Total Time', '合計時間', lang)}**: {total_minutes} {get_bilingual_text('minutes', '分', lang)}\n"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Agenda created: {output_path}", file=sys.stderr)
    return 0


def create_decision_log(args) -> int:
    """Create decision log template."""
    config = load_config(args.config)
    if not config:
        return 1

    output_path = Path(args.output)
    lang = config.language

    attendees_list = ", ".join(a.name for a in config.attendees)

    lines = [
        f"# {get_bilingual_text('Decision Log', '決定事項ログ', lang)}\n",
        f"**{get_bilingual_text('Meeting', '会議', lang)}**: {config.title}",
        f"**{get_bilingual_text('Date', '日時', lang)}**: {config.date}",
        f"**{get_bilingual_text('Attendees', '参加者', lang)}**: {attendees_list}\n",
        "---\n",
        f"## {get_bilingual_text('Decisions Made', '決定事項', lang)}\n",
        f"| # | {get_bilingual_text('Decision', '決定事項', lang)} | "
        f"{get_bilingual_text('Rationale', '理由', lang)} | "
        f"{get_bilingual_text('Owner', '担当', lang)} | "
        f"{get_bilingual_text('Date', '日付', lang)} |",
        "|---|----------|-----------|-------|------|",
        f"| 1 |          |           |       | {config.date} |",
        f"| 2 |          |           |       | {config.date} |",
        f"| 3 |          |           |       | {config.date} |",
        "",
        "---\n",
        f"## {get_bilingual_text('Pending Decisions', '未決定事項', lang)}\n",
        f"| # | {get_bilingual_text('Topic', '議題', lang)} | "
        f"{get_bilingual_text('Blocker', '障害', lang)} | "
        f"{get_bilingual_text('Target Date', '目標日', lang)} |",
        "|---|-------|---------|-------------|",
        "| 1 |       |         |             |",
        "",
        "---\n",
        f"**{get_bilingual_text('Last Updated', '最終更新', lang)}**: {config.date}",
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Decision log created: {output_path}", file=sys.stderr)
    return 0


def create_action_items(args) -> int:
    """Create action items template."""
    config = load_config(args.config)
    if not config:
        return 1

    output_path = Path(args.output)
    lang = config.language

    lines = [
        f"# {get_bilingual_text('Action Items', 'アクションアイテム', lang)}\n",
        f"**{get_bilingual_text('Meeting', '会議', lang)}**: {config.title}",
        f"**{get_bilingual_text('Date', '日時', lang)}**: {config.date}\n",
        "---\n",
        f"## {get_bilingual_text('Summary', 'サマリー', lang)}\n",
        f"| {get_bilingual_text('Status', '状態', lang)} | {get_bilingual_text('Count', '件数', lang)} |",
        "|--------|-------|",
        f"| {get_bilingual_text('Open', '未着手', lang)} | 0 |",
        f"| {get_bilingual_text('In Progress', '進行中', lang)} | 0 |",
        f"| {get_bilingual_text('Blocked', '保留', lang)} | 0 |",
        f"| {get_bilingual_text('Completed', '完了', lang)} | 0 |",
        "",
        "---\n",
        f"## {get_bilingual_text('Action Items', 'アクションアイテム一覧', lang)}\n",
        f"| # | {get_bilingual_text('Task', 'タスク', lang)} | "
        f"{get_bilingual_text('Owner', '担当', lang)} | "
        f"{get_bilingual_text('Priority', '優先度', lang)} | "
        f"{get_bilingual_text('Due Date', '期限', lang)} | "
        f"{get_bilingual_text('Status', '状態', lang)} |",
        "|---|------|-------|----------|----------|--------|",
        f"| 1 |      |       | {get_bilingual_text('High', '高', lang)} |          | {get_bilingual_text('Open', '未着手', lang)} |",
        f"| 2 |      |       | {get_bilingual_text('Medium', '中', lang)} |          | {get_bilingual_text('Open', '未着手', lang)} |",
        f"| 3 |      |       | {get_bilingual_text('Low', '低', lang)} |          | {get_bilingual_text('Open', '未着手', lang)} |",
        "",
        "---\n",
        f"**{get_bilingual_text('Last Updated', '最終更新', lang)}**: {config.date}",
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Action items template created: {output_path}", file=sys.stderr)
    return 0


def package_meeting(args) -> int:
    """Package all meeting assets into a directory."""
    config = load_config(args.config)
    if not config:
        return 1

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    lang = config.language

    # Copy or verify input files
    files_to_include = []

    if args.agenda and Path(args.agenda).exists():
        files_to_include.append(("agenda.md", Path(args.agenda)))
    if args.references and Path(args.references).exists():
        files_to_include.append(("references.md", Path(args.references)))
    if args.decision_log and Path(args.decision_log).exists():
        files_to_include.append(("decision_log.md", Path(args.decision_log)))
    if args.action_items and Path(args.action_items).exists():
        files_to_include.append(("action_items.md", Path(args.action_items)))

    # Copy files to output directory
    for dest_name, src_path in files_to_include:
        dest_path = output_dir / dest_name
        dest_path.write_text(src_path.read_text(encoding="utf-8"), encoding="utf-8")

    # Create index file
    index_lines = [
        f"# {get_bilingual_text('Meeting Package', '会議パッケージ', lang)}\n",
        f"**{get_bilingual_text('Meeting', '会議', lang)}**: {config.title}",
        f"**{get_bilingual_text('Date', '日時', lang)}**: {config.date} {config.time} {config.timezone}",
        f"**{get_bilingual_text('Created', '作成日', lang)}**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        "---\n",
        f"## {get_bilingual_text('Contents', '目次', lang)}\n",
    ]

    for dest_name, _ in files_to_include:
        display_name = dest_name.replace("_", " ").replace(".md", "").title()
        index_lines.append(f"- [{display_name}]({dest_name})")

    index_lines.extend(
        [
            "",
            "---\n",
            f"## {get_bilingual_text('Attendees', '参加者', lang)}\n",
        ]
    )
    for att in config.attendees:
        role_str = f" ({att.role})" if att.role else ""
        index_lines.append(f"- {att.name}{role_str}")

    if config.objectives:
        index_lines.extend(
            [
                "",
                f"## {get_bilingual_text('Objectives', '目的', lang)}\n",
            ]
        )
        for obj in config.objectives:
            index_lines.append(f"- {obj}")

    index_path = output_dir / "index.md"
    index_path.write_text("\n".join(index_lines), encoding="utf-8")

    print(f"Meeting package created: {output_dir}", file=sys.stderr)
    print("  - index.md", file=sys.stderr)
    for dest_name, _ in files_to_include:
        print(f"  - {dest_name}", file=sys.stderr)

    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Meeting Asset Preparer - Generate comprehensive meeting assets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize meeting configuration")
    init_parser.add_argument("--title", required=True, help="Meeting title")
    init_parser.add_argument("--date", required=True, help="Meeting date (YYYY-MM-DD)")
    init_parser.add_argument("--time", help="Meeting time (HH:MM)")
    init_parser.add_argument("--timezone", default="UTC", help="Timezone (e.g., JST, EST)")
    init_parser.add_argument("--duration", type=int, default=60, help="Duration in minutes")
    init_parser.add_argument("--attendees", help="Comma-separated attendee names")
    init_parser.add_argument("--objectives", help="Comma-separated meeting objectives")
    init_parser.add_argument("--language", choices=["en", "ja", "bilingual"], default="en")
    init_parser.add_argument("--output", "-o", required=True, help="Output config file path")

    # compile-refs command
    refs_parser = subparsers.add_parser("compile-refs", help="Compile reference materials")
    refs_parser.add_argument("--config", "-c", required=True, help="Meeting config file")
    refs_parser.add_argument("--project-dir", help="Project directory to scan")
    refs_parser.add_argument("--output", "-o", required=True, help="Output file path")

    # generate-agenda command
    agenda_parser = subparsers.add_parser("generate-agenda", help="Generate meeting agenda")
    agenda_parser.add_argument("--config", "-c", required=True, help="Meeting config file")
    agenda_parser.add_argument("--topics", help="Comma-separated agenda topics")
    agenda_parser.add_argument("--durations", help="Comma-separated durations (minutes)")
    agenda_parser.add_argument("--presenters", help="Comma-separated presenter names")
    agenda_parser.add_argument("--output", "-o", required=True, help="Output file path")

    # create-decision-log command
    decision_parser = subparsers.add_parser("create-decision-log", help="Create decision log template")
    decision_parser.add_argument("--config", "-c", required=True, help="Meeting config file")
    decision_parser.add_argument("--output", "-o", required=True, help="Output file path")

    # create-action-items command
    action_parser = subparsers.add_parser("create-action-items", help="Create action items template")
    action_parser.add_argument("--config", "-c", required=True, help="Meeting config file")
    action_parser.add_argument("--output", "-o", required=True, help="Output file path")

    # package command
    package_parser = subparsers.add_parser("package", help="Package all meeting assets")
    package_parser.add_argument("--config", "-c", required=True, help="Meeting config file")
    package_parser.add_argument("--agenda", help="Agenda file path")
    package_parser.add_argument("--references", help="References index file path")
    package_parser.add_argument("--decision-log", help="Decision log file path")
    package_parser.add_argument("--action-items", help="Action items file path")
    package_parser.add_argument("--output-dir", "-o", required=True, help="Output directory")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    command_handlers = {
        "init": init_meeting,
        "compile-refs": compile_refs,
        "generate-agenda": generate_agenda,
        "create-decision-log": create_decision_log,
        "create-action-items": create_action_items,
        "package": package_meeting,
    }

    handler = command_handlers.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
