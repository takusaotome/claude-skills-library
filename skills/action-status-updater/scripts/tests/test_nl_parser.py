"""
Tests for the natural language parser module.
"""

import pytest
from nl_parser import (
    Intent,
    Language,
    detect_intent,
    detect_language,
    extract_channel,
    extract_person,
    parse_status_update,
)


class TestDetectLanguage:
    """Tests for language detection."""

    def test_japanese_hiragana(self):
        """Test detection of Japanese with hiragana."""
        assert detect_language("返信した") == Language.JAPANESE

    def test_japanese_kanji(self):
        """Test detection of Japanese with kanji."""
        assert detect_language("完了") == Language.JAPANESE

    def test_japanese_mixed(self):
        """Test detection of Japanese with mixed characters."""
        assert detect_language("Seanのメールには返信しておいた") == Language.JAPANESE

    def test_english_simple(self):
        """Test detection of English."""
        assert detect_language("Done") == Language.ENGLISH

    def test_english_sentence(self):
        """Test detection of English sentence."""
        assert detect_language("Delegated the task to Mike") == Language.ENGLISH

    def test_empty_string(self):
        """Test handling of empty string."""
        assert detect_language("") == Language.UNKNOWN


class TestDetectIntent:
    """Tests for intent detection."""

    def test_japanese_completed_replied(self):
        """Test Japanese completed intent - replied."""
        intent, confidence = detect_intent("返信した", Language.JAPANESE)
        assert intent == Intent.COMPLETED
        assert confidence > 0.8

    def test_japanese_completed_done(self):
        """Test Japanese completed intent - done."""
        intent, confidence = detect_intent("完了", Language.JAPANESE)
        assert intent == Intent.COMPLETED
        assert confidence > 0.9

    def test_japanese_delegated(self):
        """Test Japanese delegated intent."""
        intent, confidence = detect_intent("田中さんに依頼した", Language.JAPANESE)
        assert intent == Intent.DELEGATED
        assert confidence > 0.8

    def test_japanese_deferred(self):
        """Test Japanese deferred intent."""
        intent, confidence = detect_intent("来週対応する", Language.JAPANESE)
        assert intent == Intent.DEFERRED
        assert confidence > 0.7

    def test_japanese_in_progress(self):
        """Test Japanese in-progress intent."""
        intent, confidence = detect_intent("対応中", Language.JAPANESE)
        assert intent == Intent.IN_PROGRESS
        assert confidence > 0.8

    def test_english_completed_done(self):
        """Test English completed intent - done."""
        intent, confidence = detect_intent("Done", Language.ENGLISH)
        assert intent == Intent.COMPLETED
        assert confidence > 0.8

    def test_english_completed_finished(self):
        """Test English completed intent - finished."""
        intent, confidence = detect_intent("Task finished", Language.ENGLISH)
        assert intent == Intent.COMPLETED
        assert confidence > 0.8

    def test_english_delegated(self):
        """Test English delegated intent."""
        intent, confidence = detect_intent("Delegated to Mike", Language.ENGLISH)
        assert intent == Intent.DELEGATED
        assert confidence > 0.8

    def test_english_deferred(self):
        """Test English deferred intent."""
        intent, confidence = detect_intent("Postponed to next week", Language.ENGLISH)
        assert intent == Intent.DEFERRED
        assert confidence > 0.7

    def test_english_in_progress(self):
        """Test English in-progress intent."""
        intent, confidence = detect_intent("Working on it", Language.ENGLISH)
        assert intent == Intent.IN_PROGRESS
        assert confidence > 0.8

    def test_unknown_intent(self):
        """Test unknown intent for ambiguous input."""
        intent, confidence = detect_intent("hello world", Language.ENGLISH)
        assert intent == Intent.UNKNOWN
        assert confidence == 0.0


class TestExtractPerson:
    """Tests for person name extraction."""

    def test_japanese_san_suffix(self):
        """Test extraction with さん suffix."""
        person = extract_person("田中さんのメール", Language.JAPANESE)
        assert person == "田中"

    def test_japanese_no_email(self):
        """Test extraction from email context."""
        person = extract_person("Seanのメール", Language.JAPANESE)
        assert person == "Sean"

    def test_english_to_preposition(self):
        """Test extraction with 'to' preposition."""
        person = extract_person("Sent reply to Mike", Language.ENGLISH)
        assert person == "Mike"

    def test_english_possessive(self):
        """Test extraction with possessive."""
        person = extract_person("Sean's email", Language.ENGLISH)
        assert person == "Sean"


class TestExtractChannel:
    """Tests for channel extraction."""

    def test_japanese_email(self):
        """Test Japanese email channel detection."""
        assert extract_channel("メール返信した") == "email"

    def test_japanese_slack(self):
        """Test Japanese Slack channel detection."""
        assert extract_channel("Slackで連絡した") == "slack"

    def test_english_email(self):
        """Test English email channel detection."""
        assert extract_channel("Replied to email") == "email"

    def test_english_meeting(self):
        """Test English meeting channel detection."""
        assert extract_channel("Discussed in meeting") == "meeting"

    def test_no_channel(self):
        """Test when no channel is detected."""
        assert extract_channel("Done") is None


class TestParseStatusUpdate:
    """Integration tests for full parsing."""

    def test_japanese_email_reply_completed(self):
        """Test parsing Japanese email reply completion."""
        result = parse_status_update("Seanのメールには返信しておいた")

        assert result.intent == Intent.COMPLETED
        assert result.language == Language.JAPANESE
        assert result.person == "Sean"
        assert result.channel == "email"
        assert result.confidence > 0.8

    def test_japanese_delegation(self):
        """Test parsing Japanese delegation."""
        result = parse_status_update("Lu対応予定")

        assert result.intent == Intent.DELEGATED
        assert result.language == Language.JAPANESE

    def test_english_delegation_to_mike(self):
        """Test parsing English delegation."""
        result = parse_status_update("Delegated the report to Mike")

        assert result.intent == Intent.DELEGATED
        assert result.language == Language.ENGLISH
        assert result.delegatee == "Mike"
        assert result.confidence > 0.8

    def test_english_simple_done(self):
        """Test parsing simple English done."""
        result = parse_status_update("Done")

        assert result.intent == Intent.COMPLETED
        assert result.language == Language.ENGLISH
        assert result.confidence > 0.8

    def test_raw_input_preserved(self):
        """Test that raw input is preserved."""
        input_text = "Task completed successfully"
        result = parse_status_update(input_text)

        assert result.raw_input == input_text

    def test_japanese_deferred_next_week(self):
        """Test parsing Japanese deferral to next week."""
        result = parse_status_update("田中さんの件は来週対応")

        assert result.intent == Intent.DEFERRED
        assert result.language == Language.JAPANESE
        assert result.person == "田中"
        assert result.confidence > 0.7

    def test_english_working_on(self):
        """Test parsing English in-progress."""
        result = parse_status_update("Working on the proposal")

        assert result.intent == Intent.IN_PROGRESS
        assert result.language == Language.ENGLISH
        assert result.confidence > 0.8
        assert "proposal" in result.keywords
