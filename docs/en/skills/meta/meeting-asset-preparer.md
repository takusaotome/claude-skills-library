---
layout: default
title: "Meeting Asset Preparer"
grand_parent: English
parent: Meta & Quality
nav_order: 15
lang_peer: /ja/skills/meta/meeting-asset-preparer/
permalink: /en/skills/meta/meeting-asset-preparer/
---

# Meeting Asset Preparer
{: .no_toc }

Prepare comprehensive meeting assets including agendas, reference materials, decision logs, and action items. Use when preparing for project meetings, cross-regional sessions, or creating bilingual (Japanese/English) meeting documentation.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/meeting-asset-preparer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/meeting-asset-preparer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill prepares comprehensive meeting assets by gathering project context, generating structured agendas, compiling relevant reference materials, and creating templates for decision logs and action items. It supports bilingual (Japanese/English) output for cross-regional meetings and integrates with project artifacts such as estimates, implementation documents, and prior meeting notes.

---

## 2. Prerequisites

- Python 3.9+
- No API keys required
- Standard library plus `pyyaml` for configuration parsing

---

## 3. Quick Start

```bash
python3 scripts/prepare_meeting.py init \
  --title "Sprint Review Meeting" \
  --date "2026-03-15" \
  --time "14:00" \
  --timezone "JST" \
  --attendees "Alice,Bob,Carol" \
  --language "bilingual" \
  --output meeting_config.yaml
```

---

## 4. How It Works

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/meeting-asset-preparer/references/meeting-best-practices.md`

**Scripts:**

- `skills/meeting-asset-preparer/scripts/prepare_meeting.py`
