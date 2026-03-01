---
name: production-schedule-optimizer
description: |
  製造施設（セントラルキッチン、食品工場、製造ライン）の週次生産スケジュールを最適化するスキル。
  製品の賞味期限、作業室の容量、人員配置、設備制約を考慮したタイムテーブル生成、
  人員要件見積、シフト計画、カバレッジ検証を提供。
  Use when: 「製造スケジュールを作成」「生産計画を最適化」「人員配置を見積もり」
  「CK スケジュール」「週次製造計画」「シフト計画」
---

# Production Schedule Optimizer

## Overview

製造施設（セントラルキッチン、食品工場など）の週次生産スケジュールを自動生成・最適化するスキル。
4種類のCSV（製品マスタ、需要、作業室、人員）を入力とし、賞味期限に基づく製造頻度、作業室容量、人員制約を考慮した週次タイムテーブルを生成する。

**Primary language**: Japanese (default), English supported
**Frameworks**: Greedy Bin-Packing (Largest-First Decreasing), FEFO, HACCP-aware room assignment
**Output format**: Weekly schedule (Markdown table), staff reports, shift plans, alert summaries

---

## When to Use

- セントラルキッチンや食品工場の週次製造スケジュールを作成したい
- 賞味期限ベースの製造頻度を自動計算したい
- 作業室の容量と人員制約を考慮した最適タイムテーブルが必要
- 人員要件を見積もり、シフト計画を立てたい
- 既存スケジュールのボトルネック特定と改善をしたい
- 複数作業室間の負荷バランスを最適化したい

## Prerequisites

- Python 3.9+
- 外部依存なし（標準ライブラリのみ）
- 入力CSVはUTF-8エンコーディング
- 4種類のCSVファイル（products, demand, rooms, staff）を事前準備

## Output

### generate_schedule.py
- **形式**: Markdown テーブル（曜日別タイムテーブル + アラートセクション）
- **内容**: 曜日×作業室×製品ごとの開始時刻、終了時刻、数量、人員、所要時間

### estimate_staff.py
- **形式**: Markdown テーブル（曜日別人員要件）
- **内容**: 作業室×曜日ごとの必要人時、ピーク人員、最小人員、推奨人員、タスク数

---

## Input Specification

4種類のCSVファイルを入力として受け取る。

### 1. products.csv — 製品マスタ

| Column | Type | Description |
|--------|------|-------------|
| product_code | string | 製品コード（一意キー） |
| name | string | 製品名 |
| prep_time_min | int | 1ロット（base_qty分）の調理時間（分） |
| base_qty | int | 1ロットの基準数量 |
| required_staff | int | 1ロット製造に必要な人数 |
| shelf_life_days | int | 賞味期限（日数） |
| room_codes | string | 割当可能な作業室コード（セミコロン区切り） |

```csv
product_code,name,prep_time_min,base_qty,required_staff,shelf_life_days,room_codes
BREAD-001,Sandwich Bread,120,50,2,2,BAKERY
SAUCE-001,Tomato Sauce,90,80,2,5,SAUCE;BROTH
```

### 2. demand.csv — 週次需要

| Column | Type | Description |
|--------|------|-------------|
| product_code | string | 製品コード（products.csvと一致） |
| qty | int | 週次需要数量 |

### 3. rooms.csv — 作業室マスタ

| Column | Type | Description |
|--------|------|-------------|
| room_code | string | 作業室コード（一意キー） |
| name | string | 作業室名 |
| max_staff | int | 最大同時作業人数 |

### 4. staff.csv — 人員配置

| Column | Type | Description |
|--------|------|-------------|
| day | string | 曜日（MON/TUE/WED/THU/FRI/SAT/SUN） |
| room_code | string | 作業室コード（rooms.csvと一致） |
| staff_count | int | 配置人数 |
| shift_hours | float | シフト時間（時間） |

> **Sample files**: `assets/sample_products.csv`, `assets/sample_demand.csv`, `assets/sample_rooms.csv`, `assets/sample_staff.csv`

---

## Workflow 1: Product & Constraint Modeling

**Purpose**: 入力CSVを読み込み、バリデーションと派生フィールド計算を実施する。

### Step 1: Load and Cross-Reference

1. 4つのCSVファイルを読み込み、カラム名を正規化（小文字化、空白トリム）
2. demand.csv の product_code が products.csv に存在するか確認
3. staff.csv / products.csv の room_code が rooms.csv に存在するか確認
4. 孤立レコードを警告出力

### Step 2: Field-Level Validation

