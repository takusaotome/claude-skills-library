"""
Tests for validate_sections.py
"""

import pytest
from validate_sections import (
    REQUIRED_SECTIONS,
    SECTION_ALIASES,
    DocumentType,
    DocumentValidationResult,
    SectionValidationResult,
    extract_sections_from_markdown,
    find_section,
    format_validation_report,
    parse_document_type,
    validate_document,
)


class TestParseDocumentType:
    """Tests for parse_document_type function."""

    def test_parse_english_types(self):
        """Test parsing English document type names."""
        assert parse_document_type("ringi") == DocumentType.RINGI
        assert parse_document_type("purchase") == DocumentType.PURCHASE
        assert parse_document_type("proposal") == DocumentType.PROPOSAL
        assert parse_document_type("report") == DocumentType.REPORT
        assert parse_document_type("request") == DocumentType.REQUEST

    def test_parse_japanese_types(self):
        """Test parsing Japanese document type names."""
        assert parse_document_type("稟議書") == DocumentType.RINGI
        assert parse_document_type("購入申請書") == DocumentType.PURCHASE
        assert parse_document_type("提案書") == DocumentType.PROPOSAL
        assert parse_document_type("報告書") == DocumentType.REPORT
        assert parse_document_type("依頼書") == DocumentType.REQUEST

    def test_parse_short_japanese_forms(self):
        """Test parsing short Japanese forms."""
        assert parse_document_type("稟議") == DocumentType.RINGI
        assert parse_document_type("購入申請") == DocumentType.PURCHASE
        assert parse_document_type("提案") == DocumentType.PROPOSAL
        assert parse_document_type("報告") == DocumentType.REPORT
        assert parse_document_type("依頼") == DocumentType.REQUEST

    def test_parse_invalid_type(self):
        """Test error handling for invalid types."""
        with pytest.raises(ValueError, match="Unknown document type"):
            parse_document_type("invalid")


class TestExtractSectionsFromMarkdown:
    """Tests for extract_sections_from_markdown function."""

    def test_extract_h2_headers(self):
        """Test extraction of H2 headers."""
        content = """
# Document Title

## 目的

Content here.

## 背景

More content.
"""
        sections = extract_sections_from_markdown(content)

        assert "目的" in sections
        assert "背景" in sections

    def test_extract_h3_headers(self):
        """Test extraction of H3 headers."""
        content = """
## Main Section

### 詳細

Content.

### 補足

More content.
"""
        sections = extract_sections_from_markdown(content)

        assert "詳細" in sections
        assert "補足" in sections

    def test_extract_numbered_headers(self):
        """Test extraction of numbered headers."""
        content = """
## 1. 目的

Content.

## 2. 背景

Content.

## 3. 効果

Content.
"""
        sections = extract_sections_from_markdown(content)

        assert "目的" in sections
        assert "背景" in sections
        assert "効果" in sections

    def test_extract_from_empty_content(self):
        """Test extraction from empty content."""
        sections = extract_sections_from_markdown("")

        assert sections == []


class TestFindSection:
    """Tests for find_section function."""

    def test_find_direct_match(self):
        """Test finding section by direct name match."""
        found_sections = ["目的", "背景", "効果"]

        assert find_section("目的", found_sections) == "目的"
        assert find_section("背景", found_sections) == "背景"

    def test_find_by_alias(self):
        """Test finding section by alias."""
        found_sections = ["Purpose", "Background"]

        # "目的" should match "Purpose" alias
        result = find_section("目的", found_sections)
        assert result == "Purpose"

    def test_find_not_found(self):
        """Test when section is not found."""
        found_sections = ["目的", "背景"]

        assert find_section("リスク", found_sections) is None
        assert find_section("費用", found_sections) is None

    def test_find_partial_match(self):
        """Test finding section by partial match."""
        found_sections = ["1. 目的について", "2. 背景説明"]

        assert find_section("目的", found_sections) is not None
        assert find_section("背景", found_sections) is not None


class TestValidateDocument:
    """Tests for validate_document function."""

    def test_validate_complete_ringi(self):
        """Test validation of complete ringi document."""
        content = """
# 稟議書

## 基本情報

| 項目 | 内容 |
|------|------|
| 件名 | テスト |
| 起案日 | 2024-01-01 |
| 起案者 | 山田太郎 |
| 起案部署 | IT部 |
| 決裁期限 | 2024-01-15 |

## 目的

テスト目的

## 背景

テスト背景

## 内容

テスト内容

## 効果

テスト効果

## リスク

テストリスク

## 費用

テスト費用

## 承認欄

| 役職 | 氏名 |
|------|------|
"""
        result = validate_document(content, DocumentType.RINGI)

        assert result.is_valid is True
        assert result.completeness_score == 100.0
        assert len(result.missing_required) == 0

    def test_validate_incomplete_document(self):
        """Test validation of incomplete document."""
        content = """
# 稟議書

## 目的

テスト目的

## 背景

テスト背景
"""
        result = validate_document(content, DocumentType.RINGI)

        assert result.is_valid is False
        assert result.completeness_score < 100.0
        assert len(result.missing_required) > 0

    def test_validate_purchase_request(self):
        """Test validation of purchase request."""
        content = """
# 購入申請書

## 件名

テスト購入

## 申請日

2024-01-01

## 申請者

山田太郎

## 品名

テスト商品

## 数量

10

## 単価

1000

## 合計金額

10000

## 購入先

テスト会社

## 購入理由

テスト理由

## 希望納期

2024-02-01
"""
        result = validate_document(content, DocumentType.PURCHASE)

        assert result.is_valid is True

    def test_validate_with_aliases(self):
        """Test validation recognizes aliases."""
        content = """
# Proposal

## Subject

Test subject

## Purpose

Test purpose
"""
        result = validate_document(content, DocumentType.PROPOSAL)

        # Should recognize English aliases
        found_names = [s.section_name for s in result.sections if s.found]
        # At least some sections should be found via aliases
        assert len(result.found_sections) > 0


