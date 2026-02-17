#!/usr/bin/env python3
"""Tests for AI pattern detector — TDD RED/GREEN approach."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from detect_ai_patterns import AIPatternDetector, TextAnalyzer


class TestTextAnalyzer(unittest.TestCase):
    """Smoke tests for TextAnalyzer utility."""

    def test_split_sentences(self):
        text = "これは文1です。これは文2です。これは文3です。"
        sentences = TextAnalyzer.split_sentences(text)
        self.assertEqual(len(sentences), 3)

    def test_count_paragraphs(self):
        text = "段落1です。\n\n段落2です。\n\n段落3です。"
        self.assertEqual(TextAnalyzer.count_paragraphs(text), 3)


class TestPattern1SmokeTests(unittest.TestCase):
    """Smoke tests — existing Pattern 1 detection should not break."""

    def setUp(self):
        self.detector = AIPatternDetector()

    def test_bold_marker_detected(self):
        text = "これは**太字**のテストです。"
        result = self.detector.detect_all(text)
        p1 = result.pattern_results[0]
        self.assertTrue(any(m.pattern_name == "太字マーカー" for m in p1.matches))

    def test_heading_marker_detected(self):
        text = "## 見出しです\n本文です。"
        result = self.detector.detect_all(text)
        p1 = result.pattern_results[0]
        self.assertTrue(any(m.pattern_name == "見出しマーカー" for m in p1.matches))

    def test_em_dash_detected(self):
        text = "これは—テストです。"
        result = self.detector.detect_all(text)
        p1 = result.pattern_results[0]
        self.assertTrue(any(m.pattern_name == "エムダッシュ" for m in p1.matches))


class TestPattern1DocTypeAwareness(unittest.TestCase):
    """Pattern 1: structural markdown scoring should depend on doc_type."""

    def test_heading_and_bullets_not_scored_in_structured_doc(self):
        detector = AIPatternDetector(doc_type="structured")
        text = "## 設計概要\n- 項目A\n- 項目B\n本文です。"
        result = detector.detect_all(text)
        p1 = result.pattern_results[0]
        self.assertFalse(any(m.pattern_name == "見出しマーカー" for m in p1.matches))
        self.assertFalse(any(m.pattern_name == "箇条書き過多" for m in p1.matches))
        self.assertEqual(result.doc_type, "structured")

    def test_heading_scored_in_email_doc(self):
        detector = AIPatternDetector(doc_type="email")
        text = "## 件名: ご連絡\n本文です。"
        result = detector.detect_all(text)
        p1 = result.pattern_results[0]
        self.assertTrue(any(m.pattern_name == "見出しマーカー" for m in p1.matches))
        self.assertEqual(result.doc_type, "email")

    def test_auto_doc_type_resolves_structured_with_table(self):
        detector = AIPatternDetector()
        text = "## 見積書\n\n| 項目 | 金額 |\n|---|---:|\n| 実装 | 100 |\n"
        result = detector.detect_all(text)
        self.assertEqual(result.doc_type, "structured")
        p1 = result.pattern_results[0]
        self.assertFalse(any(m.pattern_name == "見出しマーカー" for m in p1.matches))


class TestPattern6DesignDocVsMetaphor(unittest.TestCase):
    """Pattern 6: avoid literal '設計書' false positives while keeping metaphor detection."""

    def test_literal_design_doc_title_not_detected(self):
        detector = AIPatternDetector(doc_type="structured")
        text = "## 在庫連携バッチ 設計書（概要）\n本文です。"
        result = detector.detect_all(text)
        p6 = result.pattern_results[5]
        self.assertFalse(
            any(m.pattern_name == "設計書/青写真" for m in p6.matches),
            "Literal document title containing 設計書 should not be flagged as stock metaphor",
        )

    def test_metaphorical_designbook_detected(self):
        detector = AIPatternDetector()
        text = "この方針は現場改革の設計書となります。"
        result = detector.detect_all(text)
        p6 = result.pattern_results[5]
        self.assertTrue(
            any(m.pattern_name == "設計書/青写真" for m in p6.matches),
            "Metaphorical use like '〜の設計書となる' should be detected",
        )

    def test_blueprint_detected(self):
        detector = AIPatternDetector()
        text = "この計画は次の3年の青写真です。"
        result = detector.detect_all(text)
        p6 = result.pattern_results[5]
        self.assertTrue(
            any(m.pattern_name == "設計書/青写真" for m in p6.matches),
            "青写真 should continue to be detected",
        )


class TestPattern4SmokeTests(unittest.TestCase):
    """Smoke tests — existing Pattern 4 hedge detection should not break."""

    def setUp(self):
        self.detector = AIPatternDetector()

    def test_hedge_word_detected(self):
        text = "これはかもしれません。"
        result = self.detector.detect_all(text)
        p4 = result.pattern_results[3]
        self.assertTrue(any(m.pattern_name == "ヘッジ語" for m in p4.matches))

    def test_existing_disclaimer_detected(self):
        text = "ケースバイケースで対応します。状況によって異なります。"
        result = self.detector.detect_all(text)
        p4 = result.pattern_results[3]
        self.assertTrue(any(m.pattern_name == "免責表現" for m in p4.matches))


# ===== NEW FEATURE TESTS (initially RED, then GREEN) =====


class TestPattern1NestedQuotation(unittest.TestCase):
    """Pattern 1: Nested quotation marks detection."""

    def setUp(self):
        self.detector = AIPatternDetector()

    def test_nested_quotation_detected(self):
        text = "彼が「これは『重要だ』と言った」と述べた。"
        result = self.detector.detect_all(text)
        p1 = result.pattern_results[0]
        self.assertTrue(
            any(m.pattern_name == "入れ子引用符" for m in p1.matches),
            "Nested quotation marks should be detected",
        )

    def test_normal_quotation_not_detected(self):
        text = "彼が「これは重要だ」と述べた。"
        result = self.detector.detect_all(text)
        p1 = result.pattern_results[0]
        self.assertFalse(
            any(m.pattern_name == "入れ子引用符" for m in p1.matches),
            "Normal quotation marks should NOT be detected as nested",
        )


class TestPattern3ExhaustiveListing(unittest.TestCase):
    """Pattern 3: Exhaustive listing detection (3+ items, 2+ occurrences)."""

    def setUp(self):
        self.detector = AIPatternDetector()

    def test_exhaustive_listing_detected(self):
        text = (
            "戦略的な計画、組織的な実行、継続的な改善が必要です。\n\n"
            "品質管理、コスト削減、納期短縮を実現しました。"
        )
        result = self.detector.detect_all(text)
        p3 = result.pattern_results[2]
        self.assertTrue(
            any(m.pattern_name == "網羅的列挙" for m in p3.matches),
            "Exhaustive listing (3+ items, 2+ times) should be detected",
        )

    def test_single_listing_not_detected(self):
        text = "戦略的な計画、組織的な実行、継続的な改善が必要です。\n\nそれ以外は問題ありません。"
        result = self.detector.detect_all(text)
        p3 = result.pattern_results[2]
        self.assertFalse(
            any(m.pattern_name == "網羅的列挙" for m in p3.matches),
            "Single listing occurrence should NOT be detected",
        )


class TestPattern4DisclaimerExpression(unittest.TestCase):
    """Pattern 4: Missing disclaimer expression detection."""

    def setUp(self):
        self.detector = AIPatternDetector()

    def test_personal_opinion_disclaimer_detected(self):
        text = "これは個人の見解であり、会社の方針ではありません。"
        result = self.detector.detect_all(text)
        p4 = result.pattern_results[3]
        self.assertTrue(
            any(m.pattern_name == "免責表現" for m in p4.matches),
            "'個人の見解であり' should be detected as disclaimer",
        )


class TestPattern5Buzzwords(unittest.TestCase):
    """Pattern 5: Buzzword detection."""

    def setUp(self):
        self.detector = AIPatternDetector()

    def test_buzzword_detected(self):
        text = "シナジーを活かしてレバレッジを効かせます。"
        result = self.detector.detect_all(text)
        p5 = result.pattern_results[4]
        buzzword_matches = [m for m in p5.matches if m.pattern_name == "バズワード"]
        self.assertTrue(
            len(buzzword_matches) >= 2,
            "Buzzwords (シナジー, レバレッジ) should be detected",
        )

    def test_normal_words_not_detected_as_buzzwords(self):
        text = "会議で議論しました。プロジェクトは順調です。"
        result = self.detector.detect_all(text)
        p5 = result.pattern_results[4]
        self.assertFalse(
            any(m.pattern_name == "バズワード" for m in p5.matches),
            "Normal words should NOT be detected as buzzwords",
        )


class TestPattern2ConjunctionInSentence(unittest.TestCase):
    """Pattern 2: Conjunction detection within a single line (mid-sentence)."""

    def setUp(self):
        self.detector = AIPatternDetector()

    def test_mid_sentence_conjunction_detected(self):
        text = "これは重要です。また、次の点も重要です。"
        result = self.detector.detect_all(text)
        p2 = result.pattern_results[1]
        self.assertTrue(
            any(m.pattern_name == "接続詞開始" for m in p2.matches),
            "Conjunction after period on the same line should be detected",
        )


class TestPattern4ParagraphNeutrality(unittest.TestCase):
    """Pattern 4: Forced neutrality at paragraph level (across lines)."""

    def setUp(self):
        self.detector = AIPatternDetector()

    def test_forced_neutrality_across_lines_in_paragraph(self):
        text = "一方で賛成意見もあります。\n他方では反対意見もあります。"
        result = self.detector.detect_all(text)
        p4 = result.pattern_results[3]
        self.assertTrue(
            any(m.pattern_name == "強制中立" for m in p4.matches),
            "Forced neutrality across lines in same paragraph should be detected",
        )

    def test_neutrality_in_different_paragraphs_not_detected(self):
        text = "一方で賛成意見もあります。\n\n他方では反対意見もあります。"
        result = self.detector.detect_all(text)
        p4 = result.pattern_results[3]
        self.assertFalse(
            any(m.pattern_name == "強制中立" for m in p4.matches),
            "Neutral patterns in DIFFERENT paragraphs should NOT be detected",
        )


class TestPattern4SamePatternTwice(unittest.TestCase):
    """Pattern 4: Same neutral pattern appearing twice in same paragraph."""

    def setUp(self):
        self.detector = AIPatternDetector()

    def test_same_pattern_twice_detected(self):
        text = "一方で効率が上がります。一方でコストも増えます。"
        result = self.detector.detect_all(text)
        p4 = result.pattern_results[3]
        self.assertTrue(
            any(m.pattern_name == "強制中立" for m in p4.matches),
            "Same neutral pattern (一方で) appearing twice should be detected",
        )


if __name__ == "__main__":
    unittest.main()
