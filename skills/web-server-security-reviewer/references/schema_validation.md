# Schema Validation — schema 静的検証手順

YAML ファイル（機械検証対象）と Markdown ファイル（人手レビュー対象）を分離して検証。target_profile.yaml の整合性、enum cross-check、placeholder 解決検証も本ファイルでカバー。

---

## 1. 検証対象ファイル

### 機械検証対象（YAML）
- `references/checklist_9axes.yaml`
- `references/command_reference.yaml`
- `references/role_extensions/_schema.yaml`
- `references/role_extensions/generic_*.yaml`
- `assets/target_profile_template.yaml`
- 実体 `target_profile.yaml`（レビュー実行時）

### 人手レビュー対象（Markdown）
- `SKILL.md`
- `references/severity_criteria.md`
- `references/finding_taxonomy.md`
- `references/guardrails.md`
- `references/secret_masking.md`
- `references/input_contract.md`
- `references/observation_status.md`
- `references/schema_validation.md`（本ファイル）
- `references/unsupported_matrix.md`
- `assets/evidence_directory_layout.md`
- `assets/report_template.md`
- `assets/finding_table_template.md`
- `assets/action_plan_template.md`
- `assets/self_review_template.md`

---

## 2. クロスプラットフォーム sha256 計算

### 2.1 単一ファイル

```bash
# macOS（標準）
shasum -a 256 <file>

# Linux（GNU coreutils 標準）
sha256sum <file>

# Python 3（クロスプラットフォーム、最も移植性高い）
python3 -c "import hashlib, sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest(), sys.argv[1])" <file>
```

### 2.2 MANIFEST.txt 一括検証

```bash
# Python 3（推奨、macOS/Linux 共通）
python3 <<'PY'
import hashlib, pathlib, sys
ok = True
for line in open('MANIFEST.txt'):
    line = line.strip()
    if not line or line.startswith('#'): continue
    parts = line.split(maxsplit=1)
    if len(parts) != 2: continue
    expected_sha, path = parts
    p = path.lstrip('./')
    try:
        actual = hashlib.sha256(open(p,'rb').read()).hexdigest()
        status = 'OK' if actual == expected_sha else 'FAIL'
        if status == 'FAIL': ok = False
        print(f"{status}  {p}")
    except FileNotFoundError:
        print(f"MISS  {p}")
        ok = False
sys.exit(0 if ok else 1)
PY

# macOS（標準ツール）
shasum -a 256 -c MANIFEST.txt

# Linux（GNU coreutils）
sha256sum -c MANIFEST.txt
```

### 2.3 manifest_attestation.txt 検証

```bash
# 1. manifest_attestation.txt から manifest_sha256 を取得
expected=$(grep '^manifest_sha256:' manifest_attestation.txt | awk '{print $2}')

# 2. MANIFEST.txt の実 sha256 を計算
# macOS
actual=$(shasum -a 256 MANIFEST.txt | awk '{print $1}')
# Linux
actual=$(sha256sum MANIFEST.txt | awk '{print $1}')

# 3. 比較
if [ "$expected" = "$actual" ]; then
  echo "OK: MANIFEST.txt integrity verified"
else
  echo "FAIL: MANIFEST.txt has been modified"
  exit 1
fi
```

### 2.4 GPG 署名検証（authenticity_level: gpg_signed 時）

```bash
gpg --verify manifest_attestation.txt.asc manifest_attestation.txt
```

### 2.5 SSH 署名検証（authenticity_level: ssh_signed 時）

```bash
ssh-keygen -Y verify -f allowed_signers -I <signer_id> -n manifest \
  -s manifest_attestation.txt.sig < manifest_attestation.txt
```

---

## 3. YAML schema 検証

### 3.1 構文確認

```bash
# YAML パース確認
python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <file>
```

### 3.2 target_profile.yaml 必須キー検証

