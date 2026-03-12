#!/usr/bin/env python3
"""
GHG Emissions Calculator for ESG Reporting

Calculates Scope 1, 2, and 3 greenhouse gas emissions from activity data.
Supports multiple fuel types, electricity grids, and transportation modes.

Usage:
    python calculate_emissions.py --input energy_data.csv --output emissions.csv
    python calculate_emissions.py --input data.csv --scope 1,2 --output scope12.csv
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class EmissionScope(Enum):
    """GHG Protocol emission scopes."""

    SCOPE_1 = 1  # Direct emissions
    SCOPE_2 = 2  # Indirect energy emissions
    SCOPE_3 = 3  # Value chain emissions


@dataclass
class EmissionFactor:
    """Emission factor with metadata."""

    value: float  # kg CO2e per unit
    unit: str
    source: str
    year: int = 2023


# Emission factors database (kg CO2e per unit)
EMISSION_FACTORS = {
    # Scope 1: Stationary combustion (kg CO2e per unit)
    "natural_gas_m3": EmissionFactor(1.93, "m³", "EPA", 2023),
    "natural_gas_mmbtu": EmissionFactor(53.06, "MMBtu", "EPA", 2023),
    "natural_gas_therm": EmissionFactor(5.31, "therm", "EPA", 2023),
    "diesel_liter": EmissionFactor(2.68, "liter", "EPA", 2023),
    "diesel_gallon": EmissionFactor(10.21, "gallon", "EPA", 2023),
    "gasoline_liter": EmissionFactor(2.31, "liter", "EPA", 2023),
    "gasoline_gallon": EmissionFactor(8.78, "gallon", "EPA", 2023),
    "lpg_liter": EmissionFactor(1.51, "liter", "EPA", 2023),
    "lpg_gallon": EmissionFactor(5.72, "gallon", "EPA", 2023),
    "coal_kg": EmissionFactor(2.42, "kg", "IPCC", 2023),
    "heating_oil_liter": EmissionFactor(2.52, "liter", "EPA", 2023),
    # Scope 1: Mobile combustion (kg CO2e per km)
    "vehicle_gasoline_km": EmissionFactor(0.21, "km", "DEFRA", 2023),
    "vehicle_diesel_km": EmissionFactor(0.17, "km", "DEFRA", 2023),
    "truck_light_km": EmissionFactor(0.27, "km", "DEFRA", 2023),
    "truck_heavy_km": EmissionFactor(0.89, "km", "DEFRA", 2023),
    # Scope 2: Electricity by region (kg CO2e per kWh)
    "electricity_us_avg": EmissionFactor(0.386, "kWh", "eGRID", 2022),
    "electricity_us_california": EmissionFactor(0.225, "kWh", "eGRID", 2022),
    "electricity_us_texas": EmissionFactor(0.398, "kWh", "eGRID", 2022),
    "electricity_us_midwest": EmissionFactor(0.499, "kWh", "eGRID", 2022),
    "electricity_eu_avg": EmissionFactor(0.256, "kWh", "IEA", 2022),
    "electricity_uk": EmissionFactor(0.207, "kWh", "DEFRA", 2022),
    "electricity_germany": EmissionFactor(0.385, "kWh", "IEA", 2022),
    "electricity_france": EmissionFactor(0.056, "kWh", "IEA", 2022),
    "electricity_japan": EmissionFactor(0.471, "kWh", "IEA", 2022),
    "electricity_china": EmissionFactor(0.582, "kWh", "IEA", 2022),
    "electricity_india": EmissionFactor(0.708, "kWh", "IEA", 2022),
    "electricity_world_avg": EmissionFactor(0.494, "kWh", "IEA", 2022),
    # Scope 2: Steam and heating (kg CO2e per kWh)
    "steam_natural_gas": EmissionFactor(0.067, "kWh", "EPA", 2023),
    "district_heating": EmissionFactor(0.18, "kWh", "IEA", 2022),
    "district_cooling": EmissionFactor(0.15, "kWh", "IEA", 2022),
    # Scope 3: Business travel (kg CO2e per passenger-km)
    "air_short_haul": EmissionFactor(0.255, "passenger-km", "DEFRA", 2023),
    "air_medium_haul": EmissionFactor(0.156, "passenger-km", "DEFRA", 2023),
    "air_long_haul": EmissionFactor(0.150, "passenger-km", "DEFRA", 2023),
    "rail_travel": EmissionFactor(0.041, "passenger-km", "DEFRA", 2023),
    "taxi_km": EmissionFactor(0.149, "km", "DEFRA", 2023),
    "hotel_night": EmissionFactor(20.0, "night", "DEFRA", 2023),
    # Scope 3: Freight (kg CO2e per tonne-km)
    "freight_road": EmissionFactor(0.062, "tonne-km", "DEFRA", 2023),
    "freight_rail": EmissionFactor(0.022, "tonne-km", "DEFRA", 2023),
    "freight_sea": EmissionFactor(0.016, "tonne-km", "DEFRA", 2023),
    "freight_air": EmissionFactor(0.602, "tonne-km", "DEFRA", 2023),
    # Scope 3: Employee commuting (kg CO2e per km)
    "commute_car": EmissionFactor(0.17, "km", "DEFRA", 2023),
    "commute_bus": EmissionFactor(0.089, "km", "DEFRA", 2023),
    "commute_subway": EmissionFactor(0.041, "km", "DEFRA", 2023),
}

# Scope classification
SCOPE_MAPPING = {
    # Scope 1
    "natural_gas_m3": EmissionScope.SCOPE_1,
    "natural_gas_mmbtu": EmissionScope.SCOPE_1,
    "natural_gas_therm": EmissionScope.SCOPE_1,
    "diesel_liter": EmissionScope.SCOPE_1,
    "diesel_gallon": EmissionScope.SCOPE_1,
    "gasoline_liter": EmissionScope.SCOPE_1,
    "gasoline_gallon": EmissionScope.SCOPE_1,
    "lpg_liter": EmissionScope.SCOPE_1,
    "lpg_gallon": EmissionScope.SCOPE_1,
    "coal_kg": EmissionScope.SCOPE_1,
    "heating_oil_liter": EmissionScope.SCOPE_1,
    "vehicle_gasoline_km": EmissionScope.SCOPE_1,
    "vehicle_diesel_km": EmissionScope.SCOPE_1,
    "truck_light_km": EmissionScope.SCOPE_1,
    "truck_heavy_km": EmissionScope.SCOPE_1,
    # Scope 2
    "electricity_us_avg": EmissionScope.SCOPE_2,
    "electricity_us_california": EmissionScope.SCOPE_2,
    "electricity_us_texas": EmissionScope.SCOPE_2,
    "electricity_us_midwest": EmissionScope.SCOPE_2,
    "electricity_eu_avg": EmissionScope.SCOPE_2,
    "electricity_uk": EmissionScope.SCOPE_2,
    "electricity_germany": EmissionScope.SCOPE_2,
    "electricity_france": EmissionScope.SCOPE_2,
    "electricity_japan": EmissionScope.SCOPE_2,
    "electricity_china": EmissionScope.SCOPE_2,
    "electricity_india": EmissionScope.SCOPE_2,
    "electricity_world_avg": EmissionScope.SCOPE_2,
    "steam_natural_gas": EmissionScope.SCOPE_2,
    "district_heating": EmissionScope.SCOPE_2,
    "district_cooling": EmissionScope.SCOPE_2,
    # Scope 3
    "air_short_haul": EmissionScope.SCOPE_3,
    "air_medium_haul": EmissionScope.SCOPE_3,
    "air_long_haul": EmissionScope.SCOPE_3,
    "rail_travel": EmissionScope.SCOPE_3,
    "taxi_km": EmissionScope.SCOPE_3,
    "hotel_night": EmissionScope.SCOPE_3,
    "freight_road": EmissionScope.SCOPE_3,
    "freight_rail": EmissionScope.SCOPE_3,
    "freight_sea": EmissionScope.SCOPE_3,
    "freight_air": EmissionScope.SCOPE_3,
    "commute_car": EmissionScope.SCOPE_3,
    "commute_bus": EmissionScope.SCOPE_3,
    "commute_subway": EmissionScope.SCOPE_3,
}


@dataclass
class EmissionRecord:
    """Single emission calculation record."""

    source: str
    activity_type: str
    activity_value: float
    emission_factor: float
    emissions_kg: float
    emissions_tonnes: float
    scope: int
    unit: str
    factor_source: str


class EmissionsCalculator:
    """Calculate GHG emissions from activity data."""

    def __init__(self):
        self.emission_factors = EMISSION_FACTORS
        self.scope_mapping = SCOPE_MAPPING

    def get_available_activity_types(self) -> list[str]:
        """Return list of available activity types."""
        return sorted(self.emission_factors.keys())

    def get_emission_factor(self, activity_type: str) -> Optional[EmissionFactor]:
        """Get emission factor for activity type."""
        return self.emission_factors.get(activity_type.lower())

    def get_scope(self, activity_type: str) -> Optional[EmissionScope]:
        """Get scope for activity type."""
        return self.scope_mapping.get(activity_type.lower())

    def calculate_emissions(
        self, activity_type: str, activity_value: float, source_name: str = ""
    ) -> Optional[EmissionRecord]:
        """
        Calculate emissions for a single activity.

        Args:
            activity_type: Type of activity (e.g., 'natural_gas_m3', 'electricity_us_avg')
            activity_value: Amount of activity (in appropriate units)
            source_name: Optional name for the emission source

        Returns:
            EmissionRecord with calculation results, or None if activity type unknown
        """
        factor = self.get_emission_factor(activity_type)
        scope = self.get_scope(activity_type)

        if factor is None or scope is None:
            return None

        emissions_kg = activity_value * factor.value
        emissions_tonnes = emissions_kg / 1000

        return EmissionRecord(
            source=source_name or activity_type,
            activity_type=activity_type,
            activity_value=activity_value,
            emission_factor=factor.value,
            emissions_kg=emissions_kg,
            emissions_tonnes=emissions_tonnes,
            scope=scope.value,
            unit=factor.unit,
            factor_source=factor.source,
        )

    def calculate_from_csv(self, input_path: Path, scopes: Optional[list[int]] = None) -> list[EmissionRecord]:
        """
        Calculate emissions from CSV file.

        Expected CSV format:
            source,activity_type,activity_value

        Args:
            input_path: Path to input CSV file
            scopes: Optional list of scopes to include (1, 2, 3)

        Returns:
            List of EmissionRecord objects
        """
        records = []

        with open(input_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                source = row.get("source", "")
                activity_type = row.get("activity_type", "")

                try:
                    activity_value = float(row.get("activity_value", 0))
                except ValueError:
                    continue

                record = self.calculate_emissions(
                    activity_type=activity_type, activity_value=activity_value, source_name=source
                )

                if record:
                    if scopes is None or record.scope in scopes:
                        records.append(record)

        return records

    def summarize_by_scope(self, records: list[EmissionRecord]) -> dict[int, float]:
        """Summarize emissions by scope."""
        summary = {1: 0.0, 2: 0.0, 3: 0.0}

        for record in records:
            summary[record.scope] += record.emissions_tonnes

        return summary

    def generate_report(self, records: list[EmissionRecord], output_format: str = "markdown") -> str:
        """Generate emissions report."""
        summary = self.summarize_by_scope(records)
        total = sum(summary.values())

        if output_format == "markdown":
            lines = [
                "# GHG Emissions Report",
                "",
                "## Summary by Scope",
                "",
                "| Scope | Emissions (tCO2e) | % of Total |",
                "|-------|-------------------|------------|",
            ]

            for scope, emissions in sorted(summary.items()):
                pct = (emissions / total * 100) if total > 0 else 0
                lines.append(f"| Scope {scope} | {emissions:,.2f} | {pct:.1f}% |")

            lines.extend(
                [
                    f"| **Total** | **{total:,.2f}** | **100%** |",
                    "",
                    "## Detailed Breakdown",
                    "",
                    "| Source | Activity Type | Value | Unit | Emissions (tCO2e) | Scope |",
                    "|--------|---------------|-------|------|-------------------|-------|",
                ]
            )

            for record in sorted(records, key=lambda r: (-r.scope, -r.emissions_tonnes)):
                lines.append(
                    f"| {record.source} | {record.activity_type} | "
                    f"{record.activity_value:,.2f} | {record.unit} | "
                    f"{record.emissions_tonnes:,.2f} | {record.scope} |"
                )

            return "\n".join(lines)

        elif output_format == "json":
            return json.dumps(
                {
                    "summary": {f"scope_{k}": v for k, v in summary.items()},
                    "total_tonnes": total,
                    "records": [
                        {
                            "source": r.source,
                            "activity_type": r.activity_type,
                            "activity_value": r.activity_value,
                            "unit": r.unit,
                            "emissions_tonnes": r.emissions_tonnes,
                            "scope": r.scope,
                        }
                        for r in records
                    ],
                },
                indent=2,
            )

        else:
            raise ValueError(f"Unknown output format: {output_format}")


def write_csv_output(records: list[EmissionRecord], output_path: Path) -> None:
    """Write emission records to CSV file."""
    fieldnames = [
        "source",
        "activity_type",
        "activity_value",
        "unit",
        "emission_factor",
        "factor_source",
        "emissions_kg",
        "emissions_tonnes",
        "scope",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            writer.writerow(
                {
                    "source": record.source,
                    "activity_type": record.activity_type,
                    "activity_value": record.activity_value,
                    "unit": record.unit,
                    "emission_factor": record.emission_factor,
                    "factor_source": record.factor_source,
                    "emissions_kg": record.emissions_kg,
                    "emissions_tonnes": record.emissions_tonnes,
                    "scope": record.scope,
                }
            )


def main():
    parser = argparse.ArgumentParser(description="Calculate GHG emissions from activity data")
    parser.add_argument("--input", "-i", type=Path, help="Input CSV file with activity data")
    parser.add_argument("--output", "-o", type=Path, help="Output file path (CSV or Markdown)")
    parser.add_argument(
        "--scope", type=str, default="1,2,3", help="Scopes to include (comma-separated, e.g., '1,2' or '1,2,3')"
    )
    parser.add_argument(
        "--format", "-f", choices=["csv", "markdown", "json"], default="csv", help="Output format (default: csv)"
    )
    parser.add_argument("--list-types", action="store_true", help="List available activity types and exit")

    args = parser.parse_args()

    calculator = EmissionsCalculator()

    if args.list_types:
        print("Available activity types:")
        print("-" * 50)
        for activity_type in calculator.get_available_activity_types():
            factor = calculator.get_emission_factor(activity_type)
            scope = calculator.get_scope(activity_type)
            if factor and scope:
                print(f"  {activity_type}: {factor.value} kg CO2e/{factor.unit} (Scope {scope.value})")
        sys.exit(0)

    if not args.input:
        parser.error("--input is required")

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Parse scopes
    scopes = [int(s.strip()) for s in args.scope.split(",")]

    # Calculate emissions
    records = calculator.calculate_from_csv(args.input, scopes)

    if not records:
        print("Warning: No emission records generated", file=sys.stderr)
        sys.exit(0)

    # Generate output
    if args.output:
        if args.format == "csv":
            write_csv_output(records, args.output)
            print(f"Results written to: {args.output}")
        else:
            report = calculator.generate_report(records, args.format)
            args.output.write_text(report, encoding="utf-8")
            print(f"Report written to: {args.output}")
    else:
        # Print to stdout
        report = calculator.generate_report(records, args.format if args.format != "csv" else "markdown")
        print(report)

    # Print summary
    summary = calculator.summarize_by_scope(records)
    total = sum(summary.values())
    print(f"\nTotal emissions: {total:,.2f} tCO2e")
    print(f"  Scope 1: {summary[1]:,.2f} tCO2e")
    print(f"  Scope 2: {summary[2]:,.2f} tCO2e")
    print(f"  Scope 3: {summary[3]:,.2f} tCO2e")


if __name__ == "__main__":
    main()
