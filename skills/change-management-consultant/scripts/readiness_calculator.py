#!/usr/bin/env python3
"""
Change Readiness Calculator

Calculates organizational change readiness scores based on key factors.
Provides interpretation and mitigation recommendations.
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ReadinessFactors:
    """Represents change readiness assessment factors."""

    leadership: int  # Leadership commitment (default weight: 30%)
    culture: int  # Organizational culture (default weight: 25%)
    capacity: int  # Current workload/capacity (default weight: 20%)
    history: int  # Past change history (default weight: 15%)
    resources: int  # Available resources (default weight: 10%)

    # Optional custom weights (must sum to 100)
    weights: dict = field(
        default_factory=lambda: {
            "leadership": 30,
            "culture": 25,
            "capacity": 20,
            "history": 15,
            "resources": 10,
        }
    )

    def __post_init__(self):
        """Validate scores and weights."""
        for attr in ["leadership", "culture", "capacity", "history", "resources"]:
            value = getattr(self, attr)
            if not 1 <= value <= 10:
                raise ValueError(f"{attr} must be between 1 and 10, got {value}")

        total_weight = sum(self.weights.values())
        if total_weight != 100:
            raise ValueError(f"Weights must sum to 100, got {total_weight}")

    @property
    def weighted_score(self) -> float:
        """Calculate weighted readiness score."""
        return (
            self.leadership * self.weights["leadership"]
            + self.culture * self.weights["culture"]
            + self.capacity * self.weights["capacity"]
            + self.history * self.weights["history"]
            + self.resources * self.weights["resources"]
        ) / 100

    @property
    def simple_average(self) -> float:
        """Calculate simple average score."""
        return (self.leadership + self.culture + self.capacity + self.history + self.resources) / 5

    def get_weak_factors(self) -> list[tuple[str, int]]:
        """Identify factors scoring below threshold."""
        factors = [
            ("Leadership Commitment", self.leadership),
            ("Organizational Culture", self.culture),
            ("Capacity", self.capacity),
            ("Change History", self.history),
            ("Resources", self.resources),
        ]
        return [(name, score) for name, score in factors if score < 6]

    def get_status(self, score: float) -> str:
        """Get status indicator for a score."""
        if score >= 8:
            return "✅"
        elif score >= 6:
            return "🟡"
        else:
            return "🔴"


def get_mitigation_strategies(factor: str) -> list[str]:
    """Get mitigation strategies for weak factors."""
    strategies = {
        "Leadership Commitment": [
            "Schedule executive briefing to reinforce business case",
            "Request visible sponsorship actions from senior leaders",
            "Establish regular steering committee meetings",
            "Align change with strategic objectives in communications",
            "Address any leadership concerns or reservations directly",
        ],
        "Organizational Culture": [
            "Identify and leverage cultural change champions",
            "Frame change in terms of organizational values",
            "Build on existing cultural strengths",
            "Address cultural barriers through targeted interventions",
            "Use storytelling to connect change to cultural identity",
        ],
        "Capacity": [
            "Phase implementation to spread workload",
            "Identify tasks that can be deprioritized or postponed",
            "Provide additional temporary resources",
            "Simplify change requirements where possible",
            "Build in recovery time between major milestones",
        ],
        "Change History": [
            "Acknowledge past change failures openly",
            "Explain what's different about this initiative",
            "Demonstrate early wins to build credibility",
            "Address lingering concerns from previous changes",
            "Involve people burned by past changes in planning",
        ],
        "Resources": [
            "Develop detailed resource plan and request approval",
            "Identify internal resources that can be redeployed",
            "Consider external support for critical activities",
            "Prioritize resource allocation to high-impact areas",
            "Build contingency into resource estimates",
        ],
    }
    return strategies.get(factor, [])


def get_readiness_interpretation(score: float) -> tuple[str, str, str]:
    """Get interpretation based on readiness score."""
    if score >= 8:
        return (
            "High Readiness",
            "Organization is well-positioned for change success.",
            "Proceed with confidence. Monitor to maintain readiness.",
        )
    elif score >= 6:
        return (
            "Moderate Readiness",
            "Organization can proceed but with attention to weak areas.",
            "Address gaps before major milestones. Build contingency plans.",
        )
    elif score >= 4:
        return (
            "Low Readiness",
            "Significant preparation needed before proceeding.",
            "Delay major activities until readiness improves. Intensive intervention required.",
        )
    else:
        return (
            "Critical Risk",
            "Organization is not ready for this change.",
            "Reassess change approach. Consider scope reduction or postponement.",
        )


def generate_report(factors: ReadinessFactors, output_format: str = "markdown") -> str:
    """Generate readiness assessment report."""
    weak_factors = factors.get_weak_factors()
    level, description, recommendation = get_readiness_interpretation(factors.weighted_score)

    if output_format == "json":
        return json.dumps(
            {
                "scores": {
                    "leadership": factors.leadership,
                    "culture": factors.culture,
                    "capacity": factors.capacity,
                    "history": factors.history,
                    "resources": factors.resources,
                },
                "weights": factors.weights,
                "weighted_score": round(factors.weighted_score, 2),
                "simple_average": round(factors.simple_average, 2),
                "readiness_level": level,
                "description": description,
                "recommendation": recommendation,
                "weak_factors": [{"name": name, "score": score} for name, score in weak_factors],
                "mitigation_strategies": {name: get_mitigation_strategies(name) for name, _ in weak_factors},
            },
            indent=2,
            ensure_ascii=False,
        )

    # Build mitigation section
    mitigation_section = ""
    if weak_factors:
        mitigation_section = "\n### Mitigation Strategies\n"
        for name, score in weak_factors:
            strategies = get_mitigation_strategies(name)
            strat_list = "\n".join(f"  - {s}" for s in strategies[:3])
            mitigation_section += f"\n**{name}** (Score: {score}/10)\n{strat_list}\n"

    report = f"""# Change Readiness Assessment Report

