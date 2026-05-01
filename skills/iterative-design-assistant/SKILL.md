---
name: iterative-design-assistant
description: Track design iteration history and apply consistent styling decisions across revision cycles. Use when handling follow-up change requests that reference previous design decisions (e.g., '前回も色で良いんだけど', 'same style as before', 'like we discussed').
---

# Iterative Design Assistant

## Overview

This skill maintains a session-local design decision log that tracks styling choices, revision history, and contextual relationships across multiple document or presentation revision cycles. It enables Claude to understand references to previous changes and apply consistent design decisions without requiring users to repeat context.

## When to Use

- User references a previous design decision ("前回も色で良いんだけど", "like last time", "same as before")
- Multiple revision cycles on the same document/presentation
- Need to track which design elements were changed and why
- Applying consistent styling across related documents
- Reviewing design history to understand evolution of a document
- User asks to "undo" or "revert" to a previous design state

## Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (json, datetime, pathlib)

## Workflow

### Step 1: Initialize Design Session

When starting work on a document/presentation, initialize a design session log. The log file is created in the current working directory.

```bash
python3 scripts/design_log.py init \
  --document "presentation.pptx" \
  --session-name "Q4 Sales Deck Revisions"
```

This creates a `.design-log.json` file that tracks all design decisions for the session.

### Step 2: Record Design Decisions

Each time a design change is made, record it in the log with context about what was changed and why.

```bash
python3 scripts/design_log.py record \
  --category "color" \
  --element "header-background" \
  --old-value "#FFFFFF" \
  --new-value "#003366" \
  --reason "User requested corporate blue for headers" \
  --reference "slide-3"
```

Categories include:
- `color` - Color changes (hex values, color names)
- `typography` - Font family, size, weight changes
- `layout` - Positioning, spacing, alignment changes
- `content` - Text, image, or data changes
- `style` - Border, shadow, effect changes

### Step 3: Query Previous Decisions

When user references a previous decision, query the log to retrieve context.

```bash
python3 scripts/design_log.py query \
  --category "color" \
  --limit 5
```

Or search by keyword:

```bash
python3 scripts/design_log.py search \
  --keyword "header" \
  --limit 10
```

### Step 4: Apply Consistent Styling

When applying a previous decision to new elements, reference the decision ID.

```bash
python3 scripts/design_log.py apply \
  --decision-id "dec_001" \
  --target-element "slide-7-title"
```

This records that the same styling was applied to a new element, maintaining traceability.

### Step 5: Review Design History

Generate a summary of all design decisions for documentation or review.

```bash
python3 scripts/design_log.py history \
  --format markdown \
  --output design-history.md
```

### Step 6: Handle Contextual References

When user says something like "前回も色で良いんだけど" (the color from last time is fine), use the context resolution workflow:

1. Query recent color-related decisions
2. Identify the most relevant previous decision
3. Apply the same value to the current context
4. Record the new application with reference to the original decision

```bash
# Find recent color decisions
python3 scripts/design_log.py query --category color --limit 3

# Apply the identified decision
python3 scripts/design_log.py apply \
  --decision-id "dec_003" \
  --target-element "current-element" \
  --context "User confirmed previous color choice"
```

## Output Format

### Design Log JSON Schema

```json
{
  "schema_version": "1.0",
  "session": {
    "id": "session_uuid",
    "name": "Q4 Sales Deck Revisions",
    "document": "presentation.pptx",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T14:45:00Z"
  },
  "decisions": [
    {
      "id": "dec_001",
      "timestamp": "2024-01-15T10:35:00Z",
      "category": "color",
      "element": "header-background",
      "old_value": "#FFFFFF",
      "new_value": "#003366",
      "reason": "User requested corporate blue for headers",
      "reference": "slide-3",
      "applied_to": ["slide-3-header", "slide-7-title"],
      "superseded_by": null
    }
  ],
  "design_tokens": {
    "colors": {
      "primary": "#003366",
      "secondary": "#F0F0F0"
    },
    "typography": {
      "heading-font": "Arial Bold",
      "body-font": "Arial"
    }
  }
}
```

### Markdown History Report

```markdown
# Design History: Q4 Sales Deck Revisions

**Document**: presentation.pptx
**Session Started**: 2024-01-15 10:30

## Timeline

### 2024-01-15 10:35 - Color Change
- **Element**: header-background
- **Change**: #FFFFFF → #003366
- **Reason**: User requested corporate blue for headers
- **Applied to**: slide-3-header, slide-7-title

### 2024-01-15 11:20 - Typography Change
- **Element**: body-text
- **Change**: 12pt → 14pt
- **Reason**: Improved readability for presentation room

## Design Tokens

| Category | Token | Value |
|----------|-------|-------|
| Color | Primary | #003366 |
| Color | Secondary | #F0F0F0 |
| Typography | Heading Font | Arial Bold |
| Typography | Body Font | Arial |
```

## Resources

- `scripts/design_log.py` -- CLI tool for managing design decision logs
- `references/design-decision-methodology.md` -- Best practices for tracking and applying design decisions

## Key Principles

1. **Context Preservation** -- Every design decision includes the reason and context, enabling accurate interpretation of future references
2. **Bidirectional Traceability** -- Track which decisions were applied to which elements, and which elements derive from which decisions
3. **Incremental History** -- Build up a design token vocabulary as decisions accumulate, enabling consistent future styling
4. **Natural Language Resolution** -- Support vague references ("like before", "前回と同じ") by matching against recent relevant decisions
5. **Session Isolation** -- Each document/session has its own log, preventing cross-contamination while allowing explicit cross-referencing

## Integration with Other Skills

This skill complements:
- `fujisoft-presentation-creator` -- Track design decisions made during presentation creation
- `presentation-reviewer` -- Reference design history when reviewing presentations
- `markdown-to-pdf` -- Apply consistent styling tokens to PDF generation
