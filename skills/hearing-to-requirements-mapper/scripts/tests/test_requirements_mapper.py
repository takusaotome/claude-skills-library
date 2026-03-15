"""
Tests for requirements_mapper.py
"""

import json

import pytest
from requirements_mapper import (
    AmbiguityDetector,
    Gap,
    GapCategory,
    GapSeverity,
    HearingParser,
    LanguageDetector,
    Priority,
    PriorityClassifier,
    Requirement,
    RequirementClassifier,
    RequirementsDocument,
    RequirementType,
    Source,
    parse_hearing_file,
)


class TestLanguageDetector:
    """Tests for LanguageDetector class."""

    def test_detect_japanese(self):
        """Test detection of Japanese text."""
        text = "システムはユーザーのメールアドレス形式を検証する"
        assert LanguageDetector.detect(text) == "ja"

    def test_detect_english(self):
        """Test detection of English text."""
        text = "System shall validate user email address format"
        assert LanguageDetector.detect(text) == "en"

    def test_detect_mixed(self):
        """Test detection of mixed Japanese/English text."""
        text = "User authentication via OAuth 2.0 / OAuth 2.0による認証が必要"
        result = LanguageDetector.detect(text)
        assert result in ("ja", "mixed")  # Could be either depending on ratio

    def test_detect_empty_text(self):
        """Test handling of empty or numeric-only text."""
        assert LanguageDetector.detect("") == "en"
        assert LanguageDetector.detect("12345") == "en"


class TestAmbiguityDetector:
    """Tests for AmbiguityDetector class."""

    @pytest.fixture
    def detector(self):
        """Create detector instance."""
        return AmbiguityDetector()

    def test_detect_japanese_vague_quantifier(self, detector):
        """Test detection of vague quantifiers in Japanese."""
        text = "多くのユーザーがシステムを使用する"
        ambiguities = detector.detect_ambiguities(text, "ja")

        assert len(ambiguities) > 0
        assert any(a["category"] == "vague_quantifier" for a in ambiguities)
        assert any("多く" in a["matched_text"] for a in ambiguities)

    def test_detect_english_vague_quantifier(self, detector):
        """Test detection of vague quantifiers in English."""
        text = "Many users will access the system quickly"
        ambiguities = detector.detect_ambiguities(text, "en")

        assert len(ambiguities) > 0
        vague_matches = [a for a in ambiguities if a["category"] == "vague_quantifier"]
        assert len(vague_matches) >= 1

    def test_detect_open_list_japanese(self, detector):
        """Test detection of open-ended lists in Japanese."""
        text = "レポートをExcel、PDF、CSVなど"
        ambiguities = detector.detect_ambiguities(text, "ja")

        assert len(ambiguities) > 0
        assert any(a["category"] == "open_list" for a in ambiguities)

    def test_detect_open_list_english(self, detector):
        """Test detection of open-ended lists in English."""
        text = "Export to Excel, PDF, CSV, etc."
        ambiguities = detector.detect_ambiguities(text, "en")

        assert len(ambiguities) > 0
        assert any(a["category"] == "open_list" for a in ambiguities)

    def test_detect_temporal_ambiguity(self, detector):
        """Test detection of temporal ambiguity."""
        text_ja = "データは定期的にバックアップされる"
        text_en = "Data should be backed up periodically"

        ambiguities_ja = detector.detect_ambiguities(text_ja, "ja")
        ambiguities_en = detector.detect_ambiguities(text_en, "en")

        assert any(a["category"] == "temporal_ambiguity" for a in ambiguities_ja)
        assert any(a["category"] == "temporal_ambiguity" for a in ambiguities_en)

    def test_no_ambiguity_in_clear_text(self, detector):
        """Test that clear text has no ambiguities."""
        text = "応答時間は3秒以内とする"  # Clear requirement with specific metric
        ambiguities = detector.detect_ambiguities(text, "ja")

        # Should have no vague quantifier ambiguities
        assert not any(a["category"] == "vague_quantifier" for a in ambiguities)

    def test_auto_language_detection(self, detector):
        """Test auto language detection in ambiguity detection."""
        text_ja = "多くのユーザー"
        text_en = "many users"

        # Should detect language automatically
        ambiguities_ja = detector.detect_ambiguities(text_ja, "auto")
        ambiguities_en = detector.detect_ambiguities(text_en, "auto")

        assert len(ambiguities_ja) > 0
        assert len(ambiguities_en) > 0


