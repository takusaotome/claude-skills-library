---
name: gogcli-expert
description: gogcli（gog コマンド）の専門家スキル。Google Workspace と関連サービス25以上（Gmail, Calendar, Chat, Drive, Sheets, Docs, Slides, Tasks, Keep, Contacts, People, Groups, Admin, Classroom, Forms, Meet, Maps, YouTube, Photos, Sites, Analytics, Search Console, Apps Script, Zoom）をターミナルから操作するGoベースCLIツールの使い方を支援。OAuth2/サービスアカウント認証、マルチアカウント管理、自動化・エージェント安全機能を提供。Use when working with Google Workspace services via CLI, managing Gmail/Calendar/Drive/Sheets, automating Google Workspace tasks, or setting up gogcli authentication.
---

# gogcli Expert

## Overview

gogcli（コマンド名: `gog`）は、Google Workspace と関連サービスをターミナルから操作するGoベースのCLIツールです。`openclaw/gogcli` リポジトリで開発されています。本スキルは **v0.27.0** を基準にしています。

**対応サービス（25以上）:**

| カテゴリ | サービス |
|---------|---------|
| Communication | Gmail, Calendar, Chat [Workspace] |
| Productivity | Drive, Sheets, Docs, Slides, Tasks, Keep [Workspace + SA] |
| People | Contacts, People |
| Workspace Admin | Groups, Admin [Directory API], Classroom |
| Content/Media | Forms, Meet, Photos, Sites, YouTube |
| External/Data | Maps, Analytics [GA4], Search Console, Apps Script, Zoom |
| Utility | Time, backup（暗号化バックアップ）, batch, mcp（MCPサーバ） |

**主要特徴:**
- OAuth2 + サービスアカウント認証
- マルチアカウント・マルチクライアント対応
- `--json` / `--plain` 出力でパイプライン統合に最適
- OSキーリングまたは暗号化ファイルによる認証情報の安全な保管
- エージェント安全機能: `--gmail-no-send`、`--dry-run`、`--enable-commands` / `--disable-commands`、`mcp` サブコマンド
- シェル補完（Bash, Zsh, Fish, PowerShell）

**バージョン確認:**

```bash
gog --version    # 例: v0.27.0 (274a2a61 ...)
```

## Prerequisites

このスキルを使用する前に以下を準備してください:

1. **gogcli のインストール**
   - macOS/Linux: `brew install openclaw/tap/gogcli`
   - または GitHub からソースビルド

2. **Google Cloud Console でのセットアップ**
   - Google Cloud プロジェクト
   - 必要な API の有効化（Gmail API, Calendar API, Drive API 等）
   - OAuth 同意画面の設定とテストユーザー追加
   - 「デスクトップアプリケーション」タイプの OAuth2 クライアント ID 作成
   - クレデンシャル JSON のダウンロード

3. **初期認証**
   - `gog auth credentials set <path-to-json>` でクレデンシャル登録
   - `gog auth add <email>`（別名 `gog login <email>`）でアカウント認証

## Workflow

gogcli を使った基本的なワークフロー:

```
1. セットアップ
   └─> gog auth credentials set ~/client_secret.json
   └─> gog auth add user@gmail.com        # 別名: gog login user@gmail.com
   └─> gog status                          # 認証・設定確認（別名: gog auth status）

2. 日常操作
   ├─> Gmail: gog gmail search "is:unread" / gog gmail send ...
   ├─> Calendar: gog calendar events --today
   ├─> Drive: gog drive ls / gog drive download <id>
   └─> Sheets: gog sheets get <id> <range>

3. 自動化・スクリプト統合
   └─> --json 出力 + jq でパース
   └─> CI/CD: GOG_KEYRING_PASSWORD + --no-input

4. マルチアカウント管理
   └─> gog auth alias set work user@company.com
   └─> gog --account work <command>

5. 不調時の診断
   └─> gog auth doctor --check            # 認証・キーリング・トークンを診断
```

## When to Use This Skill

このスキルを使用するタイミング:

- gogcli（gog コマンド）のインストール・セットアップ方法を知りたい
- Google Workspace サービスをCLIから操作したい
- Gmail の検索・送信・ラベル管理をターミナルで行いたい
- Calendar のイベント管理・空き時間確認をCLIで行いたい
- Drive のファイル操作・権限管理をCLIで自動化したい
- Sheets / Docs / Slides の読み書き・書式設定をスクリプトで行いたい
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
- "How do I search Gmail with gogcli?"
- "How to set up gogcli service account?"

