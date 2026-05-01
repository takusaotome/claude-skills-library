---
layout: default
title: "Supply Chain Consultant"
grand_parent: 日本語
parent: プロジェクト・経営
nav_order: 22
lang_peer: /en/skills/management/supply-chain-consultant/
permalink: /ja/skills/management/supply-chain-consultant/
---

# Supply Chain Consultant
{: .no_toc }

Supply Chain Consultant に関する日本語ガイドです。`skills/supply-chain-consultant/SKILL.md` をもとに、利用開始手順、参照ファイル、補助スクリプトへの入口を日本語で整理しています。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/supply-chain-consultant.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/supply-chain-consultant){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

このページは **Supply Chain Consultant** スキルの日本語サマリーです。
- スキル本体: `skills/supply-chain-consultant/SKILL.md`
- 参照ガイド: 6 件
- 補助スクリプト: 3 件
- 詳細な背景説明や判断基準は英語版ガイドを参照してください。

---

## 2. 前提条件

- APIキーは不要です
- Python 3.9 以上を推奨します

---

## 3. クイックスタート

### Workflow 1: Demand Forecasting Optimization

**Purpose**: Improve demand forecast accuracy to reduce stockouts and excess inventory.

---

## 4. 進め方

1. `skills/supply-chain-consultant/SKILL.md` を開き、対象タスクと期待する成果物を確認します。
2. クイックスタートのコマンドや最小サンプルで、手順が通ることを先に確認します。
3. 必要な観点に応じて `references/` 配下のガイドを確認し、判断基準を揃えます。
4. 補助スクリプトがある場合は小さな入力で実行し、出力形式を確認してから本番データへ広げます。
5. 仕上げ時に、出力内容と前提条件が依頼内容に合っているか見直します。

---

## 5. 使用例

- **Supply Chain Consultant** に沿って作業の進め方を整理したいとき
- まず最小の入力やサンプルデータで手順を確認したいとき
- 補助スクリプトを使って定型処理や検証を実行したいとき
- 参照ガイドを見ながら出力の粒度や観点を揃えたいとき
- 詳細な実装判断や例外ケースは英語版ガイドも併用したいとき

---

## 6. 出力の読み方

- スキルの手順に沿った構造化された回答、分析結果、または文書ドラフト
- 参照ガイド 6 件を根拠にした判断材料
- 補助スクリプト 3 件による補助出力や検証結果
- 後続レビューや別スキル連携に回せる中間成果物

---

## 7. ベストプラクティス

- まずは小さな入力で試し、期待する出力形式になっていることを確認してから対象範囲を広げてください。
- 詳細な手順や判断基準は `skills/supply-chain-consultant/SKILL.md` を基準にしてください。
- 参照ガイドは必要なものから順に読むと、過剰に読み散らかさずに進められます。
- 補助スクリプトは本番データの前にサンプル入力で実行し、引数と出力先を確認してください。
- 出力前に、前提条件・入力範囲・未確定事項を明示すると後戻りが減ります。

---

## 8. 他スキルとの連携

- 同じカテゴリのスキルと組み合わせると、計画・実装・レビューまでの流れをつなぎやすくなります。
- 日本語のカテゴリ一覧: [カテゴリページ]({{ '/ja/skills/management/' | relative_url }})
- 詳細な関連ワークフローを探す場合は英語版カテゴリ一覧も参照してください: [English category]({{ '/en/skills/management/' | relative_url }})

---

## 9. トラブルシューティング

- まず前提条件を確認し、必要なランタイムやパッケージが揃っているかを見直してください。
- 補助スクリプトを使う場合は、最小入力で一度実行してから本番データへ広げてください。
- 期待する出力にならない場合は、参照ガイドにある入力形式や観点の前提を確認してください。
- 引数や出力先の指定漏れが多いため、コマンド例をそのまま起点に調整すると安全です。

---

## 10. リファレンス

**参照ガイド:**

- `skills/supply-chain-consultant/references/demand_forecasting_guide.md`
- `skills/supply-chain-consultant/references/inventory_optimization_guide.md`
- `skills/supply-chain-consultant/references/kpi_reference.md`
- `skills/supply-chain-consultant/references/logistics_network_guide.md`
- `skills/supply-chain-consultant/references/procurement_strategy_guide.md`
- `skills/supply-chain-consultant/references/sop_planning_guide.md`

**補助スクリプト:**

- `skills/supply-chain-consultant/scripts/generate_demand_kpi_dashboard.py`
- `skills/supply-chain-consultant/scripts/generate_inventory_policy.py`
- `skills/supply-chain-consultant/scripts/generate_sop_agenda.py`

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/management/supply-chain-consultant/' | relative_url }}) を参照してください。
