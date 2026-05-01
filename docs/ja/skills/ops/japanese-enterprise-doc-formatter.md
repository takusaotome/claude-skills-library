---
layout: default
title: "Japanese Enterprise Document Formatter"
grand_parent: 日本語
parent: 運用・ドキュメント
nav_order: 13
lang_peer: /en/skills/ops/japanese-enterprise-doc-formatter/
permalink: /ja/skills/ops/japanese-enterprise-doc-formatter/
---

# Japanese Enterprise Document Formatter
{: .no_toc }

稟議書・購入申請書・提案書など、日本企業の稟議ワークフロー向けにドキュメントをフォーマットするスキル。バイリンガル要件、適切な敬語レベル、必須承認セクション、社内テンプレ準拠を扱います。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/japanese-enterprise-doc-formatter.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/japanese-enterprise-doc-formatter){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

5 つの企業文書タイプ（稟議書／購入申請書／提案書／報告書／依頼書）を、4 つの敬語レベル（最上級／上級／標準／基本）でフォーマット。完全性スコア付きセクション検証、英語サマリー付きバイリンガル出力、文書タイプに応じた承認セクション生成を含みます。

---

## 2. 前提条件

- Python 3.9+
- No API keys required

---

## 3. クイックスタート

```bash
# ローカルにスキルをインストール
make install SKILL=japanese-enterprise-doc-formatter

# または .skill パッケージを取得
curl -L -o japanese-enterprise-doc-formatter.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/japanese-enterprise-doc-formatter.skill
```

その後、Claude Code 内でやりたいことを自然言語で記述するとスキルが自動起動します。トリガーとなるフレーズは「使用例」セクションを参照してください。

---

## 4. 進め方

スキルは `SKILL.md` に記載されたワークフローに従って動作します。主要ステージ：

1. **入力パース** — ユーザーリクエストと提供されたソースファイルを解釈
2. **コア処理** — スキル固有のドメインロジックを適用（リファレンスセクション参照）
3. **出力生成** — 後段で利用可能な構造化アーティファクト（Markdown／JSON／テンプレート）を生成

完全な手順は `skills/japanese-enterprise-doc-formatter/SKILL.md` を参照してください。

---

## 5. 使用例

- 稟議書・購入申請書・提案書など、社内承認向け文書を作成する
- 文書タイプごとの敬語レベル正規化を自動化したい
- 必須セクション構造（背景／目的／効果／費用／承認 等）に対するバリデーションが欲しい
- 海外承認も通すためのバイリンガル版を生成したい

---

## 6. 出力の読み方

スキルはテンプレートとリファレンスドキュメント（セクション10参照）の規約に従って構造化出力を生成します。出力は：

- **再現性** — 同じ入力＋同じテンプレートなら同じ出力構造
- **レビュー可能** — 各セクションが一貫してラベル付け・順序付け
- **連携可能** — このスキルの出力を隣接スキルに渡せる（セクション8参照）

---

## 7. ベストプラクティス

- まずは小さな現実的な入力でワークフローを検証してから本番データに広げる
- このガイドと並行して `skills/japanese-enterprise-doc-formatter/SKILL.md` を開く（こちらが正本）
- 全リファレンスを読破するのではなく、関連性の高いものから順に確認する
- 本番データに適用する前にテストデータでスクリプトを実行する
- 中間出力を保持して、想定や判断の根拠を後から説明できるようにする

---

## 8. 他スキルとの連携

- 同じカテゴリの隣接スキルと組み合わせて、計画→実装→レビューの流れをカバー
- 運用・ドキュメント カテゴリで関連ワークフローを探す: [カテゴリ一覧]({{ '/ja/skills/ops/' | relative_url }})
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

- `skills/japanese-enterprise-doc-formatter/references/document_types.md`
- `skills/japanese-enterprise-doc-formatter/references/keigo_guide.md`
- `skills/japanese-enterprise-doc-formatter/references/section_templates.md`

**スクリプト:**

- `skills/japanese-enterprise-doc-formatter/scripts/format_document.py`
- `skills/japanese-enterprise-doc-formatter/scripts/transform_keigo.py`
- `skills/japanese-enterprise-doc-formatter/scripts/validate_sections.py`

**アセット:**

_(なし)_

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/ops/japanese-enterprise-doc-formatter/' | relative_url }}) を参照してください。
