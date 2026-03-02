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

<span class="badge badge-scripts">Scripts</span>
<span class="badge badge-workflow">Workflow</span>

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

The review runs in three steps, each building on the previous output.

### Step 1: Auto Axis + LLM Prompt Generation

The Python script (`run_dual_axis_review.py`) scans the target skill directory and runs deterministic checks across 5 dimensions. It produces a JSON score file and, when `--emit-llm-prompt` is set, a Markdown prompt file for the next step.

The script selects a skill randomly by default. Use `--skill <name>` for a fixed target or `--all` to review every skill in the project.

### Step 2: LLM Review

Claude (or another LLM) reads the generated prompt and performs a deep content review. The output must be a structured JSON object following the schema in `references/llm_review_schema.md`:

```json
{
  "score": 85,
  "summary": "one-paragraph assessment",
  "findings": [
    {
      "severity": "high",
      "path": "skills/example/scripts/main.py",
      "line": 42,
      "message": "Unchecked file open without error handling",
      "improvement": "Wrap in try/except and log the error"
    }
  ]
}
```

When running inside Claude Code, Claude acts as both orchestrator and reviewer -- it reads the prompt, produces the JSON, and saves it for the merge step.

### Step 3: Merge

The script merges auto and LLM scores using configurable weights (default 50/50). It produces a final JSON report and a human-readable Markdown report. If the final score is below 90, improvement items from both axes are consolidated and listed.

### Auto Axis: 5-Dimension Scoring Detail

The auto axis evaluates five areas, each with a specific weight reflecting its importance to skill quality.

| Dimension | Weight | What It Measures |
|:----------|:-------|:-----------------|
| **Metadata & Use Case** | 20 pts | SKILL.md frontmatter completeness: `name`, `description` fields exist and are informative. Clear trigger conditions so Claude can invoke the skill correctly. |
| **Workflow Coverage** | 25 pts | Presence and quality of documented workflows: step-by-step sections, input/output specifications, and concrete examples. Missing core sections create ambiguity in real use. |
| **Execution Safety & Reproducibility** | 25 pts | Command examples use correct syntax, paths are relative (not hardcoded), scripts handle errors gracefully, and results are reproducible across environments. |
| **Supporting Artifacts** | 10 pts | Required directories exist (`scripts/`, `references/`, `assets/`) and contain meaningful content. Lower weight because artifacts support but do not define skill quality. |
| **Test Health** | 20 pts | Test files exist under `scripts/tests/`, and they pass when executed. Runtime confidence is critical -- passing tests strongly increase trust in automation. |

**Total: 100 points.** The auto axis score is a direct sum of all dimension scores.

**Knowledge-only skill handling:** Skills without executable scripts (no `scripts/*.py`) are classified as `knowledge_only`. Script-related checks (`supporting_artifacts`, `test_health`) are adjusted so that missing scripts/tests do not penalize the score unfairly. The skill must still have clear `When to Use`, `Prerequisites`, and workflow structure.

### LLM Axis Scoring

The LLM axis scores the skill on a 0--100 scale, focusing on:

- **Correctness** -- do the instructions and scripts actually do what they claim?
- **Risk** -- are there security, data-loss, or reliability risks?
- **Missing logic** -- are there edge cases or error paths not covered?
- **Maintainability** -- is the skill easy to update, extend, and debug?

Each finding includes a severity (high / medium / low), the affected file and line, a problem statement, and an actionable improvement suggestion.

### Final Score Calculation

```
Final Score = (Auto Score x auto_weight) + (LLM Score x llm_weight)
```

Default weights: `auto_weight = 0.5`, `llm_weight = 0.5`. Adjust via CLI flags.

### Score Thresholds

| Score | Meaning | Action |
|:------|:--------|:-------|
| 90--100 | Production-ready | Merge-safe; meets all quality standards |
| 80--89 | Usable | Targeted improvements recommended |
| 70--79 | Notable gaps | Strengthen before regular use |
| Below 70 | High risk | Treat as draft; prioritize fixes before merge |

