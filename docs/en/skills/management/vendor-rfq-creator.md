---
layout: default
title: "Vendor RFQ Creator"
grand_parent: English
parent: Project & Business
nav_order: 27
lang_peer: /ja/skills/management/vendor-rfq-creator/
permalink: /en/skills/management/vendor-rfq-creator/
---

# Vendor RFQ Creator
{: .no_toc }

This skill should be used when creating RFQ (Request for Quotation) documents for software development projects to send to vendors. Use this skill when you have received vague requirements from clients and need to structure them into clear, comprehensive RFQs that enable vendors to provide accurate estimates. Supports Japanese (default) and English, with systematic requirements elicitation, clarification, and markdown-formatted output.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-rfq-creator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/vendor-rfq-creator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

This skill transforms vague client requirements into comprehensive RFQ (Request for Quotation) documents for software development projects. It guides you through requirements elicitation, clarification, structuring, and professional RFQ creation in Markdown format.

**Primary language**: Japanese (default)
**Output format**: Markdown

Use this skill when:
- Clients provide vague or incomplete project requirements
- You need to create formal RFQs to send to development vendors
- You want to ensure all necessary information is included for accurate estimates
- You need to standardize RFQ creation across your organization

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

1. **Requirements Elicitation**: Extract and understand client needs through structured questioning
2. **Requirements Structuring**: Transform vague requirements into clear specifications
3. **RFQ Document Creation**: Generate professional, comprehensive RFQ documents
4. **Quality Review**: Verify completeness before sending to vendors

---

## 4. How It Works

1. **Requirements Elicitation**: Extract and understand client needs through structured questioning
2. **Requirements Structuring**: Transform vague requirements into clear specifications
3. **RFQ Document Creation**: Generate professional, comprehensive RFQ documents
4. **Quality Review**: Verify completeness before sending to vendors

---

## 5. Usage Examples

- Use **Vendor RFQ Creator** when you need a structured workflow rather than an ad-hoc answer.
- Start with a small representative input before applying the workflow to production data or assets.
- Review the helper scripts and reference guides to tailor the output format to your project.

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 1 guide file(s).
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/vendor-rfq-creator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: rfq_checklist_ja.md.
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

- `skills/vendor-rfq-creator/references/rfq_checklist_ja.md`
