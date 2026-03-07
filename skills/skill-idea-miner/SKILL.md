---
name: skill-idea-miner
description: Mine Claude Code session logs for skill idea candidates. Use when running the skill generation pipeline to extract, score, and backlog new skill ideas from recent coding sessions.
---

# Skill Idea Miner

Automatically extract skill idea candidates from Claude Code session logs,
score them for novelty, feasibility, and work utility, and maintain a
prioritized backlog for downstream skill generation.

## When to Use

- Weekly automated pipeline run for skill idea generation
- Manual backlog refresh: `python3 scripts/mine_session_logs.py`
- Dry-run to preview candidates without LLM scoring

## Workflow

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
   - Work Utility (0-100): practical value for business professionals
   - Composite = 0.3 * Novelty + 0.3 * Feasibility + 0.4 * Work Utility
4. Merge scored candidates into `logs/.skill_generation_backlog.yaml`

## Output Format

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
ideas:
  - id: "idea_20260308_001"
    title: "Project Charter Generator"
    description: "Skill that generates project charters..."
    category: "project-management"
    scores: {novelty: 75, feasibility: 60, work_utility: 80, composite: 72.5}
    status: "pending"
```

## Resources

- `references/idea_extraction_rubric.md` -- Signal detection criteria and scoring rubric
- `scripts/mine_session_logs.py` -- Session log parser
- `scripts/score_ideas.py` -- Scorer and deduplicator
