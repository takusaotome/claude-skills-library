# CX Error Analysis Report

## レポートヘッダー

| 項目 | 内容 |
|------|------|
| プロジェクト名 | {PROJECT_NAME} |
| 分析対象 | {ANALYSIS_TARGET} |
| 分析対象期間 | {ANALYSIS_PERIOD} |
| 作成日 | {CREATED_DATE} |
| 作成者 | {AUTHOR} |
| バージョン | {VERSION} |

---

## 1. エグゼクティブサマリー

### 主要発見事項

- 分析対象エラーシナリオ数: **{TOTAL_SCENARIOS}件**
- CXスコア分布:
  - Critical（4.0-5.0）: **{CRITICAL_COUNT}件**
  - Significant（3.0-3.9）: **{SIGNIFICANT_COUNT}件**
  - Moderate（2.0-2.9）: **{MODERATE_COUNT}件**
  - Minor（1.0-1.9）: **{MINOR_COUNT}件**
- 平均CXスコア: **{AVERAGE_CX_SCORE}**
- Error CX Health Score: **{CX_HEALTH_SCORE}/100**

### Quick Wins

- Quick Win対象: **{QUICK_WIN_COUNT}件**（高インパクト＋低工数の改善施策）
- Quick Win実施による推定効果:
  - サポートチケット削減: 約{TICKET_REDUCTION_PERCENT}%削減（年間{TICKET_REDUCTION_COST}節約）
  - チャーンリスク低減: 約{CHURN_REDUCTION_USERS}名のチャーン防止（年間{CHURN_PREVENTION_REVENUE}相当）

### 推奨アクション

1. {TOP_RECOMMENDATION_1}
2. {TOP_RECOMMENDATION_2}
3. {TOP_RECOMMENDATION_3}

---

## 2. エラーシナリオ一覧

| ERR-ID | シナリオ | 分類 | ジャーニーステージ | 現在のエラーメッセージ |
|--------|----------|------|--------------------|-----------------------|
| {ERR_ID_1} | {SCENARIO_1} | {CATEGORY_1} | {STAGE_1} | {CURRENT_MESSAGE_1} |
| {ERR_ID_2} | {SCENARIO_2} | {CATEGORY_2} | {STAGE_2} | {CURRENT_MESSAGE_2} |
| {ERR_ID_3} | {SCENARIO_3} | {CATEGORY_3} | {STAGE_3} | {CURRENT_MESSAGE_3} |

### 分類別サマリー

| 分類 | 件数 | 平均CXスコア |
|------|------|-------------|
| Validation (VAL) | {VAL_COUNT} | {VAL_AVG_SCORE} |
| System (SYS) | {SYS_COUNT} | {SYS_AVG_SCORE} |
| Network (NET) | {NET_COUNT} | {NET_AVG_SCORE} |
| Auth (AUTH) | {AUTH_COUNT} | {AUTH_AVG_SCORE} |
| Business Logic (BIZ) | {BIZ_COUNT} | {BIZ_AVG_SCORE} |
| External (EXT) | {EXT_COUNT} | {EXT_AVG_SCORE} |

### ジャーニーステージ別サマリー

| ステージ | 件数 | 平均CXスコア | 最も深刻なエラー |
|----------|------|-------------|-----------------|
| Discovery | {DISC_COUNT} | {DISC_AVG} | {DISC_WORST} |
| Onboarding | {ONB_COUNT} | {ONB_AVG} | {ONB_WORST} |
| Core Task | {CORE_COUNT} | {CORE_AVG} | {CORE_WORST} |
| Checkout | {CHK_COUNT} | {CHK_AVG} | {CHK_WORST} |
| Support | {SUP_COUNT} | {SUP_AVG} | {SUP_WORST} |

---

## 3. 多軸評価サマリー

### 全シナリオ評価一覧

| ERR-ID | 影響度 | 頻度 | 復旧容易性 | メッセージ品質 | 感情的影響 | ビジネスコスト | CXスコア | ティア |
|--------|--------|------|-----------|--------------|-----------|--------------|---------|--------|
| {ERR_ID_1} | {IMPACT_1} | {FREQ_1} | {RECOVERY_1} | {MESSAGE_1} | {EMOTION_1} | {BUSINESS_1} | {SCORE_1} | {TIER_1} |
| {ERR_ID_2} | {IMPACT_2} | {FREQ_2} | {RECOVERY_2} | {MESSAGE_2} | {EMOTION_2} | {BUSINESS_2} | {SCORE_2} | {TIER_2} |
| {ERR_ID_3} | {IMPACT_3} | {FREQ_3} | {RECOVERY_3} | {MESSAGE_3} | {EMOTION_3} | {BUSINESS_3} | {SCORE_3} | {TIER_3} |

