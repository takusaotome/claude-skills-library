# Adversarial Regression Backlog

Track regression tests derived from past defects and proactive adversarial patterns. Each entry ensures a specific failure mode can never recur without being detected by automated tests.

## Instructions

1. For each past defect or RCA, create an entry describing the exploit/failure pattern
2. Define the minimal reproducible scenario (smallest test that would catch it)
3. Specify the expected protected behavior (what the system should do instead of failing)
4. Determine the regression scope (related areas needing similar protection)
5. Assign priority: P0 (must have before next release), P1 (within sprint), P2 (backlog)

## Regression Backlog

### From Past Defects

| # | Source Defect | Exploit / Failure Pattern | Minimal Reproducible Scenario | Expected Protected Behavior | Regression Scope | Priority | Status |
|---|--------------|--------------------------|------------------------------|---------------------------|-----------------|----------|--------|
| 1 | INC-2024-003: PostgreSQL UPSERT failure in production | Application uses `INSERT OR REPLACE` (SQLite syntax) which fails on PostgreSQL `ON CONFLICT` syntax | Insert a record, then insert again with same unique key using the application's upsert method against PostgreSQL | Upsert succeeds: record created on first call, updated on second call; no SQL error | All repository methods that perform upsert or insert-or-update operations | P0 | To Do |
| 2 | BUG-1247: Order saved but not in DB | API handler catches `IntegrityError`, logs it, but returns HTTP 200 with success message; order not persisted | Create order via API with a foreign key referencing non-existent product; observe response status and DB state | API returns HTTP 400/409 with error details; no row in `orders` table; no success message to user | All API handlers that perform database writes; verify error propagation pattern | P0 | To Do |
| 3 | INC-2024-007: TypeError on datetime comparison | Code compares `datetime.now()` (naive) with DB-returned `TIMESTAMPTZ` value (aware) in a sort operation | Create two records with timestamps; call sort/comparison function that mixes aware and naive datetimes | All datetime comparisons use UTC-aware datetimes; no `TypeError`; correct chronological ordering | All code paths that compare datetimes from different sources (user input, DB, API response) | P0 | To Do |
| 4 | BUG-1189: Missing import in production container | `import pandas` works in dev (globally installed) but fails in Docker image (not in requirements.txt) | Run import smoke test for all application modules in clean container environment | All production imports succeed; any missing dependency is caught at build time, not runtime | All modules listed in application source; verify requirements.txt completeness | P1 | To Do |
| 5 | BUG-1302: Stale lockfile causes version mismatch | `package-lock.json` not updated after `package.json` change; CI installs different version than dev | Run `npm ci` in clean directory; should fail if lockfile is stale | `npm ci` either succeeds with correct versions or fails loudly; never silently installs wrong version | All lockfile changes must be committed alongside package manifest changes | P1 | To Do |

### Proactive Adversarial Patterns

| # | Source Defect | Exploit / Failure Pattern | Minimal Reproducible Scenario | Expected Protected Behavior | Regression Scope | Priority | Status |
|---|--------------|--------------------------|------------------------------|---------------------------|-----------------|----------|--------|
| 6 | (Proactive) SQL Injection | User input in search field concatenated into SQL query string | Submit search query: `'; DROP TABLE users; --` | Query uses parameterized statements; malicious input treated as literal string; no SQL execution | All endpoints accepting user text input that participate in DB queries | P0 | To Do |
| 7 | (Proactive) Auth bypass via header | API trusts `X-User-ID` header from client without server-side session validation | Send request to protected endpoint with fabricated `X-User-ID` header but no valid session token | Server rejects request with 401; user identity derived only from validated session/token | All authenticated API endpoints; verify auth middleware applies to each | P1 | To Do |
| 8 | (Proactive) Path traversal in file download | User-controlled filename parameter used to construct file path without sanitization | Request file download with filename: `../../../etc/passwd` | Server resolves canonical path; rejects requests outside allowed directory; returns 403/404 | All file upload/download endpoints; template rendering with user-supplied paths | P1 | To Do |
| 9 | (Proactive) Double submission | User clicks "Submit" button twice rapidly; two identical records created | Send same POST request twice within 100ms with same idempotency key | Second request returns same response as first; only one record created in database | All create/submit endpoints; payment processing; form submissions | P1 | To Do |
| 10 | (Proactive) Invalid state transition | API called to "approve" a record that is already "cancelled" | Call approve endpoint with order in "cancelled" status | Server returns 409 Conflict; order status unchanged; audit log records rejected transition attempt | All state machine transitions; workflow engines; status update endpoints | P2 | To Do |

## Status Legend

| Status | Meaning |
|--------|---------|
| To Do | Test not yet written |
| In Progress | Test being developed |
| Done | Test written, passing, and in CI |
| Blocked | Cannot implement due to dependency or architecture issue |
| Monitoring | Covered by runtime monitoring instead of test (document why) |

## Priority Definitions

| Priority | Meaning | Timeline |
|----------|---------|----------|
| P0 | Critical: past production incident or high-blast-radius vulnerability | Must complete before next release |
| P1 | Important: likely failure pattern or medium-blast-radius risk | Within current sprint |
| P2 | Desirable: low-probability or low-impact pattern | Backlog; implement when capacity allows |

## Backlog Health Metrics

Track these metrics to measure regression backlog effectiveness:

| Metric | Current | Target |
|--------|---------|--------|
| Total entries | | |
| P0 items Done | | 100% |
| P1 items Done | | > 80% |
| P2 items Done | | > 50% |
| Items Blocked | | 0 |
| Items added from new incidents | | Track monthly |
| False positive rate (flaky regression tests) | | < 5% |

## Adding New Entries

When a new production defect occurs or a new vulnerability is discovered:

1. Create entry immediately (even before the fix is deployed)
2. Assign priority based on blast radius and recurrence likelihood
3. Define minimal reproducible scenario while the defect is fresh
4. Link to incident report or bug ticket for traceability
5. After the test is written, verify it fails against the unfixed code (proves the test catches the bug)
6. Mark as Done only after the test is in CI and passing
