#!/usr/bin/env python3
"""
Exploratory Data Profiler

データセットの基本プロファイリングを実行し、
探索的検証の出発点となる情報を収集する。
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
import json


def normalize_id(id_val) -> Optional[str]:
    """ID値を正規化（float .0サフィックス対応）"""
    if pd.isna(id_val):
        return None
    return str(id_val).replace('.0', '').strip()


def profile_dataframe(df: pd.DataFrame, name: str = "Dataset") -> Dict[str, Any]:
    """
    DataFrameの包括的なプロファイルを生成

    Args:
        df: 分析対象のDataFrame
        name: データセット名

    Returns:
        プロファイル情報の辞書
    """
    profile = {
        "name": name,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": {},
        "quality_metrics": {},
        "potential_issues": []
    }

    # カラム別分析
    for col in df.columns:
        col_profile = analyze_column(df[col], col)
        profile["columns"][col] = col_profile

        # 潜在的問題の検出
        issues = detect_column_issues(col_profile, col)
        profile["potential_issues"].extend(issues)

    # 全体的な品質メトリクス
    profile["quality_metrics"] = calculate_quality_metrics(df, profile["columns"])

    return profile


def analyze_column(series: pd.Series, col_name: str) -> Dict[str, Any]:
    """
    単一カラムの詳細分析

    Args:
        series: 分析対象のSeries
        col_name: カラム名

    Returns:
        カラムプロファイルの辞書
    """
    col_profile = {
        "dtype": str(series.dtype),
        "non_null_count": series.notna().sum(),
        "null_count": series.isna().sum(),
        "null_percentage": series.isna().mean() * 100,
        "unique_count": series.nunique(),
        "unique_percentage": series.nunique() / len(series) * 100 if len(series) > 0 else 0
    }

    # 文字列型の追加分析
    if series.dtype == 'object':
        col_profile["empty_string_count"] = (series == '').sum()
        col_profile["na_string_count"] = series.str.upper().isin(['N/A', 'NA', 'NULL', 'NONE', '']).sum()

        # 最頻値
        if series.notna().any():
            value_counts = series.value_counts()
            col_profile["top_values"] = value_counts.head(5).to_dict()
            col_profile["top_concentration"] = value_counts.iloc[0] / len(series) * 100 if len(value_counts) > 0 else 0

    # 数値型の追加分析
    elif np.issubdtype(series.dtype, np.number):
        col_profile["min"] = series.min()
        col_profile["max"] = series.max()
        col_profile["mean"] = series.mean()
        col_profile["median"] = series.median()
        col_profile["std"] = series.std()
        col_profile["zero_count"] = (series == 0).sum()
        col_profile["negative_count"] = (series < 0).sum()

    # 日付型の追加分析
    elif pd.api.types.is_datetime64_any_dtype(series):
        col_profile["min_date"] = str(series.min())
        col_profile["max_date"] = str(series.max())

    return col_profile


def detect_column_issues(col_profile: Dict, col_name: str) -> List[Dict]:
    """
    カラムプロファイルから潜在的問題を検出

    Args:
        col_profile: カラムプロファイル
        col_name: カラム名

    Returns:
        検出した問題のリスト
    """
    issues = []

    # 高いNULL率
    if col_profile["null_percentage"] > 50:
        issues.append({
            "column": col_name,
            "issue": "HIGH_NULL_RATE",
            "severity": "MEDIUM",
            "detail": f"{col_profile['null_percentage']:.1f}% of values are NULL"
        })

    # 極端な集中
    if "top_concentration" in col_profile and col_profile["top_concentration"] > 50:
        issues.append({
            "column": col_name,
            "issue": "VALUE_CONCENTRATION",
            "severity": "LOW",
            "detail": f"Top value represents {col_profile['top_concentration']:.1f}% of records"
        })

    # 一意性の問題（ID列の疑い）
    if col_profile["unique_percentage"] > 95 and col_profile["unique_percentage"] < 100:
        if any(keyword in col_name.lower() for keyword in ['id', 'key', 'code', 'external']):
            issues.append({
                "column": col_name,
                "issue": "POTENTIAL_DUPLICATE_IDS",
                "severity": "HIGH",
                "detail": f"Column appears to be an ID but has {100 - col_profile['unique_percentage']:.2f}% duplicates"
            })

    return issues


def calculate_quality_metrics(df: pd.DataFrame, columns_profile: Dict) -> Dict[str, Any]:
    """
    全体的なデータ品質メトリクスを計算

    Args:
        df: 対象DataFrame
        columns_profile: カラム別プロファイル

    Returns:
        品質メトリクスの辞書
    """
    total_cells = len(df) * len(df.columns)
    null_cells = df.isna().sum().sum()

    metrics = {
        "completeness": (1 - null_cells / total_cells) * 100 if total_cells > 0 else 0,
        "columns_with_nulls": sum(1 for c in columns_profile.values() if c["null_count"] > 0),
        "columns_all_null": sum(1 for c in columns_profile.values() if c["null_percentage"] == 100),
        "columns_all_unique": sum(1 for c in columns_profile.values() if c["unique_percentage"] == 100)
    }

    return metrics


def validate_reference_integrity(
    detail_df: pd.DataFrame,
    master_df: pd.DataFrame,
    ref_col: str,
    master_id_col: str,
    detail_name: str = "Detail",
    master_name: str = "Master"
) -> Dict[str, Any]:
    """
    参照整合性を検証

    Args:
        detail_df: 参照元DataFrame
        master_df: 参照先DataFrame
        ref_col: 参照元のカラム名
        master_id_col: 参照先のIDカラム名
        detail_name: 参照元の名前
        master_name: 参照先の名前

    Returns:
        検証結果の辞書
    """
    # ID正規化
    detail_refs = detail_df[ref_col].apply(normalize_id).dropna()
    master_ids = set(master_df[master_id_col].apply(normalize_id).dropna())

    valid_refs = detail_refs[detail_refs.isin(master_ids)]
    orphan_refs = detail_refs[~detail_refs.isin(master_ids)]

    return {
        "detail_name": detail_name,
        "master_name": master_name,
        "total_references": len(detail_refs),
        "valid_count": len(valid_refs),
        "orphan_count": len(orphan_refs),
        "validity_rate": len(valid_refs) / len(detail_refs) * 100 if len(detail_refs) > 0 else 100,
        "orphan_samples": list(orphan_refs.head(10))
    }


def analyze_distribution(df: pd.DataFrame, column: str, top_n: int = 10) -> Dict[str, Any]:
    """
    カテゴリカルカラムの分布を分析

    Args:
        df: 対象DataFrame
        column: 分析するカラム名
        top_n: 上位N件

    Returns:
        分布分析結果
    """
    value_counts = df[column].value_counts()
    total = len(df)

    distribution = []
    cumulative = 0
    for val, count in value_counts.head(top_n).items():
        pct = count / total * 100
        cumulative += pct
        distribution.append({
            "value": str(val),
            "count": int(count),
            "percentage": round(pct, 2),
            "cumulative": round(cumulative, 2)
        })

    return {
        "column": column,
        "total_records": total,
        "unique_values": len(value_counts),
        "null_count": df[column].isna().sum(),
        "top_n": top_n,
        "distribution": distribution,
        "concentration_top_3": value_counts.head(3).sum() / total * 100 if total > 0 else 0
    }


def generate_profile_report(profile: Dict[str, Any]) -> str:
    """
    プロファイル結果をMarkdown形式のレポートに変換

    Args:
        profile: プロファイル辞書

    Returns:
        Markdownレポート文字列
    """
    lines = [
        f"# Data Profile: {profile['name']}",
        "",
        "## Overview",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Rows | {profile['row_count']:,} |",
        f"| Total Columns | {profile['column_count']} |",
        f"| Completeness | {profile['quality_metrics']['completeness']:.1f}% |",
        f"| Columns with NULLs | {profile['quality_metrics']['columns_with_nulls']} |",
        "",
        "## Potential Issues",
        ""
    ]

    if profile["potential_issues"]:
        lines.append("| Column | Issue | Severity | Detail |")
        lines.append("|--------|-------|:--------:|--------|")
        for issue in profile["potential_issues"]:
            lines.append(f"| {issue['column']} | {issue['issue']} | {issue['severity']} | {issue['detail']} |")
    else:
        lines.append("No potential issues detected.")

    lines.extend([
        "",
        "## Column Details",
        ""
    ])

    for col_name, col_info in profile["columns"].items():
        lines.append(f"### {col_name}")
        lines.append(f"- Type: `{col_info['dtype']}`")
        lines.append(f"- Non-null: {col_info['non_null_count']:,} ({100 - col_info['null_percentage']:.1f}%)")
        lines.append(f"- Unique: {col_info['unique_count']:,} ({col_info['unique_percentage']:.1f}%)")

        if "top_values" in col_info:
            lines.append(f"- Top values: {list(col_info['top_values'].keys())[:3]}")

        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # 使用例
    import sys

    if len(sys.argv) < 2:
        print("Usage: python exploratory_profiler.py <excel_file>")
        print("\nExample:")
        print("  python exploratory_profiler.py data.xlsx")
        sys.exit(1)

    file_path = sys.argv[1]
    df = pd.read_excel(file_path)

    profile = profile_dataframe(df, Path(file_path).stem)
    report = generate_profile_report(profile)
    print(report)
