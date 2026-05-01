---
layout: default
title: "Vendor Estimate Reviewer"
grand_parent: English
parent: Project & Business
nav_order: 26
lang_peer: /ja/skills/management/vendor-estimate-reviewer/
permalink: /en/skills/management/vendor-estimate-reviewer/
---

# Vendor Estimate Reviewer
{: .no_toc }

This skill should be used when reviewing vendor estimates for software development projects. Use this skill when you need to evaluate whether a vendor's cost estimate, timeline, and approach are reasonable and whether the project is likely to succeed. This skill helps identify gaps, risks, overestimates, underestimates, and unfavorable contract terms. It generates comprehensive Markdown review reports with actionable recommendations to optimize costs while ensuring project success.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-estimate-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/vendor-estimate-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Thank you for your detailed estimate. To ensure we have a complete understanding before proceeding, we'd like to clarify several items:

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
python scripts/analyze_estimate.py vendor_estimate.xlsx \
  --vendor "Acme Development" \
  --project "CRM System Modernization" \
  --budget 500000 \
  --output initial_review.md \
  --verbose
```

---

## 4. How It Works

Use this workflow when you first receive a vendor estimate and need to quickly assess its quality and identify any immediate concerns.

### Step 1: Gather Context

Collect key information about the estimate:
- Vendor name and background
- Project name and high-level scope
- Your budget (if available)
- Any specific concerns or focus areas
- Estimate format (Excel, PDF, etc.)

### Step 2: Quick Automated Analysis (Optional)

If the estimate is in Excel or CSV format, run the automated analysis script:

```bash
python scripts/analyze_estimate.py vendor_estimate.xlsx \
  --vendor "Acme Development" \
  --project "CRM System Modernization" \
  --budget 500000 \
  --output initial_review.md \
  --verbose
```

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- You've received a vendor estimate/quotation for software development
- You need to compare multiple vendor estimates
- You want to validate if an estimate is reasonable before contract signing
- You need to prepare negotiation points with a vendor
- You want to identify potential project risks early
- You need documentation for stakeholder approval

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 3 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/vendor-estimate-reviewer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: cost_estimation_standards.md, risk_factors.md, review_checklist.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: analyze_estimate.py.
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

- `skills/vendor-estimate-reviewer/references/cost_estimation_standards.md`
- `skills/vendor-estimate-reviewer/references/review_checklist.md`
- `skills/vendor-estimate-reviewer/references/risk_factors.md`

**Scripts:**

- `skills/vendor-estimate-reviewer/scripts/analyze_estimate.py`
