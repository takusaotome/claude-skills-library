#!/usr/bin/env python3
"""
Financial Analyzer - Comprehensive Financial Analysis Toolkit
==============================================================

A professional toolkit for financial analysis including:
- Financial ratio analysis (Profitability, Safety, Efficiency)
- DCF/NPV/IRR investment evaluation
- Budget variance analysis
- Sensitivity and scenario analysis

Usage:
    python financial_analyzer.py ratios <input.json> [--output report.md] [--visualize]
    python financial_analyzer.py dcf <project.json> [--discount-rate 0.10]
    python financial_analyzer.py variance <actual.csv> <budget.csv> [--threshold 5]
    python financial_analyzer.py sensitivity <model.json> [--variables revenue,costs]

Examples:
    python financial_analyzer.py ratios company_financials.json --visualize
    python financial_analyzer.py dcf investment_project.json --discount-rate 0.12
    python financial_analyzer.py variance actual_q4.csv budget_q4.csv --threshold 10
"""

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    import numpy as np
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas/numpy not available. Some features may be limited.")

try:
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class FinancialData:
    """Container for financial statement data"""

    company: str
    period: str
    total_assets: float
    current_assets: float
    cash: float
    inventory: float
    receivables: float
    total_liabilities: float
    current_liabilities: float
    long_term_debt: float
    total_equity: float
    revenue: float
    cost_of_goods_sold: float
    gross_profit: float
    operating_expenses: float
    operating_income: float
    interest_expense: float
    net_income: float


@dataclass
class RatioResult:
    """Container for a calculated ratio"""

    name: str
    category: str
    value: float
    interpretation: str
    status: str  # 'strong', 'acceptable', 'weak'


# =============================================================================
# FINANCIAL RATIO ANALYZER
# =============================================================================


