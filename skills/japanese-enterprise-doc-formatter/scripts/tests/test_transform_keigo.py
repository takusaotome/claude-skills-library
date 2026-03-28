"""
Tests for transform_keigo.py
"""

import pytest
from transform_keigo import (
    CLOSING_TEMPLATES,
    TRANSFORMATION_RULES,
    VERB_TRANSFORMATIONS,
    KeigoLevel,
    TransformationResult,
    TransformationRule,
    apply_transformation_rules,
    detect_keigo_issues,
    get_closing_phrase,
    get_level_hierarchy,
    parse_keigo_level,
    transform_text,
    transform_verb_humble,
    transform_verb_respectful,
)


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

    def test_parse_case_insensitive(self):
        """Test case insensitivity."""
        assert parse_keigo_level("HIGHEST") == KeigoLevel.HIGHEST
        assert parse_keigo_level("Standard") == KeigoLevel.STANDARD

    def test_parse_invalid_level(self):
        """Test error handling for invalid levels."""
        with pytest.raises(ValueError, match="Unknown keigo level"):
            parse_keigo_level("invalid")


class TestGetLevelHierarchy:
    """Tests for get_level_hierarchy function."""

    def test_hierarchy_order(self):
        """Test that hierarchy levels are correctly ordered."""
        assert get_level_hierarchy(KeigoLevel.BASIC) < get_level_hierarchy(KeigoLevel.STANDARD)
        assert get_level_hierarchy(KeigoLevel.STANDARD) < get_level_hierarchy(KeigoLevel.UPPER)
        assert get_level_hierarchy(KeigoLevel.UPPER) < get_level_hierarchy(KeigoLevel.HIGHEST)

    def test_hierarchy_values(self):
        """Test specific hierarchy values."""
        assert get_level_hierarchy(KeigoLevel.BASIC) == 1
        assert get_level_hierarchy(KeigoLevel.STANDARD) == 2
        assert get_level_hierarchy(KeigoLevel.UPPER) == 3
        assert get_level_hierarchy(KeigoLevel.HIGHEST) == 4


class TestVerbTransformations:
    """Tests for verb transformation functions."""

    def test_transform_verb_humble(self):
        """Test humble verb transformations."""
        assert transform_verb_humble("いる") == "おる"
        assert transform_verb_humble("行く") == "参る"
        assert transform_verb_humble("言う") == "申す"
        assert transform_verb_humble("見る") == "拝見する"
        assert transform_verb_humble("する") == "いたす"

    def test_transform_verb_humble_unknown(self):
        """Test humble transformation for unknown verbs."""
        assert transform_verb_humble("unknown") is None
        assert transform_verb_humble("走る") is None

    def test_transform_verb_respectful(self):
        """Test respectful verb transformations."""
        assert transform_verb_respectful("いる") == "いらっしゃる"
        assert transform_verb_respectful("言う") == "おっしゃる"
        assert transform_verb_respectful("見る") == "ご覧になる"
        assert transform_verb_respectful("する") == "なさる"

    def test_transform_verb_respectful_unknown(self):
        """Test respectful transformation for unknown verbs."""
        assert transform_verb_respectful("unknown") is None


class TestApplyTransformationRules:
    """Tests for apply_transformation_rules function."""

    def test_transform_to_highest(self):
        """Test transformation to highest keigo level."""
        text = "報告します"
        transformed, applied = apply_transformation_rules(text, KeigoLevel.HIGHEST)

        # Should contain more formal ending
        assert "させていただきます" in transformed or "いたします" in transformed

    def test_transform_to_standard(self):
        """Test transformation to standard keigo level."""
        text = "報告する"
        transformed, applied = apply_transformation_rules(text, KeigoLevel.STANDARD)

        assert "します" in transformed

    def test_no_transformation_needed(self):
        """Test when no transformation is needed."""
        text = "これは完全に別のテキストです"
        transformed, applied = apply_transformation_rules(text, KeigoLevel.BASIC)

        # May or may not have transformations depending on content
        assert isinstance(transformed, str)
        assert isinstance(applied, list)


class TestDetectKeigoIssues:
    """Tests for detect_keigo_issues function."""

    def test_detect_informal_in_formal(self):
        """Test detection of informal endings in formal context."""
        text = "報告します。"
        warnings = detect_keigo_issues(text, KeigoLevel.HIGHEST)

        # Should suggest more formal alternatives
        assert any("いたします" in w or "させていただきます" in w for w in warnings)

    def test_detect_double_honorific(self):
        """Test detection of double honorifics."""
        text = "お読みになられました"
        warnings = detect_keigo_issues(text, KeigoLevel.STANDARD)

        assert any("Double honorific" in w for w in warnings)

    def test_no_issues_in_basic(self):
        """Test that basic level doesn't flag informal endings."""
        text = "報告します。"
        warnings = detect_keigo_issues(text, KeigoLevel.BASIC)

        # Basic level should not warn about informal endings
        assert len(warnings) == 0


