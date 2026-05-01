---
layout: default
title: "Technical Spec Writer"
grand_parent: English
parent: Project & Business
nav_order: 24
lang_peer: /ja/skills/management/technical-spec-writer/
permalink: /en/skills/management/technical-spec-writer/
---

# Technical Spec Writer
{: .no_toc }

要件定義と実装の間を埋める技術仕様書を体系的に作成するスキル。 画面設計、API設計、DB設計、シーケンス図、状態遷移図をMermaid形式で生成し、 IEEE 830/ISO 29148準拠の仕様書を出力する。Use when creating functional specifications, API design documents, database design documents, screen design specifications, or sequence/state diagrams from requirements. Triggers: "technical specification", "functional spec", "API design", "database design", "screen design", "画面設計書", "API設計書", "DB設計書", "技術仕様書", "シーケンス図", "状態遷移図"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/technical-spec-writer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/technical-spec-writer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill bridges the gap between requirements definition (BRD/User Stories) and implementation by producing structured, standards-compliant technical specification documents. It generates screen designs, API specifications, database designs, sequence diagrams, and state transition diagrams using Mermaid notation, following IEEE 830 and ISO/IEC/IEEE 29148 standards.

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

### Workflow 1: Requirements Intake（要件取り込み）

**Purpose**: Gather and structure input requirements to determine document scope.

---

## 4. How It Works

### Workflow 1: Requirements Intake（要件取り込み）

**Purpose**: Gather and structure input requirements to determine document scope.

1. **Receive input** — Accept BRD, user stories, verbal requirements, or existing partial specs
2. **Determine document scope** — Classify the requested output:
   - 全体仕様書（Full functional specification）
   - 画面設計書（Screen design specification）
   - API設計書（API design specification）
   - DB設計書（Database design specification）
   - 個別ダイアグラム（Individual diagram）
3. **Create document outline** — Establish the ID numbering scheme:
   - SCR-xxx for screens
   - API-xxx for endpoints
   - TBL-xxx for tables
   - SEQ-xxx for sequence diagrams
   - STS-xxx for state diagrams
4. **Establish traceability** — Build a REQ-xxx to SCR/API/TBL mapping table to ensure every requirement is addressed
5. **Confirm scope with user** — Present the outline and confirm before proceeding
6. **Load** `references/spec_writing_standards.md` for ID conventions and quality criteria

### Workflow 2: Screen Design Specification（画面設計）

**Purpose**: Produce detailed screen design documents with UI elements, events, and transitions.

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- 要件定義（BRD）から技術仕様書を作成する
- 画面設計書を作成する
- API設計書を作成する
- DB設計書を作成する
- シーケンス図や状態遷移図を作成する
- 既存仕様書のレビューや改善を行う

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 4 guide file(s).
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/technical-spec-writer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: spec_writing_standards.md, mermaid_diagram_patterns.md, db_design_guide.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/management/' | relative_url }}).
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

- `skills/technical-spec-writer/references/api_design_guide.md`
- `skills/technical-spec-writer/references/db_design_guide.md`
- `skills/technical-spec-writer/references/mermaid_diagram_patterns.md`
- `skills/technical-spec-writer/references/spec_writing_standards.md`
