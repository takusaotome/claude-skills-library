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
- [technical-spec-writer]({{ '/en/skills/ops/technical-spec-writer/' | relative_url }}) -- IEEE 830 compliant technical specification writing
