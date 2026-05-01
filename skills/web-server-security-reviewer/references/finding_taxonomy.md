# Finding Taxonomy — 汎用 Finding パターン辞書（v1 スケルトン）

各 Template Finding ID（`TPL-<CATEGORY>-<NAME>`）に対応する典型的な発見内容、根拠、推奨対応のパターン辞書。新規 Finding 起票時の参照、既存 Finding の分類精度向上に使用。

**状態**: スケルトン。代表 TPL を配置済（汎用 19 個 + role_extensions 参照分 11 個 + Phase 2 引き継ぎ 1 個 = 計 31 個）。本番運用には更なる拡充も検討。

---

## 1. 命名規則

```
TPL-<CATEGORY>-<NAME>
```

- `<CATEGORY>`: 観点ベースの大分類（OS / DISK / LOG / WEB / NET / SVC / AUTH / CRED / MON / BACKUP / TLS / NTP / RUNTIME / DEPS）
- `<NAME>`: 短い英大文字スネークケース

例:
- `TPL-OS-EOL`
- `TPL-LOG-ROTATE-MISSING`
- `TPL-WEB-ROOT-LEAK`
- `TPL-CRED-PLAINTEXT`

---

## 2. 各 TPL のフォーマット

```markdown
### TPL-<ID>: <見出し>

- **観点**: A1..A9
- **デフォルト重大度**: Critical | High | Medium | Low
- **典型的な observation_status**: confirmed
- **典型根拠**:
  - <観測パターン 1>
  - <観測パターン 2>
- **典型的な 3 軸スコア**:
  - Exploitability: ...
  - Blast Radius: ...
  - Service Criticality: ...（target 依存）
- **典型推奨対応**:
  - <対応 1>
  - <対応 2>
- **昇格条件**: <あれば>
- **降格条件**: <あれば>
- **関連 TPL**: <ID>
```

---

## 3. TPL 一覧（v1 スケルトン）

### TPL-OS-EOL: OS / カーネルが EOL

- **観点**: A1
- **デフォルト重大度**: High
- **典型根拠**: `cat /etc/os-release` で表示されるバージョンが vendor サポート期限切れ
- **3 軸スコア**: Exploitability=medium, Blast Radius=self〜lateral_internal, Service Criticality=target 依存
- **典型推奨対応**: 新 OS 版への移行計画策定、ESM 契約検討、移行までの暫定的な脆弱性軽減策
- **昇格条件**: active CVE 紐付け + active_incident 連動可能性 → Critical
- **降格条件**: ESM 契約済 + 動作確認済 → Medium

### TPL-OS-LONG-UPTIME: 長期未再起動（カーネルパッチ未適用疑い）

- **観点**: A1
- **デフォルト重大度**: High
- **典型根拠**: `uptime -s` で 180 日以上前
- **典型推奨対応**: メンテナンス再起動計画、月次/四半期次の再起動ウィンドウ制度化

### TPL-DISK-HIGH-USAGE: ディスク使用率閾値超過

- **観点**: A2
- **デフォルト重大度**: Medium（業務クリティカル + 90% 超で Critical）
- **典型根拠**: `df -h` で >70%
- **典型推奨対応**: 大容量ディレクトリ特定 → 削減ポリシー策定、容量監視アラート設定
- **昇格条件**: business_critical + >90% / 急上昇 / 過去同種インシデント → Critical (C2 成立)

### TPL-LOG-ROTATE-MISSING: ログローテーション未設定

- **観点**: A3
- **デフォルト重大度**: High
- **典型根拠**: `/etc/logrotate.d/` に対象ログのエントリなし、または log4js/winston 等の設定で `numBackups`/`compress` 未指定
- **典型推奨対応**: logrotate 設定追加、または framework 側のローテーション設定有効化
- **昇格条件**: 現にディスク逼迫 + business_critical → Critical (C2)

### TPL-LOG-CLEANUP-SILENT-FAIL: 削除スクリプト無言失敗

- **観点**: A3
- **デフォルト重大度**: High
- **典型根拠**: cron に登録された削除スクリプトの実体が不在、または cron からの呼び出しなし
- **典型推奨対応**: スクリプト実体復旧、cron 登録、cron 失敗検知設定

### TPL-LOG-DEBUG-IN-PROD: 本番で debug ログレベル

- **観点**: A3
- **デフォルト重大度**: Medium
- **典型根拠**: アプリ設定に `level: debug` または `enableCallStack: true`
- **典型推奨対応**: 本番設定を `level: info` に、`enableCallStack: false` に変更

