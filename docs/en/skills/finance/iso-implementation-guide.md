---
layout: default
title: "ISO Implementation Guide"
grand_parent: English
parent: Finance & Analysis
nav_order: 8
lang_peer: /ja/skills/finance/iso-implementation-guide/
permalink: /en/skills/finance/iso-implementation-guide/
---

# ISO Implementation Guide
{: .no_toc }

ISO規格（ISO 9001品質、ISO 27001情報セキュリティ、ISO 22301事業継続等）の認証取得支援スキル。
ギャップ分析、文書化支援、内部監査、認証準備を提供。
Use when pursuing ISO certification, conducting gap analysis, or implementing ISO-compliant management systems.
Triggers: "ISO 9001", "ISO 27001", "ISO 22301", "ISO certification", "quality management", "ISMS", "gap analysis".

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/iso-implementation-guide.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/iso-implementation-guide){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides expert guidance for implementing ISO management system standards and achieving certification. Supports ISO 9001 (Quality), ISO 27001 (Information Security), ISO 22301 (Business Continuity), and other ISO standards.

**Primary language**: Japanese (default), English supported
**Supported Standards**: ISO 9001, ISO 27001, ISO 22301, ISO 45001, ISO 14001
**Output format**: Gap analysis reports, implementation roadmaps, document templates, audit checklists

---

---

## 2. Prerequisites

1. **Python 3.9+** for running automation scripts
2. **Access to target ISO standard** (official document recommended)
3. **Stakeholder access** for interviews during gap analysis
4. **Existing documentation** (policies, procedures, records) for assessment

---

---

## 3. Quick Start

```bash
┌─────────────────────────────────────────────────────────────┐
│                    ISO Implementation                        │
├─────────────────────────────────────────────────────────────┤
│  1. Gap Analysis    →  Assess current state vs requirements │
│  2. Roadmap         →  Plan phased implementation          │
│  3. Documentation   →  Create policies, procedures         │
│  4. Internal Audit  →  Verify compliance internally        │
│  5. Certification   →  Stage 1 + Stage 2 external audit    │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    ISO Implementation                        │
├─────────────────────────────────────────────────────────────┤
│  1. Gap Analysis    →  Assess current state vs requirements │
│  2. Roadmap         →  Plan phased implementation          │
│  3. Documentation   →  Create policies, procedures         │
│  4. Internal Audit  →  Verify compliance internally        │
│  5. Certification   →  Stage 1 + Stage 2 external audit    │
└─────────────────────────────────────────────────────────────┘
```

**Typical Timeline**: 6-18 months depending on starting maturity

---

## 5. Usage Examples

- **Planning ISO certification**: Organization is pursuing ISO 9001, 27001, 22301, or other certification
- **Conducting gap analysis**: Need to assess current state vs. ISO requirements
- **Developing documentation**: Creating policies, procedures, and work instructions
- **Preparing for audits**: Getting ready for Stage 1/Stage 2 certification audits
- **Implementing management systems**: Building quality, security, or continuity systems
- **Integrating multiple standards**: Combining ISO 9001 + 27001 + 22301 using HLS

---

## 6. Understanding the Output

This skill generates:

| Output | Description | Format |
|--------|-------------|--------|
| Gap Analysis Report | Clause-by-clause compliance assessment | Markdown/CSV |
| Implementation Roadmap | Phased plan with milestones | Markdown/Mermaid |
| Maturity Score | 0-5 score per clause, overall average | Numeric |
| Action Plan | Prioritized gaps with owners and effort | Table |
| Internal Audit Checklist | Clause-specific audit questions | Markdown |
| Document Templates | Policy, procedure, record templates | Markdown |

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/iso-implementation-guide/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: iso-hls-structure.md, gap-analysis-methodology.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: gap_analysis.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/finance/' | relative_url }}).
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

- `skills/iso-implementation-guide/references/gap-analysis-methodology.md`
- `skills/iso-implementation-guide/references/iso-hls-structure.md`

**Scripts:**

- `skills/iso-implementation-guide/scripts/gap_analysis.py`
