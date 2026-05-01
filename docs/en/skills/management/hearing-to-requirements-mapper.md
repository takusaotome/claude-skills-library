---
layout: default
title: "Hearing To Requirements Mapper"
grand_parent: English
parent: Project & Business
nav_order: 13
lang_peer: /ja/skills/management/hearing-to-requirements-mapper/
permalink: /en/skills/management/hearing-to-requirements-mapper/
---

# Hearing To Requirements Mapper
{: .no_toc }

Transform client hearing sheets and meeting notes into structured requirements documents. Use when converting raw hearing data (Japanese/English) into formal requirements, generating traceability matrices, identifying gaps/ambiguities, and mapping requirements to WBS items. Triggers include "hearing to requirements", "meeting notes to specs", "requirements traceability", "gap analysis for requirements", or requests involving hearing sheet analysis.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/hearing-to-requirements-mapper.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/hearing-to-requirements-mapper){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill transforms unstructured client hearing sheets, meeting notes, and interview transcripts into structured requirements documents. It extracts requirements, maps them to WBS items, identifies gaps and ambiguities, and generates traceability matrices. The skill supports bilingual (Japanese/English) input and output with configurable templates.

**Key Capabilities:**
- Parse and extract requirements from hearing sheets, meeting notes, and transcripts
- Classify requirements by type (functional, non-functional, business, stakeholder)
- Map requirements to WBS items for project planning
- Identify gaps, conflicts, and ambiguities in captured requirements
- Generate requirements traceability matrices (RTM)
- Support both Japanese and English input/output

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Required packages: pandas, openpyxl (for Excel output)

---

## 3. Quick Start

```bash
python3 scripts/parse_hearing.py \
  --input hearing_sheet.md \
  --format markdown \
  --language auto \
  --output parsed_requirements.json
```

---

## 4. How It Works

### Step 1: Load and Parse Hearing Data

Load the hearing sheet, meeting notes, or interview transcript:

```bash
python3 scripts/parse_hearing.py \
  --input hearing_sheet.md \
  --format markdown \
  --language auto \
  --output parsed_requirements.json
```

**Supported input formats:**
- Markdown (.md)
- Plain text (.txt)
- CSV (.csv) - for structured hearing sheets
- JSON (.json) - for pre-parsed data

**The parser:**
1. Detects document language (Japanese/English/Mixed)
2. Identifies sections and structure
3. Extracts requirement statements
4. Tags initial requirement type (functional/non-functional/business/stakeholder)
5. Preserves source context for traceability

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Converting raw client hearing sheets into formal requirements documents
- Transforming meeting notes or interview transcripts into structured specifications
- Creating requirements traceability matrices from project documentation
- Identifying gaps and ambiguities in existing requirements
- Mapping requirements to WBS items for estimation
- Preparing requirements for vendor RFQs or internal development teams

---

## 6. Understanding the Output

### JSON Report (structured_requirements.json)

```json
{
  "schema_version": "1.0",
  "metadata": {
    "project_name": "CRM System Renewal",
    "created_at": "2025-01-15T10:00:00Z",
    "source_documents": ["hearing_20250110.md", "meeting_20250112.md"],
    "language": "ja"
  },
  "requirements": [
    {
      "id": "FR-001",
      "type": "functional",
      "category": "user_management",
      "description": "システムはユーザーのメールアドレス形式を検証する",
      "description_en": "System shall validate user email address format",

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/hearing-to-requirements-mapper/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: ambiguity_patterns.md, requirements_checklist.md, requirements_classification.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: requirements_mapper.py.
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

- `skills/hearing-to-requirements-mapper/references/ambiguity_patterns.md`
- `skills/hearing-to-requirements-mapper/references/requirements_checklist.md`
- `skills/hearing-to-requirements-mapper/references/requirements_classification.md`
- `skills/hearing-to-requirements-mapper/references/wbs_template.md`

**Scripts:**

- `skills/hearing-to-requirements-mapper/scripts/requirements_mapper.py`
