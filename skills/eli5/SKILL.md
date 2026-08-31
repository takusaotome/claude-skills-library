---
name: eli5
description: Explain a topic like I'm a 5 year old, as a single HTML artifact built from big pictures and very few words. Use this whenever the user asks for a dead-simple explanation of how something works, says "ELI5", "explain like I'm five", "簡単に説明して", "図で説明して", "初心者向けに", "素人にもわかるように", wants to explain a concept to a non-technical manager, customer, or family member, or asks for a visual explainer — even if they don't say "ELI5" explicitly.
---

# eli5

Explain the topic like I'm someone who knows nothing about it, using a single HTML artifact with big pictures and few words.

The topic is whatever the user asked to have explained. If they named an audience (a manager, a customer, a parent, a five-year-old), keep that person in mind while choosing analogies and vocabulary.

## When to Use

- The user says "ELI5", "explain like I'm five", 「簡単に説明して」, 「図で説明して」, 「初心者向けに」, or 「素人にもわかるように」.
- They need to explain something technical to a non-technical manager, customer, or family member.
- They ask for a visual explainer, a picture-led walkthrough, or a one-pager a newcomer can follow.
- An earlier explanation did not land and they ask for a simpler version.
- Assumed background knowledge is what stands between the reader and the idea — even if they never say "ELI5".

Not this skill: a precise technical specification, an architecture document, or a slide deck for an audience that already knows the domain.

## Why this shape

The name says "5 year old", but the real goal is to strip out assumed background knowledge, not to talk like a child. Aiming at a literal five-year-old's vocabulary tends to make the explanation inaccurate. Aiming at "a smart adult who has never heard of this" keeps it both simple and true.

Big visuals with little text work because the reader is meeting the idea for the first time. A diagram shows the shape of the thing at a glance; a wall of text makes them reconstruct that shape in their head. So let the pictures carry the explanation and use words only to label and connect them.

## What to produce

One self-contained HTML artifact. Inline all CSS and SVG so it renders anywhere; do not load external scripts, stylesheets, or images.

- Open with the one-sentence version of the idea, large.
- Then walk through it in a few big panels, each with one picture and one or two short lines. Simple SVG shapes, arrows, and labels are enough; a good analogy drawn as a picture beats a precise technical diagram here.
- Prefer one concrete example over a general definition.
- End with a single "so what" line: why the reader might care.
- Keep the total text short enough to read in about a minute. If you find yourself writing paragraphs, turn them into a picture instead.

Write in the language the user is using. If the audience they named reads a different language, use that one.

---

Adapted from the MIT-licensed [eli5 plugin](https://github.com/anthropics/claude-plugins-community/tree/main/eli5) by Thariq Shihipar.
