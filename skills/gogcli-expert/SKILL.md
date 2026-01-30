---
name: gogcli-expert
description: gogcli（gog コマンド）の専門家スキル。Google Workspaceの13サービス（Gmail, Calendar, Drive, Sheets, Docs, Slides, Contacts, Tasks, Chat, Groups, Keep, Classroom, People）をターミナルから操作するGoベースCLIツールの使い方を支援。OAuth2/サービスアカウント認証、マルチアカウント管理、自動化パターンを提供。Use when working with Google Workspace services via CLI, managing Gmail/Calendar/Drive/Sheets, automating Google Workspace tasks, or setting up gogcli authentication.
---

# gogcli Expert

## Overview

gogcli（コマンド名: `gog`）は、Google Workspaceの13サービスをターミナルから操作するGoベースのCLIツールです。steipete/gogcli リポジトリで開発されています。

**対応サービス:**

| カテゴリ | サービス |
|---------|---------|
| Communication | Gmail, Calendar, Chat [Workspace only] |
| Productivity | Drive, Sheets, Docs, Slides, Tasks, Keep [Workspace + SA only] |
| Workspace Admin | Groups [Workspace only], Classroom, People, Contacts |
| Utility | Time（UTC/ローカル時刻表示） |

**主要特徴:**
- OAuth2 + サービスアカウント認証
- マルチアカウント・マルチクライアント対応
- `--json` / `--plain` 出力（パイプライン統合に最適）
- OSキーリングまたは暗号化ファイルによる認証情報の安全な保管
- シェル補完（Bash, Zsh, Fish, PowerShell）

## When to Use This Skill

このスキルを使用するタイミング:

- gogcli（gog コマンド）のインストール・セットアップ方法を知りたい
- Google Workspace サービスをCLIから操作したい
- Gmail の検索・送信・ラベル管理をターミナルで行いたい
- Calendar のイベント管理・空き時間確認をCLIで行いたい
- Drive のファイル操作・権限管理をCLIで自動化したい
- Sheets の読み書き・書式設定をスクリプトで行いたい
- OAuth2 認証やサービスアカウントの設定方法を知りたい
- マルチアカウント環境の設定方法を知りたい
- gogcli のエラーやトラブルを解決したい

**Example triggers:**
- "gog コマンドで Gmail を検索するには？"
- "gogcli でカレンダーのイベントを作成したい"
- "Drive のファイルをダウンロードするコマンドは？"
- "Sheets のデータを読み取るには？"
- "gogcli の認証設定を教えて"
- "gog コマンドでメール送信したい"
- "Google Workspace の CLI ツールを使いたい"
- "How do I search Gmail with gogcli?"
- "How to set up gogcli service account?"

## Installation & Prerequisites

### Installation

```bash
# macOS/Linux (Homebrew)
brew install steipete/tap/gogcli

# ソースからビルド
git clone https://github.com/steipete/gogcli.git
cd gogcli && make
./bin/gog --help

# バージョン確認
gog --version
```

### Shell Completions

```bash
# Bash
gog completion bash > $(brew --prefix)/etc/bash_completion.d/gog

# Zsh
gog completion zsh > "${fpath[1]}/_gog"

# Fish
gog completion fish > ~/.config/fish/completions/gog.fish

# PowerShell
gog completion powershell > gog.ps1
```

### Google Cloud Console Setup

gogcli を利用するには、Google Cloud Console で OAuth2 クレデンシャルを準備する必要があります:

1. Google Cloud Console でプロジェクトを作成（または既存プロジェクトを選択）
2. 必要な API を有効化（Gmail API, Calendar API, Drive API 等）
3. OAuth 同意画面を設定し、テストユーザーを追加
4. 「デスクトップアプリケーション」タイプのOAuth2クライアントIDを作成
5. クレデンシャル JSON をダウンロード

## Authentication Setup

### OAuth2 Basic Setup

```bash
# 1. クレデンシャルJSONを登録
gog auth credentials ~/Downloads/client_secret.json

# 2. アカウントを認証（ブラウザが開く）
gog auth add user@gmail.com

# 3. 認証確認
gog auth list

# 4. デフォルトアカウント確認
gog auth status
```

### Scope Control

認証時にサービスを限定できます（最小権限の原則）:

