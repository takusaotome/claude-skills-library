# Verification Summary — v1 リリース判定

`web-server-security-reviewer` スキル v1 minimum viable の検証 A〜G 結果。

- **実施日時**: 2026-05-01T07:56:10Z
- **対象スキル root**: `~/.claude/skills/web-server-security-reviewer/`
- **総合**: 自動検証 17/17 PASS、分析検証 2/2 PASS、文書のみ 3 件確認済（合計 22 項目、うち再実行可能 19 項目）

---

## 1. 検証カテゴリ

3 種類に分類:

| カテゴリ | 検証手段 | 再実行可能性 |
|---|---|---|
| **自動検証**（17 項目）| `scripts/verify_skill.py` | ✓ exit code で機械判定 |
| **分析検証**（2 項目）| `scripts/verification_run.py` | ✓ keyword 辞書品質に依存（決定論的）|
| **文書のみの検証**（3 項目）| 本ファイル §4 で論証 | ✗ 仮想プロファイル前提のため非自動 |

---

## 2. 自動検証（verify_skill.py、17/17 PASS）

`python3 scripts/verify_skill.py` で実行、exit 0/1 で判定。

| 検証 ID | 内容 | 結果 |
|---|---|---|
| E-1.1 | YAML パース 7/7 | ✓ |
| E-1.2 | schema 必須キー全 25 check 準拠 | ✓ |
| E-2.1 | observation_status ↔ severity_criteria enum 完全一致 | ✓ |
| E-3.1 | forbidden 21 コマンド網羅 | ✓ |
| E-3.2 | SSH redirect 4 ケース明記 | ✓ |
| F.1 | hard fail 条件記載 | ✓ |
| F.2 | windows hard_fail 動作 | ✓ |
| F.3 | iis hard_fail 動作 | ✓ |
| F.4 | rhel/nginx 正常系 | ✓ |
| G.1 | MANIFEST 自己参照断ち明記 | ✓ |
| G.2 | attestation 真正性レベル明記 | ✓ |
| G.3 | 正常時の sha256 一致 | ✓ |
| G.4 | ファイル改変検出 | ✓ |
| G.5 | MANIFEST 改変検出 | ✓ |
| D-γ | Spo-cha 固有名詞混入検査 | ✓ |
| TPL | template_finding_id 全件解決 | ✓ |
| cmd_refs | command_refs 全件解決 | ✓ |

**再実行コマンド**:
```bash
cd ~/.claude/skills/web-server-security-reviewer
python3 scripts/verify_skill.py
echo "exit=$?"  # 0 = 全 PASS / 1 = FAIL あり
```

---

## 3. 分析検証（verification_run.py、2/2 PASS）

既存 3 レポート（`docs/server_review_2026Q2/`）を入力として、keyword 辞書ベースで観点マッピングを実施。辞書品質に依存するため、新概念の Finding 追加時は辞書拡充が必要。

| 検証 ID | 内容 | 結果 | 詳細 |
|---|---|---|---|
| A.1 | HQ Critical/High recall | ✓ 100% | C={H-F1}, H={H-F2,H-F3,H-F5}, mapped 4/4 |
| B.1 | 9 観点マッピング率 ≥90% | ✓ 100% | extracted=86, real=83, mapped=83 |

**再実行コマンド**:
```bash
cd ~/.claude/skills/web-server-security-reviewer
python3 scripts/verification_run.py [path_to_reports_dir]
# デフォルトレポートパス: docs/server_review_2026Q2
echo "exit=$?"
```

### A.1 判定根拠（HQ Finding → 9 観点マッピング）

| Finding | 内容 | 対応 axis | 対応 TPL |
|---|---|---|---|
| H-F1 (Critical) | `/log/spocha_manage/` に 16GB 累積 | A2/A3 | TPL-DISK-HIGH-USAGE / TPL-LOG-ROTATE-MISSING |
| H-F2 (High) | remove_log.sh が cron 不在で無言失敗 | A3 | TPL-LOG-CLEANUP-SILENT-FAIL |
| H-F3 (High) | 稼働 435 日（カーネルパッチ未適用疑い）| A1 | TPL-OS-LONG-UPTIME |
| H-F5 (High) | アプリ配下に DB ダンプ 644 放置 | A6 | TPL-SECRET-WORLD-READABLE |

---

## 4. 文書のみの検証（3 項目、再実行非自動）

仮想プロファイル前提のため `verify_skill.py` / `verification_run.py` では再実行できない。本セクションが結果証跡そのもの。

### 4.1 C: API Gateway 拡張シミュレーション ✓ PASS

