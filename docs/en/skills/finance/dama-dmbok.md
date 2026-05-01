---
layout: default
title: "Dama Dmbok"
grand_parent: English
parent: Finance & Analysis
nav_order: 5
lang_peer: /ja/skills/finance/dama-dmbok/
permalink: /en/skills/finance/dama-dmbok/
---

# Dama Dmbok
{: .no_toc }

DAMA-DMBOK（Data Management Body of Knowledge）準拠のデータマネジメントスキル。
11の知識領域（データガバナンス、データ品質、メタデータ管理、MDM等）を網羅し、
データ戦略策定から具体的な改善施策まで支援する。
Use when: データ戦略策定、データガバナンス構築、データ品質改善、データカタログ作成、
MDM導入、DX推進、データ移行プロジェクト、データ成熟度評価。
Triggers: "データガバナンス", "データ品質", "データカタログ", "メタデータ管理",
"MDM", "データ戦略", "DMBOK", "データ成熟度", "データリネージ"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/dama-dmbok.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/dama-dmbok){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

DAMA-DMBOK（Data Management Body of Knowledge）は、DAMA International が策定した
データマネジメントの国際的な知識体系です。データを組織の戦略的資産として管理するための
包括的なフレームワークを提供します。

**核心原則:**
- **Data as an Asset（データは資産）**: データを戦略的資産として管理
- **Data Governance（ガバナンス）**: 統制とアカウンタビリティの確立
- **Data Quality（品質）**: 信頼できるデータの維持
- **Data Security（セキュリティ）**: 適切な保護とアクセス管理

```
┌─────────────────────────────────────────────────────────────────────┐
│                      DAMA-DMBOK Framework                           │
│                                                                     │
│                    ┌───────────────────┐                           │
│                    │  Data Governance  │                           │
│                    │  （データガバナンス）│                           │
│                    │    [中心・統括]    │                           │
│                    └─────────┬─────────┘                           │
│                              │                                      │
│    ┌─────────────────────────┼─────────────────────────┐           │
│    │                         │                         │           │
│    ▼                         ▼                         ▼           │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ │Data      │  │Data      │  │Data      │  │Reference │  │Data      │
│ │Quality   │  │Architecture│ │Security  │  │& Master  │  │Integration│
│ │品質      │  │アーキテクチャ│ │セキュリティ│  │MDM      │  │統合      │
│ └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
│                                                                     │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ │Metadata  │  │Data      │  │DWH &     │  │Data      │  │Document  │
│ │Management│  │Modeling  │  │BI        │  │Storage   │  │& Content │
│ │メタデータ │  │モデリング │  │DWH/BI   │  │ストレージ│  │文書管理  │
│ └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
└─────────────────────────────────────────────────────────────────────┘
```

---

---

## 2. Prerequisites

- **組織情報**: 対象組織の業種、規模、データ関連の課題
- **ゴール明確化**: データガバナンス構築、品質改善、カタログ作成などの目的
- **現状把握**（任意）: 既存のデータ管理体制、ポリシー、ツールの情報

> **Note**: 本スキルはアドバイザリー型であり、特別なツールやライブラリのインストールは不要です。

---

---

## 3. Quick Start

```bash
┌─────────────────────────────────────────────────────────────┐
│                    DAMA-DMBOK Skill Workflow                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 課題・目的のヒアリング                                    │
│         ↓                                                   │
│  2. 適切なCore Workflowの選択                                │
│     ├── Workflow 1: Data Governance Assessment              │
│     ├── Workflow 2: Data Quality Improvement                │
│     ├── Workflow 3: Data Catalog Creation                   │
│     ├── Workflow 4: Master Data Management                  │
│     └── Workflow 5: Data Strategy Development               │
│         ↓                                                   │
│  3. ワークフローに沿った段階的ガイダンス                        │
│         ↓                                                   │
│  4. 成果物テンプレートの提供・カスタマイズ支援                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. How It Works

本スキルは5つのCore Workflowを提供します。ユーザーの課題に応じて適切なワークフローを選択してください。

```
┌─────────────────────────────────────────────────────────────┐
│                    DAMA-DMBOK Skill Workflow                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 課題・目的のヒアリング                                    │
│         ↓                                                   │
│  2. 適切なCore Workflowの選択                                │
│     ├── Workflow 1: Data Governance Assessment              │
│     ├── Workflow 2: Data Quality Improvement                │
│     ├── Workflow 3: Data Catalog Creation                   │
│     ├── Workflow 4: Master Data Management                  │
│     └── Workflow 5: Data Strategy Development               │
│         ↓                                                   │
│  3. ワークフローに沿った段階的ガイダンス                        │
│         ↓                                                   │
│  4. 成果物テンプレートの提供・カスタマイズ支援                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

詳細は各Core Workflowセクションを参照してください。

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- **データ戦略の策定**
- 全社データ戦略の立案
- データ活用ロードマップの作成
- データ投資の優先順位付け
- **データガバナンスの構築**
- ガバナンス組織体制の設計

---

## 6. Understanding the Output

本スキルはアドバイザリー/ナレッジ型スキルです。主な出力形式:

- **対話型ガイダンス**: ユーザーの状況に応じた段階的なアドバイス
- **フレームワーク適用**: DAMA-DMBOK知識体系に基づく分析・提案
- **テンプレート提供**: `assets/`配下のテンプレートをカスタマイズして提示
- **ベストプラクティス共有**: 業界標準に基づく推奨事項

> **Note**: ファイル自動生成は行いません。必要に応じてテンプレートを会話内で提示し、ユーザーが自身の環境で活用できるようにします。

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/dama-dmbok/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: data_governance.md, metadata_management.md, data_quality.md.
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

---

## 10. Reference

**References:**

- `skills/dama-dmbok/references/data_architecture.md`
- `skills/dama-dmbok/references/data_governance.md`
- `skills/dama-dmbok/references/data_quality.md`
- `skills/dama-dmbok/references/dmbok_overview.md`
- `skills/dama-dmbok/references/master_data_management.md`
- `skills/dama-dmbok/references/metadata_management.md`
