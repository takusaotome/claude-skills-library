# Communication Services -- Gmail / Calendar / Chat

このリファレンスは gogcli **v0.27.0** のコマンド体系に対応しています。v0.9 系からコマンドパスが大きく変わっているので、古い `gog gmail threads` や `gog calendar event create` などは使えません。

## Gmail

### Gmail Search Query Syntax

Gmail の検索系コマンドはすべて Gmail の検索構文をそのまま受け取ります。スレッド検索は `gog gmail search "<query>"`、メッセージ単位の検索は `gog gmail messages search "<query>"` で、いずれも**クエリが必須引数**です。クエリを省略した一覧表示はできません。

**基本検索演算子:**

| 演算子 | 説明 | 例 |
|-------|------|-----|
| `from:` | 送信者 | `from:boss@company.com` |
| `to:` | 受信者 | `to:team@company.com` |
| `cc:` | CC | `cc:manager@company.com` |
| `bcc:` | BCC | `bcc:archive@company.com` |
| `subject:` | 件名 | `subject:weekly report` |
| `label:` | ラベル | `label:important` |
| `has:attachment` | 添付ファイル付き | `has:attachment` |
| `filename:` | 添付ファイル名 | `filename:pdf` or `filename:report.xlsx` |
| `in:` | メールボックス | `in:inbox`, `in:sent`, `in:trash` |
| `is:` | 状態 | `is:unread`, `is:starred`, `is:important` |
| `after:` | 指定日以降 | `after:2025/01/01` |
| `before:` | 指定日以前 | `before:2025/01/31` |
| `newer_than:` | 相対日付 | `newer_than:7d`, `newer_than:1m` |
| `older_than:` | 相対日付 | `older_than:1y` |
| `size:` | サイズ | `size:5m`（5MB以上） |
| `larger:` / `smaller:` | サイズ比較 | `larger:10m` |

**スレッド検索（`gog gmail search`、エイリアス find/query/ls/list）:**

```bash
# 上司からの未読メール（直近1週間）
gog gmail search "from:boss@company.com is:unread newer_than:7d"

# PDF添付ファイル付きメール
gog gmail search "has:attachment filename:pdf"

# 特定の件名で受信トレイ内
gog gmail search "subject:\"monthly report\" in:inbox"

# 複数条件の OR 検索
gog gmail search "{from:alice@company.com from:bob@company.com}"

# 除外検索
gog gmail search "from:newsletter -label:important"

# 日付範囲
gog gmail search "after:2025/01/01 before:2025/01/31 has:attachment"

# 件数指定とJSON出力（--max のデフォルトは 10）
gog gmail search "is:unread" --max 50 --json

# 全ページ取得・結果ゼロでエラー終了させる
gog gmail search "label:invoices" --all --fail-empty
```

連絡先名から送信者を解決したいときは `--from-contact` が使えます。Google Contacts を引いて `from:(email OR email)` をクエリに追加します。

```bash
gog gmail search "is:unread" --from-contact "Alice Tanaka"
```

**メッセージ検索（`gog gmail messages search`、エイリアス find/query/ls/list）:**

スレッドではなく個々のメッセージを探す場合に使います。本文を含めたいときは `--include-body`、全文表示は `--full` です。

```bash
# メッセージ単位で検索（--max のデフォルトは 10）
gog gmail messages search "from:alice@company.com newer_than:30d"

# 本文（デコード済み）を含めて取得
gog gmail messages search "subject:invoice" --include-body --body-format text

# 全文を省略せず表示
gog gmail messages search "subject:invoice" --full
```

### Reading Messages and Threads

**メッセージ取得（`gog gmail get`、エイリアス info/show）:**

`gog gmail message <id>` は廃止され、`gog gmail get <id>` に統合されました。`--format` で full / metadata / raw を切り替えます。

```bash
# メッセージ全体（デフォルト full）
gog gmail get <message-id>

# メタデータのみ（指定ヘッダーだけ取得）
gog gmail get <message-id> --format metadata --headers "From,Subject,Date"

# JSON出力
gog gmail get <message-id> --json

# エージェント向けにサニタイズ（HTML除去・URL除去・生ペイロード省略）
gog gmail get <message-id> --sanitize-content --json
```

