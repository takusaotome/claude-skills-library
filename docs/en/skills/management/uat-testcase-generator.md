---
layout: default
title: "UAT Testcase Generator"
grand_parent: English
parent: Project & Business
nav_order: 25
lang_peer: /ja/skills/management/uat-testcase-generator/
permalink: /en/skills/management/uat-testcase-generator/
---

# UAT Testcase Generator
{: .no_toc }

This skill should be used when creating UAT (User Acceptance Testing) test cases in Excel format for Salesforce CRM projects. It generates standardized test case documents with summary sheets and detailed test case lists, following a specific format structure with test case ID, priority, category, scenario, preconditions, test steps, expected results, and acceptance criteria.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/uat-testcase-generator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/uat-testcase-generator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill generates UAT (User Acceptance Testing) test case documents in Excel format for Salesforce CRM projects. The generated documents include a summary sheet with category breakdowns and a detailed test case list with all required fields for UAT execution.

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

### Step 1: Gather Information

Collect the following from the user:

---

## 4. How It Works

### Step 1: Gather Information

Collect the following from the user:

1. **Project Name**: The name of the project (e.g., "Redac Salesforce CRM")
2. **Requirements Source**: User stories, system flow diagrams, or requirement documents
3. **Test Categories**: Main categories (e.g., "Data Migration", "Business Scenarios", "Security")
4. **Priority Criteria**: Guidelines for assigning High/Medium/Low priorities (if not provided, use business criticality)

### Step 2: Analyze Requirements

Review the source material and:
- Identify main test categories and sub-categories
- Determine test scenarios for each category
- Group related test cases together
- Assign priorities based on business impact

### Step 3: Generate Test Cases

Create test cases with the following structure:

| Field | Description | Example |
|-------|-------------|---------|
| **テストケースID** | Unique ID (CATEGORY-###) | `DATA-001` |

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Creating UAT test case documents for Salesforce implementations
- Generating test cases based on system requirements or user stories
- Converting system flow diagrams or requirement documents into test cases
- Needing a standardized Excel format for UAT documentation with Japanese field names

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 1 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/uat-testcase-generator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: uat_best_practices.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: generate_uat_testcases.py.
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

- `skills/uat-testcase-generator/references/uat_best_practices.md`

**Scripts:**

- `skills/uat-testcase-generator/scripts/generate_uat_testcases.py`
