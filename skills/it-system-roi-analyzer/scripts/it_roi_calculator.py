#!/usr/bin/env python3
"""
IT System ROI Calculator

A command-line tool for calculating ROI, NPV, IRR, and Payback Period
for IT system investments.

Usage:
    python it_roi_calculator.py --investment 50000000 --annual-benefit 15000000 --years 5 --rate 0.10
    python it_roi_calculator.py --input project_data.json --output report.md
"""

import argparse
import json
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ProjectData:
    """Data class for IT project financial data."""

    project_name: str
    initial_investment: float
    annual_operating_cost: float
    annual_benefits: Dict[str, float]
    discount_rate: float


@dataclass
class FinancialMetrics:
    """Data class for calculated financial metrics."""

    roi: float
    npv: float
    irr: float
    payback_period: float
    total_benefits: float
    total_costs: float
    cash_flows: List[float]


class ITROICalculator:
    """Calculator for IT System ROI analysis."""

    @staticmethod
    def calculate_roi(total_benefits: float, total_investment: float) -> float:
        """
        Calculate Return on Investment (ROI).

        Args:
            total_benefits: Total benefits over the period
            total_investment: Total investment including operating costs

        Returns:
            ROI as a percentage
        """
        if total_investment == 0:
            return 0.0
        return ((total_benefits - total_investment) / total_investment) * 100

    @staticmethod
    def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
        """
        Calculate Net Present Value (NPV).

        Args:
            cash_flows: List of cash flows starting from Year 0
            discount_rate: Discount rate (e.g., 0.10 for 10%)

        Returns:
            NPV value
        """
        npv = 0.0
        for t, cf in enumerate(cash_flows):
            npv += cf / ((1 + discount_rate) ** t)
        return npv

    @staticmethod
    def calculate_irr(
        cash_flows: List[float], guess: float = 0.10, tolerance: float = 0.0001, max_iterations: int = 100
    ) -> float:
        """
        Calculate Internal Rate of Return (IRR) using Newton-Raphson method.

        Args:
            cash_flows: List of cash flows starting from Year 0
            guess: Initial guess for IRR
            tolerance: Convergence tolerance
            max_iterations: Maximum number of iterations

        Returns:
            IRR as a decimal (e.g., 0.15 for 15%)
        """
        rate = guess

        for _ in range(max_iterations):
            # Calculate NPV at current rate
            npv = sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cash_flows))

            if abs(npv) < tolerance:
                return rate

            # Calculate derivative of NPV
            derivative = sum(-t * cf / ((1 + rate) ** (t + 1)) for t, cf in enumerate(cash_flows))

            if derivative == 0:
                break

            # Newton-Raphson update
            rate = rate - npv / derivative

            # Prevent rate from going too negative or too high
            if rate < -0.99:
                rate = -0.99
            elif rate > 10:
                rate = 10

        return rate

    @staticmethod
    def calculate_payback_period(initial_investment: float, annual_cash_flows: List[float]) -> float:
        """
        Calculate Payback Period.

        Args:
            initial_investment: Initial investment (positive value)
            annual_cash_flows: List of annual net cash flows (starting from Year 1)

        Returns:
            Payback period in years
        """
        cumulative = -initial_investment

        for year, cf in enumerate(annual_cash_flows, start=1):
            if cumulative + cf >= 0:
                # Linear interpolation for partial year
                fraction = -cumulative / cf
                return year - 1 + fraction
            cumulative += cf

        # If payback not achieved within the period
        return float("inf")

    def sensitivity_analysis(
        self, base_metrics: FinancialMetrics, project_data: ProjectData
    ) -> Dict[str, FinancialMetrics]:
        """
        Perform sensitivity analysis with multiple scenarios.

        Args:
            base_metrics: Base case financial metrics
            project_data: Original project data

        Returns:
            Dictionary of scenario names to financial metrics
        """
        scenarios = {
            "optimistic": {"benefit_factor": 1.20, "cost_factor": 0.90},
            "base": {"benefit_factor": 1.00, "cost_factor": 1.00},
            "pessimistic": {"benefit_factor": 0.80, "cost_factor": 1.10},
            "worst_case": {"benefit_factor": 0.70, "cost_factor": 1.20},
        }

        results = {}

        for scenario_name, factors in scenarios.items():
            # Adjust benefits and costs
            adjusted_benefits = {k: v * factors["benefit_factor"] for k, v in project_data.annual_benefits.items()}
            adjusted_op_cost = project_data.annual_operating_cost * factors["cost_factor"]

            # Calculate metrics for this scenario
            metrics = self.calculate_all_metrics(
                project_data.initial_investment,
                adjusted_op_cost,
                list(adjusted_benefits.values()),
                project_data.discount_rate,
            )

            results[scenario_name] = metrics

        return results

    def calculate_all_metrics(
        self,
        initial_investment: float,
        annual_operating_cost: float,
        annual_benefits: List[float],
        discount_rate: float,
    ) -> FinancialMetrics:
        """
        Calculate all financial metrics.

        Args:
            initial_investment: Initial investment amount
            annual_operating_cost: Annual operating cost
            annual_benefits: List of annual benefits
            discount_rate: Discount rate

        Returns:
            FinancialMetrics object with all calculated values
        """
        years = len(annual_benefits)

        # Build cash flows
        cash_flows = [-initial_investment]
        annual_net_cfs = []

        for i, benefit in enumerate(annual_benefits):
            net_cf = benefit - annual_operating_cost
            cash_flows.append(net_cf)
            annual_net_cfs.append(net_cf)

        # Calculate totals
        total_benefits = sum(annual_benefits)
        total_costs = initial_investment + (annual_operating_cost * years)

        # Calculate metrics
        roi = self.calculate_roi(total_benefits, total_costs)
        npv = self.calculate_npv(cash_flows, discount_rate)
        irr = self.calculate_irr(cash_flows)
        payback = self.calculate_payback_period(initial_investment, annual_net_cfs)

        return FinancialMetrics(
            roi=roi,
            npv=npv,
            irr=irr,
            payback_period=payback,
            total_benefits=total_benefits,
            total_costs=total_costs,
            cash_flows=cash_flows,
        )


