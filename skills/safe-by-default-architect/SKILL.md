---
name: safe-by-default-architect
description: |
  再発しやすい危険な実装パターンを、安全側に倒れる標準パターン・禁止事項・共通層・静的ルール候補へ
  変換するスキル。ORM強制、deny-by-default認可、サービス経由I/O、永続化確認後の成功表示などを設計する。
  レビューで危険コードを見つけるのではなく、危険コードを書きにくくする設計標準を作ることが目的。
  Use when turning repeated defect patterns into safe architectural defaults, forbidden-to-safe
  mapping tables, common layer designs, and enforceable static analysis rules.
---

# Safe By Default Architect

## Overview

This skill converts recurring dangerous implementation patterns into safe architectural defaults and enforceable standards. Rather than catching unsafe code during review, it designs the codebase so that **the safe way is the easy way** and the dangerous way requires deliberate effort.

The core philosophy: **If a developer can accidentally write dangerous code, the architecture has failed.**

**Scope Boundary**: This skill designs standards, abstractions, and rules. For reviewing existing code against those standards, use `critical-code-reviewer`. For investigating incidents caused by unsafe patterns, use `incident-rca-specialist`.

## When to Use

- Repeated defects of the same class appear across multiple PRs or services
- Raw SQL, opt-in authorization, or direct file path construction appears in controller/route layers
- No common service layer exists for cross-cutting concerns (auth, file I/O, datetime handling)
- You need to convert RCA findings into enforceable coding standards
- Static analysis rules (lint/semgrep/custom checks) need to be designed
- A "forbidden patterns" list needs to be paired with approved alternatives
- Architecture Decision Records need to codify safe defaults
- A new project or module needs safe-by-default foundations from day one

## Inputs

- RCA reports, bug tickets, or critical review findings
- Coding guidelines and architecture documents (if any)
- Technology stack information (language, framework, ORM, tooling)
- Static analysis / lint configuration (if any)
- Relevant code fragments showing dangerous patterns

## Outputs

1. **Safe Pattern Catalog** -- approved patterns per category with rationale
2. **Forbidden Pattern List** -- anti-patterns with danger classification and alternatives
3. **Common Layer Design** -- shared services and abstraction recommendations
4. **Static Rule Candidate List** -- lint/semgrep rule proposals with false positive assessment
5. **Exception Handling Rule** -- when and how to approve deviations
6. **Review Checklist Addendum** -- additions to existing code review checklists

## Prerequisites

- **Defect/RCA data available**: Bug reports, RCA findings, or review findings that reveal recurring unsafe patterns
- **Technology stack identified**: Language, framework, ORM, and tooling context
- **Existing standards accessible**: Current coding guidelines, lint configuration, and architecture documents (if any)
- **Stakeholder alignment**: Agreement that architectural enforcement is needed (not just documentation)

## Workflows

### Workflow 1: Recurring Pattern Aggregation (再発パターン集約)

Collect and consolidate recurring dangerous patterns from defect data.

1. Gather inputs: RCA reports, bug tickets, critical review findings, security scan results
2. Extract each distinct dangerous pattern with:
   - **Pattern name**: Short identifier (e.g., "raw-sql-concatenation")
   - **Frequency**: How often this pattern has caused issues
   - **Example code**: Representative code snippet from actual incidents
   - **Affected components**: Which modules, layers, or services are impacted
3. Deduplicate patterns that are variations of the same root issue
4. Load `references/safe_pattern_catalog.md` and check if existing safe patterns cover the identified dangers
5. Output: Consolidated pattern inventory (aim for 10-30 distinct patterns)

### Workflow 2: Danger Classification (危険理由分類)

Classify each dangerous pattern by its threat mechanism.

1. Load `references/forbidden_patterns.md` for the classification taxonomy
2. Assign each pattern to one or more danger categories:
   - **Injection / Bypass / Traversal**: Attacker-controlled input reaches sensitive operations
   - **Silent Corruption**: Data is modified or lost without error or notification
   - **Environment Divergence**: Behavior differs between dev/staging/production
   - **Hidden Dependency**: Implicit coupling that breaks under change
   - **Human Error Amplification**: Design makes mistakes easy and recovery hard
   - **Unverifiable Behavior**: Cannot confirm correctness through testing alone
3. Rank patterns by: `frequency x blast_radius x detection_difficulty`
4. Identify patterns that span multiple danger categories (highest priority)
5. Output: Classified and ranked danger inventory

### Workflow 3: Safe Standard Definition (標準パターン定義)

Define the approved safe replacement for each forbidden pattern.

1. Load `references/safe_pattern_catalog.md` for reference patterns
2. For each dangerous pattern, define:
   - **Forbidden practice**: What is explicitly prohibited
   - **Approved pattern**: The safe alternative developers must use
   - **Required abstraction**: Common layer, wrapper, or service that enforces safety
   - **Minimum contract test**: The test that proves the safe pattern is used
   - **Static rule candidate**: How to detect violations automatically
   - **Review checkpoint**: What reviewers must verify
3. Use `assets/safe_standard_template.md` to document each standard
4. Use `assets/forbidden_to_safe_mapping_template.md` to create the mapping table
5. Validate that every forbidden pattern has a concrete, usable alternative

### Workflow 4: Safe Default Decision (安全デフォルト決定)

Establish the project-wide safe defaults that apply universally.

