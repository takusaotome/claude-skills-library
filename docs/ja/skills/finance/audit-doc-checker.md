---
layout: default
title: "Audit Doc Checker"
grand_parent: 日本語
parent: 財務・分析
nav_order: 3
lang_peer: /en/skills/finance/audit-doc-checker/
permalink: /ja/skills/finance/audit-doc-checker/
---

# Audit Doc Checker
{: .no_toc }

Review audit-related documents (control design documents, bottleneck analyses, requirements definitions, etc.) for quality, scoring them 0-100 with a severity-rated findings list. Use when reviewing audit documents, checking control design quality, or verifying cross-document consistency. Supports documents governed by US GAAP, IFRS, or J-GAAP.

{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/audit-doc-checker.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/audit-doc-checker){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

This skill reviews audit-related documents against 12 quality check categories and produces a structured quality score (0-100) with a detailed findings list. Each finding includes severity (High/Medium/Low), location in the document, description, and recommended fix.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

None. This is a knowledge-based skill that uses reference documents to guide the review.

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

### Step 1: Identify the Target Document

Read the document to be reviewed. Determine the document type:

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

- `skills/audit-doc-checker/references/check_rules.md`
- `skills/audit-doc-checker/references/scoring_model.md`
