---
name: duckdb-expert
description: DuckDBを使用した大規模データ分析の専門スキル。DuckDBのアーキテクチャ、SQL構文、パフォーマンス最適化、各種ファイル形式（CSV、Parquet、JSON等）の効率的な読み込み・書き出しを熟知。メモリ効率の良い分析、複雑なクエリの最適化、データパイプライン構築を支援。Use when analyzing large datasets, querying CSV/Parquet/JSON files directly, building data pipelines, or optimizing analytical queries with DuckDB.
---

# DuckDB Expert

## Overview

DuckDBは、OLAP（オンライン分析処理）に最適化された組み込み型の列指向データベースです。このスキルは、DuckDBを使用した効率的なデータ分析、大規模データセットの処理、パフォーマンス最適化を支援します。

## When to Use This Skill

- 大規模なCSV、Parquet、JSONファイルを直接クエリしたい
- メモリに収まらない大きなデータセットを分析したい
- SQLを使ってデータ変換やETLパイプラインを構築したい
- pandas/Polarsと連携した高速なデータ処理を行いたい
- ファイルベースのデータウェアハウスを構築したい
- 複雑な分析クエリのパフォーマンスを最適化したい

## Quick Start

### インストールと基本接続

```python
import duckdb

# インメモリデータベース（一時的な分析向け）
con = duckdb.connect()

# 永続化データベース（データを保存する場合）
con = duckdb.connect('my_analysis.duckdb')

# 読み取り専用モード（並列アクセス可能）
con = duckdb.connect('my_analysis.duckdb', read_only=True)
```

### ファイルの直接クエリ

```python
# CSVファイルを直接クエリ（ロード不要）
result = con.execute("SELECT * FROM 'data.csv' LIMIT 10").fetchdf()

# Parquetファイル
result = con.execute("SELECT * FROM 'data.parquet' WHERE year = 2024").fetchdf()

# 複数ファイルのワイルドカードクエリ
result = con.execute("SELECT * FROM 'data/*.parquet'").fetchdf()

# リモートファイル（S3、HTTP）- httpfs拡張が必要
con.execute("INSTALL httpfs; LOAD httpfs;")

# S3認証設定（必要な場合）
con.execute("""
    SET s3_region = 'us-east-1';
    SET s3_access_key_id = 'your_key';
    SET s3_secret_access_key = 'your_secret';
""")
# または環境変数 AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY を使用

result = con.execute("SELECT * FROM 's3://bucket/data.parquet'").fetchdf()

# HTTPファイル（httpfs拡張をロード後に使用可能）
result = con.execute("SELECT * FROM 'https://example.com/data.csv'").fetchdf()
```

## Core Workflows

### Workflow 1: 大規模データの探索的分析

```
1. データソース確認 → 2. スキーマ推論 → 3. サンプリング分析 → 4. 集計・可視化
```

**Step 1: データソースの確認**

```python
# ファイルのスキーマを確認
con.execute("DESCRIBE SELECT * FROM 'large_data.csv'").fetchdf()

# ファイルサイズと行数の概算
con.execute("""
    SELECT
        COUNT(*) as row_count,
        COUNT(DISTINCT column1) as unique_values
    FROM 'large_data.csv'
""").fetchdf()
```

**Step 2: サンプリングによる高速分析**

```python
# TABLESAMPLEでランダムサンプリング（大規模データに有効）
con.execute("""
    SELECT * FROM 'large_data.parquet'
    USING SAMPLE 1% (bernoulli)
""").fetchdf()

# RESERVOIR SAMPLINGで固定行数サンプル
con.execute("""
    SELECT * FROM 'large_data.csv'
    USING SAMPLE reservoir(10000 ROWS)
""").fetchdf()
```

**Step 3: 効率的な集計**

```python
# 列指向の強みを活かした集計
con.execute("""
    SELECT
        category,
        COUNT(*) as count,
        AVG(value) as avg_value,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value) as median
    FROM 'large_data.parquet'
    GROUP BY category
    ORDER BY count DESC
""").fetchdf()
```

### Workflow 2: ETLパイプライン構築

```
1. ソース定義 → 2. 変換ロジック → 3. 品質チェック → 4. 出力
```

**Step 1: 複数ソースの統合**

```python
# 複数ファイルの統合
con.execute("""
    CREATE OR REPLACE VIEW combined_data AS
    SELECT *, 'source_a' as source FROM 'data_a/*.parquet'
    UNION ALL
    SELECT *, 'source_b' as source FROM 'data_b/*.parquet'
""")

# 異なるフォーマットの結合
con.execute("""
    SELECT a.*, b.category_name
    FROM 'transactions.csv' a
    LEFT JOIN 'categories.json' b ON a.category_id = b.id
""")
```

