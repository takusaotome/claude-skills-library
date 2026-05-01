---
layout: default
title: "Salesforce Flow Expert"
grand_parent: English
parent: Software Development
nav_order: 28
lang_peer: /ja/skills/dev/salesforce-flow-expert/
permalink: /en/skills/dev/salesforce-flow-expert/
---

# Salesforce Flow Expert
{: .no_toc }

Expert guidance for Salesforce Flow implementation from design through deployment. Use this skill when building Screen Flows, Record-Triggered Flows, Schedule-Triggered Flows, or Autolaunched Flows. Covers Flow design patterns, metadata XML generation, variable/element reference validation, governor limit optimization, and sf CLI deployment. Critical for preventing reference errors (undeclared variables, invalid element references) and deployment failures. Use when creating new Flows, debugging Flow errors, optimizing Flow performance, or deploying Flows to production.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/salesforce-flow-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/salesforce-flow-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides comprehensive guidance for Salesforce Flow implementation, from initial design through production deployment. It emphasizes preventing the most common Flow errors—particularly variable and element reference issues—through automated validation, proper metadata generation, and deployment best practices. Use this skill to build robust, error-free Flows that deploy successfully on the first attempt.

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
python3 scripts/validate_flow.py MyFlow.flow-meta.xml --format markdown > validation_report.md
```

---

## 4. How It Works

Follow this end-to-end workflow for error-free Flow implementation:

**Phase 1: Design** (10-20 minutes)
1. Determine Flow type using decision matrix (Capability 1)
2. Sketch Flow logic on paper or whiteboard
3. Define variables with proper naming conventions
4. Identify data operations (Get, Create, Update, Delete)

**Phase 2: Build** (30-60 minutes)
5. Create Flow in Flow Builder (Setup → Flows → New Flow)
6. Implement business logic following design patterns
7. Test manually in sandbox with sample data
8. Export Flow files (`.flow` and `.flow-meta.xml`)

**Phase 3: Validate** (5 minutes)
9. Run validation script:
   ```bash
   python3 scripts/validate_flow.py MyFlow.flow-meta.xml --format markdown > validation_report.md
   ```
10. Review validation report and fix all errors
11. Re-run validation until clean (0 errors)

**Phase 4: Deploy** (5-10 minutes)
12. Deploy to sandbox with validation:

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- **Flow Development**: Creating new Screen Flows, Record-Triggered Flows, Schedule-Triggered Flows, or Autolaunched Flows
- **Error Prevention**: Validating Flows before deployment to catch reference errors, type mismatches, or undeclared variables
- **Debugging**: Troubleshooting "Element not found", "Variable not declared", or type mismatch errors
- **Deployment**: Deploying Flows to sandbox or production using sf CLI with proper error handling
- **Optimization**: Identifying governor limit issues (DML in loops, SOQL in loops) and implementing bulkification patterns
- **Metadata Management**: Generating or troubleshooting Flow-meta.xml files with correct structure and API versions

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 5 guide file(s).
- Script-assisted execution using 4 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/salesforce-flow-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: governor_limits_optimization.md, metadata_xml_reference.md, variable_reference_patterns.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: extract_flow_elements.py, validate_flow.py, generate_flow_metadata.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
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

- `skills/salesforce-flow-expert/references/deployment_guide.md`
- `skills/salesforce-flow-expert/references/flow_types_guide.md`
- `skills/salesforce-flow-expert/references/governor_limits_optimization.md`
- `skills/salesforce-flow-expert/references/metadata_xml_reference.md`
- `skills/salesforce-flow-expert/references/variable_reference_patterns.md`

**Scripts:**

- `skills/salesforce-flow-expert/scripts/deploy_flow.py`
- `skills/salesforce-flow-expert/scripts/extract_flow_elements.py`
- `skills/salesforce-flow-expert/scripts/generate_flow_metadata.py`
- `skills/salesforce-flow-expert/scripts/validate_flow.py`
