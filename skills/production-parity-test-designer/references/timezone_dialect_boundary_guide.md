# Timezone and Dialect Boundary Guide

A detailed guide to handling timezone-related failures, database timestamp semantics, SQLite vs PostgreSQL datetime behavior, and locale-sensitive formatting. These boundaries are among the most frequent sources of production escapes because they often work in development (single timezone, permissive DB) but fail in production (multiple timezones, strict DB).

## Aware vs Naive Datetime Mixing

### The Fundamental Problem

Python (and most languages) distinguish between timezone-aware and timezone-naive datetime objects. Mixing them causes `TypeError` at comparison or arithmetic operations.

```python
from datetime import datetime, timezone

# Naive: no timezone information
naive_dt = datetime(2024, 1, 15, 10, 0, 0)
# repr: datetime.datetime(2024, 1, 15, 10, 0)

# Aware: has timezone information
aware_dt = datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc)
# repr: datetime.datetime(2024, 1, 15, 10, 0, tzinfo=datetime.timezone.utc)

# This WILL raise TypeError
try:
    result = aware_dt - naive_dt
except TypeError as e:
    print(e)  # "can't subtract offset-naive and offset-aware datetimes"
```

### Why This Works in Development but Fails in Production

| Source | Development | Production |
|--------|-------------|------------|
| `datetime.now()` | Naive (no tz) | Naive (no tz) |
| `datetime.utcnow()` | Naive (no tz) -- misleading! | Naive (no tz) |
| `datetime.now(timezone.utc)` | Aware (UTC) | Aware (UTC) |
| Database `TIMESTAMP` read | Depends on driver and column type | Depends on driver and column type |
| API response parsing | Depends on parser and format | Depends on parser and format |
| `pendulum.now()` | Aware (local tz) | Aware (server tz) |

The dangerous scenario:
1. Application uses `datetime.now()` (naive) for some operations
2. Database returns aware datetimes (e.g., PostgreSQL `TIMESTAMPTZ`)
3. Code compares them -> `TypeError` in production

### Testing Patterns for Aware/Naive Mixing

```python
import pytest
from datetime import datetime, timezone, timedelta

def test_aware_naive_comparison_safety():
    """Verify the application handles mixed datetime types."""
    aware = datetime.now(timezone.utc)
    naive = datetime.now()

    # The function under test should handle both types
    # without raising TypeError
    result = normalize_to_utc(aware)
    assert result.tzinfo is not None

    result = normalize_to_utc(naive)
    assert result.tzinfo is not None

def test_database_datetime_roundtrip():
    """Verify datetime survives a database round-trip without losing timezone."""
    original = datetime.now(timezone.utc)

    # Write to database
    save_record({"timestamp": original})

    # Read from database
    record = load_record()
    loaded = record["timestamp"]

    # Verify timezone information preserved
    assert loaded.tzinfo is not None, "Timezone lost during DB round-trip"

    # Verify value preserved (within 1 second tolerance for DB precision)
    assert abs((loaded - original).total_seconds()) < 1

def test_cross_timezone_ordering():
    """Verify records from different timezones sort correctly."""
    jst = timezone(timedelta(hours=9))
    utc = timezone.utc
    est = timezone(timedelta(hours=-5))

    # All represent different absolute times
    t1 = datetime(2024, 1, 15, 10, 0, 0, tzinfo=utc)   # 10:00 UTC
    t2 = datetime(2024, 1, 15, 20, 0, 0, tzinfo=jst)    # 11:00 UTC
    t3 = datetime(2024, 1, 15, 7, 0, 0, tzinfo=est)     # 12:00 UTC

    records = [
        {"name": "C", "timestamp": t3},  # Latest
        {"name": "A", "timestamp": t1},  # Earliest
        {"name": "B", "timestamp": t2},  # Middle
    ]

    sorted_records = sort_by_timestamp(records)
    assert [r["name"] for r in sorted_records] == ["A", "B", "C"]
```

### Recommended Datetime Strategy

