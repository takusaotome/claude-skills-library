#!/usr/bin/env python3
"""Generate a business plan outline in Markdown."""

from __future__ import annotations

import argparse
from pathlib import Path

PURPOSE_LABELS = {
    "ja": {
        "investor_pitch": "投資家向けピッチ",
        "bank_loan": "銀行融資申請",
        "internal_proposal": "社内提案",
        "draft": "初期検討ドラフト",
        "public_agency": "公的機関向け創業計画",
    },
    "en": {
        "investor_pitch": "Investor Pitch",
        "bank_loan": "Bank Loan Application",
        "internal_proposal": "Internal Proposal",
        "draft": "Draft Plan",
        "public_agency": "Public Agency Startup Plan",
    },
}


SECTIONS = {
    "full": [
        "1. Executive Summary",
        "2. Background and Objectives",
        "3. Market Analysis",
        "4. Competitive Analysis",
        "5. Product / Service",
        "6. Business Model",
        "7. Go-to-Market Strategy",
        "8. Operations Plan",
        "9. Financial Plan",
        "10. Risks and Mitigations",
        "11. Milestones and KPI",
        "12. Appendix",
    ],
    "short": [
        "1. Proposal Summary",
        "2. Problem and Opportunity",
        "3. Solution Overview",
        "4. Market and Competition",
        "5. Financial Snapshot",
        "6. Execution Timeline",
        "7. Risks and Mitigations",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--purpose",
        choices=[
            "investor_pitch",
            "bank_loan",
            "internal_proposal",
            "draft",
            "public_agency",
        ],
        required=True,
        help="Plan purpose.",
    )
    parser.add_argument(
        "--industry",
        default="general",
        help="Industry keyword (e.g. saas, ecommerce, consulting, restaurant).",
    )
    parser.add_argument(
        "--language",
        choices=["ja", "en"],
        default="ja",
        help="Output language.",
    )
    parser.add_argument(
        "--company",
        default="TBD Company",
        help="Company or project name.",
    )
    parser.add_argument(
        "--horizon-years",
        type=int,
        default=3,
        help="Planning horizon in years.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output markdown file path.",
    )
    return parser.parse_args()


def choose_template(purpose: str) -> str:
    if purpose in {"internal_proposal", "draft"}:
        return "short"
    return "full"


def render_markdown(args: argparse.Namespace) -> str:
    labels = PURPOSE_LABELS[args.language]
    template = choose_template(args.purpose)
    sections = SECTIONS[template]
    purpose_label = labels[args.purpose]

    lines = [
        f"# {args.company} Business Plan Outline",
        "",
        "## Plan Metadata",
        f"- Purpose: {purpose_label}",
        f"- Industry: {args.industry}",
        f"- Planning Horizon: {args.horizon_years} years",
        f"- Language: {args.language}",
        "",
        "## Required Inputs",
        "- Customer segment",
        "- Value proposition",
        "- Revenue model",
        "- Cost structure",
        "- Key risks",
        "",
        "## Suggested Structure",
    ]
    lines.extend([f"- {item}" for item in sections])
    lines.extend(
        [
            "",
            "## Financial Scenarios",
            "- Base: realistic assumptions",
            "- Upside: 1.3x growth assumptions",
            "- Downside: 0.6x growth assumptions",
            "",
            "## Notes",
            "- Add evidence for every market size number.",
            "- Record assumptions explicitly in the financial section.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    content = render_markdown(args)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
