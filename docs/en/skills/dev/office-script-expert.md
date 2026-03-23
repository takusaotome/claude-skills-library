---
layout: default
title: "Office Script Expert"
grand_parent: English
parent: Software Development
nav_order: 23
lang_peer: /ja/skills/dev/office-script-expert/
permalink: /en/skills/dev/office-script-expert/
---

# Office Script Expert
{: .no_toc }

Office Scripts (Excel Online / Microsoft 365) development expert skill. Covers platform limitations, ExcelScript API patterns, testing strategy (lib + Vitest), and 13 real-world bug patterns discovered during production development. Trigger words: Office Scripts, ExcelScript, Excel Online, Office Script development, TypeScript Excel, Excel automation, CalculateRequirements, ImportCsvData

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/office-script-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/office-script-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Office Scripts are TypeScript-based automation scripts for Excel on the web (Microsoft 365).
They are fundamentally different from VBA and Power Automate:

| Aspect | Office Scripts | VBA | Power Automate |
|--------|---------------|-----|----------------|
| Language | TypeScript (subset) | VBA | Low-code / expressions |
| Runtime | Server-side (Excel Online) | Client-side (Desktop) | Cloud service |
| Module system | **None** (no import/export) | Modules | Connectors |
| External libs | **Not available** | COM references | Connectors |
| Timeout | **120 seconds** | None | 30 min (premium) |
| Testing | Indirect (lib extraction) | Manual | Manual |

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

Invoke this skill by describing your analysis needs to Claude.

---

## 4. How It Works

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/office-script-expert/references/common_bug_patterns.md`
- `skills/office-script-expert/references/excel_api_patterns.md`
- `skills/office-script-expert/references/platform_limitations.md`
- `skills/office-script-expert/references/testing_strategy.md`
