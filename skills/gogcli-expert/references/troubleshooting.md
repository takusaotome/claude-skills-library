# Troubleshooting Guide

## Authentication Issues

### OAuth Flow Fails to Complete

**症状:** `gog auth add` でブラウザが開くが認証が完了しない。

**原因と対策:**

| 原因 | 対策 |
|------|------|
| ブラウザが自動起動しない | 表示されたURLを手動でコピーしてブラウザに貼り付け |
| ローカルコールバック失敗 | ファイアウォールがローカルポートをブロックしていないか確認 |
| OAuth同意画面が未設定 | Google Cloud Console で同意画面を設定し、テストユーザーを追加 |
| 必要な API が未有効化 | Google Cloud Console → APIs & Services → Library で対象APIを有効化 |
| テストユーザー未登録 | OAuth同意画面の設定で認証したいメールアドレスをテストユーザーに追加 |

```bash
# 詳細ログで問題を特定
gog --verbose auth add user@gmail.com
```

### Token Expired or Revoked

**症状:** `token has been expired or revoked` エラー。

**原因:**
- リフレッシュトークンが失効（Google側で無効化）
- ユーザーがアカウント設定でアクセスを取り消し
- OAuth同意画面がテストモードで、7日間の有効期限切れ
- パスワード変更によるトークン無効化

**対策:**

```bash
# 再認証
gog auth add user@gmail.com

# 再同意を強制（スコープ変更時にも有効）
gog auth add user@gmail.com --force-consent
```

**OAuth テストモードの制限:**
- テストモードのトークンは7日間で失効
- 本番運用の場合は OAuth同意画面を「本番」に移行
- 本番移行には Google による審査が必要な場合がある

### Refresh Token Not Returned

**症状:** `gog auth add` 実行後、リフレッシュトークンが保存されない。

**原因:** 既にアプリに対して承認済みの場合、Google は新しいリフレッシュトークンを返さないことがある。

**対策:**

```bash
# 再同意を強制
gog auth add user@gmail.com --force-consent
```

または:
1. Google Account → Security → Third-party apps with account access
2. gogcli のアクセスを削除
3. 再度 `gog auth add` を実行

### Keyring Issues

**症状:** キーリングへのアクセスエラー。

**macOS Keychain:**

```bash
# キーリングバックエンドを確認
gog auth keyring

# macOS Keychain に切り替え
gog auth keyring keychain

# Keychain Access.app でロック状態を確認
security unlock-keychain ~/Library/Keychains/login.keychain-db
```

**Linux (Secret Service / libsecret):**

```bash
# gnome-keyring が起動しているか確認
systemctl --user status gnome-keyring-daemon

# ファイルバックエンドにフォールバック
gog auth keyring file
```

**暗号化ファイルバックエンド:**

```bash
# ファイルバックエンドを使用
gog auth keyring file

# パスワードを設定（非対話環境用）
export GOG_KEYRING_PASSWORD='secure-password'
```

### Multiple Account Confusion

**症状:** 意図しないアカウントでコマンドが実行される。

**対策:**

```bash
# 現在のアカウント確認
gog auth status

# アカウント一覧
gog auth list

# 明示的にアカウント指定
gog --account work@company.com gmail threads

# デフォルトアカウント設定
export GOG_ACCOUNT=work@company.com
# または
gog config set default_account work@company.com
```

---

## Scope & Permission Issues

### 403 Forbidden / Insufficient Permission

**症状:** `403 Forbidden` または `Request had insufficient authentication scopes` エラー。

**原因と対策:**

| 原因 | 対策 |
|------|------|
| サービスのスコープが未認証 | `gog auth add <email> --services <svc> --force-consent` |
| 読み取り専用で認証したが書き込みが必要 | `gog auth add <email> --force-consent`（readonlyなしで再認証） |
| Drive スコープが制限的 | `gog auth add <email> --drive-scope full --force-consent` |
| サービスアカウントのスコープが未許可 | Workspace Admin Console でスコープを追加 |
| API が未有効化 | Google Cloud Console で該当APIを有効化 |

```bash
# 現在のスコープを確認
gog auth status --json

# 特定サービスのスコープを追加
gog auth add user@gmail.com --services sheets --force-consent

# すべてのサービスで再認証
gog auth add user@gmail.com --force-consent
```

### Adding New Services After Initial Auth

初回認証後に新しいサービスを追加する場合:

```bash
# スコープ追加（--force-consent が必要な場合がある）
gog auth add user@gmail.com --services tasks --force-consent
```

Google がリフレッシュトークンを返さない場合:
1. Google Account → Third-party apps で gogcli のアクセスを削除
2. `gog auth add user@gmail.com --services gmail,calendar,drive,sheets,tasks`

### Service Account Permission Denied

**症状:** サービスアカウントで 403 エラー。

**チェックリスト:**

1. ドメイン全体の委任が有効か
2. Workspace Admin Console でスコープが許可されているか
3. サービスアカウントのクライアントID（数値）が正しいか
4. 対象ユーザーがドメイン内に存在するか

```bash
# 詳細ログで確認
gog --verbose --account admin@domain.com gmail threads
```

---

