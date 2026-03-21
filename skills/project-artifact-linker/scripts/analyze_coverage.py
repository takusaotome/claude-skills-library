#!/usr/bin/env python3
"""
Analyze traceability coverage and identify gaps in project artifacts.

Usage:
    python3 analyze_coverage.py --artifacts artifacts.json --links links.json --output coverage.json
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional


class CoverageAnalyzer:
    """Analyze traceability coverage and identify gaps."""

    def __init__(self, artifacts: dict, links: list):
        self.artifacts = artifacts
        self.links = links
        self._build_indices()

    def _build_indices(self):
        """Build indices for fast lookup."""
        # Index links by source and target
        self.links_by_source = defaultdict(list)
        self.links_by_target = defaultdict(list)

        for link in self.links:
            source_key = (link["source_type"], link["source_id"])
            target_key = (link["target_type"], link["target_id"])
            self.links_by_source[source_key].append(link)
            self.links_by_target[target_key].append(link)

    def _has_outgoing_link(self, artifact_type: str, artifact_id: str) -> bool:
        """Check if artifact has outgoing links."""
        return bool(self.links_by_source.get((artifact_type, artifact_id)))

    def _has_incoming_link(self, artifact_type: str, artifact_id: str) -> bool:
        """Check if artifact has incoming links."""
        return bool(self.links_by_target.get((artifact_type, artifact_id)))

    def analyze_requirements_coverage(self) -> dict:
        """Analyze requirement traceability coverage."""
        requirements = self.artifacts.get("requirements", [])
        if not requirements:
            return {
                "total": 0,
                "with_tasks": 0,
                "without_tasks": 0,
                "coverage_percent": 0.0,
                "gaps": [],
            }

        with_tasks = []
        without_tasks = []

        for req in requirements:
            req_id = req.get("id")
            has_task = any(
                link["target_type"] == "wbs_task" for link in self.links_by_source.get(("requirement", req_id), [])
            )
            if has_task:
                with_tasks.append(req_id)
            else:
                without_tasks.append(
                    {
                        "id": req_id,
                        "description": req.get("description", "")[:100],
                        "priority": req.get("priority"),
                        "source_file": req.get("source_file"),
                    }
                )

        total = len(requirements)
        return {
            "total": total,
            "with_tasks": len(with_tasks),
            "without_tasks": len(without_tasks),
            "coverage_percent": round(len(with_tasks) / total * 100, 1) if total > 0 else 0.0,
            "gaps": without_tasks,
        }

    def analyze_task_traceability(self) -> dict:
        """Analyze WBS task traceability (back to requirements)."""
        tasks = self.artifacts.get("wbs_tasks", [])
        if not tasks:
            return {
                "total": 0,
                "with_requirements": 0,
                "without_requirements": 0,
                "traceability_percent": 0.0,
                "gaps": [],
            }

        with_reqs = []
        without_reqs = []

        for task in tasks:
            task_id = task.get("id")
            has_req = any(
                link["source_type"] == "requirement" for link in self.links_by_target.get(("wbs_task", task_id), [])
            )
            if has_req:
                with_reqs.append(task_id)
            else:
                without_reqs.append(
                    {
                        "id": task_id,
                        "name": task.get("name"),
                        "owner": task.get("owner"),
                        "source_file": task.get("source_file"),
                    }
                )

        total = len(tasks)
        return {
            "total": total,
            "with_requirements": len(with_reqs),
            "without_requirements": len(without_reqs),
            "traceability_percent": round(len(with_reqs) / total * 100, 1) if total > 0 else 0.0,
            "gaps": without_reqs,
        }

    def analyze_decision_documentation(self) -> dict:
        """Analyze decision documentation coverage."""
        # Collect all decisions
        standalone_decisions = self.artifacts.get("decisions", [])
        meeting_decisions = []
        for meeting in self.artifacts.get("meetings", []):
            for dec in meeting.get("decisions", []):
                dec["meeting_id"] = meeting.get("id")
                meeting_decisions.append(dec)

        # Check which standalone decisions link to requirements
        linked_decisions = []
        unlinked_decisions = []

        for dec in standalone_decisions:
            dec_id = dec.get("id")
            has_link = bool(self.links_by_source.get(("decision", dec_id)))
            if has_link:
                linked_decisions.append(dec_id)
            else:
                unlinked_decisions.append(
                    {
                        "id": dec_id,
                        "description": dec.get("description", "")[:100],
                        "date": dec.get("date"),
                        "issue": "no_requirement_link",
                    }
                )

        # Check which meeting decisions have requirement links
        for dec in meeting_decisions:
            dec_id = dec.get("id")
            has_req_link = any(
                link["target_type"] == "requirement" for link in self.links_by_source.get(("decision", dec_id), [])
            )
            if has_req_link:
                linked_decisions.append(dec_id)
            else:
                unlinked_decisions.append(
                    {
                        "id": dec_id,
                        "meeting_id": dec.get("meeting_id"),
                        "description": dec.get("description", "")[:100],
                        "issue": "no_requirement_link",
                    }
                )

        total = len(standalone_decisions) + len(meeting_decisions)
        return {
            "total": total,
            "standalone": len(standalone_decisions),
            "from_meetings": len(meeting_decisions),
            "linked_to_requirements": len(linked_decisions),
            "unlinked": len(unlinked_decisions),
            "documentation_percent": round(len(linked_decisions) / total * 100, 1) if total > 0 else 0.0,
            "gaps": unlinked_decisions,
        }

    def analyze_action_item_resolution(self) -> dict:
        """Analyze action item resolution tracking."""
        action_items = []
        for meeting in self.artifacts.get("meetings", []):
            for ai in meeting.get("action_items", []):
                ai["meeting_id"] = meeting.get("id")
                ai["meeting_date"] = meeting.get("date")
                action_items.append(ai)

        if not action_items:
            return {
                "total": 0,
                "mapped_to_tasks": 0,
                "unmapped": 0,
                "resolution_percent": 0.0,
                "gaps": [],
            }

        mapped = []
        unmapped = []

        for ai in action_items:
            ai_id = ai.get("id")
            has_task = any(
                link["target_type"] == "wbs_task" for link in self.links_by_source.get(("action_item", ai_id), [])
            )
            if has_task:
                mapped.append(ai_id)
            else:
                unmapped.append(
                    {
                        "id": ai_id,
                        "description": ai.get("description", "")[:100],
                        "owner": ai.get("owner"),
                        "due_date": ai.get("due_date"),
                        "meeting_id": ai.get("meeting_id"),
                        "meeting_date": ai.get("meeting_date"),
                    }
                )

        total = len(action_items)
        return {
            "total": total,
            "mapped_to_tasks": len(mapped),
            "unmapped": len(unmapped),
            "resolution_percent": round(len(mapped) / total * 100, 1) if total > 0 else 0.0,
            "gaps": unmapped,
        }

    def analyze_link_quality(self) -> dict:
        """Analyze quality of links based on confidence scores."""
        if not self.links:
            return {
                "total_links": 0,
                "high_confidence": 0,
                "medium_confidence": 0,
                "low_confidence": 0,
                "average_confidence": 0.0,
                "low_confidence_links": [],
            }

        high = []  # >= 0.80
        medium = []  # 0.60 - 0.79
        low = []  # < 0.60

        for link in self.links:
            confidence = link.get("confidence", 0)
            if confidence >= 0.80:
                high.append(link)
            elif confidence >= 0.60:
                medium.append(link)
            else:
                low.append(link)

        total = len(self.links)
        avg_conf = sum(l.get("confidence", 0) for l in self.links) / total if total > 0 else 0

        return {
            "total_links": total,
            "high_confidence": len(high),
            "medium_confidence": len(medium),
            "low_confidence": len(low),
            "average_confidence": round(avg_conf, 2),
            "low_confidence_links": [
                {
                    "source": f"{l['source_type']}:{l['source_id']}",
                    "target": f"{l['target_type']}:{l['target_id']}",
                    "confidence": l.get("confidence"),
                    "reason": l.get("match_reason"),
                }
                for l in low
            ],
        }

    def calculate_overall_health(self) -> dict:
        """Calculate overall traceability health score."""
        req_coverage = self.analyze_requirements_coverage()
        task_trace = self.analyze_task_traceability()
        dec_doc = self.analyze_decision_documentation()
        ai_res = self.analyze_action_item_resolution()
        link_quality = self.analyze_link_quality()

        # Weight components
        weights = {
            "requirements": 0.30,
            "tasks": 0.25,
            "decisions": 0.20,
            "action_items": 0.15,
            "link_quality": 0.10,
        }

        scores = {
            "requirements": req_coverage["coverage_percent"],
            "tasks": task_trace["traceability_percent"],
            "decisions": dec_doc["documentation_percent"],
            "action_items": ai_res["resolution_percent"],
            "link_quality": link_quality["average_confidence"] * 100,
        }

        overall = sum(scores[k] * weights[k] for k in weights)

        # Determine health status
        if overall >= 80:
            status = "healthy"
            recommendation = "Traceability is well-maintained. Continue regular reviews."
        elif overall >= 60:
            status = "needs_attention"
            recommendation = "Some gaps exist. Address orphaned artifacts and improve link confidence."
        else:
            status = "critical"
            recommendation = "Significant traceability gaps. Prioritize linking requirements to tasks."

        return {
            "overall_score": round(overall, 1),
            "status": status,
            "recommendation": recommendation,
            "component_scores": scores,
            "weights": weights,
        }

    def generate_report(self) -> dict:
        """Generate comprehensive coverage analysis report."""
        return {
            "schema_version": "1.0",
            "analysis_date": datetime.now().isoformat(),
            "overall_health": self.calculate_overall_health(),
            "requirements_coverage": self.analyze_requirements_coverage(),
            "task_traceability": self.analyze_task_traceability(),
            "decision_documentation": self.analyze_decision_documentation(),
            "action_item_resolution": self.analyze_action_item_resolution(),
            "link_quality": self.analyze_link_quality(),
        }


def main():
    parser = argparse.ArgumentParser(description="Analyze traceability coverage and identify gaps")
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
        default=Path("coverage_analysis.json"),
        help="Output JSON file path",
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

    # Analyze coverage
    analyzer = CoverageAnalyzer(
        artifacts.get("artifacts", artifacts),
        links.get("links", []),
    )

    report = analyzer.generate_report()

    # Write output
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"Coverage analysis written to {args.output}")

    # Print summary
    health = report["overall_health"]
    print(f"\nOverall Health Score: {health['overall_score']}/100 ({health['status']})")
    print(f"Recommendation: {health['recommendation']}")

    print("\nComponent Scores:")
    for component, score in health["component_scores"].items():
        print(f"  {component}: {score:.1f}%")


if __name__ == "__main__":
    main()
