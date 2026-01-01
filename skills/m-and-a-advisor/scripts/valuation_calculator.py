#!/usr/bin/env python3
"""
M&A Valuation Calculator - Enterprise Valuation Toolkit
=========================================================

A professional toolkit for M&A valuation analysis including:
- DCF (Discounted Cash Flow) valuation
- WACC (Weighted Average Cost of Capital) calculation
- Comparable companies analysis (multiples)
- Precedent transaction analysis
- Synergy NPV calculation
- Sensitivity analysis matrix

Usage:
    python valuation_calculator.py dcf <projections.json> [--output valuation.md]
    python valuation_calculator.py wacc <params.json>
    python valuation_calculator.py multiples <target.json> <comps.json>
    python valuation_calculator.py synergy <synergy.json> [--discount-rate 0.08]
    python valuation_calculator.py sensitivity <model.json> [--output matrix.md]

Examples:
    python valuation_calculator.py dcf target_projections.json --output dcf_report.md
    python valuation_calculator.py wacc wacc_params.json
    python valuation_calculator.py multiples target.json comparable_companies.json
    python valuation_calculator.py synergy synergy_model.json --discount-rate 0.10
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from dataclasses import dataclass

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("Warning: numpy not available. Using basic math.")


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class WACCParameters:
    """Parameters for WACC calculation"""
    risk_free_rate: float
    equity_risk_premium: float
    beta: float
    size_premium: float
    cost_of_debt: float
    tax_rate: float
    market_value_equity: float
    market_value_debt: float

    @property
    def cost_of_equity(self) -> float:
        """Calculate cost of equity using CAPM"""
        return self.risk_free_rate + (self.beta * self.equity_risk_premium) + self.size_premium

    @property
    def wacc(self) -> float:
        """Calculate Weighted Average Cost of Capital"""
        total_capital = self.market_value_equity + self.market_value_debt
        if total_capital == 0:
            return 0
        equity_weight = self.market_value_equity / total_capital
        debt_weight = self.market_value_debt / total_capital
        after_tax_cost_of_debt = self.cost_of_debt * (1 - self.tax_rate)
        return (equity_weight * self.cost_of_equity) + (debt_weight * after_tax_cost_of_debt)


@dataclass
class DCFResult:
    """Container for DCF valuation results"""
    pv_fcf: float
    terminal_value: float
    pv_terminal_value: float
    enterprise_value: float
    net_debt: float
    minority_interest: float
    non_operating_assets: float
    equity_value: float
    shares_outstanding: float
    per_share_value: float


@dataclass
class ComparableResult:
    """Container for comparable company multiple result"""
    company: str
    ev_ebitda: float
    ev_revenue: float
    pe_ratio: float
    ev_ebit: float


@dataclass
class SynergyItem:
    """Container for synergy analysis"""
    category: str
    item: str
    annual_impact: float
    probability: float
    realization_year1: float
    realization_year2: float
    realization_year3: float


# =============================================================================
# WACC CALCULATOR
# =============================================================================

class WACCCalculator:
    """Calculate Weighted Average Cost of Capital"""

    # US Market Reference Data (2024-2025)
    REFERENCE_DATA = {
        'risk_free_rate_10y': 0.0425,  # 10-year Treasury yield
        'equity_risk_premium': 0.055,   # Historical ERP
        'size_premium': {
            'large': 0.00,    # Large cap
            'mid': 0.0100,    # Mid cap
            'small': 0.0175,  # Small cap
            'micro': 0.0350,  # Micro cap
        },
        'industry_betas': {
            'technology': 1.20,
            'healthcare': 0.85,
            'financial_services': 1.05,
            'manufacturing': 1.00,
            'retail': 1.10,
            'utilities': 0.65,
            'real_estate': 0.85,
            'energy': 1.15,
            'consumer_goods': 0.90,
            'default': 1.00,
        }
    }

    def __init__(self, params: WACCParameters):
        self.params = params

    def calculate(self) -> Dict[str, float]:
        """Calculate WACC with component breakdown"""
        cost_of_equity = self.params.cost_of_equity
        after_tax_cost_of_debt = self.params.cost_of_debt * (1 - self.params.tax_rate)

        total_capital = self.params.market_value_equity + self.params.market_value_debt
        if total_capital == 0:
            return {'wacc': 0, 'cost_of_equity': cost_of_equity, 'after_tax_cost_of_debt': after_tax_cost_of_debt}

        equity_weight = self.params.market_value_equity / total_capital
        debt_weight = self.params.market_value_debt / total_capital

        wacc = (equity_weight * cost_of_equity) + (debt_weight * after_tax_cost_of_debt)

        return {
            'risk_free_rate': self.params.risk_free_rate,
            'equity_risk_premium': self.params.equity_risk_premium,
            'beta': self.params.beta,
            'size_premium': self.params.size_premium,
            'cost_of_equity': cost_of_equity,
            'cost_of_debt_pre_tax': self.params.cost_of_debt,
            'tax_rate': self.params.tax_rate,
            'cost_of_debt_after_tax': after_tax_cost_of_debt,
            'equity_weight': equity_weight,
            'debt_weight': debt_weight,
            'wacc': wacc,
        }

    def generate_report(self) -> str:
        """Generate WACC calculation report"""
        results = self.calculate()

        report = []
        report.append("# WACC Calculation Report\n")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        report.append("---\n")
        report.append("## Cost of Equity (CAPM)\n")
        report.append("```")
        report.append("Re = Rf + β × ERP + Size Premium")
        report.append(f"Re = {results['risk_free_rate']:.2%} + {results['beta']:.2f} × {results['equity_risk_premium']:.2%} + {results['size_premium']:.2%}")
        report.append(f"Re = {results['cost_of_equity']:.2%}")
        report.append("```\n")

        report.append("| Component | Value |")
        report.append("|-----------|-------|")
        report.append(f"| Risk-Free Rate (Rf) | {results['risk_free_rate']:.2%} |")
        report.append(f"| Levered Beta (β) | {results['beta']:.2f} |")
        report.append(f"| Equity Risk Premium (ERP) | {results['equity_risk_premium']:.2%} |")
        report.append(f"| Size Premium | {results['size_premium']:.2%} |")
        report.append(f"| **Cost of Equity (Re)** | **{results['cost_of_equity']:.2%}** |\n")

        report.append("## Cost of Debt\n")
        report.append("| Component | Value |")
        report.append("|-----------|-------|")
        report.append(f"| Pre-tax Cost of Debt | {results['cost_of_debt_pre_tax']:.2%} |")
        report.append(f"| Tax Rate | {results['tax_rate']:.1%} |")
        report.append(f"| After-tax Cost of Debt | {results['cost_of_debt_after_tax']:.2%} |\n")

        report.append("## WACC Calculation\n")
        report.append("```")
        report.append("WACC = (E/V) × Re + (D/V) × Rd × (1-T)")
        report.append(f"WACC = {results['equity_weight']:.1%} × {results['cost_of_equity']:.2%} + {results['debt_weight']:.1%} × {results['cost_of_debt_after_tax']:.2%}")
        report.append(f"WACC = {results['wacc']:.2%}")
        report.append("```\n")

        report.append("| Component | Weight | Cost | Contribution |")
        report.append("|-----------|--------|------|--------------|")
        equity_contribution = results['equity_weight'] * results['cost_of_equity']
        debt_contribution = results['debt_weight'] * results['cost_of_debt_after_tax']
        report.append(f"| Equity | {results['equity_weight']:.1%} | {results['cost_of_equity']:.2%} | {equity_contribution:.2%} |")
        report.append(f"| Debt | {results['debt_weight']:.1%} | {results['cost_of_debt_after_tax']:.2%} | {debt_contribution:.2%} |")
        report.append(f"| **WACC** | **100%** | | **{results['wacc']:.2%}** |\n")

        return "\n".join(report)


# =============================================================================
# DCF VALUATION
# =============================================================================

class DCFValuation:
    """DCF Valuation for M&A"""

    def __init__(
        self,
        fcf_projections: List[float],
        wacc: float,
        terminal_growth_rate: float,
        net_debt: float,
        minority_interest: float = 0,
        non_operating_assets: float = 0,
        shares_outstanding: float = 1,
    ):
        self.fcf = fcf_projections
        self.wacc = wacc
        self.terminal_growth = terminal_growth_rate
        self.net_debt = net_debt
        self.minority_interest = minority_interest
        self.non_operating_assets = non_operating_assets
        self.shares_outstanding = shares_outstanding
        self.projection_years = len(fcf_projections)

    def calculate_terminal_value(self) -> float:
        """Calculate terminal value using Gordon Growth Model"""
        if self.wacc <= self.terminal_growth:
            raise ValueError("WACC must be greater than terminal growth rate")
        final_fcf = self.fcf[-1] if self.fcf else 0
        return final_fcf * (1 + self.terminal_growth) / (self.wacc - self.terminal_growth)

    def calculate_pv_fcf(self) -> List[float]:
        """Calculate present value of each year's FCF"""
        pv_list = []
        for year, fcf in enumerate(self.fcf, 1):
            pv = fcf / ((1 + self.wacc) ** year)
            pv_list.append(pv)
        return pv_list

    def calculate(self) -> DCFResult:
        """Perform full DCF calculation"""
        pv_fcf_list = self.calculate_pv_fcf()
        pv_fcf_total = sum(pv_fcf_list)

        terminal_value = self.calculate_terminal_value()
        pv_terminal = terminal_value / ((1 + self.wacc) ** self.projection_years)

        enterprise_value = pv_fcf_total + pv_terminal
        equity_value = enterprise_value - self.net_debt - self.minority_interest + self.non_operating_assets
        per_share_value = equity_value / self.shares_outstanding if self.shares_outstanding > 0 else 0

        return DCFResult(
            pv_fcf=pv_fcf_total,
            terminal_value=terminal_value,
            pv_terminal_value=pv_terminal,
            enterprise_value=enterprise_value,
            net_debt=self.net_debt,
            minority_interest=self.minority_interest,
            non_operating_assets=self.non_operating_assets,
            equity_value=equity_value,
            shares_outstanding=self.shares_outstanding,
            per_share_value=per_share_value,
        )

    def sensitivity_analysis(
        self,
        wacc_range: Tuple[float, float] = (0.06, 0.10),
        growth_range: Tuple[float, float] = (0.01, 0.03),
        steps: int = 5,
    ) -> List[List[float]]:
        """Generate sensitivity matrix for WACC vs Terminal Growth"""
        wacc_values = [wacc_range[0] + i * (wacc_range[1] - wacc_range[0]) / (steps - 1) for i in range(steps)]
        growth_values = [growth_range[0] + i * (growth_range[1] - growth_range[0]) / (steps - 1) for i in range(steps)]

        matrix = []
        for wacc in wacc_values:
            row = []
            for growth in growth_values:
                original_wacc = self.wacc
                original_growth = self.terminal_growth
                self.wacc = wacc
                self.terminal_growth = growth
                try:
                    result = self.calculate()
                    row.append(result.equity_value)
                except ValueError:
                    row.append(float('nan'))
                self.wacc = original_wacc
                self.terminal_growth = original_growth
            matrix.append(row)

        return matrix, wacc_values, growth_values

    def generate_report(self, company_name: str = "Target Company") -> str:
        """Generate DCF valuation report"""
        result = self.calculate()

        report = []
        report.append("# DCF Valuation Analysis\n")
        report.append(f"**Target Company:** {company_name}")
        report.append(f"**Valuation Date:** {datetime.now().strftime('%Y-%m-%d')}")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        report.append("---\n")
        report.append("## Key Assumptions\n")
        report.append("| Parameter | Value |")
        report.append("|-----------|-------|")
        report.append(f"| Projection Period | {self.projection_years} years |")
        report.append(f"| WACC | {self.wacc:.2%} |")
        report.append(f"| Terminal Growth Rate | {self.terminal_growth:.2%} |")
        report.append(f"| Net Debt | ${self.net_debt:,.0f}M |")
        if self.minority_interest > 0:
            report.append(f"| Minority Interest | ${self.minority_interest:,.0f}M |")
        if self.non_operating_assets > 0:
            report.append(f"| Non-Operating Assets | ${self.non_operating_assets:,.0f}M |")
        report.append("")

        report.append("## Projected Free Cash Flow\n")
        report.append("| Year | FCF | Discount Factor | Present Value |")
        report.append("|------|-----|-----------------|---------------|")
        pv_list = self.calculate_pv_fcf()
        for year, (fcf, pv) in enumerate(zip(self.fcf, pv_list), 1):
            df = 1 / ((1 + self.wacc) ** year)
            report.append(f"| Year {year} | ${fcf:,.0f}M | {df:.4f} | ${pv:,.0f}M |")
        report.append(f"| **Total PV of FCF** | | | **${result.pv_fcf:,.0f}M** |\n")

        report.append("## Terminal Value\n")
        report.append("```")
        report.append("TV = FCF(n) × (1 + g) / (WACC - g)")
        report.append(f"TV = ${self.fcf[-1]:,.0f}M × (1 + {self.terminal_growth:.2%}) / ({self.wacc:.2%} - {self.terminal_growth:.2%})")
        report.append(f"TV = ${result.terminal_value:,.0f}M")
        report.append(f"PV of TV = ${result.pv_terminal_value:,.0f}M")
        report.append("```\n")

        report.append("## Enterprise Value Bridge\n")
        report.append("| Component | Amount |")
        report.append("|-----------|--------|")
        report.append(f"| PV of Projected FCF | ${result.pv_fcf:,.0f}M |")
        report.append(f"| PV of Terminal Value | ${result.pv_terminal_value:,.0f}M |")
        report.append(f"| **Enterprise Value** | **${result.enterprise_value:,.0f}M** |")
        report.append(f"| (-) Net Debt | (${result.net_debt:,.0f}M) |")
        if result.minority_interest > 0:
            report.append(f"| (-) Minority Interest | (${result.minority_interest:,.0f}M) |")
        if result.non_operating_assets > 0:
            report.append(f"| (+) Non-Operating Assets | ${result.non_operating_assets:,.0f}M |")
        report.append(f"| **Equity Value** | **${result.equity_value:,.0f}M** |\n")

        if self.shares_outstanding > 1:
            report.append(f"**Per Share Value:** ${result.per_share_value:,.2f}")
            report.append(f"(Based on {self.shares_outstanding:,.0f} shares outstanding)\n")

        # Sensitivity Analysis
        matrix, wacc_values, growth_values = self.sensitivity_analysis()
        report.append("## Sensitivity Analysis (Equity Value, $M)\n")
        header = "| WACC \\ Growth | " + " | ".join([f"{g:.1%}" for g in growth_values]) + " |"
        report.append(header)
        report.append("|" + "------|" * (len(growth_values) + 1))
        for i, wacc in enumerate(wacc_values):
            row_values = [f"${v:,.0f}" if not (v != v) else "N/A" for v in matrix[i]]  # v != v checks for NaN
            row = f"| {wacc:.1%} | " + " | ".join(row_values) + " |"
            report.append(row)
        report.append("")

        return "\n".join(report)


