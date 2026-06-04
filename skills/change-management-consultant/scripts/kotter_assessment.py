#!/usr/bin/env python3
"""
Kotter 8-Step Change Assessment Tool

Evaluates organizational progress against Kotter's 8-Step Change Model.
Generates recommendations based on assessment results.
"""

import argparse
import json
import sys
from dataclasses import dataclass


@dataclass
class KotterScore:
    """Represents Kotter 8-Step assessment scores."""

    urgency: int  # Step 1: Create Urgency
    coalition: int  # Step 2: Build Guiding Coalition
    vision: int  # Step 3: Form Strategic Vision
    communicate: int  # Step 4: Communicate the Vision
    empower: int  # Step 5: Enable Action by Removing Barriers
    wins: int  # Step 6: Generate Short-Term Wins
    sustain: int  # Step 7: Sustain Acceleration
    anchor: int  # Step 8: Institute Change

    def __post_init__(self):
        """Validate scores are within range."""
        attrs = [
            "urgency",
            "coalition",
            "vision",
            "communicate",
            "empower",
            "wins",
            "sustain",
            "anchor",
        ]
        for attr in attrs:
            value = getattr(self, attr)
            if not 1 <= value <= 5:
                raise ValueError(f"{attr} must be between 1 and 5, got {value}")

    @property
    def total(self) -> int:
        """Calculate total score."""
        return (
            self.urgency
            + self.coalition
            + self.vision
            + self.communicate
            + self.empower
            + self.wins
            + self.sustain
            + self.anchor
        )

    @property
    def max_score(self) -> int:
        """Maximum possible score."""
        return 40

    @property
    def percentage(self) -> float:
        """Calculate percentage score."""
        return (self.total / self.max_score) * 100

    @property
    def current_phase(self) -> str:
        """Determine current phase based on scores."""
        phase1_avg = (self.urgency + self.coalition + self.vision) / 3
        phase2_avg = (self.communicate + self.empower + self.wins) / 3
        phase3_avg = (self.sustain + self.anchor) / 2

        if phase1_avg < 3:
            return "Phase 1: Creating the Climate for Change"
        elif phase2_avg < 3:
            return "Phase 2: Engaging and Enabling the Organization"
        else:
            return "Phase 3: Implementing and Sustaining the Change"

    @property
    def weakest_step(self) -> tuple[int, str, int]:
        """Find the weakest step (first low-scoring step in sequence)."""
        steps = [
            (1, "Create Urgency", self.urgency),
            (2, "Build Guiding Coalition", self.coalition),
            (3, "Form Strategic Vision", self.vision),
            (4, "Communicate the Vision", self.communicate),
            (5, "Enable Action by Removing Barriers", self.empower),
            (6, "Generate Short-Term Wins", self.wins),
            (7, "Sustain Acceleration", self.sustain),
            (8, "Institute Change", self.anchor),
        ]
        for num, name, score in steps:
            if score < 3:
                return (num, name, score)
        # If all >= 3, return lowest
        return min(steps, key=lambda x: x[2])

    def get_status(self, score: int) -> str:
        """Get status indicator for a score."""
        if score >= 4:
            return "✅"
        elif score >= 3:
            return "🟡"
        else:
            return "🔴"


