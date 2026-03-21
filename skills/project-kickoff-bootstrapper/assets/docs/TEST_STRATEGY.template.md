# TEST_STRATEGY

## 1. Purpose

この文書は、どのテストを、どの環境で、どの深さまで行うかを定義する。

## 2. System Under Test

- Feature / change target:
- Affected modules:
- Critical user / business flow:
- Main failure concerns:

## 3. Test Levels and Responsibilities

| Level | Main Objective | What to Catch | What Not to Rely On |
|---|---|---|---|
| Unit | ロジック単体の正しさ | 分岐、境界値、純粋関数の誤り | 環境差分、接続、永続化 |
| Integration | モジュール間 / DB / API 接続 | 契約ズレ、SQL、依存関係 | ブラウザ全体の実動線 |
| E2E / Workflow | 利用者動線の成立 | 画面遷移、成功 / 失敗体験、永続化確認 | 細かい全分岐の網羅 |
| Production Parity / Smoke | 本番同等条件での破綻検知 | DB方言差、runtime依存、packaging、環境差 | 単体ロジック網羅 |

## 4. Risk Coverage Matrix

| Risk Area | Unit | Integration | E2E | Production Parity | Notes |
|---|---|---|---|---|---|
| Business rule correctness | Yes | Optional | Optional | Optional |  |
| Auth / permission | Optional | Yes | Yes | Optional |  |
| DB query / migration | Optional | Yes | Optional | Yes |  |
| File I/O / storage | Optional | Yes | Optional | Yes |  |
| External API / runtime dependency | Optional | Yes | Optional | Yes |  |
| Time / timezone / scheduling | Yes | Yes | Optional | Yes |  |
| Money / rounding / calculation | Yes | Yes | Optional | Optional |  |
| Cross-module consistency | Optional | Yes | Yes | Optional |  |

## 5. Environment Matrix

| Environment | Purpose | Closest to Prod? | Key Differences | Required Test Types |
|---|---|---|---|---|
| Local | 開発中の高速確認 | No |  |  |
| CI | 自動回帰 | Partial |  |  |
| Staging | 結合確認 / リリース前確認 | Usually |  |  |
| Production-like sandbox | 本番同等検証 | Yes |  |  |

## 6. Mandatory Test Scenarios

### Happy Path
-
-

### Error Path
-
-

### Boundary / Edge Cases
-
-

### Data Integrity
- 保存、更新、削除、再実行、冪等性

### Environment Parity
- DB dialect 差
- secret / config 差
- packaging / image build 差
- optional dependency / runtime import 差

## 7. Production Parity Checklist

- [ ] 本番DBと同じ方言 / 主要機能で確認した
- [ ] migration の forward / rollback を考慮した
- [ ] UI 成功表示だけでなく永続化結果を確認した
- [ ] mock に隠れた依存を洗い出した
- [ ] background job / async 処理の最終結果を確認した
- [ ] packaging / container / deployment artifact で起動確認した
- [ ] 外部連携失敗時の挙動を確認した

## 8. Commands and Evidence

| Scenario | Command / Procedure | Evidence Location |
|---|---|---|
| Unit | `{{UNIT_TEST_COMMAND}}` |  |
| Integration | `{{INTEGRATION_TEST_COMMAND}}` |  |
| E2E / smoke | `{{E2E_OR_SMOKE_COMMAND}}` |  |
| Prod parity | `{{PROD_PARITY_COMMAND}}` |  |
| Packaging | `{{PACKAGE_OR_DEPLOY_COMMAND}}` |  |

## 9. Exit Criteria

テスト完了とみなすための条件。

- 必須シナリオが実行済み
- 結果が残っている
- 未実施項目が明示されている
- 高リスク領域に盲点が残っていない、または残っているなら合意済み

## 10. Open Risks

| Risk | Why Not Fully Tested | Temporary Mitigation | Owner |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |
