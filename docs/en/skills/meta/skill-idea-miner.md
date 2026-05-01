---
layout: default
title: "Skill Idea Miner"
grand_parent: English
parent: Meta & Quality
nav_order: 21
lang_peer: /ja/skills/meta/skill-idea-miner/
permalink: /en/skills/meta/skill-idea-miner/
---

# Skill Idea Miner
{: .no_toc }

Mine Claude Code session logs for skill idea candidates. Use when running the skill generation pipeline to extract, score, and backlog new skill ideas from recent coding sessions.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/skill-idea-miner.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/skill-idea-miner){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

# Skill Idea Miner

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

### Stage 1: Session Log Mining

1. Enumerate session logs from project directories in `~/.claude/projects/`
2. Filter to past 7 days by file mtime, confirm with `timestamp` field
3. Extract user messages (`type: "user"`, `userType: "external"`)
4. Extract tool usage patterns from assistant messages
5. Run deterministic signal detection:
   - Skill usage frequency (`skills/*/` path references)
   - Error patterns (non-zero exit codes, `is_error` flags, exception keywords)
   - Repetitive tool sequences (3+ tools repeated 3+ times)

---

## 4. How It Works

### Stage 1: Session Log Mining

1. Enumerate session logs from project directories in `~/.claude/projects/`
2. Filter to past 7 days by file mtime, confirm with `timestamp` field
3. Extract user messages (`type: "user"`, `userType: "external"`)
4. Extract tool usage patterns from assistant messages
5. Run deterministic signal detection:
   - Skill usage frequency (`skills/*/` path references)
   - Error patterns (non-zero exit codes, `is_error` flags, exception keywords)
   - Repetitive tool sequences (3+ tools repeated 3+ times)
   - Automation request keywords (English and Japanese)
   - Unresolved requests (5+ minute gap after user message)
6. Invoke Claude CLI headless for idea abstraction
7. Output `raw_candidates.yaml`

### Stage 2: Scoring and Deduplication

1. Load existing skills from `skills/*/SKILL.md` frontmatter
2. Deduplicate via Jaccard similarity (threshold > 0.5) against:
   - Existing skill names and descriptions
   - Existing backlog ideas
3. Score non-duplicate candidates with Claude CLI:
   - Novelty (0-100): differentiation from existing skills
   - Feasibility (0-100): technical implementability

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Weekly automated pipeline run for skill idea generation
- Manual backlog refresh: `python3 scripts/mine_session_logs.py`
- Dry-run to preview candidates without LLM scoring

---

## 6. Understanding the Output

### raw_candidates.yaml

```yaml
generated_at_utc: "2026-03-08T06:00:00Z"
lookback_days: 7
sessions_analyzed: 12
candidates:
  - id: "raw_20260308_001"
    title: "Project Charter Generator"
    scanned_projects: ["PycharmProjects-claude-skills-library"]
    description: "Generate project charters from requirements."
    category: "project-management"
```

### Backlog (logs/.skill_generation_backlog.yaml)

```yaml
updated_at_utc: "2026-03-08T06:15:00Z"

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/skill-idea-miner/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: idea_extraction_rubric.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: mine_session_logs.py, score_ideas.py.
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

- `skills/skill-idea-miner/references/idea_extraction_rubric.md`

**Scripts:**

- `skills/skill-idea-miner/scripts/mine_session_logs.py`
- `skills/skill-idea-miner/scripts/score_ideas.py`
