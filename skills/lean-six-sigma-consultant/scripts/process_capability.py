#!/usr/bin/env python3
"""
Process Capability Analyzer

Calculate process capability indices (Cp, Cpk, Pp, Ppk) and generate reports.

Usage:
    python process_capability.py --data data.csv --lsl 9.5 --usl 10.5
    python process_capability.py --mean 10.0 --std 0.1 --lsl 9.5 --usl 10.5
"""

import argparse
import math
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import sys

try:
    import numpy as np
    from scipy import stats
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


@dataclass
class SpecificationLimits:
    """Specification limits for process capability."""
    usl: float  # Upper Specification Limit
    lsl: float  # Lower Specification Limit
    target: Optional[float] = None  # Target value (defaults to midpoint)

    def __post_init__(self):
        if self.target is None:
            self.target = (self.usl + self.lsl) / 2

        if self.usl <= self.lsl:
            raise ValueError("USL must be greater than LSL")


class ProcessCapabilityAnalyzer:
    """
    Analyze process capability using statistical methods.

    Supports:
    - Cp, Cpk (short-term capability using within-subgroup variation)
    - Pp, Ppk (long-term performance using overall variation)
    - Cpm (Taguchi capability index)
    """

    def __init__(self, data: List[float], specs: SpecificationLimits,
                 subgroup_size: int = 1):
        """
        Initialize analyzer with data and specifications.

        Args:
            data: Process measurement data
            specs: Specification limits (USL, LSL, target)
            subgroup_size: Size of rational subgroups for within variation
        """
        if not HAS_NUMPY:
            raise ImportError("numpy and scipy required. Install with: pip install numpy scipy")

        self.data = np.array(data)
        self.specs = specs
        self.subgroup_size = subgroup_size

        # Calculate statistics
        self.mean = np.mean(self.data)
        self.std_overall = np.std(self.data, ddof=1)  # Sample std dev
        self.std_within = self._calculate_within_std()
        self.n = len(self.data)

    def _calculate_within_std(self) -> float:
        """
        Calculate within-subgroup standard deviation.

        Uses average range method for subgroup_size > 1,
        or moving range method for individual data.
        """
        if self.subgroup_size == 1:
            # Moving Range method for individuals
            mr = np.abs(np.diff(self.data))
            avg_mr = np.mean(mr)
            d2 = 1.128  # d2 constant for n=2
            return avg_mr / d2
        else:
            # Average Range method for subgroups
            n_subgroups = len(self.data) // self.subgroup_size
            ranges = []

            for i in range(n_subgroups):
                start = i * self.subgroup_size
                end = start + self.subgroup_size
                subgroup = self.data[start:end]
                ranges.append(np.max(subgroup) - np.min(subgroup))

            avg_range = np.mean(ranges)

            # d2 constants for different subgroup sizes
            d2_table = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326,
                        6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078}
            d2 = d2_table.get(self.subgroup_size, 3.078)

            return avg_range / d2

    def calculate_cp(self) -> float:
        """
        Calculate Cp (Process Capability).

        Cp = (USL - LSL) / (6 * σ_within)

        Measures potential capability if process were centered.
        """
        tolerance = self.specs.usl - self.specs.lsl
        return tolerance / (6 * self.std_within)

    def calculate_cpk(self) -> float:
        """
        Calculate Cpk (Process Capability Index).

        Cpk = min(CPU, CPL)
        CPU = (USL - μ) / (3 * σ_within)
        CPL = (μ - LSL) / (3 * σ_within)

        Measures actual capability considering process centering.
        """
        cpu = (self.specs.usl - self.mean) / (3 * self.std_within)
        cpl = (self.mean - self.specs.lsl) / (3 * self.std_within)
        return min(cpu, cpl)

    def calculate_pp(self) -> float:
        """
        Calculate Pp (Process Performance).

        Pp = (USL - LSL) / (6 * σ_overall)

        Uses overall standard deviation (long-term variation).
        """
        tolerance = self.specs.usl - self.specs.lsl
        return tolerance / (6 * self.std_overall)

    def calculate_ppk(self) -> float:
        """
        Calculate Ppk (Process Performance Index).

        Ppk = min(PPU, PPL)
        PPU = (USL - μ) / (3 * σ_overall)
        PPL = (μ - LSL) / (3 * σ_overall)
        """
        ppu = (self.specs.usl - self.mean) / (3 * self.std_overall)
        ppl = (self.mean - self.specs.lsl) / (3 * self.std_overall)
        return min(ppu, ppl)

    def calculate_cpm(self) -> float:
        """
        Calculate Cpm (Taguchi Capability Index).

        Cpm = Cp / sqrt(1 + ((μ - Target) / σ)²)

        Penalizes deviation from target value.
        """
        cp = self.calculate_cp()
        deviation_ratio = (self.mean - self.specs.target) / self.std_within
        return cp / math.sqrt(1 + deviation_ratio ** 2)

    def calculate_sigma_level(self) -> float:
        """
        Calculate sigma level from Cpk.

        Sigma Level = 3 * Cpk + 1.5 (with shift)
        """
        cpk = self.calculate_cpk()
        return 3 * cpk + 1.5  # Adding 1.5 sigma shift

    def calculate_dpmo(self) -> float:
        """
        Calculate estimated DPMO from capability.

        Based on proportion outside specification limits.
        """
        z_upper = (self.specs.usl - self.mean) / self.std_overall
        z_lower = (self.mean - self.specs.lsl) / self.std_overall

        prob_defect = stats.norm.sf(z_upper) + stats.norm.cdf(-z_lower)
        return prob_defect * 1_000_000

    def calculate_percent_out_of_spec(self) -> Tuple[float, float, float]:
        """
        Calculate percentage out of specification.

        Returns:
            Tuple of (% below LSL, % above USL, % total out of spec)
        """
        z_upper = (self.specs.usl - self.mean) / self.std_overall
        z_lower = (self.mean - self.specs.lsl) / self.std_overall

        below_lsl = stats.norm.cdf(-z_lower) * 100
        above_usl = stats.norm.sf(z_upper) * 100
        total = below_lsl + above_usl

        return below_lsl, above_usl, total

    def get_interpretation(self, cpk: float) -> Dict[str, str]:
        """
        Get interpretation of Cpk value.

        Returns:
            Dictionary with rating, description, and recommendations
        """
        if cpk >= 2.0:
            return {
                'rating': 'Excellent (World Class)',
                'description': 'Process is highly capable with excellent control',
                'recommendation': 'Maintain current controls, consider reducing inspection',
                'color': 'GREEN'
            }
        elif cpk >= 1.67:
            return {
                'rating': 'Good',
                'description': 'Process meets Six Sigma requirements',
                'recommendation': 'Continue monitoring, look for optimization opportunities',
                'color': 'GREEN'
            }
        elif cpk >= 1.33:
            return {
                'rating': 'Acceptable',
                'description': 'Process is capable but has room for improvement',
                'recommendation': 'Monitor closely, implement improvements when possible',
                'color': 'YELLOW'
            }
        elif cpk >= 1.0:
            return {
                'rating': 'Marginal',
                'description': 'Process barely meets minimum capability',
                'recommendation': 'Improvement required, increase monitoring',
                'color': 'YELLOW'
            }
        elif cpk >= 0.67:
            return {
                'rating': 'Poor',
                'description': 'Process not capable, significant defects expected',
                'recommendation': 'Immediate improvement required, 100% inspection needed',
                'color': 'RED'
            }
        else:
            return {
                'rating': 'Unacceptable',
                'description': 'Process is not capable at all',
                'recommendation': 'Stop production, fundamental process redesign needed',
                'color': 'RED'
            }

    def get_full_report(self) -> Dict:
        """
        Generate comprehensive capability report.
        """
        cp = self.calculate_cp()
        cpk = self.calculate_cpk()
        pp = self.calculate_pp()
        ppk = self.calculate_ppk()
        cpm = self.calculate_cpm()
        sigma = self.calculate_sigma_level()
        dpmo = self.calculate_dpmo()
        below_lsl, above_usl, total_oos = self.calculate_percent_out_of_spec()

        interp = self.get_interpretation(cpk)

        return {
            'specifications': {
                'USL': self.specs.usl,
                'LSL': self.specs.lsl,
                'Target': self.specs.target,
                'Tolerance': self.specs.usl - self.specs.lsl
            },
            'process_statistics': {
                'Sample_Size': self.n,
                'Mean': round(self.mean, 4),
                'Std_Dev_Within': round(self.std_within, 4),
                'Std_Dev_Overall': round(self.std_overall, 4),
                'Min': round(float(np.min(self.data)), 4),
                'Max': round(float(np.max(self.data)), 4)
            },
            'capability_indices': {
                'Cp': round(cp, 3),
                'Cpk': round(cpk, 3),
                'Pp': round(pp, 3),
                'Ppk': round(ppk, 3),
                'Cpm': round(cpm, 3)
            },
            'performance': {
                'Sigma_Level': round(sigma, 2),
                'DPMO_Estimated': round(dpmo, 0),
                'Yield_Percent': round(100 - (dpmo / 10000), 4),
                'Percent_Below_LSL': round(below_lsl, 4),
                'Percent_Above_USL': round(above_usl, 4),
                'Percent_Out_of_Spec': round(total_oos, 4)
            },
            'interpretation': interp,
            'comparison': {
                'Cp_vs_Cpk': 'Centered' if abs(cp - cpk) < 0.1 else 'Off-center',
                'Short_vs_Long_Term': 'Stable' if abs(cpk - ppk) < 0.2 else 'Special causes present'
            }
        }


