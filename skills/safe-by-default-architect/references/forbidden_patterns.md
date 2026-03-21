# Forbidden Patterns Reference

This reference catalogs implementation patterns that are explicitly forbidden, explaining why each is dangerous, showing common manifestations, providing safe alternatives, and defining the narrow conditions under which exceptions may be granted.

---

## Classification Taxonomy

Every forbidden pattern is classified by its primary danger mechanism:

| Category | Code | Description |
|----------|------|-------------|
| Injection / Bypass / Traversal | IBT | Attacker-controlled input reaches sensitive operations |
| Silent Corruption | SC | Data is modified or lost without error or notification |
| Environment Divergence | ED | Behavior differs between dev/staging/production |
| Hidden Dependency | HD | Implicit coupling that breaks under change |
| Human Error Amplification | HEA | Design makes mistakes easy and recovery hard |
| Unverifiable Behavior | UB | Cannot confirm correctness through testing alone |

---

## FP-01: Raw SQL String Concatenation

**Classification**: IBT (Injection / Bypass / Traversal)

**What is Forbidden**: Constructing SQL queries by concatenating or formatting user-supplied values directly into query strings.

**Why Dangerous**: SQL injection allows attackers to read, modify, or delete arbitrary data, bypass authentication, and in some configurations execute operating system commands. It is the single most exploited class of web application vulnerability. String concatenation makes injection trivial because the database cannot distinguish between query structure and data.

**Common Manifestations**:
```python
# FORBIDDEN: String concatenation
query = "SELECT * FROM users WHERE email = '" + user_email + "'"

# FORBIDDEN: f-string / format
query = f"SELECT * FROM users WHERE id = {user_id}"

# FORBIDDEN: % formatting
query = "SELECT * FROM users WHERE name = '%s'" % user_name
```

**Safe Alternatives**:
```python
# APPROVED: Parameterized query
cursor.execute("SELECT * FROM users WHERE email = %s", [user_email])

# APPROVED: ORM
User.objects.filter(email=user_email)

# APPROVED: Query builder
query = select(users).where(users.c.email == user_email)
```

**Exception Conditions**: None. There is no legitimate reason to concatenate user input into SQL. Even for dynamic column names or ORDER BY clauses, use allowlists of permitted identifiers.

---

## FP-02: Opt-In Authorization

**Classification**: IBT (Injection / Bypass / Traversal), HEA (Human Error Amplification)

**What is Forbidden**: Authorization models where endpoints are accessible by default and developers must remember to add protection to each new route.

**Why Dangerous**: Every new endpoint starts as a security hole. The defect is invisible because the endpoint works correctly from a functional perspective. Authorization gaps are only discovered through security audits or exploitation. The probability of missing authorization on at least one endpoint approaches certainty as the codebase grows.

**Common Manifestations**:
```python
# FORBIDDEN: Authorization only on some endpoints
@app.route("/admin/users")
@require_admin  # This endpoint is protected
def list_users(): ...

@app.route("/admin/export")  # MISSING authorization check
def export_data(): ...

# FORBIDDEN: Role check inside handler (easy to forget)
def update_settings(request):
    if not request.user.is_admin:  # What if this check is forgotten?
        return HttpResponseForbidden()
```

**Safe Alternatives**:
```python
# APPROVED: Global deny-by-default middleware
# All routes require authorization; public routes must be explicitly annotated
@app.route("/admin/export")
@require_permission("admin.export")
def export_data(): ...

@app.route("/public/health")
@public  # Explicit opt-out of authorization
def health_check(): ...
```

**Exception Conditions**: Public-facing read-only endpoints (health checks, public API documentation, login page) may use an `@public` annotation. This annotation must be explicitly applied and is itself an authorization decision (declaring "this endpoint is intentionally public").

---

## FP-03: Direct File Path Construction

**Classification**: IBT (Injection / Bypass / Traversal), HEA (Human Error Amplification)

**What is Forbidden**: Building file paths by concatenating user-supplied values, or accessing the filesystem directly without a service abstraction layer.

**Why Dangerous**: Path traversal attacks use `../` sequences or absolute paths to escape the intended directory and access arbitrary files. Direct filesystem access also bypasses access controls, audit logging, and makes it impossible to swap storage backends.

**Common Manifestations**:
```python
# FORBIDDEN: Path concatenation
file_path = "/uploads/" + username + "/" + filename
data = open(file_path).read()

# FORBIDDEN: f-string path construction
path = f"/data/reports/{report_id}.pdf"

# FORBIDDEN: os.path.join with unsanitized input
path = os.path.join(BASE_DIR, user_input)  # user_input could be "/etc/passwd"
```

