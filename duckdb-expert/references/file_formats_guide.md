# DuckDB File Formats Guide

DuckDBがサポートする各種ファイル形式の詳細ガイド。最適な設定と使用方法を解説。

## 1. CSV

### 基本的な読み込み

```python
import duckdb
con = duckdb.connect()

# 自動検出（デフォルト）
df = con.execute("SELECT * FROM 'data.csv'").fetchdf()

# 明示的な関数呼び出し
df = con.execute("SELECT * FROM read_csv('data.csv')").fetchdf()
```

### 読み込みオプション一覧

| オプション | 型 | デフォルト | 説明 |
|-----------|-----|---------|------|
| `header` | bool | true | ヘッダー行の有無 |
| `delim` | string | ',' | 区切り文字 |
| `quote` | string | '"' | 引用符 |
| `escape` | string | '"' | エスケープ文字 |
| `nullstr` | string | '' | NULL値の表現 |
| `skip` | int | 0 | スキップする行数 |
| `columns` | dict | auto | 列名と型の指定 |
| `auto_detect` | bool | true | 型の自動検出 |
| `sample_size` | int | 20480 | 型推論のサンプル行数 |
| `all_varchar` | bool | false | 全列をVARCHARとして読む |
| `filename` | bool | false | ファイル名を列として追加 |
| `parallel` | bool | true | 並列読み込み |
| `compression` | string | auto | 圧縮形式（gzip, zstd等） |

### よく使うパターン

```python
# TSVファイル（タブ区切り）
con.execute("""
    SELECT * FROM read_csv('data.tsv', delim = '\t')
""")

# ヘッダーなしCSV
con.execute("""
    SELECT * FROM read_csv('data.csv',
        header = false,
        columns = {'col1': 'INTEGER', 'col2': 'VARCHAR', 'col3': 'DATE'}
    )
""")

# NULL値の指定
con.execute("""
    SELECT * FROM read_csv('data.csv',
        nullstr = ['NA', 'NULL', 'N/A', '']
    )
""")

# 圧縮CSV
con.execute("""
    SELECT * FROM read_csv('data.csv.gz', compression = 'gzip')
""")

# 型推論の精度向上（大きなサンプル）
con.execute("""
    SELECT * FROM read_csv('data.csv', sample_size = 100000)
""")

# 複数ファイルの結合
con.execute("""
    SELECT * FROM read_csv('data/*.csv', union_by_name = true)
""")
```

### CSV書き出し

```python
# 基本的な書き出し
con.execute("""
    COPY (SELECT * FROM table) TO 'output.csv' (HEADER, DELIMITER ',')
""")

# オプション付き書き出し
con.execute("""
    COPY (SELECT * FROM table) TO 'output.csv' (
        FORMAT CSV,
        HEADER true,
        DELIMITER ',',
        QUOTE '"',
        ESCAPE '"',
        NULL 'NA',
        FORCE_QUOTE (name, description)  -- 特定列を常に引用
    )
""")

# 圧縮CSV
con.execute("""
    COPY (SELECT * FROM table) TO 'output.csv.gz' (COMPRESSION 'gzip')
""")
```

## 2. Parquet

### 基本的な読み込み

```python
# 単一ファイル
df = con.execute("SELECT * FROM 'data.parquet'").fetchdf()

# 複数ファイル（ワイルドカード）
df = con.execute("SELECT * FROM 'data/*.parquet'").fetchdf()

# リモートファイル
df = con.execute("SELECT * FROM 's3://bucket/data.parquet'").fetchdf()
```

### 読み込みオプション一覧

| オプション | 型 | デフォルト | 説明 |
|-----------|-----|---------|------|
| `filename` | bool | false | ファイル名を列として追加 |
| `file_row_number` | bool | false | 行番号を列として追加 |
| `hive_partitioning` | bool | auto | Hiveパーティション認識 |
| `union_by_name` | bool | false | 列名でスキーマ統合 |
| `encryption_config` | struct | null | 暗号化設定 |

### よく使うパターン

```python
# Hiveパーティションからの読み込み
# ディレクトリ構造: data/year=2024/month=01/data.parquet
con.execute("""
    SELECT * FROM read_parquet('data/**/*.parquet',
        hive_partitioning = true
    )
    WHERE year = 2024 AND month = 1
""")

# スキーマが異なるファイルの結合
con.execute("""
    SELECT * FROM read_parquet('data/*.parquet',
        union_by_name = true
    )
""")

# メタデータの確認
con.execute("""
    SELECT * FROM parquet_metadata('data.parquet')
""").fetchdf()

# スキーマの確認
con.execute("""
    SELECT * FROM parquet_schema('data.parquet')
""").fetchdf()
```