```bash
# 特定サービスのみ認証
gog auth add user@gmail.com --services drive,calendar

# 読み取り専用モード
gog auth add user@gmail.com --readonly

# Drive 固有のスコープ制御
gog auth add user@gmail.com --drive-scope full      # 完全アクセス
gog auth add user@gmail.com --drive-scope readonly   # 読み取り/ダウンロード/エクスポートのみ
gog auth add user@gmail.com --drive-scope file       # アプリ作成ファイルのみ書き込み可
```

### Adding Services Later

後からサービスを追加する場合、`--force-consent` が必要なことがあります:

```bash
gog auth add user@gmail.com --services sheets --force-consent
```

### Multiple Accounts

```bash
# 複数アカウントを追加
gog auth add personal@gmail.com
gog auth add work@company.com

# アカウント指定で実行
gog --account work@company.com calendar events --today

# エイリアス設定
gog auth alias set work work@company.com
gog auth alias set personal personal@gmail.com
gog auth alias list

# エイリアスで実行
gog --account work calendar events --today

# デフォルトアカウントを環境変数で設定
export GOG_ACCOUNT=work
```

### Multiple OAuth Clients

組織ごとに異なるOAuthクライアントを使用する場合:

```bash
# クライアント名付きでクレデンシャル登録
gog --client work auth credentials ~/work-client-secret.json
gog --client personal auth credentials ~/personal-client-secret.json

# クライアント指定で認証
gog --client work auth add user@company.com
gog --client personal auth add user@gmail.com
```

**ドメインマッピング（config.json）:**

```json5
{
  account_clients: { "user@company.com": "work" },
  client_domains: { "company.com": "work" }
}
```

### Service Account (Workspace Only)

ドメイン全体の委任（Domain-Wide Delegation）を使用する場合:

```bash
# サービスアカウント設定
gog auth service-account set admin@domain.com --key ~/service-account.json

# サービスアカウントが OAuth よりも優先される
# 確認
gog auth list
```

**前提条件:**
1. Google Cloud Console でサービスアカウントを作成
2. キーファイル（JSON）をダウンロード
3. Workspace 管理コンソールでドメイン全体の委任を設定
4. 必要なスコープを許可リストに追加

### Keyring Configuration

```bash
# キーリングバックエンド確認
gog auth keyring

# バックエンド設定（auto / keychain / file）
gog auth keyring auto      # プラットフォーム最適（デフォルト）
gog auth keyring keychain   # macOS Keychain
gog auth keyring file       # 暗号化ファイル（パスワード必要）

# CI/非対話環境用
export GOG_KEYRING_PASSWORD='your-secure-password'
```

## Core Services -- Communication

### Gmail

**スレッド・メッセージ検索:**

```bash
# 受信トレイの最新スレッド
gog gmail threads

# Gmail 検索構文で検索
gog gmail threads --query "from:boss@company.com subject:report"
gog gmail threads --query "is:unread after:2025/01/01"
gog gmail threads --query "has:attachment filename:pdf"

# メッセージ詳細表示
gog gmail messages --thread-id <thread-id>
gog gmail message <message-id>
```

**メール送信:**

```bash
# 基本送信
gog gmail send --to recipient@example.com --subject "件名" --body "本文"

# CC/BCC付き
gog gmail send --to a@example.com --cc b@example.com --bcc c@example.com \
  --subject "件名" --body "本文"

# HTML本文
gog gmail send --to recipient@example.com --subject "Report" --body-html "<h1>Report</h1><p>Details...</p>"

# 添付ファイル付き
gog gmail send --to recipient@example.com --subject "資料" --body "添付をご確認ください" \
  --attach report.pdf --attach data.xlsx

# 開封トラッキング（要事前設定）
gog gmail send --to recipient@example.com --body-html "<p>Hi</p>" --track
```

**ラベル管理:**

```bash
# ラベル一覧
gog gmail labels

# ラベル作成
gog gmail label create "Projects/Active"

# メッセージにラベル適用
gog gmail label apply <message-id> --label "Projects/Active"
```

**その他の機能:**

```bash
# 下書き
gog gmail drafts
gog gmail draft create --to recipient@example.com --subject "下書き" --body "内容"

# フィルタ
gog gmail filters

# 不在応答（バケーション設定）
gog gmail vacation --enable --subject "不在のお知らせ" --body "現在不在です"
gog gmail vacation --disable

# 委任
gog gmail delegates
```

### Calendar

**イベント管理:**