スクリプトや LLM 連携で API レスポンスをそのまま欲しいときは `gog gmail raw <message-id>` を使うとロスレスな JSON が得られます。

**スレッド取得（`gog gmail thread get`、エイリアス info/show）:**

スレッド内の全メッセージをまとめて読むには `thread get` を使います。`thread` のエイリアスは threads/read です。

```bash
# スレッド全体を表示
gog gmail thread get <thread-id>

# 本文を省略せず表示
gog gmail thread get <thread-id> --full

# 添付ファイルもダウンロード
gog gmail thread get <thread-id> --download --out-dir ./downloads/
```

**添付ファイル:**

```bash
# スレッド内の添付一覧、必要ならダウンロード
gog gmail thread attachments <thread-id>
gog gmail thread attachments <thread-id> --download --out-dir ./downloads/

# 単一の添付をダウンロード
gog gmail attachment <message-id> <attachment-id> --out ./downloads/report.pdf
```

### Sending Emails

**基本送信（`gog gmail send`）:**

```bash
# テキストメール
gog gmail send \
  --to recipient@example.com \
  --subject "Meeting Follow-up" \
  --body "Thanks for attending today's meeting."

# CC/BCC付き
gog gmail send \
  --to recipient@example.com \
  --cc manager@example.com \
  --bcc archive@example.com \
  --subject "Project Update" \
  --body "Please find the latest update below."
```

`--body`（プレーンテキスト）か `--body-html`（HTML）のどちらかが必須です。本文をファイルから渡すなら `--body-file` / `--body-html-file` を使い、`-` で標準入力を読めます。

**HTML メール:**

```bash
gog gmail send \
  --to recipient@example.com \
  --subject "Weekly Report" \
  --body-html "<h1>Weekly Report</h1><p>Key metrics this week:</p><ul><li>Revenue: \$10K</li></ul>"
```

**添付ファイル（`--attach` は繰り返し指定可）:**

```bash
gog gmail send \
  --to recipient@example.com \
  --subject "Documents" \
  --body "Attached are the requested documents." \
  --attach report.pdf \
  --attach data.xlsx \
  --attach summary.docx
```

**スレッド返信・署名:**

`--reply-to-message-id` を指定すると In-Reply-To / References が設定され、同じスレッドに返信できます。`--reply-all` は元メッセージから宛先を自動補完します。`--signature` でアクティブな send-as の Gmail 署名を末尾に付けられます。

```bash
gog gmail send \
  --reply-to-message-id <message-id> \
  --reply-all \
  --body "ご確認ありがとうございます。" \
  --signature
```

**返信専用コマンド（`reply` / `reply-all`）:**

元メッセージへの返信は専用サブコマンドのほうが簡単です。引用は既定で付き、`--no-quote` で外せます。`reply-all` は全参加者へ返信します。

```bash
# 単一送信者へ返信
gog gmail reply <message-id> --body "了解しました。"

# 全員へ返信し、宛先を追加
gog gmail reply-all <message-id> --body "共有ありがとうございます。" --cc extra@company.com
```

**転送（`gog gmail forward`）:**

```bash
gog gmail forward <message-id> \
  --to newrecipient@example.com \
  --note "参考までに転送します。"

# 添付を外して転送
gog gmail forward <message-id> --to newrecipient@example.com --skip-attachments
```

**自動返信（`gog gmail autoreply`）:**

クエリに一致したメッセージへ一度だけ返信し、重複防止用のラベルを付けます。既定の重複ラベルは `AutoReplied`、メールマガジン等の一括メールは既定でスキップします。

```bash
gog gmail autoreply "is:unread from:customer@example.com" \
  --body "お問い合わせありがとうございます。担当より追ってご連絡します。" \
  --mark-read
```

**開封トラッキング:**

