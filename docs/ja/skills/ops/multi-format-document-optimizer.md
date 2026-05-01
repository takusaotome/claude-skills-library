---
layout: default
title: "Multi-Format Document Optimizer"
grand_parent: 日本語
parent: 運用・ドキュメント
nav_order: 14
lang_peer: /en/skills/ops/multi-format-document-optimizer/
permalink: /ja/skills/ops/multi-format-document-optimizer/
---

# Multi-Format Document Optimizer
{: .no_toc }

docling-converter、imagemagick-expert、markdown-to-pdf を連携させる統合ドキュメント最適化スキル。入力形式を自動検出し、適切な変換パイプラインを適用、埋め込み画像を最適化、設定可能な品質プリセットで Web/印刷向けの出力を生成します。
{: .fs-6 .fw-300 }

<span class="badge badge-free">docling + ImageMagick + markdown-to-pdf</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/multi-format-document-optimizer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/multi-format-document-optimizer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

形式を検出してパイプライン（pdf_optimize / docx_to_pdf / pptx_to_pdf 等）にルーティング。4 つの品質プリセット — web（80%／96dpi／WebP）、print（95%／300dpi）、archive（90%／150dpi）、minimal（70%／72dpi）を提供。CLI コマンド analyze/convert/batch/optimize-images/verify、PyMuPDF による PDF 画像の抽出・再埋め込み、並列バッチワーカーをサポート。

---

## 2. 前提条件

- Python 3.9+
- docling CLI (`pip install docling`)
- ImageMagick 7+
- fpdf2 / Playwright + chromium
- PyMuPDF (optional)

---

## 3. クイックスタート

```bash
# ローカルにスキルをインストール
make install SKILL=multi-format-document-optimizer

# または .skill パッケージを取得
curl -L -o multi-format-document-optimizer.skill https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/multi-format-document-optimizer.skill
```

その後、Claude Code 内でやりたいことを自然言語で記述するとスキルが自動起動します。トリガーとなるフレーズは「使用例」セクションを参照してください。

---

## 4. 進め方

スキルは `SKILL.md` に記載されたワークフローに従って動作します。主要ステージ：

1. **入力パース** — ユーザーリクエストと提供されたソースファイルを解釈
2. **コア処理** — スキル固有のドメインロジックを適用（リファレンスセクション参照）
3. **出力生成** — 後段で利用可能な構造化アーティファクト（Markdown／JSON／テンプレート）を生成

完全な手順は `skills/multi-format-document-optimizer/SKILL.md` を参照してください。

---

## 5. 使用例

- PPTX/DOCX を PDF に変換し Web 向けに埋め込み画像を縮小したい
- 複数フォーマット混在のディレクトリをバッチ処理したい
- Web／印刷／アーカイブの品質プリセットを CLI フラグ一つで切り替えたい
- 最適化後に出力品質を検証したい

---

## 6. 出力の読み方

スキルはテンプレートとリファレンスドキュメント（セクション10参照）の規約に従って構造化出力を生成します。出力は：

- **再現性** — 同じ入力＋同じテンプレートなら同じ出力構造
- **レビュー可能** — 各セクションが一貫してラベル付け・順序付け
- **連携可能** — このスキルの出力を隣接スキルに渡せる（セクション8参照）

---

## 7. ベストプラクティス

- まずは小さな現実的な入力でワークフローを検証してから本番データに広げる
- このガイドと並行して `skills/multi-format-document-optimizer/SKILL.md` を開く（こちらが正本）
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

- `skills/multi-format-document-optimizer/references/image_optimization_guide.md`
- `skills/multi-format-document-optimizer/references/pipeline_guide.md`

**スクリプト:**

- `skills/multi-format-document-optimizer/scripts/document_optimizer.py`

**アセット:**

_(なし)_

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/ops/multi-format-document-optimizer/' | relative_url }}) を参照してください。
