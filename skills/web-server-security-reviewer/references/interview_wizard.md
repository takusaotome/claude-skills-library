# Interview Wizard — target_profile.yaml 対話収集仕様

`target_profile.yaml` が未提供のとき、Claude Code エージェントは本仕様に従って AskUserQuestion を順番に発行し、回答を `wizard_answers.json` に集約する。最後に `scripts/build_target_profile.py` を実行して target_profile.yaml を生成する。

**設計原則:**

- 対話で聞くのは **判断・本人確認・承認・スコープ確定** に必要な情報のみ
- 既定値・派生値・空配列は `build_target_profile.py` 側で補完
- Stage 1 の hard fail (windows / iis) を最優先で実行し、検出時は以降の質問を打ち切る
- 配列入力は AskUserQuestion で頑張らず、カンマ区切り自由記述 → script で正規化
- ツール呼び出し原稿ではなく **宣言的設問仕様** として記述（API 差異に強い）

---

## 1. ステージ一覧

| Stage | 目的 | 設問数 | call 数 | 条件 |
|---|---|---|---|---|
| 1 | Mode 選択 / hard-fail gate | 4 (全 choice) | 1 | 常時 |
| 1.5 | custom role 文字列入力 | 1 (free-text) | 1 | `Stage 1 で role=custom` |
| 2 | 識別子 (target 上位) | 4 (free-text 中心) | 1 | Stage 1 で hard fail しなかった場合 |
| 3 | host_fingerprint (本人確認) | 4 (free-text 3 + choice 1) | 1 | 〃 |
| 4 | SSH 承認 | 4 (free-text 中心) | 1 | `connection_mode == ssh_direct` |
| 5 | evidence (採取・provenance) | **5** (free-text 中心) | **2** (4+1 必須分割) | 常時 |
| 6 | scope / incident | 4 (free-text + choice 混在) | 1 | 常時 |
| 7 | retention | 4 (free-text + choice 混在) | 1 | 常時 |

> **Stage 5 は 5 fields あるため、AskUserQuestion の 1 call ≤ 4 question 制約により必ず 2 call に分割する**。推奨分割: call A = `collected_by` / `collection_completed_at` / `evidence_dir` / `raw_evidence_store`、call B = `authenticity_level` (choice-only 単問)。

### 1.1 AskUserQuestion 呼び出し回数

AskUserQuestion API の制約: 1 call あたり **最大 4 questions**、各 question は **2-4 options 必須**（自由記述は自動付与される "Other" 経由）。

stage 内の field を実際の AskUserQuestion 呼び出しに分解する規則:

- **choice-only batch**: stage 内の全 field が choices を持つ場合 → 1 stage = 1 AskUserQuestion call（最大 4 fields）
- **free-text singleton**: 自由記述 field は **placeholder choices 2-3 個 + "Other" 経由**で 1 question として発行。同じ stage 内に他の choice-only field があれば同じ call にバッチ可
- **conditional skip**: condition が偽の場合は call 自体を発行しない (Stage 1.5, Stage 4 等)

**実呼び出し回数の目安:** (Stage 5 は必ず 2 call にカウント)

| シナリオ | call 数 | 内訳 |
|---|---|---|
| ssh_direct + role=preset | **8 calls** | Stage 1, 2, 3, 4, **5a, 5b**, 6, 7 |
| ssh_direct + role=custom | **9 calls** | Stage 1, 1.5, 2, 3, 4, **5a, 5b**, 6, 7 |
| offline_evidence + role=preset | **7 calls** | Stage 4 を除く + Stage 5 は 2 call |
| offline_evidence + role=custom | **8 calls** | + Stage 1.5 |
| Stage 1 で hard fail | 1 call のみ | 以降中断 |

各 stage の実呼び出し設計（call 内に何を batch するか）はエージェントの裁量。free-text 比率が高い stage では複数 call に分けても可（合計の質問内容が本仕様と一致していれば良い）。

---