## Installation

```bash
# macOS/Linux (Homebrew)
brew install openclaw/tap/gogcli

# tap が untrusted 扱いでブロックされる場合は一度信頼する
brew trust openclaw/tap
brew install openclaw/tap/gogcli

# 既存環境のアップグレード
brew upgrade gogcli

# ソースからビルド
git clone https://github.com/openclaw/gogcli.git
cd gogcli && make
./bin/gog --version

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

gogcli を利用するには、Google Cloud Console で OAuth2 クレデンシャルを準備します:

1. Google Cloud Console でプロジェクトを作成または選択
2. 必要な API を有効化（Gmail API, Calendar API, Drive API 等）
3. OAuth 同意画面を設定し、テストユーザーを追加
4. 「デスクトップアプリケーション」タイプの OAuth2 クライアント ID を作成
5. クレデンシャル JSON をダウンロード

## Authentication Setup

### OAuth2 Basic Setup

```bash
# 1. クレデンシャルJSONを登録（v0.27 では credentials set サブコマンド）
gog auth credentials set ~/Downloads/client_secret.json

# 2. アカウントを認証（ブラウザが開く）。別名 gog login
gog auth add user@gmail.com

# 3. 認証済みアカウント一覧
gog auth list

# 4. 認証・設定状態の確認
gog status              # gog auth status と同じ
```

### Scope Control

認証時にサービスやスコープを限定できます（最小権限の原則）:

```bash
# 特定サービスのみ認証（--services はカンマ区切り）
gog auth add user@gmail.com --services gmail,calendar,drive

# 読み取り専用スコープ
gog auth add user@gmail.com --readonly

# Gmail / Drive 固有のスコープ制御
gog auth add user@gmail.com --gmail-scope readonly   # full|readonly
gog auth add user@gmail.com --drive-scope readonly    # full|readonly|file
```

利用可能なサービス名は `gog auth services` で一覧できます。代表例: `gmail, calendar, chat, classroom, drive, docs, slides, contacts, tasks, sheets, people, forms, sites, meet, appscript, analytics, searchconsole, youtube, photos`。`admin, groups, keep` はサービスアカウント専用です。

### Adding Services Later

後からサービスを追加する場合、再同意が必要なことがあります:

```bash
gog auth add user@gmail.com --services sheets --force-consent
```

### Multiple Accounts

```bash
# 複数アカウントを追加
gog auth add personal@gmail.com
gog auth add work@company.com

# アカウント指定で実行（-a は --account の短縮）
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

組織ごとに異なる OAuth クライアントを使用する場合:

```bash
# クライアント名付きでクレデンシャル登録
gog --client work auth credentials set ~/work-client-secret.json
gog --client personal auth credentials set ~/personal-client-secret.json

# クライアント指定で認証
gog --client work auth add user@company.com
gog --client personal auth add user@gmail.com

# ドメインを直接マッピング
gog auth credentials set ~/work-client-secret.json --domain company.com
```

### Service Account (Workspace Only)

ドメイン全体の委任を使用する場合:

```bash
# サービスアカウントキーを登録（email は impersonation 対象）
gog auth service-account set admin@domain.com --key ~/service-account.json

# 状態確認
gog auth service-account status admin@domain.com

# 解除
gog auth service-account unset admin@domain.com
```

**前提条件:**
1. Google Cloud Console でサービスアカウントを作成
2. キーファイル（JSON）をダウンロード
3. Workspace 管理コンソールでドメイン全体の委任を設定
4. 必要なスコープを許可リストに追加

Google Keep はサービスアカウント専用です。`gog auth keep --key ~/sa.json <email>` で設定します。

### Keyring Configuration

```bash
# キーリングバックエンド確認・設定（auto / keychain / file）
gog auth keyring
gog auth keyring auto       # プラットフォーム最適（デフォルト）
gog auth keyring keychain    # macOS Keychain
gog auth keyring file        # 暗号化ファイル（パスワード必要）

# CI・非対話環境用
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSWORD='your-secure-password'
```

> ⚠️ **バージョン更新後のキーリング・タイムアウト:** gog のバイナリが更新されると macOS Keychain がアクセス許可を再要求します。非対話実行だと `keyring connection timed out after 10s` で失敗します。ターミナルで一度 `gog auth list` を実行し、Keychain プロンプトで「常に許可」を押してください。詳細は `references/troubleshooting.md` 参照。