# =============================================================================
# COMPARABLE COMPANIES ANALYSIS
# =============================================================================

class ComparableAnalysis:
    """Comparable companies (trading multiples) analysis"""

    def __init__(self, target_metrics: Dict[str, float], comparable_companies: List[Dict]):
        self.target = target_metrics
        self.comps = comparable_companies

    def calculate_multiples(self) -> List[ComparableResult]:
        """Calculate trading multiples for each comparable"""
        results = []
        for comp in self.comps:
            ev = comp.get('enterprise_value', 0)
            ebitda = comp.get('ebitda', 0)
            ebit = comp.get('ebit', 0)
            revenue = comp.get('revenue', 0)
            net_income = comp.get('net_income', 0)
            market_cap = comp.get('market_cap', 0)

            results.append(ComparableResult(
                company=comp.get('company', 'Unknown'),
                ev_ebitda=ev / ebitda if ebitda > 0 else 0,
                ev_revenue=ev / revenue if revenue > 0 else 0,
                pe_ratio=market_cap / net_income if net_income > 0 else 0,
                ev_ebit=ev / ebit if ebit > 0 else 0,
            ))
        return results

    def calculate_statistics(self) -> Dict[str, Dict[str, float]]:
        """Calculate mean and median of multiples"""
        multiples = self.calculate_multiples()

        stats = {
            'ev_ebitda': {'values': [m.ev_ebitda for m in multiples if m.ev_ebitda > 0]},
            'ev_revenue': {'values': [m.ev_revenue for m in multiples if m.ev_revenue > 0]},
            'pe_ratio': {'values': [m.pe_ratio for m in multiples if m.pe_ratio > 0]},
            'ev_ebit': {'values': [m.ev_ebit for m in multiples if m.ev_ebit > 0]},
        }

        for key, data in stats.items():
            values = data['values']
            if values:
                data['mean'] = sum(values) / len(values)
                sorted_values = sorted(values)
                n = len(sorted_values)
                data['median'] = sorted_values[n // 2] if n % 2 == 1 else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
                data['min'] = min(values)
                data['max'] = max(values)
            else:
                data['mean'] = data['median'] = data['min'] = data['max'] = 0

        return stats

    def apply_multiples_to_target(self) -> Dict[str, Dict[str, float]]:
        """Apply comparable multiples to target company"""
        stats = self.calculate_statistics()
        target_ebitda = self.target.get('ebitda', 0)
        target_revenue = self.target.get('revenue', 0)
        target_ebit = self.target.get('ebit', 0)
        target_net_debt = self.target.get('net_debt', 0)

        implied_values = {
            'ev_ebitda': {
                'enterprise_value_mean': target_ebitda * stats['ev_ebitda']['mean'],
                'enterprise_value_median': target_ebitda * stats['ev_ebitda']['median'],
                'equity_value_mean': target_ebitda * stats['ev_ebitda']['mean'] - target_net_debt,
                'equity_value_median': target_ebitda * stats['ev_ebitda']['median'] - target_net_debt,
            },
            'ev_revenue': {
                'enterprise_value_mean': target_revenue * stats['ev_revenue']['mean'],
                'enterprise_value_median': target_revenue * stats['ev_revenue']['median'],
                'equity_value_mean': target_revenue * stats['ev_revenue']['mean'] - target_net_debt,
                'equity_value_median': target_revenue * stats['ev_revenue']['median'] - target_net_debt,
            },
            'ev_ebit': {
                'enterprise_value_mean': target_ebit * stats['ev_ebit']['mean'],
                'enterprise_value_median': target_ebit * stats['ev_ebit']['median'],
                'equity_value_mean': target_ebit * stats['ev_ebit']['mean'] - target_net_debt,
                'equity_value_median': target_ebit * stats['ev_ebit']['median'] - target_net_debt,
            },
        }
        return implied_values

    def generate_report(self, target_name: str = "Target Company") -> str:
        """Generate comparable companies analysis report"""
        multiples = self.calculate_multiples()
        stats = self.calculate_statistics()
        implied = self.apply_multiples_to_target()

        report = []
        report.append("# Comparable Companies Analysis\n")
        report.append(f"**Target Company:** {target_name}")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        report.append("---\n")
        report.append("## Comparable Companies\n")
        report.append("| Company | EV/EBITDA | EV/Revenue | EV/EBIT | P/E |")
        report.append("|---------|-----------|------------|---------|-----|")
        for m in multiples:
            report.append(f"| {m.company} | {m.ev_ebitda:.1f}x | {m.ev_revenue:.2f}x | {m.ev_ebit:.1f}x | {m.pe_ratio:.1f}x |")
        report.append("")

        report.append("## Multiple Statistics\n")
        report.append("| Multiple | Mean | Median | Min | Max |")
        report.append("|----------|------|--------|-----|-----|")
        report.append(f"| EV/EBITDA | {stats['ev_ebitda']['mean']:.1f}x | {stats['ev_ebitda']['median']:.1f}x | {stats['ev_ebitda']['min']:.1f}x | {stats['ev_ebitda']['max']:.1f}x |")
        report.append(f"| EV/Revenue | {stats['ev_revenue']['mean']:.2f}x | {stats['ev_revenue']['median']:.2f}x | {stats['ev_revenue']['min']:.2f}x | {stats['ev_revenue']['max']:.2f}x |")
        report.append(f"| EV/EBIT | {stats['ev_ebit']['mean']:.1f}x | {stats['ev_ebit']['median']:.1f}x | {stats['ev_ebit']['min']:.1f}x | {stats['ev_ebit']['max']:.1f}x |")
        report.append(f"| P/E | {stats['pe_ratio']['mean']:.1f}x | {stats['pe_ratio']['median']:.1f}x | {stats['pe_ratio']['min']:.1f}x | {stats['pe_ratio']['max']:.1f}x |\n")

        report.append("## Target Company Metrics\n")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Revenue | ${self.target.get('revenue', 0):,.0f}M |")
        report.append(f"| EBITDA | ${self.target.get('ebitda', 0):,.0f}M |")
        report.append(f"| EBIT | ${self.target.get('ebit', 0):,.0f}M |")
        report.append(f"| Net Debt | ${self.target.get('net_debt', 0):,.0f}M |\n")

        report.append("## Implied Valuation\n")
        report.append("| Method | Enterprise Value | Equity Value |")
        report.append("|--------|------------------|--------------|")
        report.append(f"| EV/EBITDA (Median) | ${implied['ev_ebitda']['enterprise_value_median']:,.0f}M | ${implied['ev_ebitda']['equity_value_median']:,.0f}M |")
        report.append(f"| EV/Revenue (Median) | ${implied['ev_revenue']['enterprise_value_median']:,.0f}M | ${implied['ev_revenue']['equity_value_median']:,.0f}M |")
        report.append(f"| EV/EBIT (Median) | ${implied['ev_ebit']['enterprise_value_median']:,.0f}M | ${implied['ev_ebit']['equity_value_median']:,.0f}M |\n")

        # Summary range
        equity_values = [
            implied['ev_ebitda']['equity_value_median'],
            implied['ev_revenue']['equity_value_median'],
            implied['ev_ebit']['equity_value_median'],
        ]
        equity_values = [v for v in equity_values if v > 0]
        if equity_values:
            report.append(f"**Implied Equity Value Range:** ${min(equity_values):,.0f}M - ${max(equity_values):,.0f}M\n")

        return "\n".join(report)


# =============================================================================
# SYNERGY NPV CALCULATOR
# =============================================================================

class SynergyNPVCalculator:
    """Calculate NPV of expected synergies"""

    def __init__(
        self,
        synergies: List[Dict],
        discount_rate: float = 0.08,
        realization_costs: float = 0,
    ):
        self.synergies = synergies
        self.discount_rate = discount_rate
        self.realization_costs = realization_costs

    def calculate_annual_synergies(self, years: int = 5) -> List[float]:
        """Calculate probability-weighted annual synergies"""
        annual_totals = [0.0] * years

        for syn in self.synergies:
            annual_impact = syn.get('annual_impact', 0)
            probability = syn.get('probability', 1.0)
            realization = [
                syn.get('realization_year1', 0),
                syn.get('realization_year2', 0),
                syn.get('realization_year3', 1.0),
                1.0,
                1.0,
            ]

            for year in range(years):
                factor = realization[year] if year < len(realization) else 1.0
                annual_totals[year] += annual_impact * probability * factor

        return annual_totals

    def calculate_npv(self, years: int = 5) -> float:
        """Calculate NPV of synergies"""
        annual_synergies = self.calculate_annual_synergies(years)
        npv = 0

        for year, synergy in enumerate(annual_synergies, 1):
            pv = synergy / ((1 + self.discount_rate) ** year)
            npv += pv

        npv -= self.realization_costs
        return npv

    def generate_report(self) -> str:
        """Generate synergy analysis report"""
        annual_synergies = self.calculate_annual_synergies()
        npv = self.calculate_npv()

        report = []
        report.append("# Synergy NPV Analysis\n")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        report.append("---\n")
        report.append("## Synergy Items\n")
        report.append("| Category | Item | Annual Impact | Probability | Y1 | Y2 | Y3 |")
        report.append("|----------|------|---------------|-------------|----|----|---- |")

        for syn in self.synergies:
            report.append(
                f"| {syn.get('category', '')} | {syn.get('item', '')} | "
                f"${syn.get('annual_impact', 0):,.0f}M | {syn.get('probability', 1.0):.0%} | "
                f"{syn.get('realization_year1', 0):.0%} | {syn.get('realization_year2', 0):.0%} | "
                f"{syn.get('realization_year3', 1.0):.0%} |"
            )
        report.append("")

        report.append("## Annual Synergy Realization\n")
        report.append("| Year | Probability-Adjusted Synergy | Discount Factor | Present Value |")
        report.append("|------|------------------------------|-----------------|---------------|")

        total_pv = 0
        for year, synergy in enumerate(annual_synergies, 1):
            df = 1 / ((1 + self.discount_rate) ** year)
            pv = synergy * df
            total_pv += pv
            report.append(f"| Year {year} | ${synergy:,.0f}M | {df:.4f} | ${pv:,.0f}M |")
        report.append(f"| **Total** | | | **${total_pv:,.0f}M** |\n")

        report.append("## NPV Summary\n")
        report.append("| Item | Amount |")
        report.append("|------|--------|")
        report.append(f"| PV of Synergies | ${total_pv:,.0f}M |")
        report.append(f"| (-) Realization Costs | (${self.realization_costs:,.0f}M) |")
        report.append(f"| **Net Synergy NPV** | **${npv:,.0f}M** |\n")

        report.append(f"**Discount Rate:** {self.discount_rate:.1%}\n")

        return "\n".join(report)


# =============================================================================
# CLI HANDLERS
# =============================================================================

def handle_dcf_command(args):
    """Handle DCF valuation command"""
    with open(args.input_file, 'r') as f:
        data = json.load(f)

    dcf = DCFValuation(
        fcf_projections=data.get('fcf_projections', data.get('cash_flows', [])),
        wacc=data.get('wacc', 0.08),
        terminal_growth_rate=data.get('terminal_growth_rate', 0.02),
        net_debt=data.get('net_debt', 0),
        minority_interest=data.get('minority_interest', 0),
        non_operating_assets=data.get('non_operating_assets', 0),
        shares_outstanding=data.get('shares_outstanding', 1),
    )

    report = dcf.generate_report(data.get('company_name', 'Target Company'))
    print(report)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport saved to: {args.output}")


def handle_wacc_command(args):
    """Handle WACC calculation command"""
    with open(args.input_file, 'r') as f:
        data = json.load(f)

    params = WACCParameters(
        risk_free_rate=data.get('risk_free_rate', 0.0425),
        equity_risk_premium=data.get('equity_risk_premium', 0.055),
        beta=data.get('beta', 1.0),
        size_premium=data.get('size_premium', 0.01),
        cost_of_debt=data.get('cost_of_debt', 0.05),
        tax_rate=data.get('tax_rate', 0.25),
        market_value_equity=data.get('market_value_equity', 0),
        market_value_debt=data.get('market_value_debt', 0),
    )

    calculator = WACCCalculator(params)
    report = calculator.generate_report()
    print(report)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport saved to: {args.output}")


def handle_multiples_command(args):
    """Handle comparable companies analysis command"""
    with open(args.target_file, 'r') as f:
        target = json.load(f)

    with open(args.comps_file, 'r') as f:
        comps_data = json.load(f)

    comps = comps_data if isinstance(comps_data, list) else comps_data.get('companies', [])

    analyzer = ComparableAnalysis(target, comps)
    report = analyzer.generate_report(target.get('company_name', 'Target Company'))
    print(report)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport saved to: {args.output}")


def handle_synergy_command(args):
    """Handle synergy NPV calculation command"""
    with open(args.input_file, 'r') as f:
        data = json.load(f)

    synergies = data.get('synergies', [])
    realization_costs = data.get('realization_costs', 0)

    calculator = SynergyNPVCalculator(
        synergies=synergies,
        discount_rate=args.discount_rate,
        realization_costs=realization_costs,
    )

    report = calculator.generate_report()
    print(report)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\nReport saved to: {args.output}")


def handle_sensitivity_command(args):
    """Handle sensitivity analysis command"""
    with open(args.input_file, 'r') as f:
        data = json.load(f)

    dcf = DCFValuation(
        fcf_projections=data.get('fcf_projections', data.get('cash_flows', [])),
        wacc=data.get('wacc', 0.08),
        terminal_growth_rate=data.get('terminal_growth_rate', 0.02),
        net_debt=data.get('net_debt', 0),
    )

    wacc_range = (data.get('wacc_min', 0.06), data.get('wacc_max', 0.10))
    growth_range = (data.get('growth_min', 0.01), data.get('growth_max', 0.03))

    matrix, wacc_values, growth_values = dcf.sensitivity_analysis(
        wacc_range=wacc_range,
        growth_range=growth_range,
        steps=args.steps,
    )

    report = []
    report.append("# Sensitivity Analysis\n")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("## Equity Value Matrix ($M)\n")

    header = "| WACC \\ Growth | " + " | ".join([f"{g:.1%}" for g in growth_values]) + " |"
    report.append(header)
    report.append("|" + "------|" * (len(growth_values) + 1))

    for i, wacc in enumerate(wacc_values):
        row_values = [f"${v:,.0f}" if not (v != v) else "N/A" for v in matrix[i]]
        row = f"| {wacc:.1%} | " + " | ".join(row_values) + " |"
        report.append(row)

    report_text = "\n".join(report)
    print(report_text)

    if args.output:
        Path(args.output).write_text(report_text)
        print(f"\nReport saved to: {args.output}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='M&A Valuation Calculator - Enterprise Valuation Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest='command', help='Valuation command')

    # DCF command
    dcf_parser = subparsers.add_parser('dcf', help='DCF valuation analysis')
    dcf_parser.add_argument('input_file', help='JSON file with FCF projections')
    dcf_parser.add_argument('--output', '-o', help='Output file path')

    # WACC command
    wacc_parser = subparsers.add_parser('wacc', help='WACC calculation')
    wacc_parser.add_argument('input_file', help='JSON file with WACC parameters')
    wacc_parser.add_argument('--output', '-o', help='Output file path')

    # Multiples command
    multiples_parser = subparsers.add_parser('multiples', help='Comparable companies analysis')
    multiples_parser.add_argument('target_file', help='JSON file with target company metrics')
    multiples_parser.add_argument('comps_file', help='JSON file with comparable companies')
    multiples_parser.add_argument('--output', '-o', help='Output file path')

    # Synergy command
    synergy_parser = subparsers.add_parser('synergy', help='Synergy NPV calculation')
    synergy_parser.add_argument('input_file', help='JSON file with synergy items')
    synergy_parser.add_argument('--discount-rate', '-r', type=float, default=0.08,
                                help='Discount rate (default: 0.08)')
    synergy_parser.add_argument('--output', '-o', help='Output file path')

    # Sensitivity command
    sensitivity_parser = subparsers.add_parser('sensitivity', help='Sensitivity analysis matrix')
    sensitivity_parser.add_argument('input_file', help='JSON file with model parameters')
    sensitivity_parser.add_argument('--steps', '-s', type=int, default=5,
                                    help='Number of steps in matrix (default: 5)')
    sensitivity_parser.add_argument('--output', '-o', help='Output file path')

    args = parser.parse_args()

    if args.command == 'dcf':
        handle_dcf_command(args)
    elif args.command == 'wacc':
        handle_wacc_command(args)
    elif args.command == 'multiples':
        handle_multiples_command(args)
    elif args.command == 'synergy':
        handle_synergy_command(args)
    elif args.command == 'sensitivity':
        handle_sensitivity_command(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