1. **Always use timezone-aware datetimes internally**: `datetime.now(timezone.utc)`
2. **Never use `datetime.utcnow()`**: It returns a naive datetime despite the "utc" in the name (deprecated in Python 3.12)
3. **Convert to UTC on input boundaries**: When receiving datetime from any external source, immediately convert to UTC-aware
4. **Store as UTC in the database**: Use `TIMESTAMPTZ` (PostgreSQL) or equivalent
5. **Convert to local timezone only for display**: Format for the user's timezone at the presentation layer

## Database Timestamp Semantics

### PostgreSQL Timestamp Types

| Type | Stores TZ? | Behavior |
|------|-----------|----------|
| `TIMESTAMP` (without time zone) | No | Stores literal value; no TZ conversion |
| `TIMESTAMPTZ` (with time zone) | Yes (converts to UTC) | Stores in UTC; converts on read using session TZ |

**Critical behavior**: `TIMESTAMPTZ` always stores UTC internally. When you insert `2024-01-15 10:00:00+09:00` (JST), PostgreSQL stores `2024-01-15 01:00:00+00:00` (UTC). On read, it converts to the session's timezone.

```sql
-- Session timezone affects TIMESTAMPTZ display
SET timezone = 'Asia/Tokyo';
SELECT '2024-01-15 01:00:00+00'::timestamptz;
-- Result: 2024-01-15 10:00:00+09

SET timezone = 'US/Eastern';
SELECT '2024-01-15 01:00:00+00'::timestamptz;
-- Result: 2024-01-15 -04:00 (or -05:00 depending on DST)
```

### SQLite Timestamp Handling

SQLite has **no native datetime type**. Dates are stored as:
- TEXT: `"2024-01-15 10:00:00"` (ISO 8601 string)
- REAL: Julian day number
- INTEGER: Unix timestamp

**Implications**:
- No timezone enforcement at the DB level
- No automatic conversion between timezones
- `datetime()` function operates on strings, not real datetime types
- Comparison works lexicographically for TEXT, which is correct for ISO 8601 format

### MySQL Timestamp Types

| Type | Behavior |
|------|----------|
| `DATETIME` | Stores literal value; no TZ conversion |
| `TIMESTAMP` | Stored as UTC; converted using `time_zone` session variable |

**Critical behavior**: MySQL `TIMESTAMP` has a range limit of `1970-01-01 00:00:01` to `2038-01-19 03:14:07` UTC (the Year 2038 problem).

### Testing Database Timestamp Behavior

```python
def test_timestamptz_storage_and_retrieval():
    """Verify TIMESTAMPTZ stores UTC and converts on read."""
    # Insert with JST timezone
    jst = timezone(timedelta(hours=9))
    jst_time = datetime(2024, 1, 15, 19, 0, 0, tzinfo=jst)  # 10:00 UTC

    conn.execute(
        text("INSERT INTO events (name, occurred_at) VALUES (:name, :ts)"),
        {"name": "test", "ts": jst_time}
    )

    # Read back -- should be equivalent to 10:00 UTC
    result = conn.execute(text("SELECT occurred_at FROM events WHERE name = 'test'"))
    stored = result.scalar()

    # Verify the absolute time is preserved
    assert stored.astimezone(timezone.utc).hour == 10

def test_timestamp_comparison_across_timezones():
    """Verify timestamp comparisons work correctly across timezones."""
    # Insert records with different timezone offsets
    utc_time = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    jst_time = datetime(2024, 1, 15, 20, 0, 0, tzinfo=timezone(timedelta(hours=9)))
    # Both represent 12:00 UTC -- should be considered equal

    conn.execute(text("INSERT INTO events (name, occurred_at) VALUES ('utc', :ts)"), {"ts": utc_time})
    conn.execute(text("INSERT INTO events (name, occurred_at) VALUES ('jst', :ts)"), {"ts": jst_time})

    # Range query should include both
    result = conn.execute(text(
        "SELECT COUNT(*) FROM events "
        "WHERE occurred_at BETWEEN :start AND :end"
    ), {
        "start": datetime(2024, 1, 15, 11, 59, 0, tzinfo=timezone.utc),
        "end": datetime(2024, 1, 15, 12, 1, 0, tzinfo=timezone.utc),
    })
    assert result.scalar() == 2
```

