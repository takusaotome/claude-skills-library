# Test Tier Allocation Matrix

Map each identified failure mode to its optimal test tier. This matrix is the primary output of Steps 1-3 of the Production Parity Test Designer workflow.

## Instructions

1. List every production gap identified in Step 1
2. For each gap, enumerate specific failure modes from Step 2
3. Assign each failure mode to the appropriate test tier from Step 3
4. Mark whether the test must run in PR CI
5. Specify the data set or fixture required
6. Define the specific assertion that verifies protection
7. Assign an owner responsible for maintaining the test

## Matrix

| # | Failure Mode | Production Gap | Test Tier | Must Run in PR? | Data Set / Fixture | Assertion | Owner |
|---|-------------|---------------|-----------|:---------------:|-------------------|-----------|-------|
| 1 | `INSERT OR REPLACE` syntax fails on PostgreSQL | DB dialect (SQLite vs PostgreSQL) | Integration | Yes | Seed user record + conflict record | `UPSERT` succeeds; record count unchanged; values updated | Backend team |
| 2 | UI shows success toast but no row in `orders` table | Persistence not verified | E2E + Smoke | Yes (smoke) | Create order via UI | Read-after-write: `SELECT * FROM orders WHERE id = :new_id` returns 1 row | QA team |
| 3 | `import cv2` fails in production container | Missing native dependency | Packaging | No (nightly) | Clean container build | `python -c "import cv2"` exits 0 | DevOps |
| 4 | `TypeError` comparing aware and naive `datetime` | Timezone aware/naive mixing | Unit + Integration | Yes | UTC-aware + naive datetime pair | No `TypeError`; result is timezone-aware UTC | Backend team |
| 5 | `GROUP BY` query returns extra columns on PostgreSQL strict mode | DB dialect (GROUP BY strictness) | Integration | Yes | Multi-row dataset with grouping | Query executes without error; result matches expected aggregation | Backend team |
| 6 | `LIKE 'abc%'` is case-sensitive on PostgreSQL, not on SQLite | DB dialect (case sensitivity) | Integration | Yes | Records with mixed case | Search returns correct results on target DB engine | Backend team |
| 7 | Missing `API_KEY` env var causes silent fallback to demo mode | Env var configuration drift | Smoke | Yes | Unset `API_KEY` env var | Application raises startup error or logs explicit warning | DevOps |
| 8 | `npm ci` fails because `package-lock.json` is stale | Lockfile misalignment | Packaging | Yes | Fresh `npm ci` in clean dir | Install completes without error; all modules import | Frontend team |
| 9 | Soft-deleted records appear in dashboard count | Visible state vs stored state divergence | E2E | No (nightly) | 10 records, 3 soft-deleted | Dashboard count = 7; API list length = 7 | QA team |
| 10 | Concurrent approve + cancel on same order leaves inconsistent state | Race condition / optimistic locking | Integration | No (nightly) | Order in "pending" state | One operation succeeds, other returns conflict error; final state is consistent | Backend team |

## Tier Legend

| Tier | Scope | Typical Runtime | Runs In |
|------|-------|----------------|---------|
| Unit | Pure logic, no I/O | < 30s total | Local, PR CI |
| Integration | Real DB, real services | 1-5 min total | PR CI |
| E2E | Full UI + API + DB | 5-15 min total | Staging |
| Smoke | Minimum parity checks | 2-5 min total | PR CI (required) |
| Packaging | Build/install/import | 1-3 min total | Pre-release |
| Nightly | Full parity suite | 15-60 min total | Scheduled nightly |

## Coverage Summary

After completing the matrix, fill in this summary:

| Tier | Total Tests | PR-Required | Estimated Runtime |
|------|------------|:-----------:|-------------------|
| Unit | | | |
| Integration | | | |
| E2E | | | |
| Smoke | | | |
| Packaging | | | |
| Nightly | | | |
| **Total** | | | |

## Gap Analysis

List any failure modes that could not be assigned to a test tier:

| Failure Mode | Reason Not Testable | Alternative Mitigation |
|-------------|--------------------|-----------------------|
| | | |

These gaps should be covered by monitoring, alerting, or operational procedures instead.
