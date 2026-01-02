# Metadata API vs REST API (Analytics)

Salesforceレポート作成における2つのAPIアプローチの比較ガイド。

## 概要比較

| 観点 | Metadata API | REST API (Analytics) |
|:---|:---|:---|
| **方式** | XMLファイルをデプロイ | HTTP POST/PATCHで直接作成 |
| **コマンド** | `sf project deploy start` | Python/curlでAPI呼び出し |
| **ファイル管理** | `force-app/main/default/` | Salesforce組織内のみ |
| **バージョン管理** | 可能（Git管理） | 不可 |
| **CI/CD適性** | 高い | 低い |

## Metadata API

### 利点
- ソースコードとしてGit管理可能
- CI/CDパイプラインに統合しやすい
- 環境間の移行が容易
- 監査証跡が残る

### 欠点
- カスタムレポートタイプでフィールド参照エラーが発生しやすい
- XMLフォーマットの理解が必要
- デプロイ後の反映に時間がかかる場合がある

### 使用例

```bash
# デプロイ
sf project deploy start \
  --source-dir force-app/main/default/reports \
  --target-org myorg

# デプロイ状況確認
sf project deploy report --target-org myorg
```

### ファイル構造

```
force-app/
└── main/
    └── default/
        ├── reportTypes/
        │   └── MyReportType.reportType-meta.xml
        └── reports/
            └── MyFolder/
                └── MyReport.report-meta.xml
```

## REST API (Analytics)

### 利点
- カスタムレポートタイプで安定動作
- 即座にレポートが作成される
- フィールド参照形式がシンプル
- プログラムからの動的作成に最適

### 欠点
- ソース管理が困難
- CI/CDへの統合が複雑
- 認証トークン管理が必要

### 使用例

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
        "name": "My Report",
        "reportFormat": "TABULAR",
        "reportType": {"type": "MyReportType__c"},
        "detailColumns": ["Object__c.Name", "Object__c.Field__c"],
        "standardDateFilter": {
            "column": "Object__c.CreatedDate",
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
    print(f"Report ID: {result['reportMetadata']['id']}")
```

### API エンドポイント

| 操作 | メソッド | エンドポイント |
|:---|:---|:---|
| レポート作成 | POST | `/services/data/v62.0/analytics/reports` |
| レポート更新 | PATCH | `/services/data/v62.0/analytics/reports/{id}` |
| レポートタイプ情報 | GET | `/services/data/v62.0/analytics/reportTypes/{type}` |
| レポート実行 | GET | `/services/data/v62.0/analytics/reports/{id}` |

## 推奨使い分け

### Metadata APIを使用すべき場合
- 標準オブジェクト（Account, Contact等）のレポート
- CI/CDパイプラインでの自動デプロイ
- 環境間でのレポート移行
- 変更履歴の追跡が必要な場合

### REST APIを使用すべき場合
- カスタムオブジェクトのレポート（推奨）
- プログラムからの動的レポート生成
- Metadata APIでエラーが発生する場合
- 即座にレポートを作成したい場合

## ハイブリッドアプローチ

実運用では両方を組み合わせることも有効：

1. **レポートタイプ**: Metadata APIでデプロイ（バージョン管理）
2. **レポート本体**: REST APIで作成（安定性重視）

```bash
# Step 1: レポートタイプをMetadata APIでデプロイ
sf project deploy start --source-dir force-app/main/default/reportTypes --target-org myorg

# Step 2: レポートをREST APIで作成
python scripts/create_reports_via_api.py --org myorg
```

## トラブルシューティング

### Metadata APIでのエラー

```
Error: Invalid field name: Property__c.Name
```

**原因**: カスタムレポートタイプのフィールド参照形式の問題

**解決策**: REST APIに切り替える

### REST APIでのエラー

```
Error: Only a report with fewer than 100 columns can be run
```

**原因**: detailColumnsの制限（100列）

**解決策**: 列数を99以下に制限

```python
columns = columns[:99]
```