Cloudflare Worker をバックエンドにした開封トラッキングが使えます。コマンド群は `gog gmail track ...` 配下です。

```bash
# 1. トラッキング設定（初回のみ。Worker をデプロイ）
gog gmail track setup --worker-url https://gog-email-tracker.example.workers.dev --deploy

# 2. トラッキング付き送信（HTML本文が必須）
gog gmail send \
  --to recipient@example.com \
  --subject "Proposal" \
  --body-html "<p>Please review the attached proposal.</p>" \
  --track

# 3. 開封の確認
gog gmail track opens --since 24h --to recipient@example.com

# 4. 設定状況の確認
gog gmail track status

# 5. 暗号鍵のローテーション
gog gmail track key rotate
```

**制約:**
- トラッキングには HTML 本文が必須（`--body-html`）。
- 受信者ごとに別送したいときは `--track-split` を併用する。

### Label Management

ラベル操作は `gog gmail labels ...` 配下に整理されました。一覧は `labels list`、作成は `labels create` です。

```bash
# ラベル一覧
gog gmail labels list

# ラベル作成
gog gmail labels create "Projects"
gog gmail labels create "Projects/Active"

# ラベルの詳細（件数を含む）
gog gmail labels get "Projects/Active"

# ラベル名の変更・色やスタイルの変更
gog gmail labels rename "Projects/Active" "Projects/Current"
gog gmail labels style "Projects/Current" --background-color "#16a765" --text-color "#ffffff"

# ラベル削除
gog gmail labels delete "Projects/Archived"
```

**ラベルの付与・除去:**

メッセージやスレッドへのラベル付け替えは `modify` 系で行います。対象の単位ごとにコマンドが分かれます。

```bash
# 単一メッセージのラベルを変更
gog gmail messages modify <message-id> --add "Projects/Current" --remove "INBOX"

# スレッド内の全メッセージのラベルを変更
gog gmail thread modify <thread-id> --add "IMPORTANT"

# 複数スレッドをまとめて変更（labels modify はスレッドID群を取る）
gog gmail labels modify <thread-id-1> <thread-id-2> --add "Reviewed"

# 複数メッセージをまとめて変更
gog gmail batch modify <message-id-1> <message-id-2> --add "Processed" --remove "UNREAD"
```

### Inbox State (archive / trash / read / unread)

メッセージの状態変更は専用サブコマンドで行えます。ID を直接渡すほか、`--query` で一致した全件にまとめて適用できます。

```bash
# 受信トレイから外す（アーカイブ）
gog gmail archive <message-id>
gog gmail archive --query "from:newsletter older_than:30d" --max 200

# スレッド全体をアーカイブ
gog gmail archive --thread <thread-id>

# ゴミ箱へ移動（通常の削除。デフォルトスコープで使える）
gog gmail trash <message-id>
gog gmail trash --query "from:spam@example.com"

# 既読・未読
gog gmail mark-read <message-id>
gog gmail mark-read --query "label:newsletters is:unread"
gog gmail unread <message-id>
```

> **完全削除に関する注意**: `gog gmail batch delete` はメッセージを**ゴミ箱を経由せず完全削除**します。これには `https://mail.google.com/` の広い OAuth スコープが必要です。通常の削除は `gog gmail trash`（30日間は復元可能）を使い、`batch delete` は本当に消したい場合だけにしてください。

### Drafts

下書き操作は `gog gmail drafts ...`（エイリアス draft）配下にまとまっています。サブコマンドは list / create / get / update / send / delete です。

```bash
# 下書き一覧
gog gmail drafts list

# 下書き作成
gog gmail drafts create \
  --to recipient@example.com \
  --subject "Draft Subject" \
  --body "Draft content..."

# 下書きの詳細表示
gog gmail drafts get <draft-id>

# 下書き更新（内容差し替え。--subject は必須）
gog gmail drafts update <draft-id> --subject "..." --body-file body.txt

# 下書き送信（推奨: 作成と同じ経路で送信し、孤立ドラフトを残さない）
gog gmail drafts send <draft-id>

# 下書き削除（破壊的。下記の警告を必読）
gog gmail drafts delete <draft-id>
```