## SQLite vs PostgreSQL: Key Differences

### Behavioral Differences That Cause Production Escapes

| Feature | SQLite | PostgreSQL | Production Escape |
|---------|--------|------------|-------------------|
| Type enforcement | None (type affinity) | Strict | Insert string into INTEGER column: SQLite accepts, PostgreSQL rejects |
| NULL in UNIQUE | Multiple NULLs allowed | Multiple NULLs allowed (SQL standard) | Usually OK, but check your constraints |
| Boolean | Stored as 0/1 INTEGER | Native BOOLEAN | `WHERE active = true` works in PG, needs `WHERE active = 1` in SQLite |
| JSON | `json_extract(col, '$.key')` | `col->>'key'` or `col->'key'` | JSON query syntax incompatible |
| String comparison | Case-insensitive by default | Case-sensitive | `WHERE name = 'John'` matches 'john' in SQLite, not in PostgreSQL |
| Date arithmetic | String functions | Native interval arithmetic | `date + INTERVAL '1 day'` works in PG, not SQLite |
| UPSERT syntax | `INSERT OR REPLACE` | `INSERT ... ON CONFLICT DO UPDATE` | Completely different SQL syntax |
| Concurrent writes | File-level locking | Row-level locking | Concurrent writes that work in PG may serialize or fail in SQLite |
| Subquery in UPDATE | Limited support | Full support | Complex UPDATE with subquery may fail in SQLite |

### Testing Strategy for Dialect Differences

**Option A: Dual database testing** (recommended for critical paths)
```python
@pytest.fixture(params=["sqlite", "postgresql"])
def db_engine(request):
    if request.param == "sqlite":
        return create_engine("sqlite:///test.db")
    else:
        return create_engine("postgresql://localhost/test_db")

def test_upsert(db_engine):
    """Test upsert works on all supported databases."""
    repo = UserRepository(db_engine)
    repo.upsert(User(id="user-1", name="Alice"))
    repo.upsert(User(id="user-1", name="Alice Updated"))

    user = repo.get("user-1")
    assert user.name == "Alice Updated"
```

**Option B: PostgreSQL-only integration tests** (minimum viable)
```python
@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get("DATABASE_URL", "").startswith("postgresql"),
    reason="Requires PostgreSQL"
)
def test_pg_specific_query():
    """Verify query uses correct PostgreSQL syntax."""
    # This test ONLY runs when PostgreSQL is available
    pass
```

## Locale-Sensitive Formatting

### Date Formatting Across Locales

| Format | en-US | ja-JP | de-DE |
|--------|-------|-------|-------|
| Short date | 1/15/24 | 2024/01/15 | 15.01.24 |
| Long date | January 15, 2024 | 2024年1月15日 | 15. Januar 2024 |
| Time | 10:00 AM | 10:00 | 10:00 |
| Currency | $1,234.56 | 1,234円 | 1.234,56 EUR |
| Number | 1,234.56 | 1,234.56 | 1.234,56 |

### Testing Locale-Sensitive Operations

```python
import locale

def test_number_formatting_locale_safety():
    """Verify number formatting is locale-independent for data processing."""
    # Parse a number that uses period as decimal separator
    value = parse_numeric_value("1234.56")
    assert value == 1234.56  # Must work regardless of system locale

    # This can fail on systems with de_DE locale where comma is decimal separator

def test_csv_parsing_locale_independence():
    """Verify CSV parsing is not affected by system locale."""
    csv_content = "amount\n1234.56\n7890.12"
    records = parse_csv(csv_content)

    assert records[0]["amount"] == 1234.56
    assert records[1]["amount"] == 7890.12
```

### Common Locale-Related Failures

