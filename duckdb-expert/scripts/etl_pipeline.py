#!/usr/bin/env python3
"""
DuckDB ETL Pipeline

DuckDBを使用したETLパイプラインのテンプレートスクリプト。
データの抽出、変換、ロードを効率的に行います。

Usage:
    python etl_pipeline.py <config_file>
    python etl_pipeline.py --source data.csv --target output.parquet

Examples:
    python etl_pipeline.py config.yaml
    python etl_pipeline.py --source 'raw/*.csv' --target processed.parquet --transform "WHERE amount > 0"
    python etl_pipeline.py --source data.csv --target output.parquet --overwrite
    python etl_pipeline.py --source data.json --source-format json --target output.parquet
"""

import argparse
import json
import os
import shutil
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

try:
    import duckdb
except ImportError:
    print("Error: duckdb is not installed. Run: pip install duckdb")
    sys.exit(1)


@dataclass
class ETLConfig:
    """ETLパイプラインの設定"""
    source_path: str
    target_path: str
    source_format: str = "auto"  # auto, csv, parquet, json, ndjson
    target_format: str = "parquet"
    transformations: List[str] = field(default_factory=list)
    select_columns: Optional[List[str]] = None
    where_clause: Optional[str] = None
    partition_by: Optional[List[str]] = None
    compression: str = "zstd"
    memory_limit: str = "4GB"
    threads: Optional[int] = None
    overwrite: bool = True  # True: 上書き, False: エラー
    if_exists: str = "replace"  # replace, append, fail
    validate: bool = True
    retry_count: int = 3  # リトライ回数
    retry_delay: float = 1.0  # リトライ間隔（秒）
    csv_options: Optional[Dict[str, Any]] = None  # CSV読み込みオプション
    parquet_options: Optional[Dict[str, Any]] = None  # Parquet読み込みオプション
    json_options: Optional[Dict[str, Any]] = None  # JSON読み込みオプション


