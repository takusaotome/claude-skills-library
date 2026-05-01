#!/usr/bin/env python3
"""
Generate vendor quote comparison report.

Compares received quotes across multiple dimensions and generates
a formatted comparison report in Markdown.
"""

import argparse
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from procurement_models import (
    ProcurementProject,
    Vendor,
    VendorStatus,
)


def load_project(project_dir: Path) -> ProcurementProject:
    """Load procurement project from directory."""
    config_path = project_dir / "procurement.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"No procurement project found at {project_dir}")
    return ProcurementProject.load(config_path)


def calculate_price_scores(vendors: list[Vendor]) -> dict[str, int]:
    """
    Calculate relative price scores for vendors.

    Lowest price gets 100, others scored relative to lowest.
    """
    scores = {}
    amounts = []

    for v in vendors:
        if v.quote and v.quote.amount:
            amounts.append((v.name, v.quote.amount))

    if not amounts:
        return scores

    lowest = min(a[1] for a in amounts)

    for name, amount in amounts:
        score = int((lowest / amount) * 100)
        scores[name] = min(score, 100)

    return scores


def format_currency(amount: Optional[float], currency: str = "JPY") -> str:
    """Format currency amount for display."""
    if amount is None:
        return "-"
    if currency == "JPY":
        return f"¥{amount:,.0f}"
    elif currency == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{currency} {amount:,.2f}"


