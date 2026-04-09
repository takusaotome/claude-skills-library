# Design Decision Tracking Methodology

## Purpose

This document establishes best practices for tracking design decisions across iterative revision cycles. The methodology enables consistent styling, accurate context resolution, and clear communication between designers, clients, and AI assistants.

## Core Concepts

### Design Decision

A **design decision** is any intentional change to a visual or structural element of a document or presentation. Each decision has:

- **What** -- The element being changed
- **From/To** -- The old and new values
- **Why** -- The reason or user request driving the change
- **Where** -- The specific location(s) affected

### Design Token

A **design token** is a named, reusable value extracted from design decisions. Tokens enable consistent application of styling across elements. Examples:

| Category | Token Name | Example Value |
|----------|------------|---------------|
| Color | primary-color | #003366 |
| Color | accent-color | #FF6B00 |
| Typography | heading-font | "Arial Bold" |
| Typography | body-size | 14pt |
| Spacing | margin-standard | 24px |

### Contextual Reference

A **contextual reference** is when a user refers to a previous decision without explicit identification. Common patterns:

| Language | Example | Resolution Strategy |
|----------|---------|---------------------|
| Japanese | "前回も色で良いんだけど" | Most recent color decision |
| Japanese | "さっきと同じフォントで" | Most recent typography decision |
| English | "like before" | Most recent decision in same category |
| English | "same style as the header" | Query by element name |
| English | "revert to the original" | Find superseded_by chain |

## Decision Categories

### 1. Color Decisions

Track color changes with full context:

```json
{
  "category": "color",
  "element": "header-background",
  "old_value": "#FFFFFF",
  "new_value": "#003366",
  "color_space": "hex",
  "semantic_name": "corporate-blue"
}
```

**Color Resolution Priority:**
1. Exact hex match
2. Semantic name match ("corporate blue")
3. Category + recency (most recent color change)

### 2. Typography Decisions

Track font and text styling changes:

```json
{
  "category": "typography",
  "element": "body-text",
  "properties_changed": ["font-size", "line-height"],
  "old_value": {"font-size": "12pt", "line-height": "1.2"},
  "new_value": {"font-size": "14pt", "line-height": "1.5"},
  "reason": "Improved readability for conference room"
}
```

### 3. Layout Decisions

Track positioning and structural changes:

```json
{
  "category": "layout",
  "element": "slide-grid",
  "change_type": "spacing",
  "old_value": "20px gap",
  "new_value": "32px gap",
  "affected_slides": [3, 5, 7, 8]
}
```

### 4. Content Decisions

Track meaningful content changes (not typo fixes):

```json
{
  "category": "content",
  "element": "chart-data",
  "change_type": "data-update",
  "description": "Updated Q3 numbers to final actuals",
  "reference": "slide-12-revenue-chart"
}
```

### 5. Style Decisions

Track visual effects and decorations:

```json
{
  "category": "style",
  "element": "card-border",
  "old_value": "none",
  "new_value": "1px solid #E0E0E0",
  "reason": "Added subtle borders for visual separation"
}
```

## Contextual Reference Resolution

### Resolution Algorithm

When a user makes a contextual reference:

1. **Parse Intent** -- Identify the category being referenced (color, typography, etc.)
2. **Scope Search** -- Determine if reference is element-specific or general
3. **Time Ordering** -- Sort matching decisions by recency
4. **Confidence Scoring** -- Rank matches by relevance
5. **Confirmation** -- For ambiguous cases, confirm with user before applying

### Confidence Scoring Matrix

| Signal | Weight |
|--------|--------|
| Exact category match | +3 |
| Same element reference | +2 |
| Recent (last 5 decisions) | +2 |
| Semantic keyword match | +1 |
| Same session | +1 |

**Threshold**: Confidence ≥ 4 = auto-apply, < 4 = confirm with user

### Common Reference Patterns

**Japanese Patterns:**