## 2. 設問定義 (declarative)

各 stage は以下のスキーマで記述する:

```yaml
stage_id: <int>
title: <str>
condition: <str|null>          # null なら常時実行。例: "answers.connection_mode == 'ssh_direct'"
on_hard_fail: stop_wizard      # Stage 1 のみ
fields:
  - field: <dotted.path>       # answers JSON 内の格納先
    prompt: <str>              # 設問文
    header: <str (≤12 chars)>  # AskUserQuestion の header
    choices: [<str>, ...]      # 省略時は自由記述
    multiSelect: <bool>        # default false
    required: <bool>           # default true
    normalize_to: <str|null>   # csv_list | bool | int | iso8601 | null
    hint: <str|null>           # 入力例や注意書き
```

---

### Stage 1 — Mode (hard-fail gate)

```yaml
stage_id: 1
title: 対象サーバの種別と接続モード
condition: null
on_hard_fail: stop_wizard
fields:
  - field: target.os_family
    prompt: 対象サーバの OS ファミリは？
    header: OS family
    choices: [rhel, debian, windows]
    hint: "windows は v1 hard fail（レビュー継続不可）"

  - field: target.web_server
    prompt: 対象の Web サーバは？
    header: Web server
    choices: [nginx, apache, none, iis]
    hint: "iis は v1 hard fail（レビュー継続不可）"

  - field: connection_mode
    prompt: 接続モードを選択
    header: Conn mode
    choices: [ssh_direct, offline_evidence]

  - field: target.role
    prompt: 対象サーバの役割は？
    header: Role
    choices: [public_facing, internal, edge, custom]
    hint: "custom 選択時は Stage 1.5 で実際の役割名文字列を入力"
```

**hard-fail 早期離脱:** `target.os_family == "windows"` または `target.web_server == "iis"` を検知した時点で、エージェントは以降の AskUserQuestion を発行せず、unsupported_matrix.md の文面に沿って中断メッセージを返す。

---

### Stage 1.5 — custom role 文字列入力（条件付き）

```yaml
stage_id: 1.5
title: custom role の実際の役割名
condition: "answers.target.role == 'custom'"
fields:
  - field: target.custom_role
    prompt: 実際の役割名を入力（例 api_gateway / batch_worker / control_plane）
    header: Custom role
    hint: "Stage 1 で 'custom' を選んだ場合のみ。'custom' 自身は再入力不可。"
```

**バリデーション:** script 側で `role=='custom' かつ custom_role 未指定` → WizardError。`custom_role` の値が空文字や再度 `'custom'` でも WizardError。指定された custom_role 文字列が `target.role` に substitute される。`scope.role_extensions` は preset テーブルにヒットしないため自動推定は **空配列**。custom role に紐づく拡張 yaml がある場合は wizard_answers.json の `scope.role_extensions` に明示すること。

---

### Stage 2 — 識別子

```yaml
stage_id: 2
title: 対象サーバの識別情報
condition: null
fields:
  - field: target.hostname
    prompt: 対象 hostname を入力
    header: Hostname
    hint: "例: web01"

  - field: target.fqdn
    prompt: 公開 FQDN（内部用途で空可）
    header: FQDN
    required: false

  - field: target.os_version
    prompt: OS バージョン
    header: OS version
    hint: "例: Rocky Linux 9.5, Ubuntu 22.04"

  - field: review_id
    prompt: review_id を入力（フォーマット PROJECT-REVIEW-YYYY-MMDD-NN）
    header: Review ID
    hint: "例: ACME-REVIEW-2026-0501-01"
```

**自動補完:** `target.app_runtime` は質問しない。未指定なら `"none"` を自動補完。

---

### Stage 3 — host_fingerprint（本人確認）