## Command Issues

### Command Not Found

**症状:** `gog: command not found`

**対策:**

```bash
# Homebrew でインストール確認
brew list steipete/tap/gogcli

# パスを確認
which gog

# Homebrew リンクを修復
brew link steipete/tap/gogcli

# ソースビルドの場合
ls ./bin/gog
# PATH に追加 または フルパスで実行
./bin/gog --help
```

### Command Blocked by Sandbox

**症状:** コマンドがブロックされ実行できない。

**原因:** `--enable-commands` フラグまたは `GOG_ENABLE_COMMANDS` 環境変数でコマンドが制限されている。

```bash
# 環境変数を確認
echo $GOG_ENABLE_COMMANDS

# 制限を解除（環境変数をクリア）
unset GOG_ENABLE_COMMANDS

# または必要なコマンドを追加
export GOG_ENABLE_COMMANDS=gmail,calendar,drive,tasks
```

### Account Selection Errors

**症状:** `no account configured` または意図しないアカウントが使用される。

```bash
# アカウント一覧を確認
gog auth list

# 明示的に指定
gog --account user@gmail.com gmail threads

# 自動選択の仕組み:
# 1. --account フラグ
# 2. GOG_ACCOUNT 環境変数
# 3. config の default_account
# 4. 唯一のアカウント（1つだけの場合）
# 5. エラー（複数アカウントで指定なし）
```

### JSON Output Issues

**症状:** JSON出力がパースできない。

**原因:** 進捗メッセージが stderr に混在している場合がある。

```bash
# stderr を抑制して stdout のみ取得
gog gmail threads --json 2>/dev/null | jq .

# または verbose を無効化
gog gmail threads --json
```

---

## Service-Specific Issues

### Gmail: Send Fails

**症状:** メール送信が失敗する。

| 原因 | 対策 |
|------|------|
| `gmail.send` スコープ未認証 | `gog auth add <email> --services gmail --force-consent` |
| 送信制限に到達 | Gmail の1日あたり送信制限（個人: 500通、Workspace: 2000通）を確認 |
| 添付ファイルが大きすぎる | Gmail の添付制限は 25MB |
| 受信者アドレスが無効 | メールアドレスの形式を確認 |

### Gmail: Draft Delete が送信済みメールを消す（データ消失・重大）

**症状:** CLI で作った下書きを送信したはずなのに、後日その送信済みメールが Sent からもゴミ箱からも見つからない。`drafts delete` を実行した前後で「送信履歴が消える」事象が再発する。

**根本原因（メカニズム）:**

- Gmail の「下書き」は、本体メッセージに `DRAFT` ラベルを付けた**ポインタ**にすぎない。
- **API/CLI で作成した下書きを Gmail の Web 画面から送信**すると、理想動作（送信時に下書きが消え、新IDの送信メッセージになる）から外れ、**下書きのポインタが残ったまま実体が送信済みになる**ことがある（orphaned draft）。
- この孤立ドラフトの `draft-id` を `drafts delete` すると、Gmail API の `users.drafts.delete` は**ポインタの先の本体メッセージを即時・完全削除**する。実体が送信済みなら**送信済みメールごと消える**。
- `drafts.delete` は「**Does not simply trash it（ゴミ箱に入れず完全削除）**」仕様のため、**ゴミ箱からも復元不可**。`in:anywhere`（Trash/Spam含む全検索）でもヒットしなくなる。

**決定的な兆候（このシグナルが出たら止まる）:**

| シグナル | 意味 |
|---------|------|
| `drafts update <id>` → **`Message not a draft`（HTTP 400）** | その下書きの実体は**もう下書きではない＝送信済み**。404 ではなく 400 が出る点が重要 |
| `drafts list` に出ないのに `drafts get <id>` は返る | 孤立ドラフト（orphaned draft）のサイン |
| `drafts delete` が成功した後、Sent からメールが消える | 送信済み本体を削除した可能性が高い |

**対策・安全ルール:**

1. `Message not a draft` が出たら、**その `draft-id` を絶対に `delete` しない**。`gog gmail search 'in:sent ...'` や Google Admin の Email Log Search で送信済みかを先に確認する。
2. 下書きの「作り直し」を **delete → create で行わない**。内容変更は `gog gmail drafts update` を使う。
3. 送信後に残った孤立ドラフトの掃除は、**Gmail Web 画面からゴミ箱へ**移す（30日間は復元可能）。API の `drafts delete` は完全削除なので使わない。
4. **作成と送信を同じ経路で完結**させる。CLI で作った下書きは `gog gmail drafts send <id>` で送り、Web 画面からの送信と混在させない（混在が孤立ドラフトの主因）。
5. 「送ったか未送信か」の判断は、**メールボックスの Sent ではなく Google Admin の Email Log Search／受信者確認を真実**とする。削除で Sent コピーが消えると Sent が空に見え、**未送信と誤認して二重送信するリスク**が生じる。

**復旧（既に消えてしまった場合）:**

