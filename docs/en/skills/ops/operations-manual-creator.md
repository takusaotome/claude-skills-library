---
layout: default
title: Operations Manual Creator
grand_parent: English
parent: Operations & Docs
nav_order: 2
lang_peer: /ja/skills/ops/operations-manual-creator/
permalink: /en/skills/ops/operations-manual-creator/
---

# Operations Manual Creator
{: .no_toc }

Create structured, professional operations manuals using the STEP format with ANSI Z535-inspired safety labels.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-workflow">Workflow</span>
<span class="badge badge-bilingual">Bilingual</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Operations Manual Creator produces complete, ready-to-use operations manuals for business systems. Each procedure step follows the STEP format (Specific/Target/Expected/Proceed), ensuring consistency and clarity. Caution and warning labels follow an ANSI Z535-inspired classification system (DANGER/WARNING/CAUTION/NOTE), and every manual includes a comprehensive troubleshooting guide with escalation paths.

Output is available in both Japanese and English, suitable for enterprise environments.

---

## When to Use

- Creating operations manuals for business systems
- Writing standard operating procedures (SOPs)
- Building system administration guides
- Producing user guides for end-users
- Documenting work procedures for onboarding

---

## Prerequisites

- **Claude Code** installed and running
- **operations-manual-creator** skill installed (`cp -r ./skills/operations-manual-creator ~/.claude/skills/`)
- No external APIs or additional tools required

---

## How It Works

The skill follows a 6-step workflow:

1. **Scope & Audience Definition** -- Clarify the target system, operations to cover, and audience skill level (Beginner/Intermediate/Advanced)
2. **Operations Inventory** -- List and categorize all operations with IDs (OP-001, OP-002, ...), frequency, role, dependencies, and estimated time
3. **Procedure Writing** -- Write each operation using the STEP format:
   - **S**pecific: What exactly to do (precise action verbs)
   - **T**arget: Which UI element (button name, menu path)
   - **E**xpected: What should happen after the step
   - **P**roceed: How to confirm success and move on
4. **Caution/Warning Labels** -- Apply ANSI Z535-inspired classifications (DANGER/WARNING/CAUTION/NOTE) before relevant steps, always including the consequence of ignoring the warning
5. **Troubleshooting Guide** -- Create Symptom-Cause-Resolution tables, decision trees, and three-tier escalation paths (L1 Self-service, L2 Helpdesk, L3 Engineering)
6. **Assembly & Review** -- Assemble all components into the final template, generate a table of contents, and run a quality checklist

### STEP format detailed example

Each procedure step is written using the four STEP components. Here is a concrete example for a user account creation operation:

| STEP | Content |
|:-----|:--------|
| **S**pecific | Click the "Add New User" button |
| **T**arget | Top-right corner of the User Management screen (Menu > Administration > User Management) |
| **E**xpected | The "New User Registration" modal dialog opens with empty fields for Name, Email, and Role |
| **P**roceed | Confirm the modal is displayed and the cursor is in the Name field, then go to Step 2 |

A complete procedure uses numbered main steps (1, 2, 3...), sub-steps (1.1, 1.2...) for detailed actions within a step, and conditional branches (1a, 1b) when the flow diverges based on a condition. Every step includes a screenshot placeholder `[Screenshot: {description}]` to mark where actual images should be inserted later.

### ANSI Z535 safety label reference

The skill uses an ANSI Z535-inspired classification to apply consistent caution and warning labels throughout the manual:

| Level | Color | When to Use | Example |
|:------|:------|:------------|:--------|
| **DANGER** | Red | Risk of irreversible data destruction or account termination | "DANGER: Clicking 'Delete All Records' permanently removes all data. This action cannot be undone." |
| **WARNING** | Orange | Changes affecting all users, bulk operations, permission escalation | "WARNING: Changing the authentication method will force all 500 users to re-login immediately." |
| **CAUTION** | Yellow | Risk of unexpected results, unsaved data loss, long-running processes | "CAUTION: This report generation may take up to 30 minutes. Do not close the browser tab." |
| **NOTE** | Blue | Helpful tips, best practices, access requirements | "NOTE: You need the Admin role to access this screen. Contact IT if you lack permissions." |

Labels are always placed **before** the step they relate to, and each label includes the consequence of ignoring it.

