---
layout: default
title: Critical Code Reviewer
grand_parent: English
parent: Software Development
nav_order: 1
lang_peer: /ja/skills/dev/critical-code-reviewer/
permalink: /en/skills/dev/critical-code-reviewer/
---

# Critical Code Reviewer
{: .no_toc }

Multi-persona parallel code review from four expert perspectives.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-workflow">Workflow</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Critical Code Reviewer examines your source code through **four independent expert personas** running in parallel. Each persona focuses on a different quality dimension, producing a unified review report with severity-rated findings and actionable recommendations.

The four personas are:

| Persona | Focus | Key Question |
|:--------|:------|:-------------|
| **Veteran Engineer** (20 yr) | Design decisions, anti-patterns, long-term maintainability | "Can we maintain this in 5 years?" |
| **TDD Expert** | Testability, dependency management, refactoring safety | "Can we test this in isolation?" |
| **Clean Code Expert** | Naming, readability, SOLID principles | "Is this understandable at a glance?" |
| **Bug Hunter** | State transitions, exception paths, async races, dependency completeness | "Will this break in production?" |

## When to Use

- You want a **comprehensive code review** before merging a PR
- You need to **evaluate design quality** of existing code before refactoring
- You want to **hunt for production bugs** in state management, async logic, or error handling
- You are onboarding to an unfamiliar codebase and want a quality assessment
- You need a structured review report with severity ratings

## Prerequisites

- Claude Code installed and running
- The `critical-code-reviewer` skill copied to `~/.claude/skills/`
- Source files accessible in your working directory

No external API keys or services are required.

## How It Works

The review follows three phases:

```
Phase 1: Preparation
       |
  +---------+---------+---------+
  |         |         |         |
Veteran   TDD     Clean     Bug
Engineer  Expert  Code      Hunter
  |         |         |         |
  +---------+---------+---------+
       |
Phase 3: Integrated Report
```

### Phase 1: Preparation

Claude analyzes the review target before launching the personas:

- **Target identification** -- determines which files, directories, classes, or functions to review. For PR reviews, Claude scopes to the changed files automatically.
- **Language detection** -- detects the programming language(s) and activates language-specific checklists. Python and JavaScript/TypeScript receive additional checks (see [Language-Specific Checks](#language-specific-checks) below).
- **Dependency pre-scan** -- searches for in-function imports, checks them against `requirements.txt` or `pyproject.toml`, and flags missing or unused dependencies. This context is passed to the Bug Hunter persona.
- **Context gathering** -- if design documents, existing test suites, or related configuration files are present, Claude loads them so that each persona can reference project-specific conventions.

### Phase 2: Parallel Review

Four agents run **simultaneously** via the Agent tool, each with an inline persona prompt from `references/agents/*.md`. Each agent receives the target code and relevant reference materials. Agents output findings with **Impact** descriptions (not severity) — severity is assigned in Phase 3 using the authoritative `references/severity_criteria.md`. Because they run in parallel, total review time stays close to that of a single persona.

The skill is fully self-contained: all persona prompts are embedded in `references/agents/`, eliminating dependencies on external agent definitions.

### Phase 3: Integration

Claude collects all findings and post-processes them:

- **Deduplication** -- when multiple personas flag the same issue (e.g., both Bug Hunter and Veteran Engineer note a missing null check), Claude merges them into a single finding and records which personas contributed.
- **Severity assignment** -- each finding receives a severity level based on production impact (see table below).
- **Report generation** -- a structured Markdown report is produced using the bundled template (`assets/code_review_report_template.md`), including an executive summary, per-severity findings, persona-specific insights, and improvement recommendations.

### Severity Levels

| Severity | Definition | Example |
|:---------|:-----------|:--------|
| **Critical** | Bugs, data loss, or security issues | Missing null check, resource leak |
| **Major** | Significant maintainability or design problems | God class, untestable design |
| **Minor** | Recommended improvements, not urgent | Naming improvements, minor refactoring |
| **Info** | Best practice suggestions | Alternative approach proposals |

## Persona Deep Dive

Each persona applies a distinct lens to the code:

### Veteran Engineer (20 years experience)

Evaluates long-term sustainability and operational readiness. Checks include:

- Design pattern misuse and anti-patterns (God Object, Shotgun Surgery, Feature Envy)
- Coupling and cohesion balance across modules
- Operational concerns: logging, monitoring hooks, graceful degradation
- Backward compatibility and migration safety

### TDD Expert

Inspired by the "testing-first" philosophy. Checks include:

- Dependency injection readiness -- can collaborators be replaced with test doubles?
- Side-effect isolation -- do functions separate pure logic from I/O?
- Test boundary clarity -- are public APIs well-defined and mockable?
- Refactoring safety -- will existing tests survive structural changes?

### Clean Code Expert

Focuses on readability and structural clarity. Checks include:

- Naming accuracy -- do names reveal intent without comments?
- Function length and single responsibility
- SOLID principle adherence (especially SRP, OCP, DIP)
- Code duplication and abstraction opportunities

### Bug Hunter

Specializes in runtime failure modes. Checks include:

- **State transitions** -- cross-module state consistency, orphaned states
- **Exception paths** -- unhandled errors that leave resources open or state corrupted
- **Dependency completeness** -- imports vs. declared dependencies in manifest files
- **Async race conditions** -- shared mutable state, missing locks, unordered promise resolution

## Language-Specific Checks

### Python

| Check | What the personas look for |
|:------|:---------------------------|
| Type hints | Missing or incorrect type annotations, `Optional` misuse |
| Pythonic patterns | Opportunities for list comprehensions, context managers, generator expressions |
| Exception handling | Bare `except`, overly broad exception clauses, swallowed errors |
| Import hygiene | In-function imports, circular imports, missing `__init__.py` |

### JavaScript / TypeScript

| Check | What the personas look for |
|:------|:---------------------------|
| Type safety (TS) | Overuse of `any`, missing return types, incorrect generics |
| Async patterns | Unhandled promise rejections, sequential awaits that could be parallel |
| `this` binding | Arrow vs. regular function misuse in callbacks and class methods |
| Error propagation | Missing `.catch()` chains, error swallowing in try/catch |

## Usage Examples

### Example 1: Review a single file

```
Review this file critically: src/services/payment_processor.py
```

Claude will run all four personas against the file and produce a severity-rated report.

### Example 2: Review a PR diff

```
Do a critical code review of the changes in this PR.
Focus on the new authentication module.
```

Claude scopes the review to the changed files and highlights risks introduced by the diff.

### Example 3: Targeted bug hunting

```
Check src/workers/queue_handler.ts for async race conditions
and exception handling issues.
```

The Bug Hunter persona receives special emphasis, while other personas still contribute their findings.

### Example 4: Pre-refactoring assessment

```
I'm about to refactor the data pipeline in src/etl/.
Run a critical code review so I know what to fix first.
```

Claude reviews all files in the directory, ranks issues by severity, and highlights which problems should be addressed before or during the refactoring effort.

## Troubleshooting

### Personas return shallow findings on large files

**Symptom**: When reviewing files over 500 lines, some personas produce only surface-level observations.

**Solution**: Split the review by specifying classes or functions individually (e.g., "Review the `PaymentProcessor` class in `checkout.py`"). Smaller, focused targets give each persona more room to analyze deeply.

### Language-specific checks not applied

**Symptom**: Python or TypeScript-specific findings (type hints, async patterns) are missing from the report.

**Solution**: Explicitly mention the language in your prompt: "Review this **Python** file critically." Claude relies on file extensions and content heuristics; naming the language ensures the specialized checklists activate.

### Duplicate findings across personas

**Symptom**: The integrated report still contains near-duplicate items from different personas.

**Solution**: This can happen when findings are similar but framed differently. Ask Claude to "merge overlapping findings" in a follow-up prompt, or request a condensed report with `--concise` style instructions.

## Tips & Best Practices

- **Scope the review** -- pointing Claude at specific files or directories produces more focused results than reviewing an entire repository at once.
- **Mention the language** if Claude does not detect it automatically -- this activates language-specific checks (Python, JavaScript/TypeScript).
- **Combine with tests** -- pair this skill with `tdd-developer` to first get a review, then write tests for the issues found.
- **Use severity to prioritize** -- fix Critical and Major issues before merge; Minor and Info items can go into a backlog.

## Related Skills

- [TDD Developer]({{ '/en/skills/dev/tdd-developer/' | relative_url }}) -- write tests for issues found during review
- [Data Scientist]({{ '/en/skills/dev/data-scientist/' | relative_url }}) -- data analysis and ML workflows