**Step 2: データ変換**

```python
# 型変換とクレンジング
con.execute("""
    SELECT
        CAST(id AS INTEGER) as id,
        TRIM(LOWER(email)) as email,
        COALESCE(amount, 0) as amount,
        TRY_CAST(date_str AS DATE) as date,
        CASE
            WHEN status IN ('active', 'enabled') THEN 'active'
            ELSE 'inactive'
        END as status_normalized
    FROM 'raw_data.csv'
    WHERE id IS NOT NULL
""")
```

**Step 3: 品質チェック**

```python
# データ品質レポート
con.execute("""
    SELECT
        COUNT(*) as total_rows,
        COUNT(*) FILTER (WHERE id IS NULL) as null_ids,
        COUNT(*) FILTER (WHERE amount < 0) as negative_amounts,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM transformed_data
""").fetchdf()
```

**Step 4: 効率的な出力**

```python
# Parquet形式で出力（圧縮・パーティション付き）
con.execute("""
    COPY (SELECT * FROM transformed_data)
    TO 'output' (FORMAT PARQUET, PARTITION_BY (year, month), COMPRESSION 'zstd')
""")

# CSV出力
con.execute("""
    COPY (SELECT * FROM result_table)
    TO 'output.csv' (HEADER, DELIMITER ',')
""")
```

### Workflow 3: 高度な分析クエリ

**ウィンドウ関数の活用**

```python
# ランキングと累積計算
con.execute("""
    SELECT
        date,
        category,
        sales,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC) as rank,
        SUM(sales) OVER (PARTITION BY category ORDER BY date) as cumulative_sales,
        LAG(sales, 1) OVER (PARTITION BY category ORDER BY date) as prev_sales,
        sales - LAG(sales, 1) OVER (PARTITION BY category ORDER BY date) as sales_change
    FROM 'sales_data.parquet'
""").fetchdf()
```

**CTEを使った複雑なクエリ**

```python
con.execute("""
    WITH monthly_stats AS (
        SELECT
            DATE_TRUNC('month', date) as month,
            category,
            SUM(amount) as total_amount,
            COUNT(*) as transaction_count
        FROM transactions
        GROUP BY 1, 2
    ),
    ranked AS (
        SELECT *,
            RANK() OVER (PARTITION BY month ORDER BY total_amount DESC) as rank
        FROM monthly_stats
    )
    SELECT * FROM ranked WHERE rank <= 5
""").fetchdf()
```

**PIVOT/UNPIVOT操作**

```python
# PIVOT: 行を列に変換
con.execute("""
    PIVOT sales_data
    ON category
    USING SUM(amount)
    GROUP BY month
""").fetchdf()

# UNPIVOT: 列を行に変換
con.execute("""
    UNPIVOT wide_table
    ON col1, col2, col3
    INTO NAME metric VALUE value
""").fetchdf()
```

## Performance Optimization

### メモリ設定

```python
# メモリ制限の設定（デフォルト: システムメモリの80%）
con.execute("SET memory_limit = '8GB'")

# 一時ファイルディレクトリの設定（メモリ超過時のスピル先）
con.execute("SET temp_directory = '/tmp/duckdb'")

# スレッド数の調整
con.execute("SET threads = 4")
```

### クエリ最適化のベストプラクティス

1. **列の選択を明示する**
   ```python
   # Good: 必要な列のみ選択
   SELECT id, name, amount FROM large_table

   # Bad: 全列選択は避ける
   SELECT * FROM large_table
   ```

2. **フィルタを早期に適用**
   ```python
   # Good: WHERE句でフィルタリング
   SELECT * FROM 'data.parquet' WHERE year = 2024

   # Parquetのpredicate pushdownが効く
   ```

3. **適切なファイル形式を選択**
   ```
   - Parquet: 大規模分析に最適（列指向、圧縮、メタデータ）
   - CSV: 互換性重視、小規模データ
   - JSON: 半構造化データ
   ```

4. **パーティショニングの活用**
   ```python
   # パーティションされたデータの効率的なクエリ
   SELECT * FROM 'data/year=2024/month=*/data.parquet'
   ```

### EXPLAIN ANALYZEでの分析

```python
# クエリプランの確認
con.execute("EXPLAIN ANALYZE SELECT ...").fetchdf()

# プロファイリング有効化
con.execute("PRAGMA enable_profiling")
con.execute("PRAGMA profiling_output = 'profile.json'")
```

