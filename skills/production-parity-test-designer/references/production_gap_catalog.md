# Production Gap Catalog

A comprehensive taxonomy of differences between development/CI environments and production that cause "tests pass, production fails" scenarios. Use this catalog as a checklist during Step 1 (Production Gap Inventory) to ensure no category is overlooked.

## Category 1: Database Dialect Gaps

The most common source of production escapes. Tests run against a lightweight DB (SQLite, H2) while production uses a full-featured DB (PostgreSQL, MySQL, Oracle).

### SQL Syntax Differences

| Feature | SQLite | PostgreSQL | MySQL |
|---------|--------|------------|-------|
| `UPSERT` | `INSERT OR REPLACE` | `INSERT ... ON CONFLICT DO UPDATE` | `INSERT ... ON DUPLICATE KEY UPDATE` |
| `BOOLEAN` | Stored as INTEGER (0/1) | Native BOOLEAN | TINYINT(1) |
| `AUTO_INCREMENT` | `AUTOINCREMENT` on INTEGER PRIMARY KEY | `SERIAL` or `GENERATED ALWAYS` | `AUTO_INCREMENT` |
| `LIMIT` with offset | `LIMIT N OFFSET M` | `LIMIT N OFFSET M` | `LIMIT M, N` (reversed order!) |
| `GROUP BY` strictness | Lenient (allows non-aggregated columns) | Strict (requires all non-aggregated in GROUP BY) | Depends on `sql_mode` |
| `LIKE` case sensitivity | Case-insensitive by default | Case-sensitive (use `ILIKE`) | Depends on collation |
| JSON operations | `json_extract()` | `->`, `->>`, `jsonb` operators | `JSON_EXTRACT()`, `->` |
| String concatenation | `||` | `||` | `CONCAT()` |
| Date functions | `date()`, `strftime()` | `DATE_TRUNC()`, `EXTRACT()` | `DATE_FORMAT()`, `EXTRACT()` |

### Schema and Constraint Differences

- **Foreign key enforcement**: SQLite does not enforce foreign keys by default (`PRAGMA foreign_keys = ON` required)
- **Type coercion**: SQLite has "type affinity" -- it stores any value in any column. PostgreSQL strictly enforces types
- **NULL handling in UNIQUE constraints**: SQLite allows multiple NULLs in UNIQUE columns; some DBs allow only one
- **Column length enforcement**: SQLite ignores `VARCHAR(255)` length limits; PostgreSQL enforces them
- **Default values**: Computed defaults (`DEFAULT NOW()`) behave differently across engines
- **Transaction isolation**: Default isolation levels differ (PostgreSQL: Read Committed, MySQL: Repeatable Read)

### Migration and Schema Drift

- **Migration tool behavior**: Alembic, Flyway, Liquibase generate dialect-specific SQL
- **Schema comparison**: Use `pg_dump --schema-only` vs actual production schema to detect drift
- **Index types**: B-tree is universal, but GIN/GiST (PostgreSQL), FULLTEXT (MySQL) are dialect-specific

### How to Test

- Run core queries against real PostgreSQL in CI (service container)
- Test at least: INSERT, UPDATE/UPSERT, SELECT with JOIN, aggregation with GROUP BY
- Verify constraint violations raise expected exceptions

## Category 2: Dependency Installation Gaps

Differences in how dependencies are installed and available at runtime.

### Native Extension Failures

- Python: `psycopg2` requires `libpq-dev`, `Pillow` requires `libjpeg`, `cryptography` requires `openssl`
- Node.js: `sharp` requires `vips`, `canvas` requires `cairo`, `bcrypt` requires build tools
- Ruby: `nokogiri` requires `libxml2`, `pg` requires `libpq`

### Version Resolution Gaps

- **Lockfile vs transitive**: Lockfile pins direct dependencies but transitive dependencies may resolve differently across platforms
- **Platform-specific wheels**: Python wheels for macOS vs Linux may have different behavior
- **Node.js optional dependencies**: `optionalDependencies` install on one platform, skip on another

