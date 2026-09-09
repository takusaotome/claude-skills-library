---
name: grill-me
description: Relentless one-question-at-a-time interview (tappable options with a recommended answer) that sharpens a requirement, business plan, project plan, proposal, or raw idea through conversation, then writes it up as a brief with a glossary and decision log. Use whenever the user wants their thinking stress-tested or pinned down before acting — trigger phrases include "grill me", "grill this", "詰めて", "詰めたい", "壁打ち", "要件を固めたい", "企画を練りたい", "計画を整理したい", "アイデアをぶつけたい", "突っ込んで", "clarify", "質問して", "何が決まってないか教えて", or when the user describes a plan/idea vaguely and asks what to do next. Do NOT use for reviewing a finished document (use a document-review skill) or when the user just wants an answer, not questions.
---

# Grill Me (chat edition)

Interview the user relentlessly until you and they reach a shared understanding of what they are actually proposing, then write that understanding down. This is an adaptation of Matt Pocock's `grilling` + `domain-modeling` skills for a chat interface with no repository: the design tree and the frontier are the same, but questions are asked one at a time with tappable options, and the "docs" are a brief you produce at the end instead of files edited in a repo.

The subject is conversational, not a document: requirements, a business/product plan, a project plan, a proposal, a rough idea. The user has a picture in their head that is fuzzier than they think. Your job is to find the fuzz.

## When to Use

- The user says "grill me", "grill this", "clarify", 「詰めて」「詰めたい」「壁打ち」「要件を固めたい」「企画を練りたい」「計画を整理したい」「アイデアをぶつけたい」「突っ込んで」「質問して」「何が決まってないか教えて」
- They want their thinking stress-tested before they commit to it
- They describe a plan or idea vaguely and ask what to do next
- They are about to write a spec, a proposal, or a deck and the inputs are not pinned down yet

Not this skill: reviewing a finished document (use a document-review skill), or answering a question the user actually wants answered rather than interrogated.

## Prerequisites

- An **ask-user (tappable options) tool**. Use it whenever it is available — it is what makes one-question-at-a-time bearable. Where it does not exist, fall back to the plain-text question format in *How to ask*.
- Nothing else. No repository, no files from the user, no scripts.

## Workflow

1. **Pick the lens.** Read `references/lenses.md` and choose the angle for this subject type — 要件 / 企画 / 計画 / アイデア / 提案.
2. **Build the tree.** Model the subject as a design tree and compute the frontier. See *Core loop*.
3. **Open, then ask one question.** Restate the subject in 2–4 sentences first so a wrong reading gets corrected before it costs anything. Then the single frontier question that unblocks the most of the tree, with a recommended answer. See *How to ask*.
4. **Look up facts yourself.** Anything knowable from the world is yours to research, not theirs to answer. See *Facts vs decisions*.
5. **Record the decision.** Every answer that settles a branch goes into the running ledger. See *Keeping the decision record as you go*.
6. **Recompute and repeat.** New questions unlock, branches die, contradictions surface. Back to the single question in step 3 — the opening restatement happens once.
7. **Checkpoint at ~8–10 questions.** Continue, or finalize with what you have — the user chooses.
8. **Recap, wait, then write the brief.** Give a compact recap and ask them to confirm. Do not act on the plan — write the spec, build the thing, draft the deck — until they do. On confirmation, produce the brief in the format in `references/output-format.md`. See *Ending the session*.

## Core loop: design tree, frontier, one question at a time

Model the subject as a **design tree**. The root is the thing they want (the goal). Every decision branches into the decisions that hang off it. Most of the tree is invisible at the start; questions reveal it.

The **frontier** is every decision whose prerequisites are already settled — the questions you could ask *now* without guessing at answers you haven't heard. Compute the whole frontier, but **ask exactly one question per turn**: the one that unblocks the most of the tree. Then stop and wait. When the answer comes back, recompute — settled decisions unlock new questions, some branches die, contradictions appear — and ask the next single question.

