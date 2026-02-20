#!/usr/bin/env python3
"""Generate a Demand Forecast KPI Dashboard in Markdown format.

Usage:
    python3 generate_demand_kpi_dashboard.py input.csv -o output.md

Input CSV format (columns):
    category, period, actual, forecast

Example:
    category,period,actual,forecast
    Category A,2025-01,1200,1250
    Category A,2025-02,1300,1280
    Category B,2025-01,890,920
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def load_data(csv_path: str) -> list[dict]:
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "category": row["category"].strip(),
                    "period": row["period"].strip(),
                    "actual": float(row["actual"]),
                    "forecast": float(row["forecast"]),
                }
            )
    return rows


def calc_mape(actuals: list[float], forecasts: list[float]) -> float:
    if not actuals:
        return 0.0
    errors = []
    for a, f in zip(actuals, forecasts):
        if a != 0:
            errors.append(abs(a - f) / abs(a))
    return (sum(errors) / len(errors)) * 100 if errors else 0.0


def calc_bias(actuals: list[float], forecasts: list[float]) -> float:
    if not actuals:
        return 0.0
    return sum(f - a for a, f in zip(actuals, forecasts)) / len(actuals)


def calc_tracking_signal(actuals: list[float], forecasts: list[float]) -> float:
    if not actuals:
        return 0.0
    errors = [f - a for a, f in zip(actuals, forecasts)]
    running_sum = sum(errors)
    mad = sum(abs(e) for e in errors) / len(errors)
    return running_sum / mad if mad != 0 else 0.0


def status_icon(mape: float, target: float = 20.0) -> str:
    if mape <= target:
        return "Good"
    elif mape <= target * 1.5:
        return "Review"
    else:
        return "Action Required"


def generate_dashboard(data: list[dict]) -> str:
    by_category = defaultdict(lambda: {"actuals": [], "forecasts": []})
    all_actuals = []
    all_forecasts = []

    for row in data:
        cat = row["category"]
        by_category[cat]["actuals"].append(row["actual"])
        by_category[cat]["forecasts"].append(row["forecast"])
        all_actuals.append(row["actual"])
        all_forecasts.append(row["forecast"])

    overall_mape = calc_mape(all_actuals, all_forecasts)
    overall_bias = calc_bias(all_actuals, all_forecasts)
    bias_pct = (overall_bias / (sum(all_actuals) / len(all_actuals))) * 100 if all_actuals else 0

    now = datetime.now().strftime("%Y-%m-%d")

    lines = [
        "# Demand Forecast Performance Dashboard",
        "",
        f"**Generated**: {now}",
        f"**Data periods**: {len(data)} records across {len(by_category)} categories",
        "",
        "## Overall Accuracy",
        f"- **MAPE**: {overall_mape:.1f}% {'(Target: <20%)' if overall_mape <= 20 else '(Target: <20% - EXCEEDS)'}",
        f"- **Bias**: {bias_pct:+.1f}% ({'Over' if bias_pct > 0 else 'Under'}-forecasting)",
        "",
        "## By Product Category",
        "",
        "| Category | MAPE | Bias | Tracking Signal | Status |",
        "|----------|------|------|-----------------|--------|",
    ]

    for cat in sorted(by_category.keys()):
        d = by_category[cat]
        mape = calc_mape(d["actuals"], d["forecasts"])
        bias = calc_bias(d["actuals"], d["forecasts"])
        ts = calc_tracking_signal(d["actuals"], d["forecasts"])
        avg_actual = sum(d["actuals"]) / len(d["actuals"])
        bias_pct_cat = (bias / avg_actual) * 100 if avg_actual != 0 else 0
        status = status_icon(mape)
        lines.append(f"| {cat} | {mape:.1f}% | {bias_pct_cat:+.1f}% | {ts:+.1f} | {status} |")

    lines.extend(
        [
            "",
            "## Stockout / Excess Summary",
            "",
            "*(Requires additional data: stockout incidents and excess inventory value)*",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Demand Forecast KPI Dashboard")
    parser.add_argument("input_file", help="CSV file with category,period,actual,forecast columns")
    parser.add_argument("-o", "--output", help="Output markdown file (default: stdout)")
    args = parser.parse_args()

    data = load_data(args.input_file)
    dashboard = generate_dashboard(data)

    if args.output:
        Path(args.output).write_text(dashboard, encoding="utf-8")
        print(f"Dashboard written to {args.output}")
    else:
        print(dashboard)


if __name__ == "__main__":
    main()
