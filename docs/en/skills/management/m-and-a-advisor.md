---
layout: default
title: "M And A Advisor"
grand_parent: English
parent: Project & Business
nav_order: 16
lang_peer: /ja/skills/management/m-and-a-advisor/
permalink: /en/skills/management/m-and-a-advisor/
---

# M And A Advisor
{: .no_toc }

M&Aアドバイザリー支援スキル。デューデリジェンス（DD）実施、企業価値評価（バリュエーション）、
シナジー分析、PMI（Post Merger Integration）計画策定を包括的に支援。
Use when conducting M&A due diligence (Financial, Legal, IT, HR), company valuation
(DCF, Comparable Companies, Precedent Transactions), synergy analysis, or post-merger
integration planning.
Triggers: "M&A", "デューデリジェンス", "DD", "バリュエーション", "企業価値評価", "DCF",
"comparable", "類似企業", "先行取引", "PMI", "統合計画", "シナジー分析", "買収", "合併"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/m-and-a-advisor.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/m-and-a-advisor){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

M&Aアドバイザリー業務を包括的に支援するスキル。デューデリジェンス（DD）の実施から企業価値評価、シナジー分析、PMI計画策定まで、M&Aプロセス全体をカバー。

**主要機能:**
1. **デューデリジェンス（DD）** - 財務/法務/IT/HR の4領域 + 業種別DD
2. **バリュエーション** - DCF/類似企業比較/先行取引分析の3手法
3. **シナジー分析** - コスト/収益シナジーの定量化
4. **PMI計画** - 統合計画の策定と実行支援

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
□ 財務DD (Financial Due Diligence)
□ 法務DD (Legal Due Diligence)
□ IT DD (IT/Technology Due Diligence)
□ 人事DD (HR Due Diligence)
□ 業種別DD (Industry-Specific DD)
```

---

## 4. How It Works

### Step 1.1: DDスコープ定義

**対象領域の特定:**
```
□ 財務DD (Financial Due Diligence)
□ 法務DD (Legal Due Diligence)
□ IT DD (IT/Technology Due Diligence)
□ 人事DD (HR Due Diligence)
□ 業種別DD (Industry-Specific DD)
```

**業種別DD選択:**
- IT・ソフトウェア業 → `references/dd-industry/it_software_dd.md`
- 製造業 → `references/dd-industry/manufacturing_dd.md`
- 金融・保険業 → `references/dd-industry/financial_services_dd.md`
- 小売・消費財 → `references/dd-industry/retail_consumer_dd.md`

### Step 1.2: 各領域のDD実施

**財務DD** (`references/dd-checklists/financial_dd_checklist.md`):
1. 財務諸表分析（過去3-5年）
2. 収益性・成長性分析
3. 運転資本・キャッシュフロー分析
4. 税務リスク評価

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Use **M And A Advisor** when you need a structured workflow rather than an ad-hoc answer.
- Start with a small representative input before applying the workflow to production data or assets.
- Review the helper scripts and reference guides to tailor the output format to your project.

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 2 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/m-and-a-advisor/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: synergy_analysis_guide.md, pmi_framework.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: valuation_calculator.py.
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

- `skills/m-and-a-advisor/references/pmi_framework.md`
- `skills/m-and-a-advisor/references/synergy_analysis_guide.md`

**Scripts:**

- `skills/m-and-a-advisor/scripts/valuation_calculator.py`
