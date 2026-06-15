# Productivity Services -- Drive / Sheets / Docs / Slides / Tasks / Keep

> 対象バージョン: gogcli v0.27.0。本リファレンスのコマンド・フラグはこのバージョンのスキーマ（`gog schema --json`）に基づきます。旧 v0.9 系から多くのコマンド名・サブコマンドが変更されています。

## Drive

### File Listing & Search

一覧は `gog drive ls`。トップレベル別名 `gog ls` でも同じ動作です。`--all-drives` は既定で有効で、共有ドライブも含めて一覧します。My Drive のみに絞るときは `--no-all-drives` を付けます。

```bash
# ファイル一覧（My Drive ルート）
gog drive ls
gog ls                        # トップレベル別名

# 件数制限
gog drive ls --max 50

# フォルダ内のファイル一覧
gog drive ls --parent <folder-id>

# Drive 検索クエリでフィルタ
gog drive ls --query "name contains 'report'"
gog drive ls --query "mimeType = 'application/pdf'"
gog drive ls --query "modifiedTime > '2025-01-01'"
gog drive ls --query "trashed = false and name contains 'budget'"

# My Drive のみ（共有ドライブを除外）
gog drive ls --no-all-drives

# JSON出力
gog drive ls --json | jq '.[] | {name, id, mimeType}'
```

全文検索には `gog drive search`（別名 `gog search` / `gog find`）を使います。引数は通常の検索語で、`--raw-query` を付けると Drive クエリ言語をそのまま渡せます。

```bash
# 全文検索
gog drive search "quarterly report"

# 特定フォルダ配下に限定
gog drive search "budget" --parent <folder-id>

# 特定の共有ドライブに限定
gog drive search "spec" --drive <drive-id>

# Drive クエリ言語を直接渡す
gog drive search "mimeType = 'application/pdf' and modifiedTime > '2025-01-01'" --raw-query
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

### File Metadata & URL

```bash
# ファイルのメタデータ取得
gog drive get <file-id>

# フィールドを限定して取得
gog drive get <file-id> --fields "id,name,modifiedTime,owners"

# 生の Drive API レスポンス（スクリプト・LLM 向け）
gog drive raw <file-id> --pretty

# Web URL を表示
gog drive url <file-id>
```

### File Download

ダウンロードは `gog drive download`。Google 形式のファイルは自動でエクスポートされます。トップレベル別名 `gog download` / `gog dl` も利用できます。

```bash
# ファイルダウンロード（既定の保存先）
gog drive download <file-id>

# 出力先を指定
gog drive download <file-id> --out ./report.pdf

# Google Docs/Sheets/Slides をエクスポート形式を明示してダウンロード
gog drive download <doc-id> --format pdf --out ./report.pdf
gog drive download <doc-id> --format docx --out ./report.docx
gog drive download <spreadsheet-id> --format csv --out ./data.csv
gog drive download <spreadsheet-id> --format xlsx --out ./data.xlsx
gog drive download <slides-id> --format pptx --out ./deck.pptx

# 複数ファイルの一括ダウンロード（パイプライン利用）
gog drive ls --parent <folder-id> --json | \
  jq -r '.[].id' | \
  xargs -I{} gog drive download {}
```

`--format` で指定できる値は `pdf|csv|xlsx|pptx|txt|png|docx|md`。省略時はファイル種別から推測されます。各サービスには専用のエクスポートコマンド（`gog sheets export` / `gog docs export` / `gog slides export`）もあり、そちらは下の各節で説明します。

### File Upload

アップロードは `gog drive upload`（トップレベル別名 `gog upload` / `gog up` / `gog put`）。`--convert` を付けると拡張子に応じて Google ネイティブ形式へ自動変換します。

```bash
# ファイルアップロード（My Drive ルート）
gog drive upload report.pdf

# フォルダ指定でアップロード
gog drive upload report.pdf --parent <folder-id>

# 名前を指定してアップロード
gog drive upload report.pdf --name "Q1 Report.pdf"

