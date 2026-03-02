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

<span class="badge badge-free">No API Required</span> <span class="badge badge-workflow">Workflow</span>

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

### Full Workflow

1. **Understand Requirements** -- Claude helps break down the feature into small, testable behaviors and identify edge cases.
2. **Plan Test Cases** -- Create a prioritized list of test cases before writing any code.
3. **Execute Cycles** -- Work through each test case using Red-Green-Refactor.
4. **Review** -- After all behaviors are implemented, review overall design and architecture.

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