## Integration with Python Ecosystem

### pandas連携

```python
import pandas as pd
import duckdb

# pandasからDuckDB
df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
result = duckdb.query("SELECT * FROM df WHERE a > 1").fetchdf()

# DuckDBからpandas
result_df = con.execute("SELECT * FROM table").fetchdf()
```

### Polars連携

```python
import polars as pl
import duckdb

# PolarsからDuckDB
pl_df = pl.DataFrame({'a': [1, 2, 3]})
result = duckdb.query("SELECT * FROM pl_df").pl()

# DuckDBからPolars
result_pl = con.execute("SELECT * FROM table").pl()
```

### Arrow連携

```python
import pyarrow as pa

# ArrowからDuckDB（ゼロコピー）
arrow_table = pa.table({'a': [1, 2, 3]})
result = duckdb.query("SELECT * FROM arrow_table").arrow()
```

## File Format Reference

### CSV読み込みオプション

```python
con.execute("""
    SELECT * FROM read_csv('data.csv',
        header = true,
        delim = ',',
        quote = '"',
        escape = '"',
        nullstr = 'NA',
        skip = 1,
        columns = {'id': 'INTEGER', 'name': 'VARCHAR'},
        auto_detect = true,
        sample_size = 10000
    )
""")
```

### Parquet読み込みオプション

```python
con.execute("""
    SELECT * FROM read_parquet('data.parquet',
        filename = true,  -- ファイル名を列として追加
        hive_partitioning = true,  -- Hiveパーティション認識
        union_by_name = true  -- スキーマが異なるファイルの結合
    )
""")
```

### JSON読み込みオプション

```python
con.execute("""
    SELECT * FROM read_json('data.json',
        auto_detect = true,
        format = 'auto',  -- 'array', 'unstructured', 'newline_delimited'
        maximum_object_size = 16777216
    )
""")
```

## Common Patterns

### パターン1: 大規模CSVの効率的な処理

```python
# ストリーミング処理（メモリ効率）
for chunk in con.execute("SELECT * FROM 'huge.csv'").fetch_record_batch(100000):
    process(chunk.to_pandas())
```

### パターン2: 増分データ処理

```python
# 方法1: INSERT OR REPLACE（PRIMARY KEY制約が必要）
# テーブル作成時に主キーを定義
con.execute("""
    CREATE TABLE IF NOT EXISTS target_table (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        value DOUBLE,
        updated_at TIMESTAMP
    )
""")

# 主キーに基づいて更新または挿入
con.execute("""
    INSERT OR REPLACE INTO target_table
    SELECT * FROM 'new_data.parquet'
    WHERE updated_at > (SELECT COALESCE(MAX(updated_at), '1970-01-01') FROM target_table)
""")

# 方法2: DELETE + INSERT（主キーがない場合）
con.execute("""
    DELETE FROM target_table
    WHERE id IN (SELECT id FROM 'new_data.parquet');

    INSERT INTO target_table
    SELECT * FROM 'new_data.parquet'
""")

# 方法3: 一時テーブルを使ったマージパターン
con.execute("""
    -- 新データを一時テーブルに読み込み
    CREATE TEMP TABLE new_data AS SELECT * FROM 'new_data.parquet';

    -- 既存データを削除
    DELETE FROM target_table WHERE id IN (SELECT id FROM new_data);

    -- 新データを挿入
    INSERT INTO target_table SELECT * FROM new_data;

    -- 一時テーブル削除
    DROP TABLE new_data;
""")
```

### パターン3: データ品質チェック

```python
# 包括的な品質レポート
quality_report = con.execute("""
    SELECT
        'total_rows' as metric, COUNT(*)::VARCHAR as value FROM data
    UNION ALL
    SELECT 'null_rate_col1', ROUND(100.0 * COUNT(*) FILTER (WHERE col1 IS NULL) / COUNT(*), 2)::VARCHAR FROM data
    UNION ALL
    SELECT 'duplicate_keys', COUNT(*)::VARCHAR FROM (SELECT key FROM data GROUP BY key HAVING COUNT(*) > 1)
""").fetchdf()
```

## Resources

### scripts/

- `duckdb_analyzer.py`: データプロファイリングと品質チェックの自動化スクリプト
- `etl_pipeline.py`: ETLパイプラインのテンプレートスクリプト

### references/

- `duckdb_functions_reference.md`: 主要な関数リファレンス
- `performance_tuning_guide.md`: パフォーマンスチューニングガイド
- `file_formats_guide.md`: ファイル形式別の最適な設定ガイド

### assets/

このスキルにはアセットファイルは含まれません。