### Missing Runtime Dependencies

- Development environment has globally-installed tools (ImageMagick, ffmpeg, wkhtmltopdf) that are not in the production container
- Development `PATH` includes tools that production `PATH` does not
- Homebrew-installed libraries on macOS not available in Linux production

### How to Test

- Run `import <module>` for every production dependency in a clean environment
- Verify native extensions load (not just the Python wrapper)
- Test in a container matching the production base image

## Category 3: Environment Variable Gaps

Differences in configuration between environments that cause silent behavior changes.

### Missing Variables

- **Feature flags**: `FEATURE_X_ENABLED=true` in dev, missing in production (defaults to `false`)
- **API endpoints**: `API_BASE_URL` pointing to dev instance, not production
- **Secrets**: `DATABASE_URL`, `API_KEY`, `JWT_SECRET` missing or different

### Value Differences

- **Log level**: `LOG_LEVEL=DEBUG` in dev, `LOG_LEVEL=WARNING` in production (hiding important errors)
- **Concurrency settings**: `WORKERS=1` in dev, `WORKERS=8` in production (race conditions only appear in production)
- **Timeout values**: Generous timeouts in dev, strict in production
- **File paths**: `/tmp/uploads/` in dev, `/mnt/shared/uploads/` in production

### How to Test

- Maintain a `.env.example` with all required variables
- Validate all required env vars are present at startup (fail fast, not fail silent)
- Test with production-equivalent values in CI (not production secrets, but same structure)

## Category 4: Timezone and Locale Gaps

Datetime and locale differences that cause data corruption or logic errors.

### Timezone Gaps

- **Developer machine**: Local timezone (JST, EST, PST)
- **CI server**: Usually UTC
- **Production server**: Usually UTC
- **Database server**: May have its own timezone setting
- **Application code**: May use `datetime.now()` (local) vs `datetime.utcnow()` vs `datetime.now(tz=UTC)`

### Aware vs Naive Mixing

The most dangerous timezone gap. When code mixes timezone-aware and timezone-naive datetime objects:

```python
# This WILL raise TypeError in Python
aware = datetime.now(timezone.utc)      # 2024-01-15 10:00:00+00:00
naive = datetime.now()                   # 2024-01-15 19:00:00 (no tzinfo)
result = aware - naive                   # TypeError: can't subtract offset-naive and offset-aware
```

This may work in development (where all datetimes are naive) but fail in production (where some come from the DB as aware).

### Locale Gaps

- **Date formatting**: `1/2/2024` -- January 2nd or February 1st?
- **Number formatting**: `1,234.56` vs `1.234,56`
- **Currency symbols**: `$`, `EUR`, `JPY` formatting differences
- **Sort order**: Locale-sensitive string sorting produces different results
- **Character encoding**: UTF-8 vs Latin-1 in file I/O and DB connections

### How to Test

See `references/timezone_dialect_boundary_guide.md` for detailed testing patterns.

## Category 5: OS and Filesystem Gaps

Differences between development and production operating systems.

### Path and Filesystem

- **Path separator**: `\` (Windows) vs `/` (Unix) -- use `pathlib.Path` not string concatenation
- **Case sensitivity**: macOS filesystem is case-insensitive by default; Linux is case-sensitive
- **Maximum path length**: Windows 260 chars, Linux 4096 chars, but NFS may have lower limits
- **Symlink handling**: Different behavior across OS and container runtimes
- **Temporary directory**: `/tmp` location, cleanup policy, available space

### Line Endings

- **Git config**: `autocrlf` setting can change line endings between platforms
- **File comparison**: `\r\n` vs `\n` causes diff failures and checksum mismatches
- **Shell scripts**: `\r\n` line endings cause `#!/bin/bash\r: No such file or directory`

### Process and Permissions

- **File permissions**: `chmod` behavior differs between macOS and Linux
- **User IDs**: Container runs as root or specific UID, different from dev machine
- **Process limits**: `ulimit` settings (open files, memory) differ between dev and production
- **Signal handling**: `SIGTERM` cleanup behavior may differ