class ETLPipeline:
    """DuckDBを使用したETLパイプライン"""

    # 中間ビュー名のリスト（クリーンアップ用）
    INTERMEDIATE_VIEWS = [
        "_source_data", "_selected", "_filtered", "_transformed"
    ]

    def __init__(self, config: ETLConfig):
        """
        初期化

        Args:
            config: ETL設定
        """
        self.config = config
        self.con = duckdb.connect()
        self.con.execute(f"SET memory_limit = '{config.memory_limit}'")
        if config.threads:
            self.con.execute(f"SET threads = {config.threads}")

        self.metrics = {
            "start_time": None,
            "end_time": None,
            "source_rows": 0,
            "target_rows": 0,
            "transformations_applied": [],
            "errors": [],
            "warnings": [],
            "retries": 0
        }

    def run(self) -> Dict[str, Any]:
        """
        ETLパイプラインを実行

        Returns:
            実行結果のメトリクス
        """
        self.metrics["start_time"] = datetime.now().isoformat()

        try:
            # 1. 出力先の確認
            self._check_target()

            # 2. Extract
            print(f"[Extract] Reading from: {self.config.source_path}")
            print(f"  Source format: {self.config.source_format}")
            source_data = self._extract()

            # 3. Transform
            print("[Transform] Applying transformations...")
            transformed_data = self._transform(source_data)

            # 4. Validate (optional)
            if self.config.validate:
                print("[Validate] Running data quality checks...")
                self._validate(transformed_data)

            # 5. Load (with retry)
            print(f"[Load] Writing to: {self.config.target_path}")
            print(f"  Target format: {self.config.target_format}")
            self._load_with_retry(transformed_data)

            self.metrics["end_time"] = datetime.now().isoformat()
            print("[Complete] ETL pipeline finished successfully")

        except Exception as e:
            self.metrics["errors"].append(str(e))
            self.metrics["end_time"] = datetime.now().isoformat()
            raise
        finally:
            # 中間ビューのクリーンアップ
            self._cleanup_views()

        return self.metrics

    def _check_target(self):
        """出力先の確認と処理"""
        target_path = Path(self.config.target_path)

        # ディレクトリの場合（パーティション出力）
        if self.config.partition_by:
            if target_path.exists():
                if self.config.if_exists == "fail":
                    raise FileExistsError(f"Target directory already exists: {target_path}")
                elif self.config.if_exists == "replace" and self.config.overwrite:
                    print(f"  Removing existing directory: {target_path}")
                    shutil.rmtree(target_path)
            return

        # ファイルの場合
        if target_path.exists():
            if self.config.if_exists == "fail":
                raise FileExistsError(f"Target file already exists: {target_path}")
            elif self.config.if_exists == "replace" and self.config.overwrite:
                print(f"  Will overwrite existing file: {target_path}")
            elif self.config.if_exists == "append":
                print(f"  Will append to existing file: {target_path}")
                self.metrics["warnings"].append("Append mode is only supported for some formats")

    def _build_read_function(self) -> str:
        """ソースファイル形式に応じた読み込み関数を構築"""
        source_path = self.config.source_path
        source_format = self.config.source_format.lower()

        # 自動検出
        if source_format == "auto":
            ext = Path(source_path.replace("*", "x")).suffix.lower()
            if ext in ['.parquet', '.pq']:
                source_format = "parquet"
            elif ext == '.json':
                source_format = "json"
            elif ext in ['.ndjson', '.jsonl']:
                source_format = "ndjson"
            elif ext in ['.csv', '.tsv', '.txt']:
                source_format = "csv"
            else:
                source_format = "csv"  # デフォルト

        # 形式別の読み込み関数構築
        if source_format == "parquet":
            options = self.config.parquet_options or {}
            opt_str = self._build_options_string(options, {
                "union_by_name": "true",
                "hive_partitioning": "true"
            })
            return f"read_parquet('{source_path}'{opt_str})"

        elif source_format == "csv":
            options = self.config.csv_options or {}
            opt_str = self._build_options_string(options, {
                "auto_detect": "true"
            })
            return f"read_csv('{source_path}'{opt_str})"

        elif source_format == "json":
            options = self.config.json_options or {}
            opt_str = self._build_options_string(options, {
                "auto_detect": "true"
            })
            return f"read_json('{source_path}'{opt_str})"

        elif source_format == "ndjson":
            options = self.config.json_options or {}
            opt_str = self._build_options_string(options, {
                "format": "'newline_delimited'"
            })
            return f"read_json('{source_path}'{opt_str})"

        else:
            return f"'{source_path}'"

    def _build_options_string(self, options: Dict, defaults: Dict) -> str:
        """オプション文字列を構築"""
        merged = {**defaults, **options}
        if not merged:
            return ""

        opt_parts = []
        for k, v in merged.items():
            if isinstance(v, bool):
                opt_parts.append(f"{k}={str(v).lower()}")
            elif isinstance(v, str) and not v.startswith("'"):
                opt_parts.append(f"{k}={v}")
            else:
                opt_parts.append(f"{k}={v}")

        return ", " + ", ".join(opt_parts) if opt_parts else ""

    def _extract(self) -> str:
        """
        データの抽出

        Returns:
            一時ビュー名
        """
        read_func = self._build_read_function()

        # ソース行数をカウント
        try:
            count_result = self.con.execute(f"""
                SELECT COUNT(*) FROM {read_func}
            """).fetchone()
            self.metrics["source_rows"] = count_result[0]
            print(f"  Source rows: {self.metrics['source_rows']:,}")
        except Exception as e:
            print(f"  Warning: Could not count source rows: {e}")
            self.metrics["warnings"].append(f"Could not count source rows: {e}")

        # 一時ビューとして登録
        self.con.execute(f"""
            CREATE OR REPLACE VIEW _source_data AS
            SELECT * FROM {read_func}
        """)

        return "_source_data"

    def _transform(self, source_view: str) -> str:
        """
        データの変換

        Args:
            source_view: ソースビュー名

        Returns:
            変換後のビュー名
        """
        current_view = source_view

        # カラム選択
        if self.config.select_columns:
            columns = ", ".join([f'"{c}"' for c in self.config.select_columns])
            self.con.execute(f"""
                CREATE OR REPLACE VIEW _selected AS
                SELECT {columns} FROM {current_view}
            """)
            current_view = "_selected"
            self.metrics["transformations_applied"].append(
                f"Column selection: {len(self.config.select_columns)} columns"
            )
            print(f"  Applied column selection: {len(self.config.select_columns)} columns")

        # WHERE句
        if self.config.where_clause:
            self.con.execute(f"""
                CREATE OR REPLACE VIEW _filtered AS
                SELECT * FROM {current_view}
                WHERE {self.config.where_clause}
            """)
            current_view = "_filtered"
            self.metrics["transformations_applied"].append(
                f"Filter: {self.config.where_clause}"
            )
            print(f"  Applied filter: {self.config.where_clause}")

        # カスタム変換
        for i, transformation in enumerate(self.config.transformations):
            view_name = f"_transform_{i}"
            # 変換がSELECT文の場合
            if transformation.strip().upper().startswith("SELECT"):
                sql = transformation.replace("FROM _input", f"FROM {current_view}")
            else:
                # 変換が関数やカラム変換の場合
                sql = f"""
                    SELECT *, {transformation}
                    FROM {current_view}
                """

            try:
                self.con.execute(f"""
                    CREATE OR REPLACE VIEW {view_name} AS
                    {sql}
                """)
                current_view = view_name
                # クリーンアップ対象に追加
                if view_name not in self.INTERMEDIATE_VIEWS:
                    self.INTERMEDIATE_VIEWS.append(view_name)
                self.metrics["transformations_applied"].append(f"Custom: {transformation[:50]}...")
                print(f"  Applied transformation {i+1}: {transformation[:50]}...")
            except Exception as e:
                print(f"  Warning: Transformation {i+1} failed: {e}")
                self.metrics["errors"].append(f"Transform {i+1}: {str(e)}")

        # 最終ビューを作成
        self.con.execute(f"""
            CREATE OR REPLACE VIEW _transformed AS
            SELECT * FROM {current_view}
        """)

        return "_transformed"

    def _validate(self, transformed_view: str) -> bool:
        """
        データ品質の検証

        Args:
            transformed_view: 検証対象のビュー名

        Returns:
            検証結果（True: 成功, False: 警告あり）
        """
        warnings = []

        # 行数チェック
        result = self.con.execute(f"""
            SELECT COUNT(*) FROM {transformed_view}
        """).fetchone()
        row_count = result[0]

        if row_count == 0:
            warnings.append("Warning: Transformed data has 0 rows")

        # NULL値チェック
        schema = self.con.execute(f"""
            DESCRIBE SELECT * FROM {transformed_view}
        """).fetchall()

        for col in schema:
            col_name = col[0]
            null_count = self.con.execute(f"""
                SELECT COUNT(*) FILTER (WHERE "{col_name}" IS NULL)
                FROM {transformed_view}
            """).fetchone()[0]

            if null_count > 0:
                null_pct = 100.0 * null_count / row_count if row_count > 0 else 0
                if null_pct > 50:
                    warnings.append(f"Warning: Column '{col_name}' has {null_pct:.1f}% NULL values")

        if warnings:
            for w in warnings:
                print(f"  {w}")
                self.metrics["warnings"].append(w)
            return False

        print("  Validation passed")
        return True

    def _load_with_retry(self, transformed_view: str):
        """リトライ付きでデータをロード"""
        last_error = None

        for attempt in range(self.config.retry_count):
            try:
                self._load(transformed_view)
                return  # 成功
            except Exception as e:
                last_error = e
                self.metrics["retries"] += 1

                if attempt < self.config.retry_count - 1:
                    print(f"  Retry {attempt + 1}/{self.config.retry_count} after error: {e}")
                    time.sleep(self.config.retry_delay)

        # 全リトライ失敗
        raise RuntimeError(f"Load failed after {self.config.retry_count} attempts: {last_error}")

    def _load(self, transformed_view: str):
        """
        データのロード（書き出し）

        Args:
            transformed_view: 書き出し対象のビュー名
        """
        target_format = self.config.target_format.lower()
        target_path = self.config.target_path

        # パーティション設定
        partition_clause = ""
        if self.config.partition_by:
            partition_columns = ", ".join(self.config.partition_by)
            partition_clause = f", PARTITION_BY ({partition_columns})"

        # 上書き設定
        overwrite_clause = ", OVERWRITE_OR_IGNORE true" if self.config.overwrite else ""

        # 書き出し実行
        if target_format == "parquet":
            self.con.execute(f"""
                COPY (SELECT * FROM {transformed_view})
                TO '{target_path}'
                (FORMAT PARQUET, COMPRESSION '{self.config.compression}'{partition_clause}{overwrite_clause})
            """)
        elif target_format == "csv":
            self.con.execute(f"""
                COPY (SELECT * FROM {transformed_view})
                TO '{target_path}'
                (FORMAT CSV, HEADER true{partition_clause}{overwrite_clause})
            """)
        elif target_format == "json":
            self.con.execute(f"""
                COPY (SELECT * FROM {transformed_view})
                TO '{target_path}'
                (FORMAT JSON{overwrite_clause})
            """)
        elif target_format == "ndjson":
            self.con.execute(f"""
                COPY (SELECT * FROM {transformed_view})
                TO '{target_path}'
                (FORMAT JSON, ARRAY false{overwrite_clause})
            """)
        else:
            raise ValueError(f"Unsupported target format: {target_format}")

        # 出力行数
        self.metrics["target_rows"] = self.con.execute(f"""
            SELECT COUNT(*) FROM {transformed_view}
        """).fetchone()[0]

        print(f"  Target rows: {self.metrics['target_rows']:,}")

    def _cleanup_views(self):
        """中間ビューのクリーンアップ"""
        for view_name in self.INTERMEDIATE_VIEWS:
            try:
                self.con.execute(f"DROP VIEW IF EXISTS {view_name}")
            except Exception:
                pass  # エラーは無視

    def close(self):
        """接続のクローズ"""
        self._cleanup_views()
        self.con.close()