def print_report(report: Dict) -> None:
    """Print formatted capability report."""
    print("\n" + "=" * 70)
    print("PROCESS CAPABILITY ANALYSIS REPORT")
    print("=" * 70)

    print("\n📐 SPECIFICATION LIMITS:")
    for key, value in report['specifications'].items():
        print(f"   {key}: {value}")

    print("\n📊 PROCESS STATISTICS:")
    for key, value in report['process_statistics'].items():
        print(f"   {key.replace('_', ' ')}: {value}")

    print("\n📈 CAPABILITY INDICES:")
    indices = report['capability_indices']
    print(f"   {'Index':<8} {'Value':>8}  {'Interpretation'}")
    print("   " + "-" * 50)
    print(f"   {'Cp':<8} {indices['Cp']:>8.3f}  Potential (if centered)")
    print(f"   {'Cpk':<8} {indices['Cpk']:>8.3f}  Actual (short-term)")
    print(f"   {'Pp':<8} {indices['Pp']:>8.3f}  Potential (long-term)")
    print(f"   {'Ppk':<8} {indices['Ppk']:>8.3f}  Actual (long-term)")
    print(f"   {'Cpm':<8} {indices['Cpm']:>8.3f}  Taguchi (target-based)")

    print("\n⚡ PERFORMANCE METRICS:")
    perf = report['performance']
    print(f"   Sigma Level: {perf['Sigma_Level']}σ")
    print(f"   Estimated DPMO: {perf['DPMO_Estimated']:,.0f}")
    print(f"   Expected Yield: {perf['Yield_Percent']:.4f}%")
    print(f"   % Below LSL: {perf['Percent_Below_LSL']:.4f}%")
    print(f"   % Above USL: {perf['Percent_Above_USL']:.4f}%")
    print(f"   % Total Out of Spec: {perf['Percent_Out_of_Spec']:.4f}%")

    interp = report['interpretation']
    print(f"\n🎯 INTERPRETATION: [{interp['color']}]")
    print(f"   Rating: {interp['rating']}")
    print(f"   {interp['description']}")
    print(f"   Recommendation: {interp['recommendation']}")

    print("\n🔍 ANALYSIS:")
    comp = report['comparison']
    print(f"   Process Centering: {comp['Cp_vs_Cpk']}")
    print(f"   Process Stability: {comp['Short_vs_Long_Term']}")

    print("\n" + "=" * 70)

    # Capability reference table
    print("\n📋 CAPABILITY INDEX REFERENCE:")
    print("-" * 50)
    print(f"{'Cpk Range':<15} {'Rating':<20} {'% Defects'}")
    print("-" * 50)
    print(f"{'≥ 2.00':<15} {'World Class':<20} < 0.002%")
    print(f"{'1.67 - 2.00':<15} {'Good (6σ target)':<20} < 0.006%")
    print(f"{'1.33 - 1.67':<15} {'Acceptable':<20} < 0.063%")
    print(f"{'1.00 - 1.33':<15} {'Marginal':<20} < 0.27%")
    print(f"{'< 1.00':<15} {'Poor/Unacceptable':<20} > 0.27%")
    print("-" * 50)