### Diagnostics

```bash
# 認証・キーリング・リフレッシュトークンを総合診断
gog auth doctor

# リフレッシュトークンを実際に交換して検証
gog auth doctor --check
gog auth list --check
```

## Core Services -- Communication

### Gmail

**スレッド・メッセージ検索（v0.27 ではクエリ必須）:**

```bash
# スレッド検索（別名 list/ls/find/query）。クエリは Gmail 検索構文
gog gmail search "in:inbox" --max 10
gog gmail search "from:boss@company.com subject:report"
gog gmail search "is:unread newer_than:7d"
gog gmail search "has:attachment filename:pdf"

# メッセージ単位の検索
gog gmail messages search "is:unread"

# メッセージ詳細（full|metadata|raw）
gog gmail get <messageId>
gog gmail get <messageId> --format metadata --headers "From,Subject,Date"

# スレッド全体を取得
gog gmail thread get <threadId>
```

**メール送信:**

```bash
# 基本送信（トップレベル別名 gog send も可）
gog gmail send --to recipient@example.com --subject "件名" --body "本文"

# CC/BCC付き
gog gmail send --to a@example.com --cc b@example.com --bcc c@example.com \
  --subject "件名" --body "本文"

# HTML本文
gog gmail send --to recipient@example.com --subject "Report" --body-html "<h1>Report</h1><p>...</p>"

# 添付ファイル付き（--attach は繰り返し可）
gog gmail send --to recipient@example.com --subject "資料" --body "添付をご確認ください" \
  --attach report.pdf --attach data.xlsx

# 返信（元メッセージのスレッドに紐付け）
gog gmail reply <messageId> --body "了解しました"
```

**ラベル管理:**

```bash
# ラベル一覧
gog gmail labels list

# ラベル作成
gog gmail labels create "Projects/Active"

# メッセージのラベルを変更（付与/除去。--add / --remove はカンマ区切り）
gog gmail messages modify <messageId> --add "Projects/Active"
gog gmail thread modify <threadId> --add STARRED
```

**整理・その他:**

```bash
# アーカイブ / ゴミ箱 / 既読・未読
gog gmail archive <messageId>
gog gmail trash <messageId>
gog gmail mark-read <messageId>
gog gmail unread <messageId>

# 下書き
gog gmail drafts list
gog gmail drafts create --to recipient@example.com --subject "下書き" --body "内容"
gog gmail drafts send <draftId>
```

> ⚠️ **`drafts delete` のデータ消失注意:** CLI で作った下書きを Gmail Web 画面から送信すると孤立ドラフトが残り、その `draft-id` を `gog gmail drafts delete` すると**送信済みメールごと完全削除**されます（ゴミ箱にも残らない）。`drafts update` が **`Message not a draft`** を返したら「送信済み」のサインなので**削除しない**こと。詳細は `references/troubleshooting.md` 参照。

**設定（filters/vacation/delegates 等は settings 配下）:**

```bash
# フィルタ
gog gmail settings filters list

# 不在応答（バケーション）
gog gmail settings vacation get
gog gmail settings vacation update --enable --subject "不在のお知らせ" --body "現在不在です"

# 委任
gog gmail settings delegates list
```

### Calendar

**イベント管理:**

```bash
# 今日のイベント
gog calendar events --today

# 今後N日間 / 今週
gog calendar events --days 7
gog calendar events --week

# 期間指定（全カレンダー横断は --all）
gog calendar events --from 2026-02-01 --to 2026-02-28 --all

# イベント作成（calendarId は primary など。別名 add/new）
gog calendar create primary --summary "ミーティング" \
  --from "2026-02-01T10:00:00" --to "2026-02-01T11:00:00" \
  --attendees "a@example.com,b@example.com" --with-meet

# イベント更新・削除
gog calendar update <eventId> --summary "更新後のタイトル"
gog calendar delete <eventId>

# 単一イベント取得
gog calendar event <eventId>
```

**スケジュール管理:**

```bash
# カレンダー一覧
gog calendar calendars

# 競合検出
gog calendar conflicts --from 2026-02-01 --to 2026-02-07

# 空き時間確認（--cal は繰り返し可。メールはカレンダーIDとして使える）
gog calendar freebusy --cal a@example.com --cal b@example.com \
  --from "2026-02-01T09:00:00Z" --to "2026-02-07T18:00:00Z"

# 招待への応答（calendarId と eventId は位置引数）
gog calendar respond primary <eventId> --status accepted
```