When the final score is below 90, improvement items are **mandatory** in the report output.

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

### Example 4: Auto axis only for quick triage

```
Run a quick structural check on the bug-ticket-creator skill.
Skip tests and skip the LLM review -- just the auto axis.
```

Claude runs the script with `--skip-tests` and without `--emit-llm-prompt`, producing a fast structural score in seconds.

## CI/CD Integration

The dual-axis reviewer can be integrated into automated pipelines to enforce quality gates on skill PRs.

### GitHub Actions Example

```yaml
name: Skill Quality Gate
on:
  pull_request:
    paths:
      - 'skills/**'

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Run auto axis review
        run: |
          uv run skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
            --project-root . \
            --all \
            --skip-tests \
            --output-dir reports/

      - name: Check minimum score
        run: |
          python3 -c "
          import json, glob, sys
          for f in glob.glob('reports/skill_review_*.json'):
              data = json.load(open(f))
              score = data.get('auto_score', 0)
              name = data.get('skill_name', f)
              print(f'{name}: {score}')
              if score < 70:
                  print(f'FAIL: {name} scored {score} (minimum: 70)')
                  sys.exit(1)
          print('All skills passed minimum threshold.')
          "
```

### Key integration patterns

- **PR gate (auto axis only)**: Run `--all --skip-tests` on every PR that touches `skills/`. Fast and deterministic -- completes in seconds.
- **Nightly full review**: Run the full 3-step workflow (auto + LLM + merge) on a schedule. Use `--seed $(date +%j)` for reproducible daily selection.
- **Pre-release audit**: Run `--all` with both axes before tagging a release. Require a minimum final score of 90 for all skills.
- **JSON output for automation**: Parse the `skill_review_*.json` files programmatically to track scores over time or post results as PR comments.

## Troubleshooting

### Script fails with "No skills found"

**Symptom**: The script exits with an error saying no skills were found in the project.

**Solution**: Verify that `--project-root` points to a directory containing a `skills/` subdirectory with at least one skill. Each skill must have a `SKILL.md` file. Check the path with `ls <project-root>/skills/*/SKILL.md`.

### LLM merge fails with schema validation error

**Symptom**: The merge step rejects the LLM review JSON with a validation error.

**Solution**: Ensure the JSON follows the required schema exactly: top-level `score` (integer 0--100), `summary` (string), and `findings` (array of objects with `severity`, `path`, `line`, `message`, `improvement`). The `line` field can be `null` but must be present. Do not wrap the JSON in a Markdown code block.

### Test health score is 0 despite having tests

**Symptom**: The auto axis reports test health as 0 even though test files exist.

**Solution**: The script looks for test files matching `scripts/tests/test_*.py`. Ensure your test files follow this naming convention and are located in the `scripts/tests/` subdirectory (not `tests/` at the skill root). Also verify that tests pass when run manually with `uv run pytest skills/<skill-name>/scripts/tests/ -v`.

## Tips & Best Practices

- **Start with auto axis only** (`--skip-tests` for speed) to get a quick structural assessment before investing in the full LLM review.
- **Adjust weights** depending on your priorities: increase `--auto-weight` for stricter structural gating, increase `--llm-weight` when content depth matters more.
- **Use `--seed`** for reproducible random skill selection during CI runs.
- **Review the generated prompt** before running the LLM step -- it provides full context on what will be evaluated.
- **Integrate into CI** -- use the JSON output to enforce a minimum score threshold on PRs that modify skills.

## Related Skills

- [Critical Code Reviewer]({{ '/en/skills/dev/critical-code-reviewer/' | relative_url }}) -- multi-persona code review for source files
- [Critical Document Reviewer]({{ '/en/skills/ops/critical-document-reviewer/' | relative_url }}) -- multi-persona document quality review
