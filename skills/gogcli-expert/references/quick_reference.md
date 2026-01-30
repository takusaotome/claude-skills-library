# gogcli Quick Reference

全13サービスのコマンドチートシート。各コマンドの詳細はサービス別リファレンスを参照。

## Authentication Commands

| コマンド | 説明 |
|---------|------|
| `gog auth credentials <path>` | OAuth2 クレデンシャル JSON を登録 |
| `gog --client <name> auth credentials <path>` | 名前付きクライアントでクレデンシャル登録 |
| `gog auth add <email>` | アカウントを認証（ブラウザ起動） |
| `gog auth add <email> --services <csv>` | 特定サービスのみ認証 |
| `gog auth add <email> --readonly` | 読み取り専用で認証 |
| `gog auth add <email> --force-consent` | 再同意を強制（スコープ追加時） |
| `gog auth add <email> --drive-scope <scope>` | Drive スコープ指定（full/readonly/file） |
| `gog auth list` | 認証済みアカウント一覧 |
| `gog auth status` | 現在のアカウント状態 |
| `gog auth remove <email>` | アカウント削除 |
| `gog auth alias set <alias> <email>` | エイリアス設定 |
| `gog auth alias list` | エイリアス一覧 |
| `gog auth alias unset <alias>` | エイリアス削除 |
| `gog auth keyring` | キーリングバックエンド確認 |
| `gog auth keyring <backend>` | キーリングバックエンド設定（auto/keychain/file） |
| `gog auth service-account set <email> --key <path>` | サービスアカウント設定 |

## Configuration Commands

| コマンド | 説明 |
|---------|------|
| `gog config path` | 設定ファイルの場所を表示 |
| `gog config list` | 全設定を表示 |
| `gog config get <key>` | 設定値を取得 |
| `gog config set <key> <value>` | 設定値を変更 |
| `gog config unset <key>` | 設定値を削除 |

## Gmail

| コマンド | 説明 |
|---------|------|
| `gog gmail threads` | スレッド一覧 |
| `gog gmail threads --query "<query>"` | Gmail 検索構文でスレッド検索 |
| `gog gmail messages --thread-id <id>` | スレッド内のメッセージ一覧 |
| `gog gmail message <id>` | メッセージ詳細 |
| `gog gmail send --to <email> --subject "<subj>" --body "<text>"` | メール送信 |
| `gog gmail send --to <email> --body-html "<html>" --track` | 開封トラッキング付きHTML送信 |
| `gog gmail send ... --attach <file>` | 添付ファイル付き送信 |
| `gog gmail labels` | ラベル一覧 |
| `gog gmail label create "<name>"` | ラベル作成 |
| `gog gmail label apply <msg-id> --label "<name>"` | ラベル適用 |
| `gog gmail drafts` | 下書き一覧 |
| `gog gmail draft create --to <email> --subject "<subj>" --body "<text>"` | 下書き作成 |
| `gog gmail filters` | フィルタ一覧 |
| `gog gmail vacation --enable --subject "<subj>" --body "<text>"` | 不在応答を有効化 |
| `gog gmail vacation --disable` | 不在応答を無効化 |
| `gog gmail delegates` | 委任一覧 |
| `gog gmail track setup --worker-url <url>` | 開封トラッキング設定 |

## Calendar

| コマンド | 説明 |
|---------|------|
| `gog calendar events --today` | 今日のイベント |
| `gog calendar events --from <date> --to <date>` | 期間指定でイベント取得 |
| `gog calendar events --next <duration>` | 今後N日/時間のイベント |
| `gog calendar event create --summary "<title>" --start "<dt>" --end "<dt>"` | イベント作成 |
| `gog calendar event create ... --attendees "<emails>"` | 出席者付きイベント作成 |
| `gog calendar event create ... --recurrence "<rrule>"` | 繰り返しイベント作成 |
| `gog calendar event create ... --event-type focusTime` | フォーカスタイム作成 |
| `gog calendar event create ... --event-type outOfOffice` | OOO イベント作成 |
| `gog calendar event update <id> --summary "<new>"` | イベント更新 |
| `gog calendar event delete <id>` | イベント削除 |
| `gog calendar conflicts --from <date> --to <date>` | 競合検出 |
| `gog calendar freebusy --emails "<csv>" --from <dt> --to <dt>` | 空き時間確認 |
| `gog calendar list` | カレンダー一覧 |

## Drive

| コマンド | 説明 |
|---------|------|
| `gog drive list` | ファイル一覧 |
| `gog drive list --query "<query>"` | ファイル検索 |
| `gog drive list --folder <id>` | フォルダ内ファイル一覧 |
| `gog drive download <file-id>` | ファイルダウンロード |
| `gog drive download <file-id> --output <dir>` | 出力先指定でダウンロード |
| `gog drive upload <file>` | ファイルアップロード |
| `gog drive upload <file> --folder <id>` | フォルダ指定でアップロード |
| `gog drive export <file-id> --mime <type>` | Google ファイルのエクスポート |
| `gog drive folder create "<name>"` | フォルダ作成 |
| `gog drive folder create "<name>" --parent <id>` | 親フォルダ指定で作成 |
| `gog drive permissions <file-id>` | 権限一覧 |
| `gog drive share <file-id> --email <email> --role <role>` | 権限付与 |
| `gog drive shared-drives` | 共有ドライブ一覧 |

## Sheets

| コマンド | 説明 |
|---------|------|
| `gog sheets get <id>` | スプレッドシート全体を読み取り |
| `gog sheets get <id> --range "<A1>"` | 範囲指定で読み取り（A1記法） |
| `gog sheets update <id> --range "<A1>" --values "<csv>"` | セルに書き込み |
| `gog sheets append <id> --range "<A1>" --values "<csv>"` | 行追加 |
| `gog sheets create --title "<name>"` | 新規スプレッドシート作成 |
| `gog sheets list <id>` | シート一覧（タブ一覧） |