# Google ネイティブ形式へ自動変換
gog drive upload notes.md --convert
gog drive upload data.csv --convert-to sheet
gog drive upload draft.docx --convert-to doc

# 既存ファイルの内容を差し替え（共有リンク・権限は維持）
gog drive upload report.pdf --replace <file-id>

# 複数ファイルアップロード
for f in *.pdf; do gog drive upload "$f" --parent <folder-id>; done
```

### Folder Management

フォルダ作成は `gog drive mkdir`。配下のファイル一覧は `gog drive ls --parent` を使います。

```bash
# フォルダ作成
gog drive mkdir "Project Documents"

# 親フォルダ指定で作成
gog drive mkdir "Q1 Reports" --parent <parent-folder-id>

# フォルダ内ファイル一覧
gog drive ls --parent <folder-id>

# フォルダのみ検索
gog drive ls --query "mimeType = 'application/vnd.google-apps.folder'"

# フォルダツリーを表示（読み取り専用）
gog drive tree --parent <folder-id> --depth 3

# フォルダのサイズ集計
gog drive du --parent <folder-id> --sort size
```

### File Organization (Move / Rename / Copy / Delete)

```bash
# 移動（別フォルダへ）
gog drive move <file-id> --parent <new-folder-id>

# リネーム
gog drive rename <file-id> "New Name.pdf"

# コピー
gog drive copy <file-id> "Copy of Report" --parent <folder-id>

# ゴミ箱へ移動（既定）
gog drive delete <file-id>

# ゴミ箱を経由せず完全削除（取り消し不可。注意）
gog drive delete <file-id> --permanent

# ショートカット作成
gog drive shortcut create <target-id> --parent <folder-id> --name "Link to Report"
```

> `gog drive delete --permanent` はゴミ箱を経由せずファイルを即時削除します。復元できないため、対象 ID を必ず確認してください。

### Permission Management

権限付与は `gog drive share`。共有先は `--to anyone|user|domain` で選び、`--email` または `--domain` で対象を指定します。ロールは `reader|writer|commenter`。

```bash
# 権限一覧
gog drive permissions <file-id>

# ユーザーに共有
gog drive share <file-id> --to user --email user@example.com --role reader
gog drive share <file-id> --to user --email user@example.com --role writer
gog drive share <file-id> --to user --email user@example.com --role commenter --notify

# ドメイン全体に共有
gog drive share <file-id> --to domain --domain company.com --role reader

# リンク共有（anyone）
gog drive share <file-id> --to anyone --role reader

# 権限の削除
gog drive unshare <file-id> <permission-id>
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

### Sharing Audit & Bulk Operations

共有状態の棚卸しと一括変更が可能です。`audit` 系は読み取り専用で安全に実行できます。

```bash
# 公開・外部共有の検出（フォルダツリーをスキャン）
gog drive audit sharing --parent <folder-id>

# 外部ユーザーのみ報告
gog drive audit sharing --parent <folder-id> --external-only

# 特定ユーザーに付与された権限を洗い出す
gog drive audit user user@example.com --parent <folder-id>

# 公開（anyone）権限を一括削除
gog drive bulk remove-public --parent <folder-id>

# ロールを一括変更（writer → reader など）
gog drive bulk update-role --parent <folder-id> --from writer --to reader
```

### Shared Drives

共有ドライブ一覧は `gog drive drives`。

```bash
# 共有ドライブ一覧
gog drive drives

# 特定の共有ドライブを検索
gog drive drives --query "name contains 'Marketing'"

# 共有ドライブ内のファイル検索
gog drive search "spec" --drive <drive-id>

# JSON出力
gog drive drives --json
```

### Comments

```bash
# コメント一覧
gog drive comments list <file-id>

# 未解決・解決済みを含むすべて（quoted テキスト付き）
gog drive comments list <file-id> --include-quoted

# コメント追加
gog drive comments create <file-id> "Please review this section."

# 返信
gog drive comments reply <file-id> <comment-id> "Done, updated."

# 解決
gog drive comments resolve <file-id> <comment-id>
```

