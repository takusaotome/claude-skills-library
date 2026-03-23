# Safe Pattern Catalog

This reference provides approved safe patterns organized by category. Each pattern includes the rationale for why it is considered safe, the dangerous alternative it replaces, and implementation guidance.

---

## 1. Query Construction

### Safe Pattern: Parameterized Queries / ORM Exclusively

**Rationale**: SQL injection remains a top-10 vulnerability (OWASP A03:2021). String concatenation with user input creates injection vectors that are trivial to exploit and difficult to detect in review.

**Approved Approaches**:

| Approach | When to Use | Example |
|----------|-------------|---------|
| ORM query builder | Standard CRUD, filtering, pagination | `User.objects.filter(email=user_input)` |
| Parameterized raw SQL | Complex reporting, performance-critical paths | `cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])` |
| Named parameters | Stored procedure calls | `CALL update_balance(:account_id, :amount)` |

**Safety Properties**:
- User input never touches query structure
- Database driver handles escaping and type coercion
- Query plan caching is possible (performance benefit)

**Implementation Guidance**:
- Create a `QueryService` or repository layer that only exposes parameterized methods
- Framework-level middleware should reject any `execute()` call that does not use parameter binding
- For dynamic column selection or ORDER BY, use allowlists of permitted column names rather than parameterization (most drivers cannot parameterize identifiers)

**Contract Test**:
```python
def test_query_uses_parameters():
    """Verify that no query method constructs SQL via string concatenation."""
    # Inspect all repository methods for raw string formatting
    # Assert all SQL execution uses parameterized form
```

---

## 2. Authorization

### Safe Pattern: Deny-by-Default Authorization

**Rationale**: Opt-in authorization (where endpoints are open unless explicitly protected) guarantees that every new endpoint is a potential security hole until someone remembers to add the check. Deny-by-default inverts this: every endpoint is blocked unless explicitly granted.

**Approved Approaches**:

| Approach | When to Use | Example |
|----------|-------------|---------|
| Framework-level middleware | All HTTP endpoints | `@require_permission("users.read")` |
| Policy-based authorization | Complex business rules | `AuthorizationPolicy.can?(current_user, :view, resource)` |
| Attribute-based access control (ABAC) | Multi-tenant, role-hierarchy | `policy.evaluate(subject, action, resource, context)` |

**Safety Properties**:
- New endpoints are inaccessible by default until permissions are explicitly configured
- Authorization logic is centralized, not scattered across controllers
- Permission checks are auditable and testable

**Implementation Guidance**:
- Install a global middleware/interceptor that rejects requests unless the handler is annotated with a permission
- Use an `@public` annotation for genuinely public endpoints (forces explicit declaration of intent)
- Authorization decisions should be logged for audit purposes
- Permission definitions should live in a single registry, not inline in handler code

**Contract Test**:
```python
def test_all_endpoints_have_authorization():
    """Verify every registered route has an authorization annotation."""
    for route in app.routes:
        assert has_permission_annotation(route), f"Route {route.path} missing authorization"
```

---

## 3. File Handling

### Safe Pattern: Service-Layer File Abstraction

**Rationale**: Direct file path construction using string concatenation enables path traversal attacks (`../../etc/passwd`). Direct filesystem calls bypass access controls, audit logging, and storage abstraction.

**Approved Approaches**:

| Approach | When to Use | Example |
|----------|-------------|---------|
| FileService with path validation | All file read/write operations | `file_service.read(bucket, safe_filename)` |
| Storage abstraction layer | Cloud/local portability | `storage.get_object(container, key)` |
| Sandboxed upload handler | User-uploaded files | `upload_handler.save(file, allowed_types=["pdf", "png"])` |

**Safety Properties**:
- All paths are validated against a base directory (no traversal escape)
- File type validation occurs at the service boundary
- Operations are logged with caller identity and resource path
- Storage backend is swappable without changing business logic

