---
layout: default
title: "Business Plan Creator"
grand_parent: English
parent: Project & Business
nav_order: 7
lang_peer: /ja/skills/management/business-plan-creator/
permalink: /en/skills/management/business-plan-creator/
---

# Business Plan Creator
{: .no_toc }

事業計画書を体系的に作成するスキル。新規事業、既存事業の拡大、スタートアップのピッチ資料、 社内新規プロジェクト提案など、あらゆる事業計画のドキュメントを構造化して作成する。 「事業計画」「ビジネスプラン」「business plan」「新規事業提案」「事業企画」「収支計画」 「プロジェクト提案書」「投資計画」「起業」「創業計画」などのキーワードが出たら必ずこのスキルを使用する。 事業のアイデア段階から、市場分析、競合分析、収支シミュレーション、リスク評価まで 包括的にカバーする。日本語・英語の両方に対応。

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/business-plan-creator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/business-plan-creator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

# 事業計画書作成スキル (Business Plan Creator)

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

Invoke this skill by describing your analysis needs to Claude.

---

## 4. How It Works

Follow the skill's SKILL.md workflow step by step, starting from a small validated input.

---

## 5. Usage Examples

- Use **Business Plan Creator** when you need a structured workflow rather than an ad-hoc answer.
- Start with a small representative input before applying the workflow to production data or assets.
- Review the helper scripts and reference guides to tailor the output format to your project.

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 3 guide file(s).
- Script-assisted execution using 2 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/business-plan-creator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: frameworks.md, industry-templates.md, financial-modeling.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: generate_outline.py, generate_financial_scenarios.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/management/' | relative_url }}).
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

- `skills/business-plan-creator/references/financial-modeling.md`
- `skills/business-plan-creator/references/frameworks.md`
- `skills/business-plan-creator/references/industry-templates.md`

**Scripts:**

- `skills/business-plan-creator/scripts/generate_financial_scenarios.py`
- `skills/business-plan-creator/scripts/generate_outline.py`
