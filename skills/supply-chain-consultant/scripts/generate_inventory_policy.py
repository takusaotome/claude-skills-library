#!/usr/bin/env python3
"""Generate an Inventory Policy Table with Safety Stock and EOQ calculations.

Usage:
    python3 generate_inventory_policy.py input.csv -o output.md --service-level 0.975

Input CSV format (columns):
    sku, category, annual_demand, daily_demand_avg, daily_demand_stddev,
    lead_time_days, lead_time_stddev, order_cost, unit_cost, holding_cost_pct

Example:
    sku,category,annual_demand,daily_demand_avg,daily_demand_stddev,lead_time_days,lead_time_stddev,order_cost,unit_cost,holding_cost_pct
    WGT-A-001,A,36000,100,20,14,3,150,50,0.20
    WGT-B-015,B,12000,33,10,7,1,80,30,0.20
"""

from __future__ import annotations

import argparse
import csv
import math
from datetime import datetime
from pathlib import Path

Z_SCORES = {
    0.90: 1.28,
    0.95: 1.65,
    0.975: 1.96,
    0.99: 2.33,
    0.999: 3.09,
}

POLICY_MAP = {
    "A": ("Continuous (s,Q)", "Daily"),
    "B": ("Periodic (R,S)", "Weekly"),
    "C": ("Min-Max", "Monthly"),
}


def load_data(csv_path: str) -> list[dict]:
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "sku": row["sku"].strip(),
                    "category": row["category"].strip().upper(),
                    "annual_demand": float(row["annual_demand"]),
                    "daily_demand_avg": float(row["daily_demand_avg"]),
                    "daily_demand_stddev": float(row["daily_demand_stddev"]),
                    "lead_time_days": float(row["lead_time_days"]),
                    "lead_time_stddev": float(row["lead_time_stddev"]),
                    "order_cost": float(row["order_cost"]),
                    "unit_cost": float(row["unit_cost"]),
                    "holding_cost_pct": float(row["holding_cost_pct"]),
                }
            )
    return rows


def calc_safety_stock(z: float, lt: float, sigma_d: float, d_avg: float, sigma_lt: float) -> int:
    """Calculate safety stock: SS = Z * sigma_DLT
    where sigma_DLT = sqrt(LT * sigma_D^2 + D_avg^2 * sigma_LT^2)
    """
    sigma_dlt = math.sqrt(lt * sigma_d**2 + d_avg**2 * sigma_lt**2)
    return round(z * sigma_dlt)


def calc_eoq(annual_demand: float, order_cost: float, unit_cost: float, holding_pct: float) -> int:
    """Calculate EOQ = sqrt(2 * D * S / H) where H = unit_cost * holding_pct"""
    h = unit_cost * holding_pct
    if h == 0:
        return 0
    return round(math.sqrt(2 * annual_demand * order_cost / h))


def generate_policy_table(data: list[dict], service_level: float) -> str:
    z = Z_SCORES.get(service_level)
    if z is None:
        closest = min(Z_SCORES.keys(), key=lambda x: abs(x - service_level))
        z = Z_SCORES[closest]

    now = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "# Inventory Policy Table",
        "",
        f"**Generated**: {now}",
        f"**Service Level**: {service_level*100:.1f}% (Z = {z:.2f})",
        f"**SKUs**: {len(data)}",
        "",
        "## Policy Summary",
        "",
        "| SKU | Category | Policy Type | Safety Stock | EOQ | Reorder Point | Max Stock | Review Freq |",
        "|-----|----------|-------------|-------------|-----|---------------|-----------|-------------|",
    ]

    total_ss_value = 0.0
    for row in data:
        ss = calc_safety_stock(
            z, row["lead_time_days"], row["daily_demand_stddev"],
            row["daily_demand_avg"], row["lead_time_stddev"],
        )
        eoq = calc_eoq(
            row["annual_demand"], row["order_cost"],
            row["unit_cost"], row["holding_cost_pct"],
        )
        rop = round(row["daily_demand_avg"] * row["lead_time_days"]) + ss
        max_stock = rop + eoq
        policy_type, review_freq = POLICY_MAP.get(row["category"], ("Min-Max", "Monthly"))
        total_ss_value += ss * row["unit_cost"]

        lines.append(
            f"| {row['sku']} | {row['category']} "
            f"| {policy_type} | {ss:,} | {eoq:,} | {rop:,} | {max_stock:,} | {review_freq} |"
        )

    lines.extend([
        "",
        "## Cost Summary",
        "",
        f"- **Total Safety Stock Value**: ${total_ss_value:,.0f}",
        f"- **Annual Carrying Cost (SS only)**: ${total_ss_value * 0.20:,.0f} (at 20%)",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Inventory Policy Table")
    parser.add_argument("input_file", help="CSV file with SKU inventory parameters")
    parser.add_argument("-o", "--output", help="Output markdown file (default: stdout)")
    parser.add_argument(
        "--service-level", type=float, default=0.975,
        help="Target service level (default: 0.975 = 97.5%%)",
    )
    args = parser.parse_args()

    data = load_data(args.input_file)
    table = generate_policy_table(data, args.service_level)

    if args.output:
        Path(args.output).write_text(table, encoding="utf-8")
        print(f"Policy table written to {args.output}")
    else:
        print(table)


if __name__ == "__main__":
    main()
