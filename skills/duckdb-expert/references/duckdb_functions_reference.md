# DuckDB Functions Reference

DuckDBで頻繁に使用する関数のクイックリファレンス。

## 集計関数 (Aggregate Functions)

### 基本統計

| 関数 | 説明 | 例 |
|------|------|-----|
| `COUNT(*)` | 行数をカウント | `SELECT COUNT(*) FROM t` |
| `COUNT(col)` | NULL以外の値をカウント | `SELECT COUNT(name) FROM t` |
| `COUNT(DISTINCT col)` | ユニーク値をカウント | `SELECT COUNT(DISTINCT category) FROM t` |
| `SUM(col)` | 合計 | `SELECT SUM(amount) FROM t` |
| `AVG(col)` | 平均 | `SELECT AVG(price) FROM t` |
| `MIN(col)` / `MAX(col)` | 最小/最大値 | `SELECT MIN(date), MAX(date) FROM t` |

### 高度な統計

| 関数 | 説明 | 例 |
|------|------|-----|
| `STDDEV(col)` | 標準偏差（サンプル） | `SELECT STDDEV(value) FROM t` |
| `STDDEV_POP(col)` | 標準偏差（母集団） | `SELECT STDDEV_POP(value) FROM t` |
| `VARIANCE(col)` | 分散（サンプル） | `SELECT VARIANCE(value) FROM t` |
| `MEDIAN(col)` | 中央値 | `SELECT MEDIAN(price) FROM t` |
| `MODE(col)` | 最頻値 | `SELECT MODE(category) FROM t` |
| `QUANTILE_CONT(col, p)` | 分位数（連続） | `SELECT QUANTILE_CONT(value, 0.25) FROM t` |
| `QUANTILE_DISC(col, p)` | 分位数（離散） | `SELECT QUANTILE_DISC(value, 0.5) FROM t` |

### 条件付き集計

```sql
-- FILTER句を使った条件付き集計
SELECT
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE status = 'active') as active_count,
    SUM(amount) FILTER (WHERE year = 2024) as sum_2024,
    AVG(value) FILTER (WHERE category IN ('A', 'B')) as avg_ab
FROM sales;
```

### リスト・配列集計

| 関数 | 説明 | 例 |
|------|------|-----|
| `LIST(col)` | 値をリストに集約 | `SELECT LIST(name) FROM t GROUP BY category` |
| `ARRAY_AGG(col)` | 配列に集約 | `SELECT ARRAY_AGG(id ORDER BY date) FROM t` |
| `STRING_AGG(col, sep)` | 文字列結合 | `SELECT STRING_AGG(name, ', ') FROM t` |
| `FIRST(col)` | 最初の値 | `SELECT FIRST(value ORDER BY date) FROM t` |
| `LAST(col)` | 最後の値 | `SELECT LAST(value ORDER BY date) FROM t` |

## ウィンドウ関数 (Window Functions)

### ランキング関数

```sql
SELECT
    id,
    category,
    value,
    -- ランキング
    ROW_NUMBER() OVER (ORDER BY value DESC) as row_num,
    RANK() OVER (ORDER BY value DESC) as rank,
    DENSE_RANK() OVER (ORDER BY value DESC) as dense_rank,
    NTILE(4) OVER (ORDER BY value DESC) as quartile,
    -- パーティション別ランキング
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY value DESC) as rank_in_category
FROM sales;
```

### 集計ウィンドウ関数

```sql
SELECT
    date,
    value,
    -- 累積計算
    SUM(value) OVER (ORDER BY date) as cumulative_sum,
    AVG(value) OVER (ORDER BY date) as running_avg,
    -- 移動平均（7日）
    AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7,
    -- 全体に対する割合
    value * 100.0 / SUM(value) OVER () as pct_of_total
FROM daily_sales;
```

### オフセット関数

```sql
SELECT
    date,
    value,
    -- 前後の値
    LAG(value, 1) OVER (ORDER BY date) as prev_value,
    LEAD(value, 1) OVER (ORDER BY date) as next_value,
    -- 差分計算
    value - LAG(value, 1) OVER (ORDER BY date) as diff,
    -- 最初/最後の値
    FIRST_VALUE(value) OVER (ORDER BY date) as first_val,
    LAST_VALUE(value) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_val
FROM daily_sales;
```

## 文字列関数 (String Functions)

### 基本操作

| 関数 | 説明 | 例 |
|------|------|-----|
| `LENGTH(s)` | 文字数 | `SELECT LENGTH('hello')` → 5 |
| `LOWER(s)` / `UPPER(s)` | 小文字/大文字変換 | `SELECT LOWER('HELLO')` → 'hello' |
| `TRIM(s)` | 前後の空白削除 | `SELECT TRIM('  hi  ')` → 'hi' |
| `LTRIM(s)` / `RTRIM(s)` | 左/右の空白削除 | `SELECT LTRIM('  hi')` → 'hi' |
| `CONCAT(s1, s2, ...)` | 文字列結合 | `SELECT CONCAT('a', 'b', 'c')` → 'abc' |
| `\|\|` | 結合演算子 | `SELECT 'a' \|\| 'b'` → 'ab' |

