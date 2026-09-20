# Jev Artifact Style Review

A Japanese-first bilingual Agent Skill for actionable editorial review of documents, deliverables and messages.
It evaluates observable style friction, not whether a person or an AI wrote the artifact.

## Installation

Copy the entire `jev-artifact-style-review` folder into `.claude/skills/` in a Claude Code project.
Other Agent Skills-compatible hosts must be configured to discover the folder and run Python.
The package has not been live-loaded in those hosts during this build.

Python 3.10+ is required. The core CLI uses only the standard library.
PDF, DOCX and PPTX text extraction requires `pip install -r requirements.txt`.
Set `TYPESAFE_API_KEY` in your local environment, never in prompts or artifacts.

```bash
python scripts/review.py draft.md --language en --profile email \
  --context brief.json --dry-run --out runs/preview

python scripts/review.py draft.md --language en --profile email \
  --context brief.json --model jev-1.13.0 --allow-remote --out runs/v1
```

Remote execution sends extracted text and brief to TypeSafe. Explicit consent is required.
A dry run does not call Jev and never produces pretend scores.

## Review design

Eight style dimensions: stock phrasing, redundancy, over-templated structure, mechanical rhythm,
register mismatch, translation-like awkwardness, inflated rhetoric and conversational assistant residue.
Four separate content-quality dimensions: missing context-specific information, unclear next action,
certainty beyond supplied support and conflicts with explicit instructions.

Only the style dimensions contribute to the provisional 0–100 style-friction index.
The index is not an authorship probability, reader survey result or overall quality grade.
Jev confidence is a statistic of its answer distribution, not demonstrated accuracy on this task.

The model independently rates applicability and ordinal severity, then selects evidence from actual source segments.
Python validates and quotes the source; it does not ask Jev to generate explanations or rewrites.
The host generative agent validates each finding and writes concrete before/after suggestions in `reviewer_feedback.md`.
CLI-only output provides a report and rule-based editing directions, not a free-form rewrite.

## Bounded improvement loop

Review → validate evidence → return up to three focused edits → author revision → independent fact/meaning/requirements check → same-configuration review.
Stop after at most two revisions, or earlier when no useful reader-facing improvement remains.
A lower index does not authorize release. Never add fabricated facts, anecdotes, errors or random quirks to sound human.

```bash
python scripts/compare.py runs/v1/review.json runs/v2/review.json --out runs/comparison.json
```

The comparison refuses changed models, context, rubric, language, profiles or extraction configuration,
withheld indices, materially changed coverage or changed assessed dimensions. Numeric tokens, URLs and protected literal changes
are warnings for independent review, not proof of an error.

## Scope and validation

Supports text, Markdown, approximate visible HTML and explicit JSON text exports.
Optional readers cover PDF text layers, DOCX body/table text and PPTX shape/table text.
No OCR, image/chart interpretation, visual design assessment, external fact-checking or automatic PII redaction is included.
Long documents are evaluated by complete eligible-text chunks, not with a whole-document coherence guarantee.
Short texts and inadequate confidence/coverage can withhold the overall index.

The API contract and local behavior were tested offline. No live Jev request or Japanese/English task-accuracy benchmark
was run during this build. All thresholds are provisional. See `TEST_REPORT.md` and `references/CALIBRATION.md`.

Full Japanese setup, brief schema, output definitions and limitations: `README_ja.md`.
Official sources and their verification date: `references/API_AND_SOURCES.md`.