```python
import yaml, sys

REQUIRED = {
    "review_id": str,
    "target": {
        "hostname": str,
        "fqdn": (str, type(None)),
        "role": str,
        "os_family": str,
        "os_version": str,
        "web_server": str,
        "app_runtime": str,
        "host_fingerprint": {
            "machine_id": str,
            "primary_ipv4": str,
            "ssh_host_key_sha256": str,
            "timezone": str,
        },
    },
    "connection_mode": str,
    "evidence": {
        "collected_by": str,
        "collection_started_at": str,
        "collection_completed_at": str,
        "evidence_dir": str,
        "raw_evidence_store": str,
        "authenticity_level": str,
        "source_confidence": str,
        "source_confidence_reason": str,
        "masking_at_collection": bool,
    },
    "scope": {
        "axes_in_scope": list,
        "role_extensions": list,
        "out_of_scope": list,
    },
    "incident_context": {
        "active_incident": bool,
    },
    "retention": {
        "raw_retention_days": int,
        "owner": str,
        "delete_after": str,
        "access_approvers": list,
        "rotation_dependencies": list,
        "early_deletion_conditions": list,
    },
}

def validate(d, schema, path=""):
    errors = []
    for key, expected_type in schema.items():
        full_path = f"{path}.{key}" if path else key
        if key not in d:
            errors.append(f"MISSING: {full_path}")
            continue
        if isinstance(expected_type, dict):
            if not isinstance(d[key], dict):
                errors.append(f"TYPE: {full_path} should be dict")
            else:
                errors.extend(validate(d[key], expected_type, full_path))
        elif isinstance(expected_type, tuple):
            if not isinstance(d[key], expected_type):
                errors.append(f"TYPE: {full_path}")
        else:
            if not isinstance(d[key], expected_type):
                errors.append(f"TYPE: {full_path} should be {expected_type.__name__}")
    return errors

d = yaml.safe_load(open(sys.argv[1]))
errors = validate(d, REQUIRED)
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK")
```

### 3.3 enum 値検証

```python
ENUMS = {
    "target.role": ["public_facing", "internal", "edge"],  # custom 許可
    "target.os_family": ["rhel", "debian", "windows"],
    "target.web_server": ["nginx", "apache", "iis", "none"],
    "connection_mode": ["ssh_direct", "offline_evidence"],
    "evidence.authenticity_level": ["attestation_only", "external_channel", "gpg_signed", "ssh_signed"],
    "evidence.source_confidence": ["high", "medium", "low"],
}

# axes_in_scope の各値は ["A1".."A9"] のいずれか
AXES = [f"A{i}" for i in range(1, 10)]
```

---

## 4. enum cross-check（ファイル間整合性）

`observation_status.md` と `severity_criteria.md` で参照される enum 値が完全一致しているかを確認。

```bash
# observation_status.md の enum 値抽出
grep -E '^\| `[a-z_]+` \|' references/observation_status.md \
  | awk -F'`' '{print $2}' \
  | sort -u > /tmp/obs_enum.txt

# severity_criteria.md で使われている observation_status の値抽出
grep -oE '`(confirmed|likely|not_observed|not_applicable|unknown_evidence_missing|blocked_by_permission|out_of_scope_phase1|unsupported_in_v1|confirmed_with_mitigation_unverified)`' \
  references/severity_criteria.md \
  | tr -d '`' \
  | sort -u > /tmp/sev_enum.txt

# 差分確認
diff /tmp/obs_enum.txt /tmp/sev_enum.txt
# 出力なし = OK
```

---

## 5. placeholder 解決検証

`command_log.jsonl` の `command_resolved` に未解決 placeholder が残っていないか確認。

```python
import re, json, sys

def check_resolved(log_path):
    errors = []
    for i, line in enumerate(open(log_path)):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        cmd = entry.get("command_resolved", "")
        leftover = re.findall(r'<[a-z_][a-z0-9_]*>', cmd)
        if leftover:
            errors.append(f"line {i+1}: unresolved placeholder {leftover} in command_resolved")
    return errors

errors = check_resolved(sys.argv[1])
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK")
```

実行前検証として、Phase 1-b でコマンド実行する直前にこのチェックを通す。残った placeholder があれば実行ブロック。

---

## 6. unsupported hard fail 検出

`unsupported_matrix.md` §5 の Python ロジックを Phase 0 で実行し、`hard_fail` なら停止。

---

## 7. Markdown 人手レビューチェックリスト

各 MD ファイルに必須セクションがあることを目視確認:

| ファイル | 必須セクション |
|---|---|
| SKILL.md | §0 絶対安全規律、§1-§10 |
| guardrails.md | 6 階層分類、SSH redirect 4 ケース |
| secret_masking.md | 収集段階ルール、保存前 regex、多段階検査 |
| severity_criteria.md | 3 軸補助、Critical 条件、enum 参照表 |
| observation_status.md | enum 定義、cross-reference |
| input_contract.md | 必須セクション一覧、enum 値リスト |
| unsupported_matrix.md | hard fail 一覧、best_effort 一覧 |

新規ファイル追加時はこの表に追記。
