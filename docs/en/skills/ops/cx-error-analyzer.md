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

### Workflow 1: Error Scenario Inventory（エラーシナリオ棚卸し）

Enumerate and classify all error scenarios in the target system or feature.

1. **List all error scenarios** in the system or feature under analysis
   - Review source code, API documentation, and existing error logs
   - Interview stakeholders (developers, support, QA) for known error patterns
   - Examine user feedback and support ticket data for unreported errors
2. **Classify each error** into one of 6 categories:
   - **Validation**: Input format, required fields, range limits
   - **System**: Server errors, database failures, memory issues
   - **Network**: Timeout, connection loss, DNS failure
   - **Auth**: Authentication failure, session expiry, permission denied
   - **Business Logic**: Rule violations, state conflicts, limit exceeded
   - **External**: Third-party API failures, payment gateway errors, integration issues
3. **Map each error to a user journey stage**:
   - Discovery (browsing, searching)
   - Onboarding (registration, initial setup)
   - Core Task (primary feature usage)
   - Checkout (purchase, submission, completion)
   - Support (help, account management)
4. **Assign error IDs**: ERR-001, ERR-002, ERR-003...
5. **Capture current state** for each error:
   - Current error message text (exact wording)

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- エラーシナリオの顧客体験を評価するとき
- エラーメッセージの品質を改善するとき
- エラー改善の優先順位を付けるとき
- CX観点でのエラーハンドリング改善レポートを作成するとき
- エラー体験の定量的評価を行うとき
- 新機能リリース前にエラーシナリオのCXレビューを実施するとき

---

## 6. Understanding the Output

This skill provides **conversational guidance and analysis** rather than file generation. Outputs include:

- Structured error scenario inventories with classifications
- Multi-axis CX evaluation scores with rationale
- Prioritized improvement recommendations (Quick Wins, Strategic Projects)
- Before/after error message comparisons
- ROI estimates and business impact projections

When formal documentation is needed, use Workflow 5 to generate a comprehensive report using the provided templates.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/cx-error-analyzer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: error_ux_best_practices.md, cx_metrics_reference.md, cx_evaluation_methodology.md.
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

---

## 10. Reference

**References:**

- `skills/cx-error-analyzer/references/cx_evaluation_methodology.md`
- `skills/cx-error-analyzer/references/cx_metrics_reference.md`
- `skills/cx-error-analyzer/references/error_ux_best_practices.md`
