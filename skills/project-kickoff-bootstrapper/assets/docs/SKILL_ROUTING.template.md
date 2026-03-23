# SKILL_ROUTING

## 1. Purpose

この文書は、プロジェクト内で AI エージェントが「どのタイミングで」「どのスキルを」「何のために」使うかを定義する。

## 2. Operating Rule

- 低リスクの小修正を除き、作業開始時に **Primary Skill** を1つ選ぶ。
- 高リスク変更では **Primary Skill + Secondary Skill** を選ぶ。
- スキルが未導入なら、同等の手順を手動で実施し、その不足を報告する。
- 完了判定は `QUALITY_GATES.md` を優先する。

## 3. Phase-Based Routing

| Phase | Situation / Trigger | Primary Skill | Secondary Skill | Expected Output | Exit Condition |
|---|---|---|---|---|---|
| Discovery | 要件が曖昧 / スコープが広い / 関係者調整が必要 | `project-manager` | `project-plan-creator` | 目的・範囲・WBS・リスク | 実装対象と成功条件が明確 |
| Kickoff | 完了条件が曖昧 / 品質ゲートが未定義 | `completion-quality-gate-designer` | `project-completeness-scorer` | `QUALITY_GATES.md` | Ready / Done / Release の定義が固定 |
| Design | 既存コード再利用だが挙動が怪しい / 契約が不明 | `hidden-contract-investigator` | `design-implementation-reviewer` | `HIDDEN_CONTRACT_REGISTER.md` 更新 | 実契約が確認済み |
| Design | 認可、SQL、ファイルI/O、外部連携、危険パターンを含む | `safe-by-default-architect` | `critical-code-reviewer` | 安全側の標準案 / 禁止パターン | 危険な実装を避ける標準が決まった |
| Design / Implementation | 2モジュール以上に影響 / 類似フローが複数 / コピペ懸念 | `cross-module-consistency-auditor` | `project-manager` | `CROSS_MODULE_CONSISTENCY_MATRIX.md` 更新 | 影響範囲と更新漏れが見える |
| Implementation | テスト先行で進めたい / 失敗条件から固めたい | `tdd-developer` | `production-parity-test-designer` | テスト計画 / テスト実装 | 主要失敗ケースがテスト化 |
| Verification | 本番との差分が不安 / DB方言差 / 依存差 / packaging差 | `production-parity-test-designer` | `migration-validation-explorer` | `TEST_STRATEGY.md` 更新 | parity テスト観点が定義済み |
| Pre-merge | 批判的レビューが必要 / バグを積極的に探したい | `critical-code-reviewer` | `design-implementation-reviewer` | レビュー指摘一覧 | 高優先度指摘の扱いが確定 |
| Release | リリース可否を判断したい / 未解決リスクがある | `project-completeness-scorer` | `completion-quality-gate-designer` | リリース判定メモ | 必須ゲート充足 or 例外承認 |
| Post-incident | 不具合が出た / 傾向を見たい | `incident-rca-specialist` | `qa-bug-analyzer` | RCA / 再発防止策 | 真因と対策が整理済み |

## 4. Signal-Based Routing

### Use `hidden-contract-investigator` when:
- 名前から挙動を推測して使いそう
- 共通関数・共通サービスを流用する
- 戻り値型、エラー挙動、副作用が不明
- テストでモックされていて実実装が見えていない

### Use `safe-by-default-architect` when:
- 認可・権限・機微データを触る
- 生SQLや直書きファイル操作を入れたくなる
- 危険だが手軽な実装と、安全だがやや手間な実装が並んでいる
- 今後似た実装が増える見込みがある

### Use `cross-module-consistency-auditor` when:
- 同じ仕様が複数画面 / 複数バッチ / 複数APIにまたがる
- 集計ルールや判定ルールが複数箇所にある
- 変更漏れが起こりやすい構造になっている

### Use `production-parity-test-designer` when:
- 本番でしか使わない DB / middleware / secret / packaging がある
- staging / CI / local の差がある
- UI の成功と永続化成功がズレる可能性がある
- migration, background job, container build, runtime dependency が絡む

### Use `completion-quality-gate-designer` when:
- 「どこまでできたら完了か」が曖昧
- 証跡が人によって違う
- テストはしたと言うが何をしたか残らない
- 例外運用や waiver の扱いが決まっていない

## 5. Required Outputs by Skill

| Skill | Required Artifact |
|---|---|
| `completion-quality-gate-designer` | `docs/QUALITY_GATES.md` |
| `hidden-contract-investigator` | `docs/HIDDEN_CONTRACT_REGISTER.md` |
| `safe-by-default-architect` | 設計メモ または `.claude/rules/` 更新 |
| `cross-module-consistency-auditor` | `docs/CROSS_MODULE_CONSISTENCY_MATRIX.md` |
| `production-parity-test-designer` | `docs/TEST_STRATEGY.md` |
| `critical-code-reviewer` | レビュー結果メモ |
| `project-completeness-scorer` | 完成度 / リリース判定メモ |

## 6. Escalation Rule

次のいずれかに当てはまる場合、低リスク作業として扱わず、レビュー・テスト深度を上げる。

- 金額、税、丸め、計算ロジック
- 権限、認証、個人情報、秘密情報
- 日付、時刻、タイムゾーン、締め時刻
- DBスキーマ変更、クエリ変更、マイグレーション
- 外部 API、メッセージング、ジョブ、ファイル保存
- 同一仕様が複数箇所に散っている変更