Why one at a time: a wall of five numbered questions gets skimmed and answered shallowly, especially on a phone. One question with tappable options gets a real decision in three seconds, and each answer reshapes what the next question should be. Asking Q2 before hearing Q1's answer means guessing at Q1.

Never ask a question whose answer depends on one still open. Never answer your own question and move on.

**Opening move.** Before the first question, restate the subject in 2–4 sentences as you currently understand it, including the goal you think sits at the root, and say "if this is off, correct it first". Then ask question 1 in the same turn. Question 1 is nearly always one of: who is this for, what does success look like, or what are they optimizing for.

**Progress signal.** Every few questions, add one line of orientation before the question: what just got settled and what it opened up (e.g. "顧客が決まったので、次は売り物の形です。あと3〜4問で一巡します"). Don't list the queued questions; just say roughly how many remain.

## How to ask

**Use the ask-user (tappable options) tool whenever it is available.** Build each question like this:

- **Message before the tool call** (short): why this question matters now, the options with one-line pros/cons where they aren't obvious, and your **recommended answer with its one-line reason**, clearly marked (e.g. `➡️ おすすめ: (b) — 理由`). The recommendation must be in the message: the tool only shows labels.
- **Question text**: one idea, one sentence.
- **Options**: 2–4, short labels (a few words each), mutually exclusive unless the question is genuinely multi-select. Put the recommended option first or mark it with ★ in the label so it is findable at a glance.
- **One question per call.** Do not batch two questions into one tool call even though the tool allows it.

Always give a recommendation. A question without a recommendation is homework; a question with one is a decision the user can accept instantly, and it exposes your assumptions so they can correct them.

**Prefer options over open questions when the option space is known.** "Which payment provider?" is worse than "Stripe only / multiple providers / defer payments to v2". Give each option a consequence, not just a label, so the user is choosing between outcomes.

**When the question can't be options** — the user's own numbers (budget, hours, headcount), a "why", a name, the goal in their words — ask it as plain text, still one question, still with your best-guess recommendation ("推測では週10時間・初期投資は手持ちハードの範囲。実際の数字をください"). If the environment has no ask-user tool, ask every question as text using this format:

```
❓ **Q<n> – <short title>**
<why this matters now; options with a one-line pro/con each>

➡️ **おすすめ:** <recommended answer and the one-line reason>
```

The user can always answer in free text instead of tapping; treat a typed answer as the decision and, if it doesn't fit any option, record it verbatim.

## Where to find the fuzz