```bash
# 今日のイベント
gog calendar events --today

# 期間指定
gog calendar events --from 2025-02-01 --to 2025-02-28

# 今後7日間
gog calendar events --next 7d

# イベント作成
gog calendar event create --summary "ミーティング" \
  --start "2025-02-01T10:00:00" --end "2025-02-01T11:00:00" \
  --attendees "a@example.com,b@example.com"

# イベント更新
gog calendar event update <event-id> --summary "更新後のタイトル"

# イベント削除
gog calendar event delete <event-id>
```

**スケジュール管理:**

```bash
# 競合検出
gog calendar conflicts --from 2025-02-01 --to 2025-02-07

# 空き時間確認（Free/Busy）
gog calendar freebusy --emails "a@example.com,b@example.com" \
  --from 2025-02-01 --to 2025-02-07

# カレンダー一覧
gog calendar list
```

**特殊イベント:**

```bash
# フォーカスタイム
gog calendar event create --summary "Focus Time" --event-type focusTime \
  --start "2025-02-01T09:00:00" --end "2025-02-01T12:00:00"

# 不在（Out of Office）
gog calendar event create --summary "OOO" --event-type outOfOffice \
  --start "2025-02-10" --end "2025-02-14"

# 繰り返しイベント
gog calendar event create --summary "Weekly Standup" \
  --start "2025-02-03T09:00:00" --end "2025-02-03T09:30:00" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=MO"
```

### Chat [Workspace Only]

```bash
# スペース一覧
gog chat spaces

# メッセージ一覧
gog chat messages --space <space-id>

# メッセージ送信
gog chat send --space <space-id> --text "メッセージ内容"

# DM送信
gog chat dm --email colleague@company.com --text "Hi!"
```

## Core Services -- Productivity

### Drive

**ファイル操作:**

```bash
# ファイル一覧
gog drive list
gog drive list --query "name contains 'report'"

# ファイルダウンロード
gog drive download <file-id>
gog drive download <file-id> --output ./downloads/

# ファイルアップロード
gog drive upload report.pdf
gog drive upload report.pdf --folder <folder-id>

# Google Docs/Sheets/Slides のエクスポート
gog drive export <file-id> --mime application/pdf
gog drive export <file-id> --mime text/csv
```

**フォルダ管理:**

```bash
# フォルダ作成
gog drive folder create "Project Documents"
gog drive folder create "Subfolder" --parent <parent-folder-id>

# フォルダ内のファイル一覧
gog drive list --folder <folder-id>
```

**権限管理:**

```bash
# 権限一覧
gog drive permissions <file-id>

# 権限付与
gog drive share <file-id> --email user@example.com --role writer
gog drive share <file-id> --email user@example.com --role reader

# 共有ドライブ一覧
gog drive shared-drives
```

### Sheets

**データ読み取り:**

```bash
# シート全体の読み取り
gog sheets get <spreadsheet-id>

# 範囲指定（A1記法）
gog sheets get <spreadsheet-id> --range "Sheet1!A1:D10"
gog sheets get <spreadsheet-id> --range "Sheet1!A:A"

# JSON出力
gog sheets get <spreadsheet-id> --range "Sheet1!A1:D10" --json
```

**データ書き込み:**

```bash
# セル書き込み
gog sheets update <spreadsheet-id> --range "Sheet1!A1" --values "Hello,World"

# 行追加
gog sheets append <spreadsheet-id> --range "Sheet1!A1" --values "New,Row,Data"
```

**シート管理:**

```bash
# 新規スプレッドシート作成
gog sheets create --title "New Spreadsheet"

# シート一覧
gog sheets list <spreadsheet-id>
```

### Docs & Slides

Docs と Slides は主に Drive 経由のエクスポートで利用します:

```bash
# Google Docs → PDF
gog drive export <doc-id> --mime application/pdf

# Google Docs → DOCX
gog drive export <doc-id> --mime application/vnd.openxmlformats-officedocument.wordprocessingml.document

# Google Slides → PDF
gog drive export <slides-id> --mime application/pdf

# Google Slides → PPTX
gog drive export <slides-id> --mime application/vnd.openxmlformats-officedocument.presentationml.presentation
```

### Tasks

```bash
# タスクリスト一覧
gog tasks lists

# タスク一覧
gog tasks list <tasklist-id>

# タスク作成
gog tasks add <tasklist-id> --title "タスク名" --due 2025-02-15

# タスク完了
gog tasks done <tasklist-id> <task-id>

# タスク未完了に戻す
gog tasks undo <tasklist-id> <task-id>

# タスク削除
gog tasks delete <tasklist-id> <task-id>

# 完了済みタスクをクリア
gog tasks clear <tasklist-id>
```

