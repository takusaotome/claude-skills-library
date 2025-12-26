# Common Code Defects & Design Gaps

> **Note:** This reference covers general-purpose code defects. Security vulnerabilities are out of scope - use a dedicated security reference for that purpose.

## Part 1: Code Defects (Bugs)

### Category A: Type Errors

#### A.1 String vs Number Comparison
```python
# BUG
order_id = "1234"
if order_id == 1234:  # Always False
    process()

# FIX
if str(order_id) == str(1234):
    process()
```

#### A.2 Float Precision
```python
# BUG
if total == 100.0:  # Unreliable
    apply_discount()

# FIX
import math
if math.isclose(total, 100.0, rel_tol=1e-9):
    apply_discount()
```

#### A.3 Excel Float Formatting
```python
# BUG: Excel stores "8236" as 8236.0
df.merge(left_on='Order')  # "8236" != 8236.0

# FIX
df['Order'] = df['Order'].apply(lambda x: str(int(float(x))) if pd.notna(x) else x)
```

### Category B: Null Handling

#### B.1 Silent NaN Propagation
```python
# BUG
df['total'] = df['price'] * df['qty']  # NaN if either is NaN

# FIX
df['total'] = df['price'].fillna(0) * df['qty'].fillna(0)
# Or explicitly handle:
df['total'] = df.apply(
    lambda r: r['price'] * r['qty'] if pd.notna(r['price']) and pd.notna(r['qty']) else None,
    axis=1
)
```

#### B.2 None in String Operations
```python
# BUG
name.lower()  # AttributeError if None

# FIX
name.lower() if name else ""
# Or
str(name or "").lower()
```

#### B.3 Empty Collection Access
```python
# BUG
first_item = items[0]  # IndexError if empty

# FIX
first_item = items[0] if items else None
```

### Category C: Logic Errors

#### C.1 Off-by-One
```python
# BUG: Misses last item
for i in range(len(items) - 1):
    process(items[i])

# FIX
for i in range(len(items)):
    process(items[i])
```

#### C.2 Wrong Operator
```python
# BUG: Should be "or"
if has_email and has_phone:  # Requires BOTH
    can_contact = True

# FIX
if has_email or has_phone:  # Requires EITHER
    can_contact = True
```

#### C.3 Inverted Condition
```python
# BUG
if not is_valid:
    save_to_database()  # Saves INVALID data!

# FIX
if is_valid:
    save_to_database()
```

### Category D: Data Flow Errors

#### D.1 Asymmetric Normalization
```python
# BUG: Only left side normalized
left_df['key'] = normalize(left_df['key'])
result = left_df.merge(right_df, on='key')  # Mismatch!

# FIX
left_df['key'] = normalize(left_df['key'])
right_df['key'] = normalize(right_df['key'])  # Both sides
result = left_df.merge(right_df, on='key')
```

#### D.2 Use Before Initialize
```python
# BUG
df['full_name'] = df['first'] + " " + df['last']
df['first'] = df['first'].str.strip()  # Too late!

# FIX
df['first'] = df['first'].str.strip()  # First
df['full_name'] = df['first'] + " " + df['last']  # Then
```

#### D.3 Overwrite Before Use
```python
# BUG
df['status'] = map_to_new_status(df['status'])
if df['status'] == 'OLD_VALUE':  # Never matches!
    ...

# FIX
df['new_status'] = map_to_new_status(df['status'])
if df['status'] == 'OLD_VALUE':  # Original preserved
    ...
```

### Category E: Wiring Errors

#### E.1 Dead Function
```python
# BUG: Function defined but never called
def important_validation(data):
    return validate(data)

# ... nowhere in codebase calls important_validation()
```

#### E.2 Placeholder Arguments
```python
# BUG: Always passes None
def process(data, config=None, lookup=None):
    if lookup:
        # This NEVER runs because caller always passes None
        enhanced = lookup_values(data, lookup)

# Caller:
process(data, config=None, lookup=None)  # Dead code inside
```

#### E.3 Ignored Return Value
```python
# BUG
validate(data)  # Returns errors list, but ignored!
save(data)  # Saves even if invalid

# FIX
errors = validate(data)
if not errors:
    save(data)
```

### Category F: Concurrency / Idempotency / Transactions

#### F.1 Race Condition
```python
# BUG: TOCTOU (time-of-check to time-of-use)
if balance >= amount:
    # Another thread may modify balance here!
    balance -= amount

# FIX: Use atomic operation or lock
with lock:
    if balance >= amount:
        balance -= amount
```

#### F.2 Non-Idempotent Operation
```python
# BUG: Counter increments on every retry
def process_order(order_id):
    increment_counter()  # Runs multiple times on retry!
    do_work()

# FIX: Check if already processed
def process_order(order_id):
    if is_processed(order_id):
        return
    increment_counter()
    do_work()
    mark_processed(order_id)
```

#### F.3 Missing Transaction Boundary
```python
# BUG: Partial update if second operation fails
update_inventory(item_id, -1)
create_order(order_data)  # If this fails, inventory is wrong

# FIX: Wrap in transaction
with transaction():
    update_inventory(item_id, -1)
    create_order(order_data)
```

### Category G: Timeouts / Retry / Resource Leak

