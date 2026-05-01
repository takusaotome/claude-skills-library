"""Tests for process_capability.py"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from process_capability import (
    ProcessCapabilityAnalyzer,
    SpecificationLimits,
    generate_sample_data,
)


class TestSpecificationLimits:
    """Tests for SpecificationLimits dataclass."""

    def test_basic_creation(self):
        """Test basic specification limits creation."""
        specs = SpecificationLimits(usl=10.5, lsl=9.5)
        assert specs.usl == 10.5
        assert specs.lsl == 9.5
        assert specs.target == 10.0  # Midpoint

    def test_custom_target(self):
        """Test specification with custom target."""
        specs = SpecificationLimits(usl=10.5, lsl=9.5, target=10.2)
        assert specs.target == 10.2

    def test_invalid_limits(self):
        """Test that USL <= LSL raises ValueError."""
        with pytest.raises(ValueError):
            SpecificationLimits(usl=9.0, lsl=10.0)

    def test_equal_limits(self):
        """Test that equal limits raise ValueError."""
        with pytest.raises(ValueError):
            SpecificationLimits(usl=10.0, lsl=10.0)


class TestProcessCapabilityAnalyzer:
    """Tests for ProcessCapabilityAnalyzer class."""

    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing."""
        return generate_sample_data(n=100, mean=10.02, std=0.08, seed=42)

    @pytest.fixture
    def specs(self):
        """Create standard specification limits."""
        return SpecificationLimits(usl=10.5, lsl=9.5, target=10.0)

    @pytest.fixture
    def analyzer(self, sample_data, specs):
        """Create analyzer with sample data."""
        return ProcessCapabilityAnalyzer(sample_data, specs, subgroup_size=1)

    def test_mean_calculation(self, analyzer):
        """Test mean is calculated correctly."""
        assert 9.9 <= analyzer.mean <= 10.1

    def test_std_calculation(self, analyzer):
        """Test standard deviation is calculated."""
        assert analyzer.std_overall > 0
        assert analyzer.std_within > 0

    def test_cp_calculation(self, analyzer):
        """Test Cp calculation."""
        cp = analyzer.calculate_cp()
        # With specs (10.5 - 9.5 = 1.0) and std ~ 0.08, Cp should be > 1.5
        assert cp > 1.0

    def test_cpk_calculation(self, analyzer):
        """Test Cpk calculation."""
        cpk = analyzer.calculate_cpk()
        cp = analyzer.calculate_cp()
        # Cpk should be less than or equal to Cp
        assert cpk <= cp + 0.01  # Small tolerance for floating point

    def test_cpk_less_than_cp_when_off_center(self):
        """Test that Cpk < Cp when process is off-center."""
        # Create data with mean far from target
        import numpy as np

        np.random.seed(42)
        data = list(np.random.normal(10.3, 0.08, 100))  # Mean shifted to 10.3
        specs = SpecificationLimits(usl=10.5, lsl=9.5, target=10.0)
        analyzer = ProcessCapabilityAnalyzer(data, specs)

        cp = analyzer.calculate_cp()
        cpk = analyzer.calculate_cpk()
        assert cpk < cp - 0.1  # Cpk should be noticeably less

    def test_pp_calculation(self, analyzer):
        """Test Pp calculation."""
        pp = analyzer.calculate_pp()
        assert pp > 0

    def test_ppk_calculation(self, analyzer):
        """Test Ppk calculation."""
        ppk = analyzer.calculate_ppk()
        pp = analyzer.calculate_pp()
        assert ppk <= pp + 0.01

    def test_cpm_calculation(self, analyzer):
        """Test Cpm (Taguchi) calculation."""
        cpm = analyzer.calculate_cpm()
        assert cpm > 0

    def test_sigma_level_calculation(self, analyzer):
        """Test sigma level calculation from Cpk."""
        sigma = analyzer.calculate_sigma_level()
        cpk = analyzer.calculate_cpk()
        # Sigma = 3 * Cpk + 1.5
        expected_sigma = 3 * cpk + 1.5
        assert abs(sigma - expected_sigma) < 0.01

    def test_dpmo_calculation(self, analyzer):
        """Test DPMO estimation."""
        dpmo = analyzer.calculate_dpmo()
        assert dpmo >= 0
        assert dpmo <= 1_000_000

    def test_percent_out_of_spec(self, analyzer):
        """Test percent out of specification calculation."""
        below, above, total = analyzer.calculate_percent_out_of_spec()
        assert below >= 0
        assert above >= 0
        assert abs(total - (below + above)) < 0.001

    def test_interpretation_excellent(self):
        """Test interpretation for excellent Cpk."""
        import numpy as np

        np.random.seed(42)
        # Very capable process
        data = list(np.random.normal(10.0, 0.02, 100))
        specs = SpecificationLimits(usl=10.5, lsl=9.5)
        analyzer = ProcessCapabilityAnalyzer(data, specs)

        cpk = analyzer.calculate_cpk()
        interp = analyzer.get_interpretation(cpk)
        assert "Excellent" in interp["rating"] or "Good" in interp["rating"]

    def test_interpretation_poor(self):
        """Test interpretation for poor Cpk."""
        import numpy as np

        np.random.seed(42)
        # Poor process with high variation
        data = list(np.random.normal(10.0, 0.25, 100))
        specs = SpecificationLimits(usl=10.5, lsl=9.5)
        analyzer = ProcessCapabilityAnalyzer(data, specs)

        cpk = analyzer.calculate_cpk()
        interp = analyzer.get_interpretation(cpk)
        assert "Poor" in interp["rating"] or "Marginal" in interp["rating"] or "Unacceptable" in interp["rating"]

    def test_full_report(self, analyzer):
        """Test full report generation."""
        report = analyzer.get_full_report()

        assert "specifications" in report
        assert "process_statistics" in report
        assert "capability_indices" in report
        assert "performance" in report
        assert "interpretation" in report
        assert "comparison" in report

    def test_full_report_specifications(self, analyzer, specs):
        """Test specifications in full report."""
        report = analyzer.get_full_report()

        assert report["specifications"]["USL"] == specs.usl
        assert report["specifications"]["LSL"] == specs.lsl
        assert report["specifications"]["Target"] == specs.target

    def test_full_report_capability_indices(self, analyzer):
        """Test capability indices in full report."""
        report = analyzer.get_full_report()
        indices = report["capability_indices"]

        assert "Cp" in indices
        assert "Cpk" in indices
        assert "Pp" in indices
        assert "Ppk" in indices
        assert "Cpm" in indices


class TestGenerateSampleData:
    """Tests for sample data generation."""

    def test_generates_correct_count(self):
        """Test that correct number of data points are generated."""
        data = generate_sample_data(n=50)
        assert len(data) == 50

    def test_reproducible_with_seed(self):
        """Test that same seed produces same data."""
        data1 = generate_sample_data(n=20, seed=123)
        data2 = generate_sample_data(n=20, seed=123)
        assert data1 == data2

    def test_different_seeds_different_data(self):
        """Test that different seeds produce different data."""
        data1 = generate_sample_data(n=20, seed=123)
        data2 = generate_sample_data(n=20, seed=456)
        assert data1 != data2

    def test_mean_approximately_correct(self):
        """Test that generated data has approximately correct mean."""
        import numpy as np

        data = generate_sample_data(n=1000, mean=50.0, std=1.0)
        assert abs(np.mean(data) - 50.0) < 0.2

    def test_std_approximately_correct(self):
        """Test that generated data has approximately correct std."""
        import numpy as np

        data = generate_sample_data(n=1000, mean=50.0, std=2.0)
        assert abs(np.std(data, ddof=1) - 2.0) < 0.3