**特殊イベント:**

```bash
# フォーカスタイム
gog calendar focus-time --from "2026-02-01T09:00:00" --to "2026-02-01T12:00:00"

# 不在（Out of Office）
gog calendar out-of-office --from "2026-02-10" --to "2026-02-14"

# 繰り返しイベント（--rrule は繰り返し可）
gog calendar create primary --summary "Weekly Standup" \
  --from "2026-02-03T09:00:00" --to "2026-02-03T09:30:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO"
```

### Chat [Workspace Only]

```bash
# スペース一覧
gog chat spaces list

# メッセージ一覧（spaceId は位置引数。spaces/... 形式）
gog chat messages list <spaceId>

# メッセージ送信
gog chat messages send <spaceId> --text "メッセージ内容"

# DM送信（email は位置引数）
gog chat dm send colleague@company.com --text "Hi!"
```

詳細は `references/communication_services.md` を参照。

## Core Services -- Productivity

### Drive

```bash
# ファイル一覧（トップレベル別名 gog ls も可）
gog drive ls
gog drive ls --query "name contains 'report'"
gog drive ls --parent <folderId>

# 全文検索
gog drive search "quarterly report"

# ダウンロード（Google 形式は自動エクスポート）
gog drive download <fileId>
gog drive download <fileId> --format pdf --out ./downloads/report.pdf

# アップロード（gog upload も可）
gog drive upload report.pdf --parent <folderId>
gog drive upload notes.md --convert-to doc       # ネイティブ Google 形式に変換

# フォルダ作成・ツリー表示
gog drive mkdir "Project Documents"
gog drive tree <folderId>

# 共有・権限（--to で共有先種別を指定）
gog drive share <fileId> --to user --email user@example.com --role writer
gog drive permissions <fileId>

# 共有ドライブ一覧
gog drive drives
```

### Sheets

```bash
# 読み取り（spreadsheetId と range は位置引数。A1 記法）
gog sheets get <spreadsheetId> "Sheet1!A1:D10"
gog sheets get <spreadsheetId> "Sheet1!A:A" --render FORMULA

# 書き込み（values は位置引数）
gog sheets update <spreadsheetId> "Sheet1!A1" "Hello" "World"
gog sheets update <spreadsheetId> "Sheet1!A1:B2" --values-json '[["a","b"],["c","d"]]'

# 追記
gog sheets append <spreadsheetId> "Sheet1!A1" "New" "Row" "Data"

# 新規作成・メタデータ
gog sheets create --title "New Spreadsheet"
gog sheets metadata <spreadsheetId>

# エクスポート（pdf|xlsx|csv）
gog sheets export <spreadsheetId> --format csv --out data.csv
```

Sheets は書式・チャート・条件付き書式・テーブル・名前付き範囲など多数のサブコマンドがあります。詳細は `references/productivity_services.md` を参照。

### Docs & Slides

v0.27 では Docs / Slides がフル編集に対応しています。

```bash
# Docs: 作成・本文取得・エクスポート
gog docs create --title "新規ドキュメント"
gog docs cat <docId>                              # プレーンテキストで取得
gog docs export <docId> --format pdf --out doc.pdf  # pdf|docx|txt|md|html
gog docs find-replace <docId> "旧称" "新称"           # find / replace は位置引数

# Slides: Markdown からスライド生成・エクスポート（title は位置引数、本文は --content-file）
gog slides create-from-markdown "プレゼン" --content-file deck.md
gog slides export <presentationId> --format pptx --out deck.pptx
```

### Tasks

```bash
# タスクリスト一覧（lists はグループ化。list サブコマンドが必要）
gog tasks lists list

# タスク一覧（tasklistId は位置引数）
gog tasks list <tasklistId>

# タスク作成（--title 必須）
gog tasks add <tasklistId> --title "タスク名" --due 2026-02-15

# 完了 / 未完了化 / 削除 / 完了クリア
gog tasks done <tasklistId> <taskId>
gog tasks undo <tasklistId> <taskId>
gog tasks delete <tasklistId> <taskId>
gog tasks clear <tasklistId>
```

### Keep [Workspace + Service Account]

```bash
gog keep list
gog keep create --title "メモ" --text "本文"
gog keep search "キーワード"
```

詳細は `references/productivity_services.md` を参照。

## Core Services -- People & Admin

### People & Contacts