### How to Test

- Run tests in a Linux container matching production OS
- Include tests with paths containing special characters, long names, and deep nesting
- Verify file operations use `pathlib.Path` not manual string concatenation

## Category 6: Mock vs Real Dependency Gaps

Differences caused by mocking external dependencies instead of using real ones.

### What Mocks Hide

| Real Behavior | What Mock Misses |
|---------------|-----------------|
| Network latency | Timeout handling, retry logic |
| Connection failures | Circuit breaker activation |
| Rate limiting | Backoff implementation |
| Large response payloads | Memory usage, streaming |
| Authentication expiry | Token refresh logic |
| Partial failures | Error recovery, compensating transactions |
| Schema changes | Response parsing failures |

### Acceptable vs Unacceptable Mocks

**Acceptable mocks** (external, uncontrollable):
- Third-party payment processors (Stripe, PayPal)
- External notification services (Twilio, SendGrid)
- Rate-limited APIs (Google Maps, OpenAI)
- External auth providers (OAuth, SAML) -- but use contract tests

**Unacceptable mocks** (internal, controllable):
- Your own database
- Your own cache (Redis, Memcached)
- Your own message queue (RabbitMQ, Kafka)
- Your own file storage
- Your own microservices (use contract tests instead)

### How to Test

- Replace mock-only tests with integration tests against real services
- For acceptable mocks, add contract tests that verify mock behavior matches real API
- Maintain a "mock registry" documenting all mocks, their justification, and last verification date

## Category 7: Serialization and Parsing Gaps

Differences in data encoding, serialization, and parsing between environments.

### JSON/YAML Parsing

- **Floating point precision**: `0.1 + 0.2 = 0.30000000000000004` in JSON serialization
- **Date serialization**: `datetime` -> JSON varies by serializer (ISO 8601, Unix timestamp, custom format)
- **Null handling**: JSON `null` vs YAML `null`/`~`/empty vs Python `None` vs DB `NULL`
- **Unicode handling**: Emoji, CJK characters, RTL text in JSON strings
- **Key ordering**: JSON objects are unordered; serialization order varies by library

### Binary and Encoding

- **Character encoding**: UTF-8 vs Shift-JIS vs Latin-1 in file reads
- **BOM (Byte Order Mark)**: CSV files from Excel may have BOM prefix
- **Binary file handling**: `open(file, 'r')` vs `open(file, 'rb')` causes `UnicodeDecodeError`
- **Base64 encoding**: Standard vs URL-safe alphabet, padding differences

### Protocol and Format

- **HTTP content type**: Missing `Content-Type: application/json` causes parsing failure
- **gzip compression**: Response decompression handled differently by HTTP clients
- **Multipart form data**: File upload encoding varies by client library

### How to Test

- Test serialization round-trips (serialize -> deserialize -> compare)
- Include edge cases: empty strings, null values, Unicode, very large numbers
- Verify encoding headers in HTTP responses and file operations

## Gap Discovery Checklist

Use this checklist during Step 1 to ensure comprehensive coverage:

- [ ] **Database**: Same engine and version as production?
- [ ] **Dependencies**: All native extensions available?
- [ ] **Environment variables**: All required vars documented and validated?
- [ ] **Timezone**: Server TZ, DB TZ, and app TZ all match production?
- [ ] **OS**: Same OS family and version?
- [ ] **Filesystem**: Case sensitivity, path length, permissions match?
- [ ] **Mocks**: All mocked dependencies documented with justification?
- [ ] **Serialization**: JSON/YAML/binary encoding matches production?
- [ ] **Networking**: DNS, proxy, TLS certificate handling matches?
- [ ] **Concurrency**: Worker count, thread pool size matches production?
- [ ] **Caching**: Cache layer (Redis, Memcached) present in test environment?
- [ ] **Logging**: Log output format and destination match?
