---
layout: default
title: "Yt Dlp Expert"
grand_parent: English
parent: Software Development
nav_order: 33
lang_peer: /ja/skills/dev/yt-dlp-expert/
permalink: /en/skills/dev/yt-dlp-expert/
---

# Yt Dlp Expert
{: .no_toc }

yt-dlpを使用した動画ダウンロードの専門スキル。YouTube、ニコニコ動画、Twitter/X、TikTok等1000以上のサイトから動画・音声・字幕をダウンロード。フォーマット選択、プレイリスト処理、メタデータ抽出を効率的に支援。Use when downloading videos, extracting audio, getting subtitles, or fetching metadata from YouTube and other video sites.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/yt-dlp-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/yt-dlp-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

# yt-dlp Expert

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

Invoke this skill by describing your analysis needs to Claude.

---

## 4. How It Works

Follow the skill's SKILL.md workflow step by step, starting from a small validated input.

---

## 5. Usage Examples

- Use **Yt Dlp Expert** when you need a structured workflow rather than an ad-hoc answer.
- Start with a small representative input before applying the workflow to production data or assets.
- Review the helper scripts and reference guides to tailor the output format to your project.

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 3 guide file(s).
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/yt-dlp-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: authentication.md, download_options.md, subtitle_extraction.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.

---

## 10. Reference

**References:**

- `skills/yt-dlp-expert/references/authentication.md`
- `skills/yt-dlp-expert/references/download_options.md`
- `skills/yt-dlp-expert/references/subtitle_extraction.md`