```bash
# 自分のプロフィール（トップレベル別名 gog me / gog whoami）
gog people me

# Workspace ディレクトリ検索
gog people search "John Smith"

# 連絡先検索・作成・一覧
gog contacts search "Jane"
gog contacts create --name "Jane Doe" --email jane@example.com --phone "+1-555-0100"
gog contacts list

# その他の連絡先（やり取り履歴から自動生成）
gog contacts other list
```

### Groups & Admin

```bash
# Cloud Identity Groups（Workspace のみ）
gog groups list
gog groups members <groupEmail>

# Directory API（ドメイン全体委任が必要）
gog admin users list
gog admin groups list
```

### Classroom

```bash
gog classroom courses list
gog classroom roster <courseId>
gog classroom coursework list <courseId>
gog classroom submissions list <courseId> <courseworkId>
```

詳細・新サービス（Forms, Meet, Maps, YouTube, Photos, Sites, Analytics, Search Console, Apps Script, Zoom）は `references/workspace_admin_services.md` を参照。

## Output Formats & Global Flags

### Output Formats

```bash
# 人間可読形式（デフォルト）
gog gmail search "in:inbox"

# JSON出力（パイプライン統合に最適）
gog gmail search "in:inbox" --json
gog gmail search "in:inbox" --json | jq '.[] | .subject'

# プレーン出力（TSV形式）
gog gmail search "in:inbox" --plain

# JSON モードで主要結果のみ / フィールド選択
gog drive ls --json --results-only
gog drive ls --json --select "id,name"

# 進捗メッセージは stderr に出力されるため、stdout をクリーンにパイプ可能
gog drive ls --json 2>/dev/null | jq '.[] | .name'
```

### Global Flags

| フラグ | 説明 |
|-------|------|
| `-a, --account <email\|alias\|auto>` | 使用するアカウントを選択 |
| `--client <name>` | OAuth クライアントを選択 |
| `--access-token <token>` | アクセストークンを直接指定（リフレッシュトークンをバイパス、約1hで失効） |
| `-j, --json` | JSON 出力 |
| `-p, --plain` | TSV 出力 |
| `--results-only` | JSON で主要結果のみ出力（envelope を除外） |
| `--select <csv>` | JSON で指定フィールドのみ出力 |
| `--wrap-untrusted` | 取得テキストを untrusted-content マーカーで囲む |
| `--color <auto\|always\|never>` | カラー出力制御 |
| `-n, --dry-run` | 変更を行わず実行予定だけ表示 |
| `-y, --force` | 確認プロンプトをスキップ |
| `--no-input` | プロンプト時にエラー終了（CI向け） |
| `--gmail-no-send` | Gmail 送信操作をブロック（エージェント安全） |
| `--enable-commands <csv>` | 使用可能コマンドを制限（サンドボックス） |
| `--disable-commands <csv>` | 指定コマンドを無効化 |
| `--home <dir>` | config/data/state/cache のルートを上書き |
| `-v, --verbose` | 詳細ログ出力 |

### Environment Variables

| 変数 | 説明 |
|-----|------|
| `GOG_ACCOUNT` | デフォルトアカウント |
| `GOG_CLIENT` | デフォルトOAuthクライアント |
| `GOG_ACCESS_TOKEN` | アクセストークンの直接指定 |
| `GOG_JSON` | デフォルトJSON出力（`1` or `true`） |
| `GOG_PLAIN` | デフォルトプレーン出力（`1` or `true`） |
| `GOG_COLOR` | カラーモード |
| `GOG_TIMEZONE` | タイムゾーン（IANA名, `UTC`, `local`） |
| `GOG_HOME` | config/data/state/cache のルート |
| `GOG_ENABLE_COMMANDS` | コマンド許可リスト |
| `GOG_KEYRING_BACKEND` | キーリングバックエンド（`auto`/`keychain`/`file`） |
| `GOG_KEYRING_PASSWORD` | 暗号化キーリングのパスワード |

## Configuration

### Config File

```bash
# 設定ファイルの場所を表示
gog config path
# macOS: ~/Library/Application Support/gogcli/config.json
# Linux: ~/.config/gogcli/config.json (XDG_CONFIG_HOME準拠)
# Windows: %AppData%\gogcli\config.json

# 設定キー一覧 / 全値一覧
gog config keys
gog config list

# 値の取得・設定・削除
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
gog gmail search "is:unread newer_than:1d" --json | \
  jq -r '.[] | "\(.from) | \(.subject)"'
```

