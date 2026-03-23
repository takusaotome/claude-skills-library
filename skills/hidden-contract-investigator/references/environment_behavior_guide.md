# Environment Behavior Guide

## Purpose

This reference documents the most common ways that code behavior silently changes across environments (development, staging, production) and across technology stacks (SQLite vs. PostgreSQL, mock vs. real dependencies, etc.). Use during Workflow 3 (Actual Contract Extraction) and Workflow 6 (Verification Design) to identify environment-dependent hidden contracts.

---

## Category 1: Dev / Staging / Prod Behavioral Differences

### Configuration-Driven Behavior Divergence

Code that branches on environment variables or configuration settings creates hidden contracts that are only exercisable in specific environments.

**Common Patterns:**

#### Pattern 1.1: Feature Flag Environment Coupling

```python
def process_payment(order):
    if settings.ENV == "production":
        return stripe.charge(order.total)   # Real payment
    else:
        return {"status": "success", "id": "test_123"}  # Fake success
```

**Hidden contract**: The function's return type and shape differ between environments. In dev/staging, the return is a static dict; in production, it's a Stripe response object with additional fields.

**Risk**: Code tested in dev may depend on fields that don't exist in the Stripe response, or may not handle Stripe-specific errors.

**Verification approach**: Mock the payment gateway in tests but validate the response shape against the real API schema.

#### Pattern 1.2: Debug-Only Code Paths

```python
def generate_report(data):
    if settings.DEBUG:
        # Skip validation for faster iteration
        pass
    else:
        validate_data_integrity(data)  # Only runs in prod
    return render_report(data)
```

**Hidden contract**: Data validation only runs in production. A data integrity bug caught in production would never surface in development.

**Risk**: Silent data corruption that only manifests after deployment.

**Verification approach**: Always run with validation enabled in CI/CD tests, regardless of environment flag.

#### Pattern 1.3: Connection Pool Configuration

```python
# dev: pool_size=1, timeout=30s
# staging: pool_size=5, timeout=10s
# prod: pool_size=20, timeout=5s
```

**Hidden contract**: Concurrency bugs and timeout behaviors only manifest under production-like pool configuration. A function that works fine with pool_size=1 may deadlock with pool_size=20.

**Risk**: Race conditions, deadlocks, and timeout failures that are invisible in development.

### Logging and Monitoring Differences

- **Log level divergence**: DEBUG logging in dev captures all state changes; production INFO logging misses intermediate states
- **Structured logging**: Dev uses plain text, prod uses JSON -- log parsing code may fail if tested only against one format
- **APM instrumentation**: Performance monitoring adds overhead and behavior (tracing context propagation) that doesn't exist in dev
- **Error reporting**: Sentry/Datadog error capture may modify exception handling behavior (e.g., adding breadcrumbs)

### Network and Infrastructure Differences

- **DNS resolution**: `localhost` vs. service discovery vs. load balancer -- DNS failure modes differ
- **TLS/SSL**: Dev may use self-signed certs or no TLS; prod requires valid certificates with different handshake characteristics
- **Network latency**: Local calls have sub-millisecond latency; prod calls may take 100ms+ -- timeout thresholds that work locally may be too tight for prod
- **Firewall rules**: Functions that call external APIs may succeed in dev (no firewall) but fail in prod (restricted egress)

### Verification Checklist for Dev/Staging/Prod

- [ ] List all environment-conditional branches in the target code
- [ ] Identify which code paths are exercised only in production
- [ ] Check for debug/test shortcuts that bypass critical logic
- [ ] Verify that connection configuration (pool size, timeout) matches production in test
- [ ] Ensure error handling is tested with production-like error responses
- [ ] Check if monitoring/logging changes behavior (e.g., async flushing blocks on shutdown)

---

## Category 2: SQLite vs. PostgreSQL Behavioral Differences

When development uses SQLite and production uses PostgreSQL (or MySQL), numerous behavioral contracts silently differ.

### Type System Differences

| Aspect | SQLite | PostgreSQL | Risk |
|--------|--------|------------|------|
| Type enforcement | Dynamic (stores any type in any column) | Static (rejects type mismatch) | Code that writes int to a text column works in SQLite, fails in PostgreSQL |
| Boolean type | Stored as 0/1 integer | Native `BOOLEAN` type | `WHERE active = 1` works in SQLite; PostgreSQL needs `WHERE active = TRUE` |
| Date/time type | Stored as TEXT or REAL | Native `TIMESTAMP`, `DATE` | Date comparison operators behave differently |
| JSON type | TEXT storage only | Native `JSONB` with operators | `->` and `->>` operators work differently |
| Array type | Not supported | Native `ARRAY` type | Code using arrays must use workarounds in SQLite |
| DECIMAL precision | Approximated as REAL | True fixed-point decimal | Financial calculations may produce different results |

