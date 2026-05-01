# Input Contract — target_profile.yaml 仕様

レビュー対象を記述する入力契約。`assets/target_profile_template.yaml` を雛形に作成し、すべてのレビュー実行で必須。

---

## 1. ファイル位置と運用

- 雛形: `assets/target_profile_template.yaml`
- 実体: 各レビューごとに作成（例: `~/security_review_logs/<review_id>/target_profile.yaml`）
- 検証: `references/schema_validation.md` の手順で必須キー・enum 値・整合性を確認

---

## 2. 必須セクション

### 2.1 review_id
- フォーマット: `<PROJECT>-REVIEW-<YYYY-MMDD>-<NN>`
- 例: `ACME-REVIEW-2026-0501-01`、`PROJX-REVIEW-2026-0501-03`

### 2.2 target
| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `hostname` | string | ✓ | 対象 hostname |
| `fqdn` | string \| null | ✓ | 公開 FQDN（内部用途で空なら空文字）|
| `role` | enum | ✓ | `public_facing` / `internal` / `edge` / `<custom>` |
| `os_family` | enum | ✓ | `rhel` / `debian` / `windows`（windows は v1 hard fail）|
| `os_version` | string | ✓ | 例: `Rocky Linux 9.5`、`Ubuntu 22.04` |
| `web_server` | enum | ✓ | `nginx` / `apache` / `iis` / `none`（iis は v1 hard fail）|
| `app_runtime` | string | ✓ | 例: `nodejs-v20.10.0`、`python-3.11`、`none` |
| `host_fingerprint` | object | ✓ | 対象同定の証跡（次表）|

#### host_fingerprint
| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `machine_id` | string | ✓ | `/etc/machine-id` のハッシュ（生値は記録しない）|
| `primary_ipv4` | string | ✓ | 内部 IP（公開 IP は別管理）|
| `ssh_host_key_sha256` | string | ✓ | SSH ホスト鍵フィンガープリント |
| `timezone` | string | ✓ | 例: `America/Los_Angeles`、`Asia/Tokyo` |

### 2.3 connection_mode
- enum: `ssh_direct` / `offline_evidence`

### 2.4 ssh（ssh_direct 時のみ必須）
| キー | 型 | 説明 |
|---|---|---|
| `bastion` | string \| null | 踏み台 hostname |
| `user` | string | read-only 推奨ユーザ |
| `approved_by` | string | 立会者氏名 |
| `approved_at` | ISO8601 | 承認日時 |

### 2.5 evidence
| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `collected_by` | string | ✓ | 採取者氏名 |
| `collection_started_at` | ISO8601 | ✓ | 採取開始 |
| `collection_completed_at` | ISO8601 | ✓ | 採取完了 |
| `evidence_dir` | path | ✓ | マスク済み証跡の保管先（採取者ローカル or 共有ストレージ）|
| `raw_evidence_store` | path/URI | ✓ | 生ログ専用、別ストレージ（S3 URI 等）|
| `authenticity_level` | enum | ✓ | `attestation_only` / `external_channel` / `gpg_signed` / `ssh_signed` |
| `source_confidence` | enum | ✓ | `high` / `medium` / `low` |
| `source_confidence_reason` | string | ✓ | 信頼度の根拠 |
| `masking_at_collection` | bool | ✓ | 採取時マスク有無 |

### 2.6 scope
| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `axes_in_scope` | array<string> | ✓ | `["A1","A2",...,"A9"]` |
| `role_extensions` | array<string> | ✓ | 適用する role_extensions ファイル名 |
| `out_of_scope` | array<string> | ✓ | 範囲外と明示する項目 |

### 2.7 incident_context
| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `active_incident` | bool | ✓ | 現在インシデント発生中か |
| `incident_id` | string | | active なら必須 |
| `incident_summary` | string | | active なら必須 |

### 2.8 retention（v5 追加）
| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `raw_retention_days` | int | ✓ | 生ログ保持日数（デフォルト 90）|
| `owner` | string | ✓ | retention 責任者氏名 |
| `delete_after` | ISO8601 | ✓ | `collection_completed_at + raw_retention_days` で算出 |
| `access_approvers` | array<string> | ✓ | アクセス承認者リスト |
| `rotation_dependencies` | array<string> | ✓ | 例: VPN 認証情報ローテ完了確認 |
| `early_deletion_conditions` | array<string> | ✓ | 早期削除条件（ローテ完了等）|

### 2.9 exceptional_approvals（exceptional_sensitive_read 実施時のみ）
| キー | 型 | 説明 |
|---|---|---|
| `command` | string | 実行コマンド |
| `purpose` | string | 取得理由 |
| `approved_by_witness` | string | 立会者承認 |
| `approved_by_secret_owner` | string | シークレットオーナー承認 |
| `approved_at` | ISO8601 | 承認日時 |
| `raw_storage_path` | path | raw 保存先 |

---

## 3. enum 値リスト

| キー | 値 |
|---|---|
| `role` | `public_facing` / `internal` / `edge` / `<custom string>` |
| `os_family` | `rhel` / `debian` / `windows` |
| `web_server` | `nginx` / `apache` / `iis` / `none` |
| `connection_mode` | `ssh_direct` / `offline_evidence` |
| `authenticity_level` | `attestation_only` / `external_channel` / `gpg_signed` / `ssh_signed` |
| `source_confidence` | `high` / `medium` / `low` |
| `axes_in_scope` 各値 | `A1` / `A2` / `A3` / `A4` / `A5` / `A6` / `A7` / `A8` / `A9` |

---

## 4. hard fail 条件

以下のいずれかが target_profile.yaml に記述されている場合、Phase 0 で **hard fail**:

- `os_family: windows`
- `web_server: iis`
- 必須キーの欠落
- enum 値の不正
- ISO8601 形式の不正

詳細は `references/unsupported_matrix.md`、検証手順は `references/schema_validation.md` 参照。

---

## 5. 整合性検証

レビュー開始時に必ず以下を確認:

1. `MANIFEST.txt` 内の各ファイル sha256 が実値と一致
2. `manifest_attestation.txt` の `manifest_sha256` が `MANIFEST.txt` の sha256 と一致
3. `authenticity_level` に応じた追加検証:
   - `attestation_only`: 採取者の自己申告のみ確認
   - `external_channel`: 立会者と別チャネル（暗号化メール等）で hash 照合
   - `gpg_signed`: `gpg --verify manifest_attestation.txt.asc manifest_attestation.txt`
   - `ssh_signed`: `ssh-keygen -Y verify ...`

詳細手順は `references/schema_validation.md` 参照。
