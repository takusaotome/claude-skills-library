#!/usr/bin/env python3
"""
Contract Analyzer - Automated preliminary contract analysis tool.

This script performs automated analysis of contract documents to:
- Detect contract type (NDA, MSA, SOW, SLA, License)
- Extract key clauses and terms
- Identify red flag patterns
- Calculate preliminary risk scores
- Generate Markdown analysis reports

Usage:
    python analyze_contract.py contract.txt --output report.md
    python analyze_contract.py contract.pdf --type nda --output nda_report.md
    python analyze_contract.py contract.txt --party-name "Acme Corp" --verbose
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# Constants for context extraction and limits (MN-003)
CONTEXT_CHARS_BEFORE = 100
CONTEXT_CHARS_AFTER = 100
MAX_RECOMMENDATIONS = 5

# Import pattern definitions
from pattern_definitions import CLAUSE_PATTERNS, CONTRACT_TYPE_PATTERNS, RED_FLAG_PATTERNS

# Optional PDF support
try:
    import PyPDF2

    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False


@dataclass
class RedFlag:
    """Represents a detected red flag in the contract."""

    pattern_id: str
    title: str
    severity: str  # Critical, High, Medium, Low
    category: str  # Financial, Operational, Legal, Strategic, Reputational
    clause_text: str
    location: str
    description: str
    recommendation: str


@dataclass
class ContractInfo:
    """Basic contract information extracted from the document."""

    contract_type: str = "Unknown"
    parties: list[str] = field(default_factory=list)
    effective_date: str = ""
    term: str = ""
    governing_law: str = ""
    auto_renewal: bool = False
    liability_cap: str = ""
    indemnification_type: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result."""

    contract_info: ContractInfo
    red_flags: list[RedFlag] = field(default_factory=list)
    risk_score: int = 0
    risk_level: str = "Low"
    clause_coverage: dict[str, bool] = field(default_factory=dict)
    recommendations: list[dict[str, str]] = field(default_factory=list)


def read_file(filepath: Path) -> str:
    """Read content from file (supports .txt, .md, .pdf).

    Raises:
        ImportError: If PDF support is not available
        ValueError: If PDF is encrypted or contains no extractable text
        RuntimeError: If PDF parsing fails
    """
    if filepath.suffix.lower() == ".pdf":
        if not PDF_SUPPORT:
            raise ImportError("PyPDF2 not installed. Install with: pip install PyPDF2")

        text_content = []
        try:
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)

                if reader.is_encrypted:
                    raise ValueError("PDF is encrypted. Cannot analyze encrypted documents.")

                total_pages = len(reader.pages)
                for i, page in enumerate(reader.pages, 1):
                    try:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
                    except Exception as e:
                        print(f"Warning: Failed to extract page {i}/{total_pages}: {e}")

        except (ValueError, ImportError):
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF: {e}")

        if not text_content:
            raise ValueError("No text could be extracted. Document may be image-based.")

        return "\n".join(text_content)
    else:
        # CR-001: Proper encoding handling with fallback
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 (lossless for any byte sequence)
            with open(filepath, "r", encoding="latin-1") as f:
                return f.read()


def detect_contract_type(text: str, override_type: Optional[str] = None) -> str:
    """Detect the contract type from content."""
    if override_type:
        return override_type.upper()

    normalized_text = text.lower()
    type_scores: dict[str, int] = {}

    for contract_type, patterns in CONTRACT_TYPE_PATTERNS.items():
        score = 0
        for pattern in patterns:
            if re.search(pattern, normalized_text):
                score += 1
        type_scores[contract_type] = score

    if max(type_scores.values()) > 0:
        return max(type_scores, key=type_scores.get)
    return "Unknown"


def _has_negation_context(text: str, match_start: int, context_chars: int = 30) -> bool:
    """Check if match is preceded by negation words.

    Args:
        text: The text being searched (should be lowercase)
        match_start: Start position of the match
        context_chars: Number of characters to look back for negation

    Returns:
        True if negation words are found in the context before the match
    """
    start = max(0, match_start - context_chars)
    context = text[start:match_start]
    negation_words = ["not ", "no ", "never ", "without ", "doesn't ", "does not ", "shall not "]
    return any(neg in context for neg in negation_words)


