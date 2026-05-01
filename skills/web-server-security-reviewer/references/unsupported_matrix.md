# Unsupported Matrix — v1 範囲外と hard fail 一覧

target_profile.yaml で受領した時点で hard fail する条件、および best_effort で続行する条件を定義。

---

## 1. v1 hard fail 一覧

target_profile.yaml に以下のいずれかが記述されている場合、Phase 0 で **hard fail**（それ以上の Phase に進まない）。

| 項目 | v1 status | 振る舞い |
|---|---|---|
| `target.os_family: windows` | unsupported_in_v1 | hard fail。target_profile 受領時点で停止 |
| `target.web_server: iis` | unsupported_in_v1 | hard fail |
| 必須キーの欠落 | invalid_input | エラー表示、欠落キー一覧を提示 |
| enum 値の不正 | invalid_input | エラー表示、許可値一覧を提示 |
| ISO8601 形式の不正 | invalid_input | エラー表示、修正サンプル提示 |
| `MANIFEST.txt` ハッシュ不一致 | integrity_failure | レビュー中断、立会者にエスカレーション |
| `manifest_attestation.txt` 不在 | integrity_failure | レビュー中断 |

---

## 2. best_effort（警告のうえ続行）

| 項目 | 扱い |
|---|---|
| `target.os_family: alpine` | 警告表示、RHEL/Debian 系コマンドで代替試行 |
| `target.os_family: suse` | 警告表示、RHEL 系コマンドで代替試行 |
| `target.os_family: arch` | 警告表示、Debian 系コマンドで代替試行 |
| `target.web_server: caddy` | 警告表示、A4 系の固有 check は手動補完 |
| `target.web_server: traefik` | 同上 |
| `target.web_server: envoy` | 同上 |

best_effort で続行した場合、レポート §10 に「best_effort で実施、未対応コマンドあり」を必須記述。

---

## 3. out_of_scope（スキル範囲外）

| 項目 | 推奨 |
|---|---|
| Phase 2 コードレビュー（npm audit、依存パッケージ脆弱性、実装妥当性） | 別フェーズ。Phase 1 では「観測として古い」を注記するに留める |
| ペネトレーションテスト（実攻撃） | 拒否。本スキルは設定レビューに限定 |
| ランタイム挙動検査（fuzzing 等） | Phase 2 範疇 |
| 物理層調査（IPMI、BMC、ハードウェア検査） | 対象外 |
| アプリケーション層検査（OWASP Top 10 動的検査）| Phase 2 / 別ツール（OWASP ZAP 等）|

---

## 4. hard fail 時のメッセージテンプレート

```
[ERROR] target_profile.yaml に v1 で未対応の項目が含まれています。

  os_family: windows  ← v1 では未対応 (Linux RHEL/Debian 系のみ)

選択肢:
  (a) 対象を切り替える
      target.os_family を rhel または debian に変更
  (b) v2 を待つ
      Windows/IIS は v2 で本格対応予定
  (c) 別スキル / ツールを使う
      Windows サーバ向けの専用ツールを検討してください

レビューを停止します。
```

---

## 5. 検出ロジック

`schema_validation.md` の Python 実装で以下を順に検証:

```python
import yaml, sys

UNSUPPORTED_OS = ["windows"]
UNSUPPORTED_WEB = ["iis"]
BEST_EFFORT_OS = ["alpine", "suse", "arch"]
BEST_EFFORT_WEB = ["caddy", "traefik", "envoy"]

def check_unsupported(profile_path):
    d = yaml.safe_load(open(profile_path))
    os_family = d.get("target", {}).get("os_family", "")
    web_server = d.get("target", {}).get("web_server", "")

    if os_family in UNSUPPORTED_OS:
        return ("hard_fail", f"os_family: {os_family} は v1 では未対応")
    if web_server in UNSUPPORTED_WEB:
        return ("hard_fail", f"web_server: {web_server} は v1 では未対応")
    if os_family in BEST_EFFORT_OS:
        return ("best_effort", f"os_family: {os_family} は best_effort で続行")
    if web_server in BEST_EFFORT_WEB:
        return ("best_effort", f"web_server: {web_server} は best_effort で続行")
    return ("ok", None)
```