### Revisions, Changes & Activity

```bash
# リビジョン一覧
gog drive revisions list <file-id>

# リビジョンのメタデータ
gog drive revisions get <file-id> <revision-id>

# 同期用の開始ページトークンを取得
gog drive changes start-token

# トークン以降の変更を列挙（同期・自動化向け）
gog drive changes list --token <page-token>

# Drive アクティビティ（監査イベント）の照会
gog drive activity query --folder <folder-id> --actions edit,create,delete
```

### Inventory & Labels

```bash
# 読み取り専用の Drive インベントリを出力
gog drive inventory --parent <folder-id> --sort path

# ラベルスキーマ一覧
gog drive labels list

# ファイルに適用されたラベル一覧
gog drive labels file list <file-id>

# ファイルにラベルを適用
gog drive labels file apply <file-id> <label-id> --text status=approved
```

---

## Sheets

Sheets は v0.27 で大幅に拡張され、値の読み書きに加えて書式・条件付き書式・グラフ・テーブル・データ検証など多数のサブコマンドを備えます。ここでは代表的なものを扱います。レンジは A1 記法で指定します。

### Reading Data

値取得は `gog sheets get`（別名 `read` / `show`）。

```bash
# A1記法で範囲指定
gog sheets get <spreadsheet-id> "Sheet1!A1:D10"
gog sheets get <spreadsheet-id> "Sheet1!A:A"      # A列全体
gog sheets get <spreadsheet-id> "Sheet1!1:1"      # 1行目全体
gog sheets get <spreadsheet-id> "Sheet1!A1:Z"     # A1から最終行まで

# 別のシート（タブ）
gog sheets get <spreadsheet-id> "Data!B2:F20"

# 数式や未整形値を取得
gog sheets get <spreadsheet-id> "Sheet1!A1:D10" --render FORMULA
gog sheets get <spreadsheet-id> "Sheet1!A1:D10" --render UNFORMATTED_VALUE
```

**出力形式とパイプライン:**

```bash
# JSON出力（プログラム処理向き）
gog sheets get <spreadsheet-id> "Sheet1!A1:D10" --json

# jqで特定列を抽出
gog sheets get <spreadsheet-id> "Sheet1!A1:D10" --json | \
  jq -r '.values[] | .[0] + "\t" + .[2]'
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

更新は `gog sheets update`（別名 `edit` / `set`）、追記は `gog sheets append`、消去は `gog sheets clear`。

```bash
# セルに書き込み
gog sheets update <spreadsheet-id> "Sheet1!A1" "Hello"

# 複数列に書き込み
gog sheets update <spreadsheet-id> "Sheet1!A1:C1" "Name" "Email" "Phone"

# JSON 2次元配列で複数行を一括書き込み
gog sheets update <spreadsheet-id> "Sheet1!A1" \
  --values-json '[["Name","Email"],["Alice","alice@example.com"],["Bob","bob@example.com"]]'

# 末尾に行を追加
gog sheets append <spreadsheet-id> "Sheet1!A:C" "John" "john@example.com" "555-0100"

# 範囲をクリア
gog sheets clear <spreadsheet-id> "Sheet1!A1:C100"

# 複数レンジを1リクエストで更新
gog sheets batch-update <spreadsheet-id> \
  --data-json '[{"range":"Sheet1!A1:B1","values":[["x","y"]]},{"range":"Sheet1!A2:B2","values":[["1","2"]]}]'
```

入力解釈は `--input` で切り替えます。既定は `USER_ENTERED`（数式や日付を解釈）。文字列をそのまま入れたいときは `--input RAW`。

### Spreadsheet & Tab Management

旧 `gog sheets list` は廃止されました。スプレッドシート全体の情報は `gog sheets metadata`（別名 `info`）で取得します。シートIDやタブ名はここで確認できます。

```bash
# 新規スプレッドシート作成
gog sheets create "Monthly Report"

