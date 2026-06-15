# gogcli Quick Reference (v0.27.0)

25以上のサービスをカバーするコマンドチートシート。各サービスは「よく使うコマンド」を中心に整理しています。網羅的な一覧は `gog <service> --help` または `gog schema` を参照してください。

多くのコマンドにはエイリアスがあります。例として `gog drive ls` は `gog drv ls`、`gog gmail` は `gog mail` でも実行できます。`list` 系は `ls`、`get` 系は `info`/`show` でも代用できます。

## Authentication & Setup

認証は次の順序で進めます。

```bash
# 1. OAuth クライアントのクレデンシャル JSON を登録（最初に一度だけ）
gog auth credentials set ./credentials.json

#    名前付きクライアント・ドメイン割り当て
gog auth credentials set ./work.json --domain example.com
gog auth credentials list

# 2. アカウントを認証（ブラウザが起動）。login は auth add のエイリアス
gog auth add user@gmail.com
gog login user@gmail.com

#    特定サービスのみ／読み取り専用で認証
gog auth add user@gmail.com --services gmail,calendar,drive
gog auth add user@gmail.com --readonly
gog auth add user@gmail.com --drive-scope full      # full|readonly|file
gog auth add user@gmail.com --force-consent         # 再同意を強制（スコープ追加時）

# 3. サービスアカウント（Workspace のドメイン全体委任）
gog auth service-account set admin@example.com --key ./sa.json
gog auth service-account status admin@example.com
gog auth keep admin@example.com --key ./sa.json     # Keep 専用 SA 設定

# 4. 状態確認・診断
gog status                 # auth status のエイリアス
gog auth status
gog auth list              # 認証済みアカウント一覧
gog auth list --check      # リフレッシュトークンを実際に検証
gog auth doctor            # 認証・キーリング・トークンを診断
gog auth doctor --check    # トークンをアクセストークンに交換して検証
gog auth services          # 対応サービスとスコープの一覧
gog whoami                 # 現在のプロフィール（people me のエイリアス）
```

その他の認証管理コマンド。

| コマンド | 説明 |
|---------|------|
| `gog auth remove <email>` / `gog logout <email>` | アカウント削除 |
| `gog auth alias set <alias> <email>` | アカウントのエイリアス設定 |
| `gog auth alias list` / `gog auth alias unset <alias>` | エイリアス一覧／削除 |
| `gog auth keyring [<backend>]` | キーリングバックエンド確認・設定 |
| `gog auth import --email <e> --refresh-token-stdin` | リフレッシュトークンを非対話インポート |
| `gog auth tokens list` / `export` / `import` / `delete` | トークンの一覧・退避・取り込み |
| `gog auth manage` | ブラウザでアカウント管理 UI を開く（login の旧名） |

## Global Flags

全コマンド共通のグローバルフラグ。

| フラグ | 短縮 | 説明 |
|-------|------|------|
| `--account <email\|alias\|auto>` | `-a` | 使用するアカウント |
| `--json` | `-j` | JSON 出力（スクリプト向け） |
| `--plain` | `-p` | 安定した TSV 出力（色なし） |
| `--dry-run` | `-n` | 変更せず意図したアクションのみ表示 |
| `--force` | `-y` | 破壊的操作の確認をスキップ |
| `--verbose` | `-v` | 詳細ログ |
| `--no-input` | | プロンプトを出さず失敗させる（CI 向け） |
| `--gmail-no-send` | | Gmail 送信操作をブロック（エージェント安全策） |
| `--enable-commands <csv>` | | 許可するコマンドプレフィックスに限定 |
| `--disable-commands <csv>` | | 指定コマンドを無効化 |
| `--select <fields>` | | JSON モードで指定フィールドのみ抽出 |
| `--results-only` | | JSON モードで主結果のみ出力（nextPageToken 等を除く） |
| `--wrap-untrusted` | | 取得テキストを untrusted マーカーで囲む |
| `--access-token <token>` | | アクセストークンを直接利用（約1時間有効） |
| `--client <name>` | | OAuth クライアントを選択 |
| `--home <path>` | | gogcli の設定・データルートを上書き（GOG_HOME 相当） |
| `--color <mode>` | | カラー制御（auto/always/never） |

