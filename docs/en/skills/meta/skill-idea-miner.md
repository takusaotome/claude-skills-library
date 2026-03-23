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

- `skills/skill-idea-miner/references/idea_extraction_rubric.md`

**Scripts:**

- `skills/skill-idea-miner/scripts/mine_session_logs.py`
- `skills/skill-idea-miner/scripts/score_ideas.py`
