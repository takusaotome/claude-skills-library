# Communication Services -- Gmail / Calendar / Chat

## Gmail

### Gmail Search Query Syntax

gogcli の `--query` フラグは Gmail の検索構文をそのまま使用できます。

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

**複合検索例:**

```bash
# 上司からの未読メール（直近1週間）
gog gmail threads --query "from:boss@company.com is:unread newer_than:7d"

# PDF添付ファイル付きメール
gog gmail threads --query "has:attachment filename:pdf"

# 特定の件名で受信トレイ内
gog gmail threads --query "subject:\"monthly report\" in:inbox"

# 複数条件の OR 検索
gog gmail threads --query "{from:alice@company.com from:bob@company.com}"

# 除外検索
gog gmail threads --query "from:newsletter -label:important"

# 日付範囲
gog gmail threads --query "after:2025/01/01 before:2025/01/31 has:attachment"
```

### Thread and Message Operations

**スレッド操作:**

```bash
# スレッド一覧（デフォルト: 最新20件）
gog gmail threads

# 件数指定
gog gmail threads --max 50

# JSON出力で詳細情報取得
gog gmail threads --query "is:unread" --json

# スレッド内のメッセージ一覧
gog gmail messages --thread-id <thread-id>
```

**メッセージ操作:**

```bash
# メッセージ詳細表示
gog gmail message <message-id>

# JSON出力（ヘッダー、本文、添付情報含む）
gog gmail message <message-id> --json

# 添付ファイル一覧
gog gmail attachments <message-id>

# 添付ファイルダウンロード
gog gmail attachment <message-id> <attachment-id> --output ./downloads/
```

### Sending Emails

**基本送信:**

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

**HTML メール:**

```bash
gog gmail send \
  --to recipient@example.com \
  --subject "Weekly Report" \
  --body-html "<h1>Weekly Report</h1><p>Key metrics this week:</p><ul><li>Revenue: $10K</li></ul>"
```

**添付ファイル:**

```bash
# 単一添付
gog gmail send \
  --to recipient@example.com \
  --subject "Report" \
  --body "Please review the attached report." \
  --attach report.pdf

# 複数添付
gog gmail send \
  --to recipient@example.com \
  --subject "Documents" \
  --body "Attached are the requested documents." \
  --attach report.pdf \
  --attach data.xlsx \
  --attach summary.docx
```

**開封トラッキング:**

Cloudflare Worker バックエンドを使用した開封トラッキング:

```bash
# 1. トラッキング設定（初回のみ）
gog gmail track setup --worker-url https://your-worker.workers.dev

# 2. トラッキング付き送信（HTML本文 + 単一受信者が必要）
gog gmail send \
  --to recipient@example.com \
  --subject "Proposal" \
  --body-html "<p>Please review the attached proposal.</p>" \
  --track

# 3. トラッキング状況確認
gog gmail track status
```

**制約:**
- トラッキングには HTML 本文が必須（`--body-html`）
- 単一受信者のみ対応

### Label Management

```bash
# ラベル一覧
gog gmail labels

# ラベル作成
gog gmail label create "Projects"
gog gmail label create "Projects/Active"
gog gmail label create "Projects/Archived"

# メッセージにラベル適用
gog gmail label apply <message-id> --label "Projects/Active"

# ラベル削除
gog gmail label delete "Projects/Archived"
```

### Drafts

```bash
# 下書き一覧
gog gmail drafts

# 下書き作成
gog gmail draft create \
  --to recipient@example.com \
  --subject "Draft Subject" \
  --body "Draft content..."

# 下書き送信
gog gmail draft send <draft-id>
```

### Filters

```bash
# フィルタ一覧
gog gmail filters

# フィルタの詳細はGmail UIで管理を推奨
# gogcli はフィルタの一覧表示に対応
```

### Vacation / Out of Office

```bash
# 不在応答を有効化
gog gmail vacation --enable \
  --subject "Out of Office" \
  --body "I am currently out of the office and will return on Feb 10."

# HTML本文で不在応答
gog gmail vacation --enable \
  --subject "不在のお知らせ" \
  --body-html "<p>ご連絡ありがとうございます。</p><p>現在不在にしております。2月10日に戻ります。</p>"

# 不在応答を無効化
gog gmail vacation --disable
```

### Delegation

```bash
# 委任一覧
gog gmail delegates

# 委任の追加・削除は Workspace 管理者権限が必要
```

### History & Watch (Pub/Sub)

```bash
# 履歴の取得（変更追跡）
gog gmail history --start-history-id <id>

# Pub/Sub Watch の設定（リアルタイム通知）
gog gmail watch --topic "projects/my-project/topics/gmail-notifications"
```

---

## Calendar

### Event Listing

**日付ベースの取得:**

```bash
# 今日のイベント
gog calendar events --today

# 明日のイベント
gog calendar events --from tomorrow --to tomorrow

# 期間指定
gog calendar events --from 2025-02-01 --to 2025-02-28

# 今後N日間
gog calendar events --next 7d
gog calendar events --next 24h

# 特定カレンダーのイベント
gog calendar events --today --calendar <calendar-id>
```

**JSON出力の活用:**

```bash
# JSON出力にはstartDayOfWeek、endDayOfWeekなどの便利フィールドが含まれる
gog calendar events --today --json | jq '.[].summary'

# 出席者情報を含む
gog calendar events --today --json | jq '.[] | {summary, start, attendees}'
```

### Event Creation

**基本イベント:**

