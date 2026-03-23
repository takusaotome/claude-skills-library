# Runtime Boundary Checklist

## Purpose

Implicit contracts are most likely to break at runtime boundaries -- the points where data crosses from one system, format, or execution context to another. This checklist provides systematic verification items for each major boundary type. Use during Workflow 6 (Verification Design) to ensure contract tests cover the most failure-prone integration points.

---

## Boundary 1: Database Boundary

Data contracts frequently shift when values pass between application code and database storage. Types coerce, precision changes, and default behaviors differ between database engines.

### Type Coercion Checks

- [ ] **Integer precision**: Does the application use `int` but the DB column is `BIGINT`? Or vice versa (overflow risk)?
- [ ] **Decimal precision**: Application `float` vs. DB `DECIMAL(10,2)` -- is precision lost on round-trip?
- [ ] **String truncation**: Application allows arbitrary-length strings but DB column has `VARCHAR(255)` limit
- [ ] **Boolean representation**: DB stores `0/1` but application expects `True/False` -- does the ORM handle conversion correctly?
- [ ] **Null semantics**: Application uses empty string `""` but DB stores `NULL` -- are they treated equivalently?
- [ ] **UUID format**: Application uses UUID object but DB stores as `VARCHAR(36)` or `BINARY(16)` -- format preserved?

### Dialect-Specific Checks

- [ ] **Auto-increment behavior**: SQLite auto-increment vs. PostgreSQL `SERIAL` vs. MySQL `AUTO_INCREMENT` -- gap behavior differs
- [ ] **Case sensitivity**: PostgreSQL identifiers are case-folded; MySQL depends on `lower_case_table_names` setting
- [ ] **Date/time storage**: SQLite stores datetimes as strings; PostgreSQL has native `TIMESTAMP` types with timezone awareness
- [ ] **JSON handling**: PostgreSQL `JSONB` vs. SQLite JSON text -- query and indexing behavior differs
- [ ] **Transaction isolation**: Default isolation levels differ between engines (READ COMMITTED in PostgreSQL, SERIALIZABLE in SQLite)
- [ ] **Constraint enforcement**: SQLite does not enforce `CHECK` constraints by default; foreign key enforcement requires `PRAGMA foreign_keys = ON`
- [ ] **Empty string vs. NULL**: Oracle treats empty string as NULL; PostgreSQL does not

### ORM-Specific Checks

- [ ] **Lazy loading**: Does accessing a relationship trigger a new query? (N+1 hidden contract)
- [ ] **Dirty tracking**: Does the ORM detect in-place mutations on JSON fields?
- [ ] **Flush timing**: When does the ORM actually write to DB? (implicit flush on query)
- [ ] **Cascade behavior**: Does deleting a parent cascade to children? Configured at ORM or DB level?
- [ ] **Default values**: Are defaults applied by the ORM or the DB? (behavior differs for computed defaults)

### Contract Test Patterns for DB Boundary

```
Test: Round-trip type preservation
  Given: Save a value with specific type to DB
  When: Read it back
  Then: Type and value are identical (no silent coercion)

Test: Null vs. empty string distinction
  Given: Save NULL and "" to the same column
  When: Read both back
  Then: They remain distinguishable (or document that they merge)

Test: Precision preservation
  Given: Save a high-precision decimal (e.g., 0.10000000000000001)
  When: Read it back
  Then: Value matches within acceptable tolerance (document the tolerance)
```

---

## Boundary 2: Serialization Boundary

When data is serialized (JSON, pickle, protobuf, XML, CSV) and deserialized, type information and structural contracts can shift.

### JSON Serialization Checks

- [ ] **Datetime handling**: Python `datetime` is not JSON-serializable by default -- how is it converted? ISO format? Unix timestamp?
- [ ] **Decimal handling**: `Decimal("1.10")` becomes `1.1` in JSON (trailing zero lost) -- does precision matter?
- [ ] **Set/tuple handling**: JSON has no set or tuple type -- these become arrays, losing distinctiveness
- [ ] **None vs. missing key**: JSON `null` vs. absent key -- does the deserializer distinguish them?
- [ ] **Integer overflow**: JSON integers have no size limit, but deserializers may cap at 32/64-bit
- [ ] **Key ordering**: JSON objects are unordered by spec, but some consumers depend on key order
- [ ] **Binary data**: How is `bytes` encoded? Base64? Hex? Raw string escape?
- [ ] **NaN/Infinity**: Not valid JSON values -- how are they handled?

### Pickle/Binary Serialization Checks