def generate_comparison_report(
    project: ProcurementProject,
    evaluation_weights: Optional[dict[str, int]] = None,
) -> str:
    """
    Generate vendor comparison report in Markdown format.

    Args:
        project: The procurement project
        evaluation_weights: Optional custom weights for evaluation dimensions

    Returns:
        Markdown formatted report
    """
    # Default weights if not provided
    if evaluation_weights is None:
        evaluation_weights = {
            "price": 30,
            "delivery": 25,
            "technical": 25,
            "experience": 20,
        }

    # Get vendors with quotes
    vendors_with_quotes = [v for v in project.vendors if v.status == VendorStatus.QUOTE_RECEIVED]

    if not vendors_with_quotes:
        return "# Vendor Comparison Report\n\nNo quotes received yet."

    # Calculate price scores
    price_scores = calculate_price_scores(vendors_with_quotes)

    # Build report
    lines = []
    lines.append("# Vendor Comparison Report")
    lines.append("")
    lines.append(f"## Project: {project.name}")
    lines.append(f"**Client:** {project.client}")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Vendors Compared:** {len(vendors_with_quotes)}")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Vendor | Quote Amount | Delivery Date | Price Score |")
    lines.append("|--------|-------------|---------------|-------------|")

    for v in sorted(vendors_with_quotes, key=lambda x: x.quote.amount or float("inf")):
        amount_str = format_currency(v.quote.amount, v.quote.currency)
        delivery_str = str(v.quote.delivery_date) if v.quote.delivery_date else "-"
        score = price_scores.get(v.name, "-")
        lines.append(f"| {v.name} | {amount_str} | {delivery_str} | {score}/100 |")

    lines.append("")

    # Price analysis
    lines.append("## Price Analysis")
    lines.append("")

    amounts = [(v.name, v.quote.amount, v.quote.currency) for v in vendors_with_quotes if v.quote.amount]

    if amounts:
        sorted_amounts = sorted(amounts, key=lambda x: x[1])
        lowest_name, lowest_amount, lowest_currency = sorted_amounts[0]
        highest_name, highest_amount, highest_currency = sorted_amounts[-1]

        lines.append(f"- **Lowest Quote:** {lowest_name} at {format_currency(lowest_amount, lowest_currency)}")
        lines.append(f"- **Highest Quote:** {highest_name} at {format_currency(highest_amount, highest_currency)}")

        if len(amounts) > 1:
            spread = highest_amount - lowest_amount
            spread_pct = (spread / lowest_amount) * 100
            lines.append(f"- **Price Spread:** {format_currency(spread, lowest_currency)} ({spread_pct:.1f}%)")

            avg = sum(a[1] for a in amounts) / len(amounts)
            lines.append(f"- **Average Quote:** {format_currency(avg, lowest_currency)}")

    lines.append("")

    # Delivery timeline
    lines.append("## Delivery Timeline")
    lines.append("")

    delivery_data = [(v.name, v.quote.delivery_date) for v in vendors_with_quotes if v.quote.delivery_date]

    if delivery_data:
        sorted_delivery = sorted(delivery_data, key=lambda x: x[1])
        lines.append("| Vendor | Delivery Date | Days from Today |")
        lines.append("|--------|---------------|-----------------|")

        for name, delivery in sorted_delivery:
            days = (delivery - date.today()).days
            lines.append(f"| {name} | {delivery} | {days} |")

        lines.append("")
    else:
        lines.append("No delivery dates specified in quotes.")
        lines.append("")

    # Detailed vendor profiles
    lines.append("## Vendor Details")
    lines.append("")

    for v in vendors_with_quotes:
        lines.append(f"### {v.name}")
        lines.append("")
        lines.append(f"- **Quote Amount:** {format_currency(v.quote.amount, v.quote.currency)}")
        lines.append(f"- **Delivery Date:** {v.quote.delivery_date or 'Not specified'}")
        lines.append(f"- **Quote Valid Until:** {v.quote.valid_until or 'Not specified'}")
        lines.append(f"- **Quote Received:** {v.quote.received_date}")
        lines.append(f"- **Price Score:** {price_scores.get(v.name, '-')}/100")

        if v.quote.notes:
            lines.append(f"- **Notes:** {v.quote.notes}")

        lines.append("")

    # Evaluation criteria reminder
    lines.append("## Evaluation Criteria")
    lines.append("")
    lines.append("| Dimension | Weight | Notes |")
    lines.append("|-----------|--------|-------|")
    lines.append(f"| Price | {evaluation_weights.get('price', 30)}% | Relative scoring based on lowest quote |")
    lines.append(f"| Delivery | {evaluation_weights.get('delivery', 25)}% | Timeline alignment with project needs |")
    lines.append(f"| Technical | {evaluation_weights.get('technical', 25)}% | Solution approach and capabilities |")
    lines.append(
        f"| Experience | {evaluation_weights.get('experience', 20)}% | Relevant project history and references |"
    )
    lines.append("")

    # Non-responders
    non_responders = [v for v in project.vendors if v.status in (VendorStatus.PENDING, VendorStatus.CONTACTED)]
    declined = [v for v in project.vendors if v.status == VendorStatus.DECLINED]

    if non_responders or declined:
        lines.append("## Other Vendors")
        lines.append("")

        if non_responders:
            lines.append("**Pending Response:**")
            for v in non_responders:
                lines.append(f"- {v.name}")
            lines.append("")

        if declined:
            lines.append("**Declined to Participate:**")
            for v in declined:
                reason = f" - {v.notes}" if v.notes else ""
                lines.append(f"- {v.name}{reason}")
            lines.append("")

    # Recommendations section (placeholder)
    lines.append("## Recommendations")
    lines.append("")
    lines.append("*Complete detailed technical evaluation and populate this section with:*")
    lines.append("")
    lines.append("1. Recommended vendor(s) with rationale")
    lines.append("2. Risk considerations")
    lines.append("3. Negotiation points")
    lines.append("4. Next steps")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("*Report generated by Vendor Procurement Coordinator*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate vendor quote comparison report")
    parser.add_argument("--project-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Output file path (default: stdout)")
    parser.add_argument("--price-weight", type=int, default=30, help="Price evaluation weight (%%)")
    parser.add_argument("--delivery-weight", type=int, default=25, help="Delivery evaluation weight (%%)")
    parser.add_argument("--technical-weight", type=int, default=25, help="Technical evaluation weight (%%)")
    parser.add_argument("--experience-weight", type=int, default=20, help="Experience evaluation weight (%%)")

    args = parser.parse_args()

    try:
        project = load_project(args.project_dir)

        weights = {
            "price": args.price_weight,
            "delivery": args.delivery_weight,
            "technical": args.technical_weight,
            "experience": args.experience_weight,
        }

        report = generate_comparison_report(project, weights)

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