### TPL-WEB-ROOT-LEAK: Web ドキュメントルート設定不備

- **観点**: A4
- **デフォルト重大度**: High
- **典型根拠**: nginx/apache の `root` ディレクティブが広範囲、`location` ブロック欠如により秘密ファイル直接配信（loopback + Host ヘッダで HTTP 200）
- **典型推奨対応**: `location` ブロック追加で秘密パス拒否、機密ファイルを Web root 外へ移動、`.git` 配下の deny
- **昇格条件**: 外部到達経路立証 + 機密本文取得可能 → Critical (C1 成立、漏洩前提扱い)

### TPL-WEB-GIT-IN-PROD: `.git` 本番残置

- **観点**: A4
- **デフォルト重大度**: High
- **典型根拠**: アプリ配置ディレクトリに `.git/` ディレクトリ存在、`/.git/HEAD` への HTTP 200
- **典型推奨対応**: 本番から `.git` 除外、デプロイ方式見直し（tar/scp/rsync 等）、nginx で `/.git` を deny

### TPL-WEB-TLS-OLD-VERSION: TLS 旧バージョン有効

- **観点**: A4 / A9
- **デフォルト重大度**: Medium
- **典型根拠**: `nginx -T` または `apachectl -S` 出力に `ssl_protocols TLSv1 TLSv1.1` 記載、`openssl s_client -tls1` で接続成立
- **典型推奨対応**: TLSv1.2 + TLSv1.3 のみに制限、Mozilla Intermediate 準拠の cipher suite

### TPL-RUNTIME-EOL: アプリランタイム EOL

- **観点**: A5
- **デフォルト重大度**: High
- **典型根拠**: `<runtime> --version` が vendor EOL 後のバージョン（Node.js 10/11、Python 2、PHP 5、Ruby 2.x 等）
- **典型推奨対応**: 最新 LTS 版への移行計画、移行中の脆弱性軽減策
- **昇格条件**: root 実行 + 0.0.0.0 バインド + 外部到達 + active CVE → Critical (C3 観測 3 点立証)

### TPL-APP-ROOT-EXEC: アプリが root 実行

- **観点**: A5
- **デフォルト重大度**: High
- **典型根拠**: `ps -ef` でアプリプロセスが UID 0
- **典型推奨対応**: 非特権ユーザ作成、systemd unit 化、capability 必要なら `AmbientCapabilities`

### TPL-CRED-PLAINTEXT: 認証情報の平文保存

- **観点**: A6
- **デフォルト重大度**: High
- **典型根拠**: VPN / DB / API 認証情報がスクリプトや設定ファイルに平文記述（`stat` でファイル存在 + `jq keys` でキー名確認、本文は exceptional_sensitive_read で限定確認）
- **典型推奨対応**: Secrets Manager / Vault 化、認証情報ローテーション、関連スクリプトの権限 600
- **昇格条件**: 外部到達経路ありで取得可能 → Critical (C4 漏洩前提)

### TPL-AUTH-ROOT-SSH: root への SSH 鍵経路存在

- **観点**: A6
- **デフォルト重大度**: High
- **典型根拠**: `sshd -T` 出力に `permitrootlogin without-password` または `yes`、`/root/.ssh/authorized_keys` 存在
- **典型推奨対応**: `PermitRootLogin no`、root への SSH 廃止、踏み台 + sudo 経由

### TPL-AUTH-NOPASSWD-ALL: sudoers NOPASSWD: ALL

- **観点**: A6
- **デフォルト重大度**: High
- **典型根拠**: `/etc/sudoers` または `/etc/sudoers.d/*` に `<user> ALL=(ALL) NOPASSWD: ALL`（exceptional_sensitive_read で確認）
- **典型推奨対応**: NOPASSWD 解除、必要最小限のコマンド許可リスト化

### TPL-MAC-DISABLED: SELinux / AppArmor 無効

- **観点**: A6
- **デフォルト重大度**: High
- **典型根拠**: `getenforce` が `Disabled` または `Permissive`、AppArmor が unloaded
- **典型推奨対応**: SELinux: Permissive → Enforcing 段階的移行、AppArmor: 該当プロファイルの enforce

### TPL-SECRET-WORLD-READABLE: 秘密ファイルが world-readable

- **観点**: A6
- **デフォルト重大度**: High
- **典型根拠**: `find` で mode -004 の `.env` / `*config*.json` / `*.key` 検出
- **典型推奨対応**: `chmod 600` または `640`、Secrets Manager 化検討

### TPL-MONITORING-ABSENT: 監視エージェント不在