- [ ] **Class versioning**: Pickled objects fail to deserialize if the class definition changes
- [ ] **Cross-version compatibility**: Python 2 pickle vs. Python 3 -- protocol version matters
- [ ] **Security**: Unpickling arbitrary data executes code (supply chain risk)
- [ ] **Module path dependency**: Pickle stores the full module path -- refactoring breaks deserialization

### CSV/TSV Serialization Checks

- [ ] **Encoding**: UTF-8 with or without BOM? Shift-JIS? Latin-1?
- [ ] **Quoting rules**: Does the serializer properly escape commas, newlines, and quotes within fields?
- [ ] **Numeric strings**: "001234" as ID vs. 1234 as number -- does the deserializer preserve leading zeros?
- [ ] **Empty fields**: Is empty field parsed as empty string, None, or NaN?
- [ ] **Date format ambiguity**: "01/02/2025" -- January 2nd or February 1st?

### Contract Test Patterns for Serialization Boundary

```
Test: Round-trip preservation
  Given: An object with diverse field types
  When: Serialize then deserialize
  Then: All field types and values are preserved (or document known losses)

Test: Edge value handling
  Given: Values like NaN, Infinity, empty string, very long string, Unicode
  When: Serialize then deserialize
  Then: Values survive or raise explicit errors (not silent corruption)

Test: Backward compatibility
  Given: Serialized data from version N
  When: Deserialize with version N+1 code
  Then: No data loss or crash (or explicit migration path documented)
```

---

## Boundary 3: Timezone Boundary

Timezone handling is one of the most failure-prone boundaries because errors are often silent, intermittent, and environment-dependent.

### Aware vs. Naive Datetime Checks

- [ ] **Mixing aware and naive**: Does the code compare timezone-aware and timezone-naive datetimes? (raises TypeError in Python)
- [ ] **Default timezone assumption**: When a naive datetime is created, what timezone is assumed? Server local? UTC?
- [ ] **Database timezone**: Is the DB configured for UTC? Does the ORM add timezone info on read?
- [ ] **API response timezone**: Do API responses include timezone info? If not, what is assumed?
- [ ] **User input timezone**: When users enter dates, in what timezone are they interpreted?

### DST (Daylight Saving Time) Checks