class TestRequirementClassifier:
    """Tests for RequirementClassifier class."""

    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return RequirementClassifier()

    def test_classify_business_requirement_ja(self, classifier):
        """Test classification of Japanese business requirement."""
        text = "売上を20%向上させることが目標"
        assert classifier.classify(text, "ja") == RequirementType.BUSINESS

    def test_classify_business_requirement_en(self, classifier):
        """Test classification of English business requirement."""
        text = "Goal is to increase revenue by 20%"
        assert classifier.classify(text, "en") == RequirementType.BUSINESS

    def test_classify_functional_requirement_ja(self, classifier):
        """Test classification of Japanese functional requirement."""
        text = "システムはメールアドレス形式を検証する"
        assert classifier.classify(text, "ja") == RequirementType.FUNCTIONAL

    def test_classify_functional_requirement_en(self, classifier):
        """Test classification of English functional requirement."""
        text = "System shall validate email address format"
        assert classifier.classify(text, "en") == RequirementType.FUNCTIONAL

    def test_classify_nonfunctional_requirement(self, classifier):
        """Test classification of non-functional requirement."""
        text_ja = "応答時間は3秒以内とする"
        text_en = "Response time must be under 3 seconds"

        assert classifier.classify(text_ja, "ja") == RequirementType.NON_FUNCTIONAL
        assert classifier.classify(text_en, "en") == RequirementType.NON_FUNCTIONAL

    def test_classify_stakeholder_requirement(self, classifier):
        """Test classification of stakeholder requirement."""
        text_ja = "管理者は全ユーザーの権限を管理できる"
        text_en = "Admin must be able to manage all user permissions"

        assert classifier.classify(text_ja, "ja") == RequirementType.STAKEHOLDER
        assert classifier.classify(text_en, "en") == RequirementType.STAKEHOLDER

    def test_classify_constraint(self, classifier):
        """Test classification of constraint."""
        text_ja = "予算は5000万円以内という制約がある"
        text_en = "Budget constraint of $500,000"

        assert classifier.classify(text_ja, "ja") == RequirementType.CONSTRAINT
        assert classifier.classify(text_en, "en") == RequirementType.CONSTRAINT

    def test_classify_assumption(self, classifier):
        """Test classification of assumption."""
        text_ja = "ユーザーは安定したインターネット環境を持つと想定"
        text_en = "Assuming users have stable internet connectivity"

        assert classifier.classify(text_ja, "ja") == RequirementType.ASSUMPTION
        assert classifier.classify(text_en, "en") == RequirementType.ASSUMPTION


class TestPriorityClassifier:
    """Tests for PriorityClassifier class."""

    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return PriorityClassifier()

    def test_classify_must_have_ja(self, classifier):
        """Test classification of must-have priority in Japanese."""
        text = "セキュリティ対応は必須"
        assert classifier.classify(text, "ja") == Priority.MUST_HAVE

    def test_classify_must_have_en(self, classifier):
        """Test classification of must-have priority in English."""
        text = "Security compliance is required and mandatory"
        assert classifier.classify(text, "en") == Priority.MUST_HAVE

    def test_classify_should_have(self, classifier):
        """Test classification of should-have priority."""
        text_ja = "この機能は重要"
        text_en = "This feature is important and should be included"

        assert classifier.classify(text_ja, "ja") == Priority.SHOULD_HAVE
        assert classifier.classify(text_en, "en") == Priority.SHOULD_HAVE

    def test_classify_could_have(self, classifier):
        """Test classification of could-have priority."""
        text_ja = "可能ならこの機能も追加"
        text_en = "Nice to have if possible"

        assert classifier.classify(text_ja, "ja") == Priority.COULD_HAVE
        assert classifier.classify(text_en, "en") == Priority.COULD_HAVE

    def test_classify_wont_have(self, classifier):
        """Test classification of won't-have priority."""
        text_ja = "この機能は今回は対象外"
        text_en = "This feature is out of scope for this release"

        assert classifier.classify(text_ja, "ja") == Priority.WONT_HAVE
        assert classifier.classify(text_en, "en") == Priority.WONT_HAVE

    def test_default_priority(self, classifier):
        """Test default priority for unclear text."""
        text = "Some generic requirement"
        assert classifier.classify(text, "en") == Priority.SHOULD_HAVE