### Operations inventory structure

Before writing procedures, the skill creates a comprehensive inventory table:

| OP-ID | Operation Name | Category | Frequency | Target Role | Est. Time | Prerequisites |
|:------|:---------------|:---------|:----------|:------------|:----------|:--------------|
| OP-001 | Create user account | User Management | Ad-hoc | Admin | 5 min | -- |
| OP-002 | Assign role permissions | User Management | Ad-hoc | Admin | 3 min | OP-001 |
| OP-003 | Daily batch export | Data Export | Daily | Operator | 10 min | -- |

This inventory drives the order and grouping of procedures in the final manual.

---

## Usage Examples

### Example 1: Inventory management system manual

```
Create an operations manual for our inventory management system.
Target audience: warehouse staff with low IT literacy.
Cover receiving, shipping, and stocktaking operations.
```

The skill will define scope, inventory all operations, write STEP-format procedures with screenshot placeholders, add appropriate warnings (e.g., WARNING for irreversible shipping confirmation), and include troubleshooting for barcode reader errors.

### Example 2: CRM admin SOP

```
Create a user management SOP for our CRM admin panel.
Operations: add user, change permissions, disable account.
Target: IT administrators.
```

The skill will produce individual procedure documents with STEP-format steps, WARNING labels for admin privilege assignments, and NOTE labels for password policy reminders.

### Example 3: Quick-start guide

```
Create a quick-start guide for new employees using our expense reporting system.
Focus on the 5 most common operations only.
```

The skill will select the essential operations, write beginner-friendly procedures with detailed UI navigation, and include a FAQ-style troubleshooting section.

### Example 4: System admin runbook

```
Create an operations runbook for our PostgreSQL database.
Target: infrastructure team (advanced).
Cover backup, restore, failover, and performance monitoring.
```

The skill will produce advanced-level procedures focused on edge cases and configuration, with DANGER labels for destructive operations like manual failover, and a decision tree for troubleshooting replication lag.

---

## Troubleshooting

### Steps are too vague

**Symptom**: Generated procedures use phrases like "configure the settings appropriately" or "set values as needed" without specifying exact actions.

**Solution**: The skill prohibits ambiguous language by design. If vague steps appear, provide more context about the system (screen names, field labels, exact menu paths). The skill will then produce precise STEP-format instructions. You can also prompt with "Rewrite this step using the STEP format with exact UI element names."

### Too many WARNING labels

**Symptom**: Almost every step has a WARNING or CAUTION label, which dilutes their importance and makes the manual feel alarmist.

**Solution**: Review the labels against the ANSI Z535 classification criteria. DANGER and WARNING should be reserved for truly consequential actions (data destruction, bulk changes). Routine precautions should use NOTE (blue). Ask the skill to "Review and downgrade labels that do not involve irreversible consequences."

### Manual is too long for the audience

**Symptom**: The generated manual is hundreds of pages long and the target audience (e.g., general users) only needs a subset.

**Solution**: Use the quick-start guide scope option in Workflow 1. Specify "quick-start guide" to limit output to the 5-10 most common operations. For comprehensive manuals, consider splitting into role-based volumes (Admin Guide, User Guide, Operator Guide) by specifying the target role during scope definition.

---

## Tips & Best Practices

- **One step = one action**: Complex operations are decomposed into individual actions. Never combine multiple clicks or inputs into a single step.
- **Be precise with UI elements**: Use exact names like "the blue Save button at the top right," not vague references like "save it."
- **Warnings before steps**: DANGER/WARNING/CAUTION/NOTE labels are always placed before the step they relate to, never after.
- **Screenshot placeholders**: The skill includes `[Screenshot: {description}]` markers so you can insert actual images later.
- **Avoid ambiguity**: Phrases like "as appropriate" or "if necessary" are prohibited. Every condition is made explicit.

---

## Related Skills

- [incident-rca-specialist]({{ '/en/skills/ops/incident-rca-specialist/' | relative_url }}) -- Post-incident review and root cause analysis
- [markdown-to-pdf]({{ '/en/skills/ops/markdown-to-pdf/' | relative_url }}) -- Convert the generated manual to professional PDF
- **technical-spec-writer** -- IEEE 830 compliant technical specification writing