def extract_contract_info(text: str) -> ContractInfo:
    """Extract basic contract information."""
    info = ContractInfo()
    normalized_text = text.lower()

    # Contract type
    info.contract_type = detect_contract_type(text)

    # Parties (basic extraction)
    party_pattern = r"(?:between|by\s+and\s+between)\s+(.+?)\s+(?:and|,)\s+(.+?)(?:\.|,|\()"
    party_match = re.search(party_pattern, text, re.IGNORECASE)
    if party_match:
        info.parties = [party_match.group(1).strip(), party_match.group(2).strip()]

    # Effective date
    date_pattern = (
        r"(?:effective|dated?|as\s+of)\s+(?:the\s+)?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\w+\s+\d{1,2},?\s+\d{4})"
    )
    date_match = re.search(date_pattern, text, re.IGNORECASE)
    if date_match:
        info.effective_date = date_match.group(1)

    # Auto-renewal (CR-003: with negation context check)
    auto_renewal_match = re.search(r"auto[\-\s]?renew|automatically\s+renew", normalized_text)
    if auto_renewal_match and not _has_negation_context(normalized_text, auto_renewal_match.start()):
        info.auto_renewal = True

    # Governing law
    law_pattern = (
        r"(?:governed\s+by|governing\s+law).{0,50}(?:laws?\s+of\s+(?:the\s+)?)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
    )
    law_match = re.search(law_pattern, text)
    if law_match:
        info.governing_law = law_match.group(1)

    # Liability cap
    cap_pattern = r"(?:liability|aggregate).{0,50}(?:not\s+exceed|limited\s+to|capped\s+at).{0,30}(\$[\d,]+|[\d]+\s*(?:times?|x)\s*(?:the\s+)?(?:fees?|amount))"
    cap_match = re.search(cap_pattern, text, re.IGNORECASE)
    if cap_match:
        info.liability_cap = cap_match.group(1)
    else:
        # CR-003: Check for unlimited liability with negation context
        unlimited_match = re.search(r"unlimited\s+liability|no\s+limit\s+on\s+liability", normalized_text)
        if unlimited_match and not _has_negation_context(normalized_text, unlimited_match.start()):
            info.liability_cap = "UNLIMITED"

    # Indemnification type
    if re.search(r"mutual\s+indemnif|each\s+party\s+shall\s+indemnif", normalized_text):
        info.indemnification_type = "Mutual"
    elif re.search(r"customer\s+shall\s+indemnif|licensee\s+shall\s+indemnif", normalized_text):
        info.indemnification_type = "One-sided (Customer)"
    elif re.search(r"vendor\s+shall\s+indemnif|provider\s+shall\s+indemnif", normalized_text):
        info.indemnification_type = "One-sided (Vendor)"

    return info


def detect_red_flags(text: str) -> list[RedFlag]:
    """Detect red flag patterns in the contract."""
    red_flags: list[RedFlag] = []
    normalized_text = text.lower()

    for red_flag_pattern in RED_FLAG_PATTERNS:
        matches = list(re.finditer(red_flag_pattern["pattern"], normalized_text, re.IGNORECASE | re.DOTALL))
        for match in matches:
            # Extract surrounding context
            start = max(0, match.start() - CONTEXT_CHARS_BEFORE)
            end = min(len(text), match.end() + CONTEXT_CHARS_AFTER)
            context = text[start:end].strip()

            # Find approximate location
            lines_before = text[: match.start()].count("\n") + 1
            location = f"Approx. line {lines_before}"

            red_flag = RedFlag(
                pattern_id=red_flag_pattern["id"],
                title=red_flag_pattern["title"],
                severity=red_flag_pattern["severity"],
                category=red_flag_pattern["category"],
                clause_text=context,
                location=location,
                description=red_flag_pattern["description"],
                recommendation=red_flag_pattern["recommendation"],
            )
            red_flags.append(red_flag)

    return red_flags


def check_clause_coverage(text: str) -> dict[str, bool]:
    """Check which standard clauses are present."""
    coverage: dict[str, bool] = {}
    normalized_text = text.lower()

    for clause_name, pattern in CLAUSE_PATTERNS.items():
        coverage[clause_name] = bool(re.search(pattern, normalized_text))

    return coverage