> ⚠️ **データ消失の重大注意 — `drafts delete` が「送信済みメール」を完全削除することがある**
>
> **事象:** API/CLI で作成した下書きを Gmail の Web 画面から送信すると、下書きが自動消去されず「孤立（orphaned draft）」して残ることがある。この孤立ドラフトの `draft-id` を `drafts delete` すると、ポインタの先＝**送信済み本体メッセージごと完全削除**される。`drafts.delete` は「即時・完全削除（ゴミ箱に入れない）」仕様のため、**ゴミ箱からも復元できない**。スキーマ上も「not recoverable; drafts are not moved to Trash」と明記されている。
>
> **決定的な兆候:** `drafts update <draft-id>` が **`Message not a draft`（HTTP 400）** を返したら、その下書きは**すでに送信済み**を意味する（404 ではない点に注意）。`drafts list` に出てこないのに `drafts get <draft-id>` が返る場合も孤立ドラフトのサイン。
>
> **安全ルール:**
> 1. `Message not a draft` が出たら **その `draft-id` を絶対に `delete` しない**。まず送信済みか確認する。
> 2. 下書きの「作り直し」を **delete → create で行わない**。変更は `drafts update` を使う。
> 3. 送信後に残った孤立ドラフトの掃除は **Gmail Web 画面でゴミ箱へ**（30日間は復元可能）。API の `drafts delete` は使わない。
> 4. **作成と送信は同じ経路で完結**させる。CLI で作ったら `gog gmail drafts send` で送る。
> 5. 「送ったか」の真偽は**メールボックスの Sent ではなく、Google Admin の Email Log Search／受信者確認を真実**とする。削除で Sent コピー自体が消えると「未送信」に見え、**二重送信のリスク**が生じる。
>
> 詳細は `references/troubleshooting.md` の「Gmail: Draft Delete が送信済みメールを消す」を参照。

### Settings (filters / vacation / delegates / send-as / forwarding)

設定・管理系は `gog gmail settings ...` 配下に集約されました。

**フィルタ（`settings filters`）:**

```bash
# フィルタ一覧・詳細
gog gmail settings filters list
gog gmail settings filters get <filter-id>

# フィルタ作成（条件＋アクションをフラグで指定）
gog gmail settings filters create \
  --from "newsletter@example.com" \
  --add-label "Newsletters" \
  --archive

# Gmail WebUI 互換 XML としてエクスポート
gog gmail settings filters export --out filters.xml

# フィルタ削除
gog gmail settings filters delete <filter-id>
```

**不在応答 / バケーション（`settings vacation`）:**

```bash
# 現在の設定を確認
gog gmail settings vacation get

# 不在応答を有効化（--body は HTML 本文、期間は RFC3339）
gog gmail settings vacation update \
  --enable \
  --subject "Out of Office" \
  --body "<p>現在不在にしております。2月10日に戻ります。</p>" \
  --start "2025-02-03T00:00:00Z" \
  --end "2025-02-10T23:59:59Z"

# 連絡先のみ・同一ドメインのみに限定
gog gmail settings vacation update --enable --subject "OOO" --body "<p>...</p>" --contacts-only

# 不在応答を無効化
gog gmail settings vacation update --disable
```

**委任（`settings delegates`）:**

```bash
# 委任一覧・詳細
gog gmail settings delegates list
gog gmail settings delegates get assistant@company.com

# 委任の追加・削除（Workspace 管理者権限が必要）
gog gmail settings delegates add assistant@company.com
gog gmail settings delegates remove assistant@company.com
```

**送信エイリアス（`settings sendas`）:**

```bash
# send-as 一覧
gog gmail settings sendas list

# エイリアス追加（表示名・署名を設定。追加後は検証が必要）
gog gmail settings sendas create alias@company.com \
  --display-name "Sales Team" \
  --signature "<p>Sales Team / Company</p>"

# 検証メールの再送
gog gmail settings sendas verify alias@company.com

# 既定の送信元に設定
gog gmail settings sendas update alias@company.com --make-default
```