- [ ] **DST transition**: Does a daily job that runs at "2:30 AM" handle the spring-forward gap (2:30 AM doesn't exist)?
- [ ] **Duration calculation**: Is the duration between two timestamps calculated correctly across DST changes?
- [ ] **Recurring events**: Weekly meetings at "3 PM ET" -- does the UTC equivalent shift with DST?
- [ ] **Historical queries**: Are past dates stored with the timezone that was in effect at the time?

### Cross-Timezone Checks

- [ ] **Server timezone vs. user timezone**: Are displayed times converted to the user's timezone?
- [ ] **Date boundary differences**: "Today" in JST might be "yesterday" in UTC -- do date-filtered queries account for this?
- [ ] **Midnight ambiguity**: "End of day" is midnight of the next day in some systems, 23:59:59 in others
- [ ] **Calendar date vs. instant**: Does the system distinguish "March 15" (a date) from "March 15 00:00:00 UTC" (an instant)?

### Contract Test Patterns for Timezone Boundary

```
Test: Naive datetime rejection
  Given: Code path that requires timezone-aware datetime
  When: Pass a naive datetime
  Then: Explicit error, not silent assumption

Test: DST transition handling
  Given: A timestamp just before and after DST transition
  When: Calculate duration between them
  Then: Duration accounts for the clock change (23 or 25 hours, not 24)

Test: Cross-timezone date filtering
  Given: A record created at 2025-03-15 01:00 UTC
  When: Query for records on "March 15" in JST (UTC+9)
  Then: Record is included (it's March 15 10:00 in JST)
```

---

## Boundary 4: Retry and Exception Boundary

Retry logic and exception handling create hidden contracts about failure modes, idempotency, and partial completion.

### Retry Behavior Checks

- [ ] **Retry count**: How many times does the function retry? Is this configurable or hard-coded?
- [ ] **Retry delay**: Linear, exponential, or fixed? Is there jitter?
- [ ] **Idempotency**: Is the retried operation safe to repeat? (POST vs. PUT, insert vs. upsert)
- [ ] **Partial completion**: If the first attempt partially succeeds, does the retry cause duplicates?
- [ ] **Timeout interaction**: Does the total retry time exceed the caller's timeout? (retry succeeds but caller already gave up)
- [ ] **Circuit breaker**: Is there a mechanism to stop retrying when the downstream is unhealthy?

### Exception Propagation Checks

- [ ] **Exception wrapping**: Does the function wrap low-level exceptions in domain exceptions? Or do raw DB/HTTP errors leak?
- [ ] **Exception information loss**: Does catching and re-raising preserve the original stack trace?
- [ ] **Catch-all blocks**: Are there bare `except:` or `except Exception:` blocks that hide specific errors?
- [ ] **Finally block side effects**: Does the `finally` block perform operations that could fail independently?
- [ ] **Error state cleanup**: If the function fails mid-operation, is partial state cleaned up?

### Timeout Checks

- [ ] **Connection timeout vs. read timeout**: Are both configured? What are the defaults?
- [ ] **Cascading timeouts**: Does function A call function B with a 30s timeout, but A's own caller has a 10s timeout?
- [ ] **Timeout behavior**: Does timeout raise an exception or return None?
- [ ] **Resource cleanup on timeout**: Are connections/files/locks released when a timeout occurs?

### Contract Test Patterns for Retry/Exception Boundary

```
Test: Retry idempotency
  Given: An operation that succeeds on the second attempt
  When: Retry mechanism activates
  Then: No duplicate side effects (records, messages, charges)

Test: Exception type preservation
  Given: A downstream service returns a 404
  When: The function catches and re-raises
  Then: Caller receives a specific NotFoundError, not a generic Exception

Test: Timeout resource cleanup
  Given: An operation that times out mid-execution
  When: Timeout fires
  Then: All resources (connections, file handles, locks) are released
```

---

## Boundary 5: Locale and Formatting Boundary

Locale-dependent behavior creates silent contracts that work perfectly in one locale but fail in another.

### Number Formatting Checks

- [ ] **Decimal separator**: Is it `.` (English) or `,` (European)? Does the code hardcode one?
- [ ] **Thousands separator**: Is it `,` (English) or `.` (European) or ` ` (French)?
- [ ] **Currency format**: `$1,234.56` vs. `1.234,56 EUR` vs. `JPY 1,234` -- how is this determined?
- [ ] **Negative number format**: `-100` vs. `(100)` vs. `100-` -- which convention is used?
- [ ] **Number parsing**: `"1,234"` -- is the comma a thousands separator or a decimal separator?

### String Collation Checks

- [ ] **Sort order**: Does sorting depend on locale? (e.g., `a < b` is locale-dependent for accented characters)
- [ ] **Case conversion**: Turkish locale has dotless i (`I` lowercases to `i` in English but `\u0131` in Turkish)
- [ ] **String length**: Multi-byte characters -- does `len()` count bytes or characters?
- [ ] **Normalization**: Unicode NFC vs. NFD -- `e + combining accent` vs. precomposed `e-acute`

### Date/Time Formatting Checks

- [ ] **Date format**: `MM/DD/YYYY` (US) vs. `DD/MM/YYYY` (EU) vs. `YYYY-MM-DD` (ISO)
- [ ] **Week start**: Sunday (US) vs. Monday (ISO 8601) -- affects week number calculations
- [ ] **Calendar system**: Gregorian vs. Japanese era vs. Islamic -- does the system support multiple?
- [ ] **12h vs. 24h**: Is the time format consistent across the system?

### Contract Test Patterns for Locale/Formatting Boundary

```
Test: Locale-independent parsing
  Given: A numeric string "1,234.56"
  When: Parse it in both English and German locales
  Then: Both produce the same numeric value (or fail explicitly in one)

Test: Unicode round-trip
  Given: A string with accented characters, CJK, and emoji
  When: Process through the function and compare
  Then: All characters preserved without corruption

Test: Date format consistency
  Given: A date string "01/02/2025"
  When: Parse it
  Then: The function uses an explicit, documented format (not locale-dependent parsing)
```

---

## Boundary Priority Matrix

When time is limited, prioritize boundary testing based on the following risk assessment:

| Boundary | Failure Visibility | Fix Difficulty | Data Loss Risk | Priority |
|----------|-------------------|---------------|---------------|----------|
| Timezone | Low (silent) | High | Medium | Highest |
| DB Dialect | Medium | High | High | High |
| Serialization | Medium | Medium | High | High |
| Retry/Exception | Low (masked) | Medium | Low | Medium |
| Locale/Formatting | Medium | Low | Low | Medium |

Timezone and DB dialect boundaries should always be investigated first because they produce silent failures that are difficult to diagnose and expensive to fix after deployment.
