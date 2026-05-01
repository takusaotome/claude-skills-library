---
layout: default
title: "Meeting Minutes Reviewer"
grand_parent: English
parent: Meta & Quality
nav_order: 31
lang_peer: /ja/skills/meta/meeting-minutes-reviewer/
permalink: /en/skills/meta/meeting-minutes-reviewer/
---

# Meeting Minutes Reviewer
{: .no_toc }

Review meeting minutes for completeness, action item clarity, decision documentation, and consistency with source materials such as hearing sheets or transcripts. Generates structured feedback with specific improvement suggestions and quality scores across 5 dimensions.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/meeting-minutes-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/meeting-minutes-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Reviews an existing meeting-minutes document against quality standards and (optionally) the source materials it was drafted from. Scores the minutes on five weighted dimensions — Completeness (25%), Action Items (25%), Decisions (20%), Consistency (15%), Clarity (15%) — and emits structured findings with concrete improvement suggestions.

This skill is review-only. To **generate** minutes from a transcript, use `meeting-minutes-writer` (which has its own self-review loop). To **prepare** meeting assets ahead of time, use `meeting-asset-preparer`.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (json, re, pathlib)

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=meeting-minutes-reviewer

# Or fetch the .skill package
curl -L -o meeting-minutes-reviewer.skill \
  https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/meeting-minutes-reviewer.skill

# Run a review against a sample
python3 skills/meeting-minutes-reviewer/scripts/review_minutes.py \
  --minutes path/to/minutes.md \
  --output review_report.md
```

---

## 4. How It Works

1. **Gather inputs** — the minutes document, plus any source materials the reviewer wants checked against (hearing sheet, transcript, prior decision log, agenda).
2. **5-dimension scoring** — each dimension is scored 0-100 with weighted contribution to the total:
   - Completeness (25%) — required sections present (date, attendees, agenda, decisions, action items, next steps)
   - Action Items (25%) — every action has owner, deadline, and a non-vague description
   - Decisions (20%) — context, rationale, and alternatives considered are documented
   - Consistency (15%) — minutes align with source materials and don't contradict themselves
   - Clarity (15%) — vague language, undefined acronyms, and ambiguous pronouns flagged
3. **Findings** — structured list of issues with severity (HIGH / MEDIUM / LOW) and suggested fixes
4. **Output** — JSON for machine consumption + Markdown for human reading

---

## 5. Usage Examples

- After drafting meeting minutes and before distribution
- Reviewing minutes created by others for quality assurance
- Validating that minutes accurately reflect source materials (hearing sheets, transcripts)
- Ensuring action items meet trackability standards before they enter a project tracker
- Preparing minutes for formal project documentation or audit trails

---

## 6. Understanding the Output

```
Score:                 78/100
  Completeness:        85/100  (good — minor: "next steps" section thin)
  Action Items:        65/100  (3 items missing owner; 1 vague description)
  Decisions:           80/100
  Consistency:         85/100  (no contradictions vs. source)
  Clarity:             75/100  (3 undefined acronyms)
Findings:              7 (1 HIGH, 4 MEDIUM, 2 LOW)
```

The Markdown report lists each finding with its location (line / section), severity, and a concrete suggested fix. The JSON report has the same data in structured form for downstream tooling.

---

## 7. Tips & Best Practices

- Provide the source material when available — consistency scoring is much more useful with a reference.
- Treat HIGH findings as blocking before distribution; MEDIUM as "fix-this-revision"; LOW as "nice to have".
- Don't manually rewrite the minutes inside this skill — re-run the writing workflow (or `meeting-minutes-writer`'s self-review loop) and re-review.
- For audit trails, archive both the minutes and the review report together.
- The score is guidance, not a gate. A 60 with the right HIGH findings fixed is better than an 85 with a buried action-item omission.

---

## 8. Combining with Other Skills

- Pair with `meeting-minutes-writer` — generate minutes there (which has a 3-iteration self-review), then run this skill as an independent second-pass review.
- Hand confirmed action items to `project-artifact-linker` to thread them into WBS / requirements.
- Use after `video2minutes` so transcribed minutes get the same QA treatment as authored ones.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).
- See the full English skill catalog: [skill catalog]({{ '/en/skill-catalog/' | relative_url }}).

---

## 9. Troubleshooting

- **Score is suspiciously high** — double-check that you actually passed the source material. Without it, Consistency defaults to a permissive baseline.
- **No findings on Action Items** — confirm action items aren't formatted as plain prose; the parser looks for explicit list / table structures.
- **"Vague language" false positives** — domain jargon may trigger clarity flags; treat them as suggestions, not bugs.
- **JSON output is empty** — ensure the input is valid Markdown; the parser tolerates minor issues but not totally non-Markdown input.

---

## 10. Reference

**References:**

- `skills/meeting-minutes-reviewer/references/review-criteria.md` — detailed scoring criteria and quality standards
- `skills/meeting-minutes-reviewer/references/meeting-minutes-checklist.md` — complete checklist for meeting minutes

**Scripts:**

- `skills/meeting-minutes-reviewer/scripts/review_minutes.py` — main review script with 5-dimension quality analysis
- `skills/meeting-minutes-reviewer/scripts/test_minutes_sample.md` — sample input for smoke-testing
