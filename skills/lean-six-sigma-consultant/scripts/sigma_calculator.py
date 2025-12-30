#!/usr/bin/env python3
"""
Sigma Level Calculator

Calculate sigma level, DPMO, DPU, yield, and related Six Sigma metrics.

Usage:
    python sigma_calculator.py --defects 15 --units 1000 --opportunities 5
    python sigma_calculator.py --sigma 4.0
    python sigma_calculator.py --dpmo 6210
    python sigma_calculator.py --yield 99.38
"""

import argparse
import math
from typing import Tuple, Dict, Optional
from scipy import stats


def dpmo_from_defects(defects: int, units: int, opportunities: int = 1) -> float:
    """
    Calculate Defects Per Million Opportunities (DPMO).

    Args:
        defects: Total number of defects observed
        units: Total number of units inspected
        opportunities: Number of defect opportunities per unit

    Returns:
        DPMO value

    Example:
        >>> dpmo_from_defects(15, 1000, 5)
        3000.0
    """
    if units <= 0 or opportunities <= 0:
        raise ValueError("Units and opportunities must be positive")

    total_opportunities = units * opportunities
    dpmo = (defects / total_opportunities) * 1_000_000
    return dpmo


def dpu_from_defects(defects: int, units: int) -> float:
    """
    Calculate Defects Per Unit (DPU).

    Args:
        defects: Total number of defects
        units: Total number of units

    Returns:
        DPU value
    """
    if units <= 0:
        raise ValueError("Units must be positive")
    return defects / units


def sigma_from_dpmo(dpmo: float, shift: float = 1.5) -> float:
    """
    Calculate sigma level from DPMO.

    Uses the inverse normal distribution with optional shift (default 1.5σ).
    The 1.5σ shift accounts for long-term process variation.

    Args:
        dpmo: Defects Per Million Opportunities
        shift: Sigma shift for long-term performance (default 1.5)

    Returns:
        Sigma level (Z-score + shift)

    Example:
        >>> sigma_from_dpmo(3.4)  # World-class Six Sigma
        6.0
    """
    if dpmo <= 0:
        return 6.0 + shift  # Perfect quality
    if dpmo >= 1_000_000:
        return shift  # All defective

    # Convert DPMO to proportion
    proportion_defective = dpmo / 1_000_000

    # Calculate Z-score using inverse normal
    z_score = stats.norm.ppf(1 - proportion_defective)

    # Add shift for short-term sigma level
    sigma_level = z_score + shift

    return sigma_level


def dpmo_from_sigma(sigma: float, shift: float = 1.5) -> float:
    """
    Calculate DPMO from sigma level.

    Args:
        sigma: Sigma level
        shift: Sigma shift (default 1.5)

    Returns:
        DPMO value

    Example:
        >>> dpmo_from_sigma(6.0)
        3.4
    """
    # Remove shift to get Z-score
    z_score = sigma - shift

    # Calculate proportion defective
    proportion_defective = 1 - stats.norm.cdf(z_score)

    # Convert to DPMO
    dpmo = proportion_defective * 1_000_000

    return dpmo


def yield_from_dpmo(dpmo: float) -> float:
    """
    Calculate yield percentage from DPMO.

    Args:
        dpmo: Defects Per Million Opportunities

    Returns:
        Yield as percentage (0-100)
    """
    return (1 - dpmo / 1_000_000) * 100


def dpmo_from_yield(yield_percent: float) -> float:
    """
    Calculate DPMO from yield percentage.

    Args:
        yield_percent: Yield as percentage (0-100)

    Returns:
        DPMO value
    """
    return (1 - yield_percent / 100) * 1_000_000


def yield_from_sigma(sigma: float, shift: float = 1.5) -> float:
    """
    Calculate yield percentage from sigma level.

    Args:
        sigma: Sigma level
        shift: Sigma shift (default 1.5)

    Returns:
        Yield as percentage
    """
    dpmo = dpmo_from_sigma(sigma, shift)
    return yield_from_dpmo(dpmo)


def sigma_from_yield(yield_percent: float, shift: float = 1.5) -> float:
    """
    Calculate sigma level from yield percentage.

    Args:
        yield_percent: Yield as percentage (0-100)
        shift: Sigma shift (default 1.5)

    Returns:
        Sigma level
    """
    dpmo = dpmo_from_yield(yield_percent)
    return sigma_from_dpmo(dpmo, shift)


