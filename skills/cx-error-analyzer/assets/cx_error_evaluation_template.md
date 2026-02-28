# CX Error Evaluation Card

## エラー基本情報

| 項目 | 内容 |
|------|------|
| Error ID | {ERR_ID} |
| シナリオ | {SCENARIO_DESCRIPTION} |
| 分類 | {CLASSIFICATION} (VAL / SYS / NET / AUTH / BIZ / EXT) |
| ユーザージャーニーステージ | {JOURNEY_STAGE} (Discovery / Onboarding / Core Task / Checkout / Support) |
| 発生条件 | {TRIGGER_CONDITIONS} |
| 影響を受けるユーザーセグメント | {AFFECTED_SEGMENTS} |

---

## 現在のエラー体験

### 現在のエラーメッセージ

```
{CURRENT_ERROR_MESSAGE_EXACT_TEXT}
```

### 現在の復旧フロー

1. {CURRENT_RECOVERY_STEP_1}
2. {CURRENT_RECOVERY_STEP_2}
3. {CURRENT_RECOVERY_STEP_3}

### エラー発生時のスクリーンショット / UI状態

{SCREENSHOT_OR_UI_DESCRIPTION}

### 関連データ

| データ項目 | 値 | ソース |
|-----------|-----|--------|
| 月間発生回数 | {MONTHLY_OCCURRENCES} | {DATA_SOURCE_1} |
| 影響ユーザー数/月 | {MONTHLY_AFFECTED_USERS} | {DATA_SOURCE_2} |
| 関連サポートチケット数/月 | {MONTHLY_SUPPORT_TICKETS} | {DATA_SOURCE_3} |
| 平均復旧時間 | {AVG_RECOVERY_TIME} | {DATA_SOURCE_4} |

---

## 6軸 CX評価

### 評価スコア一覧

| # | 評価軸 | ウェイト | スコア (1-5) | 根拠 |
|---|--------|---------|-------------|------|
| 1 | Impact Severity (影響度) | 25% | {IMPACT_SCORE} | {IMPACT_RATIONALE} |
| 2 | Frequency (頻度) | 20% | {FREQUENCY_SCORE} | {FREQUENCY_RATIONALE} |
| 3 | Recovery Ease (復旧容易性) | 15% | {RECOVERY_SCORE} | {RECOVERY_RATIONALE} |
| 4 | Message Quality (メッセージ品質) | 15% | {MESSAGE_SCORE} | {MESSAGE_RATIONALE} |
| 5 | Emotional Impact (感情的影響) | 10% | {EMOTIONAL_SCORE} | {EMOTIONAL_RATIONALE} |
| 6 | Business Cost (ビジネスコスト) | 15% | {BUSINESS_SCORE} | {BUSINESS_RATIONALE} |

### 各軸の詳細評価

#### 1. Impact Severity (影響度): {IMPACT_SCORE}/5

**評価根拠:**
{IMPACT_DETAILED_RATIONALE}

**考慮事項:**
- タスク完了への影響: {TASK_COMPLETION_IMPACT}
- データ損失リスク: {DATA_LOSS_RISK}
- ワークアラウンドの有無: {WORKAROUND_AVAILABILITY}

#### 2. Frequency (頻度): {FREQUENCY_SCORE}/5

**評価根拠:**
{FREQUENCY_DETAILED_RATIONALE}

**データ:**
- セッション影響率: {SESSION_IMPACT_RATE}
- 期間トレンド: {FREQUENCY_TREND} (増加 / 安定 / 減少)
- ピーク時期: {PEAK_PERIOD}

#### 3. Recovery Ease (復旧容易性): {RECOVERY_SCORE}/5

**評価根拠:**
{RECOVERY_DETAILED_RATIONALE}

**考慮事項:**
- 復旧に必要なステップ数: {RECOVERY_STEPS_COUNT}
- 復旧パスの発見容易性: {RECOVERY_PATH_DISCOVERABILITY}
- 必要な技術知識レベル: {REQUIRED_TECHNICAL_KNOWLEDGE}
- 復旧中のデータ保全: {DATA_PRESERVATION_DURING_RECOVERY}

#### 4. Message Quality (メッセージ品質): {MESSAGE_SCORE}/5

**評価根拠:**
{MESSAGE_DETAILED_RATIONALE}

**メッセージ品質チェックリスト:**
- [ ] 何が起きたか明確に伝えている
- [ ] なぜ起きたか説明している
- [ ] 次に何をすべきか具体的に示している
- [ ] 代替手段を提案している
- [ ] ユーザーを責めない表現を使っている
- [ ] 技術用語を使っていない
- [ ] 安心感を与える表現がある

#### 5. Emotional Impact (感情的影響): {EMOTIONAL_SCORE}/5

**評価根拠:**
{EMOTIONAL_DETAILED_RATIONALE}

**感情的影響の増幅要因:**
- 金銭的コンテキスト: {FINANCIAL_CONTEXT} (あり / なし)
- 時間投資量: {TIME_INVESTMENT} (大 / 中 / 小)
- 繰り返し発生の可能性: {REPETITION_LIKELIHOOD} (高 / 中 / 低)
- 緊急性: {URGENCY_LEVEL} (高 / 中 / 低)