### 軸別分析

**影響度（Impact Severity）が高いシナリオ（スコア4以上）:**
- {HIGH_IMPACT_SCENARIOS}

**頻度（Frequency）が高いシナリオ（スコア4以上）:**
- {HIGH_FREQUENCY_SCENARIOS}

**復旧が困難なシナリオ（Recovery Ease スコア4以上）:**
- {HARD_RECOVERY_SCENARIOS}

**メッセージ品質が低いシナリオ（Message Quality スコア4以上）:**
- {POOR_MESSAGE_SCENARIOS}

---

## 4. CXスコアランキング

### スコア降順ランキング

| 順位 | ERR-ID | シナリオ | CXスコア | ティア | 主な問題 |
|------|--------|----------|---------|--------|---------|
| 1 | {RANK1_ID} | {RANK1_SCENARIO} | {RANK1_SCORE} | {RANK1_TIER} | {RANK1_ISSUE} |
| 2 | {RANK2_ID} | {RANK2_SCENARIO} | {RANK2_SCORE} | {RANK2_TIER} | {RANK2_ISSUE} |
| 3 | {RANK3_ID} | {RANK3_SCENARIO} | {RANK3_SCORE} | {RANK3_TIER} | {RANK3_ISSUE} |

### ティア別分布

```
Critical  (4.0-5.0): {CRITICAL_BAR}  {CRITICAL_COUNT}件
Significant (3.0-3.9): {SIGNIFICANT_BAR}  {SIGNIFICANT_COUNT}件
Moderate  (2.0-2.9): {MODERATE_BAR}  {MODERATE_COUNT}件
Minor     (1.0-1.9): {MINOR_BAR}  {MINOR_COUNT}件
```

---

## 5. 改善優先度マトリクス

### Impact vs Effort マトリクス

```
High Impact  ┌─────────────────────┬─────────────────────┐
(CX Score    │                     │                     │
 3.5+)       │  Strategic Projects │     Quick Wins      │
             │  {STRATEGIC_LIST}   │  {QUICKWIN_LIST}    │
             │                     │                     │
             ├─────────────────────┼─────────────────────┤
             │                     │                     │
(CX Score    │   Deprioritize      │     Fill-Ins        │
 <3.5)       │  {DEPRIORITIZE_LIST}│  {FILLIN_LIST}      │
             │                     │                     │
Low Impact   └─────────────────────┴─────────────────────┘
              High Effort            Low Effort
              (>5 days)              (<5 days)
```

### 象限別一覧

#### Quick Wins（高インパクト＋低工数）-- 最優先

| ERR-ID | シナリオ | CXスコア | 推定工数 | 改善内容 |
|--------|----------|---------|---------|---------|
| {QW_ID_1} | {QW_SCENARIO_1} | {QW_SCORE_1} | {QW_EFFORT_1} | {QW_ACTION_1} |
| {QW_ID_2} | {QW_SCENARIO_2} | {QW_SCORE_2} | {QW_EFFORT_2} | {QW_ACTION_2} |

#### Strategic Projects（高インパクト＋高工数）-- 計画的に推進

| ERR-ID | シナリオ | CXスコア | 推定工数 | 改善内容 |
|--------|----------|---------|---------|---------|
| {SP_ID_1} | {SP_SCENARIO_1} | {SP_SCORE_1} | {SP_EFFORT_1} | {SP_ACTION_1} |

#### Fill-Ins（低インパクト＋低工数）-- バッチ処理

| ERR-ID | シナリオ | CXスコア | 推定工数 | 改善内容 |
|--------|----------|---------|---------|---------|
| {FI_ID_1} | {FI_SCENARIO_1} | {FI_SCORE_1} | {FI_EFFORT_1} | {FI_ACTION_1} |

#### Deprioritize（低インパクト＋高工数）-- 後回し

| ERR-ID | シナリオ | CXスコア | 推定工数 | 理由 |
|--------|----------|---------|---------|------|
| {DP_ID_1} | {DP_SCENARIO_1} | {DP_SCORE_1} | {DP_EFFORT_1} | {DP_REASON_1} |

---

## 6. Quick Wins 一覧

即座に実施可能な改善施策の詳細です。

### Quick Win #{QW_NUMBER_1}: {QW_TITLE_1}