```bash
# 時間指定イベント
gog calendar event create \
  --summary "Team Meeting" \
  --start "2025-02-01T10:00:00" \
  --end "2025-02-01T11:00:00"

# 終日イベント（日付のみ指定）
gog calendar event create \
  --summary "Company Holiday" \
  --start "2025-02-11" \
  --end "2025-02-11"

# 場所・説明付き
gog calendar event create \
  --summary "Quarterly Review" \
  --start "2025-02-01T14:00:00" \
  --end "2025-02-01T16:00:00" \
  --location "Conference Room A" \
  --description "Q4 performance review and Q1 planning."
```

**出席者付きイベント:**

```bash
gog calendar event create \
  --summary "Project Kickoff" \
  --start "2025-02-03T09:00:00" \
  --end "2025-02-03T10:00:00" \
  --attendees "alice@company.com,bob@company.com,carol@company.com"
```

**繰り返しイベント（RRULE）:**

```bash
# 毎週月曜
gog calendar event create \
  --summary "Weekly Standup" \
  --start "2025-02-03T09:00:00" \
  --end "2025-02-03T09:30:00" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=MO"

# 毎月第1火曜
gog calendar event create \
  --summary "Monthly Review" \
  --start "2025-02-04T14:00:00" \
  --end "2025-02-04T15:00:00" \
  --recurrence "RRULE:FREQ=MONTHLY;BYDAY=1TU"

# 平日毎日（10回で終了）
gog calendar event create \
  --summary "Daily Check-in" \
  --start "2025-02-03T08:30:00" \
  --end "2025-02-03T08:45:00" \
  --recurrence "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=10"

# 隔週金曜（2025年6月まで）
gog calendar event create \
  --summary "Bi-weekly Sprint Review" \
  --start "2025-02-07T16:00:00" \
  --end "2025-02-07T17:00:00" \
  --recurrence "RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=FR;UNTIL=20250630T000000Z"
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

```bash
# フォーカスタイム
gog calendar event create \
  --summary "Deep Work" \
  --event-type focusTime \
  --start "2025-02-03T09:00:00" \
  --end "2025-02-03T12:00:00"

# Out of Office（不在）
gog calendar event create \
  --summary "Vacation" \
  --event-type outOfOffice \
  --start "2025-02-10" \
  --end "2025-02-14"

# Working Location（勤務場所）
gog calendar event create \
  --summary "Work from Home" \
  --event-type workingLocation \
  --start "2025-02-03" \
  --end "2025-02-03"
```

### Event Update & Delete

```bash
# イベント更新
gog calendar event update <event-id> --summary "Updated Title"
gog calendar event update <event-id> --start "2025-02-01T11:00:00" --end "2025-02-01T12:00:00"

# イベント削除
gog calendar event delete <event-id>

# 確認なしで削除
gog calendar event delete <event-id> --force
```

### Conflict Detection

```bash
# 特定期間の競合を検出
gog calendar conflicts --from 2025-02-03 --to 2025-02-07

# JSON出力で詳細
gog calendar conflicts --from 2025-02-03 --to 2025-02-07 --json
```

### Free/Busy Queries

チームメンバーの空き時間を確認:

```bash
# 複数メンバーの空き時間
gog calendar freebusy \
  --emails "alice@company.com,bob@company.com,carol@company.com" \
  --from "2025-02-03T09:00:00" \
  --to "2025-02-03T18:00:00"

# JSON出力
gog calendar freebusy \
  --emails "team@company.com" \
  --from 2025-02-03 --to 2025-02-07 \
  --json
```

### Calendar Management

```bash
# カレンダー一覧
gog calendar list

# カレンダーIDの確認（JSONで取得）
gog calendar list --json | jq '.[] | {summary, id}'
```

### Timezone Handling

```bash
# デフォルトタイムゾーン設定
gog config set default_timezone "Asia/Tokyo"

# 環境変数で一時的に変更
GOG_TIMEZONE=UTC gog calendar events --today
GOG_TIMEZONE="America/New_York" gog calendar events --today

# イベント作成時のタイムゾーン
# ISO 8601形式で指定可能
gog calendar event create \
  --summary "Cross-timezone Meeting" \
  --start "2025-02-03T10:00:00-05:00" \
  --end "2025-02-03T11:00:00-05:00"
```

### Invitations & RSVP

```bash
# 招待の管理（出席者付きイベント）
gog calendar event create \
  --summary "Review Meeting" \
  --start "2025-02-03T14:00:00" \
  --end "2025-02-03T15:00:00" \
  --attendees "reviewer@company.com"

# 新しい時間の提案
gog calendar event propose-time <event-id> \
  --start "2025-02-03T15:00:00" \
  --end "2025-02-03T16:00:00"
```

---

## Chat [Workspace Only]

> Chat サービスは Google Workspace アカウントでのみ利用可能です。
> 個人の Gmail アカウントでは使用できません。

### Space Management

```bash
# スペース一覧
gog chat spaces

# スペースの詳細
gog chat space <space-id>

# JSON出力
gog chat spaces --json
```

### Messages

```bash
# スペース内のメッセージ一覧
gog chat messages --space <space-id>

# メッセージ送信
gog chat send --space <space-id> --text "Hello team!"

# スレッド内返信
gog chat send --space <space-id> --thread <thread-id> --text "Reply to thread"
```

### Direct Messages

```bash
# DM送信
gog chat dm --email colleague@company.com --text "Quick question about the project"
```

### Limitations

- Chat API は Google Workspace アカウントが必要
- 個人 Gmail アカウントでは使用不可
- Bot/App としてのメッセージ送信はサービスアカウント経由
- ファイル添付は現在非対応（API制限）
