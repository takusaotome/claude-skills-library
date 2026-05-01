# Report Template — Web Server Security Review

レビューレポート出力雛形。10 章構成。Finding 表は `finding_table_template.md`、アクションプランは `action_plan_template.md`、自己レビューは `self_review_template.md` 参照。

---

```markdown
---
title: <ROLE> セキュリティレビュー結果（Phase 1 / <状態>）
subtitle: <インシデント名 or トリガー>
document_number: <PROJECT>-REVIEW-<YYYY-MMDD>-<NN>
date: <YYYY 年 M 月 D 日>
author: <担当>
confidential: true
---

# <ROLE> セキュリティレビュー結果（Phase 1）

- **実施日**: <YYYY-MM-DD（TZ）>
- **実施者**: <氏名>
- **立会者・承認者**: <氏名>
- **対象サーバ**: <hostname / role / OS / web_server>（具体的な IP・ユーザ名・鍵名は target_profile.yaml 側で正本管理）
- **生セッションログ**: `<raw_evidence_store の path>`（アクセス制御ストレージ、Git 管理外）
- **進捗**: <Phase 1-a〜1-e の実施範囲>
- **ルール遵守状況**: SKILL.md §0 の read-only 原則に <準拠 | 違反あり>、変更系コマンドは <0 | N> 件
- **source_confidence**: <high / medium / low>
- **authenticity_level**: <attestation_only / external_channel / gpg_signed / ssh_signed>

---

## 1. エグゼクティブサマリ

Phase 1 のレビュー完了。**合計 N 件の発見事項**（Critical M1 件、High M2 件、Medium M3 件、Low / Observation M4 件）。

### 特に重大な X クラスタ

#### Cluster A: <最重大事項の見出し>
<1-3 行の要約>

**確認済み事項（断定）:**
- ...

**未検証事項（確度切り分け）:**
- ...

#### Cluster B: <次に重大な事項>
...

#### Cluster C: <次に重大な事項>
...

---

## 2. 重大度別 件数

| 重大度 | 件数 | 備考 |
|--------|-----:|------|
| Critical | M1 | <備考> |
| High | M2 | <備考> |
| Medium | M3 | |
| Low / Observation | M4 | |
| **合計** | **N** | |

**ID 採番ルール**: `<ROLE>-F<3 桁連番>`、欠番再利用なし。統合事項は `_merged_into` で参照、ID は欠番化。

---

## 3. 発見事項 全リスト（重大度別）

### 3.1 Critical（即時対応・24 時間以内・インシデント扱い）

> 最重大 Finding は単独セクションで詳細記述（finding_table_template.md の構造）。

#### <ROLE>-F001: <発見見出し>

（finding_table_template.md の Finding 詳細フォーマットに従う）

### 3.2 High（2 週間以内）

| ID | 発見 | 観測ステータス | Exploitability / Blast Radius / Service Criticality | 推奨対応 |
|----|------|---|---|---|
| <ROLE>-F002 | <発見内容> | confirmed | medium / lateral_internal / business_critical | <推奨対応> |
| ... | | | | |

### 3.3 Medium（1-2 ヶ月）

| ID | 発見 | 観測ステータス | 3 軸スコア | 推奨対応 |
|----|------|---|---|---|
| ... | | | | |

### 3.4 Low / Observation

| ID | 発見 | メモ |
|----|------|------|
| ... | | |

### 3.5 未確認事項（unknown_evidence_missing / blocked_by_permission）

> Low に格下げ禁止。追加証跡要求リスト形式。

| ID | check_id | observation_status | 必要証跡 | 取得依頼先 |
|----|---|---|---|---|
| <ROLE>-F0NN | A4.5 | unknown_evidence_missing | raw_evidence_store/raw_outputs/nginx_T_full.txt | <採取者氏名> |

### 3.6 Phase 2 引き継ぎ（out_of_scope_phase1）

| ID | 発見 | 引き継ぎ理由 |
|----|------|---|
| <ROLE>-F0NN | 依存パッケージ脆弱性スキャン未実施 | Phase 2 で `npm audit` 等を実施 |

---

## 4. 観点（9 軸）別サマリ

### 4.1 A1 OS・カーネル
- 検査結果サマリ
- 関連 Finding: <ROLE>-F001, F005

### 4.2 A2 リソース
- ...

### 4.3 A3 ログ設定
- ...

### 4.4 A4 ネットワーク
- ...

### 4.5 A5 サービス・プロセス
- ...

### 4.6 A6 認証・アクセス制御
- ...

### 4.7 A7 監視
- ...

### 4.8 A8 バックアップ
- ...

### 4.9 A9 証明書・時刻同期
- ...

---

## 5. 役割固有セクション（拡張）

`scope.role_extensions` で指定された役割固有 check の結果。例: `generic_public_facing` の場合、外部到達性検証、WAF 動作、rate limit 等。

---

## 6. 横展開リスク

他サーバで同型 Finding が観測される可能性。target_profile.yaml の `target.role` と類似する他サーバへの展開判断:

| 本サーバ Finding ID | 同型 Finding 想定先 | 確度 | 確認推奨アクション |
|---|---|---|---|
| <ROLE>-F001 | <他サーバ名 / 役割> | likely | <該当サーバの追加レビュー> |

---

## 7. 推奨アクションプラン

`action_plan_template.md` の P0/P1/P2 構造に従う。

### 7.1 P0（24 時間以内、インシデント扱い）

1. **<ROLE>-F001 緊急対応** — <具体策>
   - 担当: <氏名> / 期日: <ISO8601>
   - 完了判定: <検証コマンド + 期待結果>
   - ロールバック: <手順 / 不要なら "対応自体がロールバック相当">

2. **資格情報ローテーション** — <対象スコープ>
   - 担当 / 期日 / 完了判定 / ロールバック

### 7.2 P1（1〜2 週間）

| # | 項目 | 担当 | 期日 | 完了判定 | ロールバック |
|---|---|---|---|---|---|
| 1 | <推奨対応> | <氏名> | <ISO8601> | <基準> | <手順> |

### 7.3 P2（1〜2 ヶ月）

| # | 項目 | 担当 | 期日 | 完了判定 | ロールバック |
|---|---|---|---|---|---|
| 1 | <推奨対応> | <氏名> | <ISO8601> | <基準> | <手順> |

---

## 8. ログ衛生事項

### 8.1 生ログ取り扱い
- 生ログ保管先: `<raw_evidence_store の path>`（Git 管理外、アクセス制御）
- 含まれる機密: <例: `exceptional_sensitive_read` で取得した sudoers/vpnc 設定内容>
- アクセス承認者: <立会者氏名 / シークレットオーナー氏名>

### 8.2 マスキング適用状況
- `_masking_audit.log` 参照
- 多段階検査（既知パターン → 高エントロピー → allowlist → 立会者承認）通過確認済 / 未実施

### 8.3 保持期間と削除計画
- `target_profile.yaml.retention.delete_after`: <ISO8601>
- 早期削除条件成立可否: <内容>
- ローテーション依存: <VPN / DB / API 認証情報のローテ完了確認>

---

## 9. 次のステップ

- **Phase 1 残タスク**: <あれば>
- **Phase 2 引き継ぎ**: §3.6 参照
- **再レビュー予定日**: <ISO8601 or 条件>
- **横展開レビュー**: <該当サーバ>

---

## 10. 自己レビュー

`self_review_template.md` のチェックリストに従い、レポート完了後に必ず実施した結果を記載。

### 10.1 観点網羅性
- 9 観点それぞれに最低 1 件の Finding または `not_observed` 記録あり: ✓ / 未達（理由: ...）

### 10.2 断定 / 推測の区別
- 全 Finding に observation_status 付与: ✓
- `likely` / `confirmed_with_mitigation_unverified` の根拠記述: ✓

### 10.3 ID 採番整合性
- `<ROLE>-F<3 桁>` 形式遵守: ✓
- 欠番再利用なし: ✓

### 10.4 機密混入チェック（多段階）
- (d-1) 既知パターン grep ヒット: <件数 → allowlist 適用後 0>
- (d-2) 高エントロピー検出ヒット: <件数 → allowlist 適用後 0>
- (d-3) allowlist FP 除外完了: ✓
- (d-4) 立会者署名 (`secret_scan_attestation.txt`): ✓

### 10.5 観測ステータス紛れ込み
- `unknown_evidence_missing` を Low に格下げしていない: ✓
- `not_observed` / `not_applicable` を Finding 表に載せていない: ✓

### 10.6 過学習チェック
- 他プロジェクトの固有名詞混入なし（grep でゼロ確認）: ✓

### 10.7 改善提案
<次回レビューでの改善点>

---

## 付録 A: 検証コマンドログサマリ
- `command_log.jsonl` の件数: N 件
- conditional_sensitive 実行: M 件
- exceptional_sensitive_read 実行: K 件（二重承認取得済）
- forbidden 違反: 0 件

## 付録 B: 整合性検証結果
- MANIFEST.txt sha256: <一致 / 不一致>
- manifest_attestation.txt 検証: <PASS / FAIL>
- 認証チャネル: <authenticity_level>
```
