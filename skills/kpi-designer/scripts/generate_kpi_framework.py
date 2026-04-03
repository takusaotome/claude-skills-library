#!/usr/bin/env python3
"""
KPI Framework Generator

Generates KPI framework documents from strategic objectives.
Validates KPIs against SMART criteria.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class IndicatorType(Enum):
    LEADING = "Leading"
    LAGGING = "Lagging"


class SMARTScore(Enum):
    PASS = "Pass"
    PARTIAL = "Partial"
    FAIL = "Fail"


@dataclass
class KPI:
    """Represents a Key Performance Indicator."""

    name: str
    description: str = ""
    formula: str = ""
    owner: str = ""
    indicator_type: IndicatorType = IndicatorType.LAGGING
    current_value: Optional[str] = None
    target_value: Optional[str] = None
    frequency: str = "Monthly"
    data_source: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "formula": self.formula,
            "owner": self.owner,
            "indicator_type": self.indicator_type.value,
            "current_value": self.current_value,
            "target_value": self.target_value,
            "frequency": self.frequency,
            "data_source": self.data_source,
        }


@dataclass
class SMARTValidation:
    """SMART criteria validation result for a KPI."""

    kpi_name: str
    specific: SMARTScore = SMARTScore.FAIL
    measurable: SMARTScore = SMARTScore.FAIL
    achievable: SMARTScore = SMARTScore.FAIL
    relevant: SMARTScore = SMARTScore.FAIL
    time_bound: SMARTScore = SMARTScore.FAIL
    notes: list = field(default_factory=list)

    @property
    def overall_score(self) -> int:
        """Calculate overall SMART score (0-100)."""
        score_map = {SMARTScore.PASS: 20, SMARTScore.PARTIAL: 10, SMARTScore.FAIL: 0}
        return (
            score_map[self.specific]
            + score_map[self.measurable]
            + score_map[self.achievable]
            + score_map[self.relevant]
            + score_map[self.time_bound]
        )

    @property
    def status(self) -> str:
        """Get overall status based on score."""
        score = self.overall_score
        if score >= 80:
            return "Strong"
        elif score >= 60:
            return "Acceptable"
        elif score >= 40:
            return "Needs Improvement"
        else:
            return "Weak"


@dataclass
class KPIFramework:
    """Represents a complete KPI framework."""

    name: str
    objectives: list
    industry: str = "General"
    level: str = "Company"
    strategic_kpis: list = field(default_factory=list)
    tactical_kpis: list = field(default_factory=list)
    operational_kpis: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class KPIFrameworkGenerator:
    """Generates KPI framework documents."""

    # Common KPIs by category
    COMMON_KPIS = {
        "revenue": [
            KPI(
                "Revenue Growth",
                "Year-over-year revenue growth rate",
                "(Current - Previous) / Previous × 100",
                indicator_type=IndicatorType.LAGGING,
            ),
            KPI(
                "Monthly Recurring Revenue (MRR)",
                "Total recurring revenue per month",
                "Sum of all recurring subscription revenue",
                indicator_type=IndicatorType.LAGGING,
            ),
        ],
        "customer": [
            KPI(
                "Net Promoter Score (NPS)",
                "Customer loyalty metric",
                "% Promoters - % Detractors",
                indicator_type=IndicatorType.LEADING,
            ),
            KPI(
                "Customer Churn Rate",
                "Percentage of customers lost",
                "Customers Lost / Starting Customers × 100",
                indicator_type=IndicatorType.LAGGING,
            ),
            KPI(
                "Customer Satisfaction (CSAT)",
                "Satisfaction survey score",
                "Satisfied Responses / Total Responses × 100",
                indicator_type=IndicatorType.LEADING,
            ),
        ],
        "efficiency": [
            KPI(
                "Operating Margin",
                "Operational efficiency",
                "(Revenue - Operating Costs) / Revenue × 100",
                indicator_type=IndicatorType.LAGGING,
            ),
            KPI(
                "Customer Acquisition Cost (CAC)",
                "Cost to acquire a customer",
                "Sales & Marketing Spend / New Customers",
                indicator_type=IndicatorType.LEADING,
            ),
        ],
        "quality": [
            KPI(
                "Defect Rate",
                "Percentage of defective output",
                "Defects / Total Output × 100",
                indicator_type=IndicatorType.LAGGING,
            ),
            KPI(
                "First Time Resolution Rate",
                "Issues resolved on first contact",
                "First Contact Resolutions / Total Issues × 100",
                indicator_type=IndicatorType.LEADING,
            ),
        ],
    }

    def __init__(self, objectives: list, industry: str = "General", level: str = "Company"):
        self.objectives = objectives
        self.industry = industry
        self.level = level

    def _categorize_objective(self, objective: str) -> list:
        """Identify KPI categories based on objective keywords."""
        objective_lower = objective.lower()
        categories = []

        if any(kw in objective_lower for kw in ["revenue", "growth", "sales", "profit"]):
            categories.append("revenue")
        if any(kw in objective_lower for kw in ["customer", "satisfaction", "nps", "churn", "retention"]):
            categories.append("customer")
        if any(kw in objective_lower for kw in ["efficiency", "cost", "reduce", "optimize"]):
            categories.append("efficiency")
        if any(kw in objective_lower for kw in ["quality", "defect", "error", "bug"]):
            categories.append("quality")

        return categories if categories else ["revenue"]  # default to revenue

    def generate_framework(self) -> KPIFramework:
        """Generate a KPI framework from objectives."""
        framework = KPIFramework(
            name=f"{self.industry} KPI Framework",
            objectives=self.objectives,
            industry=self.industry,
            level=self.level,
        )

        # Collect relevant KPIs based on objectives
        selected_kpis = set()
        for objective in self.objectives:
            categories = self._categorize_objective(objective)
            for category in categories:
                for kpi in self.COMMON_KPIS.get(category, []):
                    selected_kpis.add(kpi.name)

        # Distribute KPIs across tiers
        all_kpis = []
        for category_kpis in self.COMMON_KPIS.values():
            for kpi in category_kpis:
                if kpi.name in selected_kpis:
                    all_kpis.append(kpi)

        # Assign to tiers (simplified logic)
        for i, kpi in enumerate(all_kpis):
            if kpi.indicator_type == IndicatorType.LAGGING:
                framework.strategic_kpis.append(kpi)
            elif i % 2 == 0:
                framework.tactical_kpis.append(kpi)
            else:
                framework.operational_kpis.append(kpi)

        return framework

    def to_markdown(self, framework: KPIFramework) -> str:
        """Convert framework to markdown document."""
        lines = [
            f"# KPI Framework: {framework.name}",
            "",
            f"**Industry**: {framework.industry}",
            f"**Level**: {framework.level}",
            f"**Generated**: {framework.created_at[:10]}",
            "",
            "## Strategic Objectives",
            "",
        ]

        for i, obj in enumerate(framework.objectives, 1):
            lines.append(f"{i}. {obj}")

        lines.extend(["", "---", "", "## KPI Hierarchy", ""])

        # Strategic KPIs
        lines.extend(["### Tier 1: Strategic KPIs (Executive)", ""])
        if framework.strategic_kpis:
            lines.append("| KPI | Type | Formula | Frequency |")
            lines.append("|-----|------|---------|-----------|")
            for kpi in framework.strategic_kpis:
                lines.append(f"| {kpi.name} | {kpi.indicator_type.value} | {kpi.formula} | {kpi.frequency} |")
        else:
            lines.append("*No strategic KPIs identified. Add based on high-level objectives.*")

        lines.append("")

        # Tactical KPIs
        lines.extend(["### Tier 2: Tactical KPIs (Managers)", ""])
        if framework.tactical_kpis:
            lines.append("| KPI | Type | Formula | Frequency |")
            lines.append("|-----|------|---------|-----------|")
            for kpi in framework.tactical_kpis:
                lines.append(f"| {kpi.name} | {kpi.indicator_type.value} | {kpi.formula} | {kpi.frequency} |")
        else:
            lines.append("*No tactical KPIs identified. Add department-level metrics.*")

        lines.append("")

        # Operational KPIs
        lines.extend(["### Tier 3: Operational KPIs (Teams)", ""])
        if framework.operational_kpis:
            lines.append("| KPI | Type | Formula | Frequency |")
            lines.append("|-----|------|---------|-----------|")
            for kpi in framework.operational_kpis:
                lines.append(f"| {kpi.name} | {kpi.indicator_type.value} | {kpi.formula} | Weekly |")
        else:
            lines.append("*No operational KPIs identified. Add team-level metrics.*")

        lines.extend(
            [
                "",
                "---",
                "",
                "## KPI Definitions",
                "",
            ]
        )

        all_kpis = framework.strategic_kpis + framework.tactical_kpis + framework.operational_kpis
        for kpi in all_kpis:
            lines.extend(
                [
                    f"### {kpi.name}",
                    "",
                    f"**Description**: {kpi.description}",
                    "",
                    f"**Formula**: `{kpi.formula}`",
                    "",
                    f"**Type**: {kpi.indicator_type.value} Indicator",
                    "",
                    f"**Frequency**: {kpi.frequency}",
                    "",
                    "**Target**: *To be defined*",
                    "",
                    "**Owner**: *To be assigned*",
                    "",
                    "---",
                    "",
                ]
            )

        lines.extend(
            [
                "## Next Steps",
                "",
                "1. Assign owners for each KPI",
                "2. Set baseline and target values",
                "3. Configure data sources and dashboards",
                "4. Establish review cadence",
                "5. Define action triggers (RAG thresholds)",
            ]
        )

        return "\n".join(lines)


class KPIValidator:
    """Validates KPIs against SMART criteria."""

    # Patterns for validation
    NUMERIC_PATTERN = re.compile(r"\d+\.?\d*\s*%?")
    TIME_KEYWORDS = ["daily", "weekly", "monthly", "quarterly", "annual", "by q", "by 20"]

    def validate_kpi(self, kpi_name: str, context: str = "") -> SMARTValidation:
        """Validate a KPI name against SMART criteria."""
        validation = SMARTValidation(kpi_name=kpi_name)
        name_lower = kpi_name.lower()
        context_lower = context.lower() if context else ""

        # Specific: Check for vague terms
        vague_terms = ["improve", "better", "good", "enhance", "optimize", "increase", "decrease"]
        specific_terms = ["rate", "score", "count", "ratio", "percentage", "time", "cost", "revenue"]

        if any(term in name_lower for term in specific_terms):
            validation.specific = SMARTScore.PASS
        elif any(term in name_lower for term in vague_terms) and not any(term in name_lower for term in specific_terms):
            validation.specific = SMARTScore.PARTIAL
            validation.notes.append("Consider adding specific metric type (rate, score, etc.)")
        else:
            validation.specific = SMARTScore.PARTIAL

        # Measurable: Check for quantifiable indicators
        if self.NUMERIC_PATTERN.search(kpi_name) or self.NUMERIC_PATTERN.search(context):
            validation.measurable = SMARTScore.PASS
        elif any(term in name_lower for term in ["score", "rate", "count", "number", "percentage"]):
            validation.measurable = SMARTScore.PASS
        elif any(term in name_lower for term in ["satisfaction", "happiness", "quality"]):
            validation.measurable = SMARTScore.PARTIAL
            validation.notes.append("Define how this will be measured (survey, score, etc.)")
        else:
            validation.measurable = SMARTScore.FAIL
            validation.notes.append("Add measurable component (%, count, score)")

        # Achievable: Check for realistic scope (basic heuristics)
        extreme_terms = ["100%", "zero", "eliminate all", "perfect"]
        if any(term in name_lower for term in extreme_terms):
            validation.achievable = SMARTScore.PARTIAL
            validation.notes.append("Consider if target is realistic given constraints")
        else:
            validation.achievable = SMARTScore.PASS

        # Relevant: Check for business-related terms
        business_terms = ["customer", "revenue", "cost", "efficiency", "quality", "satisfaction", "retention", "growth"]
        if any(term in name_lower for term in business_terms):
            validation.relevant = SMARTScore.PASS
        else:
            validation.relevant = SMARTScore.PARTIAL
            validation.notes.append("Clarify connection to business objectives")

        # Time-bound: Check for time references
        if any(term in name_lower or term in context_lower for term in self.TIME_KEYWORDS):
            validation.time_bound = SMARTScore.PASS
        else:
            validation.time_bound = SMARTScore.FAIL
            validation.notes.append("Add measurement frequency or deadline")

        return validation

    def validate_kpis(self, kpi_names: list) -> list:
        """Validate multiple KPIs."""
        return [self.validate_kpi(name) for name in kpi_names]

    def to_markdown(self, validations: list) -> str:
        """Convert validations to markdown report."""
        lines = [
            "# KPI SMART Validation Report",
            "",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Summary",
            "",
            "| KPI | Score | Status | Notes |",
            "|-----|-------|--------|-------|",
        ]

        for v in validations:
            notes_str = "; ".join(v.notes[:2]) if v.notes else "-"
            lines.append(f"| {v.kpi_name} | {v.overall_score}/100 | {v.status} | {notes_str} |")

        lines.extend(["", "## Detailed Analysis", ""])

        for v in validations:
            lines.extend(
                [
                    f"### {v.kpi_name}",
                    "",
                    f"**Overall Score**: {v.overall_score}/100 ({v.status})",
                    "",
                    "| Criteria | Result |",
                    "|----------|--------|",
                    f"| Specific | {v.specific.value} |",
                    f"| Measurable | {v.measurable.value} |",
                    f"| Achievable | {v.achievable.value} |",
                    f"| Relevant | {v.relevant.value} |",
                    f"| Time-bound | {v.time_bound.value} |",
                    "",
                ]
            )

            if v.notes:
                lines.append("**Recommendations**:")
                for note in v.notes:
                    lines.append(f"- {note}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate KPI framework documents or validate existing KPIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate KPI framework
  python generate_kpi_framework.py --objectives "Increase revenue 20%, Reduce churn" --industry SaaS

  # Validate existing KPIs
  python generate_kpi_framework.py --validate-kpis "NPS, Customer Satisfaction, Revenue"

  # Output to file
  python generate_kpi_framework.py --objectives "Grow market share" --output ./kpi_framework.md
        """,
    )

    parser.add_argument("--objectives", type=str, help="Comma-separated strategic objectives")
    parser.add_argument(
        "--industry", type=str, default="General", help="Industry context (SaaS, E-commerce, Manufacturing, etc.)"
    )
    parser.add_argument(
        "--level", type=str, default="Company", choices=["Company", "Department", "Team"], help="Organizational level"
    )
    parser.add_argument("--validate-kpis", type=str, help="Comma-separated KPI names to validate")
    parser.add_argument("--output", "-o", type=str, help="Output file path (default: stdout)")
    parser.add_argument("--format", type=str, default="markdown", choices=["markdown", "json"], help="Output format")

    args = parser.parse_args()

    # Validation mode
    if args.validate_kpis:
        kpi_names = [k.strip() for k in args.validate_kpis.split(",")]
        validator = KPIValidator()
        validations = validator.validate_kpis(kpi_names)

        if args.format == "json":
            output = json.dumps(
                [
                    {"kpi_name": v.kpi_name, "score": v.overall_score, "status": v.status, "notes": v.notes}
                    for v in validations
                ],
                indent=2,
            )
        else:
            output = validator.to_markdown(validations)

    # Framework generation mode
    elif args.objectives:
        objectives = [o.strip() for o in args.objectives.split(",")]
        generator = KPIFrameworkGenerator(objectives, args.industry, args.level)
        framework = generator.generate_framework()

        if args.format == "json":
            output = json.dumps(
                {
                    "name": framework.name,
                    "objectives": framework.objectives,
                    "industry": framework.industry,
                    "level": framework.level,
                    "strategic_kpis": [k.to_dict() for k in framework.strategic_kpis],
                    "tactical_kpis": [k.to_dict() for k in framework.tactical_kpis],
                    "operational_kpis": [k.to_dict() for k in framework.operational_kpis],
                },
                indent=2,
            )
        else:
            output = generator.to_markdown(framework)

    else:
        parser.print_help()
        sys.exit(1)

    # Output
    if args.output:
        Path(args.output).write_text(output)
        print(f"Output written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
