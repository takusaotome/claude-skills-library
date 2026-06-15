"""Tests for generate_financial_scenarios.py"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).parent.parent / "generate_financial_scenarios.py"


class TestGenerateFinancialScenarios:
    """Tests for the financial scenarios generator script."""

    def test_generates_csv_file(self, tmp_path: Path) -> None:
        """Test that the script generates a CSV file."""
        output_file = tmp_path / "scenarios.csv"

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-cogs-rate",
                "0.4",
                "--base-opex",
                "30000",
                "--output",
                str(output_file),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert output_file.exists()

    def test_csv_has_correct_headers(self, tmp_path: Path) -> None:
        """Test that the CSV has all expected columns."""
        output_file = tmp_path / "scenarios.csv"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-cogs-rate",
                "0.4",
                "--base-opex",
                "30000",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        with open(output_file) as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

        expected_headers = [
            "scenario",
            "month",
            "revenue",
            "cogs",
            "gross_profit",
            "opex",
            "operating_profit",
            "cogs_rate",
            "growth_rate",
        ]
        assert headers == expected_headers

    def test_generates_three_scenarios(self, tmp_path: Path) -> None:
        """Test that all three scenarios are generated."""
        output_file = tmp_path / "scenarios.csv"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-cogs-rate",
                "0.4",
                "--base-opex",
                "30000",
                "--months",
                "12",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        scenarios = set(row["scenario"] for row in rows)
        assert scenarios == {"upside", "base", "downside"}

    def test_correct_row_count(self, tmp_path: Path) -> None:
        """Test that the correct number of rows are generated."""
        output_file = tmp_path / "scenarios.csv"
        months = 6

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-cogs-rate",
                "0.4",
                "--base-opex",
                "30000",
                "--months",
                str(months),
                "--output",
                str(output_file),
            ],
            check=True,
        )

        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # 3 scenarios * months
        assert len(rows) == 3 * months

    def test_month_one_revenue_matches_base(self, tmp_path: Path) -> None:
        """Test that month 1 revenue matches base revenue for base scenario."""
        output_file = tmp_path / "scenarios.csv"
        base_revenue = 150000.0

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                str(base_revenue),
                "--base-cogs-rate",
                "0.3",
                "--base-opex",
                "40000",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        base_month1 = [r for r in rows if r["scenario"] == "base" and r["month"] == "1"][0]
        assert float(base_month1["revenue"]) == pytest.approx(base_revenue, rel=0.01)

    def test_gross_profit_calculation(self, tmp_path: Path) -> None:
        """Test that gross profit = revenue - cogs."""
        output_file = tmp_path / "scenarios.csv"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-cogs-rate",
                "0.4",
                "--base-opex",
                "30000",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            revenue = float(row["revenue"])
            cogs = float(row["cogs"])
            gross_profit = float(row["gross_profit"])
            assert gross_profit == pytest.approx(revenue - cogs, rel=0.01)

    def test_operating_profit_calculation(self, tmp_path: Path) -> None:
        """Test that operating profit = gross profit - opex."""
        output_file = tmp_path / "scenarios.csv"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-cogs-rate",
                "0.4",
                "--base-opex",
                "30000",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            gross_profit = float(row["gross_profit"])
            opex = float(row["opex"])
            operating_profit = float(row["operating_profit"])
            assert operating_profit == pytest.approx(gross_profit - opex, rel=0.01)

    def test_upside_has_higher_growth(self, tmp_path: Path) -> None:
        """Test that upside scenario has higher growth rate."""
        output_file = tmp_path / "scenarios.csv"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-growth-rate",
                "0.05",
                "--base-cogs-rate",
                "0.4",
                "--base-opex",
                "30000",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        upside_row = [r for r in rows if r["scenario"] == "upside"][0]
        base_row = [r for r in rows if r["scenario"] == "base"][0]
        downside_row = [r for r in rows if r["scenario"] == "downside"][0]

        assert float(upside_row["growth_rate"]) > float(base_row["growth_rate"])
        assert float(base_row["growth_rate"]) > float(downside_row["growth_rate"])

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        """Test that the script creates parent directories if needed."""
        output_file = tmp_path / "nested" / "dir" / "scenarios.csv"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-cogs-rate",
                "0.4",
                "--base-opex",
                "30000",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        assert output_file.exists()

    def test_missing_required_args_fails(self) -> None:
        """Test that missing required arguments cause failure."""
        result = subprocess.run(
            ["python3", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0

    def test_cogs_rate_clamped_to_valid_range(self, tmp_path: Path) -> None:
        """Test that COGS rate is clamped between 0 and 1."""
        output_file = tmp_path / "scenarios.csv"

        # High COGS rate that might exceed 1.0 with downside multiplier
        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-cogs-rate",
                "0.95",  # With 1.15x multiplier would be 1.0925
                "--base-opex",
                "30000",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            cogs_rate = float(row["cogs_rate"])
            assert 0.0 <= cogs_rate <= 1.0

    def test_custom_growth_rate(self, tmp_path: Path) -> None:
        """Test custom base growth rate."""
        output_file = tmp_path / "scenarios.csv"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--base-revenue",
                "100000",
                "--base-growth-rate",
                "0.10",  # 10% monthly growth
                "--base-cogs-rate",
                "0.4",
                "--base-opex",
                "30000",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        base_row = [r for r in rows if r["scenario"] == "base"][0]
        assert float(base_row["growth_rate"]) == pytest.approx(0.10, rel=0.01)