- **観点**: A7
- **デフォルト重大度**: Medium（public_facing で High 昇格検討）
- **典型根拠**: `systemctl list-units` で代表的監視エージェント（CloudWatch / Datadog / Zabbix / Prometheus / New Relic）すべて未稼働
- **典型推奨対応**: 監視エージェント導入、ディスク/CPU/メモリ/プロセスのアラーム設定

### TPL-BACKUP-ABSENT: バックアップ取得不在

- **観点**: A8
- **デフォルト重大度**: Medium
- **典型根拠**: systemd timer / cron / クラウドスナップショットいずれにもバックアップジョブなし
- **典型推奨対応**: バックアップ方針策定、自動取得機構導入、リストアテスト計画

### TPL-TLS-CERT-EXPIRY: TLS 証明書期限間近

- **観点**: A9
- **デフォルト重大度**: Medium（30 日以内 High、期限切れ Critical）
- **典型根拠**: `openssl s_client + x509 -dates` で `notAfter` まで残 90 日以下
- **典型推奨対応**: certbot / ACM / 自動更新スクリプトで自動化、期限切れアラート

### TPL-DEPS-OLD: 依存パッケージが長期未更新

- **観点**: A5
- **デフォルト重大度**: Medium（observation_status: out_of_scope_phase1）
- **典型根拠**: `package.json` / `requirements.txt` / `Gemfile.lock` 等のバージョンが 2-3 年以上前
- **典型推奨対応**: Phase 2 で `npm audit` / `pip-audit` / `bundler-audit` 等の脆弱性スキャン、重要 CVE 対応

### TPL-NET-BIND-WILDCARD: アプリの 0.0.0.0 / [::] バインド

- **観点**: A4
- **デフォルト重大度**: Medium（internal で High 昇格、外部到達経路ありで Critical）
- **典型根拠**: `ss -tlnp` でアプリポートが `0.0.0.0:` または `*:` バインド
- **典型推奨対応**: `127.0.0.1` または内部 IF 限定バインドへ修正、SG/FW で外部遮断確認
- **昇格条件**: 内部用途なのに 0.0.0.0 バインド + ホスト FW 不在 → High

### TPL-NTP-INACTIVE: NTP デーモン不稼働

- **観点**: A9
- **デフォルト重大度**: Low
- **典型根拠**: chronyd / ntpd / systemd-timesyncd すべて inactive
- **典型推奨対応**: いずれか 1 つを active 化、`timedatectl set-ntp true`、外部 NTP サーバ設定

### TPL-NET-WAF-INACTIVE: WAF 設定が確認できない / 不在

- **観点**: A4
- **デフォルト重大度**: Medium（public_facing で）
- **典型根拠**: `nginx -V` / `apachectl -M` に modsecurity / naxsi なし、AWS WAF / Cloudflare 等の前段確認も不可
- **典型推奨対応**: WAF 導入（モジュール または 前段サービス）、本番への能動テストはステージング環境または別ツールで実施
- **注**: 本スキルは設定確認のみ。能動テスト（疑似攻撃）は範囲外

### TPL-NET-RATE-LIMIT-MISSING: rate limit 設定不在

- **観点**: A4
- **デフォルト重大度**: Medium
- **典型根拠**: nginx `limit_req_zone` / `limit_conn_zone` 不在、apache `mod_ratelimit` 未設定
- **典型推奨対応**: 重要エンドポイント（auth, login, search, api）に rate limit 設定追加

### TPL-INTERNAL-EXPOSED: 内部用途サーバが外部に露出

- **観点**: A4
- **デフォルト重大度**: High
- **典型根拠**: 内部用途サーバなのに 0.0.0.0 / [::] バインド、または公開 IP で名前解決可能
- **典型推奨対応**: 内部 IF / 127.0.0.1 限定バインド、SG / FW での外部遮断、内部 DNS のみで名前解決
- **昇格条件**: 機密データ取扱 + 認証なしアクセス可能 → Critical

### TPL-BASTION-NOT-ENFORCED: 踏み台経由アクセスが強制されていない

- **観点**: A6
- **デフォルト重大度**: Medium
- **典型根拠**: `sshd_config` に `AllowUsers` / `AllowGroups` / `Match` の接続元制限なし、または踏み台 IP 以外も許可
- **典型推奨対応**: `Match Address <bastion_ip>` ブロックで接続元制限、または前段 SG/FW で SSH 22/tcp を踏み台のみに制限

### TPL-MONITORING-COLOCATED: 監視サーバが踏み台などと同居

