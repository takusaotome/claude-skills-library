---
name: project-kickoff-bootstrapper
description: |
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
---

# Project Kickoff Bootstrapper

## Overview

This skill installs or refreshes the minimum Claude-facing project context needed for a new repository to operate predictably from day one. It does three things at once:

1. **Inspects repository evidence** to infer stack, commands, directories, and existing governance docs.
2. **Collects only the missing information** from the user instead of forcing a long upfront questionnaire.
3. **Creates or updates a coherent kickoff file set** so Claude can understand the project, know which skills to use, and know what “done” means.

This skill is intentionally a **bootstrap orchestrator**. It seeds starter artifacts quickly and consistently. It does **not** replace deeper follow-on work such as designing rigorous quality gates, investigating hidden contracts, or building a production-parity regression strategy. After scaffolding, route those deeper tasks to the dedicated skills.

## Scope Boundary

This skill **does**:
- create or refresh the project kickoff file set from templates
- merge repository evidence with user-confirmed answers
- keep `CLAUDE.md` short and push detail into `docs/` and `.claude/rules/`
- choose a practical installation profile (`minimal`, `standard`, `full`)
- preserve unknown information as `TBD` instead of inventing false precision

This skill **does not**:
- perform a full project plan or WBS breakdown (use `project-plan-creator`)
- deeply score project readiness (use `project-completeness-scorer`)
- perform detailed gate design (use `completion-quality-gate-designer`)
- perform detailed hidden-contract analysis (use `hidden-contract-investigator`)
- perform detailed cross-module consistency analysis (use `cross-module-consistency-auditor`)
- design full production-parity regression suites (use `production-parity-test-designer`)

## When to Use

- 新しいプロジェクトを始めるので、最初から Claude に必要文脈を持たせたい
- 既存リポジトリに後付けで `CLAUDE.md` と kickoff ドキュメント群を導入したい
- AI エージェントが「いつどのスキルを使うか」を最初から理解できる状態にしたい
- チームごとにバラバラな完了判定やテスト方針を最低限そろえたい
- `.claude/rules/` や `/project-kickoff` の導入を素早く行いたい
- A repository has code but no durable AI memory or project operating guide
- The team wants a repeatable starter pack that can be installed in less than one session

## Inputs

Use repository evidence first, then confirm gaps with the user.

### Required Inputs
- target repository root
- project name or working title
- one-line project summary
- intended installation mode: `create`, `refresh`, or `augment`

### Usually Needed Inputs
- owner or team
- current phase
- main stack and primary language
- main source directory, test directory, DB/migration directory
- standard commands (build / test / lint / typecheck / CI / packaging)
- major risk areas
- desired installation profile: `minimal`, `standard`, or `full`

### Acceptable Unknowns
If any of the above are not known, write `TBD` and list them in the final summary instead of guessing.

## Outputs

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

### Session Deliverables
- populated bootstrap input sheet (working artifact; save only if useful)
- created/updated file list
- unresolved `TBD` list
- recommended next skills to run for deeper refinement

## Installation Profiles

Load `references/install_profiles.md` before generating files.

- **minimal**: core kickoff files only; best for prototypes or very small repos
- **standard**: core files + extended docs + path-based rules; best default for most team projects
- **full**: standard profile + slash command template and fuller governance scaffolding; best for long-lived or high-risk repos

Default to **standard** unless the repository is obviously tiny or the user asks for the lightest possible setup.

## Workflow

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
   - prefer `standard` for normal product or internal app work
   - prefer `full` for multi-person, regulated, or long-lived systems
4. Load `references/non_destructive_update_policy.md`.
5. If important files already exist and are heavily customized, do not overwrite blindly. Merge carefully or create a proposed draft when needed.

### Phase 3: Ask Only the Missing, High-Leverage Questions

1. Load `references/question_strategy.md`.
2. Ask 2–4 questions per round, prioritizing:
   - project purpose and success criteria
   - owner / team / current phase
   - risk areas and environment differences
   - required commands and release conditions
