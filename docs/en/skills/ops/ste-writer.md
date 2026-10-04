---
layout: default
title: "STE Writer"
grand_parent: English
parent: Operations & Docs
nav_order: 18
lang_peer: /ja/skills/ops/ste-writer/
permalink: /en/skills/ops/ste-writer/
---

# STE Writer
{: .no_toc }

Write new English text, or rewrite existing text, to the main rules of ASD-STE100 Simplified Technical English.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-workflow">Write / Rewrite</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ste-writer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ste-writer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

ASD-STE100 Simplified Technical English (STE) lets a reader who knows only a little English follow instructions with no risk of misreading them. The method is one meaning per word, one idea per sentence, and no clever phrasing. The result is plain, but each sentence has one clear meaning, and it machine-translates well.

This skill works in two ways:

- **Rewrite**: you give existing text, and the skill converts it.
- **Write new**: you give facts, notes, bullet points, a topic, or code, and the skill writes a new document in STE.

{: .callout .warning }
The skill applies the core rules from memory. It does not include the official ASD-STE100 specification or its approved-word Dictionary, so its output is "written to the main ASD-STE100 rules", not "STE-compliant" or "certified". For formal compliance, check the result with the official Dictionary or a checker tool. If you give the skill the spec or a word list, it follows that over its own notes.

---

## 2. When to Use

- Procedures, manuals, SOPs, runbooks, or release notes for readers whose first language is not English.
- Text that will be machine-translated.
- Existing English documentation that is wordy, passive, or ambiguous.
- Requests that mention STE, simple technical English, ASD-STE100, or "80% STE".

For Japanese documents, use [japanese-clear-writing]({{ '/en/skills/ops/japanese-clear-writing/' | relative_url }}).

---

## 3. Prerequisites

None. The skill is instructions only, with no scripts and no API key.

---

## 4. Quick Start

Rewrite existing text:

```
Rewrite docs/install.md in STE.
```

Write a new procedure from notes:

```
Write an STE procedure from these notes: reset procedure for the badge printer.
Hold the button, wait for the light. Takes about a minute. Unplug first.
```

Use the softer mode:

```
Rewrite this release note in 80% STE and keep my technical terms.
```

The skill replies in the language of your request. The document itself is always in English.

---

## 5. Strictness

| Mode | What it does |
|:-----|:-------------|
| **Full** (default) | Applies all 14 core rules. |
| **Soft** | Applies rules 1 to 6, keeps the author's technical terms and natural rhythm, and allows some sentences up to about 25 words. Used when you ask for "80%", "lightly", or "keep my tone". |

The output always states which mode was used.

---

## 6. Core Rules

1. One instruction per sentence. Procedure sentences are 20 words or fewer; descriptive sentences are 25 words or fewer.
2. Use the imperative for actions: "Remove the cover."
3. Use the active voice.
4. Use only the simple present, simple past, and future.
5. Keep one word for one meaning. Do not swap in synonyms for variety.
6. Choose the simple, common word: "use", not "utilize".
7. Keep articles and short helper words. No telegraphic text.
8. Use at most three nouns in a row.
9. Replace phrasal verbs and idioms with one clear verb.
10. Avoid contractions and unclear pronouns.
11. Keep paragraphs to one topic and at most six sentences.
12. Put warnings and cautions before the step they apply to. "WARNING" is for danger to people; "CAUTION" is for danger to equipment or data.
13. Use "must" for requirements, "can" for ability, and "may" for permission.
14. Write numbers as digits and keep the unit with the number.

Example of a rewrite:

| Before | After |
|:-------|:------|
| Before the unit is powered on, it should be ensured that all of the connectors have been properly seated, otherwise damage could occur. | CAUTION: Make sure that all connectors are fully connected before you start the unit. If a connector is loose, the unit can be damaged. |

---

## 7. Output

The skill gives, in this order:

1. **The document**, in the format of its destination. When it rewrites a file, it writes the result to a new file next to the original and does not overwrite it.
2. **Changes** (rewrite) — the 3 to 6 most important kinds of change, each with a before/after example. **Key terms** (new text) — the terms chosen, so you can keep them the same in later documents.
3. **Questions for the author** — one for each `[CHECK: ...]` marker. The skill uses these markers instead of guessing missing values such as a torque, a time, or a command.
4. One line with the mode and a reminder that this is not official certification.

---

## 8. Resources

- `SKILL.md` — rules, word swaps, workflows, output format, and examples
