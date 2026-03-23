---
name: hidden-contract-investigator
description: |
  既存コード・既存関数・既存モジュールの暗黙契約を抽出するスキル。
  戻り値型、副作用、例外、前提条件、境界条件、環境依存挙動を確認し、
  reuse前のリスクを可視化する。名前やコメントではなく実際の挙動から
  契約を読み取り、不一致を分類し、再利用可否を判定する。
  Use when reusing legacy code, verifying actual behavior of existing
  functions, or extracting implicit contracts before implementation.
  Covers: hidden contract, implicit contract, reuse risk, legacy behavior, 暗黙契約, 既存資産調査.
  Analyzes return types, side effects, exceptions, preconditions,
  boundary conditions, and environment-dependent behavior.
---

# Hidden Contract Investigator

## Overview

A skill for extracting **implicit contracts** from existing code before reuse. Instead of trusting function names, comments, or type annotations at face value, this skill systematically uncovers the actual behavioral contracts embedded in code: what a function really returns, what side effects it triggers, what hidden preconditions it assumes, and how it behaves across different environments.

The root motivation: many production defects originate not from new code bugs, but from **misunderstanding the actual behavior of reused code**. A function named `keepTwoDecimal()` that returns a comma-formatted string instead of a numeric value, a variable that shadows another in a different scope, a utility that silently depends on production-only configuration -- these hidden contracts are the real source of integration failures.

**Scope Boundary**: This skill focuses on pre-implementation investigation of existing code assets. For reviewing already-written code, use `critical-code-reviewer`. For post-incident root cause analysis, use `incident-rca-specialist`.

## When to Use

- Reusing existing functions/modules/services in new feature implementation
- Working with legacy code where names and comments may be unreliable
- Investigating actual return types, side effects, and exception paths before integration
- Assessing whether an existing code asset is safe to reuse as-is
- Preparing contract tests for critical integration points
- Onboarding onto an unfamiliar codebase and need to understand actual behavior
- Post-RCA follow-up: hardening reuse patterns that caused incidents

## Prerequisites

- **Target code available**: Source code of the reuse candidate must be readable
- **Caller context identified**: Know which new feature or module will consume the reused code
- **Related artifacts accessible**: Tests, bug tickets, and caller code provide critical evidence
- **No active incident**: This is a pre-implementation investigation skill, not incident response

## Inputs

- Target code (function, class, module, or service boundary)
- Caller code or planned integration point
- Type definitions / interface definitions (if any)
- Existing test code covering the target
- Bug tickets or RCA reports related to the target (if available)

## Outputs

1. **Implicit Contract Sheet** -- documented actual contracts vs. stated contracts (includes Mismatch List as the "Risk" and "Observed contract" columns per entry in `assets/implicit_contract_sheet_template.md`)
2. **Reuse Risk Register** -- risk assessment for each reuse candidate
3. **Contract Verification Test Ideas** -- test designs to lock down critical contracts
4. **Adoption Recommendation** -- reuse decision with guardrails and prerequisites

## Workflows

### Workflow 1: Target Identification (対象特定)

Define the investigation boundary and scope.

1. Identify reuse candidates at the appropriate granularity:
   - **Single function**: utility, formatter, calculator, validator
   - **Class / module**: a cohesive unit with internal state
   - **Screen flow**: a UI workflow with multiple state transitions
   - **Service boundary**: an API or microservice with request/response contracts
   - **DB persistence boundary**: ORM models, repositories, migration scripts
   - **External API / library call**: third-party dependencies with version-sensitive behavior
2. For each candidate, document:
   - Where it lives (file, module, package)
   - Who currently calls it (known consumers)
   - When it was last modified (staleness risk)
   - Whether tests exist (coverage signal)
3. Prioritize investigation order by:
   - Criticality to the new feature (high-impact reuse first)
   - Complexity of the target (more complex = more hidden contracts)
   - Staleness and lack of documentation (higher risk of drift)

### Workflow 2: Surface Contract Recording (見た目の契約記録)

Record what the code **appears** to promise -- without yet verifying it.

