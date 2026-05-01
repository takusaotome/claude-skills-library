---
layout: default
title: "Action Status Updater"
grand_parent: English
parent: Meta & Quality
nav_order: 24
lang_peer: /ja/skills/meta/action-status-updater/
permalink: /en/skills/meta/action-status-updater/
---

# Action Status Updater
{: .no_toc }

Track and update action item status from natural language updates like "Seanのメールには返信しておいた" or "Lu対応予定". Integrates with daily-comms-ops workflow.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/action-status-updater.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/action-status-updater){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Parses Japanese and English natural-language status updates, extracts intent (completed/delegated/deferred/in-progress) plus owner/channel/keyword, and persists state to YAML for later reporting.

---

## 2. Prerequisites

- Python 3.9+
- PyYAML
- No API keys required

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=action-status-updater

# Or fetch the .skill package
curl -L -o action-status-updater.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/action-status-updater.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/action-status-updater/SKILL.md`.

---

## 5. Usage Examples

- You log status updates in mixed JP/EN like "Seanにフォローした" / "Lu対応予定"
- You want a single source of truth for action items across Slack/email/meetings
- You need a daily/weekly status report from those NL notes
- You're running a daily-comms-ops loop and want it to feed your action tracker

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/action-status-updater/SKILL.md` open alongside this guide; it remains the authoritative source.
- Read the most relevant reference file first (see Section 10) instead of trying to absorb all of them.
- Run scripts on test data before applying to production-bound inputs.
- Preserve intermediate outputs so you can explain assumptions and trace decisions.

---

## 8. Combining with Other Skills

- Pair with adjacent skills in the same category to cover the planning → execution → review arc.
- Browse the Meta & Quality category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).
- See the full English skill catalog: [skill catalog]({{ '/en/skill-catalog/' | relative_url }}).

---

## 9. Troubleshooting

- Re-check prerequisites first; missing runtime dependencies are the most common failure mode.
- Run helper scripts on a minimal input before applying them to a full dataset.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata.
- Confirm Python version (3.9+) and required packages are installed in the active environment.
- When output looks incomplete, re-read the relevant reference file to verify the input contract.

---

## 10. Reference

**References:**

- `skills/action-status-updater/references/integration_guide.md`
- `skills/action-status-updater/references/status_patterns.md`

**Scripts:**

- `skills/action-status-updater/scripts/action_status_updater.py`
- `skills/action-status-updater/scripts/nl_parser.py`

**Assets:**

_(none)_
