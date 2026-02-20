#!/usr/bin/env python3
"""
Control Chart Analysis Tool

Analyze process data using Statistical Process Control (SPC) methods.
Supports multiple chart types and Western Electric rules for out-of-control detection.

Usage:
    python control_chart_analysis.py --data measurements.csv --chart-type xbar-r
    python control_chart_analysis.py --data data.csv --subgroup-size 5
"""

import argparse
import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

try:
    import numpy as np
    from scipy import stats

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class ChartType(Enum):
    """Types of control charts."""

    I_MR = "i-mr"  # Individual and Moving Range
    XBAR_R = "xbar-r"  # X-bar and Range
    XBAR_S = "xbar-s"  # X-bar and Standard Deviation
    P = "p"  # Proportion defective
    NP = "np"  # Number defective
    C = "c"  # Count of defects
    U = "u"  # Defects per unit


# Control chart constants
CONSTANTS = {
    # d2: For estimating sigma from average range
    "d2": {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078},
    # d3: For range chart control limits
    "d3": {2: 0.853, 3: 0.888, 4: 0.880, 5: 0.864, 6: 0.848, 7: 0.833, 8: 0.820, 9: 0.808, 10: 0.797},
    # D3: For lower control limit of R chart
    "D3": {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223},
    # D4: For upper control limit of R chart
    "D4": {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777},
    # A2: For X-bar chart control limits (using range)
    "A2": {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373, 9: 0.337, 10: 0.308},
    # c4: For estimating sigma from average standard deviation
    "c4": {2: 0.7979, 3: 0.8862, 4: 0.9213, 5: 0.9400, 6: 0.9515, 7: 0.9594, 8: 0.9650, 9: 0.9693, 10: 0.9727},
    # A3: For X-bar chart control limits (using std dev)
    "A3": {2: 2.659, 3: 1.954, 4: 1.628, 5: 1.427, 6: 1.287, 7: 1.182, 8: 1.099, 9: 1.032, 10: 0.975},
    # B3: For lower control limit of S chart
    "B3": {2: 0, 3: 0, 4: 0, 5: 0, 6: 0.030, 7: 0.118, 8: 0.185, 9: 0.239, 10: 0.284},
    # B4: For upper control limit of S chart
    "B4": {2: 3.267, 3: 2.568, 4: 2.266, 5: 2.089, 6: 1.970, 7: 1.882, 8: 1.815, 9: 1.761, 10: 1.716},
}


@dataclass
class ControlLimits:
    """Control limits for a control chart."""

    ucl: float  # Upper Control Limit
    cl: float  # Center Line
    lcl: float  # Lower Control Limit
    uwl: Optional[float] = None  # Upper Warning Limit (2σ)
    lwl: Optional[float] = None  # Lower Warning Limit (2σ)

    def __post_init__(self):
        """Calculate warning limits if not provided."""
        if self.uwl is None:
            sigma = (self.ucl - self.cl) / 3
            self.uwl = self.cl + 2 * sigma
        if self.lwl is None:
            sigma = (self.cl - self.lcl) / 3
            self.lwl = self.cl - 2 * sigma


@dataclass
class OutOfControlPoint:
    """Represents an out-of-control point with violation details."""

    index: int
    value: float
    rule: str
    description: str


def calculate_imr_limits(data: List[float]) -> Tuple[ControlLimits, ControlLimits]:
    """
    Calculate control limits for Individuals and Moving Range chart.

    Args:
        data: Individual measurements

    Returns:
        Tuple of (I chart limits, MR chart limits)
    """
    if not HAS_NUMPY:
        raise ImportError("numpy required")

    data = np.array(data)

    # Moving ranges
    mr = np.abs(np.diff(data))
    avg_mr = np.mean(mr)

    # Estimate sigma from moving range
    d2 = CONSTANTS["d2"][2]
    sigma = avg_mr / d2

    # I chart limits
    x_bar = np.mean(data)
    i_limits = ControlLimits(ucl=x_bar + 3 * sigma, cl=x_bar, lcl=x_bar - 3 * sigma)

    # MR chart limits
    D3 = CONSTANTS["D3"][2]
    D4 = CONSTANTS["D4"][2]
    mr_limits = ControlLimits(ucl=D4 * avg_mr, cl=avg_mr, lcl=D3 * avg_mr)

    return i_limits, mr_limits


