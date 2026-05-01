---
layout: default
title: "Design Implementation Reviewer"
grand_parent: English
parent: Software Development
nav_order: 15
lang_peer: /ja/skills/dev/design-implementation-reviewer/
permalink: /en/skills/dev/design-implementation-reviewer/
---

# Design Implementation Reviewer
{: .no_toc }

Use this skill for critical code review that focuses on whether the code actually works correctly and achieves the expected results - not just whether it matches a design document. This skill assumes designs can be wrong, finds bugs the design didn't anticipate, and verifies end-to-end correctness. Triggers include "critical code review", "deep code review", "verify this implementation works", "find bugs in this code", or reviewing implementation against requirements. NOTE - Security review is OUT OF SCOPE; use a dedicated security review skill for that purpose.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/design-implementation-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/design-implementation-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

# Critical Code Reviewer

---

## 2. Prerequisites

Before using this skill:
1. Have the code to review available (file paths or code snippets)
2. Understand the expected outcome or requirements (even if informal)
3. Access to sample data if validating data processing logic (recommended)

---

## 3. Quick Start

1. **Preparation**: Read required references (`references/review_checklist.md`, `references/common_gaps.md`)
2. **Define Expected Result**: Clarify input → output → success criteria before diving into code
3. **Layer 1 Review**: Code Quality (type safety, null handling, edge cases, logic, exceptions)
4. **Layer 2 Review**: Execution Flow (function wiring, data flow, joins, concurrency, resources)
5. **Layer 3 Review**: Goal Achievement (real data validation, success rate, end-to-end trace)
6. **Document Findings**: Structure output as Scope/Assumptions → Findings (by severity) → Open Questions
7. **Verify Test Plans**: Ensure Critical/High findings include specific test plans

---

## 4. How It Works

1. **Preparation**: Read required references (`references/review_checklist.md`, `references/common_gaps.md`)
2. **Define Expected Result**: Clarify input → output → success criteria before diving into code
3. **Layer 1 Review**: Code Quality (type safety, null handling, edge cases, logic, exceptions)
4. **Layer 2 Review**: Execution Flow (function wiring, data flow, joins, concurrency, resources)
5. **Layer 3 Review**: Goal Achievement (real data validation, success rate, end-to-end trace)
6. **Document Findings**: Structure output as Scope/Assumptions → Findings (by severity) → Open Questions
7. **Verify Test Plans**: Ensure Critical/High findings include specific test plans

---

## 5. Usage Examples

- Performing **critical code review** focusing on correctness and bug detection
- Verifying that implementation **actually works** (not just matches design docs)
- Conducting **deep code review** to find logic errors and edge cases
- Reviewing implementation against requirements with skepticism
- Investigating whether code achieves expected results with real data

---

## 6. Understanding the Output

This skill provides **conversational guidance** - no files are generated. Output includes:
- Structured review findings (Critical/High/Medium/Low severity)
- Code snippets highlighting problems
- Root cause analysis and fix recommendations
- Test plans for Critical/High findings
- Design gap identification

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/design-implementation-reviewer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: common_gaps.md, review_checklist.md.
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

---

## 10. Reference

**References:**

- `skills/design-implementation-reviewer/references/common_gaps.md`
- `skills/design-implementation-reviewer/references/review_checklist.md`