| Field | Condition | Rule | Alert Code |
|-------|-----------|------|------------|
| shelf_life_days | <= 0 | Reject | PSO-E001 |
| base_qty | <= 0 | Reject | PSO-E002 |
| prep_time_min | <= 0 | Reject | PSO-E003 |
| required_staff | <= 0 | Reject | PSO-E004 |
| qty (demand) | <= 0 | Skip + Warning | PSO-W001 |
| qty (demand) | NaN/missing | Skip + Warning | PSO-W002 |
| max_staff | <= 0 | Reject | PSO-E005 |
| room_codes | Unknown room | Reject | PSO-E006 |
| staff_count | Missing | Clamp to 0 + Warning | PSO-W003 |

- **Reject**: 当該レコードを処理対象から除外、エラーログ出力
- **Skip + Warning**: 当該製品をスキップ、警告ログ出力
- **Clamp**: 欠損値を0に補完、警告ログ出力

### Step 3: Compute Derived Fields

```
production_count = min(ceil(7 / shelf_life_days), 7)
qty_per_run      = ceil(qty / production_count)
lot_count        = ceil(qty_per_run / base_qty)
duration_minutes = lot_count * prep_time_min
staff_hours      = (duration_minutes * required_staff) / 60
total_staff_hours = staff_hours * production_count
```

**production_count 早見表:**
- shelf_life=1 -> 7回/週, shelf_life=2 -> 4回, shelf_life=3 -> 3回, shelf_life=7 -> 1回

> **Detail**: Load `references/food_production_guide.md` for FEFO integration and HACCP considerations.

---

## Workflow 2: Weekly Schedule Generation

**Purpose**: Greedy Bin-Packing で作業室容量と人員制約を遵守した週次スケジュールを生成する。

### Algorithm Overview

製造タスクを「大きい順」に並べ、残容量が最大の作業室・曜日に詰め込む近似アルゴリズム。

### Step 1: Task Expansion

各製品について production_count 回のタスクエントリを生成する。

```python
tasks = []
for product in validated_products:
    for i in range(product.production_count):
        tasks.append(Task(
            product_code=product.product_code, run_index=i,
            duration_minutes=product.duration_minutes,
            required_staff=product.required_staff,
            staff_hours=product.staff_hours,
            allowed_rooms=product.room_codes,
            shelf_life_days=product.shelf_life_days,
        ))
```

### Step 2: Deterministic Sort

再現性保証のための3キーソート:

| Priority | Key | Order | Rationale |
|----------|-----|-------|-----------|
| 1 | total_staff_hours | DESC | 大タスク先行（bin-packing基本戦略） |
| 2 | shelf_life_days | ASC | 短賞味期限優先（FEFO原則） |
| 3 | product_code | ASC | 同一条件時の決定性保証 |

```python
tasks.sort(key=lambda t: (-t.staff_hours, t.shelf_life_days, t.product_code))
```

### Step 3: Day Assignment

製造間隔を考慮した曜日割当（MON=0, ..., SUN=6）:

```
step = len(available_days) / production_count
assigned_days = [available_days[int(i * step)] for i in range(production_count)]
```

Examples: count=7 -> 毎日, count=3 -> [0,2,4](MON/WED/FRI), count=1 -> [0](MON)

### Step 4: Room Selection

| Priority | Key | Order | Rationale |
|----------|-----|-------|-----------|
| 1 | remaining_capacity | DESC | 負荷分散 |
| 2 | room_code | ASC | 決定性保証 |

```
remaining_capacity = (staff_count * shift_hours * 60) - already_assigned_minutes
```

**制約チェック:**
1. allowed_rooms に含まれる作業室のみ
2. remaining_capacity >= duration_minutes
3. staff_count >= required_staff

配置失敗時: PSO-W004 アラートを出力、タスクを「未配置」リストに追加

### Step 5: Time Slot Assignment

```
start_time = room_day_next_available[room][day]  # default: 08:00 (480min)
end_time = start_time + duration_minutes
room_day_next_available[room][day] = end_time
```

> **Detail**: Load `references/scheduling_methodology.md` for improvement techniques and constraint patterns.
> **Template**: Use `assets/schedule_template.md` for output formatting.

---

## Workflow 3: Staff Requirement Estimation

**Purpose**: 作業室×曜日ごとの必要人員を算出し推奨人員を提案する。

### Calculation Pipeline: staff-hours -> peak -> min -> recommended

**Step 1**: 作業室×曜日ごとの必要人時を集計
```
room_day_staff_hours[room][day] = sum(task.staff_hours for task in assigned_tasks[room][day])
```

**Step 2**: 時間帯別の同時必要人数からピーク値を算出
```
peak_staff[room][day] = max(concurrent_staff_at_time_t for t in all_time_slots)
```

**Step 3**: min_staff = peak_staff（削減不可の最低ライン）

