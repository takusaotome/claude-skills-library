---
name: web-server-security-reviewer
description: |
  Web サーバ（nginx/apache、Linux 中心）の Phase 1 設定セキュリティレビュー。
  target_profile.yaml で対象を確定し、MANIFEST.txt + manifest_attestation.txt で証跡 integrity を検証。
  SSH 直接または証跡受領モードで 9 観点 (OS/リソース/ログ/ネットワーク/サービス/認証/監視/バックアップ/証明書) を
  read-only 走査。6 階層ガード (allowed/conditional/conditional_sensitive/ask-first/exceptional_sensitive_read/forbidden)、
  3 軸補助 (Exploitability/Blast Radius/Service Criticality) の重大度判定、
  observation_status による未確認の独立管理、evidence_dir/raw_evidence_store 分離、自己レビュー必須。
  Windows/IIS は v1 hard fail。
  Use when: Web サーバの設定セキュリティレビュー、Phase 1 監査、nginx/apache 構成監査、
  EOL ランタイム調査、ログローテーション不備調査、ドキュメントルート漏えい調査。
---

# Web Server Security Reviewer

Web サーバ（nginx/apache、Linux）の Phase 1 設定セキュリティレビューを read-only で実施するスキル。

立会者承認のもと、`target_profile.yaml` を入力契約として受け取り、9 観点のチェックリストを走査して、Critical/High/Medium/Low の発見事項レポートを生成する。

---

## §0 絶対的安全規律（最初に必ず読む）

レビュー実施前に、以下 5 件の規律を必ず確認し、対象システムを変更する操作を一切行わない。

### 0.1 6 階層 read-only ガード（詳細は references/guardrails.md）

| 分類 | 例 | 扱い |
|---|---|---|
| **allowed** | `ls`, `stat`, `ps`, `ss`, `systemctl status`, `getenforce`, `df`, `du`（範囲制限）| 包括承認で実行可 |
| **conditional** | `iptables -L`, `find <制限>`, `journalctl <制限>` | 観点・対象を明示し承認後実行 |
| **conditional_sensitive** | `nginx -T`, `systemctl cat`, `sshd -T`, `apachectl -S`, `crontab -l` | 出力後マスク必須、raw 保存、要約のみ evidence_dir 転記 |
| **ask-first** | `tcpdump`, `strace`, `journalctl -f`, 広範囲 grep | 都度承認 |
| **exceptional_sensitive_read** | `sudo cat /etc/sudoers`, `sudo cat <vpn config>`, **`/etc/shadow` は原則実施しない**（やむを得ない場合のみ限定要約 `awk -F: '{print $1, length($2)}'` 等のみ可）| 二重承認 + raw 限定保管 + 要約転記禁止（本文）+ 取得理由記録 |
| **forbidden** | target host 上の `>`/`>>`/`tee`/`sed -i`/`rm`/`mv`/`cp`/`chmod`/`chown`/`systemctl restart`/`crontab -e`/`logrotate -f`/`certbot renew`/`ufw <変更>`/`firewall-cmd <変更>`/`docker compose up/down`/`dnf/apt install`/`kill`/`pkill` | **絶対禁止**。違反時はレビュー中断 |

### 0.2 target host 書込 vs 採取者ローカル書込（SSH redirect 4 ケース）

引用符の位置で remote/local の動作が変わる。**実行前に必ず確認**:

| ケース | コマンド | 動作 | 扱い |
|---|---|---|---|
| ① 引用の外で redirect | `ssh host 'cat /etc/foo' > ./evidence/file` | local（採取者端末）に書込 | **allowed** |
| ② 引用の中で redirect | `ssh host 'cat /etc/foo > /tmp/x'` | target host に書込 | **forbidden** |
| ③ パイプ後 local tee | `ssh host 'cat /etc/foo' \| tee ./evidence/file` | local に書込 | **allowed** |
| ④ 引用の中で tee | `ssh host 'cat /etc/foo \| tee /tmp/x'` | target host に書込 | **forbidden** |