### 検索・抽出

| 関数 | 説明 | 例 |
|------|------|-----|
| `SUBSTRING(s, start, len)` | 部分文字列 | `SELECT SUBSTRING('hello', 2, 3)` → 'ell' |
| `LEFT(s, n)` / `RIGHT(s, n)` | 左/右からn文字 | `SELECT LEFT('hello', 2)` → 'he' |
| `STRPOS(s, sub)` | 位置検索 | `SELECT STRPOS('hello', 'l')` → 3 |
| `CONTAINS(s, sub)` | 含むかどうか | `SELECT CONTAINS('hello', 'ell')` → true |
| `STARTS_WITH(s, prefix)` | 前方一致 | `SELECT STARTS_WITH('hello', 'he')` → true |
| `ENDS_WITH(s, suffix)` | 後方一致 | `SELECT ENDS_WITH('hello', 'lo')` → true |

### 変換・置換

| 関数 | 説明 | 例 |
|------|------|-----|
| `REPLACE(s, from, to)` | 置換 | `SELECT REPLACE('hello', 'l', 'L')` → 'heLLo' |
| `REGEXP_REPLACE(s, pat, rep)` | 正規表現置換 | `SELECT REGEXP_REPLACE('a1b2', '[0-9]', 'X')` → 'aXbX' |
| `REGEXP_EXTRACT(s, pat)` | 正規表現抽出 | `SELECT REGEXP_EXTRACT('abc123', '[0-9]+')` → '123' |
| `SPLIT_PART(s, delim, n)` | 分割して取得 | `SELECT SPLIT_PART('a-b-c', '-', 2)` → 'b' |
| `STRING_SPLIT(s, delim)` | リストに分割 | `SELECT STRING_SPLIT('a,b,c', ',')` → ['a','b','c'] |

## 日付・時刻関数 (Date/Time Functions)

### 現在日時

| 関数 | 説明 |
|------|------|
| `CURRENT_DATE` | 今日の日付 |
| `CURRENT_TIME` | 現在時刻 |
| `CURRENT_TIMESTAMP` / `NOW()` | 現在日時 |

### 日付部分の抽出

```sql
SELECT
    date_col,
    EXTRACT(YEAR FROM date_col) as year,
    EXTRACT(MONTH FROM date_col) as month,
    EXTRACT(DAY FROM date_col) as day,
    EXTRACT(DAYOFWEEK FROM date_col) as dow,  -- 0=日曜
    EXTRACT(WEEK FROM date_col) as week,
    EXTRACT(QUARTER FROM date_col) as quarter,
    YEAR(date_col) as year2,  -- 短縮形
    MONTH(date_col) as month2,
    DAY(date_col) as day2
FROM t;
```

### 日付の切り捨て

```sql
SELECT
    timestamp_col,
    DATE_TRUNC('year', timestamp_col) as year_start,
    DATE_TRUNC('month', timestamp_col) as month_start,
    DATE_TRUNC('week', timestamp_col) as week_start,
    DATE_TRUNC('day', timestamp_col) as day_start,
    DATE_TRUNC('hour', timestamp_col) as hour_start
FROM t;
```

### 日付演算

```sql
SELECT
    date_col,
    date_col + INTERVAL '1 day' as next_day,
    date_col - INTERVAL '1 month' as prev_month,
    date_col + INTERVAL '1 year 2 months 3 days' as future,
    DATE_ADD(date_col, INTERVAL 7 DAY) as plus_week,
    DATE_SUB(date_col, INTERVAL 1 MONTH) as minus_month,
    DATEDIFF('day', date1, date2) as days_between,
    AGE(date1, date2) as interval_between
FROM t;
```

### 日付の作成・変換

```sql
SELECT
    MAKE_DATE(2024, 1, 15) as date_val,
    MAKE_TIMESTAMP(2024, 1, 15, 10, 30, 0) as ts_val,
    STRFTIME(date_col, '%Y-%m-%d') as formatted,
    STRPTIME('2024-01-15', '%Y-%m-%d') as parsed,
    date_col::DATE as cast_date,
    timestamp_col::DATE as ts_to_date
FROM t;
```

## 型変換関数 (Type Conversion)

### CAST / TRY_CAST

```sql
SELECT
    -- 基本的なキャスト
    CAST('123' AS INTEGER) as int_val,
    CAST(123.45 AS VARCHAR) as str_val,
    CAST('2024-01-15' AS DATE) as date_val,

    -- エラー時にNULLを返すTRY_CAST
    TRY_CAST('abc' AS INTEGER) as null_val,  -- NULL
    TRY_CAST('2024-13-45' AS DATE) as null_date,  -- NULL

    -- 型の略記法
    '123'::INTEGER as int_val2,
    123.45::VARCHAR as str_val2
FROM t;
```