1. Capture the **name-implied contract**: what the function/method name suggests it does
2. Capture the **documented contract**: docstrings, comments, README mentions, API docs
3. Capture the **type-declared contract**: type annotations, interface definitions, schema files
4. Capture the **caller-assumed contract**: how existing callers use the return value, what they pass in
5. Record all of these in the Implicit Contract Sheet using `assets/implicit_contract_sheet_template.md`
6. **Mark everything as UNVERIFIED** at this stage -- trust nothing yet

### Workflow 3: Actual Contract Extraction (実際の契約抽出)

Read the actual implementation to discover the real behavioral contract.

> Load `references/contract_extraction_guide.md` for the extraction methodology and priority order.

1. **Return value analysis**:
   - Actual return type (not just annotation -- trace the code path)
   - Value formatting (does it add commas, currency symbols, units?)
   - Null/empty/undefined handling (what happens on edge inputs?)
   - Multiple return paths (does it return different types on different branches?)
2. **Side effect discovery**:
   - Database writes, cache updates, file system operations
   - Event emission, message queue publishing, webhook calls
   - Global/module state mutation
   - Logging with sensitive data
3. **Hidden precondition identification**:
   - Implicit ordering requirements (must call A before B)
   - Required initialization state (singleton must be configured first)
   - Assumed input constraints not enforced by validation
   - Environment variable dependencies
4. **Exception path mapping**:
   - Which exceptions are thrown vs. caught and swallowed
   - Error return values vs. exception throwing (mixed patterns)
   - Retry behavior (does it retry internally? how many times?)
5. **Environment-dependent behavior**:
   > Load `references/environment_behavior_guide.md` for environment boundary patterns
   - Configuration-driven branching (dev vs. prod behavior)
   - Database dialect differences (SQLite vs. PostgreSQL)
   - Timezone-sensitive operations
   - Locale-dependent formatting

### Workflow 4: Mismatch Classification (不一致分類)

Compare surface contracts (Workflow 2) against actual contracts (Workflow 3) and classify every discrepancy.

> Load `references/hidden_spec_patterns.md` for the full pattern catalog.

Classify each mismatch into one or more of these 6 categories:

| Category | Description | Example |
|----------|-------------|---------|
| **Naming Mismatch** | Function/variable name implies different behavior than actual | `keepTwoDecimal()` returns comma-formatted string |
| **Type Mismatch** | Return type or parameter type differs from expectation | Annotated as `float`, actually returns `str` |
| **Scope Mismatch** | Same-named identifiers exist in different scopes | `config` in module scope vs. `config` in function scope |
| **State Dependency** | Behavior depends on external mutable state | Result changes based on global cache content |
| **Environment Dependency** | Behavior varies across environments | Works in dev (SQLite), fails in prod (PostgreSQL) |
| **Hidden Side Effect** | Undocumented writes, mutations, or event emissions | `calculate_total()` also updates a database record |

For each mismatch:
1. Rate **severity**: Critical / High / Medium / Low
2. Rate **likelihood of triggering**: High / Medium / Low
3. Identify the **blast radius**: what breaks if this mismatch causes a defect
4. Document the **evidence**: specific code lines, test results, or observations

### Workflow 5: Reuse Feasibility Judgment (再利用可否判定)

Determine whether each target can be safely reused and under what conditions.

> Load `references/reuse_risk_classification.md` for the full classification framework.

Apply the 5-level reuse classification:

| Level | Verdict | Meaning | Action Required |
|-------|---------|---------|-----------------|
| **A** | Reuse as-is | Contracts match, behavior verified | Add contract test only |
| **B** | Reuse with wrapper | Core behavior is correct but interface needs adaptation | Build thin wrapper, add contract test |
| **C** | Reuse with adapter | Significant interface mismatch but logic is sound | Build adapter layer, add integration test |
| **D** | Contract test required first | Behavior is uncertain, need verification before deciding | Write contract tests, then re-evaluate |
| **E** | Do not reuse / redesign | Fundamental mismatch or unacceptable risk | Redesign or implement from scratch |

For each reuse candidate:
1. Assign a reuse level (A-E)
2. Document the rationale with evidence from Workflow 4
3. Specify guardrails: what callers must do (or never do) to use safely
4. Identify naming improvements if the current name is misleading
5. Record results in `assets/reuse_risk_register_template.md` and `assets/adoption_recommendation_template.md`

