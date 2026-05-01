#!/usr/bin/env python3
"""
Generate vendor comparison matrices for purchase requests.

This script creates structured vendor comparison documents with weighted scoring.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def parse_vendors(vendors_str: str) -> Dict[str, float]:
    """
    Parse vendors string into dictionary.

    Args:
        vendors_str: Comma-separated vendors in format "name:price,name:price"

    Returns:
        Dictionary of vendor name to price
    """
    vendors = {}
    for item in vendors_str.split(","):
        item = item.strip()
        if ":" in item:
            name, price = item.rsplit(":", 1)
            try:
                vendors[name.strip()] = float(price.strip())
            except ValueError:
                continue
    return vendors


def parse_criteria(criteria_str: str) -> List[str]:
    """
    Parse criteria string into list.

    Args:
        criteria_str: Comma-separated criteria names

    Returns:
        List of criteria names
    """
    return [c.strip() for c in criteria_str.split(",") if c.strip()]


def parse_scores(scores_str: str, vendors: Dict[str, float], criteria: List[str]) -> Dict[str, Dict[str, int]]:
    """
    Parse scores string into nested dictionary.

    Args:
        scores_str: Scores in format "Vendor A:4,5,4,3|Vendor B:3,4,5,4"
        vendors: Dictionary of vendors
        criteria: List of criteria names

    Returns:
        Dictionary of vendor -> criterion -> score
    """
    scores = {}
    for vendor_scores in scores_str.split("|"):
        vendor_scores = vendor_scores.strip()
        if ":" in vendor_scores:
            vendor_name, score_values = vendor_scores.split(":", 1)
            vendor_name = vendor_name.strip()
            if vendor_name in vendors:
                score_list = [int(s.strip()) for s in score_values.split(",") if s.strip()]
                scores[vendor_name] = {}
                for i, criterion in enumerate(criteria):
                    if i < len(score_list):
                        scores[vendor_name][criterion] = score_list[i]
    return scores


def parse_weights(weights_str: str, criteria: List[str]) -> Dict[str, float]:
    """
    Parse weights string into dictionary.

    Args:
        weights_str: Comma-separated weights as percentages
        criteria: List of criteria names

    Returns:
        Dictionary of criterion to weight (0-1)
    """
    weights = {}
    weight_values = [float(w.strip()) for w in weights_str.split(",") if w.strip()]
    for i, criterion in enumerate(criteria):
        if i < len(weight_values):
            weights[criterion] = weight_values[i] / 100.0
        else:
            weights[criterion] = 1.0 / len(criteria)
    return weights


def calculate_weighted_score(scores: Dict[str, int], weights: Dict[str, float]) -> float:
    """
    Calculate weighted total score for a vendor.

    Args:
        scores: Dictionary of criterion to score
        weights: Dictionary of criterion to weight

    Returns:
        Weighted total score
    """
    total = 0.0
    for criterion, score in scores.items():
        weight = weights.get(criterion, 0.0)
        total += score * weight
    return total


def generate_vendor_comparison(
    vendors: Dict[str, float],
    criteria: List[str],
    scores: Dict[str, Dict[str, int]],
    weights: Dict[str, float],
    product: str = "Product",
) -> str:
    """
    Generate a vendor comparison document.

    Args:
        vendors: Dictionary of vendor name to price
        criteria: List of evaluation criteria
        scores: Nested dictionary of scores
        weights: Dictionary of criterion to weight
        product: Product name

    Returns:
        Markdown formatted vendor comparison document
    """
    # Calculate weighted scores
    vendor_totals = {}
    for vendor_name in vendors:
        if vendor_name in scores:
            vendor_totals[vendor_name] = calculate_weighted_score(scores[vendor_name], weights)
        else:
            vendor_totals[vendor_name] = 0.0

    # Rank vendors
    ranked_vendors = sorted(vendor_totals.items(), key=lambda x: x[1], reverse=True)
    recommended_vendor = ranked_vendors[0][0] if ranked_vendors else None

    document = f"""# Vendor Comparison Analysis

## Overview

This analysis compares {len(vendors)} vendors for the procurement of **{product}**.

**Recommendation:** {recommended_vendor or "No clear recommendation"} (Highest weighted score: {vendor_totals.get(recommended_vendor, 0):.2f})

---

## Vendor Summary

| Vendor | Price | Weighted Score | Rank |
|--------|------:|:--------------:|:----:|
"""

    for rank, (vendor_name, score) in enumerate(ranked_vendors, 1):
        price = vendors.get(vendor_name, 0)
        document += f"| {vendor_name} | {format_currency(price)} | {score:.2f} | {rank} |\n"

    document += """
---

## Evaluation Criteria

| Criterion | Weight |
|-----------|-------:|
"""

    for criterion in criteria:
        weight = weights.get(criterion, 0)
        document += f"| {criterion} | {weight * 100:.0f}% |\n"

    document += """
### Scoring Scale

| Score | Description |
|:-----:|-------------|
| 5 | Excellent - Exceeds requirements |
| 4 | Good - Meets all requirements |
| 3 | Acceptable - Meets minimum requirements |
| 2 | Below Average - Some deficiencies |
| 1 | Poor - Does not meet requirements |

