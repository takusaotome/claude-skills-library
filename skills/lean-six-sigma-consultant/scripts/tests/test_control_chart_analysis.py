"""Tests for control_chart_analysis.py"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from control_chart_analysis import (
    CONSTANTS,
    ChartType,
    ControlLimits,
    OutOfControlPoint,
    calculate_c_chart_limits,
    calculate_imr_limits,
    calculate_p_chart_limits,
    calculate_xbar_r_limits,
    calculate_xbar_s_limits,
    detect_western_electric_rules,
    generate_sample_data,
    get_full_analysis,
    recommend_chart_type,
)


class TestChartType:
    """Tests for ChartType enum."""

    def test_chart_types_exist(self):
        """Test that all expected chart types exist."""
        assert ChartType.I_MR.value == "i-mr"
        assert ChartType.XBAR_R.value == "xbar-r"
        assert ChartType.XBAR_S.value == "xbar-s"
        assert ChartType.P.value == "p"
        assert ChartType.NP.value == "np"
        assert ChartType.C.value == "c"
        assert ChartType.U.value == "u"


class TestControlLimits:
    """Tests for ControlLimits dataclass."""

    def test_basic_creation(self):
        """Test basic control limits creation."""
        limits = ControlLimits(ucl=110, cl=100, lcl=90)
        assert limits.ucl == 110
        assert limits.cl == 100
        assert limits.lcl == 90

    def test_warning_limits_calculated(self):
        """Test that warning limits are calculated automatically."""
        limits = ControlLimits(ucl=109, cl=100, lcl=91)
        # 2σ should be at ± 6 from center (since 3σ = 9)
        assert abs(limits.uwl - 106) < 0.1
        assert abs(limits.lwl - 94) < 0.1

    def test_custom_warning_limits(self):
        """Test custom warning limits."""
        limits = ControlLimits(ucl=110, cl=100, lcl=90, uwl=107, lwl=93)
        assert limits.uwl == 107
        assert limits.lwl == 93


class TestConstants:
    """Tests for control chart constants."""

    def test_d2_constants(self):
        """Test d2 constants are correct."""
        assert abs(CONSTANTS["d2"][2] - 1.128) < 0.001
        assert abs(CONSTANTS["d2"][5] - 2.326) < 0.001

    def test_a2_constants(self):
        """Test A2 constants are correct."""
        assert abs(CONSTANTS["A2"][2] - 1.880) < 0.001
        assert abs(CONSTANTS["A2"][5] - 0.577) < 0.001

    def test_d4_constants(self):
        """Test D4 constants are correct."""
        assert abs(CONSTANTS["D4"][2] - 3.267) < 0.001
        assert abs(CONSTANTS["D4"][5] - 2.114) < 0.001


class TestCalculateIMRLimits:
    """Tests for I-MR control limit calculation."""

    def test_basic_calculation(self):
        """Test basic I-MR limit calculation."""
        data = generate_sample_data(n=50, in_control=True)
        i_limits, mr_limits = calculate_imr_limits(data)

        assert i_limits.ucl > i_limits.cl > i_limits.lcl
        assert mr_limits.ucl > mr_limits.cl >= mr_limits.lcl

    def test_center_line_is_mean(self):
        """Test that I chart center line is mean of data."""
        import numpy as np

        np.random.seed(42)
        data = list(np.random.normal(100, 2, 50))
        i_limits, _ = calculate_imr_limits(data)

        expected_mean = np.mean(data)
        assert abs(i_limits.cl - expected_mean) < 0.01

    def test_mr_lcl_non_negative(self):
        """Test that MR chart LCL is non-negative."""
        data = generate_sample_data(n=50)
        _, mr_limits = calculate_imr_limits(data)
        assert mr_limits.lcl >= 0


class TestCalculateXbarRLimits:
    """Tests for X-bar/R control limit calculation."""

    def test_basic_calculation(self):
        """Test basic X-bar/R limit calculation."""
        data = generate_sample_data(n=50, in_control=True)
        xbar_limits, r_limits = calculate_xbar_r_limits(data, subgroup_size=5)

        assert xbar_limits.ucl > xbar_limits.cl > xbar_limits.lcl
        assert r_limits.ucl > r_limits.cl >= r_limits.lcl

    def test_different_subgroup_sizes(self):
        """Test with different subgroup sizes."""
        data = generate_sample_data(n=100, in_control=True)

        for n in [2, 3, 5, 10]:
            xbar_limits, r_limits = calculate_xbar_r_limits(data, subgroup_size=n)
            assert xbar_limits.ucl > xbar_limits.cl > xbar_limits.lcl


class TestCalculateXbarSLimits:
    """Tests for X-bar/S control limit calculation."""

    def test_basic_calculation(self):
        """Test basic X-bar/S limit calculation."""
        data = generate_sample_data(n=100, in_control=True)
        xbar_limits, s_limits = calculate_xbar_s_limits(data, subgroup_size=10)

        assert xbar_limits.ucl > xbar_limits.cl > xbar_limits.lcl
        assert s_limits.ucl > s_limits.cl >= s_limits.lcl


class TestCalculatePChartLimits:
    """Tests for P chart control limit calculation."""

    def test_basic_calculation(self):
        """Test basic P chart limit calculation."""
        defectives = [3, 5, 2, 4, 6, 3, 4, 5, 2, 3]
        sample_sizes = [100] * 10
        limits = calculate_p_chart_limits(defectives, sample_sizes)

        assert 0 <= limits.lcl <= limits.cl <= limits.ucl <= 1

    def test_ucl_capped_at_one(self):
        """Test that UCL is capped at 1.0."""
        defectives = [90, 85, 88, 92, 87]
        sample_sizes = [100] * 5
        limits = calculate_p_chart_limits(defectives, sample_sizes)

        assert limits.ucl <= 1.0

    def test_lcl_non_negative(self):
        """Test that LCL is non-negative."""
        defectives = [1, 2, 1, 0, 1]
        sample_sizes = [100] * 5
        limits = calculate_p_chart_limits(defectives, sample_sizes)

        assert limits.lcl >= 0


class TestCalculateCChartLimits:
    """Tests for C chart control limit calculation."""

    def test_basic_calculation(self):
        """Test basic C chart limit calculation."""
        defect_counts = [10, 12, 8, 15, 11, 9, 13, 10, 14, 12]
        limits = calculate_c_chart_limits(defect_counts)

        assert limits.ucl > limits.cl > limits.lcl

    def test_lcl_non_negative(self):
        """Test that LCL is non-negative."""
        defect_counts = [1, 2, 0, 1, 2]
        limits = calculate_c_chart_limits(defect_counts)

        assert limits.lcl >= 0


class TestDetectWesternElectricRules:
    """Tests for Western Electric rule detection."""

    def test_rule_1_point_above_ucl(self):
        """Test Rule 1: point above UCL."""
        import numpy as np

        np.random.seed(42)
        data = list(np.random.normal(100, 2, 50))
        data[25] = 120  # Extreme outlier
        limits = ControlLimits(ucl=106, cl=100, lcl=94)

        violations = detect_western_electric_rules(data, limits)
        rule_1_violations = [v for v in violations if v.rule == "Rule 1"]
        assert len(rule_1_violations) > 0

    def test_rule_1_point_below_lcl(self):
        """Test Rule 1: point below LCL."""
        import numpy as np

        np.random.seed(42)
        data = list(np.random.normal(100, 2, 50))
        data[25] = 80  # Extreme low point
        limits = ControlLimits(ucl=106, cl=100, lcl=94)

        violations = detect_western_electric_rules(data, limits)
        rule_1_violations = [v for v in violations if v.rule == "Rule 1"]
        assert len(rule_1_violations) > 0

    def test_rule_4_eight_consecutive_above(self):
        """Test Rule 4: eight consecutive points above center."""
        import numpy as np

        data = [100.0] * 20
        # 8 consecutive above center line
        for i in range(10, 18):
            data[i] = 103.0
        limits = ControlLimits(ucl=106, cl=100, lcl=94)

        violations = detect_western_electric_rules(data, limits)
        rule_4_violations = [v for v in violations if v.rule == "Rule 4"]
        assert len(rule_4_violations) > 0

    def test_in_control_data_no_violations(self):
        """Test that in-control data has no violations (or minimal)."""
        data = generate_sample_data(n=50, in_control=True)
        i_limits, _ = calculate_imr_limits(data)

        violations = detect_western_electric_rules(data, i_limits)
        # Allow some minor violations due to randomness
        assert len(violations) < 5


class TestRecommendChartType:
    """Tests for chart type recommendation."""

    def test_continuous_individual(self):
        """Test recommendation for continuous individual data."""
        result = recommend_chart_type("continuous", subgroup_size=1)
        assert "I-MR" in result

    def test_continuous_small_subgroup(self):
        """Test recommendation for continuous data with small subgroups."""
        result = recommend_chart_type("continuous", subgroup_size=5)
        assert "X-bar and R" in result

    def test_continuous_large_subgroup(self):
        """Test recommendation for continuous data with large subgroups."""
        result = recommend_chart_type("continuous", subgroup_size=15)
        assert "X-bar and S" in result

    def test_defectives(self):
        """Test recommendation for defectives data."""
        result = recommend_chart_type("defectives", subgroup_size=100)
        assert "P chart" in result

    def test_defects(self):
        """Test recommendation for defects data."""
        result = recommend_chart_type("defects", subgroup_size=1)
        assert "C chart" in result or "U chart" in result


class TestGetFullAnalysis:
    """Tests for full control chart analysis."""

    def test_imr_analysis(self):
        """Test full I-MR analysis."""
        data = generate_sample_data(n=50, in_control=True)
        analysis = get_full_analysis(data, chart_type="i-mr")

        assert analysis["chart_type"] == "I-MR"
        assert "primary_chart" in analysis
        assert "secondary_chart" in analysis
        assert analysis["primary_chart"]["name"] == "Individuals"
        assert analysis["secondary_chart"]["name"] == "Moving Range"

    def test_xbar_r_analysis(self):
        """Test full X-bar/R analysis."""
        data = generate_sample_data(n=100, in_control=True)
        analysis = get_full_analysis(data, chart_type="xbar-r", subgroup_size=5)

        assert analysis["chart_type"] == "XBAR-R"
        assert analysis["primary_chart"]["name"] == "X-bar"
        assert analysis["secondary_chart"]["name"] == "Range"

    def test_auto_chart_type_individual(self):
        """Test auto chart type selection for individual data."""
        data = generate_sample_data(n=50)
        analysis = get_full_analysis(data, chart_type="auto", subgroup_size=1)

        assert analysis["chart_type"] == "I-MR"

    def test_auto_chart_type_subgroup(self):
        """Test auto chart type selection for subgroup data."""
        data = generate_sample_data(n=100)
        analysis = get_full_analysis(data, chart_type="auto", subgroup_size=5)

        assert analysis["chart_type"] == "XBAR-R"

    def test_process_status_in_control(self):
        """Test process status for in-control data."""
        data = generate_sample_data(n=50, in_control=True)
        analysis = get_full_analysis(data, chart_type="i-mr")

        # In-control data should have few or no violations
        assert analysis["total_violations"] < 5

    def test_process_status_out_of_control(self):
        """Test process status for out-of-control data."""
        data = generate_sample_data(n=50, in_control=False)
        analysis = get_full_analysis(data, chart_type="i-mr")

        # Out-of-control data should have violations
        assert analysis["total_violations"] > 0 or analysis["process_status"] == "OUT OF CONTROL"

    def test_invalid_chart_type(self):
        """Test that invalid chart type raises ValueError."""
        data = generate_sample_data(n=50)
        with pytest.raises(ValueError):
            get_full_analysis(data, chart_type="invalid")


class TestGenerateSampleData:
    """Tests for sample data generation."""

    def test_generates_correct_count(self):
        """Test correct number of data points."""
        data = generate_sample_data(n=75)
        assert len(data) == 75

    def test_in_control_data_stable(self):
        """Test that in-control data is relatively stable."""
        import numpy as np

        data = generate_sample_data(n=100, in_control=True)

        # Standard deviation should be reasonable
        assert np.std(data) < 5

    def test_out_of_control_has_outliers(self):
        """Test that out-of-control data has noticeable outliers."""
        import numpy as np

        data = generate_sample_data(n=50, in_control=False)

        # Should have some values far from the center
        deviations = np.abs(np.array(data) - np.mean(data))
        assert np.max(deviations) > 5
