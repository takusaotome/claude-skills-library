# Productivity Services -- Drive / Sheets / Docs / Slides / Tasks / Keep

## Drive

### File Listing & Search

```bash
# ファイル一覧（My Drive ルート）
gog drive list

# 件数制限
gog drive list --max 50

# Drive 検索クエリ
gog drive list --query "name contains 'report'"
gog drive list --query "mimeType = 'application/pdf'"
gog drive list --query "modifiedTime > '2025-01-01'"
gog drive list --query "trashed = false and name contains 'budget'"

# フォルダ内のファイル一覧
gog drive list --folder <folder-id>

# JSON出力
gog drive list --json | jq '.[] | {name, id, mimeType}'
```

**Drive 検索クエリ演算子:**

| 演算子 | 説明 | 例 |
|-------|------|-----|
| `name contains '<text>'` | 名前に含まれる | `name contains 'report'` |
| `name = '<text>'` | 完全一致 | `name = 'Budget 2025.xlsx'` |
| `mimeType = '<type>'` | ファイルタイプ | `mimeType = 'application/pdf'` |
| `modifiedTime > '<date>'` | 変更日以降 | `modifiedTime > '2025-01-01'` |
| `createdTime > '<date>'` | 作成日以降 | `createdTime > '2025-01-01'` |
| `trashed = false` | ゴミ箱以外 | `trashed = false` |
| `'<email>' in owners` | 所有者 | `'user@company.com' in owners` |
| `'<email>' in writers` | 書き込み権限者 | `'user@company.com' in writers` |
| `sharedWithMe` | 共有されたファイル | `sharedWithMe` |
| `starred` | スター付き | `starred` |

**Google ファイルのMIMEタイプ:**

| MIMEタイプ | ファイル種類 |
|-----------|------------|
| `application/vnd.google-apps.document` | Google Docs |
| `application/vnd.google-apps.spreadsheet` | Google Sheets |
| `application/vnd.google-apps.presentation` | Google Slides |
| `application/vnd.google-apps.folder` | フォルダ |
| `application/vnd.google-apps.form` | Google Forms |
| `application/vnd.google-apps.drawing` | Google Drawings |

### File Download

```bash
# ファイルダウンロード（カレントディレクトリ）
gog drive download <file-id>

# 出力先指定
gog drive download <file-id> --output ./downloads/

# 複数ファイルの一括ダウンロード（パイプライン利用）
gog drive list --folder <folder-id> --json | \
  jq -r '.[].id' | \
  xargs -I{} gog drive download {} --output ./downloads/
```

### File Upload

```bash
# ファイルアップロード（My Drive ルート）
gog drive upload report.pdf

# フォルダ指定でアップロード
gog drive upload report.pdf --folder <folder-id>

# 複数ファイルアップロード
for f in *.pdf; do gog drive upload "$f" --folder <folder-id>; done
```

### Google File Export

Google Docs/Sheets/Slides は直接ダウンロードではなく、エクスポートが必要:

```bash
# Google Docs → PDF
gog drive export <doc-id> --mime application/pdf

# Google Docs → DOCX
gog drive export <doc-id> --mime application/vnd.openxmlformats-officedocument.wordprocessingml.document

# Google Docs → Plain Text
gog drive export <doc-id> --mime text/plain

# Google Sheets → CSV
gog drive export <spreadsheet-id> --mime text/csv

# Google Sheets → XLSX
gog drive export <spreadsheet-id> --mime application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

# Google Slides → PDF
gog drive export <slides-id> --mime application/pdf

# Google Slides → PPTX
gog drive export <slides-id> --mime application/vnd.openxmlformats-officedocument.presentationml.presentation

# 出力先指定
gog drive export <doc-id> --mime application/pdf --output ./exports/
```

**エクスポート可能なMIMEタイプ一覧:**

| 元ファイル | エクスポート形式 | MIMEタイプ |
|-----------|----------------|-----------|
| Docs | PDF | `application/pdf` |
| Docs | DOCX | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Docs | Plain Text | `text/plain` |
| Docs | HTML | `text/html` |
| Docs | Rich Text | `application/rtf` |
| Docs | EPUB | `application/epub+zip` |
| Sheets | CSV | `text/csv` |
| Sheets | XLSX | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Sheets | PDF | `application/pdf` |
| Sheets | TSV | `text/tab-separated-values` |
| Slides | PDF | `application/pdf` |
| Slides | PPTX | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| Slides | PNG（1ページ目） | `image/png` |
| Slides | JPEG（1ページ目） | `image/jpeg` |

