---
layout: default
title: "Render CLI Expert"
grand_parent: English
parent: Software Development
nav_order: 25
lang_peer: /ja/skills/dev/render-cli-expert/
permalink: /en/skills/dev/render-cli-expert/
---

# Render CLI Expert
{: .no_toc }

Render CLIを使用したクラウドサービス管理の専門スキル。デプロイ、ログ監視、SSH接続、PostgreSQL接続、サービス管理などRenderプラットフォームのCLI操作を効率的に支援。定期的に公式ドキュメントをチェックして最新情報を取得。Use when managing Render services via CLI, deploying applications, viewing logs, connecting to databases, or automating cloud infrastructure tasks.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/render-cli-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/render-cli-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Render CLIは、Renderクラウドプラットフォームのサービスをターミナルから直接管理するための公式CLIツールです。このスキルは、Render CLIを使用した効率的なサービス管理、デプロイ自動化、トラブルシューティングを支援します。

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

- Renderサービスをターミナルからデプロイ・管理したい
- サービスのログをリアルタイムで監視したい
- PostgreSQLデータベースにpsqlで接続したい
- SSHでサービスにリモート接続したい
- CI/CDパイプラインでRender操作を自動化したい
- ワークスペースやサービスの一覧を取得したい

---

## 6. Understanding the Output

### Available Formats

```bash
# JSON形式
render services -o json

# YAML形式
render services -o yaml

# テキスト形式（デフォルト）
render services -o text
```

### Automation Flags

```bash
# 確認プロンプトをスキップ
render deploys create srv-abc123 --confirm

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/render-cli-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: last_check.json, cli_updates.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: render_cli_updater.py.
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
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/render-cli-expert/references/cli_updates.md`
- `skills/render-cli-expert/references/last_check.json`

**Scripts:**

- `skills/render-cli-expert/scripts/render_cli_updater.py`