**転送（`settings forwarding` / `settings autoforward`）:**

転送先アドレスの登録と、自動転送の有効化は別コマンドです。自動転送は事前に検証済みの転送先が必要です。

```bash
# 転送先アドレスの登録・一覧
gog gmail settings forwarding create forward@company.com
gog gmail settings forwarding list

# 自動転送の有効化（転送後の扱いを --disposition で指定）
gog gmail settings autoforward update \
  --enable \
  --email forward@company.com \
  --disposition leaveInInbox

# 自動転送の状態確認・無効化
gog gmail settings autoforward get
gog gmail settings autoforward update --disable
```

### History & Watch (Pub/Sub)

履歴の取得は `gog gmail history`、Pub/Sub 連携は `gog gmail settings watch ...` 配下に移動しました。

```bash
# 履歴の取得（変更追跡。開始 history ID を指定）
gog gmail history --since <history-id>

# Pub/Sub Watch の開始（リアルタイム通知）
gog gmail settings watch start --topic "projects/my-project/topics/gmail-notifications"

# Watch の状態確認・更新・停止
gog gmail settings watch status
gog gmail settings watch renew --ttl 168h
gog gmail settings watch stop

# Push ハンドラ / Pull コンシューマを起動（Webhook へ転送）
gog gmail settings watch serve --hook-url https://example.com/hook --port 8788
gog gmail settings watch pull --subscription "projects/.../subscriptions/gmail-sub" --hook-url https://example.com/hook
```

### Web URL

スレッドの Gmail Web URL を出力するには `gog gmail url <thread-id>` を使います。複数 ID を渡せます。

```bash
gog gmail url <thread-id-1> <thread-id-2>
```

---

## Calendar

v0.27.0 ではイベント操作のコマンドパスが変わっています。作成は `gog calendar create`、更新は `gog calendar update`、削除は `gog calendar delete`、単一取得は `gog calendar event`、一覧は `gog calendar events`、カレンダー一覧は `gog calendar calendars` です。多くのコマンドが**最初の位置引数に `<calendarId>` を取る**点に注意してください（`primary` を指定すると自分のメインカレンダー）。

### Event Listing

**イベント一覧（`gog calendar events`、エイリアス list/ls）:**

```bash
# 今日のイベント
gog calendar events --today

# 明日のイベント
gog calendar events --tomorrow

# 今週
gog calendar events --week

# 期間指定（RFC3339・日付・相対指定が使える）
gog calendar events --from 2025-02-01 --to 2025-02-28

# 今後N日間
gog calendar events --days 7

# 特定カレンダーのイベント（位置引数または --cal）
gog calendar events primary --today
gog calendar events --cal "team@company.com" --week

# 全カレンダー横断（--all、開始時刻順に並べる）
gog calendar events --all --week --sort start
```

**JSON出力と曜日列の活用:**

```bash
# 曜日列を付けて表示
gog calendar events --today --weekday

# JSON出力からタイトルを抽出
gog calendar events --today --json | jq '.[].summary'

# 出席者情報を含む
gog calendar events --today --json | jq '.[] | {summary, start, attendees}'
```

**検索（`gog calendar search`、エイリアス find/query）:**

```bash
# フリーテキストでイベントを検索
gog calendar search "kickoff" --week
gog calendar search "1on1" --calendar primary --days 30
```

### Event Creation

イベント作成は `gog calendar create`（エイリアス add/new）です。第1引数に対象カレンダー ID を渡し、開始・終了は `--from` / `--to`、タイトルは `--summary` で指定します。

**基本イベント:**

```bash
# 時間指定イベント（RFC3339）
gog calendar create primary \
  --summary "Team Meeting" \
  --from "2025-02-01T10:00:00" \
  --to "2025-02-01T11:00:00"

# 終日イベント（--all-day を付け、日付のみ指定）
gog calendar create primary \
  --summary "Company Holiday" \
  --all-day \
  --from "2025-02-11" \
  --to "2025-02-11"

# 場所・説明付き
gog calendar create primary \
  --summary "Quarterly Review" \
  --from "2025-02-01T14:00:00" \
  --to "2025-02-01T16:00:00" \
  --location "Conference Room A" \
  --description "Q4 performance review and Q1 planning."
```

