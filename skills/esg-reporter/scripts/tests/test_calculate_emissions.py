"""Tests for calculate_emissions.py"""

import csv
import json

# Add parent directory to path for imports
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from calculate_emissions import (
    EmissionRecord,
    EmissionsCalculator,
    EmissionScope,
    write_csv_output,
)


class TestEmissionsCalculator:
    """Tests for EmissionsCalculator class."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance."""
        return EmissionsCalculator()

    def test_get_available_activity_types(self, calculator):
        """Test getting list of activity types."""
        types = calculator.get_available_activity_types()
        assert len(types) > 0
        assert "natural_gas_m3" in types
        assert "electricity_us_avg" in types
        assert "air_long_haul" in types

    def test_get_emission_factor_valid(self, calculator):
        """Test getting emission factor for valid activity."""
        factor = calculator.get_emission_factor("natural_gas_m3")
        assert factor is not None
        assert factor.value == 1.93
        assert factor.unit == "m³"

    def test_get_emission_factor_invalid(self, calculator):
        """Test getting emission factor for invalid activity."""
        factor = calculator.get_emission_factor("unknown_activity")
        assert factor is None

    def test_get_scope_valid(self, calculator):
        """Test getting scope for valid activity."""
        scope = calculator.get_scope("natural_gas_m3")
        assert scope == EmissionScope.SCOPE_1

        scope = calculator.get_scope("electricity_us_avg")
        assert scope == EmissionScope.SCOPE_2

        scope = calculator.get_scope("air_long_haul")
        assert scope == EmissionScope.SCOPE_3

    def test_get_scope_invalid(self, calculator):
        """Test getting scope for invalid activity."""
        scope = calculator.get_scope("unknown_activity")
        assert scope is None

    def test_calculate_emissions_natural_gas(self, calculator):
        """Test calculating emissions for natural gas."""
        record = calculator.calculate_emissions(
            activity_type="natural_gas_m3", activity_value=10000, source_name="Building A"
        )

        assert record is not None
        assert record.source == "Building A"
        assert record.activity_type == "natural_gas_m3"
        assert record.activity_value == 10000
        assert record.emission_factor == 1.93
        assert record.emissions_kg == pytest.approx(19300, rel=0.01)
        assert record.emissions_tonnes == pytest.approx(19.3, rel=0.01)
        assert record.scope == 1

    def test_calculate_emissions_electricity(self, calculator):
        """Test calculating emissions for electricity."""
        record = calculator.calculate_emissions(
            activity_type="electricity_us_avg", activity_value=500000, source_name="HQ Office"
        )

        assert record is not None
        assert record.emissions_kg == pytest.approx(193000, rel=0.01)
        assert record.emissions_tonnes == pytest.approx(193, rel=0.01)
        assert record.scope == 2

    def test_calculate_emissions_air_travel(self, calculator):
        """Test calculating emissions for air travel."""
        # Long-haul flight: 5000 passenger-km
        record = calculator.calculate_emissions(
            activity_type="air_long_haul", activity_value=5000, source_name="Business Travel"
        )

        assert record is not None
        assert record.emission_factor == 0.150
        assert record.emissions_kg == pytest.approx(750, rel=0.01)
        assert record.scope == 3

    def test_calculate_emissions_invalid_activity(self, calculator):
        """Test calculating emissions for invalid activity."""
        record = calculator.calculate_emissions(activity_type="unknown_activity", activity_value=1000)
        assert record is None

    def test_calculate_from_csv(self, calculator):
        """Test calculating emissions from CSV file."""
        csv_content = """source,activity_type,activity_value
Building A,natural_gas_m3,10000
HQ Office,electricity_us_avg,500000
Travel,air_long_haul,5000
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(csv_content)
            csv_path = Path(f.name)

        try:
            records = calculator.calculate_from_csv(csv_path)
            assert len(records) == 3

            # Check scopes are correct
            scopes = {r.scope for r in records}
            assert scopes == {1, 2, 3}
        finally:
            csv_path.unlink()

    def test_calculate_from_csv_scope_filter(self, calculator):
        """Test filtering by scope when reading CSV."""
        csv_content = """source,activity_type,activity_value
