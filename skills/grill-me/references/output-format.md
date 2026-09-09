# Brief format

The brief is one Markdown file, named `grill-<slug>.md` (slug from the subject, e.g. `grill-party-booking-renewal.md`). Write it in the language of the conversation. Deliver it as a downloadable file, and give a 2–3 line pointer in chat — don't paste the whole thing back into the conversation.

It has four numbered sections plus a closing next step. Keep each one tight; the value is in what was *decided*, not in prose.

```md
# <Subject> — grilled <YYYY-MM-DD>

## 1. What we're doing (sharpened)

<The subject as it stands after the session: 1–3 short paragraphs or a compact
bullet list. Goal at the top, then scope, then the main shape of the answer.
Write it so a colleague who wasn't in the conversation could act on it.>

**Not in scope:** <explicit non-goals, one line each>

**Success looks like:** <the acceptance / metric / kill criteria that were agreed>

## 2. Language

<Only terms that were pinned down during the session — words that were
ambiguous or overloaded until the user chose a meaning. Be opinionated:
one canonical term, one or two sentence definition, and the words to avoid.>

**<Term>**:
<What it IS, in one or two sentences.>
_Avoid_: <other words the user or their team might use for the same thing>

## 3. Decisions

<One row per decision that was hard to reverse, non-obvious to a future
reader, or the result of a real trade-off. Skip the obvious ones. Rationale
in the user's own words where you have them.>

| # | Decision | Chosen | Why | Alternatives considered | Owner | Follow-up |
|---|----------|--------|-----|-------------------------|-------|-----------|
| 1 | <topic> | <what> | <reason> | <rejected options, or "—"> | <person/role or "—"> | <Yes: what / No> |

## 4. Open items

**Assumptions we're proceeding on** — things nobody could confirm; each with the
default we chose and what would change if it's wrong.

- <assumption> → default: <x>; if wrong: <consequence>

**Questions for other people** — grouped by who can answer, phrased so they can
be sent as-is.

- **<Person / role>**: <question>. _Why it matters:_ <one line>

**Still unexplored** — branches of the tree we didn't reach (only present if
the brief was requested early or the user chose to finalize with the frontier
non-empty).

- <branch>

## Next step

<The single next action, if one was agreed.>
```

## Rules

- **Section 1 is the deliverable.** If the user only reads one section, it's this one. Everything else supports it.
- **Glossary is a glossary.** No implementation detail, no decisions, no rationale — that's what section 3 is for. If no term was actually contested during the session, write "No contested terms" and move on; don't invent entries.
- **Decision table earns its rows.** Three good rows beat fifteen trivial ones. A decision that could be reversed in an afternoon and surprises nobody doesn't belong here — it's already covered in section 1.
- **Open items are honest.** An assumption is not a decision. If the user said "I don't know, let's assume X", it goes in section 4, not section 3.
- **Partial brief is fine.** When the user asks for the brief before the frontier is empty, produce it exactly the same way and fill in "Still unexplored". Label the title with "(partial)".
- **Dates**: use the actual current date from the environment, not a guess.