## Top-Level Aliases

頻出操作にはトップレベルの別名があります。

| 別名 | 実体 |
|------|------|
| `gog ls` / `gog list` | `gog drive ls` |
| `gog search <q>` | `gog drive search` |
| `gog download <id>` / `gog dl` | `gog drive download` |
| `gog upload <path>` / `gog up` | `gog drive upload` |
| `gog send` | `gog gmail send` |
| `gog open <target>` | Google URL/ID の Web URL をオフラインで生成 |
| `gog me` / `gog whoami` | `gog people me` |
| `gog login` / `gog logout` | `gog auth add` / `gog auth remove` |
| `gog status` / `gog st` | `gog auth status` |

## Gmail

```bash
# 検索・閲覧
gog gmail search "from:boss is:unread"          # スレッド検索（Gmail 検索構文）
gog gmail messages search "subject:invoice"      # メッセージ単位の検索
gog gmail thread get <threadId> --full           # スレッド全文
gog gmail get <messageId> --format full          # メッセージ取得（full|metadata|raw）

# 送信・返信・転送
gog gmail send --to a@x.com --subject "Hi" --body "text"
gog gmail send --to a@x.com --subject "Hi" --body-html "<p>hi</p>" --track
gog gmail send --to a@x.com --subject "Hi" --body "t" --attach file.pdf
gog gmail reply <messageId> --body "thanks"
gog gmail reply-all <messageId> --body "thanks"
gog gmail forward <messageId> --to c@x.com --note "FYI"

# 下書き（draft のデータ消失に注意。troubleshooting.md 参照）
gog gmail drafts create --to a@x.com --subject "Draft" --body "text"
gog gmail drafts list
gog gmail drafts update <draftId> --body "edited"
gog gmail drafts send <draftId>

# 整理
gog gmail labels list
gog gmail labels create "Project"
gog gmail messages modify <messageId> --add "Project" --remove "INBOX"
gog gmail thread modify <threadId> --add "Project"
gog gmail trash <messageId>                       # ゴミ箱へ（復元可）
gog gmail archive <messageId>
gog gmail mark-read <messageId> / gog gmail unread <messageId>

# 設定
gog gmail settings vacation update --enable --subject "OOO" --body "<p>away</p>"
gog gmail settings vacation update --disable
gog gmail settings filters list
gog gmail settings delegates list
gog gmail settings sendas list
gog gmail track setup --worker-url <url>          # 開封トラッキング
gog gmail track opens
```

`gog gmail batch delete` は完全削除で `https://mail.google.com/` スコープが必要です。通常は `gog gmail trash` を使ってください。

## Calendar

```bash
gog calendar events --today                       # 今日のイベント
gog calendar events --week
gog calendar events --from 2026-06-01 --to 2026-06-30
gog calendar events --days 7                      # 今後7日
gog calendar events --all                         # 全カレンダーから取得
gog calendar calendars                            # カレンダー一覧
gog calendar event <calendarId> <eventId>         # イベント取得

# 作成・更新・削除（第1引数は calendarId。primary が既定の対象）
gog calendar create primary --summary "MTG" --from "2026-06-20T10:00:00+09:00" --to "2026-06-20T11:00:00+09:00"
gog calendar create primary --summary "MTG" --from ... --to ... --attendees "a@x.com,b@x.com"
gog calendar create primary --summary "Sync" --from ... --to ... --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO" --with-meet
gog calendar update primary <eventId> --summary "Renamed"
gog calendar update primary <eventId> --add-attendee "c@x.com"
gog calendar delete primary <eventId>

# 空き時間・競合・特殊イベント
gog calendar freebusy --cal primary --from <rfc3339> --to <rfc3339>
gog calendar conflicts --today
gog calendar focus-time --from ... --to ...        # フォーカスタイム
gog calendar out-of-office --from ... --to ...     # OOO
gog calendar search "standup" --week
gog calendar respond primary <eventId> --status accepted
```

## Drive

