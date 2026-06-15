# Workspace Admin Services -- Admin / Groups / Classroom / People / Contacts / Additional Services

> 対象 gogcli バージョン: v0.27.0。コマンドパス・フラグは `gog <command> --help` の実出力に基づく。

## Service Account Setup (Domain-Wide Delegation)

サービスアカウントは、人間のユーザーではなくアプリケーション自体が Google API にアクセスするための認証方式です。Workspace 管理者がドメイン全体の委任を設定することで、サービスアカウントが組織内の任意のユーザーとして API を実行できます。Directory API を使う `gog admin` 系コマンドはこの委任が前提です。

### Prerequisites

1. **Google Cloud Console**: サービスアカウントの作成とキーファイルの生成
2. **Workspace Admin Console**: ドメイン全体の委任の設定とスコープの許可
3. **gogcli**: サービスアカウントキーの登録

### Step 1: Create Service Account (Google Cloud Console)

1. Google Cloud Console → IAM & Admin → Service Accounts
2. 「+ CREATE SERVICE ACCOUNT」をクリック
3. 名前と説明を入力
4. ロールは不要。API アクセスはスコープで制御する
5. キーを作成（JSON形式）してダウンロード

### Step 2: Enable Domain-Wide Delegation (Workspace Admin Console)

1. Workspace Admin Console → Security → API Controls → Domain-wide delegation
2. 「Add new」をクリック
3. サービスアカウントのクライアントID（Numeric ID）を入力
4. 必要なスコープをカンマ区切りで入力

**スコープ許可リスト（よく使用されるもの）:**

| サービス | スコープ |
|---------|--------|
| Gmail | `https://mail.google.com/` |
| Gmail (readonly) | `https://www.googleapis.com/auth/gmail.readonly` |
| Gmail (send) | `https://www.googleapis.com/auth/gmail.send` |
| Calendar | `https://www.googleapis.com/auth/calendar` |
| Calendar (readonly) | `https://www.googleapis.com/auth/calendar.readonly` |
| Drive | `https://www.googleapis.com/auth/drive` |
| Drive (readonly) | `https://www.googleapis.com/auth/drive.readonly` |
| Sheets | `https://www.googleapis.com/auth/spreadsheets` |
| Sheets (readonly) | `https://www.googleapis.com/auth/spreadsheets.readonly` |
| Contacts | `https://www.googleapis.com/auth/contacts` |
| Contacts (readonly) | `https://www.googleapis.com/auth/contacts.readonly` |
| Groups | `https://www.googleapis.com/auth/cloud-identity.groups.readonly` |
| Admin Directory (users) | `https://www.googleapis.com/auth/admin.directory.user` |
| Admin Directory (groups) | `https://www.googleapis.com/auth/admin.directory.group` |
| Admin Directory (orgunits) | `https://www.googleapis.com/auth/admin.directory.orgunit` |
| Tasks | `https://www.googleapis.com/auth/tasks` |
| Chat | `https://www.googleapis.com/auth/chat.spaces` |
| Chat (messages) | `https://www.googleapis.com/auth/chat.messages` |
| Classroom | `https://www.googleapis.com/auth/classroom.courses.readonly` |
| Classroom (roster) | `https://www.googleapis.com/auth/classroom.rosters.readonly` |
| Classroom (coursework) | `https://www.googleapis.com/auth/classroom.coursework.students` |
| Keep | `https://www.googleapis.com/auth/keep` |
| People | `https://www.googleapis.com/auth/directory.readonly` |

**最小権限の推奨:**
- 読み取りのみの場合は `.readonly` スコープを使用
- Gmail 送信のみの場合は `.send` スコープを使用
- 必要なサービスのスコープのみを許可

### Step 3: Configure gogcli

```bash
# サービスアカウントキーを登録（特定ユーザーとして実行）
gog auth service-account set admin@domain.com --key ~/service-account-key.json

# 確認
gog auth list

# サービスアカウントでコマンド実行
gog --account admin@domain.com gmail search "in:inbox"
```

