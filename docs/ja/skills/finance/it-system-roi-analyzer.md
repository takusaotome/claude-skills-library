---
layout: default
title: "IT System ROI Analyzer"
grand_parent: 日本語
parent: 財務・分析
nav_order: 9
lang_peer: /en/skills/finance/it-system-roi-analyzer/
permalink: /ja/skills/finance/it-system-roi-analyzer/
---

# IT System ROI Analyzer
{: .no_toc }

IT System ROI Analyzer に関する日本語ガイドです。`skills/it-system-roi-analyzer/SKILL.md` をもとに、利用開始手順、参照ファイル、補助スクリプトへの入口を日本語で整理しています。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/it-system-roi-analyzer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/it-system-roi-analyzer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

このページは **IT System ROI Analyzer** スキルの日本語サマリーです。
- スキル本体: `skills/it-system-roi-analyzer/SKILL.md`
- 参照ガイド: 3 件
- 補助スクリプト: 1 件
- 詳細な背景説明や判断基準は英語版ガイドを参照してください。

---

## 2. 前提条件

- APIキーは不要です
- Python 3.9 以上を推奨します
- 詳細な実行条件は英語版ガイドまたは `SKILL.md` を参照してください。

---

## 3. クイックスタート

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

## 4. 進め方

1. `skills/it-system-roi-analyzer/SKILL.md` を開き、対象タスクと期待する成果物を確認します。
2. クイックスタートのコマンドや最小サンプルで、手順が通ることを先に確認します。
3. 必要な観点に応じて `references/` 配下のガイドを確認し、判断基準を揃えます。
4. 補助スクリプトがある場合は小さな入力で実行し、出力形式を確認してから本番データへ広げます。
5. 仕上げ時に、出力内容と前提条件が依頼内容に合っているか見直します。

---

## 5. 使用例

- **IT System ROI Analyzer** に沿って作業の進め方を整理したいとき
- まず最小の入力やサンプルデータで手順を確認したいとき
- 補助スクリプトを使って定型処理や検証を実行したいとき
- 参照ガイドを見ながら出力の粒度や観点を揃えたいとき
- 詳細な実装判断や例外ケースは英語版ガイドも併用したいとき

---

## 6. 出力の読み方

- スキルの手順に沿った構造化された回答、分析結果、または文書ドラフト
- 参照ガイド 3 件を根拠にした判断材料
- 補助スクリプト 1 件による補助出力や検証結果
- 後続レビューや別スキル連携に回せる中間成果物

---

## 7. ベストプラクティス

- まずは小さな入力で試し、期待する出力形式になっていることを確認してから対象範囲を広げてください。
- 詳細な手順や判断基準は `skills/it-system-roi-analyzer/SKILL.md` を基準にしてください。
- 参照ガイドは必要なものから順に読むと、過剰に読み散らかさずに進められます。
- 補助スクリプトは本番データの前にサンプル入力で実行し、引数と出力先を確認してください。
- 出力前に、前提条件・入力範囲・未確定事項を明示すると後戻りが減ります。

---

## 8. 他スキルとの連携

- 同じカテゴリのスキルと組み合わせると、計画・実装・レビューまでの流れをつなぎやすくなります。
- 日本語のカテゴリ一覧: [カテゴリページ]({{ '/ja/skills/finance/' | relative_url }})
- 詳細な関連ワークフローを探す場合は英語版カテゴリ一覧も参照してください: [English category]({{ '/en/skills/finance/' | relative_url }})

---

## 9. トラブルシューティング

- まず前提条件を確認し、必要なランタイムやパッケージが揃っているかを見直してください。
- 補助スクリプトを使う場合は、最小入力で一度実行してから本番データへ広げてください。
- 期待する出力にならない場合は、参照ガイドにある入力形式や観点の前提を確認してください。
- Python のバージョン差分が原因になることがあるため、推奨バージョンを確認してください。
- 引数や出力先の指定漏れが多いため、コマンド例をそのまま起点に調整すると安全です。

---

## 10. リファレンス

**参照ガイド:**

- `skills/it-system-roi-analyzer/references/benefit_quantification.md`
- `skills/it-system-roi-analyzer/references/it_roi_methodology.md`
- `skills/it-system-roi-analyzer/references/tco_analysis_guide.md`

**補助スクリプト:**

- `skills/it-system-roi-analyzer/scripts/it_roi_calculator.py`

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/finance/it-system-roi-analyzer/' | relative_url }}) を参照してください。