```yaml
stage_id: 3
title: 対象サーバの fingerprint（本人確認用）
condition: null
fields:
  - field: target.host_fingerprint.machine_id_sha256
    prompt: /etc/machine-id の SHA256 ハッシュ（lowercase hex 64 文字）
    header: machine-id
    hint: "shasum -a 256 /etc/machine-id の出力。raw machine-id は不可。"

  - field: target.host_fingerprint.primary_ipv4
    prompt: 内部 primary IPv4 アドレス
    header: IPv4

  - field: target.host_fingerprint.ssh_host_key_sha256
    prompt: SSH ホスト鍵の SHA256 fingerprint
    header: SSH key

  - field: target.host_fingerprint.timezone
    prompt: タイムゾーン
    header: Timezone
    choices: [America/Los_Angeles, America/New_York, Asia/Tokyo, UTC]
    hint: "他のタイムゾーンが必要なら自由記述で入力可"
```

**バリデーション:** `machine_id_sha256` は script 側で `^[a-f0-9]{64}$` を強制。raw machine-id（典型的に 32 文字）が来たら拒否。

---

### Stage 4 — SSH 承認（条件付き）

```yaml
stage_id: 4
title: SSH 接続承認
condition: "answers.connection_mode == 'ssh_direct'"
fields:
  - field: ssh.bastion
    prompt: 踏み台 hostname（直接接続なら "none" / "null" / "なし" / 空欄のいずれか）
    header: Bastion
    required: false
    normalize_to: optional_null
    hint: "script 側で空文字 / 'none' / 'null' / 'なし' / 'n/a' は null に正規化"

  - field: ssh.user
    prompt: 接続用ユーザ（read-only 推奨）
    header: SSH user

  - field: ssh.approved_by
    prompt: 立会者氏名
    header: Witness

  - field: ssh.approved_at
    prompt: 承認日時（ISO8601）
    header: Approved at
    normalize_to: iso8601
    hint: "例: 2026-04-30T21:00:00-07:00"
```

**スキップ条件:** `connection_mode == offline_evidence` の場合は Stage 4 を完全スキップ。`ssh` ブロックは出力 YAML から null として残る。

---

### Stage 5 — evidence

```yaml
stage_id: 5
title: 証跡採取と provenance
condition: null
fields:
  - field: evidence.collected_by
    prompt: 採取者氏名
    header: Collector
    hint: "ssh.approved_by と同一なら source_confidence=high の条件"

  - field: evidence.collection_completed_at
    prompt: 証跡採取完了日時（ISO8601、必須）
    header: Completed
    normalize_to: iso8601
    hint: "delete_after 算出に使用。collection_started_at は未入力なら同値で補完。"

  - field: evidence.evidence_dir
    prompt: マスク済み証跡ディレクトリ path
    header: Evidence dir
    hint: "例: ./review_acme/evidence/"

  - field: evidence.raw_evidence_store
    prompt: 生ログ保管先（別ストレージ）
    header: Raw store
    hint: "例: s3://acme-security/raw/<review_id>/ または社内セキュア共有 path"

  - field: evidence.authenticity_level
    prompt: 真正性レベル
    header: Authnty
    choices: [attestation_only, external_channel, gpg_signed, ssh_signed]
```

**自動派生:**
- `source_confidence` / `source_confidence_reason` は connection_mode + authenticity_level + collected_by/approved_by 一致から script が導出（高信頼性で再現性あり）。明示的に上書きしたい場合のみ wizard_answers.json に直接書き足す
- `masking_at_collection` は質問せず `true` 既定
- `collection_started_at` は未指定なら `collection_completed_at` と同値

---

### Stage 6 — scope / incident

```yaml
stage_id: 6
title: スコープと進行中インシデント
condition: null
fields:
  - field: scope.out_of_scope
    prompt: 範囲外項目（カンマ区切り、空可）
    header: Out of scope
    normalize_to: csv_list
    required: false
    hint: "例: Phase 2 コードレビュー, ペネトレーションテスト"

  - field: incident_context.active_incident
    prompt: 現在インシデント発生中か？
    header: Active inc
    choices: [false, true]
    normalize_to: bool

  - field: incident_context.incident_id
    prompt: incident_id（active_incident=true 時のみ必須）
    header: Inc ID
    required: false

  - field: incident_context.incident_summary
    prompt: incident 概要（active_incident=true 時のみ必須）
    header: Inc summary
    required: false
```

