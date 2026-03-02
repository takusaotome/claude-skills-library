---
layout: default
title: Getting Started
parent: English
nav_order: 1
lang_peer: /ja/getting-started/
permalink: /en/getting-started/
---

# Getting Started
{: .no_toc }

Install and start using Claude Skills in minutes.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Prerequisites

{: .prerequisite }
> - **Claude Code CLI** installed and authenticated ([Installation Guide](https://docs.anthropic.com/en/docs/claude-code))
> - A terminal with `bash` or `zsh`
> - Git (to clone the repository)

---

## 1. Clone the Repository

```bash
git clone https://github.com/takusaotome/claude-skills-library.git
cd claude-skills-library
```

---

## 2. Install a Skill

Copy the skill directory to your Claude skills folder:

```bash
cp -r ./skills/critical-code-reviewer ~/.claude/skills/
```

This installs the **critical-code-reviewer** skill. Replace the skill name with any skill from the [Skill Catalog]({{ '/en/skill-catalog/' | relative_url }}).

{: .warning }
> Do **not** place skill directories in `~/.claude/commands/`. That folder is only for `.md` slash-command files.

---

## 3. Verify Installation

Confirm the `SKILL.md` file exists:

```bash
ls ~/.claude/skills/critical-code-reviewer/SKILL.md
```

---

## 4. Use the Skill

Once installed, Claude Code **automatically detects** the skill and applies it when the context matches. For example:

```
> Review this Python file for bugs and code quality issues.
```

Claude will recognize the code-review context and activate the `critical-code-reviewer` skill, performing a multi-persona review covering bug hunting, clean code, TDD, and architecture perspectives.

---

## Installing Multiple Skills

You can install several skills at once:

```bash
for skill in critical-code-reviewer tdd-developer data-scientist markdown-to-pdf; do
  cp -r ./skills/$skill ~/.claude/skills/
done
```

---

## Uninstalling a Skill

Simply remove the skill directory:

```bash
rm -rf ~/.claude/skills/critical-code-reviewer
```

---

## Skill Structure

Every skill follows a consistent three-tier structure:

```
skill-name/
├── SKILL.md        # Main documentation (metadata + workflow)
├── scripts/        # Executable automation (Python/Bash)
├── references/     # Methodology guides loaded into context
└── assets/         # Templates used in output generation
```

- **SKILL.md** -- The entry point. Contains YAML front matter that tells Claude *when* to use the skill, plus detailed workflow instructions.
- **scripts/** -- Automation code that Claude can execute (e.g., `auto_eda.py`, `project_health_check.py`).
- **references/** -- Domain knowledge documents that Claude reads to inform its reasoning.
- **assets/** -- Templates and boilerplate that Claude uses when generating output.

---

## Next Steps

- Browse the [Skill Catalog]({{ '/en/skill-catalog/' | relative_url }}) to find skills for your workflow
- Read individual skill guides for detailed usage instructions
- Contribute your own skills -- see the repository README for development guidelines
