---
layout: default
title: "Project Artifact Linker"
grand_parent: English
parent: Project & Business
nav_order: 19
lang_peer: /ja/skills/management/project-artifact-linker/
permalink: /en/skills/management/project-artifact-linker/
---

# Project Artifact Linker
{: .no_toc }

Cross-reference project artifacts (WBS, meeting minutes, requirements docs) by date, participant, and action items. Extract commitments from meeting minutes and link to WBS tasks. Generate traceability reports showing which decisions were captured in which documents.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/project-artifact-linker.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/project-artifact-linker){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill enables comprehensive cross-referencing of project documents to maintain traceability across WBS elements, meeting minutes, requirements, and decisions. It extracts commitments, action items, and decisions from meeting minutes and links them to corresponding WBS tasks, creating a unified traceability matrix that shows the provenance of all project artifacts.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Dependencies: `pyyaml` (for YAML parsing), standard library otherwise

---

## 3. Quick Start

```bash
# Example: List all artifacts in a project directory
find /path/to/project -name "*.md" -o -name "*.json" -o -name "*.csv"
```

---

## 4. How It Works

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

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- When you need to trace decisions back to the meetings where they were made
- When auditing project documentation for completeness and traceability
- When onboarding to a project and need to understand decision history
- When preparing for project reviews and need to show artifact linkages
- When extracting action items from meeting minutes and mapping to WBS tasks
- When generating compliance reports showing requirement-to-deliverable traceability

---

## 6. Understanding the Output

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

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/project-artifact-linker/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: artifact_patterns.md, link_heuristics.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: generate_traceability_report.py, link_artifacts.py, parse_artifacts.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/management/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/project-artifact-linker/references/artifact_patterns.md`
- `skills/project-artifact-linker/references/link_heuristics.md`

**Scripts:**

- `skills/project-artifact-linker/scripts/analyze_coverage.py`
- `skills/project-artifact-linker/scripts/generate_traceability_report.py`
- `skills/project-artifact-linker/scripts/link_artifacts.py`
- `skills/project-artifact-linker/scripts/parse_artifacts.py`
