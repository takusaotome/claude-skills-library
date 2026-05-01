---
layout: default
title: "Action Status Updater"
grand_parent: 日本語
parent: メタ・品質
nav_order: 24
lang_peer: /en/skills/meta/action-status-updater/
permalink: /ja/skills/meta/action-status-updater/
---

# Action Status Updater
{: .no_toc }

アクションアイテムの状態を「Seanのメールには返信しておいた」「Lu対応予定」のような自然言語更新から追跡するスキル。daily-comms-ops ワークフローと連携します。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/action-status-updater.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/action-status-updater){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

日本語と英語の自然言語ステータス更新をパースし、意図（完了/委任/延期/進行中）と担当者・チャネル・キーワードを抽出して、YAML に状態を永続化します。後でレポート出力できます。

---

## 2. 前提条件

- Python 3.9+
- PyYAML
- No API keys required

---

## 3. クイックスタート

```bash
# ローカルにスキルをインストール
make install SKILL=action-status-updater

# または .skill パッケージを取得
curl -L -o action-status-updater.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/action-status-updater.skill
```

その後、Claude Code 内でやりたいことを自然言語で記述するとスキルが自動起動します。トリガーとなるフレーズは「使用例」セクションを参照してください。

---

## 4. 進め方

スキルは `SKILL.md` に記載されたワークフローに従って動作します。主要ステージ：

1. **入力パース** — ユーザーリクエストと提供されたソースファイルを解釈
2. **コア処理** — スキル固有のドメインロジックを適用（リファレンスセクション参照）
3. **出力生成** — 後段で利用可能な構造化アーティファクト（Markdown／JSON／テンプレート）を生成

完全な手順は `skills/action-status-updater/SKILL.md` を参照してください。

---

## 5. 使用例

- 「Seanにフォローした」「Lu対応予定」のような日本語＋英語混在のステータス更新を記録している
- Slack/メール/会議をまたぐアクションアイテムの単一管理元が欲しい
- NL メモから日次/週次ステータスレポートを生成したい
- daily-comms-ops ループからアクション追跡を自動更新したい

---

## 6. 出力の読み方

スキルはテンプレートとリファレンスドキュメント（セクション10参照）の規約に従って構造化出力を生成します。出力は：

- **再現性** — 同じ入力＋同じテンプレートなら同じ出力構造
- **レビュー可能** — 各セクションが一貫してラベル付け・順序付け
- **連携可能** — このスキルの出力を隣接スキルに渡せる（セクション8参照）

---

## 7. ベストプラクティス

- まずは小さな現実的な入力でワークフローを検証してから本番データに広げる
- このガイドと並行して `skills/action-status-updater/SKILL.md` を開く（こちらが正本）
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

- `skills/action-status-updater/references/integration_guide.md`
- `skills/action-status-updater/references/status_patterns.md`

**スクリプト:**

- `skills/action-status-updater/scripts/action_status_updater.py`
- `skills/action-status-updater/scripts/nl_parser.py`

**アセット:**

_(なし)_

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/meta/action-status-updater/' | relative_url }}) を参照してください。
