---
layout: default
title: "Codex Reviewer"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 13
lang_peer: /en/skills/dev/codex-reviewer/
permalink: /ja/skills/dev/codex-reviewer/
---

# Codex Reviewer
{: .no_toc }

OpenAI Codex CLIを使用してドキュメントやコードのレビューを依頼するスキル。GPT-5.3-Codexモデルを高推論モード(high)で呼び出し、最も深い分析によるレビューを実行。レビュー結果を指定フォルダに出力し、その内容を確認・分析する機能を提供。コードレビュー、ドキュメントレビュー、設計書レビュー、テスト計画レビューなど、専門的なレビューが必要な場面で使用。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/codex-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/codex-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

OpenAI Codex CLIを活用して、コードやドキュメントの専門的なレビューを実行するスキルです。レビュータイプに応じて最適なモデルを自動選択し、**xhigh推論モード**で徹底的な分析を行います。

- **コード/テスト**: GPT-5.3-Codex（エージェント型コーディングモデル）
- **ドキュメント/設計**: GPT-5.3-Thinking（深い推論モデル）

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

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
   model = "gpt-5.3-codex"
   model_reasoning_effort = "high"
   approval_policy = "never"
   ```

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

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

- `skills/codex-reviewer/references/codex_config_guide.md`
- `skills/codex-reviewer/references/review_prompts.md`

**Scripts:**

- `skills/codex-reviewer/scripts/analyze_review.py`
- `skills/codex-reviewer/scripts/run_codex_review.py`
