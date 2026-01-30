# Workspace Admin Services -- Groups / Classroom / People / Service Account

## Service Account Setup (Domain-Wide Delegation)

サービスアカウントは、人間のユーザーではなくアプリケーション自体が Google API にアクセスするための認証方式です。Workspace 管理者がドメイン全体の委任を設定することで、サービスアカウントが組織内の任意のユーザーとして API を実行できます。

### Prerequisites

1. **Google Cloud Console**: サービスアカウントの作成とキーファイルの生成
2. **Workspace Admin Console**: ドメイン全体の委任の設定とスコープの許可
3. **gogcli**: サービスアカウントキーの登録

### Step 1: Create Service Account (Google Cloud Console)

1. Google Cloud Console → IAM & Admin → Service Accounts
2. 「+ CREATE SERVICE ACCOUNT」をクリック
3. 名前と説明を入力
4. ロールは不要（API アクセスはスコープで制御）
5. キーを作成（JSON形式）→ ダウンロード

### Step 2: Enable Domain-Wide Delegation (Workspace Admin Console)

1. Workspace Admin Console → Security → API Controls → Domain-wide delegation
2. 「Add new」をクリック
3. サービスアカウントのクライアントID（Numeric ID）を入力
4. 必要なスコープを入力（カンマ区切り）

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
gog --account admin@domain.com gmail threads
```

**重要な動作:**
- サービスアカウントは OAuth リフレッシュトークンより優先される
- `--account` で指定したユーザーとして API を実行
- ドメイン内の別ユーザーとしても実行可能:

```bash
# 管理者がユーザーAのメールを確認（委任設定済みの場合）
gog auth service-account set userA@domain.com --key ~/service-account-key.json
gog --account userA@domain.com gmail threads
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
gog --account shared-inbox@domain.com gmail threads --query "is:unread"
```

---

## Groups [Workspace Only]

> Groups API は Google Workspace アカウントでのみ利用可能です。

### Group Listing

```bash
# グループ一覧
gog groups list

# JSON出力
gog groups list --json

# プレーン出力
gog groups list --plain
```

### Member Management

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

---

## Classroom

### Course Management

```bash
# コース一覧
gog classroom courses

# JSON出力
gog classroom courses --json

# 特定ステータスのコースのみ
gog classroom courses --json | jq '.[] | select(.courseState == "ACTIVE")'
```

### Roster (Student List)

```bash
# コースの名簿（生徒一覧）
gog classroom roster <course-id>

# JSON出力
gog classroom roster <course-id> --json

# 教師一覧
gog classroom teachers <course-id>
```

### Coursework (Assignments)

```bash
# 課題一覧
gog classroom coursework <course-id>

# JSON出力
gog classroom coursework <course-id> --json

# 課題の詳細
gog classroom coursework <course-id> <coursework-id>
```

### Submissions

```bash
# 提出物一覧
gog classroom submissions <course-id> <coursework-id>

# JSON出力（採点状態含む）
gog classroom submissions <course-id> <coursework-id> --json

# 提出済みのみフィルタ
gog classroom submissions <course-id> <coursework-id> --json | \
  jq '.[] | select(.state == "TURNED_IN")'
```

### Announcements & Topics

```bash
# アナウンス一覧
gog classroom announcements <course-id>

# トピック一覧
gog classroom topics <course-id>
```

### Guardians

```bash
# 保護者一覧
gog classroom guardians <student-id>
```

### Practical Patterns

```bash
# アクティブコースの課題一覧を取得
gog classroom courses --json | \
  jq -r '.[] | select(.courseState == "ACTIVE") | .id' | \
  while read course_id; do
    echo "=== Course: $course_id ==="
    gog classroom coursework "$course_id"
  done

# 未提出の生徒を特定
gog classroom submissions <course-id> <coursework-id> --json | \
  jq '.[] | select(.state == "NEW") | .userId'
```

---

## People

### Profile Information

```bash
# 自分のプロフィール
gog people me

# JSON出力
gog people me --json
```

### Directory Search (Workspace)

```bash
# Workspace ディレクトリ検索
gog people search "John Smith"

# JSON出力
gog people search "John" --json

# メールアドレスのみ抽出
gog people search "engineering" --json | jq -r '.[].emailAddresses[0].value'
```

### Limitations

- ディレクトリ検索は Workspace アカウントのドメイン内のユーザーに限定
- 個人 Gmail アカウントではディレクトリ検索は利用不可
- People API はプロフィール情報の読み取りが中心

---

## Contacts

### Contact Search

```bash
# 連絡先検索
gog contacts search "Jane"

# JSON出力
gog contacts search "Jane" --json

# その他の連絡先（やり取り履歴から自動生成）
gog contacts other
```

### Contact Creation

```bash
# 連絡先作成
gog contacts create --name "Jane Doe" --email jane@example.com

# 電話番号付き
gog contacts create --name "Jane Doe" --email jane@example.com --phone "+1-555-0100"

# 組織情報付き
gog contacts create --name "Jane Doe" --email jane@example.com \
  --organization "Acme Corp" --title "Engineer"
```

### Contact Update

```bash
# 連絡先更新
gog contacts update <contact-id> --phone "+1-555-0200"
```

### Practical Patterns

```bash
# 全連絡先のメールアドレスを抽出
gog contacts search "" --json | jq -r '.[].emailAddresses[0].value'

# CSV からの一括インポート
while IFS=, read -r name email phone; do
  gog contacts create --name "$name" --email "$email" --phone "$phone"
done < contacts.csv
```