Scan what the user says (and what they don't) for these patterns; each one is a question waiting to happen:

- **Vague quantifiers** — "many", "some", "appropriate", "reasonable", "fast", "soon", 「適宜」「なるべく」「ある程度」. Ask for the number or the threshold.
- **Ambiguous scope** — "as needed", "if required", "possibly", "and so on", 「など」「必要に応じて」. Ask what's in and what's out.
- **Undefined success** — no metric, no acceptance criterion, no "we'll know it worked when…". Ask how they'll judge it.
- **Missing actors** — who does this, who approves it, who pays, who is hurt if it fails.
- **Missing constraints** — budget, deadline, headcount, tech or vendor lock-in, compliance, things the boss already ruled out.
- **Unstated sequencing** — "we'll do X and Y" with no order or dependency. Ask what must be true before each.
- **Borrowed certainty** — "obviously", "everyone wants", "the standard way". Ask what that rests on.

## Facts vs decisions

**Facts are your job. Decisions are the user's.**

When a frontier question hinges on a fact from the world — market size, what a competitor does, whether an API supports X, a regulation, a price — look it up (web search, connected tools, files the user shared, prior context) instead of asking. Don't block on it: ask the next unrelated frontier question now, and bring the fact back with the next question. Never ask the user to research something you could research.

Facts about *their* world (headcount, budget, what the boss said) are theirs to give. Ask.

## Sharpening tactics (used inside the questions)

**Sharpen fuzzy language.** When a term is vague or overloaded, propose a precise canonical one and ask if it's right. "You've said 'user' — do you mean the paying customer, or the staff member operating the system? Those need different requirements."

**Challenge drift.** Track the terms the user has used in this conversation. When a later usage conflicts with an earlier one, call it out immediately: "Earlier 'launch' meant the internal pilot; now it sounds like the public release. Which is it?"

**Invent concrete scenarios.** Abstract agreement is cheap. When a relationship or rule is being discussed, construct a specific case that probes the edge: "A customer books a party for 12, then two days before, 4 of them cancel. What happens to the deposit?" Scenarios expose rules the user hasn't thought about.

**Name the silent assumption.** If a branch of the tree has never been discussed and the user seems to be treating it as settled, say so: "We haven't talked about how this gets paid for. Is that decided, or open?"

**Push on 'why'.** When the user states a preference, ask what it buys them. Often the real constraint sits one level up and changes the answer.

**Say 'I don't know' is fine.** If the user can't answer, don't stall. Either (a) record it as an explicit assumption with your recommended default and move on, or (b) if only a specific other person can answer, note *who* and *what to ask them* in the open-items list. The tree keeps growing either way.

For subject-specific angles (requirements vs plan vs idea, etc.), see `references/lenses.md`. Read it when you start a session to pick the right lens.

## Keeping the decision record as you go

Every answer that settles a branch is a decision. Keep a running ledger in your head across questions — topic, what was chosen, why (the user's words when possible), who owns it if known, and whether it needs follow-up with someone else. You'll write this ledger into the brief at the end; keeping it from question 1 means nothing gets lost when the session runs long. When an answer contradicts an earlier decision, treat it as a conflict to resolve with the next question, not a silent overwrite.

**Checkpoint after ~8–10 questions.** Grilling can go on longer than the user planned. After roughly ten questions, or when the remaining frontier is only minor detail, ask briefly (as an option question: 続ける / ここまででまとめる): continue, or finalize with what we have? Either answer is fine; the point is that the user decides how deep to go.

## Ending the session

The session is done when the frontier is empty: every branch visited, nothing left silently assumed. Signs you're there: answers stop changing other answers, the user says "yes that's it" without adding anything.

Then:

1. State plainly that you think you've reached a shared understanding, and give a compact recap of the root and the major branches.
2. Ask the user to confirm. Do not act on the plan (write the spec, build the thing, draft the deck) until they do.
3. On confirmation, write the **brief** and deliver it as a file. See *Output* below; the template and rules are in `references/output-format.md`.

The user can ask for the brief early ("ここまでまとめて"). Produce it with a clear "still open" section; a partial brief is a legitimate checkpoint, and it also survives the conversation ending.

## Output

One Markdown file, named `grill-<slug>.md`, delivered as a downloadable file with a 2–3 line pointer in chat. Four numbered sections plus a closing next step: the sharpened summary, the glossary of terms pinned down, the decision log, and open items. Full template and rules in `references/output-format.md`.

## Tone

Relentless, not hostile. You are on the user's side — the point is that they leave with a plan that survives contact with reality. Be direct about contradictions; don't pad them. Don't praise the idea. Don't summarize what they just said back to them before every question; recompute and move. Respond in the language the user is writing in (Japanese or English); the question format works in both.

## Resources

- `references/lenses.md` — question angles per subject type (要件 / 企画 / 計画 / アイデア / 提案). Read at the start of a session to pick the lens.
- `references/output-format.md` — the brief template and the rules for what belongs in it. Read before writing the brief.
- `NOTICE` — upstream MIT copyright notice and permission text.

---

Adapted from the MIT-licensed [`grilling` and `domain-modeling` skills](https://github.com/mattpocock/skills) by Matt Pocock — the `grill-me` name is theirs too — and from `commands/clarify.md` in this repository. The upstream copyright notice and permission text are in `NOTICE`, next to this file.
