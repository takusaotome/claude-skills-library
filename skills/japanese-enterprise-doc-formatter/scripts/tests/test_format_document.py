"""
Tests for format_document.py
"""

import json

import pytest
from format_document import (
    DOCUMENT_TYPE_NAMES,
    REQUIRED_SECTIONS,
    DocumentMetadata,
    DocumentSection,
    DocumentType,
    FormattedDocument,
    KeigoLevel,
    create_sample_document,
    format_date_japanese,
    format_document_markdown,
    generate_approval_table,
    generate_document_id,
    parse_document_type,
    parse_keigo_level,
    validate_sections,
)


class TestParseDocumentType:
    """Tests for parse_document_type function."""

    def test_parse_english_names(self):
        """Test parsing English document type names."""
        assert parse_document_type("ringi") == DocumentType.RINGI
        assert parse_document_type("purchase") == DocumentType.PURCHASE
        assert parse_document_type("proposal") == DocumentType.PROPOSAL
        assert parse_document_type("report") == DocumentType.REPORT
        assert parse_document_type("request") == DocumentType.REQUEST

    def test_parse_japanese_names(self):
        """Test parsing Japanese document type names."""
        assert parse_document_type("稟議書") == DocumentType.RINGI
        assert parse_document_type("稟議") == DocumentType.RINGI
        assert parse_document_type("購入申請書") == DocumentType.PURCHASE
        assert parse_document_type("提案書") == DocumentType.PROPOSAL
        assert parse_document_type("報告書") == DocumentType.REPORT
        assert parse_document_type("依頼書") == DocumentType.REQUEST

    def test_parse_case_insensitive(self):
        """Test case insensitivity."""
        assert parse_document_type("RINGI") == DocumentType.RINGI
        assert parse_document_type("Ringi") == DocumentType.RINGI
        assert parse_document_type("PURCHASE") == DocumentType.PURCHASE

    def test_parse_with_whitespace(self):
        """Test handling of whitespace."""
        assert parse_document_type("  ringi  ") == DocumentType.RINGI
        assert parse_document_type("\tproposal\n") == DocumentType.PROPOSAL

    def test_parse_invalid_type(self):
        """Test error handling for invalid types."""
        with pytest.raises(ValueError, match="Unknown document type"):
            parse_document_type("invalid")
        with pytest.raises(ValueError, match="Unknown document type"):
            parse_document_type("メモ")


class TestParseKeigoLevel:
    """Tests for parse_keigo_level function."""

    def test_parse_english_levels(self):
        """Test parsing English keigo level names."""
        assert parse_keigo_level("highest") == KeigoLevel.HIGHEST
        assert parse_keigo_level("formal") == KeigoLevel.HIGHEST
        assert parse_keigo_level("upper") == KeigoLevel.UPPER
        assert parse_keigo_level("standard") == KeigoLevel.STANDARD
        assert parse_keigo_level("basic") == KeigoLevel.BASIC

    def test_parse_japanese_levels(self):
        """Test parsing Japanese keigo level names."""
        assert parse_keigo_level("最上級") == KeigoLevel.HIGHEST
        assert parse_keigo_level("上級") == KeigoLevel.UPPER
        assert parse_keigo_level("標準") == KeigoLevel.STANDARD
        assert parse_keigo_level("基本") == KeigoLevel.BASIC

    def test_parse_invalid_level(self):
        """Test error handling for invalid levels."""
        with pytest.raises(ValueError, match="Unknown keigo level"):
            parse_keigo_level("invalid")


class TestGenerateDocumentId:
    """Tests for generate_document_id function."""

    def test_generate_ringi_id(self):
        """Test generating ringi document ID."""
        doc_id = generate_document_id(DocumentType.RINGI, 1)
        assert doc_id.startswith("RINGI-")
        assert "-001" in doc_id

    def test_generate_purchase_id(self):
        """Test generating purchase document ID."""
        doc_id = generate_document_id(DocumentType.PURCHASE, 42)
        assert doc_id.startswith("PO-")
        assert "-042" in doc_id

    def test_generate_proposal_id(self):
        """Test generating proposal document ID."""
        doc_id = generate_document_id(DocumentType.PROPOSAL, 100)
        assert doc_id.startswith("PROP-")
        assert "-100" in doc_id


class TestFormatDateJapanese:
    """Tests for format_date_japanese function."""

    def test_format_iso_date(self):
        """Test formatting ISO date to Japanese style."""
        assert format_date_japanese("2024-01-15") == "2024年1月15日"
        assert format_date_japanese("2024-12-31") == "2024年12月31日"

    def test_already_formatted(self):
        """Test handling already formatted dates."""
        assert format_date_japanese("2024年1月15日") == "2024年1月15日"

    def test_invalid_date(self):
        """Test handling invalid date strings."""
        assert format_date_japanese("invalid") == "invalid"


class TestValidateSections:
    """Tests for validate_sections function."""

    def test_all_sections_present(self):
        """Test validation when all required sections are present."""
        sections = [DocumentSection(name=s, content="test") for s in REQUIRED_SECTIONS[DocumentType.RINGI]]
        warnings = validate_sections(DocumentType.RINGI, sections)
        assert len(warnings) == 0

    def test_missing_sections(self):
        """Test validation when sections are missing."""
        sections = [
            DocumentSection(name="件名", content="test"),
            DocumentSection(name="目的", content="test"),
        ]
        warnings = validate_sections(DocumentType.RINGI, sections)
        assert len(warnings) > 0
        assert any("Missing required section" in w for w in warnings)

    def test_purchase_request_validation(self):
        """Test validation for purchase request."""
        sections = [DocumentSection(name=s, content="test") for s in REQUIRED_SECTIONS[DocumentType.PURCHASE]]
        warnings = validate_sections(DocumentType.PURCHASE, sections)
        assert len(warnings) == 0


