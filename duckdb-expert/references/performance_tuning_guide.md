# DuckDB Performance Tuning Guide

DuckDBで大規模データを効率的に処理するためのパフォーマンスチューニングガイド。

## 1. メモリ管理

### メモリ制限の設定

```python
import duckdb

con = duckdb.connect()

# メモリ制限の設定（デフォルト: システムメモリの80%）
con.execute("SET memory_limit = '8GB'")

# 現在の設定確認
con.execute("SELECT current_setting('memory_limit')").fetchone()
```

### 一時ファイル（スピルトゥディスク）

メモリ制限を超えた場合、DuckDBは自動的にディスクにスピルします。

```python
# スピル先ディレクトリの設定
con.execute("SET temp_directory = '/path/to/fast/ssd'")

# 現在の設定確認
con.execute("SELECT current_setting('temp_directory')").fetchone()
```

**ベストプラクティス:**
- SSDをスピル先に指定する
- 十分なディスク容量を確保（処理データの2-3倍）
- 共有ストレージは避ける

### メモリプレッシャー時の挙動

DuckDBはメモリ制限を超えると自動的に`temp_directory`にスピルします。特別な設定は不要です。

```python
# 十分なメモリ制限を設定
con.execute("SET memory_limit = '8GB'")

# スピル先を高速なSSDに設定
con.execute("SET temp_directory = '/path/to/fast/ssd'")

# プログレス表示（長時間クエリの監視）
con.execute("SET enable_progress_bar = true")
```

> **注意**: `enable_external_access`はファイルシステムや外部リソースへのアクセス許可に関する
> セキュリティ設定であり、スピルや外部ソートとは無関係です。デフォルトでtrueですが、
> セキュリティが重要な環境ではfalseに設定することを検討してください。

## 2. 並列処理の最適化

### スレッド数の調整

```python
# スレッド数の設定（デフォルト: CPUコア数）
con.execute("SET threads = 8")

# 現在の設定確認
con.execute("SELECT current_setting('threads')").fetchone()
```

**ガイドライン:**
- I/Oバウンド処理: コア数の1-2倍
- CPUバウンド処理: 物理コア数
- 他のプロセスと共存: コア数の50-75%

### パイプライン並列化

DuckDBは自動的にパイプライン並列化を行いますが、クエリ構造が影響します。

```sql
-- 並列化しやすいパターン
SELECT category, SUM(amount) FROM sales GROUP BY category;

-- 並列化が制限されるパターン（ORDER BY付きウィンドウ関数）
SELECT *, ROW_NUMBER() OVER (ORDER BY date) FROM sales;
```

## 3. ファイル形式の最適化

### Parquet vs CSV

| 項目 | Parquet | CSV |
|------|---------|-----|
| 読み込み速度 | 非常に高速 | 遅い |
| 列選択 | 必要な列のみ読む | 全列スキャン |
| 圧縮 | 内蔵（zstd, snappy等） | なし |
| 型情報 | 保持 | 推論が必要 |
| ファイルサイズ | 小さい（1/5〜1/10） | 大きい |

**推奨: 分析用途では常にParquet形式を使用**

### Parquet書き出しの最適化

```python
# 最適な圧縮設定
con.execute("""
    COPY (SELECT * FROM data)
    TO 'output.parquet'
    (FORMAT PARQUET, COMPRESSION 'zstd', COMPRESSION_LEVEL 3)
""")

# 行グループサイズの調整（デフォルト: 122,880行）
con.execute("""
    COPY (SELECT * FROM data)
    TO 'output.parquet'
    (FORMAT PARQUET, ROW_GROUP_SIZE 100000)
""")
```

### パーティショニング

大規模データセットでは、パーティショニングがクエリ性能を大幅に向上させます。

```python
# Hiveスタイルパーティション出力
con.execute("""
    COPY (SELECT * FROM sales)
    TO 'sales_partitioned'
    (FORMAT PARQUET, PARTITION_BY (year, month))
""")

# 結果: sales_partitioned/year=2024/month=01/data.parquet

# パーティションプルーニングを活用したクエリ
con.execute("""
    SELECT * FROM 'sales_partitioned/**/*.parquet'
    WHERE year = 2024 AND month = 1
""")  # 関連パーティションのみスキャン
```

## 4. クエリ最適化

### 列の選択

```python
# Bad: 全列選択
con.execute("SELECT * FROM large_table")

# Good: 必要な列のみ
con.execute("SELECT id, name, amount FROM large_table")

# Parquetの場合、列プルーニングが自動適用
```

### 早期フィルタリング

