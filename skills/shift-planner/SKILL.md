---
name: shift-planner
description: |
  従業員リスト（勤務可能時間帯・曜日・資格等の制約条件付き）と人員要件（作業室×曜日×時間帯の必要人員）を入力として、
  個人別シフトを自動編成するスキル。制約充足型 Greedy Assignment アルゴリズムにより、
  ハード制約（労働時間上限、連続勤務制限、休息時間、資格マッチング）を遵守しつつ、
  公平性（週末均等配分、時間偏差）を考慮したシフト表を生成する。
  カバレッジ検証（30分刻み）と公平性レポートも自動出力。
  Use when: 「シフトを作成」「従業員のシフト編成」「勤務表を自動生成」
  「人員配置のシフト計画」「週次シフトスケジュール」「shift schedule」
---

# Shift Planner

## Overview

従業員リスト（roster）と人員要件（requirements）を入力として、制約充足型 Greedy Assignment で個人別シフトを自動編成するスキル。
production-schedule-optimizer の出力（人員要件）を活用可能だが、単体でも汎用的なシフト計画ツールとして動作する。

**Primary language**: Japanese (default), English supported
**Algorithm**: Constraint-Satisfaction Greedy Assignment (difficulty-first slot ordering)
**Output format**: Markdown report (shift table, coverage matrix, fairness report, alerts)
**Dependencies**: None (Python standard library only)

---

## When to Use

- 従業員の個人別シフト表を自動生成したい
- 勤務可能曜日・時間帯・資格などの制約を考慮したシフト編成が必要
- production-schedule-optimizer で算出した人員要件に基づくシフト計画を立てたい
- シフトのカバレッジ（時間帯別充足状況）を検証したい
- 従業員間の公平性（労働時間偏差、週末シフト配分）を分析したい
- 監督者配置要件を含むシフト計画が必要

## Prerequisites

- Python 3.9+
- 外部依存なし（標準ライブラリのみ: csv, math, argparse, dataclasses）
- 入力CSVはUTF-8エンコーディング

## Limitations

- **深夜跨ぎシフト非対応**: `start_hour >= end_hour` のパターンは SFT-E004 で Reject
- **週単位**: 月・年単位のスケジューリングは対象外
- **1日1シフト**: 同一従業員の同日複数シフトは未対応

## Output

- **形式**: Markdown レポート（4セクション構成）
- **内容**:
  1. シフト割当表（曜日別）
  2. カバレッジマトリクス（30分刻み）
  3. 公平性レポート（従業員別）
  4. アラート一覧

---

## Input Specification

3種類のCSVファイルを入力として受け取る（シフトパターンは任意）。

### 1. roster.csv — 従業員リスト

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| employee_id | string | Yes | 一意の従業員ID（例: EMP-001） |
| name | string | Yes | 表示名 |
| available_days | string | Yes | 勤務可能曜日（セミコロン区切り: `MON;TUE;WED`） |
| max_hours_week | float | Yes | 週最大労働時間 |
| max_days_week | int | Yes | 週最大勤務日数 |
| qualifications | string | Yes | 対応可能な作業室コード（セミコロン区切り） |
| is_supervisor | int | Yes | 監督者=1, それ以外=0 |
| preferred_patterns | string | No | 希望シフトパターン（セミコロン区切り, 空=制限なし） |
| avoid_days | string | No | 回避希望曜日（ソフト制約, セミコロン区切り） |
| contract_hours | float | No | 契約時間（デフォルト=max_hours_week, 公平性計算用） |

### 2. requirements.csv — 人員要件

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| day | string | Yes | 曜日コード（MON-SUN） |
| room_code | string | Yes | 作業室コード |
| required_staff | int | Yes | 必要人員数 |
| start_hour | float | No | 稼働開始（デフォルト 8.0） |
| end_hour | float | No | 稼働終了（デフォルト 17.0） |
| need_supervisor | int | No | 監督者必須=1（デフォルト 1） |

### 3. shift_patterns.csv — シフトパターン定義（任意）

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| pattern_id | string | Yes | パターンID（例: FULL_8H） |
| name | string | Yes | 表示名 |
| start_hour | float | Yes | 開始時刻 |
| end_hour | float | Yes | 終了時刻 |
| break_start | float | No | 休憩開始（空=休憩なし） |
| break_end | float | No | 休憩終了 |
| net_hours | float | Yes | 実労働時間 |

未指定時はビルトインの5パターン（FULL_8H / EARLY_8H / LATE_8H / SHORT_6H / HALF_4H）を使用。

> **Sample files**: `skills/shift-planner/assets/sample_roster.csv`, `skills/shift-planner/assets/sample_requirements.csv`, `skills/shift-planner/assets/sample_shift_patterns.csv`

---

## Workflow 1: Shift Generation

**Purpose**: 制約充足型 Greedy Assignment で個人別シフトを自動編成する。

### Phase 1: Slot Priority Sort

- (day, room) ごとの要件を「充足困難度」でソート
- 困難度 = required_staff / 有資格従業員数（高い=先に割当）
- タイブレーク: DAY_ORDER index → room_code ASC

### Phase 2: Greedy Assignment Loop

各スロットについて:

1. **候補フィルタ (is_eligible)**: ハード制約チェック
   - available_days, qualifications, max_hours, max_days, 連続勤務, 休息時間

2. **優先度スコア (compute_priority_score)**: 固定重み式
   ```
   score = -(remaining_hours * 10)     # 契約残余多い=優先
           + (weekend_shifts * 20)      # 週末バランス
           + (avoid_penalty * 50)       # 回避曜日ペナルティ
           - (supervisor_bonus * 100)   # 監督者ボーナス
           - (speciality * 5)           # 資格専門度
           + (preference_miss * 30)     # 希望パターン不一致
   ```
   タイブレーク: score ASC → employee_id ASC（完全決定性）

