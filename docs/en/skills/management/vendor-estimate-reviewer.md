---
layout: default
title: "Vendor Estimate Reviewer"
grand_parent: English
parent: Project & Business
nav_order: 24
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

- `skills/vendor-estimate-reviewer/references/cost_estimation_standards.md`
- `skills/vendor-estimate-reviewer/references/review_checklist.md`
- `skills/vendor-estimate-reviewer/references/risk_factors.md`

**Scripts:**

- `skills/vendor-estimate-reviewer/scripts/analyze_estimate.py`
