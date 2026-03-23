# Cross-File Consistency Checklist

Run this checklist before final handoff.

## 1. Identity Consistency
- project name matches across all files
- owner / team is consistent
- current phase is not contradictory

## 2. Path Consistency
- source path in `CLAUDE.md` matches `PROJECT_BRIEF.md`
- test path in `CLAUDE.md` matches `PROJECT_BRIEF.md`
- DB/migration path matches `PROJECT_BRIEF.md` and rule files
- `CLAUDE.md` imports only files that exist

## 3. Command Consistency
- build / test / lint / typecheck / CI / packaging commands match across:
  - `CLAUDE.md`
  - `PROJECT_BRIEF.md`
  - `QUALITY_GATES.md`
  - `TEST_STRATEGY.md`
- commands are either confirmed or clearly marked `TBD`

## 4. Risk Consistency
- high-risk areas listed in `PROJECT_BRIEF.md` appear in:
  - `SKILL_ROUTING.md`
  - `QUALITY_GATES.md`
  - `TEST_STRATEGY.md`
- risk-specific gates and scenarios are not missing for obvious repo risks

## 5. Placeholder Burn-Down
- no accidental `{{PLACEHOLDER}}` remains
- intentional `TBD` values are listed in the final summary

## 6. Local Rule Alignment
- `.claude/rules/*` path globs match the actual repo layout
- `.claude/commands/project-kickoff.md` references files that were actually created