## Core Services -- Workspace Admin

### Groups [Workspace Only]

```bash
# グループ一覧
gog groups list

# グループメンバー一覧
gog groups members <group-email>
```

### Classroom

```bash
# コース一覧
gog classroom courses

# コースの名簿（生徒一覧）
gog classroom roster <course-id>

# 課題（Coursework）一覧
gog classroom coursework <course-id>

# 提出物一覧
gog classroom submissions <course-id> <coursework-id>

# アナウンス
gog classroom announcements <course-id>
```

### People & Contacts

```bash
# 自分のプロフィール
gog people me

# Workspace ディレクトリ検索
gog people search "John Smith"

# 連絡先検索
gog contacts search "Jane"

# 連絡先作成
gog contacts create --name "Jane Doe" --email jane@example.com --phone "+1-555-0100"

# その他の連絡先（やり取り履歴から自動生成）
gog contacts other
```

## Output Formats & Global Flags

### Output Formats

```bash
# 人間可読形式（デフォルト）
gog gmail threads

# JSON出力（パイプライン統合に最適）
gog gmail threads --json
gog gmail threads --json | jq '.[] | .subject'

# プレーン出力（TSV形式）
gog gmail threads --plain

# 進捗メッセージは stderr に出力されるため、stdout をクリーンにパイプ可能
gog drive list --json 2>/dev/null | jq '.[] | .name'
```

### Global Flags

| フラグ | 説明 |
|-------|------|
| `--account <email\|alias\|auto>` | 使用するアカウントを選択 |
| `--client <name>` | OAuth クライアントを選択 |
| `--json` | JSON 出力 |
| `--plain` | TSV 出力 |
| `--color <auto\|always\|never>` | カラー出力制御 |
| `--force` | 確認プロンプトをスキップ |
| `--no-input` | プロンプト時にエラー終了（CI向け） |
| `--verbose` | 詳細ログ出力 |
| `--enable-commands <csv>` | 使用可能コマンドを制限（サンドボックス） |

### Environment Variables

| 変数 | 説明 |
|-----|------|
| `GOG_ACCOUNT` | デフォルトアカウント |
| `GOG_CLIENT` | デフォルトOAuthクライアント |
| `GOG_JSON` | デフォルトJSON出力（`1` or `true`） |
| `GOG_PLAIN` | デフォルトプレーン出力（`1` or `true`） |
| `GOG_COLOR` | カラーモード |
| `GOG_TIMEZONE` | タイムゾーン（IANA名, `UTC`, `local`） |
| `GOG_ENABLE_COMMANDS` | コマンド許可リスト |
| `GOG_KEYRING_BACKEND` | キーリングバックエンド |
| `GOG_KEYRING_PASSWORD` | 暗号化キーリングのパスワード |

## Configuration

### Config File

```bash
# 設定ファイルの場所を表示
gog config path
# macOS: ~/Library/Application Support/gogcli/config.json
# Linux: ~/.config/gogcli/config.json (XDG_CONFIG_HOME準拠)
# Windows: %AppData%\gogcli\config.json

# 設定一覧
gog config list

# 値の取得・設定
gog config get default_timezone
gog config set default_timezone "Asia/Tokyo"
gog config unset default_timezone
```

**config.json の例:**

```json5
{
  keyring_backend: "auto",
  default_timezone: "Asia/Tokyo",
  account_aliases: {
    work: "user@company.com",
    personal: "user@gmail.com"
  },
  account_clients: {
    "user@company.com": "work"
  },
  client_domains: {
    "company.com": "work"
  }
}
```

## Common Patterns

### 1. 日次メールダイジェスト

```bash
# 今日の未読メールをJSON取得 → jq でサマリ化
gog gmail threads --query "is:unread newer_than:1d" --json | \
  jq -r '.[] | "\(.from) | \(.subject)"'
```

### 2. 今日のスケジュール確認

```bash
# 今日のイベント一覧
gog calendar events --today

# JSON出力で処理
gog calendar events --today --json | jq -r '.[] | "\(.start) - \(.summary)"'
```

### 3. チームの空き時間検索

