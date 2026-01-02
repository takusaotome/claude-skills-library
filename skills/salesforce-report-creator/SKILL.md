---
name: salesforce-report-creator
description: SF CLI経由でSalesforceレポートを作成するスキル。Metadata APIとREST APIの使い分け、フィールド命名規則、列数制限、レポートタイプ設定を網羅。カスタムオブジェクトレポート作成時の注意点も含む。Use when creating Salesforce reports via CLI, deploying report types, or automating report generation.
---

# Salesforce Report Creator

SF CLIを使用してSalesforceレポートを作成・デプロイするためのスキル。

## Overview

このスキルは以下の機能を提供します：

1. **レポートタイプの作成**: カスタムオブジェクト用レポートタイプXMLの生成
2. **レポートの作成**: Metadata APIまたはREST APIを使用したレポート作成
3. **フィールド管理**: 適切なフィールド命名規則と列数制限の適用
4. **デプロイ**: SF CLIを使用したSalesforce組織へのデプロイ

## When to Use This Skill

以下の場面でこのスキルを使用してください：

- SF CLIからSalesforceレポートを作成したい
- カスタムオブジェクト用のレポートタイプを定義したい
- 大量のフィールドを含むレポートを自動生成したい
- Metadata APIとREST APIのどちらを使うべきか判断したい
- レポートデプロイでエラーが発生し、トラブルシューティングが必要

**トリガーフレーズ:**
- "Salesforceレポートを作成"
- "SF CLIでレポートをデプロイ"
- "カスタムレポートタイプを作成"
- "レポートのフィールド参照エラー"

## Prerequisites

### 必須ツール

```bash
# Salesforce CLI (sf) がインストールされていること
sf --version

# 認証済みのSalesforce組織があること
sf org list
```

### 認証

```bash
# Web認証フロー
sf org login web --alias myorg

# JWTフロー（CI/CD向け）
sf org login jwt --client-id <consumer-key> --jwt-key-file <path> --username <user>

# 既存の認証を確認
sf org display --target-org myorg
```

## Core Concepts

### 1. Metadata API vs REST API

| 項目 | Metadata API | REST API (Analytics) |
|:---|:---|:---|
| **方式** | XMLファイルをデプロイ | HTTP POSTで直接作成 |
| **コマンド** | `sf project deploy start` | Python/curlでAPI呼び出し |
| **カスタムレポートタイプ** | フィールド参照でエラーが発生しやすい | 推奨（安定動作） |
| **保存場所** | `force-app/main/default/reports/` | Salesforce組織内のみ |
| **バージョン管理** | 可能（GitでXML管理） | 不可（組織内のみ） |

**推奨事項:**
- **標準オブジェクト**: Metadata APIで十分
- **カスタムオブジェクト**: REST API推奨
- **CI/CD統合**: Metadata API（バージョン管理可能）

### 2. フィールド命名規則

レポートでのフィールド参照形式はAPIによって異なります。

**REST API形式:**
```
Object.FieldName           # 基本形式
Object.Relationship.Name   # 関連オブジェクトのName表示
```

**Metadata API (XML)形式:**
```
Object.FieldName           # カスタムレポートタイプ
OBJECT.FIELDNAME           # 標準レポートタイプ（大文字）
```

**Lookupフィールドの変換:**
```python
# APIフィールド名 → レポートフィールド名
"OwnerId"        → "Owner"
"RecordTypeId"   → "RecordType"
"CreatedById"    → "CreatedBy"
"LastModifiedById" → "LastModifiedBy"
"ParentId"       → "Parent"
"AccountId"      → "Account"
"ReportsToId"    → "ReportsTo"
```

**関連オブジェクトの値表示:**
```python
# Owner名を表示したい場合
"Account.Owner.Name"    # ✓ 正しい
"Account.OwnerId"       # ✗ IDのみ表示

# Account名を表示したい場合
"Contact.Account.Name"  # ✓ 正しい
"Contact.AccountId"     # ✗ IDのみ表示
```

### 3. 列数制限

| 制限種別 | 値 | 適用場面 |
|:---|:---:|:---|
| REST API detailColumns | 100列 | Analytics API |
| 推奨設定値 | 99列 | 安全マージン |
| 絶対最大 | 200列 | Salesforce強制制限 |
| SOQL文字数 | 20,000文字 | クエリ制限 |

**対応方法:**
```python
# 列数を99に制限
filtered_columns = columns[:99]
```

### 4. 除外すべきフィールド

以下のフィールドはレポートで使用できない場合があります：

```python
EXCLUDED_FIELDS = {
    "IsDeleted",           # システムフィールド
    "MasterRecordId",      # マージ用
    "SystemModstamp",      # システム更新日時
    "LastActivityDate",    # 活動日
    "LastViewedDate",      # 参照日
    "LastReferencedDate",  # 参照日
    "Jigsaw", "JigsawCompanyId", "JigsawContactId",  # Data.com
    "PhotoUrl",            # 写真URL
    "CleanStatus",         # Data.comステータス
}

EXCLUDED_FIELD_TYPES = ["address", "location"]  # 複合フィールド
EXCLUDED_FIELD_SUFFIXES = ["__pc"]              # Person Account
```

## Workflow

### Step 1: レポートタイプの作成（カスタムオブジェクト用）

カスタムオブジェクトのレポートを作成するには、まずレポートタイプを定義します。

```bash
# フィールド一覧を取得
sf sobject describe --sobject Property__c --target-org myorg --json | \
  python3 -c "import sys,json; [print(f['name']) for f in json.load(sys.stdin)['fields']]"
```

**レポートタイプXML例:**
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
        <!-- 追加のcolumns... -->
    </sections>
