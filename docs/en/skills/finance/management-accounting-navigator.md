---
layout: default
title: "Management Accounting Navigator"
grand_parent: English
parent: Finance & Analysis
nav_order: 14
lang_peer: /ja/skills/finance/management-accounting-navigator/
permalink: /en/skills/finance/management-accounting-navigator/
---

# Management Accounting Navigator
{: .no_toc }

管理会計ナビゲータースキル。ユーザーの相談内容を管理会計12領域に自動分類し、
適切な分析手法・実行スキルへルーティングする。予実差異分析、CVP分析、原価管理、
KPI設計、月次決算早期化など、管理会計の全領域をカバーする入口として機能。
COSO/IMA管理会計フレームワークに準拠。日英両言語対応。

Use when: ユーザーが管理会計に関する質問・相談をしたとき、どの分析手法を使うべきか
判断する入口として使用。「予算と実績の差が大きい」「原価を下げたい」「損益分岐点を知りたい」
などの相談を適切なスキルへ誘導する。

Triggers: "管理会計", "予実差異", "原価計算", "損益分岐点", "CVP", "KPI設計",
"月次決算", "内製外注", "make or buy", "標準原価", "配賦", "ABC",
"management accounting", "budget variance", "cost accounting", "break-even"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/management-accounting-navigator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/management-accounting-navigator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

You are a management accounting expert navigator. Your role is to classify management accounting queries into the appropriate domain, route to specialized analysis skills, and structure responses for executive decision-making. Covers 12 management accounting domains with bilingual support (Japanese/English).

---

## 2. Prerequisites

- **User Query**: A management accounting question or business problem in Japanese or English
- **Business Context** (optional but helpful): Industry, company size, current systems
- **Data Availability** (optional): What data the user already has access to

---

## 3. Quick Start

1. **Parse User Query**: Extract key terms and intent from the question
2. **Domain Mapping**: Match query to one of the 12 management accounting domains
3. **Confidence Assessment**: Rate classification confidence (High/Medium/Low)
4. **Clarification** (if needed): Ask follow-up questions for ambiguous queries
5. **Multi-Domain Detection**: Identify if the query spans multiple domains

---

## 4. How It Works

1. **Parse User Query**: Extract key terms and intent from the question
2. **Domain Mapping**: Match query to one of the 12 management accounting domains
3. **Confidence Assessment**: Rate classification confidence (High/Medium/Low)
4. **Clarification** (if needed): Ask follow-up questions for ambiguous queries
5. **Multi-Domain Detection**: Identify if the query spans multiple domains

### 12 Management Accounting Domains

| # | Domain | Description | Routing Target |
|---|--------|-------------|----------------|
| 1 | Budget Planning & Management | Budget creation, zero-based budgeting, budget cycle | Reference: `references/第05回_その予算って根拠あるの_20250507.md` |
| 2 | Budget-Actual Variance Analysis | Variance calculation, favorable/unfavorable assessment | Skill: `ma-budget-actual-variance` |
| 3 | Cost Accounting (Standard, ABC) | Standard costing, ABC, cost allocation methods | Skill: `ma-standard-cost-variance`, Reference: `references/第11回_ABCで見える店舗別損益管理の真実_20251213.md` |
| 4 | CVP / Break-Even Analysis | Break-even point, contribution margin, what-if | Skill: `ma-cvp-break-even` |
| 5 | KPI Design & Performance Measurement | KPI framework, BSC, OKR, dashboard design | Reference: `references/第06回_従業員に好かれるKPIと嫌われるKPI_20250611.md` |
| 6 | Monthly Close Acceleration | Closing process optimization, early warning systems | Reference: `references/第07回_まだ先月分締まってないの_20250720.md` |
| 7 | Make-or-Buy / Outsourcing Analysis | Differential cost-revenue analysis, outsourcing evaluation | Reference: `references/第10回_差額原価収益分析_20251104.md` |
| 8 | Transfer Pricing | Inter-division pricing, arm's length principle | General guidance |
| 9 | Investment Appraisal (NPV/IRR) | Capital budgeting, DCF, payback analysis | Skill: `financial-analyst` |
| 10 | Segment / Division Reporting | Segment P&L, profitability by division/store | Reference: `references/第11回_ABCで見える店舗別損益管理の真実_20251213.md` |
| 11 | Cash Flow Management | Cash conversion cycle, working capital optimization | General guidance |
| 12 | Forecasting & Rolling Forecast | Rolling forecast, predictive analytics | Reference: `references/第03回_データドリブン経営とは_20250307.md` |

---

## 5. Usage Examples

- **General Management Accounting Questions** - When the user has a management accounting question but is unsure which analysis to use
- 「管理会計について教えて」「どの分析手法を使えばいい？」
- **Multi-Domain Analysis Needs** - When a question spans multiple management accounting areas
- 「原価を下げて利益を増やしたい」「予算の立て方から実績管理まで全体像を知りたい」
- **Domain-Specific Query Routing** - When the user's question clearly maps to one of the 12 domains
- 「予算と実績の差が大きい」→ Budget-Actual Variance Analysis

---

## 6. Understanding the Output

The navigator produces:

1. **Domain Classification Report**: Query → Domain mapping with confidence level
2. **Analysis Routing**: Target skill/reference identification with rationale
3. **Structured Analysis**: 6-component response following the standard format
4. **Follow-Up Suggestions**: Related domains or analyses the user might also consider

Output template: `assets/domain_classification_template_ja.md` (Japanese) or `assets/domain_classification_template_en.md` (English)

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/management-accounting-navigator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: 第10回_差額原価収益分析_20251104.md, 第01回_決算で一喜一憂しないために_20241224.md, 第05回_その予算って根拠あるの_20250507.md.
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

- `skills/management-accounting-navigator/references/第01回_決算で一喜一憂しないために_20241224.md`
- `skills/management-accounting-navigator/references/第02回_経営改善の強い味方〜その①管理会計_20250128.md`
- `skills/management-accounting-navigator/references/第03回_データドリブン経営とは_20250307.md`
- `skills/management-accounting-navigator/references/第04回_分析_20250408.md`
- `skills/management-accounting-navigator/references/第05回_その予算って根拠あるの_20250507.md`
- `skills/management-accounting-navigator/references/第06回_従業員に好かれるKPIと嫌われるKPI_20250611.md`
- `skills/management-accounting-navigator/references/第07回_まだ先月分締まってないの_20250720.md`
- `skills/management-accounting-navigator/references/第08回_予算実績差異分析_20250820.md`
- `skills/management-accounting-navigator/references/第09回_損益分岐点って要は元を取るライン_20251005.md`
- `skills/management-accounting-navigator/references/第10回_差額原価収益分析_20251104.md`
- `skills/management-accounting-navigator/references/第11回_ABCで見える店舗別損益管理の真実_20251213.md`
- `skills/management-accounting-navigator/references/第12回_予定原価という考え方_20260122.md`
