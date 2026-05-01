#!/usr/bin/env python3
"""
ROI Calculation Tool for AI-BPO Proposals

Calculates Return on Investment projections based on selected services and client volumes.
Outputs current state costs, future state projections, and key financial metrics.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Any

# Industry benchmarks for ROI calculations
BENCHMARKS = {
    # Processing time in minutes per transaction
    "processing_time": {
        "invoice_processing": {"manual": 15, "automated": 2},
        "expense_reporting": {"manual": 10, "automated": 1},
        "payroll": {"manual": 30, "automated": 3},  # per employee
        "onboarding": {"manual": 240, "automated": 60},  # per hire
        "data_entry": {"manual": 0.6, "automated": 0.05},  # per record
        "support_ticket": {"manual": 20, "automated": 5},
        "po_processing": {"manual": 20, "automated": 4},
    },
    # Error rates
    "error_rates": {
        "invoice_processing": {"manual": 0.04, "automated": 0.005},
        "expense_reporting": {"manual": 0.05, "automated": 0.008},
        "payroll": {"manual": 0.02, "automated": 0.002},
        "data_entry": {"manual": 0.03, "automated": 0.001},
    },
    # Cost per error
    "error_costs": {
        "invoice_processing": 50,  # average including rework and duplicate payments
        "expense_reporting": 25,
        "payroll": 100,
        "data_entry": 10,
    },
    # Loaded hourly rate (salary + 35% benefits/overhead)
    "hourly_rates": {
        "clerk": 35,  # ~$55k salary
        "specialist": 45,  # ~$70k salary
        "analyst": 55,  # ~$85k salary
    },
}

# Service to process type mapping
SERVICE_PROCESS_MAP = {
    "fin-001": "invoice_processing",
    "fin-002": "expense_reporting",
    "fin-003": "reconciliation",
    "fin-004": "ar_processing",
    "hr-001": "onboarding",
    "hr-002": "time_tracking",
    "hr-004": "payroll",
    "cs-001": "support_ticket",
    "cs-002": "faq_automation",
    "dp-001": "document_digitization",
    "dp-002": "data_entry",
    "pr-001": "po_processing",
    "pr-002": "vendor_management",
    "pr-003": "contract_analysis",
}


def calculate_current_state_cost(
    process_type: str,
    monthly_volume: int,
    hourly_rate: float = 35.0,
) -> dict[str, Any]:
    """
    Calculate current state (manual) processing costs.

    Args:
        process_type: Type of process (e.g., 'invoice_processing')
        monthly_volume: Monthly transaction volume
        hourly_rate: Loaded hourly rate for staff

    Returns:
        Current state cost breakdown
    """
    time_benchmarks = BENCHMARKS["processing_time"].get(process_type, {"manual": 10, "automated": 2})
    error_benchmarks = BENCHMARKS["error_rates"].get(process_type, {"manual": 0.03, "automated": 0.005})
    error_cost = BENCHMARKS["error_costs"].get(process_type, 25)

    manual_time_per_tx = time_benchmarks["manual"]
    manual_error_rate = error_benchmarks["manual"]

    # Annual calculations
    annual_volume = monthly_volume * 12
    total_hours = (annual_volume * manual_time_per_tx) / 60
    fte_equivalent = total_hours / 2080  # 2080 = 40 hours * 52 weeks

    labor_cost = total_hours * hourly_rate
    error_count = annual_volume * manual_error_rate
    error_total = error_count * error_cost

    return {
        "annual_volume": annual_volume,
        "processing_hours": round(total_hours, 1),
        "fte_equivalent": round(fte_equivalent, 2),
        "annual_labor_cost_usd": round(labor_cost, 2),
        "error_rate_pct": round(manual_error_rate * 100, 2),
        "annual_error_cost_usd": round(error_total, 2),
        "total_annual_cost_usd": round(labor_cost + error_total, 2),
    }


def calculate_future_state_cost(
    process_type: str,
    monthly_volume: int,
    service_fee: float,
    automation_rate: float = 0.85,
    hourly_rate: float = 35.0,
) -> dict[str, Any]:
    """
    Calculate future state (automated) processing costs.

    Args:
        process_type: Type of process
        monthly_volume: Monthly transaction volume
        service_fee: Annual service fee
        automation_rate: Expected automation rate (0-1)
        hourly_rate: Loaded hourly rate for remaining manual work

    Returns:
        Future state cost breakdown
    """
    time_benchmarks = BENCHMARKS["processing_time"].get(process_type, {"manual": 10, "automated": 2})
    error_benchmarks = BENCHMARKS["error_rates"].get(process_type, {"manual": 0.03, "automated": 0.005})
    error_cost = BENCHMARKS["error_costs"].get(process_type, 25)

    automated_time = time_benchmarks["automated"]
    automated_error_rate = error_benchmarks["automated"]

    annual_volume = monthly_volume * 12

    # Automated portion
    automated_volume = annual_volume * automation_rate
    # Manual exception handling
    manual_volume = annual_volume * (1 - automation_rate)

    # Time for automated reviews + manual exceptions
    total_hours = (automated_volume * automated_time + manual_volume * time_benchmarks["manual"]) / 60
    fte_equivalent = total_hours / 2080

    labor_cost = total_hours * hourly_rate
    error_count = annual_volume * automated_error_rate
    error_total = error_count * error_cost

    total_cost = labor_cost + error_total + service_fee

    return {
        "annual_volume": annual_volume,
        "automation_rate_pct": round(automation_rate * 100, 1),
        "processing_hours": round(total_hours, 1),
        "fte_equivalent": round(fte_equivalent, 2),
        "annual_labor_cost_usd": round(labor_cost, 2),
        "error_rate_pct": round(automated_error_rate * 100, 2),
        "annual_error_cost_usd": round(error_total, 2),
        "annual_service_fee_usd": round(service_fee, 2),
        "total_annual_cost_usd": round(total_cost, 2),
    }


def calculate_implementation_cost(
    service_count: int,
    complexity: str = "medium",
) -> dict[str, Any]:
    """
    Calculate one-time implementation costs.

    Args:
        service_count: Number of services being implemented
        complexity: Implementation complexity (low, medium, high)

    Returns:
        Implementation cost breakdown
    """
    complexity_multipliers = {
        "low": 0.7,
        "medium": 1.0,
        "high": 1.5,
    }
    multiplier = complexity_multipliers.get(complexity, 1.0)

    base_setup = 10000 * multiplier
    integration = 15000 * multiplier * min(service_count, 5)  # Cap at 5 integrations
    training = 5000 * multiplier
    change_management = 10000 * multiplier

    total = base_setup + integration + training + change_management

    return {
        "setup_and_configuration_usd": round(base_setup, 2),
        "integration_development_usd": round(integration, 2),
        "training_usd": round(training, 2),
        "change_management_usd": round(change_management, 2),
        "total_implementation_cost_usd": round(total, 2),
    }


def calculate_npv(
    annual_savings: float,
    implementation_cost: float,
    discount_rate: float = 0.10,
    years: int = 3,
) -> float:
    """
    Calculate Net Present Value over specified years.

    Args:
        annual_savings: Annual cost savings
        implementation_cost: One-time implementation cost
        discount_rate: Discount rate (default 10%)
        years: Number of years for calculation

    Returns:
        NPV value
    """
    npv = -implementation_cost
    for year in range(1, years + 1):
        npv += annual_savings / ((1 + discount_rate) ** year)
    return round(npv, 2)


def calculate_roi(
    services_file: str | None = None,
    services_data: dict[str, Any] | None = None,
    volumes: dict[str, int] | None = None,
    output_path: str | None = None,
) -> dict[str, Any]:
    """
    Generate comprehensive ROI analysis.

    Args:
        services_file: Path to services JSON file
        services_data: Services data dictionary (alternative to file)
        volumes: Volume dictionary with process-specific volumes
        output_path: Optional output file path

    Returns:
        ROI analysis report
    """
    # Load services
    if services_file:
        with open(services_file, "r", encoding="utf-8") as f:
            services_data = json.load(f)
    elif not services_data:
        raise ValueError("Either services_file or services_data must be provided")

    selected_services = services_data.get("selected_services", [])
    volumes = volumes or {}

    # Default volumes if not specified
    default_volumes = {
        "invoices_per_month": 2000,
        "expense_reports_per_month": 200,
        "employees": 150,
        "new_hires_per_year": 30,
        "support_tickets_per_month": 500,
        "documents_per_month": 1000,
        "records_per_month": 5000,
        "pos_per_month": 200,
    }
    volumes = {**default_volumes, **volumes}

    # Calculate costs for each service
    current_state_total = 0
    future_state_total = 0
    service_analyses = []

    for service in selected_services:
        service_id = service["service_id"]
        process_type = SERVICE_PROCESS_MAP.get(service_id, "generic")

        # Determine volume for this service
        if "invoice" in process_type:
            monthly_vol = volumes.get("invoices_per_month", 2000)
        elif "expense" in process_type:
            monthly_vol = volumes.get("expense_reports_per_month", 200)
        elif "payroll" in process_type or "onboarding" in process_type:
            monthly_vol = volumes.get("employees", 150)
        elif "ticket" in process_type:
            monthly_vol = volumes.get("support_tickets_per_month", 500)
        elif "data_entry" in process_type:
            monthly_vol = volumes.get("records_per_month", 5000)
        elif "po" in process_type:
            monthly_vol = volumes.get("pos_per_month", 200)
        else:
            monthly_vol = volumes.get("documents_per_month", 1000)

        # Calculate annual service fee
        base_fee = service.get("base_monthly_fee_usd", 3000) * 12
        automation_rate = service.get("estimated_automation_rate", 0.80)

        current = calculate_current_state_cost(process_type, monthly_vol)
        future = calculate_future_state_cost(process_type, monthly_vol, base_fee, automation_rate)

        current_state_total += current["total_annual_cost_usd"]
        future_state_total += future["total_annual_cost_usd"]

        service_analyses.append(
            {
                "service_id": service_id,
                "service_name": service["service_name"],
                "monthly_volume": monthly_vol,
                "current_state": current,
                "future_state": future,
                "annual_savings_usd": round(current["total_annual_cost_usd"] - future["total_annual_cost_usd"], 2),
            }
        )

    # Implementation costs
    implementation = calculate_implementation_cost(len(selected_services))
    implementation_total = implementation["total_implementation_cost_usd"]

    # Financial metrics
    annual_savings = current_state_total - future_state_total
    payback_months = round((implementation_total / annual_savings) * 12, 1) if annual_savings > 0 else float("inf")
    npv_3yr = calculate_npv(annual_savings, implementation_total)
    roi_pct = (
        round(((annual_savings * 3 - implementation_total) / implementation_total) * 100, 1)
        if implementation_total > 0
        else 0
    )

    report = {
        "schema_version": "1.0",
        "analysis_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "volumes_analyzed": volumes,
        "current_state": {
            "annual_cost_usd": round(current_state_total, 2),
            "fte_equivalent": round(sum(s["current_state"]["fte_equivalent"] for s in service_analyses), 2),
        },
        "future_state": {
            "annual_cost_usd": round(future_state_total, 2),
            "fte_equivalent": round(sum(s["future_state"]["fte_equivalent"] for s in service_analyses), 2),
        },
        "implementation_costs": implementation,
        "financial_summary": {
            "annual_savings_usd": round(annual_savings, 2),
            "implementation_cost_usd": implementation_total,
            "payback_months": payback_months,
            "three_year_npv_usd": npv_3yr,
            "three_year_roi_percentage": roi_pct,
        },
        "service_breakdown": service_analyses,
    }

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"ROI analysis saved to: {output_path}", file=sys.stderr)

    return report


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Calculate ROI for AI-BPO service implementation")
    parser.add_argument(
        "--services",
        required=True,
        help="Path to services JSON file from select_services.py",
    )
    parser.add_argument(
        "--volumes",
        help="JSON string with volumes (e.g., '{\"invoices_per_month\": 5000}')",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON file path",
    )

    args = parser.parse_args()

    volumes = {}
    if args.volumes:
        volumes = json.loads(args.volumes)

    report = calculate_roi(
        services_file=args.services,
        volumes=volumes,
        output_path=args.output,
    )

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
