"""Tests for sigma_calculator.py"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sigma_calculator import (
    dpmo_from_defects,
    dpmo_from_sigma,
    dpmo_from_yield,
    dpu_from_defects,
    first_pass_yield,
    get_full_report,
    get_sigma_table,
    rolled_throughput_yield,
    sigma_from_dpmo,
    sigma_from_yield,
    yield_from_dpmo,
    yield_from_sigma,
)


class TestDpmoFromDefects:
    """Tests for dpmo_from_defects function."""

    def test_basic_calculation(self):
        """Test basic DPMO calculation."""
        result = dpmo_from_defects(15, 1000, 5)
        assert result == 3000.0

    def test_single_opportunity(self):
        """Test DPMO with single opportunity per unit."""
        result = dpmo_from_defects(10, 1000, 1)
        assert result == 10000.0

    def test_zero_defects(self):
        """Test DPMO with zero defects."""
        result = dpmo_from_defects(0, 1000, 5)
        assert result == 0.0

    def test_invalid_units(self):
        """Test that invalid units raise ValueError."""
        with pytest.raises(ValueError):
            dpmo_from_defects(10, 0, 5)

    def test_invalid_opportunities(self):
        """Test that invalid opportunities raise ValueError."""
        with pytest.raises(ValueError):
            dpmo_from_defects(10, 1000, 0)


class TestDpuFromDefects:
    """Tests for dpu_from_defects function."""

    def test_basic_calculation(self):
        """Test basic DPU calculation."""
        result = dpu_from_defects(15, 1000)
        assert result == 0.015

    def test_zero_defects(self):
        """Test DPU with zero defects."""
        result = dpu_from_defects(0, 1000)
        assert result == 0.0

    def test_invalid_units(self):
        """Test that invalid units raise ValueError."""
        with pytest.raises(ValueError):
            dpu_from_defects(10, 0)


class TestSigmaConversions:
    """Tests for sigma level conversion functions."""

    def test_sigma_from_dpmo_six_sigma(self):
        """Test sigma from DPMO at Six Sigma level."""
        result = sigma_from_dpmo(3.4)
        assert 5.9 <= result <= 6.1  # Approximately 6 sigma

    def test_sigma_from_dpmo_four_sigma(self):
        """Test sigma from DPMO at 4 sigma level."""
        result = sigma_from_dpmo(6210)
        assert 3.9 <= result <= 4.1

    def test_sigma_from_dpmo_zero(self):
        """Test sigma from DPMO at zero (perfect quality)."""
        result = sigma_from_dpmo(0)
        assert result == 7.5  # 6 + 1.5 shift

    def test_sigma_from_dpmo_million(self):
        """Test sigma from DPMO at 1,000,000 (all defective)."""
        result = sigma_from_dpmo(1_000_000)
        assert result == 1.5  # Just the shift

    def test_dpmo_from_sigma_roundtrip(self):
        """Test roundtrip conversion sigma -> DPMO -> sigma."""
        original_sigma = 4.5
        dpmo = dpmo_from_sigma(original_sigma)
        recovered_sigma = sigma_from_dpmo(dpmo)
        assert abs(recovered_sigma - original_sigma) < 0.01


class TestYieldConversions:
    """Tests for yield conversion functions."""

    def test_yield_from_dpmo(self):
        """Test yield calculation from DPMO."""
        result = yield_from_dpmo(6210)
        assert abs(result - 99.379) < 0.01

    def test_yield_from_dpmo_zero(self):
        """Test yield from zero DPMO."""
        result = yield_from_dpmo(0)
        assert result == 100.0

    def test_dpmo_from_yield(self):
        """Test DPMO calculation from yield."""
        result = dpmo_from_yield(99.38)
        assert abs(result - 6200) < 100

    def test_yield_sigma_roundtrip(self):
        """Test roundtrip conversion yield -> sigma -> yield."""
        original_yield = 95.0
        sigma = sigma_from_yield(original_yield)
        recovered_yield = yield_from_sigma(sigma)
        assert abs(recovered_yield - original_yield) < 0.1


class TestRolledThroughputYield:
    """Tests for rolled throughput yield function."""

    def test_decimal_yields(self):
        """Test RTY with decimal yields."""
        result = rolled_throughput_yield([0.95, 0.98, 0.99])
        assert abs(result - 0.9218) < 0.001

    def test_percentage_yields(self):
        """Test RTY with percentage yields."""
        result = rolled_throughput_yield([95, 98, 99])
        assert abs(result - 0.9218) < 0.001

    def test_single_step(self):
        """Test RTY with single step."""
        result = rolled_throughput_yield([0.95])
        assert result == 0.95

    def test_empty_list(self):
        """Test RTY with empty list."""
        with pytest.raises(ValueError):
            rolled_throughput_yield([])


class TestFirstPassYield:
    """Tests for first pass yield function."""

    def test_basic_calculation(self):
        """Test basic FPY calculation."""
        result = first_pass_yield(90, 100)
        assert result == 0.9

    def test_perfect_yield(self):
        """Test FPY with perfect yield."""
        result = first_pass_yield(100, 100)
        assert result == 1.0

    def test_invalid_units(self):
        """Test FPY with invalid units."""
        with pytest.raises(ValueError):
            first_pass_yield(50, 0)


class TestGetSigmaTable:
    """Tests for sigma level table generation."""

    def test_table_contains_standard_levels(self):
        """Test that table contains standard sigma levels."""
        table = get_sigma_table()
        assert 2.0 in table
        assert 4.0 in table
        assert 6.0 in table

    def test_table_values_reasonable(self):
        """Test that table values are reasonable."""
        table = get_sigma_table()
        # 4 sigma should have DPMO around 6210
        assert 5000 < table[4.0]["dpmo"] < 7000
        # 6 sigma should have very low DPMO
        assert table[6.0]["dpmo"] < 10


class TestGetFullReport:
    """Tests for full report generation."""

    def test_report_from_defects(self):
        """Test report generation from defect data."""
        report = get_full_report(defects=15, units=1000, opportunities=5)
        assert "input" in report
        assert "metrics" in report
        assert "interpretation" in report
        assert report["metrics"]["dpmo"] == 3000.0

    def test_report_from_dpmo(self):
        """Test report generation from DPMO."""
        report = get_full_report(dpmo=6210)
        assert report["input"]["dpmo"] == 6210
        assert 3.9 <= report["metrics"]["sigma_level"] <= 4.1

    def test_report_from_sigma(self):
        """Test report generation from sigma level."""
        report = get_full_report(sigma=4.0)
        assert report["input"]["sigma"] == 4.0

    def test_report_from_yield(self):
        """Test report generation from yield."""
        report = get_full_report(yield_percent=99.38)
        assert report["input"]["yield_percent"] == 99.38

    def test_report_no_input(self):
        """Test that missing input raises ValueError."""
        with pytest.raises(ValueError):
            get_full_report()

    def test_quality_interpretation_world_class(self):
        """Test quality interpretation for world-class performance."""
        report = get_full_report(sigma=6.0)
        quality = report["interpretation"]["quality_level"]
        # Could be "World Class" or "Excellent" depending on exact calculation
        assert "World Class" in quality or "Excellent" in quality

    def test_quality_interpretation_poor(self):
        """Test quality interpretation for poor performance."""
        report = get_full_report(sigma=1.5)
        quality = report["interpretation"]["quality_level"]
        # Could be "Poor" or "Unacceptable" at this level
        assert "Poor" in quality or "Unacceptable" in quality