### 2. 今日のスケジュール確認

```bash
gog calendar events --today
gog calendar events --today --json | jq -r '.[] | "\(.start) - \(.summary)"'
```

### 3. チームの空き時間検索

```bash
gog calendar freebusy \
  --cal alice@company.com --cal bob@company.com --cal carol@company.com \
  --from "2026-02-03T09:00:00Z" --to "2026-02-03T18:00:00Z"
```

### 4. ファイルの一括ダウンロード

```bash
# 特定フォルダ内のファイルIDを取得してダウンロード
gog drive ls --parent <folderId> --json | \
  jq -r '.[].id' | \
  xargs -I{} gog drive download {} --out ./downloads/
```

### 5. Sheets データのCSVエクスポート

```bash
gog sheets export <spreadsheetId> --format csv --out data.csv
```

### 6. サンドボックス実行（エージェント用）

```bash
# calendar と tasks のみ許可
gog --enable-commands calendar,tasks calendar events --today

# Gmail 送信だけを禁止
gog --gmail-no-send gmail search "in:inbox"

# 変更前にドライラン
gog --dry-run calendar delete <eventId>

# 環境変数で制限
export GOG_ENABLE_COMMANDS=gmail,drive
```

### 7. CI/CD パイプラインでの使用

```bash
# 非対話モード + 暗号化キーリング
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSWORD='secure-password'
export GOG_ACCOUNT=ci-bot@company.com
export GOG_JSON=1

gog --no-input gmail send --to team@company.com \
  --subject "Build Report" --body "Build #123 passed"
```

### 8. MCP サーバとして公開（読み取り専用がデフォルト）

```bash
# 許可ツールを限定して stdio で MCP サーバを起動
gog mcp --allow-tool "gmail.*,drive_get"

# 有効なツールを確認
gog mcp --list-tools
```

## Security Best Practices

### Least Privilege Authentication

```bash
gog auth add user@gmail.com --services gmail,calendar
gog auth add user@gmail.com --readonly
gog auth add user@gmail.com --drive-scope file
```

### Command Sandboxing

エージェントや自動化スクリプトに gogcli を使わせる場合:

```bash
export GOG_ENABLE_COMMANDS=calendar,tasks
# 送信系を止めたいときは --gmail-no-send、破壊操作の前は --dry-run を併用
```

### Credential Management

- OS キーリング（`auto` or `keychain`）を推奨
- `file` バックエンドはパスワード保護必須
- CI 環境では `GOG_KEYRING_PASSWORD` を安全に管理
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
| `keyring connection timed out after 10s` | バイナリ更新で macOS Keychain が許可を再要求 | ターミナルで `gog auth list` を実行し「常に許可」。または `GOG_KEYRING_BACKEND=file` + `GOG_KEYRING_PASSWORD` |
| `token has been expired or revoked` | リフレッシュトークン失効 | `gog auth add <email>` で再認証。`gog auth doctor --check` で診断 |
| `insufficient permission` / 403 | スコープ不足 | `gog auth add <email> --services <svc> --force-consent` |
| `Refusing to load formula ... untrusted tap` | Homebrew の tap 信頼未承認 | `brew trust openclaw/tap` |
| コマンドがブロックされる | `--enable-commands` 制限 | 環境変数 `GOG_ENABLE_COMMANDS` を確認 |
| タイムゾーンが違う | 未設定 | `gog config set default_timezone "Asia/Tokyo"` |
| サービスアカウントエラー | 委任未設定 | Workspace 管理コンソールでスコープを許可 |
| `drafts update` が `Message not a draft` | その下書きは**送信済み**（孤立ドラフト） | **`drafts delete` しない**。delete すると送信済みメールごと完全削除される |

詳細なトラブルシューティングは `references/troubleshooting.md` を参照。

## Resources

このスキルには以下のリファレンスが含まれます:

| ファイル | 内容 |
|---------|------|
| `references/quick_reference.md` | 全サービスのコマンドチートシート |
| `references/communication_services.md` | Gmail/Calendar/Chat の詳細ガイド |
| `references/productivity_services.md` | Drive/Sheets/Docs/Slides/Tasks/Keep の詳細ガイド |
| `references/workspace_admin_services.md` | Groups/Admin/Classroom/People/Contacts + 新サービス群の詳細 |
| `references/troubleshooting.md` | トラブルシューティング詳細ガイド |

**公式リポジトリ:** https://github.com/openclaw/gogcli