**重要な動作:**
- サービスアカウントは OAuth リフレッシュトークンより優先される
- `--account` で指定したユーザーとして API を実行
- ドメイン内の別ユーザーとしても実行可能:

```bash
# 管理者がユーザーAのメールを確認（委任設定済みの場合）
gog auth service-account set userA@domain.com --key ~/service-account-key.json
gog --account userA@domain.com gmail search "in:inbox"
```

### Service Account Removal

```bash
# サービスアカウント設定の削除
gog auth service-account unset admin@domain.com
```

### Common Patterns with Service Account

**組織全体のカレンダー監査:**

```bash
# 各ユーザーの今日のイベント数を集計
for user in alice@domain.com bob@domain.com carol@domain.com; do
  gog auth service-account set "$user" --key ~/sa-key.json
  count=$(gog --account "$user" calendar events --today --json | jq length)
  echo "$user: $count events"
done
```

**メール委任的な使用:**

```bash
# サービスアカウント経由で共有メールボックスの検索
gog auth service-account set shared-inbox@domain.com --key ~/sa-key.json
gog --account shared-inbox@domain.com gmail search "is:unread"
```

---

## Admin (Directory API) [Domain-Wide Delegation Required]

`gog admin` は Google Workspace 管理者向けの Directory API ラッパーです。ユーザー・組織単位・グループをドメイン規模で管理します。**すべてドメイン全体委任を設定したサービスアカウントが前提**で、管理者本人として実行します。`--account` で管理者を指定してください。

### Users

```bash
# ユーザー一覧
gog admin users list
gog admin users list --domain example.com --all

# ユーザー詳細
gog admin users get user@domain.com

# ユーザー作成
gog admin users create newuser@domain.com \
  --given "Taro" --family "Yamada" \
  --password 'InitPass#123' --org-unit /Sales \
  --change-password

# 一時停止と削除
gog admin users suspend user@domain.com
gog admin users delete user@domain.com
```

`create` は `--recovery-email` / `--recovery-phone`（E.164形式）/ `--suspended` / `--archived` などにも対応します。`--password` を省くと初期パスワードが自動生成されます。

### Organizational Units (orgunits)

```bash
# 組織単位の一覧（デフォルトはルート配下）
gog admin orgunits list
gog admin orgunits list --parent /Sales --type all

# 詳細・作成・更新・削除
gog admin orgunits get /Sales
gog admin orgunits create "West" --parent /Sales --description "West region"
gog admin orgunits update /Sales/West --name "West-Coast"
gog admin orgunits delete /Sales/West
```

エイリアス `org-units` / `ou` も使えます。

### Groups (Admin / Directory API)

`gog admin groups` は Directory API 経由のグループ管理で、メンバーの追加・削除ができます。Cloud Identity 版の `gog groups`（読み取り専用、後述）とは別物です。

```bash
# ドメイン内のグループ一覧
gog admin groups list --domain example.com --all

# メンバー一覧
gog admin groups members list engineering@example.com --all

# メンバー追加（ロール指定可: MEMBER / MANAGER / OWNER）
gog admin groups members add engineering@example.com newperson@example.com --role MANAGER

# メンバー削除
gog admin groups members remove engineering@example.com person@example.com
```

---

## Groups (Cloud Identity) [Workspace Only]

> このセクションの `gog groups` は Cloud Identity Groups API を使い、**自分が所属するグループの読み取り**を行います。Workspace アカウント専用です。メンバーの追加・削除や全ドメインのグループ管理は前述の `gog admin groups` を使ってください。

### Group Listing

```bash
# 自分が所属するグループ一覧
gog groups list

# 全ページ取得・JSON出力
gog groups list --all --json
```

### Member Listing

```bash
# グループメンバー一覧
gog groups members engineering@company.com

# JSON出力（ロール情報付き）
gog groups members engineering@company.com --json

# メンバーのロール:
# OWNER   - グループ管理者
# MANAGER - グループ管理補助
# MEMBER  - 一般メンバー
```

