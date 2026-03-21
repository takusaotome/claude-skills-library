# Hidden Spec Patterns

## Purpose

This reference catalogs common patterns where implicit contracts deviate from surface expectations. Each pattern includes a description, real-world examples, detection heuristics, and associated risk. Use this catalog during Workflow 4 (Mismatch Classification) to systematically identify contract discrepancies.

---

## Pattern 1: Name vs. Behavior Mismatch

### Description
The function or variable name implies one behavior, but the implementation does something materially different. This is the most common and most dangerous hidden contract pattern because developers naturally trust names when reading and integrating code.

### Examples

**Example 1.1: Formatting hidden in a calculation name**
```python
def keepTwoDecimal(value):
    """Rounds to 2 decimal places."""
    return "{:,.2f}".format(value)
    # Name implies: numeric rounding
    # Actual: returns comma-formatted STRING "1,234.56"
    # Risk: arithmetic on return value causes TypeError or silent corruption
```

**Example 1.2: Getter with side effects**
```python
def getNextId():
    global _counter
    _counter += 1        # Side effect: mutates global state
    log_access(_counter)  # Side effect: writes to log/DB
    return _counter
    # Name implies: pure read operation
    # Actual: mutates state and logs on every call
    # Risk: calling twice gives different results; test/prod divergence
```

**Example 1.3: Validator that transforms**
```python
def validateEmail(email):
    email = email.strip().lower()  # Transforms input
    if "@" not in email:
        return None
    return email  # Returns transformed value, not boolean
    # Name implies: returns True/False validation result
    # Actual: returns cleaned email or None
    # Risk: caller uses `if validateEmail(x)` thinking it's boolean
```

### Detection Heuristics
- Compare function name verb (get, set, validate, calculate, format, check, is, has) against return type and side effects
- Flag any "get" or "is/has" function that has write operations
- Flag any "calculate" or "compute" function that returns strings
- Flag any "validate" or "check" function that returns non-boolean
- Flag any function whose name has no verb (ambiguous purpose)

---

## Pattern 2: Formatted Return Values

### Description
A function returns values with formatting applied (commas, currency symbols, padding, HTML tags) when the caller expects raw data. This pattern is especially dangerous when return values are used in further computation.

### Examples

**Example 2.1: Numeric formatting**
```python
def calculate_total(items):
    total = sum(item.price for item in items)
    return f"${total:,.2f}"  # Returns "$1,234.56" not 1234.56
```

**Example 2.2: Date formatting**
```python
def get_created_date(record):
    return record.created_at.strftime("%Y/%m/%d")  # Returns string, not datetime
```

**Example 2.3: Padded identifiers**
```python
def get_employee_id(employee):
    return str(employee.id).zfill(8)  # Returns "00001234" not 1234
```

### Detection Heuristics
- Look for `format()`, f-strings, `.strftime()`, `.zfill()` in return statements
- Check if return value goes through any string templating
- Examine if the function name suggests a data type but returns a different one
- Search callers for `int()`, `float()`, `Decimal()` wrapping (sign of known mismatch)

---

## Pattern 3: Mutable Object Sharing

### Description
A function returns a reference to an internal mutable object (list, dict, set) rather than a copy. Callers who modify the return value inadvertently modify internal state, causing action-at-a-distance bugs.

### Examples

**Example 3.1: Returning internal list**
```python
class ConfigManager:
    def __init__(self):
        self._allowed_hosts = ["localhost", "127.0.0.1"]

    def get_allowed_hosts(self):
        return self._allowed_hosts  # Returns reference, not copy
        # Risk: caller.append("evil.com") modifies internal state
```

**Example 3.2: Returning cached dict**
```python
_cache = {}

def get_user_profile(user_id):
    if user_id not in _cache:
        _cache[user_id] = db.fetch_user(user_id)
    return _cache[user_id]  # Returns cached reference
    # Risk: caller modifying returned dict corrupts cache
```

**Example 3.3: Default mutable argument**
```python
def add_item(item, items=[]):  # Mutable default shared across calls
    items.append(item)
    return items
    # Risk: items list persists between calls
```

### Detection Heuristics
- Look for functions returning `self._*` attributes (internal state exposure)
- Check for module-level dicts/lists being returned directly
- Flag mutable default arguments (`def f(x=[])`, `def f(x={})`)
- Check if returned collections are wrapped in `list()`, `dict()`, `copy()` -- absence means shared reference
- Look for `@property` decorators returning mutable internals

---

## Pattern 4: Scope Shadowing

### Description
An identifier (variable, function, class) in one scope shadows a same-named identifier in another scope. Developers reading code may reference the wrong one, especially when names are common (e.g., `config`, `result`, `data`, `user`).

### Examples

**Example 4.1: Local shadows module-level**
```python
config = load_global_config()  # Module-level

def process_request(request):
    config = request.get("config", {})  # Shadows module-level config
    validate(config)  # Which config? The local one.
    # Risk: developer adds code expecting module-level config
```

**Example 4.2: Import shadows builtin**
```python
from utils import filter  # Shadows builtin filter()

results = filter(items, criteria)  # Calls utils.filter, not builtin
```

