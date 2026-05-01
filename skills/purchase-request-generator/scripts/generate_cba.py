#!/usr/bin/env python3
"""
Generate cost-benefit analysis documents for purchase requests.

This script creates detailed CBA documents with ROI, NPV, and payback calculations.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def calculate_roi(total_benefit: float, total_cost: float) -> float:
    """
    Calculate Return on Investment.

    Args:
        total_benefit: Total benefits over the analysis period
        total_cost: Total costs including initial and ongoing

    Returns:
        ROI as a percentage
    """
    if total_cost <= 0:
        return 0.0
    return ((total_benefit - total_cost) / total_cost) * 100


def calculate_payback_months(initial_cost: float, monthly_benefit: float) -> float:
    """
    Calculate payback period in months.

    Args:
        initial_cost: Initial investment cost
        monthly_benefit: Monthly benefit amount

    Returns:
        Payback period in months
    """
    if monthly_benefit <= 0:
        return float("inf")
    return initial_cost / monthly_benefit


def calculate_npv(
    initial_cost: float,
    annual_benefit: float,
    annual_cost: float,
    years: int,
    discount_rate: float = 0.10,
) -> float:
    """
    Calculate Net Present Value.

    Args:
        initial_cost: Initial investment
        annual_benefit: Annual benefit amount
        annual_cost: Annual operating cost
        years: Analysis period in years
        discount_rate: Discount rate (default 10%)

    Returns:
        NPV value
    """
    npv = -initial_cost
    net_annual_cash_flow = annual_benefit - annual_cost

    for year in range(1, years + 1):
        npv += net_annual_cash_flow / ((1 + discount_rate) ** year)

    return npv


def parse_benefits(benefits_str: str) -> List[Tuple[str, float]]:
    """
    Parse benefits string into list of tuples.

    Args:
        benefits_str: Comma-separated benefits in format "name:value,name:value"

    Returns:
        List of (name, value) tuples
    """
    benefits = []
    if not benefits_str:
        return benefits

    for item in benefits_str.split(","):
        item = item.strip()
        if ":" in item:
            name, value = item.rsplit(":", 1)
            try:
                benefits.append((name.strip(), float(value.strip())))
            except ValueError:
                continue
    return benefits


def generate_cba(
    product: str,
    total_cost: float,
    useful_life_years: int,
    annual_benefit: float,
    benefit_description: str,
    annual_operating_cost: float = 0.0,
    training_cost: float = 0.0,
    benefits_breakdown: Optional[str] = None,
    discount_rate: float = 0.10,
) -> str:
    """
    Generate a cost-benefit analysis document.

    Args:
        product: Product name
        total_cost: Initial purchase cost
        useful_life_years: Expected useful life in years
        annual_benefit: Annual monetary benefit
        benefit_description: Description of benefits
        annual_operating_cost: Annual operating/maintenance cost
        training_cost: One-time training cost
        benefits_breakdown: Optional breakdown of benefits
        discount_rate: Discount rate for NPV calculation

    Returns:
        Markdown formatted CBA document
    """
    # Calculate metrics
    initial_investment = total_cost + training_cost
    total_operating = annual_operating_cost * useful_life_years
    total_tco = initial_investment + total_operating
    total_benefits = annual_benefit * useful_life_years

    roi = calculate_roi(total_benefits, total_tco)
    monthly_benefit = annual_benefit / 12
    payback_months = calculate_payback_months(initial_investment, monthly_benefit)
    npv = calculate_npv(
        initial_investment,
        annual_benefit,
        annual_operating_cost,
        useful_life_years,
        discount_rate,
    )

    # Parse benefits breakdown if provided
    benefits_list = parse_benefits(benefits_breakdown) if benefits_breakdown else []

    document = f"""# Cost-Benefit Analysis

## Executive Summary

This cost-benefit analysis evaluates the purchase of **{product}** with a total initial investment of {format_currency(initial_investment)} over a {useful_life_years}-year period.

| Metric | Value | Assessment |
|--------|-------|------------|
| ROI | {roi:.1f}% | {"Strong" if roi > 100 else "Moderate" if roi > 50 else "Weak"} |
| Payback Period | {payback_months:.1f} months | {"Excellent" if payback_months < 12 else "Good" if payback_months < 24 else "Acceptable" if payback_months < 36 else "Extended"} |
| NPV | {format_currency(npv)} | {"Positive" if npv > 0 else "Break-even" if npv == 0 else "Negative"} |

**Recommendation:** {"Approve - Strong financial justification" if roi > 100 and npv > 0 else "Approve with monitoring" if roi > 50 or npv > 0 else "Review alternatives"}

---

## Cost Analysis

### Initial Costs

| Cost Item | Amount |
|-----------|-------:|
| Purchase Price | {format_currency(total_cost)} |
| Training | {format_currency(training_cost)} |
| **Total Initial Investment** | **{format_currency(initial_investment)}** |

### Ongoing Costs (Annual)

| Cost Item | Amount |
|-----------|-------:|
| Operating/Maintenance | {format_currency(annual_operating_cost)} |
| **Total Annual Cost** | **{format_currency(annual_operating_cost)}** |

### Total Cost of Ownership ({useful_life_years} Years)

| Cost Category | Amount |
|---------------|-------:|
| Initial Investment | {format_currency(initial_investment)} |
| Operating ({useful_life_years} years) | {format_currency(total_operating)} |
| **Total TCO** | **{format_currency(total_tco)}** |

---

## Benefit Analysis

### Benefit Description

{benefit_description}

### Quantified Benefits

