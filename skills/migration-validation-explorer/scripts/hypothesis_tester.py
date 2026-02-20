#!/usr/bin/env python3
"""
Hypothesis Tester

仮説検証のためのユーティリティ関数群。
探索的検証の自動化を支援する。
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import pandas as pd


class HypothesisStatus(Enum):
    PENDING = "pending"
    TESTING = "testing"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    ISSUE_FOUND = "issue_found"


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class Hypothesis:
    """仮説を表すデータクラス"""

    id: str
    perspective: str  # 🏢, 💻, 🔍, 📊
    description: str
    impact: int  # 1-3
    probability: int  # 1-3
    testability: int  # 1-3
    status: HypothesisStatus = HypothesisStatus.PENDING
    test_query: Optional[str] = None
    result: Optional[Dict] = None
    tested_at: Optional[datetime] = None

    @property
    def priority_score(self) -> int:
        """優先度スコアを計算（1-27）"""
        return self.impact * self.probability * self.testability


@dataclass
class TestResult:
    """検証結果を表すデータクラス"""

    hypothesis_id: str
    status: HypothesisStatus
    total_records: int
    issue_records: int
    issue_rate: float
    severity: Optional[Severity]
    evidence: Any
    root_cause: Optional[str] = None
    recommendation: Optional[str] = None


def normalize_id(id_val) -> Optional[str]:
    """ID値を正規化"""
    if pd.isna(id_val):
        return None
    return str(id_val).replace(".0", "").strip()


# 汎用テスト関数群


def test_null_rate(df: pd.DataFrame, column: str, threshold: float = 0.05) -> TestResult:
    """
    NULL率のテスト

    Args:
        df: 対象DataFrame
        column: テスト対象カラム
        threshold: 許容閾値（デフォルト5%）

    Returns:
        TestResult
    """
    total = len(df)
    null_count = df[column].isna().sum()
    null_rate = null_count / total if total > 0 else 0

    if null_rate > threshold:
        status = HypothesisStatus.ISSUE_FOUND
        severity = Severity.HIGH if null_rate > 0.5 else Severity.MEDIUM if null_rate > 0.1 else Severity.LOW
    else:
        status = HypothesisStatus.REJECTED
        severity = None

    return TestResult(
        hypothesis_id=f"null_rate_{column}",
        status=status,
        total_records=total,
        issue_records=null_count,
        issue_rate=null_rate * 100,
        severity=severity,
        evidence={"null_count": null_count, "threshold": threshold},
    )


def test_uniqueness(df: pd.DataFrame, column: str, expected_unique: bool = True) -> TestResult:
    """
    一意性のテスト

    Args:
        df: 対象DataFrame
        column: テスト対象カラム
        expected_unique: 一意であるべきか

    Returns:
        TestResult
    """
    total = len(df)
    duplicates = df[df.duplicated(subset=[column], keep=False)]
    dup_count = len(duplicates)
    unique_count = df[column].nunique()

    if expected_unique and dup_count > 0:
        status = HypothesisStatus.ISSUE_FOUND
        severity = Severity.HIGH
    else:
        status = HypothesisStatus.REJECTED
        severity = None

    return TestResult(
        hypothesis_id=f"uniqueness_{column}",
        status=status,
        total_records=total,
        issue_records=dup_count,
        issue_rate=dup_count / total * 100 if total > 0 else 0,
        severity=severity,
        evidence={
            "unique_count": unique_count,
            "duplicate_groups": df[column].value_counts()[df[column].value_counts() > 1].to_dict(),
        },
    )


def test_reference_integrity(
    detail_df: pd.DataFrame, master_df: pd.DataFrame, ref_col: str, master_id_col: str, tolerance: float = 0.01
) -> TestResult:
    """
    参照整合性のテスト

    Args:
        detail_df: 参照元DataFrame
        master_df: 参照先DataFrame
        ref_col: 参照カラム名
        master_id_col: マスターIDカラム名
        tolerance: 許容孤児率（デフォルト1%）

    Returns:
        TestResult
    """
    detail_refs = detail_df[ref_col].apply(normalize_id).dropna()
    master_ids = set(master_df[master_id_col].apply(normalize_id).dropna())

    total = len(detail_refs)
    orphans = detail_refs[~detail_refs.isin(master_ids)]
    orphan_count = len(orphans)
    orphan_rate = orphan_count / total if total > 0 else 0

    if orphan_rate > tolerance:
        status = HypothesisStatus.ISSUE_FOUND
        severity = Severity.HIGH if orphan_rate > 0.1 else Severity.MEDIUM
    else:
        status = HypothesisStatus.REJECTED
        severity = None

    return TestResult(
        hypothesis_id=f"ref_integrity_{ref_col}",
        status=status,
        total_records=total,
        issue_records=orphan_count,
        issue_rate=orphan_rate * 100,
        severity=severity,
        evidence={"orphan_samples": list(orphans.head(10)), "tolerance": tolerance},
    )


def test_value_concentration(df: pd.DataFrame, column: str, threshold: float = 0.5) -> TestResult:
    """
    値の集中度テスト

    Args:
        df: 対象DataFrame
        column: テスト対象カラム
        threshold: 集中度閾値（デフォルト50%）

    Returns:
        TestResult
    """
    total = len(df)
    value_counts = df[column].value_counts()

    if len(value_counts) == 0:
        return TestResult(
            hypothesis_id=f"concentration_{column}",
            status=HypothesisStatus.REJECTED,
            total_records=total,
            issue_records=0,
            issue_rate=0,
            severity=None,
            evidence={"message": "No values found"},
        )

    top_value = value_counts.index[0]
    top_count = value_counts.iloc[0]
    concentration = top_count / total if total > 0 else 0

    if concentration > threshold:
        status = HypothesisStatus.ISSUE_FOUND
        severity = Severity.MEDIUM if concentration > 0.7 else Severity.LOW
    else:
        status = HypothesisStatus.REJECTED
        severity = None

    return TestResult(
        hypothesis_id=f"concentration_{column}",
        status=status,
        total_records=total,
        issue_records=top_count,
        issue_rate=concentration * 100,
        severity=severity,
        evidence={
            "top_value": str(top_value),
            "top_count": top_count,
            "threshold": threshold,
            "distribution": value_counts.head(5).to_dict(),
        },
    )


def test_consistency(
    df: pd.DataFrame, condition_col: str, condition_value: Any, required_col: str, allow_null: bool = False
) -> TestResult:
    """
    条件付き必須フィールドの整合性テスト

    Args:
        df: 対象DataFrame
        condition_col: 条件カラム
        condition_value: 条件値
        required_col: 必須となるカラム
        allow_null: NULLを許容するか

    Returns:
        TestResult
    """
    subset = df[df[condition_col] == condition_value]
    total = len(subset)

    if allow_null:
        issues = subset[subset[required_col].isna()]
    else:
        issues = subset[subset[required_col].isna() | (subset[required_col] == "")]

    issue_count = len(issues)

    if issue_count > 0:
        status = HypothesisStatus.ISSUE_FOUND
        severity = Severity.HIGH if issue_count / total > 0.1 else Severity.MEDIUM
    else:
        status = HypothesisStatus.REJECTED
        severity = None

    return TestResult(
        hypothesis_id=f"consistency_{condition_col}_{required_col}",
        status=status,
        total_records=total,
        issue_records=issue_count,
        issue_rate=issue_count / total * 100 if total > 0 else 0,
        severity=severity,
        evidence={"condition": f"{condition_col} == {condition_value}", "required_field": required_col},
    )


def test_picklist_values(
    df: pd.DataFrame, column: str, valid_values: List[str], case_sensitive: bool = False
) -> TestResult:
    """
    Picklist値の妥当性テスト

    Args:
        df: 対象DataFrame
        column: テスト対象カラム
        valid_values: 有効な値のリスト
        case_sensitive: 大文字小文字を区別するか

    Returns:
        TestResult
    """
    total = len(df)

    if case_sensitive:
        invalid = df[~df[column].isin(valid_values) & df[column].notna()]
    else:
        valid_lower = [v.lower() for v in valid_values]
        invalid = df[~df[column].str.lower().isin(valid_lower) & df[column].notna()]

    issue_count = len(invalid)
    invalid_values = invalid[column].value_counts().to_dict()

    if issue_count > 0:
        status = HypothesisStatus.ISSUE_FOUND
        severity = Severity.MEDIUM
    else:
        status = HypothesisStatus.REJECTED
        severity = None

    return TestResult(
        hypothesis_id=f"picklist_{column}",
        status=status,
        total_records=total,
        issue_records=issue_count,
        issue_rate=issue_count / total * 100 if total > 0 else 0,
        severity=severity,
        evidence={"valid_values": valid_values, "invalid_values": invalid_values},
    )


def run_test_suite(tests: List[Callable], **kwargs) -> List[TestResult]:
    """
    テストスイートを実行

    Args:
        tests: テスト関数のリスト
        **kwargs: テストに渡す引数

    Returns:
        TestResultのリスト
    """
    results = []
    for test_func in tests:
        try:
            result = test_func(**kwargs)
            results.append(result)
        except Exception as e:
            # エラー時もTestResultとして記録
            results.append(
                TestResult(
                    hypothesis_id=test_func.__name__,
                    status=HypothesisStatus.PENDING,
                    total_records=0,
                    issue_records=0,
                    issue_rate=0,
                    severity=None,
                    evidence={"error": str(e)},
                )
            )
    return results


def generate_test_report(results: List[TestResult]) -> str:
    """
    テスト結果をMarkdownレポートに変換

    Args:
        results: TestResultのリスト

    Returns:
        Markdownレポート文字列
    """
    lines = ["# Hypothesis Test Results", "", "## Summary", "", "| Status | Count |", "|--------|------:|"]

    status_counts = {}
    for r in results:
        status = r.status.value
        status_counts[status] = status_counts.get(status, 0) + 1

    for status, count in status_counts.items():
        lines.append(f"| {status} | {count} |")

    lines.extend(["", "## Issues Found", ""])

    issues = [r for r in results if r.status == HypothesisStatus.ISSUE_FOUND]
    if issues:
        lines.append("| ID | Severity | Issue Rate | Records |")
        lines.append("|-------|:--------:|-----------:|--------:|")
        for issue in sorted(issues, key=lambda x: x.severity.value if x.severity else "Z"):
            lines.append(
                f"| {issue.hypothesis_id} | {issue.severity.value if issue.severity else 'N/A'} | "
                f"{issue.issue_rate:.1f}% | {issue.issue_records:,} |"
            )
    else:
        lines.append("No issues found.")

    lines.extend(["", "## Detailed Results", ""])

    for result in results:
        lines.append(f"### {result.hypothesis_id}")
        lines.append(f"- Status: {result.status.value}")
        lines.append(f"- Total Records: {result.total_records:,}")
        lines.append(f"- Issue Rate: {result.issue_rate:.2f}%")
        if result.severity:
            lines.append(f"- Severity: {result.severity.value}")
        lines.append(f"- Evidence: `{result.evidence}`")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # 使用例
    print("Hypothesis Tester - Usage Examples")
    print("=" * 50)
    print("""
    from hypothesis_tester import *
    import pandas as pd

    df = pd.read_excel('data.xlsx')

    # NULL率テスト
    result = test_null_rate(df, 'OwnerId', threshold=0.05)
    print(f"Status: {result.status.value}")
    print(f"Issue Rate: {result.issue_rate:.1f}%")

    # 参照整合性テスト
    master_df = pd.read_excel('accounts.xlsx')
    result = test_reference_integrity(
        df, master_df,
        ref_col='AccountId',
        master_id_col='Id'
    )

    # レポート生成
    results = [result1, result2, result3]
    report = generate_test_report(results)
    print(report)
    """)