class TestGenerateApprovalTable:
    """Tests for generate_approval_table function."""

    def test_ringi_approval_table(self):
        """Test ringi approval table generation."""
        table = generate_approval_table(DocumentType.RINGI)
        assert "課長" in table
        assert "部長" in table
        assert "本部長" in table
        assert "役員" in table

    def test_purchase_approval_table(self):
        """Test purchase approval table generation."""
        table = generate_approval_table(DocumentType.PURCHASE)
        assert "課長" in table
        assert "部長" in table
        # Should not have 役員 for purchase requests
        assert table.count("役員") == 0


class TestFormattedDocument:
    """Tests for FormattedDocument class."""

    def test_to_dict(self):
        """Test converting FormattedDocument to dictionary."""
        metadata = DocumentMetadata(
            document_type=DocumentType.RINGI,
            document_id="RINGI-2024-001",
            subject="テスト件名",
            draft_date="2024-01-15",
            drafter="山田太郎",
            department="情報システム部",
            keigo_level=KeigoLevel.HIGHEST,
            bilingual=True,
        )
        doc = FormattedDocument(
            metadata=metadata,
            sections=[DocumentSection(name="目的", content="テスト目的")],
            english_summary="Test summary",
        )

        result = doc.to_dict()

        assert result["schema_version"] == "1.0"
        assert result["document_type"] == "稟議書"
        assert result["document_id"] == "RINGI-2024-001"
        assert result["metadata"]["subject"] == "テスト件名"
        assert result["metadata"]["keigo_level"] == "highest"
        assert result["metadata"]["bilingual"] is True
        assert "目的" in result["sections"]
        assert result["english_summary"] == "Test summary"

    def test_to_dict_json_serializable(self):
        """Test that to_dict output is JSON serializable."""
        doc = create_sample_document(DocumentType.PROPOSAL)
        result = doc.to_dict()

        # Should not raise
        json_str = json.dumps(result, ensure_ascii=False)
        assert len(json_str) > 0


class TestCreateSampleDocument:
    """Tests for create_sample_document function."""

    def test_create_ringi_sample(self):
        """Test creating a sample ringi document."""
        doc = create_sample_document(DocumentType.RINGI)

        assert doc.metadata.document_type == DocumentType.RINGI
        assert doc.metadata.document_id.startswith("RINGI-")
        assert len(doc.sections) > 0

    def test_create_bilingual_sample(self):
        """Test creating a bilingual sample."""
        doc = create_sample_document(DocumentType.PROPOSAL, bilingual=True)

        assert doc.metadata.bilingual is True
        assert doc.english_summary is not None

    def test_create_with_keigo_level(self):
        """Test creating sample with specific keigo level."""
        doc = create_sample_document(DocumentType.RINGI, keigo_level=KeigoLevel.HIGHEST)

        assert doc.metadata.keigo_level == KeigoLevel.HIGHEST


class TestFormatDocumentMarkdown:
    """Tests for format_document_markdown function."""

    def test_format_basic_document(self):
        """Test basic markdown formatting."""
        doc = create_sample_document(DocumentType.RINGI)
        markdown = format_document_markdown(doc)

        assert "# 稟議書" in markdown
        assert "## 基本情報" in markdown
        assert "## 承認欄" in markdown
        assert "| 項目 | 内容 |" in markdown

    def test_format_bilingual_document(self):
        """Test bilingual document formatting."""
        doc = create_sample_document(DocumentType.PROPOSAL, bilingual=True)
        markdown = format_document_markdown(doc)

        assert "## English Summary" in markdown

    def test_format_includes_closing(self):
        """Test that markdown includes closing phrase."""
        doc = create_sample_document(DocumentType.RINGI, keigo_level=KeigoLevel.HIGHEST)
        markdown = format_document_markdown(doc)

        assert "お願い申し上げます" in markdown


class TestRequiredSections:
    """Tests for REQUIRED_SECTIONS constant."""

    def test_all_document_types_have_requirements(self):
        """Test that all document types have defined requirements."""
        for doc_type in DocumentType:
            assert doc_type in REQUIRED_SECTIONS
            assert len(REQUIRED_SECTIONS[doc_type]) > 0

    def test_ringi_has_approval_section(self):
        """Test that ringi requires approval section."""
        assert "承認欄" in REQUIRED_SECTIONS[DocumentType.RINGI]

    def test_purchase_has_cost_fields(self):
        """Test that purchase request has cost-related fields."""
        purchase_sections = REQUIRED_SECTIONS[DocumentType.PURCHASE]
        assert "単価" in purchase_sections
        assert "合計金額" in purchase_sections


class TestDocumentTypeNames:
    """Tests for DOCUMENT_TYPE_NAMES constant."""

    def test_all_types_have_japanese_names(self):
        """Test that all document types have Japanese names."""
        for doc_type in DocumentType:
            assert doc_type in DOCUMENT_TYPE_NAMES
            # Japanese names should contain Japanese characters
            name = DOCUMENT_TYPE_NAMES[doc_type]
            assert any(ord(c) > 127 for c in name)