def format_currency(amount: float, currency: str = "$") -> str:
    """Format amount as currency string."""
    if abs(amount) >= 1_000_000:
        return f"{currency}{amount / 1_000_000:,.2f}M"
    elif abs(amount) >= 1_000:
        return f"{currency}{amount / 1_000:,.1f}K"
    else:
        return f"{currency}{amount:,.0f}"


def format_currency_jp(amount: float) -> str:
    """Format amount as Japanese currency (万円)."""
    if abs(amount) >= 100_000_000:
        return f"{amount / 100_000_000:,.1f}億円"
    else:
        return f"{amount / 10_000:,.0f}万円"


def generate_report(
    project_name: str,
    metrics: FinancialMetrics,
    sensitivity: Dict[str, FinancialMetrics],
    initial_investment: float,
    annual_operating_cost: float,
    discount_rate: float,
) -> str:
    """Generate a markdown report of the analysis."""

    report = f"""# {project_name} - ROI Analysis Report

## Executive Summary

| Metric | Value | Assessment |
|--------|-------|------------|
| ROI (5-Year) | {metrics.roi:.1f}% | {"Excellent" if metrics.roi > 100 else "Good" if metrics.roi > 50 else "Acceptable" if metrics.roi > 20 else "Needs Review"} |
| NPV (Rate {discount_rate * 100:.0f}%) | {format_currency(metrics.npv)} | {"Positive" if metrics.npv > 0 else "Negative"} |
| IRR | {metrics.irr * 100:.1f}% | {"Above WACC" if metrics.irr > discount_rate else "Below WACC"} |
| Payback Period | {metrics.payback_period:.2f} years | {"Good" if metrics.payback_period < 3 else "Acceptable" if metrics.payback_period < 5 else "High Risk"} |

## Investment Summary

- **Initial Investment**: {format_currency(initial_investment)}
- **Annual Operating Cost**: {format_currency(annual_operating_cost)}
- **5-Year Total Costs**: {format_currency(metrics.total_costs)}
- **5-Year Total Benefits**: {format_currency(metrics.total_benefits)}
- **Net Profit**: {format_currency(metrics.total_benefits - metrics.total_costs)}

## Cash Flow Analysis

| Year | Cash Flow | Cumulative |
|------|-----------|------------|
"""

    cumulative = 0
    for i, cf in enumerate(metrics.cash_flows):
        cumulative += cf
        year_label = "Year 0 (Initial)" if i == 0 else f"Year {i}"
        report += f"| {year_label} | {format_currency(cf)} | {format_currency(cumulative)} |\n"

    report += """
## Sensitivity Analysis

| Scenario | NPV | ROI | IRR | Payback |
|----------|-----|-----|-----|---------|
"""

    scenario_names = {
        "optimistic": "Optimistic (+20% benefits, -10% costs)",
        "base": "Base Case",
        "pessimistic": "Pessimistic (-20% benefits, +10% costs)",
        "worst_case": "Worst Case (-30% benefits, +20% costs)",
    }

    for scenario_key in ["optimistic", "base", "pessimistic", "worst_case"]:
        m = sensitivity[scenario_key]
        payback_str = f"{m.payback_period:.1f} yrs" if m.payback_period != float("inf") else "N/A"
        report += f"| {scenario_names[scenario_key]} | {format_currency(m.npv)} | {m.roi:.0f}% | {m.irr * 100:.0f}% | {payback_str} |\n"

    report += f"""
## Recommendation

{"**APPROVED**: Strong financial returns justify investment." if metrics.npv > 0 and metrics.roi > 50 else "**CONDITIONALLY APPROVED**: Acceptable returns with moderate risk." if metrics.npv > 0 else "**NOT RECOMMENDED**: Negative NPV indicates value destruction."}

---
*Generated by IT ROI Calculator*
"""

    return report