- **対象**: {QW_ERR_ID_1}（{QW_ERR_SCENARIO_1}）
- **CXスコア**: {QW_CX_SCORE_1}（{QW_TIER_1}）
- **推定工数**: {QW_EFFORT_DETAIL_1}
- **改善内容**: {QW_IMPROVEMENT_DETAIL_1}
- **期待効果**: {QW_EXPECTED_BENEFIT_1}

### Quick Win #{QW_NUMBER_2}: {QW_TITLE_2}

- **対象**: {QW_ERR_ID_2}（{QW_ERR_SCENARIO_2}）
- **CXスコア**: {QW_CX_SCORE_2}（{QW_TIER_2}）
- **推定工数**: {QW_EFFORT_DETAIL_2}
- **改善内容**: {QW_IMPROVEMENT_DETAIL_2}
- **期待効果**: {QW_EXPECTED_BENEFIT_2}

---

## 7. 改善提案詳細

上位CXスコアのシナリオに対する具体的な改善案です。

### {IMPROVEMENT_TITLE_1}（{IMP_ERR_ID_1}）

**現在の状態:**
- エラーメッセージ: "{CURRENT_MSG_1}"
- 復旧フロー: {CURRENT_RECOVERY_1}
- CXスコア: {CURRENT_CX_SCORE_1}

**改善後:**
- エラーメッセージ: "{IMPROVED_MSG_1}"
- 復旧フロー: {IMPROVED_RECOVERY_1}
- 目標CXスコア: {TARGET_CX_SCORE_1}

**Before / After 比較:**

| 項目 | Before | After |
|------|--------|-------|
| メッセージ | {BEFORE_MSG_1} | {AFTER_MSG_1} |
| 復旧ステップ数 | {BEFORE_STEPS_1} | {AFTER_STEPS_1} |
| ユーザーの感情 | {BEFORE_EMOTION_1} | {AFTER_EMOTION_1} |
| サポート問合せ率 | {BEFORE_CONTACT_1} | {AFTER_CONTACT_1} |

**実装方針:**
{IMPLEMENTATION_PLAN_1}

### {IMPROVEMENT_TITLE_2}（{IMP_ERR_ID_2}）

**現在の状態:**
- エラーメッセージ: "{CURRENT_MSG_2}"
- 復旧フロー: {CURRENT_RECOVERY_2}
- CXスコア: {CURRENT_CX_SCORE_2}

**改善後:**
- エラーメッセージ: "{IMPROVED_MSG_2}"
- 復旧フロー: {IMPROVED_RECOVERY_2}
- 目標CXスコア: {TARGET_CX_SCORE_2}

**Before / After 比較:**

| 項目 | Before | After |
|------|--------|-------|
| メッセージ | {BEFORE_MSG_2} | {AFTER_MSG_2} |
| 復旧ステップ数 | {BEFORE_STEPS_2} | {AFTER_STEPS_2} |
| ユーザーの感情 | {BEFORE_EMOTION_2} | {AFTER_EMOTION_2} |
| サポート問合せ率 | {BEFORE_CONTACT_2} | {AFTER_CONTACT_2} |

**実装方針:**
{IMPLEMENTATION_PLAN_2}

---

## 8. 期待効果

### サポートコスト削減

| 項目 | 現在 | 改善後（推定） | 削減額 |
|------|------|--------------|--------|
| 月間エラー関連チケット数 | {CURRENT_MONTHLY_TICKETS} | {PROJECTED_MONTHLY_TICKETS} | {TICKET_REDUCTION} |
| 平均対応コスト/件 | {AVG_TICKET_COST} | {AVG_TICKET_COST} | - |
| 年間サポートコスト | {CURRENT_ANNUAL_SUPPORT_COST} | {PROJECTED_ANNUAL_SUPPORT_COST} | **{ANNUAL_SUPPORT_SAVINGS}** |

### CSAT / CES 改善

| 指標 | 現在 | 改善後（推定） | 改善幅 |
|------|------|--------------|--------|
| CSAT（エラー遭遇ユーザー） | {CURRENT_CSAT} | {PROJECTED_CSAT} | {CSAT_IMPROVEMENT} |
| CES（エラー遭遇ユーザー） | {CURRENT_CES} | {PROJECTED_CES} | {CES_IMPROVEMENT} |
| Error CX Health Score | {CURRENT_HEALTH} | {PROJECTED_HEALTH} | {HEALTH_IMPROVEMENT} |

### チャーンリスク低減