1. Load `references/boundary_hardening_guide.md` for boundary-specific guidance
2. Define safe defaults for each boundary:
   - **Query construction**: ORM / parameterized queries only; raw SQL prohibited by default
   - **Authorization**: Deny-by-default; every endpoint requires explicit permission grant
   - **File operations**: Service-layer abstraction only; no direct path construction
   - **Persistence confirmation**: UI success message only after persistence is confirmed
   - **DateTime handling**: UTC-aware normalization at persistence boundary
   - **Row/data access**: Named/object access preferred; positional access prohibited
   - **Dependency loading**: Explicit injection; no implicit service locator or global state
   - **Idempotency**: All write operations must be idempotent or explicitly marked non-idempotent
3. For each default, document:
   - The default behavior (what happens when developer does nothing special)
   - The escape hatch (how to override when genuinely needed)
   - The enforcement mechanism (lint rule, wrapper API, framework constraint)
4. Output: Safe defaults specification document

### Workflow 5: Common Layer and Exception Design (共通層+例外条件)

Design the shared infrastructure that makes safe defaults easy and define exception policies.

1. Load `references/exception_policy.md` for exception handling guidance
2. Design common layer placement:
   - Which abstraction layer hosts each safe wrapper (middleware, service, repository, utility)
   - Interface contracts that enforce safe usage
   - Extension points for legitimate edge cases
3. Define exception conditions:
   - **When raw SQL is allowed**: Performance-critical reporting, database-specific migrations, vendor-mandated queries
   - **When deny-by-default can be relaxed**: Public-facing read-only endpoints with explicit annotation
   - **When direct file access is permitted**: Build scripts, CLI tools, infrastructure automation
4. Classify exceptions by approval level:
   - **Review-required**: Peer review with documented justification in code comment
   - **Approval-required**: Tech lead or security team sign-off with ADR
   - **Prohibited**: No exception allowed (e.g., SQL concatenation with user input)
5. Use `assets/architecture_decision_record_template.md` to document each decision
6. Output: Common layer design + exception policy document

### Workflow 6: Operational Rule Deployment (ルール運用化)

Convert standards into enforceable, operational rules.

1. Load `references/static_rule_design_guide.md` for rule design guidance
2. Create static analysis rule candidates:
   - Use `assets/static_rule_candidate_template.md` for each rule
   - Classify by tool suitability: lint, semgrep, regex, custom AST checker
   - Assess false positive risk and design suppression mechanisms
3. Create coding standard document entries:
   - Rule ID, severity, rationale, examples (good and bad)
   - Link to corresponding safe pattern and forbidden pattern
4. Create review checklist addendum:
   - Checklist items that map to each safe default
   - Explicit connection to `critical-code-reviewer` skill checkpoints
5. Plan rollout strategy:
   - Phase 1: Warning-only rules on new code
   - Phase 2: Error-level rules on new code
   - Phase 3: Codebase-wide enforcement with legacy migration
6. Output: Static rule candidates + coding standard entries + review checklist + rollout plan

## Resources

| Resource | Type | Purpose | When to Load |
|----------|------|---------|--------------|
| `references/safe_pattern_catalog.md` | Reference | Safe patterns by category (query, auth, file, datetime, etc.) | Workflow 1, 3 |
| `references/forbidden_patterns.md` | Reference | Forbidden patterns with danger classification and alternatives | Workflow 2, 3 |
| `references/boundary_hardening_guide.md` | Reference | Boundary-specific hardening techniques (controller, API, DB, file, time, env) | Workflow 4 |
| `references/static_rule_design_guide.md` | Reference | Lint/semgrep/regex rule design, false positive reduction | Workflow 6 |
| `references/exception_policy.md` | Reference | Exception conditions, approval levels, documentation requirements | Workflow 5 |
| `assets/safe_standard_template.md` | Template | Per-rule documentation (forbidden/approved/abstraction/test/review) | Workflow 3 |
| `assets/forbidden_to_safe_mapping_template.md` | Template | Anti-pattern to safe replacement mapping table | Workflow 3 |
| `assets/static_rule_candidate_template.md` | Template | Static analysis rule specification | Workflow 6 |
| `assets/architecture_decision_record_template.md` | Template | ADR for safe default decisions and exceptions | Workflow 5 |

## Best Practices

### Safe Defaults Philosophy

- **Make the safe way the easy way**: If the safe pattern requires more code or effort than the dangerous one, adoption will fail. Design wrappers and abstractions that are more convenient than raw access.
- **Forbid, do not discourage**: "Prefer ORM" is ignored; "Raw SQL triggers CI failure" is enforced. Use enforcement mechanisms, not suggestions.
- **Pair every prohibition with an alternative**: A forbidden pattern list without approved alternatives creates frustration and workarounds. Every "don't" needs a "do this instead."

### Incremental Adoption

- Start with the highest-frequency, highest-impact patterns (typically 3-5 rules cover 80% of recurring defects)
- Roll out as warnings first, then errors, then codebase-wide enforcement
- Provide migration tooling or codemods for existing violations
- Track adoption metrics: violation count over time, exception request frequency

### Exception Governance

- Exceptions are expected and healthy; zero exceptions usually means the rules are too loose
- Every exception must be documented in code (comment with justification) and tracked (ADR or ticket)
- Distinguish between "review-required" (peer review suffices) and "approval-required" (tech lead/security sign-off)
- Periodically review exception patterns; frequent exceptions to the same rule may indicate the rule needs refinement

### Connection to Review Process

- Safe default rules should map directly to `critical-code-reviewer` checklist items
- Reviewers should verify not just correctness but also standard compliance
- Automated checks should run before human review to reduce reviewer burden
- Review findings that reveal new unsafe patterns should feed back into Workflow 1

### Static Rule Quality

- Prioritize precision over recall: a rule with many false positives will be disabled
- Design rules that are auto-fixable when possible (provide the safe replacement automatically)
- Include suppression mechanisms with mandatory justification comments
- Test rules against the existing codebase before enabling enforcement