### Practical Patterns

```bash
# 全グループとメンバー数の一覧
gog groups list --json | jq -r '.[].email' | while read group; do
  count=$(gog groups members "$group" --json | jq length)
  echo "$group: $count members"
done

# 特定グループのメンバーメール一覧
gog groups members engineering@company.com --json | jq -r '.[].email'
```

**2系統の使い分け:**

| 目的 | コマンド | API | 必要権限 |
|------|---------|-----|---------|
| 自分の所属グループとメンバーを読む | `gog groups list` / `gog groups members` | Cloud Identity | サービスアカウント、または `cloud-identity.groups.readonly` スコープ付きトークン（標準の `auth add --services` 対象外。`gog auth services` で `groups` は user=false） |
| ドメイン全体のグループ管理・メンバー編集 | `gog admin groups ...` | Directory | サービスアカウント＋ドメイン委任 |

---

## Classroom

Google Classroom は v0.27 で大きく拡張され、コース・名簿・課題・提出物・アナウンス・教材・トピック・保護者などをフル管理できます。多くのコマンドが `list` / `get` / `create` / `update` / `delete` のサブコマンドを持ちます。代表的な操作を示します。

### Course Management

```bash
# コース一覧（状態でフィルタ可）
gog classroom courses list
gog classroom courses list --state ACTIVE --all

# 詳細・作成・更新
gog classroom courses get <course-id>
gog classroom courses create --name "Algebra 101" --section "A" --room "201"
gog classroom courses update <course-id> --name "Algebra I"

# アーカイブ・復元・削除（削除はアーカイブ済みのみ）
gog classroom courses archive <course-id>
gog classroom courses unarchive <course-id>
gog classroom courses delete <course-id>

# 参加・退出・Web URL 表示
gog classroom courses join <course-id> --role student
gog classroom courses leave <course-id>
gog classroom courses url <course-id>
```

### Roster / Students / Teachers

```bash
# 名簿（生徒＋教師）。--students / --teachers で絞り込み
gog classroom roster <course-id>
gog classroom roster <course-id> --students --all

# 生徒の一覧・追加・削除
gog classroom students list <course-id>
gog classroom students add <course-id> <user-id> --enrollment-code <code>
gog classroom students remove <course-id> <user-id>

# 教師の一覧・追加・削除
gog classroom teachers list <course-id>
gog classroom teachers add <course-id> <user-id>
gog classroom teachers remove <course-id> <user-id>
```

### Coursework (Assignments)

```bash
# 課題一覧（トピック・状態でフィルタ可）
gog classroom coursework list <course-id>
gog classroom coursework list <course-id> --state PUBLISHED --order-by "dueDate desc"

# 詳細・作成・更新・削除
gog classroom coursework get <course-id> <coursework-id>
gog classroom coursework create <course-id> --title "Homework 1" \
  --due-date 2026-07-01 --due-time 23:59 --max-points 100
gog classroom coursework update <course-id> <coursework-id> --title "HW1 (revised)"
gog classroom coursework delete <course-id> <coursework-id>

# 個別生徒への割り当て変更
gog classroom coursework assignees <course-id> <coursework-id> \
  --mode INDIVIDUAL_STUDENTS --add-student <user-id>
```

### Submissions

```bash
# 提出物一覧（状態・遅延・ユーザーでフィルタ可）
gog classroom submissions list <course-id> <coursework-id>
gog classroom submissions list <course-id> <coursework-id> --state TURNED_IN --late late

# 詳細
gog classroom submissions get <course-id> <coursework-id> <submission-id>

# 採点（下書き／確定）
gog classroom submissions grade <course-id> <coursework-id> <submission-id> --draft 85
gog classroom submissions grade <course-id> <coursework-id> <submission-id> --assigned 90

# 返却・取り戻し・提出
gog classroom submissions return <course-id> <coursework-id> <submission-id>
gog classroom submissions reclaim <course-id> <coursework-id> <submission-id>
gog classroom submissions turn-in <course-id> <coursework-id> <submission-id>
```

