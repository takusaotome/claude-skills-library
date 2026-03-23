---
layout: default
title: "Shift Planner"
grand_parent: 日本語
parent: 運用・ドキュメント
nav_order: 12
lang_peer: /en/skills/ops/shift-planner/
permalink: /ja/skills/ops/shift-planner/
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

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/shift-planner.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/shift-planner){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

従業員リスト（roster）と人員要件（requirements）を入力として、制約充足型 Greedy Assignment で個人別シフトを自動編成するスキル。
production-schedule-optimizer の出力（人員要件）を活用可能だが、単体でも汎用的なシフト計画ツールとして動作する。

**Primary language**: Japanese (default), English supported
**Algorithm**: Constraint-Satisfaction Greedy Assignment (difficulty-first slot ordering)
**Output format**: Markdown report (shift table, coverage matrix, fairness report, alerts)
**Dependencies**: None (Python standard library only)

---

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- Python 3.9+
- 外部依存なし（標準ライブラリのみ: csv, math, argparse, dataclasses）
- 入力CSVはUTF-8エンコーディング

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
score = -(remaining_hours * 10)     # 契約残余多い=優先
           + (weekend_shifts * 20)      # 週末バランス
           + (avoid_penalty * 50)       # 回避曜日ペナルティ
           - (supervisor_bonus * 100)   # 監督者ボーナス
           - (speciality * 5)           # 資格専門度
           + (preference_miss * 30)     # 希望パターン不一致
```

<!-- TODO: 翻訳 -->

---

## 4. 仕組み

<!-- TODO: 翻訳 -->

---

## 5. 使用例

<!-- TODO: 翻訳 -->

---

## 6. 出力の読み方

<!-- TODO: 翻訳 -->

---

## 7. Tips & ベストプラクティス

<!-- TODO: 翻訳 -->

---

## 8. 他スキルとの連携

<!-- TODO: 翻訳 -->

---

## 9. トラブルシューティング

<!-- TODO: 翻訳 -->

---

## 10. リファレンス

**References:**

- `skills/shift-planner/references/labor_constraints_guide.md`
- `skills/shift-planner/references/shift_planning_methodology.md`

**Scripts:**

- `skills/shift-planner/scripts/generate_shifts.py`
