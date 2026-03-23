# Boundary Hardening Guide

This reference provides hardening techniques for each architectural boundary in an application. Boundaries are the points where different trust levels, data formats, or execution contexts meet. Hardening means ensuring that data crossing a boundary is validated, normalized, and constrained before it enters the next zone.

**Core Principle**: Never trust data arriving from outside the current boundary. Validate at entry, normalize for internal use, sanitize at exit.

---

## 1. Controller / Request Boundary

The controller boundary is where external user input enters the application. This is the primary attack surface and the most critical boundary to harden.

### Hardening Techniques

**Input Validation**:
- Validate all input fields against a schema before any business logic executes
- Use allowlists (not denylists) for acceptable values, formats, and ranges
- Reject requests that contain unexpected fields (strict schema parsing)
- Apply size limits to all input fields (string length, array size, file size, numeric range)

**Type Coercion and Normalization**:
- Convert string inputs to strongly-typed values at the boundary (parse integers, dates, enums)
- Normalize string inputs: trim whitespace, normalize Unicode (NFC), lowercase emails
- Reject values that do not parse cleanly rather than attempting fuzzy interpretation

**Request Rate and Size Limiting**:
- Apply rate limiting per client/IP at the reverse proxy or middleware layer
- Set maximum request body size at the web server level
- Limit query parameter count and depth (prevent parameter pollution)

**Authentication Verification**:
- Verify authentication token/session validity before any handler executes
- Extract and validate the authenticated identity (user ID, roles, tenant) into a typed context object
- Reject expired, malformed, or unsigned tokens immediately

### Hardened Controller Pattern

```python
# Every controller method follows this pattern:
# 1. Authenticate (middleware)
# 2. Authorize (middleware or decorator)
# 3. Validate input (schema)
# 4. Call service layer (business logic)
# 5. Return serialized response

@require_permission("orders.create")
def create_order(request):
    # Validated and typed input
    validated = CreateOrderSchema.parse(request.body)
    # Service layer handles business logic
    result = order_service.create(
        user=request.auth_context.user,
        items=validated.items,
        shipping=validated.shipping_address
    )
    return OrderResponse.from_domain(result)
```

---

## 2. API Boundary (Service-to-Service)

The API boundary exists between internal services, between your application and third-party APIs, and between your application and client SDKs.

### Hardening Techniques

**Contract Enforcement**:
- Define explicit API contracts (OpenAPI, gRPC proto, GraphQL schema) and validate both requests and responses against them
- Version all APIs; never make breaking changes to existing versions
- Use consumer-driven contract testing to verify compatibility

**Response Validation**:
- Validate responses from external APIs before using them (do not trust third-party data)
- Apply the same input validation rules to API responses as to user input
- Handle unexpected response shapes gracefully (missing fields, extra fields, wrong types)

**Timeout and Circuit Breaking**:
- Set explicit timeouts on all outbound HTTP calls (connect timeout + read timeout)
- Implement circuit breakers that open after a threshold of failures, preventing cascade
- Configure retry policies with exponential backoff and jitter
- Set maximum retry counts to prevent infinite loops

**Authentication and Authorization**:
- Use service-to-service authentication (mTLS, API keys with rotation, OAuth2 client credentials)
- Apply least-privilege: each service account should only have permissions for the APIs it needs
- Log all inter-service calls with correlation IDs for traceability

### Hardened API Client Pattern

```python
class OrderApiClient:
    def __init__(self, base_url: str, credentials: ServiceCredentials, timeout: float = 5.0):
        self.session = create_session(
            base_url=base_url,
            auth=credentials.to_auth_header(),
            timeout=timeout,
            retry_policy=RetryPolicy(max_retries=3, backoff_factor=0.5),
            circuit_breaker=CircuitBreaker(failure_threshold=5, recovery_timeout=30)
        )

    def get_order(self, order_id: str) -> Order:
        response = self.session.get(f"/orders/{order_id}")
        response.raise_for_status()
        validated = OrderResponseSchema.parse(response.json())
        return Order.from_api_response(validated)
```

---

## 3. Database Boundary

The database boundary is where application logic meets the persistence layer. Hardening here prevents SQL injection, data corruption, and inconsistent state.

### Hardening Techniques

**Query Construction Safety**:
- All queries must use parameterized statements or ORM query builders
- Dynamic identifiers (column names, table names) must come from a hardcoded allowlist
- Ban string concatenation in any context that produces SQL

