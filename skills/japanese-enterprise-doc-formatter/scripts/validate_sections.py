#!/usr/bin/env python3
"""
Document Section Validator

Validates that Japanese enterprise documents contain all required sections
based on document type. Reports missing sections and provides completeness scores.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class DocumentType(Enum):
    """Supported document types."""

    RINGI = "ringi"  # 稟議書
    PURCHASE = "purchase"  # 購入申請書
    PROPOSAL = "proposal"  # 提案書
    REPORT = "report"  # 報告書
    REQUEST = "request"  # 依頼書


# Required sections for each document type
REQUIRED_SECTIONS = {
    DocumentType.RINGI: {
        "required": [
            "件名",
            "起案日",
            "起案者",
            "起案部署",
            "決裁期限",
            "目的",
            "背景",
            "内容",
            "効果",
            "リスク",
            "費用",
            "承認欄",
        ],
        "optional": ["代替案", "添付資料"],
    },
    DocumentType.PURCHASE: {
        "required": ["件名", "申請日", "申請者", "品名", "数量", "単価", "合計金額", "購入先", "購入理由", "希望納期"],
        "optional": ["予算コード", "添付資料", "比較検討"],
    },
    DocumentType.PROPOSAL: {
        "required": [
            "表題",
            "提案日",
            "提案者",
            "要旨",
            "現状の課題",
            "提案内容",
            "期待効果",
            "実施計画",
            "必要リソース",
        ],
        "optional": ["リスク分析", "成功指標", "代替案"],
    },
    DocumentType.REPORT: {
        "required": ["表題", "報告日", "報告者", "概要", "経緯", "結果", "今後の対応"],
        "optional": ["分析", "添付資料", "参考情報"],
    },
    DocumentType.REQUEST: {
        "required": ["件名", "依頼日", "依頼者", "依頼先", "依頼事項", "依頼理由", "期限"],
        "optional": ["連絡先", "備考"],
    },
}

# Section aliases (alternative names for the same section)
SECTION_ALIASES = {
    "件名": ["タイトル", "表題", "題名", "Subject"],
    "起案日": ["作成日", "日付", "Date"],
    "起案者": ["作成者", "担当者", "Author"],
    "起案部署": ["所属部署", "部署", "Department"],
    "決裁期限": ["承認期限", "期限", "Deadline"],
    "目的": ["Purpose", "目標"],
    "背景": ["経緯", "Background"],
    "内容": ["詳細", "Details", "概要"],
    "効果": ["期待効果", "メリット", "Benefits"],
    "リスク": ["懸念事項", "Risks", "課題"],
    "費用": ["コスト", "予算", "Cost", "金額"],
    "承認欄": ["決裁欄", "Approval"],
    "代替案": ["Alternative", "他の選択肢"],
    "添付資料": ["Attachments", "参考資料"],
    "申請日": ["申請日付", "Application Date"],
    "申請者": ["Applicant", "依頼者"],
    "品名": ["商品名", "製品名", "Item"],
    "数量": ["Quantity", "個数"],
    "単価": ["Unit Price", "価格"],
    "合計金額": ["総額", "Total", "合計"],
    "購入先": ["仕入先", "Vendor", "ベンダー"],
    "購入理由": ["理由", "Reason"],
    "希望納期": ["納期", "Delivery Date"],
    "提案日": ["Proposal Date"],
    "提案者": ["Proposer"],
    "要旨": ["概要", "Summary", "Executive Summary"],
    "現状の課題": ["課題", "問題点", "Issues"],
    "提案内容": ["提案", "Proposal"],
    "実施計画": ["スケジュール", "Schedule", "計画"],
    "必要リソース": ["リソース", "Resources", "予算"],
    "報告日": ["Report Date"],
    "報告者": ["Reporter"],
    "今後の対応": ["次のステップ", "Next Steps", "アクション"],
    "依頼日": ["Request Date"],
    "依頼先": ["宛先", "Recipient"],
    "依頼事項": ["依頼内容", "Request"],
}


@dataclass
class SectionValidationResult:
    """Result of section validation."""

    section_name: str
    found: bool
    found_as: Optional[str] = None  # Alias if found under different name
    is_required: bool = True


@dataclass
class DocumentValidationResult:
    """Complete document validation result."""

    document_type: DocumentType
    sections: list = field(default_factory=list)
    missing_required: list = field(default_factory=list)
    missing_optional: list = field(default_factory=list)
    found_sections: list = field(default_factory=list)
    completeness_score: float = 0.0
    is_valid: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON output."""
        return {
            "document_type": self.document_type.value,
            "validation_result": {
                "is_valid": self.is_valid,
                "completeness_score": round(self.completeness_score, 2),
            },
            "sections": {
                "found": self.found_sections,
                "missing_required": self.missing_required,
                "missing_optional": self.missing_optional,
            },
            "section_details": [
                {
                    "name": s.section_name,
                    "found": s.found,
                    "found_as": s.found_as,
                    "is_required": s.is_required,
                }
                for s in self.sections
            ],
        }