Building A,natural_gas_m3,10000
HQ Office,electricity_us_avg,500000
Travel,air_long_haul,5000
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(csv_content)
            csv_path = Path(f.name)

        try:
            # Only Scope 1 and 2
            records = calculator.calculate_from_csv(csv_path, scopes=[1, 2])
            assert len(records) == 2
            assert all(r.scope in [1, 2] for r in records)
        finally:
            csv_path.unlink()

    def test_summarize_by_scope(self, calculator):
        """Test summarizing emissions by scope."""
        records = [
            EmissionRecord(
                source="A",
                activity_type="gas",
                activity_value=100,
                emission_factor=1.0,
                emissions_kg=1000,
                emissions_tonnes=1.0,
                scope=1,
                unit="m³",
                factor_source="EPA",
            ),
            EmissionRecord(
                source="B",
                activity_type="elec",
                activity_value=200,
                emission_factor=0.5,
                emissions_kg=2000,
                emissions_tonnes=2.0,
                scope=2,
                unit="kWh",
                factor_source="IEA",
            ),
            EmissionRecord(
                source="C",
                activity_type="travel",
                activity_value=300,
                emission_factor=0.1,
                emissions_kg=3000,
                emissions_tonnes=3.0,
                scope=3,
                unit="km",
                factor_source="DEFRA",
            ),
        ]

        summary = calculator.summarize_by_scope(records)
        assert summary[1] == 1.0
        assert summary[2] == 2.0
        assert summary[3] == 3.0

    def test_generate_report_markdown(self, calculator):
        """Test generating Markdown report."""
        records = [
            EmissionRecord(
                source="Building A",
                activity_type="natural_gas_m3",
                activity_value=10000,
                emission_factor=1.93,
                emissions_kg=19300,
                emissions_tonnes=19.3,
                scope=1,
                unit="m³",
                factor_source="EPA",
            ),
        ]

        report = calculator.generate_report(records, "markdown")
        assert "# GHG Emissions Report" in report
        assert "Scope 1" in report
        assert "19.30" in report

    def test_generate_report_json(self, calculator):
        """Test generating JSON report."""
        records = [
            EmissionRecord(
                source="Building A",
                activity_type="natural_gas_m3",
                activity_value=10000,
                emission_factor=1.93,
                emissions_kg=19300,
                emissions_tonnes=19.3,
                scope=1,
                unit="m³",
                factor_source="EPA",
            ),
        ]

        report = calculator.generate_report(records, "json")
        data = json.loads(report)
        assert "summary" in data
        assert "total_tonnes" in data
        assert "records" in data
        assert data["total_tonnes"] == pytest.approx(19.3, rel=0.01)


class TestWriteCsvOutput:
    """Tests for write_csv_output function."""

    def test_write_csv_output(self):
        """Test writing emission records to CSV."""
        records = [
            EmissionRecord(
                source="Building A",
                activity_type="natural_gas_m3",
                activity_value=10000,
                emission_factor=1.93,
                emissions_kg=19300,
                emissions_tonnes=19.3,
                scope=1,
                unit="m³",
                factor_source="EPA",
            ),
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            output_path = Path(f.name)

        try:
            write_csv_output(records, output_path)

            # Read back and verify
            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            assert len(rows) == 1
            assert rows[0]["source"] == "Building A"
            assert rows[0]["activity_type"] == "natural_gas_m3"
            assert float(rows[0]["emissions_tonnes"]) == pytest.approx(19.3, rel=0.01)
        finally:
            output_path.unlink()


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def calculator(self):
        return EmissionsCalculator()

    def test_zero_activity_value(self, calculator):
        """Test calculating with zero activity value."""
        record = calculator.calculate_emissions(activity_type="natural_gas_m3", activity_value=0)
        assert record is not None
        assert record.emissions_kg == 0
        assert record.emissions_tonnes == 0

    def test_large_activity_value(self, calculator):
        """Test calculating with very large activity value."""
        record = calculator.calculate_emissions(
            activity_type="electricity_world_avg",
            activity_value=1_000_000_000,  # 1 TWh
        )
        assert record is not None
        assert record.emissions_tonnes == pytest.approx(494_000, rel=0.01)

    def test_case_insensitive_activity_type(self, calculator):
        """Test that activity types are case-insensitive."""
        record1 = calculator.calculate_emissions("NATURAL_GAS_M3", 1000)
        record2 = calculator.calculate_emissions("natural_gas_m3", 1000)
        record3 = calculator.calculate_emissions("Natural_Gas_M3", 1000)

        assert record1 is not None
        assert record2 is not None
        assert record3 is not None
        assert record1.emissions_kg == record2.emissions_kg == record3.emissions_kg

    def test_empty_source_name(self, calculator):
        """Test calculating with empty source name."""
        record = calculator.calculate_emissions(activity_type="natural_gas_m3", activity_value=1000, source_name="")
        assert record is not None
        # Empty source defaults to activity type
        assert record.source == "natural_gas_m3"

    def test_csv_with_invalid_rows(self, calculator):
        """Test that invalid CSV rows are skipped."""
        csv_content = """source,activity_type,activity_value
Building A,natural_gas_m3,10000
Invalid,unknown_type,5000
Building B,electricity_us_avg,not_a_number
Building C,diesel_liter,1000
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(csv_content)
            csv_path = Path(f.name)

        try:
            records = calculator.calculate_from_csv(csv_path)
            # Should only get 2 valid records (A and C)
            assert len(records) == 2
        finally:
            csv_path.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