def main():
    parser = argparse.ArgumentParser(
        description="IT System ROI Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic calculation:
    python it_roi_calculator.py --investment 50000000 --annual-benefit 15000000 --years 5 --rate 0.10

  From JSON file:
    python it_roi_calculator.py --input project_data.json --output report.md
        """,
    )

    parser.add_argument("--investment", "-i", type=float, help="Initial investment amount")
    parser.add_argument("--annual-benefit", "-b", type=float, help="Annual benefit amount")
    parser.add_argument("--annual-cost", "-c", type=float, default=0, help="Annual operating cost (default: 0)")
    parser.add_argument("--years", "-y", type=int, default=5, help="Analysis period in years (default: 5)")
    parser.add_argument("--rate", "-r", type=float, default=0.10, help="Discount rate (default: 0.10)")
    parser.add_argument("--input", type=str, help="Input JSON file path")
    parser.add_argument("--output", "-o", type=str, help="Output file path (markdown)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    calculator = ITROICalculator()

    # Load data from JSON or command line
    if args.input:
        with open(args.input, "r") as f:
            data = json.load(f)

        project_data = ProjectData(
            project_name=data.get("project_name", "IT Project"),
            initial_investment=data["initial_investment"],
            annual_operating_cost=data.get("annual_operating_cost", 0),
            annual_benefits=data.get("annual_benefits", {}),
            discount_rate=data.get("discount_rate", 0.10),
        )

        annual_benefits_list = list(project_data.annual_benefits.values())

    else:
        if not args.investment or not args.annual_benefit:
            parser.error("--investment and --annual-benefit are required when not using --input")

        project_data = ProjectData(
            project_name="IT Project",
            initial_investment=args.investment,
            annual_operating_cost=args.annual_cost,
            annual_benefits={f"year{i}": args.annual_benefit for i in range(1, args.years + 1)},
            discount_rate=args.rate,
        )

        annual_benefits_list = [args.annual_benefit] * args.years

    # Calculate metrics
    metrics = calculator.calculate_all_metrics(
        project_data.initial_investment,
        project_data.annual_operating_cost,
        annual_benefits_list,
        project_data.discount_rate,
    )

    # Perform sensitivity analysis
    sensitivity = calculator.sensitivity_analysis(metrics, project_data)

    # Output results
    if args.json:
        result = {
            "roi": metrics.roi,
            "npv": metrics.npv,
            "irr": metrics.irr * 100,
            "payback_period": metrics.payback_period,
            "total_benefits": metrics.total_benefits,
            "total_costs": metrics.total_costs,
            "cash_flows": metrics.cash_flows,
            "sensitivity": {
                k: {"roi": v.roi, "npv": v.npv, "irr": v.irr * 100, "payback_period": v.payback_period}
                for k, v in sensitivity.items()
            },
        }
        print(json.dumps(result, indent=2))

    else:
        # Generate report
        report = generate_report(
            project_data.project_name,
            metrics,
            sensitivity,
            project_data.initial_investment,
            project_data.annual_operating_cost,
            project_data.discount_rate,
        )

        if args.output:
            with open(args.output, "w") as f:
                f.write(report)
            print(f"Report saved to: {args.output}")
        else:
            print(report)


if __name__ == "__main__":
    main()
