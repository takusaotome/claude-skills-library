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

<span class="badge badge-free">No API Required</span> <span class="badge badge-workflow">Workflow</span>

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

1. **Preparation** -- Claude identifies target files, detects programming languages, and enables language-specific checks (Python type hints, JS/TS async patterns, etc.).
2. **Parallel Review** -- Four sub-agents run simultaneously, each applying their persona's checklist to the code.
3. **Integration** -- Results are deduplicated, assigned severity levels (Critical / Major / Minor / Info), and merged into a single structured report.

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

### Severity Levels

| Severity | Definition | Example |
|:---------|:-----------|:--------|
| **Critical** | Bugs, data loss, or security issues | Missing null check, resource leak |
| **Major** | Significant maintainability or design problems | God class, untestable design |
| **Minor** | Recommended improvements, not urgent | Naming improvements, minor refactoring |
| **Info** | Best practice suggestions | Alternative approach proposals |

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

## Tips & Best Practices

- **Scope the review** -- pointing Claude at specific files or directories produces more focused results than reviewing an entire repository at once.
- **Mention the language** if Claude does not detect it automatically -- this activates language-specific checks (Python, JavaScript/TypeScript).
- **Combine with tests** -- pair this skill with `tdd-developer` to first get a review, then write tests for the issues found.
- **Use severity to prioritize** -- fix Critical and Major issues before merge; Minor and Info items can go into a backlog.

## Related Skills

- [TDD Developer]({{ '/en/skills/dev/tdd-developer/' | relative_url }}) -- write tests for issues found during review
- [Data Scientist]({{ '/en/skills/dev/data-scientist/' | relative_url }}) -- data analysis and ML workflows
