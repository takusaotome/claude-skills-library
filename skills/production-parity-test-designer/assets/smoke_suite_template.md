# PR Smoke Suite Specification

Define the minimum set of production parity checks that must pass in every pull request. The smoke suite is the last line of defense before code reaches the main branch.

## Instructions

1. Select high-priority items from the Test Tier Matrix marked "Must Run in PR"
2. Group them into named smoke categories
3. Assign a runtime budget to each category (total must stay within 2-5 minutes)
4. Define the environment requirements (e.g., PostgreSQL service container in CI)
5. Specify blockers: what prevents this smoke test from running?
6. Define pass/fail meaning: what does a failure in this category indicate?

## Suite Overview

| Property | Value |
|----------|-------|
| Suite Name | `[project-name]-pr-smoke` |
| Total Runtime Budget | 3 minutes |
| Trigger | Every pull request to `main` / `develop` |
| Blocking | Yes -- PR cannot merge if smoke fails |
| Environment | CI with PostgreSQL 15 service container |
| Command | `pytest tests/ -m smoke --timeout=180` |

## Smoke Categories

### 1. DB Dialect Smoke

| Property | Value |
|----------|-------|
| Category Name | `db-dialect-smoke` |
| Purpose | Verify SQL queries execute correctly on the production database engine (PostgreSQL) |
| Runtime Budget | 60 seconds |
| Environment | PostgreSQL 15 service container with test schema |
| Blockers | PostgreSQL service not available in CI runner |
| Pass Meaning | All SQL queries use correct dialect syntax |
| Fail Meaning | At least one query uses SQLite-specific syntax that fails on PostgreSQL |

**Included checks**:

| # | Check | Assertion | Failure Mode Covered |
|---|-------|-----------|---------------------|
| 1 | UPSERT operation | Record created or updated without error | SQLite `INSERT OR REPLACE` vs PostgreSQL `ON CONFLICT` |
| 2 | GROUP BY strictness | Aggregation query returns expected results | Non-aggregated columns in SELECT with GROUP BY |
| 3 | Case-sensitive LIKE | Search returns correct results | PostgreSQL `LIKE` is case-sensitive vs SQLite default |
| 4 | Boolean column query | `WHERE active = true` works correctly | PostgreSQL native BOOLEAN vs SQLite INTEGER |

### 2. Import and Dependency Smoke

| Property | Value |
|----------|-------|
| Category Name | `import-smoke` |
| Purpose | Verify all production modules can be imported without error |
| Runtime Budget | 15 seconds |
| Environment | Standard CI runner (no additional services) |
| Blockers | None (should always be runnable) |
| Pass Meaning | All declared dependencies are installed and importable |
| Fail Meaning | A dependency is missing from requirements or has an import-time error |

**Included checks**:

| # | Check | Assertion | Failure Mode Covered |
|---|-------|-----------|---------------------|
| 1 | Import all application modules | `importlib.import_module(mod)` succeeds for each | Missing dependency, circular import |
| 2 | Verify native extensions | `import psycopg2; import PIL` succeeds | Missing system library |
| 3 | Version compatibility | `pkg.__version__` matches lockfile | Version mismatch |

### 3. Persistence Verification Smoke

| Property | Value |
|----------|-------|
| Category Name | `persistence-smoke` |
| Purpose | Verify that at least one critical write path persists data to the database |
| Runtime Budget | 45 seconds |
| Environment | PostgreSQL 15 service container with test schema |
| Blockers | PostgreSQL service not available in CI runner |
| Pass Meaning | Write operations actually store data in the database |
| Fail Meaning | Silent write failure -- application reports success but data not persisted |

**Included checks**:

| # | Check | Assertion | Failure Mode Covered |
|---|-------|-----------|---------------------|
| 1 | Create record via API | Read-after-write returns the record from DB | Fake success without write |
| 2 | Update record via API | Updated fields match in DB read-back | Swallowed exception on update |
| 3 | Audit log creation | Audit log entry exists after write operation | History write missing |

### 4. Timezone Boundary Smoke

| Property | Value |
|----------|-------|
| Category Name | `timezone-smoke` |
| Purpose | Verify datetime operations handle timezone-aware and timezone-naive values correctly |
| Runtime Budget | 20 seconds |
| Environment | Standard CI runner (no additional services) |
| Blockers | None |
| Pass Meaning | No `TypeError` from aware/naive mixing; correct timezone conversions |
| Fail Meaning | Code mixes aware and naive datetimes, or timezone conversion is incorrect |

**Included checks**:

| # | Check | Assertion | Failure Mode Covered |
|---|-------|-----------|---------------------|
| 1 | Aware + naive comparison | No `TypeError`; correct result | Aware/naive mixing |
| 2 | UTC round-trip through DB | Timezone info preserved after read-back | DB strips timezone on storage |
| 3 | Day boundary assignment | Event near midnight assigned to correct date | Wrong date due to timezone offset |

### 5. Serialization Smoke

| Property | Value |
|----------|-------|
| Category Name | `serialization-smoke` |
| Purpose | Verify data serialization round-trips without loss or corruption |
| Runtime Budget | 20 seconds |
| Environment | Standard CI runner (no additional services) |
| Blockers | None |
| Pass Meaning | Data survives serialize/deserialize cycle without loss |
| Fail Meaning | Serialization produces incorrect output or deserialization fails |

**Included checks**:

| # | Check | Assertion | Failure Mode Covered |
|---|-------|-----------|---------------------|
| 1 | JSON round-trip with edge cases | Null, Unicode, large numbers survive | Encoding/decoding errors |
| 2 | Datetime JSON serialization | ISO 8601 format with timezone preserved | Datetime to string conversion |
| 3 | API response format | Response matches expected schema | Schema drift between serializer versions |

## Runtime Budget Summary

| Category | Budget | % of Total |
|----------|--------|-----------|
| DB Dialect Smoke | 60s | 37% |
| Import Smoke | 15s | 9% |
| Persistence Smoke | 45s | 28% |
| Timezone Smoke | 20s | 13% |
| Serialization Smoke | 20s | 13% |
| **Total** | **160s (2m 40s)** | **100%** |

## Failure Response Protocol

| Scenario | Action |
|----------|--------|
| Single smoke category fails | Fix the failing test before merging; do not skip |
| Smoke fails due to CI infrastructure (DB not available) | Investigate CI config; do not merge until infrastructure is restored |
| Smoke is flaky (passes on retry) | Treat as a real bug; flaky smoke tests erode trust |
| Smoke exceeds runtime budget | Profile and optimize; consider moving slow checks to nightly |
| New feature needs new smoke test | Add to appropriate category; adjust runtime budget |

## CI Configuration Example

```yaml
# GitHub Actions example
smoke-tests:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:15
      env:
        POSTGRES_DB: test_db
        POSTGRES_PASSWORD: test_password
      ports:
        - 5432:5432
      options: >-
        --health-cmd pg_isready
        --health-interval 10s
        --health-timeout 5s
        --health-retries 5
  steps:
    - uses: actions/checkout@v4
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run smoke suite
      env:
        DATABASE_URL: postgresql://postgres:test_password@localhost:5432/test_db
      run: pytest tests/ -m smoke --timeout=180 -v
```