新規 role 追加に必要な作業:
1. `references/role_extensions/api_gateway.yaml` を新規作成（`_schema.yaml` 準拠）
2. 関連 cmd_id を `command_reference.yaml` に追加（既存 cmd_id 再利用も可）
3. `target_profile.yaml.scope.role_extensions` に `api_gateway` を追加

**判定**: SKILL.md / 既存 reference / asset の改変不要、YAML 1 ファイル追加のみで完結 → PASS

### 4.2 D-α: 健全 nginx 仮想コーパス ✓ PASS

仮想プロファイル: 全防御層が有効、認証情報 600、SELinux Enforcing、監視あり、TLS 期限十分:

- 9 観点 × 12 check で過剰検出なし
- Critical/High 0-2 件想定（uptime 状況依存）

**判定**: 過剰検出なし → 仕様通り PASS

### 4.3 D-β: Apache 内部仮想コーパス ✓ PASS

`PUBLIC.2.config` / `PUBLIC.3.rate_limit` で nginx と apache を独立 `if` 分岐:

```yaml
# PUBLIC.3.rate_limit より抜粋
if [ -d /etc/nginx ]; then ... fi   # nginx 側
if [ -d /etc/apache2 ] || [ -d /etc/httpd ]; then ... fi   # apache 側
```

**判定**: 片方の Web サーバ環境でも残り側はスキップ、両対応 → PASS

---

## 5. 検証スクリプトの限界

- **D-γ の固有名詞検査**: 3 文字略語（PLM/PCC/PHM/CLM/ATC/WLB）は `\b` 境界で検査するため、別意味の英語（例: PCC = Personal Computer Center）と誤認する可能性あり。汎用化後は別プロジェクトでの allowlist 整備推奨
- **B.1 の観点マッピング**: keyword matching のため、新概念の Finding 追加時は `verification_run.py` の `AXIS_KW_FULL` 辞書拡充が必要
- **G.3-G.5 の MANIFEST 検証**: シミュレーションであり、実プロジェクトでの GPG 署名連動 (`gpg --verify`) は未検証
- **C / D-α / D-β**: 仮想プロファイル前提の文書検証。実プロファイル + 擬似 evidence_dir で再現するには別途整備が必要（v2 候補）
- **擬似攻撃コマンド扱い**: `curl -A 'sqlmap'` 等は実行コマンドからは外れたが、`forbidden_variants` の説明として記載は残る（誤用防止のため意図的）

---

## 6. 既知の限界（v1）

- **チェックリストはスケルトン**: 9 観点 × 12 check + role_extensions × 13 check = 25 check のみ。本番では 40-50 check に拡充推奨
- **command_reference は最小**: 23 cmd_id のみ
- **Windows/IIS は hard fail**（v1 範囲外）
- **scripts は 2 本のみ**: `verify_skill.py`（自動）と `verification_run.py`（分析）。プロンプト主導が原則

---

## 7. ファイル構成（実測）

スキル本体配下: **25 ファイル**

```
~/.claude/skills/web-server-security-reviewer/
├── SKILL.md
├── assets/                              (8 files)
├── references/                          (11 md/yaml + 4 role_extensions = 15 files)
└── scripts/                             (2 files: verify_skill.py + verification_run.py)
```

`~/.claude/commands/web-security-review.md` (1) + `~/.claude/plans/web-giggly-bear.md` (1) を加えて **計 27 ファイル**。

---

## 8. 結論

**v1 minimum viable リリース判定: GO**

- 自動検証 17/17 + 分析検証 2/2 = 19 項目すべて PASS（exit 0）
- 文書のみの検証 3 項目 PASS（仮想プロファイル前提、本ファイル §4 が証跡）
- 参照切れ 0、Spo-cha 残滓 0、schema 不整合 0
- 6 階層 read-only ガード + SSH redirect 4 ケースで安全境界明示
- nginx/apache 両対応の役割固有 check
- 別プロジェクトでも `/web-security-review <target_profile.yaml>` で即起動可能

### 次フェーズ（v2 候補）
- checklist 40-50 check への拡充
- Windows/IIS 本格対応
- 自動 Finding 抽出スクリプト（classify_findings.py）
- 第 2 コーパス（健全 nginx + Apache 内部）の実プロファイル整備で D-α/D-β を自動化
- GPG 署名連動の実装

### 検証の再実行（リリース前/CI/受け入れテスト用）
```bash
cd ~/.claude/skills/web-server-security-reviewer

# 自動検証（17 項目）
python3 scripts/verify_skill.py
test $? -eq 0 || { echo "automated FAIL"; exit 1; }

# 分析検証（2 項目）
python3 scripts/verification_run.py
test $? -eq 0 || { echo "analytical FAIL"; exit 1; }

echo "All automated/analytical PASS (19/19)"
# 文書検証 3 項目は本ファイル §4 を目視確認
```