**出席者・通知:**

`--send-updates` で出席者への通知方法を制御します（all / externalOnly / none、既定 none）。

```bash
gog calendar create primary \
  --summary "Project Kickoff" \
  --from "2025-02-03T09:00:00" \
  --to "2025-02-03T10:00:00" \
  --attendees "alice@company.com,bob@company.com,carol@company.com" \
  --send-updates all
```

**ビデオ会議の付与:**

```bash
# Google Meet を生成
gog calendar create primary \
  --summary "Sync" \
  --from "2025-02-03T09:00:00" \
  --to "2025-02-03T09:30:00" \
  --with-meet

# Zoom を生成
gog calendar create primary --summary "Sync" \
  --from "2025-02-03T09:00:00" --to "2025-02-03T09:30:00" --with-zoom
```

**繰り返しイベント（`--rrule`、繰り返し指定可）:**

v0.9 の `--recurrence` は `--rrule` に変わりました。複数の RRULE を渡せます。

```bash
# 毎週月曜
gog calendar create primary \
  --summary "Weekly Standup" \
  --from "2025-02-03T09:00:00" \
  --to "2025-02-03T09:30:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO"

# 平日毎日（10回で終了）
gog calendar create primary \
  --summary "Daily Check-in" \
  --from "2025-02-03T08:30:00" \
  --to "2025-02-03T08:45:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=10"

# 隔週金曜（2025年6月まで）
gog calendar create primary \
  --summary "Bi-weekly Sprint Review" \
  --from "2025-02-07T16:00:00" \
  --to "2025-02-07T17:00:00" \
  --rrule "RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=FR;UNTIL=20250630T000000Z"
```

**RRULE 頻出パターン:**

| パターン | RRULE |
|---------|-------|
| 毎日 | `FREQ=DAILY` |
| 平日毎日 | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR` |
| 毎週月曜 | `FREQ=WEEKLY;BYDAY=MO` |
| 隔週 | `FREQ=WEEKLY;INTERVAL=2` |
| 毎月1日 | `FREQ=MONTHLY;BYMONTHDAY=1` |
| 毎月第3水曜 | `FREQ=MONTHLY;BYDAY=3WE` |
| 毎年 | `FREQ=YEARLY` |
| N回で終了 | 末尾に `;COUNT=N` |
| 特定日まで | 末尾に `;UNTIL=YYYYMMDDTHHmmssZ` |

### Special Event Types

v0.27.0 では旧 `--event-type` の各種が専用サブコマンド化されました。`gog calendar create` 側にも `--event-type` は残っていますが、フォーカスタイム・不在・勤務場所は専用コマンドのほうが必要なフラグが揃っていて簡単です。

**フォーカスタイム（`gog calendar focus-time`、エイリアス focus）:**

```bash
gog calendar focus-time primary \
  --summary "Deep Work" \
  --from "2025-02-03T09:00:00" \
  --to "2025-02-03T12:00:00" \
  --auto-decline all \
  --chat-status doNotDisturb
```

**不在（`gog calendar out-of-office`、エイリアス ooo）:**

不在イベントは終日指定が API 側で拒否されるため、`--from` / `--to` は日時（RFC3339）で渡します。

```bash
gog calendar out-of-office primary \
  --summary "Vacation" \
  --from "2025-02-10T00:00:00" \
  --to "2025-02-14T23:59:59" \
  --decline-message "外出中のため、戻り次第ご返信します。"
```

**勤務場所（`gog calendar working-location`、エイリアス wl）:**

`--type` は home / office / custom が必須、`--from` / `--to` は日付（YYYY-MM-DD）です。

```bash
gog calendar working-location primary \
  --type home \
  --from 2025-02-03 \
  --to 2025-02-03