def generate_sample_data(n: int = 100, mean: float = 10.0,
                         std: float = 0.1, seed: int = 42) -> List[float]:
    """Generate sample process data for demonstration."""
    if not HAS_NUMPY:
        raise ImportError("numpy required for sample data generation")

    np.random.seed(seed)
    return list(np.random.normal(mean, std, n))


def main():
    parser = argparse.ArgumentParser(
        description="Process Capability Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  From data file:
    python process_capability.py --data measurements.csv --lsl 9.5 --usl 10.5

  From parameters:
    python process_capability.py --mean 10.0 --std 0.1 --lsl 9.5 --usl 10.5 --n 100

  With target value:
    python process_capability.py --data data.csv --lsl 9.5 --usl 10.5 --target 10.0

  Generate sample report:
    python process_capability.py --demo
        """
    )

    parser.add_argument('--data', '-d',
                        help='Path to CSV file with measurement data')
    parser.add_argument('--mean', '-m', type=float,
                        help='Process mean (if no data file)')
    parser.add_argument('--std', '-s', type=float,
                        help='Process standard deviation (if no data file)')
    parser.add_argument('--n', type=int, default=100,
                        help='Sample size for simulation (default: 100)')
    parser.add_argument('--lsl', type=float, required='--demo' not in sys.argv,
                        help='Lower Specification Limit')
    parser.add_argument('--usl', type=float, required='--demo' not in sys.argv,
                        help='Upper Specification Limit')
    parser.add_argument('--target', '-t', type=float,
                        help='Target value (default: midpoint of specs)')
    parser.add_argument('--subgroup', type=int, default=1,
                        help='Subgroup size for within variation (default: 1)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--demo', action='store_true',
                        help='Run demonstration with sample data')

    args = parser.parse_args()

    if args.demo:
        print("Running demonstration with sample data...")
        data = generate_sample_data(n=100, mean=10.02, std=0.08)
        specs = SpecificationLimits(usl=10.5, lsl=9.5, target=10.0)
    elif args.data:
        # Load data from file
        try:
            if HAS_NUMPY:
                data = list(np.loadtxt(args.data, delimiter=',').flatten())
            else:
                with open(args.data, 'r') as f:
                    data = [float(x.strip()) for line in f
                            for x in line.split(',') if x.strip()]
        except Exception as e:
            print(f"Error loading data: {e}")
            return 1
        specs = SpecificationLimits(usl=args.usl, lsl=args.lsl, target=args.target)
    elif args.mean is not None and args.std is not None:
        # Generate data from parameters
        data = generate_sample_data(n=args.n, mean=args.mean, std=args.std)
        specs = SpecificationLimits(usl=args.usl, lsl=args.lsl, target=args.target)
    else:
        parser.print_help()
        return 1

    try:
        analyzer = ProcessCapabilityAnalyzer(data, specs, args.subgroup)
        report = analyzer.get_full_report()

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_report(report)

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    main()
