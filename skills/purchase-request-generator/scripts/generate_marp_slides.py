#!/usr/bin/env python3
"""
Generate MARP presentation slides for purchase request approval.

This script creates MARP-formatted markdown slides suitable for management
approval meetings.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def parse_list(items_str: str) -> List[str]:
    """
    Parse comma-separated string into list.

    Args:
        items_str: Comma-separated items

    Returns:
        List of items
    """
    return [item.strip() for item in items_str.split(",") if item.strip()]


def generate_marp_slides(
    title: str,
    product: str,
    total_cost: float,
    roi_percent: float,
    payback_months: float,
    key_benefits: List[str],
    requester: str = "Requester",
    department: str = "Department",
    vendor: str = "Vendor",
    justification: str = "",
    risks: Optional[List[str]] = None,
    npv: Optional[float] = None,
    alternatives: Optional[List[str]] = None,
) -> str:
    """
    Generate MARP presentation slides.

    Args:
        title: Presentation title
        product: Product name
        total_cost: Total cost
        roi_percent: ROI percentage
        payback_months: Payback period in months
        key_benefits: List of key benefits
        requester: Requester name
        department: Department name
        vendor: Vendor name
        justification: Business justification text
        risks: Optional list of risks
        npv: Optional NPV value
        alternatives: Optional list of alternatives considered

    Returns:
        MARP-formatted markdown slides
    """
    date = datetime.now().strftime("%Y-%m-%d")
    request_id = f"PR-{datetime.now().strftime('%Y%m%d')}"

    # Determine recommendation strength
    if roi_percent > 100 and payback_months < 24:
        recommendation = "Strong Approval Recommended"
        rec_color = "green"
    elif roi_percent > 50 or payback_months < 36:
        recommendation = "Approval Recommended"
        rec_color = "blue"
    else:
        recommendation = "Review Recommended"
        rec_color = "orange"

    slides = f"""---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {{
    background-color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }}
  h1 {{
    color: #1a365d;
    border-bottom: 3px solid #2b6cb0;
    padding-bottom: 10px;
  }}
  h2 {{
    color: #2b6cb0;
  }}
  table {{
    font-size: 0.85em;
    margin: 0 auto;
  }}
  th {{
    background-color: #2b6cb0;
    color: white;
  }}
  .green {{ color: #22543d; }}
  .blue {{ color: #2b6cb0; }}
  .orange {{ color: #c05621; }}
  .red {{ color: #c53030; }}
  .highlight {{
    background-color: #bee3f8;
    padding: 10px 20px;
    border-radius: 8px;
    display: inline-block;
  }}
  .metric-box {{
    background-color: #e2e8f0;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    margin: 5px;
  }}
---

# {title}

## {department} | {date}

**Request ID:** {request_id}
**Requester:** {requester}

---

# Executive Summary

## Purchase Request Overview

| Item | Details |
|------|---------|
| **Product** | {product} |
| **Vendor** | {vendor} |
| **Total Cost** | {format_currency(total_cost)} |

## Financial Metrics

| ROI | Payback Period |{" NPV |" if npv is not None else ""}
|:---:|:--------------:|{":---:|" if npv is not None else ""}
| **{roi_percent:.0f}%** | **{payback_months:.0f} months** |{f" **{format_currency(npv)}** |" if npv is not None else ""}

---

# Business Justification

"""

    if justification:
        slides += f"""{justification}

"""
    else:
        slides += """## Why This Purchase?

- Business need description
- Current pain points
- Expected improvements

"""

    slides += """---

# Key Benefits

"""

    for i, benefit in enumerate(key_benefits[:6], 1):
        slides += f"{i}. **{benefit}**\n"

    slides += f"""
---

# Financial Analysis

## Cost-Benefit Summary

| Metric | Value | Assessment |
|--------|------:|------------|
| Total Investment | {format_currency(total_cost)} | Initial cost |
| ROI | {roi_percent:.0f}% | {"Excellent" if roi_percent > 100 else "Good" if roi_percent > 50 else "Moderate"} |
| Payback Period | {payback_months:.0f} months | {"< 1 year" if payback_months < 12 else "< 2 years" if payback_months < 24 else "< 3 years" if payback_months < 36 else "> 3 years"} |
"""

    if npv is not None:
        slides += f"| NPV | {format_currency(npv)} | {'Positive' if npv > 0 else 'Negative'} |\n"

    slides += """
---

# ROI Breakdown

## Return on Investment Analysis

"""

    # Visual ROI representation
    if roi_percent >= 100:
        slides += f"""<div class="metric-box">
<h3 class="green">ROI: {roi_percent:.0f}%</h3>
<p>Investment returns <strong>{roi_percent / 100:.1f}x</strong> its cost</p>
</div>

"""
    else:
        slides += f"""<div class="metric-box">
<h3 class="blue">ROI: {roi_percent:.0f}%</h3>
<p>Investment returns <strong>{roi_percent:.0f}%</strong> of its cost</p>
</div>

"""

    slides += f"""**Payback:** Initial investment recovered in **{payback_months:.0f} months** ({payback_months / 12:.1f} years)

---

"""

    # Add alternatives slide if provided
    if alternatives and len(alternatives) > 0:
        slides += """# Alternatives Considered

| Option | Status |
|--------|--------|
"""
        for alt in alternatives[:5]:
            slides += f"| {alt} | Evaluated |\n"

        slides += f"""| **{product}** | **Recommended** |

---

"""

    # Add risks slide if provided
    if risks and len(risks) > 0:
        slides += """# Risk Assessment

| Risk | Mitigation |
|------|------------|
"""
        for risk in risks[:5]:
            slides += f"| {risk} | Mitigation plan TBD |\n"

        slides += """
---

"""

    slides += f"""# Implementation Timeline

## Proposed Schedule

| Phase | Timeline |
|-------|----------|
| Approval | Week 1 |
| Procurement | Week 2-3 |
| Delivery | Week 4 |
| Setup/Installation | Week 5 |
| Training | Week 6 |
| Go-Live | Week 7 |

---

# Recommendation

<div class="highlight">

## <span class="{rec_color}">{recommendation}</span>

</div>

**Approve the purchase of {product} for {format_currency(total_cost)}**

### Key Points

- ROI of **{roi_percent:.0f}%** {"exceeds" if roi_percent > 100 else "meets"} investment criteria
- Payback in **{payback_months:.0f} months** {"demonstrates" if payback_months < 24 else "shows"} {"rapid" if payback_months < 12 else "acceptable"} return
"""

    if npv is not None and npv > 0:
        slides += f"- Positive NPV of **{format_currency(npv)}** confirms value creation\n"

    slides += f"""
---

# Questions?

## Contact Information

**Requester:** {requester}
**Department:** {department}

### Supporting Documents Available

- Detailed Cost-Benefit Analysis
- Vendor Quote(s)
- Product Specifications
- Risk Assessment

---

*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    return slides


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Generate MARP presentation slides for purchase approval")
    parser.add_argument("--title", "-t", required=True, help="Presentation title")
    parser.add_argument("--product", "-p", required=True, help="Product name")
    parser.add_argument("--total-cost", "-c", type=float, required=True, help="Total cost")
    parser.add_argument("--roi-percent", "-r", type=float, required=True, help="ROI percentage")
    parser.add_argument("--payback-months", "-m", type=float, required=True, help="Payback period in months")
    parser.add_argument("--key-benefits", "-b", required=True, help="Key benefits (comma-separated)")
    parser.add_argument("--requester", default="Requester", help="Requester name")
    parser.add_argument("--department", "-d", default="Department", help="Department name")
    parser.add_argument("--vendor", "-v", default="Vendor", help="Vendor name")
    parser.add_argument("--justification", "-j", help="Business justification text")
    parser.add_argument("--risks", help="Risks (comma-separated)")
    parser.add_argument("--npv", type=float, help="Net Present Value")
    parser.add_argument("--alternatives", "-a", help="Alternatives considered (comma-separated)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        key_benefits = parse_list(args.key_benefits)
        risks = parse_list(args.risks) if args.risks else None
        alternatives = parse_list(args.alternatives) if args.alternatives else None

        slides = generate_marp_slides(
            title=args.title,
            product=args.product,
            total_cost=args.total_cost,
            roi_percent=args.roi_percent,
            payback_months=args.payback_months,
            key_benefits=key_benefits,
            requester=args.requester,
            department=args.department,
            vendor=args.vendor,
            justification=args.justification or "",
            risks=risks,
            npv=args.npv,
            alternatives=alternatives,
        )

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(slides, encoding="utf-8")
            print(f"MARP slides saved to: {output_path}", file=sys.stderr)
        else:
            print(slides)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