### Folder Management

```bash
# フォルダ作成
gog drive folder create "Project Documents"

# 親フォルダ指定で作成
gog drive folder create "Q1 Reports" --parent <parent-folder-id>

# フォルダ内ファイル一覧
gog drive list --folder <folder-id>

# フォルダのみ検索
gog drive list --query "mimeType = 'application/vnd.google-apps.folder'"
```

### Permission Management

```bash
# 権限一覧
gog drive permissions <file-id>

# 権限付与
gog drive share <file-id> --email user@example.com --role reader
gog drive share <file-id> --email user@example.com --role writer
gog drive share <file-id> --email user@example.com --role commenter

# ドメイン全体に共有
gog drive share <file-id> --domain company.com --role reader

# リンク共有（anyone）
gog drive share <file-id> --anyone --role reader
```

**権限ロール:**

| ロール | 説明 |
|-------|------|
| `owner` | 所有者（変更不可） |
| `organizer` | 共有ドライブの管理者 |
| `fileOrganizer` | 共有ドライブのコンテンツ管理者 |
| `writer` | 編集者 |
| `commenter` | コメント可 |
| `reader` | 閲覧者 |

### Shared Drives

```bash
# 共有ドライブ一覧
gog drive shared-drives

# 共有ドライブ内のファイル一覧
gog drive list --shared-drive <drive-id>

# JSON出力
gog drive shared-drives --json
```

### Comments

```bash
# コメント一覧
gog drive comments <file-id>

# コメント追加
gog drive comment <file-id> --content "Please review this section."
```

---

## Sheets

### Reading Data

**基本読み取り:**

```bash
# スプレッドシート全体
gog sheets get <spreadsheet-id>

# A1記法で範囲指定
gog sheets get <spreadsheet-id> --range "Sheet1!A1:D10"
gog sheets get <spreadsheet-id> --range "Sheet1!A:A"      # A列全体
gog sheets get <spreadsheet-id> --range "Sheet1!1:1"       # 1行目全体
gog sheets get <spreadsheet-id> --range "Sheet1!A1:Z"      # A1から最終行まで

# 別のシート（タブ）
gog sheets get <spreadsheet-id> --range "Data!B2:F20"
```

**出力形式:**

```bash
# JSON出力（プログラム処理向き）
gog sheets get <spreadsheet-id> --range "Sheet1!A1:D10" --json

# プレーン出力（TSV形式）
gog sheets get <spreadsheet-id> --range "Sheet1!A1:D10" --plain

# パイプライン例: jqで特定列を抽出
gog sheets get <spreadsheet-id> --range "Sheet1!A1:D10" --json | \
  jq -r '.values[] | .[0] + "\t" + .[2]'

# TSVからCSVへの変換
gog sheets get <spreadsheet-id> --range "Sheet1!A1:Z100" --plain | \
  tr '\t' ',' > output.csv
```

**A1記法の参考:**

| 記法 | 範囲 |
|-----|------|
| `A1` | セルA1 |
| `A1:D10` | A1からD10の矩形範囲 |
| `A:A` | A列全体 |
| `1:1` | 1行目全体 |
| `A1:Z` | A1から最終行のZ列まで |
| `Sheet1!A1:D10` | Sheet1のA1:D10 |
| `'Sheet Name'!A1:D10` | スペース含むシート名 |

### Writing Data

```bash
# セルに書き込み
gog sheets update <spreadsheet-id> --range "Sheet1!A1" --values "Hello"

# 複数セルに書き込み（カンマ区切り）
gog sheets update <spreadsheet-id> --range "Sheet1!A1" --values "Name,Email,Phone"

# 行追加（既存データの末尾に追加）
gog sheets append <spreadsheet-id> --range "Sheet1!A1" --values "John,john@example.com,555-0100"

# 複数行の書き込みの場合は繰り返し実行
gog sheets append <spreadsheet-id> --range "Sheet1!A1" --values "Alice,alice@example.com,555-0101"
gog sheets append <spreadsheet-id> --range "Sheet1!A1" --values "Bob,bob@example.com,555-0102"
```

### Sheet Management

```bash
# 新規スプレッドシート作成
gog sheets create --title "Monthly Report"

# シート（タブ）一覧
gog sheets list <spreadsheet-id>

# JSON出力（シートIDの確認に便利）
gog sheets list <spreadsheet-id> --json
```

### Practical Patterns

**データ出力パターン:**