def calculate_xbar_r_limits(data: List[float], subgroup_size: int) -> Tuple[ControlLimits, ControlLimits]:
    """
    Calculate control limits for X-bar and R chart.

    Args:
        data: Measurements (will be grouped into subgroups)
        subgroup_size: Number of samples per subgroup

    Returns:
        Tuple of (X-bar chart limits, R chart limits)
    """
    if not HAS_NUMPY:
        raise ImportError("numpy required")

    data = np.array(data)
    n_subgroups = len(data) // subgroup_size

    # Reshape into subgroups
    subgroups = data[: n_subgroups * subgroup_size].reshape(n_subgroups, subgroup_size)

    # Calculate subgroup statistics
    subgroup_means = np.mean(subgroups, axis=1)
    subgroup_ranges = np.ptp(subgroups, axis=1)  # ptp = peak to peak (max - min)

    x_double_bar = np.mean(subgroup_means)
    r_bar = np.mean(subgroup_ranges)

    # Get constants for subgroup size
    n = min(subgroup_size, 10)
    A2 = CONSTANTS["A2"][n]
    D3 = CONSTANTS["D3"][n]
    D4 = CONSTANTS["D4"][n]

    # X-bar chart limits
    xbar_limits = ControlLimits(ucl=x_double_bar + A2 * r_bar, cl=x_double_bar, lcl=x_double_bar - A2 * r_bar)

    # R chart limits
    r_limits = ControlLimits(ucl=D4 * r_bar, cl=r_bar, lcl=D3 * r_bar)

    return xbar_limits, r_limits


def calculate_xbar_s_limits(data: List[float], subgroup_size: int) -> Tuple[ControlLimits, ControlLimits]:
    """
    Calculate control limits for X-bar and S chart.

    Args:
        data: Measurements
        subgroup_size: Number of samples per subgroup

    Returns:
        Tuple of (X-bar chart limits, S chart limits)
    """
    if not HAS_NUMPY:
        raise ImportError("numpy required")

    data = np.array(data)
    n_subgroups = len(data) // subgroup_size

    subgroups = data[: n_subgroups * subgroup_size].reshape(n_subgroups, subgroup_size)

    subgroup_means = np.mean(subgroups, axis=1)
    subgroup_stds = np.std(subgroups, axis=1, ddof=1)

    x_double_bar = np.mean(subgroup_means)
    s_bar = np.mean(subgroup_stds)

    n = min(subgroup_size, 10)
    A3 = CONSTANTS["A3"][n]
    B3 = CONSTANTS["B3"][n]
    B4 = CONSTANTS["B4"][n]

    xbar_limits = ControlLimits(ucl=x_double_bar + A3 * s_bar, cl=x_double_bar, lcl=x_double_bar - A3 * s_bar)

    s_limits = ControlLimits(ucl=B4 * s_bar, cl=s_bar, lcl=B3 * s_bar)

    return xbar_limits, s_limits


def calculate_p_chart_limits(defectives: List[int], sample_sizes: List[int]) -> ControlLimits:
    """
    Calculate control limits for P chart (proportion defective).

    Args:
        defectives: Number of defectives in each sample
        sample_sizes: Size of each sample

    Returns:
        P chart control limits
    """
    if not HAS_NUMPY:
        raise ImportError("numpy required")

    defectives = np.array(defectives)
    sample_sizes = np.array(sample_sizes)

    p_bar = np.sum(defectives) / np.sum(sample_sizes)
    avg_n = np.mean(sample_sizes)

    sigma_p = np.sqrt(p_bar * (1 - p_bar) / avg_n)

    return ControlLimits(ucl=min(p_bar + 3 * sigma_p, 1.0), cl=p_bar, lcl=max(p_bar - 3 * sigma_p, 0.0))


def calculate_c_chart_limits(defect_counts: List[int]) -> ControlLimits:
    """
    Calculate control limits for C chart (count of defects).

    Args:
        defect_counts: Number of defects in each inspection unit

    Returns:
        C chart control limits
    """
    if not HAS_NUMPY:
        raise ImportError("numpy required")

    c_bar = np.mean(defect_counts)

    return ControlLimits(ucl=c_bar + 3 * np.sqrt(c_bar), cl=c_bar, lcl=max(c_bar - 3 * np.sqrt(c_bar), 0.0))


