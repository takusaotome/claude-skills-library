---
name: render-cli-expert
description: Render CLIを使用したクラウドサービス管理の専門スキル。デプロイ、ログ監視、SSH接続、PostgreSQL接続、サービス管理などRenderプラットフォームのCLI操作を効率的に支援。定期的に公式ドキュメントをチェックして最新情報を取得。Use when managing Render services via CLI, deploying applications, viewing logs, connecting to databases, or automating cloud infrastructure tasks.
---

# Render CLI Expert

## Overview

Render CLIは、Renderクラウドプラットフォームのサービスをターミナルから直接管理するための公式CLIツールです。このスキルは、Render CLIを使用した効率的なサービス管理、デプロイ自動化、トラブルシューティングを支援します。

## Auto-Update Mechanism

**重要**: このスキルには自動更新チェック機能があります。

スキルが呼び出されたとき、前回の公式ドキュメントチェックから1ヶ月以上経過している場合、自動的に最新情報を取得します。

```bash
# 更新チェックを手動で実行
python3 ~/.claude/skills/render-cli-expert/scripts/render_cli_updater.py

# 強制更新（経過時間に関係なく）
python3 ~/.claude/skills/render-cli-expert/scripts/render_cli_updater.py --force
```

更新ログは `references/cli_updates.md` に記録されます。

## When to Use This Skill

- Renderサービスをターミナルからデプロイ・管理したい
- サービスのログをリアルタイムで監視したい
- PostgreSQLデータベースにpsqlで接続したい
- SSHでサービスにリモート接続したい
- CI/CDパイプラインでRender操作を自動化したい
- ワークスペースやサービスの一覧を取得したい

**Example triggers:**
- "Renderにデプロイしたい"
- "Renderのログを見たい"
- "RenderのPostgreSQLに接続したい"
- "Render CLIの使い方を教えて"
- "CI/CDでRenderを自動化したい"

## Installation

### Homebrew (macOS/Linux - Recommended)

```bash
brew update
brew install render
```

### Direct Download (Linux/macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/render-oss/cli/refs/heads/main/bin/install.sh | sh
```

### From Source (Go required)

```bash
git clone git@github.com:render-oss/cli.git
cd cli
go build -o render
```

### Verify Installation

```bash
render --version
```

## Authentication

### Interactive Login (Development)

```bash
render login
```

ブラウザが開き、"Generate token"をクリックしてトークンを生成。その後ワークスペースを選択します。

### API Key Authentication (CI/CD Automation)

```bash
# 環境変数でAPIキーを設定
export RENDER_API_KEY=rnd_RUExip...

# 以降のコマンドは自動的に認証される
render services
```

**Note**: APIキーはCLIトークンより優先されます。長期未使用時はトークンが期限切れになることがあります。

## Core Commands Reference

### Workspace Management

```bash
# アクティブなワークスペースを設定
render workspace set

# ワークスペース一覧を表示
render workspace list
```

### Services

```bash
# サービス一覧を表示（インタラクティブ）
render services

# JSON形式で出力
render services -o json

# 特定のサービス詳細
render services show srv-abc123
```

### Deploys

```bash
# デプロイを実行（インタラクティブ）
render deploys create

# 特定サービスのデプロイ
render deploys create srv-abc123

# デプロイ完了まで待機
render deploys create srv-abc123 --wait

# 特定のGitコミットをデプロイ
render deploys create srv-abc123 --commit abc123def

# 特定のDockerイメージをデプロイ
render deploys create srv-abc123 --image registry.example.com/app:v1.0

# デプロイ履歴を表示
render deploys list srv-abc123
```

### Logs

```bash
# ログを表示（インタラクティブ）
render logs

# 特定サービスのログ
render logs srv-abc123

# リアルタイムでログをフォロー
render logs srv-abc123 --tail

# JSON形式で出力
render logs srv-abc123 -o json
```

### PostgreSQL (psql)

```bash
# PostgreSQLに接続（インタラクティブ）
render psql

# 特定のデータベースに接続
render psql dpg-abc123
```

### SSH

```bash
# SSHでサービスに接続（インタラクティブ）
render ssh

# 特定のサービスに接続
render ssh srv-abc123
```

**Standard SSH (Alternative):**

```bash
ssh YOUR_SERVICE@ssh.YOUR_REGION.render.com

# 特定インスタンスに接続
ssh srv-abc123-d4e5f@ssh.oregon.render.com

