#!/usr/bin/env python3
"""
ADKAR Assessment Tool

Calculates ADKAR scores and identifies barrier points for change management.
Generates actionable recommendations based on assessment results.
"""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class ADKARScore:
    """Represents ADKAR assessment scores for a stakeholder or group."""

    awareness: int
    desire: int
    knowledge: int
    ability: int
    reinforcement: int
    stakeholder: str = "Stakeholder"

    def __post_init__(self):
        """Validate scores are within range."""
        for attr in ["awareness", "desire", "knowledge", "ability", "reinforcement"]:
            value = getattr(self, attr)
            if not 0 <= value <= 10:
                raise ValueError(f"{attr} must be between 0 and 10, got {value}")

    @property
    def total(self) -> int:
        """Calculate total ADKAR score."""
        return self.awareness + self.desire + self.knowledge + self.ability + self.reinforcement

    @property
    def average(self) -> float:
        """Calculate average ADKAR score."""
        return self.total / 5

    @property
    def barrier_point(self) -> str:
        """Identify the lowest-scoring element (barrier point)."""
        scores = {
            "Awareness": self.awareness,
            "Desire": self.desire,
            "Knowledge": self.knowledge,
            "Ability": self.ability,
            "Reinforcement": self.reinforcement,
        }
        return min(scores, key=scores.get)

    @property
    def barrier_score(self) -> int:
        """Get the score of the barrier point."""
        scores = {
            "Awareness": self.awareness,
            "Desire": self.desire,
            "Knowledge": self.knowledge,
            "Ability": self.ability,
            "Reinforcement": self.reinforcement,
        }
        return min(scores.values())

    def get_status(self, score: int) -> str:
        """Get status indicator for a score."""
        if score >= 8:
            return "✅"
        elif score >= 5:
            return "🟡"
        else:
            return "🔴"


def get_recommendations(barrier: str, score: int) -> list[str]:
    """Get recommendations based on barrier point and score."""
    recommendations = {
        "Awareness": [
            "Communicate business case and reasons for change clearly",
            "Share data and evidence demonstrating need for change",
            "Host town halls and Q&A sessions with leadership",
            "Distribute FAQ documents addressing common questions",
            "Use multiple channels (email, meetings, intranet) to reach all stakeholders",
        ],
        "Desire": [
            "Address personal concerns through 1:1 conversations",
            "Clearly articulate 'What's In It For Me' (WIIFM) benefits",
            "Involve individuals in change design decisions",
            "Connect change to personal and professional goals",
            "Leverage peer influence and change champions",
            "Share success stories and testimonials",
        ],
        "Knowledge": [
            "Develop comprehensive training programs",
            "Create job aids and quick reference guides",
            "Provide hands-on practice opportunities",
            "Establish coaching and mentoring relationships",
            "Build knowledge base with FAQs and documentation",
            "Schedule training close to go-live for relevance",
        ],
        "Ability": [
            "Extend practice time before full deployment",
            "Provide real-time coaching and support",
            "Create safe environments to practice new skills",
            "Remove barriers to performance",
            "Offer additional 1:1 support for struggling individuals",
            "Consider phased rollout to build capability gradually",
        ],
        "Reinforcement": [
            "Publicly recognize and celebrate successes",
            "Align rewards and incentives with new behaviors",
            "Update policies and procedures to reflect new state",
            "Address relapses quickly with coaching",
            "Share progress metrics and achievements",
            "Ensure managers are reinforcing new behaviors",
        ],
    }

    # Return more recommendations for lower scores
    if score <= 3:
        return recommendations.get(barrier, [])[:5]
    elif score <= 5:
        return recommendations.get(barrier, [])[:3]
    else:
        return recommendations.get(barrier, [])[:2]


def generate_report(score: ADKARScore, output_format: str = "markdown") -> str:
    """Generate assessment report."""
    if output_format == "json":
        return json.dumps(
            {
                "stakeholder": score.stakeholder,
                "scores": {
                    "awareness": score.awareness,
                    "desire": score.desire,
                    "knowledge": score.knowledge,
                    "ability": score.ability,
                    "reinforcement": score.reinforcement,
                },
                "total": score.total,
                "average": round(score.average, 2),
                "barrier_point": score.barrier_point,
                "barrier_score": score.barrier_score,
                "recommendations": get_recommendations(score.barrier_point, score.barrier_score),
            },
            indent=2,
            ensure_ascii=False,
        )

    # Markdown format
    recommendations = get_recommendations(score.barrier_point, score.barrier_score)
    rec_list = "\n".join(f"- {r}" for r in recommendations)

    report = f"""# ADKAR Assessment Report

## Stakeholder: {score.stakeholder}

### Scores

| Element | Score | Status |
|---------|-------|--------|
| **A** - Awareness (認識) | {score.awareness}/10 | {score.get_status(score.awareness)} |
| **D** - Desire (意欲) | {score.desire}/10 | {score.get_status(score.desire)} |
| **K** - Knowledge (知識) | {score.knowledge}/10 | {score.get_status(score.knowledge)} |
| **A** - Ability (能力) | {score.ability}/10 | {score.get_status(score.ability)} |
| **R** - Reinforcement (強化) | {score.reinforcement}/10 | {score.get_status(score.reinforcement)} |

### Summary

- **Total Score**: {score.total}/50
- **Average Score**: {score.average:.1f}/10
- **Barrier Point**: **{score.barrier_point}** ({score.barrier_score}/10)

### Interpretation

"""

    if score.average >= 8:
        report += "✅ **High Change Readiness**: Strong foundation for change success. Focus on sustaining momentum.\n"
    elif score.average >= 6:
        report += "🟡 **Moderate Readiness**: Good progress but barrier point needs attention before proceeding.\n"
    elif score.average >= 4:
        report += "🔴 **Low Readiness**: Significant intervention required. Address barrier point urgently.\n"
    else:
        report += "🔴 **Critical**: Change at risk. Major interventions needed across multiple elements.\n"

    report += f"""
### Priority Actions for {score.barrier_point}

{rec_list}

### Next Steps

1. Address the barrier point ({score.barrier_point}) before advancing to later elements
2. Re-assess after interventions to measure progress
3. Monitor other elements to prevent new barriers from forming
"""

    return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ADKAR Assessment Tool for Change Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --stakeholder "Sales Team" -a 8 -d 4 -k 2 -b 0 -r 0
  %(prog)s --stakeholder "IT Department" -a 7 -d 6 -k 5 -b 3 -r 1 --format json
        """,
    )

    parser.add_argument(
        "--stakeholder", "-s", default="Stakeholder", help="Name of stakeholder or group being assessed"
    )
    parser.add_argument(
        "--awareness", "-a", type=int, required=True, help="Awareness score (0-10): Understanding why change is needed"
    )
    parser.add_argument(
        "--desire", "-d", type=int, required=True, help="Desire score (0-10): Personal motivation to support change"
    )
    parser.add_argument(
        "--knowledge", "-k", type=int, required=True, help="Knowledge score (0-10): Understanding how to change"
    )
    parser.add_argument(
        "--ability", "-b", type=int, required=True, help="Ability score (0-10): Demonstrated capability to change"
    )
    parser.add_argument(
        "--reinforcement",
        "-r",
        type=int,
        required=True,
        help="Reinforcement score (0-10): Factors sustaining the change",
    )
    parser.add_argument(
        "--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format (default: markdown)"
    )
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        score = ADKARScore(
            stakeholder=args.stakeholder,
            awareness=args.awareness,
            desire=args.desire,
            knowledge=args.knowledge,
            ability=args.ability,
            reinforcement=args.reinforcement,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(score, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
