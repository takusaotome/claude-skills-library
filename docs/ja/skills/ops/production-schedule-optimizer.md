---
layout: default
title: "Production Schedule Optimizer"
grand_parent: 日本語
parent: 運用・ドキュメント
nav_order: 11
lang_peer: /en/skills/ops/production-schedule-optimizer/
permalink: /ja/skills/ops/production-schedule-optimizer/
---

# Production Schedule Optimizer
{: .no_toc }

製造施設（セントラルキッチン、食品工場、製造ライン）の週次生産スケジュールを最適化するスキル。
製品の賞味期限、作業室の容量、人員配置、設備制約を考慮したタイムテーブル生成、
人員要件見積、シフト計画、カバレッジ検証を提供。
Use when: 「製造スケジュールを作成」「生産計画を最適化」「人員配置を見積もり」
「CK スケジュール」「週次製造計画」「シフト計画」

{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/production-schedule-optimizer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/production-schedule-optimizer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

製造施設（セントラルキッチン、食品工場など）の週次生産スケジュールを自動生成・最適化するスキル。
4種類のCSV（製品マスタ、需要、作業室、人員）を入力とし、賞味期限に基づく製造頻度、作業室容量、人員制約を考慮した週次タイムテーブルを生成する。

**Primary language**: Japanese (default), English supported
**Frameworks**: Greedy Bin-Packing (Largest-First Decreasing), FEFO, HACCP-aware room assignment
**Output format**: Weekly schedule (Markdown table), staff reports, shift plans, alert summaries

---

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- Python 3.9+
- 外部依存なし（標準ライブラリのみ）
- 入力CSVはUTF-8エンコーディング
- 4種類のCSVファイル（products, demand, rooms, staff）を事前準備

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
production_count = min(ceil(7 / shelf_life_days), 7)
qty_per_run      = ceil(qty / production_count)
lot_count        = ceil(qty_per_run / base_qty)
duration_minutes = lot_count * prep_time_min
staff_hours      = (duration_minutes * required_staff) / 60
total_staff_hours = staff_hours * production_count
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

- `skills/production-schedule-optimizer/references/food_production_guide.md`
- `skills/production-schedule-optimizer/references/scheduling_methodology.md`
- `skills/production-schedule-optimizer/references/staff_planning_guide.md`

**Scripts:**

- `skills/production-schedule-optimizer/scripts/estimate_staff.py`
- `skills/production-schedule-optimizer/scripts/generate_schedule.py`
