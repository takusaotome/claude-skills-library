# Artifact Extraction Patterns

This document defines patterns for extracting structured entities from various project document types.

## Meeting Minutes Patterns

### Date Extraction

```regex
# ISO date format
(\d{4}-\d{2}-\d{2})

# Common formats
(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}
\d{1,2}/\d{1,2}/\d{4}
\d{1,2}-\d{1,2}-\d{4}
```

### Attendee Extraction

Look for sections with these headers:
- `Attendees:`
- `Participants:`
- `Present:`
- `In Attendance:`

Pattern for attendee list:
```regex
# Comma-separated names
([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)*

# Bullet list of names
^\s*[-*]\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)
```

### Action Item Extraction

Trigger phrases:
- `ACTION:` or `Action Item:`
- `TODO:`
- `@[name] to`
- `[name] will`
- `Assigned to [name]:`

Pattern structure:
```
[Owner] + [Action verb] + [Task description] + [Optional: by Date]
```

Example matches:
- "ACTION: Alice to review security requirements by Jan 17"
- "@Bob will update the architecture diagram"
- "TODO: Schedule follow-up meeting with stakeholders"

### Decision Extraction

Trigger phrases:
- `DECISION:`
- `Decided:`
- `Agreed:`
- `Resolution:`
- `We will` / `Team will`

Pattern structure:
```
[Decision keyword] + [Decision description] + [Optional: Rationale]
```

Example matches:
- "DECISION: Adopt OAuth2 for authentication due to security requirements"
- "Agreed: Use PostgreSQL for the primary database"

## WBS Patterns

### Task ID Formats

```regex
# Hierarchical WBS numbering
WBS-\d+(\.\d+)*
\d+\.\d+(\.\d+)*

# Project-prefixed IDs
[A-Z]{2,4}-\d+
TASK-\d+
```

### Task Table Parsing

Markdown table pattern:
```markdown
| Task ID | Task Name | Owner | Start | End | Status |
```

CSV pattern:
```
task_id,task_name,owner,start_date,end_date,status
```

### Owner/Assignee Extraction

Common column headers:
- `Owner`
- `Assignee`
- `Assigned To`
- `Responsible`
- `Lead`

### Date Extraction

Common column headers for dates:
- `Start Date` / `Start`
- `End Date` / `End` / `Due Date`
- `Target Date`
- `Deadline`

## Requirements Patterns

### Requirement ID Formats

```regex
# Standard requirement IDs
REQ-[A-Z]{2,4}-\d+
R\d+
[A-Z]{2,5}-\d+

# Functional/Non-functional prefixes
FR-\d+     # Functional Requirement
NFR-\d+    # Non-Functional Requirement
SR-\d+     # Security Requirement
PR-\d+     # Performance Requirement
```

### Priority Extraction

Keywords and mappings:
- `Critical` / `P0` / `Must Have` → Priority 1
- `High` / `P1` / `Should Have` → Priority 2
- `Medium` / `P2` / `Could Have` → Priority 3
- `Low` / `P3` / `Won't Have` → Priority 4

### Acceptance Criteria Extraction

Trigger patterns:
- `Given... When... Then...` (BDD format)
- `Acceptance Criteria:`
- `Verification:`
- `Test Criteria:`

## Decision Log Patterns

### Decision ID Formats

```regex
DEC-\d+
D\d+
DECISION-\d+
ADR-\d+    # Architecture Decision Record
```

### Decision Structure

Standard fields:
- ID
- Title/Summary
- Date
- Status (Proposed, Accepted, Deprecated, Superseded)
- Context
- Decision
- Consequences
- Stakeholders/Approvers

### Rationale Extraction

Trigger phrases:
- `Because`
- `Due to`
- `Rationale:`
- `Reason:`
- `This was chosen because`

## Cross-Reference Patterns

### Explicit References

```regex
# Direct ID references
See\s+([A-Z]+-\d+)
Ref:\s*([A-Z]+-\d+)
Related\s+to\s+([A-Z]+-\d+)
Implements\s+([A-Z]+-\d+)
Addresses\s+([A-Z]+-\d+)
```

### Implicit References

Keyword overlap detection:
1. Extract key nouns and verbs from source document
2. Match against target document key terms
3. Calculate Jaccard similarity or TF-IDF score

Owner/Participant matching:
1. Extract names from meetings
2. Match against WBS task owners
3. Infer relationship through shared responsibility

## Entity Normalization

### Name Normalization

```python
# Standard normalization steps
1. Strip whitespace
2. Convert to title case
3. Remove titles (Mr., Ms., Dr., etc.)
4. Handle common aliases (Bob → Robert, etc.)
```

### Date Normalization

```python
# Convert all dates to ISO 8601 format
YYYY-MM-DD

# Handle relative dates
"next Monday" → calculate from document date
"Q1 2024" → 2024-01-01 to 2024-03-31
```

### ID Normalization

```python
# Standardize ID formats
1. Remove extra whitespace
2. Convert to uppercase
3. Normalize separators (_, -, .)
4. Add prefix if missing
```
