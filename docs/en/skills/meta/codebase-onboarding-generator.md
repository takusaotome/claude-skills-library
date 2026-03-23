---
layout: default
title: "Codebase Onboarding Generator"
grand_parent: English
parent: Meta & Quality
nav_order: 13
lang_peer: /ja/skills/meta/codebase-onboarding-generator/
permalink: /en/skills/meta/codebase-onboarding-generator/
---

# Codebase Onboarding Generator
{: .no_toc }

Automatically analyze a codebase and generate comprehensive CLAUDE.md documentation for future Claude Code sessions. Use when onboarding to a new project, creating project documentation, or generating AI coding assistant context files.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/codebase-onboarding-generator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/codebase-onboarding-generator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill analyzes a codebase to automatically generate comprehensive CLAUDE.md documentation. It identifies common commands, build processes, test patterns, directory structure conventions, and key architectural decisions. The generated documentation follows best practices for Claude Code onboarding and enables efficient AI-assisted development.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (pathlib, json, os, re)

---

## 3. Quick Start

```bash
python3 scripts/analyze_codebase.py \
  --path /path/to/project \
  --output analysis.json
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

- `skills/codebase-onboarding-generator/references/claude-md-best-practices.md`

**Scripts:**

- `skills/codebase-onboarding-generator/scripts/analyze_codebase.py`
