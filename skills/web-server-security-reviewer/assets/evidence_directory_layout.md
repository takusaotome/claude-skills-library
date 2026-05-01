# Evidence Directory Layout

`evidence_dir/` と `raw_evidence_store/` は**物理的に分離**された 2 つのストレージ。raw を `evidence_dir/` に書き込んではならない（不変条件、SKILL.md §0.5）。

---

## 1. evidence_dir/（マスク済み・成果物）

レビュー成果物として共有可能。Git 管理可。立会者・関係者に展開する。

```
<evidence_dir>/
├── target_profile.yaml             # 入力契約
├── MANIFEST.txt                    # 各ファイルの sha256 リスト（自身は含まない）
├── manifest_attestation.txt        # MANIFEST.txt の sha256 + 自己申告
├── manifest_attestation.txt.asc    # GPG 署名（authenticity_level: gpg_signed 時）
├── command_log.jsonl               # 実行コマンドログ（command_template + command_resolved）
├── _masking_audit.log              # マスク適用箇所の監査ログ
├── _violation_log.jsonl            # ガード違反検知ログ（あれば）
│
├── 01_os/                          # A1 OS・カーネル
│   ├── os_release.txt
│   ├── uname.txt
│   ├── uptime.txt
│   └── ...
├── 02_resource/                    # A2 リソース
│   ├── df.txt
│   ├── free.txt
│   ├── du_summary.txt
│   └── ...
├── 03_logging/                     # A3 ログ設定
│   ├── journald_conf.txt
│   ├── logrotate_d.txt
│   ├── log_dirs_du.txt
│   └── ...
├── 04_network/                     # A4 ネットワーク
│   ├── listen_ports.txt
│   ├── nginx_T_summary.txt         # nginx -T のマスク後要約
│   ├── tls_protocols.txt
│   └── ...
├── 05_service/                     # A5 サービス・プロセス
│   ├── ps_ef.txt
│   ├── runtime_versions.txt
│   ├── git_directories.txt
│   └── ...
├── 06_authn_access/                # A6 認証・アクセス制御
│   ├── sshd_T_summary.txt          # sshd -T のマスク後要約
│   ├── sudoers_meta.txt            # ファイル存在・権限のみ（本文 raw のみ）
│   ├── selinux_status.txt
│   ├── perms_644_files.txt
│   └── ...
├── 07_monitoring/                  # A7 監視
│   ├── monitoring_agents.txt
│   └── ...
├── 08_backup/                      # A8 バックアップ
│   ├── backup_jobs.txt
│   └── ...
├── 09_cert_time/                   # A9 証明書・時刻同期
│   ├── tls_cert_dates.txt
│   ├── chronyd_status.txt
│   └── ...
└── role_<name>/                    # 役割固有チェック
    └── <files>
```

### 不変条件
- `evidence_dir/` 配下に raw（マスク前の秘密本文）を絶対に書き込まない
- 違反検出時は `_violation_log.jsonl` に記録、レビュー中断、サニタイズ実施

---

## 2. raw_evidence_store/（生ログ専用、別ストレージ）

Git 管理外、アクセス制御ストレージ（S3 暗号化バケット、社内セキュア共有等）。秘密本文を含む生ログのみを置く。

```
<raw_evidence_store>/
├── target_profile.yaml             # evidence_dir と同じものを複製
├── retention.yaml                  # 保持期限・アクセス制御リスト
├── raw_command_log.jsonl           # exceptional / conditional_sensitive 系の raw 出力ログ
└── raw_outputs/
    ├── nginx_T_full.txt            # nginx -T の生出力（マスク前）
    ├── sshd_T_full.txt
    ├── sudoers_full.txt            # sudo cat /etc/sudoers の出力
    ├── vpn_config_full.txt
    └── <その他 conditional_sensitive / exceptional_sensitive_read 出力>
```

### retention.yaml 例

```yaml
review_id: "ACME-REVIEW-2026-0501-01"
raw_retention_days: 90
collection_completed_at: "2026-04-30T22:00:00-07:00"
delete_after: "2026-07-29T22:00:00-07:00"
owner: "<retention 責任者氏名>"
access_approvers:
  - "<立会者氏名>"
  - "<シークレットオーナー氏名>"
rotation_dependencies:
  - "VPN credentials rotation completed"
  - "DB credentials rotation completed"
early_deletion_conditions:
  - "All rotation dependencies completed AND review report finalized"
deletion_log: []
# - { event: "early_deletion_triggered", at: "<ISO8601>", by: "<owner>", reason: "rotation completed" }
```

---

## 3. command_log.jsonl

各実行コマンドを 1 行 1 JSON で記録（evidence_dir 側、マスク済み）。

### Schema

```json
{
  "ts": "2026-04-30T22:05:32-07:00",
  "axis": "A4",
  "check_id": "PUBLIC.1",
  "command_template": "curl -sk -H 'Host: <fqdn>' -o /dev/null -w '%{http_code} %{size_download}' https://localhost/<path>",
  "command_resolved": "curl -sk -H 'Host: example.internal' -o /dev/null -w '%{http_code} %{size_download}' https://localhost/.env",
  "placeholders_resolved_from": {
    "<fqdn>": "target.fqdn",
    "<path>": "args.target_path"
  },
  "exit_code": 0,
  "output_path": "04_network/listen_ports.txt",
  "masked": false,
  "approved_by": "<立会者氏名>",
  "approved_at": "2026-04-30T22:00:00-07:00",
  "constraints_applied": {
    "timeout_sec": 10,
    "max_output_lines": 200,
    "max_output_bytes": 100000
  }
}
```

### 必須フィールド

- `ts`、`axis`、`check_id`
- `command_template`（placeholder 含む元コマンド）
- `command_resolved`（target_profile から解決済みコマンド）
- `placeholders_resolved_from`（解決元の参照）
- `exit_code`、`output_path`
- `masked`（出力にマスク適用したか）
- `approved_by`、`approved_at`

### 検証

実行前に `command_resolved` 内に未解決 placeholder（`<...>` 形式）が残っていないか正規表現で検証。残っていれば実行ブロック。`schema_validation.md` 参照。

---

## 4. raw_command_log.jsonl

raw_evidence_store 側に保存。conditional_sensitive / exceptional_sensitive_read 実行時に raw 出力先を記録。

```json
{
  "ts": "2026-04-30T22:10:15-07:00",
  "axis": "A4",
  "check_id": "A4.5",
  "sensitivity": "conditional_sensitive",
  "command_resolved": "ssh host 'sudo nginx -T'",
  "raw_output_path": "raw_outputs/nginx_T_full.txt",
  "masked_summary_path": "evidence_dir/04_network/nginx_T_summary.txt",
  "exit_code": 0,
  "approved_by_witness": "<立会者氏名>",
  "approved_by_secret_owner": null,
  "approved_at": "2026-04-30T22:00:00-07:00"
}
```

`sensitivity: exceptional_sensitive_read` の場合は `approved_by_secret_owner` も必須。

---

## 5. _masking_audit.log

マスク適用箇所の監査ログ。

```
2026-04-30T22:11:00-07:00  04_network/nginx_T_summary.txt:142  pattern=password_assignment  before_chars=87  after_chars=14
2026-04-30T22:11:01-07:00  04_network/nginx_T_summary.txt:289  pattern=BEGIN_PRIVATE_KEY    before_chars=1827  after_chars=42
```

本文（before）は記録せず、文字数の差分のみ記録。
