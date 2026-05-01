# Secret Masking — 収集段階・保存前マスキングルール

機密情報を「**そもそも出さない**」「**出てしまった場合は出力前にマスクする**」「**Finding 根拠欄には絶対転記しない**」の 3 段階で防御する。

---

## 1. 設計原則

| 段階 | 防御策 | ファイル/プロセス |
|---|---|---|
| **§2 収集段階** | 秘密ファイル本文を取得しない（cat 禁止、stat / jq keys 等の代替） | レビュー実施者の判断 |
| **§3 保存前** | 採取済み出力に対して正規表現でマスク後に evidence_dir に保存 | 採取者ローカルでのフィルタ |
| **§4 レポート段階** | Finding 根拠欄に秘密値を一切転記せず、メタデータのみ記述 | Claude / レビュー者の規律 |
| **§5 検出** | 多段階検査で漏れを検出 | 検証 A の合格基準 |

---

## 2. 収集段階のルール

### 2.1 禁止される収集動作

秘密ファイル本文の `cat` / `head` / `tail` / `less` / `more` / `grep`（出力に本文が出る使い方）は禁止。対象は以下を含むがこれに限らない:

- `.env`、`.env.*`、`*.env`
- `*config*.json`、`*config*.yaml`、`*config*.yml`、`*config*.ini`
- `db-config*`、`session-config*`、`auth-config*`
- `/etc/sudoers`、`/etc/sudoers.d/*`（exceptional_sensitive_read 区分）
- `/etc/shadow`、`/etc/gshadow`（exceptional_sensitive_read 区分、原則 Phase 1 で実施しない）
- `/etc/vpnc/*`、`/etc/openvpn/*`
- `*.key`、`*.pem`、`*.p12`、`*.pfx`、`id_rsa`、`id_ed25519`、`id_ecdsa`
- `*.sql`、`*.dump`、`*.bak`（DB ダンプ）
- `~/.aws/credentials`、`~/.docker/config.json`、`~/.kube/config`、`~/.netrc`
- `/var/lib/secrets/*`、`/etc/secrets/*`

### 2.2 許可される収集動作（代替手段）

| 目的 | NG（本文取得） | OK（メタデータ・キー名のみ）|
|---|---|---|
| 存在確認 | `cat <file>` | `stat <file>`、`ls -l <file>`、`test -e <file> && echo exists` |
| サイズ確認 | `cat <file> \| wc -c` | Linux: `stat -c '%s' <file>` / macOS: `stat -f '%z' <file>` |
| パーミッション確認 | `cat <file>` | `stat -c '%a %U %G' <file>`、`ls -l <file>` |
| 行数確認 | `wc -l <file>`（注：実装依存で本文を読む可能性あり、同等の `awk` も同様） | `awk 'END{print NR}' <file>`（行数のみ）|
| JSON 構造確認 | `cat config.json` | `jq 'keys' config.json`、`jq 'paths' config.json`（値非取得）|
| YAML 構造確認 | `cat config.yaml` | `yq 'keys' config.yaml`、`yq 'paths(scalars) \| select(. != null)' config.yaml` |
| 設定ファイル全体 | `cat *.conf` | `grep -oE '^\s*[a-zA-Z_][a-zA-Z0-9_-]*' *.conf`（キー名のみ）|
| 秘密鍵タイプ判定 | `cat *.key` | `ssh-keygen -l -f *.pub`（公開鍵から）、`stat *.key` |
| アカウント一覧 | `cat /etc/shadow` | `getent passwd \| awk -F: '$3 >= 1000 {print $1}'` |
| 環境変数確認 | `systemctl cat <unit>` 全体 | `systemctl show <unit> -p Environment --value` のうえ secret_masking 適用 |

### 2.3 Finding 根拠欄の書き方

❌ NG:
```
db-config_product.json には password: "AbC123XyZ!" が含まれる
```

✅ OK:
```
db-config_product.json (186 B, mode 644, owner root) に password キーが含まれることを
stat と jq 'keys' で確認。本文は未取得。raw_evidence_store には保存していない。
```

---

## 3. 保存前マスキング（正規表現）

採取者ローカルで evidence_dir に書き込む前に、以下の正規表現で自動マスク。`secret_masking_patterns.yaml`（assets 内に置く想定）に維持し、定期更新。

### 3.1 高特異度パターン（必須）

```
# パスワード・トークン・シークレット代入
(?i)(password|passwd|secret|token|api[_-]?key|access[_-]?key|auth)\s*[:=]\s*["']?([^"'\s]+)["']?
→ \1: ***MASKED***

# Bearer トークン
Bearer\s+[A-Za-z0-9._~+/=-]+
→ Bearer ***MASKED***

# Authorization ヘッダ
Authorization:\s*[A-Za-z]+\s+[A-Za-z0-9._~+/=-]+
→ Authorization: ***MASKED***

# AWS Access Key
AKIA[0-9A-Z]{16}
→ AKIA****************

# Google API Key
AIza[0-9A-Za-z_-]{35}
→ AIza***********************************

# Slack Token
xox[abprs]-[0-9A-Za-z-]+
→ xox*-***MASKED***

# Bitbucket / GitHub App Password
ATBB[a-zA-Z0-9]{32,}
→ ATBB***MASKED***

# GitHub Personal Access Token
ghp_[A-Za-z0-9]{36,}
→ ghp_***MASKED***

# 秘密鍵ブロック
-----BEGIN (RSA |EC |OPENSSH |DSA |ENCRYPTED |)PRIVATE KEY-----[\s\S]+?-----END (RSA |EC |OPENSSH |DSA |ENCRYPTED |)PRIVATE KEY-----
→ -----BEGIN PRIVATE KEY-----\n***MASKED***\n-----END PRIVATE KEY-----

# IP アドレス + ポート + 認証情報含む URL
(https?|mongodb|redis|amqp|postgres|mysql|mssql)://[^:]+:[^@]+@
→ \1://***:***@
```

