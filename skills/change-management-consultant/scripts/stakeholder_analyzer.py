#!/usr/bin/env python3
"""
Stakeholder Analyzer

Analyzes stakeholder data from CSV and generates engagement strategies.
Produces stakeholder maps, priority matrices, and action plans.
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Stakeholder:
    """Represents a stakeholder with analysis attributes."""

    name: str
    role: str
    department: str
    power: int  # 1-5 scale
    interest: int  # 1-5 scale
    impact: int  # 1-5 scale
    attitude: int  # 1=Resistor, 2=Skeptic, 3=Neutral, 4=Supporter, 5=Champion

    def __post_init__(self):
        """Validate scores."""
        for attr in ["power", "interest", "impact", "attitude"]:
            value = getattr(self, attr)
            if not 1 <= value <= 5:
                raise ValueError(f"{attr} must be between 1 and 5, got {value}")

    @property
    def quadrant(self) -> str:
        """Determine Power-Interest quadrant."""
        if self.power >= 3 and self.interest >= 3:
            return "Manage Closely"
        elif self.power >= 3 and self.interest < 3:
            return "Keep Satisfied"
        elif self.power < 3 and self.interest >= 3:
            return "Keep Informed"
        else:
            return "Monitor"

    @property
    def attitude_label(self) -> str:
        """Get attitude label."""
        labels = {
            1: "Resistor",
            2: "Skeptic",
            3: "Neutral",
            4: "Supporter",
            5: "Champion",
        }
        return labels.get(self.attitude, "Unknown")

    @property
    def priority_score(self) -> int:
        """Calculate engagement priority score."""
        # Higher power + interest + impact = higher priority
        # Lower attitude (resistors) also increases priority
        return self.power + self.interest + self.impact + (6 - self.attitude)

    def get_engagement_strategy(self) -> list[str]:
        """Get recommended engagement strategies."""
        strategies = []

        # Quadrant-based strategies
        if self.quadrant == "Manage Closely":
            strategies.append("Regular 1:1 meetings and direct engagement")
            strategies.append("Involve in key decisions and planning")
        elif self.quadrant == "Keep Satisfied":
            strategies.append("Periodic updates and status reports")
            strategies.append("Escalate issues proactively")
        elif self.quadrant == "Keep Informed":
            strategies.append("Regular communication through newsletters/emails")
            strategies.append("Include in town halls and group meetings")
        else:
            strategies.append("Minimal effort - periodic monitoring")

        # Attitude-based strategies
        if self.attitude <= 2:  # Resistor or Skeptic
            strategies.append("Address concerns through direct dialogue")
            strategies.append("Provide evidence and data to address objections")
            strategies.append("Connect with supporters who can influence")
        elif self.attitude >= 4:  # Supporter or Champion
            strategies.append("Leverage as change advocate")
            strategies.append("Ask to influence others")

        return strategies


def load_stakeholders_from_csv(filepath: str) -> list[Stakeholder]:
    """Load stakeholder data from CSV file."""
    stakeholders = []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                stakeholder = Stakeholder(
                    name=row.get("name", row.get("Name", "")),
                    role=row.get("role", row.get("Role", "")),
                    department=row.get("department", row.get("Department", "")),
                    power=int(row.get("power", row.get("Power", 3))),
                    interest=int(row.get("interest", row.get("Interest", 3))),
                    impact=int(row.get("impact", row.get("Impact", 3))),
                    attitude=int(row.get("attitude", row.get("Attitude", 3))),
                )
                stakeholders.append(stakeholder)
            except (ValueError, KeyError) as e:
                print(f"Warning: Skipping row due to error: {e}", file=sys.stderr)

    return stakeholders


def generate_sample_csv() -> str:
    """Generate sample CSV content."""
    return """name,role,department,power,interest,impact,attitude
John Smith,CEO,Executive,5,3,5,5
Jane Doe,CIO,IT,5,5,5,4
Bob Wilson,Department Manager,Sales,3,4,4,2
Alice Brown,Team Lead,Operations,2,5,3,3
Charlie Davis,End User,Finance,1,4,2,3
"""


def generate_report(stakeholders: list[Stakeholder], output_format: str = "markdown") -> str:
    """Generate stakeholder analysis report."""
    if not stakeholders:
        return "No stakeholders to analyze."

    # Sort by priority
    sorted_stakeholders = sorted(stakeholders, key=lambda s: s.priority_score, reverse=True)

    # Group by quadrant
    quadrants = {
        "Manage Closely": [],
        "Keep Satisfied": [],
        "Keep Informed": [],
        "Monitor": [],
    }
    for s in stakeholders:
        quadrants[s.quadrant].append(s)

    # Count by attitude
    attitude_counts = {}
    for s in stakeholders:
        label = s.attitude_label
        attitude_counts[label] = attitude_counts.get(label, 0) + 1

    if output_format == "json":
        return json.dumps(
            {
                "summary": {
                    "total_stakeholders": len(stakeholders),
                    "attitude_distribution": attitude_counts,
                    "quadrant_distribution": {q: len(s) for q, s in quadrants.items()},
                },
                "stakeholders": [
                    {
                        "name": s.name,
                        "role": s.role,
                        "department": s.department,
                        "power": s.power,
                        "interest": s.interest,
                        "impact": s.impact,
                        "attitude": s.attitude,
                        "attitude_label": s.attitude_label,
                        "quadrant": s.quadrant,
                        "priority_score": s.priority_score,
                        "engagement_strategies": s.get_engagement_strategy(),
                    }
                    for s in sorted_stakeholders
                ],
            },
            indent=2,
            ensure_ascii=False,
        )

    # Markdown format
    report = f"""# Stakeholder Analysis Report

