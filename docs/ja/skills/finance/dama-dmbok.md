---
layout: default
title: "Dama Dmbok"
grand_parent: 日本語
parent: 財務・分析
nav_order: 5
lang_peer: /en/skills/finance/dama-dmbok/
permalink: /ja/skills/finance/dama-dmbok/
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

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/dama-dmbok.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/dama-dmbok){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

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

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- **組織情報**: 対象組織の業種、規模、データ関連の課題
- **ゴール明確化**: データガバナンス構築、品質改善、カタログ作成などの目的
- **現状把握**（任意）: 既存のデータ管理体制、ポリシー、ツールの情報

> **Note**: 本スキルはアドバイザリー型であり、特別なツールやライブラリのインストールは不要です。

---

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

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

- `skills/dama-dmbok/references/data_architecture.md`
- `skills/dama-dmbok/references/data_governance.md`
- `skills/dama-dmbok/references/data_quality.md`
- `skills/dama-dmbok/references/dmbok_overview.md`
- `skills/dama-dmbok/references/master_data_management.md`
- `skills/dama-dmbok/references/metadata_management.md`