class TestDocumentValidationResult:
    """Tests for DocumentValidationResult class."""

    def test_to_dict(self):
        """Test converting result to dictionary."""
        result = DocumentValidationResult(
            document_type=DocumentType.RINGI,
            sections=[
                SectionValidationResult(section_name="目的", found=True, is_required=True),
                SectionValidationResult(section_name="リスク", found=False, is_required=True),
            ],
            missing_required=["リスク"],
            missing_optional=[],
            found_sections=["目的"],
            completeness_score=50.0,
            is_valid=False,
        )

        dict_result = result.to_dict()

        assert dict_result["document_type"] == "ringi"
        assert dict_result["validation_result"]["is_valid"] is False
        assert dict_result["validation_result"]["completeness_score"] == 50.0
        assert "リスク" in dict_result["sections"]["missing_required"]


class TestFormatValidationReport:
    """Tests for format_validation_report function."""

    def test_format_valid_document(self):
        """Test formatting report for valid document."""
        result = DocumentValidationResult(
            document_type=DocumentType.RINGI,
            sections=[],
            missing_required=[],
            missing_optional=[],
            found_sections=["目的", "背景"],
            completeness_score=100.0,
            is_valid=True,
        )

        report = format_validation_report(result)

        assert "PASS" in report
        assert "100.0%" in report

    def test_format_invalid_document(self):
        """Test formatting report for invalid document."""
        result = DocumentValidationResult(
            document_type=DocumentType.RINGI,
            sections=[
                SectionValidationResult(section_name="目的", found=True, is_required=True),
                SectionValidationResult(section_name="リスク", found=False, is_required=True),
            ],
            missing_required=["リスク"],
            missing_optional=[],
            found_sections=["目的"],
            completeness_score=50.0,
            is_valid=False,
        )

        report = format_validation_report(result)

        assert "FAIL" in report
        assert "Missing Required Sections" in report
        assert "リスク" in report


class TestRequiredSections:
    """Tests for REQUIRED_SECTIONS constant."""

    def test_all_document_types_defined(self):
        """Test that all document types have required sections."""
        for doc_type in DocumentType:
            assert doc_type in REQUIRED_SECTIONS
            assert "required" in REQUIRED_SECTIONS[doc_type]
            assert "optional" in REQUIRED_SECTIONS[doc_type]

    def test_ringi_required_sections(self):
        """Test ringi required sections."""
        ringi_required = REQUIRED_SECTIONS[DocumentType.RINGI]["required"]

        assert "件名" in ringi_required
        assert "目的" in ringi_required
        assert "背景" in ringi_required
        assert "効果" in ringi_required
        assert "リスク" in ringi_required
        assert "費用" in ringi_required
        assert "承認欄" in ringi_required

    def test_purchase_required_sections(self):
        """Test purchase request required sections."""
        purchase_required = REQUIRED_SECTIONS[DocumentType.PURCHASE]["required"]

        assert "品名" in purchase_required
        assert "数量" in purchase_required
        assert "単価" in purchase_required
        assert "合計金額" in purchase_required


class TestSectionAliases:
    """Tests for SECTION_ALIASES constant."""

    def test_key_sections_have_aliases(self):
        """Test that key sections have aliases defined."""
        assert "件名" in SECTION_ALIASES
        assert "目的" in SECTION_ALIASES
        assert "背景" in SECTION_ALIASES
        assert "費用" in SECTION_ALIASES

    def test_aliases_include_english(self):
        """Test that aliases include English alternatives."""
        purpose_aliases = SECTION_ALIASES.get("目的", [])
        assert "Purpose" in purpose_aliases

        background_aliases = SECTION_ALIASES.get("背景", [])
        assert "Background" in background_aliases

    def test_aliases_are_lists(self):
        """Test that all aliases are lists."""
        for section, aliases in SECTION_ALIASES.items():
            assert isinstance(aliases, list)
            assert len(aliases) > 0


class TestIntegration:
    """Integration tests for section validation."""

    def test_full_validation_workflow(self):
        """Test complete validation workflow."""
        # Create a document with some missing sections
        content = """
# 稟議書

## 目的

新システム導入

## 背景

現状の課題

## 費用

100万円

## 承認欄

| 役職 | 氏名 |
"""
        result = validate_document(content, DocumentType.RINGI)

        # Should identify missing sections
        assert not result.is_valid
        assert len(result.missing_required) > 0
        assert result.completeness_score > 0
        assert result.completeness_score < 100

        # Format and verify report
        report = format_validation_report(result)
        assert "Missing Required Sections" in report

    def test_validation_with_mixed_languages(self):
        """Test validation with mixed Japanese/English content."""
        content = """
# Proposal Document

## Purpose

Test purpose

## Background

Test background

## 提案内容

Proposal details

## Expected Benefits

Expected benefits

## 実施計画

Implementation plan

## Resources Required

Resource details
"""
        result = validate_document(content, DocumentType.PROPOSAL)

        # Should recognize both Japanese and English sections
        assert len(result.found_sections) > 0
        # Should have reasonable completeness
        assert result.completeness_score > 0
