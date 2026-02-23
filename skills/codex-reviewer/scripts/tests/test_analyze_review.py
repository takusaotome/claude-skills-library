#!/usr/bin/env python3
"""Tests for analyze_review.py"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyze_review import (
    ReviewAnalysis,
    ReviewIssue,
    analyze_review,
    extract_action_items,
    extract_issues,
    format_actions,
    format_issues,
    format_json,
    format_summary,
    parse_severity,
)


class TestParseSeverity:
    """Tests for parse_severity function"""

    def test_critical(self):
        assert parse_severity("Critical") == "Critical"
        assert parse_severity("CRITICAL") == "Critical"
        assert parse_severity("critical") == "Critical"

    def test_high(self):
        assert parse_severity("High") == "High"
        assert parse_severity("HIGH") == "High"

    def test_medium(self):
        assert parse_severity("Medium") == "Medium"
        assert parse_severity("MEDIUM") == "Medium"

    def test_low(self):
        assert parse_severity("Low") == "Low"
        assert parse_severity("LOW") == "Low"

    def test_unknown(self):
        assert parse_severity("Unknown") == "Unknown"
        assert parse_severity("invalid") == "Unknown"


class TestExtractIssues:
    """Tests for extract_issues function"""

    def test_structured_japanese_format(self):
        content = """
- **重要度**: Critical
- **カテゴリ**: セキュリティ
- **場所**: src/auth.py:45
- **問題**: SQLインジェクションの脆弱性があります
- **推奨**: パラメータ化クエリを使用してください

"""
        issues = extract_issues(content)
        assert len(issues) == 1
        assert issues[0].severity == "Critical"
        assert issues[0].category == "セキュリティ"
        assert issues[0].location == "src/auth.py:45"
        assert "SQLインジェクション" in issues[0].problem

    def test_structured_english_format(self):
        content = """
- **Severity**: High
- **Category**: Performance
- **Location**: main.py:100
- **Problem**: N+1 query detected in loop
- **Recommendation**: Use batch loading

"""
        issues = extract_issues(content)
        assert len(issues) == 1
        assert issues[0].severity == "High"
        assert issues[0].category == "Performance"

    def test_list_format(self):
        content = """
- Critical: Security Issue (file.py:10) - SQL injection vulnerability
- High: Performance (utils.py:50) - Inefficient algorithm
"""
        issues = extract_issues(content)
        assert len(issues) == 2
        assert issues[0].severity == "Critical"
        assert issues[1].severity == "High"

    def test_header_format(self):
        content = """
### Critical: Major security vulnerability
### High: Performance bottleneck
"""
        issues = extract_issues(content)
        assert len(issues) == 2

    def test_empty_content(self):
        issues = extract_issues("")
        assert len(issues) == 0


class TestExtractActionItems:
    """Tests for extract_action_items function"""

    def test_checkbox_format(self):
        content = """
- [ ] Fix the security vulnerability
- [ ] TODO: Update dependencies
"""
        actions = extract_action_items(content)
        assert "Fix the security vulnerability" in actions
        assert "Update dependencies" in actions

    def test_recommendation_format(self):
        content = """
**推奨**: Use parameterized queries
**Recommendation**: Enable HTTPS
"""
        actions = extract_action_items(content)
        assert len(actions) >= 2

    def test_action_section(self):
        content = """
## アクションアイテム
- Review security settings
- Update documentation
"""
        actions = extract_action_items(content)
        assert "Review security settings" in actions
        assert "Update documentation" in actions

    def test_deduplication(self):
        content = """
- [ ] Fix bug
- [ ] Fix bug
"""
        actions = extract_action_items(content)
        assert actions.count("Fix bug") == 1


class TestAnalyzeReview:
    """Tests for analyze_review function"""

    def test_complete_analysis(self):
        content = """
- **重要度**: Critical
- **カテゴリ**: セキュリティ
- **場所**: auth.py:10
- **問題**: 脆弱性
- **推奨**: 修正

- **重要度**: High
- **カテゴリ**: パフォーマンス
- **場所**: db.py:20
- **問題**: 遅延
- **推奨**: 最適化

"""
        analysis = analyze_review(content)
        assert analysis.total_issues == 2
        assert analysis.issues_by_severity.get("Critical", 0) == 1
        assert analysis.issues_by_severity.get("High", 0) == 1

    def test_empty_review(self):
        analysis = analyze_review("")
        assert analysis.total_issues == 0
        assert len(analysis.issues) == 0


class TestFormatters:
    """Tests for format functions"""

    @pytest.fixture
    def sample_analysis(self):
        return ReviewAnalysis(
            total_issues=2,
            issues_by_severity={"Critical": 1, "High": 1},
            issues_by_category={"Security": 1, "Performance": 1},
            issues=[
                ReviewIssue(
                    severity="Critical",
                    category="Security",
                    location="auth.py:10",
                    problem="SQL Injection",
                    recommendation="Use parameterized queries",
                ),
                ReviewIssue(
                    severity="High",
                    category="Performance",
                    location="db.py:20",
                    problem="N+1 query",
                    recommendation="Use batch loading",
                ),
            ],
            action_items=["Fix security issue", "Optimize queries"],
            summary="Test summary",
        )

    def test_format_summary(self, sample_analysis):
        result = format_summary(sample_analysis)
        assert "レビュー結果サマリー" in result
        assert "Critical" in result
        assert "High" in result

    def test_format_issues(self, sample_analysis):
        result = format_issues(sample_analysis)
        assert "レビュー指摘事項リスト" in result
        assert "Critical" in result
        assert "Security" in result

    def test_format_actions(self, sample_analysis):
        result = format_actions(sample_analysis)
        assert "アクションアイテム" in result
        assert "[ ]" in result

    def test_format_json(self, sample_analysis):
        import json

        result = format_json(sample_analysis)
        data = json.loads(result)
        assert data["summary"]["total_issues"] == 2
        assert len(data["issues"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
