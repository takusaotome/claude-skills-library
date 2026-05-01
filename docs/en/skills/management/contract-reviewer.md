---
layout: default
title: "Contract Reviewer"
grand_parent: English
parent: Project & Business
nav_order: 10
lang_peer: /ja/skills/management/contract-reviewer/
permalink: /en/skills/management/contract-reviewer/
---

# Contract Reviewer
{: .no_toc }

Professional contract review skill for business agreements including NDAs, MSAs, SLAs, SOWs, and software license agreements. Provides systematic clause-by-clause analysis, risk assessment with quantified scoring, red flag detection, and negotiation guidance. Use this skill when reviewing vendor contracts, partnership agreements, service agreements, or any business contract requiring risk evaluation and negotiation preparation. Triggers include "review this contract", "analyze this NDA", "check this agreement for risks", "prepare for contract negotiation", or when evaluating terms and conditions.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/contract-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/contract-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill provides a structured methodology for reviewing business contracts from a risk and negotiation perspective. It helps identify unfavorable terms, quantify risks, and prepare negotiation strategies.

**Important Disclaimer**: This skill provides business-focused contract analysis, NOT legal advice. Always consult qualified legal counsel for binding decisions and jurisdiction-specific requirements.

---

## 2. Prerequisites

- **Python 3.9+**: Required for running analysis scripts
- **PyPDF2** (optional): Install with `pip install PyPDF2` for PDF document support
- **Contract Document**: Text file (.txt, .md) or PDF file (.pdf) containing the contract
- **No Legal Advice**: This skill provides business analysis; always consult legal counsel for binding decisions

---

## 3. Quick Start

**Purpose**: Quickly assess the contract and determine the appropriate review depth.
**Duration**: 15-30 minutes

### Step 1.1: Contract Classification

---

## 4. How It Works

**Purpose**: Quickly assess the contract and determine the appropriate review depth.
**Duration**: 15-30 minutes

### Step 1.1: Contract Classification

Identify the contract type and gather basic information:

```markdown

---

## 5. Usage Examples

- Reviewing vendor contracts before signing
- Evaluating NDAs and confidentiality agreements
- Analyzing Master Service Agreements (MSAs)
- Reviewing Service Level Agreements (SLAs)
- Evaluating software license terms
- Preparing for contract negotiations

---

## 6. Understanding the Output

This skill produces the following outputs:

| Output | Format | Description |
|--------|--------|-------------|
| **Analysis Report** | Markdown (.md) | Comprehensive contract review report with risk assessment |
| **Risk Score** | 0-100 integer | Quantified overall contract risk level |
| **Red Flag List** | Table | Prioritized list of identified issues with recommendations |
| **Clause Coverage** | Checklist | Summary of present/missing standard clauses |
| **Negotiation Summary** | Structured list | Deal breakers, high priority items, and acceptable terms |

**Report Sections**:
1. Contract Overview (type, parties, term, key terms)
2. Risk Assessment (score, level, red flags)
3. Clause Coverage (present/missing analysis)
4. Recommendations (prioritized action items)
5. Negotiation Guidance (alternative language, talking points)

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/contract-reviewer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: red_flag_patterns.md, clause_analysis_guide.md, contract_review_methodology.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: analyze_contract.py, pattern_definitions.py.
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
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/contract-reviewer/references/clause_analysis_guide.md`
- `skills/contract-reviewer/references/contract_review_methodology.md`
- `skills/contract-reviewer/references/negotiation_strategies.md`
- `skills/contract-reviewer/references/red_flag_patterns.md`
- `skills/contract-reviewer/references/risk_assessment_framework.md`

**Scripts:**

- `skills/contract-reviewer/scripts/analyze_contract.py`
- `skills/contract-reviewer/scripts/pattern_definitions.py`
