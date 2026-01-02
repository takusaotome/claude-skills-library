# レポートタイプ設定ガイド

Salesforceカスタムレポートタイプの設定と構成。

## レポートタイプとは

レポートタイプは、レポートで使用可能なオブジェクトとフィールドを定義するテンプレートです。

- **標準レポートタイプ**: Salesforceが提供（AccountList, ContactList等）
- **カスタムレポートタイプ**: 管理者が定義

## カスタムレポートタイプが必要な場合

1. カスタムオブジェクトのレポートを作成したい
2. 複数オブジェクトを結合したレポートが必要
3. 特定のフィールドセットのみを公開したい

## XML構造

### 基本構造

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ReportType xmlns="http://soap.sforce.com/2006/04/metadata">
    <baseObject>Property__c</baseObject>
    <category>other</category>
    <deployed>true</deployed>
    <description>Property All Fields Report Type</description>
    <label>Property All Fields</label>
    <sections>
        <columns>
            <checkedByDefault>false</checkedByDefault>
            <field>Name</field>
            <table>Property__c</table>
        </columns>
        <!-- 追加の列定義 -->
    </sections>
</ReportType>
```

### 要素説明

| 要素 | 説明 | 必須 |
|:---|:---|:---:|
| `baseObject` | 基本オブジェクトAPI名 | ✓ |
| `category` | カテゴリ（下記参照） | ✓ |
| `deployed` | デプロイ済みフラグ | ✓ |
| `description` | 説明文 | - |
| `label` | 表示ラベル | ✓ |
| `sections` | フィールドセクション | ✓ |

### カテゴリ選択

| カテゴリ | 用途 |
|:---|:---|
| `accounts` | Account関連オブジェクト |
| `opportunities` | Opportunity関連オブジェクト |
| `cases` | Case関連オブジェクト |
| `leads` | Lead関連オブジェクト |
| `campaigns` | Campaign関連オブジェクト |
| `activities` | Activity関連オブジェクト |
| `forecasts` | Forecast関連オブジェクト |
| `other` | その他（カスタムオブジェクト） |

## 列定義

### 基本列

```xml
<columns>
    <checkedByDefault>false</checkedByDefault>
    <field>Name</field>
    <table>Property__c</table>
</columns>
```

### Lookupフィールド

Lookupフィールドは、関連名（Relationship Name）で指定します。

```xml
<!-- OwnerId → Owner -->
<columns>
    <checkedByDefault>false</checkedByDefault>
    <field>Owner</field>
    <table>Property__c</table>
</columns>

<!-- CreatedById → CreatedBy -->
<columns>
    <checkedByDefault>false</checkedByDefault>
    <field>CreatedBy</field>
    <table>Property__c</table>
</columns>
```

### 変換ルール

```python
FIELD_TRANSFORMATIONS = {
    "OwnerId": "Owner",
    "RecordTypeId": "RecordType",
    "CreatedById": "CreatedBy",
    "LastModifiedById": "LastModifiedBy",
    "ParentId": "Parent",
    "AccountId": "Account",
    "ReportsToId": "ReportsTo",
}
```

## 除外すべきフィールド

以下のフィールドはレポートタイプに含めても機能しないか、エラーの原因になります。

```python
EXCLUDED_FIELDS = {
    "IsDeleted",           # 削除フラグ
    "MasterRecordId",      # マージ用
    "SystemModstamp",      # システム更新日時
    "LastActivityDate",    # 活動日
    "LastViewedDate",      # 参照日
    "LastReferencedDate",  # 参照日
    "Jigsaw",              # Data.com
    "JigsawCompanyId",     # Data.com
    "JigsawContactId",     # Data.com
    "PhotoUrl",            # 写真URL
    "CleanStatus",         # Data.comステータス
}

EXCLUDED_FIELD_TYPES = ["address", "location"]
```

## 生成スクリプト例

```python
def generate_report_type_xml(
    object_name: str,
    fields: list[dict],
    label: str,
    category: str = "other"
) -> str:
    """レポートタイプXMLを生成"""

    columns_xml = ""
    for field in fields:
        field_name = field['name']

        # 除外フィールドをスキップ
        if field_name in EXCLUDED_FIELDS:
            continue
        if field.get('type') in EXCLUDED_FIELD_TYPES:
            continue

        # Lookupフィールドを変換
        if field_name in FIELD_TRANSFORMATIONS:
            field_name = FIELD_TRANSFORMATIONS[field_name]

        columns_xml += f"""        <columns>
            <checkedByDefault>false</checkedByDefault>
            <field>{field_name}</field>
            <table>{object_name}</table>
        </columns>
"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ReportType xmlns="http://soap.sforce.com/2006/04/metadata">
    <baseObject>{object_name}</baseObject>
    <category>{category}</category>
    <deployed>true</deployed>
    <description>{label} Report Type for Data Verification</description>
    <label>{label}</label>
    <sections>
{columns_xml}    </sections>
</ReportType>
"""
```

## 複数オブジェクトの結合

### 親子関係の結合

```xml
<ReportType xmlns="http://soap.sforce.com/2006/04/metadata">
    <baseObject>Account</baseObject>
    <category>accounts</category>
    <deployed>true</deployed>
    <label>Account with Contacts</label>
    <sections>
        <!-- Account列 -->
        <columns>
            <field>Name</field>
            <table>Account</table>
        </columns>
    </sections>
    <!-- 子オブジェクト結合 -->
    <join>
        <outerJoin>true</outerJoin>
        <relationship>Contacts</relationship>
        <sections>
            <columns>
                <field>Name</field>
                <table>Contact</table>
            </columns>
        </sections>
    </join>
</ReportType>
```

## デプロイ

### 単独デプロイ

```bash
sf project deploy start \
  --source-dir force-app/main/default/reportTypes/MyReportType.reportType-meta.xml \
  --target-org myorg
```

### 一括デプロイ

```bash
sf project deploy start \
  --source-dir force-app/main/default/reportTypes \
  --target-org myorg
```

## 命名規則

### レポートタイプ名

- API名: `{Object}_All_Fields` または `{Object}_Key_Fields`
- 例: `Account_All_Fields`, `Contact_Key_Fields`, `Property_All_Fields`

### Salesforce内での名前

- カスタムレポートタイプはSalesforce内で`__c`サフィックスが付く
- 例: `Property_All_Fields__c`

```python
# レポートでの参照時
report_type = "Property_All_Fields__c"  # __c が必要
```
