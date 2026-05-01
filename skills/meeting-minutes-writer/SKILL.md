---
name: meeting-minutes-writer
description: Generate strategic-consultant-grade meeting minutes from transcripts or notes, then run a self-review loop (max 3 iterations) that checks for internal contradictions, action-item omissions, speaker-name errors, and date/day-of-week mistakes before reporting completion. Use this skill whenever the user asks to draft meeting minutes, summarize a transcript, or document a meeting discussion.
---

# Meeting Minutes Writer

## Overview

Transform raw meeting content (transcripts, notes, recordings transcribed elsewhere) into concise, scannable meeting minutes that an executive can absorb in three minutes. After producing a draft, this skill runs a structured self-review loop (up to 3 passes) to detect and fix contradictions, missing action items, speaker-name errors, and date/day-of-week mistakes. Completion is only reported when a pass returns zero findings or three passes have been exhausted.

## When to Use

Trigger this skill when the user:
- Provides a meeting transcript and asks for "議事録" / "meeting minutes" / "summary"
- Asks to "format / clean up / structure" meeting notes
- Provides a `<<Transcript>>` block, raw chat log, or recording transcript
- Wants action items and decisions extracted from a discussion

## When NOT to Use

- Pure transcript cleanup with no structuring needed → just edit text directly
- Reviewing existing minutes only (no generation) → use `meeting-minutes-reviewer`
- Generating an agenda or pre-meeting brief → use `meeting-asset-preparer`
- Transcribing video/audio first → use `video2minutes` (it can call this skill afterwards)

## Core Workflow

This skill runs in **two phases**: Generation, then a Self-Review Loop. Both phases are mandatory.

### Phase 1 — Generate Draft (ultrathink)

Use ultrathink mode to analyze the source material thoroughly before writing.

**Steps**:
1. **Scan metadata** — meeting name, date, attendees. If absent, infer from content and mark `* To be confirmed`.
2. **Identify speakers** — extract a definitive speaker list with roles where derivable.
3. **Map discussion threads** to topics. Lengthy debates collapse to 2-3 key points.
4. **Extract commitments** — every "I'll do X", "we should check Y", "let's investigate Z" becomes an action item.
5. **Synthesize decisions** — explicit consensus or directives become entries under "Decisions Made".
6. **Render the draft** using the format in `references/output_format.md`.

Save the draft to a working file (e.g. `meeting_minutes_draft.md`) so the review loop can edit and re-read it.

### Phase 2 — Self-Review Loop (up to 3 iterations)

After producing the draft, run the review loop **before reporting completion**. Each iteration produces a Findings Report; if findings are non-empty, fix the draft and re-review. Stop when a clean pass occurs OR 3 iterations have run.

```
iteration = 1
while iteration <= 3:
    findings = run_review(draft)
    if findings.is_empty():
        break  # quality gate passed
    apply_fixes(draft, findings)
    iteration += 1
```

For each iteration, run the **5 Mandatory Checks** below in order. See `references/self_review_checklist.md` for full criteria and `assets/findings_report_template.md` for the report layout.

#### The 5 Mandatory Checks

1. **Internal Contradictions** — claims that conflict with each other (e.g. "Alice will lead" in §3 but "Bob will lead" in §5; deadline "Aug 20" in action table but "Aug 22" in discussion).
2. **Consistency / Coherence** — decisions reflect discussion; action items trace back to a stated commitment; numbers, dollar amounts, and counts match across sections.
3. **Action Item Omissions** — every "will do / should / need to / let's / TODO / follow up" in the source has a corresponding row in the Action Items table; ownership and due date are not silently dropped.
4. **Speaker-Name Errors** — names spelled consistently with the source (no "Tanaka" → "Tanaka-san" → "田中さん" inconsistency, no swapped first/last names, no attribution drift).
5. **Date / Day-of-Week Errors** — every concrete date is verified to match its day-of-week using the verification helper (see below). Time-zone conversions (ET↔JST etc.) are also checked.

**Date verification — MANDATORY tool use, not memory**:

```bash
python3 -c "import calendar, datetime; d=datetime.date(YYYY, MM, DD); print(d.strftime('%Y-%m-%d %A'))"
```