# 詳細モード（トラブルシューティング用）
ssh -v YOUR_SERVICE@ssh.YOUR_REGION.render.com
```

**Note**: SSH対応はペイドサービス（Web Services, Private Services, Background Workers）のみ。Freeサービスは非対応。

### Service Restart

```bash
# サービスを再起動
render restart srv-abc123
```

### Jobs

```bash
# ワンオフジョブをトリガー
render jobs create srv-abc123
```

## Output Formats

### Available Formats

```bash
# JSON形式
render services -o json

# YAML形式
render services -o yaml

# テキスト形式（デフォルト）
render services -o text
```

### Automation Flags

```bash
# 確認プロンプトをスキップ
render deploys create srv-abc123 --confirm

# 完了まで待機
render deploys create srv-abc123 --wait
```

## CI/CD Integration Patterns

### GitHub Actions Example

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Render CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/render-oss/cli/refs/heads/main/bin/install.sh | sh

      - name: Deploy
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          render deploys create ${{ secrets.RENDER_SERVICE_ID }} --wait --confirm
```

### Shell Script Pattern

```bash
#!/bin/bash
set -e

# APIキーを環境変数から取得
export RENDER_API_KEY="${RENDER_API_KEY}"

# サービスIDを指定
SERVICE_ID="srv-abc123"

# デプロイを実行して完了を待機
echo "Deploying to Render..."
render deploys create "$SERVICE_ID" --wait --confirm -o json

# デプロイ成功を確認
if [ $? -eq 0 ]; then
    echo "Deployment successful!"
else
    echo "Deployment failed!"
    exit 1
fi
```

## Configuration

### Config File Location

```
$HOME/.render/cli.yaml
```

### Custom Config Path

```bash
export RENDER_CLI_CONFIG_PATH=/path/to/custom/cli.yaml
```

## Common Patterns

### Pattern 1: Quick Deploy with Wait

```bash
# デプロイして完了まで待機、確認スキップ
render deploys create srv-abc123 --wait --confirm
```

### Pattern 2: Log Monitoring

```bash
# リアルタイムログ監視
render logs srv-abc123 --tail

# JSON形式でログを取得（ログ解析用）
render logs srv-abc123 -o json > logs.json
```

### Pattern 3: Database Backup via psql

```bash
# PostgreSQLに接続してバックアップ
render psql dpg-abc123 -c "\\copy (SELECT * FROM users) TO '/tmp/users.csv' WITH CSV HEADER"
```

### Pattern 4: Service Health Check

```bash
# サービス一覧をJSON取得
render services -o json | jq '.[] | {name, status}'
```

### Pattern 5: Bulk Operations Script

```bash
#!/bin/bash
# 複数サービスのステータス確認

SERVICES=$(render services -o json | jq -r '.[].id')

for svc in $SERVICES; do
    echo "Service: $svc"
    render services show "$svc" -o json | jq '{name, status, updatedAt}'
    echo "---"
done
```

## Troubleshooting

### Authentication Issues

```bash
# トークンの再生成
render login

# APIキーが正しく設定されているか確認
echo $RENDER_API_KEY
```

### SSH Connection Issues

```bash
# 詳細モードで接続をデバッグ
ssh -v YOUR_SERVICE@ssh.YOUR_REGION.render.com

# SSHキーが登録されているか確認
# Render Dashboard > Account Settings > SSH Keys
```

### Command Not Found

```bash
# PATHにrender CLIが含まれているか確認
which render

# Homebrewの場合は更新
brew upgrade render
```

## Best Practices

1. **CI/CD ではAPIキーを使用**: 環境変数 `RENDER_API_KEY` でAPIキーを設定
2. **`--wait`フラグを活用**: デプロイ完了を確認してから次のステップに進む
3. **JSON出力を活用**: 自動化スクリプトでは `-o json` でパース可能な出力を取得
4. **`--confirm`フラグで自動化**: 確認プロンプトをスキップして非対話的に実行
5. **サービスIDを変数化**: 環境変数でサービスIDを管理してハードコードを避ける
6. **シークレット管理**: APIキーをコードに直接書かず、環境変数やシークレット管理ツールを使用

## Resources

### Official Documentation

- [Render CLI Docs](https://render.com/docs/cli)
- [SSH Documentation](https://render.com/docs/ssh)
- [Render API Reference](https://api-docs.render.com/)

### scripts/

- `render_cli_updater.py`: 公式ドキュメントの定期更新チェックスクリプト

### references/

- `last_check.json`: 最終更新チェック日時の記録
- `cli_updates.md`: 最新の更新情報ログ（自動生成）
