---
layout: default
title: "Contract Reviewer"
grand_parent: 日本語
parent: プロジェクト・経営
nav_order: 10
lang_peer: /en/skills/management/contract-reviewer/
permalink: /ja/skills/management/contract-reviewer/
---

# Contract Reviewer
{: .no_toc }

Professional contract review skill for business agreements including NDAs, MSAs, SLAs, SOWs, and software license agreements. Provides systematic clause-by-clause analysis, risk assessment with quantified scoring, red flag detection, and negotiation guidance. Use this skill when reviewing vendor contracts, partnership agreements, service agreements, or any business contract requiring risk evaluation and negotiation preparation. Triggers include "review this contract", "analyze this NDA", "check this agreement for risks", "prepare for contract negotiation", or when evaluating terms and conditions.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/contract-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/contract-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

This skill provides a structured methodology for reviewing business contracts from a risk and negotiation perspective. It helps identify unfavorable terms, quantify risks, and prepare negotiation strategies.

**Important Disclaimer**: This skill provides business-focused contract analysis, NOT legal advice. Always consult qualified legal counsel for binding decisions and jurisdiction-specific requirements.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- **Python 3.9+**: Required for running analysis scripts
- **PyPDF2** (optional): Install with `pip install PyPDF2` for PDF document support
- **Contract Document**: Text file (.txt, .md) or PDF file (.pdf) containing the contract
- **No Legal Advice**: This skill provides business analysis; always consult legal counsel for binding decisions

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

**Purpose**: Quickly assess the contract and determine the appropriate review depth.
**Duration**: 15-30 minutes

### Step 1.1: Contract Classification

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

- `skills/contract-reviewer/references/clause_analysis_guide.md`
- `skills/contract-reviewer/references/contract_review_methodology.md`
- `skills/contract-reviewer/references/negotiation_strategies.md`
- `skills/contract-reviewer/references/red_flag_patterns.md`
- `skills/contract-reviewer/references/risk_assessment_framework.md`

**Scripts:**

- `skills/contract-reviewer/scripts/analyze_contract.py`
- `skills/contract-reviewer/scripts/pattern_definitions.py`