**Implementation Guidance**:
- The `FileService` should resolve all paths relative to a configured base directory and reject any path containing `..` or absolute prefixes
- File names should be sanitized: strip path separators, limit character set, enforce maximum length
- Temporary files should use the framework's temp directory abstraction, not hardcoded `/tmp` paths
- File operations should be atomic where possible (write to temp, then rename)

**Contract Test**:
```python
def test_path_traversal_blocked():
    """Verify that path traversal attempts are rejected."""
    with pytest.raises(SecurityError):
        file_service.read("bucket", "../../etc/passwd")
    with pytest.raises(SecurityError):
        file_service.read("bucket", "/absolute/path/file.txt")
```

---

## 4. Persistence Confirmation

### Safe Pattern: Success Message After Persistence Confirmation

**Rationale**: Displaying a success message before the database transaction commits (or the API call succeeds) creates a false sense of completion. If the transaction rolls back or the network call fails, the user believes the action succeeded when it did not. This leads to silent data loss and corrupted business state.

**Approved Approaches**:

| Approach | When to Use | Example |
|----------|-------------|---------|
| Post-commit callback | Database writes | `transaction.on_commit(lambda: notify_user("Saved"))` |
| Response after await | Async API calls | `result = await api.save(data); show_success(result)` |
| Optimistic UI with reconciliation | High-latency operations | Show pending state, confirm on callback |

**Safety Properties**:
- User feedback accurately reflects system state
- Failed operations are surfaced to the user for retry
- No phantom success messages for rolled-back transactions

**Implementation Guidance**:
- UI frameworks should provide a `pending -> success/failure` state machine for all write operations
- Backend APIs should return the persisted entity (with generated IDs, timestamps) as confirmation
- Batch operations should report partial success/failure with item-level status
- Event-driven architectures should use outbox pattern to guarantee event delivery after commit

**Contract Test**:
```python
def test_success_only_after_commit():
    """Verify that success notification occurs after transaction commit."""
    # Simulate transaction rollback
    # Assert no success message was emitted
```

---

## 5. Dependency Loading

### Safe Pattern: Explicit Dependency Injection

**Rationale**: Implicit dependency loading (service locators, global singletons, magic imports) creates hidden coupling that makes testing unreliable, refactoring dangerous, and behavior environment-dependent.

**Approved Approaches**:

| Approach | When to Use | Example |
|----------|-------------|---------|
| Constructor injection | Class-based services | `class UserService(db: Database, cache: Cache)` |
| Function parameter injection | Functional handlers | `def handle(request, user_repo=Depends(get_user_repo))` |
| Framework DI container | Application wiring | `container.register(Database, PostgresDatabase)` |

**Safety Properties**:
- All dependencies are visible in the function/class signature
- Tests can substitute any dependency without monkey-patching
- Environment-specific configuration is centralized in the DI container
- Circular dependencies are detected at startup, not at runtime

**Implementation Guidance**:
- Prefer constructor injection over property injection (constructor enforces required dependencies)
- Use interfaces/protocols for dependency types, not concrete implementations
- Register all dependencies at application startup; avoid lazy registration
- Avoid the `@inject` pattern that hides dependencies behind decorators unless the framework mandates it

**Contract Test**:
```python
def test_no_global_state_access():
    """Verify service does not access global state directly."""
    # Analyze import statements and attribute access
    # Assert no references to global singletons or service locators
```

---

## 6. DateTime Normalization

### Safe Pattern: UTC-Aware Normalization at Persistence Boundary

**Rationale**: Mixing naive (timezone-unaware) and aware (timezone-aware) datetime objects causes silent comparison failures, incorrect scheduling, and off-by-one-day errors around midnight boundaries. The most common failure mode is storing local time as if it were UTC.

**Approved Approaches**:

| Approach | When to Use | Example |
|----------|-------------|---------|
| UTC-aware at persistence | All database writes | `aware_dt = local_dt.astimezone(timezone.utc)` before save |
| Timezone-aware throughout | Business logic | `now = datetime.now(timezone.utc)` never `datetime.now()` |
| Display conversion at boundary | UI rendering | `display_dt = utc_dt.astimezone(user_timezone)` at template layer |

