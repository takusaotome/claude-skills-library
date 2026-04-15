---
layout: default
title: "Codex Reviewer"
grand_parent: English
parent: Software Development
nav_order: 13
lang_peer: /ja/skills/dev/codex-reviewer/
permalink: /en/skills/dev/codex-reviewer/
---

# Codex Reviewer
{: .no_toc }

OpenAI Codex CLIを使用してドキュメントやコードのレビューを依頼するスキル。GPT-5.4モデルをhigh推論モードで呼び出し、深い分析によるレビューを実行。レビュー結果を指定フォルダに出力し、その内容を確認・分析する機能を提供。コードレビュー、ドキュメントレビュー、設計書レビュー、テスト計画レビューなど、専門的なレビューが必要な場面で使用。
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/codex-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/codex-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

OpenAI Codex CLIを活用して、コードやドキュメントの専門的なレビューを実行するスキルです。全レビュータイプで **GPT-5.4** モデルを **high推論モード**で使用し、徹底的な分析を行います。

---

## 2. Prerequisites

1. **Codex CLIのインストール**
   ```bash
   npm install -g @openai/codex
   # または
   brew install --cask codex
   ```

2. **認証設定**
   ```bash
   codex login
   ```

3. **推奨: プロファイル設定** (`~/.codex/config.toml`)
   ```toml
   # デフォルトプロファイル
   [profiles.deep-review]
   model = "gpt-5.4"
   model_reasoning_effort = "high"
   approval_policy = "never"
   ```

---

## 3. Quick Start

```bash
# コードレビュー
python3 scripts/run_codex_review.py \
  --type code \
  --target src/ \
  --output ./reviews

# ドキュメントレビュー
python3 scripts/run_codex_review.py \
  --type document \
  --target docs/spec.md \
  --output ./reviews
```

---

## 4. How It Works

### Phase 1: レビュー依頼の準備

1. **レビュー対象の確認**
   - ファイルパスまたはディレクトリパスを特定
   - レビュータイプを決定（コード/ドキュメント/設計/テスト）
   - レビュー観点を明確化

2. **出力先フォルダの準備**
   - レビュー結果を保存するフォルダを作成または確認
   - 例: `./reviews/`, `./code-reviews/`, `./doc-reviews/`

### Phase 2: Codex CLIによるレビュー実行

> **重要**: `run_codex_review.py` スクリプトは常に **`--full-auto` モード**で実行されます。
> これにより、ユーザー承認なしでCodexがコマンドを自動実行します。
> また、スクリプトは**内部定義のプロファイル**を使用するため、`~/.codex/config.toml` のプロファイル設定は参照されません。

**スクリプトを使用したレビュー（推奨）:**
```bash
# コードレビュー
python3 scripts/run_codex_review.py \
  --type code \
  --target src/ \
  --output ./reviews

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- コードの品質レビュー、セキュリティレビュー、パフォーマンスレビューが必要な時
- 設計書、仕様書、技術ドキュメントのレビューが必要な時
- テスト計画、テストケースのレビューが必要な時
- プルリクエストの詳細レビューが必要な時
- 外部の専門的な視点でのレビューを得たい時

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 2 guide file(s).
- Script-assisted execution using 2 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/codex-reviewer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: codex_config_guide.md, review_prompts.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: run_codex_review.py, analyze_review.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/codex-reviewer/references/codex_config_guide.md`
- `skills/codex-reviewer/references/review_prompts.md`

**Scripts:**

- `skills/codex-reviewer/scripts/analyze_review.py`
- `skills/codex-reviewer/scripts/run_codex_review.py`
