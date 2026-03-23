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

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

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