def detect_western_electric_rules(data: List[float], limits: ControlLimits) -> List[OutOfControlPoint]:
    """
    Detect out-of-control conditions using Western Electric Rules.

    Rules:
    1. One point beyond 3σ (UCL/LCL)
    2. Two of three consecutive points beyond 2σ
    3. Four of five consecutive points beyond 1σ
    4. Eight consecutive points on one side of center line
    5. Six consecutive points trending up or down
    6. Fifteen consecutive points within 1σ (stratification)
    7. Eight consecutive points beyond 1σ (mixture)

    Args:
        data: Process measurements
        limits: Control limits

    Returns:
        List of out-of-control points with details
    """
    if not HAS_NUMPY:
        raise ImportError("numpy required")

    data = np.array(data)
    violations = []

    sigma = (limits.ucl - limits.cl) / 3
    one_sigma = sigma
    two_sigma = 2 * sigma

    # Rule 1: Point beyond 3σ
    for i, value in enumerate(data):
        if value > limits.ucl or value < limits.lcl:
            violations.append(
                OutOfControlPoint(index=i, value=value, rule="Rule 1", description="Point beyond 3σ control limit")
            )

    # Rule 2: Two of three beyond 2σ
    for i in range(2, len(data)):
        window = data[i - 2 : i + 1]
        above_2sigma = np.sum(window > limits.cl + two_sigma)
        below_2sigma = np.sum(window < limits.cl - two_sigma)

        if above_2sigma >= 2:
            violations.append(
                OutOfControlPoint(
                    index=i, value=data[i], rule="Rule 2", description="Two of three consecutive points above 2σ"
                )
            )
        if below_2sigma >= 2:
            violations.append(
                OutOfControlPoint(
                    index=i, value=data[i], rule="Rule 2", description="Two of three consecutive points below 2σ"
                )
            )

    # Rule 3: Four of five beyond 1σ
    for i in range(4, len(data)):
        window = data[i - 4 : i + 1]
        above_1sigma = np.sum(window > limits.cl + one_sigma)
        below_1sigma = np.sum(window < limits.cl - one_sigma)

        if above_1sigma >= 4:
            violations.append(
                OutOfControlPoint(
                    index=i, value=data[i], rule="Rule 3", description="Four of five consecutive points above 1σ"
                )
            )
        if below_1sigma >= 4:
            violations.append(
                OutOfControlPoint(
                    index=i, value=data[i], rule="Rule 3", description="Four of five consecutive points below 1σ"
                )
            )

    # Rule 4: Eight consecutive on one side
    for i in range(7, len(data)):
        window = data[i - 7 : i + 1]
        if np.all(window > limits.cl):
            violations.append(
                OutOfControlPoint(
                    index=i, value=data[i], rule="Rule 4", description="Eight consecutive points above center line"
                )
            )
        if np.all(window < limits.cl):
            violations.append(
                OutOfControlPoint(
                    index=i, value=data[i], rule="Rule 4", description="Eight consecutive points below center line"
                )
            )

    # Rule 5: Six consecutive trending
    for i in range(5, len(data)):
        window = data[i - 5 : i + 1]
        diffs = np.diff(window)
        if np.all(diffs > 0):
            violations.append(
                OutOfControlPoint(
                    index=i, value=data[i], rule="Rule 5", description="Six consecutive points trending upward"
                )
            )
        if np.all(diffs < 0):
            violations.append(
                OutOfControlPoint(
                    index=i, value=data[i], rule="Rule 5", description="Six consecutive points trending downward"
                )
            )

    return violations


def recommend_chart_type(data_type: str, subgroup_size: int = 1) -> str:
    """
    Recommend appropriate control chart type.

    Args:
        data_type: Type of data ('continuous', 'defectives', 'defects')
        subgroup_size: Number of samples per subgroup

    Returns:
        Recommended chart type
    """
    if data_type == "continuous":
        if subgroup_size == 1:
            return "I-MR (Individuals and Moving Range)"
        elif subgroup_size <= 8:
            return "X-bar and R (Mean and Range)"
        else:
            return "X-bar and S (Mean and Std Dev)"
    elif data_type == "defectives":
        if subgroup_size == 1:
            return "NP chart (constant sample size) or P chart (variable)"
        else:
            return "P chart (Proportion Defective)"
    elif data_type == "defects":
        if subgroup_size == 1:
            return "C chart (constant area) or U chart (variable)"
        else:
            return "U chart (Defects per Unit)"
    else:
        return "Unknown data type. Use continuous, defectives, or defects."


