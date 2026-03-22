---
layout: default
title: "Critical Document Reviewer"
grand_parent: English
parent: Software Development
nav_order: 14
lang_peer: /ja/skills/dev/critical-document-reviewer/
permalink: /en/skills/dev/critical-document-reviewer/
---

# Critical Document Reviewer
{: .no_toc }

設計文書、分析レポート、報告書などを批判的な視点で徹底レビューするスキル。
6つの異なる立場（開発者、PM、顧客、QA、セキュリティ、運用）のペルソナを持つサブエージェントが並列でレビューを実行し、
「本当にそうか？」「根拠は何か？」「テストできるか？」「運用できるか？」という視点で
曖昧さ、根拠不足、論理飛躍、テスト不能、セキュリティリスク、運用懸念を検出する。
Use when reviewing design documents, analysis reports, incident reports, or any document requiring rigorous validation of claims and evidence.

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/critical-document-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/critical-document-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

このスキルは、ドキュメントを複数の視点（6ペルソナ）から批判的にレビューし、以下を検出します：

- **根拠不足**: 主張に対する証拠がない
- **推測混入**: 検証なしの推測が事実として記載
- **論理飛躍**: A→Cの間のBが欠落
- **トレーサビリティ欠如**: 要件や元データとの紐付けがない
- **確証バイアス**: 都合の良い解釈のみ採用
- **テスト不能**: 受入基準が曖昧でテストできない
- **セキュリティリスク**: 認証・認可・データ保護の考慮漏れ
- **運用懸念**: 監視・障害対応・保守性の考慮漏れ

---

## 2. Prerequisites

- レビュー対象となるドキュメントファイル
- （推奨）関連文書（元の要件定義書、前工程のドキュメント、ログファイルなど）

---

## 3. Quick Start

```bash
Agent tool を使用して選定したペルソナのレビューを並列実行：

例1: 基本レビュー（3ペルソナ）
1. references/agents/developer.md をプロンプトとして使用
2. references/agents/qa.md をプロンプトとして使用
3. references/agents/pm.md をプロンプトとして使用

例2: セキュリティ重視レビュー（5ペルソナ）
1. references/agents/developer.md をプロンプトとして使用
2. references/agents/qa.md をプロンプトとして使用
3. references/agents/security.md をプロンプトとして使用
4. references/agents/ops.md をプロンプトとして使用
5. references/agents/pm.md をプロンプトとして使用
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

- `skills/critical-document-reviewer/references/critical_analysis_framework.md`
- `skills/critical-document-reviewer/references/evidence_evaluation_criteria.md`
- `skills/critical-document-reviewer/references/persona_selection_matrix.md`
- `skills/critical-document-reviewer/references/red_flag_patterns.md`
- `skills/critical-document-reviewer/references/scale_strategy.md`
- `skills/critical-document-reviewer/references/severity_criteria.md`
