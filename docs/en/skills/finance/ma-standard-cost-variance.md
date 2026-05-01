---
layout: default
title: "MA Standard Cost Variance"
grand_parent: English
parent: Finance & Analysis
nav_order: 13
lang_peer: /ja/skills/finance/ma-standard-cost-variance/
permalink: /en/skills/finance/ma-standard-cost-variance/
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

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ma-standard-cost-variance.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ma-standard-cost-variance){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Analyzes the differences between standard (planned) and actual costs, decomposing variances into price and quantity components. Identifies responsible departments and provides root cause hypotheses for manufacturing cost management.

---

## 2. Prerequisites

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

---

## 3. Quick Start

1. **Validate Input Format**: Verify CSV structure and required columns
2. **Classify Cost Items**: Confirm cost category assignments (material/labor/overhead)
3. **Verify Standard Costs**: Ensure standard costs reflect current approved standards
4. **Handle Edge Cases**: Address zero quantities, missing prices, and new items without standards

---

## 4. How It Works

1. **Validate Input Format**: Verify CSV structure and required columns
2. **Classify Cost Items**: Confirm cost category assignments (material/labor/overhead)
3. **Verify Standard Costs**: Ensure standard costs reflect current approved standards
4. **Handle Edge Cases**: Address zero quantities, missing prices, and new items without standards

---

## 5. Usage Examples

- **Monthly Cost Variance Reporting** - Analyze standard vs. actual cost differences for manufacturing operations
- 「今月の原価差異を分析して」「標準原価との乖離を計算して」
- **Cost Reduction Effectiveness Measurement** - Evaluate whether cost reduction initiatives achieved target
- 「原価低減活動の効果を測定して」「コスト削減の進捗を確認して」
- **Procurement Price Monitoring** - Track material price variances against standards
- 「材料の価格差異を確認して」「仕入価格の変動を分析して」

---

## 6. Understanding the Output

The analysis produces a structured cost variance report containing:

1. **Executive Summary**: Total variance by category, key highlights
2. **Item-Level Detail**: Price variance, quantity variance, and total per item with calculation basis
3. **Category Subtotals**: Aggregated variances by material/labor/overhead
4. **Responsibility Matrix**: Variance amounts mapped to responsible departments
5. **Root Cause Analysis**: Hypotheses and recommended actions for major variances

Output template: `assets/cost_variance_report_template_ja.md` (Japanese) or `assets/cost_variance_report_template_en.md` (English)

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/ma-standard-cost-variance/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: 第11回_ABCで見える店舗別損益管理の真実_20251213.md, 第12回_予定原価という考え方_20260122.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/finance/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.

---

## 10. Reference

**References:**

- `skills/ma-standard-cost-variance/references/第11回_ABCで見える店舗別損益管理の真実_20251213.md`
- `skills/ma-standard-cost-variance/references/第12回_予定原価という考え方_20260122.md`
