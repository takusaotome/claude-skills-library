---
layout: default
title: "Design Implementation Reviewer"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 15
lang_peer: /en/skills/dev/design-implementation-reviewer/
permalink: /ja/skills/dev/design-implementation-reviewer/
---

# Design Implementation Reviewer
{: .no_toc }

Use this skill for critical code review that focuses on whether the code actually works correctly and achieves the expected results - not just whether it matches a design document. This skill assumes designs can be wrong, finds bugs the design didn't anticipate, and verifies end-to-end correctness. Triggers include "critical code review", "deep code review", "verify this implementation works", "find bugs in this code", or reviewing implementation against requirements. NOTE - Security review is OUT OF SCOPE; use a dedicated security review skill for that purpose.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/design-implementation-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/design-implementation-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

# Critical Code Reviewer

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

Before using this skill:
1. Have the code to review available (file paths or code snippets)
2. Understand the expected outcome or requirements (even if informal)
3. Access to sample data if validating data processing logic (recommended)

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

1. **Preparation**: Read required references (`references/review_checklist.md`, `references/common_gaps.md`)
2. **Define Expected Result**: Clarify input → output → success criteria before diving into code
3. **Layer 1 Review**: Code Quality (type safety, null handling, edge cases, logic, exceptions)
4. **Layer 2 Review**: Execution Flow (function wiring, data flow, joins, concurrency, resources)
5. **Layer 3 Review**: Goal Achievement (real data validation, success rate, end-to-end trace)
6. **Document Findings**: Structure output as Scope/Assumptions → Findings (by severity) → Open Questions
7. **Verify Test Plans**: Ensure Critical/High findings include specific test plans

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

- `skills/design-implementation-reviewer/references/common_gaps.md`
- `skills/design-implementation-reviewer/references/review_checklist.md`