For ET↔JST conversions, use:
```bash
# Winter (Nov 1st Sun ~ Mar 2nd Sun): JST = ET + 14h
# Summer (Mar 2nd Sun ~ Nov 1st Sun): JST = ET + 13h
python3 -c "et=14; off=14; jst=et+off; print(f'{et}:00 ET = {jst%24}:00 JST' + (' (+1d)' if jst>=24 else ''))"
```

**Findings format** — for each finding record:
- Severity (`HIGH` blocks completion / `MEDIUM` should fix / `LOW` style)
- Location (section + line range or table row)
- Issue (what's wrong)
- Evidence (quote from source if available)
- Suggested fix

Use the structure in `assets/findings_report_template.md`.

### Completion Report

Only report completion when one of these terminates the loop:
- A review iteration returns **zero findings** → clean pass
- **Three iterations** have run

The completion report MUST include:
1. Path to the final minutes file
2. Number of review iterations run
3. Findings fixed per iteration (count + brief summary)
4. **Any HIGH-severity findings still open after iteration 3** (explicitly flagged)
5. List of items the reader should manually verify (anything tagged `* To be confirmed`)

If iteration 3 ends with HIGH-severity findings still open, do **not** silently mark the work as done — surface those open items prominently in the report.

## Output Format

The minutes follow this exact structure (full template: `assets/minutes_template.md`):

```markdown
### 1. Meeting Information
- **Meeting Name**: ...
- **Date**: YYYY/MM/DD (Day of Week)
- **Attendees**: ...

### 2. Action Items
| No. | Action Item | Owner | Priority | Due Date | Notes |
|-----|-------------|-------|----------|----------|-------|

### 3. Meeting Details
#### Decisions Made
#### Key Topics and Discussion Points
#### Notes for Future Meetings / Other
```

Priority legend: 🔴 High (blocking) / 🟡 Medium (should do) / 🟢 Low (nice to have).

See `references/output_format.md` for full formatting rules, inference rules, and ambiguity handling.

## Examples

### Example 1: Standard transcript

**User**: "Here's today's product planning transcript: <<Transcript>>...<<End>>"

**Skill behavior**:
1. Generate draft following the 6-step generation workflow.
2. Iteration 1 review finds 2 issues: (a) "Alice owns DB migration" in action table but discussion shows Bob volunteered; (b) "next Tuesday" rendered as 8/13 but 8/13 is Wednesday.
3. Fix both, run iteration 2 → 0 findings → clean pass.
4. Report: 2 iterations, 2 findings fixed, file saved at `./meeting_minutes_2026-04-30.md`.

### Example 2: Sparse notes

**User**: "Quick notes from standup, please clean up"

**Skill behavior**:
1. Generate draft. Mark missing fields `* To be confirmed`.
2. Iteration 1 finds 1 omission (a "follow up with vendor next week" line wasn't captured as an action) → fix.
3. Iteration 2 → 0 findings.
4. Report: 2 iterations, 1 finding fixed, lists all `* To be confirmed` items for the user to fill in.

### Example 3: Loop exhausts

**User**: Provides a long, contradictory transcript.

**Skill behavior**:
1. Iteration 1 → 5 findings; iteration 2 → 2 remaining + 1 new; iteration 3 → 1 HIGH still open (a date that the source itself contradicts).
2. Report: 3 iterations run, 6 findings fixed total, **1 HIGH finding remains** (transcript itself is ambiguous about whether the launch is 2026-05-15 Friday or 2026-05-16 Saturday — flagged for user resolution).

## Resources

### references/
- `output_format.md` — full minutes formatting spec, inference rules, ambiguity handling
- `self_review_checklist.md` — detailed criteria for each of the 5 mandatory checks

### assets/
- `minutes_template.md` — blank meeting minutes template (Markdown)
- `findings_report_template.md` — findings report template for each review iteration

## Best Practices

- **Never skip the review loop.** Even short minutes need at least one self-review pass before completion is reported.
- **Always verify dates with `python3 -c ...`** — never guess day-of-week from memory; LLMs are unreliable here.
- **Keep findings actionable.** Every finding must include a suggested fix, not just "this is wrong."
- **Preserve user-provided names verbatim** — if the source writes "田中さん", do not normalize to "Tanaka" in the minutes.
- **Quote evidence from the source** when raising a finding so the fix is auditable.
- **Use `* To be confirmed`** markers liberally for inferred content; surface them in the completion report.
- **Don't paraphrase decisions** — record decisions in language close to what was actually agreed, to preserve auditability.
