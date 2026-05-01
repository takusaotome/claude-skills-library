---
layout: default
title: "IT System ROI Analyzer"
grand_parent: English
parent: Finance & Analysis
nav_order: 9
lang_peer: /ja/skills/finance/it-system-roi-analyzer/
permalink: /en/skills/finance/it-system-roi-analyzer/
---

# IT System ROI Analyzer
{: .no_toc }

ITシステム導入・刷新のROI（投資対効果）分析スキル。ERP、CRM、クラウド移行、基幹システム刷新、DXプロジェクト等のビジネスケース作成を支援。TCO分析、NPV/IRR計算、感度分析、経営層向けROIレポート生成を実行。「システムROI」「IT投資評価」「クラウド移行コスト」「TCO分析」「DX投資効果」等のトリガーで使用。
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/it-system-roi-analyzer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/it-system-roi-analyzer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

ITシステム導入・刷新プロジェクトのROI（投資対効果）を体系的に分析し、経営層への説得力あるビジネスケースを作成するスキル。

**対象システム:**
- ERP/基幹システム刷新
- CRM/SFA導入
- クラウド移行（オンプレ→クラウド）
- レガシーシステム更新
- DX/デジタル化プロジェクト
- セキュリティ強化
- BI/分析基盤構築

**主要機能:**
- 現状（As-Is）コスト分析
- 5年間TCO（総所有コスト）算出
- 効果の定量化（コスト削減、生産性向上、リスク低減）
- 財務指標計算（ROI, NPV, IRR, 回収期間）
- 感度分析（楽観/標準/悲観シナリオ）
- 日本語・英語レポート生成

---

---

## 2. Prerequisites

このスキルを使用するために必要なもの：

### 必須情報
- **初期投資額**: システム開発費、パッケージ/SaaS費用、インフラ構築費
- **運用コスト**: 年間の保守費用、クラウド利用料、ライセンス費
- **効果見積**: コスト削減額、生産性向上効果（定量化済み）

### 任意情報
- **割引率**: 資本コスト（WACC）、通常10-15%
- **分析期間**: 通常5年間（3-7年で調整可能）
- **シナリオ前提**: 楽観/悲観ケースの変動幅

### Python環境（スクリプト使用時）
- Python 3.8以上
- 標準ライブラリのみ使用（追加パッケージ不要）

---

---

## 3. Quick Start

```bash
1. 現状分析 (As-Is)          → 現行コスト・課題の把握
        ↓
2. 投資額算出                 → 初期投資・TCOの見積もり
        ↓
3. 効果定量化                 → コスト削減・生産性向上効果
        ↓
4. 財務指標算出               → ROI/NPV/IRR/回収期間
        ↓
5. 感度分析                   → シナリオ別評価・リスク分析
        ↓
6. ROI資料生成                → 経営層向けレポート作成
```

---

## 4. How It Works

このスキルの標準的なワークフロー：

```
1. 現状分析 (As-Is)          → 現行コスト・課題の把握
        ↓
2. 投資額算出                 → 初期投資・TCOの見積もり
        ↓
3. 効果定量化                 → コスト削減・生産性向上効果
        ↓
4. 財務指標算出               → ROI/NPV/IRR/回収期間
        ↓
5. 感度分析                   → シナリオ別評価・リスク分析
        ↓
6. ROI資料生成                → 経営層向けレポート作成
```

各ステップの詳細は後続の Core Workflow セクションを参照。

---

## 5. Usage Examples

- **新規システム導入の投資判断**
- 「ERPシステム導入のROIを算出して」
- 「CRM導入のビジネスケースを作成して」
- **システム刷新・更新の投資評価**
- 「基幹システム刷新の投資対効果を分析して」
- 「レガシーシステム更新のコスト比較をして」

---

## 6. Understanding the Output

このスキルが生成する主な成果物：

### 1. 財務指標サマリー
- ROI（投資利益率）
- NPV（正味現在価値）
- IRR（内部収益率）
- 投資回収期間

### 2. キャッシュフロー分析表
- 5年間の年次キャッシュフロー予測
- 累積キャッシュフロー推移

### 3. 感度分析レポート
- シナリオ別（楽観/標準/悲観/最悪）財務指標
- 損益分岐点分析
- リスク評価マトリクス

### 4. 経営層向けROIレポート

The full output details are documented in SKILL.md.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/it-system-roi-analyzer/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: it_roi_methodology.md, benefit_quantification.md, tco_analysis_guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: it_roi_calculator.py.
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

- `skills/it-system-roi-analyzer/references/benefit_quantification.md`
- `skills/it-system-roi-analyzer/references/it_roi_methodology.md`
- `skills/it-system-roi-analyzer/references/tco_analysis_guide.md`

**Scripts:**

- `skills/it-system-roi-analyzer/scripts/it_roi_calculator.py`
