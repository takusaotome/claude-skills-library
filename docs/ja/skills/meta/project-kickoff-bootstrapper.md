---
layout: default
title: "Project Kickoff Bootstrapper"
grand_parent: 日本語
parent: メタ・品質
nav_order: 19
lang_peer: /en/skills/meta/project-kickoff-bootstrapper/
permalink: /ja/skills/meta/project-kickoff-bootstrapper/
---

# Project Kickoff Bootstrapper
{: .no_toc }

新しいプロジェクトまたは既存リポジトリに Claude 用の kickoff 文脈を導入するスキル。
テンプレートとリポジトリ証跡、ユーザー入力をもとに `CLAUDE.md`、`docs/PROJECT_BRIEF.md`、
`docs/SKILL_ROUTING.md`、`docs/QUALITY_GATES.md`、`docs/TEST_STRATEGY.md`、
`docs/DECISION_LOG.md`、`docs/HIDDEN_CONTRACT_REGISTER.md`、
`docs/CROSS_MODULE_CONSISTENCY_MATRIX.md`、`.claude/rules/*`、
`.claude/commands/project-kickoff.md` を必要に応じて作成・更新する。
Use when starting a new project, retrofitting AI project context into an existing repository,
bootstrapping Claude memory, or standardizing kickoff documents, rules, and slash-command scaffolding.
Distinct from project-manager / project-plan-creator (which plan work),
and from completion-quality-gate-designer / hidden-contract-investigator /
safe-by-default-architect / cross-module-consistency-auditor /
production-parity-test-designer (which deeply refine individual artifacts after bootstrap).

{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/project-kickoff-bootstrapper.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/project-kickoff-bootstrapper){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

This skill installs or refreshes the minimum Claude-facing project context needed for a new repository to operate predictably from day one. It does three things at once:

1. **Inspects repository evidence** to infer stack, commands, directories, and existing governance docs.
2. **Collects only the missing information** from the user instead of forcing a long upfront questionnaire.
3. **Creates or updates a coherent kickoff file set** so Claude can understand the project, know which skills to use, and know what “done” means.

This skill is intentionally a **bootstrap orchestrator**. It seeds starter artifacts quickly and consistently. It does **not** replace deeper follow-on work such as designing rigorous quality gates, investigating hidden contracts, or building a production-parity regression strategy. After scaffolding, route those deeper tasks to the dedicated skills.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- **API Key:** None required
- **Python 3.9+** recommended

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

### Phase 1: Inspect the Repository Before Asking Questions

1. Load `references/repository_inspection_guide.md`.
2. Read repository evidence in this order:
   - root `README*`
   - language manifests (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, etc.)
   - build/test automation (`Makefile`, `justfile`, `Taskfile`, `.github/workflows/`, CI configs)
   - existing `CLAUDE.md`, `.claude/`, `docs/`, architecture docs, runbooks
3. Infer:
   - probable primary language and stack

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

- `skills/project-kickoff-bootstrapper/references/cross_file_consistency_checklist.md`
- `skills/project-kickoff-bootstrapper/references/follow_on_skill_sequence.md`
- `skills/project-kickoff-bootstrapper/references/install_profiles.md`
- `skills/project-kickoff-bootstrapper/references/non_destructive_update_policy.md`
- `skills/project-kickoff-bootstrapper/references/question_strategy.md`
- `skills/project-kickoff-bootstrapper/references/repository_inspection_guide.md`
