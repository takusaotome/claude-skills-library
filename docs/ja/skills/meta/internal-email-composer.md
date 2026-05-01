---
layout: default
title: "Internal Email Composer"
grand_parent: 日本語
parent: メタ・品質
nav_order: 26
lang_peer: /en/skills/meta/internal-email-composer/
permalink: /ja/skills/meta/internal-email-composer/
---

# Internal Email Composer
{: .no_toc }

見積依頼転送、タスク依頼、進捗報告、フォローアップなどの社内調整メールを作成するスキル。適切なビジネストーンでバイリンガル（JA/EN）ドラフトを生成します。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/internal-email-composer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/internal-email-composer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

6 つの社内シナリオ（見積依頼転送、タスク依頼、進捗報告、フォローアップ、エスカレーション、情報依頼）に対応するプロフェッショナルなバイリンガルメールを作成。日本語は適切な敬語レベル、英語はビジネストーンを適用、3 段階の緊急度が件名プレフィックスと挨拶を切り替えます。

---

## 2. 前提条件

- Python 3.9+
- No API keys required

---

## 3. クイックスタート

```bash
# ローカルにスキルをインストール
make install SKILL=internal-email-composer

# または .skill パッケージを取得
curl -L -o internal-email-composer.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/internal-email-composer.skill
```

その後、Claude Code 内でやりたいことを自然言語で記述するとスキルが自動起動します。トリガーとなるフレーズは「使用例」セクションを参照してください。

---

## 4. 進め方

スキルは `SKILL.md` に記載されたワークフローに従って動作します。主要ステージ：

1. **入力パース** — ユーザーリクエストと提供されたソースファイルを解釈
2. **コア処理** — スキル固有のドメインロジックを適用（リファレンスセクション参照）
3. **出力生成** — 後段で利用可能な構造化アーティファクト（Markdown／JSON／テンプレート）を生成

完全な手順は `skills/internal-email-composer/SKILL.md` を参照してください。

---

## 5. 使用例

- バイリンガル調整付きで vendor RFQ を社内転送している
- メールでタスク依頼する際、JA/EN ドラフトの統一感が欲しい
- 週次ステータス更新を定型トーンで送りたい
- 緊急度別の件名プレフィックス（例: [URGENT]）が必要

---

## 6. 出力の読み方

スキルはテンプレートとリファレンスドキュメント（セクション10参照）の規約に従って構造化出力を生成します。出力は：

- **再現性** — 同じ入力＋同じテンプレートなら同じ出力構造
- **レビュー可能** — 各セクションが一貫してラベル付け・順序付け
- **連携可能** — このスキルの出力を隣接スキルに渡せる（セクション8参照）

---

## 7. ベストプラクティス

- まずは小さな現実的な入力でワークフローを検証してから本番データに広げる
- このガイドと並行して `skills/internal-email-composer/SKILL.md` を開く（こちらが正本）
- 全リファレンスを読破するのではなく、関連性の高いものから順に確認する
- 本番データに適用する前にテストデータでスクリプトを実行する
- 中間出力を保持して、想定や判断の根拠を後から説明できるようにする

---

## 8. 他スキルとの連携

- 同じカテゴリの隣接スキルと組み合わせて、計画→実装→レビューの流れをカバー
- メタ・品質 カテゴリで関連ワークフローを探す: [カテゴリ一覧]({{ '/ja/skills/meta/' | relative_url }})
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

- `skills/internal-email-composer/references/business-etiquette-guide.md`
- `skills/internal-email-composer/references/email-templates.md`

**スクリプト:**

- `skills/internal-email-composer/scripts/compose_email.py`

**アセット:**

_(なし)_

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/meta/internal-email-composer/' | relative_url }}) を参照してください。
