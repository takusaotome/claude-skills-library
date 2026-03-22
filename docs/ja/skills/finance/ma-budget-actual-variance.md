---
layout: default
title: "MA Budget Actual Variance"
grand_parent: 日本語
parent: 財務・分析
nav_order: 11
lang_peer: /en/skills/finance/ma-budget-actual-variance/
permalink: /ja/skills/finance/ma-budget-actual-variance/
---

# MA Budget Actual Variance
{: .no_toc }

予算実績差異分析スキル。勘定科目タイプ（収益/費用）に応じた有利・不利差異の自動判定、
差異の分解（価格差異・数量差異）、重要度ランキング、根本原因の仮説提示を行う。
CSVデータのアップロードによる自動分析に対応。

Use when: 予算と実績の比較分析を行いたいとき。月次・四半期の予実管理レポート作成、
差異の原因分析、経営会議向けの予実サマリ作成に使用。

Triggers: "予実差異", "予算実績", "budget variance", "budget vs actual",
"予算対比", "差異分析", "variance analysis"

{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ma-budget-actual-variance.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ma-budget-actual-variance){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

Analyzes the differences between budgeted and actual figures, identifying favorable and unfavorable variances with account-type awareness. Provides materiality ranking, root cause hypotheses, and actionable recommendations for management decision-making.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

Before running this skill, ensure the following data is available:

- **Budget Data**: Approved budget figures by account (CSV or manual input)
- **Actual Data**: Actual performance figures for the same period
- **Account Classification**: Each account must be classified as `revenue` or `cost`/`expense`
- **Period Information**: Target analysis period (month, quarter, or year)

### Required CSV Format

```csv
account_name,account_type,budget,actual
Sales Revenue,revenue,1000000,1200000
Material Cost,cost,400000,380000
Labor Cost,cost,300000,320000
```

**Required Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `account_name` | string | Account or line item name |
| `account_type` | string | `revenue` or `cost` (determines favorable/unfavorable logic) |
| `budget` | numeric | Budgeted amount |
| `actual` | numeric | Actual amount |

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

1. **Validate Input Format**: Verify CSV structure and required columns are present
2. **Classify Accounts**: Confirm account type assignments (revenue vs. cost/expense)
3. **Period Alignment**: Ensure budget and actual figures correspond to the same period
4. **Data Cleansing**: Handle missing values, zero budgets, and currency formatting

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

- `skills/ma-budget-actual-variance/references/第05回_その予算って根拠あるの_20250507.md`
- `skills/ma-budget-actual-variance/references/第08回_予算実績差異分析_20250820.md`