```bash
# Sheets → CSVファイル
gog drive export <spreadsheet-id> --mime text/csv --output ./data.csv

# Sheets → XLSXファイル
gog drive export <spreadsheet-id> --mime application/vnd.openxmlformats-officedocument.spreadsheetml.sheet \
  --output ./data.xlsx

# 特定範囲をTSVとして保存
gog sheets get <spreadsheet-id> --range "Sheet1!A1:Z100" --plain > data.tsv
```

**自動化パターン:**

```bash
# スクリプトからの書き込み
while IFS=, read -r name email phone; do
  gog sheets append <spreadsheet-id> --range "Sheet1!A1" --values "$name,$email,$phone"
done < contacts.csv
```

---

## Docs

Google Docs の操作は主に Drive エクスポートで行います。

### Export

```bash
# PDF出力
gog drive export <doc-id> --mime application/pdf --output ./report.pdf

# DOCX出力
gog drive export <doc-id> --mime application/vnd.openxmlformats-officedocument.wordprocessingml.document \
  --output ./report.docx

# テキスト抽出
gog drive export <doc-id> --mime text/plain --output ./report.txt

# HTML出力
gog drive export <doc-id> --mime text/html --output ./report.html
```

### Search & List

```bash
# Google Docsのみ検索
gog drive list --query "mimeType = 'application/vnd.google-apps.document'"

# 名前で検索
gog drive list --query "mimeType = 'application/vnd.google-apps.document' and name contains 'report'"
```

---

## Slides

Google Slides の操作も主に Drive エクスポートで行います。

### Export

```bash
# PDF出力
gog drive export <slides-id> --mime application/pdf --output ./presentation.pdf

# PPTX出力
gog drive export <slides-id> --mime application/vnd.openxmlformats-officedocument.presentationml.presentation \
  --output ./presentation.pptx

# サムネイル画像（1ページ目）
gog drive export <slides-id> --mime image/png --output ./thumbnail.png
```

### Search & List

```bash
# Google Slidesのみ検索
gog drive list --query "mimeType = 'application/vnd.google-apps.presentation'"
```

---

## Tasks

### Task List Management

```bash
# タスクリスト一覧
gog tasks lists

# JSON出力
gog tasks lists --json

# タスクリスト内のタスク一覧
gog tasks list <tasklist-id>
```

### Task CRUD

```bash
# タスク作成
gog tasks add <tasklist-id> --title "Review PR #42"

# 期日付きタスク
gog tasks add <tasklist-id> --title "Submit report" --due 2025-02-15

# タスクの詳細取得
gog tasks get <tasklist-id> <task-id>

# タスク更新
gog tasks update <tasklist-id> <task-id> --title "Updated title"
```

### Task Status

```bash
# タスクを完了にする
gog tasks done <tasklist-id> <task-id>

# タスクを未完了に戻す
gog tasks undo <tasklist-id> <task-id>

# タスク削除
gog tasks delete <tasklist-id> <task-id>

# 完了済みタスクを一括クリア
gog tasks clear <tasklist-id>
```

### Recurring Tasks

```bash
# 繰り返しタスクの設定（日付のみの期日に対応）
gog tasks add <tasklist-id> --title "Weekly review" --due 2025-02-03 --repeat weekly
```

### Practical Patterns

```bash
# タスクの一覧をプレーン出力
gog tasks list <tasklist-id> --plain

# JSON で未完了タスクを抽出
gog tasks list <tasklist-id> --json | jq '.[] | select(.status != "completed")'

# 今日期日のタスクを確認
gog tasks list <tasklist-id> --json | jq '.[] | select(.due == "2025-02-01")'
```

---

## Keep [Workspace + Service Account Only]

> Keep API は Google Workspace アカウント + サービスアカウントでのみ利用可能です。
> 個人 Gmail アカウントや通常の OAuth では使用できません。

### Note Operations

```bash
# ノート一覧
gog keep notes

# ノート詳細
gog keep note <note-id>

# ノート検索
gog keep search "meeting notes"

# JSON出力
gog keep notes --json
```

### Attachments

```bash
# ノートの添付ファイルダウンロード
gog keep attachment <note-id> <attachment-id>
```

### Requirements

Keep API を使用するには:

1. Google Workspace アカウントが必要
2. サービスアカウントによるドメイン全体の委任が必要
3. Keep API スコープ（`https://www.googleapis.com/auth/keep`）の許可が必要
4. 通常の OAuth2 では Keep API にアクセス不可