### Parquet書き出し

```python
# 基本的な書き出し
con.execute("""
    COPY (SELECT * FROM table) TO 'output.parquet' (FORMAT PARQUET)
""")

# 圧縮設定
con.execute("""
    COPY (SELECT * FROM table) TO 'output.parquet' (
        FORMAT PARQUET,
        COMPRESSION 'zstd',          -- zstd, snappy, gzip, lz4, uncompressed
        COMPRESSION_LEVEL 3          -- zstd: 1-22, gzip: 1-9
    )
""")

# パーティション出力
con.execute("""
    COPY (SELECT * FROM sales) TO 'output' (
        FORMAT PARQUET,
        PARTITION_BY (year, month),
        OVERWRITE_OR_IGNORE true
    )
""")

# 行グループサイズの調整
con.execute("""
    COPY (SELECT * FROM table) TO 'output.parquet' (
        FORMAT PARQUET,
        ROW_GROUP_SIZE 100000
    )
""")
```

### 圧縮形式の比較

| 形式 | 圧縮率 | 速度 | 用途 |
|------|--------|------|------|
| `zstd` | 高い | 速い | 推奨（バランス良い） |
| `snappy` | 中程度 | 非常に速い | 読み込み重視 |
| `gzip` | 高い | 遅い | 互換性重視 |
| `lz4` | 低い | 最速 | リアルタイム処理 |
| `uncompressed` | なし | 最速 | テスト・デバッグ |

## 3. JSON / NDJSON

### 基本的な読み込み

```python
# 配列形式のJSON
# [{"a": 1}, {"a": 2}]
df = con.execute("SELECT * FROM 'data.json'").fetchdf()

# 改行区切りJSON（NDJSON）
# {"a": 1}
# {"a": 2}
df = con.execute("SELECT * FROM read_json('data.ndjson', format = 'newline_delimited')").fetchdf()
```

### 読み込みオプション一覧

| オプション | 型 | デフォルト | 説明 |
|-----------|-----|---------|------|
| `format` | string | 'auto' | 'array', 'newline_delimited', 'unstructured' |
| `auto_detect` | bool | true | スキーマ自動検出 |
| `columns` | dict | auto | 列定義 |
| `maximum_object_size` | int | 16MB | 最大オブジェクトサイズ |
| `records` | string | 'auto' | レコードの扱い |
| `sample_size` | int | 20480 | サンプル行数 |
| `ignore_errors` | bool | false | エラー行を無視 |

### よく使うパターン

```python
# 明示的な型指定
con.execute("""
    SELECT * FROM read_json('data.json',
        columns = {
            'id': 'INTEGER',
            'name': 'VARCHAR',
            'created_at': 'TIMESTAMP'
        }
    )
""")

# ネストしたJSONの処理
con.execute("""
    SELECT
        json_col->>'name' as name,
        json_col->'address'->>'city' as city,
        json_col->'items' as items_array
    FROM read_json('nested.json')
""")

# JSON配列のフラット化
con.execute("""
    SELECT
        id,
        UNNEST(items) as item
    FROM read_json('data.json')
""")

# エラー行のスキップ
con.execute("""
    SELECT * FROM read_json('messy.json',
        ignore_errors = true
    )
""")
```

### JSON書き出し

```python
# 配列形式
con.execute("""
    COPY (SELECT * FROM table) TO 'output.json' (FORMAT JSON, ARRAY true)
""")

# 改行区切り形式（NDJSON）
con.execute("""
    COPY (SELECT * FROM table) TO 'output.ndjson' (FORMAT JSON, ARRAY false)
""")
```

## 4. Excel

### 読み込み

```python
# spatial拡張が必要
con.execute("INSTALL spatial; LOAD spatial;")

# Excelファイル読み込み
df = con.execute("""
    SELECT * FROM st_read('data.xlsx',
        layer = 'Sheet1',
        open_options = ['HEADERS=FORCE']
    )
""").fetchdf()
```

### 代替手段（pandas経由）

```python
import pandas as pd

# pandasで読み込み → DuckDBで処理
excel_df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
result = duckdb.query("SELECT * FROM excel_df WHERE value > 100").fetchdf()
```