## Docs & Slides

Docs と Slides は主に Drive エクスポート経由で操作:

| コマンド | 説明 |
|---------|------|
| `gog drive export <doc-id> --mime application/pdf` | Docs → PDF |
| `gog drive export <doc-id> --mime application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Docs → DOCX |
| `gog drive export <slides-id> --mime application/pdf` | Slides → PDF |
| `gog drive export <slides-id> --mime application/vnd.openxmlformats-officedocument.presentationml.presentation` | Slides → PPTX |

## Tasks

| コマンド | 説明 |
|---------|------|
| `gog tasks lists` | タスクリスト一覧 |
| `gog tasks list <tasklist-id>` | タスク一覧 |
| `gog tasks add <tasklist-id> --title "<name>"` | タスク作成 |
| `gog tasks add <tasklist-id> --title "<name>" --due <date>` | 期日付きタスク作成 |
| `gog tasks done <tasklist-id> <task-id>` | タスク完了 |
| `gog tasks undo <tasklist-id> <task-id>` | タスク未完了に戻す |
| `gog tasks delete <tasklist-id> <task-id>` | タスク削除 |
| `gog tasks clear <tasklist-id>` | 完了済みタスクをクリア |

## Chat [Workspace Only]

| コマンド | 説明 |
|---------|------|
| `gog chat spaces` | スペース一覧 |
| `gog chat messages --space <id>` | メッセージ一覧 |
| `gog chat send --space <id> --text "<msg>"` | メッセージ送信 |
| `gog chat dm --email <email> --text "<msg>"` | DM 送信 |

## Groups [Workspace Only]

| コマンド | 説明 |
|---------|------|
| `gog groups list` | グループ一覧 |
| `gog groups members <group-email>` | メンバー一覧 |

## Classroom

| コマンド | 説明 |
|---------|------|
| `gog classroom courses` | コース一覧 |
| `gog classroom roster <course-id>` | 名簿（生徒一覧） |
| `gog classroom coursework <course-id>` | 課題一覧 |
| `gog classroom submissions <course-id> <cw-id>` | 提出物一覧 |
| `gog classroom announcements <course-id>` | アナウンス一覧 |

## People & Contacts

| コマンド | 説明 |
|---------|------|
| `gog people me` | 自分のプロフィール |
| `gog people search "<name>"` | Workspace ディレクトリ検索 |
| `gog contacts search "<name>"` | 連絡先検索 |
| `gog contacts create --name "<name>" --email <email>` | 連絡先作成 |
| `gog contacts other` | その他の連絡先（やり取り履歴） |

## Keep [Workspace + Service Account Only]

| コマンド | 説明 |
|---------|------|
| `gog keep notes` | ノート一覧 |
| `gog keep note <id>` | ノート詳細 |
| `gog keep search "<query>"` | ノート検索 |

## Time

| コマンド | 説明 |
|---------|------|
| `gog time` | 現在時刻（UTC + ローカル） |

## Global Flags

| フラグ | 短縮 | 説明 |
|-------|------|------|
| `--account <email\|alias\|auto>` | | 使用するアカウントを選択 |
| `--client <name>` | | OAuth クライアントを選択 |
| `--json` | | JSON 出力 |
| `--plain` | | TSV 出力 |
| `--color <mode>` | | カラー制御（auto/always/never） |
| `--force` | | 確認プロンプトスキップ |
| `--no-input` | | プロンプト時エラー終了（CI向け） |
| `--verbose` | | 詳細ログ |
| `--enable-commands <csv>` | | コマンド許可リスト（サンドボックス） |
| `--help` | `-h` | ヘルプ表示 |

## Environment Variables

| 変数 | 説明 | 例 |
|-----|------|-----|
| `GOG_ACCOUNT` | デフォルトアカウント | `work@company.com` or `work` |
| `GOG_CLIENT` | デフォルト OAuth クライアント | `work` |
| `GOG_JSON` | デフォルト JSON 出力 | `1` or `true` |
| `GOG_PLAIN` | デフォルト TSV 出力 | `1` or `true` |
| `GOG_COLOR` | カラーモード | `auto`, `always`, `never` |
| `GOG_TIMEZONE` | タイムゾーン | `Asia/Tokyo`, `UTC`, `local` |
| `GOG_ENABLE_COMMANDS` | コマンド許可リスト | `gmail,calendar,tasks` |
| `GOG_KEYRING_BACKEND` | キーリングバックエンド | `auto`, `keychain`, `file` |
| `GOG_KEYRING_PASSWORD` | 暗号化キーリングパスワード | (セキュアに管理) |
| `GOG_IT_ACCOUNT` | 統合テスト用アカウント | `test@gmail.com` |

## Help System

```bash
# トップレベルヘルプ
gog --help

# サービス別ヘルプ
gog gmail --help
gog calendar --help

# サブコマンドヘルプ
gog gmail send --help

# 詳細ヘルプ（全コマンド展開）
GOG_HELP=full gog --help
```

## Common MIME Types for Export

| MIME Type | 形式 | 用途 |
|-----------|------|------|
| `application/pdf` | PDF | Docs/Sheets/Slides |
| `text/csv` | CSV | Sheets |
| `text/plain` | テキスト | Docs |
| `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | DOCX | Docs |
| `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | XLSX | Sheets |
| `application/vnd.openxmlformats-officedocument.presentationml.presentation` | PPTX | Slides |
| `image/png` | PNG | Slides（1ページ目） |
| `image/jpeg` | JPEG | Slides（1ページ目） |
