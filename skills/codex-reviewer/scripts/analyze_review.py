#!/usr/bin/env python3
"""
Review Result Analyzer

Codexによるレビュー結果を分析・要約するスクリプト。
レビュー結果ファイルから問題点、アクションアイテム、要約を抽出します。

Usage:
    python3 analyze_review.py --input ./reviews/code_review_xxx.md --format summary
    python3 analyze_review.py --input ./reviews/code_review_xxx.md --format issues
    python3 analyze_review.py --input ./reviews/code_review_xxx.md --format all
"""

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class ReviewIssue:
    """レビュー指摘事項"""

    severity: str  # Critical, High, Medium, Low
    category: str
    location: str
    problem: str
    recommendation: str
    raw_text: str = ""


@dataclass
class ReviewAnalysis:
    """レビュー分析結果"""

    total_issues: int = 0
    issues_by_severity: Dict[str, int] = field(default_factory=dict)
    issues_by_category: Dict[str, int] = field(default_factory=dict)
    issues: List[ReviewIssue] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    summary: str = ""
    raw_content: str = ""


def read_review_file(file_path: str) -> str:
    """レビューファイルを読み込む"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_severity(text: str) -> str:
    """重要度を正規化"""
    text_lower = text.lower().strip()
    if "critical" in text_lower:
        return "Critical"
    elif "high" in text_lower:
        return "High"
    elif "medium" in text_lower:
        return "Medium"
    elif "low" in text_lower:
        return "Low"
    return "Unknown"


def extract_issues(content: str) -> List[ReviewIssue]:
    """レビュー内容から指摘事項を抽出"""
    issues = []

    # パターン1: 構造化された形式（複数行対応）
    # **重要度**: Critical
    # **カテゴリ**: セキュリティ
    # **場所**: file.py:10
    # **問題**: 説明（複数行可）
    # **推奨**: 改善案（複数行可）
    #
    # 各フィールドは次のフィールド開始または空行/リストアイテムまで非貪欲にマッチ
    structured_pattern = r"\*\*重要度\*\*:\s*(.+?)\s*\n\s*\*\*カテゴリ\*\*:\s*(.+?)\s*\n\s*\*\*場所\*\*:\s*(.+?)\s*\n\s*\*\*問題\*\*:\s*(.+?)\s*\n\s*\*\*推奨\*\*:\s*(.+?)(?=\n\n|\n-\s*\*\*重要度|\Z)"

    for match in re.finditer(structured_pattern, content, re.MULTILINE | re.DOTALL):
        issues.append(
            ReviewIssue(
                severity=parse_severity(match.group(1)),
                category=match.group(2).strip(),
                location=match.group(3).strip(),
                problem=match.group(4).strip(),
                recommendation=match.group(5).strip(),
                raw_text=match.group(0),
            )
        )

    # パターン2: 英語形式（複数行対応）
    # **Severity**: Critical
    # **Category**: Security
    # **Location**: file.py:10
    # **Problem**: description (multiline supported)
    # **Recommendation**: suggestion (multiline supported)
    english_pattern = r"\*\*Severity\*\*:\s*(.+?)\s*\n\s*\*\*Category\*\*:\s*(.+?)\s*\n\s*\*\*Location\*\*:\s*(.+?)\s*\n\s*\*\*Problem\*\*:\s*(.+?)\s*\n\s*\*\*Recommendation\*\*:\s*(.+?)(?=\n\n|\n-\s*\*\*Severity|\Z)"

    for match in re.finditer(english_pattern, content, re.MULTILINE | re.IGNORECASE | re.DOTALL):
        issues.append(
            ReviewIssue(
                severity=parse_severity(match.group(1)),
                category=match.group(2).strip(),
                location=match.group(3).strip(),
                problem=match.group(4).strip(),
                recommendation=match.group(5).strip(),
                raw_text=match.group(0),
            )
        )

    # パターン3: リスト形式
    # - Critical: セキュリティ問題 (file.py:10) - 説明
    list_pattern = r"-\s*(Critical|High|Medium|Low):\s*([^(]+)\s*\(([^)]+)\)\s*-\s*(.+)"

    for match in re.finditer(list_pattern, content, re.MULTILINE | re.IGNORECASE):
        issues.append(
            ReviewIssue(
                severity=parse_severity(match.group(1)),
                category=match.group(2).strip(),
                location=match.group(3).strip(),
                problem=match.group(4).strip(),
                recommendation="",
                raw_text=match.group(0),
            )
        )

    # パターン4: ヘッダーベース
    # ### Critical: タイトル
    header_pattern = r"###\s*(Critical|High|Medium|Low)[:\s]+([^\n]+)"

    for match in re.finditer(header_pattern, content, re.MULTILINE | re.IGNORECASE):
        issues.append(
            ReviewIssue(
                severity=parse_severity(match.group(1)),
                category="General",
                location="",
                problem=match.group(2).strip(),
                recommendation="",
                raw_text=match.group(0),
            )
        )

    return issues


def extract_action_items(content: str) -> List[str]:
    """アクションアイテムを抽出"""
    action_items = []

    # パターン1: チェックリスト形式
    # - [ ] アクション
    # - [ ] TODO: アクション
    checkbox_pattern = r"-\s*\[\s*\]\s*(?:TODO:?\s*)?(.+)"
    for match in re.finditer(checkbox_pattern, content, re.MULTILINE):
        action_items.append(match.group(1).strip())

    # パターン2: 推奨アクション
    # **推奨**: アクション
    recommendation_pattern = r"\*\*(?:推奨|Recommendation|アクション|Action)\*\*:\s*(.+)"
    for match in re.finditer(recommendation_pattern, content, re.MULTILINE | re.IGNORECASE):
        action_items.append(match.group(1).strip())

    # パターン3: アクションアイテムセクション
    action_section_pattern = r"##\s*(?:アクションアイテム|Action Items|TODO)[^\n]*\n((?:[-*]\s*.+\n?)+)"
    for match in re.finditer(action_section_pattern, content, re.MULTILINE | re.IGNORECASE):
        items = re.findall(r"[-*]\s*(.+)", match.group(1))
        action_items.extend([item.strip() for item in items])

    # 重複を除去
    return list(dict.fromkeys(action_items))


def analyze_review(content: str) -> ReviewAnalysis:
    """レビュー内容を分析"""
    issues = extract_issues(content)
    action_items = extract_action_items(content)

    # 重要度別カウント
    severity_counts = Counter(issue.severity for issue in issues)

    # カテゴリ別カウント
    category_counts = Counter(issue.category for issue in issues)

    # 要約の生成
    summary_parts = []
    summary_parts.append(f"合計 {len(issues)} 件の指摘事項を検出しました。")

    if severity_counts:
        severity_str = ", ".join(
            f"{sev}: {count}件"
            for sev, count in sorted(
                severity_counts.items(),
                key=lambda x: (
                    ["Critical", "High", "Medium", "Low", "Unknown"].index(x[0])
                    if x[0] in ["Critical", "High", "Medium", "Low", "Unknown"]
                    else 99
                ),
            )
        )
        summary_parts.append(f"重要度別: {severity_str}")

    if category_counts:
        top_categories = category_counts.most_common(3)
        category_str = ", ".join(f"{cat}: {count}件" for cat, count in top_categories)
        summary_parts.append(f"主なカテゴリ: {category_str}")

    if action_items:
        summary_parts.append(f"アクションアイテム: {len(action_items)}件")

    return ReviewAnalysis(
        total_issues=len(issues),
        issues_by_severity=dict(severity_counts),
        issues_by_category=dict(category_counts),
        issues=issues,
        action_items=action_items,
        summary="\n".join(summary_parts),
        raw_content=content,
    )


def format_summary(analysis: ReviewAnalysis) -> str:
    """要約形式で出力"""
    output = []
    output.append("# レビュー結果サマリー")
    output.append("")
    output.append("## 概要")
    output.append(analysis.summary)
    output.append("")

    if analysis.issues_by_severity:
        output.append("## 重要度別分布")
        for severity in ["Critical", "High", "Medium", "Low", "Unknown"]:
            count = analysis.issues_by_severity.get(severity, 0)
            if count > 0:
                bar = "█" * count
                output.append(f"- **{severity}**: {count}件 {bar}")
        output.append("")

    if analysis.issues_by_category:
        output.append("## カテゴリ別分布")
        for category, count in sorted(analysis.issues_by_category.items(), key=lambda x: -x[1]):
            output.append(f"- **{category}**: {count}件")
        output.append("")

    # Critical/High の問題をハイライト
    critical_high = [i for i in analysis.issues if i.severity in ["Critical", "High"]]
    if critical_high:
        output.append("## 要対応（Critical/High）")
        for i, issue in enumerate(critical_high, 1):
            output.append(f"### {i}. [{issue.severity}] {issue.category}")
            if issue.location:
                output.append(f"- 場所: `{issue.location}`")
            output.append(f"- 問題: {issue.problem}")
            if issue.recommendation:
                output.append(f"- 推奨: {issue.recommendation}")
            output.append("")

    return "\n".join(output)


def format_issues(analysis: ReviewAnalysis) -> str:
    """問題点リスト形式で出力"""
    output = []
    output.append("# レビュー指摘事項リスト")
    output.append("")

    for severity in ["Critical", "High", "Medium", "Low", "Unknown"]:
        issues = [i for i in analysis.issues if i.severity == severity]
        if issues:
            output.append(f"## {severity} ({len(issues)}件)")
            output.append("")
            for i, issue in enumerate(issues, 1):
                output.append(f"### {i}. {issue.category}")
                if issue.location:
                    output.append(f"- **場所**: `{issue.location}`")
                output.append(f"- **問題**: {issue.problem}")
                if issue.recommendation:
                    output.append(f"- **推奨**: {issue.recommendation}")
                output.append("")

    return "\n".join(output)


def format_actions(analysis: ReviewAnalysis) -> str:
    """アクションアイテム形式で出力"""
    output = []
    output.append("# アクションアイテム")
    output.append("")

    if analysis.action_items:
        for i, item in enumerate(analysis.action_items, 1):
            output.append(f"- [ ] {item}")
        output.append("")

    # Critical/Highの推奨事項もアクションとして追加
    critical_high = [i for i in analysis.issues if i.severity in ["Critical", "High"] and i.recommendation]
    if critical_high:
        output.append("## 優先対応事項（レビュー指摘より）")
        output.append("")
        for issue in critical_high:
            output.append(f"- [ ] [{issue.severity}] {issue.recommendation}")
            if issue.location:
                output.append(f"  - 対象: `{issue.location}`")

    return "\n".join(output)


def format_json(analysis: ReviewAnalysis) -> str:
    """JSON形式で出力"""
    data = {
        "summary": {
            "total_issues": analysis.total_issues,
            "issues_by_severity": analysis.issues_by_severity,
            "issues_by_category": analysis.issues_by_category,
            "action_items_count": len(analysis.action_items),
        },
        "issues": [
            {
                "severity": i.severity,
                "category": i.category,
                "location": i.location,
                "problem": i.problem,
                "recommendation": i.recommendation,
            }
            for i in analysis.issues
        ],
        "action_items": analysis.action_items,
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def format_all(analysis: ReviewAnalysis) -> str:
    """全形式で出力"""
    output = []
    output.append(format_summary(analysis))
    output.append("\n---\n")
    output.append(format_issues(analysis))
    output.append("\n---\n")
    output.append(format_actions(analysis))
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Codexレビュー結果を分析・要約",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # 要約を表示
  python3 analyze_review.py --input ./reviews/code_review_xxx.md --format summary

  # 問題点リストを表示
  python3 analyze_review.py --input ./reviews/code_review_xxx.md --format issues

  # アクションアイテムを抽出
  python3 analyze_review.py --input ./reviews/code_review_xxx.md --format actions

  # JSON形式で出力
  python3 analyze_review.py --input ./reviews/code_review_xxx.md --format json

  # 全形式で出力してファイルに保存
  python3 analyze_review.py --input ./reviews/code_review_xxx.md --format all --output analysis.md
        """,
    )

    parser.add_argument("--input", "-i", required=True, help="レビュー結果ファイルのパス")

    parser.add_argument(
        "--format",
        "-f",
        choices=["summary", "issues", "actions", "json", "all"],
        default="summary",
        help="出力形式（デフォルト: summary）",
    )

    parser.add_argument("--output", "-o", help="出力ファイルパス（指定しない場合は標準出力）")

    args = parser.parse_args()

    try:
        # ファイル読み込み
        content = read_review_file(args.input)

        # 分析実行
        analysis = analyze_review(content)

        # フォーマット選択
        formatters = {
            "summary": format_summary,
            "issues": format_issues,
            "actions": format_actions,
            "json": format_json,
            "all": format_all,
        }

        result = formatters[args.format](analysis)

        # 出力
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"分析結果を保存しました: {args.output}")
        else:
            print(result)

    except FileNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
