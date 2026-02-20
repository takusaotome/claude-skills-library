#!/usr/bin/env python3
"""
DuckDB Data Analyzer

データファイルの包括的なプロファイリングと品質分析を行うスクリプト。
CSV、Parquet、JSON等のファイルに対応。

Usage:
    python duckdb_analyzer.py <input_file> [options]

Examples:
    python duckdb_analyzer.py data.csv
    python duckdb_analyzer.py data.parquet --output report.md
    python duckdb_analyzer.py 'data/*.csv' --sample 10000
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import duckdb
except ImportError:
    print("Error: duckdb is not installed. Run: pip install duckdb")
    sys.exit(1)


class DuckDBAnalyzer:
    """DuckDBを使用したデータ分析クラス"""

    def __init__(self, memory_limit: str = "4GB", threads: int = None):
        """
        初期化

        Args:
            memory_limit: メモリ制限（例: '4GB', '8GB'）
            threads: 使用スレッド数（Noneでデフォルト）
        """
        self.con = duckdb.connect()
        self.con.execute(f"SET memory_limit = '{memory_limit}'")
        if threads:
            self.con.execute(f"SET threads = {threads}")

    def analyze_file(
        self, file_path: str, sample_size: Optional[int] = None, output_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        ファイルを分析してプロファイルを生成

        Args:
            file_path: 分析対象ファイルパス（ワイルドカード可）
            sample_size: サンプル行数（統計情報計算用、品質メトリクスは常に全件）
            output_format: 出力形式（'markdown', 'json', 'dict'）

        Returns:
            分析結果の辞書
        """
        # ファイル形式の判定
        file_ext = Path(file_path.replace("*", "x")).suffix.lower()

        # 基本情報の取得（常に全件）
        basic_info = self._get_basic_info(file_path, file_ext)

        # スキーマ情報
        schema_info = self._get_schema_info(file_path, file_ext)

        # 統計情報（サンプル適用可）
        stats_info = self._get_statistics(file_path, file_ext, sample_size)

        # データ品質（常に全件で計算）
        quality_info = self._get_quality_metrics(file_path, file_ext, schema_info)

        # サンプルデータ
        sample_data = self._get_sample_data(file_path, file_ext, 5)

        result = {
            "file_path": file_path,
            "file_format": file_ext.lstrip(".") or "unknown",
            "analysis_timestamp": datetime.now().isoformat(),
            "basic_info": basic_info,
            "schema": schema_info,
            "statistics": stats_info,
            "quality": quality_info,
            "sample_data": sample_data,
            "analysis_config": {"sample_size_for_statistics": sample_size, "quality_metrics_scope": "full_data"},
        }

        if output_format == "markdown":
            return self._to_markdown(result)
        elif output_format == "json":
            return json.dumps(result, indent=2, ensure_ascii=False, default=str)
        else:
            return result

    def _build_read_function(self, file_path: str, file_ext: str) -> str:
        """ファイル形式に応じた読み込み関数を構築"""
        if file_ext in [".parquet", ".pq"]:
            return f"read_parquet('{file_path}', union_by_name=true)"
        elif file_ext == ".json":
            return f"read_json('{file_path}', auto_detect=true)"
        elif file_ext in [".ndjson", ".jsonl"]:
            return f"read_json('{file_path}', format='newline_delimited')"
        elif file_ext in [".csv", ".tsv", ".txt"]:
            delim = "\t" if file_ext == ".tsv" else ","
            return f"read_csv('{file_path}', auto_detect=true, delim='{delim}')"
        else:
            # デフォルトは自動検出
            return f"'{file_path}'"

    def _get_basic_info(self, file_path: str, file_ext: str) -> Dict:
        """基本情報の取得（常に全件）"""
        read_func = self._build_read_function(file_path, file_ext)

        # 総行数（常に全件）
        total_row_count = self.con.execute(f"""
            SELECT COUNT(*) FROM {read_func}
        """).fetchone()[0]

        # 列数
        col_count = len(
            self.con.execute(f"""
            SELECT * FROM {read_func} LIMIT 1
        """).description
        )

        return {"total_row_count": total_row_count, "column_count": col_count}

    def _get_schema_info(self, file_path: str, file_ext: str) -> List[Dict]:
        """スキーマ情報の取得"""
        read_func = self._build_read_function(file_path, file_ext)

        describe_result = self.con.execute(f"""
            DESCRIBE SELECT * FROM {read_func}
        """).fetchall()

        schema = []
        for row in describe_result:
            schema.append({"column_name": row[0], "column_type": row[1], "nullable": row[2] if len(row) > 2 else "YES"})
        return schema

    def _get_statistics(self, file_path: str, file_ext: str, sample_size: Optional[int]) -> Dict:
        """統計情報の取得（サンプル適用可）"""
        read_func = self._build_read_function(file_path, file_ext)
        sample_clause = f"USING SAMPLE {sample_size} ROWS" if sample_size else ""

        # スキーマ取得
        schema = self._get_schema_info(file_path, file_ext)
        stats = {}

        for col in schema:
            col_name = col["column_name"]
            col_type = col["column_type"].upper()

            col_stats = {"type": col_type, "sampled": sample_size is not None}

            # 数値型の統計
            if any(
                t in col_type
                for t in [
                    "INT",
                    "FLOAT",
                    "DOUBLE",
                    "DECIMAL",
                    "NUMERIC",
                    "BIGINT",
                    "SMALLINT",
                    "TINYINT",
                    "HUGEINT",
                    "UBIGINT",
                ]
            ):
                try:
                    numeric_stats = self.con.execute(f"""
                        SELECT
                            MIN("{col_name}") as min_val,
                            MAX("{col_name}") as max_val,
                            AVG("{col_name}") as avg_val,
                            STDDEV("{col_name}") as std_val,
                            MEDIAN("{col_name}") as median_val,
                            COUNT(DISTINCT "{col_name}") as distinct_count
                        FROM {read_func} {sample_clause}
                    """).fetchone()

                    col_stats.update(
                        {
                            "min": numeric_stats[0],
                            "max": numeric_stats[1],
                            "mean": round(numeric_stats[2], 4) if numeric_stats[2] else None,
                            "std": round(numeric_stats[3], 4) if numeric_stats[3] else None,
                            "median": numeric_stats[4],
                            "distinct_count": numeric_stats[5],
                        }
                    )
                except Exception as e:
                    col_stats["error"] = str(e)

            # 文字列型の統計
            elif any(t in col_type for t in ["VARCHAR", "CHAR", "TEXT", "STRING", "BLOB"]):
                try:
                    string_stats = self.con.execute(f"""
                        SELECT
                            COUNT(DISTINCT "{col_name}") as distinct_count,
                            MIN(LENGTH("{col_name}")) as min_len,
                            MAX(LENGTH("{col_name}")) as max_len,
                            AVG(LENGTH("{col_name}")) as avg_len
                        FROM {read_func} {sample_clause}
                    """).fetchone()

                    col_stats.update(
                        {
                            "distinct_count": string_stats[0],
                            "min_length": string_stats[1],
                            "max_length": string_stats[2],
                            "avg_length": round(string_stats[3], 2) if string_stats[3] else None,
                        }
                    )

                    # トップ値
                    top_values = self.con.execute(f"""
                        SELECT "{col_name}", COUNT(*) as cnt
                        FROM {read_func} {sample_clause}
                        WHERE "{col_name}" IS NOT NULL
                        GROUP BY "{col_name}"
                        ORDER BY cnt DESC
                        LIMIT 5
                    """).fetchall()
                    col_stats["top_values"] = [{"value": v[0], "count": v[1]} for v in top_values]
                except Exception as e:
                    col_stats["error"] = str(e)

            # 日付型の統計
            elif any(t in col_type for t in ["DATE", "TIMESTAMP", "TIME", "INTERVAL"]):
                try:
                    date_stats = self.con.execute(f"""
                        SELECT
                            MIN("{col_name}") as min_val,
                            MAX("{col_name}") as max_val,
                            COUNT(DISTINCT "{col_name}") as distinct_count
                        FROM {read_func} {sample_clause}
                    """).fetchone()

                    col_stats.update(
                        {
                            "min": str(date_stats[0]) if date_stats[0] else None,
                            "max": str(date_stats[1]) if date_stats[1] else None,
                            "distinct_count": date_stats[2],
                        }
                    )
                except Exception as e:
                    col_stats["error"] = str(e)

            # BOOLEAN型の統計
            elif "BOOL" in col_type:
                try:
                    bool_stats = self.con.execute(f"""
                        SELECT
                            COUNT(*) FILTER (WHERE "{col_name}" = true) as true_count,
                            COUNT(*) FILTER (WHERE "{col_name}" = false) as false_count,
                            COUNT(*) FILTER (WHERE "{col_name}" IS NULL) as null_count
                        FROM {read_func} {sample_clause}
                    """).fetchone()

                    col_stats.update(
                        {"true_count": bool_stats[0], "false_count": bool_stats[1], "null_count": bool_stats[2]}
                    )
                except Exception as e:
                    col_stats["error"] = str(e)

            # LIST/ARRAY型の統計
            elif any(t in col_type for t in ["LIST", "ARRAY", "[]"]):
                try:
                    list_stats = self.con.execute(f"""
                        SELECT
                            AVG(LEN("{col_name}")) as avg_length,
                            MIN(LEN("{col_name}")) as min_length,
                            MAX(LEN("{col_name}")) as max_length
                        FROM {read_func} {sample_clause}
                        WHERE "{col_name}" IS NOT NULL
                    """).fetchone()

                    col_stats.update(
                        {
                            "avg_list_length": round(list_stats[0], 2) if list_stats[0] else None,
                            "min_list_length": list_stats[1],
                            "max_list_length": list_stats[2],
                        }
                    )
                except Exception as e:
                    col_stats["error"] = str(e)

            # STRUCT/MAP型
            elif any(t in col_type for t in ["STRUCT", "MAP"]):
                col_stats["note"] = "Complex type - detailed statistics not available"

            stats[col_name] = col_stats

        return stats

    def _get_quality_metrics(self, file_path: str, file_ext: str, schema: List[Dict]) -> Dict:
        """データ品質メトリクスの取得（常に全件で計算）"""
        read_func = self._build_read_function(file_path, file_ext)

        quality = {"scope": "full_data", "null_counts": {}, "null_percentages": {}, "completeness": {}}

        # 総行数（常に全件）
        total_rows = self.con.execute(f"""
            SELECT COUNT(*) FROM {read_func}
        """).fetchone()[0]
        quality["total_rows"] = total_rows

        # 各列のNULL情報
        for col in schema:
            col_name = col["column_name"]
            try:
                null_count = self.con.execute(f"""
                    SELECT COUNT(*) FILTER (WHERE "{col_name}" IS NULL)
                    FROM {read_func}
                """).fetchone()[0]

                quality["null_counts"][col_name] = null_count
                quality["null_percentages"][col_name] = (
                    round(100.0 * null_count / total_rows, 2) if total_rows > 0 else 0
                )
                quality["completeness"][col_name] = (
                    round(100.0 * (total_rows - null_count) / total_rows, 2) if total_rows > 0 else 0
                )
            except Exception:
                quality["null_counts"][col_name] = "Error"
                quality["null_percentages"][col_name] = "Error"
                quality["completeness"][col_name] = "Error"

        # 重複行の検出（全列でグループ化）
        try:
            # 全列名を取得してGROUP BYクエリを構築
            column_names = [f'"{col["column_name"]}"' for col in schema]
            columns_str = ", ".join(column_names)

            # 重複行数を正確に計算
            duplicate_result = self.con.execute(f"""
                SELECT COALESCE(SUM(cnt - 1), 0) as duplicate_count
                FROM (
                    SELECT COUNT(*) as cnt
                    FROM {read_func}
                    GROUP BY {columns_str}
                    HAVING COUNT(*) > 1
                ) duplicates
            """).fetchone()

            duplicate_count = duplicate_result[0] if duplicate_result else 0
            quality["duplicate_rows"] = duplicate_count
            quality["duplicate_percentage"] = round(100.0 * duplicate_count / total_rows, 2) if total_rows > 0 else 0
            quality["unique_rows"] = total_rows - duplicate_count
        except Exception as e:
            quality["duplicate_rows"] = "Error"
            quality["duplicate_percentage"] = "Error"
            quality["duplicate_error"] = str(e)

        return quality

    def _get_sample_data(self, file_path: str, file_ext: str, n: int = 5) -> List[Dict]:
        """サンプルデータの取得"""
        read_func = self._build_read_function(file_path, file_ext)

        try:
            df = self.con.execute(f"""
                SELECT * FROM {read_func} LIMIT {n}
            """).fetchdf()
            return df.to_dict(orient="records")
        except Exception:
            return []

    def _to_markdown(self, result: Dict) -> str:
        """結果をMarkdown形式に変換"""
        md = []

        # ヘッダー
        md.append("# Data Profile Report")
        md.append(f"\n**File:** `{result['file_path']}`")
        md.append(f"\n**Format:** {result['file_format']}")
        md.append(f"\n**Generated:** {result['analysis_timestamp']}")

        # 分析設定
        config = result.get("analysis_config", {})
        if config.get("sample_size_for_statistics"):
            md.append(f"\n**Statistics Sample Size:** {config['sample_size_for_statistics']:,} rows")
        md.append(f"\n**Quality Metrics Scope:** {config.get('quality_metrics_scope', 'full_data')}")

        # 基本情報
        md.append("\n## Basic Information")
        md.append("\n| Metric | Value |")
        md.append("|--------|-------|")
        md.append(f"| Total Row Count | {result['basic_info']['total_row_count']:,} |")
        md.append(f"| Column Count | {result['basic_info']['column_count']} |")

        # スキーマ
        md.append("\n## Schema")
        md.append("\n| Column | Type | Nullable |")
        md.append("|--------|------|----------|")
        for col in result["schema"]:
            md.append(f"| {col['column_name']} | {col['column_type']} | {col['nullable']} |")

        # データ品質
        md.append("\n## Data Quality (Full Data)")
        quality = result["quality"]
        md.append("\n> Quality metrics are always calculated on **full data** for accuracy.")
        md.append(f"\n**Total Rows:** {quality.get('total_rows', 'N/A'):,}")

        md.append("\n### Completeness")
        md.append("\n| Column | Null Count | Null % | Completeness % |")
        md.append("|--------|------------|--------|----------------|")
        for col_name in quality["null_counts"]:
            null_count = quality["null_counts"][col_name]
            null_pct = quality["null_percentages"][col_name]
            completeness = quality["completeness"][col_name]
            md.append(f"| {col_name} | {null_count} | {null_pct}% | {completeness}% |")

        md.append("\n### Duplicates")
        if quality.get("duplicate_rows") != "Error":
            md.append(f"\n- **Duplicate Rows:** {quality.get('duplicate_rows', 0):,}")
            md.append(f"- **Duplicate Percentage:** {quality.get('duplicate_percentage', 0)}%")
            md.append(f"- **Unique Rows:** {quality.get('unique_rows', 0):,}")
        else:
            md.append(f"\n- **Error:** {quality.get('duplicate_error', 'Could not calculate duplicates')}")

        # 統計情報
        md.append("\n## Column Statistics")
        sample_note = result.get("analysis_config", {}).get("sample_size_for_statistics")
        if sample_note:
            md.append(f"\n> Statistics below are based on a sample of **{sample_note:,} rows**.")

        for col_name, stats in result["statistics"].items():
            md.append(f"\n### {col_name}")
            md.append(f"\n- **Type:** {stats['type']}")
            if stats.get("sampled"):
                md.append("- **Sampled:** Yes")

            if stats.get("error"):
                md.append(f"- **Error:** {stats['error']}")
                continue

            if "min" in stats:
                md.append(f"- **Min:** {stats['min']}")
            if "max" in stats:
                md.append(f"- **Max:** {stats['max']}")
            if "mean" in stats:
                md.append(f"- **Mean:** {stats['mean']}")
            if "std" in stats:
                md.append(f"- **Std Dev:** {stats['std']}")
            if "median" in stats:
                md.append(f"- **Median:** {stats['median']}")
            if "distinct_count" in stats:
                md.append(f"- **Distinct Values:** {stats['distinct_count']}")
            if "min_length" in stats:
                md.append(
                    f"- **Length (min/avg/max):** {stats['min_length']} / {stats['avg_length']} / {stats['max_length']}"
                )
            if "true_count" in stats:
                md.append(
                    f"- **True/False/Null:** {stats['true_count']} / {stats['false_count']} / {stats['null_count']}"
                )
            if "avg_list_length" in stats:
                md.append(
                    f"- **List Length (min/avg/max):** {stats['min_list_length']} / {stats['avg_list_length']} / {stats['max_list_length']}"
                )
            if "note" in stats:
                md.append(f"- **Note:** {stats['note']}")

            if "top_values" in stats and stats["top_values"]:
                md.append("\n**Top Values:**")
                for tv in stats["top_values"][:5]:
                    md.append(f"  - `{tv['value']}`: {tv['count']}")

        # サンプルデータ
        if result["sample_data"]:
            md.append("\n## Sample Data")
            md.append("\n```json")
            md.append(json.dumps(result["sample_data"][:3], indent=2, ensure_ascii=False, default=str))
            md.append("```")

        return "\n".join(md)

    def run_query(self, query: str, file_path: str = None) -> "duckdb.DuckDBPyRelation":
        """
        カスタムクエリの実行

        Args:
            query: SQLクエリ
            file_path: クエリ内で'data'として参照できるファイル

        Returns:
            DuckDB結果オブジェクト
        """
        if file_path:
            self.con.execute(f"CREATE OR REPLACE VIEW data AS SELECT * FROM '{file_path}'")

        return self.con.execute(query)

    def close(self):
        """接続のクローズ"""
        self.con.close()


def main():
    parser = argparse.ArgumentParser(
        description="DuckDB Data Analyzer - Comprehensive data profiling tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python duckdb_analyzer.py data.csv
    python duckdb_analyzer.py data.parquet --output report.md
    python duckdb_analyzer.py 'data/*.csv' --sample 10000 --format json

Note:
    - Quality metrics (NULL rates, duplicates) are ALWAYS calculated on full data
    - Statistics (mean, median, etc.) can be sampled with --sample for performance
        """,
    )

    parser.add_argument("input_file", help="Input file path (supports wildcards like 'data/*.csv')")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument(
        "--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--sample", "-s", type=int, help="Sample size for statistics calculation (quality metrics always use full data)"
    )
    parser.add_argument("--memory", default="4GB", help="Memory limit (default: 4GB)")
    parser.add_argument("--threads", type=int, help="Number of threads to use")

    args = parser.parse_args()

    # 分析の実行
    analyzer = DuckDBAnalyzer(memory_limit=args.memory, threads=args.threads)

    try:
        result = analyzer.analyze_file(args.input_file, sample_size=args.sample, output_format=args.format)

        # 出力
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"Report saved to: {args.output}")
        else:
            print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