```

### Event Get / Update / Delete

**単一取得（`gog calendar event`、エイリアス get/info/show）:**

```bash
gog calendar event primary <event-id>

# 生の API レスポンスが欲しい場合
gog calendar raw primary <event-id> --pretty
```

**更新（`gog calendar update`、エイリアス edit/set）:**

第1引数にカレンダー ID、第2引数にイベント ID を渡します。出席者は `--attendees` で総入れ替え、`--add-attendee` で既存を保ったまま追加できます。繰り返しイベントは `--scope`（single / future / all）で影響範囲を指定します。

```bash
# タイトル変更
gog calendar update primary <event-id> --summary "Updated Title"

# 時間変更
gog calendar update primary <event-id> --from "2025-02-01T11:00:00" --to "2025-02-01T12:00:00"

# 出席者を保ったまま追加し、通知を送る
gog calendar update primary <event-id> --add-attendee "newguest@company.com" --send-updates all

# 繰り返しイベントのこの回だけ変更
gog calendar update primary <event-id> --scope single --original-start "2025-02-03T09:00:00" --summary "Special session"
```

**削除（`gog calendar delete`、エイリアス rm/del/remove）:**

```bash
# 単一イベント削除
gog calendar delete primary <event-id>

# 繰り返しイベントのこの回以降を削除
gog calendar delete primary <event-id> --scope future --original-start "2025-02-10T09:00:00"

# 削除を出席者へ通知
gog calendar delete primary <event-id> --send-updates all
```

**別カレンダーへ移動（`gog calendar move`、エイリアス transfer）:**

```bash
gog calendar move primary <event-id> team@company.com
```

### RSVP & Propose Time

**招待への応答（`gog calendar respond`、エイリアス rsvp/reply）:**

```bash
gog calendar respond primary <event-id> --status accepted
gog calendar respond primary <event-id> --status tentative --comment "前半のみ参加します。"
gog calendar respond primary <event-id> --status declined
```

**別時間の提案（`gog calendar propose-time`）:**

これはブラウザ専用機能のため、提案用 URL を生成します。`--decline` を付けると主催者に通知しつつ辞退できます。

```bash
gog calendar propose-time primary <event-id> --open
gog calendar propose-time primary <event-id> --decline --comment "この時間は難しいため別時間を提案します。"
```

### Conflict Detection

```bash
# 今週の競合を検出
gog calendar conflicts --week

# 期間指定で複数カレンダーを横断
gog calendar conflicts --from 2025-02-03 --to 2025-02-07 --all --json
```

### Free/Busy Queries

空き時間照会は `gog calendar freebusy` です。対象は位置引数か `--cal` で指定します。`--from` / `--to` が必須です。

```bash
# 複数メンバーの空き時間
gog calendar freebusy \
  --cal "alice@company.com" --cal "bob@company.com" --cal "carol@company.com" \
  --from "2025-02-03T09:00:00" \
  --to "2025-02-03T18:00:00"

# 全カレンダー横断
gog calendar freebusy --all --from 2025-02-03T00:00:00 --to 2025-02-07T23:59:59 --json
```

Workspace グループ全員の予定をまとめて見るには `gog calendar team <group-email>` が便利です。`--freebusy` を付けると busy/free ブロックのみを高速取得します。

```bash
gog calendar team engineers@company.com --week --freebusy
```

### Calendar Management

```bash
# カレンダー一覧（list ではなく calendars）
gog calendar calendars

# カレンダーIDの確認（JSONで取得）
gog calendar calendars --json | jq '.[] | {summary, id}'

# 副カレンダーの作成・削除
gog calendar create-calendar "Project X" --timezone "Asia/Tokyo"
gog calendar delete-calendar <calendar-id>

# 他人/共有カレンダーをカレンダーリストに追加・削除
gog calendar subscribe <calendar-id> --color-id 5
gog calendar unsubscribe <calendar-id>

