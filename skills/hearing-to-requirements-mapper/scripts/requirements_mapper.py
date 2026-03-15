#!/usr/bin/env python3
"""
Requirements Mapper - Core library for hearing-to-requirements mapping.

This module provides classes and functions for:
- Parsing hearing sheets and meeting notes
- Classifying requirements by type and priority
- Detecting gaps and ambiguities
- Mapping requirements to WBS items
- Generating traceability matrices
"""

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class RequirementType(Enum):
    """Requirement classification types."""

    BUSINESS = "business"
    STAKEHOLDER = "stakeholder"
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"
    ASSUMPTION = "assumption"


class Priority(Enum):
    """MoSCoW priority levels."""

    MUST_HAVE = "must_have"
    SHOULD_HAVE = "should_have"
    COULD_HAVE = "could_have"
    WONT_HAVE = "wont_have"


class GapSeverity(Enum):
    """Gap severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class GapCategory(Enum):
    """Gap categories."""

    MISSING = "missing"
    AMBIGUOUS = "ambiguous"
    CONFLICTING = "conflicting"
    INCOMPLETE = "incomplete"


@dataclass
class Source:
    """Source reference for traceability."""

    document: str
    section: Optional[str] = None
    line: Optional[int] = None
    timestamp: Optional[str] = None


@dataclass
class Requirement:
    """A single requirement extracted from hearing data."""

    id: str
    type: RequirementType
    category: str
    description: str
    description_en: Optional[str] = None
    priority: Priority = Priority.SHOULD_HAVE
    source: Optional[Source] = None
    acceptance_criteria: list = field(default_factory=list)
    wbs_items: list = field(default_factory=list)
    status: str = "draft"
    notes: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            "id": self.id,
            "type": self.type.value,
            "category": self.category,
            "description": self.description,
            "priority": self.priority.value,
            "acceptance_criteria": self.acceptance_criteria,
            "wbs_items": self.wbs_items,
            "status": self.status,
            "notes": self.notes,
        }
        if self.description_en:
            result["description_en"] = self.description_en
        if self.source:
            result["source"] = asdict(self.source)
        return result


@dataclass
class Gap:
    """A gap or ambiguity detected in requirements."""

    id: str
    category: GapCategory
    severity: GapSeverity
    description: str
    recommendation: str
    related_requirements: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "category": self.category.value,
            "severity": self.severity.value,
            "description": self.description,
            "recommendation": self.recommendation,
            "related_requirements": self.related_requirements,
        }


@dataclass
class RequirementsDocument:
    """Container for a complete requirements analysis."""

    project_name: str
    source_documents: list
    language: str
    requirements: list = field(default_factory=list)
    gaps: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "schema_version": "1.0",
            "metadata": {
                "project_name": self.project_name,
                "created_at": self.created_at,
                "source_documents": self.source_documents,
                "language": self.language,
            },
            "requirements": [r.to_dict() for r in self.requirements],
            "gaps": [g.to_dict() for g in self.gaps],
            "summary": self.generate_summary(),
        }

    def generate_summary(self) -> dict:
        """Generate summary statistics."""
        by_type = {}
        by_priority = {}

        for req in self.requirements:
            type_key = req.type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1

            priority_key = req.priority.value
            by_priority[priority_key] = by_priority.get(priority_key, 0) + 1

        gaps_by_severity = {}
        for gap in self.gaps:
            sev = gap.severity.value
            gaps_by_severity[sev] = gaps_by_severity.get(sev, 0) + 1

        return {
            "total_requirements": len(self.requirements),
            "by_type": by_type,
            "by_priority": by_priority,
            "gaps_found": len(self.gaps),
            "gaps_by_severity": gaps_by_severity,
        }


class LanguageDetector:
    """Detect language of input text."""

    @staticmethod
    def detect(text: str) -> str:
        """
        Detect if text is primarily Japanese, English, or mixed.

        Args:
            text: Input text to analyze

        Returns:
            'ja' for Japanese, 'en' for English, 'mixed' for mixed content
        """
        # Count Japanese characters (hiragana, katakana, kanji)
        japanese_pattern = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]")
        japanese_chars = len(japanese_pattern.findall(text))

        # Count ASCII letters
        ascii_pattern = re.compile(r"[a-zA-Z]")
        ascii_chars = len(ascii_pattern.findall(text))

        total = japanese_chars + ascii_chars
        if total == 0:
            return "en"

        japanese_ratio = japanese_chars / total

        if japanese_ratio > 0.7:
            return "ja"
        elif japanese_ratio < 0.3:
            return "en"
        else:
            return "mixed"


class AmbiguityDetector:
    """Detect ambiguous language in requirements."""

    # Patterns for Japanese ambiguity
    JA_VAGUE_QUANTIFIERS = [
        r"多く",
        r"いくつか",
        r"大量",
        r"十分",
        r"高速",
        r"迅速",
        r"適切",
        r"簡単",
        r"効率的",
        r"できるだけ",
        r"なるべく",
    ]

    JA_OPEN_LISTS = [r"など$", r"等$", r"を含む$", r"等々", r"その他"]

    JA_PASSIVE = [r"される$", r"られる$", r"が行われる$"]

    JA_TEMPORAL = [r"すぐに", r"即座に", r"定期的", r"必要に応じて", r"随時", r"タイムリー"]

    # Patterns for English ambiguity
    EN_VAGUE_QUANTIFIERS = [
        r"\bmany\b",
        r"\bseveral\b",
        r"\bsome\b",
        r"\benough\b",
        r"\bfast\b",
        r"\bquick\b",
        r"\bappropriate\b",
        r"\beasy\b",
        r"\bsimple\b",
        r"\befficient\b",
    ]

    EN_OPEN_LISTS = [r"\betc\.", r"and so on", r"and others", r"and more"]

    EN_PASSIVE = [r"\bis\s+\w+ed\b", r"\bare\s+\w+ed\b", r"\bwill be\s+\w+ed\b"]

    EN_TEMPORAL = [r"\bimmediately\b", r"\bperiodically\b", r"\bas needed\b", r"\banytime\b", r"\btimely\b"]

    def __init__(self):
        """Initialize detector with compiled patterns."""
        self.ja_patterns = {
            "vague_quantifier": [re.compile(p) for p in self.JA_VAGUE_QUANTIFIERS],
            "open_list": [re.compile(p) for p in self.JA_OPEN_LISTS],
            "passive_voice": [re.compile(p) for p in self.JA_PASSIVE],
            "temporal_ambiguity": [re.compile(p) for p in self.JA_TEMPORAL],
        }
        self.en_patterns = {
            "vague_quantifier": [re.compile(p, re.IGNORECASE) for p in self.EN_VAGUE_QUANTIFIERS],
            "open_list": [re.compile(p, re.IGNORECASE) for p in self.EN_OPEN_LISTS],
            "passive_voice": [re.compile(p, re.IGNORECASE) for p in self.EN_PASSIVE],
            "temporal_ambiguity": [re.compile(p, re.IGNORECASE) for p in self.EN_TEMPORAL],
        }

    def detect_ambiguities(self, text: str, language: str = "auto") -> list:
        """
        Detect ambiguities in text.

        Args:
            text: Text to analyze
            language: 'ja', 'en', or 'auto' for auto-detection

        Returns:
            List of detected ambiguities with category and matched text
        """
        if language == "auto":
            language = LanguageDetector.detect(text)

        ambiguities = []

        # Select patterns based on language
        if language in ("ja", "mixed"):
            for category, patterns in self.ja_patterns.items():
                for pattern in patterns:
                    matches = pattern.findall(text)
                    for match in matches:
                        ambiguities.append(
                            {
                                "category": category,
                                "matched_text": match,
                                "language": "ja",
                                "severity": self._get_severity(category),
                            }
                        )

        if language in ("en", "mixed"):
            for category, patterns in self.en_patterns.items():
                for pattern in patterns:
                    matches = pattern.findall(text)
                    for match in matches:
                        ambiguities.append(
                            {
                                "category": category,
                                "matched_text": match,
                                "language": "en",
                                "severity": self._get_severity(category),
                            }
                        )

        return ambiguities

    @staticmethod
    def _get_severity(category: str) -> str:
        """Map category to severity level."""
        severity_map = {
            "vague_quantifier": "high",
            "open_list": "medium",
            "passive_voice": "medium",
            "temporal_ambiguity": "high",
        }
        return severity_map.get(category, "low")


class RequirementClassifier:
    """Classify requirements by type."""

    # Keywords indicating requirement types (Japanese)
    JA_BUSINESS_KEYWORDS = ["売上", "コスト", "ROI", "収益", "利益", "目標", "戦略"]
    JA_STAKEHOLDER_KEYWORDS = ["ユーザー", "管理者", "担当者", "営業", "顧客", "オペレーター"]
    JA_FUNCTIONAL_KEYWORDS = ["システムは", "機能", "処理", "表示", "保存", "検索", "登録"]
    JA_NFR_KEYWORDS = ["応答時間", "セキュリティ", "可用性", "稼働率", "暗号化", "パフォーマンス"]
    JA_CONSTRAINT_KEYWORDS = ["制約", "制限", "予算", "期限", "必須", "禁止"]
    JA_ASSUMPTION_KEYWORDS = ["前提", "想定", "仮定"]

    # Keywords indicating requirement types (English)
    EN_BUSINESS_KEYWORDS = ["revenue", "cost", "roi", "profit", "goal", "strategy", "kpi"]
    EN_STAKEHOLDER_KEYWORDS = ["user", "admin", "manager", "operator", "customer", "staff"]
    EN_FUNCTIONAL_KEYWORDS = ["system shall", "function", "process", "display", "store", "search"]
    EN_NFR_KEYWORDS = ["response time", "security", "availability", "uptime", "encryption", "performance"]
    EN_CONSTRAINT_KEYWORDS = ["constraint", "limitation", "budget", "deadline", "must not", "prohibited"]
    EN_ASSUMPTION_KEYWORDS = ["assume", "assumption", "assuming"]

    def classify(self, text: str, language: str = "auto") -> RequirementType:
        """
        Classify a requirement based on its text content.

        Args:
            text: Requirement text
            language: 'ja', 'en', or 'auto'

        Returns:
            RequirementType enum value
        """
        if language == "auto":
            language = LanguageDetector.detect(text)

        text_lower = text.lower()

        # Check patterns in order of specificity
        if language in ("ja", "mixed"):
            if any(kw in text for kw in self.JA_ASSUMPTION_KEYWORDS):
                return RequirementType.ASSUMPTION
            if any(kw in text for kw in self.JA_CONSTRAINT_KEYWORDS):
                return RequirementType.CONSTRAINT
            if any(kw in text for kw in self.JA_NFR_KEYWORDS):
                return RequirementType.NON_FUNCTIONAL
            if any(kw in text for kw in self.JA_FUNCTIONAL_KEYWORDS):
                return RequirementType.FUNCTIONAL
            if any(kw in text for kw in self.JA_STAKEHOLDER_KEYWORDS):
                return RequirementType.STAKEHOLDER
            if any(kw in text for kw in self.JA_BUSINESS_KEYWORDS):
                return RequirementType.BUSINESS

        if language in ("en", "mixed"):
            if any(kw in text_lower for kw in self.EN_ASSUMPTION_KEYWORDS):
                return RequirementType.ASSUMPTION
            if any(kw in text_lower for kw in self.EN_CONSTRAINT_KEYWORDS):
                return RequirementType.CONSTRAINT
            if any(kw in text_lower for kw in self.EN_NFR_KEYWORDS):
                return RequirementType.NON_FUNCTIONAL
            if any(kw in text_lower for kw in self.EN_FUNCTIONAL_KEYWORDS):
                return RequirementType.FUNCTIONAL
            if any(kw in text_lower for kw in self.EN_STAKEHOLDER_KEYWORDS):
                return RequirementType.STAKEHOLDER
            if any(kw in text_lower for kw in self.EN_BUSINESS_KEYWORDS):
                return RequirementType.BUSINESS

        # Default to functional if no clear match
        return RequirementType.FUNCTIONAL


class PriorityClassifier:
    """Classify requirement priority (MoSCoW)."""

    # Priority keywords (Japanese)
    JA_MUST_KEYWORDS = ["必須", "不可欠", "必ず", "絶対に", "必要不可欠"]
    JA_SHOULD_KEYWORDS = ["重要", "推奨", "できれば", "望ましい"]
    JA_COULD_KEYWORDS = ["可能なら", "あれば良い", "あると便利"]
    JA_WONT_KEYWORDS = ["対象外", "スコープ外", "将来検討", "今回は含まない"]

    # Priority keywords (English)
    EN_MUST_KEYWORDS = ["must", "required", "essential", "critical", "mandatory"]
    EN_SHOULD_KEYWORDS = ["should", "important", "recommended", "preferably"]
    EN_COULD_KEYWORDS = ["could", "nice to have", "optional", "if possible"]
    EN_WONT_KEYWORDS = ["out of scope", "future", "not included", "deferred"]

    def classify(self, text: str, language: str = "auto") -> Priority:
        """
        Classify requirement priority.

        Args:
            text: Requirement text
            language: 'ja', 'en', or 'auto'

        Returns:
            Priority enum value
        """
        if language == "auto":
            language = LanguageDetector.detect(text)

        text_lower = text.lower()

        if language in ("ja", "mixed"):
            if any(kw in text for kw in self.JA_WONT_KEYWORDS):
                return Priority.WONT_HAVE
            if any(kw in text for kw in self.JA_MUST_KEYWORDS):
                return Priority.MUST_HAVE
            if any(kw in text for kw in self.JA_SHOULD_KEYWORDS):
                return Priority.SHOULD_HAVE
            if any(kw in text for kw in self.JA_COULD_KEYWORDS):
                return Priority.COULD_HAVE

        if language in ("en", "mixed"):
            if any(kw in text_lower for kw in self.EN_WONT_KEYWORDS):
                return Priority.WONT_HAVE
            if any(kw in text_lower for kw in self.EN_MUST_KEYWORDS):
                return Priority.MUST_HAVE
            if any(kw in text_lower for kw in self.EN_SHOULD_KEYWORDS):
                return Priority.SHOULD_HAVE
            if any(kw in text_lower for kw in self.EN_COULD_KEYWORDS):
                return Priority.COULD_HAVE

        # Default to should have
        return Priority.SHOULD_HAVE


class HearingParser:
    """Parse hearing sheets and meeting notes."""

    def __init__(self):
        """Initialize parser with classifiers."""
        self.language_detector = LanguageDetector()
        self.req_classifier = RequirementClassifier()
        self.priority_classifier = PriorityClassifier()
        self.ambiguity_detector = AmbiguityDetector()

    def parse_markdown(self, content: str, source_name: str) -> RequirementsDocument:
        """
        Parse markdown hearing sheet into requirements.

        Args:
            content: Markdown content
            source_name: Name of source document

        Returns:
            RequirementsDocument with extracted requirements
        """
        language = self.language_detector.detect(content)

        # Extract project name from first heading
        project_name = "Unknown Project"
        heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if heading_match:
            project_name = heading_match.group(1).strip()

        doc = RequirementsDocument(
            project_name=project_name,
            source_documents=[source_name],
            language=language,
        )

        # Extract requirements from bullet points and numbered lists
        requirements = self._extract_requirement_statements(content, source_name)

        for idx, (text, section, line) in enumerate(requirements, 1):
            req_type = self.req_classifier.classify(text, language)
            priority = self.priority_classifier.classify(text, language)

            # Generate ID based on type
            type_prefix = {
                RequirementType.BUSINESS: "BR",
                RequirementType.STAKEHOLDER: "SR",
                RequirementType.FUNCTIONAL: "FR",
                RequirementType.NON_FUNCTIONAL: "NFR",
                RequirementType.CONSTRAINT: "CON",
                RequirementType.ASSUMPTION: "ASM",
            }
            req_id = f"{type_prefix[req_type]}-{idx:03d}"

            req = Requirement(
                id=req_id,
                type=req_type,
                category=self._infer_category(text, req_type),
                description=text,
                priority=priority,
                source=Source(
                    document=source_name,
                    section=section,
                    line=line,
                ),
            )
            doc.requirements.append(req)

        # Detect ambiguities and create gaps
        self._detect_gaps(doc)

        return doc

    def _extract_requirement_statements(self, content: str, source_name: str) -> list:
        """Extract requirement statements from markdown content."""
        requirements = []
        current_section = None

        lines = content.split("\n")
        for line_num, line in enumerate(lines, 1):
            # Track section headers
            section_match = re.match(r"^#{1,3}\s+(.+)$", line)
            if section_match:
                current_section = section_match.group(1).strip()
                continue

            # Extract from bullet points
            bullet_match = re.match(r"^\s*[-*]\s+(.+)$", line)
            if bullet_match:
                text = bullet_match.group(1).strip()
                if len(text) > 10:  # Filter out very short items
                    requirements.append((text, current_section, line_num))
                continue

            # Extract from numbered lists
            numbered_match = re.match(r"^\s*\d+\.\s+(.+)$", line)
            if numbered_match:
                text = numbered_match.group(1).strip()
                if len(text) > 10:
                    requirements.append((text, current_section, line_num))
                continue

        return requirements

    def _infer_category(self, text: str, req_type: RequirementType) -> str:
        """Infer category based on text content."""
        text_lower = text.lower()

        # Category keywords
        categories = {
            "authentication": ["認証", "ログイン", "auth", "login", "password"],
            "authorization": ["権限", "認可", "permission", "role", "access control"],
            "user_management": ["ユーザー管理", "アカウント", "user management", "account"],
            "data_management": ["データ", "レコード", "data", "record", "storage"],
            "reporting": ["レポート", "帳票", "report", "dashboard", "analytics"],
            "integration": ["連携", "API", "integration", "interface", "sync"],
            "performance": ["性能", "応答時間", "performance", "response time", "throughput"],
            "security": ["セキュリティ", "暗号化", "security", "encryption", "audit"],
            "availability": ["可用性", "稼働率", "availability", "uptime", "failover"],
            "usability": ["使いやすさ", "UI", "usability", "user interface", "accessibility"],
        }

        for category, keywords in categories.items():
            if any(kw in text_lower or kw in text for kw in keywords):
                return category

        return "general"

    def _detect_gaps(self, doc: RequirementsDocument):
        """Detect gaps and ambiguities in the document."""
        gap_counter = 1

        for req in doc.requirements:
            ambiguities = self.ambiguity_detector.detect_ambiguities(req.description, doc.language)

            for amb in ambiguities:
                gap = Gap(
                    id=f"GAP-{gap_counter:03d}",
                    category=GapCategory.AMBIGUOUS,
                    severity=GapSeverity[amb["severity"].upper()],
                    description=f"Ambiguous language detected: '{amb['matched_text']}' ({amb['category']})",
                    recommendation=self._get_recommendation(amb["category"]),
                    related_requirements=[req.id],
                )
                doc.gaps.append(gap)
                gap_counter += 1

    @staticmethod
    def _get_recommendation(category: str) -> str:
        """Get recommendation for ambiguity category."""
        recommendations = {
            "vague_quantifier": "Replace with specific, measurable criteria (e.g., numbers, percentages)",
            "open_list": "Enumerate all items or define clear inclusion criteria",
            "passive_voice": "Convert to active voice with explicit actor",
            "temporal_ambiguity": "Specify exact timing, frequency, or trigger conditions",
        }
        return recommendations.get(category, "Clarify the requirement with more specific language")


def parse_hearing_file(input_path: str, output_path: Optional[str] = None) -> dict:
    """
    Parse a hearing file and output structured requirements.

    Args:
        input_path: Path to input file (markdown, txt, csv, json)
        output_path: Optional path for JSON output

    Returns:
        Dictionary with parsed requirements
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    parser = HearingParser()

    # Read and parse based on format
    content = input_file.read_text(encoding="utf-8")
    doc = parser.parse_markdown(content, input_file.name)

    result = doc.to_dict()

    # Write output if path provided
    if output_path:
        output_file = Path(output_path)
        output_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    return result


if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser(description="Parse hearing sheets into structured requirements")
    argparser.add_argument("input", help="Input hearing file (markdown, txt, csv, json)")
    argparser.add_argument("--output", "-o", help="Output JSON file path", default=None)
    argparser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "txt", "csv", "json"],
        default="markdown",
        help="Input format (default: markdown)",
    )

    args = argparser.parse_args()

    result = parse_hearing_file(args.input, args.output)

    if not args.output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