```bash
gog drive ls                                       # ルート一覧（gog ls でも可）
gog drive ls --parent <folderId>
gog drive ls --query "name contains 'report'"
gog drive search "quarterly report"                # 全文検索（gog search でも可）
gog drive get <fileId>                             # メタデータ
gog drive tree --parent <folderId>                 # フォルダツリー
gog drive du --parent <folderId>                   # 容量サマリ

# ダウンロード・アップロード・エクスポート
gog drive download <fileId> --out ./dir            # 通常ファイル／Google ファイルは自動エクスポート
gog drive download <fileId> --format pdf           # pdf|csv|xlsx|pptx|txt|png|docx|md
gog drive upload ./report.pdf --parent <folderId>
gog drive upload ./notes.md --convert-to doc       # ネイティブ Google 形式に変換

# 整理・共有
gog drive mkdir "New Folder" --parent <folderId>
gog drive move <fileId> --parent <folderId>
gog drive rename <fileId> "New Name"
gog drive copy <fileId> "Copy Name"
gog drive delete <fileId>                           # ゴミ箱へ（--permanent で完全削除）
gog drive permissions <fileId>
gog drive share <fileId> --to user --email a@x.com --role writer
gog drive unshare <fileId> <permissionId>
gog drive drives                                    # 共有ドライブ一覧

# 監査
gog drive audit sharing --public-only               # 公開・外部共有を検出
gog drive audit user a@x.com                        # 特定ユーザーへの共有を検出
```

## Sheets

```bash
gog sheets get <id> "Sheet1!A1:D10"                # 範囲を読み取り（A1 記法）
gog sheets update <id> "Sheet1!A1" "v1" "v2"        # セル更新
gog sheets update <id> "Sheet1!A1:B2" --values-json '[["a","b"],["c","d"]]'
gog sheets append <id> "Sheet1!A1" "x" "y"          # 行追加
gog sheets clear <id> "Sheet1!A1:D10"
gog sheets create "New Spreadsheet"                 # 新規作成
gog sheets metadata <id>                            # シート・タブ情報
gog sheets add-tab <id> "Q3"                        # タブ追加
gog sheets export <id> --format xlsx                # pdf|xlsx|csv
gog sheets format <id> "A1:D1" --format-json '{"textFormat":{"bold":true}}'
gog sheets find-replace <id> "old" "new"
```

`--input` は既定 `USER_ENTERED`（数式・日付を解釈）。リテラル文字列として書くなら `--input RAW` を指定します。

## Docs

```bash
gog docs create "Title" --file ./content.md         # Markdown から作成
gog docs cat <docId>                                # プレーンテキストで読む
gog docs write <docId> --file ./body.md --markdown --replace
gog docs insert <docId> "appended text"             # 末尾に挿入
gog docs find-replace <docId> "old" "new"
gog docs format <docId> --match "Heading" --heading-level 1
gog docs export <docId> --format pdf                # pdf|docx|txt|md|html
gog docs comments list <docId>
gog docs headings list <docId>
gog docs list-tabs <docId>
```

## Slides

```bash
gog slides create "Deck Title"
gog slides create-from-markdown "Deck" --content-file ./slides.md
gog slides list-slides <presentationId>             # スライドの objectId 一覧
gog slides read-slide <presentationId> <slideId>
gog slides replace-text <presentationId> "{{name}}" "Acme"
gog slides add-slide <presentationId> ./image.png --notes "speaker notes"
gog slides export <presentationId> --format pptx    # pdf|pptx
gog slides thumbnail <presentationId> <slideId> --out thumb.png
```

## Tasks

```bash
gog tasks lists list                                # タスクリスト一覧
gog tasks list <tasklistId>                         # タスク一覧
gog tasks add <tasklistId> --title "Buy milk" --due 2026-06-20
gog tasks update <tasklistId> <taskId> --title "Updated"
gog tasks done <tasklistId> <taskId>                # 完了
gog tasks undo <tasklistId> <taskId>                # 未完了に戻す
gog tasks delete <tasklistId> <taskId>
gog tasks clear <tasklistId>                        # 完了済みを一括クリア
```

## Keep [Workspace + Service Account]

Keep はサービスアカウントとインパーソネーションが前提です。

