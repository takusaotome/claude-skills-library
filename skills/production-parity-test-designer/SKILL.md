---
name: production-parity-test-designer
description: |
  本番と同じ失敗を本番前に検出するためのテスト階層設計スキル。
  DB方言差、実依存関係、永続化確認、timezone差、packaging整合性、
  adversarial regressionをunit/integration/e2e/smoke/packagingに
  適切に割り振り、PR CIで最低限の本番同等性を保証する。
  Use when designing production-parity tests, closing test blind spots,
  building smoke suites for real dependencies, verifying persistence
  beyond UI success, or creating adversarial regression backlogs.
---

# Production Parity Test Designer

## Overview

A test design skill that ensures **production failures are caught before production**. Rather than increasing test count, this skill focuses on **which test tier should cover which production gap**, eliminating proxy metrics (tests that pass but miss real failures) and structuring a layered defense from PR CI through release packaging.

**Core Philosophy**: Tests exist to reproduce production failure modes. If a test cannot fail in the same way production fails, it provides false confidence.

**Scope Boundary**: This skill designs the test architecture and allocation strategy. It does not write test code directly (use `tdd-developer` for that) or generate UAT procedures (use `uat-testcase-generator` for that).

## When to Use

- PR CI が軽すぎて本番差分を検出できないとき
- SQLite と PostgreSQL のような DB 方言差があるとき
- UI が成功表示するのに DB に書かれていない問題があるとき
- mock により runtime import error が隠れているとき
- timezone / locale / OS / dependency の差分が本番で初めて顕在化するとき
- 「何を unit で、何を smoke で見るか」が曖昧なとき
- 過去の重大 defect を再発禁止テストとして構造化したいとき
- packaging / container build の整合性を保証したいとき
- テスト構成を見直して production parity を高めたいとき

## Prerequisites

- **Existing codebase with some tests**: At least a basic test suite exists (even if insufficient)
- **Production environment information**: DB type, OS, container config, dependency list
- **CI configuration**: Current CI pipeline definition (GitHub Actions, CircleCI, etc.)
- **Known defect history**: Past incidents, RCA reports, or bug tracker data (optional but valuable)
- **Dependency manifest**: requirements.txt, package.json, Gemfile, go.mod, etc.

## Inputs

- Existing test configuration and structure
- CI pipeline definition
- Production environment specifications (DB, OS, container, runtime)
- Known defects, RCA reports, or incident history
- Dependency manifests and lockfiles
- Timezone, locale, and environment variable configuration

## Outputs

1. **Production Gap Inventory** -- comprehensive list of dev/CI vs production differences
2. **Test Tier Allocation Matrix** -- failure modes mapped to optimal test tiers
3. **PR Smoke Suite Proposal** -- minimum parity checks required in every PR
4. **Adversarial Regression Backlog** -- re-occurrence prevention tests for past defects
5. **Packaging / Dependency Integrity Checklist** -- install, import, build verification
6. **Standard Test Command Map** -- named commands for each execution context

## Workflows

### Step 1: Production Gap Inventory（本番差分の棚卸し）

Enumerate all differences between development/CI and production environments.

1. Load `references/production_gap_catalog.md` for the full gap taxonomy
2. Interview the operator or inspect configuration to identify gaps in these categories:
   - **DB dialect**: SQLite vs PostgreSQL/MySQL, schema differences, SQL syntax gaps
   - **OS / container**: macOS dev vs Linux production, filesystem case sensitivity
   - **Dependency installation**: pip install vs Docker image layers, native extensions
   - **Environment variables**: Missing secrets, different feature flags, config drift
   - **Timezone / locale**: Server TZ, DB TZ, application TZ, locale-sensitive formatting
   - **Real vs mock**: Mocked APIs, stubbed services, fake filesystems
   - **Serialization**: JSON/YAML parsing differences, encoding, binary formats
   - **Packaging / deployment**: Build artifacts, image layers, startup scripts
3. For each gap, document:
   - **Gap description**: What differs between dev/CI and production
   - **Current coverage**: Is any test currently exercising this gap?
   - **Risk if undetected**: What breaks in production if this gap is missed?
4. Output: **Production Gap Inventory** -- a standalone list of gaps, distinct from the Test Tier Allocation Matrix created in Step 3. Record gaps in the first three columns of `assets/test_tier_matrix_template.md` (Failure mode, Production gap, and current coverage); the Test tier and remaining columns are populated in Step 3.

### Step 2: Failure Mode Enumeration（失敗モードの列挙）

For each production gap, define concrete failure modes.

