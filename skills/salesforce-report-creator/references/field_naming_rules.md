# フィールド命名規則

Salesforceレポートにおけるフィールド参照の命名規則ガイド。

## 基本形式

### REST API (Analytics)

```
Object.FieldName           # 基本形式
Object.Relationship.Name   # 関連オブジェクトのName表示
```

### Metadata API (XML)

```
Object.FieldName           # カスタムレポートタイプ
OBJECT.FIELDNAME           # 標準レポートタイプ（大文字の場合あり）
```

## Lookupフィールドの変換

Lookupフィールドは、レポートでは参照名（Relationship Name）で指定する必要があります。

| APIフィールド名 | レポートフィールド名 | 説明 |
|:---|:---|:---|
| `OwnerId` | `Owner` | 所有者 |
| `RecordTypeId` | `RecordType` | レコードタイプ |
| `CreatedById` | `CreatedBy` | 作成者 |
| `LastModifiedById` | `LastModifiedBy` | 最終更新者 |
| `ParentId` | `Parent` | 親レコード |
| `AccountId` | `Account` | 取引先 |
| `ContactId` | `Contact` | 取引先責任者 |
| `ReportsToId` | `ReportsTo` | 上司 |

### 変換コード例

```python
FIELD_TRANSFORMATIONS = {
    "OwnerId": "Owner",
    "RecordTypeId": "RecordType",
    "CreatedById": "CreatedBy",
    "LastModifiedById": "LastModifiedBy",
    "ParentId": "Parent",
    "AccountId": "Account",
    "ContactId": "Contact",
    "ReportsToId": "ReportsTo",
}

def transform_field_name(field_name: str) -> str:
    """フィールド名を変換"""
    return FIELD_TRANSFORMATIONS.get(field_name, field_name)
```

## 関連オブジェクトの値表示

関連オブジェクトのNameを表示したい場合は、`.Name`サフィックスを追加します。

### 正しい形式

```python
# Owner名を表示
"Account.Owner.Name"      # ✓ 正しい

# Account名を表示
"Contact.Account.Name"    # ✓ 正しい

# 作成者名を表示
"Opportunity.CreatedBy.Name"  # ✓ 正しい
```

### 間違った形式

```python
# IDのみ表示される
"Account.OwnerId"         # ✗ 名前ではなくID

# エラーになる可能性
"Account.Owner.Id"        # ✗ 通常は不要
```

## カスタムLookupフィールド

カスタムLookupフィールドも同様の規則に従います。

```python
# カスタムLookupフィールドの例
# フィールドAPI名: Property__c.redac_ownercontact__c (Lookup to Contact)

# レポートでの参照
"Property__c.redac_ownercontact__c.Name"  # Contact名を表示
```

## 標準レポートタイプ vs カスタムレポートタイプ

### 標準レポートタイプ（AccountList等）

```xml
<!-- 大文字形式の場合がある -->
<field>ACCOUNT.NAME</field>
<field>TYPE</field>
<field>USERS.NAME</field>
```

### カスタムレポートタイプ

```xml
<!-- Object.Field形式 -->
<field>Account.Id</field>
<field>Account.Name</field>
<field>Account.Owner.Name</field>
```

## フィールド名取得方法

### SF CLIでフィールド一覧取得

```bash
# すべてのフィールドを取得
sf sobject describe --sobject Account --target-org myorg --json | \
  python3 -c "import sys,json; [print(f['name']) for f in json.load(sys.stdin)['fields']]"

# Lookupフィールドのみ取得
sf sobject describe --sobject Account --target-org myorg --json | \
  python3 -c "
import sys,json
fields = json.load(sys.stdin)['fields']
for f in fields:
    if f['type'] == 'reference':
        print(f'{f[\"name\"]} -> {f[\"relationshipName\"]}')"
```

### REST APIでレポートタイプの列を取得

```python
def get_report_type_columns(instance_url, access_token, report_type):
    url = f"{instance_url}/services/data/v62.0/analytics/reportTypes/{report_type}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())

    columns = []
    categories = data.get('reportTypeMetadata', {}).get('categories', [])
    for category in categories:
        columns.extend(category.get('columns', {}).keys())
    return columns
```

## よくある間違いと修正

| 間違い | 修正 | 理由 |
|:---|:---|:---|
| `Account.OwnerId` | `Account.Owner.Name` | Lookupは参照名で |
| `Contact.AccountId` | `Contact.Account.Name` | 名前を表示するには.Name |
| `ACCOUNT.ID` | `Account.Id` | カスタムレポートタイプは小文字 |
| `Owner.Name` | `Account.Owner.Name` | オブジェクト名を先頭に |
