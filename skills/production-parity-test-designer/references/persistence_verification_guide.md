# Persistence Verification Guide

A guide to verifying that data is actually stored correctly after user actions, going beyond UI confirmation to check the underlying data store. This guide addresses the "fake success" pattern where the application reports success but data is not persisted, partially persisted, or persisted incorrectly.

## The Core Problem

The most dangerous class of production bugs are **silent persistence failures**: the user sees a success message, the UI updates, but the data was never written to the database, was written incorrectly, or was written to the wrong location.

### Why This Happens

1. **Optimistic UI updates**: Frontend updates state before the backend confirms the write
2. **Cache-DB divergence**: Application reads from cache (updated) instead of database (not updated)
3. **Swallowed exceptions**: Backend catches database errors but returns 200 OK
4. **Transaction rollback**: Database transaction is rolled back but the response was already sent
5. **Async write failures**: Write is queued to a background worker that fails silently
6. **ORM silent failures**: ORM marks object as saved but flush/commit never executed

## What to Read After a UI Action

### The Read-After-Write Pattern

After every write operation in an E2E or integration test, perform an independent read to verify the data exists in the store.

**Critical rules**:
1. **Use a separate connection/session**: Do not read from the same ORM session that wrote the data (it may return cached state)
2. **Read from the database directly**: Use raw SQL or a separate repository instance
3. **Verify ALL fields**: Not just the primary key, but all business-relevant fields
4. **Check timestamps**: Verify `created_at`, `updated_at` are set and within expected range
5. **Verify related records**: If the write should create audit logs, history entries, or related records, check those too

### Python Example with SQLAlchemy

```python
def test_user_registration_persists():
    # ACT: Register user through the application layer
    response = client.post("/api/users", json={
        "email": "test@example.com",
        "name": "Test User",
    })
    assert response.status_code == 201

    # VERIFY PERSISTENCE: Read from a SEPARATE session
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT email, name, created_at FROM users WHERE email = :email"),
            {"email": "test@example.com"}
        )
        row = result.fetchone()

        # Verify record exists
        assert row is not None, "User record not found in database after 201 response"

        # Verify field values
        assert row.email == "test@example.com"
        assert row.name == "Test User"

        # Verify timestamp is recent (within last 5 seconds)
        assert row.created_at is not None
        assert (datetime.utcnow() - row.created_at).total_seconds() < 5
```

### JavaScript Example with Direct DB Query

```javascript
test('order creation persists to database', async () => {
  // ACT: Create order through API
  const response = await request(app)
    .post('/api/orders')
    .send({ product_id: 'PROD-001', quantity: 2 })
    .expect(201);

  const orderId = response.body.id;

  // VERIFY PERSISTENCE: Query database directly (not through ORM cache)
  const result = await pool.query(
    'SELECT id, product_id, quantity, status, created_at FROM orders WHERE id = $1',
    [orderId]
  );

  expect(result.rows).toHaveLength(1);
  expect(result.rows[0].product_id).toBe('PROD-001');
  expect(result.rows[0].quantity).toBe(2);
  expect(result.rows[0].status).toBe('pending');
  expect(result.rows[0].created_at).toBeDefined();
});
```

## Repository Read Helpers

### Building Verification Helpers

