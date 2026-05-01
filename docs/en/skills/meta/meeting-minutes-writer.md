---
layout: default
title: "Meeting Minutes Writer"
grand_parent: English
parent: Meta & Quality
nav_order: 23
lang_peer: /ja/skills/meta/meeting-minutes-writer/
permalink: /en/skills/meta/meeting-minutes-writer/
---

# Meeting Minutes Writer
{: .no_toc }

Generate strategic-consultant-grade meeting minutes from transcripts or notes, then run a self-review loop (max 3 iterations) that checks for internal contradictions, action-item omissions, speaker-name errors, and date/day-of-week mistakes before reporting completion.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/meeting-minutes-writer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/meeting-minutes-writer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill turns raw meeting content (transcripts, notes, recordings transcribed elsewhere) into concise, scannable meeting minutes that an executive can absorb in three minutes. After producing a draft, it runs a structured **self-review loop** — up to three iterations — that runs five mandatory checks against the draft and the source. The skill only reports completion when a review iteration returns **zero findings** or **three iterations** have been exhausted, and it surfaces any HIGH-severity findings still open after the third iteration.

**Languages supported**: Japanese and English are both first-class output languages. The skill matches the source language automatically — Japanese transcript → Japanese minutes (with 会議情報 / アクションアイテム / 決定事項 headings), English transcript → English minutes. Bilingual meetings use the majority language for headings while preserving names, quoted statements, and technical terms verbatim.

It complements two adjacent skills:
- `meeting-minutes-reviewer` — review-only (use when minutes already exist)
- `video2minutes` — transcribes video first, then can hand off to this skill

---

## 2. Prerequisites

- Python 3.9+ (used only for the mandatory date verification command)
- No API keys required
- No third-party packages required (uses Python's standard `datetime` module)

---

## 3. Quick Start

Provide the source material between `<<Transcript>>` tags or attach a transcript file, then ask Claude to "create meeting minutes". The skill will:

1. Generate a draft using its 6-step generation workflow.
2. Run the self-review loop (max 3 iterations).
3. Report the file path, iterations run, findings fixed per iteration, and any open HIGH-severity findings.

For each concrete date in the draft, the skill verifies the day-of-week with:

```bash
python3 -c "import datetime; d=datetime.date(2026,5,15); print(d.strftime('%Y-%m-%d %A'))"
# 2026-05-15 Friday
```

---

## 4. How It Works

The skill runs in **two mandatory phases**.

### Phase 1 — Generate Draft (ultrathink)

1. Scan metadata — meeting name, date, attendees. If missing, infer and tag `* To be confirmed`.
2. Identify speakers and roles.
3. Map discussion threads to topics, collapsing long debates to 2-3 key points each.
4. Extract every commitment ("I'll do X", "we should check Y", "let's investigate Z") as an action item.
5. Synthesize explicit consensus or directives as decisions.
6. Render the draft using the canonical structure in `references/output_format.md`.

### Phase 2 — Self-Review Loop (max 3 iterations)

```
iteration = 1
while iteration <= 3:
    findings = run_review(draft)
    if findings.is_empty():
        break  # clean pass — exit
    apply_fixes(draft, findings)
    iteration += 1
```

Each iteration runs the **5 Mandatory Checks**:

1. **Internal Contradictions** — owner / deadline / number conflicts within the draft
2. **Consistency** — draft accurately reflects the source; no fabricated content
3. **Action-Item Omissions** — every commitment in the source has a row in the action items table
4. **Speaker-Name Errors** — names spelled and attributed consistently
5. **Date / Day-of-Week Errors** — every concrete date verified with the Python `datetime` command

Findings are categorized by severity: **HIGH** (blocks completion), **MEDIUM**, **LOW**. Each finding includes location, evidence quote, and suggested fix (template: `assets/findings_report_template.md`).

### Completion Report

The skill only reports completion after the loop terminates. The report includes:
- Path to the final minutes file
- Number of review iterations run
- Findings fixed per iteration (count + brief summary)
- **Any HIGH-severity findings still open** (explicitly flagged)
- All `* To be confirmed` items the reader should manually verify

---

## 5. Usage Examples

- Converting a long product-planning transcript into minutes with verified dates and complete action items
- Cleaning up sparse standup notes into a quality-gated minutes document
- Creating bilingual minutes (matches source language: JP transcript → JP minutes)
- Producing audit-ready minutes where every decision and action is traceable to the source
- Catching the common LLM date error ("next Tuesday" rendered as the wrong calendar date)

---

## 6. Understanding the Output

### Minutes Structure

```markdown
### 1. Meeting Information
- **Meeting Name**: ...
- **Date**: 2026/04/30 (Thu)
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

### Findings Report (per iteration)

Each review iteration produces a Findings Report listing every finding with severity, location, evidence, and a suggested fix. The completion report summarizes the totals.

### Ambiguity Markers

- `* To be confirmed` — content was inferred; user should verify
- `[Details unclear]` — source content was unintelligible
- `(To be confirmed)` — appended after a name when ownership is uncertain

---

## 7. Tips & Best Practices

- **Never skip the review loop.** Even short minutes need at least one review pass before completion.
- **Always verify dates with the Python command** — never guess day-of-week from memory; LLMs are unreliable here.
- **Preserve user-provided names verbatim** — if the source writes "田中さん", do not normalize to "Tanaka".
- **Quote source evidence** when raising findings so each fix is auditable.
- **Don't paraphrase decisions** — record decisions in language close to what was actually agreed.
- Keep `* To be confirmed` markers visible in the completion report so the reader knows what to verify manually.

---

## 8. Combining with Other Skills

- Pair with `video2minutes` to go from raw video → transcript → reviewed minutes in one flow.
- Run `meeting-minutes-reviewer` afterwards if you need a separate, deeper quality scoring pass on the produced minutes.
- Hand the resulting action items to `project-manager` or `project-artifact-linker` for traceability into the project plan.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).

---

## 9. Troubleshooting

- **Date / day-of-week appears wrong in the draft** — confirm the skill ran the `python3 -c "import datetime..."` verification; if not, re-trigger the date check explicitly.
- **Action items missing** — open the source and grep for "should / will / TODO / 確認 / 対応 / フォロー" patterns; ask the skill to re-run iteration with a focus on Check 3 (Omissions).
- **Speaker names inconsistent across sections** — re-run iteration with Check 4 only; the skill should normalize to the source's own spelling.
- **Loop exits at iteration 3 with HIGH findings** — those represent ambiguity in the source itself (e.g. transcript contradicts itself); resolve manually using the evidence quoted in the report.
- **Report lacks `* To be confirmed` summary** — the skill always lists them at the end of the completion report; if absent, the source likely contained no inferred content.

---

## 10. Reference

**References:**

- `skills/meeting-minutes-writer/references/output_format.md` — canonical minutes structure, inference rules, ambiguity markers
- `skills/meeting-minutes-writer/references/self_review_checklist.md` — full criteria for the 5 Mandatory Checks and iteration logic

**Assets:**

- `skills/meeting-minutes-writer/assets/minutes_template_en.md` — blank meeting minutes template (English)
- `skills/meeting-minutes-writer/assets/minutes_template_ja.md` — meeting minutes template (Japanese)
- `skills/meeting-minutes-writer/assets/findings_report_template.md` — per-iteration findings report layout (bilingual EN + JA)
