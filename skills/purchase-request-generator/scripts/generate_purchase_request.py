#!/usr/bin/env python3
"""
Generate formal purchase request documents from specifications.

This script creates structured purchase request documents in Markdown format,
including all required sections for approval workflows.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def generate_request_id() -> str:
    """Generate a unique request ID based on current date and time."""
    now = datetime.now()
    return f"PR-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def generate_purchase_request(
    product: str,
    vendor: str,
    unit_price: float,
    quantity: int,
    justification: str,
    requester: str,
    department: str,
    specifications: Optional[str] = None,
    urgency: Optional[str] = None,
    budget_code: Optional[str] = None,
    alternatives: Optional[str] = None,
) -> str:
    """
    Generate a formal purchase request document.

    Args:
        product: Product name and model
        vendor: Vendor name
        unit_price: Price per unit
        quantity: Number of units
        justification: Business justification
        requester: Name of requester
        department: Department name
        specifications: Optional product specifications
        urgency: Optional urgency level (Low/Medium/High/Critical)
        budget_code: Optional budget code
        alternatives: Optional alternatives considered

    Returns:
        Markdown formatted purchase request document
    """
    request_id = generate_request_id()
    date = datetime.now().strftime("%Y-%m-%d")
    total_cost = unit_price * quantity

    document = f"""# Purchase Request

## Request Information

| Field | Value |
|-------|-------|
| Request ID | {request_id} |
| Date | {date} |
| Requester | {requester} |
| Department | {department} |
| Urgency | {urgency or "Medium"} |

## Product Details

| Field | Value |
|-------|-------|
| Product | {product} |
| Vendor | {vendor} |
| Quantity | {quantity} |
| Unit Price | {format_currency(unit_price)} |
| **Total Cost** | **{format_currency(total_cost)}** |

"""

    if specifications:
        document += f"""### Specifications

{specifications}

"""

    document += f"""## Business Justification

{justification}

"""

    if alternatives:
        document += f"""## Alternatives Considered

{alternatives}

"""

    document += f"""## Budget Information

| Field | Value |
|-------|-------|
| Budget Code | {budget_code or "TBD"} |
| Fiscal Year | FY{datetime.now().year} |
| Amount Requested | {format_currency(total_cost)} |

## Approval Status

| Approver | Role | Status | Date |
|----------|------|--------|------|
| TBD | Manager | Pending | - |
| TBD | Director | Pending | - |
| TBD | Finance | Pending | - |

## Supporting Documents

- [ ] Vendor Quote
- [ ] Product Specifications
- [ ] Cost-Benefit Analysis

---

*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    return document


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Generate formal purchase request documents")
    parser.add_argument("--product", "-p", required=True, help="Product name and model")
    parser.add_argument("--vendor", "-v", required=True, help="Vendor name")
    parser.add_argument("--unit-price", "-u", type=float, required=True, help="Price per unit")
    parser.add_argument("--quantity", "-q", type=int, required=True, help="Number of units")
    parser.add_argument("--justification", "-j", required=True, help="Business justification")
    parser.add_argument("--requester", "-r", required=True, help="Requester name")
    parser.add_argument("--department", "-d", required=True, help="Department name")
    parser.add_argument("--specifications", "-s", help="Product specifications")
    parser.add_argument(
        "--urgency", choices=["Low", "Medium", "High", "Critical"], default="Medium", help="Urgency level"
    )
    parser.add_argument("--budget-code", "-b", help="Budget code")
    parser.add_argument("--alternatives", "-a", help="Alternatives considered")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        document = generate_purchase_request(
            product=args.product,
            vendor=args.vendor,
            unit_price=args.unit_price,
            quantity=args.quantity,
            justification=args.justification,
            requester=args.requester,
            department=args.department,
            specifications=args.specifications,
            urgency=args.urgency,
            budget_code=args.budget_code,
            alternatives=args.alternatives,
        )

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(document, encoding="utf-8")
            print(f"Purchase request saved to: {output_path}", file=sys.stderr)
        else:
            print(document)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
