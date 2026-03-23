#!/usr/bin/env python3
"""
Generate traceability reports from artifacts and links.

Usage:
    python3 generate_traceability_report.py --artifacts artifacts.json --links links.json --output report.md
    python3 generate_traceability_report.py --artifacts artifacts.json --links links.json --output report.json --format json
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional


class TraceabilityReportGenerator:
    """Generate traceability reports from artifacts and links."""

    def __init__(self, artifacts: dict, links: dict):
        self.artifacts = artifacts
        self.links = links.get("links", [])
        self._build_indices()

    def _build_indices(self):
        """Build indices for fast lookup."""
        # Index artifacts by type and ID
        self.artifact_index = {
            "meeting": {},
            "wbs_task": {},
            "requirement": {},
            "decision": {},
            "action_item": {},
        }

        for meeting in self.artifacts.get("meetings", []):
            self.artifact_index["meeting"][meeting.get("id")] = meeting
            for ai in meeting.get("action_items", []):
                self.artifact_index["action_item"][ai.get("id")] = ai
            for dec in meeting.get("decisions", []):
                self.artifact_index["decision"][dec.get("id")] = dec

        for task in self.artifacts.get("wbs_tasks", []):
            self.artifact_index["wbs_task"][task.get("id")] = task

        for req in self.artifacts.get("requirements", []):
            self.artifact_index["requirement"][req.get("id")] = req

        for dec in self.artifacts.get("decisions", []):
            self.artifact_index["decision"][dec.get("id")] = dec

        # Index links by source and target
        self.links_by_source = defaultdict(list)
        self.links_by_target = defaultdict(list)

        for link in self.links:
            source_key = (link["source_type"], link["source_id"])
            target_key = (link["target_type"], link["target_id"])
            self.links_by_source[source_key].append(link)
            self.links_by_target[target_key].append(link)

    def _get_artifact(self, artifact_type: str, artifact_id: str) -> Optional[dict]:
        """Get artifact by type and ID."""
        return self.artifact_index.get(artifact_type, {}).get(artifact_id)

    def _get_linked_ids(self, source_type: str, source_id: str) -> list[tuple[str, str]]:
        """Get IDs of artifacts linked from a source."""
        key = (source_type, source_id)
        return [(l["target_type"], l["target_id"]) for l in self.links_by_source.get(key, [])]

    def _get_linked_from_ids(self, target_type: str, target_id: str) -> list[tuple[str, str]]:
        """Get IDs of artifacts linking to a target."""
        key = (target_type, target_id)
        return [(l["source_type"], l["source_id"]) for l in self.links_by_target.get(key, [])]

    def _count_by_type(self) -> dict[str, dict]:
        """Count artifacts by type with linked/orphan status."""
        counts = {}

        for artifact_type, artifacts in [
            ("requirement", self.artifacts.get("requirements", [])),
            ("wbs_task", self.artifacts.get("wbs_tasks", [])),
            ("decision", self.artifacts.get("decisions", [])),
        ]:
            total = len(artifacts)
            linked = sum(
                1
                for a in artifacts
                if self.links_by_source.get((artifact_type, a.get("id")))
                or self.links_by_target.get((artifact_type, a.get("id")))
            )
            counts[artifact_type] = {
                "total": total,
                "linked": linked,
                "orphaned": total - linked,
            }

        # Count action items from meetings
        action_items = []
        for meeting in self.artifacts.get("meetings", []):
            action_items.extend(meeting.get("action_items", []))
        total_ai = len(action_items)
        linked_ai = sum(1 for ai in action_items if self.links_by_source.get(("action_item", ai.get("id"))))
        counts["action_item"] = {
            "total": total_ai,
            "linked": linked_ai,
            "orphaned": total_ai - linked_ai,
        }

        return counts

    def _find_orphans(self) -> dict[str, list]:
        """Find orphaned artifacts (no links)."""
        orphans = defaultdict(list)

        # Requirements without implementing tasks
        for req in self.artifacts.get("requirements", []):
            req_id = req.get("id")
            if not self.links_by_source.get(("requirement", req_id)):
                orphans["requirements_no_task"].append(req)

        # WBS tasks without requirements
        for task in self.artifacts.get("wbs_tasks", []):
            task_id = task.get("id")
            if not self.links_by_target.get(("wbs_task", task_id)):
                orphans["tasks_no_requirement"].append(task)

        # Decisions without meeting documentation
        for dec in self.artifacts.get("decisions", []):
            dec_id = dec.get("id")
            # Check if decision is from a meeting or standalone
            is_from_meeting = any(
                dec_id in [d.get("id") for d in m.get("decisions", [])] for m in self.artifacts.get("meetings", [])
            )
            if not is_from_meeting:
                orphans["decisions_no_meeting"].append(dec)

        # Action items without task mapping
        for meeting in self.artifacts.get("meetings", []):
            for ai in meeting.get("action_items", []):
                ai_id = ai.get("id")
                if not self.links_by_source.get(("action_item", ai_id)):
                    orphans["action_items_no_task"].append(
                        {
                            **ai,
                            "meeting_id": meeting.get("id"),
                        }
                    )

        return dict(orphans)

    def generate_json_report(self) -> dict:
        """Generate traceability report in JSON format."""
        counts = self._count_by_type()
        orphans = self._find_orphans()

        # Build traceability matrix
        req_to_task = []
        for req in self.artifacts.get("requirements", []):
            req_id = req.get("id")
            linked_tasks = [
                link["target_id"]
                for link in self.links_by_source.get(("requirement", req_id), [])
                if link["target_type"] == "wbs_task"
            ]
            req_to_task.append(
                {
                    "requirement_id": req_id,
                    "description": req.get("description", "")[:100],
                    "linked_tasks": linked_tasks,
                    "status": "linked" if linked_tasks else "orphaned",
                }
            )

        dec_to_req = []
        all_decisions = list(self.artifacts.get("decisions", []))
        for meeting in self.artifacts.get("meetings", []):
            for dec in meeting.get("decisions", []):
                dec["meeting_id"] = meeting.get("id")
                all_decisions.append(dec)

        for dec in all_decisions:
            dec_id = dec.get("id")
            linked_reqs = [
                link["target_id"]
                for link in self.links_by_source.get(("decision", dec_id), [])
                if link["target_type"] == "requirement"
            ]
            dec_to_req.append(
                {
                    "decision_id": dec_id,
                    "meeting_id": dec.get("meeting_id"),
                    "description": dec.get("description", "")[:100],
                    "linked_requirements": linked_reqs,
                }
            )

        return {
            "schema_version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "requirements": counts.get("requirement", {}),
                "wbs_tasks": counts.get("wbs_task", {}),
                "decisions": counts.get("decision", {}),
                "action_items": counts.get("action_item", {}),
            },
            "traceability_matrix": {
                "requirements_to_tasks": req_to_task,
                "decisions_to_requirements": dec_to_req,
            },
            "orphans": {
                "requirements_without_tasks": [
                    {"id": r.get("id"), "description": r.get("description", "")[:100]}
                    for r in orphans.get("requirements_no_task", [])
                ],
                "tasks_without_requirements": [
                    {"id": t.get("id"), "name": t.get("name", "")} for t in orphans.get("tasks_no_requirement", [])
                ],
                "decisions_without_meetings": [
                    {"id": d.get("id"), "description": d.get("description", "")[:100]}
                    for d in orphans.get("decisions_no_meeting", [])
                ],
                "action_items_without_tasks": [
                    {"id": ai.get("id"), "description": ai.get("description", "")[:100]}
                    for ai in orphans.get("action_items_no_task", [])
                ],
            },
            "links": self.links,
        }

    def generate_markdown_report(self) -> str:
        """Generate traceability report in Markdown format."""
        counts = self._count_by_type()
        orphans = self._find_orphans()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            "# Project Traceability Report",
            "",
            f"Generated: {timestamp}",
            "",
            "## Summary",
            "",
            "| Artifact Type | Count | Linked | Orphaned |",
            "|--------------|-------|--------|----------|",
        ]

        type_names = {
            "requirement": "Requirements",
            "wbs_task": "WBS Tasks",
            "decision": "Decisions",
            "action_item": "Action Items",
        }

        for artifact_type in ["requirement", "wbs_task", "decision", "action_item"]:
            c = counts.get(artifact_type, {"total": 0, "linked": 0, "orphaned": 0})
            lines.append(f"| {type_names[artifact_type]} | {c['total']} | {c['linked']} | {c['orphaned']} |")

        # Traceability Matrix - Requirements to Tasks
        lines.extend(
            [
                "",
                "## Traceability Matrix",
                "",
                "### Requirements → WBS Tasks",
                "",
                "| Requirement | Description | WBS Task(s) | Status |",
                "|-------------|-------------|-------------|--------|",
            ]
        )

        for req in self.artifacts.get("requirements", []):
            req_id = req.get("id")
            desc = req.get("description", "")[:50]
            linked_tasks = [
                link["target_id"]
                for link in self.links_by_source.get(("requirement", req_id), [])
                if link["target_type"] == "wbs_task"
            ]
            tasks_str = ", ".join(linked_tasks) if linked_tasks else "-"
            status = "Linked" if linked_tasks else "Orphaned"
            lines.append(f"| {req_id} | {desc} | {tasks_str} | {status} |")

        # Meeting Decisions to Requirements
        lines.extend(
            [
                "",
                "### Meeting Decisions → Requirements",
                "",
                "| Decision | Meeting | Requirement(s) |",
                "|----------|---------|----------------|",
            ]
        )

        for meeting in self.artifacts.get("meetings", []):
            meeting_id = meeting.get("id")
            for dec in meeting.get("decisions", []):
                dec_id = dec.get("id")
                linked_reqs = [
                    link["target_id"]
                    for link in self.links_by_source.get(("decision", dec_id), [])
                    if link["target_type"] == "requirement"
                ]
                reqs_str = ", ".join(linked_reqs) if linked_reqs else "-"
                lines.append(f"| {dec_id} | {meeting_id} | {reqs_str} |")

        # Link Details
        lines.extend(
            [
                "",
                "### Link Details",
                "",
                "| Source | Target | Type | Confidence | Reason |",
                "|--------|--------|------|------------|--------|",
            ]
        )

        for link in sorted(self.links, key=lambda x: -x.get("confidence", 0)):
            source = f"{link['source_type']}:{link['source_id']}"
            target = f"{link['target_type']}:{link['target_id']}"
            lines.append(
                f"| {source} | {target} | {link['link_type']} | "
                f"{link['confidence']:.2f} | {link['match_reason'][:40]} |"
            )

        # Gaps and Orphans
        lines.extend(
            [
                "",
                "## Gaps and Orphans",
                "",
            ]
        )

        # Orphaned Requirements
        orphaned_reqs = orphans.get("requirements_no_task", [])
        if orphaned_reqs:
            lines.extend(
                [
                    "### Orphaned Requirements (no implementing task)",
                    "",
                ]
            )
            for req in orphaned_reqs:
                lines.append(f"- **{req.get('id')}**: {req.get('description', '')[:80]}")
            lines.append("")
        else:
            lines.extend(
                [
                    "### Orphaned Requirements",
                    "",
                    "✓ All requirements have implementing tasks.",
                    "",
                ]
            )

        # Orphaned Tasks
        orphaned_tasks = orphans.get("tasks_no_requirement", [])
        if orphaned_tasks:
            lines.extend(
                [
                    "### Orphaned WBS Tasks (no source requirement)",
                    "",
                ]
            )
            for task in orphaned_tasks:
                lines.append(f"- **{task.get('id')}**: {task.get('name', '')}")
            lines.append("")
        else:
            lines.extend(
                [
                    "### Orphaned WBS Tasks",
                    "",
                    "✓ All WBS tasks trace to requirements.",
                    "",
                ]
            )

        # Orphaned Action Items
        orphaned_ai = orphans.get("action_items_no_task", [])
        if orphaned_ai:
            lines.extend(
                [
                    "### Orphaned Action Items (no task mapping)",
                    "",
                ]
            )
            for ai in orphaned_ai:
                lines.append(
                    f"- **{ai.get('id')}** (from {ai.get('meeting_id', 'unknown')}): {ai.get('description', '')[:60]}"
                )
            lines.append("")
        else:
            lines.extend(
                [
                    "### Orphaned Action Items",
                    "",
                    "✓ All action items map to WBS tasks.",
                    "",
                ]
            )

        # Coverage Statistics
        total_reqs = counts.get("requirement", {}).get("total", 0)
        linked_reqs = counts.get("requirement", {}).get("linked", 0)
        req_coverage = (linked_reqs / total_reqs * 100) if total_reqs > 0 else 0

        total_tasks = counts.get("wbs_task", {}).get("total", 0)
        linked_tasks = counts.get("wbs_task", {}).get("linked", 0)
        task_coverage = (linked_tasks / total_tasks * 100) if total_tasks > 0 else 0

        lines.extend(
            [
                "## Coverage Statistics",
                "",
                f"- **Requirement Coverage**: {req_coverage:.1f}% ({linked_reqs}/{total_reqs})",
                f"- **Task Traceability**: {task_coverage:.1f}% ({linked_tasks}/{total_tasks})",
                f"- **Total Links Created**: {len(self.links)}",
                "",
            ]
        )

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate traceability reports from artifacts and links")
    parser.add_argument(
        "--artifacts",
        type=Path,
        required=True,
        help="Path to artifacts JSON file",
    )
    parser.add_argument(
        "--links",
        type=Path,
        required=True,
        help="Path to links JSON file",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("traceability_report.md"),
        help="Output file path",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format",
    )

    args = parser.parse_args()

    if not args.artifacts.exists():
        print(f"Error: Artifacts file not found: {args.artifacts}", file=sys.stderr)
        sys.exit(1)

    if not args.links.exists():
        print(f"Error: Links file not found: {args.links}", file=sys.stderr)
        sys.exit(1)

    # Load data
    artifacts = json.loads(args.artifacts.read_text(encoding="utf-8"))
    links = json.loads(args.links.read_text(encoding="utf-8"))

    # Generate report
    generator = TraceabilityReportGenerator(
        artifacts.get("artifacts", artifacts),
        links,
    )

    if args.format == "json":
        report = generator.generate_json_report()
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        report = generator.generate_markdown_report()
        args.output.write_text(report)

    print(f"Report written to {args.output}")


if __name__ == "__main__":
    main()