def get_full_analysis(data: List[float], chart_type: str = "auto", subgroup_size: int = 1) -> Dict:
    """
    Perform full control chart analysis.

    Args:
        data: Process measurements
        chart_type: Type of chart ('auto', 'i-mr', 'xbar-r', 'xbar-s')
        subgroup_size: Subgroup size

    Returns:
        Complete analysis results
    """
    if not HAS_NUMPY:
        raise ImportError("numpy required")

    data = np.array(data)

    # Auto-detect chart type
    if chart_type == "auto":
        if subgroup_size == 1:
            chart_type = "i-mr"
        elif subgroup_size <= 8:
            chart_type = "xbar-r"
        else:
            chart_type = "xbar-s"

    # Calculate control limits
    if chart_type == "i-mr":
        primary_limits, secondary_limits = calculate_imr_limits(data)
        primary_name = "Individuals"
        secondary_name = "Moving Range"
        primary_data = data
        secondary_data = np.abs(np.diff(data))
    elif chart_type == "xbar-r":
        primary_limits, secondary_limits = calculate_xbar_r_limits(data, subgroup_size)
        primary_name = "X-bar"
        secondary_name = "Range"
        n_subgroups = len(data) // subgroup_size
        subgroups = data[: n_subgroups * subgroup_size].reshape(n_subgroups, subgroup_size)
        primary_data = np.mean(subgroups, axis=1)
        secondary_data = np.ptp(subgroups, axis=1)
    elif chart_type == "xbar-s":
        primary_limits, secondary_limits = calculate_xbar_s_limits(data, subgroup_size)
        primary_name = "X-bar"
        secondary_name = "Std Dev"
        n_subgroups = len(data) // subgroup_size
        subgroups = data[: n_subgroups * subgroup_size].reshape(n_subgroups, subgroup_size)
        primary_data = np.mean(subgroups, axis=1)
        secondary_data = np.std(subgroups, axis=1, ddof=1)
    else:
        raise ValueError(f"Unknown chart type: {chart_type}")

    # Detect out-of-control points
    primary_violations = detect_western_electric_rules(list(primary_data), primary_limits)
    secondary_violations = detect_western_electric_rules(list(secondary_data), secondary_limits)

    # Summary statistics
    in_control = len(primary_violations) == 0 and len(secondary_violations) == 0

    return {
        "chart_type": chart_type.upper(),
        "subgroup_size": subgroup_size,
        "data_points": len(data),
        "primary_chart": {
            "name": primary_name,
            "limits": {
                "UCL": round(primary_limits.ucl, 4),
                "CL": round(primary_limits.cl, 4),
                "LCL": round(primary_limits.lcl, 4),
                "UWL": round(primary_limits.uwl, 4),
                "LWL": round(primary_limits.lwl, 4),
            },
            "violations": [
                {"index": v.index, "value": round(v.value, 4), "rule": v.rule, "description": v.description}
                for v in primary_violations
            ],
        },
        "secondary_chart": {
            "name": secondary_name,
            "limits": {
                "UCL": round(secondary_limits.ucl, 4),
                "CL": round(secondary_limits.cl, 4),
                "LCL": round(secondary_limits.lcl, 4),
            },
            "violations": [
                {"index": v.index, "value": round(v.value, 4), "rule": v.rule, "description": v.description}
                for v in secondary_violations
            ],
        },
        "process_status": "IN CONTROL" if in_control else "OUT OF CONTROL",
        "total_violations": len(primary_violations) + len(secondary_violations),
    }