3. Prefer confirmation questions over open-ended questions when repository evidence is strong.
4. When evidence is weak, ask short targeted questions rather than broad essays.
5. Update the bootstrap input sheet after every answer.

### Phase 4: Resolve Defaults and Burn Down Placeholders

1. Normalize user input and repo evidence into one authoritative value set.
2. Replace placeholders with:
   - confirmed value, if known
   - repo-inferred value, if strongly supported
   - `TBD`, if still unresolved
3. Harmonize the following across all files:
   - project name
   - owner / team
   - primary language / stack
   - key paths
   - commands
   - risk areas
4. Load `references/cross_file_consistency_checklist.md` before writing files.

### Phase 5: Create or Refresh Core Files

Use the templates in `assets/` and write project files to the target repo.

1. Create or update `CLAUDE.md` from `assets/CLAUDE.md.template.md`
2. Create or update:
   - `docs/PROJECT_BRIEF.md` from `assets/docs/PROJECT_BRIEF.template.md`
   - `docs/SKILL_ROUTING.md` from `assets/docs/SKILL_ROUTING.template.md`
   - `docs/QUALITY_GATES.md` from `assets/docs/QUALITY_GATES.template.md`
   - `docs/TEST_STRATEGY.md` from `assets/docs/TEST_STRATEGY.template.md`
3. Ensure `CLAUDE.md` imports only files that actually exist after generation.
4. Keep the generated `CLAUDE.md` concise; push detail into `docs/` and `.claude/rules/`.

### Phase 6: Install Extended Docs and Local Rules When Appropriate

If profile is `standard` or `full`, also create or update:

- `docs/DECISION_LOG.md` from `assets/docs/DECISION_LOG.template.md`
- `docs/HIDDEN_CONTRACT_REGISTER.md` from `assets/docs/HIDDEN_CONTRACT_REGISTER.template.md`
- `docs/CROSS_MODULE_CONSISTENCY_MATRIX.md` from `assets/docs/CROSS_MODULE_CONSISTENCY_MATRIX.template.md`

If the repo shape justifies it, also install:

- `.claude/rules/backend-api.md` from `assets/.claude/rules/backend-api.md.template.md`
- `.claude/rules/db-and-migrations.md` from `assets/.claude/rules/db-and-migrations.md.template.md`
- `.claude/rules/testing-and-release.md` from `assets/.claude/rules/testing-and-release.md.template.md`

When rendering rule files, remove obviously irrelevant path globs and prefer patterns that match the actual repo layout.

### Phase 7: Install the Project Slash Command When Full Profile Is Chosen

If profile is `full`, create or update:

- `.claude/commands/project-kickoff.md` from `assets/.claude/commands/project-kickoff.md.template.md`

Before writing it:
1. confirm the team actually wants a project-local slash command
2. keep the command aligned with the generated kickoff docs
3. ensure the command refers to files that were actually created

### Phase 8: Perform Final Consistency Check and Handoff

1. Load `references/follow_on_skill_sequence.md`.
2. Re-check that:
   - `CLAUDE.md` import targets exist
   - commands are consistent across files
   - risk areas in `PROJECT_BRIEF.md` appear in `SKILL_ROUTING.md`, `QUALITY_GATES.md`, and `TEST_STRATEGY.md`
   - no unreplaced `{{PLACEHOLDER}}` remains unless intentionally preserved
3. Summarize:
   - created / updated files
   - still-missing information
   - chosen profile
   - key risks detected from repo evidence
   - recommended next skills to run

## Resources