def rolled_throughput_yield(yields: list) -> float:
    """
    Calculate Rolled Throughput Yield (RTY) for multi-step processes.

    RTY = Y1 × Y2 × Y3 × ... × Yn

    Args:
        yields: List of yield values as decimals (e.g., [0.95, 0.98, 0.99])
                or as percentages (e.g., [95, 98, 99])

    Returns:
        RTY as decimal

    Example:
        >>> rolled_throughput_yield([0.95, 0.98, 0.99])
        0.9218
    """
    if not yields:
        raise ValueError("Yields list cannot be empty")

    # Convert percentages to decimals if needed
    yields_decimal = []
    for y in yields:
        if y > 1:
            yields_decimal.append(y / 100)
        else:
            yields_decimal.append(y)

    rty = 1.0
    for y in yields_decimal:
        rty *= y

    return rty


def first_pass_yield(units_passed: int, units_started: int) -> float:
    """
    Calculate First Pass Yield (FPY).

    FPY = Units passing first time / Total units started

    Args:
        units_passed: Units passing without rework
        units_started: Total units started

    Returns:
        FPY as decimal
    """
    if units_started <= 0:
        raise ValueError("Units started must be positive")
    return units_passed / units_started


def get_sigma_table() -> Dict[float, Dict[str, float]]:
    """
    Return standard sigma level lookup table.

    Returns:
        Dictionary mapping sigma level to DPMO and yield
    """
    sigma_levels = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
    table = {}

    for sigma in sigma_levels:
        dpmo = dpmo_from_sigma(sigma)
        yield_pct = yield_from_dpmo(dpmo)
        table[sigma] = {
            'dpmo': round(dpmo, 1),
            'yield': round(yield_pct, 4)
        }

    return table


def get_full_report(defects: int = None, units: int = None,
                    opportunities: int = 1, dpmo: float = None,
                    sigma: float = None, yield_percent: float = None) -> Dict:
    """
    Generate comprehensive sigma metrics report.

    Provide one of: (defects, units, opportunities), dpmo, sigma, or yield_percent

    Returns:
        Dictionary with all calculated metrics
    """
    result = {}

    # Calculate DPMO from input
    if defects is not None and units is not None:
        dpmo = dpmo_from_defects(defects, units, opportunities)
        dpu = dpu_from_defects(defects, units)
        result['input'] = {
            'defects': defects,
            'units': units,
            'opportunities_per_unit': opportunities,
            'total_opportunities': units * opportunities,
            'dpu': round(dpu, 4)
        }
    elif dpmo is not None:
        result['input'] = {'dpmo': dpmo}
    elif sigma is not None:
        dpmo = dpmo_from_sigma(sigma)
        result['input'] = {'sigma': sigma}
    elif yield_percent is not None:
        dpmo = dpmo_from_yield(yield_percent)
        result['input'] = {'yield_percent': yield_percent}
    else:
        raise ValueError("Provide defects/units, dpmo, sigma, or yield_percent")

    # Calculate all metrics
    sigma_level = sigma_from_dpmo(dpmo)
    yield_pct = yield_from_dpmo(dpmo)

    result['metrics'] = {
        'dpmo': round(dpmo, 2),
        'sigma_level': round(sigma_level, 2),
        'yield_percent': round(yield_pct, 4),
        'defect_rate_percent': round(100 - yield_pct, 4)
    }

    # Interpretation
    if sigma_level >= 6.0:
        quality = "World Class (Six Sigma)"
    elif sigma_level >= 5.0:
        quality = "Excellent"
    elif sigma_level >= 4.0:
        quality = "Good (Industry Average)"
    elif sigma_level >= 3.0:
        quality = "Acceptable (Needs Improvement)"
    elif sigma_level >= 2.0:
        quality = "Poor"
    else:
        quality = "Unacceptable"

    result['interpretation'] = {
        'quality_level': quality,
        'defects_per_million': f"{dpmo:,.0f} defects per million opportunities",
        'improvement_target': "Target: 6σ = 3.4 DPMO"
    }

    return result


