---
name: tdd-developer
description: This skill should be used when developing code using Test-Driven Development (TDD) methodology. Use this skill when the user wants to write tests first before implementation, needs guidance on the red-green-refactor cycle, or explicitly requests TDD-style development. Triggers include requests like "develop this feature using TDD", "write tests first", "help me with test-driven development", or "implement this following TDD practices". The skill guides through writing failing tests, implementing minimal code to pass, and refactoring while maintaining test coverage.
---

# TDD Developer

## Overview

This skill provides comprehensive guidance for Test-Driven Development, a methodology where tests are written before implementation code. TDD promotes better design, higher code quality, and fewer defects through the disciplined practice of the red-green-refactor cycle.

## When to Use This Skill

- User explicitly requests TDD or test-first development
- Building new features that require high reliability
- Refactoring legacy code with test coverage
- Implementing complex business logic
- Learning TDD methodology

## TDD Development Workflow

### Phase 1: Understand Requirements

Before writing any test:
1. Clarify the feature requirements with the user
2. Break down the feature into small, testable behaviors
3. Identify edge cases and error conditions
4. Create a list of test cases to implement

Ask clarifying questions such as:
- "What specific behavior should this function have?"
- "What should happen when input is invalid?"
- "Are there any edge cases to consider?"

### Phase 2: Red-Green-Refactor Cycles

For each test case, follow this cycle:

#### Step 1: RED - Write a Failing Test

1. Write a small, focused test (3-5 lines)
2. Use the Arrange-Act-Assert pattern:
   - **Arrange**: Set up test data and dependencies
   - **Act**: Execute the behavior under test
   - **Assert**: Verify the expected outcome
3. Run the test to confirm it fails
4. Verify it fails for the right reason (not syntax errors)

```python
def test_calculate_discount_for_premium_member():
    # Arrange
    calculator = PriceCalculator()
    member = Member(tier="premium")
    price = 100.0

    # Act
    result = calculator.calculate_discount(price, member)

    # Assert
    assert result == 20.0  # 20% discount
```

#### Step 2: GREEN - Make the Test Pass

1. Write the minimum code to pass the test
2. "Quick and dirty" is acceptable at this stage
3. Even hard-coded values are fine initially
4. Focus only on making the current test green

```python
def calculate_discount(self, price, member):
    if member.tier == "premium":
        return price * 0.20
    return 0
```

#### Step 3: REFACTOR - Improve the Code

1. Review the implementation for improvements
2. Apply refactoring techniques:
   - Remove duplication (DRY)
   - Extract methods/functions
   - Improve naming
   - Simplify logic
3. Run tests after each refactoring to ensure they still pass

```python
def calculate_discount(self, price, member):
    discount_rates = {
        "premium": 0.20,
        "gold": 0.15,
        "silver": 0.10,
        "standard": 0.05,
    }
    rate = discount_rates.get(member.tier, 0)
    return price * rate
```

#### Step 4: COMMIT (Optional RGRC Pattern)

After each successful cycle, commit the changes:
- Creates frequent save points
- Easy to revert if needed
- Clear commit history

### Phase 3: Iterate Until Complete

1. Select the next test case from the list
2. Repeat the red-green-refactor cycle
3. Continue until all behaviors are implemented
4. Review overall design and architecture

## Test Design Guidelines

### Test Naming

Use descriptive names that communicate intent:
- `should_return_zero_when_list_is_empty`
- `givenPremiumMember_whenCalculateDiscount_thenReturns20Percent`
- `createUser_withValidInput_savesToDatabase`

### Test Structure

Each test should:
- Test one behavior only
- Be independent from other tests
- Be deterministic (same result every run)
- Execute quickly

### Edge Cases to Cover

Always consider:
- Empty collections
- Null/None values
- Boundary values (0, -1, max)
- Invalid inputs
- Error conditions

### Parameterized Tests

For similar test cases with different values:

```python
@pytest.mark.parametrize("tier,expected_rate", [
    ("premium", 0.20),
    ("gold", 0.15),
    ("silver", 0.10),
    ("standard", 0.05),
])
def test_discount_rates(tier, expected_rate):
    member = Member(tier=tier)
    result = calculator.calculate_discount(100, member)
    assert result == expected_rate * 100
```

## Implementation Strategies

### Triangulation

When implementation is unclear:
1. Start with one example, hard-code the result
2. Add second example that forces generalization
3. Continue until the pattern emerges

### Fake It Till You Make It

1. Return constants to pass tests quickly
2. Gradually replace with real implementation
3. Let tests drive the design

### Obvious Implementation

When solution is clear:
1. Implement directly
2. If it fails, fall back to triangulation

## Test Framework Selection

Select the appropriate framework based on language:

- **Python**: pytest (recommended), unittest
- **JavaScript/TypeScript**: Jest, Vitest
- **Java**: JUnit 5, TestNG
- **Ruby**: RSpec, minitest
- **Go**: testing (built-in)
- **C#**: xUnit, NUnit

## Quality Principles

### Avoid Common Pitfalls

1. **Don't write tests after code** - Defeats TDD purpose
2. **Don't skip refactoring** - Accumulates technical debt
3. **Don't over-mock** - Tests become brittle
4. **Don't test implementation details** - Test behavior instead
5. **Don't chase 100% coverage** - Focus on meaningful coverage

### Test Quality Indicators

- Tests run fast (<1 second per test)
- No flaky tests
- Clear failure messages
- Test-to-code ratio around 1:1

## Resources

### References

For detailed methodology and patterns, load these reference files as needed:

- **`references/tdd_methodology.md`**: Complete TDD methodology including the Three Laws of TDD, Red-Green-Refactor cycle details, cycle timing, and common pitfalls to avoid

- **`references/test_patterns.md`**: Test patterns and techniques including triangulation, parameterized tests, test data builders, mocking patterns, and async testing

### When to Load References

Load `tdd_methodology.md` when:
- User asks about TDD principles or best practices
- Need to explain the Three Laws or cycle timing
- Addressing questions about test quality or metrics

Load `test_patterns.md` when:
- User needs specific test patterns (builders, mocking)
- Implementing parameterized or property-based tests
- Dealing with async testing scenarios

## Example TDD Session

User request: "Create a function to validate email addresses using TDD"

### Step 1: Plan Test Cases

```
Test cases for email validation:
1. Valid email returns true
2. Missing @ returns false
3. Missing domain returns false
4. Missing local part returns false
5. Multiple @ symbols returns false
6. Empty string returns false
7. None/null returns false
```

### Step 2: First Cycle - Valid Email

**RED:**
```python
def test_valid_email_returns_true():
    result = validate_email("user@example.com")
    assert result is True
```

**GREEN:**
```python
def validate_email(email):
    return True  # Minimal implementation
```

**REFACTOR:** No changes needed yet.

### Step 3: Second Cycle - Missing @

**RED:**
```python
def test_missing_at_symbol_returns_false():
    result = validate_email("userexample.com")
    assert result is False
```

**GREEN:**
```python
def validate_email(email):
    return "@" in email
```

**REFACTOR:** Still simple, no changes needed.

### Step 4: Continue Cycles

Continue through remaining test cases, letting the implementation emerge from the tests. The final implementation will be well-tested and handle all edge cases.

## Summary

1. **Write test first** - Always before implementation
2. **Keep cycles short** - ~1-2 minutes per cycle
3. **Minimal code** - Just enough to pass
4. **Refactor always** - Never skip this step
5. **Test behavior** - Not implementation details
6. **Commit frequently** - After each green-refactor