def calculate_risk_score(red_flags: list[RedFlag]) -> tuple[int, str]:
    """Calculate overall risk score based on red flags."""
    severity_weights = {"Critical": 20, "High": 10, "Medium": 5, "Low": 2}

    total_score = 0
    for red_flag in red_flags:
        total_score += severity_weights.get(red_flag.severity, 0)

    # Cap at 100
    total_score = min(100, total_score)

    # Determine level
    if total_score >= 76:
        level = "Critical"
    elif total_score >= 51:
        level = "High"
    elif total_score >= 26:
        level = "Moderate"
    else:
        level = "Low"

    return total_score, level


def generate_recommendations(red_flags: list[RedFlag], clause_coverage: dict[str, bool]) -> list[dict[str, str]]:
    """Generate recommendations based on analysis."""
    recommendations: list[dict[str, str]] = []

    # Red flag based recommendations
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    sorted_flags = sorted(red_flags, key=lambda x: severity_order.get(x.severity, 4))

    for red_flag in sorted_flags[:MAX_RECOMMENDATIONS]:
        recommendations.append(
            {"priority": red_flag.severity, "issue": red_flag.title, "recommendation": red_flag.recommendation}
        )

    # Missing clause recommendations
    critical_clauses = ["Liability", "Indemnification", "Termination", "Governing Law"]
    for clause in critical_clauses:
        if not clause_coverage.get(clause, False):
            recommendations.append(
                {
                    "priority": "High",
                    "issue": f"Missing {clause} clause",
                    "recommendation": f"Request addition of {clause} clause with standard protections",
                }
            )

    return recommendations


def generate_report(result: AnalysisResult, filepath: Path, party_name: str = "") -> str:
    """Generate Markdown analysis report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    reviewing_party = f"\n**Reviewing Party**: {party_name}" if party_name else ""

    report = f"""# Preliminary Contract Analysis Report

**Generated**: {now}
**Document**: {filepath.name}{reviewing_party}
**Analysis Tool**: Contract Analyzer v1.0

---

## 1. Contract Overview

| Field | Value |
|-------|-------|
| **Detected Type** | {result.contract_info.contract_type} |
| **Parties** | {", ".join(result.contract_info.parties) if result.contract_info.parties else "Not detected"} |
| **Effective Date** | {result.contract_info.effective_date or "Not detected"} |
| **Governing Law** | {result.contract_info.governing_law or "Not detected"} |
| **Auto-Renewal** | {"Yes" if result.contract_info.auto_renewal else "No"} |
| **Liability Cap** | {result.contract_info.liability_cap or "Not detected"} |
| **Indemnification** | {result.contract_info.indemnification_type or "Not detected"} |

---

## 2. Risk Assessment

### Overall Score

| Metric | Value |
|--------|-------|
| **Risk Score** | {result.risk_score} / 100 |
| **Risk Level** | **{result.risk_level}** |
| **Red Flags Found** | {len(result.red_flags)} |

"""

    # Risk level guidance
    if result.risk_level == "Critical":
        report += "> **WARNING**: Critical risk level. Do not sign without major revisions.\n\n"
    elif result.risk_level == "High":
        report += "> **CAUTION**: High risk level. Significant negotiation required.\n\n"
    elif result.risk_level == "Moderate":
        report += "> **ATTENTION**: Moderate risk. Review and negotiate key terms.\n\n"
    else:
        report += "> **OK**: Low risk level. Minor review recommended.\n\n"

    # Red flags section
    report += "### Red Flags Detected\n\n"

    if result.red_flags:
        report += "| # | Severity | Issue | Category |\n"
        report += "|---|----------|-------|----------|\n"

        for i, red_flag in enumerate(result.red_flags, 1):
            report += f"| {i} | {red_flag.severity} | {red_flag.title} | {red_flag.category} |\n"

        report += "\n#### Red Flag Details\n\n"

        for i, red_flag in enumerate(result.red_flags, 1):
            report += f"""##### {i}. {red_flag.title}

- **Severity**: {red_flag.severity}
- **Category**: {red_flag.category}
- **Location**: {red_flag.location}
- **Issue**: {red_flag.description}
- **Recommendation**: {red_flag.recommendation}

**Context**:
> ...{red_flag.clause_text}...

---