| Pattern | Meaning | Resolution |
|---------|---------|------------|
| 前回 (zenkai) | "last time" | Most recent in category |
| さっき (sakki) | "just now" | Very recent (last 3 decisions) |
| 最初の (saisho no) | "original" | First in chain or old_value |
| 同じ (onaji) | "same" | Exact value copy |
| 似た感じ (nita kanji) | "similar feel" | Approximate match |

**English Patterns:**

| Pattern | Meaning | Resolution |
|---------|---------|------------|
| "like before" | Previous similar change | Recent in category |
| "same as X" | Copy from element X | Query by element |
| "original" | Pre-change value | old_value lookup |
| "consistent with" | Match existing style | Design token lookup |
| "undo" | Revert change | Swap old/new values |

## Design Token Extraction

### Automatic Token Generation

When a value is applied to 3+ elements, automatically suggest creating a design token:

```
Detected: #003366 applied to 4 elements
Suggested token: "primary-header-color"
Accept? [Y/n]
```

### Token Naming Conventions

| Category | Pattern | Example |
|----------|---------|---------|
| Color | {semantic}-{element}-color | header-background-color |
| Typography | {purpose}-{property} | body-font-size |
| Spacing | {context}-{direction} | card-padding-horizontal |

### Token Update Propagation

When a token value is updated, track all affected elements:

```json
{
  "token_update": {
    "token_name": "primary-color",
    "old_value": "#003366",
    "new_value": "#004488",
    "affected_elements": [
      "slide-3-header",
      "slide-7-title",
      "footer-accent"
    ],
    "auto_propagated": true
  }
}
```

## Session Management

### Session Lifecycle

1. **Init** -- Create new session for document/project
2. **Active** -- Record decisions, resolve references, extract tokens
3. **Pause** -- Preserve state for later resumption
4. **Archive** -- Complete session, generate final report

### Cross-Session References

When referencing decisions from a different session:

```bash
python3 design_log.py import \
  --from-session "previous-project" \
  --decision-ids "dec_001,dec_002" \
  --as-tokens
```

This imports the values as design tokens rather than decisions, maintaining clean session boundaries.

### Session Merge

For combining related sessions:

```bash
python3 design_log.py merge \
  --sessions "draft-v1,draft-v2,draft-final" \
  --output "complete-history"
```

## Best Practices

### 1. Record Immediately

Record design decisions immediately after making them, while context is fresh. Delayed recording loses the "why" that enables future resolution.

### 2. Be Specific About Reason

"User requested" is less useful than "User requested corporate blue to match brand guidelines for client X."

### 3. Name Elements Consistently

Use consistent element naming across the session:
- Good: "slide-3-header", "slide-7-header"
- Bad: "the header on slide 3", "header3", "s3h"

### 4. Link Related Decisions

When one decision leads to another, record the relationship:

```json
{
  "id": "dec_005",
  "triggered_by": "dec_003",
  "reason": "Adjusted secondary color to maintain contrast with new primary"
}
```

### 5. Document Design Constraints

Record constraints that affect future decisions:

```json
{
  "constraint": {
    "type": "brand-guideline",
    "description": "Logo must have 20px clear space",
    "source": "brand-guidelines-2024.pdf",
    "affects": ["logo-placement", "header-layout"]
  }
}
```

## Troubleshooting

### Ambiguous References

When a reference could match multiple decisions:

1. Present the top 3 matches with confidence scores
2. Ask user to confirm or clarify
3. Record the clarification for future reference

### Conflicting Decisions

When a new decision contradicts an earlier one:

1. Check if this is an intentional override
2. Mark the earlier decision as `superseded_by: new_decision_id`
3. Update any derived tokens

### Lost Context

If session history is incomplete:

1. Review the current document state
2. Infer decisions from visible styling
3. Ask user to confirm inferred history
4. Mark inferred decisions with `confidence: "inferred"`