class FinancialRatioAnalyzer:
    """Calculate and interpret financial ratios"""

    # Thresholds for ratio interpretation
    THRESHOLDS = {
        "roe": {"strong": 0.15, "acceptable": 0.08},
        "roa": {"strong": 0.08, "acceptable": 0.03},
        "gross_margin": {"strong": 0.40, "acceptable": 0.25},
        "operating_margin": {"strong": 0.15, "acceptable": 0.08},
        "net_margin": {"strong": 0.10, "acceptable": 0.05},
        "current_ratio": {"strong": 2.0, "acceptable": 1.5},
        "quick_ratio": {"strong": 1.5, "acceptable": 1.0},
        "debt_to_equity": {"strong": 0.5, "acceptable": 1.0},  # Inverted: lower is better
        "interest_coverage": {"strong": 5.0, "acceptable": 3.0},
        "asset_turnover": {"strong": 1.5, "acceptable": 0.8},
        "inventory_turnover": {"strong": 8.0, "acceptable": 4.0},
        "receivables_turnover": {"strong": 10.0, "acceptable": 6.0},
    }

    def __init__(self, data: FinancialData):
        self.data = data
        self.ratios: List[RatioResult] = []

    def calculate_all_ratios(self) -> List[RatioResult]:
        """Calculate all financial ratios"""
        self.ratios = []

        # Profitability Ratios
        self._add_ratio("ROE", "Profitability", self._safe_divide(self.data.net_income, self.data.total_equity), "roe")
        self._add_ratio("ROA", "Profitability", self._safe_divide(self.data.net_income, self.data.total_assets), "roa")
        self._add_ratio(
            "Gross Margin",
            "Profitability",
            self._safe_divide(self.data.gross_profit, self.data.revenue),
            "gross_margin",
        )
        self._add_ratio(
            "Operating Margin",
            "Profitability",
            self._safe_divide(self.data.operating_income, self.data.revenue),
            "operating_margin",
        )
        self._add_ratio(
            "Net Profit Margin",
            "Profitability",
            self._safe_divide(self.data.net_income, self.data.revenue),
            "net_margin",
        )

        # Safety/Liquidity Ratios
        self._add_ratio(
            "Current Ratio",
            "Safety",
            self._safe_divide(self.data.current_assets, self.data.current_liabilities),
            "current_ratio",
        )
        self._add_ratio(
            "Quick Ratio",
            "Safety",
            self._safe_divide(self.data.current_assets - self.data.inventory, self.data.current_liabilities),
            "quick_ratio",
        )
        self._add_ratio(
            "Debt-to-Equity",
            "Safety",
            self._safe_divide(self.data.total_liabilities, self.data.total_equity),
            "debt_to_equity",
            inverted=True,
        )
        self._add_ratio(
            "Interest Coverage",
            "Safety",
            self._safe_divide(self.data.operating_income, self.data.interest_expense),
            "interest_coverage",
        )

        # Efficiency Ratios
        self._add_ratio(
            "Asset Turnover",
            "Efficiency",
            self._safe_divide(self.data.revenue, self.data.total_assets),
            "asset_turnover",
        )
        self._add_ratio(
            "Inventory Turnover",
            "Efficiency",
            self._safe_divide(self.data.cost_of_goods_sold, self.data.inventory),
            "inventory_turnover",
        )
        self._add_ratio(
            "Receivables Turnover",
            "Efficiency",
            self._safe_divide(self.data.revenue, self.data.receivables),
            "receivables_turnover",
        )

        return self.ratios

    def _safe_divide(self, numerator: float, denominator: float) -> float:
        """Safe division handling zero denominator"""
        if denominator == 0:
            return float("inf") if numerator > 0 else 0
        return numerator / denominator

    def _add_ratio(self, name: str, category: str, value: float, ratio_key: str, inverted: bool = False):
        """Add a ratio with interpretation"""
        thresholds = self.THRESHOLDS.get(ratio_key, {"strong": 1.0, "acceptable": 0.5})

        if inverted:
            # Lower is better (e.g., Debt-to-Equity)
            if value <= thresholds["strong"]:
                status = "strong"
                interpretation = f"Excellent - below {thresholds['strong']:.1%}"
            elif value <= thresholds["acceptable"]:
                status = "acceptable"
                interpretation = f"Acceptable - below {thresholds['acceptable']:.1%}"
            else:
                status = "weak"
                interpretation = f"Concerning - above {thresholds['acceptable']:.1%}"
        else:
            # Higher is better
            if value >= thresholds["strong"]:
                status = "strong"
                interpretation = f"Strong - above {thresholds['strong']:.1%}"
            elif value >= thresholds["acceptable"]:
                status = "acceptable"
                interpretation = f"Acceptable - above {thresholds['acceptable']:.1%}"
            else:
                status = "weak"
                interpretation = f"Weak - below {thresholds['acceptable']:.1%}"

        self.ratios.append(
            RatioResult(name=name, category=category, value=value, interpretation=interpretation, status=status)
        )

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate markdown report"""
        report = []
        report.append("# Financial Ratio Analysis Report\n")
        report.append(f"**Company:** {self.data.company}")
        report.append(f"**Period:** {self.data.period}")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        report.append("---\n")
        report.append("## Executive Summary\n")

        # Count status
        strong_count = sum(1 for r in self.ratios if r.status == "strong")
        acceptable_count = sum(1 for r in self.ratios if r.status == "acceptable")
        weak_count = sum(1 for r in self.ratios if r.status == "weak")

        if weak_count == 0:
            report.append("**Overall Assessment:** Healthy financial position with strong metrics.\n")
        elif weak_count <= 2:
            report.append("**Overall Assessment:** Generally healthy with minor areas for improvement.\n")
        else:
            report.append("**Overall Assessment:** Multiple areas require attention.\n")

        report.append(f"- Strong metrics: {strong_count}")
        report.append(f"- Acceptable metrics: {acceptable_count}")
        report.append(f"- Weak metrics: {weak_count}\n")

        # Detailed ratios by category
        for category in ["Profitability", "Safety", "Efficiency"]:
            report.append(f"## {category} Ratios\n")
            report.append("| Ratio | Value | Status | Interpretation |")
            report.append("|-------|-------|--------|----------------|")

            for ratio in self.ratios:
                if ratio.category == category:
                    status_icon = {"strong": "🟢", "acceptable": "🟡", "weak": "🔴"}[ratio.status]
                    if ratio.value == float("inf"):
                        value_str = "N/A"
                    elif abs(ratio.value) < 100:
                        value_str = f"{ratio.value:.2%}" if ratio.value <= 10 else f"{ratio.value:.2f}x"
                    else:
                        value_str = f"{ratio.value:.1f}x"
                    report.append(f"| {ratio.name} | {value_str} | {status_icon} | {ratio.interpretation} |")

            report.append("")

        report_text = "\n".join(report)

        if output_path:
            Path(output_path).write_text(report_text)
            print(f"Report saved to: {output_path}")

        return report_text

    def visualize_ratios(self, output_path: Optional[str] = None):
        """Generate radar chart visualization"""
        if not MATPLOTLIB_AVAILABLE:
            print("Warning: matplotlib not available for visualization")
            return

        # Normalize ratios for radar chart (0-100 scale)
        categories = ["Profitability", "Safety", "Efficiency"]
        category_scores = {}

        for cat in categories:
            cat_ratios = [r for r in self.ratios if r.category == cat]
            scores = []
            for r in cat_ratios:
                if r.status == "strong":
                    scores.append(100)
                elif r.status == "acceptable":
                    scores.append(60)
                else:
                    scores.append(30)
            category_scores[cat] = np.mean(scores) if scores else 50

        # Create radar chart
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle

        values = [category_scores[cat] for cat in categories]
        values += values[:1]  # Complete the circle

        ax.plot(angles, values, "o-", linewidth=2, color="#2563eb")
        ax.fill(angles, values, alpha=0.25, color="#2563eb")

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12)
        ax.set_ylim(0, 100)
        ax.set_title(
            f"Financial Health Overview\n{self.data.company} - {self.data.period}",
            fontsize=14,
            fontweight="bold",
            pad=20,
        )

        # Add legend
        strong_patch = mpatches.Patch(color="green", label="Strong (70-100)")
        acceptable_patch = mpatches.Patch(color="yellow", label="Acceptable (40-70)")
        weak_patch = mpatches.Patch(color="red", label="Weak (0-40)")
        ax.legend(handles=[strong_patch, acceptable_patch, weak_patch], loc="upper right", bbox_to_anchor=(1.3, 1.0))

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
            print(f"Chart saved to: {output_path}")
        else:
            plt.show()

        plt.close()


# =============================================================================
# DCF ANALYZER
# =============================================================================


class DCFAnalyzer:
    """Discounted Cash Flow analysis for investment evaluation"""

    def __init__(
        self,
        initial_investment: float,
        cash_flows: List[float],
        discount_rate: float = 0.10,
        terminal_growth_rate: float = 0.02,
    ):
        self.initial_investment = initial_investment
        self.cash_flows = cash_flows
        self.discount_rate = discount_rate
        self.terminal_growth_rate = terminal_growth_rate
        self.years = len(cash_flows)

    def calculate_npv(self, include_terminal: bool = True) -> float:
        """Calculate Net Present Value"""
        npv = -self.initial_investment

        for year, cf in enumerate(self.cash_flows, 1):
            npv += cf / ((1 + self.discount_rate) ** year)

        if include_terminal and self.years > 0:
            terminal_value = self._calculate_terminal_value()
            npv += terminal_value / ((1 + self.discount_rate) ** self.years)

        return npv

    def _calculate_terminal_value(self) -> float:
        """Calculate terminal value using Gordon Growth Model"""
        if self.discount_rate <= self.terminal_growth_rate:
            return 0  # Invalid case
        final_cf = self.cash_flows[-1] if self.cash_flows else 0
        return final_cf * (1 + self.terminal_growth_rate) / (self.discount_rate - self.terminal_growth_rate)

    def calculate_irr(self, guess: float = 0.10, max_iterations: int = 100, tolerance: float = 0.0001) -> float:
        """Calculate Internal Rate of Return using Newton-Raphson method"""
        cash_flows = [-self.initial_investment] + list(self.cash_flows)
        rate = guess

        for _ in range(max_iterations):
            npv = sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows))
            npv_derivative = sum(-i * cf / ((1 + rate) ** (i + 1)) for i, cf in enumerate(cash_flows))

            if abs(npv) < tolerance:
                return rate

            if npv_derivative == 0:
                break

            rate = rate - npv / npv_derivative

            # Prevent runaway values
            if rate < -0.99 or rate > 10:
                break

        return rate

    def calculate_payback_period(self, discounted: bool = False) -> float:
        """Calculate payback period"""
        cumulative = 0
        investment_recovered = False

        for year, cf in enumerate(self.cash_flows, 1):
            if discounted:
                cf = cf / ((1 + self.discount_rate) ** year)

            cumulative += cf

            if cumulative >= self.initial_investment and not investment_recovered:
                # Interpolate exact payback point
                prev_cumulative = cumulative - cf
                fraction = (self.initial_investment - prev_cumulative) / cf
                return year - 1 + fraction

        # Not recovered within projection period
        return float("inf")

    def calculate_wacc(
        self, equity_value: float, debt_value: float, cost_of_equity: float, cost_of_debt: float, tax_rate: float
    ) -> float:
        """Calculate Weighted Average Cost of Capital"""
        total_value = equity_value + debt_value
        if total_value == 0:
            return 0

        equity_weight = equity_value / total_value
        debt_weight = debt_value / total_value

        wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
        return wacc

    def generate_report(self, project_name: str = "Investment Project") -> str:
        """Generate DCF analysis report"""
        npv = self.calculate_npv()
        irr = self.calculate_irr()
        payback = self.calculate_payback_period()
        discounted_payback = self.calculate_payback_period(discounted=True)
        terminal_value = self._calculate_terminal_value()

        report = []
        report.append("# DCF Investment Analysis Report\n")
        report.append(f"**Project:** {project_name}")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        report.append("---\n")
        report.append("## Investment Summary\n")
        report.append(f"- **Initial Investment:** ${self.initial_investment:,.0f}")
        report.append(f"- **Analysis Period:** {self.years} years")
        report.append(f"- **Discount Rate:** {self.discount_rate:.1%}")
        report.append(f"- **Terminal Growth Rate:** {self.terminal_growth_rate:.1%}\n")

        report.append("## Projected Cash Flows\n")
        report.append("| Year | Cash Flow | Present Value |")
        report.append("|------|-----------|---------------|")
        for year, cf in enumerate(self.cash_flows, 1):
            pv = cf / ((1 + self.discount_rate) ** year)
            report.append(f"| {year} | ${cf:,.0f} | ${pv:,.0f} |")
        report.append(f"| Terminal | - | ${terminal_value / ((1 + self.discount_rate) ** self.years):,.0f} |")
        report.append("")

        report.append("## Key Metrics\n")
        report.append("| Metric | Value | Interpretation |")
        report.append("|--------|-------|----------------|")

        # NPV interpretation
        npv_status = "🟢 Accept" if npv > 0 else "🔴 Reject"
        report.append(f"| NPV | ${npv:,.0f} | {npv_status} - Project {'adds' if npv > 0 else 'destroys'} value |")

        # IRR interpretation
        irr_status = "🟢 Accept" if irr > self.discount_rate else "🔴 Reject"
        report.append(
            f"| IRR | {irr:.1%} | {irr_status} - {'Exceeds' if irr > self.discount_rate else 'Below'} hurdle rate |"
        )

        # Payback interpretation
        if payback == float("inf"):
            payback_str = "Not recovered"
            payback_status = "🔴"
        else:
            payback_str = f"{payback:.1f} years"
            payback_status = "🟢" if payback < 3 else "🟡"
        report.append(f"| Payback Period | {payback_str} | {payback_status} |")

        if discounted_payback != float("inf"):
            report.append(f"| Discounted Payback | {discounted_payback:.1f} years | - |")

        report.append("")

        # Recommendation
        report.append("## Recommendation\n")
        if npv > 0 and irr > self.discount_rate:
            report.append("**RECOMMEND APPROVAL** - Project generates positive NPV and IRR exceeds cost of capital.\n")
        elif npv > 0:
            report.append("**CONDITIONAL APPROVAL** - Positive NPV but marginal returns.\n")
        else:
            report.append("**DO NOT RECOMMEND** - Project destroys value at current assumptions.\n")

        return "\n".join(report)


# =============================================================================
# BUDGET VARIANCE ANALYZER
# =============================================================================


class BudgetVarianceAnalyzer:
    """Analyze budget vs actual variances"""

    def __init__(self, actual_data: Dict, budget_data: Dict, threshold_pct: float = 5.0):
        self.actual = actual_data
        self.budget = budget_data
        self.threshold = threshold_pct / 100
        self.variances: List[Dict] = []

    def calculate_variances(self) -> List[Dict]:
        """Calculate variances for all line items"""
        self.variances = []

        all_keys = set(self.actual.keys()) | set(self.budget.keys())

        for key in all_keys:
            actual_val = self.actual.get(key, 0)
            budget_val = self.budget.get(key, 0)

            variance = actual_val - budget_val
            variance_pct = (variance / budget_val) if budget_val != 0 else 0

            # Determine if favorable (depends on type - revenue vs cost)
            is_revenue = "revenue" in key.lower() or "sales" in key.lower()
            is_favorable = (variance > 0 and is_revenue) or (variance < 0 and not is_revenue)

            is_material = abs(variance_pct) >= self.threshold

            self.variances.append(
                {
                    "item": key,
                    "actual": actual_val,
                    "budget": budget_val,
                    "variance": variance,
                    "variance_pct": variance_pct,
                    "favorable": is_favorable,
                    "material": is_material,
                }
            )

        return self.variances

    def generate_report(self) -> str:
        """Generate variance analysis report"""
        if not self.variances:
            self.calculate_variances()

        report = []
        report.append("# Budget Variance Analysis Report\n")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Materiality Threshold:** {self.threshold:.0%}\n")

        report.append("---\n")
        report.append("## Variance Summary\n")

        total_favorable = sum(v["variance"] for v in self.variances if v["favorable"])
        total_unfavorable = sum(v["variance"] for v in self.variances if not v["favorable"])
        net_variance = total_favorable + total_unfavorable

        report.append(f"- **Total Favorable Variances:** ${abs(total_favorable):,.0f}")
        report.append(f"- **Total Unfavorable Variances:** ${abs(total_unfavorable):,.0f}")
        report.append(f"- **Net Variance:** ${net_variance:,.0f}\n")

        report.append("## Detailed Variances\n")
        report.append("| Item | Budget | Actual | Variance | % | Status |")
        report.append("|------|--------|--------|----------|---|--------|")

        for v in sorted(self.variances, key=lambda x: abs(x["variance"]), reverse=True):
            status = "🟢 F" if v["favorable"] else "🔴 U"
            if v["material"]:
                status += " ⚠️"
            report.append(
                f"| {v['item']} | ${v['budget']:,.0f} | ${v['actual']:,.0f} | "
                f"${v['variance']:,.0f} | {v['variance_pct']:.1%} | {status} |"
            )

        report.append("")

        # Material variances section
        material_variances = [v for v in self.variances if v["material"]]
        if material_variances:
            report.append("## Material Variances Requiring Attention\n")
            for v in material_variances:
                report.append(f"### {v['item']}")
                report.append(f"- **Variance:** ${v['variance']:,.0f} ({v['variance_pct']:.1%})")
                report.append(f"- **Type:** {'Favorable' if v['favorable'] else 'Unfavorable'}")
                report.append("- **Potential Causes:** [To be analyzed]")
                report.append("- **Recommended Actions:** [To be determined]\n")

        return "\n".join(report)


# =============================================================================
# SENSITIVITY ANALYZER
# =============================================================================


class SensitivityAnalyzer:
    """Sensitivity and scenario analysis"""

    def __init__(self, base_case: Dict):
        self.base_case = base_case
        self.results: Dict = {}

    def run_sensitivity(self, variable: str, range_pct: float = 20, steps: int = 5) -> Dict[str, float]:
        """Run single-variable sensitivity analysis"""
        if variable not in self.base_case:
            raise ValueError(f"Variable '{variable}' not found in base case")

        base_value = self.base_case[variable]
        results = {}

        for pct in np.linspace(-range_pct, range_pct, steps):
            adjusted_value = base_value * (1 + pct / 100)
            test_case = self.base_case.copy()
            test_case[variable] = adjusted_value

            # Recalculate NPV with adjusted value
            dcf = DCFAnalyzer(
                initial_investment=test_case.get("initial_investment", 0),
                cash_flows=test_case.get("cash_flows", []),
                discount_rate=test_case.get("discount_rate", 0.10),
            )
            npv = dcf.calculate_npv(include_terminal=False)
            results[f"{pct:+.0f}%"] = npv

        self.results[variable] = results
        return results

    def run_scenario_analysis(self, scenarios: Dict[str, Dict]) -> Dict[str, Dict]:
        """Run multi-variable scenario analysis"""
        results = {}

        for scenario_name, adjustments in scenarios.items():
            test_case = self.base_case.copy()
            for var, value in adjustments.items():
                test_case[var] = value

            dcf = DCFAnalyzer(
                initial_investment=test_case.get("initial_investment", 0),
                cash_flows=test_case.get("cash_flows", []),
                discount_rate=test_case.get("discount_rate", 0.10),
            )

            results[scenario_name] = {
                "npv": dcf.calculate_npv(include_terminal=False),
                "irr": dcf.calculate_irr(),
                "payback": dcf.calculate_payback_period(),
            }

        return results

    def generate_tornado_data(self, variables: List[str], range_pct: float = 20) -> List[Dict]:
        """Generate data for tornado chart"""
        tornado_data = []

        for var in variables:
            self.run_sensitivity(var, range_pct, steps=3)
            var_results = self.results.get(var, {})

            low = var_results.get(f"{-range_pct:+.0f}%", 0)
            high = var_results.get(f"{+range_pct:+.0f}%", 0)
            base = var_results.get("+0%", 0)

            tornado_data.append({"variable": var, "low": low, "high": high, "base": base, "swing": abs(high - low)})

        # Sort by swing magnitude
        tornado_data.sort(key=lambda x: x["swing"], reverse=True)
        return tornado_data

    def visualize_tornado(self, tornado_data: List[Dict], output_path: Optional[str] = None):
        """Generate tornado chart"""
        if not MATPLOTLIB_AVAILABLE:
            print("Warning: matplotlib not available for visualization")
            return

        fig, ax = plt.subplots(figsize=(10, 6))

        variables = [d["variable"] for d in tornado_data]
        y_pos = np.arange(len(variables))

        # Get base NPV
        base_npv = tornado_data[0]["base"] if tornado_data else 0

        for i, d in enumerate(tornado_data):
            # Calculate bar positions relative to base
            low_delta = d["low"] - base_npv
            high_delta = d["high"] - base_npv

            if low_delta < high_delta:
                ax.barh(i, low_delta, height=0.6, color="#ef4444", alpha=0.7, label="Downside" if i == 0 else "")
                ax.barh(i, high_delta, height=0.6, color="#22c55e", alpha=0.7, label="Upside" if i == 0 else "")
            else:
                ax.barh(i, high_delta, height=0.6, color="#ef4444", alpha=0.7, label="Downside" if i == 0 else "")
                ax.barh(i, low_delta, height=0.6, color="#22c55e", alpha=0.7, label="Upside" if i == 0 else "")

        ax.axvline(x=0, color="black", linewidth=1)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(variables)
        ax.set_xlabel("NPV Impact ($)")
        ax.set_title("Sensitivity Analysis - Tornado Chart")
        ax.legend(loc="lower right")

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
            print(f"Chart saved to: {output_path}")
        else:
            plt.show()

        plt.close()


# =============================================================================
# CLI HANDLERS
# =============================================================================


def handle_ratios_command(args):
    """Handle financial ratio analysis command"""
    with open(args.input_file, "r") as f:
        data = json.load(f)

    # Parse financial data
    bs = data.get("balance_sheet", {})
    inc = data.get("income_statement", {})

    financial_data = FinancialData(
        company=data.get("company", "Unknown"),
        period=data.get("period", "Unknown"),
        total_assets=bs.get("total_assets", 0),
        current_assets=bs.get("current_assets", 0),
        cash=bs.get("cash", 0),
        inventory=bs.get("inventory", 0),
        receivables=bs.get("receivables", 0),
        total_liabilities=bs.get("total_liabilities", 0),
        current_liabilities=bs.get("current_liabilities", 0),
        long_term_debt=bs.get("long_term_debt", 0),
        total_equity=bs.get("total_equity", 0),
        revenue=inc.get("revenue", 0),
        cost_of_goods_sold=inc.get("cost_of_goods_sold", 0),
        gross_profit=inc.get("gross_profit", 0),
        operating_expenses=inc.get("operating_expenses", 0),
        operating_income=inc.get("operating_income", 0),
        interest_expense=inc.get("interest_expense", 0),
        net_income=inc.get("net_income", 0),
    )

    analyzer = FinancialRatioAnalyzer(financial_data)
    analyzer.calculate_all_ratios()

    # Generate report
    output_path = args.output if args.output else None
    report = analyzer.generate_report(output_path)
    print(report)

    # Visualize if requested
    if args.visualize and MATPLOTLIB_AVAILABLE:
        chart_path = output_path.replace(".md", "_chart.png") if output_path else None
        analyzer.visualize_ratios(chart_path)


def handle_dcf_command(args):
    """Handle DCF analysis command"""
    with open(args.input_file, "r") as f:
        data = json.load(f)

    analyzer = DCFAnalyzer(
        initial_investment=data.get("initial_investment", 0),
        cash_flows=data.get("projected_cash_flows", data.get("cash_flows", [])),
        discount_rate=args.discount_rate,
        terminal_growth_rate=data.get("terminal_growth_rate", 0.02),
    )

    report = analyzer.generate_report(data.get("project_name", "Investment Project"))
    print(report)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport saved to: {args.output}")


def handle_variance_command(args):
    """Handle budget variance analysis command"""
    if not PANDAS_AVAILABLE:
        print("Error: pandas is required for variance analysis")
        return

    actual_df = pd.read_csv(args.actual_file)
    budget_df = pd.read_csv(args.budget_file)

    # Convert to dictionaries (assuming 'item' and 'amount' columns)
    actual_data = dict(zip(actual_df["item"], actual_df["amount"]))
    budget_data = dict(zip(budget_df["item"], budget_df["amount"]))

    analyzer = BudgetVarianceAnalyzer(actual_data, budget_data, args.threshold)
    report = analyzer.generate_report()
    print(report)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport saved to: {args.output}")


def handle_sensitivity_command(args):
    """Handle sensitivity analysis command"""
    with open(args.input_file, "r") as f:
        data = json.load(f)

    analyzer = SensitivityAnalyzer(data)

    variables = args.variables.split(",") if args.variables else list(data.keys())[:5]
    tornado_data = analyzer.generate_tornado_data(variables, args.range)

    print("\n" + "=" * 60)
    print("SENSITIVITY ANALYSIS RESULTS")
    print("=" * 60 + "\n")

    print("| Variable | Low NPV | Base NPV | High NPV | Swing |")
    print("|----------|---------|----------|----------|-------|")
    for d in tornado_data:
        print(f"| {d['variable']} | ${d['low']:,.0f} | ${d['base']:,.0f} | ${d['high']:,.0f} | ${d['swing']:,.0f} |")

    if args.visualize and MATPLOTLIB_AVAILABLE:
        chart_path = args.output.replace(".md", "_tornado.png") if args.output else None
        analyzer.visualize_tornado(tornado_data, chart_path)


# =============================================================================
# MAIN
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Financial Analyzer - Comprehensive Financial Analysis Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    subparsers = parser.add_subparsers(dest="command", help="Analysis command")

    # Ratios command
    ratios_parser = subparsers.add_parser("ratios", help="Financial ratio analysis")
    ratios_parser.add_argument("input_file", help="JSON file with financial data")
    ratios_parser.add_argument("--output", "-o", help="Output file path")
    ratios_parser.add_argument("--visualize", "-v", action="store_true", help="Generate visualization charts")

    # DCF command
    dcf_parser = subparsers.add_parser("dcf", help="DCF/NPV/IRR analysis")
    dcf_parser.add_argument("input_file", help="JSON file with cash flow projections")
    dcf_parser.add_argument("--discount-rate", "-r", type=float, default=0.10, help="Discount rate (default: 0.10)")
    dcf_parser.add_argument("--output", "-o", help="Output file path")

    # Variance command
    variance_parser = subparsers.add_parser("variance", help="Budget variance analysis")
    variance_parser.add_argument("actual_file", help="CSV file with actual values")
    variance_parser.add_argument("budget_file", help="CSV file with budget values")
    variance_parser.add_argument(
        "--threshold", "-t", type=float, default=5.0, help="Materiality threshold percentage (default: 5)"
    )
    variance_parser.add_argument("--output", "-o", help="Output file path")

    # Sensitivity command
    sensitivity_parser = subparsers.add_parser("sensitivity", help="Sensitivity analysis")
    sensitivity_parser.add_argument("input_file", help="JSON file with model parameters")
    sensitivity_parser.add_argument("--variables", "-v", help="Comma-separated list of variables")
    sensitivity_parser.add_argument(
        "--range", "-r", type=float, default=20, help="Sensitivity range percentage (default: 20)"
    )
    sensitivity_parser.add_argument("--output", "-o", help="Output file path")
    sensitivity_parser.add_argument("--visualize", action="store_true", help="Generate tornado chart")

    args = parser.parse_args()

    if args.command == "ratios":
        handle_ratios_command(args)
    elif args.command == "dcf":
        handle_dcf_command(args)
    elif args.command == "variance":
        handle_variance_command(args)
    elif args.command == "sensitivity":
        handle_sensitivity_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
