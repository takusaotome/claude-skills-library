---
name: cx-error-analyzer
description: >
  エラーや例外シナリオを顧客体験(CX)の観点で体系的に分析し、改善優先度を付ける
  スキル。6軸評価（影響度・頻度・復旧容易性・メッセージ品質・感情的影響・
  ビジネスコスト）でスコアリングし、Impact vs Effort マトリクスで改善施策を
  優先順位付けする。Use when analyzing error scenarios from customer experience
  perspective, evaluating error message quality, prioritizing error UX improvements,
  or creating CX-focused error analysis reports. Triggers: "CXエラー分析",
  "error experience", "エラーUX改善", "customer experience error",
  "エラーメッセージ品質", "error scenario analysis", "顧客体験エラー評価"
---

# CX Error Analyzer（CXエラーシナリオ分析）

## Overview

CX Error Analyzer は、システムやアプリケーションのエラーシナリオを顧客体験（Customer Experience）の観点から体系的に分析・評価するスキルです。6軸の定量評価フレームワークにより、エラーが顧客体験に与える影響を可視化し、Impact vs Effort マトリクスで改善施策の優先順位を決定します。

## When to Use

- エラーシナリオの顧客体験を評価するとき
- エラーメッセージの品質を改善するとき
- エラー改善の優先順位を付けるとき
- CX観点でのエラーハンドリング改善レポートを作成するとき
- エラー体験の定量的評価を行うとき
- 新機能リリース前にエラーシナリオのCXレビューを実施するとき
- サポートチケット削減のための改善施策を検討するとき

## Workflows

### Workflow 1: Error Scenario Inventory（エラーシナリオ棚卸し）

Enumerate and classify all error scenarios in the target system or feature.

1. **List all error scenarios** in the system or feature under analysis
   - Review source code, API documentation, and existing error logs
   - Interview stakeholders (developers, support, QA) for known error patterns
   - Examine user feedback and support ticket data for unreported errors
2. **Classify each error** into one of 6 categories:
   - **Validation**: Input format, required fields, range limits
   - **System**: Server errors, database failures, memory issues
   - **Network**: Timeout, connection loss, DNS failure
   - **Auth**: Authentication failure, session expiry, permission denied
   - **Business Logic**: Rule violations, state conflicts, limit exceeded
   - **External**: Third-party API failures, payment gateway errors, integration issues
3. **Map each error to a user journey stage**:
   - Discovery (browsing, searching)
   - Onboarding (registration, initial setup)
   - Core Task (primary feature usage)
   - Checkout (purchase, submission, completion)
   - Support (help, account management)
4. **Assign error IDs**: ERR-001, ERR-002, ERR-003...
5. **Capture current state** for each error:
   - Current error message text (exact wording)
   - Current UX flow (what happens visually)
   - Current recovery path (how the user proceeds)

### Workflow 2: Multi-Axis CX Evaluation（多軸CX評価）

Evaluate each error scenario across 6 dimensions using a 1-5 scale.

1. **Load evaluation criteria** from `references/cx_evaluation_methodology.md`
2. **Evaluate each error scenario** on 6 axes (1-5 scale each):
   - **Impact Severity (影響度)**: How much does this error disrupt the user's task?
   - **Frequency (頻度)**: How often do users encounter this error?
   - **Recovery Ease (復旧容易性)**: How easy is it for users to recover? (inverse: 5 = hard to recover)
   - **Message Quality (メッセージ品質)**: How helpful is the current error message? (inverse: 5 = poor message)
   - **Emotional Impact (感情的影響)**: How frustrated or anxious does the user feel?
   - **Business Cost (ビジネスコスト)**: What is the business impact (support tickets, churn, revenue loss)?
3. **Document rationale** for each score
4. **Use `assets/cx_error_evaluation_template.md`** to record each evaluation

### Workflow 3: CX Scoring（CXスコアリング）

Calculate weighted CX Scores and classify by severity tier.

1. **Apply weights** to each axis:
   | Axis | Weight |
   |------|--------|
   | Impact Severity (影響度) | 25% |
   | Frequency (頻度) | 20% |
   | Recovery Ease (復旧容易性) | 15% |
   | Message Quality (メッセージ品質) | 15% |
   | Emotional Impact (感情的影響) | 10% |
   | Business Cost (ビジネスコスト) | 15% |

2. **Calculate weighted CX Score** (1.0-5.0) for each scenario:
   ```
   CX Score = (Impact * 0.25) + (Frequency * 0.20) + (Recovery * 0.15)
            + (Message * 0.15) + (Emotional * 0.10) + (Business * 0.15)
   ```
   Higher score = worse customer experience.

3. **Classify by CX Score tier**:
   | Score Range | Tier | Action |
   |-------------|------|--------|
   | 4.0-5.0 | Critical CX Issue | Immediate action required |
   | 3.0-3.9 | Significant CX Issue | Plan improvement |
   | 2.0-2.9 | Moderate CX Issue | Add to backlog |
   | 1.0-1.9 | Minor CX Issue | Nice to have |

4. **Rank all scenarios** by CX Score descending
5. **Refer to `references/cx_metrics_reference.md`** for business impact estimation

### Workflow 4: Improvement Priority Matrix（改善優先度マトリクス）

Plot errors on an Impact vs Effort matrix to determine improvement priorities.

