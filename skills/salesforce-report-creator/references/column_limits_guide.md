# 列数制限ガイド

Salesforceレポートにおける列数制限と対応方法。

## 制限値一覧

| 制限種別 | 値 | 適用場面 |
|:---|:---:|:---|
| REST API detailColumns | 100列 | Analytics REST API |
| 推奨設定値 | 99列 | 安全マージン |
| Metadata API | 200列 | XMLデプロイ時 |
| 絶対最大 | 200列 | Salesforce強制制限 |
| SOQL文字数 | 20,000文字 | クエリ制限 |

## REST API (Analytics) の制限

REST APIでレポートを作成する場合、`detailColumns`は100列以下である必要があります。

### エラーメッセージ

```
{
  "errorCode": "BAD_REQUEST",
  "message": "Only a report with fewer than 100 columns can be run.",
  "specificErrorCode": 204
}
```

### 対応方法

```python
# 列数を99に制限（安全マージン）
MAX_COLUMNS = 99

filtered_columns = columns[:MAX_COLUMNS]

print(f"Available columns: {len(columns)}")
print(f"Filtered columns: {len(filtered_columns)}")
```

## オブジェクト別の典型的なフィールド数

| オブジェクト | 標準フィールド | カスタムフィールド | 合計目安 |
|:---|:---:|:---:|:---:|
| Account | 50-60 | 組織による | 100-200+ |
| Contact | 60-70 | 組織による | 100-250+ |
| Opportunity | 40-50 | 組織による | 80-150+ |
| カスタムオブジェクト | 10-20 | 組織による | 30-100+ |

## 列数削減戦略

### 1. 優先度による選択

```python
# 優先フィールドを定義
PRIORITY_FIELDS = [
    "Id", "Name", "RecordType", "Owner.Name",
    "CreatedDate", "CreatedBy.Name",
    "LastModifiedDate", "LastModifiedBy.Name",
]

# 優先フィールドを先頭に
prioritized = [f for f in PRIORITY_FIELDS if f in available_columns]
remaining = [f for f in available_columns if f not in PRIORITY_FIELDS]
columns = (prioritized + remaining)[:99]
```

### 2. フィールドタイプによる除外

```python
EXCLUDED_FIELD_TYPES = ["address", "location"]

# 除外フィールドタイプをスキップ
columns = [
    f for f in columns
    if f['type'] not in EXCLUDED_FIELD_TYPES
]
```

### 3. システムフィールドの除外

```python
EXCLUDED_FIELDS = {
    "IsDeleted", "MasterRecordId", "SystemModstamp",
    "LastActivityDate", "LastViewedDate", "LastReferencedDate",
    "Jigsaw", "JigsawCompanyId", "PhotoUrl", "CleanStatus",
}

columns = [f for f in columns if f not in EXCLUDED_FIELDS]
```

### 4. 複数レポートに分割

100列を超える場合は、複数のレポートに分割することを検討：

```python
def create_multiple_reports(columns, max_per_report=99):
    """列数が多い場合、複数レポートに分割"""
    reports = []
    for i in range(0, len(columns), max_per_report):
        chunk = columns[i:i + max_per_report]
        reports.append({
            "name": f"Report Part {i // max_per_report + 1}",
            "columns": chunk
        })
    return reports
```

## SOQL文字数制限

REST APIでレポートを実行する際、内部的にSOQLが生成されます。

### 制限

- 最大20,000文字

### 対応方法

- 列数を減らす
- フィルタ条件を簡素化する
- 複数のレポートに分割する

## 実装例

```python
def filter_columns(columns: list[str], config: dict) -> list[str]:
    """列数制限を適用"""
    max_columns = config.get("max_columns", 99)
    key_fields = config.get("key_fields")

    # 指定されたキーフィールドがあれば優先
    if key_fields:
        available_set = set(columns)
        result = [f for f in key_fields if f in available_set]
        return result[:max_columns]

    # なければ全フィールドから制限
    return columns[:max_columns]
```
