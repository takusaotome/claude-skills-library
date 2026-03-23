---
name: project-artifact-linker
description: Cross-reference project artifacts (WBS, meeting minutes, requirements docs) by date, participant, and action items. Extract commitments from meeting minutes and link to WBS tasks. Generate traceability reports showing which decisions were captured in which documents.
---

# Project Artifact Linker

## Overview

This skill enables comprehensive cross-referencing of project documents to maintain traceability across WBS elements, meeting minutes, requirements, and decisions. It extracts commitments, action items, and decisions from meeting minutes and links them to corresponding WBS tasks, creating a unified traceability matrix that shows the provenance of all project artifacts.

## When to Use

- When you need to trace decisions back to the meetings where they were made
- When auditing project documentation for completeness and traceability
- When onboarding to a project and need to understand decision history
- When preparing for project reviews and need to show artifact linkages
- When extracting action items from meeting minutes and mapping to WBS tasks
- When generating compliance reports showing requirement-to-deliverable traceability
- When identifying orphaned artifacts (decisions without documentation, tasks without requirements)

## Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: `pyyaml` (for YAML parsing), standard library otherwise

## Workflow

### Step 1: Gather Project Artifacts

Collect all project documents to be linked. Supported formats:
- Meeting minutes (Markdown, plain text)
- WBS files (Markdown tables, CSV, JSON)
- Requirements documents (Markdown, plain text)
- Decision logs (Markdown, JSON)

```bash
# Example: List all artifacts in a project directory
find /path/to/project -name "*.md" -o -name "*.json" -o -name "*.csv"
```

### Step 2: Parse and Extract Entities

Run the artifact parser to extract structured entities from each document type.

```bash
python3 scripts/parse_artifacts.py \
  --input-dir /path/to/project/docs \
  --output artifacts.json
```

The parser extracts:
- **From Meeting Minutes**: Date, attendees, action items, decisions, discussion topics
- **From WBS**: Task IDs, task names, owners, dates, dependencies
- **From Requirements**: Requirement IDs, descriptions, priorities, acceptance criteria
- **From Decision Logs**: Decision IDs, descriptions, dates, rationale, stakeholders

### Step 3: Build Cross-Reference Links

Run the linker to establish relationships between extracted entities.

```bash
python3 scripts/link_artifacts.py \
  --artifacts artifacts.json \
  --output links.json
```

Link types created:
- `action_item → wbs_task`: Action items mapped to WBS tasks by keyword/owner match
- `decision → requirement`: Decisions linked to requirements they address
- `meeting → wbs_task`: Meetings linked to tasks discussed
- `requirement → wbs_task`: Requirements traced to implementing tasks

### Step 4: Generate Traceability Report

Generate a comprehensive traceability report in Markdown or JSON format.

```bash
python3 scripts/generate_traceability_report.py \
  --artifacts artifacts.json \
  --links links.json \
  --output traceability_report.md \
  --format markdown
```

### Step 5: Identify Gaps and Orphans

Analyze the traceability matrix to identify coverage gaps.

```bash
python3 scripts/analyze_coverage.py \
  --artifacts artifacts.json \
  --links links.json \
  --output coverage_analysis.json
```

Gap types detected:
- Requirements without implementing WBS tasks
- WBS tasks without originating requirements
- Decisions without meeting documentation
- Action items without resolution tracking

## Output Format

### JSON Artifacts Schema

```json
{
  "schema_version": "1.0",
  "extraction_date": "2024-01-15T10:30:00Z",
  "artifacts": {
    "meetings": [
      {
        "id": "MTG-2024-001",
        "date": "2024-01-10",
        "attendees": ["Alice", "Bob"],
        "action_items": [
          {
            "id": "AI-001",
            "description": "Review security requirements",
            "owner": "Alice",
            "due_date": "2024-01-17"
          }
        ],
        "decisions": [
          {
            "id": "DEC-001",
            "description": "Adopt OAuth2 for authentication",
            "rationale": "Industry standard, better security"
          }
        ]
      }
    ],
    "wbs_tasks": [
      {
        "id": "WBS-1.2.3",
        "name": "Implement authentication module",
        "owner": "Alice",
        "start_date": "2024-01-15",
        "end_date": "2024-02-15"
      }
    ],
    "requirements": [
      {
        "id": "REQ-SEC-001",
        "description": "System shall support OAuth2 authentication",
        "priority": "High"
      }
    ]
  }
}
```

### JSON Links Schema

```json
{
  "schema_version": "1.0",
  "link_date": "2024-01-15T10:35:00Z",
  "links": [
    {
      "source_type": "action_item",
      "source_id": "AI-001",
      "target_type": "wbs_task",
      "target_id": "WBS-1.2.3",
      "link_type": "implements",
      "confidence": 0.85,
      "match_reason": "owner_match + keyword_overlap"
    },
    {
      "source_type": "decision",
      "source_id": "DEC-001",
      "target_type": "requirement",
      "target_id": "REQ-SEC-001",
      "link_type": "addresses",
      "confidence": 0.92,
      "match_reason": "keyword_exact_match: OAuth2"
    }
  ]
}
```

### Markdown Traceability Report

```markdown
# Project Traceability Report

Generated: 2024-01-15 10:40:00

## Summary

| Artifact Type | Count | Linked | Orphaned |
|--------------|-------|--------|----------|
| Requirements | 25    | 23     | 2        |
| WBS Tasks    | 45    | 42     | 3        |
| Decisions    | 12    | 12     | 0        |
| Action Items | 30    | 28     | 2        |

## Traceability Matrix

### Requirements → WBS Tasks

| Requirement | Description | WBS Task(s) | Status |
|-------------|-------------|-------------|--------|
| REQ-SEC-001 | OAuth2 auth | WBS-1.2.3   | Linked |

### Meeting Decisions → Requirements

| Decision | Meeting | Requirement(s) |
|----------|---------|----------------|
| DEC-001  | MTG-2024-001 | REQ-SEC-001 |

## Gaps and Orphans

### Orphaned Requirements (no implementing task)
- REQ-PERF-005: Response time < 200ms

### Orphaned WBS Tasks (no source requirement)
- WBS-2.1.4: Legacy data migration
```

## Resources

- `scripts/parse_artifacts.py` -- Extract entities from project documents
- `scripts/link_artifacts.py` -- Build cross-reference links between entities
- `scripts/generate_traceability_report.py` -- Generate traceability matrix reports
- `scripts/analyze_coverage.py` -- Identify gaps and orphaned artifacts
- `references/artifact_patterns.md` -- Patterns for extracting entities from documents
- `references/link_heuristics.md` -- Heuristics for establishing artifact links

## Key Principles

1. **Bidirectional Traceability**: Every link should be navigable in both directions
2. **Confidence Scoring**: All automated links include confidence scores for human review
3. **Gap Detection**: Proactively identify missing links rather than just documenting existing ones
4. **Flexible Input**: Support multiple document formats common in project management
5. **Incremental Updates**: Support adding new documents without re-processing entire corpus