- **観点**: A7
- **デフォルト重大度**: Low
- **典型根拠**: Zabbix `Server=` / `ServerActive=` の接続先が踏み台 IP と一致
- **典型推奨対応**: 監視サーバを別インスタンスへ分離（踏み台多機能化はセキュリティ観点で懸念）

### TPL-VPN-CRED-PLAINTEXT: VPN 認証情報の平文保存

- **観点**: A6
- **デフォルト重大度**: High
- **典型根拠**: `/etc/vpnc/*` / `/etc/openvpn/*` 等に認証情報を含むファイル存在（メタデータ確認）、本文確認は exceptional_sensitive_read で別途
- **典型推奨対応**: Secrets Manager / Vault 化、認証情報ローテーション、関連スクリプトの権限 600
- **昇格条件**: 公開サーバへの中継経路 → Critical（漏洩時に侵害連鎖）

### TPL-VPN-PROCESS-DUP: VPN プロセス重複稼働

- **観点**: A5
- **デフォルト重大度**: Medium
- **典型根拠**: `pgrep openvpn|openconnect|vpnc|wg-quick` で 2 件以上検出（再接続スクリプトのバグ等）
- **典型推奨対応**: 既存プロセスチェック追加（`pgrep` or pid ファイル）、重複プロセスのクリーンアップ

### TPL-EDGE-PII-RETENTION: エッジサーバの PII 蓄積（保持期間ポリシー不在）

- **観点**: A2
- **デフォルト重大度**: High
- **典型根拠**: `/var/lib/<app>/uploads`、`/opt/<app>/data` 等に顧客 PII（署名 PDF、撮影画像、QR コード等）が削除ポリシーなしで蓄積
- **典型推奨対応**: 保持期間ポリシー策定、自動削除機構導入、法令要件確認（各州・国のデータ保持法制）
- **昇格条件**: regulated 環境（PCI DSS / HIPAA / GDPR）→ Critical

### TPL-TZ-INCONSISTENT: タイムゾーン不統一（複数サーバ運用）

- **観点**: A9
- **デフォルト重大度**: Low
- **典型根拠**: `timedatectl` の `Time zone` がプロジェクト標準と一致しない（複数拠点で混在）
- **典型推奨対応**: TZ 標準化（または意図的に拠点別 TZ なら明文化）、ログ集約時の TZ 変換規則整備

---

## 4. 拡充 TODO（v1 完成までに追加すべき TPL）

- TPL-OS-WEAK-CONFIG: SSH の弱設定（X11Forwarding=yes、AllowUsers 未設定 等）
- TPL-LOG-JOURNALD-UNLIMITED: journald 容量無制限
- TPL-NET-FW-ABSENT: ホスト FW 不在（firewalld/ufw/iptables）
- TPL-NET-BIND-WILDCARD: アプリの 0.0.0.0 バインド
- TPL-NET-SECURITY-HEADERS-MISSING: セキュリティヘッダ欠如（HSTS/CSP/X-Frame-Options 等）
- TPL-NET-RATE-LIMIT-MISSING: rate limit 設定不在
- TPL-NET-WAF-INACTIVE: WAF 動作確認できず
- TPL-SVC-FHS-VIOLATION: アプリ配置が FHS 違反（/usr/share 配下等）
- TPL-SVC-COLOCATED: 公開サーバと内部サーバの用途同居
- TPL-CRED-WEAK-SESSION-SECRET: セッションシークレットが短い/辞書語近接
- TPL-COOKIE-INSECURE: Cookie 属性欠如（secure/httpOnly/sameSite）
- TPL-MON-NO-ALERT: 監視はあるがアラート閾値未設定
- TPL-NTP-INACTIVE: NTP デーモン不稼働
- TPL-TZ-INCONSISTENT: 複数サーバ間で TZ 不統一
- TPL-EDGE-PII-RETENTION: エッジサーバの PII 蓄積（保持期間ポリシー不在）
- TPL-VPN-CRED-PLAINTEXT: VPN 認証情報の平文保存（CRED-PLAINTEXT の派生）
- TPL-VPN-PROCESS-DUP: VPN プロセス重複稼働

---

## 5. プロジェクト固有 TPL の追加方法

プロジェクト依存の Finding パターンを追加する場合:

1. 本ファイルとは別に `references/finding_taxonomy_<project>.md` を作成
2. 命名規則は `TPL-<PROJECT>-<CATEGORY>-<NAME>`
3. 本汎用辞書を補完する形で運用（汎用版を上書きしない）
4. プロジェクト終了時に汎用版に取り込めるパターンがあれば PR で提案
