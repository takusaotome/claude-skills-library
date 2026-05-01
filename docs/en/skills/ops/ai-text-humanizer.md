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

テキストを受け取り、6パターンの検出とスコアリングを行う。

### Steps

1. **テキスト受領** — ユーザーからテキストを受け取る（ファイルパス指定。直接入力の場合は一時ファイルに保存してスクリプトに渡す）
2. **パターン検出実行** — `scripts/detect_ai_patterns.py` を実行してパターンを検出
   **Note**: 英語テキストの場合はスクリプトではなく、`references/ai_writing_patterns.md` を読み込んでClaude自身が分析する。
   ```bash
   python3 scripts/detect_ai_patterns.py <input_file> --output report.md --doc-type auto
   ```
   **doc-type の使い分け**:
   - `email` / `chat`: Markdown構造をAIマーカーとして検出
   - `blog` / `structured`: `## 見出し` と箇条書きはPattern 1で非加点
   - `auto`: 上記を簡易推定
3. **結果確認** — スクリプト出力のスコアとパターン別内訳を確認
4. **レポート確認** — スクリプトが自動生成したレポートを確認する。`assets/detection_report_template.md` はClaude手動分析時用の雛形
5. **ユーザーへ報告** — 総合スコア、パターン別内訳、具体例、推奨アクションを提示

### Output

- 総合AI臭スコア (0-100)
- パターン別スコア内訳（6パターン）
- 検出された具体例（該当箇所の引用）
- スコア解釈と推奨アクション

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- ユーザーが「AIっぽい」「AI臭い」「機械的」「リライトして」「人間らしく」「自然にして」と言ったとき
- ブログ記事、ビジネス文書、SNS投稿などをAI生成後に人間化したいとき
- AI生成テキストの品質チェック・改善が必要なとき
- テキストがAI生成かどうかの簡易判定を求められたとき

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 3 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/ai-text-humanizer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: ai_writing_patterns.md, human_writing_techniques.md, rewrite_rules.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: detect_ai_patterns.py.
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
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/ai-text-humanizer/references/ai_writing_patterns.md`
- `skills/ai-text-humanizer/references/human_writing_techniques.md`
- `skills/ai-text-humanizer/references/rewrite_rules.md`

**Scripts:**

- `skills/ai-text-humanizer/scripts/detect_ai_patterns.py`
