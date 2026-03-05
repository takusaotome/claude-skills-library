"""Tests for model_comparison.py"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from model_comparison import ModelComparison


@pytest.fixture
def regression_data():
    """Create sample regression data"""
    np.random.seed(42)
    n = 200
    X1 = np.random.randn(n)
    X2 = np.random.randn(n)
    y = 3 * X1 + 2 * X2 + np.random.randn(n) * 0.5
    return pd.DataFrame({"feature1": X1, "feature2": X2, "target": y})


@pytest.fixture
def classification_data():
    """Create sample classification data"""
    np.random.seed(42)
    n = 200
    X1 = np.random.randn(n)
    X2 = np.random.randn(n)
    y = (X1 + X2 > 0).astype(int)
    return pd.DataFrame({"feature1": X1, "feature2": X2, "target": y})


@pytest.fixture
def regression_csv(regression_data, tmp_path):
    """Create regression data CSV"""
    csv_path = tmp_path / "regression_data.csv"
    regression_data.to_csv(csv_path, index=False)
    return str(csv_path)


@pytest.fixture
def classification_csv(classification_data, tmp_path):
    """Create classification data CSV"""
    csv_path = tmp_path / "classification_data.csv"
    classification_data.to_csv(csv_path, index=False)
    return str(csv_path)


class TestModelComparison:
    """Tests for ModelComparison class"""

    def test_load_csv(self, regression_csv, tmp_path):
        """Test loading CSV file"""
        mc = ModelComparison(regression_csv, "target", problem_type="regression", output_dir=str(tmp_path / "output"))
        assert len(mc.df) == 200
        assert "feature1" in mc.df.columns

    def test_detect_regression_problem(self, regression_csv, tmp_path):
        """Test auto-detection of regression problem"""
        mc = ModelComparison(regression_csv, "target", output_dir=str(tmp_path / "output"))
        assert mc.problem_type == "regression"

    def test_detect_classification_problem(self, classification_csv, tmp_path):
        """Test auto-detection of classification problem"""
        mc = ModelComparison(classification_csv, "target", output_dir=str(tmp_path / "output"))
        assert mc.problem_type == "classification"

    def test_data_preparation(self, regression_csv, tmp_path):
        """Test data preparation"""
        mc = ModelComparison(regression_csv, "target", problem_type="regression", output_dir=str(tmp_path / "output"))
        assert mc.X_train is not None
        assert mc.X_test is not None
        assert mc.y_train is not None
        assert mc.y_test is not None
        assert len(mc.X_train) > len(mc.X_test)  # 80/20 split

    def test_train_regression_models(self, regression_csv, tmp_path):
        """Test training regression models"""
        output_dir = tmp_path / "output"
        mc = ModelComparison(regression_csv, "target", problem_type="regression", output_dir=str(output_dir))
        mc.train_models(cv=3)

        # Check results are collected
        assert len(mc.results) > 0
        assert len(mc.trained_models) > 0

        # Check metrics are present
        result = mc.results[0]
        assert "Model" in result
        assert "Test_RMSE" in result
        assert "Test_R2" in result

    def test_train_classification_models(self, classification_csv, tmp_path):
        """Test training classification models"""
        output_dir = tmp_path / "output"
        mc = ModelComparison(classification_csv, "target", problem_type="classification", output_dir=str(output_dir))
        mc.train_models(cv=3)

        # Check results are collected
        assert len(mc.results) > 0

        # Check metrics are present
        result = mc.results[0]
        assert "Model" in result
        assert "Test_F1" in result
        assert "Test_Accuracy" in result

    def test_generate_regression_report(self, regression_csv, tmp_path):
        """Test generating regression comparison report"""
        output_dir = tmp_path / "output"
        mc = ModelComparison(regression_csv, "target", problem_type="regression", output_dir=str(output_dir))
        mc.train_models(cv=3)
        mc.generate_comparison_report()

        # Check output files
        assert (output_dir / "model_results.csv").exists()
        assert (output_dir / "model_comparison.png").exists()
        assert (output_dir / "model_comparison_summary.txt").exists()

    def test_generate_classification_report(self, classification_csv, tmp_path):
        """Test generating classification comparison report"""
        output_dir = tmp_path / "output"
        mc = ModelComparison(classification_csv, "target", problem_type="classification", output_dir=str(output_dir))
        mc.train_models(cv=3)
        mc.generate_comparison_report()

        # Check output files
        assert (output_dir / "model_results.csv").exists()
        assert (output_dir / "model_comparison.png").exists()

    def test_handle_categorical_features(self, tmp_path):
        """Test handling of categorical features"""
        np.random.seed(42)
        n = 100
        df = pd.DataFrame(
            {
                "numeric": np.random.randn(n),
                "category": np.random.choice(["A", "B", "C"], n),
                "target": np.random.randn(n),
            }
        )
        csv_path = tmp_path / "mixed_data.csv"
        df.to_csv(csv_path, index=False)

        mc = ModelComparison(str(csv_path), "target", problem_type="regression", output_dir=str(tmp_path / "output"))
        # Should not raise - categorical features are encoded
        assert mc.X_train is not None

    def test_handle_missing_values(self, tmp_path):
        """Test handling of missing values"""
        np.random.seed(42)
        n = 100
        df = pd.DataFrame(
            {
                "feature1": [1, 2, None, 4, 5] * 20,
                "feature2": np.random.randn(n),
                "target": np.random.randn(n),
            }
        )
        csv_path = tmp_path / "missing_data.csv"
        df.to_csv(csv_path, index=False)

        mc = ModelComparison(str(csv_path), "target", problem_type="regression", output_dir=str(tmp_path / "output"))
        # Should not raise - missing values are imputed
        assert not mc.X_train.isnull().any().any()

    def test_get_regression_models(self, regression_csv, tmp_path):
        """Test getting regression models"""
        mc = ModelComparison(regression_csv, "target", problem_type="regression", output_dir=str(tmp_path / "output"))
        models = mc._get_models()

        assert "Linear Regression" in models
        assert "Random Forest" in models
        assert "Gradient Boosting" in models

    def test_get_classification_models(self, classification_csv, tmp_path):
        """Test getting classification models"""
        mc = ModelComparison(
            classification_csv,
            "target",
            problem_type="classification",
            output_dir=str(tmp_path / "output"),
        )
        models = mc._get_models()

        assert "Logistic Regression" in models
        assert "Random Forest" in models
        assert "SVM" in models