STEP_DESCRIPTIONS = {
    1: {
        "name": "Create Urgency",
        "name_ja": "危機感を高める",
        "description": "Help others see the need for change through a compelling reason.",
        "recommendations": [
            "Identify and communicate potential threats and opportunities",
            "Share data and evidence demonstrating need for change",
            "Get input from customers, stakeholders, and analysts",
            "Use compelling stories to illustrate the need",
            "Ensure 75%+ of leadership genuinely supports the change",
        ],
    },
    2: {
        "name": "Build Guiding Coalition",
        "name_ja": "変革推進チームを作る",
        "description": "Assemble a group with enough power to lead the change.",
        "recommendations": [
            "Identify true leaders with credibility and expertise",
            "Include people with positional power across functions",
            "Ensure the team can work outside normal hierarchy",
            "Build trust and common goals within the coalition",
            "Add line managers who can drive local implementation",
        ],
    },
    3: {
        "name": "Form Strategic Vision",
        "name_ja": "ビジョンと戦略を生み出す",
        "description": "Create a vision that directs the change effort.",
        "recommendations": [
            "Clarify how the future will differ from the past",
            "Create a simple, imaginable vision statement",
            "Develop strategy to achieve the vision",
            "Test that coalition can explain vision in 5 minutes",
            "Ensure vision is desirable, feasible, and focused",
        ],
    },
    4: {
        "name": "Communicate the Vision",
        "name_ja": "変革のビジョンを周知徹底する",
        "description": "Get as many people as possible to understand and accept the vision.",
        "recommendations": [
            "Use every communication channel available",
            "Keep messages simple and repeat constantly (7x rule)",
            "Lead by example - walk the talk",
            "Address concerns and anxieties openly",
            "Use stories and metaphors to make vision memorable",
        ],
    },
    5: {
        "name": "Enable Action by Removing Barriers",
        "name_ja": "従業員の自発を促す",
        "description": "Remove obstacles that block the vision.",
        "recommendations": [
            "Remove structural barriers to change",
            "Align systems and processes with the vision",
            "Provide training for new skills required",
            "Address supervisors who undermine the change",
            "Recognize and reward new behaviors",
        ],
    },
    6: {
        "name": "Generate Short-Term Wins",
        "name_ja": "短期的成果を実現する",
        "description": "Create visible, unambiguous successes as soon as possible.",
        "recommendations": [
            "Plan for visible improvements within 6-18 months",
            "Create wins that are clearly connected to the change",
            "Recognize and reward contributors publicly",
            "Use wins to build momentum and silence critics",
            "Publicize wins widely across the organization",
        ],
    },
    7: {
        "name": "Sustain Acceleration",
        "name_ja": "成果を生かして更なる変革を進める",
        "description": "Use credibility from wins to tackle bigger problems.",
        "recommendations": [
            "Use increased credibility to change more systems",
            "Hire and promote people who support the vision",
            "Reinvigorate process with new projects",
            "Keep urgency level high - don't declare victory early",
            "Bring in additional change agents as needed",
        ],
    },
    8: {
        "name": "Institute Change",
        "name_ja": "新しい方法を企業文化に定着させる",
        "description": "Make new behaviors stick by anchoring them in culture.",
        "recommendations": [
            "Show connections between new behaviors and success",
            "Update formal processes and systems permanently",
            "Revise hiring and promotion criteria",
            "Create means to ensure leadership continuity",
            "Articulate how new approaches will be sustained",
        ],
    },
}


def get_recommendations(step_num: int, score: int) -> list[str]:
    """Get recommendations based on step and score."""
    step = STEP_DESCRIPTIONS.get(step_num, {})
    recommendations = step.get("recommendations", [])

    # Return more recommendations for lower scores
    if score <= 2:
        return recommendations[:5]
    elif score <= 3:
        return recommendations[:3]
    else:
        return recommendations[:2]