## 5. リモートファイル

### S3

```python
# httpfs拡張のロード
con.execute("INSTALL httpfs; LOAD httpfs;")

# 認証設定
con.execute("""
    SET s3_region = 'us-east-1';
    SET s3_access_key_id = 'your_key';
    SET s3_secret_access_key = 'your_secret';
""")

# または環境変数から自動取得
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# S3からの読み込み
df = con.execute("SELECT * FROM 's3://bucket/path/data.parquet'").fetchdf()

# S3への書き出し
con.execute("""
    COPY (SELECT * FROM table) TO 's3://bucket/output.parquet' (FORMAT PARQUET)
""")
```

### HTTP/HTTPS

```python
# httpfs拡張のロード
con.execute("INSTALL httpfs; LOAD httpfs;")

# URLからの読み込み
df = con.execute("""
    SELECT * FROM 'https://example.com/data.csv'
""").fetchdf()

# GitHub等の公開データ
df = con.execute("""
    SELECT * FROM 'https://raw.githubusercontent.com/user/repo/main/data.parquet'
""").fetchdf()
```

### GCS (Google Cloud Storage)

```python
# httpfs拡張とGCS認証
con.execute("INSTALL httpfs; LOAD httpfs;")
con.execute("SET s3_endpoint = 'storage.googleapis.com';")

# または gcs:// プロトコル
df = con.execute("SELECT * FROM 'gcs://bucket/data.parquet'").fetchdf()
```

### Azure Blob Storage

```python
# azure拡張
con.execute("INSTALL azure; LOAD azure;")

# 認証設定
con.execute("""
    SET azure_storage_connection_string = 'your_connection_string';
""")

# 読み込み
df = con.execute("SELECT * FROM 'azure://container/data.parquet'").fetchdf()
```

## 6. データベース連携

### SQLite

```python
# sqlite拡張
con.execute("INSTALL sqlite; LOAD sqlite;")

# アタッチ
con.execute("ATTACH 'database.sqlite' AS sqlite_db (TYPE SQLITE)")

# クエリ
df = con.execute("SELECT * FROM sqlite_db.users").fetchdf()
```

### PostgreSQL

```python
# postgres拡張
con.execute("INSTALL postgres; LOAD postgres;")

# アタッチ
con.execute("""
    ATTACH 'host=localhost dbname=mydb user=user password=pass'
    AS pg_db (TYPE POSTGRES)
""")

# クエリ
df = con.execute("SELECT * FROM pg_db.public.users").fetchdf()
```

### MySQL

```python
# mysql拡張
con.execute("INSTALL mysql; LOAD mysql;")

# アタッチ
con.execute("""
    ATTACH 'host=localhost database=mydb user=user password=pass'
    AS mysql_db (TYPE MYSQL)
""")

# クエリ
df = con.execute("SELECT * FROM mysql_db.users").fetchdf()
```

## 7. ファイル形式の選択ガイドライン

### ユースケース別推奨

| ユースケース | 推奨形式 | 理由 |
|-------------|---------|------|
| 大規模分析 | Parquet | 列指向、圧縮、高速 |
| データ交換 | CSV | 互換性が高い |
| ログ処理 | NDJSON | ストリーミング処理向き |
| 設定・メタデータ | JSON | 人間が読みやすい |
| 長期保存 | Parquet (zstd) | 高圧縮、型保持 |
| リアルタイム | Parquet (snappy/lz4) | 低レイテンシ |

### 変換のベストプラクティス

```python
# CSVからParquetへの変換（分析前の前処理として推奨）
con.execute("""
    COPY (
        SELECT
            CAST(id AS INTEGER) as id,
            TRIM(name) as name,
            TRY_CAST(date_str AS DATE) as date,
            CAST(amount AS DOUBLE) as amount
        FROM 'raw_data.csv'
        WHERE id IS NOT NULL
    )
    TO 'processed_data.parquet'
    (FORMAT PARQUET, COMPRESSION 'zstd')
""")

# 変換後のサイズ比較
import os
csv_size = os.path.getsize('raw_data.csv')
parquet_size = os.path.getsize('processed_data.parquet')
print(f"CSV: {csv_size:,} bytes")
print(f"Parquet: {parquet_size:,} bytes")
print(f"Compression ratio: {csv_size/parquet_size:.1f}x")
```
