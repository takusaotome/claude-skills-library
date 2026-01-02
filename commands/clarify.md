---
description: "Clarify plan ambiguities through structured Q&A. Use after creating a plan to identify unclear points, gather decisions via AskUserQuestion, and update the plan with concrete specifications."
argument-hint: "[plan-file-path]"
allowed-tools:
  - Write
  - Edit
  - Read
  - Grep
  - Glob
  - TodoRead
  - TodoWrite
  - AskUserQuestion
---

# Plan Clarification Workflow

Interview me in detail about the current plan using AskUserQuestion tool to resolve all ambiguities.

## Why Use This Command?

- **Prevents rework**: Clarify decisions before implementation starts
- **Stakeholder alignment**: Document choices with rationale
- **Decision traceability**: Create audit trail for future reference

## Prerequisites

- **Plan file required**: Existing `*-plan.md` file or specify path as argument
- **Plan format**: Markdown with clear sections (Overview, Features, Technical, etc.)
- **Optional**: CLAUDE.md in project root for style/pattern guidance

**If no plan file exists**: Create one first or ask user for requirements.

## Domains to Explore

- Product specifications
- Technical architecture decisions
- UI/UX details
- Data models and storage
- Integration points
- Edge cases and error handling
- Performance requirements
- Security considerations

## Workflow Phases

### Phase 1: Analyze Plan

1. Read the plan file (look for `*-plan.md` or use argument path)
2. Identify unclear points using these detection patterns:
   - **Vague quantifiers**: "many", "some", "appropriate", "reasonable"
   - **Missing specs**: No tech stack, versions, or tools specified
   - **Ambiguous scope**: "as needed", "if required", "possibly"
   - **Undefined constraints**: No metrics, limits, or acceptance criteria
3. Categorize by domain (product, technical, UX, etc.)

### Phase 2: Generate Questions

Each question uses AskUserQuestion tool with:
- `question`: Clear, specific question text
- `options`: 2-4 choices, each with label + description (pros/cons)
- `multiSelect`: false (default)

<rules>
- Question count: **2-4** per round (adjust based on ambiguity level)
- Each question has **2-4 concrete options**
- Each option includes brief **pros/cons** in description
- Avoid open-ended questions
- "Other" option is auto-added by the tool - don't include it
- Align options with existing patterns from CLAUDE.md (if available)
- Use multiSelect sparingly (default: false)
</rules>

### Phase 3: Record Decisions

After receiving answers, document in memory:

| Item | Choice | Rationale | Owner | Follow-up |
|------|--------|-----------|-------|-----------|
| [Topic] | [Selected option] | [Why this choice] | [DRI if known] | [Yes/No] |

**Recording rules**:
- Accumulate decisions across rounds
- Note any "Other" responses verbatim
- Flag items requiring external approval

### Phase 4: Iterate Until Complete

**Termination criteria** (any of these):
- All 8 domains addressed with at least one decision each
- Maximum **5 rounds** reached
- User explicitly confirms "finalize"

**Each round**:
1. Ask: "Continue clarifying or finalize?"
2. If continue → Return to Phase 2
3. If finalize → Proceed to Phase 5

### Phase 5: Update Plan and Summarize

**Update procedure**:
1. Create backup: `[plan-name].backup.md`
2. Map each decision to relevant plan section
3. Update sections using Edit tool
4. Add `## Clarification Decisions` appendix with full decision table

**Output summary**:

```
## Clarification Summary

### Decisions Made
- [Count] decisions across [domains covered]

### Plan Updates
- [Sections modified]

### Pending Items
- [Items flagged for follow-up]

### Ready for Implementation
- [Confirmation or blockers]
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Plan file not found | Ask for correct path or offer to create new |
| Plan too vague (<50 lines) | Focus on top 3 most critical domains |
| User selects "Other" | Record verbatim, flag for follow-up |
| Contradictory decisions | Flag conflict, ask user to resolve |
| User cancels mid-session | Save decisions so far, offer to resume |

## Example

**Plan**: E-commerce MVP (high-level, 2 pages)

**Round 1 Questions**:

1. **Payment Processing**
   - Stripe only (Simple setup, 2.9% fees)
   - Multiple providers (Flexibility, complex integration)
   - Buy-now-pay-later (Higher conversion, compliance burden)

2. **User Authentication**
   - Email + password (Simple, password reset needed)
   - Social login only (Low friction, platform dependency)
   - Both options (Best UX, more maintenance)

**Decision Table**:

| Item | Choice | Rationale | Owner | Follow-up |
|------|--------|-----------|-------|-----------|
| Payment | Stripe only | "Fast launch, can add others in V2" | @backend | No |
| Auth | Both options | "Need email for B2B, social for consumers" | @frontend | No |
| Database | PostgreSQL | "Team expertise, ACID compliance" | @backend | No |

**Summary Output**:
```
## Clarification Summary

### Decisions Made
- 8 decisions across Product, Technical, UX

### Plan Updates
- Updated: Section 2 (Tech Stack)
- Updated: Section 3 (Feature Set)
- Added: Appendix A (Decision Log)

### Ready for Implementation
- Core architecture decisions complete
- Ready for technical design phase
```

## Important Notes

- **Must use AskUserQuestion tool** - Not conversational questions
- **Language**: Check CLAUDE.md for preference, fallback to user's language
- **Depth**: Continue until critical ambiguities resolved (max 5 rounds)
- Read CLAUDE.md before generating questions to align with project patterns