"""
    else:
        report += "*No red flags detected in automated scan.*\n\n"
        report += "> Note: Manual review is still recommended.\n\n"

    # Clause coverage
    report += "## 3. Clause Coverage\n\n"
    report += "| Clause | Present |\n"
    report += "|--------|--------|\n"

    for clause, present in result.clause_coverage.items():
        status = "Yes" if present else "**No**"
        report += f"| {clause} | {status} |\n"

    missing_count = sum(1 for v in result.clause_coverage.values() if not v)
    if missing_count > 0:
        report += f"\n> **Note**: {missing_count} standard clauses not detected.\n\n"

    # Recommendations
    report += "## 4. Recommendations\n\n"

    if result.recommendations:
        report += "| Priority | Issue | Recommendation |\n"
        report += "|----------|-------|----------------|\n"

        for rec in result.recommendations:
            report += f"| {rec['priority']} | {rec['issue']} | {rec['recommendation']} |\n"
    else:
        report += "*No specific recommendations from automated analysis.*\n"

    # Footer
    report += """
---

## Disclaimer

This is an automated preliminary analysis and should NOT be used as the sole basis
for contract decisions. A thorough manual review using the full contract review
workflow is recommended. Consult qualified legal counsel for binding decisions.

---

*End of Report*
"""

    return report


def analyze_contract(
    filepath: Path, contract_type: Optional[str] = None, party_name: str = "", verbose: bool = False
) -> AnalysisResult:
    """Main analysis function."""
    if verbose:
        print(f"Reading file: {filepath}")

    text = read_file(filepath)

    if verbose:
        print(f"Document length: {len(text)} characters")

    # Extract info
    if verbose:
        print("Extracting contract information...")
    contract_info = extract_contract_info(text)

    if contract_type:
        contract_info.contract_type = contract_type.upper()

    if verbose:
        print(f"Detected contract type: {contract_info.contract_type}")

    # Detect red flags
    if verbose:
        print("Scanning for red flags...")
    red_flags = detect_red_flags(text)

    if verbose:
        print(f"Found {len(red_flags)} red flags")

    # Check clause coverage
    if verbose:
        print("Checking clause coverage...")
    clause_coverage = check_clause_coverage(text)

    # Calculate risk score
    risk_score, risk_level = calculate_risk_score(red_flags)

    if verbose:
        print(f"Risk score: {risk_score} ({risk_level})")

    # Generate recommendations
    recommendations = generate_recommendations(red_flags, clause_coverage)

    return AnalysisResult(
        contract_info=contract_info,
        red_flags=red_flags,
        risk_score=risk_score,
        risk_level=risk_level,
        clause_coverage=clause_coverage,
        recommendations=recommendations,
    )


def main() -> int:
    """Main entry point.

    Returns:
        int: Exit code based on risk level:
            0 = Low risk
            1 = Moderate risk (or general error)
            2 = High risk
            3 = Critical risk
    """
    parser = argparse.ArgumentParser(
        description="Analyze contract documents for risks and red flags",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_contract.py contract.txt --output report.md
  python analyze_contract.py contract.pdf --type nda --output nda_report.md
  python analyze_contract.py contract.txt --party-name "Acme Corp" --verbose
        """,
    )

    parser.add_argument("input_file", type=Path, help="Contract file to analyze (txt, md, pdf)")
    parser.add_argument("--output", "-o", type=Path, help="Output report file (Markdown)")
    parser.add_argument(
        "--type", "-t", choices=["nda", "msa", "sow", "sla", "license"], help="Override contract type detection"
    )
    parser.add_argument("--party-name", help="Your organization's name for context")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Validate input file
    if not args.input_file.exists():
        print(f"Error: File not found: {args.input_file}")
        return 1

    # Run analysis with exception handling
    try:
        result = analyze_contract(
            args.input_file, contract_type=args.type, party_name=args.party_name or "", verbose=args.verbose
        )
    except ImportError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1

    # Generate report
    report = generate_report(result, args.input_file, args.party_name or "")

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to: {args.output}")
    else:
        print(report)

    # Return exit code based on risk level
    exit_codes = {"Critical": 3, "High": 2, "Moderate": 1, "Low": 0}
    return exit_codes.get(result.risk_level, 0)


if __name__ == "__main__":
    sys.exit(main())
