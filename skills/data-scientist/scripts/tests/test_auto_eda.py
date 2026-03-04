"""Tests for auto_eda.py"""

import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auto_eda import AutoEDA


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    np.random.seed(42)
    n = 100
    return pd.DataFrame(
        {
            "numeric1": np.random.randn(n),
            "numeric2": np.random.randn(n) * 10 + 50,
            "category": np.random.choice(["A", "B", "C"], n),
            "target": np.random.choice([0, 1], n),
        }
    )


@pytest.fixture
def sample_csv(sample_data, tmp_path):
    """Create a sample CSV file"""
    csv_path = tmp_path / "test_data.csv"
    sample_data.to_csv(csv_path, index=False)
    return str(csv_path)


class TestAutoEDA:
    """Tests for AutoEDA class"""

    def test_load_csv(self, sample_csv, tmp_path):
        """Test loading CSV file"""
        eda = AutoEDA(sample_csv, output_dir=str(tmp_path / "output"))
        assert len(eda.df) == 100
        assert "numeric1" in eda.df.columns

    def test_load_excel(self, sample_data, tmp_path):
        """Test loading Excel file"""
        xlsx_path = tmp_path / "test_data.xlsx"
        sample_data.to_excel(xlsx_path, index=False)

        eda = AutoEDA(str(xlsx_path), output_dir=str(tmp_path / "output"))
        assert len(eda.df) == 100

    def test_load_unsupported_format(self, tmp_path):
        """Test loading unsupported file format raises error"""
        bad_path = tmp_path / "test_data.txt"
        bad_path.write_text("invalid")

        with pytest.raises(ValueError, match="Unsupported file format"):
            AutoEDA(str(bad_path), output_dir=str(tmp_path / "output"))

    def test_analyze_data_quality(self, sample_csv, tmp_path):
        """Test data quality analysis"""
        eda = AutoEDA(sample_csv, output_dir=str(tmp_path / "output"))
        eda.analyze_data_quality()

        # Check report contains expected content
        assert any("Dataset Shape" in line for line in eda.report_lines)
        assert any("Data Types" in line for line in eda.report_lines)

    def test_analyze_numerical(self, sample_csv, tmp_path):
        """Test numerical analysis"""
        output_dir = tmp_path / "output"
        eda = AutoEDA(sample_csv, output_dir=str(output_dir))
        eda.analyze_numerical()

        # Check visualizations are created
        assert (output_dir / "numerical_distributions.png").exists()
        assert (output_dir / "numerical_boxplots.png").exists()

    def test_analyze_categorical(self, sample_csv, tmp_path):
        """Test categorical analysis"""
        output_dir = tmp_path / "output"
        eda = AutoEDA(sample_csv, output_dir=str(output_dir))
        eda.analyze_categorical()

        # Check report contains category info
        assert any("category" in line.lower() for line in eda.report_lines)

    def test_analyze_target(self, sample_csv, tmp_path):
        """Test target variable analysis"""
        output_dir = tmp_path / "output"
        eda = AutoEDA(sample_csv, target_col="target", output_dir=str(output_dir))
        eda.analyze_target()

        # Check report contains target analysis
        assert any("TARGET VARIABLE ANALYSIS" in line for line in eda.report_lines)
        assert (output_dir / "target_distribution.png").exists()

    def test_generate_report(self, sample_csv, tmp_path):
        """Test full report generation"""
        output_dir = tmp_path / "output"
        eda = AutoEDA(sample_csv, target_col="target", output_dir=str(output_dir))
        eda.generate_report()

        # Check report file is created
        assert (output_dir / "eda_report.txt").exists()

        # Check report content
        report_content = (output_dir / "eda_report.txt").read_text()
        assert "AUTOMATED EDA REPORT" in report_content

    def test_missing_values_handling(self, tmp_path):
        """Test handling of missing values"""
        df = pd.DataFrame(
            {
                "col1": [1, 2, None, 4, 5],
                "col2": [None, None, 3, 4, 5],
            }
        )
        csv_path = tmp_path / "missing_data.csv"
        df.to_csv(csv_path, index=False)

        eda = AutoEDA(str(csv_path), output_dir=str(tmp_path / "output"))
        eda.analyze_data_quality()

        # Check missing values are reported
        assert any("Missing Values" in line for line in eda.report_lines)

    def test_high_cardinality_detection(self, tmp_path):
        """Test detection of high cardinality columns"""
        n = 100
        df = pd.DataFrame(
            {
                "unique_id": range(n),  # 100% unique
                "low_card": ["A"] * n,  # 1 value
            }
        )
        csv_path = tmp_path / "cardinality_data.csv"
        df.to_csv(csv_path, index=False)

        eda = AutoEDA(str(csv_path), output_dir=str(tmp_path / "output"))
        eda.analyze_data_quality()

        # Check cardinality is reported
        assert any("HIGH CARDINALITY" in line for line in eda.report_lines)
        assert any("CONSTANT" in line for line in eda.report_lines)
