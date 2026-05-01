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

### Step 1: Analyze Codebase Structure

Run the codebase analyzer to detect project type, directory structure, and key files.

```bash
python3 scripts/analyze_codebase.py \
  --path /path/to/project \
  --output analysis.json
```

The analyzer detects:
- Project type (Python, Node.js, Java, Go, Rust, etc.)
- Package manager and dependency files
- Build and test configuration
- Directory conventions (src/, lib/, tests/, etc.)
- Key configuration files (.gitignore, CI configs, etc.)

### Step 2: Extract Common Commands

Parse package.json, Makefile, pyproject.toml, or other build files to extract:
- Build commands
- Test commands
- Lint/format commands
- Development server commands

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Setting up Claude Code for a new project that lacks CLAUDE.md
- Generating initial project documentation for AI assistants
- Refreshing outdated CLAUDE.md files after significant project changes
- Creating standardized onboarding documentation for team codebases
- Analyzing unfamiliar codebases to understand structure and conventions

---

## 6. Understanding the Output

### JSON Analysis Report

```json
{
  "schema_version": "1.1",
  "project_name": "example-project",
  "project_type": "python",
  "detected_at": "2024-01-15T10:30:00Z",
  "structure": {
    "root_files": ["README.md", "pyproject.toml", ".gitignore"],
    "directories": {
      "src": "Source code",
      "tests": "Test files",
      "docs": "Documentation"
    }
  },
  "commands": {
    "build": ["pip install -e ."],

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/codebase-onboarding-generator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: claude-md-best-practices.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: analyze_codebase.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).
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

- `skills/codebase-onboarding-generator/references/claude-md-best-practices.md`

**Scripts:**

- `skills/codebase-onboarding-generator/scripts/analyze_codebase.py`