def generate_report(score: KotterScore, output_format: str = "markdown") -> str:
    """Generate assessment report."""
    weak_num, weak_name, weak_score = score.weakest_step

    if output_format == "json":
        return json.dumps(
            {
                "scores": {
                    "step1_urgency": score.urgency,
                    "step2_coalition": score.coalition,
                    "step3_vision": score.vision,
                    "step4_communicate": score.communicate,
                    "step5_empower": score.empower,
                    "step6_wins": score.wins,
                    "step7_sustain": score.sustain,
                    "step8_anchor": score.anchor,
                },
                "total": score.total,
                "max_score": score.max_score,
                "percentage": round(score.percentage, 1),
                "current_phase": score.current_phase,
                "weakest_step": {
                    "number": weak_num,
                    "name": weak_name,
                    "score": weak_score,
                },
                "recommendations": get_recommendations(weak_num, weak_score),
            },
            indent=2,
            ensure_ascii=False,
        )

    # Markdown format
    recommendations = get_recommendations(weak_num, weak_score)
    rec_list = "\n".join(f"- {r}" for r in recommendations)

    report = f"""# Kotter 8-Step Change Assessment Report

## Overall Progress: {score.total}/{score.max_score} ({score.percentage:.1f}%)

**Current Phase**: {score.current_phase}

---

## Step Scores

### Phase 1: Creating the Climate for Change

| Step | Description | Score | Status |
|------|-------------|-------|--------|
| **1** | Create Urgency ({STEP_DESCRIPTIONS[1]["name_ja"]}) | {score.urgency}/5 | {score.get_status(score.urgency)} |
| **2** | Build Guiding Coalition ({STEP_DESCRIPTIONS[2]["name_ja"]}) | {score.coalition}/5 | {score.get_status(score.coalition)} |
| **3** | Form Strategic Vision ({STEP_DESCRIPTIONS[3]["name_ja"]}) | {score.vision}/5 | {score.get_status(score.vision)} |

### Phase 2: Engaging and Enabling the Organization

| Step | Description | Score | Status |
|------|-------------|-------|--------|
| **4** | Communicate the Vision ({STEP_DESCRIPTIONS[4]["name_ja"]}) | {score.communicate}/5 | {score.get_status(score.communicate)} |
| **5** | Enable Action ({STEP_DESCRIPTIONS[5]["name_ja"]}) | {score.empower}/5 | {score.get_status(score.empower)} |
| **6** | Generate Short-Term Wins ({STEP_DESCRIPTIONS[6]["name_ja"]}) | {score.wins}/5 | {score.get_status(score.wins)} |

### Phase 3: Implementing and Sustaining the Change

| Step | Description | Score | Status |
|------|-------------|-------|--------|
| **7** | Sustain Acceleration ({STEP_DESCRIPTIONS[7]["name_ja"]}) | {score.sustain}/5 | {score.get_status(score.sustain)} |
| **8** | Institute Change ({STEP_DESCRIPTIONS[8]["name_ja"]}) | {score.anchor}/5 | {score.get_status(score.anchor)} |

---

## Interpretation

"""

    if score.percentage >= 80:
        report += "✅ **Strong Progress**: The change initiative is well-managed across all steps. Focus on sustaining momentum.\n"
    elif score.percentage >= 60:
        report += "🟡 **Moderate Progress**: Good foundation, but some steps need attention before advancing further.\n"
    elif score.percentage >= 40:
        report += "🔴 **Limited Progress**: Significant gaps exist. Address foundational steps before proceeding.\n"
    else:
        report += "🔴 **Critical Gaps**: Major intervention required. Revisit Phase 1 before advancing.\n"

    report += f"""
---

## Priority Focus: Step {weak_num} - {weak_name}

**Current Score**: {weak_score}/5 {score.get_status(weak_score)}

**Description**: {STEP_DESCRIPTIONS[weak_num]["description"]}

### Recommended Actions

{rec_list}

---

## Next Steps

1. Focus on the weakest step ({weak_name}) before advancing to later steps
2. Ensure Phase 1 steps score 4+ before heavy Phase 2 investment
3. Re-assess after interventions to measure progress
4. Monitor all steps to prevent regression

---

## Readiness Scale Reference

| Score | Level | Interpretation |
|-------|-------|----------------|
| 32-40 (80-100%) | Strong | Proceed with confidence |
| 24-31 (60-79%) | Moderate | Address gaps before key milestones |
| 16-23 (40-59%) | Limited | Significant preparation needed |
| <16 (<40%) | Critical | Reassess change approach |
"""

    return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Kotter 8-Step Change Assessment Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Steps (1-5 scale):
  1. Urgency    - Is there genuine sense of urgency?
  2. Coalition  - Is there a powerful guiding coalition?
  3. Vision     - Is the vision clear and compelling?
  4. Communicate - Has vision been communicated effectively?
  5. Empower    - Have obstacles been removed?
  6. Wins       - Are there visible short-term wins?
  7. Sustain    - Are we building on wins for more change?
  8. Anchor     - Is change anchored in culture?

Examples:
  %(prog)s --urgency 4 --coalition 3 --vision 4 --communicate 2 --empower 2 --wins 1 --sustain 1 --anchor 1
  %(prog)s -u 4 -c 3 -v 4 -m 2 -e 2 -w 1 -s 1 -a 1 --format json
        """,
    )

    parser.add_argument(
        "--urgency",
        "-u",
        type=int,
        required=True,
        help="Step 1: Create Urgency score (1-5)",
    )
    parser.add_argument(
        "--coalition",
        "-c",
        type=int,
        required=True,
        help="Step 2: Build Guiding Coalition score (1-5)",
    )
    parser.add_argument(
        "--vision",
        "-v",
        type=int,
        required=True,
        help="Step 3: Form Strategic Vision score (1-5)",
    )
    parser.add_argument(
        "--communicate",
        "-m",
        type=int,
        required=True,
        help="Step 4: Communicate the Vision score (1-5)",
    )
    parser.add_argument(
        "--empower",
        "-e",
        type=int,
        required=True,
        help="Step 5: Enable Action score (1-5)",
    )
    parser.add_argument(
        "--wins",
        "-w",
        type=int,
        required=True,
        help="Step 6: Generate Short-Term Wins score (1-5)",
    )
    parser.add_argument(
        "--sustain",
        "-s",
        type=int,
        required=True,
        help="Step 7: Sustain Acceleration score (1-5)",
    )
    parser.add_argument(
        "--anchor",
        "-a",
        type=int,
        required=True,
        help="Step 8: Institute Change score (1-5)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        kotter_score = KotterScore(
            urgency=args.urgency,
            coalition=args.coalition,
            vision=args.vision,
            communicate=args.communicate,
            empower=args.empower,
            wins=args.wins,
            sustain=args.sustain,
            anchor=args.anchor,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(kotter_score, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