#### G.1 Missing Timeout
```python
# BUG: Hangs forever if API is slow
response = requests.get(url)

# FIX: Add timeout
response = requests.get(url, timeout=30)
```

#### G.2 Unbounded Retry
```python
# BUG: Retries forever
while True:
    try:
        result = call_api()
        break
    except:
        time.sleep(1)

# FIX: Max attempts with backoff
for attempt in range(3):
    try:
        result = call_api()
        break
    except:
        time.sleep(2 ** attempt)
else:
    raise MaxRetriesExceeded()
```

#### G.3 Resource Leak
```python
# BUG: Connection not closed on error
conn = open_connection()
result = conn.query()  # If this raises, connection leaks
conn.close()

# FIX: Use context manager
with open_connection() as conn:
    result = conn.query()
```

### Category H: API Contract / Backward Compatibility

#### H.1 Breaking API Change
```python
# BUG: Existing callers expect 2 return values
# BEFORE: return result, status
# AFTER:  return result  # Breaks all callers!

# FIX: Add new parameter with default
def process(data, return_status=True):
    if return_status:
        return result, status
    return result
```

#### H.2 Missing Input Validation
```python
# BUG: Trusts caller to provide valid data
def save_user(user_data):
    db.insert(user_data)  # No validation!

# FIX: Validate at API boundary
def save_user(user_data):
    validate_user(user_data)  # Enforce contract
    db.insert(user_data)
```

#### H.3 Unsafe Default Value
```python
# BUG: New parameter breaks existing behavior
def search(query, limit=None):  # Changed from limit=10
    # Existing callers now get unlimited results!

# FIX: Preserve existing default
def search(query, limit=10):
    ...
```

---

## Part 2: Design Gaps

### Category I: Missing Edge Cases

#### I.1 Empty Input Not Considered
```markdown
Design says: "Process all orders"
Missing: What if there are no orders?
Impact: Division by zero, empty file errors
```

#### I.2 Duplicate Data Not Considered
```markdown
Design says: "Join on Order Number"
Missing: What if Order Number is duplicated?
Impact: Row multiplication (1:N becomes N:M)
```

#### I.3 Special Values Not Considered
```markdown
Design says: "State is 2-letter code"
Reality: Data contains "California", "N/A", "", null
Impact: Lookup failures, wrong results
```

### Category J: Invalid Assumptions

#### J.1 Uniqueness Assumption
```markdown
Design assumes: "Each order has one address"
Reality: Multiple addresses per order (billing vs shipping)
Impact: Wrong address selected or data loss
```

#### J.2 Completeness Assumption
```markdown
Design assumes: "All records have required fields"
Reality: 30% of records missing City field
Impact: 30% of records fail to match
```

#### J.3 Format Assumption
```markdown
Design assumes: "Phone numbers are 10 digits"
Reality: International formats, extensions, "(555) 123-4567"
Impact: Validation rejects valid numbers
```

### Category K: Missing Error Handling

#### K.1 External Service Failure
```markdown
Design says: "Call API to get data"
Missing: What if API is down? Timeout? Rate limited?
Impact: Entire pipeline fails
```

#### K.2 File Not Found
```markdown
Design says: "Read from input file"
Missing: What if file doesn't exist? Wrong format?
Impact: Crash with unclear error
```

#### K.3 Data Validation Failure
```markdown
Design says: "Validate and process"
Missing: What to do with invalid records?
Impact: Silent skip or crash
```

### Category L: Performance Gaps

#### L.1 N+1 Query Pattern
```markdown
Design says: "For each order, look up customer"
Missing: This is O(n) lookups
Impact: 10,000 orders = 10,000 lookups = slow
Fix: Batch lookup or join
```

#### L.2 Memory Explosion
```markdown
Design says: "Load all data into memory"
Missing: What if data is 10GB?
Impact: Out of memory crash
Fix: Streaming or chunked processing
```

---

## Part 3: Detection Strategies

### Strategy 1: Question Everything
```markdown
For each line of code, ask:
- What if this is null?
- What if this is empty?
- What if this is the wrong type?
- What if this fails?
```

### Strategy 2: Trace a Record
```markdown
Pick a specific record and trace through:
1. Where does it enter?
2. What transformations happen?
3. Where does it exit?
4. Is the result correct?
```

### Strategy 3: Test Boundaries
```markdown
For any operation on data, test:
- Empty input
- Single item
- Maximum size
- Invalid values
- Missing values
```

### Strategy 4: Count Before and After
```markdown
At each stage:
- How many records in?
- How many records out?
- If different, is that expected?
```

### Strategy 5: Profile Real Data
```python
# Before assuming, verify:
df['column'].dtype           # Actual type
df['column'].isna().sum()    # Null count
df['column'].nunique()       # Unique values
df['column'].value_counts()  # Distribution
```

---

## Quick Reference: Red Flags

| Pattern | Likely Bug |
|---------|-----------|
| `= None` in function call | Placeholder never replaced |
| `except: pass` | Errors silently ignored |
| `[0]` without length check | Index error on empty |
| `.lower()` without null check | Attribute error on None |
| Single-side normalization | Join mismatch |
| Function defined, never called | Dead code |
| Return value not captured | Result ignored |
| `== 0.0` or `== float` | Float comparison issue |
