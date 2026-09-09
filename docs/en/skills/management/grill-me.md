---
layout: default
title: "Grill Me"
grand_parent: English
parent: Project & Business
nav_order: 31
lang_peer: /ja/skills/management/grill-me/
permalink: /en/skills/management/grill-me/
---

# Grill Me
{: .no_toc }

A relentless one-question-at-a-time interview that sharpens a requirement, plan, proposal, or raw idea, then writes it up as a brief.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/grill-me.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/grill-me){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

The user has a picture in their head that is fuzzier than they think. This skill finds the fuzz by interviewing them — one question at a time, each with a recommended answer — until both sides share the same understanding of what is actually being proposed. It then writes that understanding down as a brief.

The subject is conversational, not a document: requirements, a business or product plan, a project plan, a proposal, a rough idea. Nothing needs to exist in writing beforehand.

Two rules carry most of the value:

**One question per turn.** A wall of five numbered questions gets skimmed and answered shallowly, especially on a phone. One question with tappable options gets a real decision in three seconds, and each answer reshapes what the next question should be.

**Every question comes with a recommendation.** A question without one is homework. A question with one is a decision the user can accept instantly, and it exposes the assumption so they can correct it.

---

## 2. When to Use

- The user says "grill me", "grill this", "clarify", 「詰めて」, 「詰めたい」, 「壁打ち」, 「要件を固めたい」, 「企画を練りたい」, 「計画を整理したい」, 「アイデアをぶつけたい」, 「突っ込んで」, 「質問して」, or 「何が決まってないか教えて」
- They want their thinking stress-tested before they commit to it
- They describe a plan or idea vaguely and ask what to do next
- They are about to write a spec, a proposal, or a deck and the inputs are not pinned down yet

**Not this skill:** reviewing a finished document — use `critical-document-reviewer` — or answering a question the user actually wants answered rather than interrogated.

---

## 3. Prerequisites

- **API Key:** None required
- No scripts or dependencies — the skill is instructions only
- Works best where a tappable-options tool is available; falls back to a plain-text question format where it is not

---

## 4. Quick Start

Describe the thing and ask to be grilled:

```
新しい社内ツールの企画を考えてる。詰めて。
```

```
Grill me on this project plan before I take it to the client.
```

The interview starts immediately. Answer by tapping an option or by typing — a typed answer that fits no option is recorded verbatim.

---

## 5. How It Works

The subject is modelled as a **design tree**. The root is the goal; every decision branches into the decisions that hang off it. Most of the tree is invisible at the start, and questions reveal it.

The **frontier** is every decision whose prerequisites are already settled — the questions that can be asked *now* without guessing at answers not yet heard. The skill computes the whole frontier, asks the single question that unblocks the most of the tree, then stops. When the answer arrives it recomputes: settled decisions unlock new questions, some branches die, contradictions surface.

A question whose answer depends on one still open is never asked, and the skill never answers its own question and moves on.

### Facts versus decisions

Facts are the skill's job; decisions are the user's. When a question hinges on something knowable — market size, what a competitor does, whether an API supports X, a regulation, a price — it gets looked up rather than asked. Facts about the user's own world (headcount, budget, what the boss said) are theirs to give.

### Checkpoint

After roughly eight to ten questions, or once the remaining frontier is only minor detail, the skill asks whether to continue or finalize with what it has. Either answer is fine; the point is that the user decides how deep to go.

---

## 6. Where It Looks for Fuzz

Each pattern below is a question waiting to happen.

| Pattern | Examples | The question it raises |
|:--------|:---------|:-----------------------|
| Vague quantifiers | "many", "fast", 「適宜」「なるべく」 | What number, what threshold? |
| Ambiguous scope | "as needed", 「など」「必要に応じて」 | What is in, what is out? |
| Undefined success | no metric, no acceptance criterion | How will you know it worked? |
| Missing actors | — | Who does it, approves it, pays, is hurt if it fails? |
| Missing constraints | — | Budget, deadline, headcount, lock-in, compliance? |
| Unstated sequencing | "we'll do X and Y" | What must be true before each? |
| Borrowed certainty | "obviously", "the standard way" | What does that rest on? |

Sharpening tactics used inside the questions include proposing a precise term when one is overloaded, calling out drift when a term's meaning shifts mid-conversation, inventing a concrete edge-case scenario to expose rules nobody has thought about, and naming assumptions that are being treated as settled without discussion.

`references/lenses.md` carries the question angles per subject type — requirements, business plan, project plan, raw idea, proposal — and is read at the start of a session to pick the right lens.

---

## 7. Output

On confirmation that a shared understanding has been reached, the skill produces a **brief** as a single Markdown file, following `references/output-format.md`:

| Section | Content |
|:--------|:--------|
| What we're doing | The sharpened summary |
| Language | The glossary of terms pinned down during the interview |
| Decisions | The decision log — only what was hard to reverse, non-obvious, or a real trade-off |
| Open items | Assumptions, and questions that need other people |
| Next step | The single thing to do next |

The decision ledger is kept from question one, so nothing is lost when a session runs long. The brief can be requested early — 「ここまでまとめて」 — and comes back with an explicit "still open" section. A partial brief is a legitimate checkpoint, and it survives the conversation ending.

---

## 8. Resources

**References:**

- `skills/grill-me/references/lenses.md` — question angles per subject type
- `skills/grill-me/references/output-format.md` — brief template

---

## 9. Credits

Adapted from the MIT-licensed [`grilling` and `domain-modeling` skills](https://github.com/mattpocock/skills) by Matt Pocock — which is also where the `grill-me` name comes from — and from `commands/clarify.md` in this repository.

The upstream copyright notice and MIT permission text are bundled with the skill in `skills/grill-me/NOTICE`.
