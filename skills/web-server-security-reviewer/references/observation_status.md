# Observation Status — 観測ステータス enum

各 Finding に観測ステータスを付与し、断定 / 推測 / 未確認を明示分離する。`unknown_*` 系を Low に格下げしてはならない（自己レビュー必須項目）。

---

## 1. enum 定義

| 値 | 説明 | 重大度判定への影響 |
|---|---|---|
| `confirmed` | コマンド出力で立証済 | 通常判定 |
| `confirmed_with_mitigation_unverified` | 立証済だが既存緩和策の動作未検証 | 降格不可 |
| `likely` | 状況証拠から高蓋然性、追加検証推奨 | 通常判定（根拠欄に「likely」明記）|
| `not_observed` | 確認したが該当なし（健全）| Finding 起票せず、観点別サマリで言及 |
| `not_applicable` | 対象環境では成立しない（例: Linux check on Windows）| Finding 起票せず |
| `unknown_evidence_missing` | 証跡受領モードで証跡が無く未確認 | 重大度判定保留、未確認事項サブセクションへ |
| `blocked_by_permission` | 権限不足で確認失敗 | 重大度判定保留、追加証跡要求 |
| `out_of_scope_phase1` | Phase 2（コードレビュー）対象 | Phase 2 に送る |
| `unsupported_in_v1` | v1 範囲外（Windows/IIS 等）| hard fail で Phase 0 停止 |

---

## 2. 各値の運用

### 2.1 confirmed
コマンド出力をそのまま根拠として記述可能。重大度判定は通常通り。

### 2.2 confirmed_with_mitigation_unverified
立証済だが、既存緩和策（WAF、SG、IP 制限等）の動作確認が未実施。重大度の **降格不可**。緩和策動作確認後に再評価。

例:
```
SELinux 無効化を確認（Severity: High）
ただし AppArmor が代替で有効か未検証 → confirmed_with_mitigation_unverified
緩和策動作確認後、Medium への降格を検討
```

### 2.3 likely
コマンド出力でなく状況証拠（cron 設定、ログパターン、ファイル日付等）から高蓋然性。Finding 根拠欄に「likely」と明記、追加検証推奨を P0/P1 アクションプランに含める。

### 2.4 not_observed
確認したが該当なし（健全）。Finding として起票せず、レポート §4 観点別サマリで言及:

```
A4.5 Web ドキュメントルート設定不備: not_observed
  - nginx -T を確認、location /<sensitive_path>/ ブロックは適切に設定済
  - loopback + Host ヘッダで秘密ファイルへのアクセスを試みたが HTTP 403/404
```

### 2.5 not_applicable
対象環境では成立しない。例: Linux チェックを Windows 対象に適用、nginx 固有チェックを apache 対象に適用。Finding 起票せず、観点別サマリで言及。

### 2.6 unknown_evidence_missing
offline_evidence モードで証跡が含まれない、または ssh_direct で時間切れ等で確認できなかった項目。

**重要**: Low や Observation に格下げしない。レポート §3「未確認事項」サブセクションに集約し、追加証跡要求リストとして提示。

```
## 3.5 未確認事項（追加証跡要求）

| 項目 | check_id | observation_status | 必要証跡 |
|---|---|---|---|
| nginx -T raw 出力 | A4.5 | unknown_evidence_missing | raw_evidence_store/raw_outputs/nginx_T_full.txt |
| sshd -T raw 出力 | A6.1 | unknown_evidence_missing | raw_evidence_store/raw_outputs/sshd_T_full.txt |
```

`active_incident=true` の場合は追加証跡受領まで Phase 1 完了 pause。

### 2.7 blocked_by_permission
コマンド実行は試みたが権限不足で失敗（例: sudo 権限なし）。`unknown_evidence_missing` と同様に未確認事項サブセクションへ、追加権限取得を推奨対応に記載。

### 2.8 out_of_scope_phase1
Phase 2 コードレビューの範囲（依存パッケージ脆弱性スキャン、実装妥当性検査）。Phase 1 では「観測として古い」を注記するに留め、Phase 2 へ送る。

```
TPL-DEPS-OLD: 依存パッケージが 3 年以上未更新
  observation_status: out_of_scope_phase1
  Phase 2 で依存パッケージ脆弱性スキャン（npm audit、pip-audit、bundler-audit 等）実施、重要 CVE 対応
```

### 2.9 unsupported_in_v1
target_profile.yaml の `os_family: windows` または `web_server: iis` を検知した場合のみ。Phase 0 で hard fail、それ以上の Phase に進まない。

---

## 3. severity_criteria.md との cross-reference

`references/severity_criteria.md` §10 と本ファイル §1 の enum 値は完全一致させる。値を増やしたら両ファイルを同時更新。

不整合検出: `references/schema_validation.md` §4 の enum cross-check 手順で確認。

---

## 4. 自己レビューでのチェック項目

`assets/self_review_template.md` で以下を必須チェック:

- [ ] `unknown_evidence_missing` を Low や Observation に格下げしていないか
- [ ] `not_observed` / `not_applicable` を Finding として起票していないか（観点別サマリに言及はするが Finding 表には載せない）
- [ ] `confirmed_with_mitigation_unverified` の Finding を勝手に降格していないか
- [ ] `out_of_scope_phase1` の Finding が Phase 2 引き継ぎリストに含まれているか
- [ ] `unsupported_in_v1` を検知したら hard fail で Phase 0 停止していたか

---

## 5. レポート構造への影響

レポート §3 の構造:

```
## 3. 発見事項 全リスト

### 3.1 Critical（即時対応）
- 各 Finding に observation_status カラム

### 3.2 High（2 週間以内）
### 3.3 Medium（1-2 ヶ月）
### 3.4 Low / Observation
### 3.5 未確認事項（unknown_evidence_missing / blocked_by_permission）
  - 追加証跡要求リスト
### 3.6 Phase 2 引き継ぎ（out_of_scope_phase1）
  - 別フェーズで詳細化
```

`not_observed` / `not_applicable` は §4 観点別サマリでのみ言及、§3 の Finding 表には載せない。
