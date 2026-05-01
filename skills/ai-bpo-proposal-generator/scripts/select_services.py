#!/usr/bin/env python3
"""
Service Module Selection Tool for AI-BPO Proposals

Selects appropriate AI-BPO service modules based on client industry and pain points.
Outputs a JSON file with recommended services and estimated pricing.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Any

# Service catalog with metadata
SERVICE_CATALOG = {
    "fin-001": {
        "service_id": "fin-001",
        "service_name": "Invoice Processing Automation",
        "category": "finance_accounting",
        "ai_components": ["document_extraction", "validation", "approval_routing"],
        "applicable_industries": ["manufacturing", "trading", "retail", "services", "logistics"],
        "pain_point_keywords": ["invoice", "ap", "accounts_payable", "invoice_processing"],
        "estimated_automation_rate": 0.85,
        "base_monthly_fee_usd": 5000,
        "per_transaction_fee_usd": 1.50,
    },
    "fin-002": {
        "service_id": "fin-002",
        "service_name": "Expense Report Automation",
        "category": "finance_accounting",
        "ai_components": ["receipt_ocr", "categorization", "policy_compliance"],
        "applicable_industries": ["manufacturing", "trading", "retail", "services", "logistics", "consulting"],
        "pain_point_keywords": ["expense", "expense_reporting", "travel", "receipts"],
        "estimated_automation_rate": 0.75,
        "base_monthly_fee_usd": 3000,
        "per_employee_fee_usd": 15,
    },
    "fin-003": {
        "service_id": "fin-003",
        "service_name": "Bank Reconciliation",
        "category": "finance_accounting",
        "ai_components": ["transaction_matching", "exception_detection", "multi_bank"],
        "applicable_industries": ["manufacturing", "trading", "retail", "services", "logistics"],
        "pain_point_keywords": ["reconciliation", "bank", "cash", "treasury"],
        "estimated_automation_rate": 0.92,
        "base_monthly_fee_usd": 3000,
        "per_account_fee_usd": 500,
    },
    "fin-004": {
        "service_id": "fin-004",
        "service_name": "Accounts Receivable Automation",
        "category": "finance_accounting",
        "ai_components": ["payment_prediction", "collections_optimization", "cash_forecasting"],
        "applicable_industries": ["manufacturing", "trading", "retail", "services"],
        "pain_point_keywords": ["ar", "accounts_receivable", "collections", "dso"],
        "estimated_automation_rate": 0.80,
        "base_monthly_fee_usd": 4000,
        "per_invoice_fee_usd": 1.00,
    },
    "hr-001": {
        "service_id": "hr-001",
        "service_name": "Employee Onboarding Automation",
        "category": "hr_payroll",
        "ai_components": ["document_verification", "background_check", "training_recommendation"],
        "applicable_industries": ["manufacturing", "trading", "retail", "services", "logistics", "consulting"],
        "pain_point_keywords": ["onboarding", "hiring", "new_hire", "employee_onboarding"],
        "estimated_automation_rate": 0.68,
        "base_monthly_fee_usd": 2000,
        "per_hire_fee_usd": 50,
    },
    "hr-002": {
        "service_id": "hr-002",
        "service_name": "Time & Attendance Management",
        "category": "hr_payroll",
        "ai_components": ["anomaly_detection", "overtime_prediction", "compliance_monitoring"],
        "applicable_industries": ["manufacturing", "retail", "logistics", "services"],
        "pain_point_keywords": ["time_tracking", "attendance", "overtime", "timecard"],
        "estimated_automation_rate": 0.90,
        "base_monthly_fee_usd": 500,
        "per_employee_fee_usd": 8,
    },
    "hr-004": {
        "service_id": "hr-004",
        "service_name": "Payroll Processing",
        "category": "hr_payroll",
        "ai_components": ["multi_state_tax", "garnishment", "gl_integration", "expat_payroll"],
        "applicable_industries": ["manufacturing", "trading", "retail", "services", "logistics", "consulting"],
        "pain_point_keywords": ["payroll", "salary", "tax", "payroll_processing"],
        "estimated_automation_rate": 0.94,
        "base_monthly_fee_usd": 1000,
        "per_employee_fee_usd": 15,
    },
    "cs-001": {
        "service_id": "cs-001",
        "service_name": "Ticket Routing & Triage",
        "category": "customer_support",
        "ai_components": ["intent_classification", "sentiment_analysis", "priority_scoring"],
        "applicable_industries": ["trading", "retail", "services", "logistics"],
        "pain_point_keywords": ["support", "tickets", "customer_service", "ticket_routing"],
        "estimated_automation_rate": 0.90,
        "base_monthly_fee_usd": 1000,
        "per_ticket_fee_usd": 0.05,
    },
    "cs-002": {
        "service_id": "cs-002",
        "service_name": "FAQ & Knowledge Base Automation",
        "category": "customer_support",
        "ai_components": ["nlu", "answer_retrieval", "content_gap_detection", "bilingual"],
        "applicable_industries": ["trading", "retail", "services", "logistics"],
        "pain_point_keywords": ["faq", "knowledge_base", "self_service", "chatbot"],
        "estimated_automation_rate": 0.78,
        "base_monthly_fee_usd": 2500,
        "setup_fee_usd": 5000,
    },
    "dp-001": {
        "service_id": "dp-001",
        "service_name": "Document Digitization",
        "category": "data_processing",
        "ai_components": ["multi_format_ocr", "document_classification", "field_extraction"],
        "applicable_industries": ["manufacturing", "trading", "retail", "services", "logistics"],
        "pain_point_keywords": ["scanning", "digitization", "paper", "document_processing"],
        "estimated_automation_rate": 0.95,
        "base_monthly_fee_usd": 500,
        "per_page_fee_usd": 0.50,
    },
    "dp-002": {
        "service_id": "dp-002",
        "service_name": "Data Entry Automation",
        "category": "data_processing",
        "ai_components": ["format_detection", "field_mapping", "validation"],
        "applicable_industries": ["manufacturing", "trading", "retail", "services", "logistics"],
        "pain_point_keywords": ["data_entry", "manual_entry", "typing", "input"],
        "estimated_automation_rate": 0.94,
        "base_monthly_fee_usd": 1000,
        "per_record_fee_usd": 0.10,
    },
    "pr-001": {
        "service_id": "pr-001",
        "service_name": "Purchase Order Processing",
        "category": "procurement",
        "ai_components": ["requisition_automation", "budget_checking", "vendor_recommendation"],
        "applicable_industries": ["manufacturing", "trading", "retail", "logistics"],
        "pain_point_keywords": ["purchase_order", "po", "procurement", "ordering"],
        "estimated_automation_rate": 0.80,
        "base_monthly_fee_usd": 5000,
        "per_po_fee_usd": 2.00,
    },
    "pr-002": {
        "service_id": "pr-002",
        "service_name": "Vendor Management",
        "category": "procurement",
        "ai_components": ["risk_scoring", "performance_analytics", "spend_analytics"],
        "applicable_industries": ["manufacturing", "trading", "retail", "logistics"],
        "pain_point_keywords": ["vendor", "supplier", "vendor_management", "spend"],
        "estimated_automation_rate": 0.68,
        "base_monthly_fee_usd": 3000,
        "per_vendor_fee_usd": 100,
    },
    "pr-003": {
        "service_id": "pr-003",
        "service_name": "Contract Analysis",
        "category": "procurement",
        "ai_components": ["clause_extraction", "risk_identification", "renewal_tracking"],
        "applicable_industries": ["manufacturing", "trading", "services", "consulting"],
        "pain_point_keywords": ["contract", "contracts", "legal", "contract_management"],
        "estimated_automation_rate": 0.72,
        "base_monthly_fee_usd": 2000,
        "per_contract_fee_usd": 50,
    },
}

# Industry bundles with discounts
INDUSTRY_BUNDLES = {
    "manufacturing": {
        "name": "Manufacturing Bundle",
        "services": ["fin-001", "fin-003", "pr-001", "pr-002", "dp-001"],
        "discount": 0.15,
    },
    "trading": {
        "name": "Trading Company Bundle",
        "services": ["fin-001", "fin-004", "cs-001", "cs-002", "dp-002"],
        "discount": 0.15,
    },
    "services": {
        "name": "Professional Services Bundle",
        "services": ["hr-001", "hr-004", "fin-002", "cs-001", "pr-003"],
        "discount": 0.15,
    },
}


def normalize_pain_point(pain_point: str) -> str:
    """Normalize pain point string for matching."""
    return pain_point.lower().strip().replace(" ", "_").replace("-", "_")


def match_services(
    industry: str,
    pain_points: list[str],
    include_bundle: bool = True,
) -> list[dict[str, Any]]:
    """
    Match services based on industry and pain points.

    Args:
        industry: Client industry (e.g., 'manufacturing', 'trading')
        pain_points: List of pain point keywords
        include_bundle: Whether to suggest bundle if applicable

    Returns:
        List of matched service dictionaries
    """
    matched = []
    normalized_pain_points = [normalize_pain_point(pp) for pp in pain_points]
    industry_lower = industry.lower()

    for service_id, service in SERVICE_CATALOG.items():
        # Check industry match
        if industry_lower not in [ind.lower() for ind in service["applicable_industries"]]:
            continue

        # Check pain point match
        service_keywords = [kw.lower() for kw in service["pain_point_keywords"]]
        for pp in normalized_pain_points:
            if any(kw in pp or pp in kw for kw in service_keywords):
                matched.append(service.copy())
                break

    # Add bundle info if applicable
    bundle_info = None
    if include_bundle and industry_lower in INDUSTRY_BUNDLES:
        bundle = INDUSTRY_BUNDLES[industry_lower]
        bundle_services = set(bundle["services"])
        matched_ids = {s["service_id"] for s in matched}

        # Check if matched services overlap with bundle
        overlap = bundle_services & matched_ids
        if len(overlap) >= 2:
            bundle_info = {
                "name": bundle["name"],
                "included_services": list(bundle_services),
                "discount_rate": bundle["discount"],
            }

    return matched, bundle_info


def calculate_estimated_pricing(
    services: list[dict[str, Any]],
    bundle_info: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Calculate estimated monthly pricing for selected services.

    Args:
        services: List of selected services
        bundle_info: Bundle information if applicable

    Returns:
        Pricing breakdown dictionary
    """
    total_base_fee = sum(s.get("base_monthly_fee_usd", 0) for s in services)
    setup_fees = sum(s.get("setup_fee_usd", 0) for s in services)

    discount = 0
    if bundle_info:
        discount = total_base_fee * bundle_info["discount_rate"]

    return {
        "base_monthly_fee_usd": total_base_fee,
        "setup_fees_usd": setup_fees,
        "bundle_discount_usd": discount,
        "estimated_monthly_total_usd": total_base_fee - discount,
        "note": "Transaction-based fees not included; depend on actual volumes",
    }


