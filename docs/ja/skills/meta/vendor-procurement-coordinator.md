---
layout: default
title: "Vendor Procurement Coordinator"
grand_parent: 日本語
parent: メタ・品質
nav_order: 29
lang_peer: /en/skills/meta/vendor-procurement-coordinator/
permalink: /ja/skills/meta/vendor-procurement-coordinator/
---

# Vendor Procurement Coordinator
{: .no_toc }

RFQ 作成、メール送信、ベンダー応答追跡、顧客向け見積生成を統括する一気通貫のベンダー調達ワークフロースキル。vendor-rfq-creator と vendor-estimate-creator スキルをメール自動化と状態追跡で連携させます。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-procurement-coordinator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/vendor-procurement-coordinator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

標準ディレクトリ構造（rfq/、quotes/、estimates/、communications/）で調達プロジェクトを初期化、ベンダーを状態追跡付きで管理（追加／編集／削除／CSV インポート）、見積応答を金額／通貨／納期／有効期限付きでログ、日英 RFQ メールテンプレートとリマインダーテンプレートを提供、価格スコア付きベンダー比較レポートを生成、監査証跡用の完全なタイムラインを出力します。

---

## 2. 前提条件

- Python 3.9+
- PyYAML
- No API keys required

---

## 3. クイックスタート

```bash
# ローカルにスキルをインストール
make install SKILL=vendor-procurement-coordinator

# または .skill パッケージを取得
curl -L -o vendor-procurement-coordinator.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-procurement-coordinator.skill
```

その後、Claude Code 内でやりたいことを自然言語で記述するとスキルが自動起動します。トリガーとなるフレーズは「使用例」セクションを参照してください。

---

## 4. 進め方

スキルは `SKILL.md` に記載されたワークフローに従って動作します。主要ステージ：

1. **入力パース** — ユーザーリクエストと提供されたソースファイルを解釈
2. **コア処理** — スキル固有のドメインロジックを適用（リファレンスセクション参照）
3. **出力生成** — 後段で利用可能な構造化アーティファクト（Markdown／JSON／テンプレート）を生成

完全な手順は `skills/vendor-procurement-coordinator/SKILL.md` を参照してください。

---

## 5. 使用例

- ベンダー RFQ を一気通貫で管理（依頼 → 見積 → 顧客提示）する
- 複数ベンダーを単一の調達状態として管理したい
- バイリンガル（JA/EN）RFQ メールとリマインダーを定期送信したい
- 監査用に調達イベントの完全な追跡履歴が欲しい

---

## 6. 出力の読み方

スキルはテンプレートとリファレンスドキュメント（セクション10参照）の規約に従って構造化出力を生成します。出力は：

- **再現性** — 同じ入力＋同じテンプレートなら同じ出力構造
- **レビュー可能** — 各セクションが一貫してラベル付け・順序付け
- **連携可能** — このスキルの出力を隣接スキルに渡せる（セクション8参照）

---

## 7. ベストプラクティス

- まずは小さな現実的な入力でワークフローを検証してから本番データに広げる
- このガイドと並行して `skills/vendor-procurement-coordinator/SKILL.md` を開く（こちらが正本）
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

- `skills/vendor-procurement-coordinator/references/procurement_workflow_guide.md`
- `skills/vendor-procurement-coordinator/references/vendor_evaluation_criteria.md`

**スクリプト:**

- `skills/vendor-procurement-coordinator/scripts/compare_quotes.py`
- `skills/vendor-procurement-coordinator/scripts/init_procurement.py`
- `skills/vendor-procurement-coordinator/scripts/manage_vendors.py`
- `skills/vendor-procurement-coordinator/scripts/procurement_models.py`
- `skills/vendor-procurement-coordinator/scripts/track_responses.py`

**アセット:**

- `skills/vendor-procurement-coordinator/assets/email_templates/reminder_email.md`
- `skills/vendor-procurement-coordinator/assets/email_templates/rfq_email_en.md`
- `skills/vendor-procurement-coordinator/assets/email_templates/rfq_email_ja.md`

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/meta/vendor-procurement-coordinator/' | relative_url }}) を参照してください。
