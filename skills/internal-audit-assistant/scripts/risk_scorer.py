#!/usr/bin/env python3
"""
Risk Scorer for Internal Audit Planning

Calculates weighted risk scores for auditable entities based on multiple risk factors.
Outputs a prioritized risk matrix for audit planning.

Usage:
    python3 risk_scorer.py entities.csv --output risk_matrix.md
    python3 risk_scorer.py entities.csv --format json
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RiskFactors:
    """Risk factors for an auditable entity."""

    inherent_risk: float  # 1-5: Complexity, volume, sensitivity
    control_environment: float  # 1-5: Strength of existing controls (inverse)
    financial_impact: float  # 1-5: Potential monetary impact
    regulatory_impact: float  # 1-5: Compliance and legal consequences
    last_audit_date: float  # 1-5: Time since last audit
    management_concern: float  # 1-5: Requests from senior management


@dataclass
class AuditableEntity:
    """Represents an auditable entity with risk assessment."""

    entity_id: str
    entity_name: str
    department: str
    entity_type: str
    risk_factors: RiskFactors
    last_audit: Optional[str] = None


# Default weights per IIA risk-based audit planning best practices
DEFAULT_WEIGHTS = {
    "inherent_risk": 0.25,
    "control_environment": 0.20,
    "financial_impact": 0.20,
    "regulatory_impact": 0.20,
    "last_audit_date": 0.10,
    "management_concern": 0.05,
}


def calculate_risk_score(factors: RiskFactors, weights: dict = None) -> float:
    """
    Calculate weighted risk score for an entity.

    Args:
        factors: RiskFactors instance with scores 1-5 for each factor
        weights: Dictionary of weights (must sum to 1.0)

    Returns:
        Weighted risk score between 1.0 and 5.0
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    score = (
        factors.inherent_risk * weights["inherent_risk"]
        + factors.control_environment * weights["control_environment"]
        + factors.financial_impact * weights["financial_impact"]
        + factors.regulatory_impact * weights["regulatory_impact"]
        + factors.last_audit_date * weights["last_audit_date"]
        + factors.management_concern * weights["management_concern"]
    )
    return round(score, 2)


def get_risk_level(score: float) -> str:
    """
    Determine risk level from score.

    Args:
        score: Risk score between 1.0 and 5.0

    Returns:
        Risk level string: Critical, High, Medium, or Low
    """
    if score >= 4.0:
        return "Critical"
    elif score >= 3.0:
        return "High"
    elif score >= 2.0:
        return "Medium"
    else:
        return "Low"


def get_audit_frequency(risk_level: str) -> str:
    """
    Recommend audit frequency based on risk level.

    Args:
        risk_level: Risk level string

    Returns:
        Recommended audit frequency
    """
    frequencies = {
        "Critical": "Annual (required)",
        "High": "Every 1-2 years",
        "Medium": "Every 2-3 years",
        "Low": "Every 3-5 years",
    }
    return frequencies.get(risk_level, "N/A")


def parse_csv(filepath: Path) -> list[AuditableEntity]:
    """
    Parse CSV file containing auditable entities and risk scores.

    Expected columns:
    entity_id, entity_name, department, entity_type, last_audit,
    inherent_risk, control_environment, financial_impact,
    regulatory_impact, last_audit_date, management_concern

    Args:
        filepath: Path to CSV file

    Returns:
        List of AuditableEntity instances
    """
    entities = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            factors = RiskFactors(
                inherent_risk=float(row.get("inherent_risk", 3)),
                control_environment=float(row.get("control_environment", 3)),
                financial_impact=float(row.get("financial_impact", 3)),
                regulatory_impact=float(row.get("regulatory_impact", 3)),
                last_audit_date=float(row.get("last_audit_date", 3)),
                management_concern=float(row.get("management_concern", 3)),
            )
            entity = AuditableEntity(
                entity_id=row.get("entity_id", ""),
                entity_name=row.get("entity_name", ""),
                department=row.get("department", ""),
                entity_type=row.get("entity_type", ""),
                risk_factors=factors,
                last_audit=row.get("last_audit"),
            )
            entities.append(entity)
    return entities