def parse_document_type(type_str: str) -> DocumentType:
    """Parse document type from string."""
    type_map = {
        "ringi": DocumentType.RINGI,
        "稟議書": DocumentType.RINGI,
        "稟議": DocumentType.RINGI,
        "purchase": DocumentType.PURCHASE,
        "購入申請書": DocumentType.PURCHASE,
        "購入申請": DocumentType.PURCHASE,
        "proposal": DocumentType.PROPOSAL,
        "提案書": DocumentType.PROPOSAL,
        "提案": DocumentType.PROPOSAL,
        "report": DocumentType.REPORT,
        "報告書": DocumentType.REPORT,
        "報告": DocumentType.REPORT,
        "request": DocumentType.REQUEST,
        "依頼書": DocumentType.REQUEST,
        "依頼": DocumentType.REQUEST,
    }
    normalized = type_str.lower().strip()
    if normalized in type_map:
        return type_map[normalized]
    raise ValueError(f"Unknown document type: {type_str}")


def extract_sections_from_markdown(content: str) -> list[str]:
    """Extract section headers from markdown content."""
    sections = []

    # Match markdown headers (## or ###)
    header_pattern = r"^#{1,3}\s+(?:\d+\.\s+)?(.+)$"

    for line in content.split("\n"):
        match = re.match(header_pattern, line.strip())
        if match:
            section_name = match.group(1).strip()
            sections.append(section_name)

    # Also look for table headers that might indicate sections.
    # Important: exclude newline from the cell character class so a cell pattern
    # cannot span across rows (the `|\n|` between two rows would otherwise
    # consume the leading `|` of the next row, making every other row's first
    # cell unreachable to subsequent matches — that previously dropped rows
    # like 起案日 / 起案部署 from the extracted set).
    table_pattern = r"\|\s*([^|\n]+?)\s*\|"
    for match in re.finditer(table_pattern, content):
        cell = match.group(1).strip()
        if cell and cell not in ["---", "項目", "内容", "金額", "日付"]:
            # Check if it's a known section name
            for canonical, aliases in SECTION_ALIASES.items():
                if cell == canonical or cell in aliases:
                    sections.append(cell)
                    break

    return sections


def find_section(section_name: str, found_sections: list[str]) -> Optional[str]:
    """
    Find a section by name or alias.
    Returns the name it was found under, or None if not found.
    """
    # Direct match
    if section_name in found_sections:
        return section_name

    # Check aliases
    aliases = SECTION_ALIASES.get(section_name, [])
    for alias in aliases:
        if alias in found_sections:
            return alias

    # Partial match (section name contained in found section)
    for found in found_sections:
        if section_name in found:
            return found
        for alias in aliases:
            if alias in found:
                return found

    return None


def validate_document(content: str, doc_type: DocumentType) -> DocumentValidationResult:
    """Validate document sections against requirements."""
    requirements = REQUIRED_SECTIONS[doc_type]
    found_sections = extract_sections_from_markdown(content)

    result = DocumentValidationResult(document_type=doc_type)
    result.found_sections = found_sections

    # Validate required sections
    for section_name in requirements["required"]:
        found_as = find_section(section_name, found_sections)
        validation = SectionValidationResult(
            section_name=section_name,
            found=found_as is not None,
            found_as=found_as if found_as != section_name else None,
            is_required=True,
        )
        result.sections.append(validation)

        if not found_as:
            result.missing_required.append(section_name)

    # Check optional sections
    for section_name in requirements["optional"]:
        found_as = find_section(section_name, found_sections)
        validation = SectionValidationResult(
            section_name=section_name,
            found=found_as is not None,
            found_as=found_as if found_as != section_name else None,
            is_required=False,
        )
        result.sections.append(validation)

        if not found_as:
            result.missing_optional.append(section_name)

    # Calculate completeness score
    required_count = len(requirements["required"])
    found_required_count = required_count - len(result.missing_required)
    result.completeness_score = (found_required_count / required_count) * 100

    # Document is valid if all required sections are present
    result.is_valid = len(result.missing_required) == 0

    return result


def format_validation_report(result: DocumentValidationResult) -> str:
    """Format validation result as readable text."""
    lines = []

    lines.append(f"Document Type: {result.document_type.value}")
    lines.append(f"Validation Result: {'PASS' if result.is_valid else 'FAIL'}")
    lines.append(f"Completeness Score: {result.completeness_score:.1f}%")
    lines.append("")

    if result.missing_required:
        lines.append("Missing Required Sections:")
        for section in result.missing_required:
            lines.append(f"  - {section}")
        lines.append("")

    if result.missing_optional:
        lines.append("Missing Optional Sections:")
        for section in result.missing_optional:
            lines.append(f"  - {section}")
        lines.append("")

    lines.append("Section Details:")
    for section in result.sections:
        status = "✓" if section.found else "✗"
        req_marker = "(required)" if section.is_required else "(optional)"
        alias_info = f" [found as: {section.found_as}]" if section.found_as else ""
        lines.append(f"  {status} {section.section_name} {req_marker}{alias_info}")

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate Japanese enterprise document sections")
    parser.add_argument("--input", "-i", required=True, help="Input document file path")
    parser.add_argument(
        "--document-type", "-t", required=True, help="Document type: ringi, purchase, proposal, report, request"
    )
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    # Parse document type
    try:
        doc_type = parse_document_type(args.document_type)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Read input document
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    content = input_path.read_text(encoding="utf-8")

    # Validate
    result = validate_document(content, doc_type)

    # Output
    if args.format == "json":
        output = json.dumps(result.to_dict(), ensure_ascii=False, indent=2)
    else:
        output = format_validation_report(result)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Validation report written to: {args.output}", file=sys.stderr)
    else:
        print(output)

    # Exit with error if validation failed
    if not result.is_valid:
        sys.exit(1)


if __name__ == "__main__":
    main()
