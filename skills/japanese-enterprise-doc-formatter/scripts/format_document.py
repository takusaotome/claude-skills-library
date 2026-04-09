#!/usr/bin/env python3
"""
Japanese Enterprise Document Formatter

Formats business documents for Japanese enterprise approval workflows.
Supports ringi (稟議), purchase requests (購入申請), proposals (提案書),
reports (報告書), and requests (依頼書).
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
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


class KeigoLevel(Enum):
    """Keigo formality levels."""

    HIGHEST = "highest"  # 最上級敬語 (役員向け)
    UPPER = "upper"  # 上級敬語 (本部長/部長向け)
    STANDARD = "standard"  # 標準敬語 (課長向け)
    BASIC = "basic"  # 基本丁寧語 (同僚向け)


# Required sections for each document type
REQUIRED_SECTIONS = {
    DocumentType.RINGI: [
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
    DocumentType.PURCHASE: [
        "件名",
        "申請日",
        "申請者",
        "品名",
        "数量",
        "単価",
        "合計金額",
        "購入先",
        "購入理由",
        "希望納期",
    ],
    DocumentType.PROPOSAL: [
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
    DocumentType.REPORT: ["表題", "報告日", "報告者", "概要", "経緯", "結果", "今後の対応"],
    DocumentType.REQUEST: ["件名", "依頼日", "依頼者", "依頼先", "依頼事項", "依頼理由", "期限"],
}

# Japanese names for document types
DOCUMENT_TYPE_NAMES = {
    DocumentType.RINGI: "稟議書",
    DocumentType.PURCHASE: "購入申請書",
    DocumentType.PROPOSAL: "提案書",
    DocumentType.REPORT: "報告書",
    DocumentType.REQUEST: "依頼書",
}

# Document number prefixes
DOCUMENT_PREFIXES = {
    DocumentType.RINGI: "RINGI",
    DocumentType.PURCHASE: "PO",
    DocumentType.PROPOSAL: "PROP",
    DocumentType.REPORT: "RPT",
    DocumentType.REQUEST: "REQ",
}

# Keigo closing phrases
CLOSING_PHRASES = {
    KeigoLevel.HIGHEST: "何卒ご裁可賜りますよう、謹んでお願い申し上げます。",
    KeigoLevel.UPPER: "ご検討のほど、よろしくお願い申し上げます。",
    KeigoLevel.STANDARD: "よろしくお願いいたします。",
    KeigoLevel.BASIC: "よろしくお願いします。",
}


@dataclass
class DocumentMetadata:
    """Document metadata."""

    document_type: DocumentType
    document_id: str
    subject: str
    draft_date: str
    drafter: str
    department: str
    approval_deadline: Optional[str] = None
    keigo_level: KeigoLevel = KeigoLevel.STANDARD
    bilingual: bool = False


@dataclass
class DocumentSection:
    """A section of the document."""

    name: str
    content: str
    is_required: bool = True


@dataclass
class FormattedDocument:
    """Formatted document output."""

    metadata: DocumentMetadata
    sections: list = field(default_factory=list)
    validation_warnings: list = field(default_factory=list)
    english_summary: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON output."""
        return {
            "schema_version": "1.0",
            "document_type": DOCUMENT_TYPE_NAMES[self.metadata.document_type],
            "document_id": self.metadata.document_id,
            "metadata": {
                "subject": self.metadata.subject,
                "draft_date": self.metadata.draft_date,
                "drafter": self.metadata.drafter,
                "department": self.metadata.department,
                "approval_deadline": self.metadata.approval_deadline,
                "keigo_level": self.metadata.keigo_level.value,
                "bilingual": self.metadata.bilingual,
            },
            "sections": {s.name: s.content for s in self.sections},
            "validation": {
                "all_sections_present": len(self.validation_warnings) == 0,
                "keigo_compliance": True,
                "warnings": self.validation_warnings,
            },
            "english_summary": self.english_summary,
        }


def generate_document_id(doc_type: DocumentType, sequence: int = 1) -> str:
    """Generate a document ID."""
    prefix = DOCUMENT_PREFIXES[doc_type]
    year = datetime.now().year
    return f"{prefix}-{year}-{sequence:03d}"


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


def parse_keigo_level(level_str: str) -> KeigoLevel:
    """Parse keigo level from string."""
    level_map = {
        "highest": KeigoLevel.HIGHEST,
        "最上級": KeigoLevel.HIGHEST,
        "formal": KeigoLevel.HIGHEST,
        "upper": KeigoLevel.UPPER,
        "上級": KeigoLevel.UPPER,
        "standard": KeigoLevel.STANDARD,
        "標準": KeigoLevel.STANDARD,
        "basic": KeigoLevel.BASIC,
        "基本": KeigoLevel.BASIC,
    }
    normalized = level_str.lower().strip()
    if normalized in level_map:
        return level_map[normalized]
    raise ValueError(f"Unknown keigo level: {level_str}")