1. For each gap from Step 1, enumerate specific ways the system breaks:
   - SQLite passes but PostgreSQL throws syntax error on `UPSERT`
   - UI shows success toast but `INSERT` silently fails (no error, no data)
   - `import cv2` works in dev but fails in production container (missing native lib)
   - `datetime.now()` returns naive in dev, aware in production -> `TypeError` on comparison
   - Row index access breaks when column order changes between DB versions
2. Load `references/adversarial_test_patterns.md` for additional failure patterns
3. Classify each failure mode by:
   - **Visibility**: Silent (no error) vs Loud (exception/crash)
   - **Blast radius**: Single record vs Entire feature vs System-wide
   - **Detection difficulty**: Easy (log check) vs Hard (data audit required)
4. Output: Failure mode list annotated with classification

### Step 3: Test Tier Allocation（テスト階層への配賦）

Assign each failure mode to the optimal test tier.

1. Load `references/test_tier_strategy.md` for tier responsibilities and tradeoffs
2. Apply the following allocation rules:
   - **Unit**: Pure logic, boundary values, input validation, format conversion
   - **Integration**: Real DB queries, real repository operations, multi-component interaction
   - **E2E**: UI action -> persistence verification -> business-visible outcome
   - **Smoke**: Minimum production parity checks that must pass in every PR
   - **Packaging**: Install, import, build, container image integrity
   - **Nightly / Heavy**: Full parity suite, performance baselines, large dataset tests
3. Decision criteria for tier assignment:
   - If the failure depends on external state (DB, API, filesystem) -> Integration or higher
   - If the failure is a logic error reproducible with pure inputs -> Unit
   - If the failure requires end-to-end flow through UI -> E2E
   - If the failure relates to dependency availability -> Packaging
   - If the test must run fast enough for PR CI -> Smoke (with runtime budget)
4. Populate `assets/test_tier_matrix_template.md` with assignments
5. Flag any failure modes that have no viable test tier (requires monitoring instead)

### Step 4: Proxy Metric Elimination（プロキシメトリクスの排除）

Identify and remove tests that provide false confidence.

1. Review existing tests for proxy metric patterns:
   - **UI-only verification**: E2E checks screen display but never queries the database
   - **Mock-only coverage**: All external calls mocked, never tested with real dependencies
   - **Coverage theater**: High line coverage but no type mismatch or boundary testing
   - **All-green illusion**: Tests pass but production DB has never been touched
   - **Happy-path bias**: Only success paths tested, no error/edge case coverage
2. For each identified proxy metric:
   - Document what the test actually verifies vs what it appears to verify
   - Specify what additional assertion or real dependency is needed
   - Assign to the appropriate test tier from Step 3
3. Load `references/persistence_verification_guide.md` for persistence verification patterns
4. Output: List of proxy metrics with remediation actions

### Step 5: PR Smoke Suite Definition（PR必須スモークセットの決定）

Define the minimum set of production parity checks for every PR.

1. From the Test Tier Matrix (Step 3), select items marked "Must run in PR"
2. Apply runtime budget constraint:
   - Target: PR smoke suite completes within **2-5 minutes**
   - If over budget, prioritize by blast radius and detection difficulty
3. Define smoke categories (use `assets/smoke_suite_template.md`):
   - **DB dialect smoke**: At least one real-DB operation (upsert, query with dialect-specific syntax)
   - **Import smoke**: Verify all production imports succeed
   - **Persistence smoke**: UI action -> DB read verification
   - **Timezone smoke**: Mixed aware/naive datetime operation
   - **Serialization smoke**: Round-trip encode/decode with production formats
4. For each smoke test, document:
   - Purpose and what production gap it covers
   - Runtime budget allocation
   - Environment requirements (e.g., PostgreSQL service in CI)
   - Pass/fail meaning (what does failure indicate?)
5. Output: PR smoke suite specification

### Step 6: Adversarial Regression Backlog（再発禁止テストバックログ）

Create regression tests derived from past defects and attack patterns. This skill designs regression tests for known app-specific exploit/failure patterns, but it is **not a substitute for dedicated security review or penetration testing**.

1. Load `references/adversarial_test_patterns.md` for attack pattern catalog
2. For each known past defect or incident:
   - Identify the **exploit/failure pattern** (how did it break?)
   - Define the **minimal reproducible scenario** (smallest test that would have caught it)
   - Specify the **expected protected behavior** (what should the system do instead?)
   - Determine the **regression scope** (which related areas need similar protection?)
3. Add proactive adversarial tests for common patterns:
   - SQL injection via user input fields
   - Authentication bypass via header manipulation
   - Path traversal in file upload/download
   - Invalid state transitions in workflow engines
   - Duplicate submission / idempotency violations
   - Stale write / optimistic locking failures