### Query Behavior Differences

| Aspect | SQLite | PostgreSQL | Risk |
|--------|--------|------------|------|
| String comparison | Case-sensitive by default | Case-sensitive by default, but `ILIKE` available | Different case-handling assumptions |
| LIMIT/OFFSET | `LIMIT -1` means no limit | `LIMIT ALL` or omit clause | Negative limit causes error in PostgreSQL |
| GROUP BY | Allows non-aggregated columns | Strict: all non-aggregated columns must be in GROUP BY | Queries that work in SQLite fail in PostgreSQL |
| UPSERT syntax | `INSERT OR REPLACE` | `INSERT ... ON CONFLICT DO UPDATE` | Different syntax, different semantics |
| Concurrent writes | File-level locking | Row-level locking | SQLite blocks all concurrent writes; PostgreSQL allows them |
| Transaction DDL | DDL is transactional | DDL is transactional (but some operations take exclusive locks) | Lock contention differs |

### Migration-Specific Risks

- **Auto-increment gaps**: SQLite reuses IDs after deletion; PostgreSQL sequences never reuse
- **Foreign key enforcement**: SQLite requires `PRAGMA foreign_keys = ON` per connection; PostgreSQL always enforces
- **Null sorting**: SQLite sorts NULLs as smallest; PostgreSQL sorts NULLs as largest (configurable with `NULLS FIRST/LAST`)
- **String concatenation**: SQLite uses `||`; PostgreSQL uses `||` (same) but behavior with NULL differs (NULL || 'a' = NULL in PostgreSQL, some SQLite versions may differ)
- **Index behavior**: Partial indexes, expression indexes, and GIN/GiST indexes are PostgreSQL-specific

### Verification Checklist for DB Dialect

- [ ] Run the full test suite against both SQLite and PostgreSQL
- [ ] Check all queries for dialect-specific syntax
- [ ] Verify type coercion behavior for all column types used by the target
- [ ] Test concurrent access patterns if any exist
- [ ] Verify NULL handling in comparisons, sorting, and concatenation
- [ ] Check UPSERT/merge patterns for dialect compatibility

---

## Category 3: Mock vs. Real Dependency Behavioral Differences

Test doubles (mocks, stubs, fakes) create a hidden contract problem: the mock's behavior is an assumption about the real dependency's behavior, and that assumption may be wrong.

### Common Mock Divergence Patterns

#### Pattern 3.1: Missing Error Responses

```python
# Mock (in test)
mock_api.get_user.return_value = {"id": 1, "name": "Test"}

# Real API also returns:
# - 404 with {"error": "not_found"} body
# - 429 with retry-after header
# - 500 with HTML error page
# - 200 with {"id": 1, "name": "Test", "metadata": {...}} (extra fields)
```

**Risk**: Tests never exercise error handling or response parsing for unexpected fields.

#### Pattern 3.2: Timing and Ordering Assumptions

```python
# Mock: always returns immediately
mock_queue.publish.return_value = True

# Real queue:
# - May block for 100ms-5s under load
# - May reorder messages
# - May duplicate messages on retry
# - May fail silently (return True but message is lost)
```

**Risk**: Code works in tests but fails under real queue's timing and ordering guarantees.

#### Pattern 3.3: State Accumulation

```python
# Mock: stateless, returns same thing every call
mock_cache.get.return_value = None  # Always cache miss

# Real cache:
# - First call: cache miss (returns None)
# - Second call: cache hit (returns cached value)
# - After TTL: cache miss again
```

**Risk**: Code that depends on cache behavior (warm-up, TTL, eviction) is never tested.

### Contract Test Strategy for Mock Divergence

For each mocked dependency, create a **contract test** that runs against the real dependency (in CI or staging):

```
Contract Test: verify mock matches real API
  Given: Mock returns {"id": 1, "name": "Test"} for get_user(1)
  When: Call real API with get_user(1)
  Then: Response contains at least {"id": ..., "name": ...}
        AND response type matches mock's return type
```

### Verification Checklist for Mock/Real Divergence

