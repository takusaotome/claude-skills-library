# Non-Destructive Update Policy

This skill must be safe to run on existing repositories.

## 1. File State Categories

Treat each target file as one of:

- **Absent**: create from template
- **Template-aligned**: update in place using the latest resolved values
- **User-customized**: merge carefully; preserve important project-specific detail
- **Unknown / messy**: do not overwrite blindly; propose a draft or ask for confirmation

## 2. Safe Default Behavior

When uncertain, prefer:
- additive updates
- preserving user-authored sections
- marking unresolved values as `TBD`
- summarizing what changed at the end

Avoid:
- wiping curated rules
- replacing rich architecture or operations notes with thin templates
- normalizing everything into the template if it removes useful detail

## 3. Merge Heuristics

### `CLAUDE.md`
- keep it short
- preserve project-specific non-negotiables
- ensure imports point to real files
- avoid duplicating long policy text already stored in `docs/` or `.claude/rules/`

### `docs/*`
- preserve already-captured decisions and project specifics
- backfill missing sections from the template
- do not erase evidence, links, or stakeholder information

### `.claude/rules/*`
- preserve path globs that clearly match the repo
- remove only obviously wrong or dead globs
- keep rules concise and actionable

## 4. When to Create a Draft Instead of Overwriting

Prefer a draft output when:
- the existing file is long and heavily curated
- ownership is ambiguous
- the user did not authorize replacement
- the template would remove meaningful detail

Draft naming suggestion:
- `CLAUDE.bootstrap-proposed.md`
- `docs/PROJECT_BRIEF.bootstrap-proposed.md`

Use this only when needed; do not overproduce draft files.