4. Populate `assets/adversarial_regression_template.md`
5. Output: Prioritized adversarial regression backlog

### Step 7: Packaging / Dependency Integrity Checklist（パッケージング・依存整合性チェック）

Verify that the application builds, installs, and imports correctly in a production-equivalent environment.

1. Load `references/packaging_integrity_guide.md` for verification patterns
2. Populate `assets/packaging_checklist_template.md` covering:
   - **Dependency files**: lockfile alignment, pinned versions, no floating ranges
   - **Install path**: clean install from lockfile succeeds without network for pinned deps
   - **Import smoke**: all top-level imports succeed in a fresh environment
   - **Runtime command**: main entry point starts without error
   - **Image parity**: container image matches production base image and dependencies
   - **Environment secrets**: required env vars are documented and validated at startup
3. Output: Completed packaging / dependency integrity checklist

### Step 8: Standard Command Map（実行コマンドの固定）

Define named test commands for each execution context.

1. Use `assets/command_map_template.md` to define commands for:
   - **Local fast**: Developer runs during coding (unit + basic integration)
   - **PR CI required**: Smoke suite that gates every pull request
   - **Nightly parity**: Full production parity suite on schedule
   - **Staging E2E**: End-to-end tests against staging environment
   - **Release packaging**: Build, install, import verification before release
2. For each command:
   - Specify the exact command syntax (e.g., `pytest tests/ -m smoke --timeout=300`)
   - List which test tiers are included
   - Define execution context (local / CI / staging / release)
   - Assign ownership (team or individual responsible for maintenance)
3. Output: Complete command map with all execution contexts

## Resources

| Resource | Type | Purpose | When to Load |
|----------|------|---------|--------------|
| `references/production_gap_catalog.md` | Reference | Full taxonomy of production vs dev/CI differences | Step 1 |
| `references/test_tier_strategy.md` | Reference | Tier responsibilities, speed vs reliability tradeoffs, PR criteria | Step 3 |
| `references/adversarial_test_patterns.md` | Reference | Attack and failure pattern catalog for regression tests | Step 2, 6 |
| `references/persistence_verification_guide.md` | Reference | Patterns for verifying stored state beyond UI display | Step 4 |
| `references/packaging_integrity_guide.md` | Reference | Dependency, build, import, container verification patterns | Step 7, 8 |
| `references/timezone_dialect_boundary_guide.md` | Reference | Timezone mixing, DB timestamp semantics, locale formatting | Step 1, 2 |
| `assets/test_tier_matrix_template.md` | Template | Failure mode to test tier allocation table | Step 3 |
| `assets/smoke_suite_template.md` | Template | PR smoke suite specification template | Step 5 |
| `assets/adversarial_regression_template.md` | Template | Regression test backlog with exploit patterns | Step 6 |
| `assets/packaging_checklist_template.md` | Template | Dependency and build integrity checklist | Step 7 |
| `assets/command_map_template.md` | Template | Test command definitions per execution context | Step 8 |

## Best Practices

### Production Gap First, Test Count Second

- Never start by asking "how many tests do we need?"
- Start by asking "what production failures are invisible to our current tests?"
- A single well-placed integration test against a real PostgreSQL instance is worth more than 50 unit tests running against SQLite

### Persistence Over Presentation

- Every E2E test that checks UI display MUST also verify the underlying data store
- "Success toast appeared" is not a valid assertion -- verify the database row exists, has correct values, and timestamps are properly stored
- Load `references/persistence_verification_guide.md` for read-after-write patterns

### Runtime Budget Discipline

- PR smoke suites MUST have a runtime budget (target: 2-5 minutes)
- Tests that exceed the budget get demoted to nightly, not skipped
- Track actual vs budgeted runtime and alert on drift
- Fast feedback loops keep developers engaged; slow suites get ignored

### Mock Minimization Strategy

- Mocks are acceptable for: external rate-limited APIs, payment processors in test, third-party webhook senders
- Mocks are NOT acceptable for: your own database, your own file storage, your own message queue
- Every mock should have a corresponding integration test that uses the real dependency
- Document which mocks exist and why -- unreviewed mocks become invisible risk

### Adversarial Thinking

- For every feature, ask: "How would a malicious user or a chaotic system break this?"
- Past defects are the best source of adversarial test ideas -- every RCA should produce at least one regression test
- Load `references/adversarial_test_patterns.md` for systematic exploit patterns

### Environment Parity in CI

- CI should match production as closely as possible: same DB engine, same OS family, same timezone config
- Use service containers (e.g., PostgreSQL in GitHub Actions) rather than in-memory substitutes
- Pin dependency versions in CI to match production lockfiles
- Load `references/packaging_integrity_guide.md` for container and dependency alignment
