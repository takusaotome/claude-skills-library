---
layout: default
title: "ELI5"
grand_parent: English
parent: Operations & Docs
nav_order: 15
lang_peer: /ja/skills/ops/eli5/
permalink: /en/skills/ops/eli5/
---

# ELI5
{: .no_toc }

Explain a topic like I'm a 5 year old, as a single HTML artifact built from big pictures and very few words.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/eli5.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/eli5){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill turns a topic into a single self-contained HTML explainer: big pictures, very few words, readable in about a minute.

The name says "5 year old", but the goal is to strip out assumed background knowledge, not to talk like a child. Aiming at a literal five-year-old's vocabulary tends to make the explanation inaccurate. Aiming at "a smart adult who has never heard of this" keeps it both simple and true.

Big visuals with little text work because the reader is meeting the idea for the first time. A diagram shows the shape of the thing at a glance; a wall of text makes them reconstruct that shape in their head. The pictures carry the explanation and the words only label and connect them.

If the request names an audience — a manager, a customer, a parent, a five-year-old — that person drives the choice of analogies and vocabulary.

---

## 2. When to Use

- The user says "ELI5", "explain like I'm five", 「簡単に説明して」, 「図で説明して」, 「初心者向けに」, or 「素人にもわかるように」.
- They need to explain something technical to a non-technical manager, customer, or family member.
- They ask for a visual explainer, a picture-led walkthrough, or a one-pager a newcomer can follow.
- An earlier explanation did not land and they ask for a simpler version.
- Assumed background knowledge is what stands between the reader and the idea — even if they never say "ELI5".

**Not this skill:** a precise technical specification (see `technical-spec-writer`), an architecture document, or a slide deck for an audience that already knows the domain (see `fujisoft-presentation-creator`).

---

## 3. Prerequisites

- **API Key:** None required
- No scripts, dependencies, or external services — the skill is instructions only

---

## 4. Quick Start

Ask for a simple explanation of any topic:

```
ELI5 how DNS works
```

```
うちの部長にRAGを説明したい。図で説明して。
```

Claude produces one HTML artifact and hands back the link.

---

## 5. Output Shape

One self-contained HTML artifact, with all CSS and SVG inlined so it renders anywhere. No external scripts, stylesheets, or images.

| Part | Content |
|:-----|:--------|
| Opening | The one-sentence version of the idea, set large |
| Panels | A few big panels, each with one picture and one or two short lines |
| Example | One concrete example rather than a general definition |
| Closing | A single "so what" line: why the reader might care |

Simple SVG shapes, arrows, and labels are enough. A good analogy drawn as a picture beats a precise technical diagram here. Total text stays short enough to read in about a minute — if a paragraph appears, it becomes a picture instead.

The artifact is written in the language the user is using. If the named audience reads a different language, that language wins.

---

## 6. Resources

This skill uses built-in Claude capabilities without external scripts or references.

---

## 7. Credits

Adapted from the MIT-licensed [eli5 plugin](https://github.com/anthropics/claude-plugins-community/tree/main/eli5) by Thariq Shihipar.