1. **Decimal separator confusion**: `float("1.234,56")` works in some locales, fails in others
2. **Date parsing ambiguity**: `01/02/2024` -- January 2nd or February 1st?
3. **Sort order changes**: Accented characters sort differently by locale
4. **String comparison**: Case folding rules differ by locale (Turkish `i` problem)
5. **Calendar differences**: First day of week (Sunday vs Monday)
6. **Number grouping**: Thousand separator is `,` in US, `.` in Germany, ` ` in France

### Best Practices for Locale Safety

1. **Use ISO 8601 for all date/time data interchange**: `2024-01-15T10:00:00Z`
2. **Use period as decimal separator in data processing**: Format for display only at the UI layer
3. **Specify locale explicitly for formatting**: Never rely on system default locale
4. **Use Unicode-aware string operations**: `str.casefold()` instead of `str.lower()` for comparison
5. **Test with at least two locales**: Your development locale and a significantly different one (e.g., `en_US` and `ja_JP`)

## Boundary Testing Patterns

### Day Boundary Tests

```python
@pytest.mark.parametrize("tz_name,expected_date", [
    ("UTC", "2024-01-15"),
    ("Asia/Tokyo", "2024-01-16"),       # UTC+9: already next day
    ("US/Pacific", "2024-01-14"),        # UTC-8: still previous day
    ("Pacific/Auckland", "2024-01-16"),  # UTC+13: already next day
])
def test_daily_report_date_assignment(tz_name, expected_date):
    """Verify events are assigned to correct date in each timezone."""
    # Event at 2024-01-15 20:00 UTC
    event_time = datetime(2024, 1, 15, 20, 0, 0, tzinfo=timezone.utc)

    report_date = assign_report_date(event_time, tz_name)
    assert report_date.isoformat() == expected_date
```

### DST Transition Tests

```python
def test_dst_spring_forward():
    """Verify handling of the 'lost hour' during spring DST transition."""
    # In US Eastern: 2024-03-10 02:00 becomes 03:00 (2:30 AM does not exist)
    # Application should handle this gracefully
    result = schedule_event("2024-03-10T02:30:00", timezone="US/Eastern")
    # Should either adjust to 03:30 or raise a clear error, not crash

def test_dst_fall_back():
    """Verify handling of the 'repeated hour' during fall DST transition."""
    # In US Eastern: 2024-11-03 01:00-01:59 occurs twice
    # Application must disambiguate
    result = schedule_event("2024-11-03T01:30:00", timezone="US/Eastern")
    # Should use fold parameter or explicit UTC conversion
```

### Month/Year Boundary Tests

```python
@pytest.mark.parametrize("test_time,expected_month", [
    # Last second of month in UTC, but already next month in JST
    ("2024-01-31T23:59:59+00:00", {"UTC": 1, "JST": 2}),
    # Last day of February (leap year)
    ("2024-02-29T15:00:00+00:00", {"UTC": 2, "JST": 3}),
    # Year boundary
    ("2024-12-31T23:00:00+00:00", {"UTC": 12, "JST": 1}),
])
def test_monthly_aggregation_boundary(test_time, expected_month):
    """Verify monthly aggregation handles timezone-aware boundaries."""
    event = parse_datetime(test_time)

    for tz_name, expected in expected_month.items():
        month = get_aggregation_month(event, tz_name)
        assert month == expected, f"Wrong month for {tz_name}: expected {expected}, got {month}"
```

## Summary: Key Testing Requirements

| Category | Minimum Test Coverage |
|----------|--------------------|
| Aware/naive mixing | At least one test comparing aware and naive datetimes |
| DB timestamp round-trip | Write aware datetime, read back, verify TZ preserved |
| Cross-timezone ordering | Records from 3+ timezones sort correctly |
| Day boundary | Event near midnight assigned to correct date per timezone |
| DST transition | Spring forward and fall back handled gracefully |
| Locale number parsing | Decimal separator consistent regardless of system locale |
| Date format parsing | ISO 8601 used for data interchange, locale-specific only for display |
| DB dialect datetime functions | Date arithmetic uses correct syntax for target database |
