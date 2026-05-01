---
layout: default
title: "Project Kickoff Bootstrapper"
grand_parent: English
parent: Meta & Quality
nav_order: 19
lang_peer: /ja/skills/meta/project-kickoff-bootstrapper/
permalink: /en/skills/meta/project-kickoff-bootstrapper/
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

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/project-kickoff-bootstrapper.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/project-kickoff-bootstrapper){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill installs or refreshes the minimum Claude-facing project context needed for a new repository to operate predictably from day one. It does three things at once:

1. **Inspects repository evidence** to infer stack, commands, directories, and existing governance docs.
2. **Collects only the missing information** from the user instead of forcing a long upfront questionnaire.
3. **Creates or updates a coherent kickoff file set** so Claude can understand the project, know which skills to use, and know what “done” means.

This skill is intentionally a **bootstrap orchestrator**. It seeds starter artifacts quickly and consistently. It does **not** replace deeper follow-on work such as designing rigorous quality gates, investigating hidden contracts, or building a production-parity regression strategy. After scaffolding, route those deeper tasks to the dedicated skills.

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

### Phase 1: Inspect the Repository Before Asking Questions

1. Load `references/repository_inspection_guide.md`.
2. Read repository evidence in this order:
   - root `README*`
   - language manifests (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, etc.)
   - build/test automation (`Makefile`, `justfile`, `Taskfile`, `.github/workflows/`, CI configs)
   - existing `CLAUDE.md`, `.claude/`, `docs/`, architecture docs, runbooks
3. Infer:
   - probable primary language and stack

---

## 4. How It Works

### Phase 1: Inspect the Repository Before Asking Questions

1. Load `references/repository_inspection_guide.md`.
2. Read repository evidence in this order:
   - root `README*`
   - language manifests (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, etc.)
   - build/test automation (`Makefile`, `justfile`, `Taskfile`, `.github/workflows/`, CI configs)
   - existing `CLAUDE.md`, `.claude/`, `docs/`, architecture docs, runbooks
3. Infer:
   - probable primary language and stack
   - candidate source / test / DB directories
   - build / test / lint / typecheck / packaging commands
   - whether DB, migrations, API, or release automation exist
4. Record findings in `assets/bootstrap_input_sheet_template.md` before asking the user anything.

### Phase 2: Choose Profile and Update Strategy

1. Load `references/install_profiles.md`.
2. Decide whether the session is:
   - **create**: files do not exist yet
   - **refresh**: files exist and appear to be from the same template family
   - **augment**: files exist but only part of the kickoff set is present
3. Select installation profile:
   - prefer `minimal` for solo experiments / throwaway repos

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- 新しいプロジェクトを始めるので、最初から Claude に必要文脈を持たせたい
- 既存リポジトリに後付けで `CLAUDE.md` と kickoff ドキュメント群を導入したい
- AI エージェントが「いつどのスキルを使うか」を最初から理解できる状態にしたい
- チームごとにバラバラな完了判定やテスト方針を最低限そろえたい
- `.claude/rules/` や `/project-kickoff` の導入を素早く行いたい
- A repository has code but no durable AI memory or project operating guide

---

## 6. Understanding the Output

### Core Files
- `CLAUDE.md`
- `docs/PROJECT_BRIEF.md`
- `docs/SKILL_ROUTING.md`
- `docs/QUALITY_GATES.md`
- `docs/TEST_STRATEGY.md`

### Extended Files
- `docs/DECISION_LOG.md`
- `docs/HIDDEN_CONTRACT_REGISTER.md`
- `docs/CROSS_MODULE_CONSISTENCY_MATRIX.md`

### Optional Claude Support Files
- `.claude/rules/backend-api.md`
- `.claude/rules/db-and-migrations.md`
- `.claude/rules/testing-and-release.md`
- `.claude/commands/project-kickoff.md`

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/project-kickoff-bootstrapper/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: repository_inspection_guide.md, follow_on_skill_sequence.md, install_profiles.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.

---

## 10. Reference

**References:**

- `skills/project-kickoff-bootstrapper/references/cross_file_consistency_checklist.md`
- `skills/project-kickoff-bootstrapper/references/follow_on_skill_sequence.md`
- `skills/project-kickoff-bootstrapper/references/install_profiles.md`
- `skills/project-kickoff-bootstrapper/references/non_destructive_update_policy.md`
- `skills/project-kickoff-bootstrapper/references/question_strategy.md`
- `skills/project-kickoff-bootstrapper/references/repository_inspection_guide.md`