**Step 4**: バッファ係数を適用
```
recommended_staff = ceil(min_staff * 1.1)
```
- 10%バッファ: 急な欠勤、トラブル、清掃時間を吸収
- max_staff 超過時は max_staff にクランプ + PSO-W005 アラート

**Step 5**: Gap分析
```
gap = recommended_staff - current_staff  # >0:不足, 0:適正, <0:余剰
```

### Output Example

| Room | Day | Current | Peak | Min | Recommended | Gap | Status |
|------|-----|---------|------|-----|-------------|-----|--------|
| BAKERY | MON | 3 | 2 | 2 | 3 | 0 | OK |
| BROTH | MON | 2 | 3 | 3 | 4 | +2 | SHORTAGE |

> **Detail**: Load `references/staff_planning_guide.md` for shift patterns and labor constraints.

---

## Workflow 4: Shift Planning & Coverage Verification

> **Note**: This workflow provides guidance for manual implementation. No automated script is provided. Use the output from Workflow 3 as input for shift design.

**Purpose**: 推奨人員に基づくシフト自動生成と時間帯別カバレッジ検証。

### Shift Patterns

| Pattern | Start | End | Break | Net Hours |
|---------|-------|-----|-------|-----------|
| FULL_8H | 08:00 | 17:00 | 12:00-13:00 | 8.0h |
| EARLY_8H | 06:00 | 15:00 | 11:00-12:00 | 8.0h |
| LATE_8H | 10:00 | 19:00 | 14:00-15:00 | 8.0h |
| SHORT_6H | 08:00 | 14:00 | None | 6.0h |
| HALF_4H | 08:00 | 12:00 | None | 4.0h |

### Auto-Assignment

1. 平日: FULL_8H 優先、土日: SHORT_6H 優先
2. ピーク時間帯に HALF_4H を追加検討

### Coverage Verification

時間帯別（1時間刻み）で assigned >= required を検証:
```
for hour in [06:00..19:00]:
    if assigned_staff(hour) < required_staff(hour):
        alert PSO-W006: Coverage gap at {room} {day} {hour}
```

### Gap Resolution

1. **シフト追加**: ギャップ時間帯をカバーするパターン追加
2. **シフト変更**: 既存シフトの時刻調整
3. **作業移動**: タスクを別時間帯・曜日に移動

> **Detail**: Load `references/staff_planning_guide.md` for detailed shift design and labor constraints.

---

## Workflow 5: Validation, Alerts & Improvement

**Purpose**: スケジュール全体の品質検証、アラート集約、改善提案。

### Alert System

**Error (PSO-E): 処理停止**

| Code | Trigger | Description |
|------|---------|-------------|
| PSO-E001 | shelf_life_days <= 0 | 賞味期限が無効 |
| PSO-E002 | base_qty <= 0 | 基準数量が無効 |
| PSO-E003 | prep_time_min <= 0 | 調理時間が無効 |
| PSO-E004 | required_staff <= 0 | 必要人員が無効 |
| PSO-E005 | max_staff <= 0 | 作業室最大人員が無効 |
| PSO-E006 | Unknown room_code | 作業室コード不在 |

**Warning (PSO-W): 処理継続**

| Code | Trigger | Description |
|------|---------|-------------|
| PSO-W001 | qty <= 0 | 需要0以下（スキップ） |
| PSO-W002 | qty NaN/missing | 需要欠損（スキップ） |
| PSO-W003 | staff_count missing | 人員欠損（0に補完） |
| PSO-W004 | Capacity overflow | 全作業室で容量不足（未配置） |
| PSO-W005 | recommended > max_staff | 推奨人員超過（クランプ） |
| PSO-W006 | Coverage gap | カバレッジ不足 |

### Quality Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Room Utilization | used_hours / available_hours (per room/day) | 70-85% |
| Staff Efficiency | required_staff_hours / assigned_staff_hours | 80-90% |
| Completeness | assigned_demand / total_demand | 100% |
| Balance Score | 1 - std_dev(utilizations) / mean(utilizations) | >= 0.8 |

### Bottleneck Identification

1. **容量ボトルネック**: utilization > 90% の作業室×曜日
2. **人員ボトルネック**: gap > 0（Workflow 3結果）
3. **カバレッジボトルネック**: PSO-W006 発生時間帯
4. **未配置タスク**: PSO-W004 で未配置のタスク

### Improvement Suggestions

| Bottleneck Type | Suggestion |
|-----------------|------------|
| 容量 | タスク別曜日移動、稼働時間延長、別作業室振替 |
| 人員 | シフト追加、パートタイム活用、時間帯分散 |
| カバレッジ | シフト時間帯変更、タスク開始時刻調整 |
| 未配置 | 作業室追加、休日製造検討、外部委託 |

