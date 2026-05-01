---
layout: default
title: "Email Triage Responder"
grand_parent: English
parent: Meta & Quality
nav_order: 25
lang_peer: /ja/skills/meta/email-triage-responder/
permalink: /en/skills/meta/email-triage-responder/
---

# Email Triage Responder
{: .no_toc }

Analyze inbox emails to identify action-required items, prioritize by urgency / importance, classify by topic, and draft contextual replies. Tracks response status across the lifecycle.
{: .fs-6 .fw-300 }

<span class="badge badge-free">gogcli / Outlook MCP</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/email-triage-responder.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/email-triage-responder){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Pulls unread emails (Gmail via gogcli or Outlook via MCP), scores urgency/importance, classifies into 8 topic categories, places each into an Eisenhower-Matrix quadrant (Q1-Q4), drafts contextual replies in the source language/tone, and tracks response state (pending → draft_ready → sent → delegated → archived).

---

## 2. Prerequisites

- Python 3.9+
- gogcli (for Gmail) または Outlook MCP server
- No API keys beyond email access

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=email-triage-responder

# Or fetch the .skill package
curl -L -o email-triage-responder.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/email-triage-responder.skill
```

Then trigger the skill in Claude Code by describing what you want — see the **Usage Examples** section below for trigger phrases.

---

## 4. How It Works

The skill follows the workflow documented in its `SKILL.md`. Key stages:

1. **Input parsing** — interprets the user request and any provided source files.
2. **Core processing** — applies the skill's domain logic (see Reference section).
3. **Output generation** — produces structured artifacts (markdown / JSON / templates) ready for downstream use.

For the authoritative step-by-step procedure, open `skills/email-triage-responder/SKILL.md`.

---

## 5. Usage Examples

- You need to triage a backlog of unread emails by what truly needs action
- You want bilingual (JA/EN) draft responses generated from context
- You want a single dashboard of pending → sent → archived email states
- You're processing emails in bulk with consistent prioritization rules

---

## 6. Understanding the Output

The skill produces structured output following the conventions in its templates and reference docs (see Section 10). Outputs are:

- **Reproducible** — identical input + same templates → same output structure.
- **Reviewable** — each section is labeled and ordered consistently.
- **Composable** — outputs of this skill can feed adjacent skills (see Section 8).

---

## 7. Tips & Best Practices

- Start with a small, realistic input to validate the workflow before scaling.
- Keep `skills/email-triage-responder/SKILL.md` open alongside this guide; it remains the authoritative source.
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

- `skills/email-triage-responder/references/email-classification.md`
- `skills/email-triage-responder/references/response-templates.md`

**Scripts:**

- `skills/email-triage-responder/scripts/triage_emails.py`

**Assets:**

_(none)_
