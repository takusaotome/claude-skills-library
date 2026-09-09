# grill-me (chat edition)

A relentless, one-question-at-a-time interview skill for claude.ai / Claude app that sharpens
requirements, business plans, project plans, proposals, and raw ideas through
conversation, then writes the result up as a brief (summary + glossary + decision
log + open items).

Adapted from:
- `grilling` and `domain-modeling` by Matt Pocock — https://github.com/mattpocock/skills (MIT)
- `commands/clarify.md` by takusaotome — https://github.com/takusaotome/claude-skills-library

Changes for the chat environment: no repository, no CONTEXT.md/ADR files — the
glossary and decisions are collected during the interview and written into a
single brief at the end. Questions are asked one at a time via the tappable-options (ask-user) tool. The
design tree, the frontier, the recommended answer, and the `❓`/`➡️` text format come
from grilling — which asks the whole frontier in one numbered round, so asking one
question at a time is this adaptation's own change. The tappable-options
presentation, vagueness-detection patterns, options-with-tradeoffs style, decision
ledger columns, and progress checkpoint come from clarify. Sharpening fuzzy language,
challenging drift against the glossary, inventing concrete scenarios, the rule that a
glossary holds no implementation detail, and the test for which decisions are worth
recording — hard to reverse, non-obvious, or a real trade-off — come from
domain-modeling.

## Install (claude.ai)
Settings → Capabilities → Skills → upload the `.skill` / zip file.

## Files
- `SKILL.md` — the interview procedure
- `references/lenses.md` — question angles per subject type (要件 / 企画 / 計画 / アイデア / 提案)
- `references/output-format.md` — brief template
- `NOTICE` — upstream MIT copyright notice and permission text