def generate_service_selection(
    industry: str,
    pain_points: list[str],
    output_path: str | None = None,
) -> dict[str, Any]:
    """
    Generate service selection report.

    Args:
        industry: Client industry
        pain_points: List of pain points
        output_path: Optional output file path

    Returns:
        Service selection report dictionary
    """
    matched_services, bundle_info = match_services(industry, pain_points)
    pricing = calculate_estimated_pricing(matched_services, bundle_info)

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "client_industry": industry,
        "pain_points_analyzed": pain_points,
        "selected_services": matched_services,
        "bundle_recommendation": bundle_info,
        "pricing_estimate": pricing,
        "service_count": len(matched_services),
    }

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Service selection saved to: {output_path}", file=sys.stderr)

    return report


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Select AI-BPO service modules based on industry and pain points")
    parser.add_argument(
        "--industry",
        required=True,
        help="Client industry (manufacturing, trading, retail, services, logistics, consulting)",
    )
    parser.add_argument(
        "--pain-points",
        required=True,
        help="Comma-separated pain points (e.g., 'invoice_processing,expense_reporting')",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON file path",
    )
    parser.add_argument(
        "--no-bundle",
        action="store_true",
        help="Disable bundle recommendations",
    )

    args = parser.parse_args()

    pain_points = [pp.strip() for pp in args.pain_points.split(",")]

    report = generate_service_selection(
        industry=args.industry,
        pain_points=pain_points,
        output_path=args.output,
    )

    # Print summary to stdout
    print(json.dumps(report, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