#### 6. Business Cost (ビジネスコスト): {BUSINESS_SCORE}/5

**評価根拠:**
{BUSINESS_DETAILED_RATIONALE}

**ビジネスインパクト:**
- サポートチケットコスト: {SUPPORT_TICKET_COST}/月
- チャーンリスク: {CHURN_RISK_ESTIMATE}
- 収益への直接影響: {DIRECT_REVENUE_IMPACT}
- ブランドへの影響: {BRAND_IMPACT}

---

## CXスコア算出

### 計算

```
CX Score = ({IMPACT_SCORE} * 0.25) + ({FREQUENCY_SCORE} * 0.20) + ({RECOVERY_SCORE} * 0.15)
         + ({MESSAGE_SCORE} * 0.15) + ({EMOTIONAL_SCORE} * 0.10) + ({BUSINESS_SCORE} * 0.15)
         = {WEIGHTED_IMPACT} + {WEIGHTED_FREQUENCY} + {WEIGHTED_RECOVERY}
         + {WEIGHTED_MESSAGE} + {WEIGHTED_EMOTIONAL} + {WEIGHTED_BUSINESS}
         = {TOTAL_CX_SCORE}
```

### 結果

| 項目 | 値 |
|------|-----|
| **CXスコア** | **{TOTAL_CX_SCORE}** |
| **ティア** | **{CX_TIER}** |
| **推奨アクション** | {RECOMMENDED_ACTION} |

**ティア判定:**
- 4.0-5.0: Critical CX Issue (即時対応必要) -- {IS_CRITICAL}
- 3.0-3.9: Significant CX Issue (改善計画策定) -- {IS_SIGNIFICANT}
- 2.0-2.9: Moderate CX Issue (バックログ追加) -- {IS_MODERATE}
- 1.0-1.9: Minor CX Issue (余裕があれば対応) -- {IS_MINOR}

---

## 改善提案

### 改善後エラーメッセージ

**現在:**
```
{CURRENT_ERROR_MESSAGE_EXACT_TEXT}
```

**改善案:**
```
{IMPROVED_ERROR_MESSAGE}
```

**改善ポイント:**
- {MESSAGE_IMPROVEMENT_POINT_1}
- {MESSAGE_IMPROVEMENT_POINT_2}
- {MESSAGE_IMPROVEMENT_POINT_3}

### 改善後復旧フロー

**現在の復旧フロー:**
1. {CURRENT_RECOVERY_STEP_1}
2. {CURRENT_RECOVERY_STEP_2}
3. {CURRENT_RECOVERY_STEP_3}

**改善後の復旧フロー:**
1. {IMPROVED_RECOVERY_STEP_1}
2. {IMPROVED_RECOVERY_STEP_2}
3. {IMPROVED_RECOVERY_STEP_3}

### 実装工数見積もり

| 改善項目 | 工数 | 難易度 |
|----------|------|--------|
| エラーメッセージ修正 | {MSG_EFFORT} | {MSG_DIFFICULTY} (High / Medium / Low) |
| 復旧フロー改善 | {FLOW_EFFORT} | {FLOW_DIFFICULTY} (High / Medium / Low) |
| バリデーション追加 | {VAL_EFFORT} | {VAL_DIFFICULTY} (High / Medium / Low) |
| 合計 | **{TOTAL_EFFORT}** | **{OVERALL_DIFFICULTY}** |

### Before / After 比較

| 項目 | Before | After (目標) |
|------|--------|-------------|
| エラーメッセージ | {BEFORE_MESSAGE} | {AFTER_MESSAGE} |
| 復旧ステップ数 | {BEFORE_RECOVERY_STEPS} | {AFTER_RECOVERY_STEPS} |
| 想定される感情 | {BEFORE_USER_EMOTION} | {AFTER_USER_EMOTION} |
| サポート問合せ率 | {BEFORE_CONTACT_RATE} | {AFTER_CONTACT_RATE} |
| 目標CXスコア | {CURRENT_CX_SCORE_REPEAT} | {TARGET_CX_SCORE} |
| CXスコア改善幅 | - | **{CX_SCORE_IMPROVEMENT}** |

### 優先度マトリクス配置

| 項目 | 値 |
|------|-----|
| Impact (CXスコア) | {TOTAL_CX_SCORE} |
| Effort (実装工数) | {OVERALL_DIFFICULTY} |
| **マトリクス象限** | **{MATRIX_QUADRANT}** (Quick Win / Strategic Project / Fill-In / Deprioritize) |

---

## 補足情報

### 関連エラーシナリオ

- {RELATED_ERROR_1}: {RELATION_DESCRIPTION_1}
- {RELATED_ERROR_2}: {RELATION_DESCRIPTION_2}

### 参考情報

- {REFERENCE_INFO_1}
- {REFERENCE_INFO_2}

### 評価者メモ

{EVALUATOR_NOTES}

---

*評価日: {EVALUATION_DATE}*
*評価者: {EVALUATOR_NAME}*
*レビュー者: {REVIEWER_NAME}*