判定: redirect / tee の対象パスが SSH 引用符の **外側** ならローカル書込（allowed）、**内側** なら target 書込（forbidden）。

### 0.3 収集段階マスキング（詳細は references/secret_masking.md）

- **デフォルト禁止**: 秘密ファイル本文の `cat` / `head` / `tail` / `grep` は通常の `conditional` / `allowed` 区分では禁止対象（`.env`、`*config*.json`、`*.key`、SQL dump 等）
- **`/etc/sudoers`、`/etc/vpnc/*` 等**: §0.1 の **exceptional_sensitive_read** で**二重承認のもとでのみ実施可**（raw 限定保管 + 要約転記禁止）
- **`/etc/shadow`**: 原則 Phase 1 では実施しない。やむを得ない場合のみ exceptional_sensitive_read（限定要約 `awk -F: '{print $1, length($2)}'` 等のみ可、本文取得不可）
- 代替手段: `stat`、`ls -l`（パーミッション・サイズのみ）、`jq 'keys'`（キー名のみ）、`getent passwd`（shadow を読まずアカウント一覧）
- 証跡保存前に正規表現マスク自動適用
- Finding 根拠欄に秘密値を一切転記しない（メタデータのみ記述）

### 0.4 立会者承認 + 二重承認（exceptional 時）

- すべての SSH セッション・コマンド実行は立会者承認必須（`target_profile.yaml` の `approved_by` / `approved_at` 必須）
- `exceptional_sensitive_read` 区分は **立会者 + シークレットオーナーの二重承認** が追加で必要
- 承認外コマンドの実行検知時はレビュー中断、エスカレーション

### 0.5 evidence_dir に raw を入れない不変条件

- `evidence_dir/`: 要約・マスク済み出力のみ。Git 共有可、レビュー成果物
- `raw_evidence_store/`: 生ログ・秘密本文を含む証跡のみ。アクセス制御ストレージ、Git 管理外
- 違反検出（evidence_dir に raw 混入）時は **レビュー中断**、`raw_evidence_store` への移送と evidence_dir のサニタイズを実施

---

## §1 適用範囲とトリガー

### 1.1 対象
- 任意 Web サーバ（nginx / apache）× Linux（RHEL 系 / Debian 系）
- 公開・内部・エッジの各役割（`role_extensions/` で拡張）

### 1.2 トリガー
- スラッシュコマンド: `/web-security-review <target_profile.yaml のパス>`
- 自然言語: 「Web サーバのセキュリティレビュー」「Phase 1 設定監査」「nginx 構成監査」等

### 1.3 unsupported hard fail（references/unsupported_matrix.md 参照）
- `os_family: windows`、`web_server: iis` を target_profile で受領した時点で **hard fail**
- 「v1 では未対応。v2 計画に含めるか、別の対象に切り替えるか」を提示し、それ以上の Phase に進まない

### 1.4 非対象
- Phase 2 コードレビュー（依存パッケージ脆弱性スキャン、実装妥当性）
- ペネトレーションテスト（実攻撃）

---

## §2 入力契約と provenance/integrity 検証

### 2.1 入力契約
`target_profile.yaml`（雛形: `assets/target_profile_template.yaml`、仕様: `references/input_contract.md`）

必須セクション:
- `review_id`、`target`（hostname/fqdn/role/os_family/os_version/web_server/host_fingerprint）
- `connection_mode`（ssh_direct | offline_evidence）
- `ssh`（bastion/user/approved_by/approved_at、ssh_direct 時のみ）
- `evidence`（collected_by/collection_*at/evidence_dir/raw_evidence_store/authenticity_level/source_confidence/masking_at_collection）
- `scope`（axes_in_scope/role_extensions/out_of_scope）
- `incident_context`（active_incident/incident_id/incident_summary）
- `retention`（raw_retention_days/owner/delete_after/access_approvers/rotation_dependencies）

