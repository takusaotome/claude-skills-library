"""Tests for timeseries_analysis.py"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from timeseries_analysis import TimeSeriesAnalysis


@pytest.fixture
def timeseries_data():
    """Create sample time series data"""
    np.random.seed(42)
    dates = pd.date_range(start="2020-01-01", periods=365, freq="D")
    trend = np.linspace(100, 150, 365)
    seasonal = 10 * np.sin(2 * np.pi * np.arange(365) / 7)  # Weekly seasonality
    noise = np.random.randn(365) * 5
    values = trend + seasonal + noise
    return pd.DataFrame({"date": dates, "value": values})


@pytest.fixture
def timeseries_csv(timeseries_data, tmp_path):
    """Create time series data CSV"""
    csv_path = tmp_path / "timeseries_data.csv"
    timeseries_data.to_csv(csv_path, index=False)
    return str(csv_path)


class TestTimeSeriesAnalysis:
    """Tests for TimeSeriesAnalysis class"""

    def test_load_csv(self, timeseries_csv, tmp_path):
        """Test loading CSV file"""
        tsa = TimeSeriesAnalysis(timeseries_csv, "value", date_col="date", output_dir=str(tmp_path / "output"))
        assert len(tsa.df) == 365
        assert "value" in tsa.df.columns

    def test_auto_detect_date_column(self, timeseries_csv, tmp_path):
        """Test auto-detection of date column"""
        tsa = TimeSeriesAnalysis(timeseries_csv, "value", output_dir=str(tmp_path / "output"))
        assert tsa.date_col == "date"

    def test_analyze_basic_stats(self, timeseries_csv, tmp_path):
        """Test basic statistics analysis"""
        output_dir = tmp_path / "output"
        tsa = TimeSeriesAnalysis(timeseries_csv, "value", date_col="date", output_dir=str(output_dir))
        tsa.analyze_basic_stats()

        # Check report contains expected content
        assert any("Data Points" in line for line in tsa.report_lines)
        assert any("Mean" in line for line in tsa.report_lines)
        assert (output_dir / "basic_stats.png").exists()

    def test_test_stationarity(self, timeseries_csv, tmp_path):
        """Test stationarity testing"""
        output_dir = tmp_path / "output"
        tsa = TimeSeriesAnalysis(timeseries_csv, "value", date_col="date", output_dir=str(output_dir))
        tsa.test_stationarity()

        # Check stationarity tests are performed
        assert any("Augmented Dickey-Fuller" in line for line in tsa.report_lines)
        assert any("KPSS" in line for line in tsa.report_lines)
        assert (output_dir / "stationarity.png").exists()

    def test_decompose_series(self, timeseries_csv, tmp_path):
        """Test time series decomposition"""
        output_dir = tmp_path / "output"
        tsa = TimeSeriesAnalysis(timeseries_csv, "value", date_col="date", output_dir=str(output_dir))
        tsa.decompose_series()

        # Check decomposition is performed
        assert any("Strength of Trend" in line for line in tsa.report_lines)
        assert (output_dir / "decomposition_additive.png").exists()

    def test_analyze_autocorrelation(self, timeseries_csv, tmp_path):
        """Test autocorrelation analysis"""
        output_dir = tmp_path / "output"
        tsa = TimeSeriesAnalysis(timeseries_csv, "value", date_col="date", output_dir=str(output_dir))
        tsa.analyze_autocorrelation()

        # Check ACF/PACF plots are generated
        assert (output_dir / "autocorrelation.png").exists()

    def test_forecast(self, timeseries_csv, tmp_path):
        """Test forecasting"""
        output_dir = tmp_path / "output"
        tsa = TimeSeriesAnalysis(timeseries_csv, "value", date_col="date", output_dir=str(output_dir))
        tsa.forecast(periods=30)

        # Check forecast outputs
        assert (output_dir / "forecast.png").exists()
        assert (output_dir / "forecast.csv").exists()

        # Check forecast CSV content
        forecast_df = pd.read_csv(output_dir / "forecast.csv")
        assert len(forecast_df) == 30
        assert "Forecast" in forecast_df.columns

    def test_generate_report(self, timeseries_csv, tmp_path):
        """Test full report generation"""
        output_dir = tmp_path / "output"
        tsa = TimeSeriesAnalysis(timeseries_csv, "value", date_col="date", output_dir=str(output_dir))
        tsa.generate_report(forecast_periods=14)

        # Check report file is created
        assert (output_dir / "timeseries_analysis_report.txt").exists()

        # Check report content
        report_content = (output_dir / "timeseries_analysis_report.txt").read_text()
        assert "TIME SERIES ANALYSIS REPORT" in report_content

    def test_handle_missing_values(self, tmp_path):
        """Test handling of missing values in time series"""
        dates = pd.date_range(start="2020-01-01", periods=100, freq="D")
        values = list(range(100))
        values[10] = None
        values[50] = None
        df = pd.DataFrame({"date": dates, "value": values})

        csv_path = tmp_path / "missing_ts.csv"
        df.to_csv(csv_path, index=False)

        tsa = TimeSeriesAnalysis(str(csv_path), "value", date_col="date", output_dir=str(tmp_path / "output"))
        # Should handle missing values via interpolation
        assert not tsa.ts.isnull().any()

    def test_short_time_series(self, tmp_path):
        """Test handling of short time series"""
        dates = pd.date_range(start="2020-01-01", periods=20, freq="D")
        values = np.random.randn(20)
        df = pd.DataFrame({"date": dates, "value": values})

        csv_path = tmp_path / "short_ts.csv"
        df.to_csv(csv_path, index=False)

        tsa = TimeSeriesAnalysis(str(csv_path), "value", date_col="date", output_dir=str(tmp_path / "output"))
        # Should handle short series gracefully
        tsa.analyze_basic_stats()
        tsa.test_stationarity()

    def test_no_date_column(self, tmp_path):
        """Test handling when no date column is provided"""
        df = pd.DataFrame({"value": np.random.randn(100)})
        csv_path = tmp_path / "no_date_ts.csv"
        df.to_csv(csv_path, index=False)

        tsa = TimeSeriesAnalysis(str(csv_path), "value", output_dir=str(tmp_path / "output"))
        # Should create synthetic date column
        assert tsa.date_col == "index_date"
        assert len(tsa.ts) == 100

    def test_load_excel(self, timeseries_data, tmp_path):
        """Test loading Excel file"""
        xlsx_path = tmp_path / "timeseries_data.xlsx"
        timeseries_data.to_excel(xlsx_path, index=False)

        tsa = TimeSeriesAnalysis(str(xlsx_path), "value", date_col="date", output_dir=str(tmp_path / "output"))
        assert len(tsa.df) == 365

    def test_unsupported_format(self, tmp_path):
        """Test unsupported file format raises error"""
        bad_path = tmp_path / "data.txt"
        bad_path.write_text("invalid")

        with pytest.raises(ValueError, match="Unsupported file format"):
            TimeSeriesAnalysis(str(bad_path), "value", output_dir=str(tmp_path / "output"))
