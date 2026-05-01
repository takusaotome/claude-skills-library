#!/usr/bin/env python3
"""
ISO Gap Analysis Tool

Generates gap analysis reports and calculates maturity scores for ISO standards.
Supports ISO 9001, ISO 27001, ISO 22301, ISO 45001, and ISO 14001.
"""

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class ISOStandard(Enum):
    """Supported ISO standards."""

    ISO_9001 = "ISO 9001:2015"
    ISO_27001 = "ISO 27001:2022"
    ISO_22301 = "ISO 22301:2019"
    ISO_45001 = "ISO 45001:2018"
    ISO_14001 = "ISO 14001:2015"


# High-Level Structure clauses common to all ISO management system standards
HLS_CLAUSES = {
    "4": {
        "title": "Context of the Organization",
        "subclauses": {
            "4.1": "Understanding the organization and its context",
            "4.2": "Understanding the needs and expectations of interested parties",
            "4.3": "Determining the scope of the management system",
            "4.4": "Management system and its processes",
        },
    },
    "5": {
        "title": "Leadership",
        "subclauses": {
            "5.1": "Leadership and commitment",
            "5.2": "Policy",
            "5.3": "Organizational roles, responsibilities and authorities",
        },
    },
    "6": {
        "title": "Planning",
        "subclauses": {
            "6.1": "Actions to address risks and opportunities",
            "6.2": "Objectives and planning to achieve them",
            "6.3": "Planning of changes",
        },
    },
    "7": {
        "title": "Support",
        "subclauses": {
            "7.1": "Resources",
            "7.2": "Competence",
            "7.3": "Awareness",
            "7.4": "Communication",
            "7.5": "Documented information",
        },
    },
    "8": {
        "title": "Operation",
        "subclauses": {
            "8.1": "Operational planning and control",
        },
    },
    "9": {
        "title": "Performance Evaluation",
        "subclauses": {
            "9.1": "Monitoring, measurement, analysis and evaluation",
            "9.2": "Internal audit",
            "9.3": "Management review",
        },
    },
    "10": {
        "title": "Improvement",
        "subclauses": {
            "10.1": "General",
            "10.2": "Nonconformity and corrective action",
            "10.3": "Continual improvement",
        },
    },
}


@dataclass
class ClauseAssessment:
    """Assessment result for a single clause."""

    clause_id: str
    clause_title: str
    score: int  # 0-5
    current_state: str
    gap_description: str
    evidence_reviewed: str
    recommended_actions: str
    priority: str  # High, Medium, Low
    effort_weeks: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class GapAnalysisReport:
    """Complete gap analysis report."""

    organization: str
    standard: str
    assessor: str
    assessment_date: str
    scope: str
    assessments: list[ClauseAssessment] = field(default_factory=list)

    @property
    def overall_maturity(self) -> float:
        """Calculate overall maturity score."""
        applicable = [a for a in self.assessments if a.score > 0]
        if not applicable:
            return 0.0
        return sum(a.score for a in applicable) / len(applicable)

    @property
    def compliance_summary(self) -> dict:
        """Count assessments by compliance level."""
        summary = {
            "fully_compliant": 0,
            "mostly_compliant": 0,
            "partially_compliant": 0,
            "minimally_compliant": 0,
            "not_compliant": 0,
            "not_applicable": 0,
        }
        for a in self.assessments:
            if a.score == 5:
                summary["fully_compliant"] += 1
            elif a.score == 4:
                summary["mostly_compliant"] += 1
            elif a.score == 3:
                summary["partially_compliant"] += 1
            elif a.score == 2:
                summary["minimally_compliant"] += 1
            elif a.score == 1:
                summary["not_compliant"] += 1
            else:
                summary["not_applicable"] += 1
        return summary

    @property
    def high_priority_gaps(self) -> list[ClauseAssessment]:
        """Get high priority gaps."""
        return [a for a in self.assessments if a.priority == "High" and a.score < 4]

    @property
    def estimated_timeline_months(self) -> int:
        """Estimate implementation timeline based on maturity."""
        maturity = self.overall_maturity
        if maturity >= 4.0:
            return 6
        elif maturity >= 3.0:
            return 9
        elif maturity >= 2.0:
            return 12
        else:
            return 18

    def to_dict(self) -> dict:
        return {
            "organization": self.organization,
            "standard": self.standard,
            "assessor": self.assessor,
            "assessment_date": self.assessment_date,
            "scope": self.scope,
            "overall_maturity": round(self.overall_maturity, 2),
            "compliance_summary": self.compliance_summary,
            "estimated_timeline_months": self.estimated_timeline_months,
            "assessments": [a.to_dict() for a in self.assessments],
        }


