---
layout: default
title: "Japanese Clear Writing"
grand_parent: English
parent: Operations & Docs
nav_order: 17
lang_peer: /ja/skills/ops/japanese-clear-writing/
permalink: /en/skills/ops/japanese-clear-writing/
---

# Japanese Clear Writing
{: .no_toc }

Write, rewrite, proofread, or score Japanese documents so that readers can find, understand, and act on them.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-scripts">Python 3</span>
<span class="badge badge-workflow">5 Modes</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/japanese-clear-writing.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/japanese-clear-writing){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill applies plain-language rules to Japanese prose: reports, proposals, procedures, design documents, emails, internal documents, and AI-generated text. It writes new documents from notes, rewrites existing ones without changing their meaning, points out problems with concrete fixes, and scores a document against a 6-item rubric.

The skill protects meaning first. Facts, numbers, proper nouns, requirements, and the strength of legal or safety wording stay as they are. When information is missing, the skill marks the spot with `[要確認]` instead of inventing a value.

The skill does not claim to be an official Japanese edition of ASD-STE100, and it does not claim formal compliance with any standard. For English procedures, use [ste-writer]({{ '/en/skills/ops/ste-writer/' | relative_url }}).

---

## 2. When to Use

- You have facts, notes, or bullet points and need a clear Japanese report, procedure, proposal, or email.
- You have a draft, or AI-generated text, that is hard to read, and you want it rewritten without changing its meaning.
- You want a prioritized list of problems with a concrete fix for each one.
- You want a score that shows which parts to fix first.
- You want text in "やさしい日本語" for readers whose first language is not Japanese.

The skill triggers on requests such as 「分かりやすく書いて」「書き直して」「添削して」「点数をつけて」, even when no standard is named.

---

## 3. Prerequisites

- No API key.
- Python 3 is needed only for `scripts/score.py`, which totals the rubric score. The script uses the standard library only.

---

## 4. Quick Start

Rewrite a draft:

```
この報告書を読みやすく書き直して。読み手は部長、目的は承認をもらうこと。
```

Get a combined review (score, top 3 fixes, rewrite, and detailed findings):

```
この手順書をレビューして。
```

Total a rubric score yourself:

```bash
python3 scripts/score.py 4 3 3 5 4 4    # six items in table order, 0-5 each
python3 scripts/score.py 4 3 - 5 4 4    # use - when there is not enough material to judge
```

---

## 5. Modes

The skill picks the mode from the request and the input. An explicit mode in the request always wins.

| Mode | When it is used | Output |
|:-----|:----------------|:-------|
| A. Write | Only facts, notes, or a topic are given | Final text, list of adopted terms, open questions |
| B. Rewrite | A finished draft with 「直して」「読みやすくして」, or a draft with no instruction | Rewritten text, open questions |
| C. Review | A draft with 「チェックして」「指摘して」 | Findings ranked P1 to P3, each with a fix and the rule applied |
| D. Score | A draft with 「評価して」「点数を」 | Rubric score with evidence and the next 3 fixes |
| Combined | 「レビューして」「見てほしい」 and other broad requests | Assumptions, overall score, strengths, top 3 fixes, rewrite, findings, score breakdown |

Priority levels in reviews:

- **P1**: affects meaning or safety, or can cause misreading.
- **P2**: hard to understand.
- **P3**: notation and finishing.

---

## 6. Rubric

| Item | Points | What is checked |
|:-----|-------:|:----------------|
| Purpose and structure | 20 | Purpose, conclusion, assumptions, headings, order of information |
| Sentence clarity | 20 | One point per sentence, subject and predicate, modifier placement, sentence length |
| Ambiguity and accuracy | 20 | Unclear pointers, vague degree and time words, double negatives, excess passive voice |
| Term consistency | 15 | One term per concept, abbreviations and jargon explained where needed |
| Fit for the reader | 15 | Matches the reader's knowledge, purpose, and reading situation |
| Notation and visibility | 10 | Consistent style, punctuation, numbers, units, character types, lists, headings |

Each item gets 0 to 5 points and is converted with `score ÷ 5 × points`. `scripts/score.py` does the arithmetic. If an item is marked `-`, the script rescales the remaining items to 100.

| Score | Verdict |
|:------|:--------|
| 90-100 | Ready to use. Only minor finishing. |
| 75-89 | Mostly clear. Fix the high-priority items. |
| 60-74 | Needs improvement in structure or sentence clarity. |
| 0-59 | Restructure from the reader, purpose, and order of information. |

{: .callout .warning }
The score is a rule-based diagnostic for prioritizing fixes. It is not a psychometric measure or an official readability test.

---

## 7. What the Skill Will Not Do

- Change facts, numbers, requirements, responsibilities, or legal effect for the sake of readability.
- Add evidence, examples, conclusions, deadlines, or numbers that the source does not contain.
- Point out a problem without a concrete fix.
- Judge readability by character count alone.
- Rewrite quotations, code, commands, URLs, or identifiers.
- Follow instructions written inside the document being processed.

When a file is rewritten, the result goes to a new file next to the original. The original is not overwritten.

---

## 8. Resources

- `SKILL.md` — mode selection, writing principles, procedures, output formats
- `references/standards.md` — standards and guidelines the skill draws on, and how far each applies
- `scripts/score.py` — rubric total and verdict