**Transaction Management**:
- Use explicit transaction boundaries (not auto-commit for write operations)
- Implement optimistic concurrency control (version columns) for concurrent updates
- Ensure that all operations within a transaction either fully commit or fully roll back
- Use savepoints for partial rollback within complex transactions

**Schema Constraints**:
- Enforce data integrity at the database level (NOT NULL, UNIQUE, FOREIGN KEY, CHECK)
- Use ENUM types or CHECK constraints for status/type fields
- Set appropriate column sizes and precision (do not use VARCHAR(MAX) by default)
- Create indexes for foreign keys and frequently queried columns

**Connection Management**:
- Use connection pooling with configured limits (min, max, idle timeout)
- Set statement timeout to prevent runaway queries from consuming resources
- Monitor connection usage and alert on pool exhaustion
- Use read replicas for read-heavy queries to reduce primary load

### Hardened Repository Pattern

```python
class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_by_email(self, email: str) -> Optional[User]:
        """All queries go through parameterized methods only."""
        row = self.db.query_one(
            "SELECT id, name, email FROM users WHERE email = %s",
            [email]
        )
        return User.from_row(row) if row else None

    def update_name(self, user_id: int, new_name: str, expected_version: int) -> User:
        """Optimistic concurrency with version check."""
        with self.db.transaction() as tx:
            updated = tx.execute(
                "UPDATE users SET name = %s, version = version + 1 "
                "WHERE id = %s AND version = %s RETURNING *",
                [new_name, user_id, expected_version]
            )
            if not updated:
                raise ConcurrencyConflictError(f"User {user_id} was modified concurrently")
            return User.from_row(updated)
```

---

## 4. File System Boundary

The file system boundary is where application logic interacts with files, directories, and storage systems.

### Hardening Techniques

**Path Validation**:
- Resolve all paths to their canonical form (resolve symlinks, normalize `.` and `..`)
- Verify that the resolved path is within the allowed base directory
- Reject paths containing null bytes, which can truncate strings in some languages/OS combinations
- Use a dedicated storage service that encapsulates all path validation

**File Content Validation**:
- Validate file content type by inspecting magic bytes, not by trusting the file extension or MIME type header
- Enforce maximum file sizes at multiple layers (web server, application, storage)
- Scan uploaded files for malware before storing
- Strip or sanitize metadata from uploaded files (EXIF data, embedded scripts)

**Atomic File Operations**:
- Write to a temporary file first, then atomically rename to the target path
- Use advisory or mandatory file locking for concurrent access scenarios
- Create backup/snapshot before destructive operations (overwrite, delete)
- Ensure cleanup of temporary files in all code paths (including error paths)

**Permission Management**:
- Create files with the minimum necessary permissions (no world-readable/writable by default)
- Run the application process with a dedicated service account (not root)
- Use OS-level directory permissions to enforce isolation between tenants or modules

### Hardened File Service Pattern

```python
class FileService:
    def __init__(self, base_dir: Path, allowed_types: set, max_size: int):
        self.base_dir = base_dir.resolve()
        self.allowed_types = allowed_types
        self.max_size = max_size

    def resolve_safe_path(self, relative_path: str) -> Path:
        """Resolve path and verify it's within base directory."""
        candidate = (self.base_dir / relative_path).resolve()
        if not candidate.is_relative_to(self.base_dir):
            raise SecurityError(f"Path traversal detected: {relative_path}")
        return candidate

    def save_upload(self, filename: str, content: bytes) -> Path:
        """Save uploaded file with validation."""
        if len(content) > self.max_size:
            raise ValidationError(f"File exceeds maximum size: {self.max_size}")
        detected_type = magic.from_buffer(content, mime=True)
        if detected_type not in self.allowed_types:
            raise ValidationError(f"File type not allowed: {detected_type}")
        safe_name = self._sanitize_filename(filename)
        target = self.resolve_safe_path(safe_name)
        # Atomic write: temp file then rename
        temp_path = target.with_suffix(".tmp")
        temp_path.write_bytes(content)
        temp_path.rename(target)
        return target
```

---

## 5. Time Boundary

The time boundary exists wherever datetime values are created, stored, transmitted, compared, or displayed. This boundary is especially dangerous because failures are often silent and intermittent (appearing only during DST transitions or across timezones).

### Hardening Techniques

**Creation**:
- Always create timezone-aware datetime objects
- Use a `Clock` abstraction to centralize time creation (enables testing)
- Ban `datetime.now()` and `datetime.utcnow()` in application code