```python
# Good: WHERE句でフィルタ（Predicate Pushdown）
con.execute("""
    SELECT * FROM 'data.parquet'
    WHERE date >= '2024-01-01' AND category = 'A'
""")

# Bad: サブクエリ後のフィルタ
con.execute("""
    SELECT * FROM (
        SELECT * FROM 'data.parquet'
    ) sub
    WHERE date >= '2024-01-01'
""")
```

### JOINの最適化

```python
# 小さいテーブルを右側に（ハッシュジョインの効率化）
con.execute("""
    SELECT *
    FROM large_fact_table f
    JOIN small_dim_table d ON f.key = d.key
""")

# INの代わりにSEMI JOINを使用（大量の値がある場合）
con.execute("""
    SELECT * FROM orders
    WHERE customer_id IN (SELECT id FROM vip_customers)
""")
# DuckDBは自動的にSEMI JOINに変換
```

### サブクエリのマテリアライズ

```python
# 複数回参照されるサブクエリはCTEでマテリアライズ
con.execute("""
    WITH expensive_calc AS MATERIALIZED (
        SELECT category, SUM(amount) as total
        FROM sales
        GROUP BY category
    )
    SELECT a.*, b.*
    FROM expensive_calc a
    JOIN expensive_calc b ON a.category != b.category
""")
```

## 5. EXPLAIN ANALYZEの活用

### クエリプランの確認

```python
# 実行プランの表示
plan = con.execute("""
    EXPLAIN ANALYZE
    SELECT category, SUM(amount)
    FROM 'sales.parquet'
    WHERE year = 2024
    GROUP BY category
""").fetchdf()
print(plan)
```

### 確認すべきポイント

1. **Filter Pushdown**: フィルタがスキャン時に適用されているか
2. **Column Pruning**: 必要な列のみ読み込んでいるか
3. **Hash Join vs Nested Loop**: 適切なJOINアルゴリズムか
4. **Parallelism**: 並列実行されているか

### プロファイリング

```python
# 詳細なプロファイリング
con.execute("PRAGMA enable_profiling = 'query_tree'")
con.execute("PRAGMA profiling_output = '/tmp/profile.json'")

# クエリ実行
con.execute("SELECT ...")

# プロファイル結果の確認
con.execute("PRAGMA disable_profiling")
```

## 6. データ読み込みの最適化

### 並列読み込み

```python
# 複数ファイルの並列読み込み
con.execute("SELECT * FROM 'data/*.parquet'")

# ファイル数が多い場合のパフォーマンス向上
con.execute("""
    SELECT * FROM read_parquet(
        'data/*.parquet',
        parallel = true
    )
""")
```

### サンプリングによる高速探索

```python
# パーセントサンプル
con.execute("""
    SELECT * FROM 'large_data.parquet'
    USING SAMPLE 1%
""")

# 固定行数サンプル（Reservoir Sampling）
con.execute("""
    SELECT * FROM 'large_data.parquet'
    USING SAMPLE reservoir(10000 ROWS)
""")

# 再現可能なサンプル（シード指定）
con.execute("""
    SELECT * FROM 'large_data.parquet'
    USING SAMPLE 1% (bernoulli, 42)
""")
```

### ストリーミング処理

```python
# 大規模データのチャンク処理
result = con.execute("SELECT * FROM 'huge.parquet'")

# Arrow RecordBatchで効率的に取得
for batch in result.fetch_record_batch(100000):
    df = batch.to_pandas()
    process(df)
```

## 7. 永続化データベースの最適化

### インデックスとART

DuckDBは**PRIMARY KEY/UNIQUE制約を定義した場合のみ**Adaptive Radix Tree (ART)インデックスを作成します。
通常のテーブルでは自動的にインデックスは作成されません。

> **重要**: DuckDBは列指向データベースであり、ベクトル化された実行エンジンを持つため、
> 多くの分析クエリではインデックスなしでも高速に動作します。インデックスは主に
> 主キー検索やUNIQUE制約の強制に使用されます。

```python
# PRIMARY KEY制約を定義するとARTインデックスが作成される
con.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name VARCHAR
    )
""")

# UNIQUE制約でもARTインデックスが作成される
con.execute("""
    CREATE TABLE products (
        id INTEGER,
        sku VARCHAR UNIQUE,
        name VARCHAR
    )
""")

# 明示的なインデックス作成（分析クエリでは通常不要）
# 特定の検索パターンが頻繁に発生する場合のみ検討
con.execute("CREATE INDEX idx_name ON users(name)")
```

**インデックスが有効なケース:**
- 主キーによる単一行の検索
- UNIQUE制約の強制
- 小さなテーブルとの頻繁なJOIN

