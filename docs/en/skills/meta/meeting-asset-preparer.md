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

### Step 1: Gather Meeting Context

Collect meeting metadata including title, date/time, attendees, objectives, and language preferences. Create a meeting configuration file.

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

### Step 2: Compile Reference Materials

Scan project directories for relevant documents (estimates, specs, prior meeting notes) and generate a reference index.

```bash
python3 scripts/prepare_meeting.py compile-refs \
  --config meeting_config.yaml \
  --project-dir ./project \
  --output references_index.md

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Preparing assets for an upcoming project meeting or status review
- Creating bilingual meeting documentation for cross-regional teams
- Compiling reference materials from estimates, specs, and implementation docs
- Generating structured agendas with time allocations
- Setting up decision log and action item tracking templates
- Preparing follow-up documentation after a meeting concludes

---

## 6. Understanding the Output

### Meeting Configuration (YAML)

```yaml
meeting:
  title: "Sprint Review Meeting"
  date: "2026-03-15"
  time: "14:00"
  timezone: "JST"
  duration_minutes: 60
  attendees:
    - name: "Alice"
      role: "Product Owner"
    - name: "Bob"
      role: "Developer"
  objectives:
    - "Review sprint deliverables"
    - "Discuss blockers"
  language: "bilingual"  # en, ja, or bilingual

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/meeting-asset-preparer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: meeting-best-practices.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: prepare_meeting.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/meeting-asset-preparer/references/meeting-best-practices.md`

**Scripts:**

- `skills/meeting-asset-preparer/scripts/prepare_meeting.py`