## Overall Readiness Score: {factors.weighted_score:.1f}/10 {factors.get_status(factors.weighted_score)}

**Level**: {level}
**Assessment**: {description}
**Recommendation**: {recommendation}

---

## Factor Scores

| Factor | Weight | Score | Status |
|--------|--------|-------|--------|
| Leadership Commitment | {factors.weights["leadership"]}% | {factors.leadership}/10 | {factors.get_status(factors.leadership)} |
| Organizational Culture | {factors.weights["culture"]}% | {factors.culture}/10 | {factors.get_status(factors.culture)} |
| Capacity | {factors.weights["capacity"]}% | {factors.capacity}/10 | {factors.get_status(factors.capacity)} |
| Change History | {factors.weights["history"]}% | {factors.history}/10 | {factors.get_status(factors.history)} |
| Resources | {factors.weights["resources"]}% | {factors.resources}/10 | {factors.get_status(factors.resources)} |

**Weighted Score**: {factors.weighted_score:.2f}/10
**Simple Average**: {factors.simple_average:.2f}/10

---

## Risk Areas

"""

    if weak_factors:
        for name, score in weak_factors:
            report += f"- 🔴 **{name}**: {score}/10 - Requires immediate attention\n"
    else:
        report += "✅ No critical risk areas identified.\n"

    report += mitigation_section

    report += """
---

## Readiness Scale Reference

| Score | Level | Interpretation |
|-------|-------|----------------|
| 8-10 | High | Proceed with confidence |
| 6-7.9 | Moderate | Proceed with attention to gaps |
| 4-5.9 | Low | Significant preparation needed |
| <4 | Critical | Reassess change approach |

---

## Next Steps

1. Address any factors scoring below 6 before proceeding
2. Schedule follow-up assessment in 2-4 weeks
3. Update change management plan based on findings
4. Communicate readiness status to steering committee
"""

    return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Change Readiness Calculator for Organizational Change",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --leadership 8 --culture 6 --capacity 5 --history 7 --resources 9
  %(prog)s -l 7 -c 5 -a 4 -y 6 -r 8 --format json
        """,
    )

    parser.add_argument("--leadership", "-l", type=int, required=True, help="Leadership commitment score (1-10)")
    parser.add_argument("--culture", "-c", type=int, required=True, help="Organizational culture score (1-10)")
    parser.add_argument("--capacity", "-a", type=int, required=True, help="Capacity/workload score (1-10)")
    parser.add_argument("--history", "-y", type=int, required=True, help="Past change history score (1-10)")
    parser.add_argument("--resources", "-r", type=int, required=True, help="Available resources score (1-10)")
    parser.add_argument(
        "--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format (default: markdown)"
    )
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        factors = ReadinessFactors(
            leadership=args.leadership,
            culture=args.culture,
            capacity=args.capacity,
            history=args.history,
            resources=args.resources,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(factors, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