| 項目 | 現在 | 改善後（推定） | 効果 |
|------|------|--------------|------|
| エラー起因チャーン率 | {CURRENT_CHURN_RATE} | {PROJECTED_CHURN_RATE} | {CHURN_REDUCTION_RATE} |
| 年間チャーン防止人数 | - | {PREVENTED_CHURN_USERS} | - |
| チャーン防止による年間収益保全 | - | **{PREVENTED_CHURN_REVENUE}** | - |

### ROI サマリー

```
改善投資コスト:            {TOTAL_IMPROVEMENT_COST}
年間期待効果:
  サポートコスト削減:       {ANNUAL_SUPPORT_SAVINGS}
  チャーン防止収益:         {PREVENTED_CHURN_REVENUE}
  コンバージョン回復:       {CONVERSION_RECOVERY_REVENUE}
  合計:                    {TOTAL_ANNUAL_BENEFIT}

ROI:                       {ROI_PERCENTAGE}%
投資回収期間:               {PAYBACK_PERIOD}
```

---

## 9. 実施ロードマップ

### Phase 1: Quick Wins（{PHASE1_TIMELINE}）

| # | 施策 | 担当 | 期限 | ステータス |
|---|------|------|------|-----------|
| 1 | {PHASE1_ITEM_1} | {PHASE1_OWNER_1} | {PHASE1_DUE_1} | {PHASE1_STATUS_1} |
| 2 | {PHASE1_ITEM_2} | {PHASE1_OWNER_2} | {PHASE1_DUE_2} | {PHASE1_STATUS_2} |

### Phase 2: Strategic Projects（{PHASE2_TIMELINE}）

| # | 施策 | 担当 | 期限 | ステータス |
|---|------|------|------|-----------|
| 1 | {PHASE2_ITEM_1} | {PHASE2_OWNER_1} | {PHASE2_DUE_1} | {PHASE2_STATUS_1} |

### Phase 3: Fill-Ins & Continuous Improvement（{PHASE3_TIMELINE}）

| # | 施策 | 担当 | 期限 | ステータス |
|---|------|------|------|-----------|
| 1 | {PHASE3_ITEM_1} | {PHASE3_OWNER_1} | {PHASE3_DUE_1} | {PHASE3_STATUS_1} |

---

## 10. 付録

### A. 評価基準詳細

6軸評価の詳細な基準は `references/cx_evaluation_methodology.md` を参照してください。

| 軸 | ウェイト | スケール | 方向 |
|----|---------|---------|------|
| Impact Severity (影響度) | 25% | 1-5 | 高い = 悪い |
| Frequency (頻度) | 20% | 1-5 | 高い = 悪い |
| Recovery Ease (復旧容易性) | 15% | 1-5 (inverse) | 高い = 復旧困難 |
| Message Quality (メッセージ品質) | 15% | 1-5 (inverse) | 高い = 低品質 |
| Emotional Impact (感情的影響) | 10% | 1-5 | 高い = 悪い |
| Business Cost (ビジネスコスト) | 15% | 1-5 | 高い = 悪い |

**CXスコア計算式:**
```
CX Score = (Impact * 0.25) + (Frequency * 0.20) + (Recovery * 0.15)
         + (Message * 0.15) + (Emotional * 0.10) + (Business * 0.15)
```

### B. データソース

| データ | ソース | 取得日 | 備考 |
|--------|--------|--------|------|
| {DATA_SOURCE_1} | {SOURCE_SYSTEM_1} | {RETRIEVAL_DATE_1} | {NOTE_1} |
| {DATA_SOURCE_2} | {SOURCE_SYSTEM_2} | {RETRIEVAL_DATE_2} | {NOTE_2} |

### C. 用語集

| 用語 | 定義 |
|------|------|
| CXスコア | 6軸の重み付き平均スコア（1.0-5.0）。高いほどCXが悪い |
| CES | Customer Effort Score。顧客が目的達成に要した労力の指標 |
| CSAT | Customer Satisfaction Score。顧客満足度 |
| NPS | Net Promoter Score。推奨意向スコア |
| LTV | Lifetime Value。顧客生涯価値 |
| Quick Win | 高インパクト＋低工数の改善施策 |
| Recovery Flow | エラー発生後にユーザーがタスクを再開・完了するまでの一連の手順 |

---

*本レポートは CX Error Analyzer スキルにより生成されました。*
*評価基準の詳細は付録Aを、CXメトリクスの算出根拠は `references/cx_metrics_reference.md` を参照してください。*