---

## Detailed Comparison Matrix

| Criterion | Weight |"""

    for vendor_name in vendors:
        document += f" {vendor_name} |"
    document += "\n|-----------|-------:|"
    for _ in vendors:
        document += ":------:|"
    document += "\n"

    for criterion in criteria:
        weight = weights.get(criterion, 0)
        document += f"| {criterion} | {weight * 100:.0f}% |"
        for vendor_name in vendors:
            score = scores.get(vendor_name, {}).get(criterion, "-")
            document += f" {score} |"
        document += "\n"

    document += "| **Weighted Total** | |"
    for vendor_name in vendors:
        total = vendor_totals.get(vendor_name, 0)
        document += f" **{total:.2f}** |"
    document += "\n"

    document += """
---

## Price Comparison

| Vendor | Price | Price Rank | Value Score* |
|--------|------:|:----------:|:------------:|
"""

    # Sort by price
    price_ranked = sorted(vendors.items(), key=lambda x: x[1])
    for rank, (vendor_name, price) in enumerate(price_ranked, 1):
        quality_score = vendor_totals.get(vendor_name, 0)
        # Value score = quality score / (price / lowest price)
        lowest_price = price_ranked[0][1] if price_ranked else 1
        price_ratio = price / lowest_price if lowest_price > 0 else 1
        value_score = quality_score / price_ratio if price_ratio > 0 else 0
        document += f"| {vendor_name} | {format_currency(price)} | {rank} | {value_score:.2f} |\n"

    document += """
*Value Score = Weighted Quality Score / Price Ratio (higher is better)

---

## Strengths and Weaknesses

"""

    for vendor_name in vendors:
        vendor_scores = scores.get(vendor_name, {})
        if not vendor_scores:
            continue

        # Find strengths (score >= 4) and weaknesses (score <= 2)
        strengths = [c for c, s in vendor_scores.items() if s >= 4]
        weaknesses = [c for c, s in vendor_scores.items() if s <= 2]

        document += f"### {vendor_name}\n\n"
        document += f"**Price:** {format_currency(vendors[vendor_name])}\n\n"

        if strengths:
            document += "**Strengths:**\n"
            for s in strengths:
                document += f"- {s} (Score: {vendor_scores[s]})\n"
            document += "\n"

        if weaknesses:
            document += "**Weaknesses:**\n"
            for w in weaknesses:
                document += f"- {w} (Score: {vendor_scores[w]})\n"
            document += "\n"

        if not strengths and not weaknesses:
            document += "*Average performance across all criteria*\n\n"

    document += f"""---

## Recommendation

Based on the weighted evaluation:

**Recommended Vendor: {recommended_vendor or "N/A"}**

| Factor | Assessment |
|--------|------------|
| Weighted Score | {vendor_totals.get(recommended_vendor, 0):.2f} / 5.00 |
| Price | {format_currency(vendors.get(recommended_vendor, 0))} |
| Rank | #1 of {len(vendors)} |

### Justification

"""

    if recommended_vendor and recommended_vendor in scores:
        rec_scores = scores[recommended_vendor]
        high_scores = [c for c, s in rec_scores.items() if s >= 4]
        if high_scores:
            document += f"{recommended_vendor} demonstrates strong performance in: {', '.join(high_scores)}.\n\n"

    document += """### Alternative Considerations

"""

    for rank, (vendor_name, score) in enumerate(ranked_vendors[1:], 2):
        price_diff = vendors.get(vendor_name, 0) - vendors.get(recommended_vendor, 0)
        document += f"- **{vendor_name}** (Rank #{rank}): Score {score:.2f}, "
        if price_diff < 0:
            document += f"saves {format_currency(abs(price_diff))}\n"
        elif price_diff > 0:
            document += f"costs {format_currency(price_diff)} more\n"
        else:
            document += "same price\n"

    document += f"""
---

*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    return document


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Generate vendor comparison documents")
    parser.add_argument(
        "--vendors", "-v", required=True, help="Vendors and prices (format: 'Vendor A:4500,Vendor B:5000')"
    )
    parser.add_argument(
        "--criteria", "-c", required=True, help="Evaluation criteria (format: 'Price,Support,Warranty,Delivery')"
    )
    parser.add_argument(
        "--scores", "-s", required=True, help="Scores per vendor (format: 'Vendor A:4,5,4,3|Vendor B:3,4,5,4')"
    )
    parser.add_argument("--weights", "-w", help="Weights per criterion as percentages (format: '30,25,25,20')")
    parser.add_argument("--product", "-p", default="Product", help="Product name")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        vendors = parse_vendors(args.vendors)
        criteria = parse_criteria(args.criteria)

        if args.weights:
            weights = parse_weights(args.weights, criteria)
        else:
            # Equal weights if not specified
            weights = {c: 1.0 / len(criteria) for c in criteria}

        scores = parse_scores(args.scores, vendors, criteria)

        document = generate_vendor_comparison(
            vendors=vendors,
            criteria=criteria,
            scores=scores,
            weights=weights,
            product=args.product,
        )

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(document, encoding="utf-8")
            print(f"Vendor comparison saved to: {output_path}", file=sys.stderr)
        else:
            print(document)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