**Safety Properties**:
- All persisted datetimes are UTC-aware (no ambiguity)
- Comparisons between datetimes are always valid (same timezone or aware objects)
- User sees times in their local timezone without corrupting stored data
- DST transitions are handled correctly

**Implementation Guidance**:
- Ban `datetime.now()` and `datetime.utcnow()` (both return naive datetimes in Python); require `datetime.now(timezone.utc)`
- Database columns should use `TIMESTAMP WITH TIME ZONE` (not `TIMESTAMP`)
- Serialization formats should always include timezone offset (ISO 8601 with `Z` or `+00:00`)
- Provide a `Clock` abstraction for testability (avoid `datetime.now()` in business logic)

**Contract Test**:
```python
def test_all_persisted_datetimes_are_utc_aware():
    """Verify that no naive datetime reaches the persistence layer."""
    # Intercept all ORM save operations
    # Assert all datetime fields have tzinfo set to UTC
```

---

## 7. Idempotency and Retries

### Safe Pattern: Idempotent Write Operations with Retry Safety

**Rationale**: Network failures, timeouts, and client retries mean that any write operation may be executed multiple times. Non-idempotent operations (e.g., incrementing a counter, creating a record without deduplication) produce incorrect state when retried.

**Approved Approaches**:

| Approach | When to Use | Example |
|----------|-------------|---------|
| Idempotency key | API write endpoints | `POST /orders` with `Idempotency-Key: uuid` header |
| Upsert with natural key | Data synchronization | `INSERT ... ON CONFLICT (external_id) DO UPDATE` |
| Outbox pattern | Event publishing | Write event to outbox table in same transaction; relay separately |
| State machine transitions | Status updates | Only allow valid transitions; reject duplicate transitions |

**Safety Properties**:
- Retried operations produce the same result as the first execution
- Duplicate records are prevented at the database level (unique constraints)
- Event consumers can safely replay without side effects
- Partial failures in distributed operations are recoverable

**Implementation Guidance**:
- All `POST` and `PUT` endpoints should accept an idempotency key and return the cached result for duplicate keys
- Use database-level unique constraints as the ultimate deduplication mechanism (not application-level checks alone)
- Design event handlers to be idempotent: check if the action has already been performed before executing
- For financial operations, use double-entry or ledger patterns that are inherently idempotent
- Configure retry policies with exponential backoff and jitter to avoid thundering herd

**Contract Test**:
```python
def test_duplicate_request_produces_same_result():
    """Verify that sending the same request twice returns identical responses."""
    key = str(uuid4())
    response1 = client.post("/orders", json=data, headers={"Idempotency-Key": key})
    response2 = client.post("/orders", json=data, headers={"Idempotency-Key": key})
    assert response1.json() == response2.json()
    assert Order.objects.filter(idempotency_key=key).count() == 1
```

---

## Cross-Category Patterns

### Named/Object Access Over Positional Access

**Rationale**: Positional access (`row[3]`, `args[0]`) is fragile and breaks silently when column order or argument order changes.

**Safe Pattern**: Always use named access (`row["email"]`, `args.email`). When working with database result sets, use ORM objects or named tuples. When working with CSV/Excel data, use pandas DataFrames with column names.

### Explicit Error Handling Over Silent Swallowing

**Rationale**: Bare `except: pass` or empty catch blocks hide failures that compound into corrupt state.

**Safe Pattern**: Catch specific exceptions, log with context, and either re-raise, return an error result, or take a defined recovery action. Never catch and ignore.

### Configuration Over Convention for Security-Relevant Behavior

**Rationale**: Convention-based security (e.g., "all files in /public are world-readable") fails when someone accidentally places a sensitive file in the wrong directory.

**Safe Pattern**: Security-relevant access is configured explicitly (allowlists, permission annotations, policy rules). Convention can supplement configuration but never replace it for security.