1. **Assess implementation effort** for improving each error scenario:
   - **Low Effort**: Message text change, minor UI update (< 1 day)
   - **Medium Effort**: Recovery flow redesign, new validation logic (1-5 days)
   - **High Effort**: Architectural change, new error handling infrastructure (> 5 days)
2. **Plot on 2x2 matrix** (Impact = CX Score, Effort = Implementation Difficulty):

   ```
   High Impact ┌──────────────┬──────────────┐
               │  Strategic   │  Quick Wins  │
               │  Projects    │  (Do First)  │
               │              │              │
               ├──────────────┼──────────────┤
               │ Deprioritize │  Fill-Ins    │
               │  (Avoid)     │  (Batch)     │
   Low Impact  └──────────────┴──────────────┘
               High Effort     Low Effort
   ```

3. **Identify Quick Wins** (High Impact + Low Effort) for immediate action
4. **Plan Strategic Projects** (High Impact + High Effort) with proper roadmap
5. **Suggest specific improvements** for top priority items:
   - Load `references/error_ux_best_practices.md` for design patterns
   - Draft improved error messages (before/after)
   - Design improved recovery flows
   - Estimate improvement impact using `references/cx_metrics_reference.md`

### Workflow 5: Report Generation（レポート出力）

Compile all analysis results into a comprehensive CX Error Analysis Report.

1. **Load report template** from `assets/cx_error_report_template.md`
2. **Populate all sections**:
   - Executive summary with key findings
   - Complete error scenario inventory
   - Multi-axis evaluation results for every scenario
   - CX Score ranking
   - Priority matrix visualization
   - Quick Wins list with specific action items
   - Detailed improvement proposals (top scenarios)
   - Expected benefits (support cost reduction, CSAT improvement, churn reduction)
3. **Include quantitative estimates** where possible:
   - Use `references/cx_metrics_reference.md` for ROI calculations
   - Estimate support ticket reduction
   - Project CSAT/CES improvement
4. **Review and finalize** the report

## Resources

| File | Purpose | When to Load |
|------|---------|--------------|
| `references/cx_evaluation_methodology.md` | Detailed scoring criteria for all 6 evaluation axes, error classification taxonomy, and data collection guidance | Workflow 2 (Multi-Axis CX Evaluation) |
| `references/error_ux_best_practices.md` | Error message design principles, recovery flow patterns, emotional design, accessibility guidelines, and good/bad examples | Workflow 4 (Improvement Priority Matrix) when drafting improvements |
| `references/cx_metrics_reference.md` | CX metrics (CES, CSAT, NPS), support cost formulas, churn risk estimation, industry benchmarks, and ROI calculation | Workflow 3 (CX Scoring) and Workflow 5 (Report Generation) |
| `assets/cx_error_report_template.md` | Complete CX Error Analysis Report template with all sections and placeholders | Workflow 5 (Report Generation) |
| `assets/cx_error_evaluation_template.md` | Individual error scenario evaluation card template for per-scenario assessment | Workflow 2 (Multi-Axis CX Evaluation) for each scenario |

---

## Best Practices

### Do's
- 実際のエラーメッセージテキストをそのまま記録する（推測しない）
- ユーザージャーニーの文脈でエラーを評価する（同じエラーでも決済時とブラウジング時で影響度が異なる）
- 改善提案には必ず「改善前→改善後」のメッセージ比較を含める
- ROI計算にサポートコスト削減とチャーンリスク低減の両方を含める
- Quick Winsを最優先で特定する（小さな改善でも即効性が高い）

### Don'ts
- 技術的な正確性だけでエラーを評価しない（CX観点が主軸）
- 頻度データなしにスコアリングしない（推定でも頻度を見積もる）
- 感情的影響を過小評価しない（ユーザーの不安・焦りは離脱に直結する）
- 改善コストの見積もりを省略しない（Impact vs Effort マトリクスに必須）

---

## Examples

### 例1: ECサイトのエラーCX分析

```
User: ECサイトのエラー体験を改善したい。主要なエラーシナリオを分析してください。

Claude:
1. [Workflow 1] エラー棚卸し → ERR-001(在庫切れ), ERR-002(決済失敗),
   ERR-003(セッションタイムアウト), ERR-004(住所バリデーション), ...
2. [Workflow 2] 6軸評価 → ERR-002(決済失敗)が最高スコア4.2: 影響度5, 復旧困難4, 感情5
3. [Workflow 3] CXスコア計算 → ERR-002: 4.2(Critical), ERR-003: 3.5(Significant), ...
4. [Workflow 4] 優先度マトリクス → Quick Win: ERR-004(メッセージ改善のみ、工数Low)
5. [Workflow 5] レポート出力: 改善提案8件、推定サポートコスト削減20%
```

### 例2: SaaSログイン周りのエラーUX改善

```
User: ログイン・認証エラーのUXを改善したい。

Claude:
1. [Workflow 1] 棚卸し → ERR-001(パスワード誤り), ERR-002(アカウントロック),
   ERR-003(2FA失敗), ERR-004(SSO連携エラー)
2. [Workflow 2] 各シナリオを評価 → ERR-002のメッセージ品質が5(最低: "Account locked"のみ)
3. [Workflow 4] Quick Win: ERR-002のメッセージ改善
   Before: "Account locked. Contact support."
   After: "セキュリティのためアカウントがロックされました。30分後に自動解除されます。
          すぐにログインが必要な場合はパスワードリセットをお試しください。"
```