| File | Type | Purpose | When to Load |
|------|------|---------|--------------|
| `references/install_profiles.md` | Reference | Decide minimal / standard / full installation scope | Phase 2 |
| `references/repository_inspection_guide.md` | Reference | Infer stack, commands, directories, and risk signals from repo evidence | Phase 1 |
| `references/question_strategy.md` | Reference | Ask concise, high-leverage follow-up questions without over-interviewing | Phase 3 |
| `references/non_destructive_update_policy.md` | Reference | Refresh existing kickoff docs safely without destructive overwrite | Phase 2, Phase 5, Phase 6, Phase 7 |
| `references/cross_file_consistency_checklist.md` | Reference | Ensure names, commands, paths, and file links stay aligned across artifacts | Phase 4, Phase 8 |
| `references/follow_on_skill_sequence.md` | Reference | Recommend the next deeper skill after scaffolding is complete | Phase 8 |
| `assets/bootstrap_input_sheet_template.md` | Template | Working sheet for resolved values, inferred commands, open questions, and chosen profile | Phase 1–4 |
| `assets/bootstrap_summary_template.md` | Template | Final handoff summary for created files, unresolved items, and next skills | Phase 8 |
| `assets/CLAUDE.md.template.md` | Template | Root Claude memory entrypoint for the project | Phase 5 |
| `assets/docs/PROJECT_BRIEF.template.md` | Template | Project purpose, scope, architecture, commands, and risk areas | Phase 5 |
| `assets/docs/SKILL_ROUTING.template.md` | Template | Phase-based and signal-based skill usage rules | Phase 5 |
| `assets/docs/QUALITY_GATES.template.md` | Template | Starter completion and release gate definitions | Phase 5 |
| `assets/docs/TEST_STRATEGY.template.md` | Template | Starter test-level and production-parity strategy | Phase 5 |
| `assets/docs/DECISION_LOG.template.md` | Template | Persistent decision log for project-level design and quality choices | Phase 6 |
| `assets/docs/HIDDEN_CONTRACT_REGISTER.template.md` | Template | Registry for reuse-risk and implicit behavior investigation | Phase 6 |
| `assets/docs/CROSS_MODULE_CONSISTENCY_MATRIX.template.md` | Template | Impact and update-leak tracking for duplicated rules across modules | Phase 6 |
| `assets/.claude/rules/backend-api.md.template.md` | Template | Path-scoped backend rule file | Phase 6 |
| `assets/.claude/rules/db-and-migrations.md.template.md` | Template | Path-scoped DB/migration rule file | Phase 6 |
| `assets/.claude/rules/testing-and-release.md.template.md` | Template | Path-scoped testing/release rule file | Phase 6 |
| `assets/.claude/commands/project-kickoff.md.template.md` | Template | Optional project-local slash command for future refreshes | Phase 7 |

## Best Practices

### Evidence First, User Second
- Infer what you can from the repository before asking questions.
- Ask the user to confirm or correct, rather than forcing them to restate obvious facts.

### Keep the First Install Lightweight
- Prefer a good starter set over a bloated governance pack.
- `minimal` and `standard` profiles should be fast to install in one working session.

### Never Invent Commands
- If build/test/lint/typecheck commands cannot be verified, write `TBD`.
- A wrong command in `CLAUDE.md` is worse than an unresolved field because it trains future sessions on bad defaults.

### Preserve Existing Work
- If a repository already has strong docs, merge or augment rather than replace.
- When in doubt, propose a draft update instead of overwriting heavily curated files.

### Treat Unknowns as First-Class Outputs
- Missing information is not failure; hidden assumptions are.
- The final summary must explicitly list unresolved placeholders and recommended owners.

### Use Follow-On Skills Deliberately
After bootstrap, recommend deeper refinement where needed:
- `completion-quality-gate-designer` for stronger `QUALITY_GATES.md`
- `hidden-contract-investigator` for risky reuse areas
- `safe-by-default-architect` for security-sensitive design choices
- `cross-module-consistency-auditor` for multi-flow or duplicated rule changes
- `production-parity-test-designer` for real production-like verification design

## Starter Success Criteria

A bootstrap session is successful when:
- Claude can open the repo and immediately understand purpose, scope, and high-risk areas
- There is an explicit file telling Claude which skills to use in which situations
- There is a starter definition of completion and test evidence
- The generated files match actual repo structure closely enough to be useful on day one
- Unknowns are visible, bounded, and easy for the team to resolve later