### 2.2 整合性検証手順
1. `manifest_attestation.txt` を読み、`manifest_sha256` を取得
2. `shasum -a 256 MANIFEST.txt`（macOS）または `sha256sum MANIFEST.txt`（Linux）で実 sha256 計算
3. 不一致なら MANIFEST.txt 改変疑い → レビュー中断
4. MANIFEST.txt 内の各ファイル sha256 を逐一検証（`schema_validation.md` の Python 実装参照）
5. `authenticity_level` を確認: `attestation_only` / `external_channel` / `gpg_signed` / `ssh_signed`。高リスク案件で `attestation_only` のみなら立会者にエスカレーション

### 2.3 source_confidence 判定
- `high`: SSH 直接接続 + 立会者承認 + manifest 検証済 + 採取者本人がレビュー実施
- `medium`: SSH 直接接続だが他者採取、または manifest あり offline_evidence
- `low`: manifest なし offline_evidence、採取経路不明、時刻飛び等の異常

`low` の場合、Critical 判定を保留し追加証跡要求リストに記録。

---

## §3 フェーズ分割

### Phase 0: スコープ確定・立会者承認取得
- target_profile.yaml の整合性検証
- unsupported hard fail チェック
- 立会者承認の確認（approved_by/approved_at が ISO8601 で記録されているか）
- evidence_dir / raw_evidence_store のパス確認

### Phase 1-a: 環境プローブ
- OS/Web サーバ/ランタイムの確認
- 9 観点の前提情報収集（uname、/etc/os-release、systemctl list-units、ss -tlnp 等）

### Phase 1-b: 9 観点 checklist 走査
- `references/checklist_9axes.yaml` を順に実行
- 各 check は `references/command_reference.yaml` の許可された実行パターンに従う
- 結果を `evidence_dir/<axis>/` に保存（マスク済み）、raw が必要なら `raw_evidence_store/raw_outputs/` へ

### Phase 1-c: 役割固有 check
- `target_profile.scope.role_extensions` で指定された `references/role_extensions/<role>.yaml` をロード
- 追加 check を実行（schema は `_schema.yaml` に準拠）

### Phase 1-d: Finding 整理・観測ステータス付与・重大度判定
- 各 Finding に observation_status（references/observation_status.md）を付与
- 重大度を 3 軸補助で判定（references/severity_criteria.md）
- Finding ID は `<ROLE>-F<3 桁連番>`、欠番再利用なし

### Phase 1-e: レポート生成・自己レビュー
- `assets/report_template.md` を雛形に出力
- `assets/self_review_template.md` で自己レビュー（観点網羅性、断定/推測、ID 整合性、機密混入、観測ステータス紛れ込み）

---

## §4 接続モードと evidence_dir / raw_evidence_store

### 4.1 ssh_direct モード
- bastion + read-only ユーザ前提
- 立会者承認のもとコマンド実行
- 各実行を `command_log.jsonl` に記録（`command_template` + `command_resolved` 必須、§5 参照）

### 4.2 offline_evidence モード
- 事前収集済みの evidence_dir + raw_evidence_store + MANIFEST.txt + manifest_attestation.txt を受領
- §2.2 の整合性検証 PASS 後に Phase 1-b へ
- conditional_sensitive 系で raw が含まれない場合は `unknown_evidence_missing` 扱い

### 4.3 evidence_dir 構造（assets/evidence_directory_layout.md 参照）

```
<evidence_dir>/
├── target_profile.yaml
├── MANIFEST.txt              # MANIFEST 自身は除外
├── manifest_attestation.txt  # MANIFEST.txt の sha256（自己申告）
├── command_log.jsonl
├── 01_os/   02_resource/   03_logging/   04_network/
├── 05_service/   06_authn_access/   07_monitoring/
├── 08_backup/   09_cert_time/
├── role_<name>/
└── _masking_audit.log
```

`raw_evidence_store/` は別ストレージ（S3 暗号化、社内セキュア共有等）。