class ETLBuilder:
    """ETLパイプラインのビルダー"""

    def __init__(self, source_path: str):
        """
        ビルダーの初期化

        Args:
            source_path: ソースファイルパス
        """
        self._config = {
            "source_path": source_path,
            "target_path": None,
            "transformations": [],
        }

    def source_format(self, format: str) -> "ETLBuilder":
        """ソース形式を指定"""
        self._config["source_format"] = format
        return self

    def to(self, target_path: str, format: str = "parquet") -> "ETLBuilder":
        """出力先の設定"""
        self._config["target_path"] = target_path
        self._config["target_format"] = format
        return self

    def select(self, *columns: str) -> "ETLBuilder":
        """カラム選択"""
        self._config["select_columns"] = list(columns)
        return self

    def where(self, condition: str) -> "ETLBuilder":
        """フィルタ条件"""
        self._config["where_clause"] = condition
        return self

    def transform(self, sql: str) -> "ETLBuilder":
        """カスタム変換を追加"""
        self._config["transformations"].append(sql)
        return self

    def partition_by(self, *columns: str) -> "ETLBuilder":
        """パーティション設定"""
        self._config["partition_by"] = list(columns)
        return self

    def compress(self, compression: str) -> "ETLBuilder":
        """圧縮設定"""
        self._config["compression"] = compression
        return self

    def memory(self, limit: str) -> "ETLBuilder":
        """メモリ制限"""
        self._config["memory_limit"] = limit
        return self

    def overwrite(self, enabled: bool = True) -> "ETLBuilder":
        """上書き設定"""
        self._config["overwrite"] = enabled
        return self

    def if_exists(self, action: str) -> "ETLBuilder":
        """既存ファイルの扱い (replace, append, fail)"""
        self._config["if_exists"] = action
        return self

    def retry(self, count: int = 3, delay: float = 1.0) -> "ETLBuilder":
        """リトライ設定"""
        self._config["retry_count"] = count
        self._config["retry_delay"] = delay
        return self

    def csv_options(self, **options) -> "ETLBuilder":
        """CSV読み込みオプション"""
        self._config["csv_options"] = options
        return self

    def parquet_options(self, **options) -> "ETLBuilder":
        """Parquet読み込みオプション"""
        self._config["parquet_options"] = options
        return self

    def json_options(self, **options) -> "ETLBuilder":
        """JSON読み込みオプション"""
        self._config["json_options"] = options
        return self

    def build(self) -> ETLConfig:
        """設定オブジェクトを構築"""
        if not self._config.get("target_path"):
            raise ValueError("Target path is required. Call .to() first.")
        return ETLConfig(**self._config)

    def run(self) -> Dict[str, Any]:
        """パイプラインを構築して実行"""
        config = self.build()
        pipeline = ETLPipeline(config)
        try:
            return pipeline.run()
        finally:
            pipeline.close()


