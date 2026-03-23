---
layout: default
title: "MA Standard Cost Variance"
grand_parent: 日本語
parent: 財務・分析
nav_order: 13
lang_peer: /en/skills/finance/ma-standard-cost-variance/
permalink: /ja/skills/finance/ma-standard-cost-variance/
---

# MA Standard Cost Variance
{: .no_toc }

標準原価差異分析スキル。標準原価（予定原価）と実際原価の差異を価格差異・数量差異に分解し、
材料費・労務費・製造間接費のカテゴリ別に集計・分析する。差異の有利/不利判定、
責任部門の特定、根本原因の仮説提示を行う。CSVデータのアップロードによる自動分析に対応。

Use when: 製造原価の差異分析を行いたいとき。標準原価計算制度の運用、
月次原価差異レポート作成、原価低減活動の効果測定に使用。

Triggers: "標準原価", "原価差異", "価格差異", "数量差異", "standard cost",
"cost variance", "price variance", "quantity variance", "予定原価",
"操業度差異", "原価管理"

{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ma-standard-cost-variance.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ma-standard-cost-variance){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

Analyzes the differences between standard (planned) and actual costs, decomposing variances into price and quantity components. Identifies responsible departments and provides root cause hypotheses for manufacturing cost management.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

Before running this skill, ensure the following data is available:

- **Standard Cost Data**: Standard price and standard quantity per item
- **Actual Cost Data**: Actual price and actual quantity per item
- **Cost Category Classification**: Each item classified as `material`, `labor`, or `overhead`
- **Period Information**: Target analysis period

### Required CSV Format

```csv
item_name,cost_category,standard_price,actual_price,standard_quantity,actual_quantity
Eggs,material,2.50,3.20,100,105
Line Worker,labor,25.00,26.50,40,42
Equipment Depreciation,overhead,5000,5000,1,1
```

**Required Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `item_name` | string | Cost item name |
| `cost_category` | string | `material`, `labor`, or `overhead` |
| `standard_price` | numeric | Standard (planned) unit price |
| `actual_price` | numeric | Actual unit price |
| `standard_quantity` | numeric | Standard quantity for actual output |
| `actual_quantity` | numeric | Actual quantity consumed |

### Cost Categories

- **material**: Raw materials and components (e.g., flour, eggs, packaging)
- **labor**: Direct labor (e.g., line workers, supervisors)
- **overhead**: Manufacturing overhead (e.g., depreciation, utilities, maintenance)

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

1. **Validate Input Format**: Verify CSV structure and required columns
2. **Classify Cost Items**: Confirm cost category assignments (material/labor/overhead)
3. **Verify Standard Costs**: Ensure standard costs reflect current approved standards
4. **Handle Edge Cases**: Address zero quantities, missing prices, and new items without standards

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

- `skills/ma-standard-cost-variance/references/第11回_ABCで見える店舗別損益管理の真実_20251213.md`
- `skills/ma-standard-cost-variance/references/第12回_予定原価という考え方_20260122.md`
