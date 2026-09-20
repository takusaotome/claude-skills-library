---
layout: default
title: "Jev Artifact Style Review"
grand_parent: English
parent: Operations & Docs
nav_order: 16
lang_peer: /ja/skills/ops/jev-artifact-style-review/
permalink: /en/skills/ops/jev-artifact-style-review/
---

# Jev Artifact Style Review
{: .no_toc }

Japanese-first bilingual editorial style review that turns "this reads like AI wrote it" into concrete, fixable writing problems.
{: .fs-6 .fw-300 }

<span class="badge badge-required">TYPESAFE_API_KEY Required</span>
<span class="badge badge-scripts">Python 3.10+</span>
<span class="badge badge-bilingual">Bilingual JA/EN</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/jev-artifact-style-review.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/jev-artifact-style-review){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

A reader who says a document "feels like AI wrote it" is usually reacting to something concrete: a stock phrase, the same sentence ending four times in a row, a heading structure heavier than the content under it, English word order showing through a Japanese sentence. This skill treats those as editorial defects that can be pointed at and fixed, not as evidence about who wrote the text.

**It is not an AI-authorship detector.** It produces no "written by AI" verdict, and having used AI is not treated as a fault.

The work is split deliberately. Jev — a TypeSafe model — does the scoring and picks which source segments support each finding. The host agent reads the original, decides whether each finding actually holds, writes the short explanation, and drafts the concrete replacement wording. Jev is never asked to invent prose, rewrites, or facts.

Scores are one axis of quality, not a pass/fail gate. Accuracy, completeness, evidence, stated conditions, and courtesy all outrank a lower friction index.

---

## 2. When to Use

- A Japanese or English document, email, message, proposal, technical write-up, or slide deck reads as stiff, templated, or machine-translated, and you need to say *why* in specific terms.
- You want to hand a writer a short list of concrete "this sentence → that sentence" edits instead of "make it sound more human".
- You need a second, repeatable reading pass before a customer-facing document goes out.
- You revised a draft and want to re-score it under identical conditions to see whether the revision actually helped.

**Not this skill:** deciding whether a person used AI; judging visual layout, slide design, or scanned images; verifying facts or legal validity; rewriting a document wholesale.

---

## 3. Prerequisites

- **API Key:** `TYPESAFE_API_KEY` in your local environment. Required for live scoring; the dry run works without it.
- **Python 3.10+**. Markdown, TXT, HTML, and JSON text exports need only the standard library.
- **Optional readers** for PDF / DOCX / PPTX text extraction: `pip install -r requirements.txt` (`pypdf`, `python-docx`, `python-pptx`).
- **Authorization to send the content.** The skill will not transmit material you are not permitted to send. Check what would leave your machine with `--dry-run` first.

{: .callout .prerequisite }
Never paste the API key into chat, a document, a command argument, or an output file. Read it into the environment with `read -s TYPESAFE_API_KEY; export TYPESAFE_API_KEY`.

---

## 4. Quick Start

Ask Claude directly:

```
jev-artifact-style-review で draft.md を顧客向け日本語メールとして評価して。
brief.json に目的と確認済みの事実が入っています。作成者に返す主要3件の
具体的な修正案まで作って。全面改稿はまだしないで。
```

Or drive the CLI yourself. Step 1 sends nothing over the network:

```bash
python scripts/review.py draft.md \
  --language ja --profile email --context brief.json \
  --dry-run --out runs/style-v1-preview
```

`request_preview.json` shows exactly what would be transmitted. There is no automatic PII masking, and a dry run produces no score — it will not invent a placeholder number.

Then score, revise, and compare under identical settings:

```bash
python scripts/review.py draft.md --language ja --profile email \
  --context brief.json --model jev-1.13.0 --allow-remote --out runs/style-v1

python scripts/review.py draft-v2.md --language ja --profile email \
  --context brief.json --model jev-1.13.0 --allow-remote --out runs/style-v2

python scripts/compare.py runs/style-v1/review.json runs/style-v2/review.json \
  --out runs/style-comparison.json
```

Revision is capped at two rounds by design. A comparison that cannot be made is never reported as an improvement.

---

## 5. Evaluation Design

Two groups of axes are scored independently and never mixed into one number.

| Group | What it covers |
|:------|:---------------|
| **Style — 8 axes** | Stock phrases, tautology, over-structuring, monotonous sentence patterns and endings, register/politeness mismatch, translationese, embellishment, leftover chat-assistant boilerplate |
| **Content quality — 4 axes** | Missing context or specificity, unclear next action, claims beyond the supplied evidence, mismatch with explicit instructions |

The 0–100 **style-friction index** aggregates the 8 style axes only. Higher means more stylistic friction.

{: .callout .warning }
The index is **not** a probability that AI wrote the text, and **not** the share of real readers who would find it odd. `confidence` is derived from the model's output distribution — it is not this task's accuracy rate, and it must not be conflated with the per-choice `probabilities`.

Weights, thresholds, and level descriptions live in `assets/rubric.json`. Seven use-case profiles adjust what counts as a defect: `email`, `chat`, `report`, `proposal`, `technical`, `slides`, `formal`. Slides exempt bullet lists and parallel structure; technical documents are not penalized for consistent sentence patterns; `formal` protects contractual boilerplate — without assessing legal validity.

A context file (`assets/context.example.json`, schema in `schemas/context.schema.json`) supplies purpose, audience, constraints, `source_facts`, `required_information`, `protected_fragments`, and `locked_sections`. Unknown fields are rejected. Leave a field out rather than inventing a value — an unknown audience means that axis is held back, not guessed.

---

## 6. Output

| File | Contents |
|:-----|:---------|
| `review.md` | Human-readable scores, source quotations, editing direction |
| `review.json` | Per-dimension values, confidence, quotation offsets, usage, model, rubric, raw response and request hashes |
| `writer_handoff.json` | Revision candidates, preservation conditions, and a writer response field (pending until answered) |
| `extracted.json` | Normalized full text, segments, character offsets, exclusion reasons, extraction warnings |
| `context.json`, `plan.json` | The conditions the run executed under |
| `run_status.json` | Completed or failed; `release_approval` is always false |
| `request_preview.json` | Dry run only: exactly what would be transmitted |
| `reviewer_feedback.md` | Written by the host agent, not the CLI: original → replacement wording with the reasoning behind each |

Which files appear depends on the mode. A dry run writes `extracted.json`, `context.json`, `plan.json`, and `request_preview.json`, then stops — it produces no `run_status.json`. A live run adds `review.md`, `review.json`, `writer_handoff.json`, and `run_status.json`. A failure writes `run_status.json` with `status: failed` only if it happens after the output directory was created; a failure before that point (a missing API key, an unreadable input) leaves no files at all.

Quotations are sliced from the source text by Python using the segment IDs Jev selected — Jev never authors a quotation. The output directory must be new or empty; an existing evaluation is never overwritten. On POSIX systems files are written 600 and the directory 700. Output contains the document body and quotations, so keep it out of Git and shared drives.

---

## 7. Scope and Limitations

| Input | What is evaluated |
|:------|:------------------|
| MD / TXT | Body text; code fences, blockquotes, and declared locked sections excluded |
| HTML | Approximate text with scripts and some hidden elements removed — not the computed rendering |
| JSON | `{"text": "..."}` or `{"blocks": [{"locator": "...", "text": "..."}]}` |
| PDF | Text layer only; empty or scanned pages are flagged. No OCR |
| DOCX | Body and table text; headers, footers, comments, tracked changes not interpreted |
| PPTX | Text frames and tables; figures, images, notes, and visual placement not evaluated |

Out of scope: image-led artifacts, code correctness, spreadsheet calculations, and visual design. Long documents are scored per chunk and aggregated, so overall structure, distant repetition, and argument flow are not fully assessed. Limits: 30 MB per file, 500,000 extracted characters, 128 chunks (`--max-chunks`), 150 logical API calls. Chunks are the units sent for scoring, and are distinct from the `segments` recorded in `extracted.json`.

{: .callout .warning }
**Calibration status: unvalidated.** The bundled test suite (64 tests) uses synthetic responses and never contacts the API. Real authentication, response quality, Japanese-language accuracy, false-positive rate, and confidence calibration have not been measured. Treat the index as provisional until you run the human-rating procedure in `references/CALIBRATION.md`. The 5-point difference used when comparing revisions is a rough guide, not a passing threshold.

Prompt-injection resistance is not guaranteed. The skill detects embedded instructions heuristically, uses explicit data boundaries, a fixed API endpoint, redirect refusal, and output validation — but hostile input still needs independent review. Evaluation instructions, self-scores, quotations, and code inside a document are never executed as commands, and a document cannot change the thresholds or rubric.

---

## 8. Resources

**References:**

- `references/RUBRIC_ja.md` — 12 axes, profile adjustments, index formula and interpretation
- `references/WRITER_LOOP.md` — handoff format and the revision loop in practice
- `references/CALIBRATION.md` — human-rating procedure and conditions for production use
- `references/API_AND_SOURCES.md` — official API, model, confidence, and language constraints (verified 2026-09-20)

**Scripts:** `scripts/review.py` (extract, dry run, score), `scripts/compare.py` (compare two runs)

**Assets:** `assets/rubric.json`, `assets/context.example.json` · **Schemas:** `schemas/*.schema.json`

**Verification:** `TEST_REPORT.md` records what was tested and what was not.

---

## 9. Notes on this repository copy

The upstream v1.0.0 distribution is vendored as-is, with two deliberate exceptions.

Its 11 Python files were reformatted to satisfy this repository's `ruff check` / `ruff format` CI. Formatting only — no logic was changed, and the bundled suite still passes 64/64 afterwards.

`TEST_REPORT.md` used two-space Markdown hard breaks in its three header lines. This repository's pre-commit hook strips trailing whitespace, which would have collapsed them into one paragraph, so they were converted to a bullet list. The wording is unchanged.

`MANIFEST.sha256` was regenerated over both changes, so it no longer matches the upstream zip.
