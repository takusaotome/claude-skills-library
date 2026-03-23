---
layout: default
title: TDD Developer
grand_parent: English
parent: Software Development
nav_order: 2
lang_peer: /ja/skills/dev/tdd-developer/
permalink: /en/skills/dev/tdd-developer/
---

# TDD Developer
{: .no_toc }

Guided Test-Driven Development with the Red-Green-Refactor cycle.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/tdd-developer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/tdd-developer){: .btn .fs-5 .mb-4 .mb-md-0 }
<span class="badge badge-workflow">Workflow</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

TDD Developer guides you through disciplined Test-Driven Development. Instead of writing code first and adding tests later, Claude follows the **Red-Green-Refactor** cycle: write a failing test, implement the minimum code to pass, then refactor while keeping tests green. This produces cleaner designs, higher code quality, and fewer defects.

The skill supports multiple languages and test frameworks including pytest, Jest, Vitest, JUnit 5, RSpec, Go testing, and xUnit.

## When to Use

- You want to **develop a new feature using TDD** from scratch
- You are **refactoring legacy code** and need test coverage first
- You need to implement **complex business logic** where correctness is critical
- You want to **learn TDD methodology** with guided examples
- You explicitly request test-first development

## Prerequisites

- Claude Code installed and running
- The `tdd-developer` skill copied to `~/.claude/skills/`
- A test framework installed for your language (e.g., `pytest` for Python, `jest` for JS/TS)

No external API keys or services are required.

## How It Works

### The Red-Green-Refactor Cycle

Each feature is built through repeated short cycles:

1. **RED** -- Write a small, focused test that fails. Confirm it fails for the right reason (not a syntax error).
2. **GREEN** -- Write the minimum code to make the test pass. Hard-coded values are acceptable at this stage.
3. **REFACTOR** -- Improve the code (remove duplication, improve naming, simplify logic) while keeping all tests green.
4. **COMMIT** (optional) -- Commit after each successful cycle for a clean history.

```
  RED           GREEN         REFACTOR
 Write         Write min      Improve
 failing  -->  code to   -->  code,
 test          pass           tests stay
                              green
      \__________________________/
               Repeat
```

### The Three Laws of TDD

These laws define the discipline that keeps cycles tight:

1. **You shall not write production code unless you have a failing test.** No implementation without a test that demands it.
2. **You shall not write more of a test than is sufficient to fail.** A compile error counts as a failure -- stop as soon as the test fails.
3. **You shall not write more production code than is sufficient to pass the currently failing test.** Resist the urge to add extra logic.

Following these laws naturally produces short cycles (1-2 minutes each) and ensures every line of production code is covered by a test.

### Full Workflow

1. **Understand Requirements** -- Claude helps break down the feature into small, testable behaviors and identify edge cases. Claude asks clarifying questions such as "What should happen when input is invalid?" or "Are there boundary values to consider?".
2. **Plan Test Cases** -- Create a prioritized list of test cases before writing any code. Edge cases (empty collections, null values, boundary values) are identified upfront.
3. **Execute Cycles** -- Work through each test case using Red-Green-Refactor. Claude runs the tests at every step to confirm red/green status.
4. **Review** -- After all behaviors are implemented, review overall design and architecture.

## Implementation Strategies

When transitioning from RED to GREEN, Claude selects the most appropriate strategy:

### Triangulation

Use when the correct implementation is not immediately obvious:

1. Write a first test and hard-code the return value to pass.
2. Add a second test with different data that forces the hard-coded value to break.
3. Generalize the implementation to handle both cases.
4. Continue adding examples until the general algorithm emerges.

This is the safest strategy for complex logic because it builds the solution incrementally from concrete examples.

### Fake It Till You Make It

Use when you want fast feedback:

1. Return a constant to pass the first test immediately.
2. Gradually replace constants with variables and expressions as new tests arrive.
3. Let the accumulation of tests drive the real implementation organically.

This strategy keeps cycles extremely short and avoids over-engineering.

### Obvious Implementation

Use when the solution is straightforward:

1. Write the test.
2. Implement the real logic directly (no faking).
3. If the test unexpectedly fails, fall back to Triangulation for a more cautious approach.

Choose this when the mapping from test to implementation is clear and unlikely to have edge cases.

## Usage Examples

### Example 1: Build a feature with TDD

```
Create a function to validate email addresses using TDD.
It should handle missing @, missing domain, empty strings, and null values.
```

Claude will plan test cases, then walk through each Red-Green-Refactor cycle, running tests at every step.

### Example 2: Add test coverage to existing code

```
I have this PriceCalculator class. Help me add TDD-style tests
and refactor it to be more testable.
```

Claude writes tests for existing behavior first, then helps refactor while keeping tests green.

### Example 3: TDD with a specific framework

```
Use TDD with pytest to implement a shopping cart module.
Start with adding items, then quantities, then discount logic.
```

Claude uses the specified framework and builds up functionality incrementally through test cycles.

### Example 4: TDD for bug reproduction

```
There's a bug where duplicate orders are created when
the user double-clicks submit. Write a failing test first
that reproduces this, then fix it.
```

Claude writes a test that demonstrates the race condition, confirms it fails, then implements the fix while keeping the test green.

## Troubleshooting

### Tests pass but Claude skips the Refactor step

**Symptom**: Claude writes the test (RED), makes it pass (GREEN), then immediately moves to the next test without refactoring.

**Solution**: Explicitly ask Claude to "refactor before moving on" or say "follow strict Red-Green-Refactor." You can also remind Claude to check for duplication between the current implementation and previous code before proceeding.

### Cycles are too large and take too long

**Symptom**: A single Red-Green-Refactor cycle spans many files or takes more than a few minutes.

**Solution**: Break the behavior into smaller pieces. Instead of "implement the full authentication flow," start with "validate that a username is non-empty." Each cycle should involve one small, focused test. If the GREEN step requires more than a few lines, the test is probably too ambitious.

### Test framework not detected

**Symptom**: Claude writes tests using the wrong framework or syntax (e.g., `unittest` instead of `pytest`).

**Solution**: Specify the framework in your prompt: "Use TDD **with pytest**" or "Use TDD **with Jest**." If your project has an existing test suite, point Claude to an existing test file so it can match conventions.

## Tips & Best Practices

- **Keep cycles short** -- aim for 1-2 minutes per Red-Green-Refactor cycle. If a cycle takes longer, break the test into a smaller behavior.
- **Test behavior, not implementation** -- assert on outputs and side effects, not on internal structure. This keeps tests resilient to refactoring.
- **Use the Arrange-Act-Assert pattern** -- structure each test clearly with setup, execution, and verification sections.
- **Don't skip refactoring** -- the Refactor step is where design improvement happens. Skipping it leads to technical debt.
- **Avoid over-mocking** -- excessive mocks make tests brittle and tightly coupled to implementation.
- **Use parameterized tests** for similar test cases with different input values.

### Common Pitfalls to Avoid

| Pitfall | Why It's a Problem |
|:--------|:-------------------|
| Writing tests after code | Defeats the TDD design benefit |
| Chasing 100% coverage | Focus on meaningful coverage instead |
| Testing implementation details | Tests break on refactoring |
| Writing large tests | Hard to pinpoint failures |
| Skipping the refactor step | Accumulates technical debt |

## Related Skills

- [Critical Code Reviewer]({{ '/en/skills/dev/critical-code-reviewer/' | relative_url }}) -- review code quality after TDD implementation
- [Data Scientist]({{ '/en/skills/dev/data-scientist/' | relative_url }}) -- data analysis and ML workflows
