---
layout: default
title: "AI Text Humanizer"
grand_parent: English
parent: Operations & Docs
nav_order: 4
lang_peer: /ja/skills/ops/ai-text-humanizer/
permalink: /en/skills/ops/ai-text-humanizer/
---

# AI Text Humanizer
{: .no_toc }

AI（LLM）が生成した日本語テキストの「AI臭」を検出・診断し、人間らしい文章にリライトするスキル。 Use when: 「AIっぽい文章を直して」「人間らしくリライトして」「AI臭を消して」「この文章をもっと自然にして」 「テキストのAI感を減らして」「機械っぽさを取りたい」 "make this sound more human", "remove AI tone", "humanize this text", "detect if this is AI-generated". 6つのAI特有パターン（視覚的マーカー、単調なリズム、マニュアル的構成、非コミット姿勢、抽象語の濫用、 定型メタファー）を正規表現ベースで検出し、0-100のAI臭スコアを算出。3つの人間化技法 （バランスを崩す・客観を崩す・論理を崩す）でリライトを実行する。 Note: 検出スクリプトは日本語テキスト専用。英語テキストの場合はClaude自身がreferences/を参照して分析・リライトする。

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ai-text-humanizer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ai-text-humanizer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

LLMが生成するテキストには、人間の文章にはほとんど現れない6つの特有パターンがある。このスキルは：

1. **6パターン検出** — 視覚的マーカー残存、単調なリズム、マニュアル的構成、非コミット姿勢、抽象語の濫用、定型メタファーを正規表現ベースで検出
2. **AI臭スコアリング** — 0-100のスコアで「どのくらいAIっぽいか」を定量化
3. **人間化リライト** — 3つの技法（バランスを崩す・客観を崩す・論理を崩す）で自然な文章に変換

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
python3 scripts/detect_ai_patterns.py <input_file> --output report.md --doc-type auto
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

- `skills/ai-text-humanizer/references/ai_writing_patterns.md`
- `skills/ai-text-humanizer/references/human_writing_techniques.md`
- `skills/ai-text-humanizer/references/rewrite_rules.md`

**Scripts:**

- `skills/ai-text-humanizer/scripts/detect_ai_patterns.py`
