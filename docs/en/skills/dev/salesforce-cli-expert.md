---
layout: default
title: "Salesforce CLI Expert"
grand_parent: English
parent: Software Development
nav_order: 26
lang_peer: /ja/skills/dev/salesforce-cli-expert/
permalink: /en/skills/dev/salesforce-cli-expert/
---

# Salesforce CLI Expert
{: .no_toc }

This skill should be used when generating Salesforce CLI commands for tasks like authenticating to orgs, querying data with SOQL, retrieving metadata (profiles, permission sets, security settings), deploying configuration changes, or automating security audits. Use when the user describes what they want to accomplish with Salesforce and needs the specific CLI command syntax.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/salesforce-cli-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/salesforce-cli-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill enables Claude to act as a Salesforce CLI expert, translating user requirements into precise `sf` CLI commands. It covers authentication, SOQL queries, metadata retrieval/deployment, and automation patterns specifically for security configuration management and org auditing.

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

Invoke this skill by describing your analysis needs to Claude.

---

## 4. How It Works

Follow the skill's SKILL.md workflow step by step, starting from a small validated input.

---

## 5. Usage Examples

- Asks how to perform a Salesforce operation via CLI
- Needs to retrieve security configurations (profiles, permission sets, org settings, sharing rules)
- Wants to query user data, roles, or permission assignments
- Needs to deploy security updates or configuration changes
- Asks for automation patterns (JSON output, bulk operations, CI/CD integration)
- Requests examples of specific `sf` or legacy `sfdx` commands

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 1 guide file(s).
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/salesforce-cli-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: Salesforce_CLI_Usage_Guide.md.
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

- `skills/salesforce-cli-expert/references/Salesforce_CLI_Usage_Guide.md`