def generate_blank_template(standard: str, output_path: Path) -> None:
    """Generate a blank CSV template for gap analysis input."""
    clauses = []
    for clause_num, clause_info in HLS_CLAUSES.items():
        for subclause_id, subclause_title in clause_info["subclauses"].items():
            clauses.append(
                {
                    "clause_id": subclause_id,
                    "clause_title": subclause_title,
                    "score": "",
                    "current_state": "",
                    "gap_description": "",
                    "evidence_reviewed": "",
                    "recommended_actions": "",
                    "priority": "",
                    "effort_weeks": "",
                }
            )

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=clauses[0].keys())
        writer.writeheader()
        writer.writerows(clauses)

    print(f"Template generated: {output_path}")
    print(f"Standard: {standard}")
    print(f"Clauses: {len(clauses)}")


def load_assessments_from_csv(csv_path: Path) -> list[ClauseAssessment]:
    """Load assessment data from CSV file."""
    assessments = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("score", "").strip():
                assessment = ClauseAssessment(
                    clause_id=row["clause_id"],
                    clause_title=row["clause_title"],
                    score=int(row["score"]),
                    current_state=row.get("current_state", ""),
                    gap_description=row.get("gap_description", ""),
                    evidence_reviewed=row.get("evidence_reviewed", ""),
                    recommended_actions=row.get("recommended_actions", ""),
                    priority=row.get("priority", "Medium"),
                    effort_weeks=int(row.get("effort_weeks", 0) or 0),
                )
                assessments.append(assessment)
    return assessments


def generate_markdown_report(report: GapAnalysisReport) -> str:
    """Generate markdown report from gap analysis."""
    summary = report.compliance_summary
    maturity = report.overall_maturity

    md = f"""# {report.standard} Gap Analysis Report

## Executive Summary

| Attribute | Value |
|-----------|-------|
| Organization | {report.organization} |
| Standard | {report.standard} |
| Assessor | {report.assessor} |
| Date | {report.assessment_date} |
| Scope | {report.scope} |

### Overall Assessment

| Metric | Value |
|--------|-------|
| **Maturity Score** | **{maturity:.2f}/5.0** |
| Fully Compliant (5) | {summary["fully_compliant"]} clauses |
| Mostly Compliant (4) | {summary["mostly_compliant"]} clauses |
| Partially Compliant (3) | {summary["partially_compliant"]} clauses |
| Minimally Compliant (2) | {summary["minimally_compliant"]} clauses |
| Not Compliant (1) | {summary["not_compliant"]} clauses |
| Not Applicable (0) | {summary["not_applicable"]} clauses |
| **Estimated Timeline** | **{report.estimated_timeline_months} months** |

### Maturity Interpretation

"""
    if maturity >= 4.5:
        md += "> **Ready for certification** - Minor refinements may be needed.\n"
    elif maturity >= 3.5:
        md += "> **Minor improvements needed** - Address gaps before audit.\n"
    elif maturity >= 2.5:
        md += "> **Significant work required** - Plan systematic implementation.\n"
    elif maturity >= 1.5:
        md += "> **Major implementation needed** - Establish foundational processes.\n"
    else:
        md += "> **Starting from scratch** - Comprehensive implementation required.\n"

    md += """
---

## High Priority Gaps

"""
    high_priority = report.high_priority_gaps
    if high_priority:
        md += "| Clause | Title | Score | Gap | Effort |\n"
        md += "|--------|-------|-------|-----|--------|\n"
        for a in high_priority:
            md += f"| {a.clause_id} | {a.clause_title} | {a.score}/5 | {a.gap_description[:50]}... | {a.effort_weeks}w |\n"
    else:
        md += "_No high priority gaps identified._\n"

    md += """
---

## Clause-by-Clause Assessment

"""
    current_main_clause = ""
    for a in report.assessments:
        main_clause = a.clause_id.split(".")[0]
        if main_clause != current_main_clause:
            current_main_clause = main_clause
            if main_clause in HLS_CLAUSES:
                md += f"\n### Clause {main_clause}: {HLS_CLAUSES[main_clause]['title']}\n\n"

        score_indicator = "🟢" if a.score >= 4 else "🟡" if a.score >= 3 else "🔴"
        md += f"""#### {a.clause_id} {a.clause_title} {score_indicator}

- **Score**: {a.score}/5 ({_score_label(a.score)})
- **Priority**: {a.priority}
- **Current State**: {a.current_state or "Not assessed"}
- **Gap**: {a.gap_description or "None identified"}
- **Evidence Reviewed**: {a.evidence_reviewed or "None"}
- **Recommended Actions**: {a.recommended_actions or "None"}
- **Estimated Effort**: {a.effort_weeks} weeks

"""

    md += """---

## Action Plan Summary

| Priority | Clause | Action | Owner | Effort |
|----------|--------|--------|-------|--------|
"""
    for a in sorted(
        report.assessments,
        key=lambda x: (0 if x.priority == "High" else 1 if x.priority == "Medium" else 2, -x.effort_weeks),
    ):
        if a.recommended_actions and a.score < 5:
            md += f"| {a.priority} | {a.clause_id} | {a.recommended_actions[:40]}... | TBD | {a.effort_weeks}w |\n"

    md += f"""
---

## Recommendations

1. **Quick Wins**: Address low-effort, high-impact gaps first
2. **Documentation**: Establish document control system early
3. **Training**: Plan awareness training for all staff
4. **Internal Audit**: Conduct internal audits before external certification
5. **Management Review**: Schedule regular management reviews

---

_Report generated: {datetime.now().isoformat()}_
"""
    return md