**Example 4.3: Nested function shadows parameter**
```python
def outer(data):
    def inner():
        data = transform(data)  # UnboundLocalError: shadows parameter
        return data
    return inner()
```

### Detection Heuristics
- Search for same-named variables at different scope levels (module, class, function, block)
- Check for local assignments that match parameter names
- Look for imports that shadow builtins (`list`, `dict`, `type`, `filter`, `map`, `id`, `input`)
- In languages with block scoping, check for re-declarations in nested blocks
- Flag common shadow-prone names: `config`, `data`, `result`, `response`, `error`, `user`, `item`, `value`

---

## Pattern 5: Optional Parameter Behavior Change

### Description
A function's behavior changes significantly based on the presence or value of optional parameters, and the default behavior is not what the caller expects.

### Examples

**Example 5.1: Destructive default**
```python
def save_record(record, overwrite=True):
    # Default overwrites existing record without warning
    if overwrite:
        db.upsert(record)
    else:
        db.insert(record)  # Raises on duplicate
    # Risk: caller doesn't pass overwrite, silently overwrites data
```

**Example 5.2: Mode-switching parameter**
```python
def fetch_data(query, use_cache=True):
    if use_cache:
        return _cache.get(query, None)  # Returns None if not cached
    else:
        return db.execute(query)  # Returns QueryResult
    # Risk: different return types based on parameter
    # Cached path returns None; non-cached path never returns None
```

**Example 5.3: Silent behavior suppression**
```python
def send_notification(user, message, dry_run=False):
    if dry_run:
        logger.info(f"Would send: {message}")
        return {"status": "dry_run"}
    result = email_service.send(user.email, message)
    audit_log.record(user.id, message)  # Side effect only in non-dry_run
    return result
    # Risk: tests use dry_run=True, never exercise real send path
    # Audit logging contract invisible in test environment
```

### Detection Heuristics
- List all optional parameters and their defaults for the target function
- Check if any optional parameter controls a branch that changes return type
- Check if any optional parameter enables/disables side effects
- Look for boolean parameters named `force`, `overwrite`, `dry_run`, `silent`, `strict`, `raw`
- Examine if tests always pass the same optional parameter values (narrowing the tested contract)

---

## Pattern 6: Exception Swallowing and Mixed Error Handling

### Description
A function catches exceptions internally and returns a fallback value instead of propagating the error. Or a function mixes exception-based and return-value-based error signaling, making the error contract ambiguous.

### Examples

**Example 6.1: Silent exception swallowing**
```python
def parse_config(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}  # Silently returns empty dict on ANY error
    # Risk: file permission error, JSON syntax error, and missing file
    # all return {} -- caller cannot distinguish error from empty config
```

**Example 6.2: Mixed error signaling**
```python
def find_user(user_id):
    if not user_id:
        return None           # Error via return value
    user = db.query(User, user_id)
    if not user:
        raise UserNotFoundError(user_id)  # Error via exception
    return user
    # Risk: caller must handle BOTH None check AND exception catch
```

**Example 6.3: Retry masking**
```python
def call_api(endpoint):
    for attempt in range(3):
        try:
            return requests.get(endpoint).json()
        except RequestException:
            time.sleep(2 ** attempt)
    return None  # After 3 failures, silently returns None
    # Risk: caller sees None but doesn't know it means "API unreachable"
    # Transient failures become silent data gaps
```

### Detection Heuristics
- Search for bare `except Exception` or `except:` blocks in the target function
- Check if catch blocks return a value instead of re-raising
- Look for functions that return different "shapes" on success vs. failure
- Flag functions where `None` return could mean "not found" OR "error occurred"
- Check for retry loops that end with a fallback return value

---

## Pattern Summary Matrix

| Pattern | Primary Risk | Detection Difficulty | Typical Severity |
|---------|-------------|---------------------|-----------------|
| Name vs. Behavior | Type error, logic error | Low (name analysis) | Critical |
| Formatted Return | Arithmetic corruption | Medium (trace returns) | High |
| Mutable Sharing | Action-at-distance bugs | Medium (reference analysis) | High |
| Scope Shadowing | Wrong variable reference | Low (scope analysis) | Medium-High |
| Optional Parameter | Mode-dependent behavior | Medium (parameter analysis) | Medium-High |
| Exception Swallowing | Silent failures | High (trace all paths) | Critical |

## Cross-Pattern Interactions

Some of the most dangerous hidden contracts emerge when multiple patterns combine:

- **Name Mismatch + Formatted Return**: `calculatePrice()` returns `"$1,234.56"` -- name suggests number, format confirms string
- **Mutable Sharing + Scope Shadowing**: returned mutable object is assigned to a variable that shadows another, causing cascading confusion
- **Optional Parameter + Exception Swallowing**: `dry_run=True` suppresses an exception path that only surfaces in production
- **Scope Shadowing + State Dependency**: shadowed variable reads from global state in one scope but local state in another

When classifying mismatches, always check for pattern combinations -- single-pattern mismatches are easier to catch; multi-pattern interactions cause the worst incidents.
