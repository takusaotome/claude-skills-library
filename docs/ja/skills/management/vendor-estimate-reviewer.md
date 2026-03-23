---
layout: default
title: "Vendor Estimate Reviewer"
grand_parent: 日本語
parent: プロジェクト・経営
nav_order: 24
lang_peer: /en/skills/management/vendor-estimate-reviewer/
permalink: /ja/skills/management/vendor-estimate-reviewer/
---

# Vendor Estimate Reviewer
{: .no_toc }

This skill should be used when reviewing vendor estimates for software development projects. Use this skill when you need to evaluate whether a vendor's cost estimate, timeline, and approach are reasonable and whether the project is likely to succeed. This skill helps identify gaps, risks, overestimates, underestimates, and unfavorable contract terms. It generates comprehensive Markdown review reports with actionable recommendations to optimize costs while ensuring project success.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-estimate-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/vendor-estimate-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

Thank you for your detailed estimate. To ensure we have a complete understanding before proceeding, we'd like to clarify several items:

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- **API Key:** None required
- **Python 3.9+** recommended

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
python scripts/analyze_estimate.py vendor_estimate.xlsx \
  --vendor "Acme Development" \
  --project "CRM System Modernization" \
  --budget 500000 \
  --output initial_review.md \
  --verbose
```

<!-- TODO: 翻訳 -->

---

## 4. 仕組み

<!-- TODO: 翻訳 -->

---

## 5. 使用例

<!-- TODO: 翻訳 -->

---

## 6. 出力の読み方

<!-- TODO: 翻訳 -->

---

## 7. Tips & ベストプラクティス

<!-- TODO: 翻訳 -->

---

## 8. 他スキルとの連携

<!-- TODO: 翻訳 -->

---

## 9. トラブルシューティング

<!-- TODO: 翻訳 -->

---

## 10. リファレンス

**References:**

- `skills/vendor-estimate-reviewer/references/cost_estimation_standards.md`
- `skills/vendor-estimate-reviewer/references/review_checklist.md`
- `skills/vendor-estimate-reviewer/references/risk_factors.md`

**Scripts:**

- `skills/vendor-estimate-reviewer/scripts/analyze_estimate.py`