```bash
# 複数メンバーの空き時間を確認
gog calendar freebusy \
  --emails "alice@company.com,bob@company.com,carol@company.com" \
  --from "2025-02-03T09:00:00" --to "2025-02-03T18:00:00"
```

### 4. ファイルの一括ダウンロード

```bash
# 特定フォルダ内のファイルIDを取得してダウンロード
gog drive list --folder <folder-id> --json | \
  jq -r '.[].id' | \
  xargs -I{} gog drive download {} --output ./downloads/
```

### 5. Sheets データのCSVエクスポート

```bash
# Sheets → プレーン出力（TSV）でリダイレクト
gog sheets get <spreadsheet-id> --range "Sheet1!A1:Z100" --plain > data.tsv
```

### 6. サンドボックス実行（エージェント用）

```bash
# calendar と tasks のみ許可
gog --enable-commands calendar,tasks calendar events --today

# 環境変数で制限
export GOG_ENABLE_COMMANDS=gmail,drive
gog gmail threads  # OK
gog calendar events  # ブロックされる
```

### 7. CI/CD パイプラインでの使用

```bash
# 非対話モード + 暗号化キーリング
export GOG_KEYRING_PASSWORD='secure-password'
export GOG_ACCOUNT=ci-bot@company.com
export GOG_JSON=1

# エラー時にプロンプトではなく即座に失敗
gog --no-input gmail send --to team@company.com \
  --subject "Build Report" --body "Build #123 passed"
```

### 8. マルチアカウント切り替え

```bash
# エイリアス設定
gog auth alias set work work@company.com
gog auth alias set personal personal@gmail.com

# エイリアスで使い分け
gog --account work gmail threads
gog --account personal gmail threads

# 一時的な切り替え
GOG_ACCOUNT=work gog calendar events --today
```

## Security Best Practices

### Least Privilege Authentication

```bash
# 必要なサービスのみ認証
gog auth add user@gmail.com --services gmail,calendar

# 読み取り専用で十分な場合
gog auth add user@gmail.com --readonly

# Drive は file スコープで制限
gog auth add user@gmail.com --drive-scope file
```

### Command Sandboxing

エージェントや自動化スクリプトに gogcli を使わせる場合:

```bash
# 使用可能コマンドを制限
export GOG_ENABLE_COMMANDS=calendar,tasks

# 確認プロンプトをスキップしない（デフォルト）
# --force は明示的に必要な場合のみ使用
```

### Credential Management

- OS キーリング（`auto` or `keychain`）を推奨
- `file` バックエンドはパスワード保護必須
- CI 環境では `GOG_KEYRING_PASSWORD` を安全に管理（シークレットマネージャ等）
- クレデンシャル JSON は安全な場所に保管し、バージョン管理に含めない
- サービスアカウントキーは定期的にローテーション

### Multi-Account Security

- 本番環境と開発環境でアカウントを分離
- `--account` を明示指定して誤操作を防止
- 環境変数 `GOG_ACCOUNT` でデフォルトアカウントを明確に設定

## Troubleshooting

### Quick Reference

| 症状 | 原因 | 対策 |
|-----|------|------|
| `token has been expired or revoked` | リフレッシュトークン失効 | `gog auth add <email>` で再認証 |
| `insufficient permission` / 403 | スコープ不足 | `gog auth add <email> --services <svc> --force-consent` |
| コマンドがブロックされる | `--enable-commands` 制限 | 環境変数 `GOG_ENABLE_COMMANDS` を確認 |
| キーリングエラー | バックエンド問題 | `gog auth keyring auto` でリセット |
| タイムゾーンが違う | 未設定 | `gog config set default_timezone "Asia/Tokyo"` |
| サービスアカウントエラー | 委任未設定 | Workspace 管理コンソールでスコープを許可 |

詳細なトラブルシューティングは `references/troubleshooting.md` を参照。

## Resources

このスキルには以下のリファレンスが含まれます:

| ファイル | 内容 |
|---------|------|
| `references/quick_reference.md` | 全13サービスのコマンドチートシート |
| `references/communication_services.md` | Gmail/Calendar/Chat の詳細ガイド |
| `references/productivity_services.md` | Drive/Sheets/Docs/Slides/Tasks/Keep の詳細ガイド |
| `references/workspace_admin_services.md` | Groups/Classroom/People + サービスアカウント詳細 |
| `references/troubleshooting.md` | トラブルシューティング詳細ガイド |

**公式リポジトリ:** https://github.com/steipete/gogcli