# シート名を指定して作成
gog sheets create "Monthly Report" --sheets "Summary,Detail,Raw"

# スプレッドシートのメタデータ（タブ一覧・シートID）
gog sheets metadata <spreadsheet-id>

# タブ操作
gog sheets add-tab <spreadsheet-id> "Q2"
gog sheets rename-tab <spreadsheet-id> "Sheet1" "Summary"
gog sheets delete-tab <spreadsheet-id> "Old"
gog sheets reorder-tab <spreadsheet-id> --tab "Summary" --to 0

# Google Sheet を複製
gog sheets copy <spreadsheet-id> "Report (Copy)" --parent <folder-id>
```

### Formatting, Charts & Structure

書式・条件付き書式・グラフ・テーブルなどの代表例です。これら以外にも `banding`（縞模様）、`merge`/`unmerge`、`freeze`、`insert`、`delete-dimension`、`resize-columns`/`resize-rows`、`number-format`、`named-ranges`、`notes`、`links`、`validation`、`copy-paste`、`read-format` など多数のサブコマンドがあります。詳細は `gog sheets <command> --help` を参照してください。

```bash
# 範囲に書式を適用（CellFormat JSON）
gog sheets format <spreadsheet-id> "Sheet1!A1:D1" \
  --format-json '{"textFormat":{"bold":true},"backgroundColor":{"red":0.9,"green":0.9,"blue":0.9}}'

# 数値フォーマット（通貨・日付など）
gog sheets number-format <spreadsheet-id> "Sheet1!B2:B100" --type CURRENCY --pattern '$#,##0.00'

# 行・列の固定
gog sheets freeze <spreadsheet-id> --rows 1

# 条件付き書式（値が100超で背景色）
gog sheets conditional-format add <spreadsheet-id> "Sheet1!B2:B100" \
  --type number-gt --expr 100 \
  --format-json '{"backgroundColor":{"red":1,"green":0.8,"blue":0.8}}'

# 検索・置換
gog sheets find-replace <spreadsheet-id> "TODO" "DONE" --sheet "Tasks"

# グラフ作成（ChartSpec JSON）
gog sheets chart create <spreadsheet-id> --spec-json @chart.json --anchor E2 --sheet "Summary"

# PDF/XLSX/CSV へエクスポート
gog sheets export <spreadsheet-id> --format csv --out ./data.csv
gog sheets export <spreadsheet-id> --format xlsx --out ./data.xlsx
gog sheets export <spreadsheet-id> --format pdf --out ./report.pdf
```

### Practical Patterns

```bash
# CSV を1行ずつ末尾に追記
while IFS=, read -r name email phone; do
  gog sheets append <spreadsheet-id> "Sheet1!A:C" "$name" "$email" "$phone"
done < contacts.csv

# 生の Sheets API レスポンス（スクリプト・LLM 向け）
gog sheets raw <spreadsheet-id> --pretty
```

---

## Docs

v0.27 では Docs にフル編集サーフェスが追加されました。作成・本文の読み書き・検索置換・書式・画像/表挿入・コメント・タブ操作などが行えます。代表的なものを紹介します。

### Create, Read & Export

```bash
# 空の Google Doc を作成
gog docs create "Design Notes"

# Markdown ファイルから作成
gog docs create "Design Notes" --file ./notes.md

# 本文をプレーンテキストで取得
gog docs cat <doc-id>

# 段落番号付きで取得（編集位置の特定に便利）
gog docs cat <doc-id> --numbered

# メタデータ
gog docs info <doc-id>

# エクスポート（pdf|docx|txt|md|html）
gog docs export <doc-id> --format pdf --out ./report.pdf
gog docs export <doc-id> --format docx --out ./report.docx
gog docs export <doc-id> --format md --out ./report.md
```

### Writing & Editing

本文の書き込みは `gog docs write`、任意位置への挿入は `gog docs insert`、検索置換は `gog docs find-replace`（または `edit`）、正規表現置換は `gog docs sed`。

```bash
# 本文を Markdown で置き換え
gog docs write <doc-id> --markdown --replace --file ./body.md