**インデックスが不要なケース（DuckDBの強み）:**
- 大規模な集計クエリ（GROUP BY、SUM等）
- 範囲スキャン（WHERE date BETWEEN ...）
- 分析的なJOIN（ハッシュジョインが効率的）

### テーブル統計の更新

```python
# 統計情報の収集（クエリオプティマイザ用）
con.execute("ANALYZE users")

# 全テーブルの統計更新
con.execute("ANALYZE")
```

### VACUUM

```python
# 不要なデータの削除・圧縮
con.execute("VACUUM")

# 特定テーブル
con.execute("VACUUM users")
```

## 8. 一般的なパフォーマンス問題と解決策

### 問題1: メモリ不足エラー

```
OutOfMemoryException: could not allocate block of X bytes
```

**解決策:**
```python
# メモリ制限を上げる
con.execute("SET memory_limit = '16GB'")

# スピルを有効化
con.execute("SET temp_directory = '/tmp/duckdb'")

# クエリを分割（LIMIT, OFFSET）
con.execute("SELECT * FROM large_table LIMIT 1000000 OFFSET 0")
```

### 問題2: 遅いCSV読み込み

**解決策:**
```python
# Parquetに変換
con.execute("""
    COPY (SELECT * FROM 'slow.csv')
    TO 'fast.parquet' (FORMAT PARQUET)
""")

# または、スキーマを明示（型推論をスキップ）
con.execute("""
    SELECT * FROM read_csv('data.csv',
        columns = {'id': 'INTEGER', 'name': 'VARCHAR', 'value': 'DOUBLE'},
        auto_detect = false
    )
""")
```

### 問題3: JOINが遅い

**解決策:**
```python
# 小さいテーブルを先にフィルタ
con.execute("""
    WITH filtered_dim AS (
        SELECT * FROM dim_table WHERE active = true
    )
    SELECT * FROM fact_table f
    JOIN filtered_dim d ON f.key = d.key
""")

# カーディナリティが低い列でJOIN
```

### 問題4: GROUP BYが遅い

**解決策:**
```python
# カーディナリティの高いキーを減らす
# 必要な集計のみ行う
con.execute("""
    SELECT
        DATE_TRUNC('day', timestamp) as day,  -- 秒単位ではなく日単位
        category,
        SUM(amount)
    FROM sales
    GROUP BY 1, 2
""")
```

## 9. ベンチマーク・監視

### クエリ実行時間の測定

```python
import time

start = time.time()
result = con.execute("SELECT ...").fetchdf()
elapsed = time.time() - start
print(f"Execution time: {elapsed:.2f} seconds")
```

### プログレスバー

```python
# 長時間クエリのプログレス表示
con.execute("SET enable_progress_bar = true")
con.execute("SET enable_progress_bar_print = true")

# 実行
con.execute("SELECT * FROM huge_table")  # プログレスが表示される
```

### システムリソースの監視

```python
# 現在のメモリ使用量
con.execute("SELECT * FROM duckdb_memory()").fetchdf()

# 実行中のクエリ
con.execute("SELECT * FROM duckdb_queries()").fetchdf()
```

### 大規模ファイルのベンチマーク例

```python
import duckdb
import time
from pathlib import Path

def benchmark_query(con, query: str, iterations: int = 3) -> dict:
    """クエリのベンチマークを実行"""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        con.execute(query).fetchall()
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        "min": min(times),
        "max": max(times),
        "avg": sum(times) / len(times),
        "iterations": iterations
    }

# ベンチマーク実行例
con = duckdb.connect()
con.execute("SET memory_limit = '8GB'")

# Row Groupサイズの影響を測定
for row_group_size in [50000, 100000, 200000]:
    # テストデータ作成
    con.execute(f"""
        COPY (SELECT * FROM range(10000000) t(id))
        TO 'benchmark_{row_group_size}.parquet'
        (FORMAT PARQUET, ROW_GROUP_SIZE {row_group_size})
    """)

    # ベンチマーク
    result = benchmark_query(con, f"""
        SELECT COUNT(*), SUM(id), AVG(id)
        FROM 'benchmark_{row_group_size}.parquet'
    """)

    print(f"Row Group Size {row_group_size}: {result['avg']:.3f}s avg")

# object_cacheの効果を測定
con.execute("SET enable_object_cache = false")
result_no_cache = benchmark_query(con, "SELECT * FROM 'large.parquet' WHERE id < 1000")

con.execute("SET enable_object_cache = true")
result_with_cache = benchmark_query(con, "SELECT * FROM 'large.parquet' WHERE id < 1000")

print(f"Without cache: {result_no_cache['avg']:.3f}s")
print(f"With cache: {result_with_cache['avg']:.3f}s")
```

