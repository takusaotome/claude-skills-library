# Test Tier Strategy

A comprehensive guide to separating test responsibilities across tiers, balancing speed against reliability, and determining what belongs in PR CI versus nightly or staging suites.

## Tier Definitions

### Unit Tests

**Responsibility**: Verify isolated logic without external dependencies.

- Pure function correctness, boundary values, input validation
- Format conversion, parsing, serialization logic
- Business rule calculations, state machine transitions (in-memory)
- Error handling for invalid inputs

**Characteristics**:
- No I/O (no database, no filesystem, no network)
- Millisecond execution per test
- Deterministic (no randomness, no timing)
- Can run in any order, fully parallelizable

**What Does NOT Belong Here**:
- Anything requiring a real database connection
- Anything that validates inter-component behavior
- Mocked database calls pretending to be "unit tests" (these hide dialect gaps)

**Speed Target**: Entire unit suite completes in under 30 seconds.

### Integration Tests

**Responsibility**: Verify multi-component interactions with real external dependencies.

- Real database operations (CRUD, transactions, migrations)
- Real repository/storage layer operations
- Service-to-service communication (with real or contract-tested stubs)
- File I/O with actual filesystem
- Message queue produce/consume cycles

**Characteristics**:
- Requires running services (database, cache, queue)
- Second-to-minute execution per test
- May require test data setup and teardown
- Order-sensitive if sharing state (prefer isolation)

**Critical Integration Patterns**:

| Pattern | What It Catches |
|---------|----------------|
| Real DB dialect query | SQL syntax that works in SQLite but fails in PostgreSQL |
| Transaction rollback | Partial writes that leave data inconsistent |
| Migration round-trip | Schema migration up + down leaves DB in clean state |
| Connection pool exhaustion | Tests that leak connections under concurrent load |
| Concurrent write conflict | Optimistic locking failures, lost updates |

**Speed Target**: Integration suite completes in 1-5 minutes.

### End-to-End (E2E) Tests

**Responsibility**: Verify complete user workflows from UI through persistence to business-visible outcome.

- User action -> API call -> business logic -> persistence -> response
- Multi-step workflows (create -> edit -> approve -> complete)
- Cross-system integrations visible to users
- Report generation and data aggregation

**Critical E2E Rule**: Every E2E test MUST verify persistence, not just UI display.

**Anti-Pattern (Proxy Metric)**:
```
1. Click "Save" button
2. Assert: success toast is displayed   # <-- This is the ONLY assertion
# MISSING: Assert the database actually contains the saved data
```

**Correct Pattern**:
```
1. Click "Save" button
2. Assert: success toast is displayed
3. Query database directly
4. Assert: row exists with correct values
5. Assert: timestamp is within expected range
6. Assert: audit log entry was created
```

**Characteristics**:
- Slowest tier (seconds to minutes per test)
- Most brittle (UI changes break tests)
- Most realistic (closest to actual user experience)
- Requires full environment (UI + API + DB + services)

**Speed Target**: E2E suite completes in 5-15 minutes (staging), subset in PR.

### Smoke Tests

**Responsibility**: Minimum production parity verification that gates every PR.

Smoke tests are NOT simplified versions of other tests. They are specifically designed to catch **production-only failures** that unit and basic integration tests miss.

**Smoke Test Selection Criteria**:

| Criterion | Question | If Yes -> Include in Smoke |
|-----------|----------|---------------------------|
| Dialect dependency | Does the code use DB-specific syntax? | Yes |
| Runtime import | Does the feature depend on native libraries? | Yes |
| Persistence criticality | Does a save operation affect business data? | Yes |
| Timezone sensitivity | Does the code handle datetime with mixed awareness? | Yes |
| Environment sensitivity | Does behavior change with env vars or config? | Yes |

**Smoke tests must**:
- Complete within the PR runtime budget (2-5 minutes total)
- Use real production-equivalent dependencies (real DB engine, real imports)
- Have clear pass/fail semantics (no "flaky is OK" tolerance)
- Be maintained with the same rigor as production code

**Speed Target**: Smoke suite completes in 2-5 minutes.

### Packaging Tests

**Responsibility**: Verify that the built artifact (package, container image, installer) works correctly.

- All production imports succeed in the built artifact
- Dependency versions match lockfile specifications
- Container image starts and responds to health check
- CLI entry points execute without import errors
- Configuration files are included and parseable

