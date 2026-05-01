---
layout: default
title: "Production Schedule Optimizer"
grand_parent: English
parent: Operations & Docs
nav_order: 11
lang_peer: /ja/skills/ops/production-schedule-optimizer/
permalink: /en/skills/ops/production-schedule-optimizer/
---

# Production Schedule Optimizer
{: .no_toc }

製造施設（セントラルキッチン、食品工場、製造ライン）の週次生産スケジュールを最適化するスキル。
製品の賞味期限、作業室の容量、人員配置、設備制約を考慮したタイムテーブル生成、
人員要件見積、シフト計画、カバレッジ検証を提供。
Use when: 「製造スケジュールを作成」「生産計画を最適化」「人員配置を見積もり」
「CK スケジュール」「週次製造計画」「シフト計画」

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/production-schedule-optimizer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/production-schedule-optimizer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

製造施設（セントラルキッチン、食品工場など）の週次生産スケジュールを自動生成・最適化するスキル。
4種類のCSV（製品マスタ、需要、作業室、人員）を入力とし、賞味期限に基づく製造頻度、作業室容量、人員制約を考慮した週次タイムテーブルを生成する。

**Primary language**: Japanese (default), English supported
**Frameworks**: Greedy Bin-Packing (Largest-First Decreasing), FEFO, HACCP-aware room assignment
**Output format**: Weekly schedule (Markdown table), staff reports, shift plans, alert summaries

---

---

## 2. Prerequisites

- Python 3.9+
- 外部依存なし（標準ライブラリのみ）
- 入力CSVはUTF-8エンコーディング
- 4種類のCSVファイル（products, demand, rooms, staff）を事前準備

---

## 3. Quick Start

```bash
production_count = min(ceil(7 / shelf_life_days), 7)
qty_per_run      = ceil(qty / production_count)
lot_count        = ceil(qty_per_run / base_qty)
duration_minutes = lot_count * prep_time_min
staff_hours      = (duration_minutes * required_staff) / 60
total_staff_hours = staff_hours * production_count
```

---

## 4. How It Works

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

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- セントラルキッチンや食品工場の週次製造スケジュールを作成したい
- 賞味期限ベースの製造頻度を自動計算したい
- 作業室の容量と人員制約を考慮した最適タイムテーブルが必要
- 人員要件を見積もり、シフト計画を立てたい
- 既存スケジュールのボトルネック特定と改善をしたい
- 複数作業室間の負荷バランスを最適化したい

---

## 6. Understanding the Output

### generate_schedule.py
- **形式**: Markdown テーブル（曜日別タイムテーブル + アラートセクション）
- **内容**: 曜日×作業室×製品ごとの開始時刻、終了時刻、数量、人員、所要時間

### estimate_staff.py
- **形式**: Markdown テーブル（曜日別人員要件）
- **内容**: 作業室×曜日ごとの必要人時、ピーク人員、最小人員、推奨人員、タスク数

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/production-schedule-optimizer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: staff_planning_guide.md, scheduling_methodology.md, food_production_guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: generate_schedule.py, estimate_staff.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/ops/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/production-schedule-optimizer/references/food_production_guide.md`
- `skills/production-schedule-optimizer/references/scheduling_methodology.md`
- `skills/production-schedule-optimizer/references/staff_planning_guide.md`

**Scripts:**

- `skills/production-schedule-optimizer/scripts/estimate_staff.py`
- `skills/production-schedule-optimizer/scripts/generate_schedule.py`