# 末尾に追記
gog docs write <doc-id> --append --text "Appendix"

# テキスト挿入（リテラルテキストをアンカーに、その直前へ）
gog docs insert <doc-id> "Inserted line" --at "Section 2"

# 検索置換（全置換）
gog docs find-replace <doc-id> "v0.9" "v0.27"

# 最初の1件のみ置換
gog docs find-replace <doc-id> "draft" "final" --first

# 正規表現置換（sed 形式）
gog docs sed <doc-id> 's/colour/color/g'

# 範囲の削除（リテラルテキストをアンカーに）
gog docs delete <doc-id> --at "Obsolete paragraph"
```

### Formatting, Images & Tables

```bash
# 段落・文字書式（見出し化・太字など）
gog docs format <doc-id> --match "Overview" --heading-level 1
gog docs format <doc-id> --match "重要" --bold --text-color "#CC0000"

# 画像挿入（公開 URL またはローカル画像をアップロード）
gog docs insert-image <doc-id> --url "https://example.com/chart.png"
gog docs insert-image <doc-id> --file ./diagram.png --width 400

# 表の挿入
gog docs insert-table <doc-id> --rows 3 --cols 4 --at-end

# 表の行・列を編集
gog docs table-row insert <doc-id> --at end --table 1
gog docs table-column delete <doc-id> --col 2 --table 1

# 見出し・構造・タブの確認
gog docs headings list <doc-id>
gog docs structure <doc-id>
gog docs tabs list <doc-id>
```

このほか `comments`（コメント）、`named-range`（名前付き範囲）、`page-layout`（ページ設定）、`insert-page-break`、`insert-date-chip` / `insert-person` / `insert-file-chip`（スマートチップ）、`raw`（生 API レスポンス）など多数のサブコマンドがあります。詳細は `gog docs <command> --help` を参照してください。

### Search & List

```bash
# Google Docsのみ検索
gog drive ls --query "mimeType = 'application/vnd.google-apps.document'"

# 名前で検索
gog drive ls --query "mimeType = 'application/vnd.google-apps.document' and name contains 'report'"
```

---

## Slides

Slides も作成からエクスポートまで一通り操作できます。Markdown やテンプレートからのデッキ生成にも対応します。

### Create & Export

```bash
# 空のプレゼンテーションを作成
gog slides create "Q1 Review"

# Markdown からデッキを生成（## Notes はスピーカーノートになる）
gog slides create-from-markdown "Q1 Review" --content-file ./deck.md

# テンプレートから生成（プレースホルダ置換）
gog slides create-from-template <template-id> "Client Proposal" \
  --replace "client=Acme" --replace "date=2026-06-14"

# エクスポート（pdf|pptx）
gog slides export <presentation-id> --format pdf --out ./deck.pdf
gog slides export <presentation-id> --format pptx --out ./deck.pptx

# メタデータ
gog slides info <presentation-id>
```

### Edit Slides

```bash
# スライド一覧（オブジェクトID確認）
gog slides list-slides <presentation-id>

# 1枚のスライドの内容を読む（ノート・テキスト・画像）
gog slides read-slide <presentation-id> <slide-id>

# 全面画像のスライドを追加（スピーカーノート付き）
gog slides add-slide <presentation-id> ./slide1.png --notes "導入"

# 既存スライドの画像を差し替え
gog slides replace-slide <presentation-id> <slide-id> ./slide1-v2.png

# スライド削除
gog slides delete-slide <presentation-id> <slide-id>

# 画像・テキストの挿入
gog slides insert-image <presentation-id> <slide-id> ./logo.png --width 120
gog slides insert-text <presentation-id> <object-id> "Updated heading" --replace

# 全体の文字列置換
gog slides replace-text <presentation-id> "{{title}}" "Q1 Business Review"

# スピーカーノート更新
gog slides update-notes <presentation-id> <slide-id> --notes "話す内容"