### Announcements / Materials / Topics

```bash
# アナウンス
gog classroom announcements list <course-id>
gog classroom announcements create <course-id> --text "Welcome to class"

# 教材
gog classroom materials list <course-id>
gog classroom materials create <course-id> --title "Syllabus"

# トピック
gog classroom topics list <course-id>
gog classroom topics create <course-id> --name "Unit 1"
```

### Guardians / Invitations / Profile

```bash
# 保護者一覧・招待
gog classroom guardians list <student-id>
gog classroom guardian-invitations create <student-id> --email parent@example.com

# コース招待（生徒・教師・オーナー）
gog classroom invitations create <course-id> <user-id> --role STUDENT
gog classroom invitations accept <invitation-id>

# ユーザープロフィール
gog classroom profile get [<user-id>]
```

### Practical Patterns

```bash
# アクティブコースの課題一覧を取得
gog classroom courses list --state ACTIVE --json | \
  jq -r '.[].id' | \
  while read course_id; do
    echo "=== Course: $course_id ==="
    gog classroom coursework list "$course_id"
  done

# 未提出の生徒を特定
gog classroom submissions list <course-id> <coursework-id> --json | \
  jq '.[] | select(.state == "NEW") | .userId'
```

---

## People

`gog people` は Google People API のラッパーです。自分のプロフィール表示とディレクトリ検索が中心です。

### Profile Information

```bash
# 自分のプロフィール
gog people me

# トップレベルの別名でも同じ結果
gog me
gog whoami

# 特定ユーザーのプロフィールを ID 指定で取得
gog people get <user-id>
```

### Directory Search (Workspace)

`search` のエイリアスは `find` / `query` です。

```bash
# Workspace ディレクトリ検索
gog people search "John Smith"

# 全ページ取得・JSON出力
gog people search "engineering" --all --json

# メールアドレスのみ抽出
gog people search "engineering" --json | jq -r '.[].emailAddresses[0].value'
```

### Relations / Raw

```bash
# ユーザーのリレーション情報
gog people relations [<user-id>] --type manager

# People API の生レスポンスを JSON でダンプ（スクリプト・LLM 用、ロスレス）
gog people raw <user-id> --pretty
gog people raw <user-id> --person-fields "names,emailAddresses,organizations"
```

### Limitations

- ディレクトリ検索は Workspace アカウントのドメイン内のユーザーに限定
- 個人 Gmail アカウントではディレクトリ検索は利用不可
- People API はプロフィール情報の読み取りが中心

---

## Contacts

`gog contacts` は Google Contacts（People API）のラッパーです。個人の連絡先、やり取り履歴から自動生成される「その他の連絡先」、Workspace ディレクトリの3系統を扱います。連絡先 ID は People API の `resourceName`（例 `people/c123...`）です。

### Listing & Search

```bash
# 連絡先一覧
gog contacts list

# 連絡先検索（名前・メール・電話）
gog contacts search "Jane"
gog contacts search "Jane" --json

# その他の連絡先（やり取り履歴から自動生成）
gog contacts other list
gog contacts other search "support"
```

### Create / Get / Update / Delete

```bash
# 連絡先作成（--given は必須）
gog contacts create --given "Jane" --family "Doe" --email jane@example.com

# 電話・組織・役職付き
gog contacts create --given "Jane" --family "Doe" --email jane@example.com \
  --phone "+1-555-0100" --org "Acme Corp" --title "Engineer"

# 詳細取得
gog contacts get people/c1234567890

# 更新（空文字を渡すとそのフィールドをクリア）
gog contacts update people/c1234567890 --phone "+1-555-0200"

# 削除
gog contacts delete people/c1234567890
```

### Directory (Workspace)

```bash
# Workspace ディレクトリの人を一覧・検索
gog contacts directory list --all
gog contacts directory search "engineering"
```

### Dedupe / Export / Raw