def generate_markdown_report(entities: list[AuditableEntity]) -> str:
    """
    Generate markdown risk matrix report.

    Args:
        entities: List of AuditableEntity instances

    Returns:
        Markdown formatted report string
    """
    # Calculate scores and sort by risk
    scored = []
    for entity in entities:
        score = calculate_risk_score(entity.risk_factors)
        level = get_risk_level(score)
        frequency = get_audit_frequency(level)
        scored.append((entity, score, level, frequency))

    scored.sort(key=lambda x: x[1], reverse=True)

    # Generate report
    lines = [
        "# Risk Assessment Matrix",
        "",
        "## Summary",
        "",
    ]

    # Count by risk level
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for _, _, level, _ in scored:
        counts[level] += 1

    lines.extend(
        [
            f"- **Total Entities**: {len(scored)}",
            f"- **Critical Risk**: {counts['Critical']}",
            f"- **High Risk**: {counts['High']}",
            f"- **Medium Risk**: {counts['Medium']}",
            f"- **Low Risk**: {counts['Low']}",
            "",
            "## Risk Matrix",
            "",
            "| Entity ID | Entity Name | Department | Type | Risk Score | Risk Level | Recommended Frequency |",
            "|-----------|-------------|------------|------|------------|------------|----------------------|",
        ]
    )

    for entity, score, level, frequency in scored:
        lines.append(
            f"| {entity.entity_id} | {entity.entity_name} | {entity.department} | "
            f"{entity.entity_type} | {score:.2f} | {level} | {frequency} |"
        )

    lines.extend(
        [
            "",
            "## Risk Factor Weights",
            "",
            "| Factor | Weight |",
            "|--------|--------|",
        ]
    )

    for factor, weight in DEFAULT_WEIGHTS.items():
        factor_name = factor.replace("_", " ").title()
        lines.append(f"| {factor_name} | {weight:.0%} |")

    lines.extend(
        [
            "",
            "## Risk Level Definitions",
            "",
            "| Level | Score Range | Audit Frequency |",
            "|-------|-------------|-----------------|",
            "| Critical | 4.0 - 5.0 | Annual (required) |",
            "| High | 3.0 - 3.9 | Every 1-2 years |",
            "| Medium | 2.0 - 2.9 | Every 2-3 years |",
            "| Low | 1.0 - 1.9 | Every 3-5 years |",
            "",
        ]
    )

    return "\n".join(lines)


def generate_json_report(entities: list[AuditableEntity]) -> str:
    """
    Generate JSON risk matrix report.

    Args:
        entities: List of AuditableEntity instances

    Returns:
        JSON formatted report string
    """
    results = []
    for entity in entities:
        score = calculate_risk_score(entity.risk_factors)
        level = get_risk_level(score)
        frequency = get_audit_frequency(level)
        results.append(
            {
                "entity_id": entity.entity_id,
                "entity_name": entity.entity_name,
                "department": entity.department,
                "entity_type": entity.entity_type,
                "last_audit": entity.last_audit,
                "risk_factors": {
                    "inherent_risk": entity.risk_factors.inherent_risk,
                    "control_environment": entity.risk_factors.control_environment,
                    "financial_impact": entity.risk_factors.financial_impact,
                    "regulatory_impact": entity.risk_factors.regulatory_impact,
                    "last_audit_date": entity.risk_factors.last_audit_date,
                    "management_concern": entity.risk_factors.management_concern,
                },
                "risk_score": score,
                "risk_level": level,
                "recommended_frequency": frequency,
            }
        )

    results.sort(key=lambda x: x["risk_score"], reverse=True)
    return json.dumps({"entities": results, "weights": DEFAULT_WEIGHTS}, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Calculate risk scores for internal audit planning")
    parser.add_argument("input_file", help="CSV file with auditable entities")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)", default=None)
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    entities = parse_csv(input_path)

    if args.format == "json":
        report = generate_json_report(entities)
    else:
        report = generate_markdown_report(entities)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
        print(f"Report written to: {output_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