### 3.2 高エントロピー文字列パターン（補助）

```
# base64 32+ 文字（前後に文字列なら除外）
(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{32,}={0,2}(?![A-Za-z0-9+/])
→ ***POSSIBLE_BASE64_SECRET***

# hex 32+ 文字
(?<![a-fA-F0-9])[a-fA-F0-9]{32,}(?![a-fA-F0-9])
→ ***POSSIBLE_HEX_SECRET***
```

これらは false positive が多いため、`secret_scan_attestation.txt` で立会者承認のうえ allowlist 化。

### 3.3 マスキング監査ログ

`evidence_dir/_masking_audit.log` に以下を記録:
- マスク適用箇所のファイル名・行番号・パターン名
- マスク前後の文字数（差分検出用、本文は記録しない）
- 適用日時

---

## 4. レポート段階のルール

### 4.1 Finding 根拠欄

- 秘密値の本文転記禁止
- 「ファイルが存在し、〜キーが含まれることを確認」の構造化記述
- raw が必要な場合は `raw_evidence_store/<path> 参照` の形で間接参照

### 4.2 推奨対応欄

- 「パスワードを変更」ではなく「漏洩前提で全認証情報をローテーション」と書く
- 具体的な認証情報名（DB パスワード、VPN パスワード、API キー等）は範囲を示すのみで値を書かない

### 4.3 エグゼクティブサマリ

- 「機密情報がインターネット公開されている」と影響範囲のみ記述
- 「db-config_product.json の password が `AbC123` で〜」のような具体例は禁止

---

## 5. 機密混入の多段階検査（検証 A の (d) 合格基準）

レポート完成後、機密混入ゼロを以下 4 段の AND で確認:

### 5.1 (d-1) 既知パターン grep

```bash
grep -nE '(password|passwd|secret|token|api[_-]?key|access[_-]?key)\s*[:=]\s*[^*]' <report>
grep -nE 'Authorization:\s*[A-Za-z]+\s+[A-Za-z0-9]' <report>
grep -nE 'Bearer\s+[A-Za-z0-9]' <report>
grep -nE '-----BEGIN ' <report>
grep -nE 'AKIA[0-9A-Z]{16}' <report>
grep -nE 'AIza[0-9A-Za-z_-]{35}' <report>
grep -nE 'xox[abprs]-' <report>
grep -nE 'ghp_[A-Za-z0-9]{36,}' <report>
```

注: `key` 単体は `primary_key`、`ssh_host_key`、`config key` 等で多発するため (d-1) には含めない。

### 5.2 (d-2) 高エントロピー文字列検出

```bash
# base64 32+ 文字
grep -nE '[A-Za-z0-9+/]{32,}={0,2}' <report>

# hex 32+ 文字
grep -nE '[a-f0-9]{32,}' <report>
```

### 5.3 (d-3) allowlist による FP 除外

以下は false positive として除外（`secret_allowlist.txt` に維持）:
- `test`, `example`, `placeholder`, `dummy`, `<...>` を含む行
- 公開された hash（commit hash、Docker image digest 等）
- レポート内の Finding ID（`PUBLIC-F042` 等）
- プロジェクト固有の公知パターン（プロジェクトごとに別途 allowlist に追加）

### 5.4 (d-4) 残ったヒットを人手目視で承認

立会者が「機密ではない」と署名したログを `secret_scan_attestation.txt` に保存:

```
# secret_scan_attestation.txt
report: 02_hq_server_regenerated.md
scan_run_at: 2026-04-30T22:00:00-07:00
attested_by: <立会者氏名>
attested_at: 2026-04-30T22:15:00-07:00
findings:
  - line: 142
    matched_pattern: "[a-f0-9]{40,}"
    matched_text: "abc123...def456 (commit hash)"
    classification: not_secret
    rationale: "Git commit hash, public information"
  - line: 287
    matched_pattern: "Authorization: "
    matched_text: "Authorization: <example>"
    classification: not_secret
    rationale: "documentation example with placeholder"
total_hits: 2
remaining_after_allowlist: 2
manually_attested: 2
true_secrets_found: 0
```

`true_secrets_found > 0` なら検証 A 不合格。

---

## 6. 生ログ管理

### 6.1 保管場所

- 採取者ローカル: 一時的のみ。レビュー終了後 24 時間以内に消去
- raw_evidence_store: アクセス制御ストレージ（S3 暗号化バケット、社内セキュア共有等）。Git 管理外
- evidence_dir: マスク済みのみ。レビュー成果物として共有可

### 6.2 保持期間

target_profile.yaml の `retention` セクションに従う:
- デフォルト: `raw_retention_days: 90`
- 認証情報ローテーション完了確認まで: 関係者限定アクセス
- 完全削除: ローテーション完了 + レポート確定後、または 90 日経過時のいずれか早い方

### 6.3 削除手順

```bash
# 採取者ローカル消去（即時）
shred -uvz ~/security_review_logs/<file>

# raw_evidence_store 消去（保持期限後）
# S3 の場合
aws s3 rm s3://<bucket>/<path> --recursive
# 社内ストレージの場合
# 各組織の secure deletion 手順に従う
```

削除実施を target_profile.yaml の retention セクションに記録。