- **受信側のコピーは残る**（送達済みなら受信者の受信トレイにある）。コンテンツ自体は失われない。
- **Google Vault**（保持設定が有効な場合）は、ユーザー削除と無関係にメールを保持するため、管理者がエクスポートで復元できる。
- **Google Admin の Email Log Search** にメタデータ（ヘッダ）の監査記録は残る。
- 完全削除されたメールボックス内コピーは、ゴミ箱を経由しないため通常 UI からは復元できない。

**参考:**
- [users.drafts.delete（完全削除・ゴミ箱に入れない）](https://developers.google.com/gmail/api/reference/rest/v1/users.drafts/delete)
- [Gmail API: Create and send draft emails](https://developers.google.com/workspace/gmail/api/guides/drafts)
- [gmailr Issue #119（送信後に下書きが自動削除されず残る）](https://github.com/r-lib/gmailr/issues/119)

### Gmail: Track Setup Fails

**症状:** `gog gmail track setup` が失敗する。

**対策:**
- Cloudflare Worker のURLが正しいか確認
- Worker がデプロイ済みか確認
- トラッキングには HTML 本文（`--body-html`）と単一受信者が必要

### Calendar: Timezone Issues

**症状:** イベントの時刻がずれる。

```bash
# タイムゾーン設定を確認
gog config get default_timezone

# タイムゾーンを設定
gog config set default_timezone "Asia/Tokyo"

# 一時的に変更
GOG_TIMEZONE="America/New_York" gog calendar events --today

# イベント作成時にタイムゾーンを明示
gog calendar event create \
  --summary "Meeting" \
  --start "2025-02-01T10:00:00+09:00" \
  --end "2025-02-01T11:00:00+09:00"
```

### Calendar: Event Creation Fails

| 原因 | 対策 |
|------|------|
| 日時形式が不正 | ISO 8601 形式を使用: `2025-02-01T10:00:00` |
| 終了時刻が開始時刻より前 | 開始・終了の順序を確認 |
| `calendar` スコープ未認証 | `gog auth add <email> --services calendar --force-consent` |
| 繰り返しルールが不正 | RRULE 構文を確認（`FREQ=WEEKLY;BYDAY=MO`） |

### Drive: Download/Upload Fails

| 原因 | 対策 |
|------|------|
| ファイルIDが不正 | `gog drive list --json` でIDを再確認 |
| 権限不足 | ファイルの共有設定を確認 |
| Googleファイルをダウンロード | `gog drive export` を使用（`download` ではなく） |
| ファイルが大きすぎる | Drive API の制限を確認 |
| `drive` スコープが制限的 | `--drive-scope full` で再認証 |

```bash
# Googleファイル（Docs/Sheets/Slides）はexportを使用
gog drive export <file-id> --mime application/pdf

# 通常ファイル（PDF, XLSX等）はdownloadを使用
gog drive download <file-id>
```

### Sheets: Range Errors

**症状:** `Unable to parse range` エラー。

```bash
# 正しいA1記法:
gog sheets get <id> --range "Sheet1!A1:D10"     # OK
gog sheets get <id> --range "'Sheet Name'!A1:D10" # スペース含むシート名

# よくある間違い:
# gog sheets get <id> --range "A1:D10"            # シート名なし（デフォルトで最初のシート）
# gog sheets get <id> --range "Sheet 1!A1:D10"    # スペース含むがクォートなし
```

### Chat/Groups/Keep: Workspace Required

**症状:** `403` または `Not authorized` エラー。

これらのサービスは Google Workspace アカウントが必要です:

| サービス | 要件 |
|---------|------|
| Chat | Workspace アカウント |
| Groups | Workspace アカウント |
| Keep | Workspace + サービスアカウント |

個人の Gmail アカウントでは使用できません。

---

## Configuration Issues

### Config File Location

```bash
# 設定ファイルの場所を確認
gog config path

# macOS: ~/Library/Application Support/gogcli/config.json
# Linux: ~/.config/gogcli/config.json
# Windows: %AppData%\gogcli\config.json

# 設定一覧
gog config list

# 設定をリセット（設定ファイルを削除）
rm "$(gog config path)"
```

### Environment Variable Conflicts

環境変数は設定ファイルより優先されます:

```bash
# 現在の環境変数を確認
env | grep GOG_

# 競合する環境変数をクリア
unset GOG_ACCOUNT
unset GOG_CLIENT
unset GOG_JSON
unset GOG_PLAIN
unset GOG_TIMEZONE
unset GOG_ENABLE_COMMANDS
unset GOG_KEYRING_BACKEND
unset GOG_KEYRING_PASSWORD
```

---

## Diagnostic Commands

問題の切り分けに使用できるコマンド:

```bash
# バージョン確認
gog --version

# 認証状態
gog auth status
gog auth list

# 設定確認
gog config list
gog config path

# キーリング状態
gog auth keyring

# 詳細ログでコマンド実行
gog --verbose gmail threads

# ヘルプ確認
gog --help
gog gmail --help
GOG_HELP=full gog --help
```

## Getting Help

- **公式リポジトリ:** https://github.com/steipete/gogcli
- **Issue報告:** https://github.com/steipete/gogcli/issues
- **コマンドヘルプ:** `gog <command> --help`
- **詳細ヘルプ:** `GOG_HELP=full gog --help`
