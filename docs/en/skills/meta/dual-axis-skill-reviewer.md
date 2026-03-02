---
layout: default
title: Dual-Axis Skill Reviewer
grand_parent: English
parent: Meta & Quality
nav_order: 1
lang_peer: /ja/skills/meta/dual-axis-skill-reviewer/
permalink: /en/skills/meta/dual-axis-skill-reviewer/
---

# Dual-Axis Skill Reviewer
{: .no_toc }

Reproducible quality scoring for Claude skills using deterministic checks and LLM deep review.
{: .fs-6 .fw-300 }

<span class="badge badge-scripts">Scripts</span> <span class="badge badge-workflow">Workflow</span>

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## Overview

Dual-Axis Skill Reviewer evaluates Claude skills through two complementary axes:

| Axis | Method | What It Checks |
|:-----|:-------|:---------------|
| **Auto Axis** | Deterministic Python script | Structure, metadata, scripts, tests, execution safety, artifact presence |
| **LLM Axis** | AI-powered deep review | Content quality, correctness, risk, missing logic, maintainability |

The final score is a weighted average of both axes. Skills scoring below 90 receive a list of concrete improvement items. This makes the reviewer ideal for quality gating in CI/CD pipelines or before merging skill PRs.

## When to Use

- You need **reproducible quality scoring** for any skill with a `SKILL.md`
- You want to **gate merges** with a minimum score threshold (e.g., 90+)
- You need **concrete improvement items** for low-scoring skills
- You want both **deterministic checks** (structure, tests) and **qualitative review** (content, logic)
- You need to review skills in a **different project** from where the reviewer is installed

## Prerequisites

- Python 3.9+
- `uv` (recommended) -- auto-resolves the `pyyaml` dependency via inline metadata
- For test execution: `uv sync --extra dev` or equivalent in the target project
- The `dual-axis-skill-reviewer` skill copied to `~/.claude/skills/` (or available in the same project)

No external API keys are required for the auto axis. The LLM axis uses Claude itself as the reviewer.

## How It Works

The review runs in three steps:

1. **Auto Axis + LLM Prompt Generation** -- the Python script (`run_dual_axis_review.py`) scans the skill directory, runs deterministic checks, scores 5 dimensions, and optionally generates a prompt for the LLM review.
2. **LLM Review** -- Claude reads the generated prompt, performs a deep content review, and produces a structured JSON response.
3. **Merge** -- the script merges auto and LLM scores using configurable weights (default 50/50) and produces the final report.

### Auto Axis Dimensions

The auto axis evaluates five areas:

- **Metadata** -- SKILL.md frontmatter completeness and correctness
- **Workflow Coverage** -- presence and quality of documented workflows
- **Execution Safety** -- script error handling, input validation
- **Artifact Presence** -- required directories (scripts/, references/, assets/)
- **Test Health** -- test files exist and pass

Knowledge-only skills (no scripts) receive adjusted expectations to avoid unfair penalties.

### Scoring

| Score | Meaning |
|:------|:--------|
| 90--100 | Production-ready, meets all quality standards |
| 70--89 | Functional but needs improvement in specific areas |
| Below 70 | Significant gaps requiring attention before merge |

## Usage Examples

### Example 1: Quick quality check on a single skill

```
Review the financial-analyst skill using dual-axis-skill-reviewer.
```

Claude runs the auto axis, performs the LLM review, merges the scores, and presents a report with the final score and any improvement items.

### Example 2: Review all skills with a score threshold

```
Run dual-axis-skill-reviewer on all skills in this project.
Flag any skill scoring below 90.
```

Claude iterates through `skills/*/SKILL.md`, scores each one, and produces a summary table highlighting skills that need attention.

### Example 3: Cross-project review

```
Review the skills in ~/other-project/ using dual-axis-skill-reviewer.
Use --project-root ~/other-project/ and save reports to ~/other-project/reports/.
```

Claude uses the `--project-root` flag to point the script at a different project directory.

## Tips & Best Practices

- **Start with auto axis only** (`--skip-tests` for speed) to get a quick structural assessment before investing in the full LLM review.
- **Adjust weights** depending on your priorities: increase `--auto-weight` for stricter structural gating, increase `--llm-weight` when content depth matters more.
- **Use `--seed`** for reproducible random skill selection during CI runs.
- **Review the generated prompt** before running the LLM step -- it provides full context on what will be evaluated.
- **Integrate into CI** -- use the JSON output to enforce a minimum score threshold on PRs that modify skills.

## Related Skills

- [Critical Code Reviewer]({{ '/en/skills/dev/critical-code-reviewer/' | relative_url }}) -- multi-persona code review for source files
- [Critical Document Reviewer]({{ '/en/skills/ops/critical-document-reviewer/' | relative_url }}) -- multi-persona document quality review