Create dedicated verification functions that read directly from the database (not through the application's ORM/cache layer).

```python
class PersistenceVerifier:
    """Direct database verification bypassing ORM cache."""

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)

    def verify_record_exists(self, table: str, conditions: dict) -> dict:
        """Verify a record exists and return its data."""
        where_clause = " AND ".join(f"{k} = :{k}" for k in conditions)
        query = text(f"SELECT * FROM {table} WHERE {where_clause}")

        with self.engine.connect() as conn:
            result = conn.execute(query, conditions)
            row = result.fetchone()

            if row is None:
                raise AssertionError(
                    f"Record not found in {table} with conditions: {conditions}"
                )
            return dict(row._mapping)

    def verify_record_count(self, table: str, conditions: dict, expected: int):
        """Verify the number of records matching conditions."""
        where_clause = " AND ".join(f"{k} = :{k}" for k in conditions)
        query = text(f"SELECT COUNT(*) as cnt FROM {table} WHERE {where_clause}")

        with self.engine.connect() as conn:
            result = conn.execute(query, conditions)
            actual = result.scalar()

            assert actual == expected, (
                f"Expected {expected} records in {table} with {conditions}, "
                f"found {actual}"
            )

    def verify_audit_log(self, entity_type: str, entity_id: str, action: str):
        """Verify an audit log entry was created for the action."""
        query = text(
            "SELECT * FROM audit_logs "
            "WHERE entity_type = :entity_type "
            "AND entity_id = :entity_id "
            "AND action = :action "
            "ORDER BY created_at DESC LIMIT 1"
        )

        with self.engine.connect() as conn:
            result = conn.execute(query, {
                "entity_type": entity_type,
                "entity_id": entity_id,
                "action": action,
            })
            row = result.fetchone()

            if row is None:
                raise AssertionError(
                    f"Audit log not found for {action} on {entity_type}:{entity_id}"
                )
            return dict(row._mapping)

    def verify_field_values(self, table: str, record_id: str, expected: dict):
        """Verify specific field values for a record."""
        row = self.verify_record_exists(table, {"id": record_id})

        mismatches = []
        for field, expected_value in expected.items():
            actual_value = row.get(field)
            if actual_value != expected_value:
                mismatches.append(
                    f"  {field}: expected={expected_value!r}, actual={actual_value!r}"
                )

        if mismatches:
            raise AssertionError(
                f"Field value mismatches in {table} (id={record_id}):\n"
                + "\n".join(mismatches)
            )
```

### Usage in Tests

```python
verifier = PersistenceVerifier(TEST_DATABASE_URL)

def test_order_complete_workflow():
    # Create order
    order = create_order(product="PROD-001", quantity=2)

    # Verify creation persisted
    row = verifier.verify_record_exists("orders", {"id": order.id})
    assert row["status"] == "pending"
    assert row["quantity"] == 2

    # Approve order
    approve_order(order.id)

    # Verify approval persisted
    row = verifier.verify_record_exists("orders", {"id": order.id})
    assert row["status"] == "approved"

    # Verify audit log
    verifier.verify_audit_log("order", str(order.id), "approved")

    # Verify history record
    verifier.verify_record_count(
        "order_history",
        {"order_id": str(order.id)},
        expected=2  # created + approved
    )
```

## Visible State vs Stored State

### The Divergence Problem

Visible state (what the user sees in the UI or API response) can diverge from stored state (what is actually in the database) in several ways:

| Visible State | Stored State | Problem |
|---------------|-------------|---------|
| "Saved successfully" | No record in database | Swallowed exception, transaction rollback |
| Shows updated value | Database has old value | Cache served stale data, write failed |
| Shows 5 items | Database has 3 items | Query includes soft-deleted or draft items |
| Shows correct total | Individual records sum to different total | Denormalized total not updated |
| Shows "Active" status | Database status is "Pending" | UI maps multiple DB states to one display state |

### Testing Visible vs Stored State

For each UI view or API endpoint, define:

1. **What the user sees**: The visible representation
2. **What must be true in the database**: The stored state that supports the visible representation
3. **The verification query**: A direct database query that confirms alignment

**Example: Dashboard Summary**

```
Visible: "Total Orders: 42, Revenue: $12,500"

Stored state requirements:
- COUNT(*) FROM orders WHERE status != 'cancelled' = 42
- SUM(total_amount) FROM orders WHERE status != 'cancelled' = 12500.00

Test:
1. Render dashboard
2. Extract displayed values
3. Run verification queries
4. Assert visible values match stored values
```

### Common Divergence Patterns

#### Cache Divergence

The application updates the cache but the database write fails. Subsequent reads show the cached (incorrect) data.

**Test pattern**:
```python
def test_cache_database_consistency():
    # Write through the application
    update_user_profile(user_id, name="New Name")

    # Read from application (may use cache)
    app_result = get_user_profile(user_id)

    # Read directly from database (bypasses cache)
    db_result = verifier.verify_record_exists("users", {"id": user_id})

    # They MUST match
    assert app_result["name"] == db_result["name"]
```

#### Soft Delete Divergence

UI shows "deleted" but record still exists with a flag. Or UI shows count that includes soft-deleted records.

**Test pattern**:
```python
def test_soft_delete_consistency():
    # Delete the item
    delete_item(item_id)

    # UI should NOT show the item
    items = list_items()
    assert item_id not in [i["id"] for i in items]

    # Database should have the record with deleted flag
    row = verifier.verify_record_exists("items", {"id": item_id})
    assert row["deleted_at"] is not None

    # Count should exclude deleted items
    active_count = verifier.verify_record_count(
        "items", {"deleted_at": None}, expected=len(items)
    )
```

## History Write vs Business Data Write

### Distinguishing Write Types

When an action occurs, the system typically writes two types of data:

1. **Business data write**: The primary record that drives application behavior (order status, user profile, account balance)
2. **History/audit write**: Secondary records that track what happened (audit log, changelog, event stream)

Both must be verified, as they serve different purposes:

| Write Type | Purpose | If Missing |
|-----------|---------|-----------|
| Business data | Drives current application state | Feature is broken, user sees incorrect state |
| History/audit | Provides trail for compliance, debugging, undo | Compliance violation, no way to trace what happened |
| Aggregated data | Denormalized summaries for performance | Reports show incorrect totals |

### Testing Both Write Types

```python
def test_order_approval_writes():
    order = create_order(product="PROD-001")

    # Approve the order
    approve_order(order.id, approver="user-42")

    # BUSINESS DATA: Order status updated
    row = verifier.verify_record_exists("orders", {"id": order.id})
    assert row["status"] == "approved"
    assert row["approved_by"] == "user-42"
    assert row["approved_at"] is not None

    # HISTORY: Audit log entry created
    audit = verifier.verify_audit_log("order", str(order.id), "approved")
    assert audit["actor"] == "user-42"
    assert audit["old_value"] == "pending"
    assert audit["new_value"] == "approved"

    # HISTORY: Order history entry created
    verifier.verify_record_count(
        "order_history",
        {"order_id": str(order.id)},
        expected=2  # create + approve
    )

    # AGGREGATED: Daily stats updated (if applicable)
    stats = verifier.verify_record_exists(
        "daily_order_stats",
        {"date": date.today().isoformat(), "status": "approved"}
    )
    assert stats["count"] >= 1
```

### What to Verify for Each Action Type

| Action | Business Data | History/Audit | Aggregated |
|--------|--------------|---------------|-----------|
| Create | Record exists with correct values | Audit: "created" entry | Count incremented |
| Update | Fields changed to new values | Audit: old + new values | Totals recalculated |
| Delete | Record removed or soft-deleted | Audit: "deleted" entry | Count decremented |
| Status change | Status field updated | Audit: old + new status | Status counts updated |
| Transfer | Source decremented, target incremented | Audit: transfer details | Balances recalculated |
| Batch operation | All affected records updated | Audit: batch reference | Totals recalculated |

## Persistence Verification Checklist

Use this checklist for every write operation in the system:

- [ ] **Record exists**: After create/update, the record is in the database
- [ ] **Field values correct**: All business fields match the input
- [ ] **Timestamps set**: `created_at`, `updated_at` are populated and reasonable
- [ ] **Foreign keys valid**: Related records exist and are correctly linked
- [ ] **Audit trail created**: History/audit entry exists with correct details
- [ ] **Cache consistent**: Application reads match database reads
- [ ] **Aggregates updated**: Denormalized counts/totals reflect the change
- [ ] **Concurrent safety**: Write under concurrent access does not lose data
- [ ] **Error visibility**: If write fails, error is propagated (not swallowed)
- [ ] **Transaction completeness**: Partial writes are rolled back, not committed

## Integration with Test Tiers

| Verification | Recommended Tier | Rationale |
|-------------|-----------------|-----------|
| Record exists after API call | Integration | Needs real DB |
| All fields correct | Integration | Needs real DB, fast enough for PR |
| Audit log created | Integration | Needs real DB |
| Cache-DB consistency | Integration or E2E | May need application cache layer |
| UI display matches DB | E2E | Needs full UI + DB |
| Concurrent write safety | Integration (parallel) | Needs real DB with concurrency |
| Error propagation on failure | Integration | Simulate DB failure |
| Full workflow persistence | E2E | Multi-step user workflow |
| Read-after-write in PR smoke | Smoke | At least one critical path in PR |
