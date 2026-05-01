#!/usr/bin/env python3
"""
Natural Language Parser for Action Status Updates.

Parses natural language status updates in Japanese and English
to extract intent, person, channel, and description keywords.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Intent(Enum):
    """Action item status intents."""

    COMPLETED = "completed"
    DELEGATED = "delegated"
    DEFERRED = "deferred"
    IN_PROGRESS = "in_progress"
    UNKNOWN = "unknown"


class Language(Enum):
    """Detected language of input."""

    JAPANESE = "ja"
    ENGLISH = "en"
    UNKNOWN = "unknown"


@dataclass
class ParseResult:
    """Result of parsing a natural language status update."""

    intent: Intent
    language: Language
    person: Optional[str] = None
    delegatee: Optional[str] = None
    channel: Optional[str] = None
    keywords: Optional[list[str]] = None
    confidence: float = 0.0
    raw_input: str = ""


# Japanese patterns
JP_COMPLETED_PATTERNS = [
    (r"返信し(た|ておいた|済み)", 0.9),
    (r"完了(した)?", 0.95),
    (r"済(み|んだ)", 0.85),
    (r"終わ(った|らせた)", 0.85),
    (r"送(った|信した)", 0.8),
    (r"対応(した|完了)", 0.9),
    (r"やっ(た|ておいた)", 0.75),
    (r"片付けた", 0.85),
    (r"処理した", 0.85),
]

JP_DELEGATED_PATTERNS = [
    (r"(.+?)に依頼(した)?", 0.9),
    (r"(.+?)にお願い(した)?", 0.85),
    (r"(.+?)に任せた", 0.9),
    (r"(.+?)に振った", 0.8),
    (r"(.+?)対応予定", 0.7),
]

JP_DEFERRED_PATTERNS = [
    (r"延期(した)?", 0.9),
    (r"来週", 0.8),
    (r"来月", 0.8),
    (r"(後|あと)で", 0.7),
    (r"保留(中)?", 0.85),
    (r"ペンディング", 0.85),
    (r"先送り", 0.85),
]

JP_IN_PROGRESS_PATTERNS = [
    (r"(対応|進行|作業|確認|検討)中", 0.9),
    (r"やって(る|いる)", 0.8),
    (r"取り組み中", 0.85),
]

# English patterns
EN_COMPLETED_PATTERNS = [
    (r"\b(done|finished|completed)\b", 0.9),
    (r"\b(sent|replied|responded)\b", 0.85),
    (r"\b(handled|resolved|fixed)\b", 0.85),
    (r"\b(closed|wrapped\s*up)\b", 0.8),
    (r"took\s+care\s+of", 0.85),
]

EN_DELEGATED_PATTERNS = [
    (r"\b(delegated|assigned)\b.*\bto\s+(\w+)", 0.9),
    (r"handed\s+off\s+to\s+(\w+)", 0.85),
    (r"passed\s+to\s+(\w+)", 0.8),
    (r"asked\s+(\w+)\s+to", 0.75),
]

EN_DEFERRED_PATTERNS = [
    (r"\b(postponed|deferred)\b", 0.9),
    (r"next\s+(week|month)", 0.8),
    (r"\blater\b", 0.7),
    (r"on\s+hold", 0.85),
    (r"pushed\s+back", 0.8),
    (r"put\s+off", 0.8),
]

EN_IN_PROGRESS_PATTERNS = [
    (r"working\s+on", 0.85),
    (r"in\s+progress", 0.9),
    (r"\b(handling|addressing)\b", 0.8),
    (r"\b(reviewing|looking\s+into)\b", 0.75),
    (r"\b(started|began)\b", 0.7),
]

# Person extraction patterns
JP_PERSON_PATTERNS = [
    r"(\w+)さん",
    r"(\w+)の(メール|Slack|件|slack)",
    r"(\w+)に(返信|連絡|依頼)",
]

EN_PERSON_PATTERNS = [
    r"to\s+([A-Z][a-z]+)",
    r"from\s+([A-Z][a-z]+)",
    r"([A-Z][a-z]+)'s\s+(email|message|request|mail)",
    r"([A-Z][a-z]+)\s+handled",
]

# Channel detection
CHANNEL_PATTERNS = {
    "email": [r"メール", r"Eメール", r"\bemail\b", r"\bmail\b"],
    "slack": [r"Slack", r"スラック", r"\bslack\b", r"\bDM\b"],
    "meeting": [r"会議", r"ミーティング", r"MTG", r"\bmeeting\b", r"\bcall\b"],
    "teams": [r"Teams", r"チームズ", r"\bteams\b"],
    "phone": [r"電話", r"\bphone\b"],
    "chat": [r"チャット", r"\bchat\b", r"\bmessage\b"],
}


def detect_language(text: str) -> Language:
    """Detect if text is primarily Japanese or English."""
    # Check for Japanese characters (hiragana, katakana, kanji)
    jp_pattern = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]")
    jp_matches = len(jp_pattern.findall(text))

    # Check for English words
    en_pattern = re.compile(r"\b[a-zA-Z]+\b")
    en_matches = len(en_pattern.findall(text))

    if jp_matches > 0 and jp_matches >= en_matches:
        return Language.JAPANESE
    elif en_matches > 0:
        return Language.ENGLISH
    return Language.UNKNOWN


def extract_person(text: str, language: Language) -> Optional[str]:
    """Extract person name from text."""
    patterns = JP_PERSON_PATTERNS if language == Language.JAPANESE else EN_PERSON_PATTERNS

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def extract_delegatee(text: str, language: Language) -> Optional[str]:
    """Extract delegatee name from delegation updates."""
    if language == Language.JAPANESE:
        patterns = [
            r"(.+?)に(依頼|お願い|任せ|振っ)",
            r"(.+?)(担当|対応予定)",
        ]
    else:
        patterns = [
            r"\b(delegated|assigned)\b.*\bto\s+(\w+)",
            r"handed\s+off\s+to\s+(\w+)",
            r"passed\s+to\s+(\w+)",
        ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Get the appropriate group based on pattern structure
            groups = match.groups()
            if language == Language.JAPANESE:
                name = groups[0]
                # Clean up Japanese name (remove さん suffix if present)
                name = re.sub(r"さん$", "", name)
                return name.strip()
            else:
                # For English, delegatee is usually in the last group
                return groups[-1] if groups else None

    return None


def extract_channel(text: str) -> Optional[str]:
    """Extract communication channel from text."""
    text_lower = text.lower()

    for channel, patterns in CHANNEL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return channel

    return None


def extract_keywords(text: str, language: Language) -> list[str]:
    """Extract meaningful keywords for description matching."""
    # Remove common particles and connectors
    if language == Language.JAPANESE:
        # Remove Japanese particles
        cleaned = re.sub(r"[はがのにをでとへやか]", " ", text)
        # Remove common verbs and auxiliary verbs
        cleaned = re.sub(r"(した|しておいた|する|やった|いる|ある|ない)", "", cleaned)
    else:
        # Remove common English words
        stopwords = {"the", "a", "an", "to", "for", "of", "with", "on", "in", "is", "was", "are", "were"}
        words = text.lower().split()
        words = [w for w in words if w not in stopwords]
        cleaned = " ".join(words)

    # Extract remaining meaningful tokens
    if language == Language.JAPANESE:
        # Extract katakana and remaining kanji compounds
        keywords = re.findall(r"[\u30A0-\u30FF]+|[\u4E00-\u9FFF]+", cleaned)
    else:
        # Extract English words
        keywords = re.findall(r"\b[a-zA-Z]{3,}\b", cleaned)

    return keywords


def detect_intent(text: str, language: Language) -> tuple[Intent, float]:
    """Detect the intent of a status update."""
    best_intent = Intent.UNKNOWN
    best_confidence = 0.0

    if language == Language.JAPANESE:
        pattern_sets = [
            (JP_COMPLETED_PATTERNS, Intent.COMPLETED),
            (JP_DELEGATED_PATTERNS, Intent.DELEGATED),
            (JP_DEFERRED_PATTERNS, Intent.DEFERRED),
            (JP_IN_PROGRESS_PATTERNS, Intent.IN_PROGRESS),
        ]
    else:
        pattern_sets = [
            (EN_COMPLETED_PATTERNS, Intent.COMPLETED),
            (EN_DELEGATED_PATTERNS, Intent.DELEGATED),
            (EN_DEFERRED_PATTERNS, Intent.DEFERRED),
            (EN_IN_PROGRESS_PATTERNS, Intent.IN_PROGRESS),
        ]

    for patterns, intent in pattern_sets:
        for pattern, confidence in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_intent = intent

    return best_intent, best_confidence


def parse_status_update(text: str) -> ParseResult:
    """
    Parse a natural language status update.

    Args:
        text: Natural language status update in Japanese or English.

    Returns:
        ParseResult with extracted intent, person, channel, and keywords.
    """
    text = text.strip()

    # Detect language
    language = detect_language(text)

    # Detect intent
    intent, confidence = detect_intent(text, language)

    # Extract person
    person = extract_person(text, language)

    # Extract delegatee if delegation intent
    delegatee = None
    if intent == Intent.DELEGATED:
        delegatee = extract_delegatee(text, language)

    # Extract channel
    channel = extract_channel(text)

    # Extract keywords
    keywords = extract_keywords(text, language)

    return ParseResult(
        intent=intent,
        language=language,
        person=person,
        delegatee=delegatee,
        channel=channel,
        keywords=keywords,
        confidence=confidence,
        raw_input=text,
    )


if __name__ == "__main__":
    # Quick test with sample inputs
    test_inputs = [
        "Seanのメールには返信しておいた",
        "Lu対応予定",
        "Delegated the report to Mike",
        "The task is done",
        "来週対応する",
        "Working on the proposal",
        "田中さんに依頼した",
    ]

    for text in test_inputs:
        result = parse_status_update(text)
        print(f"\nInput: {text}")
        print(f"  Intent: {result.intent.value}")
        print(f"  Language: {result.language.value}")
        print(f"  Person: {result.person}")
        print(f"  Delegatee: {result.delegatee}")
        print(f"  Channel: {result.channel}")
        print(f"  Keywords: {result.keywords}")
        print(f"  Confidence: {result.confidence:.2f}")