def print_report(report: Dict) -> None:
    """Print formatted report."""
    print("\n" + "=" * 60)
    print("SIGMA LEVEL ANALYSIS REPORT")
    print("=" * 60)

    print("\n📥 INPUT DATA:")
    for key, value in report['input'].items():
        print(f"   {key.replace('_', ' ').title()}: {value}")

    print("\n📊 CALCULATED METRICS:")
    for key, value in report['metrics'].items():
        if 'dpmo' in key.lower():
            print(f"   DPMO: {value:,.2f}")
        elif 'sigma' in key.lower():
            print(f"   Sigma Level: {value}σ")
        elif 'yield' in key.lower():
            print(f"   Yield: {value}%")
        else:
            print(f"   {key.replace('_', ' ').title()}: {value}")

    print("\n📈 INTERPRETATION:")
    for key, value in report['interpretation'].items():
        print(f"   {value}")

    print("\n" + "=" * 60)

    # Print reference table
    print("\n📋 SIGMA LEVEL REFERENCE TABLE:")
    print("-" * 40)
    print(f"{'Sigma':^8} {'DPMO':^12} {'Yield %':^12}")
    print("-" * 40)
    for sigma in [2.0, 3.0, 4.0, 5.0, 6.0]:
        dpmo = dpmo_from_sigma(sigma)
        yield_pct = yield_from_dpmo(dpmo)
        print(f"{sigma:^8.1f} {dpmo:^12,.0f} {yield_pct:^12.4f}")
    print("-" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="Six Sigma Level Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Calculate from defect data:
    python sigma_calculator.py --defects 15 --units 1000 --opportunities 5

  Calculate from DPMO:
    python sigma_calculator.py --dpmo 6210

  Calculate from sigma level:
    python sigma_calculator.py --sigma 4.0

  Calculate from yield:
    python sigma_calculator.py --yield 99.38

  Show sigma table:
    python sigma_calculator.py --table
        """
    )

    parser.add_argument('--defects', '-d', type=int,
                        help='Number of defects observed')
    parser.add_argument('--units', '-u', type=int,
                        help='Number of units inspected')
    parser.add_argument('--opportunities', '-o', type=int, default=1,
                        help='Defect opportunities per unit (default: 1)')
    parser.add_argument('--dpmo', type=float,
                        help='Defects Per Million Opportunities')
    parser.add_argument('--sigma', '-s', type=float,
                        help='Sigma level')
    parser.add_argument('--yield', dest='yield_pct', type=float,
                        help='Yield percentage')
    parser.add_argument('--shift', type=float, default=1.5,
                        help='Sigma shift for long-term (default: 1.5)')
    parser.add_argument('--table', '-t', action='store_true',
                        help='Show sigma level reference table')
    parser.add_argument('--rty', nargs='+', type=float,
                        help='Calculate Rolled Throughput Yield from step yields')

    args = parser.parse_args()

    if args.table:
        print("\n📋 SIGMA LEVEL REFERENCE TABLE (with 1.5σ shift):")
        print("-" * 50)
        print(f"{'Sigma':^10} {'DPMO':^15} {'Yield %':^15}")
        print("-" * 50)
        table = get_sigma_table()
        for sigma, values in table.items():
            print(f"{sigma:^10.1f} {values['dpmo']:^15,.1f} {values['yield']:^15.4f}")
        print("-" * 50)
        return

    if args.rty:
        rty = rolled_throughput_yield(args.rty)
        print(f"\n📊 ROLLED THROUGHPUT YIELD (RTY):")
        print(f"   Step Yields: {args.rty}")
        print(f"   RTY: {rty:.4f} ({rty*100:.2f}%)")
        sigma = sigma_from_yield(rty * 100, args.shift)
        print(f"   Equivalent Sigma Level: {sigma:.2f}σ")
        return

    try:
        if args.defects is not None and args.units is not None:
            report = get_full_report(
                defects=args.defects,
                units=args.units,
                opportunities=args.opportunities
            )
        elif args.dpmo is not None:
            report = get_full_report(dpmo=args.dpmo)
        elif args.sigma is not None:
            report = get_full_report(sigma=args.sigma)
        elif args.yield_pct is not None:
            report = get_full_report(yield_percent=args.yield_pct)
        else:
            parser.print_help()
            return

        print_report(report)

    except ValueError as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    main()
