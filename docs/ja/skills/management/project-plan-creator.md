---
layout: default
title: Project Plan Creator
grand_parent: 日本語
parent: プロジェクト・経営
nav_order: 1
lang_peer: /en/skills/management/project-plan-creator/
permalink: /ja/skills/management/project-plan-creator/
---

# Project Plan Creator
{: .no_toc }

PMBOK準拠のプロジェクト計画を、WBS・ガントチャート・RACI・リスク管理を含めてMarkdown + Mermaid図で一括作成します。
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

Project Plan Creatorは、プロジェクトの要件とステークホルダーのニーズから、PMBOK準拠のプロジェクト管理成果物一式を作成するスキルです。チャーター作成、スコープ定義、WBS策定、ガントチャートによるスケジュール作成、RACIマトリクスによるリソース計画、リスク管理計画までを体系的にカバーします。

出力はMarkdown + Mermaid図形式で、GitHub・GitLab等のMarkdown対応ツールでそのまま表示できます。

11ファイル（544KB）のPMナレッジベース（PMBOK第6/7/8版、DevOps/Agileベストプラクティス、IT PM指針、PRINCE2・ITIL 4・ISO 21502とのクロスフレームワーク対応表）を参照可能です。

## 利用シーン

- 新規システム開発・導入プロジェクトの立ち上げ
- プロジェクトチャーターの正式作成
- WBS・スケジュール・リソース配分を含む包括的なプロジェクト計画の策定
- Mermaid図（ガント・WBS・ワークフロー）によるプロジェクト構造の可視化
- PMBOK準拠のプロジェクトドキュメント作成

## 前提条件

- `project-plan-creator` スキルがインストールされたClaude Code
- プロジェクトのスコープとステークホルダーの基本的な把握
- 外部APIや有料サービスは不要

## 仕組み

7つのワークフローを順に実行します。

1. **プロジェクトチャーター作成** -- インプット収集、目的・スコープ・マイルストーン・予算・ステークホルダー・成功基準の定義
2. **スコープ定義とWBS** -- チャーターの高レベルスコープを詳細化し、Mermaid図付きの階層的WBSを作成
3. **スケジュール作成** -- アクティビティ定義、依存関係設定（FS/SS/FF/SF）、PERT三点見積もり、Mermaidガントチャートとクリティカルパス分析
4. **リソース計画とRACI** -- プロジェクトロール定義、RACIマトリクス、コミュニケーションプロトコル、チーム体制図の可視化
5. **リスク管理** -- リスク識別（技術・スコープ・リソース・統合・外部）、確率と影響の評価、対応戦略の計画、モニタリングプロセスの確立
6. **コミュニケーションと品質計画** -- ステークホルダーの情報ニーズ定義、品質基準、QAプロセス、受け入れ基準
7. **統合とドキュメント生成** -- 全成果物を12セクション・5つ以上のMermaid図を含むプロジェクト計画書に統合

## 使用例

### 例1: プロジェクトチャーターの作成

```
ECサイトリニューアルプロジェクトのプロジェクトチャーターを作成してください。
予算: 1億円、期間: 2026年4月～11月、
PM: 鈴木花子、スポンサー: CTO山田
```

### 例2: フルプロジェクト計画の生成

```
CRM刷新プロジェクトです。画面数50、API40本、
外部連携3システムの規模です。
WBS、ガントチャート、RACIマトリクス、リスク登録簿を含む
完全なプロジェクト計画を作成してください。
```

### 例3: リスク管理計画のみ

```
オンプレERPのクラウド移行を計画しています。
技術リスク、データ移行リスク、組織変革リスクをカバーした
リスク管理計画を作成してください。
```

## ヒントとベストプラクティス

- **チャーターから始める。** プロジェクトを正式に認可するチャーターを先に作ることで、スコープの混乱を防げます。
- **Mermaid図を活用する。** GitHub、GitLab等でネイティブ表示できるため、画像のエクスポートが不要です。
- **RACIは早めに定義する。** 各成果物にAccountable（説明責任者）が1名だけ設定されていることを確認しましょう。
- **スケジュールは保守的に。** PERT三点見積もりを使い、クリティカルパスにはバッファを設けましょう。
- **ベースラインを確定する。** 計画承認後はベースラインとして保存し、変更はスコープ変更管理プロセスを通します。
- **ナレッジベースを活用する。** PMBOK標準やSaaS PMのQ&A、クロスフレームワーク対応表を参照できます。

## 関連スキル

- [Business Analyst]({{ '/ja/skills/management/business-analyst/' | relative_url }}) -- 要件定義とBRD作成がプロジェクト計画のインプットになります。
- [Vendor Estimate Creator]({{ '/ja/skills/management/vendor-estimate-creator/' | relative_url }}) -- プロジェクト計画と整合するWBS付きコスト見積を作成できます。
- [Strategic Planner]({{ '/ja/skills/management/strategic-planner/' | relative_url }}) -- 戦略方針がプロジェクト目標のインプットになります。