**Storage**:
- Use `TIMESTAMP WITH TIME ZONE` database column type
- Store all timestamps in UTC
- Serialize with ISO 8601 format including timezone offset

**Transmission**:
- Include timezone offset in all datetime fields in API responses
- Document the timezone of each datetime field in API documentation
- Reject datetime inputs that lack timezone information

**Comparison**:
- Never compare naive and aware datetimes (this is a runtime error in many languages)
- Normalize both sides to UTC before comparison
- For date-only comparisons, be explicit about which timezone defines "today"

**Display**:
- Convert to user's local timezone only at the display boundary (templates, client-side)
- Never store the display-formatted version; always derive it from the UTC value
- Test display logic around DST transition dates (spring forward, fall back)

### Hardened Clock Pattern

```python
from datetime import datetime, timezone
from typing import Protocol

class Clock(Protocol):
    def now(self) -> datetime: ...

class SystemClock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)

class FixedClock:
    """For testing."""
    def __init__(self, fixed_time: datetime):
        assert fixed_time.tzinfo is not None, "Clock must be timezone-aware"
        self.fixed_time = fixed_time

    def now(self) -> datetime:
        return self.fixed_time
```

---

## 6. Environment Boundary

The environment boundary separates configuration, secrets, and infrastructure details from application code. Hardening here ensures that the application behaves consistently across development, staging, and production environments.

### Hardening Techniques

**Configuration Management**:
- Load all configuration from environment variables or configuration services (never hardcoded)
- Validate all configuration values at application startup (fail fast on missing or invalid config)
- Use typed configuration objects, not raw string access scattered through the code
- Provide sensible defaults for non-sensitive settings; require explicit values for sensitive ones

**Secret Management**:
- Never commit secrets to version control (use `.gitignore`, pre-commit hooks, secret scanning)
- Use a secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager) in production
- Rotate secrets on a defined schedule; design the application to handle rotation gracefully
- Log secret access for audit purposes (but never log the secret value itself)

**Environment Parity**:
- Use the same database engine in all environments (not SQLite in dev and PostgreSQL in prod)
- Use containerization to minimize environment differences
- Run integration tests against production-like infrastructure
- Document all environment-specific behaviors and configuration differences

**Feature Flags**:
- Use feature flags for gradual rollout instead of environment-specific code branches
- Centralize feature flag evaluation in a single service
- Default all flags to the safe/off state; require explicit enablement
- Remove flag evaluation code after full rollout (flag debt is technical debt)

### Hardened Configuration Pattern

```python
from pydantic import BaseSettings, Field, validator

class AppConfig(BaseSettings):
    database_url: str = Field(..., description="PostgreSQL connection string")
    redis_url: str = Field(default="redis://localhost:6379", description="Redis connection string")
    max_upload_size: int = Field(default=10_485_760, description="Max upload size in bytes")
    log_level: str = Field(default="INFO", description="Logging level")

    @validator("database_url")
    def validate_database_url(cls, v):
        if not v.startswith("postgresql://"):
            raise ValueError("Only PostgreSQL is supported")
        return v

    @validator("log_level")
    def validate_log_level(cls, v):
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v.upper()

    class Config:
        env_prefix = "APP_"

# Fail fast at startup
config = AppConfig()  # Raises ValidationError if required config is missing
```

---

## Boundary Interaction Checklist

When data crosses multiple boundaries, each transition must be hardened independently. Use this checklist to verify that all transitions are covered:

| From | To | Key Checks |
|------|----|------------|
| User Input | Controller | Schema validation, type coercion, size limits |
| Controller | Service Layer | Authorization verified, input typed, context attached |
| Service Layer | Database | Parameterized queries, transaction boundaries, concurrency control |
| Service Layer | File System | Path validation, type validation, atomic writes |
| Service Layer | External API | Timeout, circuit breaker, response validation |
| Database | Service Layer | Null handling, type mapping, version checking |
| External API | Service Layer | Response schema validation, error handling, fallback |
| Service Layer | Controller | Serialization, field filtering (no internal data leakage) |
| Controller | User Response | Output encoding (XSS prevention), appropriate status codes |
| Any Layer | Time Operations | Timezone-aware, UTC normalized, Clock abstraction |
| Any Layer | Configuration | Validated at startup, typed access, secrets never logged |

Each row represents a boundary crossing. Every data field that moves across a boundary should be validated, normalized, and constrained at the destination side.