```bash
# 重複候補の検出（プレビューのみ、削除はしない）
gog contacts dedupe --match email,phone

# vCard (.vcf) としてエクスポート
gog contacts export --all -o contacts.vcf
gog contacts export --query "Acme" -o acme.vcf

# 生の People API レスポンスを JSON でダンプ
gog contacts raw people/c1234567890 --pretty
```

### Practical Patterns

```bash
# 全連絡先のメールアドレスを抽出
gog contacts list --json | jq -r '.[].emailAddresses[0].value'

# CSV からの一括インポート
while IFS=, read -r given family email phone; do
  gog contacts create --given "$given" --family "$family" --email "$email" --phone "$phone"
done < contacts.csv
```

---

# Additional Services (v0.27 で追加)

v0.27 では以下の新サービス群が追加されました。各サービスとも `gog <service> <command>` の形で、多くは `--json` 出力に対応します。Workspace 限定や追加 API 有効化が必要なものはその旨を明記します。

## Forms

Google Forms の作成・編集・回答取得を行います。

```bash
# フォーム作成・取得
gog forms create --title "Survey 2026" --description "Customer survey"
gog forms get <form-id>

# 設問の追加（type: text|paragraph|radio|checkbox|dropdown|scale|date|time）
gog forms add-question <form-id> --title "Your name" --type text --required
gog forms add-question <form-id> --title "Rating" --type radio \
  --option "Good" --option "OK" --option "Bad"

# 設問の一覧・移動・削除
gog forms questions add <form-id> --title "Comments" --type paragraph
gog forms move-question <form-id> <oldIndex> <newIndex>
gog forms delete-question <form-id> <index>

# 回答取得
gog forms responses list <form-id>
gog forms responses get <form-id> <response-id>

# 公開・更新・生データ
gog forms publish <form-id>
gog forms publish <form-id> --unpublish
gog forms update <form-id> --quiz true
gog forms raw <form-id> --pretty
```

`watch`（Cloud Pub/Sub への回答プッシュ通知）は別途 Pub/Sub トピックの用意が必要です。

```bash
gog forms watch create <form-id> --topic projects/<proj>/topics/<topic>
```

## Meet

Google Meet の会議スペース作成と通話履歴・参加者の確認を行います。

```bash
# 会議スペース作成（--access: open|trusted|restricted）
gog meet create --access trusted --open

# 取得・設定変更・終了
gog meet get <meeting-code>
gog meet update <meeting-code> --access open
gog meet end <meeting-code>

# 過去の通話履歴と参加者
gog meet history <meeting-code> --all
gog meet participants <meeting-code> --max 50
```

## Maps

Google Maps Platform を使った経路・距離・ジオコーディング・場所検索です。**Maps Platform の API キー有効化が必要**です。

```bash
# 経路（route エイリアスあり）。mode: driving|walking|bicycling|transit
gog maps directions --origin "Tokyo Station" --destination "Shibuya" --mode transit

# 距離・所要時間マトリクス
gog maps distance --origins "Tokyo" --destinations "Osaka,Kyoto" --units metric

# ジオコーディング・逆ジオコーディング
gog maps geocode "1600 Amphitheatre Parkway"
gog maps reverse-geocode --lat 35.6812 --lng 139.7671

# 場所検索・詳細
gog maps places search "ramen near Shinjuku"
gog maps places details <place-id>
```

## YouTube

YouTube Data API による検索・動画・チャンネル・プレイリスト・登録・コメントの操作です。`--mine` を使う操作はアカウント指定（`-a` / `--account`）が必要です。

```bash
# 検索（type: video|channel|playlist）
gog youtube search list "lo-fi beats" --type video --order viewCount

# 動画・チャンネル
gog youtube videos list --id <id1>,<id2>
gog youtube videos list --chart mostPopular --region US
gog youtube channels list --mine

# プレイリスト
gog youtube playlists list --mine
gog youtube playlists create --title "My Mix" --privacy private
gog youtube playlists add --playlist-id <pl-id> --video-id <video-id>
gog youtube playlists items list --playlist-id <pl-id> --all
gog youtube playlists remove --playlist-id <pl-id> --video-id <video-id>

# 登録チャンネル・アクティビティ・コメント
gog youtube subscriptions list --all
gog youtube activities list --mine
gog youtube comments list --video-id <video-id>
```