def _score_label(score: int) -> str:
    """Get human-readable label for score."""
    labels = {
        5: "Fully Compliant",
        4: "Mostly Compliant",
        3: "Partially Compliant",
        2: "Minimally Compliant",
        1: "Not Compliant",
        0: "Not Applicable",
    }
    return labels.get(score, "Unknown")


def main():
    parser = argparse.ArgumentParser(
        description="ISO Gap Analysis Tool - Generate templates and reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate blank template for ISO 27001
  python gap_analysis.py template --standard ISO_27001 --output gap_template.csv

  # Generate report from completed assessment
  python gap_analysis.py report --input completed_assessment.csv \\
    --standard ISO_27001 --organization "ACME Corp" \\
    --assessor "John Smith" --scope "IT Department" \\
    --output gap_report.md

  # Output JSON format
  python gap_analysis.py report --input assessment.csv --format json --output report.json
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Template command
    template_parser = subparsers.add_parser("template", help="Generate blank assessment template")
    template_parser.add_argument(
        "--standard",
        "-s",
        choices=[s.name for s in ISOStandard],
        default="ISO_9001",
        help="ISO standard (default: ISO_9001)",
    )
    template_parser.add_argument(
        "--output", "-o", type=Path, default=Path("gap_analysis_template.csv"), help="Output file path"
    )

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate gap analysis report")
    report_parser.add_argument("--input", "-i", type=Path, required=True, help="Input CSV file with assessment data")
    report_parser.add_argument(
        "--standard",
        "-s",
        choices=[s.name for s in ISOStandard],
        default="ISO_9001",
        help="ISO standard (default: ISO_9001)",
    )
    report_parser.add_argument("--organization", "-org", default="Organization Name", help="Organization name")
    report_parser.add_argument("--assessor", "-a", default="Assessor Name", help="Assessor name")
    report_parser.add_argument("--scope", default="Full organization", help="Assessment scope")
    report_parser.add_argument("--output", "-o", type=Path, help="Output file path (default: stdout)")
    report_parser.add_argument(
        "--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format (default: markdown)"
    )

    args = parser.parse_args()

    if args.command == "template":
        standard_value = ISOStandard[args.standard].value
        generate_blank_template(standard_value, args.output)

    elif args.command == "report":
        if not args.input.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        assessments = load_assessments_from_csv(args.input)
        standard_value = ISOStandard[args.standard].value

        report = GapAnalysisReport(
            organization=args.organization,
            standard=standard_value,
            assessor=args.assessor,
            assessment_date=datetime.now().strftime("%Y-%m-%d"),
            scope=args.scope,
            assessments=assessments,
        )

        if args.format == "json":
            output = json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
        else:
            output = generate_markdown_report(report)

        if args.output:
            args.output.write_text(output, encoding="utf-8")
            print(f"Report generated: {args.output}")
        else:
            print(output)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
