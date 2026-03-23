# Contract Extraction Guide

## Purpose

This guide defines the methodology for extracting actual behavioral contracts from existing code. The core principle is **behavior-first, not comment-first**: always prioritize what the code actually does over what documentation claims it does.

## Evidence Priority Order

When investigating implicit contracts, gather evidence from the following sources in priority order. Higher-priority sources override lower-priority sources when they conflict.

### Priority 1: Passing Test Assertions

Test assertions are machine-verified behavioral contracts. A passing test that asserts `assertEqual(result, "1,234.56")` tells you more about the actual contract than any docstring.

**What to look for:**
- Assertion patterns: what types and values are expected
- Edge case coverage: what boundary conditions are tested
- Setup/teardown: what preconditions the test requires (these are implicit contracts too)
- Mocking boundaries: what is mocked reveals which dependencies are real contracts
- Missing tests: absence of tests for a code path means that contract is unverified

**Extraction technique:**
```
1. Find all test files that reference the target function/class
2. Read each test's assertions to infer the behavioral contract
3. Note what the test mocks -- mocked dependencies are contract boundaries
4. Check parameterized tests for the range of expected inputs/outputs
5. Check for negative tests (expected exceptions, error handling)
```

### Priority 2: Caller Usage Patterns

How existing callers consume the function reveals the real-world contract. If every caller wraps the return value in `str()`, the actual contract may differ from the declared type.

**What to look for:**
- How callers handle the return value (type casting, null checks, error handling)
- What callers pass as arguments (reveals valid input ranges)
- Whether callers use the function in sequence with other calls (ordering contract)
- Whether callers duplicate or workaround behavior (suggests known contract gaps)
- Whether multiple callers use the function differently (reveals ambiguous contracts)

**Extraction technique:**
```
1. Search for all call sites of the target function
2. For each call site, document how the return value is consumed
3. Check if callers add defensive code (null checks, type guards, try/catch)
4. Identify callers that transform the output -- this reveals contract gaps
5. Note if any callers have comments explaining "why" they call this way
```

### Priority 3: Implementation Code

The implementation is the authoritative behavioral specification. Read it line by line, focusing on what the code **does**, not what surrounding comments say.

**What to look for:**
- All `return` statements (different branches may return different types)
- All mutation operations (database writes, file operations, global state changes)
- Conditional branches that change behavior (environment checks, feature flags)
- Error handling patterns (throw vs. return null vs. return error object)
- Internal function calls (transitive dependencies are hidden contracts)

**Extraction technique:**
```
1. Trace every execution path from entry to exit
2. For each path, document: return type, return value shape, side effects
3. Identify all branch conditions that change behavior
4. List all external dependencies accessed during execution
5. Map the exception hierarchy: what is caught, what propagates
```

### Priority 4: Bug Tickets and RCA Reports

Past incidents document contract violations that actually caused harm. These are extremely valuable because they reveal which hidden contracts are dangerous in practice.

**What to look for:**
- The exact contract that was violated (e.g., "assumed numeric return, got string")
- The blast radius of the violation (how many systems were affected)
- Whether the fix addressed the root cause or just the symptom
- Whether the same kind of violation recurred (pattern indicator)

### Priority 5: Type Annotations

Type annotations provide useful hints but must be verified against implementation. Annotations can be outdated, incomplete, or intentionally loose (e.g., `Any`).

**Common annotation traps:**
- `Optional[str]` that never actually returns `None` (overly defensive annotation)
- `float` annotation on a function that returns `str` (annotation drift)
- `dict` without key/value type detail (hides internal structure contract)
- Union types that suggest flexibility but only one branch is ever used
- `Any` used as a shortcut that masks the real contract

### Priority 6: Comments and Docstrings

Comments are the lowest-priority evidence source. They are useful for understanding intent but must never be trusted as behavioral specifications.

**Common comment traps:**
- Comment says "returns X" but code returns Y (comment drift)
- TODO comments that were never addressed (promises never fulfilled)
- Docstring documents the original design, not the current behavior
- Copy-pasted comments from similar functions that don't apply
- Comments explaining workarounds for bugs that have since been fixed

## Behavior-First Extraction Checklist

For each target function/method, systematically extract:

### Return Value Contract
- [ ] What type is actually returned? (trace all return paths)
- [ ] Is the return value formatted? (commas, currency, padding)
- [ ] What is returned for null/empty/invalid input?
- [ ] Can different code paths return different types?
- [ ] Is the return value a reference to mutable internal state?

### Side Effect Contract
- [ ] Does it write to a database, file, or external service?
- [ ] Does it modify global or module-level state?
- [ ] Does it emit events, publish messages, or trigger webhooks?
- [ ] Does it modify its input arguments (mutable reference mutation)?
- [ ] Does it log sensitive data as a side effect?

### Precondition Contract
- [ ] What must be true before calling this function?
- [ ] Are there initialization requirements (singletons, connections)?
- [ ] Are there ordering requirements (must call X before Y)?
- [ ] What environment variables or configuration must exist?
- [ ] What import-time side effects does the module have?

### Exception Contract
- [ ] What exceptions can be thrown?
- [ ] Which exceptions are caught internally vs. propagated?
- [ ] Does the function mix exception throwing with error return values?
- [ ] Are there retry mechanisms that mask transient failures?
- [ ] What happens when a dependency fails (network, DB, file system)?

### Dependency Contract
- [ ] What external services does it depend on?
- [ ] What internal modules does it import and use?
- [ ] Are dependencies injected or hard-coded?
- [ ] Do dependencies have their own hidden contracts?
- [ ] Are there circular dependency risks?

## When to Stop Extraction

Extraction is complete when:
1. All return paths have been traced and documented
2. All side effects have been identified
3. All preconditions have been identified
4. The evidence priority has been applied (higher sources override lower ones)
5. Every finding has been recorded in the Implicit Contract Sheet

Do not pursue exhaustive coverage of irrelevant paths. Focus extraction effort on the code paths that the new feature will actually exercise.