**Safe Alternatives**:
```python
# APPROVED: Service layer with path validation
content = file_service.read(bucket="uploads", key=filename)

# APPROVED: Validated path resolution
safe_path = storage.resolve_safe_path(base_dir, user_input)
# Internally: resolves symlinks, rejects traversal, validates within base

# APPROVED: Cloud storage abstraction
blob = storage_client.get_blob(container="reports", name=f"{report_id}.pdf")
```

**Exception Conditions**: Build scripts, infrastructure automation, and CLI tools that do not handle user input may access the filesystem directly. Application code that serves or processes user-specified paths must always use the service abstraction.

---

## FP-04: Success Message Before Persistence Confirmation

**Classification**: SC (Silent Corruption), HEA (Human Error Amplification)

**What is Forbidden**: Displaying success feedback to the user before the write operation has been confirmed by the persistence layer (database commit, API response, file system sync).

**Why Dangerous**: If the transaction rolls back, the API call fails, or the write is lost, the user believes the action succeeded. This leads to phantom records, lost data, and business decisions based on incorrect state. The user has no reason to retry because they saw a success message.

**Common Manifestations**:
```javascript
// FORBIDDEN: Success before await
showToast("Order saved successfully!");
await api.saveOrder(orderData);  // This might fail

// FORBIDDEN: Success before commit
flash("Record updated")
db.session.add(record)
db.session.commit()  // This might throw
```

**Safe Alternatives**:
```javascript
// APPROVED: Success after confirmation
try {
    const result = await api.saveOrder(orderData);
    showToast("Order saved successfully!");  // Only after response
} catch (error) {
    showToast("Failed to save order. Please retry.", "error");
}

// APPROVED: Post-commit callback
db.session.add(record)
db.session.commit()
flash("Record updated")  // After successful commit
```

**Exception Conditions**: Optimistic UI patterns are acceptable when paired with reconciliation. The initial "success" must be visually distinct (e.g., "Saving..." or a pending indicator), and failure must be surfaced retroactively with a retry mechanism.

---

## FP-05: Mixed Naive and Aware DateTime Objects

**Classification**: SC (Silent Corruption), ED (Environment Divergence)

**What is Forbidden**: Using naive (timezone-unaware) datetime objects in any code that persists, compares, or transmits datetime values. Mixing naive and aware datetimes in the same codebase.

**Why Dangerous**: Naive datetimes are ambiguous (is `2024-03-15 09:00:00` UTC? Local time? Server time?). Comparing a naive and aware datetime raises an exception in some languages and silently returns wrong results in others. The most insidious failure mode is storing local server time as if it were UTC, which works in UTC-aligned environments but breaks everywhere else.

**Common Manifestations**:
```python
# FORBIDDEN: datetime.now() returns naive datetime
created_at = datetime.now()

# FORBIDDEN: datetime.utcnow() also returns naive datetime
timestamp = datetime.utcnow()

# FORBIDDEN: Parsing without timezone
dt = datetime.strptime("2024-03-15 09:00", "%Y-%m-%d %H:%M")

# FORBIDDEN: Comparing naive and aware
if naive_dt > aware_dt:  # TypeError or wrong result
    ...
```

**Safe Alternatives**:
```python
# APPROVED: Always timezone-aware
from datetime import datetime, timezone
created_at = datetime.now(timezone.utc)

# APPROVED: Parse with timezone
from dateutil.parser import parse
dt = parse("2024-03-15 09:00+09:00")

# APPROVED: Convert to UTC at persistence boundary
utc_dt = local_dt.astimezone(timezone.utc)
db.save(record, created_at=utc_dt)
```

**Exception Conditions**: Date-only values (no time component) may use `date` objects without timezone when the business context is date-granular (e.g., "birthday", "hire date"). Datetime values must always be timezone-aware.

---

## FP-06: Positional Data Access

**Classification**: SC (Silent Corruption), HEA (Human Error Amplification)

**What is Forbidden**: Accessing data by numeric index position when named/keyed access is available. This includes database row access by column index, CSV parsing by position, and function arguments by position for complex signatures.

**Why Dangerous**: Positional access is fragile. Adding, removing, or reordering columns/fields changes the meaning of every subsequent index. The code continues to run without error but produces incorrect results. The failure is silent and often only discovered through downstream data corruption.

**Common Manifestations**:
```python
# FORBIDDEN: Column index access
name = row[1]    # What is column 1? What if a column is added before it?
email = row[3]   # This breaks if any column is inserted at position 0-2

# FORBIDDEN: Tuple unpacking without names
for id, name, email, phone in cursor.fetchall():
    ...  # Breaks if SELECT column order changes
```

