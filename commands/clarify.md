---
description: "Clarify plan ambiguities through structured Q&A. Use after creating a plan to identify unclear points, gather decisions via AskUserQuestion, and update the plan with concrete specifications."
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
1. Read the plan file (look for `*-plan.md` or ask user for path)
2. Identify all unclear points, assumptions, and decision points
3. Categorize by domain (product, technical, UX, etc.)

### Phase 2: Generate Questions

<rules>
- Question count: **2-4** per round (adjust based on ambiguity level)
- Each question has **2-4 concrete options**
- Each option includes brief **pros/cons**
- Avoid open-ended questions
- "Other" option is auto-added by the tool - don't include it
- Align options with existing patterns from CLAUDE.md (if available)
- Use multiSelect sparingly (default: false)
</rules>

### Phase 3: Record Decisions

After receiving answers, document:

| Item | Choice | Rationale | Notes |
|------|--------|-----------|-------|
| [Topic] | [Selected option] | [Why] | [Additional context] |

### Phase 4: Iterate Until Complete
- Check if remaining unclear points exist
- If YES → Return to Phase 2 with new questions
- If NO → Proceed to Phase 5

### Phase 5: Update Plan and Summarize

1. Apply all decisions to the plan file
2. Output summary:

```
## Clarification Summary

### Decisions Made
- [List of key decisions]

### Plan Updates
- [What was added/changed in the plan]

### Ready for Implementation
- [Confirmation that plan is now actionable]
```

## Important Notes

- **Must use AskUserQuestion tool** - Not conversational questions
- **Language**: Check CLAUDE.md for preference, fallback to user's language
- **Depth**: Continue questioning until ALL ambiguities are resolved
- Read CLAUDE.md before generating questions to align with project patterns