# サムネイル画像の取得
gog slides thumbnail <presentation-id> <slide-id> --out ./thumb.png --size large
```

### Search & List

```bash
# Google Slidesのみ検索
gog drive ls --query "mimeType = 'application/vnd.google-apps.presentation'"
```

---

## Tasks

v0.27 でタスクリスト操作は `gog tasks lists` 配下にグループ化されました。タスク本体の操作はトップレベルの `gog tasks <command>` です。

### Task List Management

```bash
# タスクリスト一覧
gog tasks lists list

# JSON出力
gog tasks lists list --json

# タスクリスト作成
gog tasks lists create "Project Alpha"
```

### Task Listing & CRUD

タスク一覧は `gog tasks list`（別名 `ls`）、追加は `gog tasks add`（別名 `create`）。いずれも対象タスクリストID が必須です。

```bash
# タスク一覧
gog tasks list <tasklist-id>

# タスク作成（--title 必須）
gog tasks add <tasklist-id> --title "Review PR #42"

# 期日付きタスク
gog tasks add <tasklist-id> --title "Submit report" --due 2026-06-30

# サブタスクとして作成
gog tasks add <tasklist-id> --title "Subtask" --parent <parent-task-id>

# タスクの詳細取得
gog tasks get <tasklist-id> <task-id>

# タスク更新
gog tasks update <tasklist-id> <task-id> --title "Updated title" --notes "追記"
```

### Task Status

完了化は `gog tasks done`（別名 `complete`）、未完了化は `gog tasks undo`、削除は `gog tasks delete`、完了済みの一括クリアは `gog tasks clear`。

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

繰り返しは `--repeat`（または別名 `--recur`）で指定します。`--repeat-count` や `--repeat-until` で回数・終了日を制御できます。

```bash
# 毎週繰り返すタスク
gog tasks add <tasklist-id> --title "Weekly review" --due 2026-06-15 --repeat weekly

# 回数を指定
gog tasks add <tasklist-id> --title "Daily standup" --due 2026-06-15 --repeat daily --repeat-count 5
```

### Practical Patterns

```bash
# 未完了タスクのみ抽出
gog tasks list <tasklist-id> --json | jq '.[] | select(.status != "completed")'

# 期日でフィルタ
gog tasks list <tasklist-id> --due-min 2026-06-01T00:00:00Z --due-max 2026-06-30T23:59:59Z

# 生の Tasks API レスポンス
gog tasks raw <tasklist-id> <task-id> --pretty
```

---

## Keep [Workspace + Service Account Only]

> Keep API は Google Workspace アカウント + サービスアカウントでのみ利用可能です。個人 Gmail アカウントや通常の OAuth では使用できません。`gog auth keep` でサービスアカウントを設定するか、各コマンドに `--service-account <path>` と `--impersonate <email>` を渡します。

### Note Operations

```bash
# ノート一覧
gog keep list

# フィルタ付き一覧
gog keep list --filter 'create_time > "2026-01-01T00:00:00Z"'

# ノート詳細
gog keep get <note-id>

# ノート検索（クライアント側のテキスト一致）
gog keep search "meeting notes"

# ノート作成（本文）
gog keep create --title "Ideas" --text "First idea"

# チェックリストノートを作成
gog keep create --title "Shopping" --item "Milk" --item "Bread"

# ノート削除
gog keep delete <note-id>

# JSON出力
gog keep list --json
```

### Attachments

```bash
# ノートの添付ファイルダウンロード
gog keep attachment <attachment-name> --mime-type image/jpeg --out ./photo.jpg
```

### Requirements

Keep API を使用するには:

1. Google Workspace アカウントが必要
2. サービスアカウントによるドメイン全体の委任が必要
3. Keep API スコープ（`https://www.googleapis.com/auth/keep`）の許可が必要
4. 各コマンドにサービスアカウントを渡す方法は2通り: `gog auth keep` で事前設定するか、`--service-account <path> --impersonate <email>` を都度指定する
5. 通常の OAuth2 では Keep API にアクセス不可