---

## §5 9 観点 checklist 走査

### 5.1 観点
- A1 OS・カーネル / A2 リソース / A3 ログ設定 / A4 ネットワーク / A5 サービス・プロセス
- A6 認証・アクセス制御 / A7 監視 / A8 バックアップ / A9 証明書・時刻同期

### 5.2 実行原則
- `command_reference.yaml` に記載された **許可された実行パターン** のみ使用
- 各コマンドの `constraints`（`timeout_sec`、`maxdepth`、`max_output_lines`、`max_output_bytes`、`time_window`、`ionice`、`nice`）を遵守
- find 系の `-name` OR は必ず `\( ... \)` で括弧付き
- curl `-k` は外部到達性・HTTP status・size 確認用途のみ。証明書品質評価は `openssl s_client` で別途

### 5.3 placeholder 解決ルール
`command_reference.yaml` の `command` フィールドに含まれる `<...>` 形式の placeholder は、実行前に必ず target_profile から解決:

- `<fqdn>` → `target.fqdn`
- `<role>` → `target.role`
- `<os_family>` → `target.os_family`
- `<path>` → コンテキスト依存（args.target_path 等）

`command_log.jsonl` の各行に **`command_template`（解決前）** と **`command_resolved`（解決後）** を必須記録。実行前に未解決 `<...>` が残っていないか正規表現で検証し、残れば実行ブロック（`schema_validation.md` 参照）。

### 5.4 conditional_sensitive 実行手順
1. 立会者に「出力に秘密値が含まれる可能性あり」を通知し承認取得
2. 出力本体は raw_evidence_store にのみ保存
3. `secret_masking.md` の正規表現でマスク後、要約を evidence_dir に転記
4. Finding 根拠欄には「`nginx -T` 出力で確認、本文は raw_evidence_store/<path> 参照」のように記述
5. offline_evidence で raw が提供されない場合は `unknown_evidence_missing` 扱い、追加証跡要求リストへ。`active_incident=true` なら追加受領まで Phase 1 完了 pause

---

## §6 重大度判定（references/severity_criteria.md）

### 6.1 3 軸補助スコア
各 Finding に以下 3 軸を併記:
- **Exploitability**: none / low / medium / high
- **Blast Radius**: self / lateral_internal / cross_service / cross_org
- **Service Criticality**: non_critical / standard / business_critical / regulated

### 6.2 Critical 必須条件（OR、いずれか成立で Critical）
- C1 機密外部到達（Exploitability=high + 機密本文取得可能）
- C2 サービス影響迫り（business_critical 以上 + ディスク逼迫 / 急上昇 / 過去 30 日同種インシデント）
- C3 root RCE 経路（CVE 紐付け or インシデント紐付け or 外部到達+認証バイパス+権限昇格の 3 点立証）
- C4 認証情報漏洩前提（外部到達経路あり、または既知の漏洩兆候）

### 6.3 昇格・降格
- 昇格: Service Criticality 上昇、過去 30 日同種障害発生、複合発生
- 降格: 既存緩和策の **動作確認済** で High → Medium。動作未確認なら降格不可（observation_status: confirmed_with_mitigation_unverified）

### 6.4 判定根拠記述
各 Finding に「Severity / Exploitability / Blast Radius / Service Criticality / Conditions evaluated / Mitigation status」の構造化記述を必須。

---

## §7 レポート生成

`assets/report_template.md` の 10 章構成に従う:

1. エグゼクティブサマリ（Cluster A/B/C 形式の重大事項要約）
2. 重大度別 件数表
3. 発見事項 全リスト（Critical 単独セクション + High/Medium/Low 表 + **未確認事項サブセクション**）
4. 観点（9 軸）別サマリ
5. 役割固有セクション
6. 横展開リスク
7. 推奨アクションプラン（P0/P1/P2、各項目に担当・期日・完了判定・ロールバック）
8. ログ衛生事項
9. 次のステップ
10. 自己レビュー

