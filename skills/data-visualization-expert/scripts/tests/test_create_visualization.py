"""
Tests for create_visualization.py

Tests core visualization functions to ensure they produce valid matplotlib figures.
"""

import platform

# Add parent directory to path for imports
import sys
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from create_visualization import (
    PALETTES,
    STYLE_CONFIG,
    create_bar_chart,
    create_distribution_plot,
    create_heatmap,
    create_line_chart,
    create_scatter_plot,
    get_japanese_fonts,
    setup_style,
)

# --- Fixtures ---


@pytest.fixture
def sample_categorical_data():
    """Sample data for bar charts"""
    return pd.DataFrame(
        {
            "category": ["A", "B", "C", "D", "E"],
            "value": [100, 250, 180, 300, 150],
            "group": ["X", "X", "Y", "Y", "X"],
        }
    )


@pytest.fixture
def sample_time_series_data():
    """Sample data for line charts"""
    dates = pd.date_range("2024-01-01", periods=12, freq="ME")
    return pd.DataFrame(
        {
            "date": dates,
            "revenue": [100, 110, 105, 120, 130, 125, 140, 150, 145, 160, 170, 180],
            "region": ["North"] * 6 + ["South"] * 6,
        }
    )


@pytest.fixture
def sample_scatter_data():
    """Sample data for scatter plots"""
    np.random.seed(42)
    n = 50
    return pd.DataFrame(
        {
            "x": np.random.randn(n) * 10 + 50,
            "y": np.random.randn(n) * 15 + 100,
            "size": np.random.randint(10, 100, n),
            "category": np.random.choice(["A", "B", "C"], n),
        }
    )


@pytest.fixture
def sample_correlation_matrix():
    """Sample correlation matrix for heatmaps"""
    np.random.seed(42)
    data = np.random.randn(100, 4)
    df = pd.DataFrame(data, columns=["Metric1", "Metric2", "Metric3", "Metric4"])
    return df.corr()


@pytest.fixture
def sample_distribution_data():
    """Sample data for distribution plots"""
    np.random.seed(42)
    return pd.DataFrame(
        {
            "values": np.concatenate([np.random.normal(50, 10, 100), np.random.normal(80, 15, 100)]),
            "group": ["A"] * 100 + ["B"] * 100,
        }
    )


# --- Test Configuration Functions ---


class TestConfiguration:
    """Tests for configuration functions"""

    def test_get_japanese_fonts_returns_list(self):
        """get_japanese_fonts should return a non-empty list"""
        fonts = get_japanese_fonts()
        assert isinstance(fonts, list)
        assert len(fonts) > 0

    def test_get_japanese_fonts_platform_specific(self):
        """get_japanese_fonts should return platform-appropriate fonts"""
        fonts = get_japanese_fonts()
        system = platform.system()

        if system == "Darwin":
            assert "Hiragino Sans" in fonts
        elif system == "Windows":
            assert "Yu Gothic" in fonts
        else:  # Linux
            assert "Noto Sans CJK JP" in fonts

    def test_palettes_defined(self):
        """All expected palettes should be defined"""
        expected_palettes = [
            "default",
            "colorblind_safe",
            "tableau10",
            "corporate",
            "sequential_blue",
            "diverging_rdbu",
            "positive_negative",
        ]
        for palette in expected_palettes:
            assert palette in PALETTES, f"Missing palette: {palette}"
            assert isinstance(PALETTES[palette], list)
            assert len(PALETTES[palette]) >= 3

    def test_style_config_keys(self):
        """STYLE_CONFIG should have essential keys"""
        essential_keys = ["font.size", "axes.titlesize", "axes.grid", "axes.unicode_minus"]
        for key in essential_keys:
            assert key in STYLE_CONFIG, f"Missing config key: {key}"

    def test_setup_style_returns_palette(self):
        """setup_style should return the requested palette"""
        colors = setup_style("colorblind_safe")
        assert colors == PALETTES["colorblind_safe"]

    def test_setup_style_default_palette(self):
        """setup_style should return default palette for unknown names"""
        colors = setup_style("nonexistent_palette")
        assert colors == PALETTES["default"]

    def test_setup_style_configures_matplotlib(self):
        """setup_style should configure matplotlib rcParams"""
        setup_style()
        assert plt.rcParams["axes.unicode_minus"] is False
        assert plt.rcParams["font.family"] == "sans-serif"


# --- Test Chart Creation Functions ---