```bash
gog keep list --service-account ./sa.json --impersonate user@example.com
gog keep create --title "Note" --text "body" --service-account ./sa.json --impersonate user@example.com
gog keep search "meeting" --service-account ./sa.json --impersonate user@example.com
gog keep get <noteId> --service-account ./sa.json --impersonate user@example.com
```

`gog auth keep <email> --key ./sa.json` で SA を保存しておけば、毎回のフラグ指定を省けます。

## Contacts & People

```bash
gog people me                                       # 自分のプロフィール（gog me でも可）
gog people search "Yamada"                           # Workspace ディレクトリ検索
gog contacts list
gog contacts search "Yamada"
gog contacts create --given "Taro" --family "Yamada" --email t@x.com
gog contacts other list                              # やり取り履歴からの「その他の連絡先」
gog contacts directory search "sales"                # ディレクトリ
gog contacts export --all -o contacts.vcf            # vCard 出力
gog contacts dedupe                                  # 重複候補の検出（プレビュー）
```

## Chat [Workspace]

```bash
gog chat spaces list
gog chat spaces find "Project X"
gog chat messages list <space>
gog chat messages send <space> --text "Hello"
gog chat dm send a@x.com --text "DM"                 # DM 送信
gog chat threads list <space>
```

## Groups & Admin [Workspace]

```bash
# Cloud Identity Groups（自分の所属）
gog groups list
gog groups members <groupEmail>

# Directory API（ドメイン全体委任が必要）
gog admin users list --domain example.com
gog admin users get user@example.com
gog admin users create new@example.com --given Taro --family Yamada
gog admin users suspend user@example.com
gog admin groups list --domain example.com
gog admin groups members list <groupEmail>
gog admin groups members add <groupEmail> <memberEmail> --role MEMBER
gog admin orgunits list
```

## Classroom

```bash
gog classroom courses list
gog classroom courses get <courseId>
gog classroom roster <courseId> --students --teachers   # 名簿
gog classroom coursework list <courseId>
gog classroom submissions list <courseId> <courseworkId>
gog classroom announcements list <courseId>
gog classroom topics list <courseId>
```

## Forms

```bash
gog forms create --title "Survey"
gog forms get <formId>
gog forms add-question <formId> --title "Your name?" --type text --required
gog forms add-question <formId> --title "Pick one" --type radio -o "A" -o "B"
gog forms responses list <formId>
gog forms publish <formId>
```

## Meet

```bash
gog meet create                                      # 会議スペース作成
gog meet create --access open --open
gog meet get <meeting-code>
gog meet participants <meeting-code>                 # 直近の通話の参加者
gog meet history <meeting-code>                      # 過去の通話
```

## Maps

```bash
gog maps geocode "1600 Amphitheatre Pkwy, CA"
gog maps reverse-geocode --lat 37.42 --lng -122.08
gog maps directions --origin "Tokyo" --destination "Osaka" --mode driving
gog maps distance --origins "Tokyo" --destinations "Osaka,Kyoto"
gog maps places search "ramen near Shibuya"
gog maps places details <placeId>
```

## YouTube

```bash
gog youtube search list "golang tutorial" --max 10
gog youtube videos list --id <videoId>
gog youtube channels list --mine -a me@gmail.com
gog youtube playlists list --mine -a me@gmail.com
gog youtube playlists items list --playlist-id <id>
gog youtube subscriptions list -a me@gmail.com
gog youtube comments list --video-id <videoId>
```

## Photos

```bash
gog photos list                                      # アプリ作成のメディア一覧
gog photos search --media-type PHOTO --from 2026-01-01 --to 2026-06-01
gog photos download <mediaItemId> --out ./dir
gog photos picker create --open                      # ユーザー選択フロー（Picker API）
gog photos picker list <sessionId>
```

## Sites

```bash
gog sites list                                       # Drive 上の Google Sites
gog sites search "intranet"
gog sites get <siteId>
gog sites url <siteId>                               # エディタ URL を表示
```

## Analytics & Search Console