class TestTransformText:
    """Tests for transform_text function."""

    def test_transform_returns_result_object(self):
        """Test that transform_text returns proper result object."""
        result = transform_text("テスト文章です", KeigoLevel.STANDARD)

        assert isinstance(result, TransformationResult)
        assert result.original_text == "テスト文章です"
        assert isinstance(result.transformed_text, str)
        assert result.target_level == KeigoLevel.STANDARD
        assert isinstance(result.transformations_applied, list)
        assert isinstance(result.warnings, list)

    def test_transform_preserves_content(self):
        """Test that transformation doesn't lose content."""
        original = "これは重要な報告です。承認をお願いします。"
        result = transform_text(original, KeigoLevel.UPPER)

        # Key content should be preserved
        assert "報告" in result.transformed_text
        assert "承認" in result.transformed_text


class TestGetClosingPhrase:
    """Tests for get_closing_phrase function."""

    def test_highest_closing(self):
        """Test closing phrase for highest level."""
        phrase = get_closing_phrase(KeigoLevel.HIGHEST)

        assert "お願い申し上げます" in phrase

    def test_standard_closing(self):
        """Test closing phrase for standard level."""
        phrase = get_closing_phrase(KeigoLevel.STANDARD)

        assert "お願いいたします" in phrase or "よろしく" in phrase

    def test_basic_closing(self):
        """Test closing phrase for basic level."""
        phrase = get_closing_phrase(KeigoLevel.BASIC)

        assert "お願いします" in phrase

    def test_closing_index_wraps(self):
        """Test that closing phrase index wraps around."""
        phrase1 = get_closing_phrase(KeigoLevel.HIGHEST, 0)
        phrase2 = get_closing_phrase(KeigoLevel.HIGHEST, 100)

        # Should not raise and should return valid phrases
        assert len(phrase1) > 0
        assert len(phrase2) > 0


class TestTransformationRules:
    """Tests for TRANSFORMATION_RULES constant."""

    def test_rules_have_required_fields(self):
        """Test that all rules have required fields."""
        for rule in TRANSFORMATION_RULES:
            assert isinstance(rule.pattern, str)
            assert isinstance(rule.replacement, str)
            assert isinstance(rule.level, KeigoLevel)
            assert isinstance(rule.category, str)
            assert rule.category in ["尊敬語", "謙譲語", "丁寧語"]

    def test_rules_cover_all_levels(self):
        """Test that rules exist for all keigo levels."""
        levels_covered = {rule.level for rule in TRANSFORMATION_RULES}

        assert KeigoLevel.HIGHEST in levels_covered
        assert KeigoLevel.UPPER in levels_covered
        assert KeigoLevel.STANDARD in levels_covered
        assert KeigoLevel.BASIC in levels_covered


class TestVerbTransformationsData:
    """Tests for VERB_TRANSFORMATIONS constant."""

    def test_humble_transformations_exist(self):
        """Test that humble transformations are defined."""
        assert "humble" in VERB_TRANSFORMATIONS
        humble = VERB_TRANSFORMATIONS["humble"]

        assert len(humble) > 0
        assert "する" in humble
        assert "言う" in humble

    def test_respectful_transformations_exist(self):
        """Test that respectful transformations are defined."""
        assert "respectful" in VERB_TRANSFORMATIONS
        respectful = VERB_TRANSFORMATIONS["respectful"]

        assert len(respectful) > 0
        assert "する" in respectful
        assert "言う" in respectful


class TestClosingTemplates:
    """Tests for CLOSING_TEMPLATES constant."""

    def test_all_levels_have_templates(self):
        """Test that all keigo levels have closing templates."""
        for level in KeigoLevel:
            assert level in CLOSING_TEMPLATES
            assert len(CLOSING_TEMPLATES[level]) > 0

    def test_templates_are_japanese(self):
        """Test that templates contain Japanese text."""
        for level, templates in CLOSING_TEMPLATES.items():
            for template in templates:
                # Should contain Japanese characters
                assert any(ord(c) > 127 for c in template)
                # Should end with proper punctuation
                assert template.endswith("。")


class TestIntegration:
    """Integration tests for keigo transformation."""

    def test_full_transformation_workflow(self):
        """Test complete transformation workflow."""
        # Start with informal text
        original = "報告する。承認をお願いする。"

        # Transform to highest level
        result = transform_text(original, KeigoLevel.HIGHEST)

        # Should have more formal language
        assert "させていただき" in result.transformed_text or "いたします" in result.transformed_text

        # Should track transformations
        assert len(result.transformations_applied) > 0

    def test_level_appropriate_output(self):
        """Test that output matches requested level."""
        text = "報告します"

        # Highest level should be most formal
        highest_result = transform_text(text, KeigoLevel.HIGHEST)

        # Basic level should be least formal
        basic_result = transform_text(text, KeigoLevel.BASIC)

        # Highest should have more or equal transformations
        assert len(highest_result.transformations_applied) >= len(basic_result.transformations_applied)
