# TDD Methodology Reference

## The Three Laws of TDD (Uncle Bob)

Robert C. Martin's Three Laws define the fundamental discipline of TDD:

1. **Do not write production code unless it is to make a failing unit test pass**
2. **Do not write more of a unit test than is sufficient to fail (compilation failures are failures)**
3. **Do not write more production code than is sufficient to pass the one failing unit test**

These laws promote line-by-line granularity and maintain constant forward momentum.

## Red-Green-Refactor Cycle

### Red Phase
- Write a small, focused test that fails
- Target: 3-5 lines of test code maximum
- Test should fail for the right reason (not syntax errors)
- Duration: ~30 seconds

### Green Phase
- Write the minimum code to make the test pass
- "Quick and dirty" is acceptable - even hard-coded values
- Focus on making test green, not perfect code
- Duration: ~30 seconds to 1 minute

### Refactor Phase
- Clean up the code while tests remain green
- Remove duplication (DRY principle)
- Improve naming and readability
- Extract methods/classes if needed
- Apply design patterns where appropriate
- Duration: Variable, but keep it focused

### Cycle Timing
- One complete cycle: ~1-2 minutes
- 20-40 cycles per hour is normal
- Every few cycles, spend more time on refactoring
- Never skip the refactor phase

## TDD Cycle Levels

### Nano-cycle (Seconds)
The Three Laws of TDD - line-by-line development

### Micro-cycle (Minutes)
Red-Green-Refactor for each unit test

### Milli-cycle (10 Minutes)
Specific-to-Generic pattern:
- As tests become more specific, code becomes more generic
- Avoid over-engineering early

### Primary cycle (Hourly)
Architecture review:
- Check for architectural boundary crossings
- Ensure Clean Architecture principles
- Review overall system structure

## Arrange-Act-Assert (AAA) Pattern

Structure every test in three clear sections:

### Arrange
Set up the test conditions:
- Initialize objects
- Configure mocks/stubs
- Prepare test data

### Act
Execute the behavior under test:
- Call a single method/function
- Should be one line ideally

### Assert
Verify the expected outcome:
- Check return values
- Verify state changes
- Assert mock interactions

### Example Structure

```python
def test_calculate_total_with_tax():
    # Arrange
    calculator = PriceCalculator()
    price = 100.0
    tax_rate = 0.10

    # Act
    result = calculator.calculate_total(price, tax_rate)

    # Assert
    assert result == 110.0
```

## Given-When-Then (BDD Style)

Alternative pattern with behavior focus:

- **Given**: Initial context/preconditions
- **When**: Action/event occurs
- **Then**: Expected outcome

This pattern encourages thinking in terms of behavior rather than internal state.

## Test Quality Principles (MC-FIRE)

Good tests should be:

- **M**aintainable - Easy to update when requirements change
- **C**lear - Self-documenting with descriptive names
- **F**ocused - Test one thing only
- **I**solated - No dependencies on other tests
- **R**epeatable - Same result every time
- **E**xecutable - Fast to run

## Test Naming Conventions

Descriptive test names communicate intent:

### Pattern 1: should_expectedBehavior_when_stateUnderTest
```
should_return_zero_when_list_is_empty
should_throw_exception_when_input_is_null
```

### Pattern 2: methodName_stateUnderTest_expectedBehavior
```
calculateTotal_withNegativePrice_throwsException
getUser_withValidId_returnsUser
```

### Pattern 3: given_when_then
```
givenEmptyCart_whenCheckout_thenReturnsZero
givenValidUser_whenLogin_thenReturnsToken
```

## Common TDD Pitfalls to Avoid

### 1. Writing Tests After Code
- Defeats the design benefits of TDD
- Tests become verification, not specification

### 2. Tests Too Large
- Test multiple behaviors at once
- Difficult to identify failures

### 3. Skipping Refactoring
- Accumulates technical debt
- Code becomes unmaintainable

### 4. Over-mocking
- Tests become brittle
- Refactoring breaks test suites
- Use real objects when possible

### 5. Testing Implementation Details
- Tests should verify behavior, not internals
- Treat code under test as black box

### 6. Chasing 100% Coverage
- Coverage != quality
- Focus on meaningful coverage + mutation score
- Prioritize edge cases and critical paths

### 7. Getting Stuck (Local Optimum)
- Solution: Backtrack and delete recent tests
- Take a different approach
- Think about higher-level design

## Test Doubles (Mocks, Stubs, Fakes)

### When to Use Test Doubles
- External dependencies (databases, APIs)
- Slow operations
- Non-deterministic behavior
- Unavailable resources

### Types of Test Doubles
- **Stub**: Returns predetermined data
- **Mock**: Verifies interactions
- **Fake**: Working implementation (in-memory database)
- **Spy**: Records information about calls

### Best Practices
- Don't over-mock - test real integrations where possible
- Keep test doubles simple
- Verify behavior, not implementation

## Language-Specific Frameworks

### Python
- pytest (recommended)
- unittest (built-in)
- hypothesis (property-based testing)

### JavaScript/TypeScript
- Jest
- Mocha + Chai
- Vitest

### Java
- JUnit 5
- TestNG
- Mockito (mocking)

### Ruby
- RSpec (BDD-style)
- minitest

### C#/.NET
- xUnit
- NUnit
- MSTest

### Go
- testing (built-in)
- testify

## Metrics and Quality Indicators

### Code Coverage
- Statement coverage
- Branch coverage
- Path coverage
- Mutation score (more valuable)

### TDD Health Indicators
- Test-to-code ratio (typically 1:1 to 2:1)
- Test execution time
- Flaky test rate
- Defect escape rate

## RGRC Pattern (Red-Green-Refactor-Commit)

Extended workflow that adds commit step:
1. Red - Write failing test
2. Green - Make it pass
3. Refactor - Clean up
4. Commit - Save progress

Benefits:
- Frequent save points
- Easy to revert mistakes
- Clear commit history
- Encourages small, focused changes
