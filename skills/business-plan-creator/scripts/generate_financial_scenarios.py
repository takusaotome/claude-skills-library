#!/usr/bin/env python3
"""Generate 3-scenario monthly financial projection CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

SCENARIOS = {
    "upside": {"growth_multiplier": 1.30, "cogs_multiplier": 0.95, "opex_multiplier": 1.00},
    "base": {"growth_multiplier": 1.00, "cogs_multiplier": 1.00, "opex_multiplier": 1.00},
    "downside": {
        "growth_multiplier": 0.60,
        "cogs_multiplier": 1.15,
        "opex_multiplier": 1.10,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-revenue", type=float, required=True, help="Month-1 revenue.")
    parser.add_argument(
        "--base-growth-rate",
        type=float,
        default=0.05,
        help="Monthly growth rate for base scenario (e.g. 0.05 for 5%).",
    )
    parser.add_argument(
        "--base-cogs-rate",
        type=float,
        required=True,
        help="Base COGS ratio (0.0-1.0).",
    )
    parser.add_argument(
        "--base-opex",
        type=float,
        required=True,
        help="Base monthly operating expenses.",
    )
    parser.add_argument("--months", type=int, default=12, help="Projection length in months.")
    parser.add_argument("--output", required=True, help="Output CSV path.")
    return parser.parse_args()


def clamp_ratio(value: float) -> float:
    return max(0.0, min(1.0, value))


def generate_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for scenario, factors in SCENARIOS.items():
        scenario_growth = args.base_growth_rate * factors["growth_multiplier"]
        cogs_rate = clamp_ratio(args.base_cogs_rate * factors["cogs_multiplier"])
        opex = args.base_opex * factors["opex_multiplier"]

        for month in range(1, args.months + 1):
            revenue = args.base_revenue * ((1 + scenario_growth) ** (month - 1))
            cogs = revenue * cogs_rate
            gross_profit = revenue - cogs
            operating_profit = gross_profit - opex

            rows.append(
                {
                    "scenario": scenario,
                    "month": str(month),
                    "revenue": f"{revenue:.2f}",
                    "cogs": f"{cogs:.2f}",
                    "gross_profit": f"{gross_profit:.2f}",
                    "opex": f"{opex:.2f}",
                    "operating_profit": f"{operating_profit:.2f}",
                    "cogs_rate": f"{cogs_rate:.4f}",
                    "growth_rate": f"{scenario_growth:.4f}",
                }
            )

    return rows


def main() -> None:
    args = parse_args()
    rows = generate_rows(args)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "scenario",
                "month",
                "revenue",
                "cogs",
                "gross_profit",
                "opex",
                "operating_profit",
                "cogs_rate",
                "growth_rate",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
