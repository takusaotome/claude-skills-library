---
layout: default
title: Strategic Planner
grand_parent: 日本語
parent: プロジェクト・経営
nav_order: 3
lang_peer: /en/skills/management/strategic-planner/
permalink: /ja/skills/management/strategic-planner/
---

# Strategic Planner
{: .no_toc }

MBA標準の戦略フレームワークを活用した体系的な戦略企画 -- SWOT、PEST、Porter 5F、BCG/GEマトリクス、Ansoff、ビジネスモデルキャンバス等を網羅。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>
<span class="badge badge-workflow">ワークフロー</span>

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 概要

Strategic Plannerは、中期経営計画・新規事業企画・事業ポートフォリオ分析を、確立された戦略フレームワークを用いて体系的に作成するスキルです。環境分析からMermaidガントチャートによる実行ロードマップまで、戦略立案の全サイクルをカバーします。

利用可能なフレームワーク:

| フレームワーク | 用途 |
|:--------------|:-----|
| PEST / PESTLE | マクロ環境分析 |
| Porter's Five Forces | 業界競争構造分析 |
| Value Chain | 内部能力の評価 |
| SWOT / Cross-SWOT | 戦略オプションの導出 |
| Business Model Canvas / Lean Canvas | ビジネスモデル設計 |
| BCG Matrix / GE Matrix | ポートフォリオ投資配分 |
| Ansoff Matrix | 成長戦略の方向性決定 |
| Balanced Scorecard | 戦略KPI体系の構築 |

## 利用シーン

- **中期経営計画策定** -- 「製造部門の3年間の戦略計画を策定したい」
- **新規事業企画** -- 「新しいSaaS製品のビジネスモデルを設計したい」
- **ポートフォリオ分析** -- 「5つの事業部門の投資優先度を評価したい」
- **個別フレームワーク活用** -- 「SWOT分析をしたい」「Porter 5F分析を行いたい」
- **戦略ロードマップ** -- 「成長戦略のガントベースの実行ロードマップを作成したい」

## 前提条件

- `strategic-planner` スキルがインストールされたClaude Code
- 分析対象の事業・業界に関する基本的な知識
- 外部APIや有料サービスは不要

## 仕組み

7つのワークフローを個別または組み合わせて使用します。

1. **現状分析** -- PEST/PESTLEによるマクロトレンド、Porter's Five Forcesによる業界構造、Value Chainによる内部強み分析。環境分析レポートを出力。
2. **SWOT分析と戦略オプション** -- 分析結果をSWOTマトリクスに統合し、Cross-SWOT（SO/WO/ST/WT象限）で戦略を導出。加重スコアリングで優先順位付け。
3. **ビジョンと戦略目標** -- ビジョンステートメント策定、ミッションとの整合確認、Balanced Scorecardの4視点（財務・顧客・業務プロセス・学習と成長）による戦略目標設定、KPI体系の構築。
4. **ビジネスモデル設計** -- Business Model Canvas（9ブロック）またはLean Canvas（スタートアップ/新規事業向け）の作成。バリュープロポジションと収益モデルの設計。
5. **ポートフォリオ分析** -- BCGマトリクス（Star/Cash Cow/Question Mark/Dog）、GE/McKinsey 9セルマトリクス、Ansoffマトリクスの適用。投資配分の提言。
6. **戦略施策とロードマップ** -- 戦略オプションを具体的施策に変換、戦略適合性/実現可能性/インパクト/緊急性で優先順位付け、Mermaidガントでロードマップ作成、マイルストーン設定。
7. **中期経営計画の統合** -- 全分析を統合し、エグゼクティブサマリー・財務計画・投資計画・リスクマトリクス・ガバナンス体制・KPIダッシュボードを含む計画書を完成。

### 成果物別ワークフロー対応表

| 成果物 | 必須ワークフロー | オプション |
|:-------|:--------------|:----------|
| 中期経営計画 | 1, 2, 3, 5, 6, 7 | 4 |
| 新規事業企画書 | 1, 2, 4 | 3, 6 |
| ポートフォリオ分析レポート | 1, 5 | 2 |
| SWOT分析レポート | 1, 2 | -- |

## 使用例

### 例1: 中期経営計画

```
中堅製造業（年商500億円）の3年間の中期経営計画を作成してください。
主要課題: ICE部品からEV部品への転換。
PEST、Porter 5F、SWOT、ポートフォリオ分析、財務目標、
実行ロードマップを含めてください。
```

### 例2: 新規事業企画

```
AI文書管理プラットフォームのSaaSビジネスモデルを設計してください。
ターゲットは中小企業です。
Lean Canvas、バリュープロポジション分析、収益モデル、
主要指標を含めてください。
```

### 例3: SWOT分析と戦略オプション

```
当社小売チェーンのCross-SWOT分析を実施してください。
強み: 強いブランド、200店舗
弱み: EC未対応、老朽化したITシステム
機会: O2O、サブスクリプションモデル
脅威: Amazon、賃料上昇
優先順位付きの戦略オプションを導出してください。
```

## ヒントとベストプラクティス

- **データに基づく分析を。** 「ブランド力が強い」のような曖昧なSWOT記述は避け、「ターゲット層でのブランド認知78%（業界平均45%）」のように測定可能な表現を使いましょう。
- **単純SWOTよりCross-SWOTを。** 単純なSWOTリストは記述的ですが、Cross-SWOTは交差点からアクション可能な戦略オプションを生成します。
- **施策を絞り込む。** 20の戦略施策がある計画は焦点が定まりません。5-7の高優先施策に絞りましょう。
- **ロードマップにはMermaidガントを。** ビジュアルなタイムラインにより、ステークホルダーがフェージングと依存関係を一目で把握できます。
- **エグゼクティブサマリーは最後に書く。** 全分析を完了してから、要点を簡潔な1ページにまとめましょう。
- **ポートフォリオ評価基準は事前合意を。** ステークホルダーと評価ウェイトを事前に合意しておくことで、後の主観性の議論を避けられます。

## 関連スキル

- [Business Analyst]({{ '/ja/skills/management/business-analyst/' | relative_url }}) -- 詳細な要件分析とプロセス分析が戦略レベルの計画を補完します。
- [Project Plan Creator]({{ '/ja/skills/management/project-plan-creator/' | relative_url }}) -- 戦略施策を実行可能なプロジェクト計画に変換します。
- [Vendor Estimate Creator]({{ '/ja/skills/management/vendor-estimate-creator/' | relative_url }}) -- 戦略的投資施策のコスト見積を作成します。