| Benefit | Annual Value |
|---------|-------------:|
"""

    if benefits_list:
        for name, value in benefits_list:
            document += f"| {name} | {format_currency(value)} |\n"
        document += f"| **Total Annual Benefit** | **{format_currency(annual_benefit)}** |\n"
    else:
        document += f"| Primary Benefit | {format_currency(annual_benefit)} |\n"
        document += f"| **Total Annual Benefit** | **{format_currency(annual_benefit)}** |\n"

    document += f"""
### Total Benefits ({useful_life_years} Years)

| Metric | Value |
|--------|------:|
| Annual Benefit | {format_currency(annual_benefit)} |
| Total Benefit ({useful_life_years} years) | {format_currency(total_benefits)} |
| **Net Benefit** | **{format_currency(total_benefits - total_tco)}** |

---

## Financial Analysis

### Return on Investment (ROI)

```
ROI = (Total Benefits - Total Costs) / Total Costs × 100
ROI = ({format_currency(total_benefits)} - {format_currency(total_tco)}) / {format_currency(total_tco)} × 100
ROI = {roi:.1f}%
```

**Interpretation:** {"Investment generates significant returns exceeding costs" if roi > 100 else "Investment returns positive but moderate" if roi > 50 else "Investment returns are marginal; consider alternatives"}

### Payback Period

```
Payback = Initial Investment / Monthly Benefit
Payback = {format_currency(initial_investment)} / {format_currency(monthly_benefit)}
Payback = {payback_months:.1f} months ({payback_months / 12:.1f} years)
```

**Interpretation:** {"Excellent payback under 1 year" if payback_months < 12 else "Good payback within 2 years" if payback_months < 24 else "Acceptable payback within 3 years" if payback_months < 36 else "Extended payback; may need additional justification"}

### Net Present Value (NPV)

Using discount rate of {discount_rate * 100:.0f}%:

```
NPV = Σ (Net Cash Flow_t / (1 + r)^t) - Initial Investment
NPV = {format_currency(npv)}
```

**Interpretation:** {"Positive NPV indicates value creation" if npv > 0 else "Break-even NPV" if abs(npv) < 100 else "Negative NPV indicates value destruction; review alternatives"}

---

## Sensitivity Analysis

### Break-Even Analysis

| Scenario | Required Value |
|----------|----------------|
| Minimum Annual Benefit for Break-Even | {format_currency(total_tco / useful_life_years)} |
| Maximum Acceptable Initial Cost | {format_currency(total_benefits - total_operating)} |

### Risk Scenarios

| Scenario | ROI | Payback | Assessment |
|----------|-----|---------|------------|
| Base Case | {roi:.1f}% | {payback_months:.1f} mo | Baseline |
| Benefit -20% | {calculate_roi(total_benefits * 0.8, total_tco):.1f}% | {calculate_payback_months(initial_investment, monthly_benefit * 0.8):.1f} mo | {"Still viable" if calculate_roi(total_benefits * 0.8, total_tco) > 0 else "Review"} |
| Cost +20% | {calculate_roi(total_benefits, total_tco * 1.2):.1f}% | {calculate_payback_months(initial_investment * 1.2, monthly_benefit):.1f} mo | {"Still viable" if calculate_roi(total_benefits, total_tco * 1.2) > 0 else "Review"} |

---

## Assumptions

1. Useful life of {useful_life_years} years before replacement
2. Benefits realized from first month of implementation
3. Discount rate of {discount_rate * 100:.0f}% for NPV calculation
4. No salvage value at end of useful life
5. Operating costs remain constant over the period

---

## Recommendation

Based on this analysis:

- **ROI of {roi:.1f}%** {"exceeds" if roi > 100 else "meets" if roi > 50 else "falls below"} typical investment thresholds
- **Payback of {payback_months:.1f} months** {"demonstrates" if payback_months < 24 else "shows"} {"rapid" if payback_months < 12 else "acceptable" if payback_months < 24 else "extended"} cost recovery
- **NPV of {format_currency(npv)}** {"confirms" if npv > 0 else "indicates"} {"value creation" if npv > 0 else "value concern"}

**Overall Recommendation:** {"APPROVE - Strong financial case" if roi > 100 and npv > 0 and payback_months < 24 else "APPROVE WITH MONITORING - Moderate financial case" if roi > 50 or npv > 0 else "REVIEW ALTERNATIVES - Marginal financial case"}

---

*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    return document


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Generate cost-benefit analysis documents")
    parser.add_argument("--product", "-p", required=True, help="Product name")
    parser.add_argument("--total-cost", "-c", type=float, required=True, help="Total purchase cost")
    parser.add_argument("--useful-life-years", "-y", type=int, required=True, help="Expected useful life in years")
    parser.add_argument("--annual-benefit", "-b", type=float, required=True, help="Annual monetary benefit")
    parser.add_argument("--benefit-description", "-d", required=True, help="Description of benefits")
    parser.add_argument(
        "--annual-operating-cost", "-op", type=float, default=0.0, help="Annual operating/maintenance cost"
    )
    parser.add_argument("--training-cost", "-t", type=float, default=0.0, help="One-time training cost")
    parser.add_argument("--benefits-breakdown", help="Benefits breakdown (format: 'name:value,name:value')")
    parser.add_argument("--discount-rate", "-r", type=float, default=0.10, help="Discount rate for NPV (default: 0.10)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        document = generate_cba(
            product=args.product,
            total_cost=args.total_cost,
            useful_life_years=args.useful_life_years,
            annual_benefit=args.annual_benefit,
            benefit_description=args.benefit_description,
            annual_operating_cost=args.annual_operating_cost,
            training_cost=args.training_cost,
            benefits_breakdown=args.benefits_breakdown,
            discount_rate=args.discount_rate,
        )

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(document, encoding="utf-8")
            print(f"Cost-benefit analysis saved to: {output_path}", file=sys.stderr)
        else:
            print(document)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