**自動補完:**
- `scope.axes_in_scope` は既定で `[A1..A9]` 全部。サブセット運用が必要なら wizard_answers.json に直接書き足す
- `scope.role_extensions` は `target.role` から推定 (`public_facing` → `[generic_public_facing]` 等)。custom role の場合は推定が空になるので wizard_answers.json に直接書き足す

---

### Stage 7 — retention

```yaml
stage_id: 7
title: 生ログ保持と承認体制
condition: null
fields:
  - field: retention.raw_retention_days
    prompt: 生ログ保持日数
    header: Retention
    choices: [30, 60, 90, 180]
    normalize_to: int

  - field: retention.owner
    prompt: retention 責任者氏名
    header: Owner

  - field: retention.access_approvers
    prompt: アクセス承認者リスト（カンマ区切り、最低 1 名）
    header: Approvers
    normalize_to: csv_list

  - field: retention.rotation_dependencies
    prompt: ローテーション依存（カンマ区切り、空可）
    header: Rotation
    normalize_to: csv_list
    required: false
    hint: "例: VPN 認証情報ローテーション完了確認, DB 認証情報ローテーション完了確認"
```

**自動派生:**
- `retention.delete_after` は `collection_completed_at + raw_retention_days` で script が算出
- `retention.early_deletion_conditions` は省略時に既定値（`シークレットローテーション完了 かつ レビュー成果物確定後`）を補完

---

## 3. 集約 → ファイル化フロー

1. 各 stage の AskUserQuestion 結果を `answers` dict にマージ（`field` の dotted-path に沿って）
2. Stage 4 を実行した場合のみ `evidence.approved_by` に `ssh.approved_by` を自動コピー（source_confidence 派生のため）
3. `answers` を `wizard_answers.json` に書き出し
4. 以下を実行:

   ```bash
   python3 scripts/build_target_profile.py \
       --answers wizard_answers.json \
       --output <evidence_dir>/target_profile.yaml
   ```

5. exit code:
   - `0`: 正常生成 → Phase 1-a へ
   - `1`: 入力検証エラー → エージェントが該当 stage を再質問
   - `2`: I/O エラー
   - `3`: hard fail → unsupported メッセージで中断

---

## 4. CLI / フィールド名の固定

`build_target_profile.py` の引数名・フィールド名は本ファイルと **完全一致** で固定する。リネームする場合は本ファイル / SKILL.md / `scripts/tests/test_build_target_profile.py` を同時に更新する。

| 仕様 | 値 |
|---|---|
| script | `scripts/build_target_profile.py` |
| 必須引数 | `--output` / `-o` |
| answers 引数 | `--answers` / `-a` または positional 1 個 |
| answers JSON top-level keys | `review_id`, `target`, `connection_mode`, `ssh`, `evidence`, `scope`, `incident_context`, `retention`, `exceptional_approvals`（任意）|

未実装 CLI 名や架空オプションを SKILL.md に記載してはならない（他スキルで起きた回帰の再発防止）。

---

## 5. テスト

`scripts/tests/test_build_target_profile.py` で以下を担保:

- hard-fail gate (windows / iis)
- machine_id_sha256 の raw 値拒否
- collection_completed_at 必須 / collection_started_at 同値補完
- delete_after 算出
- enum 検証
- defaults: axes_in_scope / role_extensions 推定 / masking_at_collection
- conditional required: ssh / incident
- CSV 正規化
- source_confidence 派生
- CLI 経路（positional / --answers）

スモークテストは `assets/wizard_answers_example.json` を入力に build_target_profile.py を回し、生成された YAML が `references/input_contract.md` の必須キー一式を含むことを確認する。
