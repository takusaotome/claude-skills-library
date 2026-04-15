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

### Phase 1: 準備（Preparation）

1. **文書タイプの特定**
   - 設計文書（Design Document）
   - 不具合分析レポート（Incident/Bug Analysis Report）
   - 要件定義書（Requirements Document）
   - 提案書（Proposal）
   - その他報告書

2. **関連文書の収集**
   - 設計文書の場合: 元の要件定義書、前工程のドキュメント
   - 不具合分析の場合: ログファイル、データ、証拠となる資料
   - ユーザーに関連文書の有無を確認

3. **ペルソナの選定**（文書タイプに応じて3〜6ペルソナを自動選定）

   `references/persona_selection_matrix.md` の選定マトリクスに従ってペルソナを選定する。

   **ペルソナ選定ガイドライン:**
   - 最低3ペルソナ、最大6ペルソナまで選定可能
   - 文書タイプに応じて適切な組み合わせを選択
   - セキュリティ・運用の考慮が必要な文書は対応ペルソナを必ず含める

### Phase 1.5: スケール判定

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- 設計文書（システム設計書、API設計書、DB設計書など）のレビュー
- 要件定義書・仕様書のレビュー
- 不具合分析レポート・インシデントレポートのレビュー
- 提案書・企画書のレビュー
- セキュリティ設計書のレビュー
- 運用設計書・運用手順書のレビュー

---

## 6. Understanding the Output

レビュー結果は以下の形式で出力:

```markdown
# 批判的レビューレポート

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/critical-document-reviewer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: red_flag_patterns.md, persona_selection_matrix.md, critical_analysis_framework.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.

---

## 10. Reference

**References:**

- `skills/critical-document-reviewer/references/critical_analysis_framework.md`
- `skills/critical-document-reviewer/references/evidence_evaluation_criteria.md`
- `skills/critical-document-reviewer/references/persona_selection_matrix.md`
- `skills/critical-document-reviewer/references/red_flag_patterns.md`
- `skills/critical-document-reviewer/references/scale_strategy.md`
- `skills/critical-document-reviewer/references/severity_criteria.md`
