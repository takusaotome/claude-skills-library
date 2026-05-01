---
layout: default
title: "AI-BPO Proposal Generator"
grand_parent: 日本語
parent: プロジェクト・経営
nav_order: 29
lang_peer: /en/skills/management/ai-bpo-proposal-generator/
permalink: /ja/skills/management/ai-bpo-proposal-generator/
---

# AI-BPO Proposal Generator
{: .no_toc }

在米日系企業向けの AI 活用 BPO 提案書を生成するスキル。サービスモジュール選定、ROI 試算、実装ロードマップ、バイリンガル提案文書を含みます。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ai-bpo-proposal-generator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/ai-bpo-proposal-generator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

F&A・HR/Payroll・カスタマーサポート・データ処理・調達の 5 カテゴリ・計 15 サービスモジュールから選定し、現状 vs. 将来の ROI / NPV / 回収期間を計算。フェーズ別実装ロードマップ・3 業界向けバンドル・バイリンガル提案文書を出力します。

---

## 2. 前提条件

- Python 3.9+
- No API keys required

---

## 3. クイックスタート

```bash
# ローカルにスキルをインストール
make install SKILL=ai-bpo-proposal-generator

# または .skill パッケージを取得
curl -L -o ai-bpo-proposal-generator.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/ai-bpo-proposal-generator.skill
```

その後、Claude Code 内でやりたいことを自然言語で記述するとスキルが自動起動します。トリガーとなるフレーズは「使用例」セクションを参照してください。

---

## 4. 進め方

スキルは `SKILL.md` に記載されたワークフローに従って動作します。主要ステージ：

1. **入力パース** — ユーザーリクエストと提供されたソースファイルを解釈
2. **コア処理** — スキル固有のドメインロジックを適用（リファレンスセクション参照）
3. **出力生成** — 後段で利用可能な構造化アーティファクト（Markdown／JSON／テンプレート）を生成

完全な手順は `skills/ai-bpo-proposal-generator/SKILL.md` を参照してください。

---

## 5. 使用例

- 在米日系企業向けに AI を活用した BPO サービスを提案する
- ROI 試算入りのバイリンガル提案書（JA/EN）が必要
- 聞き取り → サービス選定 → ロードマップ → 提案書 の構造化フローを使いたい
- 業界別（F&A、HR、CS等）のサービスバンドルが必要

---

## 6. 出力の読み方

スキルはテンプレートとリファレンスドキュメント（セクション10参照）の規約に従って構造化出力を生成します。出力は：

- **再現性** — 同じ入力＋同じテンプレートなら同じ出力構造
- **レビュー可能** — 各セクションが一貫してラベル付け・順序付け
- **連携可能** — このスキルの出力を隣接スキルに渡せる（セクション8参照）

---

## 7. ベストプラクティス

- まずは小さな現実的な入力でワークフローを検証してから本番データに広げる
- このガイドと並行して `skills/ai-bpo-proposal-generator/SKILL.md` を開く（こちらが正本）
- 全リファレンスを読破するのではなく、関連性の高いものから順に確認する
- 本番データに適用する前にテストデータでスクリプトを実行する
- 中間出力を保持して、想定や判断の根拠を後から説明できるようにする

---

## 8. 他スキルとの連携

- 同じカテゴリの隣接スキルと組み合わせて、計画→実装→レビューの流れをカバー
- プロジェクト・経営 カテゴリで関連ワークフローを探す: [カテゴリ一覧]({{ '/ja/skills/management/' | relative_url }})
- 日本語スキルカタログ全体: [スキルカタログ]({{ '/ja/skill-catalog/' | relative_url }})

---

## 9. トラブルシューティング

- まず前提条件を確認。ランタイム依存が欠けているのが最頻出の失敗パターン
- 補助スクリプトは最小入力でまず実行してから本番データに広げる
- 入力データの構造をリファレンスと比較し、期待フィールド／セクション／メタデータが揃っているか確認
- Python のバージョン（3.9以上）と必要パッケージがアクティブな環境にインストールされているか確認
- 出力が不完全に見える場合は、関連リファレンスを再読して入力契約を再検証

---

## 10. リファレンス

**参照ガイド:**

- `skills/ai-bpo-proposal-generator/references/client-intake-template.md`
- `skills/ai-bpo-proposal-generator/references/roi-methodology.md`
- `skills/ai-bpo-proposal-generator/references/service-catalog.md`

**スクリプト:**

- `skills/ai-bpo-proposal-generator/scripts/calculate_roi.py`
- `skills/ai-bpo-proposal-generator/scripts/generate_proposal.py`
- `skills/ai-bpo-proposal-generator/scripts/generate_roadmap.py`
- `skills/ai-bpo-proposal-generator/scripts/select_services.py`

**アセット:**

_(なし)_

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/management/ai-bpo-proposal-generator/' | relative_url }}) を参照してください。
