---
layout: default
title: "Critical Document Reviewer"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 14
lang_peer: /en/skills/dev/critical-document-reviewer/
permalink: /ja/skills/dev/critical-document-reviewer/
---

# Critical Document Reviewer
{: .no_toc }

Critical Document Reviewer に関する日本語ガイドです。`skills/critical-document-reviewer/SKILL.md` をもとに、利用開始手順、参照ファイル、補助スクリプトへの入口を日本語で整理しています。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/critical-document-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/critical-document-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

このページは **Critical Document Reviewer** スキルの日本語サマリーです。
- スキル本体: `skills/critical-document-reviewer/SKILL.md`
- 参照ガイド: 6 件
- 補助スクリプト: なし
- 詳細な背景説明や判断基準は英語版ガイドを参照してください。

---

## 2. 前提条件

- APIキーは不要です
- Python 3.9 以上を推奨します
- 詳細な実行条件は英語版ガイドまたは `SKILL.md` を参照してください。

---

## 3. クイックスタート

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

## 4. 進め方

1. `skills/critical-document-reviewer/SKILL.md` を開き、対象タスクと期待する成果物を確認します。
2. クイックスタートのコマンドや最小サンプルで、手順が通ることを先に確認します。
3. 必要な観点に応じて `references/` 配下のガイドを確認し、判断基準を揃えます。
4. スキルの手順に沿って対話またはドキュメント作成を進めます。
5. 仕上げ時に、出力内容と前提条件が依頼内容に合っているか見直します。

---

## 5. 使用例

- **Critical Document Reviewer** に沿って作業の進め方を整理したいとき
- まず最小の入力やサンプルデータで手順を確認したいとき
- 参照ガイドを見ながら出力の粒度や観点を揃えたいとき
- 詳細な実装判断や例外ケースは英語版ガイドも併用したいとき

---

## 6. 出力の読み方

- スキルの手順に沿った構造化された回答、分析結果、または文書ドラフト
- 参照ガイド 6 件を根拠にした判断材料
- 後続レビューや別スキル連携に回せる中間成果物

---

## 7. ベストプラクティス

- まずは小さな入力で試し、期待する出力形式になっていることを確認してから対象範囲を広げてください。
- 詳細な手順や判断基準は `skills/critical-document-reviewer/SKILL.md` を基準にしてください。
- 参照ガイドは必要なものから順に読むと、過剰に読み散らかさずに進められます。
- 出力前に、前提条件・入力範囲・未確定事項を明示すると後戻りが減ります。

---

## 8. 他スキルとの連携

- 同じカテゴリのスキルと組み合わせると、計画・実装・レビューまでの流れをつなぎやすくなります。
- 日本語のカテゴリ一覧: [カテゴリページ]({{ '/ja/skills/dev/' | relative_url }})
- 詳細な関連ワークフローを探す場合は英語版カテゴリ一覧も参照してください: [English category]({{ '/en/skills/dev/' | relative_url }})

---

## 9. トラブルシューティング

- まず前提条件を確認し、必要なランタイムやパッケージが揃っているかを見直してください。
- 補助スクリプトを使う場合は、最小入力で一度実行してから本番データへ広げてください。
- 期待する出力にならない場合は、参照ガイドにある入力形式や観点の前提を確認してください。

---

## 10. リファレンス

**参照ガイド:**

- `skills/critical-document-reviewer/references/critical_analysis_framework.md`
- `skills/critical-document-reviewer/references/evidence_evaluation_criteria.md`
- `skills/critical-document-reviewer/references/persona_selection_matrix.md`
- `skills/critical-document-reviewer/references/red_flag_patterns.md`
- `skills/critical-document-reviewer/references/scale_strategy.md`
- `skills/critical-document-reviewer/references/severity_criteria.md`

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/dev/critical-document-reviewer/' | relative_url }}) を参照してください。
