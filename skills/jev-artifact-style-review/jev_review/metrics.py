"""Local diagnostics only. Counts are never converted into an authorship score."""

from __future__ import annotations

import re
from collections import Counter

INJECTION = re.compile(
    r"ignore.{0,40}(previous|instructions)|override.{0,30}(system|score)|前の指示.{0,12}無視|評価.{0,12}(0点|ゼロ)|スコア.{0,12}(ゼロ|0に)",
    re.I,
)
NUMBER = re.compile(
    r"(?<![\w])(?:[$¥€£]\s*)?[+−-]?\d[\d,]*(?:\.\d+)?(?:\s*%|\s*(?:USD|JPY))?|\d+(?:年|月|日|時|分|万|億|台|件|人|円)"
)
URL = re.compile(r"https?://[^\s<>\]）)]+")


def surface_metrics(text: str) -> dict:
    return {
        "characters": len(text),
        "nonempty_lines": sum(bool(x.strip()) for x in text.splitlines()),
        "markdown_headings": len(re.findall(r"^\s{0,3}#{1,6}\s", text, re.M)),
        "list_lines": len(re.findall(r"^\s*(?:[-*+]\s|\d+[.)]\s)", text, re.M)),
        "numeric_tokens": dict(Counter(NUMBER.findall(text))),
        "urls": sorted(set(URL.findall(text))),
        "possible_embedded_evaluator_instruction": bool(INJECTION.search(text)),
        "note": "Descriptive counts and a heuristic warning, not evidence of machine authorship.",
    }


def protected_checks(text: str, context: dict) -> dict:
    phrases = context.get("protected_fragments", [])
    return {
        "required_literals": phrases,
        "missing_literals": [p for p in phrases if p not in text],
        "semantic_fact_verification": "not_performed; independent reviewer required",
    }