## Photos

Google Photos の Library API（**アプリが作成したメディアのみ**読み取り可）と、ユーザー選択メディアを扱う Picker API の2系統です。

```bash
# アプリ作成メディアの一覧・取得・検索・ダウンロード
gog photos list --max 50
gog photos get <media-item-id>
gog photos search --from 2026-01-01 --to 2026-03-31 --media-type PHOTO
gog photos download <media-item-id> --out ./out/

# Picker API: ユーザーに選んでもらったメディアにアクセス
gog photos picker create --max-items 10 --open
gog photos picker wait <session-id>
gog photos picker list <session-id> --all
gog photos picker download <session-id> <media-item-id> --out ./picked/
gog photos picker delete <session-id>
```

Library API は他人やスマホ撮影の写真全体にはアクセスできません。ユーザー全体のライブラリから選ばせたい場合は Picker フローを使います。

## Sites

Google Sites は Drive ベースで管理され、サイトの一覧・取得・検索・編集URL表示ができます。

```bash
gog sites list
gog sites get <site-id>
gog sites search "team wiki"
gog sites url <site-id>
```

`list` / `search` は既定で共有ドライブを含みます。マイドライブのみに絞るには `--no-all-drives` を使います。

## Analytics (GA4)

Google Analytics Data API（GA4）でアカウントサマリーの一覧とレポート実行を行います。

```bash
# GA4 アカウントサマリー一覧
gog analytics accounts

# レポート（property は GA4 プロパティ ID）
gog analytics report properties/123456789 \
  --dimensions date,country --metrics activeUsers,sessions \
  --from 28daysAgo --to today
```

`--from` / `--to` は `YYYY-MM-DD` か `7daysAgo` のような GA 相対日付を受け付けます。

## Search Console (gsc)

Google Search Console の検索アナリティクス・サイトマップ・サイト管理です。エイリアスは `gsc` / `search-console` / `webmasters`。

```bash
# 検索アナリティクス（dimensions: DATE,QUERY,PAGE,COUNTRY,DEVICE など）
gog gsc query https://example.com/ \
  --dimensions QUERY --from 2026-01-01 --to 2026-01-31 --max 1000

# サイトマップ
gog gsc sitemaps list https://example.com/
gog gsc sitemaps submit https://example.com/ https://example.com/sitemap.xml
gog gsc sitemaps delete https://example.com/ https://example.com/sitemap.xml

# 登録サイト
gog gsc sites list
gog gsc sites get https://example.com/
```

`searchanalytics query` というサブコマンド形も同じクエリ機能を提供します。

## Apps Script

Google Apps Script プロジェクトの作成・取得・コンテンツ表示・実行です。`run` は対象スクリプトに API 実行可能なデプロイが必要です。

```bash
# プロジェクト作成・メタデータ・内容
gog appscript create --title "My Script"
gog appscript get <script-id>
gog appscript content <script-id>

# デプロイ済み関数の実行
gog appscript run <script-id> <function> --params '["arg1", 42]'
gog appscript run <script-id> myFunc --dev-mode
```

## Zoom

Zoom は Server-to-Server OAuth による認証情報の登録・検証のみを提供します。Zoom Marketplace で Server-to-Server OAuth アプリを作成し、account ID / client ID / client secret を取得してください。

```bash
# 認証情報の登録
gog zoom auth setup \
  --account-id <account-id> --client-id <client-id> --client-secret <secret>

# 認証情報の検証（/users/me を呼んで確認）
gog zoom auth doctor
```

複数組織を扱う場合は `--alias` で名前付き資格情報を使い分けられます。
