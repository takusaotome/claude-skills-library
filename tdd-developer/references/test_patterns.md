# Test Patterns and Techniques

## Test Structure Patterns

### Single Assertion Rule
Each test should have one logical assertion:
- Tests one behavior
- Clear failure message
- Easy to understand

```python
# Good - Single focus
def test_add_returns_sum_of_two_numbers():
    assert add(2, 3) == 5

# Avoid - Multiple unrelated assertions
def test_calculator():
    assert add(2, 3) == 5
    assert subtract(5, 3) == 2
    assert multiply(2, 3) == 6
```

### Test Isolation
Each test must be independent:
- No shared mutable state
- Tests can run in any order
- Use setup/teardown for each test

### Setup Patterns

#### Per-test Setup
```python
class TestUserService:
    def setup_method(self):
        self.db = InMemoryDatabase()
        self.service = UserService(self.db)

    def test_create_user(self):
        # Uses fresh db and service
        pass
```

#### Shared Fixtures
```python
@pytest.fixture
def database():
    db = create_test_database()
    yield db
    db.cleanup()

def test_with_database(database):
    # Uses fixture
    pass
```

## Test Types in TDD

### Unit Tests
- Test single units (functions, methods, classes)
- Fast execution (milliseconds)
- No external dependencies
- Primary focus in TDD

### Integration Tests
- Test component interactions
- May use real databases, APIs
- Slower but higher confidence

### Contract Tests
- Verify API contracts
- Test boundaries between services

## Triangulation

Strategy for discovering implementation:

1. Write first test with one example
2. Hard-code the result (make it green)
3. Write second test with different example
4. Generalize the implementation
5. Continue until pattern emerges

```python
# Test 1
def test_factorial_of_1():
    assert factorial(1) == 1

# Implementation (hard-coded)
def factorial(n):
    return 1

# Test 2 - Forces generalization
def test_factorial_of_2():
    assert factorial(2) == 2

# Implementation (still specific)
def factorial(n):
    if n == 1:
        return 1
    return 2

# Test 3 - Forces real implementation
def test_factorial_of_3():
    assert factorial(3) == 6

# Real implementation emerges
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## Fake It Till You Make It

Implementation strategy:
1. Return a constant to make test pass
2. Gradually replace constants with real code
3. Let tests drive the implementation

## Obvious Implementation

When the solution is clear:
1. Write the test
2. Implement the obvious solution
3. If it fails, back up to triangulation

## Edge Case Testing

### Boundary Values
```python
def test_boundary_values():
    # Empty collections
    assert process([]) == []

    # Single element
    assert process([1]) == [1]

    # Maximum values
    assert process([sys.maxsize]) == expected

    # Zero
    assert process(0) == 0
```

### Error Conditions
```python
def test_invalid_input():
    with pytest.raises(ValueError):
        process(None)

    with pytest.raises(TypeError):
        process("not a number")
```

### Special Cases
- Null/None values
- Empty strings
- Negative numbers
- Unicode characters
- Very large inputs
- Concurrent access

## Test Data Management

### Test Data Builders
```python
class UserBuilder:
    def __init__(self):
        self.name = "Default User"
        self.email = "default@example.com"

    def with_name(self, name):
        self.name = name
        return self

    def with_email(self, email):
        self.email = email
        return self

    def build(self):
        return User(self.name, self.email)

# Usage
user = UserBuilder().with_name("Test").build()
```

### Object Mother Pattern
```python
class TestUsers:
    @staticmethod
    def admin():
        return User("admin", "admin@test.com", role="admin")

    @staticmethod
    def guest():
        return User("guest", "guest@test.com", role="guest")
```

## Parameterized Tests

Test multiple scenarios with same logic:

```python
@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
])
def test_factorial(input, expected):
    assert factorial(input) == expected
```

## Property-Based Testing

Generate test cases automatically:

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.integers(min_value=0, max_value=100))
def test_factorial_is_positive(n):
    assert factorial(n) > 0

@given(st.lists(st.integers()))
def test_sort_maintains_length(lst):
    assert len(sort(lst)) == len(lst)
```

## Mocking Patterns

### Stub for Queries
```python
def test_with_stub():
    # Stub returns predetermined value
    api = Mock()
    api.get_user.return_value = {"name": "Test"}

    service = UserService(api)
    result = service.get_username(1)

    assert result == "Test"
```

### Mock for Commands
```python
def test_with_mock():
    # Mock verifies interaction
    notifier = Mock()
    service = OrderService(notifier)

    service.complete_order(order)

    notifier.send_confirmation.assert_called_once_with(order)
```

### Spy Pattern
```python
def test_with_spy():
    real_service = RealService()
    spy = Mock(wraps=real_service)

    result = spy.process(data)

    # Still uses real implementation
    assert result == expected
    # But can verify calls
    spy.process.assert_called_once()
```

## Async Testing

### Python (pytest-asyncio)
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await fetch_data()
    assert result == expected
```

### JavaScript (Jest)
```javascript
test('async operation', async () => {
    const result = await fetchData();
    expect(result).toEqual(expected);
});
```

## Test Organization

### File Structure
```
tests/
  unit/
    test_calculator.py
    test_user_service.py
  integration/
    test_database.py
    test_api.py
  fixtures/
    conftest.py
    test_data.py
```

### Test Categories
- **Smoke tests**: Quick sanity checks
- **Regression tests**: Prevent bug recurrence
- **Performance tests**: Speed/resource usage

## Continuous Integration Practices

### Fast Feedback
- Run unit tests first (<5 min)
- Integration tests in parallel
- Fail fast on test failures

### Test Stability
- Fix flaky tests immediately
- Use deterministic test data
- Control time-dependent tests

### Test Reporting
- Clear failure messages
- Code coverage reports
- Trend analysis
