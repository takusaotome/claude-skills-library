# Skill Structure Guide

## Directory Layout

Every skill follows this standardized three-tier structure:

```
<skill-name>/
├── SKILL.md              # Required: Skill definition with YAML frontmatter
├── scripts/              # Executable code (Python/Bash)
│   └── tests/            # Test files for scripts
├── references/           # Documentation loaded on-demand to inform decisions
└── assets/               # Templates and boilerplate files used in output
```

## Progressive Disclosure Pattern

1. **Metadata** (YAML frontmatter): When to use the skill — loads first for skill detection
2. **SKILL.md body**: Core workflows and instructions — loads when skill is invoked
3. **Resources**: Loaded on-demand as needed
   - `references/` — Documentation loaded into Claude's context to inform process and thinking (methodology guides, API references, schemas)
   - `scripts/` — Executable code that performs automation or data processing; may be executed without loading into context
   - `assets/` — Files not loaded into context, but used within Claude's output (templates, boilerplate code)

## SKILL.md Format

### YAML Frontmatter (Required — MUST be first)

**IMPORTANT**: SKILL.md must start with YAML frontmatter as the very first content. No title or text before the `---` delimiters.

```yaml
---
name: <skill-name>
description: <one-line trigger description>
---
```

- `name` MUST match the directory name exactly
- `description` defines when the skill should be triggered; keep it concise

**WRONG** (title before frontmatter):
```markdown
# Skill Name          <-- WRONG

---
name: skill-name
---
```

**CORRECT** (frontmatter first):
```markdown
---
name: skill-name
description: ...
---

# Skill Name
```

### Body Sections (Required)

1. **Overview** -- What the skill does (2-3 sentences)
2. **When to Use** -- Bullet list of trigger conditions
3. **Prerequisites** -- Python version, API keys, dependencies
4. **Workflow** -- Step-by-step execution instructions (imperative form)
5. **Output Format** -- JSON and/or Markdown report structure
6. **Resources** -- List of reference files and scripts

## Writing Style

- Use imperative/infinitive verb forms: "Analyze the chart", "Generate report"
- Write instructions for Claude to execute, NOT user instructions
- Avoid "You should..." or "Claude will..." -- state actions directly
- Include concrete bash command examples with full paths

## Naming Conventions

- Directory name: lowercase, hyphen-separated (e.g., `position-sizer`)
- SKILL.md frontmatter `name:` must match directory name
- Scripts: `snake_case.py` (e.g., `check_data_quality.py`)

## Resource Path Convention

**IMPORTANT**: Always use relative paths when referencing resources within a skill.

- In SKILL.md: Use `references/...` and `assets/...` (relative to skill directory)
- In command files: Use `references/...` and `assets/...` (relative to skill directory)
- **DO NOT** use repo-relative paths like `skills/skill-name/references/...` — these won't resolve when installed to `~/.claude/skills/`

## Script Requirements

- Check for API keys before making requests
- Validate date ranges and input parameters
- Provide helpful error messages to stderr
- Return proper exit codes (0 success, 1 error)
- Support retry logic with exponential backoff for rate limits
- Use relative paths or dynamic resolution (no hardcoded absolute paths)

## Reference Document Patterns

- Use declarative statements of fact
- Include historical examples and case studies where applicable
- Provide decision frameworks and checklists
- Organize hierarchically (H2 for major sections, H3 for subsections)