class TestHearingParser:
    """Tests for HearingParser class."""

    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return HearingParser()

    def test_parse_japanese_hearing(self, parser, sample_hearing_ja):
        """Test parsing Japanese hearing sheet."""
        doc = parser.parse_markdown(sample_hearing_ja, "hearing_ja.md")

        assert doc.project_name == "CRMシステム更新プロジェクト"
        assert doc.language == "ja"
        assert len(doc.requirements) > 0
        assert "hearing_ja.md" in doc.source_documents

    def test_parse_english_hearing(self, parser, sample_hearing_en):
        """Test parsing English hearing sheet."""
        doc = parser.parse_markdown(sample_hearing_en, "hearing_en.md")

        assert doc.project_name == "CRM System Renewal Project"
        assert doc.language == "en"
        assert len(doc.requirements) > 0

    def test_requirements_have_ids(self, parser, sample_hearing_ja):
        """Test that all requirements have unique IDs."""
        doc = parser.parse_markdown(sample_hearing_ja, "test.md")

        ids = [req.id for req in doc.requirements]
        assert len(ids) == len(set(ids))  # All unique

        # Check ID format
        for req_id in ids:
            assert req_id.startswith(("BR-", "SR-", "FR-", "NFR-", "CON-", "ASM-"))

    def test_requirements_have_source(self, parser, sample_hearing_ja):
        """Test that requirements have source information."""
        doc = parser.parse_markdown(sample_hearing_ja, "test.md")

        for req in doc.requirements:
            assert req.source is not None
            assert req.source.document == "test.md"
            assert req.source.line is not None

    def test_gap_detection(self, parser, sample_hearing_ja):
        """Test that gaps are detected."""
        doc = parser.parse_markdown(sample_hearing_ja, "test.md")

        # Should find ambiguities like "高速に" and "定期的に" and "など"
        assert len(doc.gaps) > 0
        assert any(gap.category == GapCategory.AMBIGUOUS for gap in doc.gaps)

    def test_document_summary(self, parser, sample_hearing_ja):
        """Test document summary generation."""
        doc = parser.parse_markdown(sample_hearing_ja, "test.md")
        summary = doc.generate_summary()

        assert "total_requirements" in summary
        assert "by_type" in summary
        assert "by_priority" in summary
        assert "gaps_found" in summary
        assert summary["total_requirements"] == len(doc.requirements)


class TestRequirementDataClasses:
    """Tests for data classes."""

    def test_requirement_to_dict(self):
        """Test Requirement.to_dict() method."""
        req = Requirement(
            id="FR-001",
            type=RequirementType.FUNCTIONAL,
            category="authentication",
            description="Test requirement",
            priority=Priority.MUST_HAVE,
            source=Source(document="test.md", section="1.1", line=10),
        )

        d = req.to_dict()

        assert d["id"] == "FR-001"
        assert d["type"] == "functional"
        assert d["category"] == "authentication"
        assert d["priority"] == "must_have"
        assert d["source"]["document"] == "test.md"

    def test_gap_to_dict(self):
        """Test Gap.to_dict() method."""
        gap = Gap(
            id="GAP-001",
            category=GapCategory.AMBIGUOUS,
            severity=GapSeverity.HIGH,
            description="Vague language detected",
            recommendation="Use specific metrics",
            related_requirements=["FR-001"],
        )

        d = gap.to_dict()

        assert d["id"] == "GAP-001"
        assert d["category"] == "ambiguous"
        assert d["severity"] == "high"
        assert d["related_requirements"] == ["FR-001"]

    def test_requirements_document_to_dict(self):
        """Test RequirementsDocument.to_dict() method."""
        doc = RequirementsDocument(
            project_name="Test Project",
            source_documents=["test.md"],
            language="en",
        )
        doc.requirements.append(
            Requirement(
                id="FR-001",
                type=RequirementType.FUNCTIONAL,
                category="test",
                description="Test",
            )
        )

        d = doc.to_dict()

        assert d["schema_version"] == "1.0"
        assert d["metadata"]["project_name"] == "Test Project"
        assert len(d["requirements"]) == 1
        assert d["summary"]["total_requirements"] == 1


class TestParseHearingFile:
    """Tests for parse_hearing_file function."""

    def test_parse_file(self, tmp_hearing_file):
        """Test parsing a file from path."""
        result = parse_hearing_file(str(tmp_hearing_file))

        assert result["schema_version"] == "1.0"
        assert result["metadata"]["project_name"] == "CRMシステム更新プロジェクト"
        assert len(result["requirements"]) > 0

    def test_parse_file_with_output(self, tmp_hearing_file, tmp_path):
        """Test parsing with output file."""
        output_path = tmp_path / "output.json"
        result = parse_hearing_file(str(tmp_hearing_file), str(output_path))

        assert output_path.exists()

        with open(output_path, "r", encoding="utf-8") as f:
            saved_result = json.load(f)

        assert saved_result["schema_version"] == "1.0"
        assert saved_result == result

    def test_parse_nonexistent_file(self, tmp_path):
        """Test error handling for non-existent file."""
        with pytest.raises(FileNotFoundError):
            parse_hearing_file(str(tmp_path / "nonexistent.md"))