# ACL（共有権限）一覧と利用可能な色
gog calendar acl <calendar-id>
gog calendar colors
```

長いカレンダー ID を覚えたくない場合はエイリアスを設定できます。

```bash
gog calendar alias set team team@company.com
gog calendar alias list
gog calendar events team --week   # エイリアスをそのまま使える
```

### Timezone Handling

```bash
# デフォルトタイムゾーン設定
gog config set default_timezone "Asia/Tokyo"

# 環境変数で一時的に変更
GOG_TIMEZONE=UTC gog calendar events --today
GOG_TIMEZONE="America/New_York" gog calendar events --today

# サーバ時刻と現在のタイムゾーンを確認
gog calendar time --timezone "America/New_York"

# イベント作成時のタイムゾーン指定（ISO 8601 のオフセット、または --start-timezone / --end-timezone）
gog calendar create primary \
  --summary "Cross-timezone Meeting" \
  --from "2025-02-03T10:00:00-05:00" \
  --to "2025-02-03T11:00:00-05:00"

gog calendar create primary \
  --summary "Rome Sync" \
  --from "2025-02-03T10:00:00" --to "2025-02-03T11:00:00" \
  --start-timezone "Europe/Rome" --end-timezone "Europe/Rome"
```

---

## Chat [Workspace Only]

> Chat サービスは Google Workspace アカウントでのみ利用可能です。
> 個人の Gmail アカウントでは使用できません。

v0.27.0 では Chat のコマンドが grouped 化され、`gog chat spaces` 等は単独では動かず、配下のサブコマンドを指定します。

### Space Management

```bash
# スペース一覧（spaces 単独ではなく spaces list）
gog chat spaces list

# 全ページ取得・結果ゼロでエラー終了
gog chat spaces list --all --fail-empty

# 表示名でスペースを検索（部分一致。--exact で完全一致）
gog chat spaces find "Engineering"
gog chat spaces find "Engineering Team" --exact

# スペースを作成し、メンバーを追加
gog chat spaces create "Project X" --member alice@company.com --member bob@company.com
```

### Messages

メッセージ一覧は `gog chat messages list`、送信は `gog chat messages send` です。いずれもスペース名を位置引数に取ります。

```bash
# スペース内のメッセージ一覧
gog chat messages list <space>

# 未読のみ・スレッドで絞り込み
gog chat messages list <space> --unread
gog chat messages list <space> --thread "spaces/.../threads/..."

# メッセージ送信
gog chat messages send <space> --text "Hello team!"

# スレッド内返信
gog chat messages send <space> --text "Reply to thread" --thread "spaces/.../threads/..."

# 画像など添付付き送信（--text は省略可、--attach は繰り返し可）
gog chat messages send <space> --attach ./diagram.png --text "構成図です"
```

### Reactions

絵文字リアクションは `gog chat messages react`（簡易）と `gog chat messages reactions ...`（add/list/delete）で扱います。メッセージをベア ID で渡すときは `--space` が必要です。

```bash
# リアクションを追加
gog chat messages react <message> "👍" --space <space>

# リアクション一覧
gog chat messages reactions list <message> --space <space>

# リアクション削除
gog chat messages reactions delete <reaction>
```

### Threads

```bash
# スペース内のスレッド一覧
gog chat threads list <space> --max 50
```

### Direct Messages

DM は `gog chat dm` 配下です。送信は `dm send`、DM スペースの検索・作成は `dm space` です。

```bash
# DM送信（相手のメールアドレスを指定）
gog chat dm send colleague@company.com --text "Quick question about the project"

# スレッドへの返信
gog chat dm send colleague@company.com --text "追記です" --thread "spaces/.../threads/..."

# DM スペースを検索または作成（space-id を取得したいとき）
gog chat dm space colleague@company.com
```

### Limitations

- Chat API は Google Workspace アカウントが必要。個人 Gmail では使用不可。
- Bot/App としてのメッセージ送信はサービスアカウント経由。
- メッセージ送信時の添付は `--attach` で可能（画像など）。一覧・スレッド操作はスペース名やスレッド名（`spaces/.../threads/...`）を引数に取る。
