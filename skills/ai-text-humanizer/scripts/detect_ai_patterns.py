#!/usr/bin/env python3
"""AI Text Pattern Detector - Detect AI-generated text patterns and calculate AI-smell score."""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class PatternMatch:
    """A single pattern match with location and context."""
    pattern_id: int
    pattern_name: str
    matched_text: str
    line_number: int
    weight: float


@dataclass
class PatternResult:
    """Result for a single pattern category."""
    pattern_id: int
    pattern_name: str
    score: float
    max_score: float
    matches: list = field(default_factory=list)
    details: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result."""
    total_score: float
    level: str
    doc_type: str
    char_count: int
    paragraph_count: int
    sentence_count: int
    pattern_results: list = field(default_factory=list)


class TextAnalyzer:
    """Utility for basic text statistics."""

    @staticmethod
    def count_chars(text: str) -> int:
        return len(text.strip())

    @staticmethod
    def count_paragraphs(text: str) -> int:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        return len(paragraphs)

    @staticmethod
    def split_sentences(text: str) -> list:
        sentences = re.split(r"[。！？\n]", text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def get_sentence_endings(sentences: list) -> list:
        endings = []
        for s in sentences:
            if s.endswith("です"):
                endings.append("desu")
            elif s.endswith("ます"):
                endings.append("masu")
            elif s.endswith("した"):
                endings.append("shita")
            elif s.endswith("ません"):
                endings.append("masen")
            elif re.search(r"である$", s):
                endings.append("dearu")
            elif re.search(r"だ$", s):
                endings.append("da")
            elif re.search(r"る$", s):
                endings.append("ru")
            elif re.search(r"た$", s):
                endings.append("ta")
            elif re.search(r"い$", s):
                endings.append("i")
            else:
                endings.append("other")
        return endings

    @staticmethod
    def count_consecutive_same_endings(endings: list) -> int:
        if not endings:
            return 0
        max_consecutive = 1
        current = 1
        for i in range(1, len(endings)):
            if endings[i] == endings[i - 1] and endings[i] != "other":
                current += 1
                max_consecutive = max(max_consecutive, current)
            else:
                current = 1
        return max_consecutive


class AIPatternDetector:
    """Detect 6 AI writing patterns and calculate AI-smell score."""

    DOC_TYPES = {"auto", "email", "chat", "blog", "structured"}

    PATTERN_NAMES = {
        1: "視覚的マーカー残存",
        2: "単調なリズム",
        3: "マニュアル的構成",
        4: "非コミット姿勢",
        5: "抽象語の濫用",
        6: "定型メタファー",
    }

    PATTERN_MAX_SCORES = {
        1: 15.0,
        2: 20.0,
        3: 20.0,
        4: 15.0,
        5: 15.0,
        6: 15.0,
    }

    def __init__(self, doc_type: str = "auto"):
        if doc_type not in self.DOC_TYPES:
            raise ValueError(f"Unknown doc_type: {doc_type}. Choose from {sorted(self.DOC_TYPES)}")
        self.analyzer = TextAnalyzer()
        self.doc_type = doc_type

    def _resolve_doc_type(self, text: str) -> str:
        """Resolve document type in auto mode with lightweight heuristics."""
        if self.doc_type != "auto":
            return self.doc_type

        has_table = bool(re.search(r"^\|.*\|$", text, flags=re.M))
        has_code_fence = "```" in text
        has_heading = bool(re.search(r"^#{1,6}\s", text, flags=re.M))
        has_structured_keyword = bool(
            re.search(r"(見積書|提案書|報告書|仕様書|設計書|README|readme|要件定義|設計資料)", text)
        )
        has_email_marker = bool(re.search(r"^件名[:：]", text, flags=re.M)) or "お疲れ様です" in text

        if has_table or has_code_fence or has_structured_keyword:
            return "structured"
        if has_heading and len(text) >= 500:
            return "blog"
        if has_email_marker:
            return "email"
        return "chat"

    @staticmethod
    def _allows_structural_markdown(resolved_doc_type: str) -> bool:
        return resolved_doc_type in {"blog", "structured"}

    def detect_all(self, text: str) -> AnalysisResult:
        resolved_doc_type = self._resolve_doc_type(text)
        sentences = self.analyzer.split_sentences(text)
        lines = text.split("\n")

        results = [
            self._detect_pattern1(text, lines, resolved_doc_type),
            self._detect_pattern2(text, sentences),
            self._detect_pattern3(text, lines, sentences),
            self._detect_pattern4(text, sentences, lines),
            self._detect_pattern5(text, lines),
            self._detect_pattern6(text, lines),
        ]

        total = sum(r.score for r in results)
        level = self._interpret_score(total)

        return AnalysisResult(
            total_score=round(total, 1),
            level=level,
            doc_type=resolved_doc_type,
            char_count=self.analyzer.count_chars(text),
            paragraph_count=self.analyzer.count_paragraphs(text),
            sentence_count=len(sentences),
            pattern_results=results,
        )

    def _interpret_score(self, score: float) -> str:
        if score <= 25:
            return "Natural"
        elif score <= 50:
            return "Slightly AI"
        elif score <= 75:
            return "Clearly AI"
        else:
            return "Strongly AI"

    def _detect_pattern1(self, text: str, lines: list, resolved_doc_type: str) -> PatternResult:
        """Pattern 1: Visual Marker Residue."""
        matches = []
        score = 0.0
        allow_structural_markdown = self._allows_structural_markdown(resolved_doc_type)

        # Bold markers
        for i, line in enumerate(lines):
            for m in re.finditer(r"\*\*[^*]+\*\*", line):
                matches.append(PatternMatch(1, "太字マーカー", m.group(), i + 1, 3.0))
                score += 3.0

        # Heading markers
        if not allow_structural_markdown:
            for i, line in enumerate(lines):
                if re.match(r"^#{1,6}\s", line):
                    matches.append(PatternMatch(1, "見出しマーカー", line.strip()[:50], i + 1, 3.0))
                    score += 3.0

        # Em dash
        for i, line in enumerate(lines):
            for m in re.finditer(r"—", line):
                matches.append(PatternMatch(1, "エムダッシュ", f"...{line[max(0,m.start()-10):m.end()+10]}...", i + 1, 2.0))
                score += 2.0

        # Full-width slash
        for i, line in enumerate(lines):
            for m in re.finditer(r"／", line):
                matches.append(PatternMatch(1, "全角スラッシュ", f"...{line[max(0,m.start()-10):m.end()+10]}...", i + 1, 2.0))
                score += 2.0

        # Excessive parentheses per paragraph
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        for p in paragraphs:
            paren_count = len(re.findall(r"（[^）]+）", p))
            if paren_count >= 3:
                matches.append(PatternMatch(1, "括弧過多", f"段落内に{paren_count}個の（）", 0, 5.0))
                score += 5.0

        # Nested quotation marks
        for i, line in enumerate(lines):
            for m in re.finditer(r"「[^」]*『[^』]*』[^」]*」", line):
                matches.append(PatternMatch(1, "入れ子引用符", m.group()[:40], i + 1, 3.0))
                score += 3.0

        # Bullet points ratio
        if not allow_structural_markdown:
            bullet_lines = sum(1 for line in lines if re.match(r"^\s*[-•]\s", line))
            if lines and bullet_lines / len(lines) > 0.3:
                matches.append(PatternMatch(1, "箇条書き過多", f"箇条書き{bullet_lines}/{len(lines)}行 ({bullet_lines/len(lines)*100:.0f}%)", 0, 5.0))
                score += 5.0

        max_score = self.PATTERN_MAX_SCORES[1]
        return PatternResult(
            pattern_id=1,
            pattern_name=self.PATTERN_NAMES[1],
            score=min(score, max_score),
            max_score=max_score,
            matches=matches,
            details=self._summarize_matches(matches),
        )

    def _detect_pattern2(self, text: str, sentences: list) -> PatternResult:
        """Pattern 2: Monotonous Rhythm."""
        matches = []
        score = 0.0

        # Consecutive same endings
        endings = self.analyzer.get_sentence_endings(sentences)
        max_consec = self.analyzer.count_consecutive_same_endings(endings)
        if max_consec >= 4:
            matches.append(PatternMatch(2, "文末連続", f"同一文末{max_consec}連続", 0, 8.0))
            score += 8.0
        elif max_consec >= 3:
            matches.append(PatternMatch(2, "文末連続", f"同一文末{max_consec}連続", 0, 5.0))
            score += 5.0

        # Excessive conjunctions (sentence-based to catch mid-line conjunctions)
        lines = text.split("\n")
        conj_pattern = r"^(また|さらに|そして|しかし|一方で|一方|加えて|つまり|なお|ただし|しかしながら|したがって|このように|それゆえ|このため)[、，]"
        conj_count = 0
        for sent in sentences:
            if re.match(conj_pattern, sent):
                conj_count += 1
                pos = text.find(sent)
                line_num = text[:pos].count("\n") + 1 if pos >= 0 else 0
                matches.append(PatternMatch(2, "接続詞開始", sent[:30], line_num, 0))

        if sentences:
            conj_ratio = conj_count / len(sentences)
            if conj_ratio > 0.4:
                score += 10.0
            elif conj_ratio > 0.2:
                score += 5.0

        # not A but B pattern
        nab_patterns = [r"単に.+だけでなく.+も", r".+ではなく.+", r"だけでなく.+も重要"]
        for i, line in enumerate(lines):
            for pat in nab_patterns:
                for m in re.finditer(pat, line):
                    matches.append(PatternMatch(2, "not A but B", m.group()[:40], i + 1, 3.0))
                    score += 3.0

        # Uniform sentence length
        if len(sentences) >= 5:
            lengths = [len(s) for s in sentences]
            avg = sum(lengths) / len(lengths)
            if avg > 0:
                std = (sum((l - avg) ** 2 for l in lengths) / len(lengths)) ** 0.5
                if std / avg < 0.2:
                    matches.append(PatternMatch(2, "均一文長", f"平均{avg:.0f}字, 標準偏差{std:.1f}", 0, 5.0))
                    score += 5.0

        # Mechanical closing
        closing_patterns = [
            r"と言えるでしょう",
            r"ではないでしょうか",
            r"が求められます",
            r"が期待されます",
            r"が不可欠です",
        ]
        for i, line in enumerate(lines):
            for pat in closing_patterns:
                if re.search(pat, line):
                    matches.append(PatternMatch(2, "機械的閉じ方", line.strip()[-30:], i + 1, 3.0))
                    score += 3.0

        max_score = self.PATTERN_MAX_SCORES[2]
        return PatternResult(
            pattern_id=2,
            pattern_name=self.PATTERN_NAMES[2],
            score=min(score, max_score),
            max_score=max_score,
            matches=matches,
            details=self._summarize_matches(matches),
        )

    def _detect_pattern3(self, text: str, lines: list, sentences: list) -> PatternResult:
        """Pattern 3: Manual-like Structure."""
        matches = []
        score = 0.0

        # Structure declaration
        struct_patterns = [
            r"以下では.+について",
            r"本稿では.+を",
            r"ここでは.+を見ていき",
            r"について解説します",
            r"について説明します",
            r"について考察します",
            r"を紹介します",
        ]
        for i, line in enumerate(lines):
            for pat in struct_patterns:
                if re.search(pat, line):
                    matches.append(PatternMatch(3, "構成宣言", line.strip()[:50], i + 1, 5.0))
                    score += 5.0
                    break

        # Long preamble (first paragraph > 100 chars without getting to the point)
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if paragraphs and len(paragraphs[0]) > 100:
            first_para = paragraphs[0]
            preamble_indicators = ["近年", "昨今", "現代社会", "多くの企業", "急速に", "注目を集めて"]
            if any(ind in first_para for ind in preamble_indicators):
                matches.append(PatternMatch(3, "長い前置き", first_para[:50] + "...", 1, 5.0))
                score += 5.0

        # Step notation
        step_patterns = [
            r"ステップ[0-9０-９]",
            r"第[一二三四五六七八九十]に",
            r"[0-9０-９]+つ目は",
            r"まず[、，].+次に[、，].+最後に",
        ]
        for i, line in enumerate(lines):
            for pat in step_patterns:
                if re.search(pat, line):
                    matches.append(PatternMatch(3, "ステップ表記", line.strip()[:40], i + 1, 3.0))
                    score += 3.0

        # Exhaustive listing (3+ comma-separated items, 2+ occurrences)
        listing_pattern = r"[^、。\n]+[、，][^、。\n]+[、，][^、。\n]+"
        listing_count = 0
        for i, line in enumerate(lines):
            if re.search(listing_pattern, line):
                listing_count += 1
        if listing_count >= 2:
            matches.append(PatternMatch(3, "網羅的列挙", "3項目以上の並列列挙が%d回" % listing_count, 0, 5.0))
            score += 5.0

        # Weak conclusion
        if lines:
            weak_patterns = [
                r"が重要です",
                r"が求められています",
                r"ではないでしょうか",
                r"が期待されます",
                r"を目指していきましょう",
                r"が鍵となるでしょう",
            ]
            tail = lines[-5:]
            for pat in weak_patterns:
                for tail_index, line in enumerate(tail):
                    if re.search(pat, line):
                        line_number = len(lines) - len(tail) + tail_index + 1
                        snippet = line.strip()[-60:]
                        matches.append(PatternMatch(3, "薄い結論", snippet, line_number, 5.0))
                        score += 5.0
                        break
                else:
                    continue
                break

        # Even section sizes
        if len(paragraphs) >= 3:
            para_lengths = [len(p) for p in paragraphs]
            avg_len = sum(para_lengths) / len(para_lengths)
            if avg_len > 0:
                all_within = all(abs(l - avg_len) / avg_len < 0.15 for l in para_lengths)
                if all_within:
                    matches.append(PatternMatch(3, "セクション均等", f"段落長の偏差15%以内", 0, 3.0))
                    score += 3.0

        max_score = self.PATTERN_MAX_SCORES[3]
        return PatternResult(
            pattern_id=3,
            pattern_name=self.PATTERN_NAMES[3],
            score=min(score, max_score),
            max_score=max_score,
            matches=matches,
            details=self._summarize_matches(matches),
        )

    def _detect_pattern4(self, text: str, sentences: list, lines: list) -> PatternResult:
        """Pattern 4: Non-committal Stance."""
        matches = []
        score = 0.0

        # Hedge words
        hedge_patterns = [
            (r"かもしれません", "ヘッジ語"),
            (r"の可能性があります", "ヘッジ語"),
            (r"とも考えられます", "ヘッジ語"),
            (r"一概には言えません", "ヘッジ語"),
            (r"と思われます", "ヘッジ語"),
            (r"と推測されます", "ヘッジ語"),
        ]
        for i, line in enumerate(lines):
            for pat, name in hedge_patterns:
                for m in re.finditer(pat, line):
                    matches.append(PatternMatch(4, name, f"...{line[max(0,m.start()-15):m.end()]}...", i + 1, 3.0))
                    score += 3.0

        # Forced neutrality (paragraph-based, counting occurrences not unique patterns)
        neutral_patterns = [
            r"一方で",
            r"他方では",
            r"という見方もあります",
            r"という意見もあります",
        ]
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for para in paragraphs:
            neutral_count = sum(len(re.findall(pat, para)) for pat in neutral_patterns)
            if neutral_count >= 2:
                para_pos = text.find(para)
                line_num = text[:para_pos].count("\n") + 1 if para_pos >= 0 else 0
                matches.append(PatternMatch(4, "強制中立", para[:50], line_num, 5.0))
                score += 5.0

        # Weak negation
        weak_neg_patterns = [
            r"必ずしも.+ではない",
            r"とは限りません",
        ]
        for i, line in enumerate(lines):
            for pat in weak_neg_patterns:
                if re.search(pat, line):
                    matches.append(PatternMatch(4, "弱い否定", line.strip()[:40], i + 1, 2.0))
                    score += 2.0

        # Assertion avoidance
        avoid_patterns = [
            (r"傾向にあります", "断定回避"),
            (r"ことが多いです", "断定回避"),
            (r"一般的に", "断定回避"),
            (r"個人の見解であり", "免責表現"),
            (r"ケースバイケースで", "免責表現"),
            (r"状況によって異なり", "免責表現"),
        ]
        for i, line in enumerate(lines):
            for pat, name in avoid_patterns:
                if re.search(pat, line):
                    matches.append(PatternMatch(4, name, line.strip()[:40], i + 1, 2.0))
                    score += 2.0

        # Both-sides presentation
        both_patterns = [r"メリットとデメリット", r"長所と短所", r"利点と欠点"]
        for i, line in enumerate(lines):
            for pat in both_patterns:
                if re.search(pat, line):
                    matches.append(PatternMatch(4, "両論併記", line.strip()[:40], i + 1, 3.0))
                    score += 3.0
                    break  # 1行1回のみカウント

        max_score = self.PATTERN_MAX_SCORES[4]
        return PatternResult(
            pattern_id=4,
            pattern_name=self.PATTERN_NAMES[4],
            score=min(score, max_score),
            max_score=max_score,
            matches=matches,
            details=self._summarize_matches(matches),
        )

    def _detect_pattern5(self, text: str, lines: list) -> PatternResult:
        """Pattern 5: Abstract Word Overuse."""
        matches = []
        score = 0.0

        # Hollow abstract words
        abstract_words = [
            "本質的", "包括的", "体系的", "戦略的", "革新的",
            "持続可能な", "多角的", "総合的", "抜本的", "画期的",
        ]
        for i, line in enumerate(lines):
            for word in abstract_words:
                if word in line:
                    matches.append(PatternMatch(5, "空疎な抽象語", word, i + 1, 2.0))
                    score += 2.0

        # Unsupported strong evaluation
        strong_eval_patterns = [
            r"非常に重要",
            r"極めて効果的",
            r"大きな成果",
            r"飛躍的な向上",
            r"劇的な改善",
            r"目覚ましい成長",
        ]
        for i, line in enumerate(lines):
            for pat in strong_eval_patterns:
                if re.search(pat, line):
                    matches.append(PatternMatch(5, "根拠なき強評価", pat.replace(r"\\", ""), i + 1, 3.0))
                    score += 3.0

        # Substanceless nouns
        hollow_nouns = [
            "フレームワーク", "アプローチ", "ソリューション",
            "エコシステム", "パラダイム", "メソドロジー",
        ]
        for i, line in enumerate(lines):
            for noun in hollow_nouns:
                if noun in line:
                    matches.append(PatternMatch(5, "実体なき名詞", noun, i + 1, 2.0))
                    score += 2.0

        # Spinning modifiers
        spinning_mods = ["適切な", "効果的な", "最適な", "理想的な", "有効な"]
        for i, line in enumerate(lines):
            for mod in spinning_mods:
                if mod in line:
                    matches.append(PatternMatch(5, "修飾語の空転", mod, i + 1, 1.5))
                    score += 1.5

        # Buzzwords
        buzzwords = ["シナジー", "レバレッジ", "スケーラブル", "アジャイル",
                     "イニシアチブ", "コンセンサス", "プロアクティブ"]
        for i, line in enumerate(lines):
            for word in buzzwords:
                if word in line:
                    matches.append(PatternMatch(5, "バズワード", word, i + 1, 1.5))
                    score += 1.5

        max_score = self.PATTERN_MAX_SCORES[5]
        return PatternResult(
            pattern_id=5,
            pattern_name=self.PATTERN_NAMES[5],
            score=min(score, max_score),
            max_score=max_score,
            matches=matches,
            details=self._summarize_matches(matches),
        )

    def _detect_pattern6(self, text: str, lines: list) -> PatternResult:
        """Pattern 6: Stock Metaphors."""
        matches = []
        score = 0.0

        high_metaphors = [
            (r"羅針盤", "羅針盤"),
            (r"(?:道の)?地図(?:を描く|となる)", "地図"),
            # Treat "設計書" as a stock metaphor only in metaphorical contexts.
            # Literal document titles like "在庫連携バッチ 設計書" should not be flagged.
            (r"青写真", "設計書/青写真"),
            (r"(?:[^\s。、「」『』()（）]+の)?設計書(?:として機能(?:し|する|します)?|となる|となります|になる|になります)", "設計書/青写真"),
            (r"(?:企業|組織|チーム)の?DNA", "DNA"),
            (r"車の両輪", "車の両輪"),
            (r"潤滑油", "潤滑油"),
        ]
        medium_metaphors = [
            (r"(?:の|大きな|重要な)柱", "柱"),
            (r"(?:成長|変革|イノベーション)の?エンジン", "エンジン"),
            (r"(?:隠し味|秘訣|成功)の?スパイス", "スパイス"),
            (r"(?:成功|成長)の?レシピ", "レシピ"),
            (r"架け橋|かけ橋|懸け橋", "架け橋"),
        ]
        low_metaphors = [
            (r"(?:成功|発展|成長|繁栄)の礎", "礎"),
            (r"(?:成功|発展|成長)の土台", "土台"),
        ]

        for i, line in enumerate(lines):
            for pat, name in high_metaphors:
                for m in re.finditer(pat, line):
                    matches.append(PatternMatch(6, name, m.group(), i + 1, 4.0))
                    score += 4.0

            for pat, name in medium_metaphors:
                for m in re.finditer(pat, line):
                    matches.append(PatternMatch(6, name, m.group(), i + 1, 3.0))
                    score += 3.0

            for pat, name in low_metaphors:
                for m in re.finditer(pat, line):
                    matches.append(PatternMatch(6, name, m.group(), i + 1, 2.0))
                    score += 2.0

        max_score = self.PATTERN_MAX_SCORES[6]
        return PatternResult(
            pattern_id=6,
            pattern_name=self.PATTERN_NAMES[6],
            score=min(score, max_score),
            max_score=max_score,
            matches=matches,
            details=self._summarize_matches(matches),
        )

    @staticmethod
    def _summarize_matches(matches: list) -> str:
        if not matches:
            return "検出なし"
        categories = {}
        for m in matches:
            categories.setdefault(m.pattern_name, 0)
            categories[m.pattern_name] += 1
        parts = [f"{name}({count})" for name, count in categories.items()]
        return ", ".join(parts)


def format_report(result: AnalysisResult) -> str:
    """Format analysis result as Markdown report."""
    def code_span(text: str) -> str:
        normalized = re.sub(r"\s+", " ", str(text).replace("\r", " ").replace("\n", " ")).strip()
        if not normalized:
            normalized = "…"
        max_ticks = 0
        for m in re.finditer(r"`+", normalized):
            max_ticks = max(max_ticks, len(m.group(0)))
        delimiter = "`" * (max_ticks + 1)
        return f"{delimiter}{normalized}{delimiter}"

    lines = []
    lines.append("# AI臭検出レポート\n")
    lines.append("## 総合スコア\n")
    lines.append(f"| Item | Value |")
    lines.append(f"|------|-------|")
    lines.append(f"| AI臭スコア | **{result.total_score}** / 100 |")
    lines.append(f"| 判定 | {result.level} |")
    lines.append(f"| 文書種別 | {result.doc_type} |")
    lines.append(f"| 文字数 | {result.char_count} 文字 |")
    lines.append(f"| 段落数 | {result.paragraph_count} 段落 |")
    lines.append(f"| 文数 | {result.sentence_count} 文 |")
    lines.append("")

    lines.append("## パターン別スコア\n")
    lines.append("| # | Pattern | Score | Max | Details |")
    lines.append("|---|---------|-------|-----|---------|")
    for pr in result.pattern_results:
        lines.append(f"| {pr.pattern_id} | {pr.pattern_name} | {pr.score:.1f} | {pr.max_score:.0f} | {pr.details} |")
    lines.append("")

    lines.append("## 検出された具体例\n")
    for pr in result.pattern_results:
        lines.append(f"### Pattern {pr.pattern_id}: {pr.pattern_name}\n")
        if not pr.matches:
            lines.append("検出なし\n")
        else:
            for m in pr.matches[:10]:
                loc = f"L{m.line_number}" if m.line_number > 0 else ""
                lines.append(f"- [{m.pattern_name}] {loc} {code_span(m.matched_text)}")
            if len(pr.matches) > 10:
                lines.append(f"- ... 他{len(pr.matches) - 10}件")
            lines.append("")

    lines.append("## 推奨アクション\n")
    if result.total_score <= 25:
        lines.append("修正不要。自然な文章です。")
    elif result.total_score <= 50:
        top_patterns = sorted(result.pattern_results, key=lambda x: x.score, reverse=True)[:2]
        lines.append("軽微な修正で改善可能です。以下のパターンを優先的に修正してください:\n")
        for p in top_patterns:
            if p.score > 0:
                lines.append(f"- {p.pattern_name} (スコア: {p.score:.1f}/{p.max_score:.0f})")
    elif result.total_score <= 75:
        lines.append("リライトを推奨します。以下の順序で修正してください:\n")
        for p in sorted(result.pattern_results, key=lambda x: x.score, reverse=True):
            if p.score > 0:
                lines.append(f"1. {p.pattern_name} (スコア: {p.score:.1f}/{p.max_score:.0f})")
    else:
        lines.append("全面リライトを推奨します。すべてのパターンで高いAI臭が検出されました。\n")
        lines.append("リライト時は `references/rewrite_rules.md` の変換ルールと")
        lines.append("`references/human_writing_techniques.md` の3技法を参照してください。")

    lines.append("\n---\n*Generated by AI Text Humanizer skill*")
    return "\n".join(lines)


def format_json(result: AnalysisResult) -> str:
    """Format analysis result as JSON."""
    data = {
        "total_score": result.total_score,
        "level": result.level,
        "doc_type": result.doc_type,
        "char_count": result.char_count,
        "paragraph_count": result.paragraph_count,
        "sentence_count": result.sentence_count,
        "patterns": [],
    }
    for pr in result.pattern_results:
        pattern_data = {
            "id": pr.pattern_id,
            "name": pr.pattern_name,
            "score": pr.score,
            "max_score": pr.max_score,
            "details": pr.details,
            "match_count": len(pr.matches),
            "examples": [
                {"type": m.pattern_name, "text": m.matched_text, "line": m.line_number}
                for m in pr.matches[:5]
            ],
        }
        data["patterns"].append(pattern_data)
    return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Detect AI writing patterns and calculate AI-smell score (0-100)"
    )
    parser.add_argument("input_file", help="Input text file path")
    parser.add_argument(
        "--output", "-o",
        help="Output report file path (default: stdout)",
        default=None,
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--encoding", "-e",
        default="utf-8",
        help="Input file encoding (default: utf-8)",
    )
    parser.add_argument(
        "--doc-type",
        choices=["auto", "email", "chat", "blog", "structured"],
        default="auto",
        help="Document type for markdown-aware detection (default: auto)",
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    try:
        text = input_path.read_text(encoding=args.encoding)
    except LookupError:
        print(f"Error: Unknown encoding: {args.encoding}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(
            f"Error: Cannot decode input as {args.encoding}: {e}. "
            "Try converting the file to UTF-8 or pass --encoding (e.g. cp932).",
            file=sys.stderr,
        )
        sys.exit(1)
    except OSError as e:
        print(f"Error: Cannot read file {args.input_file}: {e}", file=sys.stderr)
        sys.exit(1)

    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip():
        print("Error: Input file is empty", file=sys.stderr)
        sys.exit(1)

    detector = AIPatternDetector(doc_type=args.doc_type)
    result = detector.detect_all(text)

    if args.format == "json":
        output = format_json(result)
    else:
        output = format_report(result)

    if args.output:
        output_path = Path(args.output)
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding="utf-8")
            print(f"Report written to: {args.output}")
            print(f"AI-smell score: {result.total_score}/100 ({result.level})")
        except (IOError, OSError) as e:
            print(f"Error: Cannot write to {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()