## 10. トランザクションと同時実行

### トランザクションの基本

DuckDBはACIDトランザクションをサポートしています。

```python
import duckdb

# 永続化データベースでトランザクションを使用
con = duckdb.connect('mydb.duckdb')

# 自動コミットを無効にして明示的なトランザクション管理
con.execute("BEGIN TRANSACTION")

try:
    # 複数の操作を1つのトランザクションで実行
    con.execute("INSERT INTO orders VALUES (1, 'product_a', 100)")
    con.execute("UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 'product_a'")
    con.execute("INSERT INTO order_log VALUES (1, NOW(), 'created')")

    # すべて成功したらコミット
    con.execute("COMMIT")
    print("Transaction committed successfully")

except Exception as e:
    # エラーが発生したらロールバック
    con.execute("ROLLBACK")
    print(f"Transaction rolled back: {e}")
```

### DELETE/UPDATE操作

```python
# DELETE操作
con.execute("""
    DELETE FROM sales
    WHERE date < '2020-01-01'
""")
print(f"Deleted rows: {con.execute('SELECT changes()').fetchone()[0]}")

# UPDATE操作
con.execute("""
    UPDATE products
    SET price = price * 1.1
    WHERE category = 'premium'
""")
print(f"Updated rows: {con.execute('SELECT changes()').fetchone()[0]}")

# DELETE + INSERT パターン（UPSERT的な操作）
con.execute("""
    BEGIN TRANSACTION;

    -- 既存データを削除
    DELETE FROM target_table
    WHERE id IN (SELECT id FROM source_table);

    -- 新データを挿入
    INSERT INTO target_table
    SELECT * FROM source_table;

    COMMIT;
""")
```

### 同時実行の考慮事項

```python
# 読み取り専用モードで並列アクセス
# 複数プロセスから同時に読み取り可能
con_reader1 = duckdb.connect('mydb.duckdb', read_only=True)
con_reader2 = duckdb.connect('mydb.duckdb', read_only=True)

# 書き込みは1つの接続のみ
con_writer = duckdb.connect('mydb.duckdb')

# インメモリデータベースの共有（同一プロセス内）
shared_con = duckdb.connect(':memory:')
cursor1 = shared_con.cursor()
cursor2 = shared_con.cursor()

# 両方のカーソルから同じデータにアクセス可能
cursor1.execute("CREATE TABLE test (id INTEGER)")
cursor2.execute("INSERT INTO test VALUES (1)")
cursor1.execute("SELECT * FROM test").fetchall()  # [(1,)]
```

### チェックポイントとWAL

```python
# 永続化データベースでのチェックポイント
con = duckdb.connect('mydb.duckdb')

# 手動チェックポイント（WALをメインファイルにフラッシュ）
con.execute("CHECKPOINT")

# 強制チェックポイント
con.execute("FORCE CHECKPOINT")

# WALファイルの自動チェックポイントしきい値の設定
con.execute("SET wal_autocheckpoint = '1GB'")
```

## 11. DuckDB 1.0の主要な変更点

DuckDB 1.0では以下の点に注意してください：

### 安定したストレージフォーマット

```python
# DuckDB 1.0以降、ストレージフォーマットが安定化
# 将来のバージョンでも読み込み可能が保証される
con = duckdb.connect('stable_storage.duckdb')
```

### 破壊的変更

```python
# COPY文のオプション変更
# 旧: COPY ... WITH (HEADER=true)
# 新: COPY ... (HEADER true)
con.execute("""
    COPY (SELECT * FROM table)
    TO 'output.csv'
    (HEADER true, DELIMITER ',')
""")

# 日付/時刻のパース厳格化
# 無効な日付文字列はエラーになる
# TRY_CAST を使用して安全に変換
con.execute("""
    SELECT TRY_CAST('invalid-date' AS DATE) as safe_date
""")
```

### 新機能

```python
# PIVOT/UNPIVOT のサポート強化
con.execute("""
    PIVOT sales_data
    ON category
    USING SUM(amount)
    GROUP BY month
""")

# Lambda関数
con.execute("""
    SELECT list_transform([1, 2, 3], x -> x * 2) as doubled
""")  # [2, 4, 6]

# ASOF JOIN（時系列データの結合）
con.execute("""
    SELECT *
    FROM trades t
    ASOF JOIN quotes q
    ON t.symbol = q.symbol AND t.timestamp >= q.timestamp
""")
```
