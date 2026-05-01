---
layout: default
title: "Bug Ticket Creator"
grand_parent: English
parent: Project & Business
nav_order: 6
lang_peer: /ja/skills/management/bug-ticket-creator/
permalink: /en/skills/management/bug-ticket-creator/
---

# Bug Ticket Creator
{: .no_toc }

This skill should be used when creating bug/defect reports during system testing. Use this skill when you discover a bug, need to document test failures, or want to create comprehensive bug tickets with proper reproduction steps, severity assessment, and environment details. Guides users through interactive questioning to gather all necessary information and generates professional bug ticket documents in Markdown format. Supports Japanese (default) and English.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/bug-ticket-creator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/bug-ticket-creator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill transforms bug discoveries into comprehensive, professional bug tickets through interactive dialogue. It guides testers through systematic questioning to gather reproduction steps, environment details, severity assessment, and all necessary information, then generates a complete bug report in Markdown format.

**Primary language**: Japanese (default) with English support
**Use case**: Software testing, QA, bug reporting

---

## 2. Prerequisites

- Access to the system under test (to verify reproduction steps and environment details)
- Basic information about the bug (what happened, where, when)
- No special tools or dependencies required

---

## 3. Quick Start

1. **Initial Bug Discovery**: Capture what happened and where
2. **Reproduction Steps Collection**: Systematically gather step-by-step reproduction procedure
3. **Expected vs Actual Behavior**: Clarify the gap between specification and reality
4. **Environment Information Collection**: Gather OS, browser, device, and configuration details
5. **Severity and Priority Assessment**: Determine bug classification and urgency
6. **Bug Ticket Generation**: Create complete Markdown bug report document

---

## 4. How It Works

1. **Initial Bug Discovery**: Capture what happened and where
2. **Reproduction Steps Collection**: Systematically gather step-by-step reproduction procedure
3. **Expected vs Actual Behavior**: Clarify the gap between specification and reality
4. **Environment Information Collection**: Gather OS, browser, device, and configuration details
5. **Severity and Priority Assessment**: Determine bug classification and urgency
6. **Bug Ticket Generation**: Create complete Markdown bug report document

---

## 5. Usage Examples

- You discovered a bug during testing and need to create a bug ticket
- You want to ensure all necessary information is captured in the bug report
- You need help organizing reproduction steps systematically
- You want to determine appropriate severity and priority
- You need a professional, standardized bug report format

---

## 6. Understanding the Output

- A complete bug ticket as a Markdown file (`.md`)
- File name format: `BUG-[NUMBER]_[short-description]_[YYYY-MM-DD].md`
- Generated using templates from `assets/`

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/bug-ticket-creator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: reproduction_steps_guide.md, severity_priority_guide.md, defect_classification_guide.md.
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

---

## 10. Reference

**References:**

- `skills/bug-ticket-creator/references/defect_classification_guide.md`
- `skills/bug-ticket-creator/references/reproduction_steps_guide.md`
- `skills/bug-ticket-creator/references/severity_priority_guide.md`