class TestBarChart:
    """Tests for create_bar_chart function"""

    def test_basic_bar_chart(self, sample_categorical_data):
        """Should create a basic bar chart"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value")
        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) == 1
        plt.close(fig)

    def test_bar_chart_with_title(self, sample_categorical_data):
        """Should include title when specified"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value", title="Test Title")
        ax = fig.axes[0]
        assert ax.get_title() == "Test Title"
        plt.close(fig)

    def test_horizontal_bar_chart(self, sample_categorical_data):
        """Should create horizontal bar chart"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value", horizontal=True)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_bar_chart_with_hue(self, sample_categorical_data):
        """Should create grouped bar chart with hue"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value", hue="group")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_bar_chart_sorted(self, sample_categorical_data):
        """Should create sorted bar chart"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value", sort=True)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_bar_chart_top_n(self, sample_categorical_data):
        """Should limit to top N categories"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value", top_n=3)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestLineChart:
    """Tests for create_line_chart function"""

    def test_basic_line_chart(self, sample_time_series_data):
        """Should create a basic line chart"""
        fig = create_line_chart(sample_time_series_data, x="date", y="revenue")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_line_chart_with_markers(self, sample_time_series_data):
        """Should add markers when specified"""
        fig = create_line_chart(sample_time_series_data, x="date", y="revenue", markers=True)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_line_chart_with_area(self, sample_time_series_data):
        """Should fill area under line when specified"""
        fig = create_line_chart(sample_time_series_data, x="date", y="revenue", show_area=True)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_line_chart_with_hue(self, sample_time_series_data):
        """Should create multi-line chart with hue"""
        fig = create_line_chart(sample_time_series_data, x="date", y="revenue", hue="region")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestScatterPlot:
    """Tests for create_scatter_plot function"""

    def test_basic_scatter_plot(self, sample_scatter_data):
        """Should create a basic scatter plot"""
        fig = create_scatter_plot(sample_scatter_data, x="x", y="y")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_scatter_with_trendline(self, sample_scatter_data):
        """Should add trendline when specified"""
        fig = create_scatter_plot(sample_scatter_data, x="x", y="y", show_trendline=True)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_scatter_with_size(self, sample_scatter_data):
        """Should vary point size when size column specified"""
        fig = create_scatter_plot(sample_scatter_data, x="x", y="y", size="size")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_scatter_with_hue(self, sample_scatter_data):
        """Should color by category when hue specified"""
        fig = create_scatter_plot(sample_scatter_data, x="x", y="y", hue="category")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestHeatmap:
    """Tests for create_heatmap function"""

    def test_basic_heatmap(self, sample_correlation_matrix):
        """Should create a basic heatmap"""
        fig = create_heatmap(sample_correlation_matrix)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_heatmap_with_title(self, sample_correlation_matrix):
        """Should include title when specified"""
        fig = create_heatmap(sample_correlation_matrix, title="Correlation Matrix")
        ax = fig.axes[0]
        assert ax.get_title() == "Correlation Matrix"
        plt.close(fig)

    def test_heatmap_without_annotations(self, sample_correlation_matrix):
        """Should work without annotations"""
        fig = create_heatmap(sample_correlation_matrix, annot=False)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestDistributionPlot:
    """Tests for create_distribution_plot function"""

    def test_histogram(self, sample_distribution_data):
        """Should create a histogram"""
        fig = create_distribution_plot(sample_distribution_data, column="values", plot_type="hist")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_kde_plot(self, sample_distribution_data):
        """Should create a KDE plot"""
        fig = create_distribution_plot(sample_distribution_data, column="values", plot_type="kde")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_box_plot(self, sample_distribution_data):
        """Should create a box plot"""
        fig = create_distribution_plot(sample_distribution_data, column="values", plot_type="box")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_violin_plot(self, sample_distribution_data):
        """Should create a violin plot"""
        fig = create_distribution_plot(sample_distribution_data, column="values", plot_type="violin")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_distribution_with_hue(self, sample_distribution_data):
        """Should group by hue column"""
        fig = create_distribution_plot(sample_distribution_data, column="values", hue="group", plot_type="box")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


# --- Test File Output ---


class TestFileOutput:
    """Tests for file saving functionality"""

    def test_save_png(self, sample_categorical_data):
        """Should save chart as PNG"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value")
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_chart.png"
            fig.savefig(output_path, dpi=100)
            assert output_path.exists()
            assert output_path.stat().st_size > 0
        plt.close(fig)

    def test_save_pdf(self, sample_categorical_data):
        """Should save chart as PDF"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value")
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_chart.pdf"
            fig.savefig(output_path)
            assert output_path.exists()
            assert output_path.stat().st_size > 0
        plt.close(fig)

    def test_save_svg(self, sample_categorical_data):
        """Should save chart as SVG"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value")
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_chart.svg"
            fig.savefig(output_path)
            assert output_path.exists()
            assert output_path.stat().st_size > 0
        plt.close(fig)


# --- Test Color Palettes ---


class TestColorPalettes:
    """Tests for color palette application"""

    def test_colorblind_safe_palette(self, sample_categorical_data):
        """Should apply colorblind-safe palette"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value", palette="colorblind_safe")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_tableau10_palette(self, sample_categorical_data):
        """Should apply tableau10 palette"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value", palette="tableau10")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_corporate_palette(self, sample_categorical_data):
        """Should apply corporate palette"""
        fig = create_bar_chart(sample_categorical_data, x="category", y="value", palette="corporate")
        assert isinstance(fig, plt.Figure)
        plt.close(fig)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