### 型チェック

```sql
SELECT
    TYPEOF(column1) as type_name,
    column1 IS NULL as is_null,
    column1 IS NOT NULL as is_not_null
FROM t;
```

## 条件・制御関数 (Conditional Functions)

### CASE式

```sql
SELECT
    value,
    CASE
        WHEN value < 0 THEN 'negative'
        WHEN value = 0 THEN 'zero'
        WHEN value > 0 THEN 'positive'
    END as sign_label,

    -- 単純CASE
    CASE status
        WHEN 'A' THEN 'Active'
        WHEN 'I' THEN 'Inactive'
        ELSE 'Unknown'
    END as status_label
FROM t;
```

### NULL処理

| 関数 | 説明 | 例 |
|------|------|-----|
| `COALESCE(v1, v2, ...)` | 最初の非NULL値 | `COALESCE(col, 0)` |
| `NULLIF(v1, v2)` | 等しければNULL | `NULLIF(value, 0)` |
| `IFNULL(v, default)` | NULLなら代替値 | `IFNULL(name, 'N/A')` |
| `NVL(v, default)` | IFNULLの別名 | `NVL(amount, 0)` |

### 条件関数

```sql
SELECT
    IF(value > 0, 'positive', 'non-positive') as label,
    IIF(status = 'A', 1, 0) as is_active,
    GREATEST(a, b, c) as max_val,
    LEAST(a, b, c) as min_val
FROM t;
```

## リスト・配列関数 (List/Array Functions)

### リスト操作

```sql
SELECT
    -- リスト作成
    [1, 2, 3] as list1,
    LIST_VALUE(1, 2, 3) as list2,
    RANGE(1, 10) as range_list,  -- [1,2,3,4,5,6,7,8,9]

    -- 要素アクセス
    list_col[1] as first_elem,  -- 1-indexed
    LIST_EXTRACT(list_col, 2) as second_elem,

    -- 長さ
    LEN(list_col) as list_length,
    ARRAY_LENGTH(list_col) as array_len
FROM t;
```

### リスト変換

```sql
SELECT
    -- フラット化
    UNNEST([1, 2, 3]) as value,  -- 3行に展開

    -- フィルタ
    LIST_FILTER([1, 2, 3, 4, 5], x -> x > 2) as filtered,  -- [3,4,5]

    -- 変換
    LIST_TRANSFORM([1, 2, 3], x -> x * 2) as doubled,  -- [2,4,6]

    -- 結合
    LIST_CONCAT([1, 2], [3, 4]) as combined,  -- [1,2,3,4]

    -- ソート
    LIST_SORT([3, 1, 2]) as sorted,  -- [1,2,3]
    LIST_REVERSE_SORT([3, 1, 2]) as reverse_sorted  -- [3,2,1]
FROM t;
```

## 構造体・JSON関数 (Struct/JSON Functions)

### 構造体操作

```sql
SELECT
    -- 構造体作成
    {'name': 'Alice', 'age': 30} as person,
    ROW('Alice', 30) as row_val,

    -- フィールドアクセス
    struct_col.name as name,
    struct_col['age'] as age
FROM t;
```

### JSON操作

```sql
SELECT
    -- JSON解析
    json_col->>'name' as name,  -- 文字列として抽出
    json_col->'address'->>'city' as city,  -- ネスト
    JSON_EXTRACT(json_col, '$.name') as name2,
    JSON_EXTRACT_STRING(json_col, '$.name') as name3,

    -- JSONの型チェック
    JSON_TYPE(json_col) as type,
    JSON_VALID(json_string) as is_valid,

    -- JSON配列
    JSON_ARRAY_LENGTH(json_col->'items') as item_count
FROM t;
```

## 便利なユーティリティ関数

### ハッシュ・暗号化

```sql
SELECT
    MD5('hello') as md5_hash,
    SHA256('hello') as sha256_hash,
    HASH('hello') as duckdb_hash
FROM t;
```

### 型情報

```sql
SELECT
    TYPEOF(column1) as type,
    PG_TYPEOF(column1) as pg_type
FROM t;
```

### システム関数

```sql
-- バージョン情報
SELECT VERSION();

-- 現在のデータベース
SELECT CURRENT_DATABASE();

-- 現在のスキーマ
SELECT CURRENT_SCHEMA();
```

## PRAGMA（設定・情報取得）

```sql
-- テーブル情報
PRAGMA table_info('table_name');

-- データベース情報
PRAGMA database_list;

-- メモリ使用状況
PRAGMA memory_limit;
PRAGMA threads;

-- プロファイリング
PRAGMA enable_profiling;
PRAGMA profiling_output = 'profile.json';
```