```bash
# Google Analytics (GA4)
gog analytics accounts                               # アカウントサマリ
gog analytics report <propertyId> --metrics activeUsers,sessions --dimensions date,country --from 7daysAgo --to today

# Search Console
gog searchconsole sites list
gog searchconsole query <siteUrl> --dimensions QUERY --from 2026-06-01 --to 2026-06-07
gog searchconsole sitemaps list <siteUrl>
```

## Apps Script

```bash
gog appscript create --title "My Script"
gog appscript get <scriptId>
gog appscript content <scriptId>                     # プロジェクトのソースを取得
gog appscript run <scriptId> <function> --params '["arg1"]'
```

## Zoom

Zoom は Server-to-Server OAuth で別管理します。Calendar の `--with-zoom` と連携します。

```bash
gog zoom auth setup --account-id <id> --client-id <id> --client-secret <secret>
gog zoom auth doctor                                 # 資格情報を検証
```

## Backup

age 暗号化＋Git で Google アカウントをバックアップします。

```bash
gog backup init --remote <git-url> --recipient <age-public-key>
gog backup push --services gmail,drive               # 暗号化シャードへ書き出し
gog backup status                                     # マニフェスト確認
gog backup verify                                     # 復号して検証
gog backup export --out ./export                      # 平文エクスポート
```

## Batch

Google Docs のリクエストをまとめて投げる永続バッチです。

```bash
gog batch begin --doc <docId> --name "edits"          # batchId を返す
gog docs insert <docId> "text" --batch <batchId>      # 各 docs コマンドの --batch に追加
gog batch show <batchId>
gog batch end <batchId>                               # 送信して削除
gog batch list / gog batch abort <batchId>
```

## MCP Server

gogcli を MCP サーバーとして起動できます。既定では読み取り専用ツールのみ公開します。

```bash
gog mcp                                                # 読み取り専用ツールを stdio で公開
gog mcp --allow-tool 'gmail.*,docs_get' --allow-write  # 書き込みツールも明示的に許可
gog mcp --list-tools                                   # 有効なツールを JSON 表示
```

## Config

```bash
gog config path                                       # 設定ファイルの場所
gog config list                                       # 全設定
gog config get <key> / gog config set <key> <value>
gog config unset <key>
gog config no-send set <account>                      # アカウント単位で Gmail 送信を恒久ブロック
gog time now --timezone Asia/Tokyo                    # 現在時刻
```

## Environment Variables

| 変数 | 説明 | 例 |
|-----|------|-----|
| `GOG_ACCOUNT` | デフォルトアカウント | `work@company.com` or `work` |
| `GOG_CLIENT` | デフォルト OAuth クライアント | `work` |
| `GOG_HOME` | 設定・データルートの上書き | `~/.config/gogcli` |
| `GOG_JSON` | デフォルト JSON 出力 | `1` or `true` |
| `GOG_PLAIN` | デフォルト TSV 出力 | `1` or `true` |
| `GOG_COLOR` | カラーモード | `auto`, `always`, `never` |
| `GOG_TIMEZONE` | タイムゾーン | `Asia/Tokyo`, `UTC`, `local` |
| `GOG_ENABLE_COMMANDS` | コマンド許可リスト | `gmail,calendar,tasks` |
| `GOG_KEYRING_BACKEND` | キーリングバックエンド | `auto`, `keychain`, `file` |
| `GOG_KEYRING_PASSWORD` | 暗号化キーリングパスワード | (セキュアに管理) |

## Help & Schema

```bash
gog --help                                            # トップレベル
gog gmail --help                                      # サービス別
gog gmail send --help                                 # サブコマンド別
gog schema                                            # 機械可読のコマンド・フラグスキーマ（JSON）
gog schema gmail send                                 # 特定コマンドのスキーマ
gog version
```

## Common MIME / Export Formats

`gog drive download --format` や各サービスの `export --format`（sheets/docs/slides）で使う主な形式。

| 形式 | 用途 |
|-----|------|
| `pdf` | Docs/Sheets/Slides 共通 |
| `docx` | Docs |
| `xlsx` / `csv` | Sheets |
| `pptx` | Slides |
| `txt` / `md` / `html` | Docs |
| `png` | Slides・Docs 内画像 |