</ReportType>
```

**カテゴリ選択:**
- `accounts` - Account関連
- `opportunities` - Opportunity関連
- `cases` - Case関連
- `leads` - Lead関連
- `other` - その他（カスタムオブジェクト）

### Step 2: レポートタイプのデプロイ

```bash
# レポートタイプのみデプロイ
sf project deploy start \
  --source-dir force-app/main/default/reportTypes \
  --target-org myorg

# デプロイ結果確認
sf project deploy report --target-org myorg
```

### Step 3: レポートの作成

**方法A: REST API（推奨）**

```python
import json
import subprocess
import urllib.request

# 認証情報取得
result = subprocess.run(
    ["sf", "org", "display", "--target-org", "myorg", "--json"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
access_token = data['result']['accessToken']
instance_url = data['result']['instanceUrl']

# レポート作成
url = f"{instance_url}/services/data/v62.0/analytics/reports"
body = {
    "reportMetadata": {
        "name": "Property All Fields Report",
        "description": "All fields report for data verification",
        "reportFormat": "TABULAR",
        "reportType": {"type": "Property_All_Fields__c"},
        "detailColumns": [
            "Property__c.Name",
            "Property__c.CreatedDate",
            "Property__c.Owner.Name"
        ],
        "standardDateFilter": {
            "column": "Property__c.CreatedDate",
            "durationValue": "CUSTOM"
        }
    }
}

req = urllib.request.Request(
    url,
    data=json.dumps(body).encode('utf-8'),
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    },
    method='POST'
)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    print(f"Created report: {result['reportMetadata']['id']}")
```

**方法B: Metadata API（XMLデプロイ）**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Report xmlns="http://soap.sforce.com/2006/04/metadata">
    <columns>
        <field>Property__c.Name</field>
    </columns>
    <columns>
        <field>Property__c.CreatedDate</field>
    </columns>
    <description>Property All Fields Report</description>
    <format>Tabular</format>
    <name>Property All Fields</name>
    <reportType>Property_All_Fields__c</reportType>
    <scope>organization</scope>
    <showDetails>true</showDetails>
    <timeFrameFilter>
        <dateColumn>Property__c.CreatedDate</dateColumn>
        <interval>INTERVAL_CUSTOM</interval>
    </timeFrameFilter>
</Report>
```

```bash
sf project deploy start \
  --source-dir force-app/main/default/reports \
  --target-org myorg
```

### Step 4: フォルダへの移動（オプション）

```python
# REST APIでフォルダ移動
def move_report_to_folder(instance_url, access_token, report_id, folder_id):
    url = f"{instance_url}/services/data/v62.0/analytics/reports/{report_id}"
    body = {"reportMetadata": {"folderId": folder_id}}

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        method='PATCH'
    )
    urllib.request.urlopen(req)
```

## Troubleshooting

### エラー: "Invalid field name: Object.FieldName"

**原因:** Metadata APIでカスタムレポートタイプのフィールド参照が正しくない

**解決策:**
1. REST APIを使用する（推奨）
2. フィールド名の形式を確認（`Object.Field` vs `OBJECT.FIELD`）

### エラー: "Only a report with fewer than 100 columns can be run"

**原因:** REST APIの列数制限（100列）を超過

**解決策:**
```python
# 列数を99に制限
columns = columns[:99]
```

### エラー: "Could not find field OwnerId"

**原因:** Lookupフィールドの参照形式が間違っている

**解決策:**
```python
# ✗ 間違い
"Account.OwnerId"

# ✓ 正しい
"Account.Owner"       # 関連オブジェクトとして参照
"Account.Owner.Name"  # Owner名を表示
```

### エラー: "invalid report type"

**原因:** レポートタイプ名が一致しない、または`__c`サフィックスの問題

**解決策:**
```python
# レポートタイプはSalesforce内で__cが付く
# XML: Property_All_Fields.reportType-meta.xml
# 参照時: Property_All_Fields__c
```

### エラー: "Cannot find folder"

**原因:** レポートフォルダが存在しない

**解決策:**
```bash
# フォルダを先にデプロイ
sf project deploy start \
  --source-dir force-app/main/default/reports/MyFolder.reportFolder-meta.xml \
  --target-org myorg
```

## Resources

### リファレンスファイル

| ファイル | 内容 |
|:---|:---|
| `references/metadata_api_vs_rest_api.md` | API比較の詳細ガイド |
| `references/field_naming_rules.md` | フィールド命名規則の詳細 |
| `references/column_limits_guide.md` | 列数制限と対応方法 |
| `references/report_type_configuration.md` | レポートタイプ設定の詳細 |

### スクリプト

| ファイル | 用途 |
|:---|:---|
| `scripts/create_reports_via_api.py` | REST APIでレポートを作成するPythonスクリプト |

### アセット（テンプレート）

| ファイル | 用途 |
|:---|:---|
| `assets/report_type_template.xml` | レポートタイプXMLテンプレート |
| `assets/report_metadata_template.xml` | レポートメタデータXMLテンプレート |

## Quick Reference

### よく使うコマンド

```bash
# オブジェクトのフィールド一覧取得
sf sobject describe --sobject Account --target-org myorg --json

# レポートタイプのデプロイ
sf project deploy start --source-dir force-app/main/default/reportTypes --target-org myorg

# レポートのデプロイ
sf project deploy start --source-dir force-app/main/default/reports --target-org myorg

# デプロイ状況確認
sf project deploy report --target-org myorg

# 組織情報取得（認証トークン含む）
sf org display --target-org myorg --json
```

### REST API エンドポイント

```
# レポート作成
POST /services/data/v62.0/analytics/reports

# レポート更新（フォルダ移動など）
PATCH /services/data/v62.0/analytics/reports/{reportId}

# レポートタイプ情報取得
GET /services/data/v62.0/analytics/reportTypes/{reportType}
```
