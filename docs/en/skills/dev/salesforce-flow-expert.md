---
layout: default
title: "Salesforce Flow Expert"
grand_parent: English
parent: Software Development
nav_order: 27
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
