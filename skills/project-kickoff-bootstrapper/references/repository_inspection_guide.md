# Repository Inspection Guide

Inspect the repository before generating kickoff files. The goal is to infer defaults from evidence rather than asking the user to type everything manually.

## 1. Evidence Priority

Read in roughly this order:

1. Root `README*`
2. Existing `CLAUDE.md`, `.claude/`, and `docs/`
3. Language manifests and dependency files
4. CI workflows and task runners
5. Project tree structure

Prefer concrete machine-readable evidence over prose when they conflict.

## 2. Common Signals by Ecosystem

### Python
Look for:
- `pyproject.toml`
- `requirements.txt`
- `uv.lock`
- `poetry.lock`
- `tox.ini`
- `pytest.ini`
- `src/`, `app/`, `tests/`, `alembic/`

Candidate commands:
- build: `python -m build`, `uv build`, or project-specific task runner
- unit test: `pytest`
- lint: `ruff check .`, `flake8`, `pylint`
- typecheck: `mypy .`, `pyright`
- CI equivalent: from `.github/workflows/*` or `Makefile`

### Node / TypeScript
Look for:
- `package.json`
- `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`
- `tsconfig.json`
- `src/`, `app/`, `server/`, `test/`, `tests/`, `prisma/`

Candidate commands:
- build: `npm run build`, `pnpm build`
- test: `npm test`, `pnpm test`, `vitest`, `jest`
- lint: `npm run lint`, `eslint`
- typecheck: `tsc --noEmit`
- packaging/deploy: container build or framework-specific deploy step

### Go
Look for:
- `go.mod`
- `cmd/`, `internal/`, `pkg/`, `migrations/`
Candidate commands:
- build: `go build ./...`
- test: `go test ./...`
- lint: `golangci-lint run`

### Rust
Look for:
- `Cargo.toml`
- `src/`, `tests/`, `migrations/`
Candidate commands:
- build: `cargo build`
- test: `cargo test`
- lint: `cargo clippy`
- format check: `cargo fmt --check`

## 3. Directory Inference

Infer likely paths, but prefer actual observed directories over conventions.

- main source: `src/`, `app/`, `server/`, `backend/`, `cmd/`
- tests: `tests/`, `test/`, `__tests__/`, `spec/`
- DB/migrations: `migrations/`, `db/`, `database/`, `alembic/`, `prisma/`
- infra: `infra/`, `terraform/`, `helm/`, `deploy/`

If multiple plausible directories exist, record the ambiguity and ask the user to confirm.

## 4. Risk Signal Detection

Mark risk areas when you see:

- auth or permission code
- SQL or migration files
- money, tax, rounding, billing flows
- timezone or scheduling code
- file I/O, storage, queues, batch jobs
- external API integrations
- duplicated business logic across API / batch / admin / export flows

These signals should shape `PROJECT_BRIEF.md`, `SKILL_ROUTING.md`, `QUALITY_GATES.md`, and `TEST_STRATEGY.md`.

## 5. Existing Claude Context

If the repo already has:
- `CLAUDE.md`
- `.claude/rules/`
- `.claude/commands/`
- project governance docs

then treat the task as refresh or augment, not greenfield generation.

## 6. Command Confidence Rules

Confidence levels:
- **High**: exact command exists in manifest, CI, or Makefile
- **Medium**: command strongly implied by stack conventions and surrounding files
- **Low**: guess only; do not write as fact

Only write exact commands into generated files at **High** confidence. Otherwise use `TBD` or clearly mark as candidate.