**When Packaging Tests Save You**:
- `pip install` succeeds but `import mypackage` fails (missing native dependency)
- Docker build succeeds but container crashes on start (missing env var)
- Lockfile specifies version A but installation resolves to version B
- Package includes development-only files (test fixtures, debug configs)

**Speed Target**: Packaging verification completes in 1-3 minutes.

### Nightly / Heavy Parity Tests

**Responsibility**: Comprehensive production parity verification that is too slow for PR CI.

- Full dataset tests (large volume, edge case distributions)
- Performance baselines (response time, throughput, memory usage)
- Cross-timezone full matrix (all supported timezones)
- Full adversarial regression suite
- Multi-region / multi-locale verification
- Chaos engineering scenarios (service unavailability, network partition)

**Speed Target**: Nightly suite completes in 15-60 minutes.

## Speed vs Reliability Tradeoffs

### The Feedback Loop Principle

The value of a test is proportional to how quickly developers see the result.

| Tier | Feedback Time | Developer Impact |
|------|--------------|-----------------|
| Unit | Immediate (< 30s) | Developer runs during coding, catches logic errors instantly |
| Integration | Fast (1-5 min) | Runs in PR CI, catches dependency errors before review |
| Smoke | Fast (2-5 min) | Runs in PR CI, catches production parity gaps before merge |
| E2E | Moderate (5-15 min) | Runs in staging, catches workflow errors before release |
| Packaging | Moderate (1-3 min) | Runs before release, catches build/deploy errors |
| Nightly | Slow (15-60 min) | Runs overnight, catches comprehensive parity gaps next morning |

### Budget Allocation for PR CI

Total PR CI budget should be 5-10 minutes. Recommended allocation:

| Component | Budget | Percentage |
|-----------|--------|-----------|
| Unit tests | 30s | 8% |
| Lint + type check | 30s | 8% |
| Integration (core) | 2 min | 33% |
| Smoke suite | 3 min | 50% |
| **Total** | **6 min** | **100%** |

### What Happens When Tests Are Too Slow

When PR CI exceeds 10-15 minutes:
1. Developers stop waiting for results and context-switch
2. Multiple PRs stack up, making failures harder to attribute
3. Teams start marking flaky tests as "skip" instead of fixing
4. The entire test suite loses credibility and eventually gets ignored

**Mitigation**: Ruthlessly enforce runtime budgets. Demote slow tests to nightly tier rather than slowing PR feedback.

## What Belongs in PR CI

### Must Include

- All unit tests (they are fast by definition)
- Lint, type checking, format validation
- Smoke tests that cover production-critical gaps:
  - At least one real-DB operation
  - Import verification for native dependencies
  - One persistence read-after-write check
  - Timezone boundary check if datetime handling exists

### Should Include (If Within Budget)

- Core integration tests against real services (DB, cache)
- Contract tests for inter-service APIs
- Security-critical checks (auth, input validation)

### Must NOT Include

- Full E2E suite (too slow, too brittle for PR)
- Performance benchmarks (noisy in shared CI, run nightly)
- Large dataset tests (run nightly)
- Visual regression tests (run separately with screenshot comparison)
- Manual approval gates (block developer flow)

## Tier Escalation Rules

When a production defect escapes:

1. **Identify which tier should have caught it**: Use the failure mode classification (logic error -> unit, dependency error -> integration, workflow error -> E2E, build error -> packaging)
2. **Write the regression test at that tier**: Do not default to E2E for everything
3. **Add a smoke test if the failure is high-blast-radius**: If the defect could affect many users or core business data, add a fast smoke check to PR CI
4. **Review adjacent tests**: Check if similar gaps exist in related features

## Anti-Patterns to Avoid

### The Test Pyramid Inversion

Having more E2E tests than unit tests indicates:
- Business logic is tangled with I/O (refactor to separate)
- Teams don't trust unit tests (improve assertion quality)
- No clear tier allocation strategy (use this skill)

### The Mock Everything Approach

Mocking all external dependencies makes integration tests meaningless:
- If your "integration test" uses a mock database, it is actually a unit test
- Mock only what you cannot control (third-party APIs with rate limits)
- Your own infrastructure (DB, cache, queue) should be real in integration tests

### The Coverage Target Trap

90% code coverage with proxy metrics is worse than 60% coverage with real assertions:
- Coverage measures lines executed, not correctness verified
- A test that calls a function but asserts nothing contributes to coverage but not quality
- Focus on assertion quality and failure mode coverage, not line coverage percentage
