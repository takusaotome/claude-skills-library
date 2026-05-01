#!/usr/bin/env python3
"""
Keigo Transformation Tool

Transforms Japanese text to appropriate keigo (敬語) level based on target audience.
Supports four levels: highest (最上級), upper (上級), standard (標準), basic (基本).
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class KeigoLevel(Enum):
    """Keigo formality levels."""

    HIGHEST = "highest"  # 最上級敬語 (役員向け)
    UPPER = "upper"  # 上級敬語 (本部長/部長向け)
    STANDARD = "standard"  # 標準敬語 (課長向け)
    BASIC = "basic"  # 基本丁寧語 (同僚向け)


@dataclass
class TransformationRule:
    """A keigo transformation rule."""

    pattern: str
    replacement: str
    level: KeigoLevel
    category: str  # 尊敬語, 謙譲語, 丁寧語


# Transformation rules for different keigo levels
TRANSFORMATION_RULES = [
    # Highest level (最上級敬語)
    TransformationRule(r"します$", "させていただきます", KeigoLevel.HIGHEST, "謙譲語"),
    TransformationRule(r"いたします$", "させていただきます", KeigoLevel.HIGHEST, "謙譲語"),
    TransformationRule(r"お願いします$", "お願い申し上げます", KeigoLevel.HIGHEST, "謙譲語"),
    TransformationRule(r"お願いいたします$", "お願い申し上げます", KeigoLevel.HIGHEST, "謙譲語"),
    TransformationRule(r"ください$", "賜りますようお願い申し上げます", KeigoLevel.HIGHEST, "謙譲語"),
    TransformationRule(r"です$", "でございます", KeigoLevel.HIGHEST, "丁寧語"),
    TransformationRule(r"ありがとうございます$", "厚く御礼申し上げます", KeigoLevel.HIGHEST, "謙譲語"),
    TransformationRule(r"思います$", "存じます", KeigoLevel.HIGHEST, "謙譲語"),
    TransformationRule(r"考えています$", "考えております", KeigoLevel.HIGHEST, "謙譲語"),
    # Upper level (上級敬語)
    TransformationRule(r"します$", "いたします", KeigoLevel.UPPER, "謙譲語"),
    TransformationRule(r"お願いします$", "お願いいたします", KeigoLevel.UPPER, "謙譲語"),
    TransformationRule(r"ください$", "いただけますと幸いです", KeigoLevel.UPPER, "謙譲語"),
    TransformationRule(r"です$", "でございます", KeigoLevel.UPPER, "丁寧語"),
    TransformationRule(r"思います$", "と考えております", KeigoLevel.UPPER, "謙譲語"),
    # Standard level (標準敬語)
    TransformationRule(r"する$", "します", KeigoLevel.STANDARD, "丁寧語"),
    TransformationRule(r"だ$", "です", KeigoLevel.STANDARD, "丁寧語"),
    TransformationRule(r"ある$", "あります", KeigoLevel.STANDARD, "丁寧語"),
    TransformationRule(r"いる$", "います", KeigoLevel.STANDARD, "丁寧語"),
    TransformationRule(r"ない$", "ありません", KeigoLevel.STANDARD, "丁寧語"),
    # Basic level (基本丁寧語) - minimal transformations
    TransformationRule(r"する$", "します", KeigoLevel.BASIC, "丁寧語"),
    TransformationRule(r"だ$", "です", KeigoLevel.BASIC, "丁寧語"),
]


# Common verb transformations
VERB_TRANSFORMATIONS = {
    # Plain -> 謙譲語 (Humble)
    "humble": {
        "いる": "おる",
        "行く": "参る",
        "来る": "参る",
        "言う": "申す",
        "見る": "拝見する",
        "知る": "存じる",
        "聞く": "伺う",
        "会う": "お目にかかる",
        "もらう": "いただく",
        "する": "いたす",
        "あげる": "差し上げる",
        "思う": "存じる",
        "食べる": "いただく",
        "送る": "お送りする",
        "連絡する": "ご連絡する",
        "報告する": "ご報告する",
        "確認する": "確認いたす",
    },
    # Plain -> 尊敬語 (Respectful)
    "respectful": {
        "いる": "いらっしゃる",
        "行く": "いらっしゃる",
        "来る": "いらっしゃる",
        "言う": "おっしゃる",
        "見る": "ご覧になる",
        "知る": "ご存知である",
        "聞く": "お聞きになる",
        "する": "なさる",
        "くれる": "くださる",
        "食べる": "召し上がる",
        "読む": "お読みになる",
        "考える": "お考えになる",
    },
}


# Closing phrase templates by level
CLOSING_TEMPLATES = {
    KeigoLevel.HIGHEST: [
        "何卒ご裁可賜りますよう、謹んでお願い申し上げます。",
        "ご高配を賜りたく、お願い申し上げます。",
        "何卒ご承認賜りますようお願い申し上げます。",
    ],
    KeigoLevel.UPPER: [
        "ご検討のほど、よろしくお願い申し上げます。",
        "ご承認いただきたく、お願い申し上げます。",
        "ご確認のほど、よろしくお願いいたします。",
    ],
    KeigoLevel.STANDARD: [
        "よろしくお願いいたします。",
        "ご確認をお願いいたします。",
        "ご対応をお願いいたします。",
    ],
    KeigoLevel.BASIC: [
        "よろしくお願いします。",
        "ご確認ください。",
        "お願いします。",
    ],
}


@dataclass
class TransformationResult:
    """Result of keigo transformation."""

    original_text: str
    transformed_text: str
    target_level: KeigoLevel
    transformations_applied: list
    warnings: list


def get_level_hierarchy(level: KeigoLevel) -> int:
    """Get numeric hierarchy for keigo level (higher = more formal)."""
    hierarchy = {
        KeigoLevel.BASIC: 1,
        KeigoLevel.STANDARD: 2,
        KeigoLevel.UPPER: 3,
        KeigoLevel.HIGHEST: 4,
    }
    return hierarchy[level]


def transform_verb_humble(verb: str) -> Optional[str]:
    """Transform verb to humble form (謙譲語)."""
    return VERB_TRANSFORMATIONS["humble"].get(verb)


def transform_verb_respectful(verb: str) -> Optional[str]:
    """Transform verb to respectful form (尊敬語)."""
    return VERB_TRANSFORMATIONS["respectful"].get(verb)


def apply_transformation_rules(text: str, target_level: KeigoLevel) -> tuple[str, list]:
    """Apply transformation rules to text."""
    transformations_applied = []
    result = text

    # Filter rules by target level and apply
    applicable_rules = [
        rule for rule in TRANSFORMATION_RULES if get_level_hierarchy(rule.level) <= get_level_hierarchy(target_level)
    ]

    # Apply rules low-level -> high-level so a chain like
    #     する -> します -> いたします -> させていただきます
    # actually advances all the way to the requested level. Sorting in the
    # other direction would apply HIGHEST first, find no match, then drop
    # back to STANDARD and stop one level short of the target.
    applicable_rules.sort(key=lambda r: get_level_hierarchy(r.level))

    for rule in applicable_rules:
        # Rules use `$` to anchor at end-of-clause but real Japanese text is
        # punctuated with 。 or 、 between clauses (and may run on a single line),
        # so `$` would only match at the very end of the buffer. Rewrite a
        # trailing `$` into a lookahead that fires at sentence punctuation,
        # newlines, OR end-of-string so each clause is transformed in turn.
        pattern = rule.pattern
        if pattern.endswith("$"):
            pattern = pattern[:-1] + r"(?=[。\n]|$)"
        if re.search(pattern, result):
            new_result = re.sub(pattern, rule.replacement, result)
            if new_result != result:
                transformations_applied.append(
                    {
                        "pattern": rule.pattern,
                        "replacement": rule.replacement,
                        "category": rule.category,
                    }
                )
                result = new_result

    return result, transformations_applied


def detect_keigo_issues(text: str, target_level: KeigoLevel) -> list:
    """Detect potential keigo issues in text."""
    warnings = []

    # Check for mixing of levels
    if target_level in [KeigoLevel.HIGHEST, KeigoLevel.UPPER]:
        # Check for informal endings
        informal_patterns = [
            (r"です\。", "Consider using でございます for higher formality"),
            (r"します\。", "Consider using いたします or させていただきます"),
            (r"お願いします\。", "Consider using お願いいたします or お願い申し上げます"),
        ]
        for pattern, warning in informal_patterns:
            if re.search(pattern, text):
                warnings.append(warning)

    # Check for double honorifics (二重敬語)
    double_honorific_patterns = [
        (r"お.*になられ", "Double honorific detected: お～になられる"),
        (r"ご.*になられ", "Double honorific detected: ご～になられる"),
    ]
    for pattern, warning in double_honorific_patterns:
        if re.search(pattern, text):
            warnings.append(warning)

    # Check for incorrect humble/respectful usage
    if "おっしゃりました" in text:
        warnings.append("Consider おっしゃいました instead of おっしゃりました")

    return warnings


def transform_text(text: str, target_level: KeigoLevel) -> TransformationResult:
    """Transform text to target keigo level."""
    transformed, transformations = apply_transformation_rules(text, target_level)
    warnings = detect_keigo_issues(transformed, target_level)

    return TransformationResult(
        original_text=text,
        transformed_text=transformed,
        target_level=target_level,
        transformations_applied=transformations,
        warnings=warnings,
    )


def get_closing_phrase(level: KeigoLevel, index: int = 0) -> str:
    """Get appropriate closing phrase for keigo level."""
    phrases = CLOSING_TEMPLATES[level]
    return phrases[index % len(phrases)]


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


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Transform Japanese text to appropriate keigo level")
    parser.add_argument("--input", "-i", help="Input file path (default: stdin)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--level", "-l", default="standard", help="Target keigo level: highest, upper, standard, basic")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--text", "-t", help="Direct text input (alternative to --input)")

    args = parser.parse_args()

    try:
        target_level = parse_keigo_level(args.level)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Get input text
    if args.text:
        input_text = args.text
    elif args.input:
        input_text = Path(args.input).read_text(encoding="utf-8")
    else:
        input_text = sys.stdin.read()

    # Transform text
    result = transform_text(input_text, target_level)

    # Output
    if args.format == "json":
        output = json.dumps(
            {
                "original_text": result.original_text,
                "transformed_text": result.transformed_text,
                "target_level": result.target_level.value,
                "transformations_applied": result.transformations_applied,
                "warnings": result.warnings,
                "suggested_closing": get_closing_phrase(target_level),
            },
            ensure_ascii=False,
            indent=2,
        )
    else:
        output = result.transformed_text
        if result.warnings:
            print("\n--- Warnings ---", file=sys.stderr)
            for warning in result.warnings:
                print(f"  - {warning}", file=sys.stderr)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Output written to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