def validate_sections(doc_type: DocumentType, sections: list[DocumentSection]) -> list[str]:
    """Validate that all required sections are present."""
    warnings = []
    required = REQUIRED_SECTIONS[doc_type]
    section_names = {s.name for s in sections}

    for req in required:
        if req not in section_names:
            warnings.append(f"Missing required section: {req}")

    return warnings


def format_date_japanese(date_str: str) -> str:
    """Format date in Japanese style (YYYY年MM月DD日)."""
    try:
        if "年" in date_str:
            return date_str
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except ValueError:
        return date_str


def generate_approval_table(doc_type: DocumentType) -> str:
    """Generate approval section table."""
    if doc_type == DocumentType.RINGI:
        return """
| 役職 | 氏名 | 日付 | 印/署名 |
|------|------|------|---------|
| 課長 |      |      |         |
| 部長 |      |      |         |
| 本部長 |    |      |         |
| 役員 |      |      |         |
"""
    elif doc_type == DocumentType.PURCHASE:
        return """
| 役職 | 氏名 | 日付 | 印/署名 |
|------|------|------|---------|
| 課長 |      |      |         |
| 部長 |      |      |         |
"""
    else:
        return """
| 役職 | 氏名 | 日付 | 印/署名 |
|------|------|------|---------|
| 承認者 |    |      |         |
"""


def format_document_markdown(doc: FormattedDocument) -> str:
    """Format document as Markdown."""
    lines = []

    # Title
    doc_name = DOCUMENT_TYPE_NAMES[doc.metadata.document_type]
    lines.append(f"# {doc_name}")
    lines.append("")

    # Metadata table
    lines.append("## 基本情報")
    lines.append("")
    lines.append("| 項目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| 文書番号 | {doc.metadata.document_id} |")
    lines.append(f"| 件名 | {doc.metadata.subject} |")
    lines.append(f"| 起案日 | {format_date_japanese(doc.metadata.draft_date)} |")
    lines.append(f"| 起案者 | {doc.metadata.drafter} |")
    lines.append(f"| 起案部署 | {doc.metadata.department} |")
    if doc.metadata.approval_deadline:
        lines.append(f"| 決裁期限 | {format_date_japanese(doc.metadata.approval_deadline)} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sections
    for i, section in enumerate(doc.sections, 1):
        if section.name == "承認欄":
            lines.append(f"## {section.name}")
        else:
            lines.append(f"## {i}. {section.name}")
        lines.append("")
        lines.append(section.content)
        lines.append("")
        lines.append("---")
        lines.append("")

    # Approval section
    lines.append("## 承認欄")
    lines.append(generate_approval_table(doc.metadata.document_type))
    lines.append("---")
    lines.append("")

    # Closing phrase
    closing = CLOSING_PHRASES[doc.metadata.keigo_level]
    lines.append(closing)
    lines.append("")

    # English summary if bilingual
    if doc.metadata.bilingual and doc.english_summary:
        lines.append("---")
        lines.append("")
        lines.append("## English Summary")
        lines.append("")
        lines.append(doc.english_summary)
        lines.append("")

    return "\n".join(lines)


def create_sample_document(
    doc_type: DocumentType, keigo_level: KeigoLevel = KeigoLevel.STANDARD, bilingual: bool = False
) -> FormattedDocument:
    """Create a sample document for demonstration."""
    today = datetime.now().strftime("%Y-%m-%d")

    metadata = DocumentMetadata(
        document_type=doc_type,
        document_id=generate_document_id(doc_type),
        subject="新規システム導入の件",
        draft_date=today,
        drafter="山田太郎",
        department="情報システム部",
        approval_deadline=(datetime.now().strftime("%Y-%m-%d") if doc_type == DocumentType.RINGI else None),
        keigo_level=keigo_level,
        bilingual=bilingual,
    )

    sections = []
    required = REQUIRED_SECTIONS[doc_type]

    for section_name in required:
        if section_name in ["件名", "起案日", "起案者", "起案部署", "決裁期限"]:
            continue
        sections.append(
            DocumentSection(
                name=section_name,
                content=f"[{section_name}の内容をここに記載]",
            )
        )

    doc = FormattedDocument(
        metadata=metadata,
        sections=sections,
        validation_warnings=validate_sections(doc_type, sections),
        english_summary="[English summary to be provided]" if bilingual else None,
    )

    return doc


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Format Japanese enterprise documents")
    parser.add_argument("--type", "-t", required=True, help="Document type: ringi, purchase, proposal, report, request")
    parser.add_argument("--keigo-level", "-k", default="standard", help="Keigo level: highest, upper, standard, basic")
    parser.add_argument("--bilingual", "-b", action="store_true", help="Include English summary section")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--sample", action="store_true", help="Generate a sample document")

    args = parser.parse_args()

    try:
        doc_type = parse_document_type(args.type)
        keigo_level = parse_keigo_level(args.keigo_level)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.sample:
        doc = create_sample_document(doc_type, keigo_level, args.bilingual)
    else:
        # In real usage, this would parse input content
        doc = create_sample_document(doc_type, keigo_level, args.bilingual)

    if args.format == "json":
        output = json.dumps(doc.to_dict(), ensure_ascii=False, indent=2)
    else:
        output = format_document_markdown(doc)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Document written to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