3. **パターン選択 (select_pattern)**: ソートキー = (希望一致, -カバー時間, pattern_id ASC)

4. **割当 + 状態更新**: hours_assigned, days_assigned, last_shift_end を更新

5. **監督者チェック**: need_supervisor=1 の場合、監督者不在なら SFT-W002

### Phase 3: Coverage Verification

- **30分刻み**で assigned >= required を検証
- 休憩時間中は on_duty から除外

### Phase 4: Fairness Metrics

- 従業員別: 実労働時間, 契約時間差分, 勤務日数, 週末シフト数, 回避曜日違反数
- 全体: 週末シフト標準偏差 → SFT-W009 (>1.0)

> **Detail**: Load `skills/shift-planner/references/shift_planning_methodology.md` for algorithm details.

---

## Workflow 2: Validation & Alerts

**Purpose**: 入力データと生成結果の品質検証。

### Error (SFT-E): Processing Stops

| Code | Trigger | Description |
|------|---------|-------------|
| SFT-E001 | max_hours_week <= 0 | 週労働時間が無効 |
| SFT-E002 | max_days_week <= 0 | 週勤務日数が無効 |
| SFT-E003 | net_hours <= 0（パターン） | パターン実労働時間が無効 |
| SFT-E004 | start_hour >= end_hour（パターン） | 深夜跨ぎ非対応 |
| SFT-E005 | required_staff <= 0（要件） | 必要人員が無効 |
| SFT-E006 | room_code に有資格者ゼロ（静的） | 構造的に充足不可能 |
| SFT-E007 | 有効パターンゼロ | 全パターンが無効 |
| SFT-E008 | employee_id 重複 | 従業員ID重複 |

### Warning (SFT-W): Processing Continues

| Code | Trigger | Description |
|------|---------|-------------|
| SFT-W001 | カバレッジギャップ | assigned < required |
| SFT-W002 | 監督者不在 | need_supervisor=1 なのに未配置 |
| SFT-W003 | 回避曜日に割当 | ソフト制約違反 |
| SFT-W004 | 時間偏差 > 4h | 公平性警告 |
| SFT-W005 | 割当ゼロの従業員 | 遊休 |
| SFT-W006 | 連続勤務日数超過 | 事後監査 |
| SFT-W007 | シフト間休息時間不足 | 事後監査 |
| SFT-W008 | 候補ゼロ（動的） | 当日制約で割当不可 |
| SFT-W009 | 週末シフト標準偏差 > 1.0 | 週末不公平 |
| SFT-W010 | max_hours_week 到達 | 時間上限で未充足 |

> **Detail**: Load `skills/shift-planner/references/labor_constraints_guide.md` for labor law considerations.

---

## Scripts

### generate_shifts.py

```bash
python3 skills/shift-planner/scripts/generate_shifts.py \
  --roster roster.csv \
  --requirements requirements.csv \
  --patterns shift_patterns.csv \
  --week-start 2026-02-23 \
  --max-consecutive-days 6 \
  --min-rest-hours 11 \
  --output shifts.md
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| --roster | Yes | - | 従業員リスト CSV |
| --requirements | Yes | - | 人員要件 CSV |
| --patterns | No | ビルトイン5パターン | シフトパターン CSV |
| --week-start | Yes | - | 週開始日（YYYY-MM-DD, 表示専用） |
| --max-consecutive-days | No | 6 | 最大連続勤務日数 |
| --min-rest-hours | No | 11.0 | シフト間最小休息時間（時間） |
| --output | No | stdout | 出力先（Markdown） |

---

## Built-in Shift Patterns

| Pattern | Start | End | Break | Net Hours |
|---------|-------|-----|-------|-----------|
| FULL_8H | 08:00 | 17:00 | 12:00-13:00 | 8.0h |
| EARLY_8H | 06:00 | 15:00 | 11:00-12:00 | 8.0h |
| LATE_8H | 10:00 | 19:00 | 14:00-15:00 | 8.0h |
| SHORT_6H | 08:00 | 14:00 | None | 6.0h |
| HALF_4H | 08:00 | 12:00 | None | 4.0h |

---

## Resources

### references/

| File | Description | When to Load |
|------|-------------|--------------|
| `shift_planning_methodology.md` | アルゴリズム詳細、スコアリング重み、改善手法 | アルゴリズム理解・改善時 |
| `labor_constraints_guide.md` | 労働法制約、休憩規則、連続勤務制限 | 労働制約検討時 |

### assets/

| File | Description |
|------|-------------|
| `sample_roster.csv` | 従業員リストサンプル（8名） |
| `sample_requirements.csv` | 人員要件サンプル（7日×2室） |
| `sample_shift_patterns.csv` | シフトパターンサンプル |
| `shift_output_template.md` | 出力テンプレート |

---

## Best Practices

### 入力データ準備

1. **従業員ID命名**: 部門+連番（EMP-001, SUP-001）で管理性向上
2. **資格コード**: production-schedule-optimizer の room_code と一致させる
3. **契約時間**: 公平性計算の基準。max_hours_week と異なる場合は明示的に指定

### シフト最適化

1. **困難スロット優先**: アルゴリズムが自動処理（有資格者少ないスロット=先に割当）
2. **監督者確保**: is_supervisor=1 の従業員を十分に配置
3. **週末公平配分**: W_WEEKEND 重みで自然に分散、W009 で検知
4. **回避曜日**: ソフト制約として考慮、やむを得ない場合は W003 で通知

### production-schedule-optimizer との連携

1. estimate_staff.py の `recommended` 値を requirements.csv の `required_staff` に転記
2. room_code を一致させる
3. start_hour / end_hour は PSO の稼働時間帯に合わせる