## Summary

- **Total Stakeholders**: {len(stakeholders)}
- **Attitude Distribution**:
"""

    for label in ["Champion", "Supporter", "Neutral", "Skeptic", "Resistor"]:
        count = attitude_counts.get(label, 0)
        if count > 0:
            emoji = {"Champion": "🌟", "Supporter": "✅", "Neutral": "🟡", "Skeptic": "⚠️", "Resistor": "🔴"}.get(
                label, ""
            )
            report += f"  - {emoji} {label}: {count}\n"

    report += """
---

## Power-Interest Matrix

### High Power, High Interest (Manage Closely)
"""

    for s in quadrants["Manage Closely"]:
        report += f"- **{s.name}** ({s.role}, {s.department}) - {s.attitude_label}\n"

    if not quadrants["Manage Closely"]:
        report += "_No stakeholders in this quadrant_\n"

    report += """
### High Power, Low Interest (Keep Satisfied)
"""

    for s in quadrants["Keep Satisfied"]:
        report += f"- **{s.name}** ({s.role}, {s.department}) - {s.attitude_label}\n"

    if not quadrants["Keep Satisfied"]:
        report += "_No stakeholders in this quadrant_\n"

    report += """
### Low Power, High Interest (Keep Informed)
"""

    for s in quadrants["Keep Informed"]:
        report += f"- **{s.name}** ({s.role}, {s.department}) - {s.attitude_label}\n"

    if not quadrants["Keep Informed"]:
        report += "_No stakeholders in this quadrant_\n"

    report += """
### Low Power, Low Interest (Monitor)
"""

    for s in quadrants["Monitor"]:
        report += f"- **{s.name}** ({s.role}, {s.department}) - {s.attitude_label}\n"

    if not quadrants["Monitor"]:
        report += "_No stakeholders in this quadrant_\n"

    report += """
---

## Detailed Stakeholder Analysis

| Name | Role | Dept | Power | Interest | Impact | Attitude | Quadrant | Priority |
|------|------|------|-------|----------|--------|----------|----------|----------|
"""

    for s in sorted_stakeholders:
        report += f"| {s.name} | {s.role} | {s.department} | {s.power} | {s.interest} | {s.impact} | {s.attitude_label} | {s.quadrant} | {s.priority_score} |\n"

    report += """
---

## Engagement Action Plan

### Priority Engagements (Top 5)

"""

    for i, s in enumerate(sorted_stakeholders[:5], 1):
        strategies = s.get_engagement_strategy()
        strat_list = "\n".join(f"   - {st}" for st in strategies[:3])
        report += f"""**{i}. {s.name}** ({s.role})
   - Quadrant: {s.quadrant}
   - Attitude: {s.attitude_label}
   - Strategies:
{strat_list}

"""

    # Risk section for resistors/skeptics
    at_risk = [s for s in stakeholders if s.attitude <= 2]
    if at_risk:
        report += """---

## Risk: Stakeholders Requiring Conversion

"""
        for s in at_risk:
            report += f"""### {s.name} ({s.attitude_label})
- **Role**: {s.role}, {s.department}
- **Risk Level**: {"High" if s.power >= 3 else "Medium"}
- **Recommended Actions**:
"""
            for st in s.get_engagement_strategy():
                report += f"  - {st}\n"
            report += "\n"

    return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Stakeholder Analyzer for Change Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
CSV Format:
  name,role,department,power,interest,impact,attitude
  John Smith,CEO,Executive,5,3,5,5

Scales (1-5):
  Power: Influence over change success
  Interest: Level of concern about change
  Impact: How much change affects them
  Attitude: 1=Resistor, 2=Skeptic, 3=Neutral, 4=Supporter, 5=Champion

Examples:
  %(prog)s --input stakeholders.csv
  %(prog)s --input stakeholders.csv --output analysis.md
  %(prog)s --sample  # Generate sample CSV
        """,
    )

    parser.add_argument("--input", "-i", help="Input CSV file path")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument(
        "--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format (default: markdown)"
    )
    parser.add_argument("--sample", action="store_true", help="Generate sample CSV content")

    args = parser.parse_args()

    if args.sample:
        print(generate_sample_csv())
        return

    if not args.input:
        parser.error("--input is required (or use --sample to generate sample CSV)")

    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        stakeholders = load_stakeholders_from_csv(args.input)
    except Exception as e:
        print(f"Error loading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(stakeholders, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
