# Install Profiles

Use this guide to decide how much scaffolding to install in the current repository.

## 1. Minimal Profile

Install only the core files:

- `CLAUDE.md`
- `docs/PROJECT_BRIEF.md`
- `docs/SKILL_ROUTING.md`
- `docs/QUALITY_GATES.md`
- `docs/TEST_STRATEGY.md`

Choose `minimal` when:
- the repo is a prototype, PoC, or disposable experiment
- one person owns most changes
- the team wants the lightest possible kickoff footprint
- there is no clear need yet for local rules or long-lived governance docs

Benefits:
- fastest onboarding
- lowest maintenance burden
- enough context for Claude to behave consistently

Risks:
- less institutional memory
- more follow-up work needed as the project grows

## 2. Standard Profile

Install the core files plus:

- `docs/DECISION_LOG.md`
- `docs/HIDDEN_CONTRACT_REGISTER.md`
- `docs/CROSS_MODULE_CONSISTENCY_MATRIX.md`
- `.claude/rules/backend-api.md`
- `.claude/rules/db-and-migrations.md`
- `.claude/rules/testing-and-release.md`

Choose `standard` when:
- the project is team-owned
- changes are expected to continue over multiple sprints
- there are clear high-risk areas such as auth, DB changes, money, time, external APIs
- the team wants Claude to follow localized rules inside specific folders

This is the recommended default profile.

## 3. Full Profile

Install everything in `standard` plus:

- `.claude/commands/project-kickoff.md`

Choose `full` when:
- the team wants a reusable project-local slash command
- the repo is long-lived or has frequent new contributors
- onboarding speed and consistency matter more than minimum footprint
- the team expects to refresh kickoff docs repeatedly

## 4. Escalation Rules

Escalate from `minimal` to `standard` or `full` if any of the following are true:
- more than one major runtime or service is involved
- there is a real database or migration workflow
- the project handles money, auth, privacy, compliance, or operations-sensitive flows
- the repo already has a `.claude/` folder and the team is clearly investing in Claude-local workflows
- the user explicitly wants template-based repeatability

## 5. Practical Recommendation

Use this default sequence unless the user says otherwise:

1. Start with `standard`
2. Downgrade to `minimal` only if the repo is obviously tiny or short-lived
3. Upgrade to `full` when the team wants a reusable local slash command
