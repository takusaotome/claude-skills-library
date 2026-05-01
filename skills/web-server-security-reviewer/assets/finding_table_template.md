# Finding Table Template

Critical 単独セクション用の詳細フォーマット、および High/Medium/Low 表形式の構造定義。

---

## 1. Critical 単独セクション フォーマット

```markdown
#### <ROLE>-F<3 桁>: <発見見出し>

**発見内容**:
<1-3 段落で発見の詳細を記述。読み手が事象を理解できる粒度>

**根拠（コマンド出力）**:
- 実行コマンド: `<command_resolved>`
- 出力（マスク済み要約）:
  ```
  <出力の関連部分。秘密値は含めない>
  ```
- 出力ファイル: `evidence_dir/<axis>/<file>`
- 実行日時: <ISO8601>
- 立会者承認: <氏名> @ <ISO8601>

**観測ステータス**: confirmed | confirmed_with_mitigation_unverified | likely

**3 軸スコア**:
- Exploitability: <none | low | medium | high>（理由: ...）
- Blast Radius: <self | lateral_internal | cross_service | cross_org>（理由: ...）
- Service Criticality: <non_critical | standard | business_critical | regulated>（理由: ...）

**Severity 判定**:
- 判定: Critical
- 適用条件: <C1 | C2 | C3 | C4>
- 立証内容: <観測ベースの立証 / CVE 紐付け / インシデント紐付け 等>
- 昇降格: <なし | 昇格元: ... | 降格条件未成立>
- Mitigation status: <既存緩和策の動作確認状況>

**リスク**:
- 影響範囲: <技術的影響と業務影響>
- 想定攻撃シナリオ: <攻撃者視点の経路>
- 関連 CVE / インシデント: <あれば>

**推奨対応**:
- P0 / 24 時間以内: <具体策>
- 漏洩前提のローテーション: <対象認証情報の範囲>
- 完了判定: <検証コマンド + 期待結果>
- ロールバック手順: <手順 / 不要なら明記>
```

---

## 2. High / Medium / Low 表形式

### 2.1 High 表

```markdown
| ID | 発見 | 観測ステータス | E / B / S | 推奨対応 |
|----|------|---|---|---|
| <ROLE>-F002 | <発見内容（1 行）> | confirmed | medium / lateral_internal / business_critical | <推奨対応（1 行）> |
```

カラム説明:
- **ID**: `<ROLE>-F<3 桁>`
- **発見**: 1 行に収まる発見内容（詳細は別セクション参照可）
- **観測ステータス**: enum 値（observation_status.md 参照）
- **E / B / S**: 3 軸スコアの省略形（Exploitability / Blast Radius / Service Criticality）
- **推奨対応**: 1 行で要約（詳細はアクションプラン §7 参照）

### 2.2 Medium 表（同上）

### 2.3 Low / Observation 表

```markdown
| ID | 発見 | メモ |
|----|------|------|
| <ROLE>-F0NN | <観測事項> | <検討事項 / 改善提案> |
```

---

## 3. 未確認事項表（§3.5）

```markdown
| ID | check_id | observation_status | 必要証跡 | 取得依頼先 |
|----|---|---|---|---|
| <ROLE>-F0NN | A4.5 | unknown_evidence_missing | raw_evidence_store/raw_outputs/nginx_T_full.txt | <採取者氏名> |
| <ROLE>-F0NN | A6.10 | blocked_by_permission | sudo cat /etc/sudoers.d/* の出力（要二重承認） | <シークレットオーナー氏名> |
```

---

## 4. Phase 2 引き継ぎ表（§3.6）

```markdown
| ID | 発見 | 引き継ぎ理由 | Phase 2 アクション |
|----|------|---|---|
| <ROLE>-F0NN | <観測事項> | out_of_scope_phase1 | <Phase 2 で実施する具体策> |
```

---

## 5. 関連 Finding 参照（横展開時）

```markdown
**関連 Finding**:
- 同型: <ROLE-A>-F042 (別サーバ)
- 親 Finding: <ROLE>-F001 (本 Finding は派生)
- 統合先: `_merged_into: <ROLE>-F003`（本 ID は欠番化）
```

---

## 6. 記述上の規律

- 秘密値の本文を一切含めない（メタデータのみ）
- 確度の異なる情報を混在させない（observation_status で明示）
- 根拠コマンドは `command_resolved` を記載（template ではなく）
- 推奨対応は具体的な検証コマンドを伴う形で記述
- 担当・期日・完了判定・ロールバックを必ずセットで提示（アクションプラン §7）