---

## Inline Formulas

### Production Frequency

```
production_count = min(ceil(7 / shelf_life_days), 7)
```
前提: shelf_life_days > 0（PSO-E001でバリデーション済み）

### Manufacturing Duration

```
duration_minutes = ceil(qty_per_run / base_qty) * prep_time_min
```
前提: base_qty > 0（PSO-E002でバリデーション済み）。端数ロットも1ロット分の時間。

### Staff-Hours

```
staff_hours = (duration_minutes * required_staff) / 60
```

### Recommended Staff

```
recommended_staff = ceil(min_staff * 1.1)
```
min_staff=ピーク時最低人数、1.1=バッファ係数、ceil=切り上げ

### Room Remaining Capacity

```
remaining_capacity_min = (staff_count * shift_hours * 60) - assigned_minutes
```

---

## Scripts

### generate_schedule.py

```bash
python3 skills/production-schedule-optimizer/scripts/generate_schedule.py \
  --products products.csv --demand demand.csv \
  --rooms rooms.csv --staff staff.csv \
  --week-start 2026-02-23 \
  --work-hours 8:00-22:00 --lunch-break 12:00-13:00 \
  --output schedule.md
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| --products | Yes | - | 製品マスタCSV |
| --demand | Yes | - | 週次需要CSV |
| --rooms | Yes | - | 作業室マスタCSV |
| --staff | Yes | - | 人員配置CSV |
| --week-start | Yes | - | 週開始日（YYYY-MM-DD） |
| --work-hours | No | 8:00-22:00 | 稼働時間帯（HH:MM-HH:MM） |
| --lunch-break | No | 12:00-13:00 | 休憩時間帯（HH:MM-HH:MM） |
| --output | No | stdout | 出力先（Markdown） |

### estimate_staff.py

```bash
python3 skills/production-schedule-optimizer/scripts/estimate_staff.py \
  --products products.csv --demand demand.csv \
  --rooms rooms.csv --shift-hours 8 \
  --output staff_report.md
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| --products | Yes | - | 製品マスタCSV |
| --demand | Yes | - | 週次需要CSV |
| --rooms | Yes | - | 作業室マスタCSV |
| --shift-hours | No | 8 | 1人あたりシフト時間 |
| --output | No | stdout | 出力先（Markdown） |

---

## Resources

### references/

| File | Description | When to Load |
|------|-------------|--------------|
| `references/scheduling_methodology.md` | Bin-Packing詳細、ソート仕様、改善手法 | アルゴリズム改善検討時 |
| `references/food_production_guide.md` | 製造頻度、FEFO、HACCP考慮事項 | 食品製造制約検討時 |
| `references/staff_planning_guide.md` | 人員計算、シフト設計、カバレッジ検証 | 人員計画・シフト設計時 |

### assets/

| File | Description |
|------|-------------|
| `assets/schedule_template.md` | 週次スケジュール出力テンプレート |
| `assets/sample_products.csv` | 製品マスタサンプル（10製品） |
| `assets/sample_demand.csv` | 週次需要サンプル |
| `assets/sample_rooms.csv` | 作業室マスタサンプル（5室） |
| `assets/sample_staff.csv` | 人員配置サンプル（7日x5室） |

---

## Best Practices

### 入力データ準備

1. **製品コード命名**: カテゴリ+連番（BREAD-001, SAUCE-002）で管理性向上
2. **賞味期限の正確性**: 製造日を含む日数で指定（製造当日=1日）
3. **需要数量**: 週次合計を指定（日次ではない）

### スケジュール最適化

1. **大タスク優先**: Bin-Packing原則。手動調整時も同様
2. **FEFO準拠**: 賞味期限短い製品を先に配置
3. **Cross-training**: 複数room_codesで柔軟な配置を可能に
4. **土日負荷軽減**: 短時間シフトの土日は平日集約を検討

### 人員計画

1. **バッファ係数調整**: 安定現場=1.05x、標準=1.1x、新人多=1.2x
2. **ピーク分散**: 開始時刻をずらして人員平準化
3. **パートタイム活用**: HALF_4Hでフルタイム人員を抑制
4. **月次レビュー**: 需要変動に対応した定期見直し

### アラート対応

1. **PSO-E**: 即時対応（データ品質は後続処理に影響）
2. **PSO-W004**: 優先対応（未配置=供給不足）
3. **Balance Score < 0.7**: タスク配置再検討を推奨
4. **週次振り返り**: 実績と計画差異を次週パラメータに反映

---

このスキルの目的は、製造施設の生産スケジュール作成を自動化・最適化し、作業室と人員の効率的な活用を支援することです。
