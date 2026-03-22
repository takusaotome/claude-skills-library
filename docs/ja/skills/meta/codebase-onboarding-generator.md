---
layout: default
title: "Codebase Onboarding Generator"
grand_parent: 日本語
parent: メタ・品質
nav_order: 13
lang_peer: /en/skills/meta/codebase-onboarding-generator/
permalink: /ja/skills/meta/codebase-onboarding-generator/
---

# Codebase Onboarding Generator
{: .no_toc }

Automatically analyze a codebase and generate comprehensive CLAUDE.md documentation for future Claude Code sessions. Use when onboarding to a new project, creating project documentation, or generating AI coding assistant context files.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/codebase-onboarding-generator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/codebase-onboarding-generator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

This skill analyzes a codebase to automatically generate comprehensive CLAUDE.md documentation. It identifies common commands, build processes, test patterns, directory structure conventions, and key architectural decisions. The generated documentation follows best practices for Claude Code onboarding and enables efficient AI-assisted development.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- Python 3.9+
- No API keys required
- Standard library only (pathlib, json, os, re)

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
python3 scripts/analyze_codebase.py \
  --path /path/to/project \
  --output analysis.json
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

- `skills/codebase-onboarding-generator/references/claude-md-best-practices.md`

**Scripts:**

- `skills/codebase-onboarding-generator/scripts/analyze_codebase.py`