def print_analysis(analysis: Dict) -> None:
    """Print formatted analysis report."""
    print("\n" + "=" * 70)
    print("CONTROL CHART ANALYSIS REPORT")
    print("=" * 70)

    print(f"\n📊 CHART TYPE: {analysis['chart_type']}")
    print(f"   Subgroup Size: {analysis['subgroup_size']}")
    print(f"   Data Points: {analysis['data_points']}")

    # Primary chart
    primary = analysis["primary_chart"]
    print(f"\n📈 {primary['name'].upper()} CHART:")
    print(f"   UCL: {primary['limits']['UCL']}")
    print(f"   CL:  {primary['limits']['CL']}")
    print(f"   LCL: {primary['limits']['LCL']}")
    print(f"   Violations: {len(primary['violations'])}")

    if primary["violations"]:
        print("\n   Out-of-Control Points:")
        for v in primary["violations"][:5]:  # Show first 5
            print(f"   - Point {v['index']}: {v['value']} ({v['rule']} - {v['description']})")
        if len(primary["violations"]) > 5:
            print(f"   ... and {len(primary['violations']) - 5} more")

    # Secondary chart
    secondary = analysis["secondary_chart"]
    print(f"\n📈 {secondary['name'].upper()} CHART:")
    print(f"   UCL: {secondary['limits']['UCL']}")
    print(f"   CL:  {secondary['limits']['CL']}")
    print(f"   LCL: {secondary['limits']['LCL']}")
    print(f"   Violations: {len(secondary['violations'])}")

    # Process status
    status = analysis["process_status"]
    status_symbol = "✅" if status == "IN CONTROL" else "❌"
    print(f"\n{status_symbol} PROCESS STATUS: {status}")
    print(f"   Total Violations: {analysis['total_violations']}")

    print("\n" + "=" * 70)

    # Western Electric Rules Reference
    print("\n📋 WESTERN ELECTRIC RULES REFERENCE:")
    print("-" * 60)
    print("Rule 1: One point beyond 3σ (UCL/LCL)")
    print("Rule 2: Two of three consecutive points beyond 2σ")
    print("Rule 3: Four of five consecutive points beyond 1σ")
    print("Rule 4: Eight consecutive points on one side of center line")
    print("Rule 5: Six consecutive points trending up or down")
    print("-" * 60)


def generate_sample_data(n: int = 50, in_control: bool = True) -> List[float]:
    """Generate sample process data for demonstration."""
    if not HAS_NUMPY:
        raise ImportError("numpy required")

    np.random.seed(42)

    if in_control:
        # Normal process data
        data = np.random.normal(100, 2, n)
    else:
        # Add some out-of-control conditions
        data = np.random.normal(100, 2, n)
        # Add a shift
        data[30:35] = np.random.normal(108, 2, 5)
        # Add a trend
        data[40:46] = 100 + np.arange(6) * 1.5

    return list(data)


def main():
    parser = argparse.ArgumentParser(
        description="Control Chart Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Analyze data from CSV:
    python control_chart_analysis.py --data measurements.csv

  Specify chart type:
    python control_chart_analysis.py --data data.csv --chart-type xbar-r --subgroup-size 5

  Recommend chart type:
    python control_chart_analysis.py --recommend continuous --subgroup-size 5

  Run demonstration:
    python control_chart_analysis.py --demo
    python control_chart_analysis.py --demo --out-of-control
        """,
    )

    parser.add_argument("--data", "-d", help="Path to CSV file with measurement data")
    parser.add_argument(
        "--chart-type",
        "-c",
        default="auto",
        choices=["auto", "i-mr", "xbar-r", "xbar-s"],
        help="Control chart type (default: auto)",
    )
    parser.add_argument("--subgroup-size", "-n", type=int, default=1, help="Subgroup size (default: 1)")
    parser.add_argument(
        "--recommend", "-r", choices=["continuous", "defectives", "defects"], help="Recommend chart type for data type"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--demo", action="store_true", help="Run demonstration with sample data")
    parser.add_argument("--out-of-control", action="store_true", help="Use out-of-control sample data in demo")

    args = parser.parse_args()

    if args.recommend:
        recommendation = recommend_chart_type(args.recommend, args.subgroup_size)
        print("\n📊 CHART RECOMMENDATION:")
        print(f"   Data Type: {args.recommend}")
        print(f"   Subgroup Size: {args.subgroup_size}")
        print(f"   Recommended Chart: {recommendation}")
        return

    if args.demo:
        print("Running demonstration with sample data...")
        data = generate_sample_data(n=50, in_control=not args.out_of_control)
    elif args.data:
        try:
            if HAS_NUMPY:
                data = list(np.loadtxt(args.data, delimiter=",").flatten())
            else:
                with open(args.data, "r") as f:
                    data = [float(x.strip()) for line in f for x in line.split(",") if x.strip()]
        except Exception as e:
            print(f"Error loading data: {e}")
            return 1
    else:
        parser.print_help()
        return

    try:
        analysis = get_full_analysis(data, chart_type=args.chart_type, subgroup_size=args.subgroup_size)

        if args.json:
            print(json.dumps(analysis, indent=2))
        else:
            print_analysis(analysis)

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    main()