各 Finding は `assets/finding_table_template.md` に従い、観測ステータスと 3 軸スコアカラムを含む。

---

## §8 自己レビュー（必須）

`assets/self_review_template.md` に従い、レポート完了後に必ず以下をチェック:

- 9 観点の網羅性（各観点に最低 1 件の Finding または `not_observed` 記録）
- 断定 / 高蓋然性 / 有力候補 / 未確定の区別（observation_status 参照）
- ID 採番整合性（欠番再利用なし、`<ROLE>-F<3 桁>` 形式）
- 機密混入の多段階チェック（既知パターン → 高エントロピー → allowlist FP 除外 → 立会者署名）
- 観測ステータス紛れ込みチェック（`unknown_evidence_missing` を Low に格下げしていないか）
- 過学習チェック（他プロジェクトの固有名詞混入ゼロ）

---

## §9 拡張ポイント

### 9.1 役割追加手順
1. `references/role_extensions/<role_name>.yaml` を新規作成（`_schema.yaml` 準拠）
2. 必須キー: `extension_id`、`description`、`applicable_roles`、`checks`
3. 各 check に `id`（`<ROLE_PREFIX>.<連番>`）、`axis`（A1-A9）、`role_applicability`、`default_severity`、`severity_conditions`、`verification`（rhel/debian）、`expected`、`template_finding_id`、`masking_required`、`sensitivity` を持たせる
4. target_profile.yaml の `scope.role_extensions` に追加
5. SKILL.md §3 Phase 1-c で自動ロード

### 9.2 Finding ID namespace
- 形式: `<ROLE>-F<3 桁連番>`（例: `PUBLIC-F001`、`HQ-F042`）
- ROLE はプロジェクト側で定義（例: `PUBLIC`、`INTERNAL`、`EDGE`、`API_GW`）
- 連番は役割ごとに 001 から、欠番再利用なし
- 統合・吸収時は `_merged_into` フィールドで参照、ID は欠番化
- 横展開時は新規 ID + `related_findings: ["<元 ID>"]`

### 9.3 schema 検証
新規 YAML 追加時は必ず `references/schema_validation.md` の検証コマンドで PASS を確認。MD ファイルは人手レビューチェックリストで担保。

---

## §10 既知の限界とトレードオフ

| 論点 | v1 判断 | v2 で検討 |
|---|---|---|
| OS カバレッジ | RHEL/Debian 系のみ | Windows/IIS、Alpine、SUSE |
| Web サーバ | nginx/apache | Caddy、Traefik、Envoy、IIS |
| Phase | 設定レビュー（Phase 1）のみ | コードレビュー（Phase 2）、ランタイム挙動検査 |
| 自動化 | プロンプト主導、scripts なし | classify_findings.py 検討 |
| 真正性 | self-attestation デフォルト | GPG 署名強制（高リスク案件） |
| 検証コーパス | 既存レビュー由来コーパス + 健全 nginx + Apache 内部 | より多様なプロジェクトコーパス |

read-only 原則を破る変更系コマンドは v1 では一切実行不可。例外（exceptional_sensitive_read）も二重承認 + 限定要約 + raw 限定保管で運用。

---

## 参考

- `references/checklist_9axes.yaml`: 9 観点チェックリスト本体
- `references/command_reference.yaml`: 許可された実行パターン
- `references/severity_criteria.md`: 重大度判定基準
- `references/finding_taxonomy.md`: 汎用 Finding パターン辞書
- `references/guardrails.md`: 6 階層分類詳細
- `references/secret_masking.md`: マスキングルール
- `references/input_contract.md`: target_profile.yaml 仕様
- `references/observation_status.md`: 観測ステータス enum
- `references/schema_validation.md`: schema 検証手順
- `references/unsupported_matrix.md`: hard fail 一覧
- `references/role_extensions/`: 役割固有チェック
- `assets/`: 各種テンプレート