def from_source(source_path: str) -> ETLBuilder:
    """
    ETLパイプラインを開始

    Args:
        source_path: ソースファイルパス

    Returns:
        ETLBuilder

    Example:
        >>> result = (
        ...     from_source('data/*.csv')
        ...     .source_format('csv')
        ...     .select('id', 'name', 'amount')
        ...     .where('amount > 0')
        ...     .transform("CAST(amount AS DOUBLE) as amount_normalized")
        ...     .to('output.parquet')
        ...     .partition_by('year', 'month')
        ...     .overwrite(True)
        ...     .retry(count=3, delay=1.0)
        ...     .run()
        ... )
    """
    return ETLBuilder(source_path)


def load_config_from_yaml(config_path: str) -> ETLConfig:
    """YAMLファイルから設定を読み込み"""
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required for YAML config. Run: pip install pyyaml")

    with open(config_path, "r") as f:
        config_dict = yaml.safe_load(f)

    return ETLConfig(**config_dict)


def load_config_from_json(config_path: str) -> ETLConfig:
    """JSONファイルから設定を読み込み"""
    with open(config_path, "r") as f:
        config_dict = json.load(f)

    return ETLConfig(**config_dict)


def main():
    parser = argparse.ArgumentParser(
        description="DuckDB ETL Pipeline - Extract, Transform, Load data efficiently",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Using config file
    python etl_pipeline.py config.yaml

    # Direct command line
    python etl_pipeline.py --source 'raw/*.csv' --target processed.parquet
    python etl_pipeline.py --source data.csv --target output.parquet --where "amount > 0"
    python etl_pipeline.py --source data.csv --target output/ --partition year month

    # With explicit source format
    python etl_pipeline.py --source data.json --source-format json --target output.parquet

    # With overwrite control
    python etl_pipeline.py --source data.csv --target output.parquet --overwrite
    python etl_pipeline.py --source data.csv --target output.parquet --if-exists fail
        """
    )

    parser.add_argument(
        "config_file",
        nargs="?",
        help="Configuration file (YAML or JSON)"
    )
    parser.add_argument(
        "--source", "-s",
        help="Source file path"
    )
    parser.add_argument(
        "--source-format",
        choices=["auto", "csv", "parquet", "json", "ndjson"],
        default="auto",
        help="Source format (default: auto)"
    )
    parser.add_argument(
        "--target", "-t",
        help="Target file path"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["parquet", "csv", "json", "ndjson"],
        default="parquet",
        help="Target format (default: parquet)"
    )
    parser.add_argument(
        "--select",
        nargs="+",
        help="Columns to select"
    )
    parser.add_argument(
        "--where", "-w",
        help="WHERE clause for filtering"
    )
    parser.add_argument(
        "--partition",
        nargs="+",
        help="Partition by columns"
    )
    parser.add_argument(
        "--compression",
        default="zstd",
        help="Compression (default: zstd)"
    )
    parser.add_argument(
        "--memory",
        default="4GB",
        help="Memory limit (default: 4GB)"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files"
    )
    parser.add_argument(
        "--if-exists",
        choices=["replace", "append", "fail"],
        default="replace",
        help="Action if target exists (default: replace)"
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=3,
        help="Number of retries on failure (default: 3)"
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation"
    )

    args = parser.parse_args()

    # 設定の読み込み
    if args.config_file:
        config_path = Path(args.config_file)
        if config_path.suffix in [".yaml", ".yml"]:
            config = load_config_from_yaml(args.config_file)
        elif config_path.suffix == ".json":
            config = load_config_from_json(args.config_file)
        else:
            print(f"Error: Unsupported config format: {config_path.suffix}")
            sys.exit(1)
    elif args.source and args.target:
        config = ETLConfig(
            source_path=args.source,
            source_format=args.source_format,
            target_path=args.target,
            target_format=args.format,
            select_columns=args.select,
            where_clause=args.where,
            partition_by=args.partition,
            compression=args.compression,
            memory_limit=args.memory,
            overwrite=args.overwrite,
            if_exists=args.if_exists,
            validate=not args.no_validate,
            retry_count=args.retry
        )
    else:
        parser.print_help()
        print("\nError: Either config file or --source and --target are required")
        sys.exit(1)

    # パイプラインの実行
    pipeline = ETLPipeline(config)
    try:
        start_time = time.time()
        metrics = pipeline.run()
        elapsed = time.time() - start_time

        print("\n" + "=" * 50)
        print("ETL Pipeline Summary")
        print("=" * 50)
        print(f"Source: {config.source_path}")
        print(f"Source Format: {config.source_format}")
        print(f"Target: {config.target_path}")
        print(f"Target Format: {config.target_format}")
        print(f"Source Rows: {metrics['source_rows']:,}")
        print(f"Target Rows: {metrics['target_rows']:,}")
        print(f"Transformations: {len(metrics['transformations_applied'])}")
        print(f"Retries: {metrics['retries']}")
        print(f"Elapsed Time: {elapsed:.2f} seconds")

        if metrics['warnings']:
            print(f"\nWarnings: {len(metrics['warnings'])}")
            for warning in metrics['warnings']:
                print(f"  - {warning}")

        if metrics['errors']:
            print(f"\nErrors: {len(metrics['errors'])}")
            for error in metrics['errors']:
                print(f"  - {error}")

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        pipeline.close()


if __name__ == "__main__":
    main()