- [ ] List all mocked dependencies in the target's test suite
- [ ] For each mock, verify the mock's return type matches the real dependency's return type
- [ ] Check if mocks cover error responses (not just happy path)
- [ ] Verify timing assumptions (mocks return instantly; real dependencies have latency)
- [ ] Check if mock state behavior matches real state behavior (caching, rate limiting)
- [ ] Run integration tests against real dependencies in CI (at least nightly)

---

## Category 4: Aware vs. Naive Datetime Behavioral Differences

The distinction between timezone-aware and timezone-naive datetimes is a pervasive source of hidden contracts, especially in Python.

### Python-Specific Datetime Contracts

```python
from datetime import datetime, timezone

# Naive datetime (no timezone info)
naive = datetime(2025, 3, 15, 10, 0, 0)
# naive.tzinfo is None

# Aware datetime (has timezone info)
aware = datetime(2025, 3, 15, 10, 0, 0, tzinfo=timezone.utc)
# aware.tzinfo is timezone.utc
```

### Hidden Contract: Comparison

```python
# This RAISES TypeError in Python 3:
naive > aware  # TypeError: can't compare offset-naive and offset-aware datetimes

# But this works silently and may give wrong results:
naive.isoformat()  # "2025-03-15T10:00:00" (no timezone info)
aware.isoformat()  # "2025-03-15T10:00:00+00:00" (with timezone)
```

**Risk**: If one function returns naive and another returns aware, comparison and sorting will crash or produce incorrect results.

### Hidden Contract: now() vs. utcnow()

```python
# These return DIFFERENT types:
datetime.now()     # Naive, in server's local timezone
datetime.utcnow()  # Naive, in UTC (but tzinfo is still None!)
datetime.now(timezone.utc)  # Aware, in UTC (correct approach)
```

**Risk**: `datetime.utcnow()` returns a naive datetime that represents UTC -- but Python doesn't know it's UTC. Mixing it with `datetime.now()` produces wrong duration calculations.

### Hidden Contract: ORM Datetime Handling

```python
# Django with USE_TZ=True:
#   - Stores aware datetimes in UTC
#   - Returns aware datetimes
#   - Raises warning if you save naive datetime

# Django with USE_TZ=False:
#   - Stores naive datetimes in server timezone
#   - Returns naive datetimes
#   - No warning for naive datetimes

# SQLAlchemy:
#   - Default Column(DateTime): stores naive
#   - Column(DateTime(timezone=True)): stores aware
#   - Behavior depends on DB dialect
```

**Risk**: Code that works with one ORM configuration fails with another. Migrating from `USE_TZ=False` to `USE_TZ=True` silently changes every datetime in the system.

### Hidden Contract: Serialization

```python
import json

# Naive datetime serialization:
naive.isoformat()  # "2025-03-15T10:00:00"

# Aware datetime serialization:
aware.isoformat()  # "2025-03-15T10:00:00+00:00"

# Parsing back:
datetime.fromisoformat("2025-03-15T10:00:00")       # Naive
datetime.fromisoformat("2025-03-15T10:00:00+00:00")  # Aware
```

**Risk**: If serialization drops timezone info, the round-trip changes an aware datetime to naive, losing the timezone contract.

### Verification Checklist for Datetime Contracts

- [ ] Determine whether the target function produces aware or naive datetimes
- [ ] Check if the function mixes aware and naive in comparisons or arithmetic
- [ ] Verify which `now()` variant is used (naive local, naive UTC, or aware UTC)
- [ ] Check ORM configuration for timezone handling
- [ ] Verify serialization preserves timezone info on round-trip
- [ ] Test date arithmetic across DST transitions
- [ ] Test date boundary conditions (end of month, leap year, year boundary)
- [ ] Check if the function's datetime contract matches its callers' expectations

---

## Environment Boundary Summary

| Environment Boundary | Silent Failure Risk | Detection Strategy |
|---------------------|--------------------|--------------------|
| Dev/Staging/Prod config | High | Audit all environment-conditional branches |
| SQLite/PostgreSQL dialect | High | Run tests against both databases |
| Mock/Real dependency | Medium | Contract tests against real dependencies |
| Aware/Naive datetime | High | Static analysis + round-trip tests |
| Locale/Number format | Medium | Test with multiple locale settings |
| TLS/Network topology | Low-Medium | Integration tests in staging environment |

The most dangerous environment boundaries are those where failures are **silent** -- the code runs without error but produces incorrect results. Timezone and database dialect boundaries rank highest because they commonly produce silent data corruption rather than visible errors.
