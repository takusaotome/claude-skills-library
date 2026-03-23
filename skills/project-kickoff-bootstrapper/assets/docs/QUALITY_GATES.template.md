# QUALITY_GATES

## 1. Purpose

この文書は、プロジェクトにおける完了判定を「実装完了」「テスト完了」「リリース可能」に分解して定義する。

## 2. Definitions

| Gate | Meaning | Typical Owner |
|---|---|---|
| Ready for Design | 目的・スコープ・制約・依存が最低限明確 | PM / Tech Lead |
| Ready for Implementation | 設計方針・対象範囲・完了条件が明確 | Tech Lead |
| Implementation Complete | コード変更が揃い、意図した実装が完了 | Developer |
| Test Complete | 必要な検証が終わり、結果が記録済み | Developer / QA |
| Release Ready | 残リスクと未解決事項を含めて出荷判断可能 | PM / Tech Lead / QA |

## 3. Gate Criteria

### 3.1 Ready for Design
- 目的、対象範囲、非対象範囲が書かれている
- 成功条件がある
- 主要ステークホルダーが定義されている
- 高リスク領域が列挙されている

### 3.2 Ready for Implementation
- 変更対象ファイル / モジュールの見当がついている
- 影響範囲が整理されている
- 使うスキルとレビュー深度が決まっている
- テスト方針の当たりがついている
- 不明契約がある場合は調査タスクが切られている

### 3.3 Implementation Complete
- コード変更が反映済み
- 主要なエラーパス / 境界条件が考慮済み
- ログ、監視、エラーメッセージの方針が妥当
- 変更理由と要点を説明できる

### 3.4 Test Complete
- 実行したテストが列挙されている
- 未実施テストがあれば理由付きで記録されている
- 高リスク領域に対するテストが含まれる
- 本番同等性が必要な箇所は parity 観点がカバーされている
- 重要な結果ログ / スクリーンショット / レポートへの参照がある

### 3.5 Release Ready
- 必須テストが通っている
- 未解決課題と暫定対策が明示されている
- 運用上の注意が共有されている
- rollback / recovery の考え方がある
- 例外承認が必要なら承認者と期限が明記されている

## 4. Evidence Table

| Gate | Mandatory Evidence | Where to Record |
|---|---|---|
| Ready for Design | 目的、スコープ、制約、リスク | `PROJECT_BRIEF.md` |
| Ready for Implementation | 設計方針、対象範囲、テスト方針 | `PROJECT_BRIEF.md`, `TEST_STRATEGY.md` |
| Implementation Complete | 変更ファイル、概要、既知制約 | PR / 変更サマリ |
| Test Complete | 実行コマンド、結果、未実施項目 | `TEST_STRATEGY.md` or PR comment |
| Release Ready | 判定結果、残リスク、rollback 観点 | リリース判定メモ |

## 5. Required Commands

以下をプロジェクト実態に合わせて埋める。

| Check Type | Command | Mandatory? |
|---|---|---|
| Build | `{{BUILD_COMMAND}}` | Yes / No |
| Unit tests | `{{UNIT_TEST_COMMAND}}` | Yes / No |
| Integration tests | `{{INTEGRATION_TEST_COMMAND}}` | Yes / No |
| E2E / smoke | `{{E2E_OR_SMOKE_COMMAND}}` | Yes / No |
| Lint | `{{LINT_COMMAND}}` | Yes / No |
| Typecheck | `{{TYPECHECK_COMMAND}}` | Yes / No |
| CI equivalent | `{{CI_COMMAND}}` | Yes / No |
| Packaging / deploy verify | `{{PACKAGE_OR_DEPLOY_COMMAND}}` | Yes / No |

## 6. Risk-Based Extra Gates

次の変更では追加ゲートを入れる。

| Risk | Extra Evidence |
|---|---|
| Auth / Permission | 許可 / 拒否両方の確認 |
| Money / Tax / Rounding | 境界値、丸め差、例外系確認 |
| Time / Timezone | TZ混在、DST、締め時刻確認 |
| SQL / Migration | 対象 DB 方言、rollback、データ整合確認 |
| External API / File I/O | 接続失敗、再試行、部分失敗、永続化確認 |
| Cross-module rules | 更新漏れがないことの確認 |

## 7. Exception / Waiver Policy

例外を認める場合は、最低限次を記録する。

- 何を未実施にしたか
- なぜ未実施か
- リスクは何か
- 暫定対策は何か
- だれが承認したか
- いつまでに解消するか

## 8. Release Decision Template

```md
# Release Decision
- Decision: Go / Conditional Go / No-Go
- Scope:
- Mandatory checks passed:
- Waivers:
- Residual risks:
- Rollback notes:
- Decision owner:
- Timestamp:
```