**Safe Alternatives**:
```python
# APPROVED: Named access via ORM
user = User.objects.get(id=user_id)
name = user.name
email = user.email

# APPROVED: Dictionary-style access
row = cursor.fetchone()
name = row["name"]
email = row["email"]

# APPROVED: Named tuples or dataclasses
from collections import namedtuple
UserRow = namedtuple("UserRow", ["id", "name", "email", "phone"])
```

**Exception Conditions**: Low-level data processing where column positions are defined by a fixed specification (e.g., fixed-width file formats, binary protocols) may use positional access with clear documentation of the format specification.

---

## FP-07: Bare Exception Swallowing

**Classification**: SC (Silent Corruption), UB (Unverifiable Behavior)

**What is Forbidden**: Catching exceptions with bare `except` or `catch(Exception)` and either ignoring them entirely or logging without re-raising or returning an error state.

**Why Dangerous**: Swallowed exceptions mask failures that compound into corrupt state. A failed database write, a dropped network connection, or a permission error is silently ignored, and the code continues as if nothing happened. Debugging becomes nearly impossible because the original error context is lost.

**Common Manifestations**:
```python
# FORBIDDEN: Bare except with pass
try:
    save_to_database(record)
except:
    pass  # Silently swallows ALL errors including SystemExit

# FORBIDDEN: Catch-all with only logging
try:
    process_payment(order)
except Exception as e:
    logger.error(f"Error: {e}")
    # Continues execution as if payment succeeded

# FORBIDDEN: Overly broad catch hiding specific failures
try:
    result = complex_operation()
except Exception:
    result = default_value  # Hides the real problem
```

**Safe Alternatives**:
```python
# APPROVED: Specific exception with recovery action
try:
    save_to_database(record)
except IntegrityError as e:
    logger.warning(f"Duplicate record: {e}")
    return existing_record  # Defined recovery action
except DatabaseError as e:
    logger.error(f"Database error: {e}", exc_info=True)
    raise ServiceUnavailableError("Unable to save record") from e

# APPROVED: Specific catch with error propagation
try:
    result = process_payment(order)
except PaymentGatewayError as e:
    return PaymentResult(success=False, error=str(e))
```

**Exception Conditions**: Top-level error handlers in web frameworks or CLI tools may catch broad exceptions to prevent process crashes, but must log the full stack trace and return appropriate error responses. This is the only legitimate use of broad exception handling.

---

## FP-08: Implicit Dependency via Global State

**Classification**: HD (Hidden Dependency), ED (Environment Divergence), UB (Unverifiable Behavior)

**What is Forbidden**: Accessing shared state through global variables, module-level singletons, or service locator patterns instead of explicit dependency injection.

**Why Dangerous**: Global state creates invisible coupling between components. Tests pass when run in isolation but fail when run together due to shared state pollution. Behavior changes between environments because global state initialization differs. Refactoring is dangerous because dependency relationships are not visible in function signatures.

**Common Manifestations**:
```python
# FORBIDDEN: Module-level global
db = Database.connect(os.environ["DATABASE_URL"])

class UserService:
    def get_user(self, user_id):
        return db.query("SELECT * FROM users WHERE id = %s", [user_id])

# FORBIDDEN: Service locator
class OrderProcessor:
    def process(self, order):
        payment = ServiceLocator.get("PaymentService")
        payment.charge(order.total)
```

**Safe Alternatives**:
```python
# APPROVED: Constructor injection
class UserService:
    def __init__(self, db: Database):
        self.db = db

    def get_user(self, user_id):
        return self.db.query("SELECT * FROM users WHERE id = %s", [user_id])

# APPROVED: Framework DI
@inject
class OrderProcessor:
    def __init__(self, payment: PaymentService):
        self.payment = payment
```

**Exception Conditions**: Framework-mandated patterns (e.g., Django's `settings` module, Flask's `current_app`) are acceptable when they are the idiomatic approach for that framework. However, business logic should still receive dependencies via injection rather than accessing framework globals directly.

---

## Pattern Interaction Matrix

Some forbidden patterns compound each other's danger:

| Pattern A | Pattern B | Compound Risk |
|-----------|-----------|---------------|
| FP-01 (Raw SQL) | FP-02 (Opt-in Auth) | SQL injection on unprotected endpoint = full database compromise |
| FP-03 (Direct File) | FP-07 (Exception Swallow) | Path traversal error is silently ignored, attacker probes undetected |
| FP-04 (Early Success) | FP-05 (Naive DateTime) | User sees success, but record saved with wrong timezone corrupts data |
| FP-06 (Positional Access) | FP-05 (Naive DateTime) | Column reorder puts datetime in wrong field, silently corrupting |
| FP-08 (Global State) | FP-01 (Raw SQL) | Test mocks hide SQL injection because global DB is mocked |

When multiple forbidden patterns co-exist, prioritize eliminating the compound risks first.
