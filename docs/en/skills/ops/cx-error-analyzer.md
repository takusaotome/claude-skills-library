---
layout: default
title: "CX Error Analyzer"
grand_parent: English
parent: Operations & Docs
nav_order: 6
lang_peer: /ja/skills/ops/cx-error-analyzer/
permalink: /en/skills/ops/cx-error-analyzer/
---

# CX Error Analyzer
{: .no_toc }

エラーや例外シナリオを顧客体験(CX)の観点で体系的に分析し、改善優先度を付ける スキル。6軸評価（影響度・頻度・復旧容易性・メッセージ品質・感情的影響・ ビジネスコスト）でスコアリングし、Impact vs Effort マトリクスで改善施策を 優先順位付けする。Use when analyzing error scenarios from customer experience perspective, evaluating error message quality, prioritizing error UX improvements, or creating CX-focused error analysis reports. Triggers: "CXエラー分析", "error experience", "エラーUX改善", "customer experience error", "エラーメッセージ品質", "error scenario analysis", "顧客体験エラー評価"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/cx-error-analyzer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/cx-error-analyzer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

CX Error Analyzer は、システムやアプリケーションのエラーシナリオを顧客体験（Customer Experience）の観点から体系的に分析・評価するスキルです。6軸の定量評価フレームワークにより、エラーが顧客体験に与える影響を可視化し、Impact vs Effort マトリクスで改善施策の優先順位を決定します。

---

## 2. Prerequisites

- **Error data**: Access to error logs, support tickets, or documented error scenarios
- **User journey map** (optional): Understanding of user flows helps contextualize error impact
- **Stakeholder access** (optional): Ability to interview developers, support staff, or QA for error pattern insights
- **Business metrics** (optional): Support cost data, churn rates, or CSAT scores for ROI estimation

---

## 3. Quick Start

```bash
CX Score = (Impact * 0.25) + (Frequency * 0.20) + (Recovery * 0.15)
            + (Message * 0.15) + (Emotional * 0.10) + (Business * 0.15)
```

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

- `skills/cx-error-analyzer/references/cx_evaluation_methodology.md`
- `skills/cx-error-analyzer/references/cx_metrics_reference.md`
- `skills/cx-error-analyzer/references/error_ux_best_practices.md`
