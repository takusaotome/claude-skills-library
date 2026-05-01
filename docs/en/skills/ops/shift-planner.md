---
layout: default
title: "Shift Planner"
grand_parent: English
parent: Operations & Docs
nav_order: 12
lang_peer: /ja/skills/ops/shift-planner/
permalink: /en/skills/ops/shift-planner/
---

# Shift Planner
{: .no_toc }

従業員リスト（勤務可能時間帯・曜日・資格等の制約条件付き）と人員要件（作業室×曜日×時間帯の必要人員）を入力として、
個人別シフトを自動編成するスキル。制約充足型 Greedy Assignment アルゴリズムにより、
ハード制約（労働時間上限、連続勤務制限、休息時間、資格マッチング）を遵守しつつ、
公平性（週末均等配分、時間偏差）を考慮したシフト表を生成する。
カバレッジ検証（30分刻み）と公平性レポートも自動出力。
Use when: 「シフトを作成」「従業員のシフト編成」「勤務表を自動生成」
「人員配置のシフト計画」「週次シフトスケジュール」「shift schedule」

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/shift-planner.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/shift-planner){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

従業員リスト（roster）と人員要件（requirements）を入力として、制約充足型 Greedy Assignment で個人別シフトを自動編成するスキル。
production-schedule-optimizer の出力（人員要件）を活用可能だが、単体でも汎用的なシフト計画ツールとして動作する。

**Primary language**: Japanese (default), English supported
**Algorithm**: Constraint-Satisfaction Greedy Assignment (difficulty-first slot ordering)
**Output format**: Markdown report (shift table, coverage matrix, fairness report, alerts)
**Dependencies**: None (Python standard library only)

---

---

## 2. Prerequisites

- Python 3.9+
- 外部依存なし（標準ライブラリのみ: csv, math, argparse, dataclasses）
- 入力CSVはUTF-8エンコーディング

---

## 3. Quick Start

```bash
score = -(remaining_hours * 10)     # 契約残余多い=優先
           + (weekend_shifts * 20)      # 週末バランス
           + (avoid_penalty * 50)       # 回避曜日ペナルティ
           - (supervisor_bonus * 100)   # 監督者ボーナス
           - (speciality * 5)           # 資格専門度
           + (preference_miss * 30)     # 希望パターン不一致
```

---

## 4. How It Works

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

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- 従業員の個人別シフト表を自動生成したい
- 勤務可能曜日・時間帯・資格などの制約を考慮したシフト編成が必要
- production-schedule-optimizer で算出した人員要件に基づくシフト計画を立てたい
- シフトのカバレッジ（時間帯別充足状況）を検証したい
- 従業員間の公平性（労働時間偏差、週末シフト配分）を分析したい
- 監督者配置要件を含むシフト計画が必要

---

## 6. Understanding the Output

- **形式**: Markdown レポート（4セクション構成）
- **内容**:
  1. シフト割当表（曜日別）
  2. カバレッジマトリクス（30分刻み）
  3. 公平性レポート（従業員別）
  4. アラート一覧

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/shift-planner/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: shift_planning_methodology.md, labor_constraints_guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: generate_shifts.py.
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

- `skills/shift-planner/references/labor_constraints_guide.md`
- `skills/shift-planner/references/shift_planning_methodology.md`

**Scripts:**

- `skills/shift-planner/scripts/generate_shifts.py`
