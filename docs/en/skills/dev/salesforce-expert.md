---
layout: default
title: "Salesforce Expert"
grand_parent: English
parent: Software Development
nav_order: 27
lang_peer: /ja/skills/dev/salesforce-expert/
permalink: /en/skills/dev/salesforce-expert/
---

# Salesforce Expert
{: .no_toc }

Expert guidance for Salesforce system development and operations management. Use this skill when working with Salesforce configuration, customization, bug analysis, troubleshooting access/permission issues, designing system architecture, or implementing custom Apex/LWC development. Covers sharing settings, approval processes, trigger patterns, integration design, and data modeling best practices.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/salesforce-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/salesforce-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides comprehensive guidance for Salesforce system development and operations management, covering configuration, customization, bug analysis, architecture design, and custom development patterns. Use this skill when encountering Salesforce-specific challenges, designing solutions, or troubleshooting issues related to permissions, approval processes, integrations, or custom code.

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

When analyzing Salesforce bugs, follow this systematic approach:

### 1. Gather Context
- Record type and object involved
- User role and profile
- Error message (exact wording)
- Steps to reproduce
- Expected vs actual behavior

---

## 4. How It Works

When analyzing Salesforce bugs, follow this systematic approach:

### 1. Gather Context
- Record type and object involved
- User role and profile
- Error message (exact wording)
- Steps to reproduce
- Expected vs actual behavior

### 2. Categorize Issue
- **Access/Permissions**: Cannot view/edit records
- **Data Integrity**: Missing relationships, incorrect calculations
- **Process Automation**: Approval, workflow, validation errors
- **Integration**: API failures, callout errors
- **UI/UX**: Page layout, Lightning component issues

### 3. Diagnose Root Cause

**For Access Issues**:
1. Check OWD: Setup → Sharing Settings → Object Default Access
2. Check Record Ownership: Who owns the record?
3. Check Role Hierarchy: Is user above owner?
4. Check Sharing Rules: Any applicable rules?
5. Check Manual Shares: Query [Object]Share records

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- **Settings & Customization**: Configuring sharing settings, approval processes, validation rules, page layouts, or record types
- **Bug Analysis & Troubleshooting**: Diagnosing access denied issues, approval process errors, missing relationships, or integration failures
- **Architecture Design**: Planning data models, object relationships, integration patterns, or scalability strategies
- **Custom Development**: Implementing Apex triggers, batch jobs, Lightning Web Components, or REST APIs
- **Security & Permissions**: Resolving OWD settings, sharing rules, role hierarchy, or field-level security issues
- **Performance Optimization**: Addressing governor limit issues, slow queries, or large data volume challenges

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 4 guide file(s).
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/salesforce-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: approval_process_guide.md, architecture_best_practices.md, custom_development_patterns.md.
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

---

## 10. Reference

**References:**

- `skills/salesforce-expert/references/approval_process_guide.md`
- `skills/salesforce-expert/references/architecture_best_practices.md`
- `skills/salesforce-expert/references/custom_development_patterns.md`
- `skills/salesforce-expert/references/sharing_settings_guide.md`
