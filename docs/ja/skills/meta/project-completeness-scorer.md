---
layout: default
title: "Project Completeness Scorer"
grand_parent: 日本語
parent: メタ・品質
nav_order: 18
lang_peer: /en/skills/meta/project-completeness-scorer/
permalink: /ja/skills/meta/project-completeness-scorer/
---

# Project Completeness Scorer
{: .no_toc }

Evaluate project deliverables (code, docs, config) and calculate a 0-100 completeness score with weighted criteria and prioritized action items. Use when assessing project readiness, reviewing milestones, or identifying gaps before release.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/project-completeness-scorer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/project-completeness-scorer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

This skill systematically evaluates project deliverables across multiple dimensions (functional requirements, quality standards, test coverage, documentation, deployment readiness) and produces a weighted 0-100 completeness score. It identifies gaps, ranks missing items by priority, and provides actionable next steps to reach completion.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- Python 3.9+
- No API keys required
- Standard library only (json, pathlib, argparse)

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
# List available templates
python3 scripts/score_project.py --list-templates

# Use a specific template
python3 scripts/score_project.py --template skill --project-path ./skills/my-skill
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

- `skills/project-completeness-scorer/references/project-templates.md`
- `skills/project-completeness-scorer/references/scoring-methodology.md`

**Scripts:**

- `skills/project-completeness-scorer/scripts/score_project.py`