### Workflow 6: Verification Design (検証設計)

Design contract tests and verification strategies for critical implicit contracts.

> Load `references/runtime_boundary_checklist.md` for boundary-specific test patterns.

1. For each critical mismatch from Workflow 4, design a minimal contract test:
   - **What to verify**: the specific contract (return type, side effect absence, etc.)
   - **Minimal test case**: simplest possible test that would catch a contract violation
   - **Boundary data sets**: edge cases and environment-sensitive inputs
   - **Failure signal**: what a test failure means (which contract broke)
   - **Regression value**: how this test prevents future incidents
2. Prioritize tests by:
   - Severity of the mismatch (Critical/High first)
   - Blast radius of a contract violation
   - Ease of test implementation
3. Design environment-boundary tests for any Environment Dependency mismatches:
   - DB dialect tests (SQLite vs. PostgreSQL behavior)
   - Timezone tests (naive vs. aware datetime handling)
   - Serialization round-trip tests (JSON, pickle, protobuf)
4. Record all test ideas in `assets/contract_test_idea_template.md`
5. Connect each test back to the mismatch it guards against (traceability)

## Resources

| Resource | Type | Purpose | When to Load |
|----------|------|---------|--------------|
| `references/contract_extraction_guide.md` | Reference | Extraction methodology, evidence priority, behavior-first approach | Workflow 3 |
| `references/hidden_spec_patterns.md` | Reference | Full catalog of mismatch patterns with examples | Workflow 4 |
| `references/runtime_boundary_checklist.md` | Reference | Boundary-specific checklists for DB, serialization, timezone, retry, locale | Workflow 6 |
| `references/reuse_risk_classification.md` | Reference | 5-level reuse classification framework and decision criteria | Workflow 5 |
| `references/environment_behavior_guide.md` | Reference | Environment-dependent behavior patterns and verification strategies | Workflow 3, 6 |
| `assets/implicit_contract_sheet_template.md` | Template | Document stated vs. observed contracts with evidence | Workflow 2, 3 |
| `assets/reuse_risk_register_template.md` | Template | Risk register for reuse candidates | Workflow 5 |
| `assets/contract_test_idea_template.md` | Template | Contract test designs with data sets and failure signals | Workflow 6 |
| `assets/adoption_recommendation_template.md` | Template | Final reuse decision with guardrails and prerequisites | Workflow 5 |

## Best Practices

### Behavior Over Documentation

- **Never trust names alone**: `formatCurrency()` might truncate, `isValid()` might have side effects, `getUser()` might return cached stale data
- **Never trust comments alone**: comments drift from code; the implementation is the only source of truth
- **Read callers before comments**: how existing callers use a function reveals the actual contract more reliably than what the docstring claims
- **Read tests before code**: test assertions encode verified behavior; passing tests are machine-checked contracts

### Evidence Hierarchy

When extracting contracts, prioritize evidence sources in this order:

1. **Passing test assertions** (machine-verified behavior)
2. **Caller usage patterns** (real-world consumption reveals actual contracts)
3. **Implementation code** (the authoritative behavioral specification)
4. **Bug tickets and RCA reports** (documented contract violations)
5. **Type annotations** (may be outdated or incomplete)
6. **Comments and docstrings** (lowest priority; most likely to drift)

### Systematic Boundary Awareness

- Every time data crosses a boundary (function, module, service, DB, serialization), contracts can shift
- Pay special attention to: type coercion at boundaries, timezone handling at persistence layers, encoding changes at serialization points
- The most dangerous hidden contracts live at boundaries, not inside pure logic

### Mismatch Taxonomy Discipline

- Always classify mismatches using the 6-category taxonomy -- do not use vague labels like "bug" or "issue"
- A single finding may belong to multiple categories (e.g., both Naming Mismatch and Type Mismatch)
- Rate severity and likelihood independently -- a low-likelihood Critical mismatch still needs a contract test

### Connect to Prevention

- Every critical mismatch should produce at least one contract test idea
- Contract tests are not unit tests -- they verify the **interface promise**, not the internal logic
- Name tests after the contract they protect: `test_keepTwoDecimal_returns_numeric_not_string`
- Contract tests are the skill's primary deliverable for long-term value
