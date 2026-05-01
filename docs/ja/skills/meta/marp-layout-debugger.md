---
layout: default
title: "MARP Layout Debugger"
grand_parent: 日本語
parent: メタ・品質
nav_order: 28
lang_peer: /en/skills/meta/marp-layout-debugger/
permalink: /ja/skills/meta/marp-layout-debugger/
---

# MARP Layout Debugger
{: .no_toc }

MARP スライドのレイアウト問題（空白の不具合、ボックス整列、箇条書きフォーマット、CSS レンダリングの不一致）を診断・修正するスキル。MARP スライドの視覚的レイアウト問題や CSS 最適化に有用です。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/marp-layout-debugger.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/marp-layout-debugger){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

MARP ソースをレイアウト問題（空白、整列、箇条書き/溢れ）について解析し、CSS 修正カタログとレイアウトパターン参照から修正案を提示、Before/After を示す差分レポートを出力します。新規作成ではなく既存デッキの修復に特化しています。

---

## 2. 前提条件

- Python 3.9+
- MARP CLI (optional, for rendering)
- No API keys required

---

## 3. クイックスタート

```bash
# ローカルにスキルをインストール
make install SKILL=marp-layout-debugger

# または .skill パッケージを取得
curl -L -o marp-layout-debugger.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/marp-layout-debugger.skill
```

その後、Claude Code 内でやりたいことを自然言語で記述するとスキルが自動起動します。トリガーとなるフレーズは「使用例」セクションを参照してください。

---

## 4. 進め方

スキルは `SKILL.md` に記載されたワークフローに従って動作します。主要ステージ：

1. **入力パース** — ユーザーリクエストと提供されたソースファイルを解釈
2. **コア処理** — スキル固有のドメインロジックを適用（リファレンスセクション参照）
3. **出力生成** — 後段で利用可能な構造化アーティファクト（Markdown／JSON／テンプレート）を生成

完全な手順は `skills/marp-layout-debugger/SKILL.md` を参照してください。

---

## 5. 使用例

- MARP スライドに変な空白、溢れ、整列問題がある
- 自動生成された MARP デッキ（ジェネレータ出力等）を整える
- 特定の MARP レイアウトパターン向け CSS 修正レシピが欲しい
- 提案された CSS 変更を Before/After diff でレビューしたい

---

## 6. 出力の読み方

スキルはテンプレートとリファレンスドキュメント（セクション10参照）の規約に従って構造化出力を生成します。出力は：

- **再現性** — 同じ入力＋同じテンプレートなら同じ出力構造
- **レビュー可能** — 各セクションが一貫してラベル付け・順序付け
- **連携可能** — このスキルの出力を隣接スキルに渡せる（セクション8参照）

---

## 7. ベストプラクティス

- まずは小さな現実的な入力でワークフローを検証してから本番データに広げる
- このガイドと並行して `skills/marp-layout-debugger/SKILL.md` を開く（こちらが正本）
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

- `skills/marp-layout-debugger/references/css-fix-catalog.md`
- `skills/marp-layout-debugger/references/marp-layout-patterns.md`

**スクリプト:**

- `skills/marp-layout-debugger/scripts/analyze_marp_layout.py`
- `skills/marp-layout-debugger/scripts/fix_marp_layout.py`
- `skills/marp-layout-debugger/scripts/generate_diff_report.py`

**アセット:**

_(なし)_

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/meta/marp-layout-debugger/' | relative_url }}) を参照してください。
